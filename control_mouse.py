import pyautogui

# เลื่อนเมาส์ไปที่ตำแหน่ง (x=100, y=100) ภายใน 1 วินาที
pyautogui.moveTo(100, 100, duration=1)

# คลิกที่ตำแหน่งปัจจุบัน
pyautogui.click()

# คลิกขวา
pyautogui.rightClick()

# ดับเบิ้ลคลิก
pyautogui.doubleClick()

# ลากเมาส์ไปที่ตำแหน่ง (200, 200)
pyautogui.dragTo(200, 200, duration=1, button='left')
