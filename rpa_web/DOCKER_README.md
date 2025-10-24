# 🐳 Docker Deployment Guide - RPA Bot Manager

คู่มือการใช้งาน Docker สำหรับ RPA Bot Manager

---

## 📋 สารบัญ

1. [Quick Start](#quick-start)
2. [Development Setup](#development-setup)
3. [Production Deployment](#production-deployment)
4. [Architecture](#architecture)
5. [Commands](#commands)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Development (รวดเร็วที่สุด)

```bash
# 1. Copy environment file
cp .env.dev .env

# 2. Start everything
make dev

# หรือ
bash scripts/docker-dev.sh

# 3. เข้าใช้งาน
open http://localhost:8000
```

### Production

```bash
# 1. แก้ไข environment variables
nano .env.prod

# 2. Start production
make prod

# หรือ
bash scripts/docker-prod.sh
```

---

## 💻 Development Setup

### ข้อกำหนด

- Docker 20.10+
- Docker Compose 2.0+
- Make (optional)

### 1. ติดตั้ง Docker

**macOS:**
```bash
brew install --cask docker
# หรือดาวน์โหลด Docker Desktop
```

**Linux (Ubuntu):**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER
```

### 2. Clone & Setup

```bash
cd rpa_web

# Copy environment file
cp .env.dev .env

# ปรับแต่ง .env ถ้าต้องการ
nano .env
```

### 3. Build & Start

```bash
# วิธีที่ 1: ใช้ Makefile (แนะนำ)
make dev

# วิธีที่ 2: ใช้ script
bash scripts/docker-dev.sh

# วิธีที่ 3: ใช้ docker-compose โดยตรง
docker-compose up -d --build
```

### 4. ตรวจสอบสถานะ

```bash
# ดูสถานะ containers
docker-compose ps

# ดู logs
docker-compose logs -f

# ดู logs เฉพาะ web
docker-compose logs -f web
```

### 5. เข้าถึงแอพพลิเคชัน

- **Web App**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

### 6. สร้าง Superuser

```bash
docker-compose exec web python manage.py createsuperuser

# หรือ
make superuser
```

---

## 🏭 Production Deployment

### Architecture

```
Internet
    ↓
[Nginx:80/443] → Reverse Proxy & Static Files
    ↓
[Gunicorn:8000] → Django Application
    ↓
[PostgreSQL:5432] → Database
[Redis:6379] → Cache & Celery Broker
[Celery Worker] → Background Tasks
[Celery Beat] → Scheduled Tasks
[Flower:5555] → Celery Monitoring
```

### 1. เตรียม Environment

```bash
# Copy production env
cp .env.example .env.prod

# แก้ไข .env.prod (สำคัญมาก!)
nano .env.prod
```

**ต้องเปลี่ยน:**
```bash
DJANGO_SECRET_KEY=your-very-long-random-string-here
POSTGRES_PASSWORD=strong-password-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Build Production

```bash
# Build containers
docker-compose -f docker-compose.prod.yml build

# หรือ
make prod-build
```

### 3. Start Production

```bash
# Start all services
docker-compose -f docker-compose.prod.yml up -d

# หรือ
make prod
```

### 4. Setup SSL (Let's Encrypt)

```bash
# สร้างใบรับรอง SSL
docker-compose -f docker-compose.prod.yml run --rm certbot \
  certonly --webroot --webroot-path=/var/www/certbot \
  -d yourdomain.com -d www.yourdomain.com

# Reload Nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload
```

### 5. Monitoring

**Flower (Celery Tasks):**
```
http://your-domain:5555
```

**Logs:**
```bash
# All logs
docker-compose -f docker-compose.prod.yml logs -f

# Specific service
docker-compose -f docker-compose.prod.yml logs -f web
docker-compose -f docker-compose.prod.yml logs -f celery
```

---

## 🏗️ Architecture Details

### Services

#### 1. **db** (PostgreSQL)
- Database สำหรับเก็บข้อมูล
- Port: 5432
- Volume: `postgres_data`

#### 2. **redis**
- Cache และ Message Broker
- Port: 6379
- Volume: `redis_data`

#### 3. **web** (Django)
- Application server
- Port: 8000
- Development: Django runserver
- Production: Gunicorn

#### 4. **nginx** (Production only)
- Reverse proxy
- Static file serving
- SSL termination
- Port: 80, 443

#### 5. **celery** (Worker)
- Background task processing
- รัน RPA tasks

#### 6. **celery-beat** (Scheduler)
- Scheduled tasks
- Cron jobs

#### 7. **flower** (Production only)
- Celery monitoring UI
- Port: 5555

---

## 📝 Commands Reference

### Makefile Commands

```bash
# Development
make dev              # Start dev environment
make setup            # Local setup (no Docker)
make migrate          # Run migrations
make superuser        # Create superuser
make shell            # Django shell

# Production
make prod             # Start production
make prod-build       # Build production

# Testing
make test             # Run tests
make lint             # Code quality checks
make format           # Format code

# Maintenance
make logs             # View logs
make clean            # Clean up
make backup           # Backup database
```

### Docker Compose Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build

# View logs
docker-compose logs -f [service]

# Execute command
docker-compose exec [service] [command]

# Scale workers
docker-compose up -d --scale celery=3
```

### Common Tasks

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic

# Django shell
docker-compose exec web python manage.py shell

# Database shell
docker-compose exec db psql -U rpa_user -d rpa_db

# Redis CLI
docker-compose exec redis redis-cli

# View running tasks
docker-compose exec web celery -A config inspect active
```

---

## 🔍 Environment Variables

### Development (.env.dev)

```bash
DJANGO_SETTINGS_MODULE=config.settings.dev
DEBUG=True
POSTGRES_DB=rpa_db
POSTGRES_USER=rpa_user
POSTGRES_PASSWORD=rpa_password_dev
```

### Production (.env.prod)

```bash
DJANGO_SETTINGS_MODULE=config.settings.prod
DEBUG=False
DJANGO_SECRET_KEY=your-secret-key
POSTGRES_PASSWORD=strong-password
ALLOWED_HOSTS=yourdomain.com
```

---

## 🐛 Troubleshooting

### Container ไม่ start

```bash
# ดู logs
docker-compose logs [service]

# ตรวจสอบสถานะ
docker-compose ps

# Restart service
docker-compose restart [service]
```

### Database connection failed

```bash
# ตรวจสอบว่า database พร้อมหรือไม่
docker-compose exec db pg_isready

# รอ database สักครู่แล้ว restart web
docker-compose restart web
```

### Port ถูกใช้แล้ว

```bash
# หา process ที่ใช้ port
lsof -i :8000

# เปลี่ยน port ใน docker-compose.yml
ports:
  - "8001:8000"  # เปลี่ยนจาก 8000 เป็น 8001
```

### Permission denied

```bash
# Fix permissions
sudo chown -R $USER:$USER .

# หรือเพิ่ม user ใน docker group
sudo usermod -aG docker $USER
```

### Clean everything

```bash
# หยุดและลบทุกอย่าง
docker-compose down -v

# ลบ images
docker-compose down --rmi all

# เริ่มใหม่
docker-compose up -d --build
```

---

## 📊 Performance Tuning

### Scale Workers

```bash
# เพิ่ม Celery workers
docker-compose up -d --scale celery=5

# ใน production
docker-compose -f docker-compose.prod.yml up -d --scale celery=10
```

### Database Optimization

```bash
# Vacuum database
docker-compose exec db vacuumdb -U rpa_user -d rpa_db

# Analyze
docker-compose exec db vacuumdb -U rpa_user -d rpa_db --analyze
```

---

## 🔐 Security Best Practices

1. **เปลี่ยน Secret Key**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

2. **ใช้ Strong Passwords**
3. **เปิด HTTPS (SSL)**
4. **จำกัด ALLOWED_HOSTS**
5. **ตั้งค่า Firewall**
6. **Backup ข้อมูลสม่ำเสมอ**

---

## 📦 Backup & Restore

### Backup

```bash
# Database backup
docker-compose exec db pg_dump -U rpa_user rpa_db > backup.sql

# หรือใช้ Make
make backup

# Backup media files
tar -czf media_backup.tar.gz media/
tar -czf screenshots_backup.tar.gz screenshots/
```

### Restore

```bash
# Restore database
cat backup.sql | docker-compose exec -T db psql -U rpa_user -d rpa_db

# Restore media
tar -xzf media_backup.tar.gz
tar -xzf screenshots_backup.tar.gz
```

---

## 🚀 CI/CD Integration

### GitHub Actions Example

```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to production
        run: |
          ssh user@server 'cd /app && git pull && make prod'
```

---

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Django Deployment](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [Nginx Configuration](https://nginx.org/en/docs/)

---

## 🆘 Support

หากพบปัญหา:
1. ตรวจสอบ logs: `docker-compose logs -f`
2. ดู README.md
3. ตรวจสอบ Environment variables

---

**สร้างด้วย ❤️ สำหรับ RPA Bot Manager**
