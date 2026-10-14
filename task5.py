a = float(input("Enter first number: "))
b = float(input("Enter second number: "))
c = float(input("Enter third number: "))

if a == b and b == c:
    print("All three numbers are equal")
elif a >= b and a >= c:
    print("Largest number is", a)
elif b >= a and b >= c:
    print("Largest number is", b)
else:
    print("Largest number is", c)
