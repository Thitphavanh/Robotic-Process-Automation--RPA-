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

from .models import RPATask, TaskLog, NewsArticle, DailyReport, NewsSource, ProductCategory, ProductBrand, TrackedProduct, PriceHistory, DocSection
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

    # ข่าววันนี้ (ใช้ scraped_at เพื่อให้ได้ข่าวที่ scrape ในวันนี้)
    today = date.today()
    today_articles = NewsArticle.objects.filter(scraped_at__date=today)

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
    # Support both ID (numeric) and slug
    if slug.isdigit():
        report = get_object_or_404(DailyReport, id=int(slug))
    else:
        report = get_object_or_404(DailyReport, slug=slug)

    context = {
        "report": report,
    }

    return render(request, "rpa_bot/daily_report_detail.html", context)


def trigger_news_scrape(request):
    """Trigger ดึงข้อมูลข่าว + สร้างรายงาน + ส่ง Telegram ทันที"""
    if request.method == "POST":
        # ตรวจสอบว่ากำลัง scrape อยู่หรือไม่
        if cache.get('news_scraping_status') == 'running':
            messages.warning(request, "กำลังดึงข้อมูลข่าวอยู่แล้ว กรุณารอสักครู่...")
            return redirect("news_dashboard")

        # เริ่ม scraping + generate + send ใน background
        def run_scraping_in_background():
            try:
                from .ai_summarizer import AISummarizerService
                from datetime import date

                # ตั้งสถานะเป็น running
                cache.set('news_scraping_status', 'running', 600)  # 10 minutes timeout
                cache.set('news_scraping_progress', 0, 600)

                # Step 1: ดึงข้อมูลข่าว
                cache.set('news_scraping_progress', 10, 600)
                scrape_result = scrape_all_news()  # ใช้ task แทน

                # Step 2: สร้างรายงาน
                cache.set('news_scraping_progress', 60, 600)
                generate_result = generate_daily_report()

                # Step 3: ส่ง Telegram
                cache.set('news_scraping_progress', 80, 600)
                send_result = send_daily_report()

                # บันทึกผลลัพธ์
                cache.set('news_scraping_status', 'completed', 600)
                cache.set('news_scraping_result', {
                    'scrape': scrape_result,
                    'generate': generate_result,
                    'send': send_result
                }, 600)
                cache.set('news_scraping_progress', 100, 600)

            except Exception as e:
                cache.set('news_scraping_status', 'failed', 600)
                cache.set('news_scraping_error', str(e), 600)

        # รันใน background thread
        thread = threading.Thread(target=run_scraping_in_background)
        thread.daemon = True
        thread.start()

        messages.info(request, "เริ่มดึงข้อมูลข่าวและส่งรายงานไปยัง Telegram แล้ว! กำลังประมวลผล...")
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
    today_articles = NewsArticle.objects.filter(scraped_at__date=today)

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


# ========== E-Commerce Tracking Views ==========


def ecommerce_dashboard(request):
    """หน้า E-Commerce Dashboard"""
    # สถิติ
    total_tracked = TrackedProduct.objects.filter(is_active=True).count()
    active_alerts = TrackedProduct.objects.filter(enable_price_alert=True, is_active=True).count()
    categories_count = ProductCategory.objects.filter(is_active=True).count()
    brands_count = ProductBrand.objects.filter(is_active=True).count()

    # สินค้าที่ติดตาม (ล่าสุด 20 รายการ)
    tracked_products = TrackedProduct.objects.filter(is_active=True).select_related(
        'category', 'brand'
    ).order_by('-created_at')[:20]

    # Price alerts ที่กำลังทำงาน
    price_alerts = TrackedProduct.objects.filter(
        enable_price_alert=True,
        is_active=True,
        alert_sent=False
    ).select_related('category', 'brand')[:10]

    # สินค้าที่ราคาลดล่าสุด (Top 10)
    recently_reduced = TrackedProduct.objects.filter(
        is_active=True,
        discount_percent__gt=0
    ).select_related('category', 'brand').order_by('-discount_percent')[:10]

    context = {
        "stats": {
            "total_tracked": total_tracked,
            "active_alerts": active_alerts,
            "categories_count": categories_count,
            "brands_count": brands_count,
        },
        "tracked_products": tracked_products,
        "price_alerts": price_alerts,
        "recently_reduced": recently_reduced,
    }

    return render(request, "rpa_bot/ecommerce_dashboard.html", context)


def ecommerce_categories(request):
    """หน้าจัดการหมวดหมู่สินค้า"""
    categories = ProductCategory.objects.all().order_by('name')

    # Search
    search_query = request.GET.get("search")
    if search_query:
        categories = categories.filter(name__icontains=search_query)

    # Pagination
    paginator = Paginator(categories, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "rpa_bot/ecommerce_categories.html", context)


def ecommerce_brands(request):
    """หน้าจัดการแบรนด์"""
    brands = ProductBrand.objects.all().order_by('name')

    # Search
    search_query = request.GET.get("search")
    if search_query:
        brands = brands.filter(name__icontains=search_query)

    # Pagination
    paginator = Paginator(brands, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }

    return render(request, "rpa_bot/ecommerce_brands.html", context)


def tracked_product_detail(request, pk):
    """หน้ารายละเอียดสินค้าที่ติดตาม"""
    product = get_object_or_404(TrackedProduct, pk=pk)

    # ประวัติราคา (30 วันล่าสุด)
    price_history = product.price_history.all()[:30]

    # คำนวณสถิติ
    if price_history:
        prices = [float(h.price) for h in price_history]
        avg_price = sum(prices) / len(prices)
        price_change_30d = ((float(product.current_price) - prices[-1]) / prices[-1] * 100) if prices[-1] > 0 else 0
    else:
        avg_price = float(product.current_price) if product.current_price else 0
        price_change_30d = 0

    context = {
        "product": product,
        "price_history": price_history,
        "avg_price": avg_price,
        "price_change_30d": price_change_30d,
    }

    return render(request, "rpa_bot/tracked_product_detail.html", context)


# ========== E-Commerce API Endpoints ==========


@require_http_methods(["GET"])
def api_ecommerce_categories(request):
    """API: รายการหมวดหมู่สินค้า"""
    categories = ProductCategory.objects.filter(is_active=True)

    data = {
        "success": True,
        "categories": [
            {
                "id": cat.id,
                "name": cat.name,
                "slug": cat.slug,
                "description": cat.description,
                "keywords": cat.keywords,
                "product_count": cat.tracked_products.filter(is_active=True).count(),
            }
            for cat in categories
        ],
        "count": categories.count(),
    }

    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["POST"])
def api_ecommerce_category_create(request):
    """API: สร้างหมวดหมู่สินค้าใหม่"""
    try:
        data = json.loads(request.body)

        category = ProductCategory.objects.create(
            name=data.get("name"),
            description=data.get("description", ""),
            keywords=data.get("keywords", ""),
        )

        return JsonResponse({
            "success": True,
            "category": {
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
            },
            "message": "สร้างหมวดหมู่สำเร็จ"
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@require_http_methods(["GET"])
def api_ecommerce_brands(request):
    """API: รายการแบรนด์"""
    brands = ProductBrand.objects.filter(is_active=True)

    data = {
        "success": True,
        "brands": [
            {
                "id": brand.id,
                "name": brand.name,
                "slug": brand.slug,
                "logo_url": brand.logo_url,
                "website": brand.website,
                "product_count": brand.tracked_products.filter(is_active=True).count(),
            }
            for brand in brands
        ],
        "count": brands.count(),
    }

    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["POST"])
def api_ecommerce_brand_create(request):
    """API: สร้างแบรนด์ใหม่"""
    try:
        data = json.loads(request.body)

        brand = ProductBrand.objects.create(
            name=data.get("name"),
            logo_url=data.get("logo_url", ""),
            website=data.get("website", ""),
        )

        return JsonResponse({
            "success": True,
            "brand": {
                "id": brand.id,
                "name": brand.name,
                "slug": brand.slug,
            },
            "message": "สร้างแบรนด์สำเร็จ"
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@require_http_methods(["GET"])
def api_ecommerce_tracked_products(request):
    """API: รายการสินค้าที่ติดตาม"""
    products = TrackedProduct.objects.filter(is_active=True).select_related(
        'category', 'brand'
    )

    # Filter by platform
    platform = request.GET.get('platform')
    if platform:
        products = products.filter(platform=platform)

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Filter by brand
    brand_id = request.GET.get('brand')
    if brand_id:
        products = products.filter(brand_id=brand_id)

    # Limit
    limit = int(request.GET.get('limit', 50))
    products = products[:limit]

    data = {
        "success": True,
        "products": [
            {
                "id": p.id,
                "platform": p.platform,
                "title": p.title,
                "product_url": p.product_url,
                "current_price": float(p.current_price) if p.current_price else None,
                "original_price": float(p.original_price) if p.original_price else None,
                "discount_percent": float(p.discount_percent) if p.discount_percent else None,
                "lowest_price": float(p.lowest_price) if p.lowest_price else None,
                "highest_price": float(p.highest_price) if p.highest_price else None,
                "image_url": p.image_url,
                "rating": float(p.rating) if p.rating else None,
                "reviews_count": p.reviews_count,
                "sold_count": p.sold_count,
                "category": p.category.name if p.category else None,
                "brand": p.brand.name if p.brand else None,
                "enable_price_alert": p.enable_price_alert,
                "target_price": float(p.target_price) if p.target_price else None,
                "is_available": p.is_available,
                "last_checked_at": p.last_checked_at.isoformat() if p.last_checked_at else None,
                "created_at": p.created_at.isoformat(),
            }
            for p in products
        ],
        "count": products.count(),
    }

    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["POST"])
def api_ecommerce_track_url(request):
    """API: เพิ่มสินค้าจาก URL เพื่อติดตาม"""
    try:
        data = json.loads(request.body)
        product_url = data.get("product_url")

        if not product_url:
            return JsonResponse({"success": False, "error": "กรุณาระบุ URL"}, status=400)

        # Import ProductScraperService
        from .product_scraper import ProductScraperService

        scraper = ProductScraperService()

        # ตรวจสอบ platform
        platform = scraper.detect_platform(product_url)
        if not platform:
            return JsonResponse({
                "success": False,
                "error": "ไม่รองรับ URL นี้ กรุณาใช้ URL จาก Lazada, Shopee, TikTok, Taobao, Tmall, Pinduoduo, 1688, Alibaba, Amazon"
            }, status=400)

        # ดึงข้อมูล category และ brand (ถ้ามี)
        category = None
        if data.get("category_id"):
            category = ProductCategory.objects.filter(id=data.get("category_id")).first()

        brand = None
        if data.get("brand_id"):
            brand = ProductBrand.objects.filter(id=data.get("brand_id")).first()

        user = request.user if request.user.is_authenticated else None

        # สร้างหรืออัพเดท TrackedProduct
        tracked_product = scraper.create_or_update_tracked_product(
            product_url=product_url,
            category=category,
            brand=brand,
            user=user
        )

        # ตั้งค่า price alert (ถ้ามี)
        if data.get("enable_price_alert") and data.get("target_price"):
            tracked_product.enable_price_alert = True
            tracked_product.target_price = data.get("target_price")
            tracked_product.alert_sent = False
            tracked_product.save()

        return JsonResponse({
            "success": True,
            "product": {
                "id": tracked_product.id,
                "platform": tracked_product.platform,
                "title": tracked_product.title,
                "current_price": float(tracked_product.current_price) if tracked_product.current_price else None,
                "product_url": tracked_product.product_url,
            },
            "message": "เพิ่มสินค้าเรียบร้อยแล้ว"
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_ecommerce_update_prices(request):
    """API: อัพเดทราคาสินค้าทั้งหมด"""
    try:
        from .product_scraper import ProductScraperService

        # ตั้งสถานะเป็น running
        if cache.get('ecommerce_update_status') == 'running':
            return JsonResponse({
                "success": False,
                "message": "กำลังอัพเดทราคาอยู่แล้ว กรุณารอสักครู่..."
            }, status=400)

        # รันใน background thread
        def run_update_in_background():
            try:
                cache.set('ecommerce_update_status', 'running', 600)
                cache.set('ecommerce_update_progress', 0, 600)

                scraper = ProductScraperService()
                result = scraper.update_all_tracked_products()

                cache.set('ecommerce_update_status', 'completed', 600)
                cache.set('ecommerce_update_result', result, 600)
                cache.set('ecommerce_update_progress', 100, 600)

            except Exception as e:
                cache.set('ecommerce_update_status', 'failed', 600)
                cache.set('ecommerce_update_error', str(e), 600)

        thread = threading.Thread(target=run_update_in_background)
        thread.daemon = True
        thread.start()

        return JsonResponse({
            "success": True,
            "message": "เริ่มอัพเดทราคาสินค้าแล้ว"
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@require_http_methods(["GET"])
def api_ecommerce_update_status(request):
    """API: ตรวจสอบสถานะการอัพเดทราคา"""
    status = cache.get('ecommerce_update_status', 'idle')
    progress = cache.get('ecommerce_update_progress', 0)
    result = cache.get('ecommerce_update_result', {})
    error = cache.get('ecommerce_update_error', None)

    data = {
        "status": status,  # 'idle', 'running', 'completed', 'failed'
        "progress": progress,
        "result": result if status == 'completed' else None,
        "error": error if status == 'failed' else None,
        "timestamp": timezone.now().isoformat()
    }

    return JsonResponse(data)


@require_http_methods(["GET"])
def api_ecommerce_price_history(request, product_id):
    """API: ประวัติราคาของสินค้า"""
    try:
        product = TrackedProduct.objects.get(id=product_id)
        history = product.price_history.all()[:100]  # 100 รายการล่าสุด

        data = {
            "success": True,
            "product": {
                "id": product.id,
                "title": product.title,
                "platform": product.platform,
            },
            "history": [
                {
                    "price": float(h.price),
                    "original_price": float(h.original_price) if h.original_price else None,
                    "discount_percent": float(h.discount_percent) if h.discount_percent else None,
                    "stock_status": h.stock_status,
                    "recorded_at": h.recorded_at.isoformat(),
                }
                for h in history
            ],
            "count": history.count(),
        }

        return JsonResponse(data)

    except TrackedProduct.DoesNotExist:
        return JsonResponse({"success": False, "error": "ไม่พบสินค้า"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def api_ecommerce_product_update(request, product_id):
    """API: อัพเดทข้อมูลสินค้า"""
    try:
        product = TrackedProduct.objects.get(id=product_id)
        data = json.loads(request.body)

        # อัพเดทฟิลด์ที่อนุญาต
        if "enable_price_alert" in data:
            product.enable_price_alert = data["enable_price_alert"]
        if "target_price" in data:
            product.target_price = data["target_price"]
        if "is_active" in data:
            product.is_active = data["is_active"]
        if "category_id" in data:
            category = ProductCategory.objects.filter(id=data["category_id"]).first()
            product.category = category
        if "brand_id" in data:
            brand = ProductBrand.objects.filter(id=data["brand_id"]).first()
            product.brand = brand

        product.save()

        return JsonResponse({
            "success": True,
            "message": "อัพเดทสินค้าเรียบร้อยแล้ว",
            "product": {
                "id": product.id,
                "title": product.title,
                "enable_price_alert": product.enable_price_alert,
                "target_price": float(product.target_price) if product.target_price else None,
            }
        })

    except TrackedProduct.DoesNotExist:
        return JsonResponse({"success": False, "error": "ไม่พบสินค้า"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["DELETE"])
def api_ecommerce_product_delete(request, product_id):
    """API: ลบสินค้าที่ติดตาม"""
    try:
        product = TrackedProduct.objects.get(id=product_id)
        product_title = product.title
        product.delete()

        return JsonResponse({
            "success": True,
            "message": f"ลบสินค้า '{product_title}' เรียบร้อยแล้ว"
        })

    except TrackedProduct.DoesNotExist:
        return JsonResponse({"success": False, "error": "ไม่พบสินค้า"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@require_http_methods(["GET"])
def api_ecommerce_price_alerts(request):
    """API: รายการสินค้าที่มี Price Alert ทำงานอยู่"""
    alerts = TrackedProduct.objects.filter(
        enable_price_alert=True,
        is_active=True,
        alert_sent=False
    ).select_related('category', 'brand')

    # กรองเฉพาะที่ราคาถึง target แล้ว
    active_alerts = []
    for product in alerts:
        if product.target_price and product.current_price:
            if product.current_price <= product.target_price:
                active_alerts.append(product)

    data = {
        "success": True,
        "alerts": [
            {
                "id": p.id,
                "title": p.title,
                "platform": p.platform,
                "current_price": float(p.current_price),
                "target_price": float(p.target_price),
                "price_difference": float(p.target_price - p.current_price),
                "discount_percent": float(p.discount_percent) if p.discount_percent else 0,
                "product_url": p.product_url,
                "image_url": p.image_url,
                "created_at": p.created_at.isoformat(),
            }
            for p in active_alerts
        ],
        "count": len(active_alerts),
    }

    return JsonResponse(data)


# ========== E-Commerce Bulk Scraping API Endpoints ==========


@csrf_exempt
@require_http_methods(["POST"])
def api_ecommerce_scrape_category(request):
    """API: Scrape สินค้าตามหมวดหมู่ (Top 100)"""
    try:
        data = json.loads(request.body)
        platform = data.get("platform")
        category_id = data.get("category_id")
        limit = data.get("limit", 100)

        # Validate platform
        valid_platforms = ["lazada", "shopee", "tiktok", "taobao", "tmall", "pinduoduo", "jd", "1688", "alibaba", "aliexpress", "amazon"]
        if platform not in valid_platforms:
            return JsonResponse({
                "success": False,
                "error": f"Invalid platform. Choose from: {', '.join(valid_platforms)}"
            }, status=400)

        # Get category
        try:
            category = ProductCategory.objects.get(id=category_id)
        except ProductCategory.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": "Category not found"
            }, status=404)

        # Check if scraping is already running
        cache_key = f'bulk_scrape_category_{platform}_{category_id}'
        if cache.get(cache_key) == 'running':
            return JsonResponse({
                "success": False,
                "message": "Category scraping is already running for this platform/category"
            }, status=400)

        # Run scraping in background
        def run_scraping_in_background():
            try:
                from .product_scraper import ProductScraperService

                cache.set(cache_key, 'running', 600)
                cache.set(f'{cache_key}_progress', 0, 600)

                scraper = ProductScraperService()
                products = scraper.scrape_category_products(
                    platform=platform,
                    category=category,
                    limit=limit
                )

                cache.set(cache_key, 'completed', 600)
                cache.set(f'{cache_key}_result', {
                    'products_count': len(products),
                    'platform': platform,
                    'category': category.name
                }, 600)
                cache.set(f'{cache_key}_progress', 100, 600)

            except Exception as e:
                cache.set(cache_key, 'failed', 600)
                cache.set(f'{cache_key}_error', str(e), 600)

        thread = threading.Thread(target=run_scraping_in_background)
        thread.daemon = True
        thread.start()

        return JsonResponse({
            "success": True,
            "message": f"Started scraping {category.name} products from {platform}",
            "task_id": cache_key
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_ecommerce_scrape_brand(request):
    """API: Scrape สินค้าตามแบรนด์ (Top 100)"""
    try:
        data = json.loads(request.body)
        platform = data.get("platform")
        brand_id = data.get("brand_id")
        limit = data.get("limit", 100)

        # Validate platform
        valid_platforms = ["lazada", "shopee", "tiktok", "taobao", "tmall", "pinduoduo", "jd", "1688", "alibaba", "aliexpress", "amazon"]
        if platform not in valid_platforms:
            return JsonResponse({
                "success": False,
                "error": f"Invalid platform. Choose from: {', '.join(valid_platforms)}"
            }, status=400)

        # Get brand
        try:
            brand = ProductBrand.objects.get(id=brand_id)
        except ProductBrand.DoesNotExist:
            return JsonResponse({
                "success": False,
                "error": "Brand not found"
            }, status=404)

        # Check if scraping is already running
        cache_key = f'bulk_scrape_brand_{platform}_{brand_id}'
        if cache.get(cache_key) == 'running':
            return JsonResponse({
                "success": False,
                "message": "Brand scraping is already running for this platform/brand"
            }, status=400)

        # Run scraping in background
        def run_scraping_in_background():
            try:
                from .product_scraper import ProductScraperService

                cache.set(cache_key, 'running', 600)
                cache.set(f'{cache_key}_progress', 0, 600)

                scraper = ProductScraperService()
                products = scraper.scrape_brand_products(
                    platform=platform,
                    brand=brand,
                    limit=limit
                )

                cache.set(cache_key, 'completed', 600)
                cache.set(f'{cache_key}_result', {
                    'products_count': len(products),
                    'platform': platform,
                    'brand': brand.name
                }, 600)
                cache.set(f'{cache_key}_progress', 100, 600)

            except Exception as e:
                cache.set(cache_key, 'failed', 600)
                cache.set(f'{cache_key}_error', str(e), 600)

        thread = threading.Thread(target=run_scraping_in_background)
        thread.daemon = True
        thread.start()

        return JsonResponse({
            "success": True,
            "message": f"Started scraping {brand.name} products from {platform}",
            "task_id": cache_key
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_ecommerce_scrape_bestsellers(request):
    """API: Scrape สินค้าขายดี/ยอดนิยม (Top 100)"""
    try:
        data = json.loads(request.body)
        platform = data.get("platform")
        limit = data.get("limit", 100)

        # Validate platform
        valid_platforms = ["lazada", "shopee", "tiktok", "taobao", "tmall", "pinduoduo", "jd", "1688", "alibaba", "aliexpress", "amazon"]
        if platform not in valid_platforms:
            return JsonResponse({
                "success": False,
                "error": f"Invalid platform. Choose from: {', '.join(valid_platforms)}"
            }, status=400)

        # Check if scraping is already running
        cache_key = f'bulk_scrape_bestsellers_{platform}'
        if cache.get(cache_key) == 'running':
            return JsonResponse({
                "success": False,
                "message": "Best-sellers scraping is already running for this platform"
            }, status=400)

        # Run scraping in background
        def run_scraping_in_background():
            try:
                from .product_scraper import ProductScraperService

                cache.set(cache_key, 'running', 600)
                cache.set(f'{cache_key}_progress', 0, 600)

                scraper = ProductScraperService()
                products = scraper.scrape_best_selling(
                    platform=platform,
                    limit=limit
                )

                cache.set(cache_key, 'completed', 600)
                cache.set(f'{cache_key}_result', {
                    'products_count': len(products),
                    'platform': platform
                }, 600)
                cache.set(f'{cache_key}_progress', 100, 600)

            except Exception as e:
                cache.set(cache_key, 'failed', 600)
                cache.set(f'{cache_key}_error', str(e), 600)

        thread = threading.Thread(target=run_scraping_in_background)
        thread.daemon = True
        thread.start()

        return JsonResponse({
            "success": True,
            "message": f"Started scraping best-selling products from {platform}",
            "task_id": cache_key
        })

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)


@require_http_methods(["GET"])
def api_ecommerce_bulk_scrape_status(request):
    """API: ตรวจสอบสถานะการ Bulk Scrape"""
    task_id = request.GET.get('task_id')

    if not task_id:
        return JsonResponse({
            "success": False,
            "error": "task_id is required"
        }, status=400)

    status = cache.get(task_id, 'idle')
    progress = cache.get(f'{task_id}_progress', 0)
    result = cache.get(f'{task_id}_result', {})
    error = cache.get(f'{task_id}_error', None)

    data = {
        "success": True,
        "task_id": task_id,
        "status": status,  # 'idle', 'running', 'completed', 'failed'
        "progress": progress,
        "result": result if status == 'completed' else None,
        "error": error if status == 'failed' else None,
        "timestamp": timezone.now().isoformat()
    }

    return JsonResponse(data)


# ========== Documentation Views ==========


def docs_home(request):
    """หน้า Documentation หลัก"""
    return redirect('docs_section', section='overview')


def docs_section(request, section):
    """หน้า Documentation แต่ละส่วน - ใช้ข้อมูลจากฐานข้อมูล"""
    # ดึงข้อมูลจากฐานข้อมูล
    all_sections = DocSection.objects.filter(is_active=True).order_by('group', 'order', 'title')

    # จัดกลุ่ม sections ตาม group
    grouped_sections = {}
    for group_code, group_name in DocSection.SECTION_GROUP_CHOICES:
        sections_in_group = all_sections.filter(group=group_code)
        if sections_in_group.exists():
            grouped_sections[group_code] = {
                'name': group_name,
                'sections': sections_in_group
            }

    # หา section ปัจจุบัน พร้อม prefetch content blocks
    try:
        current_section = DocSection.objects.prefetch_related('content_blocks').get(slug=section, is_active=True)
    except DocSection.DoesNotExist:
        # ถ้าไม่เจอ redirect ไป overview หรือ section แรก
        first_section = all_sections.first()
        if first_section:
            return redirect('docs_section', section=first_section.slug)
        else:
            # ถ้าไม่มี section เลย แสดง error
            messages.error(request, "ยังไม่มีเอกสารในระบบ กรุณาเพิ่มเอกสารผ่าน Admin Panel")
            return redirect('dashboard')

    # ดึง content blocks ที่เปิดใช้งาน
    content_blocks = current_section.content_blocks.filter(is_active=True).order_by('order')

    context = {
        'grouped_sections': grouped_sections,
        'current_section': current_section,
        'current_section_key': section,
        'content_blocks': content_blocks,
    }

    return render(request, 'rpa_bot/docs/doc_template.html', context)
