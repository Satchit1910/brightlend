from django.db import models

class User(models.Model):
    user_id = models.CharField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    annual_income = models.CharField(max_length=20)
    credit_score = models.IntegerField()

    def __str__(self):
        return str(self.user_id)

class Transaction(models.Model):
    user_id = models.CharField()  # Assuming user_id is a UUIDField
    date = models.DateField()
    transaction_type = models.CharField(max_length=20)
    amount = models.IntegerField()
    
    class Meta:
        db_table = 'transactions'
        managed = False  # Inform Django that the table is managed externally

