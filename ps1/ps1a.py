# A program to calculate and print the credit card balance after one year if a person only pays the
# minimum monthly payment required by the credit card company each month.

balance = float(raw_input('Enter the outstanding balance on your credit card:'))
annual_interest_rate = float(raw_input('Enter the annual credit card interest rate as a decimal:'))
monthly_interest_rate = annual_interest_rate / 12.0
min_monthly_payment_rate = float(raw_input('Enter the minimum monthly payment rate as a decimal:'))

total_amount_paid = 0

for i in range(1,13):
    print("Month %i" % (i,))
    min_monthly_payment = min_monthly_payment_rate * balance
    interest_paid = monthly_interest_rate * balance
    principal_paid = min_monthly_payment - interest_paid
    balance -= principal_paid
    print("Minimum monthly payment: $%.2f" % (min_monthly_payment,))
    print("Principle paid: $%.2f" % (principal_paid,))
    print("Remaining balance: $%.2f" % (balance,))
    total_amount_paid += principal_paid + interest_paid

print 'RESULT'
print "Total amount paid: $%.2f" % (total_amount_paid,)
print "Remaining Balance: $%.2f" % (balance,)
