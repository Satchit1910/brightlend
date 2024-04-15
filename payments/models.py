from django.db import models
import uuid
from loans.models import Loan 

class Payment(models.Model):
    payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2) 
    date = models.DateField()
    emi_amount_principal = models.DecimalField(max_digits=10, decimal_places=2) 
    emi_amount_interest = models.DecimalField(max_digits=10, decimal_places=2) 
    interest_amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    principal_amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
