import copy

evidence = {
    "E001": {
        "filename": "report.pdf",
        "device": "A",
        "size_kb": 120,
        "status": "pending",
        "tags": ["document"]
    },
    "E002": {
        "filename": "photo.jpg",
        "device": "A",
        "size_kb": 540,
        "status": "reviewed",
        "tags": ["image"]
    },
    "E003": {
        "filename": "report.pdf",
        "device": "B",
        "size_kb": 120,
        "status": "pending",
        "tags": ["document", "duplicate-name"]
    }
}

register = copy.deepcopy(evidence)


def show_record(eid, rec):
    print(f"  {eid}: {rec['filename']} | device {rec['device']} | {rec['size_kb']} KB | {rec['status']} | tags {rec['tags']}")


def show_all(reg):
    if len(reg) == 0:
        print("  (register is empty)")
    for eid, rec in reg.items():
        show_record(eid, rec)


def print_changes(old, new):
    changed = False
    for field in new:
        if old.get(field) != new[field]:
            print(f"  {field}: {old.get(field)} -> {new[field]}")
            changed = True
    if not changed:
        print("  nothing changed")


def get_size(val):
    try:
        n = int(val)
    except ValueError:
        print("Size must be a whole number")
        return None
    if n < 0:
        print("Size cannot be negative")
        return None
    return n


def build_with_zip(ids, recs):
    if len(ids) != len(recs):
        print("  Cannot build: there are", len(ids), "IDs but", len(recs), "records")
        return None
    if len(ids) != len(set(ids)):
        dups = sorted({i for i in ids if ids.count(i) > 1})
        print("  Cannot build: duplicate IDs", dups)
        return None
    return dict(zip(ids, recs))


def zip_demo():
    ids = ["E101", "E102"]
    recs = [
        {"filename": "chat.db", "device": "C", "size_kb": 256, "status": "pending", "tags": ["database"]},
        {"filename": "mail.pst", "device": "B", "size_kb": 700, "status": "reviewed", "tags": ["email"]},
    ]
    print("Test 1 - valid lists:")
    reg2 = build_with_zip(ids, recs)
    if reg2 is not None:
        show_all(reg2)
    print("Test 2 - one extra ID:")
    build_with_zip(ids + ["E103"], recs)
    print("Test 3 - repeated ID:")
    build_with_zip(["E101", "E101"], recs)


def access():
    eid = input("Enter evidence ID: ").strip().upper()
    try:
        rec = register[eid]
        print("register[" + eid + "]:")
        show_record(eid, rec)
    except KeyError:
        print("register[" + eid + "]: KeyError, this ID does not exist")
    rec = register.get(eid)
    if rec is None:
        print("register.get('" + eid + "'): returned None, no error")
    else:
        print("register.get('" + eid + "')['filename']:", rec.get("filename"))
        print("Missing nested key with get('notes', 'no notes'):", rec.get("notes", "no notes"))


def read_record():
    filename = input("Filename: ").strip().lower()
    device = input("Device: ").strip().upper()
    size = input("Size in KB: ").strip()
    status = input("Status: ").strip().lower()
    tags = input("Tags (comma separated): ")
    if filename == "" or device == "" or status == "":
        print("Filename, device and status cannot be empty")
        return None
    size = get_size(size)
    if size is None:
        return None
    tag_list = [t.strip() for t in tags.split(",") if t.strip() != ""]
    return {"filename": filename, "device": device, "size_kb": size, "status": status, "tags": tag_list}


def insert():
    eid = input("New evidence ID: ").strip().upper()
    if eid == "":
        print("ID cannot be empty")
        return
    if eid in register:
        print("ID", eid, "already exists:")
        show_record(eid, register[eid])
        ans = input("Type U to update it, anything else to cancel: ").strip().upper()
        if ans != "U":
            print("Insert rejected, existing record kept")
            return
    rec = read_record()
    if rec is None:
        return
    if eid in register:
        print("Changes:")
        print_changes(register[eid], rec)
    register[eid] = rec
    print("Saved:")
    show_record(eid, rec)


def update_record():
    eid = input("Evidence ID to update: ").strip().upper()
    if eid not in register:
        print("ID", eid, "not found")
        return
    rec = register[eid]
    show_record(eid, rec)
    c = input("1. Change one field  2. Change status and size with update(): ").strip()
    if c == "1":
        field = input("Field (filename/device/size_kb/status/tags): ").strip().lower()
        if field not in rec:
            print("Unknown field", field)
            return
        val = input("New value: ").strip()
        if field == "size_kb":
            val = get_size(val)
            if val is None:
                return
        elif field == "tags":
            val = [t.strip() for t in val.split(",") if t.strip() != ""]
        old = rec[field]
        rec[field] = val
        print(f"  {field}: {old} -> {val}")
    elif c == "2":
        status = input("New status: ").strip().lower()
        size = get_size(input("New size in KB: ").strip())
        if size is None or status == "":
            print("Update cancelled")
            return
        old = rec.copy()
        rec.update({"status": status, "size_kb": size})
        print_changes(old, rec)
    else:
        print("Invalid choice")


def iterate():
    print("keys():", list(register.keys()))
    print("values() - filenames:", [r["filename"] for r in register.values()])
    print("items():")
    for eid, rec in register.items():
        show_record(eid, rec)


def search():
    c = input("Search by 1. ID  2. Filename  3. Device  4. Status: ").strip()
    if c not in ["1", "2", "3", "4"]:
        print("Invalid choice")
        return
    val = input("Search value: ").strip().lower()
    if val == "":
        print("Search value cannot be empty")
        return
    if c == "1":
        if val.upper() in register:
            show_record(val.upper(), register[val.upper()])
        else:
            print("No evidence with ID", val.upper())
        return
    field = {"2": "filename", "3": "device", "4": "status"}[c]
    matches = {eid: r for eid, r in register.items() if r[field].strip().lower() == val}
    if len(matches) == 0:
        print("No records found with", field, "=", val)
        return
    print(len(matches), "match(es):")
    show_all(matches)


def delete():
    if len(register) == 0:
        print("Register is empty")
        return
    eid = input("ID to delete with del: ").strip().upper()
    if eid in register:
        show_record(eid, register[eid])
        del register[eid]
        print("Deleted with del")
    else:
        print("del: ID", eid, "not found")
    eid = input("ID to delete with pop(): ").strip().upper()
    rec = register.pop(eid, None)
    if rec is None:
        print("pop(): ID", eid, "not found")
    else:
        print("pop() returned:")
        show_record(eid, rec)


def popitem_clear():
    temp = register.copy()
    try:
        eid, rec = temp.popitem()
        print("popitem() on a copy removed:", eid)
    except KeyError:
        print("popitem() on an empty register raised KeyError")
    print("Dicts keep insertion order (Python 3.7+), so popitem() removes the last added pair")
    temp2 = register.copy()
    temp2.clear()
    print("clear() on another copy:", temp2)
    print("Working register still has", len(register), "records")


def show_both():
    print("Working register:")
    show_all(register)
    print("Original register (never changed):")
    show_all(evidence)


def menu():
    print()
    print("===== Task 5: Evidence Register =====")
    print("1. Build a register with zip()")
    print("2. Access a record")
    print("3. Insert a record")
    print("4. Update a record")
    print("5. keys(), values(), items()")
    print("6. Search")
    print("7. Delete with del and pop()")
    print("8. popitem() and clear() on copies")
    print("9. Show working and original register")
    print("0. Exit")


def main():
    while True:
        menu()
        ch = input("Enter choice: ").strip()
        if ch == "1":
            zip_demo()
        elif ch == "2":
            access()
        elif ch == "3":
            insert()
        elif ch == "4":
            update_record()
        elif ch == "5":
            iterate()
        elif ch == "6":
            search()
        elif ch == "7":
            delete()
        elif ch == "8":
            popitem_clear()
        elif ch == "9":
            show_both()
        elif ch == "0":
            print("Bye")
            break
        else:
            print("Invalid choice, try again")


if __name__ == "__main__":
    main()
