from dateutil.relativedelta import relativedelta

def calculate_due_dates(disbursement_date,term_period,emi):
    due_dates = []
    current_date = disbursement_date.replace(day=1) + relativedelta(months=1)  # First EMI due on the 1st of next month
    for _ in range(term_period):
        due_dates.append({
            'Date': current_date.strftime('%Y-%m-%d'),
            'Amount_due': emi
        })
        # Move to the next month
        current_date += relativedelta(months=1)
    return due_dates

def calculate_emi(principal,remaining_term,annual_interest_rate):
    r = (annual_interest_rate / 12) / 100 
    n = remaining_term  
    emi = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return emi