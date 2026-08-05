# -*- coding: utf-8 -*-
"""Soi MOT THU MUC KHO tho tren o T7 — moi clip 3 frame, ghep contact sheet.

    python3 soi_kho.py --folder "04 Đột quỵ"
    python3 soi_kho.py --folder "02 Mạch Máu - Thần Kinh - TẾ BÀO" --lo 1
    python3 soi_kho.py --folder "06 Ngủ- Ngon- mất ngủ" --chua-khai

KHAC `soi_frames.py`: cai kia soi mot BAN DUNG da co plan (biet truoc lay giay
nao). Cai nay soi KHO THO — chua biet clip la gi, can nhin de DAT TEN.

VI SAO 3 FRAME: mot frame khong du de biet clip dien ta gi. Lay o 15% / 45% /
75% de thay dien bien. Frame dau clip hay la chu/logo nen bo qua 15% dau.

Ra `05-footage-moi/soi_kho/<folder>/lo_01.png ...` — moi tam 4 clip.
Kem `lo_01.txt` liet ke so hieu -> ten file, de doi chieu khi dat ten.
"""
import argparse
import io
import json
import os
import subprocess
import sys
import unicodedata

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clips as C   # noqa: E402

VID_EXT = (".mp4", ".mov", ".m4v", ".webm")
FRAMES = (0.15, 0.45, 0.75)     # vi tri trich, theo ti le do dai
CLIPS_PER_SHEET = 4
CELL_W = 420
LABEL_H = 46
PAD = 8
BG = (18, 20, 24)
FG = (235, 235, 235)
DIM = (150, 158, 168)
HOT = (120, 220, 150)           # clip da khai trong clips.py

OUT_ROOT = os.path.join(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))), "05-footage-moi", "soi_kho")

FONT_PATHS = ["/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
              "/Library/Fonts/Arial Unicode.ttf",
              "/System/Library/Fonts/Helvetica.ttc"]


def font(sz):
    for p in FONT_PATHS:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, sz)
            except OSError:
                pass
    return ImageFont.load_default()


def N(s):
    """Chuan hoa NFC — o T7 tra ve NFD, plan.py ghi NFC. Khong chuan hoa thi
    cung mot file dem thanh hai."""
    return unicodedata.normalize("NFC", s)


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height,duration",
                        "-of", "csv=p=0", path], capture_output=True, text=True)
    try:
        w, h, d = r.stdout.strip().split(",")[:3]
        return int(w), int(h), float(d)
    except ValueError:
        return 0, 0, 0.0


def grab(path, ss, w):
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss),
                        "-i", path, "-frames:v", "1", "-vf", f"scale={w}:-1",
                        "-f", "image2", "-c:v", "mjpeg", "-"],
                       capture_output=True)
    if r.returncode or not r.stdout:
        return None
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")


def declared():
    """{duong_dan_NFC: TEN_HANG_SO} — clip da co ten trong clips.py."""
    out = {}
    for k, v in vars(C).items():
        if k.isupper() and isinstance(v, str) and v.startswith("/Volumes"):
            out[N(v)] = k
    return out


def used_counts():
    """{duong_dan_NFC: so_lan_dung} — dem qua moi plan.py / plan.json."""
    root = os.path.join(os.path.dirname(OUT_ROOT), "..", "04-du-an")
    root = os.path.abspath(os.path.join(os.path.dirname(OUT_ROOT), "..",
                                        "04-du-an"))
    cnt = {}
    if not os.path.isdir(root):
        return cnt
    for job in os.listdir(root):
        for rel in ("plan.py", "edit/plan.json"):
            f = os.path.join(root, job, rel)
            if not os.path.isfile(f):
                continue
            try:
                txt = open(f, encoding="utf-8").read()
            except OSError:
                continue
            for chunk in txt.split('"')[1::2]:
                if chunk.startswith("/Volumes/T7"):
                    k = N(chunk)
                    cnt[k] = cnt.get(k, 0) + 1
    return cnt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--folder", required=True,
                    help='ten thu muc trong "02. Dilim Footage"')
    ap.add_argument("--lo", type=int, help="chi lam mot lo (1,2,3...)")
    ap.add_argument("--chua-khai", action="store_true",
                    help="bo qua clip da khai trong clips.py")
    a = ap.parse_args()

    src = os.path.join(C.B, a.folder)
    if not os.path.isdir(src):
        sys.exit(f"khong thay thu muc: {src}")

    dec, use = declared(), used_counts()
    files = sorted(f for f in os.listdir(src)
                   if f.lower().endswith(VID_EXT) and not f.startswith("."))

    items = []
    for f in files:
        p = os.path.join(src, f)
        key = N(p)
        if a.chua_khai and key in dec:
            continue
        w, h, d = probe(p)
        items.append(dict(name=f, path=p, w=w, h=h, dur=d,
                          const=dec.get(key), use=use.get(key, 0)))
    if not items:
        sys.exit("khong co clip nao")

    out = os.path.join(OUT_ROOT, a.folder)
    os.makedirs(out, exist_ok=True)

    f_big, f_mid, f_sm = font(20), font(16), font(13)
    lots = [items[i:i + CLIPS_PER_SHEET]
            for i in range(0, len(items), CLIPS_PER_SHEET)]
    idx0 = 1
    made = 0
    for li, lot in enumerate(lots, 1):
        if a.lo and li != a.lo:
            idx0 += len(lot)
            continue
        rows = []
        ch = 0
        for it in lot:
            ims = []
            for fr in FRAMES:
                im = grab(it["path"], max(0.1, it["dur"] * fr), CELL_W)
                if im is None:
                    im = Image.new("RGB", (CELL_W, 236), (60, 30, 30))
                    ImageDraw.Draw(im).text((10, 100), "KHONG DOC DUOC",
                                            font=f_big, fill=(255, 180, 180))
                ims.append(im)
                ch = max(ch, im.height)
            rows.append((it, ims))

        sw = len(FRAMES) * CELL_W + (len(FRAMES) + 1) * PAD
        sh = len(rows) * (ch + LABEL_H) + (len(rows) + 1) * PAD
        sheet = Image.new("RGB", (sw, sh), BG)
        d = ImageDraw.Draw(sheet)
        for n, (it, ims) in enumerate(rows):
            cy = PAD + n * (ch + LABEL_H + PAD)
            for j, im in enumerate(ims):
                sheet.paste(im, (PAD + j * (CELL_W + PAD), cy))
            num = idx0 + n
            doc = "DỌC" if it["h"] > it["w"] else ""
            tag = it["const"] or ("chưa khai" if not it["use"] else "")
            head = f"#{num}  {it['dur']:.1f}s  {it['w']}x{it['h']} {doc}"
            if it["use"]:
                head += f"   đã dùng {it['use']}×"
            d.text((PAD, cy + ch + 3), head, font=f_mid,
                   fill=HOT if it["const"] else FG)
            d.text((PAD, cy + ch + 24), f"{it['name'][:70]}", font=f_sm,
                   fill=DIM)
            if tag:
                d.text((sw - 260, cy + ch + 3), tag, font=f_mid,
                       fill=HOT if it["const"] else DIM)

        png = os.path.join(out, f"lo_{li:02d}.png")
        sheet.save(png, "PNG", optimize=True)
        with open(os.path.join(out, f"lo_{li:02d}.txt"), "w",
                  encoding="utf-8") as fh:
            for n, (it, _) in enumerate(rows):
                fh.write(f"#{idx0+n}\t{it['dur']:.1f}s\t{it['name']}\n")
        print(f"-> {png}  ({len(rows)} clip, "
              f"{os.path.getsize(png)/1024:.0f} KB)")
        made += 1
        idx0 += len(lot)

    json.dump(items, open(os.path.join(out, "_items.json"), "w"),
              ensure_ascii=False, indent=1)
    print(f"\n{len(items)} clip -> {made} tấm  ({out})")


if __name__ == "__main__":
    main()
