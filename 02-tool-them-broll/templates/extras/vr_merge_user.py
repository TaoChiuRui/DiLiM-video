# -*- coding: utf-8 -*-
"""Gop clip nguoi dung tu chon vao ke hoach + gan loi thoai goc cho tung caption."""
# THAM KHAO — script nay lay nguyen van tu dot dung 5 video VR 9.6.2026,
# duong dan job/ban duyet la cua dot do. Doc de lay CACH LAM, sua bien o dau file
# truoc khi chay lai.
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "..", "pipeline")))
from paths import JOBS_ROOT as _JR, MUSIC_ROOT as _MR  # noqa: E402
J = str(_JR)
PREV = os.path.join(J, "_preview")
JOBS = ["vr_cham_xe", "vr_song_khoe", "vr_mat_ngu", "vr_de_danh", "vr_ket_qua_nhanh"]

caps = json.load(open(os.path.join(J, "caption_final.json"), encoding="utf-8"))
duyet = json.load(open(r"D:\download\broll-duyet.json", encoding="utf-8"))

def dur(p):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                        "-of","csv=p=0",p], capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except: return 0.0

# ---- 1. gan loi thoai goc tu segments.json ----
def loi_thoai(job, t0, t1):
    p = os.path.join(J, job, "segments.json")
    if not os.path.exists(p):
        return ""
    segs = json.load(open(p, encoding="utf-8"))
    hit = [s["text"] for s in segs if s["end"] > t0 + .15 and s["start"] < t1 - .15]
    return " ".join(hit).strip()

# ---- 2. gop lua chon cua nguoi dung ----
added = {}
for vi, v in enumerate(duyet):
    for b in v.get("bosung", []):
        p = b["path"].strip().strip('"').strip()
        if os.path.exists(p):
            added.setdefault(vi, {})[b["idx"]] = p

out_all = []
for vi, V in enumerate(caps):
    mine = {}
    pj = os.path.join(J, f"broll_v{vi+1}.json")
    if os.path.exists(pj):
        for r in json.load(open(pj, encoding="utf-8")):
            mine[r["idx"]] = r

    rows, used = [], {}
    for i, r in enumerate(V["rows"], 1):
        rec = {"idx": i, "t": r["t"], "t_end": r["t_end"],
               "cap": r["d1"] + (" / " + r["d2"] if r["d2"] else ""),
               "var": r["var"], "sfx": r.get("sfx", ""),
               "say": loi_thoai(JOBS[vi], r["t"], r["t_end"]),
               "path": "", "name": "", "why": "", "src": "", "thumb": "",
               "off": 0, "dur": 0, "flags": []}
        need = r["t_end"] - r["t"]

        if i in added.get(vi, {}):                    # nguoi dung chon
            rec.update(path=added[vi][i], src="bạn chọn",
                       why="clip bạn tự chỉ định", off=0)
        elif i in mine:                               # toi chon truoc do
            m = mine[i]
            rec.update(path=m["path"], src="tôi đề xuất", why=m["why"],
                       off=m["off"], dur=m["dur"], flags=list(m["flags"]),
                       thumb=m["thumb"])

        if rec["path"]:
            rec["name"] = os.path.basename(rec["path"])
            isimg = rec["path"].lower().endswith((".jpg",".jpeg",".png"))
            if not rec["thumb"]:                      # can trich anh moi
                d = 0 if isimg else dur(rec["path"])
                rec["dur"] = round(d, 1)
                th = f"u{vi+1}_{i:02d}.jpg"
                cmd = (["ffmpeg","-v","error","-y","-i",rec["path"]] if isimg
                       else ["ffmpeg","-v","error","-y","-ss",str(rec["off"]),"-i",rec["path"]])
                subprocess.run(cmd + ["-vf","scale=340:-1","-frames:v","1",
                                      os.path.join(PREV, th)], capture_output=True)
                rec["thumb"] = th
                if not isimg and d and (d - rec["off"]) < need:
                    rec["flags"].append(f"clip {d:.1f}s < cần {need:.1f}s → sẽ lặp")
            if rec["name"] in used:
                rec["flags"].append(f"TRÙNG clip với #{used[rec['name']]}")
            used[rec["name"]] = i
        rows.append(rec)

    out_all.append({"title": V["title"], "dur": V["dur"], "rows": rows})
    co = sum(1 for x in rows if x["path"])
    ban = sum(1 for x in rows if x["src"] == "bạn chọn")
    w = sum(1 for x in rows if x["flags"])
    print(f"V{vi+1} {V['title'][:40]:<42} {co:>2}/{len(rows):<3} có B-roll "
          f"(bạn chọn {ban})" + (f"  ⚠ {w}" if w else ""))

json.dump(out_all, open(os.path.join(J, "broll_full.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("\nDa ghi broll_full.json")
