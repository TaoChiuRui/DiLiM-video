# -*- coding: utf-8 -*-
"""Dung `edit/plan.json` tu bang R trong `<job>/plan.py`.

TRUOC 04/08/2026 moi job CHEP nguyen ~60 dong logic nay vao plan.py cua no.
Gio de o day — plan.py chi con BANG R + 3 dong goi. Cac job cu van chay duoc
vi ban chep cua chung con nguyen; khong dong vao chung.

Dung trong plan.py:

    from plan_build import build
    build(HERE, R)

Viec no lam:
  1. SNAP moc `t` uoc luong vao `start` cua chu gan nhat (khong bao gio dung
     `end` cua whisper — no nuot ca khoang lang phia sau, xem 1_transcribe.py).
  2. `t_end` = `t` cua caption ke tiep, caption cuoi keo den het bai.
  3. Clip ngan hon caption -> tu lui `src_start` neu clip DU dai.
  4. Clip ngan hon CA caption -> bo trong lop B-roll va bao (mac dinh).
     Truyen `fallback=<duong dan anh>` neu muon tu doi sang anh do thay vi bo.
     MAC DINH LA BO, khong doi: ban cu tu doi sang anh san pham da mot lan gan
     nham caption "mach mau thong thoang" vao anh 2 hop (VERSION.md v1.2).
"""
import json
import os
import subprocess

# PHAI GIONG clips.IMG_EXT. Thieu ".webp" o day tu 05/08 den 07/08: kho co
# dung 1 file .webp (anlanh-anh-nghe-cu-02.webp) — plan_build coi no la VIDEO,
# ffprobe tra "N/A" -> dai 0.0s -> "ngan hon caption" -> **BO TRONG lang le**.
# Chua job nao dung file do nen loi nam im. Bat duoc khi test o T7 07/08/2026.
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".JPG", ".PNG", ".WEBP")

MIN_DUR = 0.80        # caption ngan nhat cho phep
LEAD_IN = 0.06        # bat som hon chu dau mot chut cho de doc

# --- GIU CHU (them 06/08/2026) --------------------------------------------
# Anh Thanh 06/08: *"tôi thấy bạn dùng vẫn full dòng caption... cắt bớt được
# một cách logic không?"*. Goc van de KHONG nam o so dong — no nam o dong 2
# cua docstring: `t_end` = `t` cua caption ke tiep. Nghia la chu PHU 100%
# thoi luong, khong bao gio co mot giay nao man hinh sach. Xoa bot dong chi
# lam dong TRUOC PHINH RA (8-13s), khong tao khoang tho.
#
# Gio caption hien DU LAU DE DOC roi tat, cho toi caption sau. B-roll van
# chay lien mach theo `t_end` cu — chi lop CHU la ngat quang.
GIU_MAX  = 7.0    # chu dung im lau hon nay thi mat chan — soi_plan bao tu 8s
GIU_MIN  = 1.6    # ngan hon nay thi khong kip doc
NHAY     = 0.30   # khoang sach giua 2 caption: du de mat biet la CHU MOI


def het_chu(t0, t1, txt=""):
    """Luc CHU tat. Anh Thanh 06/08 (vong 2): *"chu de dai hon chut a, dai den
    sat cai caption sau cung duoc — vi minh dang noi y key ma"*.

    Nen KHONG con tinh theo thoi gian doc nua (ban 06/08 sang: 0.9 + n/14,
    ra 65% chu tren man — anh thay chu tat qua som). Gio giu toi SAT dong sau,
    chi chua `NHAY` giay. Chan tren `GIU_MAX` de khong co dong nao dung im
    ca chuc giay o nhung cho anh ngung noi lau.
    """
    het = min(t1 - NHAY, t0 + GIU_MAX)
    return t1 if het - t0 < GIU_MIN else het


_dur_cache = {}


def _dur(path):
    if path not in _dur_cache:
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                            "format=duration", "-of", "csv=p=0", path],
                           capture_output=True, text=True)
        try:
            _dur_cache[path] = float(r.stdout.strip())
        except ValueError:
            _dur_cache[path] = 0.0
    return _dur_cache[path]


def build(here, R, fallback=None, min_dur=MIN_DUR, lead_in=LEAD_IN, giu=False):
    """here = thu muc job. R = list tuple 7 phan tu. -> ghi edit/plan.json"""
    words = json.load(open(os.path.join(here, "edit/words_cut.json"),
                           encoding="utf-8"))
    end_all = max(w["s"] for w in words) + 1.2

    starts = []
    for t, *_ in R:
        cand = min(words, key=lambda w: abs(w["s"] - t))
        starts.append(max(0.0, cand["s"] - lead_in))

    rows, probs, fixed, swapped = [], [], [], []
    for i, ((t, d1, d2, var, p, ss, note), t0) in enumerate(zip(R, starts), 1):
        t1 = starts[i] if i < len(starts) else end_all
        if t1 - t0 < min_dur:
            probs.append(f"caption {i}: chi {t1-t0:.2f}s (<{min_dur}s)")
        txt = d1 + ("\n" + d2 if d2 else "")
        if txt.count("*") % 2:
            probs.append(f"caption {i}: dau * le")
        if not var:
            probs.append(f"caption {i}: THIEU variant — se roi vao vong xoay "
                         f"mau ngau nhien, phai dien")

        if p:
            if not os.path.exists(p):
                probs.append(f"caption {i}: KHONG TIM THAY {os.path.basename(p)}")
            elif not p.endswith(IMG_EXT):
                dur, need = _dur(p), t1 - t0
                if dur - ss < need - 0.03:
                    if dur >= need:
                        ss = round(max(0.0, dur - need), 2)
                        fixed.append(f"caption {i}: lui src_start -> {ss} "
                                     f"({os.path.basename(p)})")
                    elif fallback:
                        swapped.append(f"caption {i}: {os.path.basename(p)} chi "
                                       f"{dur:.1f}s < {need:.1f}s -> "
                                       f"{os.path.basename(fallback)}")
                        p, ss = fallback, 0
                    else:
                        swapped.append(f"caption {i}: {os.path.basename(p)} chi "
                                       f"{dur:.1f}s < {need:.1f}s -> BO TRONG "
                                       f"(tim clip khac, dung de may tu doi)")
                        p, ss = "", 0

        # cap_end = luc CHU tat. Mac dinh bang t_end (hanh vi cu, cac job truoc
        # 06/08 khong doi). Bat `giu=True` thi chu chi o lai du lau de doc.
        cap_end = het_chu(t0, t1, txt) if giu else t1

        said = " ".join(w["w"] for w in words if t0 - 0.05 <= w["s"] < t1 - 0.05)
        rows.append({"idx": i, "t": round(t0, 2), "t_end": round(t1, 2),
                     "cap_end": round(cap_end, 2),
                     "d1": d1, "d2": d2, "text": txt, "variant": var,
                     "path": p, "src_start": ss, "note": note, "said": said,
                     "snap_drift": round(t0 - t, 2)})

    out = os.path.join(here, "edit/plan.json")
    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    have = sum(1 for r in rows if r["path"])
    print(f"caption   : {len(rows)}")
    print(f"co B-roll : {have}   |  de trong: {len(rows)-have}")
    print(f"phu song  : {rows[0]['t']:.2f} -> {rows[-1]['t_end']:.2f}s")
    if giu:
        tong = rows[-1]["t_end"] - rows[0]["t"]
        chu = sum(r["cap_end"] - r["t"] for r in rows)
        ngat = sum(1 for r in rows if r["cap_end"] < r["t_end"] - 0.01)
        print(f"chu tren man: {chu:.0f}s / {tong:.0f}s = {chu/tong*100:.0f}%"
              f"   ({ngat}/{len(rows)} caption tat som, con lai khoang tho)")
    print(f"snap lech : max {max(abs(r['snap_drift']) for r in rows):.2f}s")
    print(f"-> {out}")
    for x in fixed + swapped:
        print("   *", x)
    if probs:
        print("\n!!! CAN XEM LAI:")
        for x in probs:
            print("   ", x)
    else:
        print("\nKhong co loi.")
    return rows
