import webbrowser
import time
import os
import pyautogui
from PIL import ImageGrab
import google.generativeai as genai
import dotenv

dotenv.load_dotenv()

# ============================================
# Stock Bot - Thai Stock Market Web Automation
# เปิดและถ่ายภาพเว็บไซต์ตลาดหุ้นไทยแต่ละเว็บ
# ============================================

# --- Configuration ---
print("=" * 80)
print("🤖 Stock Bot - Thai Stock Market Web Automation")
print("=" * 80)
print("📊 เปิดและถ่ายภาพเว็บไซต์ตลาดหุ้นไทยทั้งหมด")
print("=" * 80)

# ตั้งค่า API Key สำหรับวิเคราะห์ (Optional)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
use_ai_analysis = False

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        test_response = model.generate_content("สวัสดี ตอบสั้นๆ")
        print("✅ เชื่อมต่อ Google Gemini API สำเร็จ - จะมีการวิเคราะห์ภาพด้วย AI")
        use_ai_analysis = True
    except:
        print("⚠️  ไม่สามารถเชื่อมต่อ Gemini API - จะถ่ายภาพอย่างเดียว")
else:
    print("ℹ️  ไม่พบ Gemini API Key - จะถ่ายภาพเว็บไซต์เท่านั้น")

print("=" * 80)

# --- รายการเว็บไซต์ตลาดหุ้นไทย ---
THAI_STOCK_WEBSITES = [
    {
        "name": "SET - ภาพรวมดัชนี",
        "url": "https://www.set.or.th/th/market/index/set/overview",
        "description": "ตลาดหลักทรัพย์แห่งประเทศไทย - ภาพรวมดัชนี SET",
        "wait_time": 8
    },
    {
        "name": "SETTRADE - สรุปภาวะตลาด",
        "url": "https://www.settrade.com/th/market/overview",
        "description": "SETTRADE - สรุปภาพรวมตลาดหุ้นไทย",
        "wait_time": 8
    },
    {
        "name": "Investing.com - SET Index",
        "url": "https://th.investing.com/indices/thailand-set",
        "description": "Investing.com - ดัชนีตลาดหลักทรัพย์ SET",
        "wait_time": 7
    },
    {
        "name": "SET - ราคาหลักทรัพย์",
        "url": "https://www.set.or.th/th/market/product/stock/quote",
        "description": "ตลาดหลักทรัพย์แห่งประเทศไทย - ค้นหาราคาหลักทรัพย์",
        "wait_time": 7
    },
    {
        "name": "RYT9 - ข่าวหุ้นไทย",
        "url": "https://www.ryt9.com/th/tag/%E0%B8%AB%E0%B8%B8%E0%B9%89%E0%B8%99%E0%B9%84%E0%B8%97%E0%B8%A2",
        "description": "RYT9 - ข่าวหุ้นไทยล่าสุด",
        "wait_time": 6
    },
    {
        "name": "Investing.com - SET50",
        "url": "https://th.investing.com/indices/set-50",
        "description": "Investing.com - ดัชนี SET50",
        "wait_time": 7
    },
    {
        "name": "TradingView - SET",
        "url": "https://th.tradingview.com/symbols/SET-SET/",
        "description": "TradingView - ชาร์ตและราคาของดัชนี SET",
        "wait_time": 8
    },
    {
        "name": "SET - ดัชนี SET100",
        "url": "https://www.set.or.th/th/market/index/set100/overview",
        "description": "ตลาดหลักทรัพย์แห่งประเทศไทย - ภาพรวมดัชนี SET100",
        "wait_time": 7
    },
    {
        "name": "SETTRADE - Top 20",
        "url": "https://www.settrade.com/th/market/overview/top-20",
        "description": "SETTRADE - หุ้น Top 20 ที่มีมูลค่าซื้อขายสูงสุด",
        "wait_time": 7
    },
    {
        "name": "XTB - หุ้นต่างประเทศ",
        "url": "https://www.xtb.com/th",
        "description": "XTB - แพลตฟอร์มเทรดหุ้นต่างประเทศ",
        "wait_time": 6
    }
]

# --- ถามผู้ใช้ว่าต้องการเปิดเว็บไซต์ใดบ้าง ---
print("\n📋 เว็บไซต์ที่มีให้เลือก:")
for i, website in enumerate(THAI_STOCK_WEBSITES, 1):
    print(f"   {i}. {website['name']}")
    print(f"      URL: {website['url']}")
    print(f"      คำอธิบาย: {website['description']}")
    print()

print("🔢 เลือกเว็บไซต์ที่ต้องการเปิด:")
print("   - พิมพ์ตัวเลข (เช่น 1,2,3 หรือ 1-5)")
print("   - พิมพ์ 'all' เพื่อเปิดทุกเว็บไซต์")
print("   - กด Enter เพื่อเปิดเว็บไซต์หลัก 5 เว็บแรก")

choice = input("\n🎯 คุณเลือก: ").strip().lower()

# ประมวลผลตัวเลือก
selected_websites = []

if choice == "" or choice == "all":
    if choice == "all":
        selected_websites = THAI_STOCK_WEBSITES
        print(f"✅ เลือกทุกเว็บไซต์ ({len(selected_websites)} เว็บ)")
    else:
        selected_websites = THAI_STOCK_WEBSITES[:5]
        print(f"✅ เลือกเว็บไซต์หลัก 5 เว็บแรก")
else:
    # แปลง input เป็น list ของ index
    try:
        if '-' in choice:
            # Range (เช่น 1-5)
            start, end = choice.split('-')
            indices = range(int(start), int(end) + 1)
        elif ',' in choice:
            # Multiple (เช่น 1,2,5)
            indices = [int(x.strip()) for x in choice.split(',')]
        else:
            # Single (เช่น 1)
            indices = [int(choice)]

        selected_websites = [THAI_STOCK_WEBSITES[i-1] for i in indices if 1 <= i <= len(THAI_STOCK_WEBSITES)]
        print(f"✅ เลือก {len(selected_websites)} เว็บไซต์")
    except:
        print("❌ รูปแบบไม่ถูกต้อง - ใช้ค่าเริ่มต้น (5 เว็บแรก)")
        selected_websites = THAI_STOCK_WEBSITES[:5]

if not selected_websites:
    print("❌ ไม่มีเว็บไซต์ที่เลือก")
    exit(1)

print("\n" + "=" * 80)
print(f"🚀 เริ่มเปิดและถ่ายภาพ {len(selected_websites)} เว็บไซต์")
print("=" * 80)

# สร้างโฟลเดอร์สำหรับเก็บภาพ
screenshot_folder = "thai_stock_screenshots"
os.makedirs(screenshot_folder, exist_ok=True)

# --- ฟังก์ชันถ่ายภาพ ---
def capture_screenshot(filename):
    """ถ่ายภาพหน้าจอทั้งหมด"""
    try:
        screenshot = ImageGrab.grab()
        filepath = os.path.join(screenshot_folder, filename)
        screenshot.save(filepath)
        print(f"   ✅ บันทึกภาพ: {filepath}")
        return filepath
    except Exception as e:
        print(f"   ❌ ไม่สามารถถ่ายภาพได้: {e}")
        return None

# --- ฟังก์ชันวิเคราะห์ภาพด้วย AI ---
def analyze_screenshot(image_path, website_info):
    """วิเคราะห์ภาพหน้าจอด้วย Gemini AI"""
    if not use_ai_analysis:
        return None

    try:
        from PIL import Image
        img = Image.open(image_path)

        prompt = f"""วิเคราะห์ข้อมูลตลาดหุ้นจากภาพหน้าจอนี้:

เว็บไซต์: {website_info['name']}
คำอธิบาย: {website_info['description']}

กรุณาวิเคราะห์และสรุป:
1. ข้อมูลหลักที่เห็นในภาพ (ดัชนี, ราคา, มูลค่าซื้อขาย)
2. แนวโน้มของตลาด (ขึ้น/ลง/ไซด์เวย์)
3. ข้อมูลที่น่าสนใจ
4. ข้อสังเกตเพิ่มเติม

ตอบเป็นภาษาไทยอย่างกระชับและชัดเจน"""

        response = model.generate_content([prompt, img])

        if response.text:
            return response.text
        else:
            return "❌ ไม่สามารถวิเคราะห์ได้ (ถูก block โดย safety filters)"

    except Exception as e:
        return f"❌ เกิดข้อผิดพลาดในการวิเคราะห์: {str(e)}"

# --- เก็บผลลัพธ์ทั้งหมด ---
all_results = []

# --- วนลูปเปิดแต่ละเว็บไซต์ ---
for i, website in enumerate(selected_websites, 1):
    print(f"\n{'='*80}")
    print(f"🌐 [{i}/{len(selected_websites)}] {website['name']}")
    print(f"{'='*80}")
    print(f"🔗 URL: {website['url']}")
    print(f"📝 คำอธิบาย: {website['description']}")

    # เปิดเว็บไซต์
    print(f"⏳ กำลังเปิดเว็บไซต์...")
    webbrowser.open(website['url'])

    # รอให้เว็บไซต์โหลด
    wait_time = website['wait_time']
    print(f"⏰ รอ {wait_time} วินาที เพื่อให้เว็บไซต์โหลดเสร็จ...")
    time.sleep(wait_time)

    # ถ่ายภาพหน้าจอหลัก
    screenshot_name = f"{i:02d}_{website['name'].replace(' ', '_').replace('-', '_')}_main.png"
    print(f"📸 กำลังถ่ายภาพหน้าจอหลัก...")
    main_screenshot = capture_screenshot(screenshot_name)

    # Scroll ลงและถ่ายภาพเพิ่มเติม
    print(f"📜 Scroll ลงเพื่อดูข้อมูลเพิ่มเติม...")
    pyautogui.scroll(-500)  # Scroll ลง
    time.sleep(2)

    screenshot_name_scroll = f"{i:02d}_{website['name'].replace(' ', '_').replace('-', '_')}_scrolled.png"
    print(f"📸 กำลังถ่ายภาพหน้าจอหลัง scroll...")
    scrolled_screenshot = capture_screenshot(screenshot_name_scroll)

    # วิเคราะห์ภาพด้วย AI (ถ้ามี)
    analysis = None
    if use_ai_analysis and main_screenshot:
        print(f"🧠 กำลังวิเคราะห์ภาพด้วย Google Gemini AI...")
        analysis = analyze_screenshot(main_screenshot, website)
        if analysis:
            print(f"\n📊 ผลการวิเคราะห์:")
            print("-" * 80)
            print(analysis)
            print("-" * 80)

    # เก็บผลลัพธ์
    result = {
        'index': i,
        'name': website['name'],
        'url': website['url'],
        'description': website['description'],
        'main_screenshot': main_screenshot,
        'scrolled_screenshot': scrolled_screenshot,
        'ai_analysis': analysis
    }
    all_results.append(result)

    print(f"✅ เสร็จสิ้นเว็บไซต์ที่ {i}")

    # พักระหว่างเว็บไซต์
    if i < len(selected_websites):
        print(f"\n⏳ พัก 3 วินาที ก่อนเปิดเว็บไซต์ถัดไป...")
        time.sleep(3)

# --- สร้างรายงานสรุป ---
print("\n" + "=" * 80)
print("📝 กำลังสร้างรายงานสรุป...")
print("=" * 80)

report_path = os.path.join(screenshot_folder, "analysis_report.txt")

with open(report_path, "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("🤖 Stock Bot - Thai Stock Market Web Automation Report\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"📅 วันที่: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"🌐 จำนวนเว็บไซต์: {len(selected_websites)}\n")
    f.write(f"🤖 AI Analysis: {'เปิดใช้งาน' if use_ai_analysis else 'ปิดใช้งาน'}\n\n")

    for result in all_results:
        f.write("=" * 80 + "\n")
        f.write(f"[{result['index']}] {result['name']}\n")
        f.write("=" * 80 + "\n")
        f.write(f"🔗 URL: {result['url']}\n")
        f.write(f"📝 คำอธิบาย: {result['description']}\n")
        f.write(f"📸 ภาพหลัก: {result['main_screenshot']}\n")
        f.write(f"📸 ภาพหลัง scroll: {result['scrolled_screenshot']}\n\n")

        if result['ai_analysis']:
            f.write("🧠 ผลการวิเคราะห์โดย AI:\n")
            f.write("-" * 80 + "\n")
            f.write(result['ai_analysis'] + "\n")
            f.write("-" * 80 + "\n\n")
        else:
            f.write("ℹ️  ไม่มีการวิเคราะห์ด้วย AI\n\n")

print(f"✅ บันทึกรายงานที่: {report_path}")
print(f"📂 ตำแหน่ง: {os.path.abspath(report_path)}")
print(f"📁 โฟลเดอร์ภาพ: {os.path.abspath(screenshot_folder)}")

# --- สรุปผลลัพธ์ ---
print("\n" + "=" * 80)
print("🎉 เสร็จสิ้นการดำเนินการทั้งหมด!")
print("=" * 80)
print(f"✅ เปิดและถ่ายภาพเว็บไซต์: {len(selected_websites)} เว็บ")
print(f"📸 จำนวนภาพทั้งหมด: {len(selected_websites) * 2} ภาพ")
print(f"📁 โฟลเดอร์: {screenshot_folder}/")
print(f"📝 รายงาน: {report_path}")

if use_ai_analysis:
    print(f"🧠 AI Analysis: เปิดใช้งาน (Gemini 2.0 Flash)")
else:
    print(f"ℹ️  AI Analysis: ปิดใช้งาน")

print("\n💡 เคล็ดลับ:")
print("   - เพิ่ม Gemini API Key เพื่อใช้การวิเคราะห์ด้วย AI")
print("   - ตั้งค่า: export GEMINI_API_KEY='your-key-here'")
print("   - หรือสร้างไฟล์ .env และใส่: GEMINI_API_KEY=your-key-here")

print("\n💰 ค่าใช้จ่าย:")
print("   - Gemini 2.0 Flash: ฟรี! (15 requests/minute)")
print("   - Screenshot: ฟรี! (ใช้เครื่องตัวเอง)")

print("\n🚀 รันใหม่:")
print("   python stock_bot_thai_web_automation.py")
print("=" * 80)
