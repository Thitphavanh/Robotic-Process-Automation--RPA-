from django.core.management.base import BaseCommand
from rpa_bot.models import DocSection

class Command(BaseCommand):
    help = 'Populate documentation content with code examples (Nextra-style)'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating documentation content with code examples...')

        # Overview Section
        overview = DocSection.objects.filter(slug='overview').first()
        if overview:
            overview.content = '''
<h2>Welcome to RPA Bot Documentation</h2>
<p>RPA Bot is a powerful automation platform built with Django that helps you automate repetitive tasks, scrape news, track e-commerce prices, and leverage AI for intelligent decision-making.</p>

<h3>Quick Start</h3>
<p>Get started with RPA Bot in minutes:</p>

<pre><code class="language-bash"># Clone the repository
git clone https://github.com/your-repo/rpa-bot.git
cd rpa-bot

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start the development server
python manage.py runserver</code></pre>

<div class="callout info">
<strong>Note:</strong> Make sure you have Python 3.10+ and PostgreSQL installed before starting.
</div>

<h3>Key Features</h3>
<ul>
<li><strong>RPA Tasks:</strong> Automate web scraping and data extraction</li>
<li><strong>News Intelligence:</strong> AI-powered news aggregation with sentiment analysis</li>
<li><strong>AI Agent:</strong> Dynamic market discovery using Claude AI</li>
<li><strong>E-Commerce Tracking:</strong> Monitor prices across 11+ platforms</li>
</ul>

<h3>Architecture</h3>
<p>RPA Bot is built with modern technologies:</p>

<pre><code class="language-python">TECH_STACK = {
    "framework": "Django 5.0",
    "database": "PostgreSQL",
    "cache": "Redis",
    "task_queue": "Celery",
    "ai": "Google Gemini + Anthropic Claude",
    "frontend": "Tailwind CSS + Alpine.js"
}</code></pre>
            '''
            overview.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Updated: {overview.title}'))

        # Get Started Section
        get_started = DocSection.objects.filter(slug='get-started').first()
        if get_started:
            get_started.content = '''
<h2>Getting Started</h2>
<p>This guide will help you set up your RPA Bot development environment.</p>

<h3>Prerequisites</h3>
<ul>
<li>Python 3.10 or higher</li>
<li>PostgreSQL 14+</li>
<li>Redis (for Celery)</li>
<li>Git</li>
</ul>

<h3>Installation</h3>

<h4>1. Clone and Setup</h4>
<pre><code class="language-bash"># Clone repository
git clone https://github.com/your-repo/rpa-bot.git
cd rpa-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt</code></pre>

<h4>2. Configure Environment</h4>
<p>Create a <code>.env.dev</code> file:</p>

<pre><code class="language-bash">SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/rpa_bot
REDIS_URL=redis://localhost:6379/0

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Anthropic Claude
ANTHROPIC_API_KEY=your-claude-api-key

# Telegram (optional)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-chat-id</code></pre>

<div class="callout warning">
<strong>Security Warning:</strong> Never commit your <code>.env</code> file to version control. Add it to <code>.gitignore</code>.
</div>

<h4>3. Database Setup</h4>
<pre><code class="language-bash"># Create database
createdb rpa_bot

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate initial data
python manage.py populate_docs
python manage.py populate_doc_content</code></pre>

<h4>4. Run Development Server</h4>
<pre><code class="language-bash"># Terminal 1: Django server
python manage.py runserver

# Terminal 2: Celery worker
celery -A config worker -l info

# Terminal 3: Celery beat (scheduler)
celery -A config beat -l info</code></pre>

<p>Visit <a href="http://localhost:8000">http://localhost:8000</a> to see your RPA Bot!</p>

<h3>Next Steps</h3>
<p>Now that you have RPA Bot running, explore:</p>
<ul>
<li>Create your first RPA task</li>
<li>Set up news sources</li>
<li>Configure AI agents</li>
<li>Track e-commerce products</li>
</ul>
            '''
            get_started.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Updated: {get_started.title}'))

        # RPA Tasks Section
        rpa_tasks = DocSection.objects.filter(slug='rpa-tasks').first()
        if rpa_tasks:
            rpa_tasks.content = '''
<h2>RPA Tasks</h2>
<p>Learn how to create and manage automated tasks with RPA Bot.</p>

<h3>Creating a Task</h3>
<p>Create a new RPA task programmatically:</p>

<pre><code class="language-python">from rpa_bot.models import RPATask

# Create a Google search task
task = RPATask.objects.create(
    name="Search Python Tutorials",
    description="Search for Python tutorials on Google",
    task_type="google_search",
    url="https://www.google.com",
    keyword="Python tutorials 2025",
    delay_seconds=3,
    max_retries=3
)

# Execute the task
from rpa_bot.rpa_runner import run_rpa_task
run_rpa_task(task)</code></pre>

<h3>Task Types</h3>
<p>RPA Bot supports multiple task types:</p>

<pre><code class="language-python">TASK_TYPES = [
    ("google_search", "Google Search"),
    ("screenshot", "Screenshot Capture"),
    ("web_automation", "Web Automation"),
    ("data_extraction", "Data Extraction"),
]</code></pre>

<h3>API Usage</h3>
<p>Use the REST API to manage tasks:</p>

<pre><code class="language-bash"># Create task via API
curl -X POST http://localhost:8000/api/tasks/create/ \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "My Task",
    "task_type": "google_search",
    "url": "https://www.google.com",
    "keyword": "RPA automation"
  }'

# Get task status
curl http://localhost:8000/api/tasks/my-task/status/

# Run task
curl -X POST http://localhost:8000/api/tasks/my-task/run/</code></pre>

<div class="callout info">
<strong>Tip:</strong> Use Celery for long-running tasks to avoid timeouts.
</div>

<h3>Monitoring Tasks</h3>
<p>Monitor task execution:</p>

<pre><code class="language-python">from rpa_bot.models import RPATask, TaskLog

# Get all running tasks
running_tasks = RPATask.objects.filter(status="running")

# Get task logs
task = RPATask.objects.get(slug="my-task")
logs = task.logs.all().order_by('-created_at')

for log in logs:
    print(f"[{log.level}] {log.message}")</code></pre>
            '''
            rpa_tasks.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Updated: {rpa_tasks.title}'))

        # AI Agent Section
        ai_agent = DocSection.objects.filter(slug='ai-agent').first()
        if ai_agent:
            ai_agent.content = '''
<h2>AI Agent</h2>
<p>Use AI to discover market trends, analyze sentiment, and make intelligent decisions.</p>

<h3>Stock Discovery</h3>
<p>Discover top stocks using Claude AI:</p>

<pre><code class="language-python">from rpa_bot.ai_agent import get_ai_agent

# Initialize AI agent
agent = get_ai_agent()

# Discover top Thai stocks
thai_stocks = agent.discover_top_stocks(market="thai", limit=10)

for stock in thai_stocks:
    print(f"{stock['symbol']}: {stock['reason']}")

# Output:
# PTT: Leading energy company with strong fundamentals
# KBANK: Major commercial bank with digital transformation
# ...</code></pre>

<h3>Crypto Discovery</h3>
<pre><code class="language-python"># Discover trending cryptocurrencies
cryptos = agent.discover_top_crypto(limit=10)

for crypto in cryptos:
    print(f"{crypto['symbol']}: ${crypto['price']}")
    print(f"Trend: {crypto['trend']}")
    print(f"Reason: {crypto['reason']}\\n")</code></pre>

<h3>Sentiment Analysis</h3>
<p>Analyze market sentiment:</p>

<pre><code class="language-python"># Analyze US market sentiment
sentiment = agent.analyze_market_sentiment(market="us")

print(f"Sentiment: {sentiment['sentiment']}")
print(f"Confidence: {sentiment['confidence']}")
print(f"Summary: {sentiment['summary']}")</code></pre>

<div class="callout success">
<strong>Pro Tip:</strong> Combine AI insights with price tracking for automated trading signals.
</div>

<h3>Configuration</h3>
<p>Configure AI agent settings:</p>

<pre><code class="language-python"># config/settings/base.py

AI_AGENT_CONFIG = {
    "model": "claude-3-5-sonnet-20241022",
    "max_tokens": 2000,
    "temperature": 0.7,
    "timeout": 30,
}</code></pre>
            '''
            ai_agent.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Updated: {ai_agent.title}'))

        # API Reference Section
        api_ref = DocSection.objects.filter(slug='api-reference').first()
        if api_ref:
            api_ref.content = '''
<h2>API Reference</h2>
<p>Complete API documentation for RPA Bot.</p>

<h3>Authentication</h3>
<p>Most endpoints require authentication:</p>

<pre><code class="language-bash">curl -H "Authorization: Bearer YOUR_API_TOKEN" \\
     http://localhost:8000/api/tasks/</code></pre>

<h3>Tasks API</h3>

<h4>List Tasks</h4>
<pre><code class="language-http">GET /api/tasks/
Response: 200 OK

{
  "tasks": [
    {
      "id": 1,
      "name": "My Task",
      "slug": "my-task",
      "status": "completed",
      "created_at": "2025-01-15T10:00:00Z"
    }
  ]
}</code></pre>

<h4>Create Task</h4>
<pre><code class="language-http">POST /api/tasks/create/
Content-Type: application/json

{
  "name": "New Task",
  "task_type": "google_search",
  "url": "https://www.google.com",
  "keyword": "Django RPA"
}

Response: 200 OK
{
  "success": true,
  "task_id": 123,
  "message": "สร้าง Task สำเร็จ"
}</code></pre>

<h3>News API</h3>

<h4>Latest Report</h4>
<pre><code class="language-bash">curl http://localhost:8000/api/news/latest-report/</code></pre>

<pre><code class="language-json">{
  "success": true,
  "report": {
    "id": 1,
    "report_date": "2025-01-15",
    "is_sent": true,
    "full_report": "..."
  }
}</code></pre>

<h3>E-Commerce API</h3>

<h4>Track Product</h4>
<pre><code class="language-python">import requests

response = requests.post(
    "http://localhost:8000/api/ecommerce/track/",
    json={
        "product_url": "https://shopee.co.th/product/123",
        "enable_price_alert": True,
        "target_price": 999.00
    }
)

data = response.json()
print(f"Tracking: {data['product']['title']}")
print(f"Current price: ${data['product']['current_price']}")</code></pre>

<div class="callout warning">
<strong>Rate Limits:</strong> API is limited to 100 requests per minute per IP.
</div>
            '''
            api_ref.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Updated: {api_ref.title}'))

        self.stdout.write(self.style.SUCCESS('\n✅ Documentation content updated successfully!'))
        self.stdout.write(self.style.SUCCESS('Visit /docs/overview/ to see the changes.'))
