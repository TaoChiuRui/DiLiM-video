# -*- coding: utf-8 -*-
"""Cat A-roll theo ban duyet — moc SNAP VAO `start` cua chu.

BAI HOC (03/08/2026): `end` cua whisper KHONG dang tin — no keo dai de nuot
luon khoang lang phia sau (chu "nhung" bi ghi la 55.12->56.16, dai 1 giay).
Chi `start` moi dung. Nen moi moc cat deu lay tu `start`:
    mo  nhat cat = start cua chu DAU TIEN bi bo
    dong nhat cat = start cua chu DAU TIEN duoc giu
Cach nay dam bao khong bao gio gam vao dau mot chu duoc giu.

    python3 cut.py
"""
import json, os, re, subprocess, sys

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
SRC = next((p for p in (os.path.join(HERE, "source.mp4"),
                        os.path.join(HERE, "source.MOV"),
                        os.path.join(HERE, "source.mov")) if os.path.exists(p)),
           os.path.join(HERE, "source.MOV"))
OUT = os.path.join(HERE, "edit/final.mp4")
TMP = os.path.join(HERE, "edit/_seg")

FADE = 0.030          # fade am 30ms moi moi noi — chong tieng "bup"

# Doan BI BO — doc tu <job>/cuts.json (moi job mot file rieng).
#   [{"t0":0.0,"t1":2.38,"why":"cau lac"}, ...]   t1 = null nghia la den het.
_cf = os.path.join(HERE, "cuts.json")
if not os.path.exists(_cf):
    raise SystemExit(f"thieu {_cf}")
CUTS = [(c["t0"], c["t1"], c.get("why", ""))
        for c in json.load(open(_cf, encoding="utf-8"))]
# HUY 2 nhat so voi ban duyet: 55.35-56.05 va 112.90-114.15.
# Do RMS cua so 50ms cho thay CON TIENG o do (-29..-33 dB, ngang muc dang noi),
# khong phai im lang. Cat la gam vao tieng.


def probe(p, s="v:0", e="duration"):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", f"format={e}",
                        "-of", "csv=p=0", p], capture_output=True, text=True)
    return float(r.stdout.strip())


def main():
    total = probe(SRC)
    global _fps
    _r = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
                         "stream=r_frame_rate","-of","csv=p=0",SRC],capture_output=True,text=True)
    _t = re.sub(r"[^0-9/]", "", _r.stdout.strip().splitlines()[0]) if _r.stdout.strip() else "30/1"
    _a, _, _b = _t.partition("/")
    _fps = float(_a) / float(_b or 1)
    if _fps > 60: print(f"nguon {_fps:.0f} fps -> ha ve 30 fps")
    cuts = [(a, b if b is not None else total, w) for a, b, w in CUTS]

    keeps, pos = [], 0.0
    for a, b, _ in cuts:
        if a > pos:
            keeps.append((pos, a))
        pos = max(pos, b)
    if pos < total:
        keeps.append((pos, total))

    os.makedirs(TMP, exist_ok=True)
    for f in os.listdir(TMP):
        os.remove(os.path.join(TMP, f))

    print(f"goc {total:.2f}s   |  bo {sum(b-a for a,b,_ in cuts):.2f}s  ({len(cuts)} nhat)")
    print(f"giu {len(keeps)} doan:\n")

    parts = []
    for i, (a, b) in enumerate(keeps):
        d = b - a
        out = os.path.join(TMP, f"s{i:02d}.mp4")
        # fade vao 30ms dau + ra 30ms cuoi cua TUNG doan -> khong nghe "bup" o moi noi
        af = f"afade=t=in:st=0:d={FADE},afade=t=out:st={max(0,d-FADE):.4f}:d={FADE}"
        cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", SRC,
               "-t", f"{d:.4f}", "-af", af,
               "-c:v", "h264_videotoolbox", "-b:v", "12M",
               # nguon >60fps (iPhone slow-mo) -> ha ve 30, video noi chuyen
               # khong can 120fps ma project CapCut se nang gap 4
               *(["-r", "30"] if _fps > 60 else []),
               "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
               "-movflags", "+faststart", out]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode:
            sys.exit(f"loi doan {i}: {r.stderr[-400:]}")
        parts.append(out)
        print(f"  doan {i+1}  {a:7.2f} -> {b:7.2f}   ({d:6.2f}s)")

    lst = os.path.join(TMP, "list.txt")
    open(lst, "w").write("\n".join(f"file '{p}'" for p in parts))
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                        "-i", lst, "-c", "copy", "-movflags", "+faststart", OUT],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"loi ghep: {r.stderr[-400:]}")

    got = probe(OUT)
    want = sum(b - a for a, b in keeps)
    print(f"\n-> {OUT}")
    print(f"   dai {got:.2f}s  ({int(got//60)}:{got%60:05.2f})   du kien {want:.2f}s   "
          f"lech {abs(got-want):.2f}s")
    print(f"   dung luong {os.path.getsize(OUT)/1024/1024:.0f} MB")
    json.dump({"source": SRC, "total": total, "cuts": cuts, "keeps": keeps},
              open(os.path.join(HERE, "edit/edl.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
