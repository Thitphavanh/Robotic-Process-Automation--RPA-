from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.cache import cache
import json
import os
import threading
import time

from .models import RPATask, TaskLog, NewsArticle, DailyReport, NewsSource
from .rpa_runner import run_rpa_task
from .tasks import scrape_all_news, generate_daily_report, send_daily_report


# ========== Dashboard & List Views ==========


def dashboard(request):
    """หน้า Dashboard หลัก"""
    tasks = RPATask.objects.all()

    # สถิติ
    stats = {
        "total": tasks.count(),
        "pending": tasks.filter(status="pending").count(),
        "running": tasks.filter(status="running").count(),
        "completed": tasks.filter(status="completed").count(),
        "failed": tasks.filter(status="failed").count(),
    }

    # Tasks ล่าสุด
    recent_tasks = tasks[:10]

    context = {
        "stats": stats,
        "recent_tasks": recent_tasks,
    }
    return render(request, "rpa_bot/dashboard.html", context)


def task_list(request):
    """หน้ารายการ Tasks ทั้งหมด"""
    tasks = RPATask.objects.all()

    # Filter
    status_filter = request.GET.get("status")
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    task_type_filter = request.GET.get("task_type")
    if task_type_filter:
        tasks = tasks.filter(task_type=task_type_filter)

    # Search
    search_query = request.GET.get("search")
    if search_query:
        tasks = tasks.filter(name__icontains=search_query)

    # Pagination
    paginator = Paginator(tasks, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "status_choices": RPATask.STATUS_CHOICES,
        "task_type_choices": RPATask.TASK_TYPE_CHOICES,
    }
    return render(request, "rpa_bot/task_list.html", context)


# ========== CRUD Operations ==========


def task_create(request):
    """สร้าง Task ใหม่"""
    if request.method == "POST":
        try:
            task = RPATask.objects.create(
                name=request.POST.get("name"),
                description=request.POST.get("description"),
                task_type=request.POST.get("task_type", "google_search"),
                url=request.POST.get("url", "https://www.google.com"),
                keyword=request.POST.get("keyword"),
                delay_seconds=int(request.POST.get("delay_seconds", 3)),
                max_retries=int(request.POST.get("max_retries", 3)),
                created_by=request.user if request.user.is_authenticated else None,
            )
            messages.success(request, f'สร้าง Task "{task.name}" สำเร็จ!')
            return redirect("task_detail", slug=task.slug)
        except Exception as e:
            messages.error(request, f"เกิดข้อผิดพลาด: {str(e)}")

    context = {
        "task_type_choices": RPATask.TASK_TYPE_CHOICES,
    }
    return render(request, "rpa_bot/task_form.html", context)


def task_detail(request, slug):
    """รายละเอียด Task"""
    task = get_object_or_404(RPATask, slug=slug)
    logs = task.logs.all()[:50]

    context = {
        "task": task,
        "logs": logs,
    }
    return render(request, "rpa_bot/task_detail.html", context)


def task_update(request, slug):
    """แก้ไข Task"""
    task = get_object_or_404(RPATask, slug=slug)

    if request.method == "POST":
        try:
            task.name = request.POST.get("name")
            task.description = request.POST.get("description")
            task.task_type = request.POST.get("task_type")
            task.url = request.POST.get("url")
            task.keyword = request.POST.get("keyword")
            task.delay_seconds = int(request.POST.get("delay_seconds", 3))
            task.max_retries = int(request.POST.get("max_retries", 3))
            task.save()

            messages.success(request, f'อัพเดท Task "{task.name}" สำเร็จ!')
            return redirect("task_detail", slug=task.slug)
        except Exception as e:
            messages.error(request, f"เกิดข้อผิดพลาด: {str(e)}")

    context = {
        "task": task,
        "task_type_choices": RPATask.TASK_TYPE_CHOICES,
    }
    return render(request, "rpa_bot/task_form.html", context)


def task_delete(request, slug):
    """ลบ Task"""
    task = get_object_or_404(RPATask, slug=slug)

    if request.method == "POST":
        task_name = task.name
        task.delete()
        messages.success(request, f'ลบ Task "{task_name}" สำเร็จ!')
        return redirect("task_list")

    return render(request, "rpa_bot/task_confirm_delete.html", {"task": task})


# ========== Task Execution ==========


def task_run(request, slug):
    """รัน Task"""
    task = get_object_or_404(RPATask, slug=slug)

    # ตรวจสอบสถานะ
    if task.status == "running":
        messages.warning(request, "Task นี้กำลังทำงานอยู่แล้ว")
        return redirect("task_detail", slug=slug)

    # รันใน Background Thread
    def run_in_background():
        try:
            run_rpa_task(task)
        except Exception as e:
            task.mark_as_failed(str(e))

    thread = threading.Thread(target=run_in_background)
    thread.daemon = True
    thread.start()

    messages.info(request, f'เริ่มรัน Task "{task.name}" แล้ว')
    return redirect("task_detail", slug=slug)


def task_stop(request, slug):
    """หยุด Task (ยังไม่ได้ implement การหยุดจริง)"""
    task = get_object_or_404(RPATask, slug=slug)

    if task.status == "running":
        # TODO: Implement actual stopping mechanism
        task.status = "pending"
        task.save()
        messages.warning(request, f'หยุด Task "{task.name}" แล้ว')
    else:
        messages.info(request, "Task ไม่ได้กำลังทำงาน")

    return redirect("task_detail", slug=slug)


# ========== API Endpoints ==========


@require_http_methods(["GET"])
def api_task_status(request, slug):
    """API: ดูสถานะ Task"""
    task = get_object_or_404(RPATask, slug=slug)

    data = {
        "id": task.id,
        "name": task.name,
        "slug": task.slug,
        "status": task.status,
        "status_display": task.get_status_display(),
        "progress": calculate_progress(task),
        "screenshot_path": task.screenshot_path,
        "error_message": task.error_message,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
        "started_at": task.started_at.isoformat() if task.started_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "duration": task.duration,
    }

    return JsonResponse(data)


@require_http_methods(["GET"])
def api_task_logs(request, slug):
    """API: ดู Logs ของ Task"""
    task = get_object_or_404(RPATask, slug=slug)
    logs = task.logs.all()[:50]

    data = {
        "task_id": task.id,
        "task_slug": task.slug,
        "logs": [
            {
                "level": log.level,
                "message": log.message,
                "created_at": log.created_at.isoformat(),
            }
            for log in logs
        ],
    }

    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["POST"])
def api_task_create(request):
    """API: สร้าง Task ใหม่"""
    try:
        data = json.loads(request.body)

        task = RPATask.objects.create(
            name=data.get("name"),
            description=data.get("description", ""),
            task_type=data.get("task_type", "google_search"),
            url=data.get("url", "https://www.google.com"),
            keyword=data.get("keyword", ""),
            delay_seconds=data.get("delay_seconds", 3),
            max_retries=data.get("max_retries", 3),
        )

        return JsonResponse(
            {"success": True, "task_id": task.id, "message": "สร้าง Task สำเร็จ"}
        )

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_task_run(request, slug):
    """API: รัน Task"""
    task = get_object_or_404(RPATask, slug=slug)

    if task.status == "running":
        return JsonResponse(
            {"success": False, "message": "Task กำลังทำงานอยู่แล้ว"}, status=400
        )

    # รันใน Background
    def run_in_background():
        try:
            run_rpa_task(task)
        except Exception as e:
            task.mark_as_failed(str(e))

    thread = threading.Thread(target=run_in_background)
    thread.daemon = True
    thread.start()

    return JsonResponse({"success": True, "message": "เริ่มรัน Task แล้ว", "slug": task.slug})


# ========== Helper Functions ==========


def calculate_progress(task):
    """คำนวณ progress ของ Task"""
    if task.status == "completed":
        return 100
    elif task.status == "failed":
        return 0
    elif task.status == "running":
        # TODO: Implement actual progress tracking
        return 50
    else:
        return 0


# ========== News Intelligence Views ==========


def news_dashboard(request):
    """หน้า Dashboard ข่าว"""
    from datetime import date, timedelta

    # รายงานล่าสุด
    latest_report = DailyReport.objects.filter(is_completed=True).first()

    # ข่าววันนี้
    today = date.today()
    today_articles = NewsArticle.objects.filter(published_at__date=today)

    # สถิติตามหมวด - จัดกลุ่มตามประเภท
    stock_categories = [
        ('stock_thai', 'หุ้นไทย'),
        ('stock_us', 'หุ้นอเมริกา'),
        ('stock_europe', 'หุ้นยุโรป'),
        ('stock_china', 'หุ้นจีน'),
    ]

    other_categories = [
        ('crypto', 'Bitcoin/Crypto'),
        ('gold', 'ราคาทองคำ'),
        ('tech_ai', 'Technology AI'),
        ('tech_hardware', 'Hardware'),
        ('tech_software', 'Software'),
        ('football', 'Football'),
        ('ev_car', 'EV Car'),
        ('rocket_space', 'Rocket & Space'),
    ]

    stock_stats = []
    for category_code, category_name in stock_categories:
        count = today_articles.filter(source__category=category_code).count()
        stock_stats.append(
            {"code": category_code, "name": category_name, "count": count}
        )

    other_stats = []
    for category_code, category_name in other_categories:
        count = today_articles.filter(source__category=category_code).count()
        other_stats.append(
            {"code": category_code, "name": category_name, "count": count}
        )

    # ข่าวล่าสุด
    recent_articles = NewsArticle.objects.all()[:20]

    context = {
        "latest_report": latest_report,
        "today_articles_count": today_articles.count(),
        "stock_stats": stock_stats,
        "other_stats": other_stats,
        "recent_articles": recent_articles,
    }

    return render(request, "rpa_bot/news_dash.html", context)


def news_articles(request):
    """หน้ารายการข่าวทั้งหมด"""
    articles = NewsArticle.objects.all()

    # Filter by category
    category_filter = request.GET.get("category")
    if category_filter:
        articles = articles.filter(source__category=category_filter)

    # Search
    search_query = request.GET.get("search")
    if search_query:
        articles = articles.filter(title__icontains=search_query)

    # Pagination
    paginator = Paginator(articles, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "category_choices": NewsSource.CATEGORY_CHOICES,
        "selected_category": category_filter,
    }

    return render(request, "rpa_bot/news_articles.html", context)


def news_article_detail(request, slug):
    """หน้ารายละเอียดข่าว"""
    article = get_object_or_404(NewsArticle, slug=slug)

    # สร้าง AI Summary ถ้ายังไม่มี
    if not article.ai_summary:
        from .ai_summarizer import AISummarizerService
        summarizer = AISummarizerService()
        summarizer.summarize_article(article)
        article.refresh_from_db()

    # ข่าวที่เกี่ยวข้อง (จากหมวดเดียวกัน)
    related_articles = NewsArticle.objects.filter(
        source__category=article.source.category
    ).exclude(slug=slug).order_by('-published_at')[:5]

    context = {
        "article": article,
        "related_articles": related_articles,
    }

    return render(request, "rpa_bot/news_article_detail.html", context)


def generate_article_analysis(request, slug):
    """สร้างการวิเคราะห์แบบละเอียดด้วย Gemini AI"""
    if request.method != "POST":
        return redirect("news_article_detail", slug=slug)

    article = get_object_or_404(NewsArticle, slug=slug)

    try:
        from .ai_summarizer import AISummarizerService

        # สร้างการวิเคราะห์
        summarizer = AISummarizerService()
        analysis_report = summarizer.generate_detailed_analysis(article)

        # บันทึกลงฐานข้อมูล
        article.detailed_analysis = analysis_report
        article.save()

        messages.success(request, "สร้างการวิเคราะห์เสร็จสมบูรณ์!")

    except Exception as e:
        messages.error(request, f"เกิดข้อผิดพลาด: {str(e)}")

    return redirect("news_article_detail", slug=slug)


def daily_reports(request):
    """หน้ารายการรายงานประจำวัน"""
    reports = DailyReport.objects.filter(is_completed=True)

    # Pagination
    paginator = Paginator(reports, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "rpa_bot/daily_reports.html", context)


def daily_report_detail(request, slug):
    """หน้ารายละเอียดรายงานประจำวัน"""
    report = get_object_or_404(DailyReport, slug=slug)

    context = {
        "report": report,
    }

    return render(request, "rpa_bot/daily_report_detail.html", context)


def trigger_news_scrape(request):
    """Trigger ดึงข้อมูลข่าวด้วยตัวเอง - แบบ Background"""
    if request.method == "POST":
        # ตรวจสอบว่ากำลัง scrape อยู่หรือไม่
        if cache.get('news_scraping_status') == 'running':
            messages.warning(request, "กำลังดึงข้อมูลข่าวอยู่แล้ว กรุณารอสักครู่...")
            return redirect("news_dashboard")

        # เริ่ม scraping ใน background
        def run_scraping_in_background():
            try:
                from .news_scraper import scrape_all_news_sources

                # ตั้งสถานะเป็น running
                cache.set('news_scraping_status', 'running', 600)  # 10 minutes timeout
                cache.set('news_scraping_progress', 0, 600)

                # ดึงข้อมูล
                result = scrape_all_news_sources()

                # บันทึกผลลัพธ์
                cache.set('news_scraping_status', 'completed', 600)
                cache.set('news_scraping_result', result, 600)
                cache.set('news_scraping_progress', 100, 600)

            except Exception as e:
                cache.set('news_scraping_status', 'failed', 600)
                cache.set('news_scraping_error', str(e), 600)

        # รันใน background thread
        thread = threading.Thread(target=run_scraping_in_background)
        thread.daemon = True
        thread.start()

        messages.info(request, "เริ่มดึงข้อมูลข่าวแล้ว! กำลังประมวลผล...")
        return redirect("news_dashboard")

    return render(request, "rpa_bot/trigger_scrape.html")


def trigger_generate_report(request):
    """Trigger สร้างรายงานด้วยตัวเอง"""
    if request.method == "POST":
        try:
            # รันแบบ synchronous ทันที (ไม่ใช้ Celery)
            from .ai_summarizer import AISummarizerService
            from datetime import date

            summarizer = AISummarizerService()
            report = summarizer.generate_daily_report(date.today())

            if report:
                messages.success(request, "สร้างรายงานเรียบร้อยแล้ว!")
            else:
                messages.warning(request, "ไม่มีข่าวใหม่สำหรับสร้างรายงาน")
        except Exception as e:
            messages.error(request, f"เกิดข้อผิดพลาด: {str(e)}")

        return redirect("news_dashboard")

    return render(request, "rpa_bot/trigger_report.html")


# ========== News API Endpoints ==========


@require_http_methods(["GET"])
def api_news_stats(request):
    """API: สถิติข่าว"""
    from datetime import date, timedelta

    today = date.today()
    today_articles = NewsArticle.objects.filter(published_at__date=today)

    # สถิติตามหมวด
    categories = {}
    for category_code, category_name in NewsSource.CATEGORY_CHOICES:
        count = today_articles.filter(source__category=category_code).count()
        categories[category_code] = {"name": category_name, "count": count}

    data = {
        "total_today": today_articles.count(),
        "categories": categories,
        "latest_update": timezone.now().isoformat(),
    }

    return JsonResponse(data)


@require_http_methods(["GET"])
def api_latest_report(request):
    """API: รายงานล่าสุด"""
    report = DailyReport.objects.filter(is_completed=True).first()

    if not report:
        return JsonResponse({"success": False, "message": "ยังไม่มีรายงาน"}, status=404)

    data = {
        "success": True,
        "report": {
            "id": report.id,
            "report_date": report.report_date.isoformat(),
            "is_sent": report.is_sent,
            "full_report": report.full_report,
            "created_at": report.created_at.isoformat(),
        },
    }

    return JsonResponse(data)


@require_http_methods(["GET"])
def api_scraping_status(request):
    """API: ตรวจสอบสถานะการ scrape ข่าว"""
    status = cache.get('news_scraping_status', 'idle')
    progress = cache.get('news_scraping_progress', 0)
    result = cache.get('news_scraping_result', {})
    error = cache.get('news_scraping_error', None)

    data = {
        "status": status,  # 'idle', 'running', 'completed', 'failed'
        "progress": progress,
        "result": result if status == 'completed' else None,
        "error": error if status == 'failed' else None,
        "timestamp": timezone.now().isoformat()
    }

    return JsonResponse(data)


# ========== AI Agent Dashboard Views ==========


def ai_agent_dashboard(request):
    """หน้า AI Agent Dashboard"""
    return render(request, "rpa_bot/ai_agent_dashboard.html")


@require_http_methods(["GET"])
def api_ai_agent_status(request):
    """API: สถานะ AI Agent"""
    data = {
        "status": "Active",
        "stocks_discovered": 40,  # 10 per market x 4 markets
        "cryptos_discovered": 10,
        "avg_discovery_time": "2.3s",
        "last_discovery": timezone.now().isoformat(),
        "api_status": "connected",
        "model": "claude-3-5-sonnet-20241022"
    }
    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["POST"])
def api_ai_agent_discover_stocks(request):
    """API: ทดสอบ Stock Discovery ด้วย AI Agent"""
    try:
        data = json.loads(request.body)
        market = data.get('market', 'thai')
        limit = data.get('limit', 10)

        from .ai_agent import get_ai_agent

        agent = get_ai_agent()
        stocks = agent.discover_top_stocks(market=market, limit=limit)

        return JsonResponse({
            "success": True,
            "market": market,
            "stocks": stocks,
            "count": len(stocks),
            "timestamp": timezone.now().isoformat()
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_ai_agent_discover_crypto(request):
    """API: ทดสอบ Crypto Discovery ด้วย AI Agent"""
    try:
        data = json.loads(request.body)
        limit = data.get('limit', 10)

        from .ai_agent import get_ai_agent

        agent = get_ai_agent()
        cryptos = agent.discover_top_crypto(limit=limit)

        return JsonResponse({
            "success": True,
            "cryptos": cryptos,
            "count": len(cryptos),
            "timestamp": timezone.now().isoformat()
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_ai_agent_sentiment(request):
    """API: วิเคราะห์ Market Sentiment ด้วย AI Agent"""
    try:
        data = json.loads(request.body)
        market = data.get('market', 'us')

        from .ai_agent import get_ai_agent

        agent = get_ai_agent()
        sentiment = agent.analyze_market_sentiment(market=market)

        return JsonResponse({
            "success": True,
            "market": market,
            **sentiment,
            "timestamp": timezone.now().isoformat()
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)
