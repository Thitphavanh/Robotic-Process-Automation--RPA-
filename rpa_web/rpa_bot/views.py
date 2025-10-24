from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator
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
            return redirect("task_detail", pk=task.pk)
        except Exception as e:
            messages.error(request, f"เกิดข้อผิดพลาด: {str(e)}")

    context = {
        "task_type_choices": RPATask.TASK_TYPE_CHOICES,
    }
    return render(request, "rpa_bot/task_form.html", context)


def task_detail(request, pk):
    """รายละเอียด Task"""
    task = get_object_or_404(RPATask, pk=pk)
    logs = task.logs.all()[:50]

    context = {
        "task": task,
        "logs": logs,
    }
    return render(request, "rpa_bot/task_detail.html", context)


def task_update(request, pk):
    """แก้ไข Task"""
    task = get_object_or_404(RPATask, pk=pk)

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
            return redirect("task_detail", pk=task.pk)
        except Exception as e:
            messages.error(request, f"เกิดข้อผิดพลาด: {str(e)}")

    context = {
        "task": task,
        "task_type_choices": RPATask.TASK_TYPE_CHOICES,
    }
    return render(request, "rpa_bot/task_form.html", context)


def task_delete(request, pk):
    """ลบ Task"""
    task = get_object_or_404(RPATask, pk=pk)

    if request.method == "POST":
        task_name = task.name
        task.delete()
        messages.success(request, f'ลบ Task "{task_name}" สำเร็จ!')
        return redirect("task_list")

    return render(request, "rpa_bot/task_confirm_delete.html", {"task": task})


# ========== Task Execution ==========


def task_run(request, pk):
    """รัน Task"""
    task = get_object_or_404(RPATask, pk=pk)

    # ตรวจสอบสถานะ
    if task.status == "running":
        messages.warning(request, "Task นี้กำลังทำงานอยู่แล้ว")
        return redirect("task_detail", pk=pk)

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
    return redirect("task_detail", pk=pk)


def task_stop(request, pk):
    """หยุด Task (ยังไม่ได้ implement การหยุดจริง)"""
    task = get_object_or_404(RPATask, pk=pk)

    if task.status == "running":
        # TODO: Implement actual stopping mechanism
        task.status = "pending"
        task.save()
        messages.warning(request, f'หยุด Task "{task.name}" แล้ว')
    else:
        messages.info(request, "Task ไม่ได้กำลังทำงาน")

    return redirect("task_detail", pk=pk)


# ========== API Endpoints ==========


@require_http_methods(["GET"])
def api_task_status(request, pk):
    """API: ดูสถานะ Task"""
    task = get_object_or_404(RPATask, pk=pk)

    data = {
        "id": task.id,
        "name": task.name,
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
def api_task_logs(request, pk):
    """API: ดู Logs ของ Task"""
    task = get_object_or_404(RPATask, pk=pk)
    logs = task.logs.all()[:50]

    data = {
        "task_id": task.id,
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
def api_task_run(request, pk):
    """API: รัน Task"""
    task = get_object_or_404(RPATask, pk=pk)

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

    return JsonResponse({"success": True, "message": "เริ่มรัน Task แล้ว"})


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

    # สถิติตามหมวด
    categories_stats = []
    for category_code, category_name in NewsSource.CATEGORY_CHOICES:
        count = today_articles.filter(source__category=category_code).count()
        categories_stats.append(
            {"code": category_code, "name": category_name, "count": count}
        )

    # ข่าวล่าสุด
    recent_articles = NewsArticle.objects.all()[:20]

    context = {
        "latest_report": latest_report,
        "today_articles_count": today_articles.count(),
        "categories_stats": categories_stats,
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


def daily_report_detail(request, pk):
    """หน้ารายละเอียดรายงานประจำวัน"""
    report = get_object_or_404(DailyReport, pk=pk)

    context = {
        "report": report,
    }

    return render(request, "rpa_bot/daily_report_detail.html", context)


def trigger_news_scrape(request):
    """Trigger ดึงข้อมูลข่าวด้วยตัวเอง"""
    if request.method == "POST":
        try:
            # เรียก Celery task
            scrape_all_news.delay()
            messages.success(request, "เริ่มดึงข้อมูลข่าวแล้ว! กรุณารอสักครู่...")
        except Exception as e:
            messages.error(request, f"เกิดข้อผิดพลาด: {str(e)}")

        return redirect("news_dashboard")

    return render(request, "rpa_bot/trigger_scrape.html")


def trigger_generate_report(request):
    """Trigger สร้างรายงานด้วยตัวเอง"""
    if request.method == "POST":
        try:
            # เรียก Celery task
            generate_daily_report.delay()
            messages.success(request, "เริ่มสร้างรายงานแล้ว! กรุณารอสักครู่...")
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
