# -*- coding: utf-8 -*-
"""BUOC 5 — Ap ban DUYET cua nguoi dung (file JSON tai ve tu bang HTML) ->
captions.json / broll_plan.json / meta.json + sfx_track.wav.

Phan "quyet dinh nguoi dung DA XAC NHAN" ben duoi la vi du that cua job Raydel:
moi job phai viet lai theo dung nhung gi nguoi dung tra loi.
"""
import json, os, re, subprocess, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline")))
from paths import MUSIC_ROOT  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
JOB = os.path.join(HERE, "v1")
SRC = r"D:\Download\raydel_v1_v2026073115-da-sua.json"   # >>> SUA: file JSON nguoi dung tai ve
FPS, TOTAL = 60, 5337                                    # >>> SUA: fps + tong so frame cua A-roll
IMG = (".jpg", ".jpeg", ".png", ".JPG")
MUSIC = str(MUSIC_ROOT)

# Nguoi dung chot 2026-07-31: "hinh hoac video CO HOP SAN PHAM moi duoc lap lai".
# Vi tri thu muc KHONG quyet dinh - bieu do nghien cuu / vien nghien cuu / sap
# mia deu nam trong "Product Broll" nhung KHONG co hop san pham -> cam lap.
CO_HOP_SAN_PHAM = ("Raydel policosanol.mp4", "Raydel Policosanol.JPG",
                   "Combo Raydel policosanol + Rich Coenzyme Q10.jpg",
                   "IMG_4200.JPG01692522.mp4")


def la_san_pham(path):
    return os.path.basename(path) in CO_HOP_SAN_PHAM

rows = json.load(open(SRC, encoding="utf-8"))
plan = {r["idx"]: r for r in json.load(open(os.path.join(JOB, "plan.json"), encoding="utf-8"))}


def norm(s):
    return unicodedata.normalize("NFC", (s or "")).replace("\u00a0", " ").strip()


def paths_of(raw):
    out = []
    for c in re.split(r'[\r\n]+', (raw or "").replace("\u00a0", " ")):
        c = c.strip().strip('"').strip()
        if os.path.isfile(c):
            out.append(c); continue
        for part in re.split(r'"\s*,?\s*"?', c):
            part = part.strip().strip('"').strip()
            if part and os.path.isfile(part):
                out.append(part)
    return out


# --- 4 quyet dinh nguoi dung DA XAC NHAN ---
FIX_TEXT = {2:  ("HOẶC MỆT MỎI", "*KHÔNG RÕ NGUYÊN NHÂN*"),   # thieu chu KHONG
            18: ("CHỐNG OXY HÓA", "*TẾ BÀO MỠ*")}             # bo lap "TE BAO MO"
MERGE_INTO = {13: 12}          # #12 va #13 ghi trung -> gop lam 1 caption
DROP_CAP = {9, 30, 31}         # de trong ca 2 dong -> bo caption
SRC_OVERRIDE = {3: 11.0}       # "cat tu doan mat truoc san pham" -> 11.0s
SPLIT_17 = 50.30               # luc noi "tao do"

caps, segs = [], []
for r in rows:
    i = r["idx"]; o = plan[i]
    t0, t1 = o["t"], o["t_end"]
    d1, d2 = norm(r["d1"]), norm(r["d2"])
    if i in FIX_TEXT:
        d1, d2 = FIX_TEXT[i]
    # caption
    if i not in DROP_CAP and i not in MERGE_INTO:
        if i == 12:
            t1c = plan[13]["t_end"]          # gop #12+#13
        else:
            t1c = t1
        txt = d1 + ("\n" + d2 if d2 else "")
        if txt:
            assert txt.count("*") % 2 == 0, f"#{i} dau * le: {txt}"
            caps.append({"from": round(t0 * FPS), "durationInFrames": round(t1c * FPS) - round(t0 * FPS),
                         "text": txt, "variant": r["variant"]})
    # b-roll
    ps = paths_of(r["path"])
    if not ps:
        continue
    if i == 17 and len(ps) >= 2:
        spans = [(t0, SPLIT_17, ps[0]), (SPLIT_17, t1, ps[1])]
    else:
        spans = [(t0, t1, ps[0])]
    for a, b, p in spans:
        ss = SRC_OVERRIDE.get(i, o["src_start"] if p == (o["path"] or "") else 0.0)
        isimg = p.lower().endswith(tuple(x.lower() for x in IMG))
        need = b - a
        if not isimg:
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                        "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip() or 0)
            if dur - ss < need - 0.03:
                ss = max(dur - need, 0)
        segs.append({"from": round(a * FPS), "durationInFrames": round(b * FPS) - round(a * FPS),
                     "path": p, "is_image": isimg, "src_start_s": round(ss, 2),
                     "xfade_prev": 0, "crop_bias": 0.5, "key_black": False})

# clip SAN PHAM dung nhieu lan -> moi lan lay mot doan KHAC nhau
_used = {}
for b in segs:
    if la_san_pham(b["path"]) and not b["is_image"]:
        k = b["path"]
        if k in _used:
            b["src_start_s"] = round(_used[k], 2)
        _used[k] = b["src_start_s"] + b["durationInFrames"] / FPS

# noi lien mach khi 2 doan lien ke cung clip
for k in range(1, len(segs)):
    a, b = segs[k - 1], segs[k]
    gap = b["from"] - (a["from"] + a["durationInFrames"])
    if a["path"] == b["path"] and 0 <= gap <= 36 and not b["is_image"]:
        if gap:                      # khe ho nho -> keo dai doan truoc cho lien mach
            a["durationInFrames"] += gap
        cont = a["src_start_s"] + a["durationInFrames"] / FPS
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                    "-of", "csv=p=0", b["path"]], capture_output=True, text=True).stdout.strip() or 0)
        if dur - cont >= b["durationInFrames"] / FPS - 0.03:
            b["src_start_s"] = round(cont, 2)

merged = []
for b in segs:
    m = merged[-1] if merged else None
    if m and m["path"] == b["path"] and m["from"] + m["durationInFrames"] == b["from"]:
        cont = m["src_start_s"] + m["durationInFrames"] / FPS
        if b["is_image"] or abs(b["src_start_s"] - cont) < 0.05:
            m["durationInFrames"] += b["durationInFrames"]; continue
        if la_san_pham(b["path"]):
            b = dict(b); b["xfade_prev"] = 15
    merged.append(dict(b))

# ---- LOI 1: khe ho giua 2 doan B-roll -> dai bi trong vai frame -> giat.
# Keo dai doan TRUOC cho cham dung diem bat dau doan SAU (khong dich doan sau
# len som). Chi noi khi khe ho <= 1s, xa hon la co y de trong.
for a, b in zip(merged, merged[1:]):
    gap = b["from"] - (a["from"] + a["durationInFrames"])
    if 0 < gap <= 60:
        a["durationInFrames"] += gap

# ---- LOI 2: B-roll hien TRUOC luc noi tu khoa.
# Doi diem vao cua B-roll den dung luc tu khoa (chu trong dau *) duoc noi ra.
WORDS = json.load(open(os.path.join(JOB, "words.json"), encoding="utf-8"))


def _n2(t):
    t = unicodedata.normalize("NFD", (t or "").lower())
    return "".join(ch for ch in t if unicodedata.category(ch) != "Mn").replace("đ", "d")


def moc_tu_khoa(cap):
    kw = re.findall(r"\*([^*]+)\*", cap["text"])
    if not kw:
        return None
    first = _n2(kw[0]).split()
    if not first:
        return None
    t0, t1 = cap["from"] / FPS, (cap["from"] + cap["durationInFrames"]) / FPS
    for w in WORDS:
        if t0 - 0.1 <= w["start"] < t1 and _n2(w["word"]).strip(" ,.?!") == first[0]:
            return w["start"]
    return None


shift = []
for i, b in enumerate(merged):
    cap = next((c for c in caps if c["from"] == b["from"]), None)
    if not cap:
        continue
    t = moc_tu_khoa(cap)
    if t is None:
        continue
    delta = round(t * FPS) - b["from"]
    if 24 <= delta <= 90 and b["durationInFrames"] - delta > 24:   # tre 0.4-1.5s
        b["from"] += delta
        b["durationInFrames"] -= delta
        if i:
            merged[i - 1]["durationInFrames"] += delta            # doan truoc chay bu
        shift.append((round(b["from"] / FPS, 2), delta, cap["text"].split(chr(10))[0][:26]))
for t, d, tx in shift:
    print(f"  doi B-roll tre {d/FPS*1000:>4.0f} ms -> {t}s  ({tx})")

caps.sort(key=lambda c: c["from"])
for a, b in zip(caps, caps[1:]):
    assert a["from"] + a["durationInFrames"] <= b["from"], "caption chong lan"
for a, b in zip(merged, merged[1:]):
    assert a["from"] + a["durationInFrames"] <= b["from"], "b-roll chong lan"

# ---- SAU KHI da chinh xong thoi gian: keo src_start ve 0 neu doan bi thieu phim
for b in merged:
    if b["is_image"]:
        continue
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                              "-of", "csv=p=0", b["path"]], capture_output=True, text=True).stdout.strip() or 0)
    need = b["durationInFrames"] / FPS
    if d - b["src_start_s"] < need - 0.02:
        moi = max(round(d - need, 2), 0.0)
        print(f"  lui src {b['src_start_s']} -> {moi} cho {os.path.basename(b['path'])[:38]}"
              + ("" if d >= need else f"  (clip chi {d:.2f}s, se GIU FRAME CUOI {need-d:.2f}s)"))
        b["src_start_s"] = moi

from collections import Counter
dup = [(os.path.basename(k), n) for k, n in
       Counter(b["path"] for b in merged if not la_san_pham(b["path"])).items() if n > 1]
if dup:
    for k, n in dup:
        print(f"  !! LAP CLIP KHONG PHAI SAN PHAM: {n}x {k}")
    raise SystemExit("dung lai - vi pham luat khong lap clip")

json.dump(caps, open(os.path.join(JOB, "captions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(merged, open(os.path.join(JOB, "broll_plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"total_frames": TOTAL, "fps": FPS, "broll_position": "top"},
          open(os.path.join(JOB, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---- SFX track ----
hits = [(plan[r["idx"]]["t"], r["sfx"]) for r in rows if r.get("sfx")]
if hits:
    info = {}
    def probe(name):
        if name in info: return info[name]
        p = os.path.join(MUSIC, name)
        r1 = subprocess.run(["ffmpeg", "-v", "info", "-i", p, "-af", "silencedetect=noise=-45dB:d=0.03",
                             "-f", "null", "-"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        ends = [float(x) for x in re.findall(r"silence_end:\s*([\d.]+)", r1.stderr)]
        starts = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", r1.stderr)]
        lead = ends[0] if ends and (not starts or starts[0] <= 0.02) else 0.0
        r2 = subprocess.run(["ffmpeg", "-v", "info", "-i", p, "-af", "volumedetect", "-f", "null", "-"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
        m = re.search(r"max_volume:\s*(-?[\d.]+) dB", r2.stderr)
        info[name] = (lead, float(m.group(1)) if m else 0.0, p)
        return info[name]
    ins, filt, labs = [], [], []
    for k, (t, name) in enumerate(hits):
        lead, peak, p = probe(name)
        start = max(t - lead, 0)
        ins += ["-i", p]
        filt.append(f"[{k}:a]volume={-6.0-peak:.1f}dB,aresample=48000,"
                    f"adelay={int(start*1000)}|{int(start*1000)}[a{k}]")
        labs.append(f"[a{k}]")
    fc = ";".join(filt) + ";" + "".join(labs) + f"amix=inputs={len(labs)}:duration=longest:normalize=0[mix]"
    out = os.path.join(JOB, "v1_03_SFX.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", fc, "-map", "[mix]",
                    "-t", f"{TOTAL/FPS:.3f}", "-ar", "48000", "-ac", "2", out], check=True)
    print(f"SFX: {len(hits)} tieng -> {os.path.basename(out)}")

cov = sum(b["durationInFrames"] for b in merged) / TOTAL * 100
print(f"v1: {len(caps)} caption | {len(merged)} doan B-roll | phu {cov:.0f}%")
