"""
RPA Task Runner - ตัวรัน RPA Tasks
"""
import time
import os
from datetime import datetime

try:
    import pyautogui
    import pyperclip
    import webbrowser
    HAS_RPA_LIBS = True
    print(f"✅ RPA libraries loaded successfully! DISPLAY={os.environ.get('DISPLAY', 'Not set')}")
except (ImportError, Exception) as e:
    HAS_RPA_LIBS = False
    print(f"❌ RPA libraries not available: {e}")

from .models import TaskLog


def log_task(task, level, message):
    """เพิ่ม Log ให้กับ Task"""
    TaskLog.objects.create(
        task=task,
        level=level,
        message=message
    )
    print(f"[{level.upper()}] {message}")


def run_rpa_task(task):
    """รัน RPA Task"""

    if not HAS_RPA_LIBS:
        error_msg = "ไม่พบ library pyautogui, pyperclip ติดตั้งด้วย: pip install pyautogui pyperclip"
        log_task(task, 'error', error_msg)
        task.mark_as_failed(error_msg)
        return

    # เริ่มต้น Task
    task.mark_as_running()
    log_task(task, 'info', f'เริ่มรัน Task: {task.name}')

    try:
        # เลือก Task Type
        if task.task_type == 'google_search':
            run_google_search(task)
        elif task.task_type == 'screenshot':
            run_screenshot(task)
        elif task.task_type == 'web_automation':
            run_web_automation(task)
        else:
            raise ValueError(f'Task Type "{task.task_type}" ยังไม่รองรับ')

        # สำเร็จ
        log_task(task, 'success', 'Task เสร็จสมบูรณ์')

    except Exception as e:
        error_msg = f'เกิดข้อผิดพลาด: {str(e)}'
        log_task(task, 'error', error_msg)

        # ลองใหม่ถ้ายังไม่เกินจำนวนครั้ง
        if task.is_retryable:
            task.increment_retry()
            log_task(task, 'warning', f'กำลังลองใหม่ครั้งที่ {task.retry_count}/{task.max_retries}')
            time.sleep(2)
            run_rpa_task(task)  # Retry
        else:
            task.mark_as_failed(error_msg)


def run_google_search(task):
    """รัน Task: ค้นหา Google และจับภาพหน้าจอ"""
    log_task(task, 'info', f'กำลังเปิด URL: {task.url}')

    # Delay ตามที่ตั้งไว้
    log_task(task, 'info', f'บอทจะเริ่มใน {task.delay_seconds} วินาที...')
    time.sleep(task.delay_seconds)

    # เปิด Browser
    webbrowser.open(task.url)
    time.sleep(2)

    # ค้นหาถ้ามี keyword
    if task.keyword:
        log_task(task, 'info', f'กำลังค้นหา: {task.keyword}')

        # Copy keyword และ Paste
        pyperclip.copy(task.keyword)
        pyautogui.hotkey('command', 'v')  # macOS
        time.sleep(1)

        # กด Enter
        pyautogui.press('enter')
        time.sleep(2)

    # จับภาพหน้าจอ
    screenshot_filename = f"{task.keyword or 'screenshot'}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot_path = os.path.join('screenshots', screenshot_filename)

    # สร้างโฟลเดอร์ถ้ายังไม่มี
    os.makedirs('screenshots', exist_ok=True)

    log_task(task, 'info', f'กำลังจับภาพหน้าจอ: {screenshot_filename}')
    pyautogui.screenshot(screenshot_path)

    # บันทึกผลลัพธ์
    task.mark_as_completed(screenshot_path=screenshot_path)
    log_task(task, 'success', f'บันทึกภาพที่: {screenshot_path}')


def run_screenshot(task):
    """รัน Task: จับภาพหน้าจอเท่านั้น"""
    log_task(task, 'info', 'กำลังจับภาพหน้าจอ...')

    time.sleep(task.delay_seconds)

    screenshot_filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    screenshot_path = os.path.join('screenshots', screenshot_filename)

    os.makedirs('screenshots', exist_ok=True)

    pyautogui.screenshot(screenshot_path)

    task.mark_as_completed(screenshot_path=screenshot_path)
    log_task(task, 'success', f'บันทึกภาพที่: {screenshot_path}')


def run_web_automation(task):
    """รัน Task: Web Automation แบบกำหนดเอง"""
    log_task(task, 'info', 'กำลังรัน Web Automation...')

    # TODO: Implement custom automation logic
    # สามารถเพิ่ม logic ที่ซับซ้อนกว่านี้ได้

    time.sleep(task.delay_seconds)
    webbrowser.open(task.url)
    time.sleep(2)

    task.mark_as_completed()
    log_task(task, 'success', 'Web Automation เสร็จสิ้น')
