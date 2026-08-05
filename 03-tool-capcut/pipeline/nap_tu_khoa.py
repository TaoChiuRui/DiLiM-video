# -*- coding: utf-8 -*-
"""Nap tu khoa anh Thanh sua tren so_kho.html NGUOC lai vao clips.py TAGS.

    python3 nap_tu_khoa.py --file ~/Downloads/tu_khoa.json          # thu
    python3 nap_tu_khoa.py --file ~/Downloads/tu_khoa.json --apply

File JSON tu nut «TAI JSON VE»:  {"DD_ONGCU1": ["đau đầu", "người già"], ...}

Chi sua DONG TAGS trong clips.py, khong dung gi khac. Hang so nao khong co
trong clips.py thi bao loi va bo qua — khong tu them.
"""
import argparse
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.join(HERE, "clips.py")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    moi = json.load(open(os.path.expanduser(a.file), encoding="utf-8"))
    txt = open(CLIPS, encoding="utf-8").read()

    sys.path.insert(0, HERE)
    import clips as C
    hien = {k: C.TAGS.get(v, [])
            for k, v in vars(C).items()
            if k.isupper() and isinstance(v, str) and v.startswith("/Volumes")}

    them, doi, thieu = [], [], []
    new = txt
    for const, tags in moi.items():
        if const not in hien:
            thieu.append(const)
            continue
        cu = hien[const]
        if [t.strip() for t in cu] == [t.strip() for t in tags]:
            continue
        dong = "    " + const + ":" + " " * max(1, 11 - len(const)) + \
               "[" + ", ".join(f'"{t}"' for t in tags) + "],"
        pat = re.compile(r"^ *" + re.escape(const) + r": *\[[^\]]*\],",
                         re.M | re.S)
        if pat.search(new):
            new = pat.sub(dong.replace("\\", "\\\\"), new, count=1)
            doi.append((const, cu, tags))
        else:
            # chua co trong TAGS -> chen truoc dau dong dong cuoi cua TAGS
            i = new.rfind("}\n\n\nif __name__")
            i = new.rfind("}", 0, new.find("\n\n\nif __name__")) \
                if i < 0 else i
            new = new[:i] + dong + "\n" + new[i:]
            them.append((const, tags))

    for c, cu, t in doi:
        print(f"  SUA  {c:12} {cu}  ->  {t}")
    for c, t in them:
        print(f"  THEM {c:12} {t}")
    for c in thieu:
        print(f"  BO QUA (khong co hang so nay trong clips.py): {c}")
    if not (doi or them):
        print("  khong co gi thay doi")
        return

    if not a.apply:
        print("\n-- THU thoi. Them --apply de ghi that. --")
        return

    shutil.copy(CLIPS, CLIPS + ".bak")
    open(CLIPS, "w", encoding="utf-8").write(new)
    print(f"\nDa ghi clips.py ({len(doi)} sua, {len(them)} them). "
          f"Ban cu: clips.py.bak")
    print("Kiem lai:  python3 clips.py")


if __name__ == "__main__":
    main()
