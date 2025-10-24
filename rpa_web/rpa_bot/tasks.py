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

        # สร้าง AI Summary สำหรับบทความที่ยังไม่มี
        articles_without_summary = NewsArticle.objects.filter(
            ai_summary__isnull=True,
            published_at__date=date.today()
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
    """ส่งรายงานประจำวัน - Task สำหรับ Celery Beat"""
    from .ai_summarizer import AISummarizerService
    from .models import DailyReport

    try:
        logger.info("📨 Starting daily report sending...")

        # หารายงานวันนี้ที่ยังไม่ได้ส่ง
        report = DailyReport.objects.filter(
            report_date=date.today(),
            is_completed=True,
            is_sent=False
        ).first()

        if not report:
            logger.warning("⚠️ No report found to send today")
            return {
                'success': False,
                'error': 'No report found'
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
    Task หลักสำหรับ Daily News Intelligence
    ทำงานทุกวันเวลา 10:00 น.
    1. ดึงข้อมูลข่าว
    2. สร้างรายงาน
    3. ส่งรายงาน
    """
    try:
        logger.info("🤖 Starting Daily News Intelligence Bot...")

        # Step 1: ดึงข้อมูลข่าว
        logger.info("Step 1/3: Scraping news...")
        scrape_result = scrape_all_news()

        if not scrape_result.get('success'):
            raise Exception(f"News scraping failed: {scrape_result.get('error')}")

        # Step 2: สร้างรายงาน
        logger.info("Step 2/3: Generating report...")
        report_result = generate_daily_report()

        if not report_result.get('success'):
            raise Exception(f"Report generation failed: {report_result.get('error')}")

        # Step 3: ส่งรายงาน
        logger.info("Step 3/3: Sending report...")
        send_result = send_daily_report()

        if not send_result.get('success'):
            raise Exception(f"Report sending failed: {send_result.get('error')}")

        logger.info("✅ Daily News Intelligence completed successfully!")

        return {
            'success': True,
            'scrape_result': scrape_result,
            'report_result': report_result,
            'send_result': send_result,
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
    """ลบบทความเก่าที่เกิน X วัน"""
    from .models import NewsArticle
    from datetime import timedelta

    try:
        cutoff_date = datetime.now() - timedelta(days=days)

        deleted_count, _ = NewsArticle.objects.filter(
            published_at__lt=cutoff_date
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
