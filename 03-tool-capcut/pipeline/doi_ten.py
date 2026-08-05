# -*- coding: utf-8 -*-
"""Doi ten file B-roll tren o T7 + SUA MOI THAM CHIEU trong du an.

    python3 doi_ten.py --map ten_moi.json                 # thu, khong ghi gi
    python3 doi_ten.py --map ten_moi.json --apply         # lam that
    python3 doi_ten.py --undo 05-footage-moi/doi_ten_log/xxx.json --apply

File map:
    {"folder": "01 Đau đầu - ...",
     "doi": {"ten cu.mp4": "daudau-abc-01.mp4", ...}}

VI SAO CAN SCRIPT: doi ten bang Finder thi clips.py va plan.py cua cac job cu
DUT LINK am tham — plan_build chi bao "KHONG TIM THAY" luc dung lai. Script nay
doi ten VA va lai duong dan trong:
    03-tool-capcut/pipeline/clips.py
    04-du-an/*/plan.py
    04-du-an/*/edit/plan.json

BAY NFC/NFD: o T7 tra ten dang NFD, plan.py ghi NFC. So chuoi truc tiep se
truot. Moi so khop o day deu chuan hoa NFC truoc.
"""
import argparse
import datetime
import json
import os
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
B = "/Volumes/T7 for Mac/02. Dilim Footage"
LOG_DIR = os.path.join(ROOT, "05-footage-moi", "doi_ten_log")


def N(s):
    return unicodedata.normalize("NFC", s)


def targets():
    """Moi file co the chua duong dan B-roll."""
    out = [os.path.join(HERE, "clips.py")]
    # 05/08/2026: them hai kho JSON. Truoc do doi ten xong, `kho_broll.json`
    # con giu ten cu -> `goi_y_broll` van goi y `VAI GÁY (1).mp4` trong khi
    # file that da thanh `dilimquay-vaigay-ong-01.mp4`. Chay ra duong dan chet.
    for _t in ("kho_broll.json", "danh_muc_kho.json"):
        _p = os.path.join(os.path.dirname(HERE), _t)
        if os.path.isfile(_p):
            out.append(_p)
    du_an = os.path.join(ROOT, "04-du-an")
    if os.path.isdir(du_an):
        for job in sorted(os.listdir(du_an)):
            for rel in ("plan.py", "edit/plan.json"):
                p = os.path.join(du_an, job, rel)
                if os.path.isfile(p):
                    out.append(p)
    return [p for p in out if os.path.isfile(p)]


def patch(pairs, apply):
    """pairs = [(duong_dan_cu, duong_dan_moi)]. -> {file: so_lan_thay}

    Hai dang duong dan phai vet ca hai:
      1. NGUYEN CA DUONG DAN  — plan.py / plan.json ghi kieu nay
      2. `/<ten file>"`       — clips.py ghi f"{DD}/mat-ngu.mp4", trong file
         KHONG he co ten thu muc. Chi so dang nay o clips.py, va chi khi ten
         file do duy nhat trong ca file — de khong va nham clip trung ten o
         thu muc khac.
    """
    hit = {}
    for f in targets():
        txt = open(f, encoding="utf-8").read()
        new = txt
        n = 0
        for old, moi in pairs:
            for form in {old, N(old), unicodedata.normalize("NFD", old)}:
                if form in new:
                    n += new.count(form)
                    new = new.replace(form, moi)
        if os.path.basename(f) == "clips.py":
            for old, moi in pairs:
                cu_b, moi_b = os.path.basename(old), os.path.basename(moi)
                for form in {f'/{cu_b}"', f'/{N(cu_b)}"',
                             f'/{unicodedata.normalize("NFD", cu_b)}"'}:
                    c = new.count(form)
                    if c:
                        n += c
                        new = new.replace(form, f'/{moi_b}"')
        if n:
            hit[os.path.relpath(f, ROOT)] = n
            if apply:
                open(f, "w", encoding="utf-8").write(new)
    return hit


def run(folder, doi, apply):
    src = os.path.join(B, folder)
    if not os.path.isdir(src):
        sys.exit(f"khong thay thu muc: {src}")

    on_disk = {N(f): f for f in os.listdir(src)}
    plan, loi = [], []
    for cu, moi in doi.items():
        real = on_disk.get(N(cu))
        if real is None:
            loi.append(f"KHONG CO tren o: {cu}")
            continue
        if N(moi) in on_disk and N(moi) != N(cu):
            loi.append(f"TRUNG TEN da co: {moi}")
            continue
        if sum(1 for _, m in doi.items() if N(m) == N(moi)) > 1:
            loi.append(f"TRUNG TEN trong map: {moi}")
            continue
        plan.append((os.path.join(src, real), os.path.join(src, moi), real, moi))

    if loi:
        for e in loi:
            print("  " + e)
        sys.exit(f"\n{len(loi)} loi — khong doi gi ca.")

    pairs = [(f"{folder}/{cu}", f"{folder}/{moi}") for _, _, cu, moi in plan]
    hit = patch(pairs, False)

    print(f"{len(plan)} file se doi ten:")
    for _, _, cu, moi in plan:
        print(f"  {cu[:52]:52} -> {moi}")
    print(f"\nTham chieu se sua ({sum(hit.values())} cho):")
    for f, n in sorted(hit.items()):
        print(f"  {n:3}x  {f}")
    if not hit:
        print("  (khong co)")

    if not apply:
        print("\n-- THU thoi. Them --apply de lam that. --")
        return

    for old, new, _, _ in plan:
        os.rename(old, new)
    patch(pairs, True)

    os.makedirs(LOG_DIR, exist_ok=True)
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log = os.path.join(LOG_DIR, f"{folder[:2]}-{stamp}.json")
    json.dump({"folder": folder, "doi": {cu: moi for _, _, cu, moi in plan},
               "tham_chieu": hit}, open(log, "w"), ensure_ascii=False, indent=1)
    print(f"\nXONG. Nhat ky hoan tac: {os.path.relpath(log, ROOT)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map")
    ap.add_argument("--undo")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()

    if a.undo:
        d = json.load(open(a.undo, encoding="utf-8"))
        run(d["folder"], {v: k for k, v in d["doi"].items()}, a.apply)
        return
    if not a.map:
        sys.exit("can --map hoac --undo")
    d = json.load(open(a.map, encoding="utf-8"))
    run(d["folder"], d["doi"], a.apply)


if __name__ == "__main__":
    main()
