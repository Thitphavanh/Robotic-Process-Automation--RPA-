from django.contrib import admin
from .models import RPATask, TaskSchedule, TaskLog, NewsSource, NewsArticle, DailyReport


@admin.register(RPATask)
class RPATaskAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "task_type",
        "status",
        "keyword",
        "created_at",
        "updated_at",
    ]
    list_filter = ["status", "task_type", "created_at"]
    search_fields = ["name", "keyword", "description"]
    readonly_fields = ["created_at", "updated_at", "started_at", "completed_at"]

    fieldsets = (
        ("ข้อมูลพื้นฐาน", {"fields": ("name", "description", "task_type")}),
        (
            "การตั้งค่า Task",
            {"fields": ("url", "keyword", "delay_seconds", "max_retries")},
        ),
        (
            "สถานะและผลลัพธ์",
            {"fields": ("status", "screenshot_path", "error_message", "retry_count")},
        ),
        (
            "วันที่และเวลา",
            {
                "fields": ("created_at", "updated_at", "started_at", "completed_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(TaskSchedule)
class TaskScheduleAdmin(admin.ModelAdmin):
    list_display = ["task", "frequency", "scheduled_time", "is_active", "last_run"]
    list_filter = ["frequency", "is_active", "scheduled_time"]
    search_fields = ["task__name"]


@admin.register(TaskLog)
class TaskLogAdmin(admin.ModelAdmin):
    list_display = ["task", "level", "message", "created_at"]
    list_filter = ["level", "created_at"]
    search_fields = ["task__name", "message"]
    readonly_fields = ["created_at"]


@admin.register(NewsSource)
class NewsSourceAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "is_active", "created_at"]
    list_filter = ["category", "is_active", "created_at"]
    search_fields = ["name", "url"]
    readonly_fields = ["created_at", "updated_at"]

    fieldsets = (
        ("ข้อมูลพื้นฐาน", {"fields": ("name", "category", "url", "is_active", "slug")}),
        ("การตั้งค่า Scraping", {"fields": ("selector", "api_endpoint", "api_key")}),
        (
            "วันที่และเวลา",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "source",
        "price",
        "change_percent",
        "sentiment",
        "published_at",
    ]
    list_filter = ["source__category", "sentiment", "published_at", "scraped_at"]
    search_fields = ["title", "content", "source__name"]
    readonly_fields = ["scraped_at"]

    fieldsets = (
        ("ข้อมูลข่าว", {"fields": ("source", "title", "content", "url", "image_url", "slug")}),
        ("ข้อมูลราคา", {"fields": ("price", "change", "change_percent")}),
        ("AI Analysis", {"fields": ("ai_summary", "sentiment")}),
        ("วันที่และเวลา", {"fields": ("published_at", "scraped_at")}),
    )


@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ["report_date", "is_completed", "is_sent", "sent_at", "created_at"]
    list_filter = ["is_completed", "is_sent", "report_date"]
    search_fields = ["full_report"]
    readonly_fields = ["created_at", "updated_at"]
    filter_horizontal = ["articles"]

    fieldsets = (
        (
            "ข้อมูลรายงาน",
            {"fields": ("report_date", "slug", "is_completed", "is_sent", "sent_at")},
        ),
        (
            "สรุปตลาดหุ้น",
            {
                "fields": (
                    "stock_thai_summary",
                    "stock_us_summary",
                    "stock_europe_summary",
                    "stock_china_summary",
                )
            },
        ),
        (
            "สรุปสินทรัพย์ดิจิทัล",
            {
                "fields": (
                    "crypto_summary",
                    "gold_summary",
                )
            },
        ),
        (
            "สรุปเทคโนโลยี",
            {
                "fields": (
                    "tech_ai_summary",
                    "tech_hardware_summary",
                    "tech_software_summary",
                    "ev_car_summary",
                    "rocket_space_summary",
                )
            },
        ),
        (
            "สรุปกีฬา",
            {
                "fields": (
                    "football_summary",
                )
            },
        ),
        ("รายงานเต็ม", {"fields": ("full_report",)}),
        ("บทความที่ใช้", {"fields": ("articles",)}),
        (
            "วันที่และเวลา",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )
