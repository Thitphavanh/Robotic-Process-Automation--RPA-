"""
Celery Tasks สำหรับ RPA และ News Intelligence
"""
from celery import shared_task
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)


@shared_task(name='rpa_bot.tasks.run_rpa_task')
def run_rpa_task_async(task_id):
    """รัน RPA Task แบบ Async"""
    from .models import RPATask
    from .rpa_runner import run_rpa_task

    try:
        task = RPATask.objects.get(pk=task_id)
        logger.info(f"Starting RPA Task: {task.name} (ID: {task_id})")

        run_rpa_task(task)

        logger.info(f"RPA Task completed: {task.name} (ID: {task_id})")
        return {
            'success': True,
            'task_id': task_id,
            'status': task.status
        }

    except RPATask.DoesNotExist:
        logger.error(f"RPA Task not found: ID {task_id}")
        return {
            'success': False,
            'error': 'Task not found'
        }

    except Exception as e:
        logger.error(f"Error running RPA Task {task_id}: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@shared_task(name='rpa_bot.tasks.scrape_all_news')
def scrape_all_news():
    """ดึงข้อมูลข่าวทุกหมวดหมู่ - Task สำหรับ Celery Beat"""
    from .news_scraper import NewsScraperService

    try:
        logger.info("🔍 Starting news scraping task...")

        scraper = NewsScraperService()

        # ดึงข้อมูลทุกหมวด
        articles_by_category = scraper.scrape_all_categories()

        # บันทึกลงฐานข้อมูล
        saved_articles = scraper.save_articles(articles_by_category)

        logger.info(f"✅ News scraping completed! Saved {len(saved_articles)} articles")

        return {
            'success': True,
            'articles_count': len(saved_articles),
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Error scraping news: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@shared_task(name='rpa_bot.tasks.generate_daily_report')
def generate_daily_report():
    """สร้างรายงานประจำวัน - Task สำหรับ Celery Beat"""
    from .ai_summarizer import AISummarizerService
    from .models import NewsArticle

    try:
        logger.info("📊 Starting daily report generation...")

        summarizer = AISummarizerService()

        # สร้าง AI Summary สำหรับบทความที่ยังไม่มี (ใช้ scraped_at เพื่อได้ข่าวที่ scrape วันนี้)
        articles_without_summary = NewsArticle.objects.filter(
            ai_summary__isnull=True,
            scraped_at__date=date.today()
        )

        for article in articles_without_summary[:50]:  # จำกัดไว้ 50 บทความต่อครั้ง
            summarizer.summarize_article(article)

        # สร้างรายงานประจำวัน
        report = summarizer.generate_daily_report()

        if report:
            logger.info(f"✅ Daily report generated successfully for {report.report_date}")

            return {
                'success': True,
                'report_id': report.id,
                'report_date': report.report_date.isoformat()
            }
        else:
            logger.error("❌ Failed to generate daily report")
            return {
                'success': False,
                'error': 'Report generation failed'
            }

    except Exception as e:
        logger.error(f"❌ Error generating daily report: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@shared_task(name='rpa_bot.tasks.send_daily_report')
def send_daily_report():
    """ส่งรายงานประจำวัน - Task สำหรับ Celery Beat (ส่งซ้ำได้ทุก 10 นาที)"""
    from .ai_summarizer import AISummarizerService
    from .models import DailyReport

    try:
        logger.info("📨 Starting daily report sending...")

        # หารายงานวันนี้ที่เสร็จแล้ว (ไม่สนใจว่าส่งไปแล้วหรือยัง)
        # เพื่อให้สามารถส่งซ้ำทุก 10 นาทีตามตารางใหม่
        report = DailyReport.objects.filter(
            report_date=date.today(),
            is_completed=True
        ).order_by('-updated_at').first()

        if not report:
            logger.warning("⚠️ No completed report found to send today")
            return {
                'success': False,
                'error': 'No completed report found'
            }

        summarizer = AISummarizerService()
        success = summarizer.send_report(report)

        if success:
            logger.info(f"✅ Daily report sent successfully for {report.report_date}")
            return {
                'success': True,
                'report_id': report.id,
                'sent_at': report.sent_at.isoformat()
            }
        else:
            logger.error("❌ Failed to send daily report")
            return {
                'success': False,
                'error': 'Report sending failed'
            }

    except Exception as e:
        logger.error(f"❌ Error sending daily report: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@shared_task(name='rpa_bot.tasks.daily_news_intelligence')
def daily_news_intelligence():
    """
    Task หลักสำหรับ Daily News Intelligence.
    1. ดึงข้อมูลข่าว
    2. สร้างรายงาน
    3. ส่งรายงาน (โดยตรง)
    """
    from .models import DailyReport
    from .ai_summarizer import AISummarizerService

    try:
        logger.info("🤖 Starting Daily News Intelligence Bot...")

        # Step 1: ดึงข้อมูลข่าว
        logger.info("Step 1/3: Scraping news...")
        scrape_result = scrape_all_news()
        if not scrape_result.get('success'):
            raise Exception(f"News scraping failed: {scrape_result.get('error')}")
        logger.info("✅ News scraping completed.")

        # Step 2: สร้างรายงาน
        logger.info("Step 2/3: Generating report...")
        generate_result = generate_daily_report()
        if not generate_result.get('success'):
            raise Exception(f"Report generation failed: {generate_result.get('error')}")
        
        report_id = generate_result.get('report_id')
        report = DailyReport.objects.get(id=report_id)
        logger.info(f"✅ Report generated successfully (ID: {report.id}).")

        # Step 3: ส่งรายงานโดยตรง
        logger.info("Step 3/3: Sending report directly...")
        summarizer = AISummarizerService()
        send_success = summarizer.send_report(report)

        if not send_success:
            raise Exception("Failed to send report to Telegram.")

        logger.info("✅ Daily News Intelligence completed successfully!")

        return {
            'success': True,
            'scrape_result': scrape_result,
            'report_result': generate_result,
            'send_success': send_success,
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Daily News Intelligence failed: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@shared_task(name='rpa_bot.tasks.cleanup_old_articles')
def cleanup_old_articles(days=30):
    """ลบบทความเก่าที่เกิน X วัน (ใช้ scraped_at)"""
    from .models import NewsArticle
    from datetime import timedelta

    try:
        cutoff_date = datetime.now() - timedelta(days=days)

        deleted_count, _ = NewsArticle.objects.filter(
            scraped_at__lt=cutoff_date
        ).delete()

        logger.info(f"🗑️ Cleaned up {deleted_count} old articles")

        return {
            'success': True,
            'deleted_count': deleted_count
        }

    except Exception as e:
        logger.error(f"❌ Error cleaning up articles: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


# ========== E-Commerce Price Tracking Tasks ==========


@shared_task(name='rpa_bot.tasks.update_tracked_products')
def update_tracked_products():
    """
    อัพเดทราคาสินค้าที่ติดตามทั้งหมด - Task สำหรับ Celery Beat
    รันทุก 6 ชั่วโมงเพื่ออัพเดทราคาและบันทึกประวัติ
    """
    from .product_scraper import ProductScraperService
    from .models import TrackedProduct

    try:
        logger.info("🛒 Starting tracked products update...")

        scraper = ProductScraperService()
        result = scraper.update_all_tracked_products()

        logger.info(f"✅ Tracked products update completed! Updated {result['updated']} products")

        return {
            'success': True,
            'updated': result['updated'],
            'failed': result['failed'],
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Error updating tracked products: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@shared_task(name='rpa_bot.tasks.check_price_alerts')
def check_price_alerts():
    """
    ตรวจสอบและส่งการแจ้งเตือนราคา - Task สำหรับ Celery Beat
    รันทุกชั่วโมงเพื่อตรวจสอบว่ามีสินค้าที่ถึงราคาเป้าหมายหรือไม่
    """
    from .models import TrackedProduct
    import os

    try:
        logger.info("🔔 Starting price alerts check...")

        # หาสินค้าที่เปิด price alert และยังไม่ได้ส่งการแจ้งเตือน
        alerts = TrackedProduct.objects.filter(
            enable_price_alert=True,
            is_active=True,
            alert_sent=False
        ).select_related('category', 'brand')

        triggered_alerts = []

        for product in alerts:
            # ตรวจสอบว่าราคาถึง target หรือไม่
            if product.target_price and product.current_price:
                if product.current_price <= product.target_price:
                    # ส่งการแจ้งเตือน (ถ้ามี Telegram Bot Token)
                    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
                    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

                    if telegram_token and telegram_chat_id:
                        send_price_alert_telegram(product, telegram_token, telegram_chat_id)

                    # Mark as sent
                    product.alert_sent = True
                    product.save()

                    triggered_alerts.append({
                        'product_id': product.id,
                        'title': product.title,
                        'current_price': float(product.current_price),
                        'target_price': float(product.target_price)
                    })

        logger.info(f"✅ Price alerts check completed! Triggered {len(triggered_alerts)} alerts")

        return {
            'success': True,
            'triggered_alerts': triggered_alerts,
            'count': len(triggered_alerts),
            'timestamp': datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"❌ Error checking price alerts: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


def send_price_alert_telegram(product, bot_token, chat_id):
    """ส่งการแจ้งเตือนราคาผ่าน Telegram"""
    import requests

    try:
        message = f"""
🔔 **Price Alert!**

**สินค้า:** {product.title}
**แพลตฟอร์ม:** {product.get_platform_display()}
{'**หมวดหมู่:** ' + product.category.name if product.category else ''}
{'**แบรนด์:** ' + product.brand.name if product.brand else ''}

💰 **ราคาปัจจุบัน:** ฿{product.current_price:,.2f}
🎯 **ราคาเป้าหมาย:** ฿{product.target_price:,.2f}
📉 **ประหยัด:** ฿{(product.target_price - product.current_price):,.2f}

🔗 **ลิงก์สินค้า:** {product.product_url}

⏰ **ตรวจสอบเมื่อ:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()

        logger.info(f"✅ Price alert sent for product: {product.title}")
        return True

    except Exception as e:
        logger.error(f"❌ Error sending Telegram price alert: {str(e)}")
        return False


@shared_task(name='rpa_bot.tasks.cleanup_old_price_history')
def cleanup_old_price_history(days=90):
    """
    ลบประวัติราคาเก่าที่เกิน X วัน - Task สำหรับ Celery Beat
    รันทุกวันเพื่อลดขนาดฐานข้อมูล
    """
    from .models import PriceHistory
    from datetime import timedelta

    try:
        cutoff_date = datetime.now() - timedelta(days=days)

        deleted_count, _ = PriceHistory.objects.filter(
            recorded_at__lt=cutoff_date
        ).delete()

        logger.info(f"🗑️ Cleaned up {deleted_count} old price history records")

        return {
            'success': True,
            'deleted_count': deleted_count
        }

    except Exception as e:
        logger.error(f"❌ Error cleaning up price history: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


@shared_task(name='rpa_bot.tasks.track_product_by_url')
def track_product_by_url(product_url, category_id=None, brand_id=None, user_id=None):
    """
    Task สำหรับเพิ่มสินค้าจาก URL แบบ Async
    ใช้เมื่อต้องการ scrape สินค้าใหม่โดยไม่ block request
    """
    from .product_scraper import ProductScraperService
    from .models import ProductCategory, ProductBrand
    from django.contrib.auth import get_user_model

    try:
        logger.info(f"🛍️ Starting to track product from URL: {product_url}")

        scraper = ProductScraperService()

        # Get related objects
        category = ProductCategory.objects.filter(id=category_id).first() if category_id else None
        brand = ProductBrand.objects.filter(id=brand_id).first() if brand_id else None
        user = get_user_model().objects.filter(id=user_id).first() if user_id else None

        # Create or update tracked product
        tracked_product = scraper.create_or_update_tracked_product(
            product_url=product_url,
            category=category,
            brand=brand,
            user=user
        )

        logger.info(f"✅ Product tracked successfully: {tracked_product.title}")

        return {
            'success': True,
            'product_id': tracked_product.id,
            'title': tracked_product.title,
            'current_price': float(tracked_product.current_price) if tracked_product.current_price else None
        }

    except Exception as e:
        logger.error(f"❌ Error tracking product from URL: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
