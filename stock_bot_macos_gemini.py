import pyautogui
import webbrowser
import time
import os
from urllib.parse import quote_plus
import google.generativeai as genai
from PIL import Image
import dotenv

dotenv.load_dotenv()

# ============================================
# Stock Bot with Google Gemini AI - macOS Version
# Advanced AI-powered web scraping and analysis
# ============================================

# --- Configuration ---
# ตั้งค่า API Key
print("=" * 80)
print("🔑 การตั้งค่า Google Gemini API Key")
print("=" * 80)

# ลองหา API Key จาก environment variable ก่อน
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    print("✅ พบ API Key จาก environment variable")
else:
    print("⚠️  ไม่พบ API Key จาก environment variable")
    print("\n📝 กรุณาใส่ Google Gemini API Key ของคุณ:")
    print("   (หาได้จาก: https://makersuite.google.com/app/apikey)")
    print("   รูปแบบ: AIzaSy...")
    GEMINI_API_KEY = input("\n🔑 API Key: ").strip()

    if not GEMINI_API_KEY:
        print("\n❌ ไม่พบ API Key! โปรแกรมจะหยุดทำงาน")
        print("\n💡 วิธีตั้งค่า API Key:")
        print("   1. ไปที่ https://makersuite.google.com/app/apikey")
        print("   2. คลิก 'Get API Key' หรือ 'Create API Key'")
        print("   3. เลือก Project หรือสร้างใหม่")
        print("   4. คัดลอก API Key")
        print("   5. รันโปรแกรมใหม่และใส่ API Key")
        print("\n   หรือตั้งค่าผ่าน environment variable:")
        print("   export GEMINI_API_KEY='AIzaSy-your-key-here'")
        print("\n💰 ค่าใช้จ่าย: Gemini Pro Vision ฟรี! (มี quota จำกัด)")
        print("\n💡 หรือใช้เวอร์ชันฟรี: python stock_bot_macos_no_api.py")
        exit(1)

# ตรวจสอบว่า API Key มีรูปแบบถูกต้อง
if not GEMINI_API_KEY.startswith("AIzaSy"):
    print("\n⚠️  API Key ไม่ถูกต้อง! ควรขึ้นต้นด้วย 'AIzaSy'")
    print("กรุณาตรวจสอบและรันใหม่อีกครั้ง")
    exit(1)

print(f"✅ API Key: {GEMINI_API_KEY[:20]}...")
print("=" * 80)

try:
    # ตั้งค่า Gemini API
    genai.configure(api_key=GEMINI_API_KEY)

    # สร้าง model (ใช้ gemini-2.5-pro สำหรับ vision)
    model = genai.GenerativeModel('gemini-2.5-pro')

    # ทดสอบการเชื่อมต่อ
    test_response = model.generate_content("สวัสดี ตอบสั้นๆ")
    print("✅ เชื่อมต่อ Google Gemini API สำเร็จ")
    print(f"✅ ใช้ Model: gemini-2.5-pro")
except Exception as e:
    print(f"\n❌ ไม่สามารถเชื่อมต่อ Google Gemini API: {e}")
    print("\n💡 กรุณาตรวจสอบ API Key และลองใหม่อีกครั้ง")
    exit(1)

# --- 1. กำหนดค่าเริ่มต้น ---
print("=" * 80)
print("🤖 Stock Bot with Google Gemini AI - macOS Version")
print("=" * 80)
print("🧠 AI-Powered Dynamic Search & Analysis")
print("=" * 80)

# ให้ผู้ใช้เลือกโหมด
print("\n📋 เลือกโหมดการทำงาน:")
print("   1. ค้นหาข้อมูลทั่วไป (Dynamic Search)")
print("   2. ค้นหาข้อมูลหุ้นไทย (Stock Focus)")
print("   3. กำหนดเอง (Custom Query)")

mode = input("\n🔢 เลือกโหมด (1-3): ").strip()

if mode == "1":
    search_query = input("\n🔍 ใส่คำค้นหา: ").strip()
    analysis_prompt = f"วิเคราะห์ข้อมูลเกี่ยวกับ '{search_query}' จากภาพหน้าจอนี้"
elif mode == "2":
    search_query = "ราคาหุ้นไทยวันนี้"
    analysis_prompt = "วิเคราะห์ข้อมูลตลาดหุ้นไทย ราคา ดัชนี และแนวโน้มจากภาพหน้าจอนี้"
elif mode == "3":
    search_query = input("\n🔍 ใส่คำค้นหา: ").strip()
    analysis_prompt = input("📝 ใส่คำสั่งวิเคราะห์: ").strip()
else:
    print("❌ โหมดไม่ถูกต้อง")
    exit(1)

num_websites = int(input("\n🌐 จำนวนเว็บไซต์ที่ต้องการเยี่ยมชม (1-10): ").strip() or "3")

print(f"\n✅ โหมด: {mode}")
print(f"🔍 คำค้นหา: {search_query}")
print(f"🌐 จำนวนเว็บไซต์: {num_websites}")

# ตรวจสอบ permissions บน macOS
print("\n⚠️  สำคัญ: ต้องอนุญาต Accessibility & Screen Recording")
print("System Settings > Privacy & Security > Accessibility")
print("System Settings > Privacy & Security > Screen Recording")
print("=" * 80)

print("\n⏰ บอทจะเริ่มทำงานใน 5 วินาที...")
time.sleep(5)


# --- 2. Helper Functions ---
def analyze_screenshot_with_gemini(image_path, prompt):
    """ใช้ Google Gemini AI วิเคราะห์ภาพหน้าจอ"""
    try:
        print(f"\n🧠 Google Gemini AI กำลังวิเคราะห์ภาพ...")

        # เปิดภาพ
        img = Image.open(image_path)

        # เรียก Gemini API (ส่งภาพและ prompt พร้อมกัน)
        response = model.generate_content([prompt, img])

        # ตรวจสอบว่ามี response
        if response.text:
            return response.text
        else:
            return "❌ Gemini ไม่สามารถวิเคราะห์ภาพนี้ได้ (อาจถูก block โดย safety filters)"

    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"


def ask_gemini_for_insights(analysis_results):
    """ขอให้ Gemini สรุปและให้ insights จากข้อมูลทั้งหมด"""
    try:
        print(f"\n🧠 Google Gemini AI กำลังสรุปข้อมูลทั้งหมด...")

        combined_text = "\n\n".join(
            [f"เว็บไซต์ {i+1}:\n{result}" for i, result in enumerate(analysis_results)]
        )

        prompt = f"""จากข้อมูลที่วิเคราะห์จากหลายเว็บไซต์ดังนี้:

{combined_text}

กรุณาสรุปข้อมูลสำคัญและให้คำแนะนำดังนี้:
1. สรุปข้อมูลหลักที่พบ
2. เปรียบเทียบข้อมูลจากแต่ละแหล่ง
3. ข้อมูลเชิงลึก (Insights)
4. คำแนะนำหรือข้อควรระวัง
5. แนวโน้มที่น่าสนใจ

ตอบเป็นภาษาไทยอย่างชัดเจนและเป็นระบบ"""

        response = model.generate_content(prompt)

        if response.text:
            return response.text
        else:
            return "❌ Gemini ไม่สามารถสรุปข้อมูลได้"

    except Exception as e:
        return f"❌ เกิดข้อผิดพลาด: {str(e)}"


# --- 3. เริ่มค้นหาและวิเคราะห์ ---
print(f"\n🔍 กำลังค้นหา: {search_query}")
encoded_search = quote_plus(search_query)
search_url = f"https://www.google.com/search?q={encoded_search}"

# เปิดเว็บเบราว์เซอร์
print("\n🌐 กำลังเปิดเว็บเบราว์เซอร์...")
webbrowser.open(search_url)
time.sleep(8)

# รับขนาดหน้าจอ
screen_width, screen_height = pyautogui.size()
print(f"📐 ขนาดหน้าจอ: {screen_width}x{screen_height}")

# ถ่ายภาพหน้าผลการค้นหา
print("\n📸 ถ่ายภาพหน้าผลการค้นหา...")
screenshot = pyautogui.screenshot()
search_results_path = "gemini_search_results.png"
screenshot.save(search_results_path)
print(f"✅ บันทึก: {search_results_path}")

# ให้ Gemini วิเคราะห์หน้าผลการค้นหา
print("\n🤖 ให้ Google Gemini AI วิเคราะห์หน้าผลการค้นหา...")
search_analysis = analyze_screenshot_with_gemini(
    search_results_path,
    f"วิเคราะห์หน้าผลการค้นหาของ Google สำหรับคำว่า '{search_query}' จากภาพนี้ บอกเว็บไซต์ที่น่าสนใจ 5 อันดับแรก พร้อมเหตุผล",
)
print("\n" + "=" * 80)
print("📊 ผลการวิเคราะห์หน้าค้นหา:")
print("=" * 80)
print(search_analysis)

# --- 4. เข้าชมและวิเคราะห์แต่ละเว็บไซต์ ---
analysis_results = []
screenshot_counter = 1

# ตำแหน่งผลการค้นหา
search_positions = [
    (screen_width // 2, int(screen_height * 0.40)),
    (screen_width // 2, int(screen_height * 0.52)),
    (screen_width // 2, int(screen_height * 0.64)),
    (screen_width // 2, int(screen_height * 0.76)),
    (screen_width // 2, int(screen_height * 0.88)),
]

for i in range(min(num_websites, len(search_positions))):
    print(f"\n{'='*80}")
    print(f"🔗 [{i+1}/{num_websites}] เยี่ยมชมเว็บไซต์ที่ {i+1}")
    print(f"{'='*80}")

    try:
        # คลิกเข้าเว็บไซต์
        print(f"🖱️  คลิกเข้าเว็บไซต์...")
        pyautogui.click(search_positions[i][0], search_positions[i][1])
        time.sleep(6)

        # ถ่ายภาพหน้าแรก
        screenshot = pyautogui.screenshot()
        website_path = f"gemini_website_{i+1:02d}_main.png"
        screenshot.save(website_path)
        print(f"📸 บันทึก: {website_path}")
        screenshot_counter += 1

        # ให้ Gemini วิเคราะห์เว็บไซต์
        website_analysis = analyze_screenshot_with_gemini(website_path, analysis_prompt)

        print("\n" + "-" * 80)
        print(f"🧠 ผลการวิเคราะห์เว็บไซต์ที่ {i+1}:")
        print("-" * 80)
        print(website_analysis)
        print("-" * 80)

        analysis_results.append(website_analysis)

        # Scroll ดูเนื้อหาเพิ่มเติม
        print(f"\n📜 Scroll ดูเนื้อหาเพิ่มเติม...")
        pyautogui.scroll(-3)
        time.sleep(2)

        # ถ่ายภาพหลัง scroll
        screenshot = pyautogui.screenshot()
        scrolled_path = f"gemini_website_{i+1:02d}_scrolled.png"
        screenshot.save(scrolled_path)
        print(f"📸 บันทึก: {scrolled_path}")

        # วิเคราะห์เนื้อหาหลัง scroll
        scrolled_analysis = analyze_screenshot_with_gemini(
            scrolled_path,
            f"วิเคราะห์ข้อมูลเพิ่มเติมจากส่วนล่างของหน้าเว็บนี้ มีข้อมูลอะไรที่น่าสนใจเพิ่มเติมบ้าง",
        )

        print("\n" + "-" * 80)
        print(f"🧠 ผลการวิเคราะห์ส่วนเพิ่มเติม:")
        print("-" * 80)
        print(scrolled_analysis)
        print("-" * 80)

        analysis_results.append(scrolled_analysis)

        # กลับไปหน้าผลการค้นหา
        if i < num_websites - 1:
            print(f"\n⬅️  กลับไปหน้าผลการค้นหา...")
            pyautogui.hotkey("command", "[")
            time.sleep(3)

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        continue

# --- 5. สรุปและให้ Insights จาก Gemini ---
print("\n" + "=" * 80)
print("🎯 สรุปผลการวิเคราะห์โดย Google Gemini AI")
print("=" * 80)

final_insights = ask_gemini_for_insights(analysis_results)
print(final_insights)

# บันทึกรายงาน
report_path = "gemini_analysis_report.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("🤖 Stock Bot Gemini AI Analysis Report\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"🔍 คำค้นหา: {search_query}\n")
    f.write(f"📅 วันที่: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"🌐 จำนวนเว็บไซต์: {num_websites}\n")
    f.write(f"🤖 AI Model: gemini-2.5-pro\n\n")

    f.write("=" * 80 + "\n")
    f.write("📊 ผลการวิเคราะห์หน้าค้นหา\n")
    f.write("=" * 80 + "\n\n")
    f.write(search_analysis + "\n\n")

    for i, result in enumerate(analysis_results, 1):
        f.write("=" * 80 + "\n")
        f.write(
            f"🌐 เว็บไซต์ที่ {(i+1)//2 + (i%2)} - {'หน้าแรก' if i%2==1 else 'หลัง Scroll'}\n"
        )
        f.write("=" * 80 + "\n\n")
        f.write(result + "\n\n")

    f.write("=" * 80 + "\n")
    f.write("🎯 สรุปและ Insights\n")
    f.write("=" * 80 + "\n\n")
    f.write(final_insights + "\n")

print(f"\n✅ บันทึกรายงานที่: {report_path}")

# --- 6. สรุปผลลัพธ์ ---
print("\n" + "=" * 80)
print("📊 สรุปผลการทำงาน")
print("=" * 80)

created_files = [
    f for f in os.listdir(".") if f.startswith("gemini_") and f.endswith(".png")
]
created_files.sort()

print(f"\n📁 ไฟล์ภาพที่สร้าง: {len(created_files)} ไฟล์")
for filename in created_files:
    size = os.path.getsize(filename) / 1024
    print(f"   ✅ {filename} ({size:.2f} KB)")

print(f"\n📄 รายงานการวิเคราะห์: {report_path}")
print(f"📂 ตำแหน่ง: {os.path.abspath('.')}")

print("\n💡 สิ่งที่บอททำ:")
print("   1. ค้นหาข้อมูลใน Google")
print("   2. ให้ Gemini AI วิเคราะห์หน้าผลการค้นหา")
print("   3. เข้าชมแต่ละเว็บไซต์")
print("   4. ให้ Gemini AI วิเคราะห์เนื้อหาในแต่ละเว็บ")
print("   5. สรุปและให้ Insights จากข้อมูลทั้งหมด")
print("   6. สร้างรายงานฉบับสมบูรณ์")

print("\n🎨 คุณสมบัติพิเศษ:")
print("   ✅ Google Gemini AI-Powered Analysis")
print("   ✅ Dynamic Search")
print("   ✅ Multi-website Comparison")
print("   ✅ Intelligent Insights")
print("   ✅ Comprehensive Report")
print("   ✅ ฟรี! (มี quota จำกัด)")

print("\n💰 ข้อมูลการใช้งาน:")
print("   - Gemini 2.0 Flash: ฟรี!")
print("   - Quota: 15 requests/minute")
print("   - ไม่มีค่าใช้จ่าย (ภายใน free tier)")

print("\n" + "=" * 80)
print("🎉 โปรแกรมสิ้นสุดการทำงาน")
print("=" * 80)
