# -*- coding: utf-8 -*-
"""BUOC 6 — Render 2 lop rieng (B-roll, TEXT) roi transcode ProRes 4444 qscale 9.
CHAY TUAN TU, mot tien trinh mot luc: 2 tien trinh ghi cung render_tmp = treo may.
"""
import json, sys, time, subprocess
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pipeline"))
from render_overlay import build_broll_track, build_track, caption_chunk, run
from caption_style import StyleCounters
JOB = Path(__file__).resolve().parent / "v1"
caps = json.loads((JOB/"captions.json").read_text(encoding="utf-8"))
plan = json.loads((JOB/"broll_plan.json").read_text(encoding="utf-8"))
meta = json.loads((JOB/"meta.json").read_text(encoding="utf-8"))
TF, FPS = meta["total_frames"], meta["fps"]
tmp = JOB/"render_tmp"; tmp.mkdir(exist_ok=True)
t=time.time(); bt=tmp/"broll_track.mov"
if not bt.exists(): build_broll_track(plan, TF, FPS, tmp/"broll_chunks", bt)
print(f"  B-roll {time.time()-t:.0f}s", flush=True)
t=time.time(); ct=tmp/"caption_track.mov"
if not ct.exists():
    c=StyleCounters()
    build_track([(x["from"],x["durationInFrames"],x) for x in sorted(caps,key=lambda z:z["from"])],
                TF, FPS, tmp/"caption_chunks", ct,
                lambda x,n,o: caption_chunk(x,c,FPS,tmp,o,meta["broll_position"]))
print(f"  TEXT {time.time()-t:.0f}s", flush=True)
for src,dst in [(bt,JOB/"v1_01_BROLL.mov"),(ct,JOB/"v1_02_TEXT.mov")]:
    run(["ffmpeg","-y","-i",str(src),"-c:v","prores_ks","-profile:v","4","-qscale:v","9",
         "-pix_fmt","yuva444p10le",str(dst)], dst.stem)
    n=subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=nb_frames",
                      "-of","csv=p=0",str(dst)],capture_output=True,text=True).stdout.strip()
    print(f"  {dst.name} {dst.stat().st_size/2**30:.2f} GB | {n} frame {'OK' if n==str(TF) else '!! LECH'}", flush=True)
