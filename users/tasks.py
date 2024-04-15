from celery import shared_task
from .models import User
from .utils import calculate_credit_score

@shared_task
def calculate_and_save_credit_score(user_id):
    # Perform credit score calculation logic
    credit_score = calculate_credit_score(user_id)

    # Retrieve the user from the database
    user = User.objects.get(user_id=user_id)

    # Save the credit score to the user's record
    user.credit_score = credit_score
    user.save()