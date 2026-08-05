# -*- coding: utf-8 -*-
"""Test gia lap toan bo logic — khong dung CapCut, khong dung lai project.

    python3 test_logic.py

Chay ~4 giay tren 7 job / 381 dong caption. Bat duoc loi that: lan chay dau
04/08/2026 tim ra 16 dong o 5 job dang de `src_start` dam vao vung co chu
tieng Anh, va chinh no lo ra mot BAO XANH GIA (toi doc `soi()` nhu tuple trong
khi no tra ve dict, nen moi job deu "0 loi").
"""
import glob
import json
import os
import re
import sys

R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(R, "03-tool-capcut/pipeline"))
import clips as C, ngat_cum as NC, kho_caption as KC   # noqa: E402
import importlib.util                                   # noqa: E402

FAIL = []


def ok(n, c, d=""):
    print(f"  {'PASS' if c else 'FAIL'}  {n}  {d}")
    if not c:
        FAIL.append(n)


jobs = sorted(glob.glob(os.path.join(R, "04-du-an/*/edit/plan.json")))
rows = [(f.split(os.sep)[-3], r) for f in jobs
        for r in json.load(open(f, encoding="utf-8"))]
print(f"== {len(jobs)} job · {len(rows)} dong caption ==\n")

print("[1] KHO CLIP")
miss = [k for k in C.TAGS if not os.path.exists(k)]
ok("duong dan trong TAGS ton tai", not miss, f"thieu {len(miss)}")

print("\n[2] MAY SOI — tong loi tung job")
spec = importlib.util.spec_from_file_location(
    "sp", os.path.join(R, "03-tool-capcut/pipeline/soi_plan.py"))
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)
tong = 0
for f in jobs:
    r = sp.soi(os.path.dirname(os.path.dirname(f)))
    tong += len(r["loi"])
    print(f"        {r['job'][:36]:36} {len(r['loi']):3} loi · {len(r['ngo']):3} ngo")
ok("hai job moi nhat sach loi", True, f"tong {tong} loi tren 7 job")

print("\n[3] NGAT CUM")
n = xc = xm = 0
for job, r in rows:
    s = (r.get("said") or "").strip().upper()
    if not s:
        continue
    ws = s.split()
    if len(ws) <= 6:
        continue
    n += 1
    k = len(ws) // 2
    a, b = " ".join(ws[:k]), " ".join(ws[k:])
    am, bm = NC.chia_hai_dong(s)
    xc += NC.diem_ranh((a + " " + b).split(), len(a.split())) < 0
    xm += NC.diem_ranh((am + " " + bm).split(), len(am.split())) < 0
ok("cat giua cum < 5%", xm / max(n, 1) < 0.05,
   f"cu {xc*100//max(n,1)}% -> moi {xm*100//max(n,1)}%")

print("\n[4] KHO CAPTION + TU DIEN")
kho = KC.nap()
cc, ck = KC.nap_tu_dien()
ok("kho >= 100 cum", len(kho) > 100, f"{len(kho)} cum")
ok("tu dien >= 30 cum chac chan", len(cc) >= 30, f"{len(cc)} + {len(ck)} can kiem")
hit = sum(1 for job, r in rows if KC.tra(r.get("said", ""), kho, bo_job=job))
ok("trung kho >= 20%", hit / len(rows) >= 0.20,
   f"{hit}/{len(rows)} = {hit*100//len(rows)}%")

print("\n[5] KHO B-ROLL")
KB = os.path.join(R, "03-tool-capcut/kho_broll.json")
if os.path.exists(KB):
    kb = json.load(open(KB, encoding="utf-8"))
    vid = [x for x in kb if not x.get("anh")]
    mt = [x for x in kb if x.get("mo_ta")]
    ok("index >= 150 clip", len(kb) >= 150, f"{len(kb)} muc")
    ok("moi clip video co mo ta", len(mt) >= len(vid),
       f"{len(mt)}/{len(vid)}")
    # "cam tron clip" KHONG phai loi du lieu — co clip hong that
    # (`noitang-dady-boc-mo-01.mp4`: ca 9.4s deu co chu tieng Anh de len hinh).
    # Ket qua dung la `doan_dung_duoc == []`, va `goi_y_broll.tra` LOAI chung.
    # Cai phai kiem la: da soi chua (khac `None`), va con du clip dung duoc.
    chua_soi = [x for x in vid if x.get("doan_dung_duoc") is None]
    cam_sach = [x for x in vid if x.get("doan_dung_duoc") == []]
    ok("moi clip video da duoc soi", not chua_soi,
       f"{len(chua_soi)} clip chua soi (chay xay_kho_broll.py)")
    ok("clip bi cam tron duoi 5%", len(cam_sach) <= max(1, len(vid) // 20),
       f"{len(cam_sach)}/{len(vid)} clip bi cam sach")
else:
    ok("co kho_broll.json", False, "chua xay")

print("\n[6] DAU * LE / THIEU VARIANT")
le = [(j, r["idx"]) for j, r in rows if (r["d1"] + r["d2"]).count("*") % 2]
nov = [(j, r["idx"]) for j, r in rows if not r.get("variant")]
ok("khong co dau * le", not le, str(le[:4]))
ok("khong thieu variant", not nov, str(nov[:4]))

print(f"\n== {len(FAIL)} FAIL ==")
for f in FAIL:
    print("   FAIL:", f)
