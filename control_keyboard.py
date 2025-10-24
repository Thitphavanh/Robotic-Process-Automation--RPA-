import pyautogui
# พิมพ์ข้อความพร้อมหน่วงเวลา 0.1 วินาทีต่ออักษร
pyautogui.write("สวัสดี PyAutoGUI!", interval=0.1)

# กดปุ่ม Enter
pyautogui.press('enter')

# กดปุ่มคีย์ลัด เช่น Ctrl+C
pyautogui.hotkey('ctrtrol', 'c')

# กดปุ่มพิเศษ
pyautogui.press('tab')