# -*- coding: utf-8 -*-
"""Bat CUE — neo caption vao DUNG chu no dang noi, roi cho hien som LEAD giay.

VAN DE (anh Thanh chi ra 03/08/2026): truoc day toi UOC LUONG moc `t` bang mat
roi snap vao chu gan nhat — snap chi khoa lai dung cai sai cua minh. Ket qua
caption #7 "VAN DE CHINH / KHONG PHAI HOAT HUYET" hien luc 20.40 trong khi chu
"van" mai 21.78 moi noi: SOM 1.38s.

CACH DUNG: doi chieu CHU trong caption voi chu that trong transcript, tim cua
so khop nhat, roi:
    t0 = start cua chu KHOP DAU TIEN  -  LEAD
Chu hien truoc mieng mot chut de nguoi xem doc kip, dung truoc qua thanh lech.

    python3 anchor.py            # xem truoc
    python3 anchor.py --apply    # ghi de edit/plan.json
"""
import json, os, re, sys, unicodedata
import plan_build

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
PLAN = os.path.join(HERE, "edit/plan.json")
WORDS = os.path.join(HERE, "edit/words_cut.json")

LEAD = 0.50          # hien truoc chu dau tien bao nhieu giay (anh chot 0.5s)
SEARCH = 7.0         # chi tim quanh moc cu +-7s, tranh vo phai cho lap tu
MIN_DUR = 0.80


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s.replace("đ", "d"))


# tu qua pho bien -> khong dung de neo (de khop nham)
STOP = {norm(x) for x in ("la", "va", "co", "cua", "cho", "thi", "ma", "o", "den",
                          "khi", "nen", "voi", "mot", "nay", "do", "duoc", "trong")}


def content_words(text):
    out = []
    for w in re.split(r"[\s,.\n]+", text.replace("*", "")):
        n = norm(w)
        if n and n not in STOP:
            out.append(n)
    return out


# ---- DAU CAU: mot chu la "MO DAU CUM" neu chu NGAY TRUOC no ket thuc bang
#      . , ? ! ; :  (hoac no la chu dau bai).
#
# ANH THANH CHI RA 04/08/2026 (toi): caption o 2:53 lech nhip — "text bi keo o
# duoi chu phat am doan sau chu khong phai phat am doan dau". Anh doan hai kha
# nang, va CA HAI DEU DUNG:
#   1. moc chia nhip chua sat dau cau  -> da sua o `make_plan_draft.group()`
#      bang `ngat_cum.diem_ranh` (do tren job 06: 27% -> 67% nhip bat dau dung
#      dau cum)
#   2. buoc neo khong phan biet dau cau -> chinh la ham nay
#
# Whisper CO tra ve dau cau, gan lien vao chu (' khong?', ' nha,', ' benh.'),
# va no song sot toi tan `words_cut.json` (202/1276 chu cua job 06 co dau).
# Nhung `norm()` o tren xoa sach dau cau bang `re.sub(r"[^a-z0-9]", "")`, nen
# tu truoc toi gio ham neo CHUA TUNG NHIN THAY mot dau phay nao.
DAU_CAU = re.compile(r"[.,?!;:]$")


def mo_dau_cum(words):
    return [True] + [bool(DAU_CAU.search(words[i - 1]["w"].strip()))
                     for i in range(1, len(words))]


SNAP_CHU = 3         # chi nhich toi da 3 chu
SNAP_GIAY = 0.7      # va toi da 0.7 giay


def snap_dau_cum(i, mo, words):
    """Neo dang o GIUA cum -> nhich ve chu MO DAU CUM gan nhat, NEU rat gan.

    Co y lam CUC BO. Ban dau toi cho no uu tien dau cum tren toan cua so tim
    kiem — do lai thi neo bi keo lui toi 3.8 giay va nhay sang chu khac han
    ("LO CAI DUONG ONG" tu 'lo' sang 'di'). Ngoai 3 chu / 0.7 giay thi cai
    "dau cum" gan nhat thuong la mot CAU KHAC, khong phai cau dang noi.
    """
    if mo[i]:
        return i
    for k in range(max(0, i - SNAP_CHU), i):
        if mo[k] and words[i]["s"] - words[k]["s"] <= SNAP_GIAY:
            return k
    return i


def main():
    plan = json.load(open(PLAN, encoding="utf-8"))
    words = json.load(open(WORDS, encoding="utf-8"))
    wn = [norm(w["w"]) for w in words]
    mo = mo_dau_cum(words)

    anchors = []
    for r in plan:
        want = content_words(r["text"])
        if not want:
            anchors.append((r["t"], 0, "khong co tu de neo"))
            continue
        best = None
        for i in range(len(words)):
            if abs(words[i]["s"] - r["t"]) > SEARCH:
                continue
            # dem bao nhieu tu cua caption xuat hien THEO THU TU tu vi tri i
            j, hit = i, 0
            for t in want:
                k = j
                while k < min(len(words), i + len(want) * 4):
                    if wn[k] == t:
                        hit += 1
                        j = k + 1
                        break
                    k += 1
            # THEM 04/08: chu MO DAU CUM chi dung de PHA HOA, KHONG cong vao diem.
            #
            # Ban dau toi cong 0.12 thang vao `score` — do lai thi HONG: chu khop
            # kem nhung dung dau cum thang nguoc chu khop dung. Caption "LO CAI
            # DUONG ONG" nhay tu 'lo' sang 'di' (-3.8s), "Q10 CO 2 DANG" tu '2'
            # sang 'no'. So caption neo duoc con tut 95 -> 91.
            # Do khop van la vua; dau cum chi len tieng khi hai ung vien BANG diem.
            score = hit / len(want)
            if best is None or score > best[0] or (score == best[0]
                                                   and abs(words[i]["s"] - r["t"]) < abs(words[best[1]]["s"] - r["t"])):
                if wn[i] == want[0] or score > 0:
                    best = (score, i)
        if best and best[0] >= 0.5 and wn[best[1]] == want[0]:
            idx = snap_dau_cum(best[1], mo, words)
            anchors.append((words[idx]["s"], best[0], words[idx]["w"]))
        elif best and best[0] >= 0.5:
            # khong khop dung tu dau -> tim chu dau tien khop duoc.
            #
            # LOI CU: vong nay chi do VE PHIA SAU (`range(best[1], best[1]+12)`),
            # khong bao gio lui. Nen moi lan truot la truot MUON, lech mot chieu
            # — dung trieu chung anh Thanh ta. Gio do CA HAI CHIEU nhung PHAI
            # khop dung chu dau cua caption, va van bi gioi han o `snap` phia sau.
            cand = [k for k in range(max(0, best[1] - 6),
                                     min(len(words), best[1] + 12))
                    if wn[k] == want[0]]
            idx = min(cand, key=lambda k: abs(k - best[1])) if cand else best[1]
            idx = snap_dau_cum(idx, mo, words)
            anchors.append((words[idx]["s"], best[0], words[idx]["w"]))
        else:
            # DO GAN DUNG: caption cua minh la ban DA SUA loi nghe cua whisper
            # (vd "MANG XO VUA" trong khi whisper ra "ban so vua") nen khop
            # nguyen van that bai. Neo tam vao chu nao GIONG NHAT trong cua so.
            def sim(a, b):
                if a == b: return 1.0
                n = 0
                for x, y in zip(a, b):
                    if x != y: break
                    n += 1
                return n / max(len(a), len(b))
            cands = []
            for i, w in enumerate(words):
                if abs(w["s"] - r["t"]) > SEARCH: continue
                sc = max(sim(wn[i], t) for t in want)
                if sc >= 0.55: cands.append((w["s"], sc, w["w"]))
            if cands:
                cands.sort(key=lambda c: (-c[1], abs(c[0] - r["t"])))
                # lay chu KHOP TOT NHAT roi lui ve chu som nhat cung cum
                best_s = cands[0][0]
                early = min((c for c in cands if c[1] >= cands[0][1] - 0.15
                             and abs(c[0] - best_s) < 2.5), key=lambda c: c[0])
                anchors.append((early[0], early[1], early[2] + " (dò gần đúng)"))
            else:
                anchors.append((r["t"], 0.0, "KHONG NEO DUOC — giu moc cu"))

    # t0 = neo - LEAD ; t_end = t0 cua caption ke tiep
    new_t = [max(0.0, a - LEAD) if s > 0 else a for a, s, _ in anchors]
    for i in range(1, len(new_t)):                     # khong cho lui qua caption truoc
        new_t[i] = max(new_t[i], new_t[i - 1] + MIN_DUR)
    end_all = max(w["s"] for w in words) + 1.2

    print(f"{'#':>3} {'cu':>7} {'moi':>7} {'lech':>7}  {'khop':>5}  neo vao chu")
    print("-" * 78)
    big = 0
    for i, (r, (a, sc, wtxt)) in enumerate(zip(plan, anchors)):
        d = new_t[i] - r["t"]
        if abs(d) > 0.4:
            big += 1
        print(f"{r['idx']:3} {r['t']:7.2f} {new_t[i]:7.2f} {d:+7.2f}  {sc*100:4.0f}%  {wtxt}")
    print(f"\n{big}/{len(plan)} caption lech qua 0.4s so voi truoc")

    if "--apply" in sys.argv:
        for i, r in enumerate(plan):
            r["t"] = round(new_t[i], 2)
            r["t_end"] = round(new_t[i + 1] if i + 1 < len(new_t) else end_all, 2)
            r["from"] = None
            r["anchor_word"] = anchors[i][2]
            r["anchor_score"] = round(anchors[i][1], 2)
            # neo doi `t` -> phai tinh lai luc CHU tat, khong thi cap_end cu
            # nam ngoai [t, t_end] (26/92 dong bi vay khi moi them 06/08).
            if "cap_end" in r:
                r["cap_end"] = round(
                    plan_build.het_chu(r["t"], r["t_end"], r["text"]), 2)
        json.dump(plan, open(PLAN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"\n-> da ghi de {PLAN}")
    else:
        print("\n(xem truoc — them --apply de ghi)")


if __name__ == "__main__":
    main()
