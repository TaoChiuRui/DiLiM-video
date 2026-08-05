# -*- coding: utf-8 -*-
"""Soi `plan.json` bang MAY — bat nhung loi khong can nhin cung biet la sai.

    python3 soi_plan.py --job 04-du-an/<ten>
    python3 soi_plan.py --job 04-du-an/<ten> --md      # ghi edit/soi.md
    python3 soi_plan.py --all                          # soi ca 04-du-an/

RANH GIOI: file nay CHI bat loi KIEM DUOC BANG LUAT — caption qua ngan, dau *
le, clip dọc, clip lap, clip ngan hon caption, src_start dang de mac dinh.
No KHONG biet clip co dung y khong — muon biet thi phai NHIN frame, viec do
la cua agent `dilim-soat-broll`.

Nguong lay tu phan bo that cua 5 job dau (369 dong caption):
    do dai dong  p50=16  p90=22  p95=24  max=28   -> canh bao tu 26
    do dai caption p50=3.2s p90=6.2s max=9.1s     -> canh bao tu 8s
"""
import argparse
import glob
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clips as C   # noqa: E402

MIN_DUR, MAX_DUR = 0.80, 8.0
MAX_LINE = 26          # ky tu mot dong (khong tinh dau *)
COOLDOWN = 25.0        # clip lap lai trong khoang nay -> ngo
LONG_CLIP = 15.0       # clip dai hon nay ma src_start=0 -> ngo "dien cho co"
GAP_NO_BROLL = 12.0    # bao nhieu giay lien khong co B-roll thi ngo

_d = {}


def dur(p):
    if p.endswith(C.IMG_EXT):
        return 1e9
    if p not in _d:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", p],
                           capture_output=True, text=True)
        try:
            _d[p] = float(r.stdout.strip())
        except ValueError:
            _d[p] = 0.0
    return _d[p]


def soi(job):
    P = os.path.join(job, "edit/plan.json")
    if not os.path.exists(P):
        return None
    plan = json.load(open(P, encoding="utf-8"))
    loi, ngo = [], []

    def L(i, msg):
        loi.append((i, msg))

    def N(i, msg):
        ngo.append((i, msg))

    seen_txt = {}
    last_use = {}
    for r in plan:
        i, t = r["idx"], r["t"]
        d = r["t_end"] - r["t"]
        p = (r.get("path") or "").strip()

        # --- caption ---
        if d < MIN_DUR:
            L(i, f"caption chỉ {d:.2f}s (<{MIN_DUR}s) — gộp với dòng bên cạnh")
        elif d > MAX_DUR:
            N(i, f"caption {d:.1f}s — dài bất thường, chữ đứng im quá lâu")
        if r["text"].count("*") % 2:
            L(i, "dấu * lẻ — engine sẽ tô màu sai từ đó tới hết dòng")
        if not r.get("variant"):
            L(i, "thiếu variant — rơi vào vòng xoay màu ngẫu nhiên")
        for k, dd in (("dòng 1", r["d1"]), ("dòng 2", r["d2"])):
            n = len(dd.replace("*", ""))
            if n > MAX_LINE:
                N(i, f"{k} dài {n} ký tự (>{MAX_LINE}) — cỡ chữ sẽ bị thu nhỏ")
        key = r["text"].strip()
        if key and key in seen_txt:
            N(i, f"caption trùng hệt #{seen_txt[key]} — cân nhắc đổi chữ")
        seen_txt.setdefault(key, i)

        # --- clip ---
        if not p:
            continue
        if not os.path.exists(p):
            L(i, f"KHÔNG THẤY FILE {os.path.basename(p)}")
            continue
        if p in C.VERTICAL:
            L(i, f"{os.path.basename(p)} là clip DỌC — dải B-roll cần clip ngang")
        if p in C.WATERMARK:
            L(i, f"{os.path.basename(p)} CÓ WATERMARK ({C.WATERMARK[p]}) — "
                 f"video bán hàng không được dính")
        if not p.endswith(C.IMG_EXT):
            usable = dur(p) - r["src_start"]
            if usable < d - 0.03:
                L(i, f"clip còn {usable:.1f}s < caption {d:.1f}s — sẽ hụt hình")
            if r["src_start"] == 0 and dur(p) > LONG_CLIP:
                N(i, f"src_start=0 trên clip {dur(p):.0f}s — clip dài hay đổi "
                     f"cảnh giữa chừng, giây 0 thường không phải khoảnh khắc cần")
        prev = last_use.get(p)
        if prev is not None and t - prev < COOLDOWN:
            N(i, f"lặp {os.path.basename(p)} sau {t-prev:.0f}s (<{COOLDOWN:.0f}s) "
                 f"— chạy 4b_vary.py")
        last_use[p] = t

    # --- khoang trong dai khong co B-roll ---
    gap0 = None
    for r in plan:
        if r.get("path"):
            if gap0 is not None and r["t"] - gap0 >= GAP_NO_BROLL:
                ngo.append((r["idx"], f"trước dòng này có {r['t']-gap0:.0f}s "
                                      f"liền không B-roll"))
            gap0 = None
        elif gap0 is None:
            gap0 = r["t"]

    # --- VUNG CAM / MIN_START: src_start co dam vao doan co CHU khong? ------
    # THEM 04/08/2026. `clips.VUNG_CAM` ton tai tu truoc nhung comment ghi ro
    # "chua script nao doc no" — nen no chi la ghi chu cho nguoi. Chay thu tren
    # 7 job: 16 dong o 5 job dang dat src_start dam vao vung chu tieng Anh /
    # man den. Gio may kiem.
    try:
        import clips as _C
        _cam = {os.path.basename(k): v for k, v in getattr(_C, "VUNG_CAM", {}).items()}
        _min = {os.path.basename(k): v for k, v in getattr(_C, "MIN_START", {}).items()}
        # NGUON CHINH tu 05/08/2026: `kho_broll.json` — OCR + do sang toan kho,
        # 160 clip. Bang tay trong clips.py chi co 4 clip, giu lam du phong.
        _kb = os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "kho_broll.json")
        if os.path.exists(_kb):
            for _x in json.load(open(_kb, encoding="utf-8")):
                if _x.get("vung_cam"):
                    _cam[_x["file"]] = [tuple(v) for v in _x["vung_cam"]]
        for r in plan:
            p = (r.get("path") or "").strip()
            if not p:
                continue
            b = os.path.basename(p)
            ss = r.get("src_start", 0) or 0
            need = r["t_end"] - r["t"]
            for a, z in _cam.get(b, []):
                # dung sai 0.06s: cham dung bien (40+4.6 = 44.600000000000001
                # vs vung cam bat dau 44.6) khong tinh la dam vao
                if ss < z - 0.06 and ss + need > a + 0.06:
                    L(r["idx"], f"src_start {ss}–{ss+need:.1f}s của «{b}» "
                                f"đâm vào VÙNG CẤM {a}–{z}s (chữ/màn đen)")
            if b in _min and ss < _min[b]:
                L(r["idx"], f"src_start {ss} < MIN_START {_min[b]} của «{b}»")
    except Exception:
        pass

    # --- DISCLAIMER: chi kiem khi ANH DA NOI RA -----------------------------
    # SUA 04/08/2026 sau khi anh Thanh chan lai: "disclaimer them hay bo la do
    # toi, ke di, toi noi thi toi co them la duoc".
    #
    # Ban dau toi bat LOI moi khi caption thieu disclaimer — sai, vi do la
    # quyet dinh cua anh, khong phai luat cua may. Nhung co MOT truong hop van
    # phai bat: anh DA NOI trong video ma caption lai sot (dung cai da xay ra o
    # job 06 — tieng con du, chu bi thieu ve dau). Nen luat dung la:
    #     anh noi + caption thieu  -> LOI  (mat dong bo, loi cua toi)
    #     anh khong noi            -> im   (anh quyet)
    _noi = " ".join(r.get("said", "") for r in plan).lower()
    _tat = " ".join((r.get("d1", "") + " " + r.get("d2", ""))
                    for r in plan).lower().replace("*", "")
    for _k, _d in [("không phải là thuốc", "SẢN PHẨM NÀY KHÔNG PHẢI LÀ THUỐC"),
                   ("thay thế thuốc chữa bệnh", "THAY THẾ THUỐC CHỮA BỆNH")]:
        if _k in _noi and _k not in _tat:
            L(plan[-1]["idx"] if plan else 0,
              f"anh CÓ NÓI «{_d}» nhưng caption không có — lệch tiếng/chữ")

    # --- so tong ---
    n = len(plan)
    have = sum(1 for r in plan if r.get("path"))
    uniq = len({r["path"] for r in plan if r.get("path")})
    anchored = [r for r in plan if "anchor_score" in r]
    exact = sum(1 for r in anchored if r["anchor_score"] == 1.0)
    fuzzy = sum(1 for r in anchored if "gần đúng" in str(r.get("anchor_word", "")))
    fail = sum(1 for r in anchored if "KHONG NEO" in str(r.get("anchor_word", "")))
    for r in anchored:
        if "KHONG NEO" in str(r.get("anchor_word", "")):
            loi.append((r["idx"], "KHÔNG NEO ĐƯỢC — mốc còn là ước lượng"))
        elif "gần đúng" in str(r.get("anchor_word", "")):
            ngo.append((r["idx"], f"neo dò gần đúng vào «{r['anchor_word']}»"))

    return {"job": os.path.basename(job), "n": n, "have": have, "uniq": uniq,
            "anchored": len(anchored), "exact": exact, "fuzzy": fuzzy,
            "fail": fail, "loi": sorted(loi), "ngo": sorted(ngo),
            "duyet": os.path.exists(os.path.join(job, "edit/duyet.json"))}


def report(s):
    o = [f"## {s['job']}", ""]
    cov = 100 * s["have"] // max(s["n"], 1)
    o.append(f"- caption **{s['n']}** · có B-roll **{s['have']} ({cov}%)** · "
             f"clip khác nhau **{s['uniq']}**")
    if s["anchored"]:
        o.append(f"- neo: khớp hệt **{s['exact']}**/{s['anchored']} · "
                 f"dò gần đúng {s['fuzzy']} · không neo được {s['fail']}")
    else:
        o.append("- **chưa chạy 4_anchor.py** — mốc còn là ước lượng bằng mắt")
    o.append(f"- bản duyệt của anh Thành: "
             f"{'CÓ' if s['duyet'] else '**CHƯA CÓ** — chưa ai chấm'}")
    o.append(f"- máy soi: **{len(s['loi'])} lỗi · {len(s['ngo'])} chỗ ngờ**")
    for tag, lst in (("LỖI", s["loi"]), ("NGỜ", s["ngo"])):
        if lst:
            o.append(f"\n**{tag}**\n")
            for i, m in lst:
                o.append(f"- `#{i:>3}` {m}")
    return "\n".join(o) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job")
    ap.add_argument("--all", action="store_true", help="soi ca 04-du-an/")
    ap.add_argument("--md", action="store_true")
    a = ap.parse_args()

    root = os.path.abspath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../.."))
    if a.all:
        jobs = sorted(os.path.dirname(os.path.dirname(p))
                      for p in glob.glob(os.path.join(root, "04-du-an/*/edit/plan.json")))
    elif a.job:
        import job_path
        jobs = [job_path.job_dir(a.job)]
    else:
        sys.exit("can --job hoac --all")

    out = []
    for j in jobs:
        s = soi(j)
        if s is None:
            print(f"(bo qua {os.path.basename(j)} — chua co plan.json)")
            continue
        txt = report(s)
        out.append(txt)
        if a.md and a.job:
            f = os.path.join(j, "edit/soi.md")
            open(f, "w", encoding="utf-8").write(f"# Máy soi\n\n{txt}")
            print(f"-> {f}")
    if not (a.md and a.job):
        print("\n".join(out))


if __name__ == "__main__":
    main()
