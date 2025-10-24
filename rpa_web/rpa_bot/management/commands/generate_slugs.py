from django.core.management.base import BaseCommand
from django.utils.text import slugify
from rpa_bot.models import RPATask, NewsArticle, DailyReport


class Command(BaseCommand):
    help = 'Generate slugs for existing records'

    def handle(self, *args, **options):
        # Generate slugs for RPATasks
        tasks_updated = 0
        for task in RPATask.objects.filter(slug__isnull=True):
            base_slug = slugify(task.name, allow_unicode=True)
            slug = base_slug
            counter = 1
            while RPATask.objects.filter(slug=slug).exclude(pk=task.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            task.slug = slug
            task.save()
            tasks_updated += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated slugs for {tasks_updated} RPATask(s)')
        )

        # Generate slugs for NewsArticles
        articles_updated = 0
        for article in NewsArticle.objects.filter(slug__isnull=True):
            base_slug = slugify(article.title, allow_unicode=True)
            slug = base_slug
            counter = 1
            while NewsArticle.objects.filter(slug=slug).exclude(pk=article.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            article.slug = slug
            article.save()
            articles_updated += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated slugs for {articles_updated} NewsArticle(s)')
        )

        # Generate slugs for DailyReports
        reports_updated = 0
        for report in DailyReport.objects.filter(slug__isnull=True):
            slug = slugify(f"report-{report.report_date}", allow_unicode=True)
            report.slug = slug
            report.save()
            reports_updated += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated slugs for {reports_updated} DailyReport(s)')
        )

        self.stdout.write(
            self.style.SUCCESS('✅ All slugs generated successfully!')
        )
