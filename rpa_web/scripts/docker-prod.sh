#!/bin/bash
# Production Docker script

set -e

echo "🚀 Starting RPA Bot Manager (Production)..."

# Check if .env.prod exists
if [ ! -f .env.prod ]; then
    echo "❌ Error: .env.prod not found!"
    echo "📝 Please create .env.prod from .env.example"
    exit 1
fi

# Build and start containers
echo "🏗️ Building Docker containers for production..."
docker-compose -f docker-compose.prod.yml build

echo "🚀 Starting containers..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for database
echo "⏳ Waiting for database..."
sleep 10

# Run migrations
echo "🔄 Running migrations..."
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput

# Collect static files
echo "📦 Collecting static files..."
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Create superuser
echo "👤 Create superuser manually with:"
echo "docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"

echo "✅ Production environment is ready!"
echo "🌐 Application running on port 80 (via Nginx)"
echo ""
echo "📊 View logs with: docker-compose -f docker-compose.prod.yml logs -f"
echo "🛑 Stop with: docker-compose -f docker-compose.prod.yml down"
