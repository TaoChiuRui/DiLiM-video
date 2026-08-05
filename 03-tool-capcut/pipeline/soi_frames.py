# -*- coding: utf-8 -*-
"""Trich frame B-roll tai DUNG giay se dung, ghep thanh vai tam CONTACT SHEET.

    python3 soi_frames.py --job 04-du-an/<ten>
    python3 soi_frames.py --job 04-du-an/<ten> --only 12,19,29   # vai dong

Ra `edit/soi_frames/sheet_01.png ...` — moi tam 12 o, moi o mot dong plan kem
so hieu va chu caption.

VI SAO GHEP THANH TAM: agent `dilim-soat-broll` phai NHIN frame moi biet clip
co dung y khong. Nhin 50 anh roi la ~50 lan tra token anh; ghep 12 o mot tam
thi con 4-5 anh. Cung mot luong thong tin, re hon nam lan.

LUU Y: o day la NGUYEN KHUNG cua clip. Dai B-roll that la 1080x672 dat o giua
— clip ngang 16:9 gan nhu lot tron, nhung ANH va clip ti le la thi bi cat tren
duoi. Anh san pham phai soi ky cho nay (luat 3 cua anh Thanh).
"""
import argparse
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

COLS, ROWS = 3, 4          # 12 o mot tam
CELL_W = 380
LABEL_H = 52
PAD = 8
BG = (18, 20, 24)
FG = (230, 230, 230)
DIM = (150, 158, 168)

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


def grab(path, ss, w):
    """1 frame -> PIL.Image, None neu that bai."""
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if not path.lower().endswith((".jpg", ".jpeg", ".png")):
        cmd += ["-ss", str(ss)]
    cmd += ["-i", path, "-frames:v", "1", "-vf", f"scale={w}:-1",
            "-f", "image2", "-c:v", "mjpeg", "-"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode or not r.stdout:
        return None
    import io
    return Image.open(io.BytesIO(r.stdout)).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    ap.add_argument("--only", help="chi vai dong, vd 12,19,29")
    a = ap.parse_args()

    job = os.path.abspath(os.path.expanduser(a.job))
    plan = json.load(open(os.path.join(job, "edit/plan.json"), encoding="utf-8"))
    pick = {int(x) for x in a.only.split(",")} if a.only else None
    rows = [r for r in plan if r.get("path")
            and (pick is None or r["idx"] in pick)]
    if not rows:
        sys.exit("khong co dong nao co clip")

    out = os.path.join(job, "edit/soi_frames")
    os.makedirs(out, exist_ok=True)
    for f in os.listdir(out):
        os.remove(os.path.join(out, f))

    f_big, f_small = font(19), font(14)
    per = COLS * ROWS
    made = []
    for k in range(0, len(rows), per):
        chunk = rows[k:k + per]
        cells = []
        ch = 0
        for r in chunk:
            im = grab(r["path"], r["src_start"], CELL_W)
            if im is None:
                im = Image.new("RGB", (CELL_W, 214), (60, 30, 30))
                ImageDraw.Draw(im).text((10, 90), "KHONG DOC DUOC", font=f_big,
                                        fill=(255, 180, 180))
            cells.append((r, im))
            ch = max(ch, im.height)

        sw = COLS * CELL_W + (COLS + 1) * PAD
        sh = ROWS * (ch + LABEL_H) + (ROWS + 1) * PAD
        sheet = Image.new("RGB", (sw, sh), BG)
        d = ImageDraw.Draw(sheet)
        for n, (r, im) in enumerate(cells):
            cx = PAD + (n % COLS) * (CELL_W + PAD)
            cy = PAD + (n // COLS) * (ch + LABEL_H + PAD)
            sheet.paste(im, (cx, cy))
            cap = r["text"].replace("\n", " / ").replace("*", "")
            d.text((cx, cy + ch + 4),
                   f"#{r['idx']}  {r['t']:.1f}s→{r['t_end']:.1f}s  "
                   f"[{r['variant']}]", font=f_big, fill=FG)
            d.text((cx, cy + ch + 26), cap[:52], font=f_small, fill=FG)
            d.text((cx, cy + ch + 40),
                   f"{os.path.basename(r['path'])[:38]} @{r['src_start']}s",
                   font=f_small, fill=DIM)

        f = os.path.join(out, f"sheet_{k//per+1:02d}.png")
        sheet.save(f, "PNG", optimize=True)
        made.append(f)
        print(f"-> {f}  ({len(chunk)} ô, {os.path.getsize(f)/1024:.0f} KB)")

    print(f"\n{len(rows)} dòng có clip -> {len(made)} tấm")


if __name__ == "__main__":
    main()
