import pyautogui
import webbrowser
import time
import os

# ============================================
# Stock Bot Direct Visit - Windows Version
# Visit specific stock websites and interact with content
# ============================================

# --- 1. กำหนดรายการเว็บไซต์ที่ต้องการเข้าชม ---
websites = [
    {
        "name": "Webull Thailand",
        "url": "https://www.webull.co.th/us-stocks?source=hy-us-stocks&gad_source=1&gad_campaignid=22300989089&gbraid=0AAAAA9djAz2Vx0uO0YspVLp25YTpa8o-G&gclid=CjwKCAjwgeLHBhBuEiwAL5gNEXUR3SqtLPeGghfhtsIi60W1gJ_yaokmV8ARwthg43DKo1RsRJbq5xoCNUwQAvD_BwE"
    },
    {
        "name": "XTB Thailand",
        "url": "https://www.xtb.com/th/stocks?utm_source=google&utm_medium=cpc&utm_campaign=google_search_th_stock&utm_term=xtbth_stock&utm_content=xtbth_stock&gclid=CjwKCAjwgeLHBhBuEiwAL5gNEY5kAZk3CYovtOwgEwqgNoCGOa9pH-phyo5qZGoLzzZdmhxUjYaxkRoCbTAQAvD_BwE&gbraid=0AAAAADXBll_by46bCEzdGn-zfmqSc6vZx&gad_campaignid=22815695003&gad_source=1"
    },
    {
        "name": "Trademan",
        "url": "https://trademan.in.th/?utm_source=google&utm_medium=cpc&utm_campaign=search-ads&gad_source=1&gad_campaignid=22662650544&gbraid=0AAAAA_3bptlYY9ShOZBtmTW10vvekjHmX&gclid=CjwKCAjwgeLHBhBuEiwAL5gNETNRdxJxRXdcUnLXsGriuErM3BYBBx-KxQqiLvlxlREITJOA1h3BgBoCJH8QAvD_BwE"
    },
    {
        "name": "SET - ตลาดหลักทรัพย์",
        "url": "https://www.set.or.th/th/market/index/set/overview"
    },
    {
        "name": "Investing.com - SET Index",
        "url": "https://www.investing.com/indices/thailand-set?utm_source=google&utm_medium=cpc&utm_campaign=21459771346&utm_content=705306894696&utm_term=dsa-1456167871416_&GL_Ad_ID=705306894696&GL_Campaign_ID=21459771346&ISP=1&npl=1&ppu=9801673&gad_source=1&gad_campaignid=21459771346&gbraid=0AAAAAqxG1s3ttBhA3nXjqwl48OFicy6i_&gclid=CjwKCAjwgeLHBhBuEiwAL5gNEQfl3PM9TNpkBHZMR4NRnkNyMpQY9-VROungMZObhmNUm3wN5yvKjBoCIS8QAvD_BwE"
    }
]

print("=" * 80)
print("🪟 Stock Bot Direct Visit - Windows Version")
print("=" * 80)
print(f"📊 จำนวนเว็บไซต์ที่จะเข้าชม: {len(websites)} เว็บ")
print("🖱️  พร้อมคลิกและโต้ตอบกับเนื้อหาในแต่ละเว็บไซต์")
print("=" * 80)

# แสดงรายชื่อเว็บไซต์
print("\n📋 รายการเว็บไซต์:")
for i, site in enumerate(websites, 1):
    print(f"   {i}. {site['name']}")

print("\n⏰ บอทจะเริ่มทำงานใน 5 วินาที...")
print("กรุณาอย่าขยับเมาส์และคีย์บอร์ด!")
time.sleep(5)

# รับขนาดหน้าจอ
screen_width, screen_height = pyautogui.size()
print(f"\n📐 ขนาดหน้าจอ: {screen_width}x{screen_height}")

screenshot_counter = 1

# --- 2. เข้าชมแต่ละเว็บไซต์ ---
for i, site in enumerate(websites, 1):
    website_name = site['name'].replace(' ', '_').replace('-', '_')
    website_url = site['url']

    print(f"\n{'='*80}")
    print(f"🔗 [{i}/{len(websites)}] {site['name']}")
    print(f"🌐 URL: {website_url[:80]}...")
    print(f"{'='*80}")

    try:
        # เปิดเว็บไซต์
        print(f"\n🌐 กำลังเปิดเว็บไซต์...")
        webbrowser.open(website_url)
        time.sleep(8)  # รอให้หน้าเว็บโหลด

        # 1. ถ่ายภาพหน้าแรก
        print(f"\n📸 [1/10] ถ่ายภาพหน้าแรก...")
        screenshot = pyautogui.screenshot()
        filename = f"{screenshot_counter:03d}_{website_name}_01_main.png"
        screenshot.save(filename)
        print(f"   ✅ บันทึก: {filename}")
        screenshot_counter += 1
        time.sleep(1)

        # 2. Scroll ดูข้อมูลส่วนบน
        print(f"\n📜 [2/10] Scroll ดูข้อมูลส่วนบน...")
        pyautogui.scroll(-2)
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        filename = f"{screenshot_counter:03d}_{website_name}_02_scroll_top.png"
        screenshot.save(filename)
        print(f"   ✅ บันทึก: {filename}")
        screenshot_counter += 1

        # 3. คลิกตรงกลาง (อาจเป็นเมนู, ปุ่ม, หรือกราฟ)
        print(f"\n🖱️  [3/10] คลิกตรงกลางหน้าจอ...")
        pyautogui.click(screen_width // 2, screen_height // 2)
        time.sleep(3)
        screenshot = pyautogui.screenshot()
        filename = f"{screenshot_counter:03d}_{website_name}_03_center_click.png"
        screenshot.save(filename)
        print(f"   ✅ บันทึก: {filename}")
        screenshot_counter += 1

        # 4. คลิกด้านบน (มักมี Navigation)
        print(f"\n🖱️  [4/10] คลิกด้านบน (Navigation)...")
        pyautogui.click(screen_width // 2, int(screen_height * 0.2))
        time.sleep(3)
        screenshot = pyautogui.screenshot()
        filename = f"{screenshot_counter:03d}_{website_name}_04_top_nav.png"
        screenshot.save(filename)
        print(f"   ✅ บันทึก: {filename}")
        screenshot_counter += 1

        # 5. Scroll ลงตรงกลาง
        print(f"\n📜 [5/10] Scroll ลงดูข้อมูลตรงกลาง...")
        pyautogui.scroll(-3)
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        filename = f"{screenshot_counter:03d}_{website_name}_05_scroll_middle.png"
        screenshot.save(filename)
        print(f"   ✅ บันทึก: {filename}")
        screenshot_counter += 1

        # 6. คลิกด้านขวา (มักมีข้อมูลเพิ่มเติม)
        print(f"\n🖱️  [6/10] คลิกด้านขวา...")
        pyautogui.click(int(screen_width * 0.75), screen_height // 2)
        time.sleep(3)
        screenshot = pyautogui.screenshot()
        filename = f"{screenshot_counter:03d}_{website_name}_06_right_side.png"
        screenshot.save(filename)
        print(f"   ✅ บันทึก: {filename}")
        screenshot_counter += 1

        # 7. Scroll ลงล่างสุด
        print(f"\n📜 [7/10] Scroll ลงล่างสุด...")
        pyautogui.scroll(-5)
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        filename = f"{screenshot_counter:03d}_{website_name}_07_scroll_bottom.png"
        screenshot.save(filename)
        print(f"   ✅ บันทึก: {filename}")
        screenshot_counter += 1

        # 8. คลิกด้านซ้าย (มักมี Sidebar)
        print(f"\n🖱️  [8/10] คลิกด้านซ้าย...")
        pyautogui.click(int(screen_width * 0.25), screen_height // 2)
        time.sleep(3)
        screenshot = pyautogui.screenshot()
        filename = f"{screenshot_counter:03d}_{website_name}_08_left_side.png"
        screenshot.save(filename)
        print(f"   ✅ บันทึก: {filename}")
        screenshot_counter += 1

        # 9. Scroll กลับขึ้นบน
        print(f"\n⬆️  [9/10] Scroll กลับขึ้นบน...")
        pyautogui.hotkey('ctrl', 'home')  # Ctrl + Home = Home
        time.sleep(2)
        screenshot = pyautogui.screenshot()
        filename = f"{screenshot_counter:03d}_{website_name}_09_back_top.png"
        screenshot.save(filename)
        print(f"   ✅ บันทึก: {filename}")
        screenshot_counter += 1

        # 10. ถ่ายภาพสุดท้าย
        print(f"\n📸 [10/10] ถ่ายภาพสรุปเว็บไซต์...")
        screenshot = pyautogui.screenshot()
        filename = f"{screenshot_counter:03d}_{website_name}_10_final.png"
        screenshot.save(filename)
        print(f"   ✅ บันทึก: {filename}")
        screenshot_counter += 1

        print(f"\n✅ เสร็จสิ้นการสำรวจ {site['name']}")
        print(f"📊 บันทึกภาพไปแล้ว 10 ภาพ")

        # รอก่อนไปเว็บถัดไป (ยกเว้นเว็บสุดท้าย)
        if i < len(websites):
            print(f"\n⏳ รอ 3 วินาทีก่อนไปเว็บถัดไป...")
            time.sleep(3)

    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดที่เว็บไซต์ {site['name']}: {e}")
        continue

# --- 3. สรุปผลลัพธ์ ---
print("\n" + "=" * 80)
print("📊 สรุปผลการทำงาน")
print("=" * 80)

# นับจำนวนไฟล์ที่สร้าง
created_files = []
for filename in os.listdir('.'):
    if filename.endswith('.png') and filename[0].isdigit():
        if os.path.exists(filename):
            created_files.append(filename)
            size = os.path.getsize(filename) / 1024
            # แสดงเฉพาะ 5 ไฟล์แรก
            if len(created_files) <= 5:
                print(f"✅ {filename} ({size:.2f} KB)")

if len(created_files) > 5:
    print(f"   ... และอีก {len(created_files) - 5} ไฟล์")

created_files.sort()

print(f"\n📁 สร้างไฟล์ทั้งหมด: {len(created_files)} ไฟล์")
print(f"📂 ตำแหน่ง: {os.path.abspath('.')}")

print("\n💡 สิ่งที่บอททำในแต่ละเว็บ (10 ขั้นตอน):")
print("   1. ถ่ายภาพหน้าแรก")
print("   2. Scroll ดูข้อมูลส่วนบน")
print("   3. คลิกตรงกลางหน้าจอ")
print("   4. คลิกด้านบน (Navigation)")
print("   5. Scroll ลงดูข้อมูลตรงกลาง")
print("   6. คลิกด้านขวา")
print("   7. Scroll ลงล่างสุด")
print("   8. คลิกด้านซ้าย")
print("   9. Scroll กลับขึ้นบน")
print("   10. ถ่ายภาพสรุปเว็บไซต์")

print(f"\n📈 สถิติ:")
print(f"   - เว็บไซต์ที่เยี่ยมชม: {len(websites)} เว็บ")
print(f"   - ภาพถ่ายต่อเว็บ: 10 ภาพ")
print(f"   - ภาพถ่ายทั้งหมด: {len(websites) * 10} ภาพ")

print("\n" + "=" * 80)
print("🎉 โปรแกรมสิ้นสุดการทำงาน")
print("=" * 80)
