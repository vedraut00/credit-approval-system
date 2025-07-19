import pandas as pd
from celery import shared_task
from decimal import Decimal
from datetime import datetime
from .models import Customer, Loan
import logging

logger = logging.getLogger(__name__)


@shared_task
def ingest_customer_data():
    """Background task to ingest customer data from Excel file"""
    try:
        df = pd.read_excel('/app/customer_data.xlsx')
        customers_created = 0
        
        for _, row in df.iterrows():
            try:
                customer, created = Customer.objects.get_or_create(  # type: ignore
                    customer_id=row['Customer ID'],
                    defaults={
                        'first_name': row['First Name'],
                        'last_name': row['Last Name'],
                        'age': int(row['Age']),
                        'phone_number': str(row['Phone Number']),
                        'monthly_salary': Decimal(str(row['Monthly Salary'])),
                        'approved_limit': Decimal(str(row['Approved Limit'])),
                        'current_debt': 0,
                    }
                )
                if created:
                    customers_created += 1
                    logger.info(f"Created customer: {customer.first_name} {customer.last_name}")
            except Exception as e:
                logger.error(f"Error creating customer {row['Customer ID']}: {str(e)}")
                continue
        
        return f"Successfully ingested {customers_created} customers"
    except Exception as e:
        logger.error(f"Error ingesting customer data: {str(e)}")
        return f"Error ingesting customer data: {str(e)}"


@shared_task
def ingest_loan_data():
    """Background task to ingest loan data from Excel file"""
    try:
        df = pd.read_excel('/app/loan_data.xlsx')
        loans_created = 0
        
        for _, row in df.iterrows():
            try:
                customer = Customer.objects.get(customer_id=row['Customer ID'])  # type: ignore
                
                # Convert date strings to datetime objects
                start_date = pd.to_datetime(row['Date of Approval']).date()  # type: ignore
                end_date = pd.to_datetime(row['End Date']).date()  # type: ignore
                
                loan, created = Loan.objects.get_or_create(  # type: ignore
                    loan_id=row['Loan ID'],
                    defaults={
                        'customer': customer,
                        'loan_amount': Decimal(str(row['Loan Amount'])),
                        'tenure': int(row['Tenure']),
                        'interest_rate': Decimal(str(row['Interest Rate'])),
                        'monthly_repayment': Decimal(str(row['Monthly payment'])),
                        'emis_paid_on_time': int(row['EMIs paid on Time']),
                        'start_date': start_date,
                        'end_date': end_date,
                    }
                )
                if created:
                    loans_created += 1
                    logger.info(f"Created loan: {loan.loan_id} for customer {customer.first_name}")
                    
            except Customer.DoesNotExist:  # type: ignore
                logger.warning(f"Customer {row['Customer ID']} not found for loan {row['Loan ID']}")
                continue
            except Exception as e:
                logger.error(f"Error creating loan {row['Loan ID']}: {str(e)}")
                continue
                
        return f"Successfully ingested {loans_created} loans"
    except Exception as e:
        logger.error(f"Error ingesting loan data: {str(e)}")
        return f"Error ingesting loan data: {str(e)}"