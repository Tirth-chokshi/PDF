from task3 import device_A, device_B, device_C, devices, show_set

watchlist = {"script.py", "macro.docm", "archive.zip"}


def exclusive():
    all_files = device_A | device_B | device_C
    for f in sorted(all_files):
        on = [d for d in sorted(devices) if f in devices[d]]
        if len(on) == 1:
            print(f"  {f}: only on device {on[0]}")


def not_on_a():
    show_set("On B or C but not on A:", (device_B | device_C) - device_A)


def watch():
    show_set("Watchlist:", watchlist)
    for d in sorted(devices):
        show_set(f"  Device {d} matches:", devices[d] & watchlist)


def subset_demo():
    small = {"report.pdf", "log.txt"}
    show_set("small =", small)
    print("small.issubset(A):", small.issubset(device_A))
    print("small.issubset(C):", small.issubset(device_C))
    print("A.issuperset(small):", device_A.issuperset(small))
    print("A.isdisjoint(B):", device_A.isdisjoint(device_B))
    print("B.isdisjoint(watchlist):", device_B.isdisjoint(watchlist))
    print("small < A (proper subset):", small < device_A)
    print("A < A:", device_A < device_A, " A <= A:", device_A <= device_A)
    print("A > small (proper superset):", device_A > small)
    print("A > A:", device_A > device_A)


def inplace_demo():
    a = device_A.copy()
    r = a.update(device_B)
    show_set("update():                     ", a)
    show_set("union():                      ", device_A.union(device_B))
    print("  same:", a == device_A.union(device_B), " update() returned", r)

    a = device_A.copy()
    a.intersection_update(device_B)
    show_set("intersection_update():        ", a)
    show_set("intersection():               ", device_A.intersection(device_B))
    print("  same:", a == device_A.intersection(device_B))

    a = device_A.copy()
    a.difference_update(device_B)
    show_set("difference_update():          ", a)
    show_set("difference():                 ", device_A.difference(device_B))
    print("  same:", a == device_A.difference(device_B))

    a = device_A.copy()
    a.symmetric_difference_update(device_B)
    show_set("symmetric_difference_update():", a)
    show_set("symmetric_difference():       ", device_A.symmetric_difference(device_B))
    print("  same:", a == device_A.symmetric_difference(device_B))

    print("The _update() versions change the copy and return None,")
    print("the normal versions return a new set.")
    show_set("Original A unchanged:", device_A)


def extensions():
    names = device_A | device_B | device_C | {"README", "id_rsa"}
    exts = {f.rsplit(".", 1)[1] for f in names if "." in f}
    no_ext = {f for f in names if "." not in f}
    show_set("Distinct extensions:", exts)
    show_set("Files without extension:", no_ext)


def similarity(s1, s2):
    if len(s1) == 0 and len(s2) == 0:
        return 1.0
    if len(s1) == 0 or len(s2) == 0:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)


def similarity_option():
    print("Similarity = files in common / all files of both (Jaccard)")
    for x, y in [("A", "B"), ("A", "C"), ("B", "C")]:
        print(f"  {x} vs {y}: {round(similarity(devices[x], devices[y]), 3)}")
    choices = {"A": device_A, "B": device_B, "C": device_C, "E": set()}
    p = input("First inventory (A/B/C, or E for empty): ").strip().upper()
    q = input("Second inventory (A/B/C, or E for empty): ").strip().upper()
    if p not in choices or q not in choices:
        print("Invalid inventory, use A, B, C or E")
        return
    print(f"Similarity {p} vs {q}: {round(similarity(choices[p], choices[q]), 3)}")


def frozen_demo():
    cases = {frozenset(device_A): "Case 101 - laptop", frozenset(device_B): "Case 102 - USB drive"}
    print("Dictionary with frozenset keys:")
    for k, v in cases.items():
        print(" ", sorted(k), "->", v)
    print("Lookup with frozenset(device_A):", cases[frozenset(device_A)])
    snap = frozenset(device_A)
    try:
        snap.add("x.txt")
    except AttributeError:
        print("frozenset has no add(), it cannot be changed")


def mutable_demo():
    try:
        d = {device_A: "laptop"}
    except TypeError as e:
        print("set as a dictionary key -> TypeError:", e)
    try:
        s = {device_A, device_B}
    except TypeError as e:
        print("set inside another set -> TypeError:", e)
    ok = {frozenset(device_A), frozenset(device_B)}
    print("frozensets inside a set works:", len(ok), "items")
    print("A set can change, so its hash could change. Keys and set elements must not change, so Python blocks it.")


def menu():
    print()
    print("===== Task 4: Set Correlation =====")
    print("1. Files on exactly one device")
    print("2. Not on A but on B or C")
    print("3. Watchlist matches")
    print("4. Subset, superset, disjoint")
    print("5. _update() methods vs normal methods")
    print("6. File extensions")
    print("7. Inventory similarity")
    print("8. frozenset as dictionary key")
    print("9. Why a set cannot be a key")
    print("0. Exit")


def main():
    while True:
        menu()
        ch = input("Enter choice: ").strip()
        if ch == "1":
            exclusive()
        elif ch == "2":
            not_on_a()
        elif ch == "3":
            watch()
        elif ch == "4":
            subset_demo()
        elif ch == "5":
            inplace_demo()
        elif ch == "6":
            extensions()
        elif ch == "7":
            similarity_option()
        elif ch == "8":
            frozen_demo()
        elif ch == "9":
            mutable_demo()
        elif ch == "0":
            print("Bye")
            break
        else:
            print("Invalid choice, try again")


if __name__ == "__main__":
    main()
