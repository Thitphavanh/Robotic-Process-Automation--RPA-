"""
AI Summarizer Service - สรุปข่าวด้วย AI
"""
from datetime import datetime, date
from django.utils import timezone
from .models import NewsArticle, DailyReport


class AISummarizerService:
    """Service สำหรับสรุปข่าวด้วย AI"""

    def __init__(self):
        pass

    def summarize_article(self, article):
        """สรุปบทความเดี่ยว"""
        # TODO: เชื่อมต่อกับ OpenAI API หรือ Local LLM
        # สำหรับตอนนี้ใช้การสรุปแบบง่าย

        try:
            content = article.content
            title = article.title

            # Basic summarization (สามารถเปลี่ยนเป็น AI model ได้)
            summary = f"{title}\n\n{content[:200]}..."

            # อัพเดท article
            article.ai_summary = summary
            article.sentiment = self._analyze_sentiment(content)
            article.save()

            return summary

        except Exception as e:
            print(f"Error summarizing article: {e}")
            return None

    def _analyze_sentiment(self, text):
        """วิเคราะห์ sentiment แบบง่าย"""
        # TODO: ใช้ AI model สำหรับ sentiment analysis

        positive_words = ['เพิ่มขึ้น', 'ดีขึ้น', 'สูงขึ้น', 'กำไร', 'เติบโต', 'up', 'gain', 'profit', 'growth']
        negative_words = ['ลดลง', 'แย่ลง', 'ขาดทุน', 'ตก', 'down', 'loss', 'decline', 'fall']

        text_lower = text.lower()

        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def generate_daily_report(self, report_date=None):
        """สร้างรายงานประจำวัน"""
        if report_date is None:
            report_date = date.today()

        try:
            # หาหรือสร้าง DailyReport
            report, created = DailyReport.objects.get_or_create(
                report_date=report_date
            )

            # ดึงบทความของวันนี้
            today_start = timezone.make_aware(datetime.combine(report_date, datetime.min.time()))
            today_end = timezone.make_aware(datetime.combine(report_date, datetime.max.time()))

            articles = NewsArticle.objects.filter(
                published_at__range=(today_start, today_end)
            )

            # แยกบทความตามหมวด
            stock_thai_articles = articles.filter(source__category='stock_thai')
            stock_foreign_articles = articles.filter(source__category='stock_foreign')
            crypto_articles = articles.filter(source__category='crypto')
            gold_articles = articles.filter(source__category='gold')
            tech_articles = articles.filter(source__category__in=['tech_ai', 'tech_hardware', 'tech_software'])
            football_articles = articles.filter(source__category='football')

            # สรุปแต่ละหมวด
            report.stock_thai_summary = self._summarize_category(
                stock_thai_articles,
                'หุ้นไทย'
            )

            report.stock_foreign_summary = self._summarize_category(
                stock_foreign_articles,
                'หุ้นต่างประเทศ'
            )

            report.crypto_summary = self._summarize_category(
                crypto_articles,
                'Bitcoin และ Cryptocurrency'
            )

            report.gold_summary = self._summarize_category(
                gold_articles,
                'ราคาทองคำ'
            )

            report.tech_summary = self._summarize_category(
                tech_articles,
                'ข่าว Technology'
            )

            report.football_summary = self._summarize_category(
                football_articles,
                'ข่าว Football'
            )

            # สร้างรายงานเต็ม
            report.full_report = self._generate_full_report(report)

            # เพิ่มบทความทั้งหมดเข้า report
            report.articles.set(articles)

            report.is_completed = True
            report.save()

            return report

        except Exception as e:
            print(f"Error generating daily report: {e}")
            return None

    def _summarize_category(self, articles, category_name):
        """สรุปข่าวในหมวดหมู่"""
        if not articles.exists():
            return f"ไม่มีข้อมูล{category_name}ในวันนี้"

        summary_parts = [f"📊 {category_name} - วันที่ {date.today().strftime('%d/%m/%Y')}\n"]

        # Ensure articles are ordered by published_at descending to get the latest
        # and take up to 10 as requested by the user for specific categories.
        # For other categories, it will still take up to 10.
        articles_to_summarize = articles.order_by('-published_at')[:10]

        for article in articles_to_summarize:
            summary_parts.append(f"• {article.title}")
            if article.price:
                summary_parts.append(
                    f"  ราคา: {article.price:,.2f}"
                )
                if article.change_percent:
                    summary_parts.append(f"  เปลี่ยนแปลง: {article.change_percent:.2f}%")
            
            if article.ai_summary:
                summary_parts.append(f"  สรุป: {article.ai_summary}")
            elif article.content: # Fallback to content if no AI summary
                summary_parts.append(f"  เนื้อหา: {article.content[:150]}...")

            summary_parts.append("") # Add an empty line for spacing

        return "\n".join(summary_parts)

    def _generate_full_report(self, report):
        """สร้างรายงานเต็มจากข้อมูลทั้งหมด"""
        full_report = f"""
📰 รายงานข่าวประจำวัน - {report.report_date.strftime('%d/%m/%Y')}
{'='*80}

{report.stock_thai_summary or ''}

{'='*80}

{report.stock_foreign_summary or ''}

{'='*80}

{report.crypto_summary or ''}

{'='*80}

{report.gold_summary or ''}

{'='*80}

{report.tech_summary or ''}

{'='*80}

{report.football_summary or ''}

{'='*80}

🤖 รายงานนี้สร้างโดย RPA Bot Manager
สร้างเมื่อ: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}
"""

        return full_report.strip()

    def send_report(self, report):
        """ส่งรายงาน (Email, LINE, Telegram)"""
        # TODO: เชื่อมต่อกับระบบส่งรายงาน

        try:
            # ตัวอย่าง: พิมพ์รายงาน
            print("="*80)
            print("📨 ส่งรายงานประจำวัน")
            print("="*80)
            print(report.full_report)
            print("="*80)

            # บันทึกว่าส่งแล้ว
            report.is_sent = True
            report.sent_at = timezone.now()
            report.save()

            return True

        except Exception as e:
            print(f"Error sending report: {e}")
            return False

    def summarize_with_ai(self, text, max_length=200):
        """สรุปข้อความด้วย AI (ต่อกับ OpenAI หรือ Local LLM)"""
        # TODO: เชื่อมต่อกับ OpenAI API

        # ตัวอย่าง: ใช้การตัดข้อความง่ายๆ
        if len(text) <= max_length:
            return text

        return text[:max_length] + "..."

    def translate_to_thai(self, text):
        """แปลข้อความเป็นภาษาไทย"""
        # TODO: เชื่อมต่อกับ Translation API
        return text
