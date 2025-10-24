import pyautogui
import time
import webbrowser
import pyperclip
from urllib.parse import quote_plus


keyword = 'อุณหภูมิกรุงเทพ' # ข้อความภาษาไทยที่ต้องการค้นหา

print("บอทจะเริ่มทำงานใน 3 วินาที...")
time.sleep(3) # หน่วงเวลาเพื่อให้เราสลับหน้าจอได้ทัน

encoded_keyword = quote_plus(keyword) # Encode ข้อความให้เป็น URL-safe format

url = f'https://www.google.com/search?q={encoded_keyword}'

# --- 1. เปิดเว็บเบราว์เซอร์ ---
webbrowser.open(url)
time.sleep(2) # รอให้เว็บโหลดเสร็จ

# --- 2. พิมพ์ข้อความค้นหา (วิธีสำหรับภาษาไทย) ---
pyperclip.copy(keyword) # ใช้วิธี Copy ข้อความภาษาไทย
time.sleep(1)
# ใช้ Hotkey 'ctrl+v' เพื่อวางข้อความที่ Copy ไว้
pyautogui.hotkey('ctrl', 'v')
time.sleep(1)

# --- 3. กด Enter เพื่อค้นหา ---
pyautogui.press('enter')
time.sleep(2) # รอหน้าผลลัพธ์โหลด

# --- 4. ถ่ายภาพหน้าจอผลลัพธ์ ---
# บันทึกไฟล์โดยใช้ชื่อเดียวกับ keyword ที่ค้นหา
pyautogui.screenshot(keyword + '.png')

print("ทำงานเสร็จสิ้น! บันทึกภาพหน้าจอเป็นไฟล์ " + keyword + ".png")