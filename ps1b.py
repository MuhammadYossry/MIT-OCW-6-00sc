# A program that calculates the minimum fixed monthly payment needed in order pay
# off a credit card balance within 12 months

balance = float(raw_input('Enter the outstanding balance on your credit card:'))
annual_interest_rate = float(raw_input('Enter the annual credit card interest rate as a decimal:'))
monthly_interest_rate = annual_interest_rate / 12.0


monthly_payment_guess = 10.0
balance_tmp = balance

while balance_tmp > 0.0:
    balance_tmp = balance
    for month in range(1,13):
        interest_paid = monthly_interest_rate * balance_tmp
        principal_paid = monthly_payment_guess - interest_paid
        balance_tmp -= principal_paid
        if balance_tmp < 0.0:
            print 'RESULT'
            print "Monthly payment to pay off debt in 1 year: $%.2f" % (monthly_payment_guess,)
            print "Number of months needed: %i" % (month,)
            print "Balance: %.2f" % (balance_tmp,)
            break
    monthly_payment_guess += 10.0
