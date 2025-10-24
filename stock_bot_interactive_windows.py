import pyautogui
import webbrowser
import time
import os
from urllib.parse import quote_plus

# ============================================
# Stock Bot Interactive - Windows Version
# Can click and interact with website content
# ============================================

# --- 1. กำหนดค่าเริ่มต้น ---
search_term = "ราคาหุ้นไทยวันนี้"
num_results_to_visit = 5  # จำนวนเว็บไซต์ที่จะเข้าไปดู

print("=" * 70)
print("🪟 Stock Bot Interactive - Windows Version")
print("=" * 70)
print(f"🔍 คำค้นหา: {search_term}")
print(f"📊 จะเข้าดูเว็บไซต์ {num_results_to_visit} เว็บแรก")
print(f"🖱️  พร้อมคลิกดูเนื้อหาภายในเว็บไซต์")
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

# ตำแหน่งผลการค้นหา
search_result_positions = [
    (screen_width // 2, int(screen_height * 0.40)),  # SET
    (screen_width // 2, int(screen_height * 0.52)),  # Settrade
    (screen_width // 2, int(screen_height * 0.64)),  # Investing.com
    (screen_width // 2, int(screen_height * 0.76)),  # RYT9
    (screen_width // 2, int(screen_height * 0.88)),  # TradingView
]

website_names = [
    "SET - ตลาดหลักทรัพย์",
    "Settrade - สรุปภาวะตลาด",
    "Investing.com - SET Index",
    "RYT9 - ข่าวหุ้น",
    "TradingView - ชาร์ต",
]

screenshot_counter = 2

for i, position in enumerate(search_result_positions[:num_results_to_visit], 1):
    website_name = website_names[i-1] if i <= len(website_names) else f"Website #{i}"
    print(f"\n{'='*70}")
    print(f"🔗 [{i}/{num_results_to_visit}] {website_name}")
    print(f"{'='*70}")

    try:
        # คลิกที่ตำแหน่งผลการค้นหา
        print(f"🖱️  คลิกเข้าเว็บไซต์...")
        pyautogui.click(position[0], position[1])
        time.sleep(6)  # รอให้หน้าเว็บโหลด

        # ถ่ายภาพหน้าแรก
        screenshot_filename = f"{screenshot_counter:02d}_{website_name.replace(' ', '_')}_main.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_filename)
        print(f"📸 บันทึก: {screenshot_filename}")
        screenshot_counter += 1

        # --- เริ่มโต้ตอบกับเนื้อหาในเว็บไซต์ ---
        print(f"\n🎯 เริ่มสำรวจเนื้อหาภายในเว็บไซต์...")

        # 1. Scroll ดูข้อมูลส่วนบน
        print(f"  📜 Scroll ดูข้อมูลส่วนบน...")
        pyautogui.scroll(-2)
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{screenshot_counter:02d}_{website_name.replace(' ', '_')}_scroll1.png")
        print(f"  📸 บันทึก: {screenshot_counter:02d}_{website_name.replace(' ', '_')}_scroll1.png")
        screenshot_counter += 1

        # 2. คลิกที่ส่วนกลางเพื่อดูรายละเอียด
        print(f"  🖱️  คลิกดูรายละเอียดเพิ่มเติม (กลางหน้าจอ)...")
        pyautogui.click(screen_width // 2, screen_height // 2)
        time.sleep(3)
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{screenshot_counter:02d}_{website_name.replace(' ', '_')}_detail.png")
        print(f"  📸 บันทึก: {screenshot_counter:02d}_{website_name.replace(' ', '_')}_detail.png")
        screenshot_counter += 1

        # 3. Scroll ดูข้อมูลตรงกลาง
        print(f"  📜 Scroll ดูข้อมูลตรงกลาง...")
        pyautogui.scroll(-3)
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{screenshot_counter:02d}_{website_name.replace(' ', '_')}_scroll2.png")
        print(f"  📸 บันทึก: {screenshot_counter:02d}_{website_name.replace(' ', '_')}_scroll2.png")
        screenshot_counter += 1

        # 4. คลิกที่ด้านขวา (มักมีเมนูหรือข้อมูลเพิ่มเติม)
        print(f"  🖱️  คลิกดูข้อมูลด้านขวา...")
        pyautogui.click(int(screen_width * 0.7), screen_height // 2)
        time.sleep(3)
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{screenshot_counter:02d}_{website_name.replace(' ', '_')}_right.png")
        print(f"  📸 บันทึก: {screenshot_counter:02d}_{website_name.replace(' ', '_')}_right.png")
        screenshot_counter += 1

        # 5. Scroll ดูข้อมูลล่างสุด
        print(f"  📜 Scroll ดูข้อมูลล่างสุด...")
        pyautogui.scroll(-4)
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{screenshot_counter:02d}_{website_name.replace(' ', '_')}_bottom.png")
        print(f"  📸 บันทึก: {screenshot_counter:02d}_{website_name.replace(' ', '_')}_bottom.png")
        screenshot_counter += 1

        # 6. คลิกที่ด้านซ้าย (มักมีเมนูหรือตัวกรอง)
        print(f"  🖱️  คลิกดูข้อมูลด้านซ้าย...")
        pyautogui.click(int(screen_width * 0.3), screen_height // 2)
        time.sleep(3)
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{screenshot_counter:02d}_{website_name.replace(' ', '_')}_left.png")
        print(f"  📸 บันทึก: {screenshot_counter:02d}_{website_name.replace(' ', '_')}_left.png")
        screenshot_counter += 1

        # 7. Scroll กลับขึ้นบน
        print(f"  ⬆️  Scroll กลับขึ้นบน...")
        pyautogui.hotkey('ctrl', 'home')  # Ctrl + Home = Home
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{screenshot_counter:02d}_{website_name.replace(' ', '_')}_back_top.png")
        print(f"  📸 บันทึก: {screenshot_counter:02d}_{website_name.replace(' ', '_')}_back_top.png")
        screenshot_counter += 1

        # 8. ถ่ายภาพสุดท้าย
        print(f"  📸 ถ่ายภาพสรุปเว็บไซต์...")
        screenshot = pyautogui.screenshot()
        screenshot.save(f"{screenshot_counter:02d}_{website_name.replace(' ', '_')}_final.png")
        print(f"  📸 บันทึก: {screenshot_counter:02d}_{website_name.replace(' ', '_')}_final.png")
        screenshot_counter += 1

        # กดปุ่ม Back เพื่อกลับไปหน้าผลการค้นหา
        if i < num_results_to_visit:
            print(f"\n⬅️  กลับไปหน้าผลการค้นหา...")
            pyautogui.hotkey('alt', 'left')  # Alt + Left = Back
            time.sleep(4)
        else:
            print(f"\n✅ เว็บไซต์สุดท้าย - เสร็จสิ้น")

        print(f"✅ เสร็จสิ้นการสำรวจ {website_name}")

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
    if filename.endswith('_windows.png') or (filename.endswith('.png') and filename[0].isdigit()):
        if os.path.exists(filename):
            created_files.append(filename)
            size = os.path.getsize(filename) / 1024
            print(f"✅ {filename} ({size:.2f} KB)")

created_files.sort()

print(f"\n📁 สร้างไฟล์ทั้งหมด: {len(created_files)} ไฟล์")
print(f"📂 ตำแหน่ง: {os.path.abspath('.')}")

print("\n💡 สิ่งที่บอททำในแต่ละเว็บ:")
print("   1. ถ่ายภาพหน้าแรก")
print("   2. Scroll ดูข้อมูลส่วนบน")
print("   3. คลิกดูรายละเอียดตรงกลาง")
print("   4. Scroll ดูข้อมูลตรงกลาง")
print("   5. คลิกดูข้อมูลด้านขวา")
print("   6. Scroll ดูข้อมูลล่างสุด")
print("   7. คลิกดูข้อมูลด้านซ้าย")
print("   8. Scroll กลับขึ้นบนและถ่ายภาพสุดท้าย")
print("\n   รวม 8 ภาพต่อเว็บไซต์!")

print("\n⚙️  การปรับแต่ง:")
print("   - เปลี่ยน num_results_to_visit เพื่อดูเว็บไซต์มากขึ้น/น้อยลง")
print("   - ปรับตำแหน่งคลิกใน search_result_positions")

print("\n" + "=" * 70)
print("🎉 โปรแกรมสิ้นสุดการทำงาน")
print("=" * 70)
