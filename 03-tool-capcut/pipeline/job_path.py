# -*- coding: utf-8 -*-
"""Giai `--job` — MOT cach duy nhat cho ca pipeline.

Truoc 05/08/2026 co HAI khuon khac nhau, khong ai ghi ra giay:

    python3 4_anchor.py     --job 04-du-an/07-...   # 13 script: DUONG DAN
    python3 goi_y_broll.py  --job 07-...            # 5 script:  TEN TRAN

Dua nham la bao "thieu --job" hoac "khong thay thu muc job" — hai thong bao
deu khong he goi y rang minh dua sai DANG. Toi vap dung cho nay khi dung job
07 (05/08/2026), va `de_xuat_cat.py` thi docstring ghi mot dang con code doc
mot dang khac.

Gio moi script deu nhan CA BA dang:

    --job 04-du-an/07-2026-08-03-dji0485     duong dan tuong doi
    --job /duong/dan/tuyet/doi/07-...        duong dan tuyet doi
    --job 07-2026-08-03-dji0485              ten thu muc tran
    --job dji0485                            mot manh ten, mien la duy nhat
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DU_AN = os.path.join(ROOT, "04-du-an")


def job_dir(name, thoat=True):
    """Tra ve duong dan tuyet doi cua thu muc job. Khong thay thi thoat han
    voi thong bao noi ro da thu nhung dang nao."""
    if not name:
        if not thoat:
            return None
        sys.exit("thieu --job. Dua duong dan (04-du-an/<ten>) hoac ten job.")

    p = os.path.abspath(os.path.expanduser(name))
    if os.path.isdir(p):
        return p

    p = os.path.join(DU_AN, name)
    if os.path.isdir(p):
        return p

    try:
        hits = [d for d in sorted(os.listdir(DU_AN))
                if name.lower() in d.lower() and os.path.isdir(os.path.join(DU_AN, d))]
    except OSError:
        hits = []
    if len(hits) == 1:
        return os.path.join(DU_AN, hits[0])

    if not thoat:
        return None
    if len(hits) > 1:
        sys.exit(f"'{name}' khop {len(hits)} job, chua ro cai nao:\n  "
                 + "\n  ".join(hits))
    sys.exit(f"khong thay job '{name}'. Da thu:\n"
             f"  - duong dan  {os.path.abspath(os.path.expanduser(name))}\n"
             f"  - trong kho  {os.path.join(DU_AN, name)}\n"
             f"  - tim manh ten trong 04-du-an/ -> khong khop cai nao")
