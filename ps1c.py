# A program that calculates the minimum fixed monthly payment needed in order pay
# off a credit card balance within 12 months using bisection search

def calculate_balance_after_year(balance, monthly_interest_rate, monthly_payment):
    """Calculate the balance of a credit card in case of fixe montly payment, returns
        final balance and how many months needed.""" 
    for month in range(1,13):
        interest_paid = monthly_interest_rate * balance
        principal_paid = monthly_payment - interest_paid
        balance -= principal_paid
        if balance < 0.0:
            return (balance, month)
    return (balance, 12)

balance = float(raw_input('Enter the outstanding balance on your credit card:'))
annual_interest_rate = float(raw_input('Enter the annual credit card interest rate as a decimal:'))
monthly_interest_rate = annual_interest_rate / 12.0

low = balance / 12.0
high = (balance * (1 + monthly_interest_rate) ** 12.0) / 12.0 


monthly_payment_guess = (high + low) / 2

balance_at_last, month = calculate_balance_after_year(balance, monthly_interest_rate, monthly_payment_guess)


while not (balance_at_last < 0.0 and balance_at_last > -0.15):
    if balance_at_last < -0.15:
        high = monthly_payment_guess
    else:
        low = monthly_payment_guess
    monthly_payment_guess = (high + low) / 2
    balance_at_last, month = calculate_balance_after_year(balance, monthly_interest_rate, monthly_payment_guess)

print 'RESULT'
print "Monthly payment to pay off debt in 1 year: $%.2f" % (monthly_payment_guess,)
print "Number of months needed: %i" % (month,)
print "Balance: %.2f" % (balance_at_last,)
