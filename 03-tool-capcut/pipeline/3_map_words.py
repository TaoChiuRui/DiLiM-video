# -*- coding: utf-8 -*-
"""Chieu moc tung chu tu timeline GOC sang timeline BAN DA CAT.

Khong transcribe lai final.mp4 — vua cham vua co the ra chu khac voi ban
minh da duyet. Thay vao do dung edl.json de doi moc:
    moc_moi = moc_cu - tong do dai cac doan bi bo NAM TRUOC no

Chu nao roi vao doan bi bo thi bien mat khoi ket qua.

    python3 map_words.py
"""
import json, os

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
SRC = os.path.join(HERE, "edit/transcripts_words/audio16k.json")
EDL = os.path.join(HERE, "edit/edl.json")
OUT = os.path.join(HERE, "edit/words_cut.json")


def main():
    d = json.load(open(SRC, encoding="utf-8"))
    keeps = json.load(open(EDL, encoding="utf-8"))["keeps"]

    # offset tich luy cho tung doan giu
    off, acc = [], 0.0
    for a, b in keeps:
        off.append((a, b, a - acc))     # moc_moi = moc_cu - (a - acc)
        acc += b - a

    words, lost = [], 0
    for s in d["segments"]:
        for w in s.get("words", []):
            t = (w.get("word") or "").strip()
            if not t:
                continue
            st = float(w["start"])
            hit = next(((a, b, o) for a, b, o in off if a <= st < b), None)
            if hit is None:
                lost += 1
                continue
            words.append({"w": t, "s": round(st - hit[2], 3),
                          "e": round(min(float(w["end"]), hit[1]) - hit[2], 3)})
            # LUU Y: `e` cua whisper khong dang tin (nuot ca khoang lang phia
            # sau) — chi dung de tham khao. Moi tinh toan caption phai bam `s`.

    words.sort(key=lambda x: x["s"])
    json.dump(words, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"chu giu lai : {len(words)}")
    print(f"chu bi cat  : {lost}")
    print(f"dai ban cat : {words[-1]['s']:.2f}s (chu cuoi bat dau)")
    print(f"-> {OUT}")

    txt = os.path.join(HERE, "edit/transcript_cut.txt")
    with open(txt, "w", encoding="utf-8") as f:
        line, t0 = [], words[0]["s"]
        for w in words:
            line.append(w["w"])
            if len(line) >= 12:
                f.write(f"[{int(t0//60)}:{t0%60:05.2f}] {' '.join(line)}\n")
                line, t0 = [], w["s"]
        if line:
            f.write(f"[{int(t0//60)}:{t0%60:05.2f}] {' '.join(line)}\n")
    print(f"-> {txt}")


if __name__ == "__main__":
    main()
