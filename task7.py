units = float(input("Enter number of units consumed: "))

if units <= 100:
    bill = units * 2
elif units <= 200:
    bill = 200 + (units - 100) * 3
elif units <= 300:
    bill = 200 + 300 + (units - 200) * 5
else:
    bill = 200 + 300 + 500 + (units - 300) * 7

bill = bill + 100

print("Total bill = Rs.", bill)
