n = int(input("Enter a positive integer: "))

temp = n
s = 0
count = 0
rev = 0

while temp > 0:
    d = temp % 10
    s = s + d
    count = count + 1
    rev = rev * 10 + d
    temp = temp // 10

print("Sum of digits =", s)
print("Number of digits =", count)
print("Reverse of number =", rev)
