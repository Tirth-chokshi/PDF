m1 = float(input("Enter marks of subject 1: "))
m2 = float(input("Enter marks of subject 2: "))
m3 = float(input("Enter marks of subject 3: "))
m4 = float(input("Enter marks of subject 4: "))
m5 = float(input("Enter marks of subject 5: "))

if m1 < 0 or m1 > 100 or m2 < 0 or m2 > 100 or m3 < 0 or m3 > 100 or m4 < 0 or m4 > 100 or m5 < 0 or m5 > 100:
    print("Invalid marks, marks should be between 0 and 100")
else:
    total = m1 + m2 + m3 + m4 + m5
    per = total / 5

    if per >= 90:
        grade = "A+"
    elif per >= 80:
        grade = "A"
    elif per >= 70:
        grade = "B"
    elif per >= 60:
        grade = "C"
    elif per >= 50:
        grade = "D"
    else:
        grade = "Fail"

    print("Total marks =", total)
    print("Percentage =", per)
    print("Grade =", grade)
