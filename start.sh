#!/bin/bash

echo "🚀 Starting Credit Approval System..."

# Build and start all services
echo "📦 Building and starting Docker services..."
docker compose up --build -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Run migrations
echo "🗄️ Running database migrations..."
docker compose exec web python manage.py migrate

# Check if data files exist and ingest them
if [ -f "customer_data.xlsx" ] && [ -f "loan_data.xlsx" ]; then
    echo "📊 Ingesting sample data..."
    docker cp customer_data.xlsx $(docker compose ps -q web):/app/
    docker cp loan_data.xlsx $(docker compose ps -q web):/app/
    docker compose exec web python manage.py ingest_data
else
    echo "⚠️ Data files not found. Skipping data ingestion."
fi

# Run tests
echo "🧪 Running tests..."
docker compose exec web python manage.py test

echo "✅ Credit Approval System is ready!"
echo "🌐 Access the application at: http://localhost:8000/loans/"
echo "📚 API Documentation available in README.md"
echo ""
echo "📋 Useful commands:"
echo "  - View logs: docker compose logs web"
echo "  - Stop services: docker compose down"
echo "  - Restart services: docker compose restart" 