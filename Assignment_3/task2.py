from task1 import orig_files, orig_sizes, normalise

names, sizes = normalise(orig_files, orig_sizes)
records = [[i, names[i], sizes[i]] for i in range(len(names))]


def get_int(msg):
    val = input(msg).strip()
    try:
        return int(val)
    except ValueError:
        print("Invalid input, please enter a whole number")
        return None


def show_records(recs):
    if len(recs) == 0:
        print("  (no records)")
    for r in recs:
        print(" ", r)


def unique_names():
    uniq = []
    for r in records:
        if r[1] not in uniq:
            uniq.append(r[1])
    return uniq


def nested():
    print("Records as [source_index, filename, size_kb]:")
    show_records(records)


def unique_option():
    print("Unique filenames in first-seen order:")
    print(" ", unique_names())


def frequency():
    all_names = [r[1] for r in records]
    for name in unique_names():
        print(f"  {name}: {all_names.count(name)}")


def sort_demo():
    nums = [r[2] for r in records]
    print("Sizes:", nums)
    a = nums.copy()
    result = a.sort()
    print("sort() changes the list itself and returns", result)
    print("  ", a)
    b = sorted(nums)
    print("sorted() returns a new sorted list:")
    print("  ", b)
    print("   original is still", nums)
    c = nums.copy()
    c.reverse()
    print("reverse() flips the list in place, it does not sort:")
    print("  ", c)
    print("[::-1] gives a new reversed list, original not changed:")
    print("  ", nums[::-1])


def sort_records():
    print("By filename ascending:")
    show_records(sorted(records, key=lambda r: r[1]))
    print("By size descending:")
    show_records(sorted(records, key=lambda r: r[2], reverse=True))
    print("By size descending, then filename, then index:")
    show_records(sorted(records, key=lambda r: (-r[2], r[1], r[0])))


def threshold():
    val = input("Enter size threshold in KB: ").strip()
    try:
        t = float(val)
    except ValueError:
        print("Invalid threshold:", val)
        return
    if t < 0:
        print("Threshold cannot be negative")
        return
    big = [r for r in records if r[2] > t]
    print(len(big), "record(s) larger than", t, "KB:")
    show_records(big)


def stats():
    if len(records) == 0:
        print("No records")
        return
    s = [r[2] for r in records]
    print("Number of records:", len(s))
    print("Total size:", sum(s), "KB")
    print("Average size:", round(sum(s) / len(s), 2), "KB")
    print("Minimum size:", min(s), "KB")
    print("Maximum size:", max(s), "KB")


def concat_demo():
    batch1 = records[:3]
    batch2 = [[100, "usb_dump.bin", 4096], [101, "chat.db", 256]]
    print("Batch 1:")
    show_records(batch1)
    print("Batch 2:")
    show_records(batch2)
    print("Batch 1 + Batch 2:")
    show_records(batch1 + batch2)
    print("List repetition ['-'] * 5:", ["-"] * 5)


def batches():
    n = get_int("Batch size n: ")
    if n is None:
        return
    if n <= 0:
        print("Batch size must be greater than 0")
        return
    parts = [records[i:i + n] for i in range(0, len(records), n)]
    for num, b in enumerate(parts, 1):
        print(f"Batch {num} ({len(b)} records):")
        show_records(b)


def rotate():
    k = get_int("Rotate right by k (negative = left): ")
    if k is None:
        return
    if len(records) == 0:
        print("Nothing to rotate")
        return
    k2 = k % len(records)
    rotated = records[-k2:] + records[:-k2]
    print("Before:", [r[1] for r in records])
    print("After: ", [r[1] for r in rotated])


def copy_demo():
    orig = [r.copy() for r in records[:3]]
    alias = orig
    shallow = orig.copy()
    deep = [r.copy() for r in orig]
    orig[0][2] = 999
    print("Changed orig[0][2] (size of first record) to 999")
    print("orig:              ", orig)
    print("alias = orig:      ", alias)
    print("shallow = copy():  ", shallow)
    print("deep (rows copied):", deep)
    print("alias is orig:", alias is orig)
    print("shallow is orig:", shallow is orig, " shallow[0] is orig[0]:", shallow[0] is orig[0])
    print("deep[0] is orig[0]:", deep[0] is orig[0])
    print("Alias and copy() both show 999 because they share the inner lists. Only the deep copy is independent.")


def matrix_demo():
    matrix = [[0] * 3] * 2
    matrix[0][0] = 1
    print("matrix = [[0] * 3] * 2, then matrix[0][0] = 1")
    print("  ", matrix)
    print("Both rows changed because * 2 repeats a reference to the same inner list")
    print("matrix[0] is matrix[1]:", matrix[0] is matrix[1])
    fixed = [[0] * 3 for _ in range(2)]
    fixed[0][0] = 1
    print("Fix: [[0] * 3 for _ in range(2)], then fixed[0][0] = 1")
    print("  ", fixed)
    print("fixed[0] is fixed[1]:", fixed[0] is fixed[1])


def menu():
    print()
    print("===== Task 2: List Analysis =====")
    print("1. Show nested records")
    print("2. Unique filenames (no set/dict)")
    print("3. Filename frequency")
    print("4. sort() vs sorted() vs reverse() vs [::-1]")
    print("5. Sort records")
    print("6. Records above a size threshold")
    print("7. Statistics")
    print("8. Concatenation and repetition")
    print("9. Split into batches")
    print("10. Rotate list")
    print("11. Aliasing vs copy() vs independent copy")
    print("12. Shared row problem")
    print("0. Exit")


def main():
    while True:
        menu()
        ch = input("Enter choice: ").strip()
        if ch == "1":
            nested()
        elif ch == "2":
            unique_option()
        elif ch == "3":
            frequency()
        elif ch == "4":
            sort_demo()
        elif ch == "5":
            sort_records()
        elif ch == "6":
            threshold()
        elif ch == "7":
            stats()
        elif ch == "8":
            concat_demo()
        elif ch == "9":
            batches()
        elif ch == "10":
            rotate()
        elif ch == "11":
            copy_demo()
        elif ch == "12":
            matrix_demo()
        elif ch == "0":
            print("Bye")
            break
        else:
            print("Invalid choice, try again")


if __name__ == "__main__":
    main()
