# -*- coding: utf-8 -*-
"""GOI Y B-ROLL v2 — tra ve CLIP KEM GIAY AN TOAN, khong chi ten file.

    python3 goi_y_broll.py --job <ten>            # in goi y
    python3 goi_y_broll.py --job <ten> --md       # ghi edit/goi_y_broll.md
    python3 goi_y_broll.py --tra "mach mau bi hep"

KHAC `suggest_clips.py` (v1) o ba diem:

  1. v1 tra ve TEN FILE. Nguoi van phai tu doan `src_start`. Day la cho de ra
     16 loi vung cam o 5 job — chon dung clip, sai giay.
     v2 doc `kho_broll.json` roi tra ve GIAY BAT DAU nam TRON trong doan sach.
  2. v1 chi tra `clips.TAGS` — tu khoa go tay, 3-5 tu moi clip. Job 06 co
     38/99 dong "KHONG TRA RA GI".
     v2 tra them **341 tu khoa hoc tu 381 dong da dung** (`hoc_lich_su.py`).
  3. v1 xep hang theo so tu khoa trung. v2 cong them **ti le song sot** —
     clip nao hay bi anh Thanh bo thi tut hang.

VAN GIU LUAT CU: may khong hieu clip quay gi. Day la GOI Y, khong phai quyet
dinh. Khong co gi khop that thi de trong con hon nhet clip sai y.
"""
import argparse
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(os.path.dirname(HERE))
KHO = os.path.join(os.path.dirname(HERE), "kho_broll.json")

DEM = {"la", "va", "co", "cua", "cho", "thi", "ma", "o", "den", "khi", "nen",
       "voi", "mot", "nay", "do", "duoc", "trong", "cac", "nhung", "cai", "no",
       "minh", "roi", "vi", "cung", "dang", "se", "da", "rat", "lai", "ra",
       "di", "ve", "hay", "hoac", "chi", "them", "nua", "hon", "qua", "lam",
       "anh", "chi", "co", "chu", "thanh"}


def norm(s):
    s = unicodedata.normalize("NFD", (s or "").lower())
    s = "".join(c for c in s if not unicodedata.combining(c)).replace("đ", "d")
    return re.sub(r"[^a-z0-9\s]", " ", s)


def tu(s):
    return {w for w in norm(s).split() if w and w not in DEM and len(w) > 1}


DANH_MUC = os.path.join(os.path.dirname(HERE), "danh_muc_kho.json")


def nap():
    """Gop HAI nguon, uu tien ban DA SOI.

      kho_broll.json   ~159 clip da OCR — co `doan_dung_duoc` (giay nao sach)
      danh_muc_kho.json ~1048 clip — chi co `mo_ta` dich tu ten file

    Truoc 05/08/2026 chi doc nguon dau, nen 874 clip trong kho khong bao gio
    duoc goi y: do 9 job chi xoay quanh 86 clip (8% kho), rieng
    `richnatto-01.mp4` gong 30 luot. Gop vao thi may THAY het kho.

    DANH DAU `chua_soi=True` cho clip chua OCR — chung KHONG co `doan_dung_duoc`
    nen `giay_an_toan` tra ve 0.0, tuc src_start=0. Do dung la cho de ra loi
    "chu tieng Anh / man den" (16 dong sai o 5 job). Vi vay ban goi y in kem
    canh bao CHUA SOI de nguoi con soi frame truoc khi chot.
    """
    kho = []
    if os.path.exists(KHO):
        kho = json.load(open(KHO, encoding="utf-8"))
    da_co = {x["file"] for x in kho}
    if os.path.exists(DANH_MUC):
        for m in json.load(open(DANH_MUC, encoding="utf-8")):
            if m["file"] in da_co:
                continue
            kho.append({**m, "chua_soi": True, "doan_dung_duoc": None})
    if not kho:
        sys.exit(f"chua co {KHO} lan {DANH_MUC} — chay xay_danh_muc.py --ghi truoc")
    return kho


def tu_khoa_cua(x, TAGS):
    """tu khoa cua mot clip = TAGS go tay + tu khoa hoc tu lich su."""
    t = set()
    for k, v in TAGS.items():
        if os.path.basename(k) == x["file"]:
            for w in v:
                t |= tu(w)
    # TU KHOA THEO NHOM — ap theo tien to ten file (xem clips.TAGS_NHOM).
    # Do 05/08/2026: khong co bang nay thi 872 clip moi chi ~7.7 tu khoa so voi
    # 17.4 cua clip cu, nen hang 1 den tu clip cu 530/531 lan. Khai them 869
    # clip ma khong doi duoc gi.
    try:
        import clips as _C
        _pre = x["file"].split("-")[0]
        for w in getattr(_C, "TAGS_NHOM", {}).get(_pre, ()):
            t |= tu(w)
    except Exception:
        pass
    t |= {w for w in x.get("tu_khoa_hoc", [])}
    # TANG 3: mo ta bang chu — thu duy nhat cho biet clip QUAY CAI GI.
    # Do 05/08: chi dung tu khoa (TAGS + hoc tu lich su) thi goi y so 1 chi
    # trung 11% khi khong cho nhin chinh job do. Tu khoa khong thay duoc mat.
    t |= tu(x.get("mo_ta") or "")
    return t


def giay_an_toan(x, can):
    """giay bat dau nam TRON trong mot doan sach du dai cho caption."""
    for a, b in x.get("doan_dung_duoc") or []:
        if b - a >= can:
            return round(a, 1)
    # khong doan nao du dai -> lay doan dai nhat, bao ro la hut
    ds = x.get("doan_dung_duoc") or []
    if ds:
        a, b = max(ds, key=lambda v: v[1] - v[0])
        return round(a, 1)
    return 0.0


_IDF = {}


def idf(kho, TAGS):
    """tu cang HIEM cang dang gia.

    Lan do dau: goi y phu 98% dong — nhung phan lon khop bang tu vo nghia
    (`ai`, `it`, `noi`, `dung`, `thieu`) co mat o hang chuc clip. Phu cao ma
    goi y rac thi te hon phu thap. Cham diem theo log(N/df) — tu co o 40 clip
    gan nhu khong duoc diem, tu chi co o 2 clip thi duoc nhieu.
    """
    if _IDF:
        return _IDF
    import math
    df = {}
    for x in kho:
        for w in tu_khoa_cua(x, TAGS):
            df[w] = df.get(w, 0) + 1
    N = max(1, len(kho))
    for w, c in df.items():
        _IDF[w] = math.log(N / c)
    return _IDF


def tra(chu, kho, TAGS, can=4.0, n=4, nguong=1.2):
    q = tu(chu)
    if not q:
        return []
    W = idf(kho, TAGS)
    ra = []
    for x in kho:
        if x.get("anh"):
            hop = 99.0
        else:
            dd = x.get("doan_dung_duoc")
            # LOI DA VAP 05/08/2026: `dd == []` nghia la DA SOI va CAM TRON CLIP
            # (vi du `noitang-dady-boc-mo-01.mp4`: ca 9.4s deu co chu tieng Anh
            # "IT SURROUNDS / INTERFERING WITH DIGESTION!"). Truoc khi va, clip
            # nay dung DAU BANG goi y voi src_start=0.0 — dung frame co chu.
            # Do la y het ho loi 16 dong sai o 5 job.
            #   dd == []   -> da soi, hong han  -> LOAI
            #   dd is None -> chua soi          -> giu, in co CHUA SOI
            if dd == []:
                continue
            hop = max([b - a for a, b in (dd or [])], default=0.0)
        tk = tu_khoa_cua(x, TAGS)
        trung = q & tk
        if not trung:
            continue
        diem = sum(W.get(w, 0.0) for w in trung)
        if diem < nguong:
            continue                          # chi khop tu vo nghia -> bo
        # thuong cho clip hay duoc GIU lai sau khi anh Thanh sua
        cd, dd = x.get("co_ban_doi_chieu", 0), x.get("con_lai_sau_khi_anh_sua", 0)
        if cd:
            diem += 1.5 * (dd / cd)
        if hop < can:
            diem -= 2.0                       # khong con doan nao du dai
        if x.get("doc"):
            diem -= 3.0                       # clip DOC khong dung cho dai ngang
        ra.append((round(diem, 2), sorted(trung), x, round(hop, 1)))
    ra.sort(key=lambda r: -r[0])
    return ra[:n]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job")
    ap.add_argument("--tra")
    ap.add_argument("--md", action="store_true")
    a = ap.parse_args()
    import clips as C
    kho = nap()

    if a.tra:
        for d, t, x, hop in tra(a.tra, kho, C.TAGS):
            print(f"{d:6.2f}  {x['file'][:40]:40} khop: {','.join(t)}")
            print(f"        doan sach: {x.get('doan_dung_duoc')}  "
                  f"-> bat tu giay {giay_an_toan(x, 4.0)}")
        return

    import job_path
    if not a.job:
        sys.exit("thieu --job hoac --tra")
    job = job_path.job_dir(a.job)
    plan = json.load(open(os.path.join(job, "edit/plan.json"), encoding="utf-8"))

    out, n_co = [], 0
    for r in plan:
        can = r["t_end"] - r["t"]
        kq = tra(r["d1"] + " " + r["d2"], kho, C.TAGS, can=can)
        txt = r["d1"] + (" / " + r["d2"] if r["d2"] else "")
        out.append(f"\n#{r['idx']:3} {r['t']:7.2f}s ({can:.1f}s)  {txt}")
        out.append(f"      nói: {r.get('said','')[:76]}")
        if not kq:
            out.append("      — khong tra ra gi")
            continue
        n_co += 1
        for d, t, x, hop in kq:
            ss = giay_an_toan(x, can)
            canh = "" if hop >= can else f"  [doan sach dai nhat chi {hop}s]"
            if x.get("chua_soi"):
                canh += "  [CHUA SOI — soi frame truoc khi chot src_start]"
            out.append(f"      {d:5.2f} {x['file'][:38]:38} src_start={ss:<6} "
                       f"({','.join(t[:4])}){canh}")

    head = (f"# Goi y B-roll v2 — {a.job}\n\n"
            f"{n_co}/{len(plan)} dong co goi y ({n_co*100//len(plan)}%).\n"
            f"`src_start` da nam TRON trong doan sach (khong co chu/man den).\n")
    s = head + "\n".join(out) + "\n"
    if a.md:
        p = os.path.join(job, "edit/goi_y_broll.md")
        open(p, "w", encoding="utf-8").write(s)
        print(f"{n_co}/{len(plan)} dong co goi y ({n_co*100//len(plan)}%)")
        print(f"-> {p}")
    else:
        print(s)


if __name__ == "__main__":
    main()
