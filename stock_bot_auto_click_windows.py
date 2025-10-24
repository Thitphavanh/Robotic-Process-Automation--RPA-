import pyautogui
import webbrowser
import time
import os
from urllib.parse import quote_plus

# ============================================
# Stock Bot Auto Click - Windows Version
# ============================================

# --- 1. กำหนดค่าเริ่มต้น ---
search_term = "ราคาหุ้นไทยวันนี้"
num_results_to_visit = 10  # จำนวนเว็บไซต์ที่จะเข้าไปดู (รวม Sponsored + Organic)

print("=" * 70)
print("🪟 Stock Bot Auto Click - Windows Version")
print("=" * 70)
print(f"🔍 คำค้นหา: {search_term}")
print(f"📊 จะเข้าดูเว็บไซต์ {num_results_to_visit} เว็บแรก")
print("=" * 70)

print("\n⏰ บอทจะเริ่มทำงานใน 5 วินาที...")
print("กรุณาอย่าขยับเมาส์และคีย์บอร์ด!")
time.sleep(5)

# --- 2. สร้าง Google Search URL พร้อม encode ภาษาไทย ---
print(f"\n🔍 กำลังค้นหาคำว่า: {search_term}")
encoded_search = quote_plus(search_term)
search_url = f"https://www.google.com/search?q={encoded_search}"
print(f"🔗 URL: {search_url}")

# --- 3. เปิดเว็บเบราว์เซอร์พร้อม Search URL ---
print("\n🌐 กำลังเปิดเว็บเบราว์เซอร์และค้นหา...")
webbrowser.open(search_url)
time.sleep(7)  # รอให้หน้าผลการค้นหาโหลด

# --- 4. ถ่ายภาพหน้าจอหน้าผลการค้นหา ---
print("\n📸 ถ่ายภาพหน้าจอผลการค้นหา...")
try:
    screenshot = pyautogui.screenshot()
    screenshot.save("01_search_results_windows.png")
    print("✅ บันทึก: 01_search_results_windows.png")
except Exception as e:
    print(f"❌ ไม่สามารถถ่ายภาพ: {e}")

# --- 5. หาตำแหน่งผลการค้นหาและคลิก ---
print("\n" + "=" * 70)
print("🖱️  เริ่มคลิกเข้าดูเว็บไซต์แต่ละเว็บ...")
print("=" * 70)

# รับขนาดหน้าจอ
screen_width, screen_height = pyautogui.size()
print(f"📐 ขนาดหน้าจอ: {screen_width}x{screen_height}")

# ตำแหน่งโดยประมาณของผลการค้นหา (สำหรับ Windows)
# รวมทั้ง Sponsored Results และ Organic Results
search_result_positions = [
    # Sponsored Results Section
    (screen_width // 2, int(screen_height * 0.25)),  # 1. XTB (Sponsored)
    (screen_width // 2, int(screen_height * 0.32)),  # 2. Webull (Sponsored)
    (screen_width // 2, int(screen_height * 0.36)),  # 3. Trademan (Sponsored)

    # Organic Results Section
    (screen_width // 2, int(screen_height * 0.45)),  # 4. SET - ภาพรวมดัชนี
    (screen_width // 2, int(screen_height * 0.54)),  # 5. Settrade - สรุปภาวะตลาด
    (screen_width // 2, int(screen_height * 0.62)),  # 6. SET - ดัชนี
    (screen_width // 2, int(screen_height * 0.70)),  # 7. Investing.com - SET Index
    (screen_width // 2, int(screen_height * 0.78)),  # 8. SET - ราคาหลักทรัพย์
    (screen_width // 2, int(screen_height * 0.86)),  # 9. Settrade - ภาพรวม Top 20
    (screen_width // 2, int(screen_height * 0.92)),  # 10. RYT9 - ข่าวหุ้นไทย
]

# ชื่อเว็บไซต์ที่จะเข้าเยี่ยมชม (สำหรับแสดงผล)
website_names = [
    "XTB (Sponsored)",
    "Webull (Sponsored)",
    "Trademan (Sponsored)",
    "SET - ภาพรวมดัชนี",
    "Settrade - สรุปภาวะตลาด",
    "SET - ดัชนี",
    "Investing.com",
    "SET - ราคาหลักทรัพย์",
    "Settrade - Top 20",
    "RYT9 - ข่าวหุ้น",
]

screenshot_counter = 2  # เริ่มนับจาก 2 เพราะ 01 ใช้ไปแล้ว

for i, position in enumerate(search_result_positions[:num_results_to_visit], 1):
    website_name = website_names[i-1] if i <= len(website_names) else f"Website #{i}"
    print(f"\n{'='*70}")
    print(f"🔗 [{i}/{num_results_to_visit}] {website_name}")
    print(f"📍 ตำแหน่งคลิก: {position}")
    print(f"{'='*70}")

    try:
        # คลิกที่ตำแหน่งผลการค้นหา
        print(f"🖱️  กำลังคลิก...")
        pyautogui.click(position[0], position[1])
        print(f"✅ คลิกสำเร็จ")

        # รอให้หน้าเว็บโหลด
        print(f"⏳ รอให้หน้าเว็บโหลด (5 วินาที)...")
        time.sleep(5)

        # ถ่ายภาพหน้าจอเมื่อเข้าเว็บ
        screenshot_filename = f"{screenshot_counter:02d}_website_{i}_initial_windows.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_filename)
        print(f"📸 บันทึก: {screenshot_filename}")
        screenshot_counter += 1

        # Scroll หน้าเว็บลงไปดูข้อมูล (เฉพาะเว็บสำคัญ)
        # สำหรับ Sponsored ads ให้ scroll น้อยลง
        num_scrolls = 2 if i <= 3 else 3  # Sponsored = 2 scroll, Organic = 3 scroll

        print(f"📜 Scroll ดูข้อมูล ({num_scrolls} ครั้ง)...")
        for scroll_step in range(1, num_scrolls + 1):
            pyautogui.scroll(-3)  # Scroll ลง
            time.sleep(1.5)

            # ถ่ายภาพหลัง scroll แต่ละครั้ง
            screenshot_scroll = f"{screenshot_counter:02d}_website_{i}_scroll_{scroll_step}_windows.png"
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_scroll)
            print(f"📸 บันทึก: {screenshot_scroll}")
            screenshot_counter += 1

        # Scroll กลับขึ้นบน
        print(f"⬆️  Scroll กลับขึ้นบน...")
        pyautogui.hotkey('ctrl', 'home')  # Ctrl + Home = Home
        time.sleep(2)

        # กดปุ่ม Back เพื่อกลับไปหน้าผลการค้นหา
        if i < num_results_to_visit:  # ไม่ต้อง back ถ้าเป็นเว็บสุดท้าย
            print(f"⬅️  กลับไปหน้าผลการค้นหา...")
            pyautogui.hotkey('alt', 'left')  # Alt + Left = Back (Windows)
            time.sleep(3)
        else:
            print(f"✅ เว็บไซต์สุดท้าย - ไม่ต้องกลับ")

    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาดที่เว็บไซต์ {i}: {e}")
        continue

# --- 6. สรุปผลลัพธ์ ---
print("\n" + "=" * 70)
print("📊 สรุปผลการทำงาน")
print("=" * 70)

# นับจำนวนไฟล์ที่สร้าง
created_files = []
for filename in os.listdir('.'):
    if filename.endswith('_windows.png') and filename.startswith(('0', '1', '2')):
        if os.path.exists(filename):
            created_files.append(filename)
            size = os.path.getsize(filename) / 1024
            print(f"✅ {filename} ({size:.2f} KB)")

created_files.sort()

print(f"\n📁 สร้างไฟล์ทั้งหมด: {len(created_files)} ไฟล์")
print(f"📂 ตำแหน่ง: {os.path.abspath('.')}")

print("\n💡 เคล็ดลับ:")
print("   1. ปรับ num_results_to_visit เพื่อดูเว็บไซต์มากขึ้น/น้อยลง")
print("   2. ปรับตำแหน่งคลิกใน search_result_positions หากคลิกผิดที่")
print("   3. Windows + Shift + S = เปิด Snipping Tool")
print("   4. ถ้าตำแหน่งคลิกไม่ถูกต้อง ให้ปรับค่า 0.40, 0.52, 0.64")

print("\n" + "=" * 70)
print("🎉 โปรแกรมสิ้นสุดการทำงาน")
print("=" * 70)
