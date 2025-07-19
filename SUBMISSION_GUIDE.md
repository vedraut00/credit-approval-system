# 🚀 Credit Approval System - Submission Guide

## 📋 Project Overview

This is a fully dockerized credit approval system built with Django that automates loan processing, eligibility checking, and customer management. The entire application runs from a single Docker Compose command as required.

## 🎯 Key Requirements Met

✅ **Fully Dockerized**: All components (Django app, PostgreSQL, Redis, Celery) are containerized  
✅ **Single Command Deployment**: Runs with `docker compose up --build -d`  
✅ **Complete Database**: PostgreSQL with all dependencies  
✅ **Production Ready**: Proper configuration and security measures  
✅ **Comprehensive Testing**: All tests passing  
✅ **Documentation**: Complete README and API documentation  

## 🚀 Quick Start for Evaluators

### Prerequisites
- Docker Desktop installed
- Docker Compose available

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd credit_approval_system
```

### Step 2: Start the Application (Single Command)
```bash
docker compose up --build -d
```

### Step 3: Run Migrations
```bash
docker compose exec web python manage.py migrate
```

### Step 4: Ingest Sample Data (Optional)
```bash
# Copy data files
docker cp customer_data.xlsx credit_approval_system-web-1:/app/
docker cp loan_data.xlsx credit_approval_system-web-1:/app/

# Ingest data
docker compose exec web python manage.py ingest_data
```

### Step 5: Access the Application
- **API Base URL**: http://localhost:8000/loans/
- **Admin Interface**: http://localhost:8000/admin/

## 🧪 Testing the Application

### Run All Tests
```bash
docker compose exec web python manage.py test
```

### Test API Endpoints

1. **Customer Registration**:
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

2. **Loan Eligibility Check**:
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

3. **Loan Creation**:
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

4. **View Loan Details**:
```bash
curl http://localhost:8000/loans/view-loan/1/
```

5. **View Customer Loans**:
```bash
curl http://localhost:8000/loans/view-loans/1/
```

## 🏗️ Architecture

### Docker Services
- **web**: Django application server (Gunicorn)
- **db**: PostgreSQL 14 database
- **redis**: Redis 6.2 cache server
- **celery**: Background task worker

### Technology Stack
- **Backend**: Django 4.2.7 + Django REST Framework
- **Database**: PostgreSQL 14
- **Cache**: Redis 6.2
- **Task Queue**: Celery
- **Containerization**: Docker & Docker Compose
- **Data Processing**: Pandas for Excel ingestion

## 📊 Features Implemented

### Core Functionality
- ✅ Customer registration with automatic approved limit calculation
- ✅ Real-time loan eligibility assessment
- ✅ Automated loan approval and creation
- ✅ Advanced credit score calculation algorithm
- ✅ EMI calculation using compound interest formula
- ✅ Bulk data ingestion from Excel files

### API Endpoints
- ✅ `POST /loans/register/` - Customer registration
- ✅ `POST /loans/check-eligibility/` - Loan eligibility check
- ✅ `POST /loans/create-loan/` - Loan creation
- ✅ `GET /loans/view-loan/{id}/` - View loan details
- ✅ `GET /loans/view-loans/{customer_id}/` - View customer loans

### Business Logic
- ✅ Credit score calculation (payment history, loan activity, volume)
- ✅ Interest rate correction based on credit score
- ✅ EMI affordability check (50% of monthly income)
- ✅ Approved limit calculation (36x monthly income)
- ✅ Data validation and error handling

## 🔧 Configuration

### Environment Variables
All configuration is handled through environment variables in `docker-compose.yml`:
- Database credentials
- Redis connection
- Django settings

### Database Schema
- **Customers**: Personal info, approved limits, current debt
- **Loans**: Loan details, EMIs, payment history, dates

## 📈 Performance & Security

### Performance Features
- Redis caching for sessions and task queue
- Background processing with Celery
- Optimized database queries
- Efficient API serialization

### Security Features
- Input validation and sanitization
- SQL injection protection (Django ORM)
- CSRF protection
- Proper error handling

## 🧪 Test Coverage

The application includes comprehensive tests covering:
- ✅ Model validation
- ✅ API endpoint functionality
- ✅ Business logic calculations
- ✅ Data serialization
- ✅ Error handling

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
├── README.md            # Comprehensive documentation
├── start.sh             # Linux/Mac startup script
├── start.bat            # Windows startup script
├── customer_data.xlsx   # Sample customer data
└── loan_data.xlsx       # Sample loan data
```

## 🎯 Evaluation Checklist

- ✅ **Dockerization**: All components containerized
- ✅ **Single Command**: `docker compose up --build -d` starts everything
- ✅ **Database**: PostgreSQL with proper configuration
- ✅ **API Functionality**: All endpoints working
- ✅ **Business Logic**: Credit scoring and loan processing
- ✅ **Data Ingestion**: Excel file processing
- ✅ **Testing**: All tests passing
- ✅ **Documentation**: Complete README and guides
- ✅ **Error Handling**: Proper validation and error responses
- ✅ **Performance**: Optimized queries and caching

## 🚀 Deployment Verification

To verify the deployment works correctly:

1. **Start Services**: `docker compose up --build -d`
2. **Check Status**: `docker compose ps` (all services should be healthy)
3. **Run Tests**: `docker compose exec web python manage.py test`
4. **Test API**: Use the curl commands above
5. **Check Logs**: `docker compose logs web`

## 📞 Support

If you encounter any issues:
1. Check the logs: `docker compose logs web`
2. Verify Docker is running: `docker --version`
3. Check service status: `docker compose ps`
4. Restart if needed: `docker compose restart`

The application is designed to be robust and self-contained. All dependencies are included in the Docker containers. 