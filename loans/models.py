from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(18), MaxValueValidator(100)])
    phone_number = models.CharField(max_length=15, unique=True)
    monthly_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    approved_limit = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    current_debt = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loans')
    loan_amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    tenure = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(360)]  # 1 month to 30 years
    )
    interest_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100.00'))]
    )
    monthly_repayment = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'loans'

    def __str__(self):
        return f"Loan {self.loan_id} - {getattr(self.customer, 'first_name', 'Unknown')}"

    @property
    def repayments_left(self) -> int:
        return self.tenure - self.emis_paid_on_time  # type: ignore

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.emis_paid_on_time > self.tenure:
            raise ValidationError("EMIs paid on time cannot exceed total tenure")
        if self.start_date and self.end_date and self.start_date >= self.end_date:
            raise ValidationError("End date must be after start date")