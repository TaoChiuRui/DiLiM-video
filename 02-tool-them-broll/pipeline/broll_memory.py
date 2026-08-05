# -*- coding: utf-8 -*-
"""BO NHO B-ROLL: y (caption) -> clip DA DUOC NGUOI DUNG DUYET.

Xay tu cac job da ban giao va da duoc duyet. Khi dung video moi cung chu de,
TRA BANG NAY TRUOC roi moi di tim clip moi - nguoi dung chot 2026-07-29:
"nếu ý giống 90% bạn có thể chọn ngay b-roll đó".

    python broll_memory.py build          # quet lai cac job da duyet -> broll_memory.json
    python broll_memory.py find "<y>"     # tra thu 1 y
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
STORE = HERE / "broll_memory.json"

# Job da ban giao & duoc duyet, theo thu tu uu tien (moi nhat/duoc duyet ky nhat truoc)
APPROVED_JOBS = ["jobs/qc_sun_mon", "jobs/sun_khop_khong_biet_keu"]

STOP = set("""la va cua chung ta minh nay do la co khong cho den khi ma nhung
nguoi anh chi nha ha thi se duoc bi ra vao len xuong tren duoi mot hai o den
tu voi nhu rat qua cung deu con moi day kia thu""".split())


def nrm(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").replace("đ", "d")
    return re.sub(r"[^a-z0-9\s]", " ", s)


def toks(s: str) -> set:
    return {w for w in nrm(s).split() if len(w) > 1 and w not in STOP}


def build():
    rows = []
    for job in APPROVED_JOBS:
        d = HERE / job
        try:
            plan = json.loads((d / "broll_plan.json").read_text(encoding="utf-8"))
            caps = json.loads((d / "captions.json").read_text(encoding="utf-8"))
        except FileNotFoundError:
            print("bo qua (thieu file):", job)
            continue
        caps.sort(key=lambda c: c["from"])
        for b in sorted(plan, key=lambda z: z["from"]):
            f0, f1 = b["from"], b["from"] + b["durationInFrames"]
            idea = " | ".join(c["text"].replace("\n", " / ").replace("*", "")
                              for c in caps if c["from"] < f1 and c["from"] + c["durationInFrames"] > f0)
            if not idea:
                continue
            rows.append({"y": idea, "path": b["path"], "src_start_s": b.get("src_start_s", 0.0),
                         "is_image": b.get("is_image", False),
                         "crop_bias": b.get("crop_bias", 0.5), "nguon": job})
    # gop trung: cung path + src_start thi gop y lai
    merged = {}
    for r in rows:
        k = (r["path"], round(r["src_start_s"], 2))
        if k in merged:
            merged[k]["y"] += " | " + r["y"]
        else:
            merged[k] = r
    out = list(merged.values())
    for r in out:
        r["tok"] = sorted(toks(r["y"]))
    STORE.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"da ghi {STORE}  ({len(out)} muc, tu {len(APPROVED_JOBS)} job da duyet)")


def load():
    return json.loads(STORE.read_text(encoding="utf-8"))


def find(idea: str, mem=None, thr: float = 0.34):
    """Tra y -> (muc, diem). Diem = do trung tu khoa (Jaccard co trong so ve phia y ngan hon)."""
    mem = mem or load()
    t = toks(idea)
    if not t:
        return None, 0.0
    best, bs = None, 0.0
    for m in mem:
        mt = set(m["tok"])
        if not mt:
            continue
        inter = len(t & mt)
        if not inter:
            continue
        score = inter / min(len(t), len(mt))          # bao phu y ngan hon
        score *= (0.6 + 0.4 * inter / max(len(t), 1))  # phat neu chi trung vai tu le
        if score > bs:
            best, bs = m, score
    return (best, bs) if bs >= thr else (None, bs)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    if cmd == "build":
        build()
    elif cmd == "find":
        m, s = find(" ".join(sys.argv[2:]), thr=0.0)
        print(f"diem {s:.2f}")
        if m:
            print("  y   :", m["y"][:140])
            print("  clip:", os.path.basename(m["path"]), "@", m["src_start_s"])
