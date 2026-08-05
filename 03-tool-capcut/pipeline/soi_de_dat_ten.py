# -*- coding: utf-8 -*-
"""Dung contact sheet de DAT TEN cho mot folder kho — buoc chuan bi cua doi_ten.py

    python3 soi_de_dat_ten.py --folder "Xương khớp - Đau"

Ra:
    <scratch>/<slug>_full.json   ban ke: ten, kich thuoc, thoi luong, ngang/doc
    <scratch>/<SLUG>1.jpg ...    contact sheet 5x8, MOI o co nhan chi so

Vi sao co script nay (05/08/2026): dat ten 15 folder con lai thi lap y het nhau
6 buoc moi lan. Ba cai bay da vap khi lam tay, nay go san:

  1. `pad` sau `scale` bao "Padded dimensions cannot be smaller" vi lam tron
     le (1080/1920*300 = 168.75). Bo pad, de PIL can le.
  2. File ANH khong ra frame bang ffmpeg -ss -> phai lui ve PIL.
  3. Nhan so ve bang ffmpeg drawtext thi ANH khong co nhan -> dem theo vi tri
     bi LECH, dat nham ten file. Nay VE NHAN BANG PIL cho MOI o.

Ky hieu tren nhan:  `K` = clip da khai trong clips.py   ·   `D` = clip doc
"""
import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata as ud

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clips as C                                                  # noqa: E402

SCRATCH = os.environ.get(
    "DILIM_SCRATCH",
    "/private/tmp/claude-501/-Users-thanh-Desktop-DiLiM-video/"
    "d06be506-f9b2-4a76-abc6-50d4e0dba61f/scratchpad")
N = lambda s: ud.normalize("NFC", s)          # noqa: E731  — o T7 tra NFD
W, H, COLS, ROWS = 300, 169, 5, 8


def slug(s):
    s = ud.normalize("NFD", s)
    s = "".join(c for c in s if not ud.combining(c))
    return re.sub(r"[^A-Za-z0-9]+", "", s)[:12] or "kho"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=True, help="ten thu muc trong kho")
    a = ap.parse_args()

    F = os.path.join(C.B, a.folder)
    if not os.path.isdir(F):
        # o T7 tra NFD, tham so go tay thuong la NFC -> do lai bang so khop chuan hoa
        hits = [d for d in os.listdir(C.B) if N(d) == N(a.folder)]
        if not hits:
            sys.exit(f"khong thay folder: {a.folder}")
        F = os.path.join(C.B, hits[0])

    khai = {N(os.path.basename(v)) for k, v in vars(C).items()
            if k.isupper() and isinstance(v, str) and v.startswith(C.B)}

    rows = []
    for f in sorted(os.listdir(F)):
        p = os.path.join(F, f)
        if f.startswith(".") or not os.path.isfile(p):
            continue
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height", "-show_entries", "format=duration",
             "-of", "json", p], capture_output=True, text=True)
        try:
            d = json.loads(r.stdout); st = d["streams"][0]
            w, h = st["width"], st["height"]
            dur = float(d["format"].get("duration", 0) or 0)
        except Exception:
            w = h = 0; dur = 0.0
        rows.append({"f": f, "w": w, "h": h, "dur": dur, "doc": h > w})

    sl = slug(a.folder)
    os.makedirs(SCRATCH, exist_ok=True)
    json.dump(rows, open(f"{SCRATCH}/{sl}_full.json", "w"), ensure_ascii=False)

    d = f"{SCRATCH}/fr_{sl}"
    os.system(f"rm -rf '{d}'"); os.makedirs(d)
    hong = []
    for i, r in enumerate(rows):
        out = f"{d}/{i:03d}.jpg"
        ss = max(0.3, (r["dur"] or 2) * 0.35)
        rr = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", str(ss), "-i", os.path.join(F, r["f"]),
             "-frames:v", "1", "-vf", "scale=300:-1", "-y", out], capture_output=True)
        if rr.returncode or not os.path.exists(out):
            try:                                   # file ANH: ffmpeg -ss truot
                im = Image.open(os.path.join(F, r["f"])).convert("RGB")
                im.thumbnail((W, H)); im.save(out)
            except Exception:
                hong.append(i)

    idxs = sorted(int(x[:3]) for x in os.listdir(d) if x.endswith(".jpg"))
    per = COLS * ROWS
    for p in range((len(idxs) + per - 1) // per):
        ch = idxs[p * per:(p + 1) * per]
        sh = Image.new("RGB", (COLS * W, ((len(ch) + COLS - 1) // COLS) * H), (28, 28, 28))
        dr = ImageDraw.Draw(sh)
        for j, i in enumerate(ch):
            im = Image.open(f"{d}/{i:03d}.jpg").convert("RGB"); im.thumbnail((W, H))
            x, y = (j % COLS) * W, (j // COLS) * H
            sh.paste(im, (x + (W - im.width) // 2, y + (H - im.height) // 2))
            lab = str(i) + (" K" if N(rows[i]["f"]) in khai else "") + (" D" if rows[i]["doc"] else "")
            dr.rectangle([x + 2, y + 2, x + 8 + len(lab) * 11, y + 22], fill=(0, 0, 0))
            dr.text((x + 5, y + 5), lab, fill=(255, 235, 0))
        sh.save(f"{SCRATCH}/{sl.upper()}{p+1}.jpg", quality=80)
        print(f"  -> {SCRATCH}/{sl.upper()}{p+1}.jpg   ({ch[0]}..{ch[-1]})")

    print(f"\n  {len(rows)} file · {len(idxs)} frame"
          + (f" · KHONG DOC DUOC: {hong} -> {[rows[i]['f'] for i in hong]}" if hong else " · doc het"))
    print(f"  ban ke: {SCRATCH}/{sl}_full.json")


if __name__ == "__main__":
    main()
