# -*- coding: utf-8 -*-
"""Chay ca chuoi cho NHIEU job — phien am SONG SONG ngay tu dau.

    python3 chay_het.py 05-natto 06-magie          # den buoc sinh khung plan.py
    python3 chay_het.py <job> --tu 6 --den 13      # chay tiep tu buoc 6

VI SAO: do that ngay 04/08 — 2 video het 1 gio 15 lam viec. Trong do
**phien am 20 phut** (8' + 12'), va toi khoi dong job 2 MUON 8 PHUT vi lam
tuan tu. Phien am la buoc duy nhat vua lau vua khong can nguoi — ban ngay tu
phut dau la an khong ~8-10 phut.

Bang thoi gian do duoc (job 389 giay):
    1_transcribe    8-12 phut   <- CHIEM 40%, chay song song duoc
    2_cut             66 giay
    6_to_capcut       35 giay
    5_render          20 giay
    con lai         < 12 giay   <- toi uu code o day la vo nghia

Cac buoc CAN NGUOI (viet cuts.json, viet plan.py, chon clip) khong tu chay —
script dung lai va bao ro con thieu gi.
"""
import argparse
import os
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
VENV = os.path.join(ROOT, "03-tool-capcut/VectCutAPI/.venv/bin/python")

BUOC = [
    (1,  "1_transcribe.py",      "phien am word-level",        None),
    (2,  None,                   "VIET TAY cuts.json",         "cuts.json"),
    (3,  "make_cut_table.py",    "bang duyet ban cat",         None),
    (4,  "2_cut.py",             "cat A-roll",                 None),
    (5,  "3_map_words.py",       "chieu moc sang ban cat",     None),
    (6,  "make_plan_draft.py",   "sinh khung plan.py",         None),
    (7,  None,                   "VIET TAY noi dung plan.py",  "plan.py"),
    (8,  "@plan",                "dung plan.json",             None),
    (9,  "suggest_clips.py",     "goi y B-roll",               None),
    (10, "4_anchor.py",          "neo caption",                None),
    (11, "4b_vary.py",           "chong lap B-roll",           None),
    (12, "soi_plan.py",          "may soi",                    None),
    (13, "make_review_table.py", "bang duyet",                 None),
    (14, "5_render_captions.py", "ve caption PNG",             None),
    (15, "6_to_capcut.py",       "dung draft CapCut",          None),
    (16, "kho_caption.py",       "nap job vao kho caption",    None),
]


CAN_T7 = {"suggest_clips.py", "@plan", "4b_vary.py", "6_to_capcut.py"}


def t7_song():
    """O T7 con doc duoc khong?

    THEM 04/08/2026: dem do o rot 5 lan, co lan mount duoc ma doc ra
    `Input/output error`. Chay pipeline luc do thi B-roll am tham hong ma
    khong ai bao. Kiem bang doc THAT, khong chi kiem duong dan ton tai.
    """
    try:
        sys.path.insert(0, HERE)
        import clips as C
        n = 0
        for k in ("MACH_MAU", "CUC_MAU", "NATTO1"):
            p = getattr(C, k, None)
            if p and os.path.exists(p) and os.path.getsize(p) > 0:
                n += 1
        return n >= 2
    except Exception:
        return False


def job_dir(name):
    p = os.path.abspath(os.path.expanduser(name))
    if os.path.isdir(p):
        return p
    p = os.path.join(ROOT, "04-du-an", name)
    if os.path.isdir(p):
        return p
    hits = [d for d in os.listdir(os.path.join(ROOT, "04-du-an"))
            if name.lower() in d.lower()]
    if len(hits) == 1:
        return os.path.join(ROOT, "04-du-an", hits[0])
    sys.exit(f"khong ro job: {name}  ({hits})")


def chay(script, job, ten):
    t0 = time.time()
    if script == "@plan":
        cmd = ["python3", os.path.join(job, "plan.py")]
    elif script == "kho_caption.py":
        cmd = ["python3", os.path.join(HERE, script), "--gom"]
    else:
        py = VENV if script == "6_to_capcut.py" else "python3"
        cmd = [py, os.path.join(HERE, script), "--job", job]
        if script in ("4_anchor.py", "4b_vary.py"):
            cmd.append("--apply")
        if script == "suggest_clips.py":
            cmd.append("--md")
        if script == "6_to_capcut.py":
            cmd.append("--install")
    r = subprocess.run(cmd, capture_output=True, text=True)
    dt = time.time() - t0
    ok = r.returncode == 0
    print(f"   [{'ok ' if ok else 'LOI'}] {ten:28} {dt:6.1f}s")
    if not ok:
        print("        " + (r.stderr or r.stdout).strip().splitlines()[-1][:120])
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("jobs", nargs="+")
    ap.add_argument("--tu", type=int, default=1)
    ap.add_argument("--den", type=int, default=6)
    a = ap.parse_args()
    jobs = [job_dir(j) for j in a.jobs]

    # ---- BUOC 1 CHAY SONG SONG CHO MOI JOB ----
    if a.tu <= 1 <= a.den:
        print(f"phien am {len(jobs)} job SONG SONG "
              f"(tuan tu se lau gap {len(jobs)} lan):")
        t0 = time.time()
        ths = []
        for j in jobs:
            t = threading.Thread(target=chay,
                                 args=("1_transcribe.py", j, os.path.basename(j)[:28]))
            t.start()
            ths.append(t)
        for t in ths:
            t.join()
        print(f"   -> xong ca {len(jobs)} job trong {time.time()-t0:.0f}s\n")

    for j in jobs:
        print(f"== {os.path.basename(j)}")
        for so, script, ten, can in BUOC:
            if so < max(a.tu, 2) or so > a.den:
                continue
            if can:
                p = os.path.join(j, can)
                if not os.path.exists(p):
                    print(f"   [DUNG] can {can} — viet xong roi chay tiep:")
                    print(f"          python3 {__file__} {os.path.basename(j)} "
                          f"--tu {so+1} --den {a.den}")
                    break
                print(f"   [co ] {can}")
                continue
            if script in CAN_T7 and not t7_song():
                print(f"   [DUNG] «{ten}» can o T7 ma o khong doc duoc.")
                print("          Cam lai o roi chay tiep — dung chay tiep khi "
                      "chua co o, B-roll se hong am tham.")
                break
            if not chay(script, j, ten):
                break
        print()


if __name__ == "__main__":
    main()
