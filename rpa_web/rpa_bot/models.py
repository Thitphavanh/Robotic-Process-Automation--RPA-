from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_summernote.fields import SummernoteTextField


class RPATask(models.Model):
    """Model สำหรับเก็บข้อมูล RPA Task"""

    STATUS_CHOICES = [
        ("pending", "รอดำเนินการ"),
        ("running", "กำลังทำงาน"),
        ("completed", "สำเร็จ"),
        ("failed", "ล้มเหลว"),
    ]

    TASK_TYPE_CHOICES = [
        ("google_search", "ค้นหา Google"),
        ("screenshot", "จับภาพหน้าจอ"),
        ("web_automation", "ระบบอัตโนมัติเว็บ"),
        ("data_extraction", "ดึงข้อมูล"),
    ]

    # ข้อมูลพื้นฐาน
    name = models.CharField(max_length=255, verbose_name="ชื่อ Task")
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="คำอธิบาย")
    task_type = models.CharField(
        max_length=50,
        choices=TASK_TYPE_CHOICES,
        default="google_search",
        verbose_name="ประเภท Task",
    )

    # ข้อมูล Task
    url = models.URLField(
        max_length=500, default="https://www.google.com", verbose_name="URL"
    )
    keyword = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="คำค้นหา"
    )

    # สถานะ
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="สถานะ"
    )

    # ผลลัพธ์
    screenshot_path = models.CharField(
        max_length=500, blank=True, null=True, verbose_name="ที่อยู่ภาพ"
    )
    result_data = models.JSONField(blank=True, null=True, verbose_name="ผลลัพธ์")
    error_message = models.TextField(blank=True, null=True, verbose_name="ข้อความ Error")

    # การตั้งค่า
    delay_seconds = models.IntegerField(default=3, verbose_name="หน่วงเวลา (วินาที)")
    max_retries = models.IntegerField(default=3, verbose_name="ลองใหม่สูงสุด")
    retry_count = models.IntegerField(default=0, verbose_name="จำนวนครั้งที่ลองแล้ว")

    # วันที่และเวลา
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="สร้างเมื่อ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="อัพเดทเมื่อ")
    started_at = models.DateTimeField(blank=True, null=True, verbose_name="เริ่มเมื่อ")
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name="เสร็จเมื่อ")

    # ผู้สร้าง
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="สร้างโดย"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "RPA Task"
        verbose_name_plural = "RPA Tasks"

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def mark_as_running(self):
        """เปลี่ยนสถานะเป็นกำลังทำงาน"""
        self.status = "running"
        self.started_at = timezone.now()
        self.save()

    def mark_as_completed(self, screenshot_path=None):
        """เปลี่ยนสถานะเป็นสำเร็จ"""
        self.status = "completed"
        self.completed_at = timezone.now()
        if screenshot_path:
            self.screenshot_path = screenshot_path
        self.save()

    def mark_as_failed(self, error_message):
        """เปลี่ยนสถานะเป็นล้มเหลว"""
        self.status = "failed"
        self.error_message = error_message
        self.completed_at = timezone.now()
        self.save()

    def increment_retry(self):
        """เพิ่มจำนวนครั้งที่ลองใหม่"""
        self.retry_count += 1
        self.save()

    @property
    def duration(self):
        """คำนวณระยะเวลาในการทำงาน"""
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            return delta.total_seconds()
        return None

    @property
    def is_retryable(self):
        """ตรวจสอบว่าสามารถลองใหม่ได้หรือไม่"""
        return self.retry_count < self.max_retries


class TaskSchedule(models.Model):
    """Model สำหรับกำหนดเวลา Task อัตโนมัติ"""

    FREQUENCY_CHOICES = [
        ("once", "ครั้งเดียว"),
        ("daily", "ทุกวัน"),
        ("weekly", "ทุกสัปดาห์"),
        ("monthly", "ทุกเดือน"),
    ]

    task = models.ForeignKey(
        RPATask, on_delete=models.CASCADE, related_name="schedules"
    )
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, default="once"
    )
    scheduled_time = models.DateTimeField(verbose_name="กำหนดเวลา")
    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งาน")
    last_run = models.DateTimeField(blank=True, null=True, verbose_name="รันครั้งล่าสุด")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_time"]
        verbose_name = "กำหนดเวลา Task"
        verbose_name_plural = "กำหนดเวลา Tasks"

    def __str__(self):
        return f"{self.task.name} - {self.get_frequency_display()}"


class TaskLog(models.Model):
    """Model สำหรับเก็บ Log การทำงาน"""

    LOG_LEVEL_CHOICES = [
        ("info", "Info"),
        ("warning", "Warning"),
        ("error", "Error"),
        ("success", "Success"),
    ]

    task = models.ForeignKey(RPATask, on_delete=models.CASCADE, related_name="logs")
    level = models.CharField(max_length=20, choices=LOG_LEVEL_CHOICES, default="info")
    message = models.TextField(verbose_name="ข้อความ")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Log"
        verbose_name_plural = "Logs"

    def __str__(self):
        return f"[{self.level.upper()}] {self.task.name} - {self.created_at}"


class NewsSource(models.Model):
    """Model สำหรับแหล่งข้อมูลข่าว"""

    CATEGORY_CHOICES = [
        ("stock_thai", "หุ้นไทย"),
        ("stock_us", "หุ้นอเมริกา"),
        ("stock_europe", "หุ้นยุโรป"),
        ("stock_china", "หุ้นจีน"),
        ("crypto", "Bitcoin/Crypto"),
        ("gold", "ราคาทองคำ"),
        ("tech_ai", "Technology AI"),
        ("tech_hardware", "Hardware"),
        ("tech_software", "Software"),
        ("football", "Football"),
        ("ev_car", "EV Car"),
        ("rocket_space", "Rocket & Space"),
        ("e_commerce", "E-Commerce Deals"),
    ]

    name = models.CharField(max_length=255, verbose_name="ชื่อแหล่งข้อมูล")
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, verbose_name="หมวดหมู่"
    )
    url = models.URLField(max_length=500, verbose_name="URL")
    selector = models.TextField(blank=True, null=True, verbose_name="CSS Selector")
    api_endpoint = models.URLField(
        max_length=500, blank=True, null=True, verbose_name="API Endpoint"
    )
    api_key = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="API Key"
    )
    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งาน")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "name"]
        verbose_name = "แหล่งข้อมูลข่าว"
        verbose_name_plural = "แหล่งข้อมูลข่าว"

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class ProductCategory(models.Model):
    """Model สำหรับหมวดหมู่สินค้า E-Commerce"""

    name = models.CharField(max_length=255, verbose_name="ชื่อหมวดหมู่")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, null=True, verbose_name="คำอธิบาย")
    keywords = models.TextField(
        blank=True,
        null=True,
        verbose_name="คำค้นหา",
        help_text="คำค้นหาหลายคำคั่นด้วย comma เช่น smartphone,มือถือ,โทรศัพท์"
    )
    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งาน")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "หมวดหมู่สินค้า"
        verbose_name_plural = "หมวดหมู่สินค้า"

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    """Model สำหรับแบรนด์สินค้า"""

    name = models.CharField(max_length=255, verbose_name="ชื่อแบรนด์")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    logo_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="โลโก้")
    website = models.URLField(max_length=500, blank=True, null=True, verbose_name="เว็บไซต์")
    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งาน")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "แบรนด์สินค้า"
        verbose_name_plural = "แบรนด์สินค้า"

    def __str__(self):
        return self.name


class TrackedProduct(models.Model):
    """Model สำหรับติดตามสินค้าเฉพาะ"""

    PLATFORM_CHOICES = [
        ("lazada", "Lazada"),
        ("shopee", "Shopee"),
        ("tiktok", "TikTok Shop"),
        ("taobao", "Taobao"),
        ("tmall", "Tmall"),
        ("pinduoduo", "Pinduoduo"),
        ("jd", "JD.com"),
        ("1688", "1688.com"),
        ("alibaba", "Alibaba.com"),
        ("aliexpress", "AliExpress"),
        ("amazon", "Amazon"),
    ]

    platform = models.CharField(
        max_length=50, choices=PLATFORM_CHOICES, verbose_name="แพลตฟอร์ม"
    )
    product_url = models.URLField(max_length=1000, verbose_name="URL สินค้า")
    product_id = models.CharField(
        max_length=255, blank=True, null=True, verbose_name="Product ID"
    )
    title = models.CharField(max_length=500, verbose_name="ชื่อสินค้า")
    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tracked_products",
        verbose_name="หมวดหมู่",
    )
    brand = models.ForeignKey(
        ProductBrand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tracked_products",
        verbose_name="แบรนด์",
    )

    # ราคาปัจจุบัน
    current_price = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="ราคาปัจจุบัน"
    )
    original_price = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="ราคาเต็ม"
    )
    discount_percent = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="ส่วนลด %"
    )

    # ราคาต่ำสุด/สูงสุดที่เคยเจอ
    lowest_price = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="ราคาต่ำสุด"
    )
    highest_price = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="ราคาสูงสุด"
    )

    # ข้อมูลสินค้า
    image_url = models.URLField(max_length=1000, blank=True, null=True, verbose_name="รูปภาพ")
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, blank=True, null=True, verbose_name="คะแนน"
    )
    reviews_count = models.IntegerField(
        default=0, blank=True, null=True, verbose_name="จำนวนรีวิว"
    )
    sold_count = models.IntegerField(
        default=0, blank=True, null=True, verbose_name="ยอดขาย"
    )
    stock_status = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="สถานะสต็อก"
    )

    # การแจ้งเตือน
    enable_price_alert = models.BooleanField(
        default=False, verbose_name="เปิดแจ้งเตือนราคา"
    )
    target_price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="ราคาเป้าหมาย",
        help_text="แจ้งเตือนเมื่อราคาต่ำกว่าหรือเท่ากับราคานี้",
    )
    alert_sent = models.BooleanField(default=False, verbose_name="ส่งการแจ้งเตือนแล้ว")

    # สถานะ
    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งาน")
    is_available = models.BooleanField(default=True, verbose_name="มีสินค้า")

    # วันที่
    last_checked_at = models.DateTimeField(
        blank=True, null=True, verbose_name="ตรวจสอบล่าสุด"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="สร้างเมื่อ")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="อัพเดทเมื่อ")

    # ผู้สร้าง
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tracked_products",
        verbose_name="สร้างโดย",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "สินค้าที่ติดตาม"
        verbose_name_plural = "สินค้าที่ติดตาม"
        indexes = [
            models.Index(fields=["platform", "is_active"]),
            models.Index(fields=["category", "brand"]),
            models.Index(fields=["-current_price"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.get_platform_display()})"

    def update_price(self, new_price):
        """อัพเดทราคาและติดตามราคาต่ำสุด/สูงสุด"""
        self.current_price = new_price

        # อัพเดทราคาต่ำสุด
        if not self.lowest_price or new_price < self.lowest_price:
            self.lowest_price = new_price

        # อัพเดทราคาสูงสุด
        if not self.highest_price or new_price > self.highest_price:
            self.highest_price = new_price

        # ตรวจสอบการแจ้งเตือน
        if self.enable_price_alert and self.target_price:
            if new_price <= self.target_price and not self.alert_sent:
                self.alert_sent = True
                # TODO: ส่ง notification

        self.last_checked_at = timezone.now()
        self.save()


class PriceHistory(models.Model):
    """Model สำหรับเก็บประวัติราคาสินค้า"""

    tracked_product = models.ForeignKey(
        TrackedProduct,
        on_delete=models.CASCADE,
        related_name="price_history",
        verbose_name="สินค้า",
    )
    price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name="ราคา")
    original_price = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="ราคาเต็ม"
    )
    discount_percent = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="ส่วนลด %"
    )
    stock_status = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="สถานะสต็อก"
    )
    recorded_at = models.DateTimeField(auto_now_add=True, verbose_name="บันทึกเมื่อ")

    class Meta:
        ordering = ["-recorded_at"]
        verbose_name = "ประวัติราคา"
        verbose_name_plural = "ประวัติราคา"
        indexes = [
            models.Index(fields=["tracked_product", "-recorded_at"]),
        ]

    def __str__(self):
        return f"{self.tracked_product.title} - {self.price} ({self.recorded_at})"


class NewsArticle(models.Model):
    """Model สำหรับเก็บข่าวที่ดึงมา"""

    source = models.ForeignKey(
        NewsSource, on_delete=models.CASCADE, related_name="articles"
    )
    title = models.CharField(max_length=500, verbose_name="หัวข้อข่าว")
    slug = models.SlugField(max_length=600, unique=True, blank=True, null=True, verbose_name="Slug")
    content = models.TextField(verbose_name="เนื้อหา")
    url = models.URLField(max_length=500, verbose_name="URL")
    image_url = models.URLField(
        max_length=500, blank=True, null=True, verbose_name="รูปภาพ"
    )

    # ข้อมูลราคา/ค่า (สำหรับหุ้น, Bitcoin, ทอง)
    price = models.DecimalField(
        max_digits=15, decimal_places=2, blank=True, null=True, verbose_name="ราคา"
    )
    change = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="การเปลี่ยนแปลง",
    )
    change_percent = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="% เปลี่ยนแปลง",
    )

    # AI Summary
    ai_summary = models.TextField(blank=True, null=True, verbose_name="สรุปโดย AI")
    detailed_analysis = models.TextField(blank=True, null=True, verbose_name="การวิเคราะห์แบบละเอียด")
    sentiment = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Sentiment"
    )

    published_at = models.DateTimeField(verbose_name="เผยแพร่เมื่อ")
    scraped_at = models.DateTimeField(auto_now_add=True, verbose_name="ดึงข้อมูลเมื่อ")

    class Meta:
        ordering = ["-published_at"]
        verbose_name = "ข่าว"
        verbose_name_plural = "ข่าว"
        indexes = [
            models.Index(fields=["-published_at"]),
            models.Index(fields=["source", "-published_at"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.source.name}"


class DailyReport(models.Model):
    """Model สำหรับรายงานประจำวัน"""

    report_date = models.DateField(verbose_name="วันที่รายงาน", unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="Slug")

    # เนื้อหารายงานแต่ละหมวด
    stock_thai_summary = models.TextField(
        blank=True, null=True, verbose_name="สรุปหุ้นไทย"
    )
    stock_us_summary = models.TextField(
        blank=True, null=True, verbose_name="สรุปหุ้นอเมริกา"
    )
    stock_europe_summary = models.TextField(
        blank=True, null=True, verbose_name="สรุปหุ้นยุโรป"
    )
    stock_china_summary = models.TextField(
        blank=True, null=True, verbose_name="สรุปหุ้นจีน"
    )
    crypto_summary = models.TextField(
        blank=True, null=True, verbose_name="สรุป Bitcoin/Crypto"
    )
    gold_summary = models.TextField(blank=True, null=True, verbose_name="สรุปราคาทอง")
    tech_ai_summary = models.TextField(blank=True, null=True, verbose_name="สรุปข่าว AI")
    tech_hardware_summary = models.TextField(blank=True, null=True, verbose_name="สรุปข่าว Hardware")
    tech_software_summary = models.TextField(blank=True, null=True, verbose_name="สรุปข่าว Software")
    football_summary = models.TextField(
        blank=True, null=True, verbose_name="สรุปข่าว Football"
    )
    ev_car_summary = models.TextField(
        blank=True, null=True, verbose_name="สรุปข่าว EV Car"
    )
    rocket_space_summary = models.TextField(
        blank=True, null=True, verbose_name="สรุปข่าว Rocket & Space"
    )
    e_commerce_summary = models.TextField(
        blank=True, null=True, verbose_name="สรุป E-Commerce Deals"
    )

    # รายงานรวม
    full_report = models.TextField(blank=True, null=True, verbose_name="รายงานเต็ม")

    # สถานะ
    is_completed = models.BooleanField(default=False, verbose_name="เสร็จสมบูรณ์")
    is_sent = models.BooleanField(default=False, verbose_name="ส่งแล้ว")
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name="ส่งเมื่อ")

    # ข้อมูลบทความที่ใช้
    articles = models.ManyToManyField(
        NewsArticle, related_name="reports", verbose_name="บทความที่ใช้"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-report_date"]
        verbose_name = "รายงานประจำวัน"
        verbose_name_plural = "รายงานประจำวัน"

    def __str__(self):
        return f"รายงานวันที่ {self.report_date}"


# Signal handlers for auto-generating slugs
@receiver(pre_save, sender=RPATask)
def generate_rpatask_slug(sender, instance, **kwargs):
    """สร้าง slug อัตโนมัติสำหรับ RPATask"""
    if not instance.slug:
        base_slug = slugify(instance.name, allow_unicode=True)
        slug = base_slug
        counter = 1
        while RPATask.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug


@receiver(pre_save, sender=NewsArticle)
def generate_newsarticle_slug(sender, instance, **kwargs):
    """สร้าง slug อัตโนมัติสำหรับ NewsArticle"""
    if not instance.slug:
        base_slug = slugify(instance.title, allow_unicode=True)
        slug = base_slug
        counter = 1
        while NewsArticle.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug


@receiver(pre_save, sender=DailyReport)
def generate_dailyreport_slug(sender, instance, **kwargs):
    """สร้าง slug อัตโนมัติสำหรับ DailyReport"""
    if not instance.slug:
        slug = slugify(f"report-{instance.report_date}", allow_unicode=True)
        instance.slug = slug


@receiver(pre_save, sender=ProductCategory)
def generate_productcategory_slug(sender, instance, **kwargs):
    """สร้าง slug อัตโนมัติสำหรับ ProductCategory"""
    if not instance.slug:
        base_slug = slugify(instance.name, allow_unicode=True)
        slug = base_slug
        counter = 1
        while ProductCategory.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug


@receiver(pre_save, sender=ProductBrand)
def generate_productbrand_slug(sender, instance, **kwargs):
    """สร้าง slug อัตโนมัติสำหรับ ProductBrand"""
    if not instance.slug:
        base_slug = slugify(instance.name, allow_unicode=True)
        slug = base_slug
        counter = 1
        while ProductBrand.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug


class DocSection(models.Model):
    """Model สำหรับจัดการหมวดหมู่เอกสาร Documentation"""

    SECTION_GROUP_CHOICES = [
        ("getting_started", "Getting Started"),
        ("core_features", "Core Features"),
        ("advanced", "Advanced"),
    ]

    title = models.CharField(max_length=255, verbose_name="ชื่อเอกสาร")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    icon = models.CharField(
        max_length=100,
        default="fa-file-alt",
        verbose_name="Font Awesome Icon",
        help_text="ชื่อ icon จาก Font Awesome เช่น fa-home, fa-rocket"
    )
    description = models.TextField(blank=True, null=True, verbose_name="คำอธิบาย")
    group = models.CharField(
        max_length=50,
        choices=SECTION_GROUP_CHOICES,
        default="getting_started",
        verbose_name="กลุ่ม"
    )
    order = models.IntegerField(default=0, verbose_name="ลำดับ")
    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งาน")

    # Content fields - สำหรับเนื้อหาแบบละเอียด
    content = models.TextField(blank=True, null=True, verbose_name="เนื้อหาหลัก")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["group", "order", "title"]
        verbose_name = "เอกสาร Documentation"
        verbose_name_plural = "เอกสาร Documentation"

    def __str__(self):
        return f"{self.title} ({self.get_group_display()})"


class DocContentBlock(models.Model):
    """Model สำหรับบล็อกเนื้อหาในแต่ละส่วนของ Documentation"""

    BLOCK_TYPE_CHOICES = [
        ("heading", "หัวข้อ"),
        ("paragraph", "ย่อหน้า"),
        ("code", "โค้ด"),
        ("list", "รายการ"),
        ("table", "ตาราง"),
        ("alert", "การแจ้งเตือน"),
        ("card", "การ์ด"),
        ("image", "รูปภาพ"),
    ]

    ALERT_TYPE_CHOICES = [
        ("info", "ข้อมูล"),
        ("success", "สำเร็จ"),
        ("warning", "คำเตือน"),
        ("danger", "อันตราย"),
    ]

    section = models.ForeignKey(
        DocSection,
        on_delete=models.CASCADE,
        related_name="content_blocks",
        verbose_name="ส่วนเอกสาร"
    )
    block_type = models.CharField(
        max_length=50,
        choices=BLOCK_TYPE_CHOICES,
        default="paragraph",
        verbose_name="ประเภทบล็อก"
    )
    order = models.IntegerField(default=0, verbose_name="ลำดับ")

    # Content
    heading = models.CharField(max_length=500, blank=True, null=True, verbose_name="หัวข้อ")
    content = models.TextField(blank=True, null=True, verbose_name="เนื้อหา")
    code_language = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="ภาษาโค้ด",
        help_text="เช่น python, javascript, bash"
    )

    # Alert specific
    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPE_CHOICES,
        blank=True,
        null=True,
        verbose_name="ประเภทการแจ้งเตือน"
    )

    # Card specific
    card_title = models.CharField(max_length=255, blank=True, null=True, verbose_name="หัวข้อการ์ด")
    card_icon = models.CharField(max_length=100, blank=True, null=True, verbose_name="ไอคอนการ์ด")
    card_color = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="สีการ์ด",
        help_text="เช่น blue, green, purple, red"
    )

    # Image specific
    image_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="URL รูปภาพ")
    image_alt = models.CharField(max_length=255, blank=True, null=True, verbose_name="คำอธิบายรูปภาพ")

    # List specific (JSON array)
    list_items = models.JSONField(blank=True, null=True, verbose_name="รายการ", help_text="JSON array ของรายการ")

    # Table specific (JSON)
    table_data = models.JSONField(blank=True, null=True, verbose_name="ข้อมูลตาราง", help_text="JSON object with headers and rows")

    is_active = models.BooleanField(default=True, verbose_name="เปิดใช้งาน")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["section", "order"]
        verbose_name = "บล็อกเนื้อหาเอกสาร"
        verbose_name_plural = "บล็อกเนื้อหาเอกสาร"

    def __str__(self):
        return f"{self.section.title} - {self.get_block_type_display()} ({self.order})"


@receiver(pre_save, sender=DocSection)
def generate_docsection_slug(sender, instance, **kwargs):
    """สร้าง slug อัตโนมัติสำหรับ DocSection"""
    if not instance.slug:
        base_slug = slugify(instance.title, allow_unicode=True)
        slug = base_slug
        counter = 1
        while DocSection.objects.filter(slug=slug).exclude(pk=instance.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug
