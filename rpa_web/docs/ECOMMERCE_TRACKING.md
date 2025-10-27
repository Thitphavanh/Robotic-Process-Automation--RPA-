# E-Commerce Price Tracking Documentation

## Overview

ระบบติดตามราคาสินค้า E-Commerce แบบครบวงจร รองรับ 9 แพลตฟอร์มหลัก พร้อมระบบแจ้งเตือนราคาอัตโนมัติ

## Supported Platforms

| Platform | Country | URL Pattern |
|----------|---------|-------------|
| **Lazada** | Thailand, Singapore, Malaysia | `lazada.co.th`, `lazada.sg`, `lazada.com.my` |
| **Shopee** | Thailand, Singapore, Malaysia | `shopee.co.th`, `shopee.sg`, `shopee.com.my` |
| **TikTok Shop** | Global | `tiktok.com/`, `shop.tiktok.com` |
| **Taobao** (淘宝) | China | `taobao.com`, `world.taobao.com` |
| **Tmall** (天猫) | China | `tmall.com`, `tmall.hk` |
| **Pinduoduo** (拼多多) | China | `pinduoduo.com`, `yangkeduo.com` |
| **1688.com** | China (B2B) | `1688.com` |
| **Alibaba.com** | International (B2B) | `alibaba.com` |
| **Amazon** | Global | `amazon.com`, `amazon.co.uk`, etc. |

## Features

### 1. Product Tracking
- ติดตามราคาสินค้าจาก URL
- จัดหมวดหมู่และแบรนด์
- บันทึกประวัติราคาอัตโนมัติ
- แสดงกราฟการเปลี่ยนแปลงราคา

### 2. Price Alerts
- ตั้งราคาเป้าหมาย (Target Price)
- แจ้งเตือนผ่าน Telegram เมื่อราคาถึงเป้าหมาย
- ระบบป้องกันการแจ้งเตือนซ้ำ

### 3. Automated Tracking
- อัพเดทราคาอัตโนมัติทุก 6 ชั่วโมง (Celery Beat)
- ตรวจสอบ Price Alerts ทุกชั่วโมง
- บันทึกประวัติราคาทุกครั้งที่อัพเดท

### 4. Analytics
- ราคาต่ำสุด/สูงสุดที่เคยมี
- ราคาเฉลี่ย 30 วัน
- % การเปลี่ยนแปลงราคา
- ส่วนลดสูงสุด

## Database Models

### ProductCategory
```python
class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
```

**ตัวอย่างหมวดหมู่:**
- Smartphones (smartphone,มือถือ,โทรศัพท์)
- Notebooks (laptop,โน้ตบุ๊ค,คอมพิวเตอร์)
- Shoes (รองเท้า,sneakers,แฟชั่น)
- Electronics (อิเล็กทรอนิกส์,เครื่องใช้ไฟฟ้า)

### ProductBrand
```python
class ProductBrand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    logo_url = models.URLField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
```

**ตัวอย่างแบรนด์:**
- Apple, Samsung, Nike, Adidas, Sony, Dell, HP, Asus

### TrackedProduct
```python
class TrackedProduct(models.Model):
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES)
    product_url = models.URLField(max_length=1000)
    title = models.CharField(max_length=500)
    category = models.ForeignKey(ProductCategory)
    brand = models.ForeignKey(ProductBrand)

    # Price Fields
    current_price = models.DecimalField(max_digits=15, decimal_places=2)
    original_price = models.DecimalField(max_digits=15, decimal_places=2)
    lowest_price = models.DecimalField(max_digits=15, decimal_places=2)
    highest_price = models.DecimalField(max_digits=15, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)

    # Price Alert
    enable_price_alert = models.BooleanField(default=False)
    target_price = models.DecimalField(max_digits=15, decimal_places=2)
    alert_sent = models.BooleanField(default=False)

    # Metadata
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    reviews_count = models.IntegerField(default=0)
    sold_count = models.IntegerField(default=0)
    stock_status = models.CharField(max_length=50)
    is_available = models.BooleanField(default=True)
```

### PriceHistory
```python
class PriceHistory(models.Model):
    tracked_product = models.ForeignKey(TrackedProduct)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    original_price = models.DecimalField(max_digits=15, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2)
    stock_status = models.CharField(max_length=50)
    recorded_at = models.DateTimeField(auto_now_add=True)
```

## API Endpoints

### Categories API

#### GET /api/ecommerce/categories/
รายการหมวดหมู่สินค้าทั้งหมด

**Response:**
```json
{
  "success": true,
  "categories": [
    {
      "id": 1,
      "name": "Smartphones",
      "slug": "smartphones",
      "description": "มือถือและสมาร์ทโฟน",
      "keywords": "smartphone,มือถือ,โทรศัพท์",
      "product_count": 15
    }
  ],
  "count": 1
}
```

#### POST /api/ecommerce/categories/create/
สร้างหมวดหมู่ใหม่

**Request:**
```json
{
  "name": "Smartphones",
  "description": "มือถือและสมาร์ทโฟน",
  "keywords": "smartphone,มือถือ,โทรศัพท์"
}
```

### Brands API

#### GET /api/ecommerce/brands/
รายการแบรนด์ทั้งหมด

#### POST /api/ecommerce/brands/create/
สร้างแบรนด์ใหม่

**Request:**
```json
{
  "name": "Apple",
  "logo_url": "https://example.com/apple-logo.png",
  "website": "https://www.apple.com"
}
```

### Tracked Products API

#### GET /api/ecommerce/tracked-products/
รายการสินค้าที่ติดตาม

**Query Parameters:**
- `platform` - กรองตาม platform (lazada, shopee, etc.)
- `category` - กรองตามหมวดหมู่ (category_id)
- `brand` - กรองตามแบรนด์ (brand_id)
- `limit` - จำนวนสูงสุดที่ต้องการ (default: 50)

**Example:**
```
GET /api/ecommerce/tracked-products/?platform=lazada&limit=10
```

**Response:**
```json
{
  "success": true,
  "products": [
    {
      "id": 1,
      "platform": "lazada",
      "title": "iPhone 15 Pro Max 256GB",
      "product_url": "https://www.lazada.co.th/...",
      "current_price": 42990.00,
      "original_price": 49990.00,
      "discount_percent": 14.00,
      "lowest_price": 42990.00,
      "highest_price": 49990.00,
      "image_url": "https://...",
      "rating": 4.8,
      "reviews_count": 1250,
      "sold_count": 3500,
      "category": "Smartphones",
      "brand": "Apple",
      "enable_price_alert": true,
      "target_price": 40000.00,
      "is_available": true,
      "last_checked_at": "2025-10-26T10:30:00Z",
      "created_at": "2025-10-25T08:00:00Z"
    }
  ],
  "count": 1
}
```

#### POST /api/ecommerce/track-url/
เพิ่มสินค้าจาก URL เพื่อติดตาม

**Request:**
```json
{
  "product_url": "https://www.lazada.co.th/products/...",
  "category_id": 1,
  "brand_id": 2,
  "enable_price_alert": true,
  "target_price": 40000.00
}
```

**Response:**
```json
{
  "success": true,
  "product": {
    "id": 1,
    "platform": "lazada",
    "title": "iPhone 15 Pro Max 256GB",
    "current_price": 42990.00,
    "product_url": "https://www.lazada.co.th/..."
  },
  "message": "เพิ่มสินค้าเรียบร้อยแล้ว"
}
```

#### PUT /api/ecommerce/product/<product_id>/update/
อัพเดทข้อมูลสินค้า

**Request:**
```json
{
  "enable_price_alert": true,
  "target_price": 38000.00,
  "category_id": 1,
  "brand_id": 2,
  "is_active": true
}
```

#### DELETE /api/ecommerce/product/<product_id>/delete/
ลบสินค้าที่ติดตาม

#### GET /api/ecommerce/price-history/<product_id>/
ประวัติราคาของสินค้า (100 รายการล่าสุด)

**Response:**
```json
{
  "success": true,
  "product": {
    "id": 1,
    "title": "iPhone 15 Pro Max 256GB",
    "platform": "lazada"
  },
  "history": [
    {
      "price": 42990.00,
      "original_price": 49990.00,
      "discount_percent": 14.00,
      "stock_status": "In Stock",
      "recorded_at": "2025-10-26T10:30:00Z"
    }
  ],
  "count": 1
}
```

### Price Updates API

#### POST /api/ecommerce/update-prices/
อัพเดทราคาสินค้าทั้งหมด (Background Task)

**Response:**
```json
{
  "success": true,
  "message": "เริ่มอัพเดทราคาสินค้าแล้ว"
}
```

#### GET /api/ecommerce/update-status/
ตรวจสอบสถานะการอัพเดทราคา

**Response:**
```json
{
  "status": "completed",
  "progress": 100,
  "result": {
    "updated": 45,
    "failed": 2
  },
  "error": null,
  "timestamp": "2025-10-26T10:35:00Z"
}
```

#### GET /api/ecommerce/price-alerts/
รายการสินค้าที่มี Price Alert ทำงานอยู่

**Response:**
```json
{
  "success": true,
  "alerts": [
    {
      "id": 1,
      "title": "iPhone 15 Pro Max 256GB",
      "platform": "lazada",
      "current_price": 39990.00,
      "target_price": 40000.00,
      "price_difference": 10.00,
      "discount_percent": 20.00,
      "product_url": "https://...",
      "image_url": "https://...",
      "created_at": "2025-10-25T08:00:00Z"
    }
  ],
  "count": 1
}
```

## Celery Tasks

### 1. update_tracked_products
**Schedule:** ทุก 6 ชั่วโมง

อัพเดทราคาสินค้าทั้งหมดที่ติดตาม

```python
from rpa_bot.tasks import update_tracked_products

# Run manually
result = update_tracked_products.delay()
```

### 2. check_price_alerts
**Schedule:** ทุกชั่วโมง

ตรวจสอบและส่งการแจ้งเตือนราคา

```python
from rpa_bot.tasks import check_price_alerts

result = check_price_alerts.delay()
```

### 3. track_product_by_url
**On-Demand Task**

เพิ่มสินค้าจาก URL แบบ Async

```python
from rpa_bot.tasks import track_product_by_url

result = track_product_by_url.delay(
    product_url="https://www.lazada.co.th/products/...",
    category_id=1,
    brand_id=2
)
```

### 4. cleanup_old_price_history
**Schedule:** ทุกวัน เวลา 03:00

ลบประวัติราคาเก่าที่เกิน 90 วัน

```python
from rpa_bot.tasks import cleanup_old_price_history

result = cleanup_old_price_history.delay(days=90)
```

## Celery Beat Configuration

เพิ่มใน `config/settings/base.py`:

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # E-Commerce Price Tracking
    'update-tracked-products': {
        'task': 'rpa_bot.tasks.update_tracked_products',
        'schedule': crontab(hour='*/6'),  # ทุก 6 ชั่วโมง
    },
    'check-price-alerts': {
        'task': 'rpa_bot.tasks.check_price_alerts',
        'schedule': crontab(minute='0', hour='*'),  # ทุกชั่วโมง
    },
    'cleanup-old-price-history': {
        'task': 'rpa_bot.tasks.cleanup_old_price_history',
        'schedule': crontab(hour='3', minute='0'),  # ทุกวัน 03:00
    },
}
```

## Usage Examples

### 1. เพิ่มสินค้าจาก URL

**Python:**
```python
from rpa_bot.product_scraper import ProductScraperService

scraper = ProductScraperService()
tracked_product = scraper.create_or_update_tracked_product(
    product_url="https://www.lazada.co.th/products/iphone-15-pro-max",
    category=ProductCategory.objects.get(slug="smartphones"),
    brand=ProductBrand.objects.get(slug="apple")
)

print(f"Tracked: {tracked_product.title}")
print(f"Price: ฿{tracked_product.current_price}")
```

**JavaScript (API):**
```javascript
const response = await fetch('/api/ecommerce/track-url/', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        product_url: 'https://www.lazada.co.th/products/...',
        enable_price_alert: true,
        target_price: 40000
    })
});

const data = await response.json();
console.log(data.product);
```

### 2. ตั้งค่า Price Alert

**Python:**
```python
product = TrackedProduct.objects.get(id=1)
product.enable_price_alert = True
product.target_price = 40000.00
product.alert_sent = False  # Reset alert status
product.save()
```

**JavaScript (API):**
```javascript
await fetch(`/api/ecommerce/product/${productId}/update/`, {
    method: 'PUT',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        enable_price_alert: true,
        target_price: 40000
    })
});
```

### 3. ดึงประวัติราคา

**Python:**
```python
product = TrackedProduct.objects.get(id=1)
history = product.price_history.all()[:30]  # 30 วันล่าสุด

for h in history:
    print(f"{h.recorded_at}: ฿{h.price}")
```

**JavaScript (API):**
```javascript
const response = await fetch(`/api/ecommerce/price-history/${productId}/`);
const data = await response.json();

// Plot chart with Chart.js
const prices = data.history.map(h => h.price);
const dates = data.history.map(h => h.recorded_at);
```

### 4. อัพเดทราคาทั้งหมด

**Python:**
```python
from rpa_bot.product_scraper import ProductScraperService

scraper = ProductScraperService()
result = scraper.update_all_tracked_products()

print(f"Updated: {result['updated']}")
print(f"Failed: {result['failed']}")
```

## Environment Variables

เพิ่มใน `.env`:

```env
# Telegram Bot (สำหรับ Price Alerts)
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# Celery
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## Price Alert Telegram Setup

1. **สร้าง Telegram Bot:**
   - ติดต่อ @BotFather
   - ใช้คำสั่ง `/newbot`
   - เก็บ Bot Token

2. **หา Chat ID:**
   - ส่งข้อความให้ Bot
   - เข้า `https://api.telegram.org/bot<TOKEN>/getUpdates`
   - คัดลอก Chat ID

3. **ตั้งค่า Environment Variables:**
   ```env
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=987654321
   ```

## Web Interface

### E-Commerce Dashboard
**URL:** `/ecommerce/`

Features:
- สถิติสินค้าที่ติดตาม
- Price Alerts แบบ Real-time
- สินค้าที่ลดราคามากที่สุด
- เพิ่มสินค้าจาก URL
- อัพเดทราคาทั้งหมด

### Product Detail Page
**URL:** `/ecommerce/product/<id>/`

Features:
- ข้อมูลสินค้าแบบละเอียด
- กราฟประวัติราคา (Chart.js)
- ตั้งค่า Price Alert
- สถิติราคา 30 วัน
- ตารางประวัติราคา

### Categories & Brands
- **Categories:** `/ecommerce/categories/`
- **Brands:** `/ecommerce/brands/`

## Best Practices

### 1. Rate Limiting
- อัพเดทราคาไม่เกิน 1 ครั้ง/นาที ต่อสินค้า
- ใช้ Celery Beat สำหรับการอัพเดทอัตโนมัติ
- เพิ่ม delay ระหว่าง requests

### 2. Error Handling
- ตรวจสอบว่า URL ถูกต้อง
- Handle dynamic content (JavaScript-rendered pages)
- Retry failed scraping (max 3 times)

### 3. Data Management
- ลบประวัติราคาเก่า > 90 วัน
- Archive สินค้าที่ไม่มีจำหน่ายแล้ว
- ตั้งค่า is_active=False แทนการลบ

### 4. Performance
- ใช้ select_related() สำหรับ category และ brand
- Index ใน database (platform, is_active, current_price)
- Cache ผลลัพธ์ของ API

## Limitations

1. **Dynamic Content:**
   - หลายเว็บใช้ JavaScript rendering
   - อาจต้องเปลี่ยนเป็น Selenium/Playwright ในอนาคต

2. **Rate Limiting:**
   - Platform อาจมี rate limit
   - แนะนำใช้ proxy rotation สำหรับ scraping มากๆ

3. **CAPTCHA:**
   - บางเว็บมี CAPTCHA protection
   - อาจต้องใช้ CAPTCHA solving service

4. **URL Changes:**
   - Product URL อาจเปลี่ยนแปลงได้
   - แนะนำใช้ Product ID แทน full URL

## Troubleshooting

### ไม่สามารถ scrape ราคาได้

**สาเหตน:**
- Dynamic JavaScript rendering
- CSS selector เปลี่ยนแปลง
- Website block IP

**แก้ไข:**
1. ตรวจสอบ CSS selector ใน `product_scraper.py`
2. ใช้ browser developer tools เพื่อหา selector ใหม่
3. เพิ่ม fallback selectors
4. พิจารณาเปลี่ยนเป็น Selenium

### Price Alert ไม่ทำงาน

**สาเหตน:**
- Telegram Bot Token ผิด
- Chat ID ผิด
- Task ไม่ได้รัน

**แก้ไข:**
1. ตรวจสอบ `.env` file
2. Test Telegram bot ด้วย manual message
3. ตรวจสอบ Celery Beat schedule
4. ดู logs: `celery -A config worker -l info`

### Celery Task ไม่รัน

**สาเหตน:**
- Celery worker ไม่ทำงาน
- Celery beat ไม่ทำงาน
- Redis connection error

**แก้ไข:**
```bash
# Start Celery Worker
celery -A config worker -l info

# Start Celery Beat
celery -A config beat -l info

# Check Redis
redis-cli ping
```

## Migration Guide

### จากระบบเก่า -> ระบบใหม่

1. **Export ข้อมูลเก่า:**
```python
# Export to JSON
old_products = OldProductModel.objects.all()
data = serializers.serialize('json', old_products)
```

2. **Import เข้าระบบใหม่:**
```python
from rpa_bot.models import TrackedProduct, ProductCategory

for old_product in old_data:
    TrackedProduct.objects.create(
        product_url=old_product['url'],
        title=old_product['name'],
        current_price=old_product['price'],
        # ... map fields
    )
```

## Support

สำหรับคำถามและการสนับสนุน:
- GitHub Issues: https://github.com/yourrepo/issues
- Email: support@yourcompany.com
- Documentation: https://docs.yourcompany.com

## License

Copyright © 2025 RPA Bot Manager. All rights reserved.
