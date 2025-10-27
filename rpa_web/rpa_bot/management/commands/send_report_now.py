"""
Django Management Command to manually trigger the daily news intelligence report.
"""
from django.core.management.base import BaseCommand
from rpa_bot.tasks import scrape_all_news, generate_daily_report
from rpa_bot.ai_summarizer import AISummarizerService
from rpa_bot.models import DailyReport
from datetime import date

class Command(BaseCommand):
    """Manually triggers the report generation and sending process."""
    help = 'Manually scrapes, generates, and sends the daily news report to Telegram, bypassing the is_sent check.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🤖 Manually triggering report process...'))

        try:
            # Step 1: Scrape all news
            self.stdout.write(self.style.SUCCESS('Step 1/3: Scraping news...'))
            scrape_result = scrape_all_news()
            if not scrape_result.get('success'):
                raise Exception(f"News scraping failed: {scrape_result.get('error')}")
            self.stdout.write(self.style.SUCCESS('✅ News scraping completed.'))

            # Step 2: Generate the report
            self.stdout.write(self.style.SUCCESS('Step 2/3: Generating daily report...'))
            # The generate_daily_report task from tasks.py returns a dict, not the object.
            # We need to get the report object ourselves.
            generate_result = generate_daily_report()
            if not generate_result.get('success'):
                raise Exception(f"Report generation failed: {generate_result.get('error')}")
            
            report_id = generate_result.get('report_id')
            report = DailyReport.objects.get(id=report_id)
            self.stdout.write(self.style.SUCCESS(f'✅ Report generated successfully (ID: {report.id}).'))

            # Step 3: Send the report directly
            self.stdout.write(self.style.SUCCESS('Step 3/3: Sending report to Telegram...'))
            summarizer = AISummarizerService()
            send_success = summarizer.send_report(report)

            if send_success:
                self.stdout.write(self.style.SUCCESS('✅ Report sent successfully to Telegram!'))
            else:
                raise Exception("Failed to send report to Telegram.")

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An unexpected error occurred: {e}'))
