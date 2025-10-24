# 🚀 คู่มือการติดตั้งและใช้งาน RPA Bot Manager

## ขั้นตอนการติดตั้งอย่างละเอียด

### 1️⃣ ติดตั้ง Python Dependencies

```bash
cd rpa_web
python -m venv venv

# สำหรับ macOS/Linux
source venv/bin/activate

# สำหรับ Windows
venv\Scripts\activate

# ติดตั้ง packages
pip install -r requirements.txt
```

### 2️⃣ ตั้งค่า macOS Accessibility Permissions (สำคัญมาก!)

**ทำไมต้องตั้งค่า?**
- PyAutoGUI ต้องการสิทธิ์ในการควบคุมคอมพิวเตอร์
- ถ้าไม่ตั้งค่า Bot จะไม่สามารถพิมพ์ข้อความหรือจับภาพหน้าจอได้

**วิธีตั้งค่า:**

1. เปิด **System Settings** (หรือ System Preferences)
2. ไปที่ **Privacy & Security**
3. เลือก **Accessibility** ทางซ้าย
4. คลิก **ปุ่ม Lock** ล่างซ้าย แล้วใส่รหัสผ่าน
5. คลิก **+** เพื่อเพิ่มแอพ
6. เลือก:
   - **Terminal** (ถ้ารันจาก Terminal)
   - **iTerm** (ถ้าใช้ iTerm)
   - **VS Code** (ถ้ารันจาก VS Code)
   - **PyCharm** (ถ้ารันจาก PyCharm)
7. เปิด toggle ให้เป็นสีเขียว ✅
8. **รีสตาร์ท Terminal/IDE**

### 3️⃣ สร้าง Database

```bash
# สร้าง migrations
python manage.py makemigrations

# รัน migrations
python manage.py migrate
```

### 4️⃣ สร้าง Superuser (สำหรับเข้า Admin)

```bash
python manage.py createsuperuser

# กรอกข้อมูล:
# Username: admin
# Email: admin@example.com
# Password: ********
# Password (again): ********
```

### 5️⃣ รัน Development Server

```bash
python manage.py runserver

# Server จะรันที่: http://127.0.0.1:8000/
```

### 6️⃣ เข้าใช้งานระบบ

**หน้าหลัก:**
```
http://localhost:8000/
```

**Django Admin:**
```
http://localhost:8000/admin/
Login: admin / รหัสผ่านที่ตั้งไว้
```

---

## 📝 การใช้งานครั้งแรก

### สร้าง Task แรก

1. **เปิดเว็บไซต์**: http://localhost:8000/
2. คลิก **"สร้าง Task ใหม่"**
3. กรอกข้อมูล:

```
ชื่อ Task: ค้นหาอุณหภูมิกรุงเทพ
คำอธิบาย: ค้นหาอุณหภูมิปัจจุบันในกรุงเทพ
ประเภท Task: ค้นหา Google
URL: https://www.google.com
คำค้นหา: อุณหภูมิกรุงเทพ
หน่วงเวลา: 3 วินาที
ลองใหม่สูงสุด: 3 ครั้ง
```

4. คลิก **"สร้าง Task"**

### รัน Task

1. ไปที่หน้า **Task Detail**
2. คลิกปุ่ม **"รัน Task"** สีเขียว
3. **สำคัญ**: อย่าไปขยับเมาส์หรือพิมพ์อะไรในขณะที่ Bot กำลังทำงาน!
4. รอจนกว่า Task จะเสร็จ (สถานะเปลี่ยนเป็น "สำเร็จ")
5. ดูภาพหน้าจอที่จับได้ในโฟลเดอร์ `screenshots/`

---

## 🔧 แก้ปัญหาที่พบบ่อย

### ❌ PyAutoGUI ไม่ทำงาน

**อาการ:**
```
Task ล้มเหลว: ไม่สามารถควบคุมเมาส์/คีย์บอร์ดได้
```

**แก้ไข:**
1. ตรวจสอบ Accessibility permissions อีกครั้ง
2. รีสตาร์ท Terminal
3. ลองรันใหม่

### ❌ Import Error: No module named 'pyautogui'

**แก้ไข:**
```bash
pip install pyautogui pyperclip
```

### ❌ Task รันแต่ไม่พิมพ์อะไร

**สาเหตุ:**
- Browser เปิดช้า Task เลยพิมพ์ก่อน browser โหลดเสร็จ

**แก้ไข:**
- เพิ่มค่า "หน่วงเวลา" เป็น 5-10 วินาที

### ❌ Screenshot ไม่มีภาพ

**ตรวจสอบ:**
```bash
ls screenshots/
```

**แก้ไข:**
- สร้างโฟลเดอร์ `screenshots` ด้วยตัวเอง:
```bash
mkdir screenshots
```

### ❌ Django Admin ไม่มี RPA Tasks

**แก้ไข:**
```bash
python manage.py migrate
python manage.py createsuperuser
```

---

## 🎯 ทดสอบว่าระบบทำงานถูกต้อง

### Test 1: ทดสอบ PyAutoGUI

สร้างไฟล์ `test_rpa.py`:

```python
import pyautogui
import time

print("Test จะเริ่มใน 3 วินาที...")
time.sleep(3)

# ทดสอบพิมพ์
pyautogui.write("Hello World")
print("สำเร็จ!")
```

รัน:
```bash
python test_rpa.py
```

### Test 2: ทดสอบ Database

```bash
python manage.py shell

# ใน shell:
from rpa_bot.models import RPATask
print(RPATask.objects.count())
```

### Test 3: ทดสอบ Web Server

เปิด browser ไปที่:
- ✅ http://localhost:8000/ - Dashboard
- ✅ http://localhost:8000/tasks/ - รายการ Tasks
- ✅ http://localhost:8000/admin/ - Admin Panel

---

## 📊 โครงสร้างโปรเจค

```
rpa_web/
├── 📁 config/               # การตั้งค่า Django
│   ├── settings.py         # ⚙️ Settings หลัก
│   ├── urls.py             # 🔗 URL routing หลัก
│   ├── wsgi.py
│   └── asgi.py
│
├── 📁 rpa_bot/             # App หลัก
│   ├── models.py           # 🗄️ Database Models
│   ├── views.py            # 👁️ Views Logic
│   ├── urls.py             # 🔗 App URLs
│   ├── admin.py            # 👑 Admin Config
│   ├── rpa_runner.py       # 🤖 RPA Runner
│   │
│   └── 📁 templates/rpa_bot/
│       ├── base.html       # 📄 Base Template
│       ├── dashboard.html  # 📊 Dashboard
│       ├── task_list.html  # 📋 Task List
│       ├── task_form.html  # ✏️ Create/Edit Form
│       └── task_detail.html # 🔍 Task Detail
│
├── 📁 screenshots/         # 📸 ภาพที่จับได้ (สร้างอัตโนมัติ)
├── 📁 media/               # 📁 Media files
├── 📁 static/              # 🎨 Static files
│
├── manage.py               # 🎮 Django Management
├── requirements.txt        # 📦 Dependencies
├── README.md              # 📖 Documentation
└── .gitignore             # 🙈 Git Ignore
```

---

## 🚀 คำสั่งที่ใช้บ่อย

### Development
```bash
# รัน server
python manage.py runserver

# สร้าง migrations
python manage.py makemigrations

# รัน migrations
python manage.py migrate

# สร้าง superuser
python manage.py createsuperuser

# เข้า Django shell
python manage.py shell
```

### Database
```bash
# Reset database (ระวัง! ลบข้อมูลทั้งหมด)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Deployment
```bash
# Collect static files
python manage.py collectstatic

# Check deployment
python manage.py check --deploy
```

---

## 🎓 เรียนรู้เพิ่มเติม

### Django Documentation
- https://docs.djangoproject.com/

### TailwindCSS
- https://tailwindcss.com/docs

### PyAutoGUI
- https://pyautogui.readthedocs.io/

### Alpine.js
- https://alpinejs.dev/

---

## 💡 Tips & Tricks

1. **เพิ่มความเร็ว**: ลด interval ใน `pyautogui.write()` ใน `rpa_runner.py`
2. **Debug**: เปิด Django Debug Toolbar
3. **Logging**: ดู Logs ใน Task Detail แบบ real-time
4. **API**: ใช้ API endpoints สำหรับ automation
5. **Scheduling**: ใช้ Celery สำหรับ scheduled tasks

---

## 🆘 ขอความช่วยเหลือ

หากพบปัญหา:
1. ตรวจสอบ Logs ใน Task Detail
2. ดู Error Message
3. ตรวจสอบ Terminal output
4. อ่าน README.md

---

## ✅ Checklist ก่อนใช้งาน

- [ ] ติดตั้ง Python 3.8+
- [ ] สร้าง Virtual Environment
- [ ] ติดตั้ง Dependencies (`pip install -r requirements.txt`)
- [ ] ตั้งค่า Accessibility Permissions (macOS)
- [ ] รัน Migrations
- [ ] สร้าง Superuser
- [ ] ทดสอบ PyAutoGUI
- [ ] รัน Development Server
- [ ] เปิด Browser ที่ localhost:8000
- [ ] สร้าง Task ทดสอบ
- [ ] รัน Task และตรวจสอบผลลัพธ์

**เมื่อทำครบทุกข้อแล้ว พร้อมใช้งาน! 🎉**
