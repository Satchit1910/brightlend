from django.db import models
import uuid
from users.models import User


class Loan(models.Model):
    loan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=1) 
    loan_type = models.CharField(max_length=20)
    loan_amount = models.IntegerField()
    term_period = models.IntegerField()  # Number of months
    disbursement_date = models.DateField()
    emi_amount = models.DecimalField(max_digits=10, decimal_places=2) 
    status = models.CharField(default='open', max_length=20)
