# -*- coding: utf-8 -*-
"""Hoc tu cac ban DA DUNG — nap tan suat + backlink/frontlink vao kho B-roll.

    python3 hoc_lich_su.py            # nap vao kho_broll.json
    python3 hoc_lich_su.py --xem      # chi xem, khong ghi

Y TUONG (anh Thanh 04/08/2026): "broll co the hoc tu video da chot roi, xay
he thong index voi quy chuan voi backlink front link vs tan suat su dung".

BA LOAI LIEN KET:

  frontlink  clip  -> nhung CAU CAPTION da dung no
                      ("clip nay minh hoa cho y gi")
  backlink   tu khoa -> nhung CLIP da duoc dung cho tu khoa do
                      (index nguoc — tra bang chu, ra clip)
  tan suat   clip  -> dung bao nhieu lan / con lai bao nhieu sau khi anh sua

CHO QUAN TRONG NHAT — `con_lai`:
`TAGS` la tu khoa toi go tay, khong ai xac nhan. Con `con_lai` la so lan mot
clip SONG SOT qua ban dung cuoi cua anh Thanh. Do la phieu bau that.
Vi du job magie: toi dat 53 doan B-roll, anh giu 49 — 4 doan bi bo la 4 phieu
chong.
"""
import argparse
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
KHO = os.path.join(os.path.dirname(HERE), "kho_broll.json")
ROOT = os.path.dirname(os.path.dirname(HERE))
DRAFTS = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")

DEM = {"la", "va", "co", "cua", "cho", "thi", "ma", "o", "den", "khi", "nen",
       "voi", "mot", "nay", "do", "duoc", "trong", "cac", "nhung", "cai", "no",
       "minh", "roi", "vi", "cung", "dang", "se", "da", "rat", "lai", "ra",
       "di", "ve", "hay", "hoac", "chi", "them", "nua", "hon", "qua", "lam"}


def chuan(s):
    import unicodedata
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c)).replace("d", "d")
    return re.sub(r"[^a-z0-9\s]", " ", s)


def tu_nghia(s):
    return [w for w in chuan(s).split() if w and w not in DEM and len(w) > 1]


def draft_broll(job):
    """clip nao CON LAI trong draft CapCut cua anh (neu co)."""
    p = os.path.join(DRAFTS, f"DiLiM - {job}", "draft_info.json")
    if not os.path.exists(p):
        return None
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception:
        return None
    V = {m["id"]: m for m in d["materials"].get("videos", [])}
    out = []
    for t in d["tracks"]:
        if t.get("name") != "broll":
            continue
        for s in t.get("segments", []):
            p2 = V.get(s["material_id"], {}).get("path", "")
            out.append(re.sub(r"^\d{3}_", "", os.path.basename(p2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xem", action="store_true")
    a = ap.parse_args()

    front = defaultdict(list)      # clip -> [caption]
    back = defaultdict(set)        # tu khoa -> {clip}
    dung = defaultdict(int)        # clip -> so lan dat
    con = defaultdict(int)         # clip -> so lan song sot qua ban cua anh
    duyet_co = defaultdict(int)    # clip -> so lan co ban duyet de doi chieu
    job_cua = defaultdict(set)

    import glob
    for f in sorted(glob.glob(os.path.join(ROOT, "04-du-an/*/edit/plan.json"))):
        job = f.split(os.sep)[-3]
        plan = json.load(open(f, encoding="utf-8"))
        conlai = draft_broll(job)
        conlai_dem = defaultdict(int)
        for c in (conlai or []):
            conlai_dem[c] += 1
        dat_dem = defaultdict(int)

        for r in plan:
            p = (r.get("path") or "").strip()
            if not p:
                continue
            b = os.path.basename(p)
            txt = (r.get("d1", "") + " " + r.get("d2", "")).replace("*", "").strip()
            dung[b] += 1
            dat_dem[b] += 1
            job_cua[b].add(job)
            front[b].append({"job": job, "idx": r["idx"], "chu": txt,
                             "variant": r.get("variant", ""),
                             "src_start": r.get("src_start", 0)})
            for w in tu_nghia(txt):
                back[w].add(b)
        if conlai is not None:
            for b, n in dat_dem.items():
                duyet_co[b] += n
                con[b] += min(n, conlai_dem.get(b, 0))

    print(f"clip da tung dung : {len(dung)}")
    print(f"tu khoa hoc duoc  : {len(back)}   (TAGS go tay hien co ~157 clip x 3-5 tu)")
    print(f"clip co doi chieu ban cua anh: {len(duyet_co)}")
    print()
    print(f"{'clip':40}{'dat':>5}{'con':>5}  ty le")
    for b in sorted(dung, key=lambda x: -dung[x])[:14]:
        if duyet_co.get(b):
            tl = f"{con[b]*100//duyet_co[b]}%"
        else:
            tl = "-"
        print(f"{b[:40]:40}{dung[b]:>5}{con.get(b,0):>5}  {tl}")

    if a.xem:
        return

    if not os.path.exists(KHO):
        sys.exit(f"chua co {KHO} — chay xay_kho_broll.py truoc")
    kho = json.load(open(KHO, encoding="utf-8"))
    for x in kho:
        b = x["file"]
        x["da_dung"] = dung.get(b, 0)
        x["con_lai_sau_khi_anh_sua"] = con.get(b, 0)
        x["co_ban_doi_chieu"] = duyet_co.get(b, 0)
        x["job"] = sorted(job_cua.get(b, []))
        x["frontlink"] = front.get(b, [])[:20]
        x["tu_khoa_hoc"] = sorted({w for w, cs in back.items() if b in cs})[:40]
    json.dump(kho, open(KHO, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    bl = os.path.join(os.path.dirname(HERE), "kho_broll_backlink.json")
    json.dump({w: sorted(cs) for w, cs in sorted(back.items())},
              open(bl, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n-> {KHO}   (+ tan suat, frontlink, tu khoa hoc)")
    print(f"-> {bl}   ({len(back)} tu khoa -> clip)")


if __name__ == "__main__":
    main()
