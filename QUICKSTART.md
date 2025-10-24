# 🚀 Quick Start Guide - Stock Bot AI

## ⚡ ใช้งานง่าย 3 ขั้นตอน

---

## 📋 ขั้นตอนที่ 1: เตรียมพร้อม

### ติดตั้ง Dependencies:
```bash
pip install pyautogui pillow anthropic python-dotenv
```

### สำหรับเวอร์ชัน OCR (ไม่ต้องใช้ API):
```bash
pip install pytesseract
brew install tesseract tesseract-lang
```

---

## 🔑 ขั้นตอนที่ 2: ตั้งค่า API Key

### วิธีที่ 1: ใช้ Environment Variable (แนะนำ)

```bash
# ตั้งค่า API Key
export ANTHROPIC_API_KEY='sk-ant-api03-your-actual-key-here'

# ตรวจสอบ
echo $ANTHROPIC_API_KEY

# เพื่อให้ใช้ได้ตลอด เพิ่มใน ~/.zshrc
echo "export ANTHROPIC_API_KEY='sk-ant-api03-your-key'" >> ~/.zshrc
source ~/.zshrc
```

### วิธีที่ 2: ใส่ตอนรันโปรแกรม

```bash
# รันโปรแกรม - จะถามเอง
python stock_bot_macos_agent.py

# จะมี prompt ให้ใส่:
🔑 API Key: [ใส่ API key ตรงนี้]
```

### วิธีที่ 3: ใช้เวอร์ชันฟรี (ไม่ต้อง API)

```bash
# ไม่ต้องตั้งค่าอะไร
python stock_bot_macos_no_api.py
```

---

## ▶️ ขั้นตอนที่ 3: รันโปรแกรม

### ทดสอบ API ก่อน (แนะนำ):
```bash
python test_anthropic_api.py
```

ถ้าเห็น:
```
✅ ทดสอบสำเร็จ! API Key ใช้งานได้
```

แสดงว่าพร้อมแล้ว!

### รัน Stock Bot AI:
```bash
python stock_bot_macos_agent.py
```

### หรือเวอร์ชันฟรี:
```bash
python stock_bot_macos_no_api.py
```

---

## 🎯 เลือกโหมดการทำงาน

เมื่อรันโปรแกรมจะมี 3 โหมดให้เลือก:

```
📋 เลือกโหมดการทำงาน:
   1. ค้นหาข้อมูลทั่วไป (Dynamic Search)
   2. ค้นหาข้อมูลหุ้นไทย (Stock Focus)
   3. กำหนดเอง (Custom Query)

🔢 เลือกโหมด (1-3):
```

### โหมด 1: Dynamic Search
- ค้นหาอะไรก็ได้
- เหมาะกับ: วิจัยหัวข้อใหม่ๆ

### โหมด 2: Stock Focus (แนะนำ)
- ค้นหา "ราคาหุ้นไทยวันนี้" อัตโนมัติ
- เหมาะกับ: ดูข้อมูลหุ้นประจำวัน

### โหมด 3: Custom Query
- กำหนดคำค้นหาและคำสั่งวิเคราะห์เอง
- เหมาะกับ: งานเฉพาะทาง

---

## 📁 ไฟล์ Output ที่ได้

หลังรันเสร็จจะได้:

```
ai_search_results.png          # ภาพหน้าค้นหา
ai_website_01_main.png         # ภาพเว็บที่ 1
ai_website_01_scrolled.png     # ภาพเว็บที่ 1 (หลัง scroll)
ai_website_02_main.png         # ภาพเว็บที่ 2
...
ai_analysis_report.txt         # รายงานสรุป AI
```

---

## ⚙️ การตั้งค่า macOS Permissions

**สำคัญ!** ต้องอนุญาตก่อนใช้งาน:

### 1. Accessibility Permission
1. **System Settings** → **Privacy & Security** → **Accessibility**
2. คลิก **+** เพิ่ม **Terminal** หรือ **iTerm**
3. เปิดสวิตช์

### 2. Screen Recording Permission
1. **System Settings** → **Privacy & Security** → **Screen Recording**
2. คลิก **+** เพิ่ม **Terminal** หรือ **iTerm**
3. เปิดสวิตช์

**⚠️ Restart Terminal หลังตั้งค่าเสร็จ!**

---

## 🔍 ตัวอย่างการใช้งาน

### ตัวอย่างที่ 1: เช็คหุ้นประจำวัน
```bash
python stock_bot_macos_agent.py

# เลือกโหมด 2
🔢 เลือกโหมด (1-3): 2

# เลือกจำนวนเว็บ
🌐 จำนวนเว็บไซต์ (1-10): 3
```

### ตัวอย่างที่ 2: ค้นหาข้อมูลบริษัท
```bash
python stock_bot_macos_agent.py

# เลือกโหมด 1
🔢 เลือกโหมด (1-3): 1

# ใส่คำค้นหา
🔍 ใส่คำค้นหา: PTT stock price today

# เลือกจำนวนเว็บ
🌐 จำนวนเว็บไซต์ (1-10): 5
```

### ตัวอย่างที่ 3: วิเคราะห์เฉพาะทาง
```bash
python stock_bot_macos_agent.py

# เลือกโหมด 3
🔢 เลือกโหมด (1-3): 3

# ใส่คำค้นหา
🔍 ใส่คำค้นหา: cryptocurrency market analysis

# ใส่คำสั่งวิเคราะห์
📝 ใส่คำสั่งวิเคราะห์: วิเคราะห์แนวโน้มตลาด crypto พร้อมแนะนำ
```

---

## 💰 ค่าใช้จ่าย

### AI Version (stock_bot_macos_agent.py):
- ต่อครั้ง: ~$0.10 - $0.50
- ต่อวัน (1 ครั้ง): ~$3 - $15/เดือน
- Free tier: $5 credit เมื่อสมัครใหม่

### Free OCR Version (stock_bot_macos_no_api.py):
- **ฟรี 100%!**
- ไม่มีค่าใช้จ่ายเลย
- ใช้ Tesseract OCR แทน AI

---

## 🆘 แก้ปัญหาเร็ว

### ปัญหา: "401 authentication_error"
```bash
# ได้ API key ใหม่จาก
# https://console.anthropic.com/settings/keys

# ตั้งค่าใหม่
export ANTHROPIC_API_KEY='your-new-key'

# ทดสอบ
python test_anthropic_api.py
```

### ปัญหา: "No module named 'anthropic'"
```bash
pip install anthropic
```

### ปัญหา: "No module named 'pytesseract'" (OCR version)
```bash
pip install pytesseract
brew install tesseract tesseract-lang
```

### ปัญหา: ถ่ายภาพไม่ได้
```bash
# ตั้งค่า Screen Recording permission
# System Settings > Privacy & Security > Screen Recording
# เพิ่ม Terminal และ Restart
```

### ปัญหา: คลิกผิดตำแหน่ง
- ตรวจสอบ browser zoom ต้องเป็น 100%
- ปิด browser tabs อื่นที่ไม่ใช้
- ลองเพิ่มเวลา sleep ใน code

---

## 🎓 เริ่มต้นแบบง่ายที่สุด

**ถ้ายังไม่มี API Key:**
```bash
# ใช้เวอร์ชันฟรี
pip install pyautogui pillow pytesseract
brew install tesseract
python stock_bot_macos_no_api.py
```

**ถ้ามี API Key แล้ว:**
```bash
# ตั้งค่า
export ANTHROPIC_API_KEY='your-key'

# ทดสอบ
python test_anthropic_api.py

# รัน
python stock_bot_macos_agent.py
```

---

## 📊 Workflow แนะนำ

### สำหรับผู้เริ่มต้น:
1. เริ่มจาก `stock_bot_macos.py` (version พื้นฐาน)
2. ลองใช้ `stock_bot_macos_no_api.py` (OCR ฟรี)
3. ถ้าพอใจ ค่อยอัปเกรดเป็น AI version

### สำหรับผู้ใช้ประจำ:
1. ใช้ `stock_bot_macos_agent.py` (AI version)
2. ตั้งค่า API key ใน environment variable
3. รันทุกเช้าเพื่อเช็คตลาด

### สำหรับผู้เชี่ยวชาญ:
1. Customize website lists
2. ปรับ position coordinates
3. เพิ่ม custom analysis prompts
4. Schedule with cron

---

## 🔄 การอัปเดต

ตรวจสอบว่าใช้ model ล่าสุด:

```python
# ใน stock_bot_macos_agent.py
model="claude-sonnet-4-20250514"  # ✅ Claude Sonnet 4.5 (Latest & Most Capable)
```

ถ้าเห็น `claude-3-5-sonnet-20241022` หรือ `claude-3-7-sonnet-20250219` แสดงว่าเวอร์ชันเก่า

**Claude Sonnet 4.5 ดีกว่ายังไง:**
- 🎯 ความแม่นยำในการวิเคราะห์ภาพสูงขึ้น
- 🧠 เข้าใจบริบทภาษาไทยดีขึ้นมาก
- 📊 วิเคราะห์ข้อมูลตลาดหุ้นแม่นยำกว่า
- ⚡ ประมวลผลเร็วขึ้น

---

## 🎉 สรุป

### ใช้งานด่วน 3 คำสั่ง:

```bash
# 1. ติดตั้ง
pip install pyautogui pillow anthropic python-dotenv

# 2. ตั้งค่า API
export ANTHROPIC_API_KEY='your-key'

# 3. รัน!
python stock_bot_macos_agent.py
```

### หรือเวอร์ชันฟรี:

```bash
# 1. ติดตั้ง
pip install pyautogui pillow pytesseract
brew install tesseract

# 2. รัน! (ไม่ต้องตั้ง API)
python stock_bot_macos_no_api.py
```

---

**🎯 เริ่มต้นได้เลย! ไม่ยาก ใช้เวลาแค่ 5 นาที**

**💡 มีปัญหา? อ่าน README.md หรือ README_API_KEY.md**

---

**Made with ❤️ for automated stock market research**
