from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import Customer, Loan
from .utils import calculate_credit_score, calculate_monthly_installment


class CreditSystemTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
    def test_customer_registration(self):
        """Test customer registration endpoint"""
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'age': 30,
            'monthly_income': 50000,  # API expects monthly_income
            'phone_number': '1234567890'
        }
        response = self.client.post('/loans/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        self.assertEqual(response.data['approved_limit'], 1800000)  # type: ignore
        
    def test_loan_eligibility(self):
        """Test loan eligibility check"""
        # Create a customer first
        customer = Customer.objects.create(  # type: ignore
            first_name='Test',
            last_name='User',
            age=30,
            phone_number='1234567890',
            monthly_salary=50000,
            approved_limit=1800000
        )
        
        data = {
            'customer_id': customer.customer_id,
            'loan_amount': 200000,
            'interest_rate': 10.5,
            'tenure': 12
        }
        response = self.client.post('/loans/check-eligibility/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # type: ignore
        
    def test_loan_creation(self):
        """Test loan creation endpoint"""
        customer = Customer.objects.create(  # type: ignore
            first_name='Test',
            last_name='User',
            age=30,
            phone_number='1234567890',
            monthly_salary=50000,
            approved_limit=1800000
        )
        
        data = {
            'customer_id': customer.customer_id,
            'loan_amount': 200000,
            'interest_rate': 12.0,
            'tenure': 12
        }
        response = self.client.post('/loans/create-loan/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # type: ignore
        
    def test_credit_score_calculation(self):
        """Test credit score calculation"""
        customer = Customer.objects.create(  # type: ignore
            first_name='Test',
            last_name='User',
            age=30,
            phone_number='1234567890',
            monthly_salary=50000,
            approved_limit=1800000
        )
        
        # Test with no loans (should return 50)
        score = calculate_credit_score(customer)
        self.assertEqual(score, 50)
        
    def test_monthly_installment_calculation(self):
        """Test EMI calculation"""
        emi = calculate_monthly_installment(100000, 12, 12.0)
        self.assertIsInstance(emi, float)
        self.assertGreater(emi, 0)
