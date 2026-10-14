device_A = {"report.pdf", "photo.jpg", "log.txt", "archive.zip", "script.py"}
device_B = {"report.pdf", "log.txt", "notes.txt", "backup.zip"}
device_C = {"photo.jpg", "report.pdf", "notes.txt", "invoice.csv"}

devices = {"A": device_A, "B": device_B, "C": device_C}


def show_set(label, s):
    if len(s) == 0:
        print(label, "(empty)")
    else:
        print(label, sorted(s))


def from_list():
    recovered = ["report.pdf", "log.txt", "report.pdf", "photo.jpg", "log.txt", "report.pdf"]
    s = set(recovered)
    print("List:", recovered, "-", len(recovered), "items")
    print("Set: ", sorted(s), "-", len(s), "items")
    print("Duplicates removed:", len(recovered) - len(s))


def empty_set():
    a = {}
    b = set()
    print("type({}) ->", type(a))
    print("type(set()) ->", type(b))
    print("{} is an empty dictionary, so an empty set has to be made with set()")


def membership():
    name = input("Filename to look for: ").strip().lower()
    if name == "":
        print("Filename cannot be empty")
        return
    for d in sorted(devices):
        if name in devices[d]:
            print(f"  {name} is on device {d}")
        else:
            print(f"  {name} is not on device {d}")
    print("Files on device A (sorted):")
    for f in sorted(device_A):
        print("  ", f)


def set_methods():
    s = device_A.copy()
    show_set("copy() of A:          ", s)
    s.add("new.txt")
    show_set("add('new.txt'):       ", s)
    s.update(["a.log", "b.log"])
    show_set("update(a.log, b.log): ", s)
    s.remove("a.log")
    show_set("remove('a.log'):      ", s)
    s.discard("b.log")
    show_set("discard('b.log'):     ", s)
    x = s.pop()
    print("pop() removed:", x, "(could be any element)")
    show_set("after pop():          ", s)
    s.clear()
    show_set("after clear():        ", s)
    show_set("Original A unchanged: ", device_A)


def absent_demo():
    name = input("Filename to remove from a copy of B: ").strip().lower()
    s1 = device_B.copy()
    s2 = device_B.copy()
    try:
        s1.remove(name)
        print("remove(): removed", name)
    except KeyError:
        print("remove(): KeyError, '" + name + "' is not in the set")
    before = len(s2)
    s2.discard(name)
    if len(s2) < before:
        print("discard(): removed", name)
    else:
        print("discard(): not found, nothing happened and no error")


def pop_empty():
    s = device_C.copy()
    print("Popping everything from a copy of C:")
    while True:
        try:
            x = s.pop()
            print("  popped:", x)
        except KeyError:
            print("  set is empty, pop() raised KeyError - handled and stopped")
            break
    print("The order above is not fixed, a set can return any element")


def compare():
    show_set("All files (A | B | C):     ", device_A | device_B | device_C)
    show_set("On all three (A & B & C):  ", device_A & device_B & device_C)
    show_set("In A not in B (A - B):     ", device_A - device_B)
    show_set("In B not in A (B - A):     ", device_B - device_A)
    show_set("In A or B, not both (A ^ B):", device_A ^ device_B)


def ops_vs_methods():
    tests = [
        ("Union", device_A | device_B, device_A.union(device_B)),
        ("Intersection", device_A & device_B, device_A.intersection(device_B)),
        ("Difference", device_A - device_B, device_A.difference(device_B)),
        ("Symmetric difference", device_A ^ device_B, device_A.symmetric_difference(device_B)),
    ]
    for name, op, m in tests:
        print(name + ":")
        print("  operator:", sorted(op))
        print("  method:  ", sorted(m))
        print("  same:", op == m)
    print("Methods accept any iterable, operators need sets on both sides:")
    print("  A.union(['x.txt']) ->", sorted(device_A.union(["x.txt"])))
    try:
        device_A | ["x.txt"]
    except TypeError as e:
        print("  A | ['x.txt'] -> TypeError:", e)


def exactly_two():
    all_files = device_A | device_B | device_C
    found = False
    for f in sorted(all_files):
        on = [d for d in sorted(devices) if f in devices[d]]
        if len(on) == 2:
            print(f"  {f}: devices {on[0]} and {on[1]}")
            found = True
    if not found:
        print("  none")


def menu():
    print()
    print("===== Task 3: Device Sets =====")
    print("1. Remove duplicates using a set")
    print("2. Empty set vs {}")
    print("3. Membership and iteration")
    print("4. Set methods")
    print("5. remove() vs discard() for a missing file")
    print("6. pop() until empty")
    print("7. Compare devices")
    print("8. Operators vs methods")
    print("9. Files on exactly two devices")
    print("0. Exit")


def main():
    while True:
        menu()
        ch = input("Enter choice: ").strip()
        if ch == "1":
            from_list()
        elif ch == "2":
            empty_set()
        elif ch == "3":
            membership()
        elif ch == "4":
            set_methods()
        elif ch == "5":
            absent_demo()
        elif ch == "6":
            pop_empty()
        elif ch == "7":
            compare()
        elif ch == "8":
            ops_vs_methods()
        elif ch == "9":
            exactly_two()
        elif ch == "0":
            print("Bye")
            break
        else:
            print("Invalid choice, try again")


if __name__ == "__main__":
    main()
