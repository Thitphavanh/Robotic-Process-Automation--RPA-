import pyautogui
import webbrowser
import time
import os
from urllib.parse import quote_plus
from PIL import Image
import pytesseract

# ============================================
# Stock Bot Advanced - macOS Version (No API Required)
# Advanced web scraping with OCR text extraction
# ============================================

print("=" * 80)
print("🤖 Stock Bot Advanced - macOS Version")
print("=" * 80)
print("📸 ถ่ายภาพ + OCR Text Extraction (ไม่ต้องใช้ API)")
print("=" * 80)

# --- 1. กำหนดค่าเริ่มต้น ---
print("\n📋 เลือกโหมดการทำงาน:")
print("   1. ค้นหาข้อมูลทั่วไป (Dynamic Search)")
print("   2. ค้นหาข้อมูลหุ้นไทย (Stock Focus)")
print("   3. กำหนดเอง (Custom Query)")

mode = input("\n🔢 เลือกโหมด (1-3): ").strip()

if mode == "1":
    search_query = input("\n🔍 ใส่คำค้นหา: ").strip()
elif mode == "2":
    search_query = "ราคาหุ้นไทยวันนี้"
elif mode == "3":
    search_query = input("\n🔍 ใส่คำค้นหา: ").strip()
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
def extract_text_from_image(image_path):
    """ใช้ OCR ดึงข้อความจากภาพ"""
    try:
        # ตรวจสอบว่าติดตั้ง tesseract หรือยัง
        text = pytesseract.image_to_string(Image.open(image_path), lang='eng+tha')
        return text.strip()
    except Exception as e:
        return f"⚠️  ไม่สามารถดึงข้อความได้ (ติดตั้ง tesseract: brew install tesseract)"

def analyze_screenshot_locally(image_path, query):
    """วิเคราะห์ภาพแบบ local (ไม่ใช้ API)"""
    print(f"\n📝 กำลังดึงข้อความจากภาพ...")

    text = extract_text_from_image(image_path)

    analysis = {
        'extracted_text': text,
        'keywords_found': [],
        'numbers_found': [],
        'urls_found': []
    }

    # หา keywords
    keywords = ['หุ้น', 'stock', 'ราคา', 'price', 'ดัชนี', 'index', 'SET', 'เพิ่มขึ้น', 'ลดลง']
    for keyword in keywords:
        if keyword.lower() in text.lower():
            analysis['keywords_found'].append(keyword)

    # หาตัวเลข
    import re
    numbers = re.findall(r'\d+[\.,]\d+|\d+', text)
    analysis['numbers_found'] = numbers[:10]  # เอาแค่ 10 ตัวแรก

    # หา URLs
    urls = re.findall(r'https?://[^\s]+', text)
    analysis['urls_found'] = urls

    return analysis

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
search_results_path = "local_search_results.png"
screenshot.save(search_results_path)
print(f"✅ บันทึก: {search_results_path}")

# วิเคราะห์หน้าผลการค้นหา
print("\n🔍 วิเคราะห์หน้าผลการค้นหา...")
search_analysis = analyze_screenshot_locally(search_results_path, search_query)

print("\n" + "=" * 80)
print("📊 ผลการวิเคราะห์หน้าค้นหา:")
print("=" * 80)
print(f"🔑 คำสำคัญที่พบ: {', '.join(search_analysis['keywords_found']) if search_analysis['keywords_found'] else 'ไม่พบ'}")
print(f"🔢 ตัวเลขที่พบ: {', '.join(search_analysis['numbers_found'][:5]) if search_analysis['numbers_found'] else 'ไม่พบ'}")

# --- 4. เข้าชมและวิเคราะห์แต่ละเว็บไซต์ ---
all_results = []

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
        website_path = f"local_website_{i+1:02d}_main.png"
        screenshot.save(website_path)
        print(f"📸 บันทึก: {website_path}")

        # วิเคราะห์เว็บไซต์
        website_analysis = analyze_screenshot_locally(website_path, search_query)

        print("\n" + "-" * 80)
        print(f"📊 ผลการวิเคราะห์เว็บไซต์ที่ {i+1}:")
        print("-" * 80)
        print(f"🔑 คำสำคัญ: {', '.join(website_analysis['keywords_found'][:10]) if website_analysis['keywords_found'] else 'ไม่พบ'}")
        print(f"🔢 ตัวเลข: {', '.join(website_analysis['numbers_found'][:10]) if website_analysis['numbers_found'] else 'ไม่พบ'}")
        print(f"🔗 URLs: {len(website_analysis['urls_found'])} links")
        print("-" * 80)

        all_results.append({
            'website_num': i+1,
            'analysis': website_analysis
        })

        # Scroll ดูเนื้อหาเพิ่มเติม
        print(f"\n📜 Scroll ดูเนื้อหาเพิ่มเติม...")
        pyautogui.scroll(-3)
        time.sleep(2)

        # ถ่ายภาพหลัง scroll
        screenshot = pyautogui.screenshot()
        scrolled_path = f"local_website_{i+1:02d}_scrolled.png"
        screenshot.save(scrolled_path)
        print(f"📸 บันทึก: {scrolled_path}")

        # วิเคราะห์หลัง scroll
        scrolled_analysis = analyze_screenshot_locally(scrolled_path, search_query)
        print(f"🔑 คำสำคัญเพิ่มเติม: {', '.join(scrolled_analysis['keywords_found'][:5]) if scrolled_analysis['keywords_found'] else 'ไม่พบ'}")

        # กลับไปหน้าผลการค้นหา
        if i < num_websites - 1:
            print(f"\n⬅️  กลับไปหน้าผลการค้นหา...")
            pyautogui.hotkey('command', '[')
            time.sleep(3)

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        continue

# --- 5. สรุปผลลัพธ์ ---
print("\n" + "=" * 80)
print("📊 สรุปผลการทำงาน")
print("=" * 80)

# บันทึกรายงาน
report_path = "local_analysis_report.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("🤖 Stock Bot Local Analysis Report\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"🔍 คำค้นหา: {search_query}\n")
    f.write(f"📅 วันที่: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"🌐 จำนวนเว็บไซต์: {num_websites}\n\n")

    f.write("=" * 80 + "\n")
    f.write("📊 ผลการวิเคราะห์หน้าค้นหา\n")
    f.write("=" * 80 + "\n\n")
    f.write(f"คำสำคัญ: {', '.join(search_analysis['keywords_found'])}\n")
    f.write(f"ตัวเลข: {', '.join(search_analysis['numbers_found'][:10])}\n\n")

    for result in all_results:
        f.write("=" * 80 + "\n")
        f.write(f"🌐 เว็บไซต์ที่ {result['website_num']}\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"คำสำคัญ: {', '.join(result['analysis']['keywords_found'])}\n")
        f.write(f"ตัวเลข: {', '.join(result['analysis']['numbers_found'][:20])}\n")
        f.write(f"URLs: {len(result['analysis']['urls_found'])} links\n\n")

print(f"\n✅ บันทึกรายงานที่: {report_path}")

# นับไฟล์ที่สร้าง
created_files = [f for f in os.listdir('.') if f.startswith('local_') and f.endswith('.png')]
created_files.sort()

print(f"\n📁 ไฟล์ภาพที่สร้าง: {len(created_files)} ไฟล์")
for filename in created_files[:5]:
    size = os.path.getsize(filename) / 1024
    print(f"   ✅ {filename} ({size:.2f} KB)")
if len(created_files) > 5:
    print(f"   ... และอีก {len(created_files) - 5} ไฟล์")

print(f"\n📄 รายงานการวิเคราะห์: {report_path}")
print(f"📂 ตำแหน่ง: {os.path.abspath('.')}")

print("\n💡 สิ่งที่บอททำ:")
print("   1. ค้นหาข้อมูลใน Google")
print("   2. ถ่ายภาพหน้าผลการค้นหา")
print("   3. ดึงข้อความด้วย OCR (ถ้าติดตั้ง tesseract)")
print("   4. เข้าชมและวิเคราะห์แต่ละเว็บไซต์")
print("   5. สรุปและสร้างรายงาน")

print("\n🎨 คุณสมบัติ:")
print("   ✅ ไม่ต้องใช้ API")
print("   ✅ ฟรี 100%")
print("   ✅ OCR Text Extraction (ถ้ามี tesseract)")
print("   ✅ Keyword Detection")
print("   ✅ Number Extraction")

print("\n💡 เคล็ดลับ:")
print("   ติดตั้ง Tesseract เพื่อดึงข้อความ:")
print("   brew install tesseract")
print("   brew install tesseract-lang")

print("\n" + "=" * 80)
print("🎉 โปรแกรมสิ้นสุดการทำงาน")
print("=" * 80)
