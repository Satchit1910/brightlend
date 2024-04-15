from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Payment
from .serializers import PaymentSerializer
from loans.models import Loan
from datetime import datetime, timedelta
from loans.utils import calculate_due_dates,calculate_emi

@api_view(['POST'])
def make_payment(request):
    loan_id = request.data.get('loan_id')
    amount = float(request.data.get('amount'))
    date = datetime.strptime(request.data.get('date'), "%Y-%m-%d")

    try:
        loan = Loan.objects.get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan does not exist.'}, status=status.HTTP_404_NOT_FOUND)

    if loan.status == 'closed':
        return Response({'error': 'This loan has already been closed'}, status=status.HTTP_400_BAD_REQUEST)

    due_dates = calculate_due_dates(loan.disbursement_date,loan.term_period,loan.emi_amount)
    for due_date in due_dates:
        due_date['Date'] = datetime.strptime(due_date['Date'], "%Y-%m-%d")

    if not any(due_date['Date'] == date for due_date in due_dates):
        return Response({'error': 'Invalid due-date.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check for existing payments for this loan
    existing_payments = Payment.objects.filter(loan_id=loan_id)
    
    # Check if there are previous EMIs due
    if existing_payments:
        for due_date in due_dates:
            if due_date['Date'] < date:
                if not existing_payments.filter(date=due_date['Date'].date()).exists():
                    return Response({'error': 'Previous EMIs are due. Please pay them first.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        if date != due_dates[0]['Date']:
            return Response({'error': 'Previous EMIs are due. Please pay them first.'}, status=status.HTTP_400_BAD_REQUEST)

    
    # Check if payment entry already exists for this due date
    if existing_payments.filter(date=date).exists():
        return Response({'error': 'Payment entry already exists for this date.'}, status=status.HTTP_400_BAD_REQUEST)
    
    loan.emi_amount = float(loan.emi_amount)
    principal_paid = 0
    for existing_payment in existing_payments:
        principal_paid = principal_paid + float(existing_payment.principal_amount_paid)
    remaining_principal = float(loan.loan_amount) - principal_paid
    emi_amount_interest = remaining_principal * float(loan.interest_rate) / 12 / 100
    emi_amount_principal = loan.emi_amount - emi_amount_interest

    print(emi_amount_interest)
    print(emi_amount_principal)

    if amount != loan.emi_amount:
        if(amount > loan.emi_amount):
            term_period_left = calculate_payments_left(due_dates,date) 
            extra_amount = amount - loan.emi_amount
            if extra_amount >= remaining_principal:
                loan.status = "closed"
                loan.save()
                payment = Payment.objects.create(loan_id=loan, amount_paid=amount, date=date,emi_amount_principal=emi_amount_principal,emi_amount_interest=emi_amount_interest,interest_amount_paid=emi_amount_interest,principal_amount_paid=emi_amount_principal+remaining_principal)
                payment_serializer = PaymentSerializer(payment)
                payment.save()
                response_data = {
                    'message': "Payment has been made and this loan has been closed successfully."
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                new_remaining_principal = remaining_principal - extra_amount
                print(extra_amount)
                new_emi = calculate_emi(new_remaining_principal,term_period_left,float(loan.interest_rate))
                loan.emi_amount = new_emi
                loan.save()
                payment = Payment.objects.create(loan_id=loan, amount_paid=amount, date=date,emi_amount_principal=emi_amount_principal,emi_amount_interest=emi_amount_interest,interest_amount_paid=emi_amount_interest,principal_amount_paid=emi_amount_principal+extra_amount)
                payment_serializer = PaymentSerializer(payment)
                payment.save()
                response_data = {
                    'message': "Payment has been made and EMI amount has been updated for the rest of the term."
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            new_remaining_principal = remaining_principal-amount
            new_emi = calculate_emi(new_remaining_principal,term_period_left,float(loan.interest_rate))
            loan.emi_amount = new_emi
            loan.save()
            payment = Payment.objects.create(loan_id=loan, amount_paid=amount, date=date,emi_amount_principal=emi_amount_principal,emi_amount_interest=emi_amount_interest,interest_amount_paid=0,principal_amount_paid=amount)
            payment_serializer = PaymentSerializer(payment)
            payment.save()
            response_data = {
                'message': "Payment has been made and EMI amount has been updated for the rest of the term."
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

    # Create payment entry
    payment = Payment.objects.create(loan_id=loan, amount_paid=amount, date=date,emi_amount_principal=emi_amount_principal,emi_amount_interest=emi_amount_interest,interest_amount_paid=emi_amount_interest,principal_amount_paid=emi_amount_principal)
    payment_serializer = PaymentSerializer(payment)
    payment.save()

    return Response({'message':"Payment has been made successfully."}, status=status.HTTP_201_CREATED)

def calculate_payments_left(due_dates,new_payment_date):
    payments_left = 0

    for due_date in due_dates:
        payment_due_date = due_date['Date']

        if payment_due_date > new_payment_date:
            payments_left += 1
    
    return payments_left

@api_view(['GET'])
def get_statement(request):
    loan_id = request.query_params.get('loan_id')

    if not loan_id:
        return Response({'error': 'Loan ID is required'}, status=400)

    try:
        loan = Loan.objects.get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response({'error': 'Loan with this Loan ID does not exist'}, status=400)

    past_transactions = Payment.objects.filter(loan_id=loan_id).values('date', 'emi_amount_principal','emi_amount_interest','amount_paid')

    due_dates = calculate_due_dates(loan.disbursement_date,loan.term_period,loan.emi_amount)
    for due_date in due_dates:
        due_date['Date'] = datetime.strptime(due_date['Date'], "%Y-%m-%d").date()
    past_transaction_dates = [transaction['date'] for transaction in past_transactions]
    
    future_due_dates = [due_date for due_date in due_dates if due_date['Date'] not in past_transaction_dates]

    # Construct response JSON
    response_data = {
        'message': "Statement Fetched Successfully",
        'loan_id': loan_id,
        'past_transactions': list(past_transactions),
        'future_due_dates': future_due_dates
    }

    return Response(response_data)