# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=config.settings.dev

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY rpa_web /app/

# Create necessary directories
RUN mkdir -p /app/logs /app/screenshots /app/staticfiles /app/media

# Collect static files
RUN python manage.py collectstatic --noinput --settings=config.settings.dev || true

# Expose port
EXPOSE 8000

# Run migrations and start server
CMD python manage.py migrate --settings=config.settings.dev && \
    python manage.py runserver 0.0.0.0:8000 --settings=config.settings.dev
