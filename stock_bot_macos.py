import pyautogui
import webbrowser
import time
import os
from urllib.parse import quote_plus

# ============================================
# Stock Bot for macOS
# ============================================

# --- 1. กำหนดค่าเริ่มต้น ---
search_term = "ราคาหุ้น Apple วันนี้"


print("\nบอทจะเริ่มทำงานใน 5 วินาที... กรุณาอย่าขยับเมาส์และคีย์บอร์ด")
time.sleep(5)

# --- 2. สร้าง Google Search URL พร้อม encode ภาษาไทย ---
print(f"\n🔍 กำลังค้นหาคำว่า: {search_term}")
# Encode คำค้นหาให้เป็น URL-safe format
encoded_search = quote_plus(search_term)
search_url = f"https://www.google.com/search?q={encoded_search}"
print(f"🔗 URL: {search_url}")

# --- 3. เปิดเว็บเบราว์เซอร์พร้อม Search URL ---
print("\n🌐 กำลังเปิดเว็บเบราว์เซอร์และค้นหา...")
webbrowser.open(search_url)
time.sleep(7)  # รอให้หน้าผลการค้นหาโหลด

# --- 4. ถ่ายภาพหน้าจอเพื่อบันทึกผลลัพธ์ ---
print("\n📸 กำลังถ่ายภาพหน้าจอ...")
filename = "stock_price_result_macos.png"

try:
    # ใช้ pyautogui สำหรับ macOS
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

    # แสดงผลลัพธ์
    print(f"\n✅ ทำงานเสร็จสิ้น!")

    # แสดงตำแหน่งไฟล์แบบเต็ม
    full_path = os.path.abspath(filename)
    print(f"📂 ตำแหน่งเต็ม: {full_path}")

    # แสดงขนาดไฟล์
    file_size = os.path.getsize(filename) / 1024  # KB
    print(f"📊 ขนาดไฟล์: {file_size:.2f} KB")

except Exception as e:
    print(f"\n❌ เกิดข้อผิดพลาด: {e}")

print("\n" + "=" * 50)
print("🎉 โปรแกรมสิ้นสุดการทำงาน")
print("=" * 50)
