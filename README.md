# RPA Bot Manager

A Django-based Robotic Process Automation (RPA) system with news scraping and AI summarization capabilities.

## Features

- News article scraping and management
- AI-powered content summarization
- Task scheduling with Celery
- Daily reports generation
- Web dashboard for monitoring

## Docker Setup

### Prerequisites

- Docker installed on your system
- Docker Compose (comes with Docker Desktop)

### Quick Start

1. Build and start all services:
```bash
docker compose up --build
```

2. Access the application:
- Web interface: http://localhost:8000
- Django admin: http://localhost:8000/admin

### Services

The application runs multiple services:
- **web**: Django application server (port 8000)
- **redis**: Message broker for Celery
- **celery**: Background task worker
- **celery-beat**: Scheduled task runner

### Common Commands

Stop all services:
```bash
docker compose down
```

View logs:
```bash
docker compose logs -f
```

View specific service logs:
```bash
docker compose logs -f web
docker compose logs -f celery
```

Rebuild after code changes:
```bash
docker compose up --build
```

Run Django management commands:
```bash
docker compose exec web python manage.py <command>
```

### Database Migrations

Migrations run automatically on startup. To run them manually:
```bash
docker compose exec web python manage.py migrate --settings=config.settings.dev
```

### Create Superuser

```bash
docker compose exec web python manage.py createsuperuser --settings=config.settings.dev
```

## Development

### Local Setup (without Docker)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
cd rpa_web
python manage.py migrate --settings=config.settings.dev
```

3. Start Redis (required for Celery):
```bash
redis-server
```

4. Start Django server:
```bash
python manage.py runserver --settings=config.settings.dev
```

5. Start Celery worker (in another terminal):
```bash
celery -A config worker -l info
```

6. Start Celery beat (in another terminal):
```bash
celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Project Structure

```
├── rpa_web/
│   ├── config/              # Django project settings
│   │   ├── settings/        # Environment-specific settings
│   │   ├── celery.py       # Celery configuration
│   │   └── urls.py         # URL routing
│   └── rpa_bot/            # Main application
│       ├── models.py       # Database models
│       ├── views.py        # View functions
│       ├── tasks.py        # Celery tasks
│       ├── news_scraper.py # News scraping logic
│       └── ai_summarizer.py # AI summarization
├── requirements.txt        # Python dependencies
├── Dockerfile             # Docker image definition
└── docker-compose.yml     # Multi-container setup
```

## Technologies

- **Django 5.0**: Web framework
- **Celery**: Distributed task queue
- **Redis**: Message broker
- **BeautifulSoup4**: Web scraping
- **Selenium**: Browser automation
