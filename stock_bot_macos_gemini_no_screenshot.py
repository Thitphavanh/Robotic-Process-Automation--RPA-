import webbrowser
import time
import os
import google.generativeai as genai
import dotenv

dotenv.load_dotenv()


# ============================================
# Stock Bot with Google Gemini AI - macOS Version (No Screenshot)
# Text-based analysis only
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
        print("\n💰 ค่าใช้จ่าย: Gemini 2.5 Pro ฟรี! (มี quota จำกัด)")
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

    # สร้าง model
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
print("🤖 Stock Bot with Google Gemini AI - Text Only Version")
print("=" * 80)
print("🧠 AI-Powered Text Analysis (No Screenshots)")
print("=" * 80)

# ให้ผู้ใช้เลือกโหมด
print("\n📋 เลือกโหมดการทำงาน:")
print("   1. วิเคราะห์ข้อมูลหุ้นไทย (Thai Stock Analysis)")
print("   2. วิเคราะห์ตลาดหุ้นโลก (Global Stock Market)")
print("   3. คำถามกำหนดเอง (Custom Question)")

mode = input("\n🔢 เลือกโหมด (1-3): ").strip()

if mode == "1":
    query = """วิเคราะห์สถานการณ์ตลาดหุ้นไทยในปัจจุบัน โดยพิจารณา:
1. ดัชนี SET และ SET50
2. หุ้นกลุ่มที่น่าสนใจ
3. ปัจจัยที่มีผลต่อตลาด
4. แนวโน้มในอนาคตใกล้
5. คำแนะนำสำหรับนักลงทุน

ตอบเป็นภาษาไทยอย่างละเอียด"""

elif mode == "2":
    query = """วิเคราะห์สถานการณ์ตลาดหุ้นโลกในปัจจุบัน โดยพิจารณา:
1. ดัชนีหลักของสหรัฐฯ (Dow Jones, S&P 500, NASDAQ)
2. ตลาดเอเชีย
3. ปัจจัยที่ส่งผลกระทบ
4. แนวโน้มของตลาด
5. ข้อควรระวัง

ตอบเป็นภาษาไทยอย่างละเอียด"""

elif mode == "3":
    query = input("\n📝 ใส่คำถามของคุณ: ").strip()
    if not query:
        print("❌ ไม่มีคำถาม")
        exit(1)
else:
    print("❌ โหมดไม่ถูกต้อง")
    exit(1)

print(f"\n✅ โหมด: {mode}")
print(f"📋 คำถาม: {query[:100]}...")

print("\n⏰ กำลังประมวลผล...")
time.sleep(1)

# --- 2. วิเคราะห์ด้วย Gemini ---
print("\n🧠 Google Gemini AI กำลังวิเคราะห์...")

try:
    response = model.generate_content(query)

    if response.text:
        analysis = response.text
    else:
        analysis = "❌ Gemini ไม่สามารถสร้างคำตอบได้ (อาจถูก block โดย safety filters)"

except Exception as e:
    analysis = f"❌ เกิดข้อผิดพลาด: {str(e)}"

# --- 3. แสดงผลลัพธ์ ---
print("\n" + "=" * 80)
print("📊 ผลการวิเคราะห์โดย Google Gemini AI")
print("=" * 80)
print(analysis)
print("=" * 80)

# --- 4. บันทึกรายงาน ---
report_path = "gemini_text_analysis_report.txt"

with open(report_path, "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("🤖 Stock Bot Gemini AI - Text Analysis Report\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"📅 วันที่: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"🤖 AI Model: gemini-2.5-pro\n")
    f.write(f"📋 Mode: {mode}\n\n")
    f.write("=" * 80 + "\n")
    f.write("📝 คำถาม:\n")
    f.write("=" * 80 + "\n")
    f.write(query + "\n\n")
    f.write("=" * 80 + "\n")
    f.write("📊 ผลการวิเคราะห์:\n")
    f.write("=" * 80 + "\n")
    f.write(analysis + "\n")

print(f"\n✅ บันทึกรายงานที่: {report_path}")
print(f"📂 ตำแหน่ง: {os.path.abspath(report_path)}")

# --- 5. ถามว่าต้องการคำถามเพิ่มเติมไหม ---
print("\n" + "=" * 80)
print("💡 คุณสมบัติพิเศษ:")
print("=" * 80)
print("   ✅ Google Gemini AI-Powered Analysis")
print("   ✅ Text-Based Analysis (No Screenshots)")
print("   ✅ Real-time Market Insights")
print("   ✅ Thai & English Support")
print("   ✅ ฟรี 100%! (ภายใน free tier)")

print("\n💰 ข้อมูลการใช้งาน:")
print("   - Gemini 2.5 Pro: ฟรี!")
print("   - Quota: 15 requests/minute")
print("   - ไม่มีค่าใช้จ่าย (ภายใน free tier)")

# เปิดเว็บไซต์ที่เกี่ยวข้อง
print("\n🌐 ต้องการเปิดเว็บไซต์ข้อมูลหุ้นไหม?")
print("   1. SET (ตลาดหลักทรัพย์แห่งประเทศไทย)")
print("   2. Investing.com")
print("   3. Yahoo Finance")
print("   4. ไม่ต้องการ")

choice = input("\n🔢 เลือก (1-4): ").strip()

if choice == "1":
    print("🌐 เปิด SET...")
    webbrowser.open("https://www.set.or.th/th/market/index/set/overview")
    time.sleep(2)
elif choice == "2":
    print("🌐 เปิด Investing.com...")
    webbrowser.open("https://www.investing.com/indices/thailand-set")
    time.sleep(2)
elif choice == "3":
    print("🌐 เปิด Yahoo Finance...")
    webbrowser.open("https://finance.yahoo.com/")
    time.sleep(2)
else:
    print("✅ ไม่เปิดเว็บไซต์")

print("\n" + "=" * 80)
print("🎉 โปรแกรมสิ้นสุดการทำงาน")
print("=" * 80)
print("\n💡 รันใหม่: python stock_bot_macos_gemini_no_screenshot.py")
