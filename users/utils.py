from .models import Transaction
import math

def calculate_credit_score(user_id):
    # Query transactions for the user
    transactions = Transaction.objects.filter(user_id=user_id)

    # Initialize net balance
    net_balance = 0

    # Calculate net balance based on transaction types
    for transaction in transactions:
        if transaction.transaction_type == 'DEBIT':
            net_balance -= transaction.amount
        elif transaction.transaction_type == 'CREDIT':
            net_balance += transaction.amount

    print(net_balance)
    if net_balance >=  1000000:
        return 900
    elif net_balance <= 100000:
        return 300
    else:
        return 300 + 10*int(math.floor(net_balance-100000)/15000)