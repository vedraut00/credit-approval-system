from rest_framework import serializers
from .models import Customer, Loan
from decimal import Decimal


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id', 'first_name', 'last_name', 'age', 'phone_number', 
                 'monthly_salary', 'approved_limit']


class CustomerRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(min_value=18, max_value=100)
    monthly_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    phone_number = serializers.CharField(max_length=15)
    
    def validate_phone_number(self, value):
        if Customer.objects.filter(phone_number=value).exists():  # type: ignore
            raise serializers.ValidationError("Phone number already exists.")
        return value


class LoanEligibilitySerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()


class LoanCreationSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    loan_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    tenure = serializers.IntegerField()


class LoanDetailSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    
    class Meta:
        model = Loan
        fields = ['loan_id', 'customer', 'loan_amount', 'interest_rate', 
                 'monthly_repayment', 'tenure']


class CustomerLoanSerializer(serializers.ModelSerializer):
    repayments_left = serializers.SerializerMethodField()
    
    class Meta:
        model = Loan
        fields = ['loan_id', 'loan_amount', 'interest_rate', 
                 'monthly_repayment', 'repayments_left']
    
    def get_repayments_left(self, obj):
        return obj.repayments_left