# E-Commerce Price Tracking - Quick Start Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Database Migration
```bash
cd /Users/hery/Desktop/Robotic-Process-Automation-\(RPA\)\ /rpa_web
python3 manage.py migrate rpa_bot
```

### Step 2: Create Sample Categories & Brands
```python
python3 manage.py shell

from rpa_bot.models import ProductCategory, ProductBrand

# Create Categories
ProductCategory.objects.create(name="Smartphones", keywords="smartphone,มือถือ,โทรศัพท์")
ProductCategory.objects.create(name="Notebooks", keywords="laptop,โน้ตบุ๊ค,คอมพิวเตอร์")
ProductCategory.objects.create(name="Shoes", keywords="รองเท้า,sneakers,แฟชั่น")

# Create Brands
ProductBrand.objects.create(name="Apple", website="https://www.apple.com")
ProductBrand.objects.create(name="Samsung", website="https://www.samsung.com")
ProductBrand.objects.create(name="Nike", website="https://www.nike.com")

exit()
```

### Step 3: Start Services
```bash
# Terminal 1: Django Server
python3 manage.py runserver

# Terminal 2: Celery Worker
celery -A config worker -l info

# Terminal 3: Celery Beat (optional - for auto updates)
celery -A config beat -l info
```

### Step 4: Open Dashboard
```
http://localhost:8000/ecommerce/
```

### Step 5: Track Your First Product

**Option A: Via Web Interface**
1. Open http://localhost:8000/ecommerce/
2. Paste product URL in "Track Product" box
3. Click "เพิ่มสินค้า"

**Option B: Via API**
```bash
curl -X POST http://localhost:8000/api/ecommerce/track-url/ \
  -H "Content-Type: application/json" \
  -d '{
    "product_url": "https://www.lazada.co.th/products/iphone-15-pro-max-256gb-...",
    "enable_price_alert": true,
    "target_price": 40000
  }'
```

---

## 📝 Example URLs to Try

### Lazada Thailand
```
https://www.lazada.co.th/products/...
```

### Shopee Thailand
```
https://shopee.co.th/...
```

### TikTok Shop
```
https://www.tiktok.com/@shop/...
```

---

## ⚙️ Configure Telegram Alerts (Optional)

### 1. Create Bot
1. Open Telegram, search for @BotFather
2. Send `/newbot`
3. Follow instructions
4. Copy Bot Token

### 2. Get Chat ID
1. Send a message to your bot
2. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
3. Copy `chat.id` from response

### 3. Update .env
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=987654321
```

### 4. Test Alert
```python
python3 manage.py shell

from rpa_bot.models import TrackedProduct

# Get first product
product = TrackedProduct.objects.first()

# Enable price alert
product.enable_price_alert = True
product.target_price = product.current_price - 100  # Set lower than current
product.alert_sent = False
product.save()

# Trigger alert check manually
from rpa_bot.tasks import check_price_alerts
result = check_price_alerts.delay()
print(result.get())
```

---

## 🎯 Common Tasks

### Update All Product Prices
```python
from rpa_bot.product_scraper import ProductScraperService

scraper = ProductScraperService()
result = scraper.update_all_tracked_products()
print(f"Updated: {result['updated']}, Failed: {result['failed']}")
```

### Get Price History
```python
from rpa_bot.models import TrackedProduct

product = TrackedProduct.objects.first()
history = product.price_history.all()[:10]

for h in history:
    print(f"{h.recorded_at}: ฿{h.price}")
```

### Check Active Alerts
```python
from rpa_bot.models import TrackedProduct

alerts = TrackedProduct.objects.filter(
    enable_price_alert=True,
    is_active=True,
    alert_sent=False
)

for product in alerts:
    if product.current_price <= product.target_price:
        print(f"ALERT: {product.title} - ฿{product.current_price}")
```

---

## 🔧 Troubleshooting

### Celery Not Working?
```bash
# Check Redis is running
redis-cli ping
# Should return: PONG

# If Redis not installed:
brew install redis  # macOS
sudo apt install redis-server  # Ubuntu

# Start Redis
redis-server
```

### Can't Scrape Product?
- Check URL is correct
- Platform may require JavaScript rendering
- Try with different product
- Check logs for errors

### Telegram Not Sending?
- Verify bot token in .env
- Verify chat ID in .env
- Test bot manually in Telegram
- Check Celery worker logs

---

## 📚 Next Steps

1. **Read Full Documentation:** `docs/ECOMMERCE_TRACKING.md`
2. **Set Up Celery Beat:** For automatic price updates
3. **Configure Telegram:** For price alerts
4. **Add More Products:** Track your favorite items
5. **Explore API:** Build integrations

---

## 🎉 Success!

You now have a fully functional E-Commerce price tracking system!

**Dashboard:** http://localhost:8000/ecommerce/
**API Docs:** `docs/ECOMMERCE_TRACKING.md`

Enjoy tracking prices! 🛍️📊
