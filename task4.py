n = int(input("Enter a number: "))

if n % 2 == 0:
    print(n, "is even")
else:
    print(n, "is odd")

if n % 5 == 0:
    if n % 7 == 0:
        print("Divisible by both 5 and 7")
    else:
        print("Divisible by 5 only")
else:
    if n % 7 == 0:
        print("Divisible by 7 only")
    else:
        print("Not divisible by 5 and 7")
