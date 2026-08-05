# -*- coding: utf-8 -*-
"""Sinh DANH MUC toan kho -> 03-tool-capcut/danh_muc_kho.json

    python3 xay_danh_muc.py            # xem thu
    python3 xay_danh_muc.py --ghi      # ghi that

HAI TANG, DUNG TRON VAO NHAU:

  TANG 1 — DANH MUC (file nay sinh ra, ~1053 clip)
      Moi clip trong kho, kem `mo_ta` tieng Viet dich tu ten file.
      De `goi_y_broll.py` TRA RA duoc. Khong can dat ten hang so.

  TANG 2 — HANG SO trong `clips.py` (~180 clip)
      Chi nhung clip da dung that, co ten de `plan.py` goi.
      Clip nao chung to huu ich thi moi nang len tang 2.

VI SAO TACH: truoc 05/08/2026 mot clip chi "ton tai" voi pipeline khi co hang
so trong `clips.py`. Ket qua do duoc: 9 job dung 414 luot B-roll nhung chi
xoay quanh 86 clip — 8% cua kho. `richnatto-01.mp4` mot minh gong 30 luot.
Khong phai vi kho ngheo, ma vi 874 clip khong ai khai nen may khong thay.
Gio khai het o tang 1, tang 2 giu nguyen su chon loc.
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clips as C                                                  # noqa: E402
import tu_dien_kho as T                                            # noqa: E402

RA = os.path.join(os.path.dirname(HERE), "danh_muc_kho.json")
# ten dung quy uoc: <chu de>[-<mo ta>...]-<so>.<duoi>
DUNG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*-\d+\.[a-zA-Z0-9]+$")
# folder chi chua nhac/tieng dong — khong phai B-roll hinh
BO_QUA = {"am thanh", "nhac video quang cao"}


def khong_dau(s):
    import unicodedata as ud
    s = ud.normalize("NFD", s)
    return "".join(c for c in s if not ud.combining(c)).lower()


def probe(p):
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height", "-show_entries", "format=duration",
         "-of", "json", p], capture_output=True, text=True)
    try:
        d = json.loads(r.stdout); st = d["streams"][0]
        return st["width"], st["height"], float(d["format"].get("duration", 0) or 0)
    except Exception:
        return 0, 0, 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ghi", action="store_true")
    a = ap.parse_args()

    if not os.path.isdir(C.B):
        sys.exit(f"khong thay kho: {C.B}\n  cam o T7, hoac dat DILIM_FOOTAGE")

    khai = {os.path.basename(v) for k, v in vars(C).items()
            if k.isupper() and isinstance(v, str) and v.startswith(C.B)}

    muc, bo, chua_chuan = [], 0, []
    for d in sorted(os.listdir(C.B)):
        p = os.path.join(C.B, d)
        if not os.path.isdir(p):
            continue
        if khong_dau(d) in BO_QUA:
            bo += len([f for f in os.listdir(p) if not f.startswith(".")])
            continue
        for f in sorted(os.listdir(p)):
            fp = os.path.join(p, f)
            if f.startswith(".") or not os.path.isfile(fp):
                continue
            if not DUNG.match(f):
                chua_chuan.append(f)
                continue
            w, h, dai = probe(fp)
            muc.append({
                "file": f, "path": fp, "folder": d,
                "w": w, "h": h, "doc": h > w, "dai": round(dai, 2),
                "anh": f.lower().endswith(C.IMG_EXT),
                "mo_ta": T.mo_ta_tu_ten(f),
                "da_khai": f in khai,
            })

    print(f"  danh muc : {len(muc)} clip")
    print(f"  trong do : {sum(1 for m in muc if m['da_khai'])} da co hang so trong clips.py")
    print(f"  bo qua   : {bo} file nhac/tieng dong")
    if chua_chuan:
        print(f"  CHUA DUNG QUY UOC ({len(chua_chuan)}): {chua_chuan[:5]}")
    print(f"\n  vi du mo_ta:")
    for m in muc[:4]:
        print(f"    {m['file'][:38]:38} -> {m['mo_ta']}")

    if a.ghi:
        json.dump(muc, open(RA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\n-> {RA}")
    else:
        print("\n-- XEM THU. Them --ghi de ghi that. --")


if __name__ == "__main__":
    main()
