l = float(input("Enter length of rectangle: "))
w = float(input("Enter width of rectangle: "))

area = l * w
peri = 2 * (l + w)

print("Area =", area)
print("Perimeter =", peri)

if l == w:
    print("It is a square")
else:
    print("It is not a square")
