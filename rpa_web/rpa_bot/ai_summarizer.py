"""
AI Summarizer Service - สรุปข่าวด้วย AI
"""
from datetime import datetime, date
from django.utils import timezone
from .models import NewsArticle, DailyReport
import os


class AISummarizerService:
    """Service สำหรับสรุปข่าวด้วย AI"""

    def __init__(self):
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY', '')
        self.use_gemini = bool(self.gemini_api_key)

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
            stock_us_articles = articles.filter(source__category='stock_us')
            stock_europe_articles = articles.filter(source__category='stock_europe')
            stock_china_articles = articles.filter(source__category='stock_china')
            crypto_articles = articles.filter(source__category='crypto')
            gold_articles = articles.filter(source__category='gold')
            tech_articles = articles.filter(source__category__in=['tech_ai', 'tech_hardware', 'tech_software'])
            football_articles = articles.filter(source__category='football')

            # สรุปแต่ละหมวด
            report.stock_thai_summary = self._summarize_category(
                stock_thai_articles,
                'หุ้นไทย - 10 บริษัทล่าสุด'
            )

            report.stock_us_summary = self._summarize_category(
                stock_us_articles,
                'หุ้นอเมริกา - 10 บริษัทล่าสุด'
            )

            report.stock_europe_summary = self._summarize_category(
                stock_europe_articles,
                'หุ้นยุโรป - 10 บริษัทล่าสุด'
            )

            report.stock_china_summary = self._summarize_category(
                stock_china_articles,
                'หุ้นจีน - 10 บริษัทล่าสุด'
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

{report.stock_us_summary or ''}

{'='*80}

{report.stock_europe_summary or ''}

{'='*80}

{report.stock_china_summary or ''}

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

    def generate_detailed_analysis(self, article):
        """สร้างการวิเคราะห์แบบละเอียดด้วย Gemini AI"""
        if not self.use_gemini:
            return self._generate_basic_analysis(article)

        try:
            import google.generativeai as genai

            # Configure Gemini API
            genai.configure(api_key=self.gemini_api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            # สร้าง prompt ตามหมวดหมู่
            prompt = self._create_analysis_prompt(article)

            # Generate analysis
            response = model.generate_content(prompt)

            # Format the report
            analysis_report = self._format_analysis_report(
                article=article,
                analysis_text=response.text,
                model_name='gemini-2.0-flash-exp'
            )

            return analysis_report

        except Exception as e:
            print(f"Error generating Gemini analysis: {e}")
            return self._generate_basic_analysis(article)

    def _create_analysis_prompt(self, article):
        """สร้าง prompt สำหรับการวิเคราะห์ตามหมวดหมู่"""
        category = article.source.category
        title = article.title
        content = article.content
        price = article.price
        change = article.change
        change_percent = article.change_percent

        base_info = f"""
หัวข้อข่าว: {title}
เนื้อหา: {content}
"""

        if price:
            base_info += f"""
ราคาปัจจุบัน: {price}
การเปลี่ยนแปลง: {change if change else 'N/A'}
% เปลี่ยนแปลง: {change_percent if change_percent else 'N/A'}%
"""

        # Prompts แบ่งตามหมวดหมู่
        if 'stock' in category:
            market_name = {
                'stock_thai': 'ตลาดหุ้นไทย',
                'stock_us': 'ตลาดหุ้นอเมริกา',
                'stock_europe': 'ตลาดหุ้นยุโรป',
                'stock_china': 'ตลาดหุ้นจีน'
            }.get(category, 'ตลาดหุ้น')

            prompt = f"""{base_info}

วิเคราะห์{market_name}จากข้อมูลข้างต้น โดยพิจารณา:

### **1. บทสรุปสำหรับผู้บริหาร (Executive Summary)**
- สรุปภาพรวมสถานการณ์ปัจจุบัน

### **2. การวิเคราะห์ราคาและการเปลี่ยนแปลง**
- ทิศทางราคา
- ปัจจัยที่ส่งผลต่อราคา

### **3. ปัจจัยพื้นฐาน (Fundamentals)**
- ข้อมูลสำคัญของบริษัท/ตลาด
- ผลประกอบการ

### **4. การวิเคราะห์ทางเทคนิค (Technical Analysis)**
- แนวรับ-แนวต้าน
- แนวโน้มราคา

### **5. แนวโน้มและคาดการณ์**
- ระยะสั้น (1-3 เดือน)
- ระยะกลาง (6-12 เดือน)
- ระยะยาว

### **6. ข้อควรระวังและความเสี่ยง**
- ความเสี่ยงที่สำคัญ
- สิ่งที่นักลงทุนควรระวัง

### **7. คำแนะนำการลงทุน**
- กลยุทธ์ที่แนะนำ
- จุดเข้า-ออก

ตอบเป็นภาษาไทยอย่างละเอียดและเป็นมืออาชีพ"""

        elif category == 'crypto':
            prompt = f"""{base_info}

วิเคราะห์ Cryptocurrency จากข้อมูลข้างต้น โดยพิจารณา:

### **1. บทสรุปสำหรับผู้บริหาร**
- ภาพรวมตลาด Crypto ปัจจุบัน

### **2. การวิเคราะห์ราคา**
- การเคลื่อนไหวของราคา
- Market Cap และ Volume

### **3. ปัจจัยขับเคลื่อน**
- ข่าวและเหตุการณ์สำคัญ
- Adoption และ Regulations

### **4. การวิเคราะห์ On-Chain**
- Whale Activity
- Network Activity

### **5. แนวโน้มและคาดการณ์**
- ระยะสั้น, กลาง, ยาว

### **6. ความเสี่ยง**
- Volatility
- Regulatory Risk
- Security Risk

### **7. คำแนะนำ**
- กลยุทธ์การลงทุน
- Risk Management

ตอบเป็นภาษาไทยอย่างละเอียด"""

        elif 'tech' in category or category in ['ev_car', 'rocket_space']:
            tech_type = {
                'tech_ai': 'AI และ Machine Learning',
                'tech_hardware': 'Hardware และ Semiconductor',
                'tech_software': 'Software และ Cloud',
                'ev_car': 'รถยนต์ไฟฟ้า (EV)',
                'rocket_space': 'เทคโนโลยีอวกาศและจรวด'
            }.get(category, 'เทคโนโลยี')

            prompt = f"""{base_info}

วิเคราะห์ข่าว{tech_type}จากข้อมูลข้างต้น โดยพิจารณา:

### **1. บทสรุปสำหรับผู้บริหาร**
- ภาพรวมข่าวและความสำคัญ

### **2. การวิเคราะห์เทคโนโลยี**
- นวัตกรรมและเทคโนโลยีใหม่
- ความก้าวหน้าทางเทคนิค

### **3. ผลกระทบต่ออุตสาหกรรม**
- Impact ต่อ Market
- การแข่งขัน

### **4. โอกาสทางธุรกิจ**
- Business Opportunities
- Market Growth

### **5. แนวโน้มอนาคต**
- Future Trends
- Predictions

### **6. ความท้าทาย**
- Technical Challenges
- Adoption Barriers

### **7. สรุปและข้อเสนอแนะ**
- Key Takeaways
- Recommendations

ตอบเป็นภาษาไทยอย่างละเอียดและเป็นมืออาชีพ"""

        elif category == 'football':
            prompt = f"""{base_info}

วิเคราะห์ข่าวฟุตบอลจากข้อมูลข้างต้น โดยพิจารณา:

### **1. บทสรุปข่าว**
- สรุปเหตุการณ์สำคัญ

### **2. การวิเคราะห์**
- วิเคราะห์ทีม/ผลการแข่งขัน
- จุดแข็ง-จุดอ่อน

### **3. สถิติและข้อมูล**
- ตัวเลขที่น่าสนใจ
- ประวัติการพบกัน

### **4. ผลกระทบ**
- Impact ต่อตารางคะแนน
- โอกาสในการแข่งขัน

### **5. แนวโน้มและคาดการณ์**
- คาดการณ์ผลการแข่งขันต่อไป

ตอบเป็นภาษาไทยอย่างสนุกและเข้าใจง่าย"""

        else:  # gold หรืออื่นๆ
            prompt = f"""{base_info}

วิเคราะห์ข่าวจากข้อมูลข้างต้น โดยพิจารณา:

### **1. บทสรุปสำหรับผู้บริหาร**
- ภาพรวมสถานการณ์

### **2. การวิเคราะห์**
- ปัจจัยสำคัญ
- การเปลี่ยนแปลง

### **3. ผลกระทบ**
- Impact Analysis

### **4. แนวโน้ม**
- คาดการณ์อนาคต

### **5. ข้อควรระวัง**
- Risks and Warnings

### **6. คำแนะนำ**
- Recommendations

ตอบเป็นภาษาไทยอย่างละเอียด"""

        return prompt

    def _format_analysis_report(self, article, analysis_text, model_name):
        """จัดรูปแบบรายงานการวิเคราะห์"""
        current_time = timezone.now()

        report = f"""================================================================================
🤖 Stock Bot Gemini AI - Text Analysis Report
================================================================================

📅 วันที่: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
🤖 AI Model: {model_name}
📋 หมวดหมู่: {article.source.get_category_display()}
📰 แหล่งข้อมูล: {article.source.name}

================================================================================
📝 หัวข้อข่าว:
================================================================================
{article.title}

================================================================================
📊 ข้อมูลราคา/การเปลี่ยนแปลง:
================================================================================
"""

        if article.price:
            report += f"💰 ราคาปัจจุบัน: {article.price:,.2f}\n"
            if article.change:
                symbol = "📈" if article.change >= 0 else "📉"
                report += f"{symbol} การเปลี่ยนแปลง: {article.change:+,.2f}\n"
            if article.change_percent:
                symbol = "📈" if article.change_percent >= 0 else "📉"
                report += f"{symbol} % เปลี่ยนแปลง: {article.change_percent:+.2f}%\n"
        else:
            report += "ไม่มีข้อมูลราคา\n"

        report += f"""
================================================================================
🔍 ผลการวิเคราะห์โดย AI:
================================================================================
{analysis_text}

================================================================================
🤖 รายงานนี้สร้างโดย RPA Bot Manager with Gemini AI
สร้างเมื่อ: {current_time.strftime('%d/%m/%Y %H:%M:%S')}
================================================================================
"""

        return report

    def _generate_basic_analysis(self, article):
        """สร้างการวิเคราะห์แบบพื้นฐาน (ไม่ใช้ AI)"""
        current_time = timezone.now()

        report = f"""================================================================================
📊 Basic Analysis Report
================================================================================

📅 วันที่: {current_time.strftime('%Y-%m-%d %H:%M:%S')}
📋 หมวดหมู่: {article.source.get_category_display()}

================================================================================
📝 หัวข้อข่าว:
================================================================================
{article.title}

================================================================================
📊 ข้อมูล:
================================================================================
{article.content}

================================================================================
💡 หมายเหตุ:
================================================================================
การวิเคราะห์แบบละเอียดต้องการ Gemini API Key
กรุณาตั้งค่า GEMINI_API_KEY ใน environment variables

================================================================================
"""

        return report
