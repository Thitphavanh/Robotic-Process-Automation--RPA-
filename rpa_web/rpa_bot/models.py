from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver


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
