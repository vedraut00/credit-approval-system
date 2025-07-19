# Credit Approval System

A comprehensive Django-based credit approval system that automates loan processing, eligibility checking, and customer management. The system uses machine learning principles to calculate credit scores and determine loan approval based on historical data and customer profiles.

## 🚀 Features

- **Customer Registration**: Register new customers with automatic approved limit calculation
- **Loan Eligibility Check**: Real-time loan eligibility assessment based on credit score
- **Loan Creation**: Automated loan approval and creation with EMI calculation
- **Credit Score Calculation**: Advanced algorithm considering payment history, loan activity, and debt ratios
- **Data Ingestion**: Bulk data import from Excel files
- **RESTful API**: Complete API endpoints for all operations
- **Dockerized**: Fully containerized application with PostgreSQL and Redis

## 🏗️ Architecture

- **Backend**: Django 4.2.7 with Django REST Framework
- **Database**: PostgreSQL 14
- **Cache**: Redis 6.2
- **Task Queue**: Celery for background tasks
- **Containerization**: Docker & Docker Compose
- **Data Processing**: Pandas for Excel file processing

## 📋 Prerequisites

- Docker
- Docker Compose

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd credit_approval_system
```

### 2. Build and Start Services
```bash
docker compose up --build -d
```

### 3. Run Database Migrations
```bash
docker compose exec web python manage.py migrate
```

### 4. Ingest Sample Data (Optional)
```bash
# Copy data files to container
docker cp customer_data.xlsx credit_approval_system-web-1:/app/
docker cp loan_data.xlsx credit_approval_system-web-1:/app/

# Ingest data
docker compose exec web python manage.py ingest_data
```

### 5. Access the Application
- **API Base URL**: http://localhost:8000/loans/
- **Admin Interface**: http://localhost:8000/admin/

## 📚 API Endpoints

### 1. Customer Registration

**Linux/Mac (curl):**
```bash
curl -X POST http://localhost:8000/loans/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "age": 30,
    "monthly_income": 50000,
    "phone_number": "9876543210"
  }'
```

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/loans/register/" -Method POST -ContentType "application/json" -Body '{"first_name": "John", "last_name": "Doe", "age": 30, "monthly_income": 50000, "phone_number": "9876543210"}'
```

### 2. Loan Eligibility Check

**Linux/Mac (curl):**
```bash
curl -X POST http://localhost:8000/loans/check-eligibility/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "loan_amount": 200000,
    "interest_rate": 12.0,
    "tenure": 12
  }'
```

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/loans/check-eligibility/" -Method POST -ContentType "application/json" -Body '{"customer_id": 1, "loan_amount": 200000, "interest_rate": 12.0, "tenure": 12}'
```

### 3. Loan Creation

**Linux/Mac (curl):**
```bash
curl -X POST http://localhost:8000/loans/create-loan/ \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "loan_amount": 200000,
    "interest_rate": 12.0,
    "tenure": 12
  }'
```

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/loans/create-loan/" -Method POST -ContentType "application/json" -Body '{"customer_id": 1, "loan_amount": 200000, "interest_rate": 12.0, "tenure": 12}'
```

### 4. View Loan Details

**Linux/Mac (curl):**
```bash
curl http://localhost:8000/loans/view-loan/1/
```

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/loans/view-loan/1/" -Method GET
```

### 5. View Customer Loans

**Linux/Mac (curl):**
```bash
curl http://localhost:8000/loans/view-loans/1/
```

**Windows (PowerShell):**
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/loans/view-loans/1/" -Method GET
```

### 📋 Quick Test Commands (Windows)

**Copy-paste these commands to test all endpoints:**

```powershell
# 1. Register a new customer
Invoke-RestMethod -Uri "http://localhost:8000/loans/register/" -Method POST -ContentType "application/json" -Body '{"first_name": "John", "last_name": "Doe", "age": 30, "monthly_income": 50000, "phone_number": "9876543210"}'

# 2. Check loan eligibility
Invoke-RestMethod -Uri "http://localhost:8000/loans/check-eligibility/" -Method POST -ContentType "application/json" -Body '{"customer_id": 1, "loan_amount": 200000, "interest_rate": 12.0, "tenure": 12}'

# 3. Create a loan
Invoke-RestMethod -Uri "http://localhost:8000/loans/create-loan/" -Method POST -ContentType "application/json" -Body '{"customer_id": 1, "loan_amount": 200000, "interest_rate": 12.0, "tenure": 12}'

# 4. View loan details
Invoke-RestMethod -Uri "http://localhost:8000/loans/view-loan/1/" -Method GET

# 5. View customer loans
Invoke-RestMethod -Uri "http://localhost:8000/loans/view-loans/1/" -Method GET
```

## 🧪 Testing

Run the test suite:
```bash
docker compose exec web python manage.py test
```

## 📊 Credit Score Algorithm

The system calculates credit scores based on:

1. **Payment History (40%)**: Ratio of EMIs paid on time
2. **Loan History (20%)**: Number of previous loans
3. **Current Activity (20%)**: Loans taken in current year
4. **Loan Volume (20%)**: Total loan amount processed

## 🔧 Configuration

### Environment Variables
- `POSTGRES_DB`: Database name (default: credit_db)
- `POSTGRES_USER`: Database user (default: postgres)
- `POSTGRES_PASSWORD`: Database password (default: password)
- `POSTGRES_HOST`: Database host (default: db)
- `CELERY_BROKER_URL`: Redis URL for Celery (default: redis://redis:6379/0)

### Database Schema
- **Customers**: Customer information and approved limits
- **Loans**: Loan details, EMIs, and payment history

## 📁 Project Structure

```
credit_approval_system/
├── credit_system/          # Django project settings
├── loans/                  # Main application
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # Data serializers
│   ├── utils.py           # Business logic
│   ├── tasks.py           # Celery tasks
│   └── management/        # Custom commands
├── docker-compose.yml     # Docker services
├── Dockerfile            # Application container
├── requirements.txt      # Python dependencies
├── customer_data.xlsx    # Sample customer data
└── loan_data.xlsx        # Sample loan data
```

## 🐳 Docker Services

- **web**: Django application server
- **db**: PostgreSQL database
- **redis**: Redis cache server
- **celery**: Background task worker

## 📈 Performance Features

- **Caching**: Redis for session and task queue
- **Background Processing**: Celery for data ingestion
- **Database Optimization**: Proper indexing and queries
- **API Optimization**: Efficient serialization and response handling

## 🔒 Security Features

- **Input Validation**: Comprehensive data validation
- **SQL Injection Protection**: Django ORM protection
- **CSRF Protection**: Built-in Django security
- **Data Sanitization**: Proper data cleaning and validation

## 📝 License

This project is created for educational and demonstration purposes.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For any questions or issues, please create an issue in the GitHub repository. 
