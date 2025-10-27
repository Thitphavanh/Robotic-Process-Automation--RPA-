from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import (
    RPATask,
    TaskSchedule,
    TaskLog,
    NewsSource,
    NewsArticle,
    DailyReport,
    ProductCategory,
    ProductBrand,
    TrackedProduct,
    PriceHistory,
    DocSection,
    DocContentBlock,
)



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


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count', 'is_active', 'created_at')
    search_fields = ('name', 'slug', 'keywords', 'description')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'product_count')
    prepopulated_fields = {}

    fieldsets = (
        ('ข้อมูลหมวดหมู่', {
            'fields': ('name', 'slug', 'description', 'keywords')
        }),
        ('สถานะ', {
            'fields': ('is_active', 'product_count')
        }),
        ('วันที่และเวลา', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def product_count(self, obj):
        """แสดงจำนวนสินค้าในหมวดหมู่นี้"""
        count = obj.tracked_products.filter(is_active=True).count()
        return f"{count} สินค้า"
    product_count.short_description = 'จำนวนสินค้า'

    actions = ['activate_categories', 'deactivate_categories']

    def activate_categories(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'เปิดใช้งาน {updated} หมวดหมู่')
    activate_categories.short_description = 'เปิดใช้งานหมวดหมู่ที่เลือก'

    def deactivate_categories(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'ปิดใช้งาน {updated} หมวดหมู่')
    deactivate_categories.short_description = 'ปิดใช้งานหมวดหมู่ที่เลือก'


@admin.register(ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'website_link', 'product_count', 'is_active', 'created_at')
    search_fields = ('name', 'slug', 'website')
    list_filter = ('is_active', 'created_at')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'product_count')

    fieldsets = (
        ('ข้อมูลแบรนด์', {
            'fields': ('name', 'slug', 'logo_url', 'website')
        }),
        ('สถานะ', {
            'fields': ('is_active', 'product_count')
        }),
        ('วันที่และเวลา', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def website_link(self, obj):
        """แสดง link ไปยังเว็บไซต์แบรนด์"""
        if obj.website:
            return f'<a href="{obj.website}" target="_blank">{obj.website[:50]}...</a>'
        return '-'
    website_link.short_description = 'Website'
    website_link.allow_tags = True

    def product_count(self, obj):
        """แสดงจำนวนสินค้าของแบรนด์นี้"""
        count = obj.tracked_products.filter(is_active=True).count()
        return f"{count} สินค้า"
    product_count.short_description = 'จำนวนสินค้า'

    actions = ['activate_brands', 'deactivate_brands']

    def activate_brands(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'เปิดใช้งาน {updated} แบรนด์')
    activate_brands.short_description = 'เปิดใช้งานแบรนด์ที่เลือก'

    def deactivate_brands(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'ปิดใช้งาน {updated} แบรนด์')
    deactivate_brands.short_description = 'ปิดใช้งานแบรนด์ที่เลือก'


class PriceHistoryInline(admin.TabularInline):
    """Inline แสดงประวัติราคาในหน้า TrackedProduct"""
    model = PriceHistory
    extra = 0
    can_delete = False
    readonly_fields = ('price', 'original_price', 'discount_percent', 'stock_status', 'recorded_at')
    fields = ('price', 'original_price', 'discount_percent', 'stock_status', 'recorded_at')
    ordering = ('-recorded_at',)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(TrackedProduct)
class TrackedProductAdmin(admin.ModelAdmin):
    list_display = (
        'title_short',
        'platform',
        'category',
        'brand',
        'price_display',
        'discount_display',
        'alert_status',
        'is_active',
        'last_checked_at',
    )
    list_filter = (
        'platform',
        'is_active',
        'category',
        'brand',
        'enable_price_alert',
        'is_available',
        'last_checked_at',
    )
    search_fields = ('title', 'product_url', 'product_id')
    readonly_fields = (
        'product_id',
        'created_at',
        'updated_at',
        'last_checked_at',
        'discount_percent',
        'price_change_display',
    )
    list_select_related = ('category', 'brand')
    list_per_page = 50
    date_hierarchy = 'created_at'
    inlines = [PriceHistoryInline]

    fieldsets = (
        ('ข้อมูลสินค้า', {
            'fields': (
                'platform',
                'product_url',
                'product_id',
                'title',
                'category',
                'brand',
                'image_url',
            )
        }),
        ('ราคาและส่วนลด', {
            'fields': (
                'current_price',
                'original_price',
                'discount_percent',
                'lowest_price',
                'highest_price',
                'price_change_display',
            )
        }),
        ('ข้อมูลเพิ่มเติม', {
            'fields': (
                'rating',
                'reviews_count',
                'sold_count',
                'stock_status',
                'is_available',
            )
        }),
        ('การแจ้งเตือนราคา', {
            'fields': (
                'enable_price_alert',
                'target_price',
                'alert_sent',
            ),
            'classes': ('collapse',)
        }),
        ('สถานะและวันที่', {
            'fields': (
                'is_active',
                'last_checked_at',
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)
        }),
    )

    def title_short(self, obj):
        """แสดงชื่อสินค้าแบบย่อ"""
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_short.short_description = 'ชื่อสินค้า'

    def price_display(self, obj):
        """แสดงราคาพร้อมสกุลเงิน"""
        if obj.current_price:
            price = float(obj.current_price)
            if obj.original_price and float(obj.original_price) > price:
                return f'฿{price:,.2f} <del>฿{float(obj.original_price):,.2f}</del>'
            return f'฿{price:,.2f}'
        return '-'
    price_display.short_description = 'ราคา'
    price_display.allow_tags = True

    def discount_display(self, obj):
        """แสดงส่วนลด"""
        if obj.discount_percent and float(obj.discount_percent) > 0:
            return f'-{float(obj.discount_percent):.0f}%'
        return '-'
    discount_display.short_description = 'ส่วนลด'

    def alert_status(self, obj):
        """แสดงสถานะการแจ้งเตือน"""
        if obj.enable_price_alert:
            if obj.alert_sent:
                return '✅ ส่งแล้ว'
            elif obj.target_price and obj.current_price and float(obj.current_price) <= float(obj.target_price):
                return '🔔 ถึงเป้า'
            else:
                return '⏳ กำลังติดตาม'
        return '-'
    alert_status.short_description = 'Alert'

    def price_change_display(self, obj):
        """แสดงการเปลี่ยนแปลงราคา"""
        if obj.lowest_price and obj.highest_price and obj.current_price:
            current = float(obj.current_price)
            lowest = float(obj.lowest_price)
            highest = float(obj.highest_price)

            # คำนวณจาก lowest
            change_from_low = ((current - lowest) / lowest * 100) if lowest > 0 else 0
            # คำนวณจาก highest
            change_from_high = ((current - highest) / highest * 100) if highest > 0 else 0

            return f'จากต่ำสุด: {change_from_low:+.1f}% | จากสูงสุด: {change_from_high:+.1f}%'
        return '-'
    price_change_display.short_description = 'การเปลี่ยนแปลงราคา'

    actions = [
        'activate_products',
        'deactivate_products',
        'enable_price_alerts',
        'disable_price_alerts',
        'mark_as_unavailable',
        'update_prices',
    ]

    def activate_products(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'เปิดใช้งาน {updated} สินค้า')
    activate_products.short_description = 'เปิดใช้งานสินค้าที่เลือก'

    def deactivate_products(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'ปิดใช้งาน {updated} สินค้า')
    deactivate_products.short_description = 'ปิดใช้งานสินค้าที่เลือก'

    def enable_price_alerts(self, request, queryset):
        updated = queryset.update(enable_price_alert=True, alert_sent=False)
        self.message_user(request, f'เปิด Price Alert สำหรับ {updated} สินค้า')
    enable_price_alerts.short_description = 'เปิด Price Alert ที่เลือก'

    def disable_price_alerts(self, request, queryset):
        updated = queryset.update(enable_price_alert=False)
        self.message_user(request, f'ปิด Price Alert สำหรับ {updated} สินค้า')
    disable_price_alerts.short_description = 'ปิด Price Alert ที่เลือก'

    def mark_as_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'ทำเครื่องหมาย {updated} สินค้าว่าหมด')
    mark_as_unavailable.short_description = 'ทำเครื่องหมายว่าสินค้าหมด'

    def update_prices(self, request, queryset):
        """อัพเดทราคาสินค้าที่เลือก"""
        from .product_scraper import ProductScraperService

        scraper = ProductScraperService()
        updated = 0
        failed = 0

        for product in queryset:
            try:
                scraper.update_tracked_product(product)
                updated += 1
            except Exception as e:
                failed += 1

        self.message_user(
            request,
            f'อัพเดทราคาเสร็จสิ้น: สำเร็จ {updated} รายการ, ล้มเหลว {failed} รายการ'
        )
    update_prices.short_description = 'อัพเดทราคาสินค้าที่เลือก'


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'tracked_product_display',
        'platform_display',
        'price',
        'original_price',
        'discount_percent',
        'stock_status',
        'recorded_at',
    )
    list_filter = (
        'tracked_product__platform',
        'stock_status',
        'recorded_at',
    )
    search_fields = ('tracked_product__title', 'tracked_product__product_id')
    readonly_fields = ('tracked_product', 'price', 'original_price', 'discount_percent', 'stock_status', 'recorded_at')
    list_select_related = ('tracked_product', 'tracked_product__category', 'tracked_product__brand')
    list_per_page = 100
    date_hierarchy = 'recorded_at'

    def has_add_permission(self, request):
        """ห้ามเพิ่มประวัติราคาด้วยตนเอง"""
        return False

    def tracked_product_display(self, obj):
        """แสดงชื่อสินค้าแบบย่อ"""
        title = obj.tracked_product.title
        return title[:50] + '...' if len(title) > 50 else title
    tracked_product_display.short_description = 'สินค้า'

    def platform_display(self, obj):
        """แสดงแพลตฟอร์ม"""
        return obj.tracked_product.get_platform_display()
    platform_display.short_description = 'แพลตฟอร์ม'


class DocContentBlockInline(admin.TabularInline):
    """Inline แสดงบล็อกเนื้อหาในหน้า DocSection"""
    model = DocContentBlock
    extra = 1
    fields = ('block_type', 'heading', 'content', 'order', 'is_active')
    ordering = ('order',)


@admin.register(DocSection)
class DocSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'group', 'order', 'icon', 'content_blocks_count', 'is_active', 'created_at')
    list_filter = ('group', 'is_active', 'created_at')
    search_fields = ('title', 'slug', 'description', 'content')
    readonly_fields = ('slug', 'created_at', 'updated_at', 'content_blocks_count')
    list_editable = ('order', 'is_active')
    ordering = ('group', 'order', 'title')
    inlines = [DocContentBlockInline]

    fieldsets = (
        ('ข้อมูลเอกสาร', {
            'fields': ('title', 'slug', 'icon', 'description')
        }),
        ('เนื้อหา', {
            'fields': ('content',),
            'description': 'เนื้อหาหลัก (สำหรับเนื้อหาแบบง่าย) หรือสามารถใช้ Content Blocks ด้านล่างสำหรับเนื้อหาที่ซับซ้อน'
        }),
        ('การจัดกลุ่ม', {
            'fields': ('group', 'order')
        }),
        ('สถานะ', {
            'fields': ('is_active', 'content_blocks_count')
        }),
        ('วันที่และเวลา', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    actions = ['activate_sections', 'deactivate_sections']

    def content_blocks_count(self, obj):
        """แสดงจำนวน Content Blocks"""
        count = obj.content_blocks.filter(is_active=True).count()
        return f"{count} blocks"
    content_blocks_count.short_description = 'Content Blocks'

    def activate_sections(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'เปิดใช้งาน {updated} เอกสาร')
    activate_sections.short_description = 'เปิดใช้งานเอกสารที่เลือก'

    def deactivate_sections(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'ปิดใช้งาน {updated} เอกสาร')
    deactivate_sections.short_description = 'ปิดใช้งานเอกสารที่เลือก'


@admin.register(DocContentBlock)
class DocContentBlockAdmin(admin.ModelAdmin):
    list_display = ('section', 'block_type', 'heading_short', 'order', 'is_active', 'created_at')
    list_filter = ('block_type', 'is_active', 'section__group', 'created_at')
    search_fields = ('heading', 'content', 'section__title')
    list_editable = ('order', 'is_active')
    ordering = ('section', 'order')
    list_select_related = ('section',)

    fieldsets = (
        ('ข้อมูลพื้นฐาน', {
            'fields': ('section', 'block_type', 'order', 'is_active')
        }),
        ('เนื้อหา', {
            'fields': ('heading', 'content')
        }),
        ('โค้ด (สำหรับ block_type=code)', {
            'fields': ('code_language',),
            'classes': ('collapse',)
        }),
        ('การแจ้งเตือน (สำหรับ block_type=alert)', {
            'fields': ('alert_type',),
            'classes': ('collapse',)
        }),
        ('การ์ด (สำหรับ block_type=card)', {
            'fields': ('card_title', 'card_icon', 'card_color'),
            'classes': ('collapse',)
        }),
        ('รูปภาพ (สำหรับ block_type=image)', {
            'fields': ('image_url', 'image_alt'),
            'classes': ('collapse',)
        }),
        ('รายการ (สำหรับ block_type=list)', {
            'fields': ('list_items',),
            'classes': ('collapse',),
            'description': 'JSON array เช่น ["item 1", "item 2", "item 3"]'
        }),
        ('ตาราง (สำหรับ block_type=table)', {
            'fields': ('table_data',),
            'classes': ('collapse',),
            'description': 'JSON object เช่น {"headers": ["Col1", "Col2"], "rows": [["A", "B"], ["C", "D"]]}'
        }),
        ('วันที่และเวลา', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ('created_at', 'updated_at')

    def heading_short(self, obj):
        """แสดงหัวข้อแบบย่อ"""
        if obj.heading:
            return obj.heading[:50] + '...' if len(obj.heading) > 50 else obj.heading
        elif obj.content:
            return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
        return '-'
    heading_short.short_description = 'หัวข้อ/เนื้อหา'

    actions = ['activate_blocks', 'deactivate_blocks']

    def activate_blocks(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'เปิดใช้งาน {updated} blocks')
    activate_blocks.short_description = 'เปิดใช้งาน Blocks ที่เลือก'

    def deactivate_blocks(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'ปิดใช้งาน {updated} blocks')
    deactivate_blocks.short_description = 'ปิดใช้งาน Blocks ที่เลือก'
