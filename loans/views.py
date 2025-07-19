from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from decimal import Decimal
from datetime import date, timedelta
from .models import Customer, Loan
from .serializers import *
from .utils import (
    calculate_credit_score,
    calculate_monthly_installment,
    check_loan_eligibility,
    round_to_nearest_lakh
)


@api_view(['POST'])
def register_customer(request):
    """Register a new customer"""
    serializer = CustomerRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data  # type: ignore

        # Calculate approved limit (36 * monthly_salary, rounded to nearest lakh)
        approved_limit = round_to_nearest_lakh(36 * data['monthly_income'])  # type: ignore

        customer = Customer.objects.create(  # type: ignore
            first_name=data['first_name'],  # type: ignore
            last_name=data['last_name'],  # type: ignore
            age=data['age'],  # type: ignore
            phone_number=data['phone_number'],  # type: ignore
            monthly_salary=data['monthly_income'],  # type: ignore
            approved_limit=approved_limit
        )

        response_data = {
            'customer_id': customer.customer_id,
            'name': f"{customer.first_name} {customer.last_name}",
            'age': customer.age,
            'monthly_income': customer.monthly_salary,
            'approved_limit': customer.approved_limit,
            'phone_number': customer.phone_number
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def check_eligibility(request):
    """Check loan eligibility for a customer"""
    serializer = LoanEligibilitySerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data  # type: ignore

        try:
            customer = Customer.objects.get(customer_id=data['customer_id'])  # type: ignore
        except Customer.DoesNotExist:  # type: ignore
            return Response(
                {'error': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check loan eligibility
        is_eligible, credit_score, corrected_rate = check_loan_eligibility(
            customer,
            data['loan_amount'],  # type: ignore
            data['interest_rate'],  # type: ignore
            data['tenure']  # type: ignore
        )

        # Calculate monthly installment
        interest_rate_to_use = corrected_rate if corrected_rate else data['interest_rate']  # type: ignore
        monthly_installment = calculate_monthly_installment(
            data['loan_amount'],  # type: ignore
            data['tenure'],  # type: ignore
            interest_rate_to_use
        )

        response_data = {
            'customer_id': data['customer_id'],  # type: ignore
            'approval': is_eligible,
            'interest_rate': float(data['interest_rate']),  # type: ignore
            'corrected_interest_rate': float(corrected_rate) if corrected_rate else None,
            'tenure': data['tenure'],  # type: ignore
            'monthly_installment': monthly_installment
        }

        return Response(response_data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_loan(request):
    """Create a new loan"""
    serializer = LoanCreationSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data  # type: ignore

        try:
            customer = Customer.objects.get(customer_id=data['customer_id'])  # type: ignore
        except Customer.DoesNotExist:  # type: ignore
            return Response(
                {'error': 'Customer not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check eligibility
        is_eligible, credit_score, corrected_rate = check_loan_eligibility(
            customer,
            data['loan_amount'],  # type: ignore
            data['interest_rate'],  # type: ignore
            data['tenure']  # type: ignore
        )

        if not is_eligible:
            return Response({
                'loan_id': None,
                'customer_id': data['customer_id'],  # type: ignore
                'loan_approved': False,
                'message': 'Loan not approved due to low credit score or high current EMI',
                'monthly_installment': 0
            }, status=status.HTTP_200_OK)

        # Calculate monthly installment
        interest_rate_to_use = corrected_rate if corrected_rate else data['interest_rate']  # type: ignore
        monthly_installment = calculate_monthly_installment(
            data['loan_amount'],  # type: ignore
            data['tenure'],  # type: ignore
            interest_rate_to_use
        )

        # Create loan
        start_date = date.today()
        end_date = start_date + timedelta(days=data['tenure'] * 30)  # Approximate  # type: ignore

        loan = Loan.objects.create(  # type: ignore
            customer=customer,
            loan_amount=data['loan_amount'],  # type: ignore
            tenure=data['tenure'],  # type: ignore
            interest_rate=interest_rate_to_use,
            monthly_repayment=Decimal(str(monthly_installment)),
            emis_paid_on_time=0,  # Initialize to 0 for new loans
            start_date=start_date,
            end_date=end_date
        )

        return Response({
            'loan_id': loan.loan_id,
            'customer_id': data['customer_id'],  # type: ignore
            'loan_approved': True,
            'message': 'Loan approved successfully',
            'monthly_installment': monthly_installment
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def view_loan(request, loan_id):
    """View loan details"""
    try:
        loan = Loan.objects.select_related('customer').get(loan_id=loan_id)  # type: ignore
        serializer = LoanDetailSerializer(loan)
        return Response(serializer.data, status=status.HTTP_200_OK)  # type: ignore
    except Loan.DoesNotExist:  # type: ignore
        return Response(
            {'error': 'Loan not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def view_customer_loans(request, customer_id):
    """View all loans for a customer"""
    try:
        customer = Customer.objects.get(customer_id=customer_id)  # type: ignore
        loans = Loan.objects.filter(customer=customer)  # type: ignore
        serializer = CustomerLoanSerializer(loans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  # type: ignore
    except Customer.DoesNotExist:  # type: ignore
        return Response(
            {'error': 'Customer not found'},
            status=status.HTTP_404_NOT_FOUND
        )
