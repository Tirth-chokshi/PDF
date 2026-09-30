a = float(input("Enter first number: "))
b = float(input("Enter second number: "))

print("Sum =", a + b)
print("Difference =", a - b)
print("Product =", a * b)

if b == 0:
    print("Division not possible, second number is zero")
else:
    print("Quotient =", a / b)
    print("Remainder =", a % b)
