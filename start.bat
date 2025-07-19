@echo off
echo Starting Credit Approval System...

REM Build and start all services
echo Building and starting Docker services...
docker compose up --build -d

REM Wait for services to be ready
echo Waiting for services to be ready...
timeout /t 30 /nobreak > nul

REM Run migrations
echo Running database migrations...
docker compose exec web python manage.py migrate

REM Check if data files exist and ingest them
if exist "customer_data.xlsx" (
    if exist "loan_data.xlsx" (
        echo Ingesting sample data...
        docker cp customer_data.xlsx credit_approval_system-web-1:/app/
        docker cp loan_data.xlsx credit_approval_system-web-1:/app/
        docker compose exec web python manage.py ingest_data
    )
) else (
    echo Data files not found. Skipping data ingestion.
)

REM Run tests
echo Running tests...
docker compose exec web python manage.py test

echo Credit Approval System is ready!
echo Access the application at: http://localhost:8000/loans/
echo API Documentation available in README.md
echo.
echo Useful commands:
echo   - View logs: docker compose logs web
echo   - Stop services: docker compose down
echo   - Restart services: docker compose restart
pause 