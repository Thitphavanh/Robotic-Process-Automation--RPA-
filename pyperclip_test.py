import time
import pyautogui

time.sleep(5)

import pyperclip  #นำไปใส่บนสุด
text = 'ประเทศไทย'
pyperclip.copy(text)

time.sleep(1)
pyautogui.hotkey('ctrl','v')
pyautogui.press('enter')
