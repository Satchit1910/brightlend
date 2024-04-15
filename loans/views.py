from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Loan
from .serializers import LoanSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from .utils import calculate_due_dates

@api_view(['POST'])
def apply_loan(request):
    user_id = request.data.get('user_id')
    loan_type = request.data.get('loan_type').lower()
    loan_amount = int(request.data.get('loan_amount'))
    interest_rate = float(request.data.get('interest_rate'))
    term_period = int(request.data.get('term_period'))
    disbursement_date = datetime.strptime(request.data.get('disbursement_date'), "%Y-%m-%d")

    # Validate interest rate
    if interest_rate < 14:
        return Response({'error': 'Interest rate should be greater than or equal to 14%'}, status=400)

    # Retrieve user information
    try:
        user = User.objects.get(user_id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    # Check credit score and annual income
    if user.credit_score < 450:
        return Response({'error': 'Credit score is too low'}, status=400)
    
    user.annual_income = int(user.annual_income)
    
    if user.annual_income < 150000:
        return Response({'error': 'Annual income is too low'}, status=400)

    # Validate loan type and amount
    loan_amount_bounds = {
        'car': 750000,
        'home': 8500000,
        'education': 5000000,
        'personal': 1000000
    }
    if loan_type not in loan_amount_bounds:
        return Response({'error': 'Invalid loan type'}, status=400)
    if loan_amount > loan_amount_bounds[loan_type]:
        return Response({'error': f'Loan amount exceeds maximum for {loan_type} loan'}, status=400)

    # Calculate EMI
    rate = interest_rate / 100 / 12  # Monthly interest rate
    emi = loan_amount * rate * (1 + rate)**term_period / (((1 + rate)**term_period) - 1)

    # Calculate total interest amount
    total_interest_amount = emi * term_period - loan_amount

    # Check EMI affordability
    user_monthly_income = user.annual_income / 12
    if emi > user_monthly_income * 0.6:
        return Response({'error': 'Tenure is too short and EMI is too high'}, status=400)
    emi = round(emi,2)

    loan = Loan(
        user_id=user,
        loan_type=loan_type,
        loan_amount=loan_amount,
        interest_rate=interest_rate,
        term_period=term_period,
        disbursement_date=disbursement_date,
        emi_amount=emi,
    )

    # Save the loan instance to the database
    loan.save()

    # Serialize the saved loan object for response
    serializer = LoanSerializer(loan)

    due_dates = calculate_due_dates(disbursement_date,term_period,emi)

    # Construct the response data including the loan_id and due_dates
    response_data = {
        'loan_id': loan.loan_id,
        'message': 'Loan application approved.',
        'Due_dates': due_dates
    }

    return Response(response_data, status=status.HTTP_201_CREATED)
