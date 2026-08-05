# -*- coding: utf-8 -*-
"""Catalog + tra cuu B-roll cho pipeline DiLiM (thay the viec ls/grep tay tung
thu muc). Quet cac nguon footage co san (KHONG di chuyen/sua file goc, chi doc
va ghi 1 file catalog JSON o day).

Usage:
    python catalog.py build
    python catalog.py search "<tu khoa>" [--pool ...] [--limit N]
    python catalog.py stats
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from paths import BROLL_ROOT as ROOT_BROLL  # noqa: E402  (doc tu config.json o goc goi)

# priority thap hon = uu tien tim/hien truoc (Da Chuan Hoa la kho nguoi dung tu
# dat ten theo y, LUON tim o day truoc theo nguyen tac da chot)
#
# 2026-08-03 — chuyen sang MacBook, kho o "/Volumes/T7 for Mac/02. Dilim Footage".
# Kho tren o Mac KHONG giong kho Windows cu:
#   - 5 thu muc doi ten, them so o dau: "01 Dau dau...", "02 Mach Mau...",
#     "04 Dot quy", "06 Ngu- Ngon- mat ngu"  (da sua ben duoi)
#   - Them 4 pool moi: 03 Rich_Natto_product, Natto Xam, Khung hinh chuyen gia,
#     05 Finish part. (Hai thu muc "Am Thanh" = SFX va "Nhac video quang cao"
#     = nhac nen KHONG them vao day: catalog chi index anh/video, khong index
#     mp3/wav. Nhac tro qua music_root trong config.json.)
#   - THIEU 9 pool, trong do co 2 pool quan trong nhat: "Đã Chuẩn Hóa" (priority 0)
#     va "Product Broll". Chua chep sang o Mac. Giu khai bao o day vi build() tu
#     bo qua root khong ton tai — chep sang la chay duoc ngay, khong phai sua code.
SOURCES = [
    # --- CHUA CO tren o Mac (build() se bao "CANH BAO ... bo qua") ---
    {"pool": "da_chuan_hoa", "root": ROOT_BROLL / "Đã Chuẩn Hóa", "priority": 0,
     "flat": True, "note": "Kho tu dat ten theo Y, uu tien tim truoc tien"},
    {"pool": "product_broll", "root": ROOT_BROLL / "Product Broll", "priority": 1,
     "flat": False, "note": "Anh/video san pham that - dung khi caption nhac ten san pham"},
    {"pool": "cta", "root": ROOT_BROLL / "CTA", "priority": 3, "flat": False, "note": "Chi dung cho doan CTA/ket"},

    # --- Co tren o Mac ---
    {"pool": "footage_dilim_quay", "root": ROOT_BROLL / "Footage Dilim Quay", "priority": 2,
     "flat": False, "note": "Footage nguoi that DiLiM tu quay"},
    {"pool": "rich_natto_product", "root": ROOT_BROLL / "03 Rich_Natto_product", "priority": 1,
     "flat": True, "note": "Anh/video san pham Rich Natto - thay cho Product Broll tren o Mac"},
    {"pool": "natto_xam", "root": ROOT_BROLL / "Natto Xám", "priority": 1,
     "flat": True, "note": "Anh san pham Natto Xam + men gao do"},
    {"pool": "khung_chuyen_gia", "root": ROOT_BROLL / "Khung hình chuyên gia", "priority": 2,
     "flat": True, "note": "Khung PNG long nguoi noi (GREEN/TRANG/DEN/be)"},
    {"pool": "finish_part", "root": ROOT_BROLL / "05 Finish part", "priority": 3,
     "flat": True, "note": "Doan ket: disclaimer 'SP nay k phai la thuoc' + logo DiLiM"},
    {"pool": "mach_mau_than_kinh", "root": ROOT_BROLL / "02 Mạch Máu - Thần Kinh - TẾ BÀO", "priority": 1, "flat": False},
    {"pool": "dau_dau_chong_mat", "root": ROOT_BROLL / "01 Đau đầu - Chóng mặt - Mệt mõi - Bệnh", "priority": 1, "flat": False},
    {"pool": "dot_quy", "root": ROOT_BROLL / "04 Đột quỵ", "priority": 1, "flat": False},
    {"pool": "xuong_khop", "root": ROOT_BROLL / "Xương khớp - Đau", "priority": 1, "flat": False},
    {"pool": "ngu_mat_ngu", "root": ROOT_BROLL / "06 Ngủ- Ngon- mất ngủ", "priority": 1, "flat": False},
    {"pool": "dau_bung_tieu_hoa", "root": ROOT_BROLL / "Đau Bụng - Tiêu hóa", "priority": 1, "flat": False},
    {"pool": "noi_tang", "root": ROOT_BROLL / "NỘI TẠNG", "priority": 1, "flat": False},
    {"pool": "toc_da_lam_dep", "root": ROOT_BROLL / "TÓC- DA- LÀM ĐẸP", "priority": 1, "flat": False},
    {"pool": "giam_can", "root": ROOT_BROLL / "Giảm cân - Mập, tăng cân", "priority": 1, "flat": False},
    {"pool": "ho_kho_tho", "root": ROOT_BROLL / "Ho - Khó Thở", "priority": 1, "flat": False},
    {"pool": "kham_benh", "root": ROOT_BROLL / "Khám bệnh - Bác Sĩ - uống Thuốc- bệnh khác", "priority": 1, "flat": False},
    {"pool": "nghien_dien_thoai", "root": ROOT_BROLL / "Nghiện Điện Thoại MXH", "priority": 1, "flat": False},
    {"pool": "nhan_vien_van_phong", "root": ROOT_BROLL / "Nhân Viên văn phòng", "priority": 1, "flat": False},
    {"pool": "the_duc_the_thao", "root": ROOT_BROLL / "Thể dục thể thao", "priority": 1, "flat": False},
    {"pool": "thien_doc_sach", "root": ROOT_BROLL / "Thiền - Đọc sách", "priority": 1, "flat": False},
    {"pool": "an_uong_lanh_manh", "root": ROOT_BROLL / "Ăn uống lành mạnh", "priority": 1, "flat": False},
    {"pool": "do_an_an_uong", "root": ROOT_BROLL / "Đồ ăn - Ăn uống", "priority": 1, "flat": False},
    {"pool": "gia_dinh", "root": ROOT_BROLL / "Gia đình - Vui vẻ- Cãi vã", "priority": 1, "flat": False},
    {"pool": "hau_vo_chong", "root": ROOT_BROLL / "Hàu- Vợ chồng", "priority": 1, "flat": False},
    {"pool": "bia_ruou", "root": ROOT_BROLL / "Bia Rượu - Nhậu", "priority": 1, "flat": False},
    {"pool": "ai", "root": ROOT_BROLL / "AI", "priority": 2, "flat": False},
    {"pool": "lon_xon_xa_ban", "root": ROOT_BROLL / "Lộn Xộn Xà bần", "priority": 4,
     "flat": True, "note": "Kho du/chua phan loai - chi tim khi cac pool khac khong co"},
]

IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".jfif"}
VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".m4v", ".avi"}

CATALOG_PATH = Path(__file__).resolve().parent / "broll_catalog.json"

# Dong nghia/mo rong tu khoa hay gap - mo rong dan qua thuc te dung, khong can
# day du. Ca 2 chieu deu normalize() khi so sanh.
SYNONYMS: dict[str, list[str]] = {
    "dau dau": ["headache", "nhuc dau"],
    "vai gay": ["dau vai", "dau co"],
    "mat ngu": ["kho ngu", "ngu khong sau giac", "thieu ngu"],
    "chong mat": ["choang vang", "hoa mat"],
    "te bi chan tay": ["te bi", "te tay", "te chan"],
    "roi loan tien dinh": ["tien dinh"],
    "hay quen": ["tri nho kem", "quen"],
    "dot quy": ["stroke", "tai bien"],
    "xuong khop": ["dau khop", "khop goi", "thoai hoa khop"],
    "gan": ["liver"],
    "than": ["kidney"],
    "tim mach": ["heart"],
    "cang thang": ["stress", "ap luc"],
    "met moi": ["ue oai", "kiet suc"],
    "beo phi": ["tang can", "map"],
    "tieu duong": ["duong huyet"],
    "rich coenzyme q10": ["rich q10", "coenzyme q10", "q10"],
    "dha epa": ["dha", "epa"],
    "nattokinase": ["natto"],
    "collagen": ["collagen thuy phan"],
}


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("đ", "d").replace("Đ", "D")
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def build() -> dict:
    items = []
    for src in SOURCES:
        root = Path(src["root"])
        if not root.is_dir():
            print(f"CANH BAO: khong tim thay {root}, bo qua pool {src['pool']}")
            continue
        count = 0
        for f in root.rglob("*"):
            if not f.is_file():
                continue
            ext = f.suffix.lower()
            if ext not in IMG_EXT and ext not in VIDEO_EXT:
                continue
            rel = f.relative_to(root)
            if src["flat"]:
                category = "(root)"
            else:
                category = rel.parts[0] if len(rel.parts) > 1 else "(root)"
            stem = f.stem
            match_text = f"{category if category != '(root)' else ''} {stem}"
            items.append(
                {
                    "path": str(f),
                    "pool": src["pool"],
                    "priority": src["priority"],
                    "category": category,
                    "filename": f.name,
                    "match_norm": normalize(match_text),
                    "type": "video" if ext in VIDEO_EXT else "image",
                    "size": f.stat().st_size,
                }
            )
            count += 1
        print(f"{src['pool']}: {count} file")

    catalog = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "sources": [{"pool": s["pool"], "root": str(s["root"]), "priority": s["priority"]} for s in SOURCES],
        "items": items,
    }
    CATALOG_PATH.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDa ghi catalog: {CATALOG_PATH} ({len(items)} file)")
    return catalog


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        raise SystemExit(f"Chua co catalog - chay 'python catalog.py build' truoc. ({CATALOG_PATH})")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def _word_boundary_in(needle: str, haystack: str) -> bool:
    if not needle:
        return False
    return re.search(rf"(?<![a-z0-9]){re.escape(needle)}(?![a-z0-9])", haystack) is not None


def search(query: str, pool: str | None = None, limit: int = 20) -> list[dict]:
    catalog = load_catalog()
    q = normalize(query)
    q_expanded = {q} | set(SYNONYMS.get(q, []))
    for key, vals in SYNONYMS.items():
        if _word_boundary_in(key, q):
            q_expanded.update(vals)

    scored = []
    for item in catalog["items"]:
        if pool and item["pool"] != pool:
            continue
        m = item["match_norm"]
        # CHI dung word-boundary match (bug that gap 2026-07-23: "term in m" la
        # substring tho, cho phep khop xuyen qua ranh gioi tu - VD tim "o to"
        # (tu "o tô") lai khop nham vao "...mo TOt trong mau..." vi chuoi "o to"
        # nam vat ngang giua chu "mo" va "tot". Bo han nhanh substring, chi giu
        # _word_boundary_in (co kiem tra ky tu truoc/sau khong phai chu/so).
        hit = any(_word_boundary_in(term, m) for term in q_expanded if term)
        if hit:
            scored.append(item)

    scored.sort(key=lambda it: (it["priority"], it["pool"], it["filename"]))
    return scored[:limit]


def cmd_build(_args):
    build()


def cmd_search(args):
    results = search(args.query, pool=args.pool, limit=args.limit)
    if not results:
        print(f'Khong tim thay ket qua nao cho "{args.query}"' + (f" (pool={args.pool})" if args.pool else ""))
        return
    print(f'Tim thay {len(results)} ket qua cho "{args.query}":')
    for item in results:
        print(f"  [{item['pool']}] ({item['type']}) {item['path']}")


def cmd_stats(_args):
    catalog = load_catalog()
    print(f"Catalog tao luc: {catalog['generated_at']}")
    print(f"Tong so file: {len(catalog['items'])}\n")
    by_pool: dict[str, int] = {}
    for item in catalog["items"]:
        by_pool[item["pool"]] = by_pool.get(item["pool"], 0) + 1
    for pool, n in sorted(by_pool.items()):
        print(f"  {pool}: {n} file")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build", help="Quet lai cac pool, ghi de catalog")
    p_build.set_defaults(func=cmd_build)

    p_search = sub.add_parser("search", help="Tim broll theo tu khoa")
    p_search.add_argument("query")
    p_search.add_argument("--pool", default=None)
    p_search.add_argument("--limit", type=int, default=20)
    p_search.set_defaults(func=cmd_search)

    p_stats = sub.add_parser("stats", help="Thong ke nhanh catalog da co")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
