# -*- coding: utf-8 -*-
"""Doi chieu clip TOI chon vs clip NGUOI DUNG chon -> rut ra quy luat."""
# THAM KHAO — script nay lay nguyen van tu dot dung 5 video VR 9.6.2026,
# duong dan job/ban duyet la cua dot do. Doc de lay CACH LAM, sua bien o dau file
# truoc khi chay lai.
import json, os, re, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "pipeline")))
from paths import JOBS_ROOT as _JR, MUSIC_ROOT as _MR  # noqa: E402
J = str(_JR)
full = json.load(open(os.path.join(J,"broll_full.json"), encoding="utf-8"))
d1 = json.load(open(r"D:\download\broll-duyet.json", encoding="utf-8"))
d3 = json.load(open(r"D:\download\broll-duyet-v3.json", encoding="utf-8"))

def clean(p):
    p=(p or "").strip().strip('"').strip(); p=re.sub(r'^="','',p)
    return p.split('","')[0].strip('"').strip()
def folder(p):
    parts = p.replace("/","\\").split("\\")
    try: return parts[parts.index("Footage B-roll")+1]
    except: return "?"

giu, thay, them = [], [], []

for vi, v in enumerate(full):
    ch3 = {r["idx"]: r for r in d3[vi]["rows"]}
    add1 = {b["idx"]: clean(b["path"]) for b in d1[vi].get("bosung", [])} if vi < len(d1) else {}

    for r in v["rows"]:
        i = r["idx"]
        moi = clean(ch3[i]["path_moi"]) if i in ch3 else ""
        goc = r["path"]                      # toi de xuat (da gom ca ban v1 nguoi dung them)
        nguon = r["src"]

        if moi:
            if goc and nguon == "tôi đề xuất":
                thay.append((vi, i, r["cap"], r["say"], goc, moi))
            else:
                them.append((vi, i, r["cap"], r["say"], moi))
        elif goc and nguon == "tôi đề xuất":
            giu.append((vi, i, r["cap"], goc))
        elif goc and nguon == "bạn chọn":
            them.append((vi, i, r["cap"], r["say"], goc))

print("="*74)
print(f"TOI DE XUAT: {len(giu)+len(thay)} clip  ->  GIU {len(giu)}  |  BI THAY {len(thay)}")
print(f"NGUOI DUNG TU THEM: {len(them)} clip")
tong = len(giu)+len(thay)
if tong: print(f"Ty le clip toi chon duoc giu: {len(giu)/tong*100:.0f}%")
print("="*74)

print("\n### THU MUC NGUOI DUNG HAY LAY (clip ho tu chon/thay vao)")
fu = Counter(folder(x[-1]) for x in them) + Counter(folder(x[5]) for x in thay)
for f, n in fu.most_common(12):
    print(f"   {n:>3}x  {f}")

print("\n### THU MUC TOI HAY LAY")
fm = Counter(folder(x[3]) for x in giu) + Counter(folder(x[4]) for x in thay)
for f, n in fm.most_common(12):
    print(f"   {n:>3}x  {f}")

print("\n### CAC CLIP BI THAY — toi chon gi, ho doi thanh gi")
for vi, i, cap, say, goc, moi in thay:
    print(f"\n V{vi+1} #{i}  {cap[:58]}")
    print(f"    tôi : [{folder(goc)}] {os.path.basename(goc)[:56]}")
    print(f"    họ  : [{folder(moi)}] {os.path.basename(moi)[:56]}")
