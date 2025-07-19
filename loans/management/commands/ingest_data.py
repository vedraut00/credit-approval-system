from django.core.management.base import BaseCommand
from loans.tasks import ingest_customer_data, ingest_loan_data


class Command(BaseCommand):
    help = 'Ingest customer and loan data from Excel files'
    
    def handle(self, *args, **options):
        self.stdout.write('Starting data ingestion...')
        
        # Ingest customer data
        self.stdout.write('Ingesting customer data...')
        customer_result = ingest_customer_data()
        self.stdout.write(f'Customer data: {customer_result}')
        
        # Ingest loan data
        self.stdout.write('Ingesting loan data...')
        loan_result = ingest_loan_data()
        self.stdout.write(f'Loan data: {loan_result}')
        
        self.stdout.write('Data ingestion completed successfully!')