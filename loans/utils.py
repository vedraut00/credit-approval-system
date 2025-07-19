from decimal import Decimal
from datetime import datetime, date
from .models import Loan, Customer
import math


def calculate_credit_score(customer):
    """Calculate credit score based on historical data"""
    loans = Loan.objects.filter(customer=customer)  # type: ignore
    
    if not loans.exists():  # type: ignore
        return 50  # Default score for new customers
    
    # Component 1: Past loans paid on time (40% weightage)
    total_emis = sum(loan.tenure for loan in loans)
    paid_on_time = sum(loan.emis_paid_on_time for loan in loans)
    on_time_ratio = paid_on_time / total_emis if total_emis > 0 else 0
    
    # Component 2: Number of loans taken (20% weightage)
    num_loans = loans.count()  # type: ignore
    
    # Component 3: Loan activity in current year (20% weightage)
    current_year = datetime.now().year
    current_year_loans = loans.filter(start_date__year=current_year).count()  # type: ignore
    
    # Component 4: Loan approved volume (20% weightage)
    total_loan_amount = sum(loan.loan_amount for loan in loans)
    
    # Component 5: Current debt vs approved limit
    current_debt = sum(
        loan.loan_amount for loan in loans 
        if loan.end_date > date.today()
    )
    
    if current_debt > customer.approved_limit:
        return 0
    
    # Calculate score (weighted average)
    score = 0
    score += on_time_ratio * 40  # 40% weight for payment history
    score += min(num_loans * 5, 20)  # Up to 20 points for loan history
    score += min(current_year_loans * 10, 20)  # Up to 20 points for current activity
    score += min(float(total_loan_amount) / 1000000 * 10, 20)  # Up to 20 points for volume
    
    return min(max(score, 0), 100)


def calculate_monthly_installment(loan_amount, tenure, interest_rate):
    """Calculate monthly installment using compound interest formula"""
    P = float(loan_amount)
    r = float(interest_rate) / (12 * 100)  # Monthly interest rate
    n = int(tenure)  # Number of months
    
    if r == 0:
        return P / n
    
    # EMI = P * r * (1 + r)^n / ((1 + r)^n - 1)
    emi = P * r * (1 + r) ** n / ((1 + r) ** n - 1)
    return round(emi, 2)


def get_corrected_interest_rate(credit_score, requested_rate):
    """Get corrected interest rate based on credit score"""
    if credit_score > 50:
        return requested_rate  # No correction needed
    elif 30 < credit_score <= 50:
        return max(requested_rate, 12.0)
    elif 10 < credit_score <= 30:
        return max(requested_rate, 16.0)
    else:
        return None  # Loan not approved


def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    """Check if customer is eligible for loan"""
    # Calculate credit score
    credit_score = calculate_credit_score(customer)
    
    # Check current EMIs
    current_loans = Loan.objects.filter(customer=customer, end_date__gt=date.today())  # type: ignore
    current_emis = sum(loan.monthly_repayment for loan in current_loans)
    
    # Calculate new EMI
    new_emi = calculate_monthly_installment(loan_amount, tenure, interest_rate)
    total_emis = current_emis + Decimal(str(new_emi))
    
    # Check if total EMIs exceed 50% of monthly salary
    if total_emis > customer.monthly_salary * Decimal('0.5'):
        return False, credit_score, None
    
    # Check credit score eligibility
    if credit_score > 50:
        return True, credit_score, interest_rate
    elif 30 < credit_score <= 50 and interest_rate >= 12:
        return True, credit_score, max(interest_rate, 12.0)
    elif 10 < credit_score <= 30 and interest_rate >= 16:
        return True, credit_score, max(interest_rate, 16.0)
    else:
        return False, credit_score, None


def round_to_nearest_lakh(amount):
    """Round amount to nearest lakh"""
    return round(amount / 100000) * 100000