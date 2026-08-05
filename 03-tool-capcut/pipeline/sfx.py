# -*- coding: utf-8 -*-
"""Sinh cue SFX cho tung caption — theo luat anh Thanh chot 15/07/2026.

Nguon luat: 01-tool-cat-video/batch/sfx_rules.py (bo Dr Son).
Che do Dr Son la "every_caption": MOI caption duoc 1 cue, khong loc chon.
Pool chia 3 theo NOI DUNG:

    benefit  -> TING, BUTTON        loi ich / tac dung / ket qua
    warning  -> CAMERA              canh bao / tieu cuc
    default  -> WHOOSE FAST, POP, CLICKS   con lai (pool dung chinh)

Khac ban Dr Son o mot cho: ban do doan pool bang HEURISTIC TU KHOA tren text.
O day khong can doan — `plan.py` da phan loai san bang `variant`, chinh xac hon.

Hai luat giu nguyen:
  - round-robin trong tung pool (khong lap lien tiep 1 file)
  - min_gap 1.5s: cue nao gan cue truoc hon 1.5s thi BO, tranh ban lien thanh
  - intro_guard: 8 giay dau khong dung pool "benefit"
    (anh: "khong chen o dau clip qua nhieu no khong hop")

Muc: -16 dB — anh ha tu -6 xuong -16 ngay 15/07 vi "sound effect va nhac nen
khong duoc to qua at tieng nguoi noi".

File nay KHONG chay rieng, duoc 6_to_capcut.py goi.
"""
import os

SFX_ROOT = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../../01-tool-cat-video/library/audio/0. SOUND TEXT"))

POOL_DIRS = {
    "benefit": ["TING"],        # BUTTON bo 04/08/2026 — xem BO_FILE
    "warning": ["CAMERA"],
    "default": ["WHOOSE FAST", "POP", "CLICKS"],
}

# ---- FILE BI LOAI (anh Thanh chot 04/08/2026) ----------------------------
# "sfx bo nhung cai click_bell doi thanh ting cho nhung doan tich cuc"
# "sound buzzer button cung bo, nghe kho chiu qua"
#
# Cai bay: `click_bell1_*.wav` nam NGAY TRONG thu muc TING (5/8 file), nen
# round-robin cua pool "benefit" van boc trung chung — bo thu muc BUTTON thoi
# la chua du. Phai loc theo TEN FILE.
# Pool tich cuc con lai: ting.mp3 · Tiếng Ting.mp3 · Ding_05.wav
BO_FILE = ["click_bell", "buzzerbutton"]

# variant trong plan.py -> pool. Thay cho heuristic tu khoa cua ban goc.
VARIANT_POOL = {
    "warning":   "warning",
    "positive":  "benefit",
    "product":   "benefit",
    "yellow":    "default",
    "cta":       "default",
    "highlight": "default",
}

MIN_GAP = 1.5          # giay — cue gan hon thi bo
INTRO_GUARD = 8.0      # giay dau: khong dung pool benefit
SFX_DB = -16.0
AUDIO_EXT = (".wav", ".mp3", ".m4a", ".aac")


def load_pools():
    pools = {}
    for name, dirs in POOL_DIRS.items():
        files = []
        for d in dirs:
            p = os.path.join(SFX_ROOT, d)
            if os.path.isdir(p):
                files += sorted(os.path.join(p, f) for f in os.listdir(p)
                                if f.lower().endswith(AUDIO_EXT)
                                and not any(b in f.lower() for b in BO_FILE))
        pools[name] = files
    return pools


def derive_cues(plan):
    """-> [(t, duong_dan_sfx, ten_pool)] — da debounce."""
    pools = load_pools()
    missing = [k for k, v in pools.items() if not v]
    if missing:
        raise SystemExit(f"pool rong: {missing} — kiem tra {SFX_ROOT}")

    idx = {k: 0 for k in pools}
    cues, last = [], None
    for r in plan:
        t = r["t"]
        pool = VARIANT_POOL.get(r["variant"], "default")
        if pool == "benefit" and t < INTRO_GUARD:
            pool = "default"          # intro_guard
        if last is not None and t - last < MIN_GAP:
            continue                  # debounce
        f = pools[pool][idx[pool] % len(pools[pool])]
        idx[pool] += 1
        cues.append((t, f, pool))
        last = t
    return cues


def volume_linear():
    return 10 ** (SFX_DB / 20)        # -16 dB -> 0.158
