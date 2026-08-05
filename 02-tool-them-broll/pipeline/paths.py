# -*- coding: utf-8 -*-
"""Duong dan dung chung cho ca goi — doc tu config.json o thu muc goc.

Moi script trong goi PHAI lay duong dan tu day, khong hard-code, de chuyen may
chi phai sua 1 file duy nhat (config.json).

    python paths.py        # kiem tra duong dan hien tai co ton tai khong
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent          # thu muc goc cua goi
PIPELINE = ROOT / "pipeline"
FONT = PIPELINE / "fonts" / "Anton-Regular.ttf"

DEFAULT = {
    "broll_root": r"D:\download\Footage B-roll",
    "music_root": "",          # de trong = <broll_root>\Music
    "jobs_root": "",           # de trong = <goc goi>\jobs
    "whisper_model": "medium",
    "whisper_device": "cpu",
    "whisper_compute_type": "int8",
}

CFG = dict(DEFAULT)
_f = ROOT / "config.json"
if _f.is_file():
    CFG.update(json.loads(_f.read_text(encoding="utf-8")))

BROLL_ROOT = Path(os.path.expandvars(CFG["broll_root"]))
MUSIC_ROOT = Path(os.path.expandvars(CFG["music_root"])) if CFG["music_root"] else BROLL_ROOT / "Music"
JOBS_ROOT = Path(os.path.expandvars(CFG["jobs_root"])) if CFG["jobs_root"] else ROOT / "jobs"

WHISPER_MODEL = CFG["whisper_model"]
WHISPER_DEVICE = CFG["whisper_device"]
WHISPER_COMPUTE_TYPE = CFG["whisper_compute_type"]

# ten thu muc con trong kho B-roll (giu nguyen dau tieng Viet nhu tren o dia)
DA_CHUAN_HOA = BROLL_ROOT / "Đã Chuẩn Hóa"
PRODUCT_BROLL = BROLL_ROOT / "Product Broll"
SFX_ROOT = BROLL_ROOT / "Âm Thanh"


def check() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    # (ten, duong dan, co that khong, bat buoc?)
    # 2 pool "Đã Chuẩn Hóa" / "Product Broll" chua chep sang o Mac -> canh bao
    # thoi, khong tinh la loi, vi catalog.py tu bo qua root khong ton tai.
    rows = [
        ("config.json", _f, _f.is_file(), True),
        ("kho B-roll", BROLL_ROOT, BROLL_ROOT.is_dir(), True),
        ("  Đã Chuẩn Hóa", DA_CHUAN_HOA, DA_CHUAN_HOA.is_dir(), False),
        ("  Product Broll", PRODUCT_BROLL, PRODUCT_BROLL.is_dir(), False),
        ("kho nhạc", MUSIC_ROOT, MUSIC_ROOT.is_dir(), True),
        ("kho SFX", SFX_ROOT, SFX_ROOT.is_dir(), False),
        ("thư mục jobs", JOBS_ROOT, JOBS_ROOT.is_dir(), True),
        ("font Anton", FONT, FONT.is_file(), True),
    ]
    bad = 0
    for name, p, ok, must in rows:
        tag = "OK   " if ok else ("THIEU" if must else "CHUA CO")
        print(f"{tag}  {name:<16} {p}")
        bad += 0 if ok or not must else 1
    for mod, pip in [("PIL", "pillow")]:
        try:
            __import__(mod)
            print(f"OK    python: {mod}")
        except ImportError:
            print(f"THIEU python: {mod}   ->  pip install {pip}")
            bad += 1

    import shutil

    # Transcribe: tren MacBook Apple Silicon dung mlx-whisper (chay GPU Metal,
    # cai bang `uv tool install mlx-whisper`) THAY CHO faster-whisper cua ban
    # Windows. Nhan ca hai, co 1 trong 2 la du.
    if shutil.which("mlx_whisper"):
        print("OK    transcribe: mlx-whisper (Apple Silicon, GPU)")
    else:
        try:
            __import__("faster_whisper")
            print("OK    transcribe: faster-whisper")
        except ImportError:
            print("THIEU transcribe   ->  uv tool install mlx-whisper   (Mac)")
            print("                   ->  pip install faster-whisper    (Windows/Linux)")
            bad += 1

    for exe in ("ffmpeg", "ffprobe"):
        if shutil.which(exe):
            print(f"OK    {exe}")
        else:
            print(f"THIEU {exe} khong co trong PATH")
            bad += 1
    print("\n=> SAN SANG" if not bad else f"\n=> CON {bad} THU CAN SUA")
    return bad


if __name__ == "__main__":
    raise SystemExit(1 if check() else 0)
