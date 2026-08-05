# -*- coding: utf-8 -*-
"""BANG TRA Y -> B-ROLL DA DUOC DUYET (chu de XUONG KHOP / SUN NANO PREMIUM).

Lay NGUYEN VAN tu ban ke hoach cuoi cung cua video "Sun khop khong dau khi dang
mon" (jobs/qc_sun_mon/broll_plan.json) - la ban nguoi dung da sua va chot.
Nguoi dung chot 2026-07-29: y nao giong ~90% thi dung ngay clip nay, ca file
LAN giay bat dau, khong tu di tim clip khac.

Moi muc: (khoa nhan dien, clip, src_start, ghi chu)
  - "moi" = tat ca tu phai xuat hien
  - "hoac" = chi can 1 nhom trong danh sach khop
Tra cuu: pick(caption_text) -> (path, src_start) hoac (None, None)
"""
from __future__ import annotations

import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "jobs", "qc_sun_b2"))
from clips import (  # noqa: E402
    x, f, NANO, GEL, GMP, FACTORY, COMBO, CTA, BUB, NANOTECH, MOL91,
    KHOP_MODEL, SUN_TACH, KHOP_VIEM, DAY_TK, CT_PHA_HUY, KHOP_MON_VANG,
    KHOP_HANG, XOAN_OC, DAU_DEM, DAU_CHAY_BO, DAU_GHE_DA, DAU_CONG_VIEN,
    DAU_GIUONG, XOA_GOI, TAY_LEN_GOI, GOI_DO, GAY_DUNG_DAY, LEO_THANG,
    TAP_PHUC_HOI, BS_KHAM_GOI, CHAY_BO_2NGUOI, DI_BO_BIEN, CU_ONG_CHAY,
    BUOC_THANG_GO, GIA_DINH,
)

# (danh sach nhom tu khoa, path, src_start)
# Mot nhom khop khi MOI tu trong nhom deu co mat trong caption.
MAP = [
    (["sun khop khong dau"], KHOP_MODEL, 2.0),
    (["cau tao khop"], KHOP_MODEL, 2.0),
    (["dang mon"], SUN_TACH, 1.2),
    (["mon tung ngay"], SUN_TACH, 1.2),
    (["khong he biet"], SUN_TACH, 1.2),
    (["khong biet"], SUN_TACH, 1.2),
    (["giai thich"], BS_KHAM_GOI, 4.0),
    (["khong muon hieu"], BS_KHAM_GOI, 4.0),
    (["day than kinh"], DAY_TK, 0.5),
    (["hao mon"], KHOP_VIEM, 2.0),
    (["ton thuong"], KHOP_VIEM, 2.0),
    (["viem"], KHOP_VIEM, 2.0),
    (["khong bao truoc"], CT_PHA_HUY, 5.0),
    (["pha huy"], CT_PHA_HUY, 5.0),
    (["dau ro"], TAY_LEN_GOI, 5.0),
    (["cung khop"], TAY_LEN_GOI, 5.0),
    (["buoi sang"], TAY_LEN_GOI, 5.0),
    (["leo cau thang"], LEO_THANG, 1.5),
    (["cau thang"], LEO_THANG, 1.5),
    (["dung len"], GAY_DUNG_DAY, 14.0),
    (["mon dang ke"], KHOP_MON_VANG, 0.5),
    (["am tham"], DAU_DEM, 1.0),
    (["khong trieu chung"], DAU_DEM, 1.0),
    (["nam truoc do"], DAU_DEM, 1.0),
    (["phat len"], DAU_CHAY_BO, 5.0),
    (["muoi may nam"], DAU_CHAY_BO, 5.0),
    (["tai tao", "nam"], TAP_PHUC_HOI, 1.0),
    (["thang", "tuan"], TAP_PHUC_HOI, 1.0),
    (["se tai tao"], KHOP_HANG, 0.2),
    (["nguon nguyen lieu"], KHOP_HANG, 0.2),
    (["nguyen lieu"], KHOP_HANG, 0.2),
    (["sun nano premium"], NANO, 10.6),
    (["nano premium"], NANO, 10.6),
    (["6 duong chat"], NANO, 10.6),
    (["nano hoa"], NANOTECH, 0.5),
    (["phan tu"], MOL91, 1.0),
    (["nanomet"], MOL91, 1.0),
    (["hap thu", "lan"], NANO, 30.9),
    (["hap thu", "80"], NANO, 30.9),
    (["nhat ban"], FACTORY, 0.0),
    (["gmp"], GMP, 0.0),
    (["gmp", "nhat ban"], GMP, 0.0),
    (["chuan", "gmp"], GMP, 0.0),
    (["san xuat", "nhat ban"], FACTORY, 0.0),
    (["khat khe"], GMP, 0.0),
    (["bao ve xuong khop"], CHAY_BO_2NGUOI, 8.0),
    (["truoc khi dau"], DI_BO_BIEN, 3.0),
    (["dau nhe"], DAU_GHE_DA, 1.0),
    (["keu nhe"], DAU_CONG_VIEN, 4.0),
    (["thoi diem thich hop"], DAU_CONG_VIEN, 4.0),
    (["dang dau khop"], DAU_GIUONG, 3.0),
    (["gluchongel"], GEL, 0.3),
    (["gel glucosamine"], GEL, 8.6),
    (["de ngua"], GEL, 8.6),
    (["que"], GEL, 8.6),
    (["khang viem"], GOI_DO, 5.0),
    (["giam dau"], GOI_DO, 5.0),
    (["mem ra"], XOA_GOI, 2.0),
    (["diu lai"], XOA_GOI, 2.0),
    (["bot dau nhuc"], XOA_GOI, 2.0),
    (["tham vao trong"], GEL, 16.0),
    (["dau nong"], GEL, 1.5),
    (["kho chiu"], GEL, 1.5),
    (["mat", "em"], GEL, 1.5),
    (["boi tu ngoai"], GEL, 1.5),
    (["phuc hoi", "tu trong"], NANO, 15.3),
    (["moi phuc hoi duoc"], XOAN_OC, 0.4),
    (["thoai mai", "nhe nhang"], CU_ONG_CHAY, 8.0),
    (["di dung de hon"], BUOC_THANG_GO, 1.0),
    (["cong viec tot hon"], BUOC_THANG_GO, 1.0),
    (["thuan loi hon"], GIA_DINH, 5.0),
    (["chinh hang"], COMBO, 0.0),
    (["dilim supplement"], COMBO, 0.0),
    (["so dien thoai"], CTA, 2.0),
    (["hotline"], CTA, 2.0),
    # 6 bubble thanh phan - khop chinh xac ten
    (["hyaluronic"], BUB["ha"], 5.0),
    (["chondroitin"], BUB["chondroitin"], 5.0),
    (["collagen type 2"], BUB["collagen2"], 5.0),
    (["glucosamine"], BUB["glucosamine"], 5.0),
    (["msm"], BUB["msm"], 5.0),
    (["canxi", "d3"], BUB["canxi"], 5.0),
    (["calcium", "d3"], BUB["canxi"], 5.0),
]


def _n(s: str) -> str:
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").replace("đ", "d")
    return " " + re.sub(r"[^a-z0-9]+", " ", s).strip() + " "


def pick(caption: str):
    """Tra 1 caption -> (path, src_start). Nhom nao DAI hon (nhieu tu hon,
    chuoi dai hon) duoc uu tien vi cu the hon."""
    t = _n(caption)
    best = None
    for keys, path, ss in MAP:
        if all(f" {_n(k).strip()} " in t for k in keys):
            w = sum(len(k) for k in keys)
            if best is None or w > best[0]:
                best = (w, path, ss)
    return (best[1], best[2]) if best else (None, None)


if __name__ == "__main__":
    print(f"{len(MAP)} muc trong bang tra")
    for s in sys.argv[1:]:
        p, ss = pick(s)
        print(f"  {s[:50]:<52} -> {os.path.basename(p) if p else '(khong co)'} @{ss}")
