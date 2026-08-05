# -*- coding: utf-8 -*-
"""Ve 44 caption thanh PNG bang DUNG engine cua bo Tinh (pipeline/caption_style.py).

Khac han cach cu (text layer cua CapCut): style o day la style that cua DiLiM —
font Anton, 3 ho mau xoay deterministic, khoi nen bo goc 14px, tu dong thu font
neu dong qua dai, dat ngay duoi dai B-roll.

    python3 render_captions.py
"""
import json, os, sys

import argparse as _ap
import sys as _sys

def _job_dir():
    """Thu muc job — truyen bang --job. Moi script trong pipeline nay deu
    dung chung, khong con chep sang tung job nua."""
    _p = _ap.ArgumentParser(add_help=False)
    _p.add_argument("--job", help="duong dan (04-du-an/<ten>) HOAC ten job")
    _a, _ = _p.parse_known_args()
    if "--help" in _sys.argv or "-h" in _sys.argv:
        print(__doc__ or "");  raise SystemExit(0)
    import job_path                      # giai ca 3 dang, xem job_path.py
    return job_path.job_dir(_a.job)


HERE = _job_dir()
PIPE = os.path.dirname(os.path.abspath(__file__))
TINH = os.path.abspath(os.path.join(PIPE, "../../02-tool-them-broll/pipeline"))
sys.path.insert(0, TINH)
from caption_style import StyleCounters, render_caption_png   # noqa: E402

PLAN = os.path.join(HERE, "edit/plan.json")
OUT = os.path.join(HERE, "edit/captions_png")


def main():
    plan = json.load(open(PLAN, encoding="utf-8"))
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        os.remove(os.path.join(OUT, f))

    counters = StyleCounters()          # dem deterministic cho CA video
    total = 0
    for p in plan:
        cap = {"text": p["text"], "variant": p["variant"]}
        out = os.path.join(OUT, f"cap_{p['idx']:03d}.png")
        render_caption_png(cap, counters, out, position_mode="top")
        total += os.path.getsize(out)

    n = len(plan)
    print(f"da ve {n} caption PNG -> {OUT}")
    print(f"tong dung luong: {total/1024/1024:.2f} MB   (trung binh {total/n/1024:.0f} KB/caption)")


if __name__ == "__main__":
    main()
