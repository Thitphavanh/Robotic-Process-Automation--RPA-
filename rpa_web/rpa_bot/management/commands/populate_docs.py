from django.core.management.base import BaseCommand
from rpa_bot.models import DocSection


class Command(BaseCommand):
    help = 'Populate initial documentation sections'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating documentation sections...')

        sections_data = [
            # Getting Started
            {
                'title': 'Overview',
                'slug': 'overview',
                'icon': 'fa-home',
                'description': 'Introduction to RPA Bot and its core features',
                'group': 'getting_started',
                'order': 1,
                'content': '''
# Overview

RPA Bot is a production-ready automation framework for scraping, monitoring, and notifying across e-commerce, news, and custom data sources. It ships with a web UI, REST API, Celery worker pool, and Telegram alerts.

## Core Features

- **Automated Task Execution** — Schedule and run RPA tasks with retry/backoff, timeouts, and circuit-breaker style fail-safes.
- **AI-Powered Intelligence** — Summarize news and extract signals with **Google Gemini** and **Claude 3.5 Sonnet**.
- **Multi-Platform E-Commerce** — Track prices on Lazada, Shopee, Amazon, AliExpress, JD.com, and more (extensible adapters).
- **RESTful API** — Access everything via JSON; includes auth, pagination, filtering, and webhooks.
- **Real-time Notifications** — Telegram alerts for price drops, task failures, and digest summaries (email/Discord optional).
- **Observability** — Structured logging, metrics, and a task history dashboard.

## Architecture (High-Level)



[Web UI / REST API] ──> [Django 5]
│
├── Schedules / Models (PostgreSQL)
├── Task Queue (Celery)
│       └── Broker/Backend (Redis)
└── Workers (Scrapers, AI, Notifiers)


## Technology Stack

**Backend:** Django 5, Celery, Redis, PostgreSQL, httpx/requests, BeautifulSoup4, (optional) Selenium/Playwright  
**Frontend:** Alpine.js, Tailwind CSS, Chart.js, Font Awesome  
**AI/ML:** Google Gemini, Claude 3.5 Sonnet via Anthropic API

## Ready to get started?

Follow the quick start to set up your first automation in minutes.

[Get Started Now](?section=get-started)
'''
            },
            {
                'title': 'Get Started',
                'slug': 'get-started',
                'icon': 'fa-rocket',
                'description': 'Quick start guide to set up and run your first automation',
                'group': 'getting_started',
                'order': 2,
                'content': '''# Get Started

Follow these steps to bring RPA Bot online and run your first job.

## Prerequisites

- Python 3.10+  
- PostgreSQL 14+  
- Redis 6+  
- (Optional) Chrome/Chromium + chromedriver for Selenium tasks

## 1) Install & Configure


python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

Update `.env`:


DJANGO_SECRET_KEY=change-me
DATABASE_URL=postgres://user:pass@localhost:5432/rpabot
REDIS_URL=redis://localhost:6379/0
ALLOWED_HOSTS=localhost,127.0.0.1
TELEGRAM_BOT_TOKEN=xxxx
TELEGRAM_CHAT_ID=123456
ANTHROPIC_API_KEY=sk-...
GOOGLE_GEMINI_API_KEY=...


## 2) Migrate & Create Admin


python manage.py migrate
python manage.py createsuperuser


## 3) Seed Documentation (optional)


python manage.py populate_docs


## 4) Run Services (Dev)


# Terminal A
python manage.py runserver 0.0.0.0:8000

# Terminal B
celery -A config.celery_app worker -l info --concurrency=4

# Terminal C (optional periodic schedules)
celery -A config.celery_app beat -l info


## 5) Create Your First Task

* Go to **Tasks → New Task**
* Choose **E-commerce Price Watch** (e.g., Shopee product URL)
* Set a threshold and **Save**
* RPA Bot enqueues and runs the job; watch logs in **Task Runs**

That’s it!
'''
},


        # Core Features
        {
            'title': 'RPA Tasks',
            'slug': 'rpa-tasks',
            'icon': 'fa-robot',
            'description': 'Create and manage RPA automation tasks',
            'group': 'core_features',
            'order': 1,
            'content': '''# RPA Tasks


Tasks are versioned, typed jobs executed by Celery workers.

## Task Types (Built-in)

* **E-commerce Price Watch** — Track price/stock from Lazada, Shopee, Amazon, AliExpress, JD.com, etc.
* **News Crawler** — Fetch headlines/articles by source/keyword/region.
* **AI Summarizer** — Summarize raw text or URLs with Gemini / Claude.
* **Generic Scrape** — Fetch HTML/JSON and parse via CSS/XPath/JSONPath.

## Creating a Task

1. **Tasks → New Task**
2. Pick **Type** and paste **Target URL** (or config)
3. Optionally set **Schedule** (cron or every N minutes)
4. Define **Success criteria** (e.g., price < 999)
5. Enable **Notifications** and **Save**

## Task Runs & History

Every execution creates a **TaskRun** row with:

* status (success, failed, retrying)
* started/ended timestamps, duration
* payload/output snapshot
* logs (structured JSON)

## Retries & Timeouts

Each task supports:

* **Timeout**: abort long runs
* **Max Retries** with **exponential backoff**
* **Circuit breaker**: auto-disable after N consecutive failures

See **Scheduling & Retries** for details.
'''
},
{
'title': 'News Intelligence',
'slug': 'news-intelligence',
'icon': 'fa-newspaper',
'description': 'AI-powered news aggregation and analysis',
'group': 'core_features',
'order': 2,
'content': '''# News Intelligence

Aggregate, cluster, and summarize news into actionable signals.

## Sources

* RSS/Atom feeds
* Direct website scrapers (configurable adapters)
* API providers (where licensed)

## Workflow

1. **Ingest** articles on schedule
2. **Deduplicate** by URL/fingerprint
3. **Classify & Tag** (topics, entities, tone)
4. **Summarize** with Gemini/Claude
5. **Alert** when rules match (keywords, companies, sentiment, volume)

## Examples

* Alert when *"Raspberry Pi supply chain"* appears with **negative sentiment**
* Daily digest for **semiconductor** sector with **top 5 stories** and **TL;DR**

## Storage

* Normalized **Article** model with source metadata
* Embeddings (optional) for semantic search
  '''
  },
  {
  'title': 'AI Agent',
  'slug': 'ai-agent',
  'icon': 'fa-brain',
  'description': 'Intelligent market discovery and sentiment analysis',
  'group': 'core_features',
  'order': 3,
  'content': '''# AI Agent

An orchestration layer that chains tools (search, scrape, summarize, compare) to answer market questions.

## Capabilities

* **Ask**: "Is product X cheaper on Shopee or Lazada today?"
* **Reason**: Compare multiple URLs, extract prices, normalize units
* **Summarize**: Provide a concise, source-linked answer
* **Follow-ups**: Store state and refine queries

## Controls

* Max depth (# of pages)
* Max tokens/cost guardrails
* Domain allow/deny lists
* PII/leak prevention (redaction of tokens/headers)

## Extending

Add a new **Tool** (Python function) and register it in the agent’s toolset. Then reference it in policies for which prompts may call which tools.
'''
},
{
'title': 'E-Commerce Tracking',
'slug': 'ecommerce-tracking',
'icon': 'fa-shopping-cart',
'description': 'Track prices across major e-commerce platforms',
'group': 'core_features',
'order': 4,
'content': '''# E-Commerce Tracking

Monitor price/stock/ratings for products across multiple marketplaces.

## Supported (out-of-the-box)

* Lazada, Shopee, Amazon, AliExpress, JD.com
* (Adapters are plugin-based; add your own.)

## How It Works

* Fetch product page
* Parse price/stock with resilient selectors
* Normalize currency
* Persist **ProductSnapshot**
* Compare with last snapshot → **Triggers** (alerts/feeds)

## Anti-bot Tips

* Randomized headers & delays
* Rotating proxies (optional)
* Fallback to **Selenium** when dynamic rendering is required
* Respect robots/ToS and local laws
  '''
  },

  
        # Advanced
        {
            'title': 'Configuration',
            'slug': 'configuration',
            'icon': 'fa-sliders-h',
            'description': 'Environment variables and settings',
            'group': 'advanced',
            'order': 1,
            'content': '''# Configuration
  

All settings are environment-driven (12-factor). Key variables:


DJANGO_DEBUG=false
DJANGO_SECRET_KEY=...
ALLOWED_HOSTS=example.com

DATABASE_URL=postgres://user:pass@db:5432/rpabot
REDIS_URL=redis://redis:6379/0

# Celery
CELERY_BROKER_URL=${REDIS_URL}
CELERY_RESULT_BACKEND=${REDIS_URL}
CELERY_TASK_TIME_LIMIT=120
CELERY_TASK_SOFT_TIME_LIMIT=90

# AI
ANTHROPIC_API_KEY=...
GOOGLE_GEMINI_API_KEY=...

# Notifications
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...

# Security
CSRF_TRUSTED_ORIGINS=https://example.com


For per-task settings, use the **Task.config** JSON field and validate via pydantic schemas in adapters.
'''
},
{
'title': 'Scheduling & Retries',
'slug': 'scheduling-retries',
'icon': 'fa-clock',
'description': 'Cron, periodic tasks, backoff, timeouts',
'group': 'advanced',
'order': 2,
'content': '''# Scheduling & Retries

## Options

* **Celery Beat** for cron expressions / periodic tasks
* **Manual run** via UI / API
* **On-demand** triggers (e.g., webhook event)

## Retry Policy

* Default: **max_retries=3**, **backoff** = 2^n + jitter
* **Soft/Hard timeouts** protect workers
* **Circuit breaker**: disable task after N consecutive failures
* **Dead-letter** queue: failed payloads for manual replay

Example Celery config (Python):


CELERY_TASK_DEFAULT_QUEUE = "default"
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_TIME_LIMIT = 120
CELERY_TASK_SOFT_TIME_LIMIT = 90


'''
},
{
'title': 'Notifications',
'slug': 'notifications',
'icon': 'fa-bell',
'description': 'Telegram, email digests, and custom notifiers',
'group': 'advanced',
'order': 3,
'content': '''# Notifications

## Telegram

* Configure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
* Toggle at **Settings → Notifications**
* Choose events: price drop, task failure, daily digests

## Email / Discord (optional)

* Add SMTP or Discord webhook URL in `.env`
* Map events → channels per task or globally

## Templating

Messages are rendered via Jinja2 with variables:

* task name / id
* status / error
* key values (price, delta, link)
  '''
  },
  {
  'title': 'API Reference',
  'slug': 'api-reference',
  'icon': 'fa-code',
  'description': 'Complete API documentation and examples',
  'group': 'advanced',
  'order': 4,
  'content': '''# API Reference

All endpoints are JSON and require token auth (Bearer).

## Auth


POST /api/v1/auth/token  → { "token": "..." }


## Tasks


GET    /api/v1/tasks/             # list (filters: type, status)
POST   /api/v1/tasks/             # create
GET    /api/v1/tasks/{id}/        # detail
PATCH  /api/v1/tasks/{id}/        # update
POST   /api/v1/tasks/{id}/run/    # enqueue now


## Runs


GET  /api/v1/runs/?task_id=...    # history
GET  /api/v1/runs/{id}/           # logs, payload, output


## Articles / News


GET /api/v1/articles/?q=raspberry+pi&sentiment=neg


## Webhooks


POST /api/v1/webhooks/events/


### Example: Create & Run


curl -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type":"price_watch","url":"https://shopee...","threshold":999}' \
  https://example.com/api/v1/tasks/

curl -X POST -H "Authorization: Bearer $TOKEN" \
  https://example.com/api/v1/tasks/123/run/


'''
},
{
'title': 'Webhooks',
'slug': 'webhooks',
'icon': 'fa-plug',
'description': 'Push events to your systems',
'group': 'advanced',
'order': 5,
'content': '''# Webhooks

Subscribe an endpoint to receive JSON on selected events.

## Events

* `task.run.succeeded`
* `task.run.failed`
* `price.drop`
* `digest.daily`

## Payload Example


{
  "event": "price.drop",
  "occurred_at": "2025-10-26T12:34:56Z",
  "task_id": 123,
  "data": {
    "product": "XYZ Keyboard",
    "old_price": 1299,
    "new_price": 949,
    "currency": "THB",
    "url": "https://shopee/..."
  },
  "signature": "hmac-sha256=..."
}


Verify `signature` with your shared secret to ensure authenticity.
'''
},
{
'title': 'Deployment',
'slug': 'deployment',
'icon': 'fa-server',
'description': 'Deploy RPA Bot to production environments',
'group': 'advanced',
'order': 6,
'content': '''# Deployment

## Docker Compose (recommended)


services:
  web:
    build: .
    env_file: .env
    command: gunicorn config.wsgi:application -w 4 -b 0.0.0.0:8000
    depends_on: [db, redis]
  worker:
    build: .
    env_file: .env
    command: celery -A config.celery_app worker -l info --concurrency=8
    depends_on: [redis, db]
  beat:
    build: .
    env_file: .env
    command: celery -A config.celery_app beat -l info
    depends_on: [redis, db]
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: rpabot
      POSTGRES_USER: rpabot
      POSTGRES_PASSWORD: change-me
  redis:
    image: redis:7
  nginx:
    image: nginx:alpine
    volumes:
      - ./deploy/nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      - "80:80"
    depends_on: [web]


## Migrations & Static


python manage.py migrate
python manage.py collectstatic --noinput


## Health Checks

* `/healthz` (app)
* `/readiness` (db, redis ping, queue depth)

Scale **worker** service horizontally for throughput.
'''
},
{
'title': 'Observability',
'slug': 'observability',
'icon': 'fa-chart-line',
'description': 'Logs, metrics, alerts, and tracing',
'group': 'advanced',
'order': 7,
'content': '''# Observability

## Logs

* JSON logs with request IDs and task IDs
* Stream to ELK/Vector/CloudWatch

## Metrics

* Celery queue depth, run durations, success rate
* Error rates by task type / domain
* Expose Prometheus endpoint `/metrics` (optional add-on)

## Tracing

* OpenTelemetry hooks around HTTP calls and parsers
* Useful for flaky e-commerce adapters
  '''
  },
  {
  'title': 'Troubleshooting',
  'slug': 'troubleshooting',
  'icon': 'fa-life-ring',
  'description': 'Common issues and fixes',
  'group': 'advanced',
  'order': 8,
  'content': '''# Troubleshooting

## Workers not picking tasks

* Check Redis connectivity
* Ensure `CELERY_BROKER_URL` matches workers
* Verify timezones and Beat schedule entries

## Pages render empty (JS sites)

* Switch adapter to **Selenium/Playwright** mode
* Increase timeout; wait for selector `.price` before parsing

## Price parsed as 0 or None

* Marketplace changed markup → update adapter selector
* Add a backup selector and unit tests for parsing

## Telegram not sending

* Verify `TELEGRAM_BOT_TOKEN` and chat ID

* Bots can't DM users unless started; send `/start` to the bot
  '''
  },
  {
  'title': 'Security & Compliance',
  'slug': 'security',
  'icon': 'fa-shield-alt',
  'description': 'Secrets, permissions, robots, and legal notes',
  'group': 'advanced',
  'order': 9,
  'content': '''# Security & Compliance

* Store secrets in environment or a vault — never in Git.

* Per-user tokens for API access; rotate regularly.

* Respect robots.txt, site ToS, and applicable laws.

* Add rate-limits and domain allow-lists in adapters.

* Redact tokens from logs; enable PII scrubbing.
  '''
  },
  {
  'title': 'FAQ',
  'slug': 'faq',
  'icon': 'fa-question-circle',
  'description': 'Frequently asked questions',
  'group': 'advanced',
  'order': 10,
  'content': '''# FAQ

**Can I add a new marketplace?**
Yes. Create a new adapter class with `fetch(url) -> ProductSnapshot`. Register it in the adapter registry.

**Do I need Selenium?**
Only for heavy client-side sites. Prefer `httpx` + parsing first.

**How do I avoid getting blocked?**
Rotate headers/IPs, backoff on 429/5xx, and lower crawl rate. Follow site ToS.

**Can I push data to my system?**
Use **Webhooks** or the **REST API**.
'''
}
]

        created_count = 0
        updated_count = 0

        for section_data in sections_data:
            section, created = DocSection.objects.update_or_create(
                slug=section_data['slug'],
                defaults=section_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ Created: {section.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.WARNING(f'↻ Updated: {section.title}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {created_count}, Updated {updated_count} documentation sections.'
        ))
