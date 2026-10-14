import copy
from task5 import evidence, show_record, show_all

register = copy.deepcopy(evidence)
register["E004"] = {"filename": "log.txt", "device": "B", "size_kb": 35, "status": "reviewed", "tags": ["log"]}
register["E005"] = {"filename": "photo.jpg", "device": "C", "size_kb": 540, "status": "pending", "tags": ["image", "duplicate-name"]}

second = {
    "E006": {"filename": "usb_dump.bin", "device": "C", "size_kb": 4096, "status": "pending", "tags": ["binary"]},
    "E007": {"filename": "chat.db", "device": "B", "size_kb": 256, "status": "pending", "tags": ["database"]},
    "E002": {"filename": "photo.jpg", "device": "A", "size_kb": 560, "status": "pending", "tags": ["image", "edited"]},
}


def filename_freq():
    freq = {}
    for rec in register.values():
        freq[rec["filename"]] = freq.get(rec["filename"], 0) + 1
    for name in sorted(freq):
        print(f"  {name}: {freq[name]}")


def device_ids():
    by_dev = {}
    for eid, rec in register.items():
        by_dev.setdefault(rec["device"], []).append(eid)
    for d in sorted(by_dev):
        print(f"  Device {d}: {by_dev[d]}")


def summary():
    count_dev = {}
    size_dev = {}
    count_status = {}
    for rec in register.values():
        d = rec["device"]
        count_dev[d] = count_dev.get(d, 0) + 1
        size_dev[d] = size_dev.get(d, 0) + rec["size_kb"]
        count_status[rec["status"]] = count_status.get(rec["status"], 0) + 1
    print("Records per device:")
    for d in sorted(count_dev):
        print(f"  {d}: {count_dev[d]}")
    print("Total size per device:")
    for d in sorted(size_dev):
        print(f"  {d}: {size_dev[d]} KB")
    print("Records per status:")
    for s in sorted(count_status):
        print(f"  {s}: {count_status[s]}")


def comprehensions():
    pending = {eid: r for eid, r in register.items() if r["status"] == "pending"}
    print("Pending records only:")
    show_all(pending)
    sizes = {eid: r["size_kb"] for eid, r in register.items()}
    print("ID -> size:", sizes)
    print("Sorted by size (largest first), ID as tie-breaker:")
    for eid in sorted(sizes, key=lambda e: (-sizes[e], e)):
        print(f"  {eid}: {sizes[eid]} KB")


def merge():
    print("Second register:")
    show_all(second)
    merged = copy.deepcopy(register)
    conflicts = []
    for eid, rec in second.items():
        if eid not in merged:
            merged[eid] = copy.deepcopy(rec)
            print("Added", eid)
        elif merged[eid] == rec:
            print(eid, "is the same in both, nothing to do")
        else:
            conflicts.append({"id": eid, "existing": merged[eid], "incoming": rec})
            print("Conflict on", eid, "- kept the existing version")
    print("Merged register:")
    show_all(merged)
    print("Conflict list:")
    if len(conflicts) == 0:
        print("  none")
    for c in conflicts:
        print("  ID", c["id"])
        print("    existing:", c["existing"])
        print("    incoming:", c["incoming"])


def overwrite_demo():
    a = copy.deepcopy(register)
    a.update(second)
    print("register.update(second): E002 size is", a["E002"]["size_kb"], "- second overwrote it")
    b = {**register, **second}
    print("{**register, **second}: E002 size is", b["E002"]["size_kb"], "- the right side wins")
    c = {**second, **register}
    print("{**second, **register}: E002 size is", c["E002"]["size_kb"], "- register is on the right so it wins")
    print("Working register E002 size is still", register["E002"]["size_kb"])


def file_devices():
    m = {}
    for rec in register.values():
        devs = m.setdefault(rec["filename"], [])
        if rec["device"] not in devs:
            devs.append(rec["device"])
    for f in sorted(m):
        print(f"  {f}: {m[f]}")


def copy_demo():
    base = copy.deepcopy(register)
    shallow = base.copy()
    deep = copy.deepcopy(base)
    shallow["E001"]["tags"].append("checked")
    print("Added 'checked' to E001 tags in the shallow copy")
    print("  base E001 tags:   ", base["E001"]["tags"])
    print("  shallow E001 tags:", shallow["E001"]["tags"])
    print("  deep E001 tags:   ", deep["E001"]["tags"])
    print("The shallow copy shares the inner dicts and lists with base, the deep copy does not")


def fromkeys_demo():
    ids = list(register.keys())
    counters = dict.fromkeys(ids, 0)
    counters["E001"] += 1
    print("dict.fromkeys(ids, 0), then counters['E001'] += 1:")
    print(" ", counters)
    shared = dict.fromkeys(ids, [])
    shared["E001"].append("viewed")
    print("dict.fromkeys(ids, []), then shared['E001'].append('viewed'):")
    print(" ", shared)
    print("Every key changed because all of them point to the same list")
    print("shared['E001'] is shared['E002']:", shared["E001"] is shared["E002"])
    fixed = {eid: [] for eid in ids}
    fixed["E001"].append("viewed")
    print("Fix with {eid: [] for eid in ids}:")
    print(" ", fixed)


def menu():
    print()
    print("===== Task 6: Aggregation and Merging =====")
    print("1. Filename frequency with get()")
    print("2. Device -> evidence IDs with setdefault()")
    print("3. Counts and totals")
    print("4. Dictionary comprehensions and sorting")
    print("5. Merge a second register")
    print("6. Overwriting with update() and **")
    print("7. Filename -> devices")
    print("8. Shallow copy vs deepcopy()")
    print("9. dict.fromkeys() counters and shared list problem")
    print("10. Show register")
    print("0. Exit")


def main():
    while True:
        menu()
        ch = input("Enter choice: ").strip()
        if ch == "1":
            filename_freq()
        elif ch == "2":
            device_ids()
        elif ch == "3":
            summary()
        elif ch == "4":
            comprehensions()
        elif ch == "5":
            merge()
        elif ch == "6":
            overwrite_demo()
        elif ch == "7":
            file_devices()
        elif ch == "8":
            copy_demo()
        elif ch == "9":
            fromkeys_demo()
        elif ch == "10":
            show_all(register)
        elif ch == "0":
            print("Bye")
            break
        else:
            print("Invalid choice, try again")


if __name__ == "__main__":
    main()
