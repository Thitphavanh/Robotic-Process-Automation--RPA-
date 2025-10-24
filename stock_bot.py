import pyautogui
import webbrowser
import time
import platform
import os
from urllib.parse import quote_plus
from PIL import ImageGrab

# --- 1. กำหนดค่าเริ่มต้น ---
search_term = 'ราคาหุ้นไทยวันนี้'

# ตรวจสอบระบบปฏิบัติการ
is_mac = platform.system() == 'Darwin'
cmd_key = 'command' if is_mac else 'ctrl'

print(f'ระบบปฏิบัติการ: {"macOS" if is_mac else "Windows/Linux"}')

# ตรวจสอบ permissions บน macOS
if is_mac:
    print('\n⚠️  สำคัญสำหรับ macOS:')
    print('ต้องอนุญาต Screen Recording สำหรับ Terminal/Python:')
    print('System Preferences > Security & Privacy > Privacy > Screen Recording')
    print('✓ เปิดใช้งาน Terminal หรือ Python\n')

print('บอทจะเริ่มทำงานใน 5 วินาที... กรุณาอย่าขยับเมาส์และคีย์บอร์ด')
time.sleep(5) # หน่วงเวลา 5 วินาที เพื่อให้เราเตรียมตัว

# --- 2. สร้าง Google Search URL พร้อม encode ภาษาไทย ---
print(f'กำลังค้นหาคำว่า: {search_term}')
# Encode คำค้นหาให้เป็น URL-safe format
encoded_search = quote_plus(search_term)
search_url = f'https://www.google.com/search?q={encoded_search}'
print(f'URL: {search_url}')

# --- 3. เปิดเว็บเบราว์เซอร์พร้อม Search URL ---
print('กำลังเปิดเว็บเบราว์เซอร์และค้นหา...')
webbrowser.open(search_url)
time.sleep(7) # รอให้หน้าผลการค้นหาโหลด

# --- 4. ถ่ายภาพหน้าจอเพื่อบันทึกผลลัพธ์ ---
print('กำลังถ่ายภาพหน้าจอ...')
filename = 'stock_price_result.png'

try:
    # ลองใช้ pyautogui ก่อน
    screenshot = pyautogui.screenshot()
    screenshot.save(filename)
    print(f'✅ ทำงานเสร็จสิ้น! บันทึกผลการค้นหาเป็นไฟล์ชื่อ {filename}')

    # แสดงตำแหน่งไฟล์
    full_path = os.path.abspath(filename)
    print(f'📁 ตำแหน่งไฟล์: {full_path}')

except Exception as e:
    print(f'❌ เกิดข้อผิดพลาดในการถ่ายภาพหน้าจอ: {e}')

    if is_mac:
        print('\n🔧 วิธีแก้ไขบน macOS:')
        print('1. เปิด System Preferences (หรือ System Settings)')
        print('2. ไปที่ Security & Privacy > Privacy')
        print('3. เลือก "Screen Recording" จากเมนูด้านซ้าย')
        print('4. คลิก 🔒 เพื่อปลดล็อค (ใส่รหัสผ่าน)')
        print('5. ✓ เปิดใช้งาน Terminal หรือ Python')
        print('6. รีสตาร์ท Terminal แล้วรันโปรแกรมอีกครั้ง')
        print('\nหรือใช้คำสั่ง: Command + Shift + 5 เพื่อถ่ายภาพหน้าจอด้วยตนเอง')
    else:
        print('\n🔧 วิธีแก้ไข: ตรวจสอบว่าติดตั้ง Pillow แล้วหรือยัง')
        print('ติดตั้งด้วยคำสั่ง: pip install Pillow')