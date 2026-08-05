# -*- coding: utf-8 -*-
"""DE XUAT `cuts.json` tu dong — theo bo luat hoc tu ban dung chuan cua anh Thanh.

    python3 de_xuat_cat.py --job 04-du-an/<ten>            # in de xuat
    python3 de_xuat_cat.py --job <ten> --ghi               # ghi cuts.json
    python3 de_xuat_cat.py --job <ten> --cham              # cham voi ban cua anh

VI SAO: backtest 04/08/2026 cho thay khau CAT la khau te nhat —
`06-magie-canxi` chi trung **61%** moc cat cua anh (8/13). Anh cat them 16 giay
o 7 cho ma toi de lai. Bay cho do khong ngau nhien, xem
`skills/dilim-autocut/references/cat-aroll.md`.

SAU LUAT, may lam duoc 5:

  R1 khoang lang >= 1.5s            (do bang RMS that, khong tin `end` cua whisper)
  R2 tieng dem dung mot minh        "Vang.", "U.", "A."
  R3 vap lap chu ngay canh nhau     "nguoi trung nien ma, MA NGUOI trung nien"
  R4 take lap lai                   giu take SAU (anh noi lai vi lo loi)
  R5 chu noi treo dau doan giu      "Nen anh chi muon..." -> xen

  R6 cau dan bo lung, R7 noi lai bang giong khac — CHUA lam duoc bang may,
  can hieu nghia. De nguoi soat.

MOI DE XUAT DEU KEM `vi_sao` — de nguoi doc con biet duong ma bo.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import unicodedata

LANG_TOI_THIEU = 1.5      # giay
RMS_IM = -45.0            # dB — duoi muc nay coi la im
DEM_MOT_MINH = {"vang", "u", "a", "o", "the", "day", "roi", "dung khong"}


def norm(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.replace("đ", "d"))


def rms(wav, t, d=0.06):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-ss", f"{t:.3f}", "-t", str(d),
                        "-i", wav, "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"mean_volume:\s*(-?[\d.]+)", r.stderr)
    return float(m.group(1)) if m else 0.0


def bien_im(wav, t0, t1):
    """Tim bien IM THAT trong khoang [t0,t1] — quet RMS moi 0.1s.

    Khong dung `end` cua whisper: no keo dai chu de nuot khoang lang phia sau
    (chu "nhung" bi ghi dai 1 giay). Bai hoc 03/08, xem 1_transcribe.py.
    """
    b, e, t = None, None, t0
    while t < t1:
        if rms(wav, t) < RMS_IM:
            if b is None:
                b = t
            e = t + 0.1
        elif b is not None and e is not None and t - e > 0.25:
            break
        t += 0.1
    return (b, e) if b is not None else (None, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    ap.add_argument("--ghi", action="store_true")
    ap.add_argument("--cham", action="store_true")
    a = ap.parse_args()
    import job_path
    job = job_path.job_dir(a.job)
    W = os.path.join(job, "edit/transcripts_words/audio16k.json")
    WAV = os.path.join(job, "edit/audio16k.wav")
    if not os.path.exists(W):
        sys.exit(f"chua co {W}")

    d = json.load(open(W, encoding="utf-8"))
    segs = d["segments"]
    words = [w for s in segs for w in s.get("words", [])]
    cuts = []

    # ---- R1 khoang lang ----
    for x, y in zip(words, words[1:]):
        gap = y["start"] - x["end"]
        if gap < LANG_TOI_THIEU:
            continue
        b, e = (bien_im(WAV, x["end"] - 0.15, y["start"] + 0.05)
                if os.path.exists(WAV) else (x["end"], y["start"]))
        if b is None:
            b, e = x["end"], y["start"]
        if e - b >= LANG_TOI_THIEU - 0.3:
            cuts.append({"t0": round(b, 2), "t1": round(min(e, y["start"]), 2),
                         "why": f"R1 khoang lang {e-b:.1f}s"})

    # ---- R2 tieng dem dung mot minh ----
    for s in segs:
        t = norm(s["text"])
        if t in DEM_MOT_MINH and s["end"] - s["start"] < 2.0:
            ws = s.get("words") or []
            if ws:
                cuts.append({"t0": round(ws[0]["start"], 2),
                             "t1": round(s["end"], 2),
                             "why": f"R2 tieng dem «{s['text'].strip()}»"})

    # ---- R3 vap lap chu ngay canh nhau ----
    for i in range(len(words) - 1):
        a1, a2 = norm(words[i]["word"]), norm(words[i + 1]["word"])
        if a1 and a1 == a2 and len(a1) >= 2:
            cuts.append({"t0": round(words[i]["start"], 2),
                         "t1": round(words[i + 1]["start"], 2),
                         "why": f"R3 vap lap «{words[i]['word'].strip()}»"})

    # ---- R4 take lap lai: cum >=5 tu nghia lap lai trong vong 40s ----
    #
    # SUA sau lan cham dau (trung 25%): 6/9 cho truot deu MUON hon anh 2.0-3.0s.
    # Ly do y het bai hoc caption toi nay — moc roi vao GIUA CUM. Cum lap co the
    # bat dau o giua cau, trong khi anh mo lai tu DAU CAU chua cum do.
    # => snap ca hai dau ve chu MO DAU CUM (chu truoc no ket thuc bang . , ? !).
    DAU = re.compile(r"[.,?!;:]$")

    def dau_cum(i):
        """lui ve chu mo dau cum gan nhat — toi da 12 chu / 4 giay."""
        for k in range(i, max(-1, i - 12), -1):
            if k == 0 or DAU.search(words[k - 1]["word"].strip()):
                if words[i]["start"] - words[k]["start"] <= 4.0:
                    return k
                break
        return i

    N = 5
    seen = {}
    for i in range(len(words) - N):
        key = " ".join(norm(w["word"]) for w in words[i:i + N])
        if len(key) < 12:
            continue
        if key in seen:
            j = seen[key]
            if 0 < words[i]["start"] - words[j]["start"] < 40:
                a0, a1 = dau_cum(j), dau_cum(i)
                if words[a1]["start"] > words[a0]["start"]:
                    cuts.append({"t0": round(words[a0]["start"], 2),
                                 "t1": round(words[a1]["start"], 2),
                                 "why": "R4 take lap — giu take sau: "
                                        f"«{' '.join(w['word'].strip() for w in words[j:j+N])}»"})
        seen.setdefault(key, i)

    # gop cac de xuat chong nhau — NHUNG CO TRAN.
    #
    # Lan cham dau: hai cap lap ke nhau bi gop thanh mot mang 23-24 giay, NUOT
    # LUON moc anh Thanh giu o giua (anh mo lai o 384.27 va 406.53, de xuat gop
    # thanh mot khoi 367->390). Cat qua tay con te hon cat thieu: cat thieu thi
    # anh cat them, cat thua thi mat noi dung.
    TRAN_GOP = 12.0
    cuts.sort(key=lambda c: c["t0"])
    gop = []
    for c in cuts:
        if gop and c["t0"] <= gop[-1]["t1"] + 0.05 \
                and max(c["t1"], gop[-1]["t1"]) - gop[-1]["t0"] <= TRAN_GOP:
            if c["t1"] > gop[-1]["t1"]:
                gop[-1]["t1"] = c["t1"]
                gop[-1]["why"] += " + " + c["why"]
        elif gop and c["t0"] < gop[-1]["t1"]:
            continue                      # nam trong cai truoc, bo qua
        else:
            gop.append(dict(c))
    gop = [c for c in gop if c["t1"] - c["t0"] >= 0.25]

    tong = sum(c["t1"] - c["t0"] for c in gop)
    print(f"{len(gop)} de xuat cat, tong {tong:.1f}s")
    for c in gop:
        print(f"   {c['t0']:7.2f} -> {c['t1']:7.2f}  ({c['t1']-c['t0']:5.2f}s)  {c['why'][:74]}")

    if a.ghi:
        p = os.path.join(job, "cuts_de_xuat.json")
        json.dump(gop, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\n-> {p}   (doi ten thanh cuts.json sau khi soat)")

    if a.cham:
        cham(job, gop)


def cham(job, gop):
    """so moc de xuat voi moc anh Thanh da chot trong draft CapCut."""
    D = os.path.expanduser("~/Movies/CapCut/User Data/Projects/com.lveditor.draft")
    p = os.path.join(D, f"DiLiM - {os.path.basename(job)}", "draft_info.json")
    if not os.path.exists(p):
        print("\n(khong co draft cua anh de cham)")
        return
    dd = json.load(open(p, encoding="utf-8"))
    src = sorted(s.get("source_timerange", {}).get("start", 0) / 1e6
                 for t in dd["tracks"] if t.get("name") == "aroll"
                 for s in t.get("segments", []))
    if len(src) < 2:
        print("\n(draft cua anh dung final.mp4, khong doi chieu duoc moc nguon)")
        return
    de = {round(c["t1"], 1) for c in gop}
    trung = [x for x in src[1:] if any(abs(x - y) <= 0.6 for y in de)]
    print(f"\nCHAM voi ban anh chot: trung {len(trung)}/{len(src)-1} moc mo lai "
          f"({len(trung)*100//max(len(src)-1,1)}%)")
    for x in src[1:]:
        gan = min((abs(x - y), y) for y in de) if de else (99, 0)
        print(f"   anh mo lai o {x:7.2f}  "
              + (f"trung (lech {gan[0]:.2f}s)" if gan[0] <= 0.6
                 else f"KHONG DE XUAT (gan nhat {gan[1]:.2f}, lech {gan[0]:.2f}s)"))


if __name__ == "__main__":
    main()
