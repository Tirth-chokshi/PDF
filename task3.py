c = float(input("Enter temperature in celsius: "))

f = (c * 9 / 5) + 32
print("Temperature in fahrenheit =", f)

if c < 0:
    print("Below freezing")
elif c <= 35:
    print("Normal")
else:
    print("Hot")
