# -*- coding: utf-8 -*-
"""Dung track am thanh SFX rieng (WAV) cho tung video.
 - Day SFX lui dung bang khoang lang dau file -> tieng NO DUNG luc chu hien
 - Chuan hoa muc to ve cung mot nguong (peak -6 dB)
"""
# THAM KHAO — script nay lay nguyen van tu dot dung 5 video VR 9.6.2026,
# duong dan job/ban duyet la cua dot do. Doc de lay CACH LAM, sua bien o dau file
# truoc khi chay lai.
import json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "pipeline")))
from paths import JOBS_ROOT as _JR, MUSIC_ROOT as _MR  # noqa: E402
J = str(_JR)
M = str(_MR)
JOBS = ["vr_cham_xe","vr_song_khoe","vr_mat_ngu","vr_de_danh","vr_ket_qua_nhanh"]
TARGET_PEAK = -6.0

caps = json.load(open(os.path.join(J, "caption_final.json"), encoding="utf-8"))

def sh(a): return subprocess.run(a, capture_output=True, text=True,
                                 encoding="utf-8", errors="replace")

# do khoang lang dau + peak cua tung file SFX (chi do 1 lan)
info = {}
def probe(name):
    if name in info: return info[name]
    p = os.path.join(M, name)
    r = sh(["ffmpeg","-v","info","-i",p,"-af","silencedetect=noise=-45dB:d=0.03","-f","null","-"])
    ends = [float(x) for x in re.findall(r"silence_end:\s*([\d.]+)", r.stderr)]
    starts = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", r.stderr)]
    lead = ends[0] if ends and (not starts or starts[0] <= 0.02) else 0.0
    r2 = sh(["ffmpeg","-v","info","-i",p,"-af","volumedetect","-f","null","-"])
    m = re.search(r"max_volume:\s*(-?[\d.]+) dB", r2.stderr)
    peak = float(m.group(1)) if m else 0.0
    info[name] = (lead, peak, p)
    return info[name]

for vi, V in enumerate(caps):
    hits = [(r["t"], r["sfx"]) for r in V["rows"] if r.get("sfx")]
    out = os.path.join(J, JOBS[vi], "sfx_track.wav")
    if not hits:
        print(f"V{vi+1}: khong co SFX"); continue

    ins, filt, labs = [], [], []
    for k, (t, name) in enumerate(hits):
        lead, peak, path = probe(name)
        start = max(t - lead, 0)              # day lui de tieng no dung luc chu hien
        gain = TARGET_PEAK - peak
        ins += ["-i", path]
        filt.append(f"[{k}:a]volume={gain:.1f}dB,aresample=48000,"
                    f"adelay={int(start*1000)}|{int(start*1000)}[a{k}]")
        labs.append(f"[a{k}]")

    fc = ";".join(filt) + ";" + "".join(labs) + \
         f"amix=inputs={len(labs)}:duration=longest:normalize=0[mix]"
    cmd = ["ffmpeg","-v","error","-y", *ins,
           "-filter_complex", fc, "-map","[mix]",
           "-t", f"{V['dur']:.3f}", "-ar","48000","-ac","2", out]
    r = sh(cmd)
    if r.returncode:
        print(f"V{vi+1} LOI:\n{r.stderr[-800:]}")
    else:
        sz = os.path.getsize(out)/1048576
        print(f"V{vi+1} {V['title'][:40]:<42} {len(hits):>2} SFX  ->  sfx_track.wav ({sz:.1f} MB)")

print("\n--- Khoang lang dau da bu tru ---")
for n,(lead,peak,_) in sorted(info.items()):
    print(f"  {n[:44]:<46} lùi {lead:.2f}s | peak {peak:>5.1f}dB")
