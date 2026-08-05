# -*- coding: utf-8 -*-
"""Doc so THAT tu mot project CapCut anh Thanh da chinh tay.

    python3 doc_capcut.py                          # liet ke project dang co
    python3 doc_capcut.py --draft "DiLiM - abc"    # doc het cac track
    python3 doc_capcut.py --draft "DiLiM - abc" --track logo

VI SAO CO FILE NAY: moi thong so trong tool nay deu di theo mot duong —
anh keo tay trong CapCut, roi so do duoc CHEP vao code (dai B-roll, vi tri
caption, logo). Truoc day toi doc so tren PANEL cua CapCut roi TU QUY DOI
sang don vi thu vien. Quy doi la doan: da sai mot lan o logo 04/08/2026.

File draft ghi THANG gia tri thu vien dung. Doc tu day thi khong con phep
doi nao o giua, chep vao code la xong.

Cach dung sau khi anh chinh:
    1. anh mo CapCut, keo/chinh cho vua y, luu lai
    2. python3 doc_capcut.py --draft "DiLiM - <ten>" --track logo
    3. chep 3 so vao LOGO_SCALE / LOGO_X / LOGO_Y trong 6_to_capcut.py
"""
import argparse
import json
import os
import sys

DRAFTS = os.path.expanduser(
    "~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
US = 1_000_000


def find(name):
    p = os.path.abspath(os.path.expanduser(name))
    if os.path.isdir(p):
        return p
    p = os.path.join(DRAFTS, name)
    if os.path.isdir(p):
        return p
    hits = [d for d in os.listdir(DRAFTS)
            if name.lower() in d.lower()
            and os.path.isdir(os.path.join(DRAFTS, d))]
    if len(hits) == 1:
        return os.path.join(DRAFTS, hits[0])
    if not hits:
        sys.exit(f"khong thay project nao ten giong «{name}» trong {DRAFTS}")
    sys.exit("ten mo ho, hop voi: " + ", ".join(hits))


def fmt(v):
    """So cho de chep vao code."""
    return f"{v:.6f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--draft", help="ten project CapCut (hoac duong dan)")
    ap.add_argument("--track", help="chi mot track, vd logo")
    ap.add_argument("--all-segments", action="store_true",
                    help="in tung segment thay vi gom cac gia tri giong nhau")
    a = ap.parse_args()

    if not a.draft:
        if not os.path.isdir(DRAFTS):
            sys.exit(f"khong thay {DRAFTS}")
        print("project dang co:")
        for d in sorted(os.listdir(DRAFTS)):
            if os.path.isdir(os.path.join(DRAFTS, d)) and not d.startswith("."):
                print(f"   {d}")
        print("\nchay lai voi --draft \"<ten>\"")
        return

    root = find(a.draft)
    info = os.path.join(root, "draft_info.json")
    if not os.path.exists(info):
        sys.exit(f"khong thay draft_info.json trong {root}")
    d = json.load(open(info, encoding="utf-8"))

    cc = d.get("canvas_config", {})
    print(f"project : {os.path.basename(root)}")
    print(f"khung   : {cc.get('width')}x{cc.get('height')}\n")

    mat = {m["id"]: m for m in d["materials"].get("videos", [])}
    for t in d["tracks"]:
        name = t.get("name") or t["type"]
        if a.track and name != a.track:
            continue
        segs = t["segments"]
        print(f"── track «{name}» · {t['type']} · {len(segs)} segment")
        if not segs:
            print()
            continue

        rows = []
        for s in segs:
            c = s.get("clip") or {}
            sc, tr = c.get("scale", {}), c.get("transform", {})
            m = mat.get(s.get("material_id"), {})
            rows.append((
                round(sc.get("x", 1), 6), round(sc.get("y", 1), 6),
                round(tr.get("x", 0), 6), round(tr.get("y", 0), 6),
                round(c.get("rotation", 0), 3),
                os.path.basename(m.get("path", "")),
                s["target_timerange"]["start"] / US,
                s["target_timerange"]["duration"] / US,
            ))

        if a.all_segments:
            for r in rows:
                print(f"   {r[6]:7.2f}s +{r[7]:5.2f}s  scale {r[0]:<9} "
                      f"x {r[2]:<11} y {r[3]:<11} rot {r[4]:<6} {r[5][:34]}")
        else:
            # gom: cac segment cung bo so thi in mot dong
            from collections import Counter
            c = Counter((r[0], r[1], r[2], r[3], r[4]) for r in rows)
            for (sx, sy, tx, ty, rot), n in c.most_common():
                print(f"   {n:3} segment  scale_x={fmt(sx)} scale_y={fmt(sy)}  "
                      f"transform_x={fmt(tx)} transform_y={fmt(ty)}"
                      + (f"  rotation={fmt(rot)}" if rot else ""))
                if name == "logo" or (a.track and n == len(rows)):
                    print(f"        -> chep vao 6_to_capcut.py:")
                    print(f"           LOGO_SCALE = {fmt(sx)}")
                    print(f"           LOGO_X     = {fmt(tx)}")
                    print(f"           LOGO_Y     = {fmt(ty)}")
        print()


if __name__ == "__main__":
    main()
