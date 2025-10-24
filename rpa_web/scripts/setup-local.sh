#!/bin/bash
# Local development setup (without Docker)

set -e

echo "🚀 Setting up RPA Bot Manager (Local Development)..."

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "📝 Creating .env..."
    cp .env.dev .env
fi

# Create directories
echo "📁 Creating directories..."
mkdir -p logs screenshots media staticfiles

# Run migrations
echo "🔄 Running migrations..."
export DJANGO_SETTINGS_MODULE=config.settings.dev
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo "👤 Creating superuser..."
python manage.py createsuperuser

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup complete!"
echo "🚀 Run the development server with:"
echo "   python manage.py runserver"
echo ""
echo "🌐 Access at: http://localhost:8000"
echo "🔧 Admin: http://localhost:8000/admin"
