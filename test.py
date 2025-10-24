import pyperclip
import pyautogui

import time
import webbrowser

url = "https://www.google.com"
keyword = "อุณหภูมิกรุงเทพ"

print("บอทจะเริ่มใน 3 วินาที...")
time.sleep(3)

webbrowser.open(url)
time.sleep(2)

pyperclip.copy(keyword)
pyautogui.hotkey("command", "v")
time.sleep(1)

pyautogui.press("enter")
time.sleep(2)

pyautogui.screenshot(keyword + ".png")
print("ทำงานเสร็จสิ้น!")

