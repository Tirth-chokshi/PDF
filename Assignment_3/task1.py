orig_files = ["  Report.PDF", "photo.jpg ", "LOG.txt", "", "archive.zip", "  script.py",
              "Report.pdf", "notes.txt ", "   ", "photo.JPG", "invoice.csv", "log.txt"]
orig_sizes = [120, 540, 35, 10, 2048, 4, 120, 35, 0, 540, 64, 35]

files = orig_files.copy()
sizes = orig_sizes.copy()


def get_int(msg):
    val = input(msg).strip()
    try:
        return int(val)
    except ValueError:
        print("Invalid input, please enter a whole number")
        return None


def get_size(msg):
    n = get_int(msg)
    if n is None:
        return None
    if n < 0:
        print("Size cannot be negative")
        return None
    return n


def same_length():
    if len(files) != len(sizes):
        print("Error: filenames has", len(files), "items but sizes has", len(sizes))
        return False
    return True


def show_list(fl, sl):
    if len(fl) == 0:
        print("  (no records)")
    for name, size in zip(fl, sl):
        print(f"  '{name}' - {size} KB")


def normalise(fl, sl):
    names = [x.strip().lower() for x in fl]
    new_f = []
    new_s = []
    for name, size in zip(names, sl):
        if name != "":
            new_f.append(name)
            new_s.append(size)
    return new_f, new_s


def check_lengths():
    print("Filenames:", len(files), "  Sizes:", len(sizes))
    if same_length():
        print("Both lists have the same number of elements")


def basic_display():
    if not same_length():
        return
    if len(files) == 0:
        print("No records to display")
        return
    print("First record:")
    show_list(files[:1], sizes[:1])
    print("Last record:")
    show_list(files[-1:], sizes[-1:])
    print("First four records:")
    show_list(files[:4], sizes[:4])
    print("Last three records:")
    show_list(files[-3:], sizes[-3:])
    print("Alternate records:")
    show_list(files[::2], sizes[::2])
    print("Reverse order:")
    show_list(files[::-1], sizes[::-1])


def by_index():
    if len(files) == 0:
        print("No records to display")
        return
    i = get_int(f"Enter index (-{len(files)} to {len(files) - 1}): ")
    if i is None:
        return
    if i < -len(files) or i >= len(files):
        print("Index", i, "is out of range")
        return
    print(f"Record at index {i}: '{files[i]}' - {sizes[i]} KB")


def read_optional(msg):
    val = input(msg).strip()
    if val == "":
        return None, True
    try:
        return int(val), True
    except ValueError:
        print("Invalid input:", val)
        return None, False


def custom_slice():
    start, ok1 = read_optional("Start (blank for default): ")
    if not ok1:
        return
    stop, ok2 = read_optional("Stop (blank for default): ")
    if not ok2:
        return
    step, ok3 = read_optional("Step (blank for default): ")
    if not ok3:
        return
    if step == 0:
        print("Step cannot be zero")
        return
    print("Slice result:")
    show_list(files[start:stop:step], sizes[start:stop:step])


def normalise_option():
    global files, sizes
    if not same_length():
        return
    before = len(files)
    files, sizes = normalise(files, sizes)
    print("Normalised filenames and removed", before - len(files), "empty record(s)")
    show_list(files, sizes)


def add_modify():
    if not same_length():
        return
    name = input("Filename to append: ").strip().lower()
    if name == "":
        print("Filename cannot be empty")
        return
    size = get_size("Size in KB: ")
    if size is None:
        return
    files.append(name)
    sizes.append(size)
    print("After append():")
    show_list(files, sizes)

    files.extend(["memo.docx", "dump.bin"])
    sizes.extend([22, 4096])
    print("After extend() with memo.docx and dump.bin:")
    show_list(files, sizes)

    pos = min(2, len(files))
    files.insert(pos, "disk.img")
    sizes.insert(pos, 8192)
    print("After insert() of disk.img at position", pos, ":")
    show_list(files, sizes)

    old = (files[0], sizes[0])
    files[0] = "report_v2.pdf"
    sizes[0] = 125
    print("Index assignment on record 0:", old, "->", (files[0], sizes[0]))

    old_f = files[1:3]
    files[1:3] = ["mail.pst", "browser.db"]
    sizes[1:3] = [700, 90]
    print("Slice assignment [1:3]:", old_f, "->", files[1:3])
    print("Records now:")
    show_list(files, sizes)


def remove_records():
    if not same_length():
        return
    if len(files) == 0:
        print("No records to remove")
        return
    name = input("Filename to remove with remove(): ").strip().lower()
    if name in files:
        i = files.index(name)
        files.remove(name)
        size = sizes.pop(i)
        print("remove(): removed", name, "-", size, "KB")
    else:
        print("remove(): filename", name, "not found")

    if len(files) > 0:
        f = files.pop()
        s = sizes.pop()
        print("pop(): removed last record", f, "-", s, "KB")
    else:
        print("pop(): list is empty, nothing to pop")

    if len(files) == 0:
        print("del: list is empty, nothing to delete")
        return
    i = get_int(f"Index to delete with del (-{len(files)} to {len(files) - 1}): ")
    if i is None:
        return
    if i < -len(files) or i >= len(files):
        print("del: index", i, "is out of range")
        return
    f = files[i]
    s = sizes[i]
    del files[i]
    del sizes[i]
    print("del: removed", f, "-", s, "KB")
    print("Records now:")
    show_list(files, sizes)


def clear_demo():
    temp_f = files.copy()
    temp_s = sizes.copy()
    print("Temporary copy before clear():", len(temp_f), "records")
    temp_f.clear()
    temp_s.clear()
    print("Temporary copy after clear():", temp_f, temp_s)
    print("Working list still has", len(files), "records")


def search():
    name = input("Filename to search: ").strip().lower()
    if name == "":
        print("Filename cannot be empty")
        return
    if name in files:
        print(name, "is in the list")
        print("count():", files.count(name))
        print("index() of first match:", files.index(name))
        print("All positions using enumerate():")
        for i, f in enumerate(files):
            if f == name:
                print(" ", i, "-", sizes[i], "KB")
    else:
        print(name, "is not in the list")


def show_data():
    print("Working copy:")
    show_list(files, sizes)
    print("Original data (never changed):")
    show_list(orig_files, orig_sizes)


def reset():
    global files, sizes
    c = input("1. Original data  2. Empty data: ").strip()
    if c == "1":
        files = orig_files.copy()
        sizes = orig_sizes.copy()
        print("Working copy reset to original data")
    elif c == "2":
        files = []
        sizes = []
        print("Working copy is now empty")
    else:
        print("Invalid choice")


def menu():
    print()
    print("===== Task 1: Evidence List =====")
    print("1. Check list lengths")
    print("2. First/last, first 4, last 3, alternate, reverse")
    print("3. Show record at an index")
    print("4. Custom slice")
    print("5. Normalise filenames and remove empty ones")
    print("6. Add and modify records")
    print("7. Remove records")
    print("8. clear() on a temporary copy")
    print("9. Search a filename")
    print("10. Show working and original data")
    print("11. Reset working copy")
    print("0. Exit")


def main():
    while True:
        menu()
        ch = input("Enter choice: ").strip()
        if ch == "1":
            check_lengths()
        elif ch == "2":
            basic_display()
        elif ch == "3":
            by_index()
        elif ch == "4":
            custom_slice()
        elif ch == "5":
            normalise_option()
        elif ch == "6":
            add_modify()
        elif ch == "7":
            remove_records()
        elif ch == "8":
            clear_demo()
        elif ch == "9":
            search()
        elif ch == "10":
            show_data()
        elif ch == "11":
            reset()
        elif ch == "0":
            print("Bye")
            break
        else:
            print("Invalid choice, try again")


if __name__ == "__main__":
    main()
