# -*- coding: utf-8 -*-
"""Goi y B-roll cho tung caption — tra bang tu khoa trong clips.TAGS.

    python3 suggest_clips.py --job 04-du-an/<ten>            # in ra man hinh
    python3 suggest_clips.py --job 04-du-an/<ten> --md       # ghi edit/goi_y_clip.md
    python3 suggest_clips.py --text "mach mau bi hep lai"    # tra le mot cau

VI SAO CO BUOC NAY: truoc day moi lan can clip la phai LUC KHO 1.102 file tren
o T7 — vua cham vua ton, va van sot (12 clip mach mau bi bo qua ngay 03/08 chi
vi ten file la tieng Anh). Bang TAGS tra ra trong mot giay, va moi lan phai tu
tay di tim mot clip thi THEM TU KHOA VAO clips.TAGS — lan sau may tra ra.

MAY CHI GOI Y. Bon cau hoi o buoc 4 cua skill dilim-video-broll van phai tu
tra loi: dung canh minh hinh dung khong · khong khi co khop khong · da xem
dung frame se dung chua · diem chen co trung chu duoc noi khong.

Luat da cai san:
  - bo clip DOC (clips.VERTICAL) — dai B-roll can clip NGANG
  - bo clip NGAN hon caption (tinh ca clips.MIN_START)
  - ha diem clip vua dung trong vong COOLDOWN giay (luat chong lap 04/08)
"""
import argparse
import json
import os
import subprocess
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clips as C   # noqa: E402

COOLDOWN = 25.0     # giay — clip vua dung trong khoang nay bi ha diem
TOP = 3

_dur = {}


def dur(p):
    if p.endswith(C.IMG_EXT):
        return 1e9
    if p not in _dur:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", p],
                           capture_output=True, text=True)
        try:
            _dur[p] = float(r.stdout.strip())
        except ValueError:
            _dur[p] = 0.0
    return _dur[p]


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " " + " ".join(s.replace("đ", "d").replace("*", " ").split()) + " "


NAME = {v: k for k, v in vars(C).items()
        if k.isupper() and isinstance(v, str) and v.startswith("/Volumes")}


def score(text, need=0.0, used=None, t=0.0):
    """-> [(diem, path, ten, ghi_chu)] sap giam dan."""
    n = norm(text)
    out = []
    for path, tags in C.TAGS.items():
        if path in C.VERTICAL:
            continue
        sc = 0
        for tag in tags:
            if norm(tag).strip() in n:
                sc += len(tag.split()) ** 2
        if not sc:
            continue
        note = []
        if not os.path.exists(path):
            note.append("MAT FILE")
            sc = 0
        else:
            usable = dur(path) - C.MIN_START.get(path, 0)
            if need and usable < need - 0.03:
                note.append(f"ngan {usable:.1f}s<{need:.1f}s")
                sc *= 0.25
        if used and path in used:
            gap = min(abs(t - u) for u in used[path])
            if gap < COOLDOWN:
                note.append(f"da dung cach {gap:.0f}s")
                sc *= 0.4
        out.append((sc, path, NAME.get(path, "?"), " · ".join(note)))
    out.sort(key=lambda x: -x[0])
    return [o for o in out if o[0] > 0][:TOP]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job")
    ap.add_argument("--text", help="tra le mot cau, khong can job")
    ap.add_argument("--md", action="store_true", help="ghi edit/goi_y_clip.md")
    ap.add_argument("--all", action="store_true",
                    help="goi y ca nhung dong DA co clip")
    a = ap.parse_args()

    if a.text:
        for sc, p, name, note in score(a.text):
            d = dur(p)
            ds = "anh" if d > 1e8 else f"{d:.1f}s"
            print(f"  {sc:5.1f}  {name:12} {ds:>6}  {os.path.basename(p)}"
                  + (f"   [{note}]" if note else ""))
        return

    if not a.job:
        sys.exit("can --job hoac --text")
    import job_path
    job = job_path.job_dir(a.job)
    plan = json.load(open(os.path.join(job, "edit/plan.json"), encoding="utf-8"))

    used = {}
    for r in plan:
        if r.get("path"):
            used.setdefault(r["path"], []).append(r["t"])
    lines, n_ask = [], 0
    for r in plan:
        if r.get("path") and not a.all:
            continue
        n_ask += 1
        need = r["t_end"] - r["t"]
        cands = score(r["text"], need, used, r["t"])
        cap = r["text"].replace("\n", " / ")
        lines.append(f"\n#{r['idx']:3}  {r['t']:7.2f}s  ({need:.1f}s)  {cap}")
        lines.append(f"      nói: {r['said'][:70]}")
        if not cands:
            lines.append("      — KHONG TRA RA GI. Tu tim tren o T7, tim xong "
                         "them tu khoa vao clips.TAGS.")
        for sc, p, name, note in cands:
            d = dur(p)
            ds = "ảnh" if d > 1e8 else f"{d:.1f}s"
            lines.append(f"      {sc:5.1f}  {name:12} {ds:>6}  "
                         f"{os.path.basename(p)[:44]}"
                         + (f"   [{note}]" if note else ""))

    head = (f"# Gợi ý clip — {os.path.basename(job)}\n\n"
            f"{n_ask}/{len(plan)} caption cần clip. Điểm cao = khớp nhiều từ "
            f"khoá hơn, KHÔNG có nghĩa là đúng ý.\n"
            f"Cột giây là độ dài clip; `[ngắn]` = không đủ phủ caption.\n"
            f"Điền tên hằng (cột 2) vào `plan.py`. Không có gì khớp thật thì "
            f"để `\"\"`.\n")
    body = head + "```" + "".join(l + "\n" for l in lines) + "```\n"

    if a.md:
        out = os.path.join(job, "edit/goi_y_clip.md")
        open(out, "w", encoding="utf-8").write(body)
        print(f"{n_ask}/{len(plan)} caption can clip")
        print(f"-> {out}  ({os.path.getsize(out)/1024:.0f} KB)")
    else:
        print(body)


if __name__ == "__main__":
    main()
