import pyautogui
import webbrowser
import time
from urllib.parse import quote_plus

search_term = "ราคาหุ้นไทยวันนี้"

time.sleep(3)

encoded_search = quote_plus(search_term)
search_url = f"https://www.google.com/search?q={encoded_search}"

webbrowser.open(search_url)
time.sleep(5)  # รอให้หน้าผลการค้นหาโหลด


filename = "stock_price_result_windows.png"

# ใช้ pyautogui สำหรับ Windows
screenshot = pyautogui.screenshot()
screenshot.save(filename)


