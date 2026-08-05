# -*- coding: utf-8 -*-
"""BACKTEST — cham ban may dung so voi ban anh Thanh da chot.

    python3 backtest.py                     # cham moi job co draft cua anh
    python3 backtest.py --job <ten-job>

VI SAO: moi con so toi bao tu truoc toi gio (32% trung kho, 70% neo dung dau
cum, 0% cat giua cum) deu do TREN CHINH DU LIEU TOI TAO RA. Chung noi "tot len
bao nhieu so voi chinh no", khong noi "dung bao nhieu so voi y anh Thanh".

Ban draft anh da sua trong CapCut MOI la chuan doc lap. File nay cham 3 thu:

  CAT      moc cat cua toi trung moc cua anh bao nhieu (sai so 0.5s)
  CAPTION  caption toi viet co con lai trong ban cua anh khong
  B-ROLL   clip toi chon co con lai khong, va con dung o cho do khong

Diem khong bao gio len 100 duoc — anh con sua theo gu. Nhung XU HUONG cua no
qua cac lan sua tool moi la cai dang nhin.
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
DRAFTS = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
SAI_SO = 0.5          # giay — moc cat lech duoi muc nay coi la trung


def base(p):
    return re.sub(r"^\d{3}_", "", os.path.basename(p or ""))


def doc_draft(job):
    p = os.path.join(DRAFTS, f"DiLiM - {job}", "draft_info.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8"))
    V = {m["id"]: m for m in d["materials"].get("videos", [])}
    out = {"aroll": [], "broll": [], "caption": []}
    for t in d["tracks"]:
        n = t.get("name")
        if n not in out:
            continue
        for s in t.get("segments", []):
            tr = s["target_timerange"]
            sr = s.get("source_timerange") or {}
            out[n].append({
                "file": base(V.get(s["material_id"], {}).get("path", "")),
                "tl": tr["start"] / 1e6, "dai": tr["duration"] / 1e6,
                "src": sr.get("start", 0) / 1e6,
            })
    for k in out:
        out[k].sort(key=lambda x: x["tl"])
    return out


def cham(job):
    import job_path
    jd = job_path.job_dir(job)
    P = os.path.join(jd, "edit/plan.json")
    E = os.path.join(jd, "edit/edl.json")
    anh = doc_draft(job)
    if anh is None or not os.path.exists(P):
        return None
    plan = json.load(open(P, encoding="utf-8"))
    r = {"job": job}

    # ---- CAT ----
    if os.path.exists(E) and anh["aroll"]:
        toi = [k[0] for k in json.load(open(E, encoding="utf-8"))["keeps"]]
        cua_anh = [s["src"] for s in anh["aroll"]]
        trung = sum(1 for a in cua_anh
                    if any(abs(a - b) <= SAI_SO for b in toi))
        r["cat"] = (trung, len(cua_anh), len(toi))

    # ---- CAPTION ----
    con = Counter(s["file"] for s in anh["caption"])
    toi_cap = [f"cap_{x['idx']:03d}.png" for x in plan]
    giu = sum(1 for c in toi_cap if con.get(c))
    r["caption"] = (giu, len(toi_cap), len(anh["caption"]))

    # ---- B-ROLL ----
    ta = Counter(base(x["path"]) for x in plan if x.get("path"))
    aa = Counter(s["file"] for s in anh["broll"])
    trung = sum(min(v, aa.get(k, 0)) for k, v in ta.items())
    r["broll"] = (trung, sum(ta.values()), sum(aa.values()))

    # clip anh BO han
    r["bo_han"] = sorted(k for k, v in ta.items() if aa.get(k, 0) == 0)
    r["anh_them"] = sorted(k for k, v in aa.items() if ta.get(k, 0) == 0)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job")
    a = ap.parse_args()
    jobs = ([a.job] if a.job else
            sorted(os.path.basename(os.path.dirname(os.path.dirname(f)))
                   for f in glob.glob(os.path.join(ROOT, "04-du-an/*/edit/plan.json"))))
    kq = [x for x in (cham(j) for j in jobs) if x]
    if not kq:
        sys.exit("khong job nao co draft cua anh de doi chieu")

    print(f"{'job':34}{'CAT':>14}{'CAPTION':>16}{'B-ROLL':>16}")
    for r in kq:
        c = r.get("cat")
        cs = f"{c[0]}/{c[1]} ({c[0]*100//max(c[1],1)}%)" if c else "-"
        p = r["caption"]; b = r["broll"]
        print(f"{r['job'][:34]:34}{cs:>14}"
              f"{f'{p[0]}/{p[1]} ({p[0]*100//max(p[1],1)}%)':>16}"
              f"{f'{b[0]}/{b[1]} ({b[0]*100//max(b[1],1)}%)':>16}")
    print()
    for r in kq:
        if r["bo_han"] or r["anh_them"]:
            print(f"{r['job']}:")
            if r["bo_han"]:
                print(f"   anh BO han : {', '.join(r['bo_han'])}")
            if r["anh_them"]:
                print(f"   anh THEM   : {', '.join(r['anh_them'])}")


if __name__ == "__main__":
    main()
