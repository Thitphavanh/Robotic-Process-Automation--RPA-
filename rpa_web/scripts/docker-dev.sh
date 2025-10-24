#!/bin/bash
# Development Docker script

set -e

echo "🚀 Starting RPA Bot Manager (Development)..."

# Copy environment file if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env from .env.dev..."
    cp .env.dev .env
fi

# Build and start containers
echo "🏗️ Building Docker containers..."
docker-compose build

echo "🚀 Starting containers..."
docker-compose up -d

# Wait for database
echo "⏳ Waiting for database..."
sleep 5

# Run migrations
echo "🔄 Running migrations..."
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

# Create superuser if needed
echo "👤 Creating superuser (optional)..."
docker-compose exec web python manage.py createsuperuser --noinput || true

# Collect static files
echo "📦 Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput

echo "✅ Development environment is ready!"
echo "🌐 Access the application at: http://localhost:8000"
echo "🔧 Admin panel: http://localhost:8000/admin"
echo ""
echo "📊 View logs with: docker-compose logs -f"
echo "🛑 Stop with: docker-compose down"
