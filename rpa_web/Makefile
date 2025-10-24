.PHONY: help dev prod setup clean migrate shell test lint

help:
	@echo "RPA Bot Manager - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make dev          - Start development environment (Docker)"
	@echo "  make setup        - Setup local development (without Docker)"
	@echo "  make shell        - Open Django shell"
	@echo "  make migrate      - Run database migrations"
	@echo "  make superuser    - Create superuser"
	@echo ""
	@echo "Production:"
	@echo "  make prod         - Start production environment (Docker)"
	@echo "  make prod-build   - Build production containers"
	@echo ""
	@echo "Testing & Quality:"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run code quality checks"
	@echo "  make format       - Format code with black and isort"
	@echo ""
	@echo "Maintenance:"
	@echo "  make logs         - View container logs"
	@echo "  make clean        - Clean up containers and volumes"
	@echo "  make backup       - Backup database"

# Development
dev:
	@bash scripts/docker-dev.sh

setup:
	@bash scripts/setup-local.sh

shell:
	docker-compose exec web python manage.py shell

migrate:
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate

superuser:
	docker-compose exec web python manage.py createsuperuser

# Production
prod:
	@bash scripts/docker-prod.sh

prod-build:
	docker-compose -f docker-compose.prod.yml build

# Testing
test:
	docker-compose exec web pytest

lint:
	docker-compose exec web flake8 .
	docker-compose exec web pylint rpa_bot/

format:
	docker-compose exec web black .
	docker-compose exec web isort .

# Maintenance
logs:
	docker-compose logs -f

logs-prod:
	docker-compose -f docker-compose.prod.yml logs -f

clean:
	docker-compose down -v
	rm -rf __pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

backup:
	docker-compose exec db pg_dump -U rpa_user rpa_db > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Docker commands
build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

restart:
	docker-compose restart

ps:
	docker-compose ps
