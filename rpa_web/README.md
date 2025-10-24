# RPA Bot Manager - Django Web Application

🤖 ระบบจัดการ Robotic Process Automation (RPA) Bot ด้วย Django, TailwindCSS และ JavaScript

## ✨ Features

- 📊 **Dashboard** - ภาพรวมสถิติและ Tasks ทั้งหมด
- ✅ **Task Management** - สร้าง แก้ไข ลบ และจัดการ Tasks
- 🚀 **Auto Execution** - รัน Tasks อัตโนมัติ
- 📸 **Screenshot Capture** - จับภาพหน้าจอผลลัพธ์
- 📝 **Real-time Logs** - ติดตามการทำงานแบบ Real-time
- 🎨 **Modern UI** - ออกแบบด้วย TailwindCSS
- 📱 **Responsive** - รองรับทุกอุปกรณ์

## 🛠️ Tech Stack

- **Backend**: Django 5.0
- **Frontend**: TailwindCSS, Alpine.js
- **Database**: SQLite (เปลี่ยนเป็น PostgreSQL ได้)
- **RPA**: PyAutoGUI, Pyperclip

## 📦 Installation

### 1. Clone หรือ Copy โปรเจค

```bash
cd rpa_web
```

### 2. สร้าง Virtual Environment

```bash
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า macOS Permissions (สำคัญ!)

**สำหรับ macOS:**
1. เปิด **System Settings** → **Privacy & Security** → **Accessibility**
2. เพิ่ม **Terminal** หรือ **Python**
3. เปิดใช้งาน (toggle เป็นสีเขียว)
4. รีสตาร์ท Terminal

### 5. Migrate Database

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. สร้าง Superuser (สำหรับ Admin)

```bash
python manage.py createsuperuser
```

### 7. รัน Server

```bash
python manage.py runserver
```

เปิด browser: **http://localhost:8000**

## 📖 การใช้งาน

### สร้าง Task ใหม่

1. ไปที่หน้า Dashboard
2. คลิก "สร้าง Task ใหม่"
3. กรอกข้อมูล:
   - **ชื่อ Task**: ชื่อที่ต้องการ
   - **ประเภท Task**: เลือกประเภท (Google Search, Screenshot, etc.)
   - **URL**: URL ที่ต้องการเปิด
   - **คำค้นหา**: คำค้นหา (ถ้าเป็น Google Search)
   - **หน่วงเวลา**: เวลารอก่อนเริ่ม (วินาที)
4. คลิก "สร้าง Task"

### รัน Task

1. ไปที่รายละเอียด Task
2. คลิกปุ่ม "รัน Task"
3. ระบบจะรัน Task ใน background
4. ดูผลลัพธ์และ Logs แบบ real-time

### ดู Logs

- Logs จะแสดงใน Task Detail
- Auto-refresh ทุก 3 วินาที
- มี 4 levels: Info, Warning, Error, Success

## 🎯 Task Types

### 1. Google Search
- เปิด Google
- ค้นหาตาม keyword
- จับภาพหน้าจอผลลัพธ์

### 2. Screenshot
- จับภาพหน้าจอปัจจุบัน

### 3. Web Automation
- เปิดเว็บไซต์ตาม URL
- สามารถเพิ่ม custom logic ได้

### 4. Data Extraction
- (Coming Soon) ดึงข้อมูลจากเว็บไซต์

## 📁 โครงสร้างโปรเจค

```
rpa_web/
├── config/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── rpa_bot/               # Main app
│   ├── models.py         # Database models
│   ├── views.py          # Views logic
│   ├── urls.py           # URL routing
│   ├── admin.py          # Admin configuration
│   ├── rpa_runner.py     # RPA execution logic
│   └── templates/        # HTML templates
│       └── rpa_bot/
│           ├── base.html
│           ├── dashboard.html
│           ├── task_list.html
│           ├── task_form.html
│           └── task_detail.html
├── manage.py
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Database
แก้ไขใน `config/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'rpa_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Time Zone
```python
TIME_ZONE = 'Asia/Bangkok'
LANGUAGE_CODE = 'th'
```

## 🚀 Production Deployment

### 1. Environment Variables
สร้างไฟล์ `.env`:

```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### 2. Collect Static Files
```bash
python manage.py collectstatic
```

### 3. Use Gunicorn
```bash
pip install gunicorn
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## 🐛 Troubleshooting

### PyAutoGUI ไม่ทำงาน
- ตรวจสอบ Accessibility permissions
- ลอง run ด้วย `sudo` (ไม่แนะนำใน production)

### Task ไม่รัน
- ตรวจสอบ Logs ใน Task Detail
- ดูว่ามี error message หรือไม่

### Import Error
```bash
pip install -r requirements.txt --upgrade
```

## 📝 API Endpoints

### Get Task Status
```
GET /api/tasks/<id>/status/
```

### Get Task Logs
```
GET /api/tasks/<id>/logs/
```

### Create Task
```
POST /api/tasks/create/
Content-Type: application/json

{
  "name": "Task Name",
  "task_type": "google_search",
  "url": "https://www.google.com",
  "keyword": "search term"
}
```

### Run Task
```
POST /api/tasks/<id>/run/
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT License

## 👨‍💻 Author

Created with ❤️ for RPA automation

## 🙏 Acknowledgments

- Django Framework
- TailwindCSS
- Alpine.js
- PyAutoGUI
- Font Awesome Icons

docker compose build --no-cache