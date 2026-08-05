# -*- coding: utf-8 -*-
"""Kho caption dung chung — cum nao viet roi thi khoi viet lai.

    python3 kho_caption.py --gom             # quet moi job, dung lai kho
    python3 kho_caption.py --tra "<loi noi>" # tra thu mot cau
    python3 kho_caption.py --thong-ke

VI SAO KHOA THEO CUM, KHONG THEO CAU (do that tren 381 dong cua 7 job, 04/08/2026):

    tra theo CAPTION da co dong  -> trung 12-19%
    tra theo LOI NOI ca cau      -> trung  1%

Anh Thanh moi lan noi mot khac: dai ngan khac nhau, tu dem khac nhau, va ranh
caption do may chia cung roi vao cho khac. Nen so sanh nguyen cau gan nhu khong
bao gio khop. Nhung Y thi lap that: 124 cum 5 tu co mat o >=2 job, rieng
"de lai ten va so dien thoai" co o 6/7 job.

=> Kho luu CUM NGHIA (chu caption da chot), roi tra bang cach hoi:
   "may tu noi dung cua cum nay co nam trong loi noi moi khong?"

BA MUC AN TOAN — co y lam khac nhau:

  1. `tu_dien_whisper.json` muc `chac_chan`  -> TU DONG SUA. Toan tu khong ton
     tai trong tieng Viet ("sơ vữa", "chết xuất", "bất ngủ") nen khong the sai.
  2. muc `can_kiem`                          -> CHI CANH BAO. Nhung tu co that
     nhung o day chac la nghe nham ("biết tay" -> "đứt tay"). Doi tu dong la
     lieu.
  3. Kho cum                                 -> CHI GOI Y, in ra thanh comment.
     KHONG tu dien. Ly do do duoc: trong 22 cum chu trung nhau giua cac job,
     variant giong nhau 21/22 nhung CLIP chi giong 16/22 — cung mot cau o hai
     bai can hai hinh khac nhau. Va dong nao co CHU SO thi doi tuyet doi phai
     kiem tay: 04/08 anh doc gia sai (28tr790) roi noi lai (31tr080) trong cung
     mot bai.
"""
import argparse
import glob
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))          # thu muc DiLiM-video
KHO = os.path.join(os.path.dirname(HERE), "kho_caption.json")
TUDIEN = os.path.join(os.path.dirname(HERE), "tu_dien_whisper.json")

# Tu de — bo khi so khop, vi chung khong mang nghia. Lay tu 381 dong that.
DEM = {
    "à", "ạ", "ấy", "nhá", "nhé", "này", "thì", "là", "mà", "cái", "có", "của",
    "và", "với", "cho", "được", "nó", "mình", "rồi", "nên", "vì", "ở", "một",
    "các", "những", "cũng", "đang", "sẽ", "đã", "rất", "lại", "ra", "đi", "về",
    "khi", "nếu", "thế", "vậy", "đó", "kia", "trong", "trên", "dưới", "ngay",
    "hay", "hoặc", "chỉ", "thêm", "nữa", "hơn", "quá", "lắm", "đúng", "không",
}


def chuan(s):
    """thuong hoa, bo dau cau, gop khoang trang. GIU DAU tieng Viet."""
    s = (s or "").replace("\n", " ").lower()
    s = re.sub(r"[^\w\sÀ-ỹ]", " ", s)
    return " ".join(s.split())


def tu_nghia(s):
    """chi giu tu MANG NGHIA — bo tu dem."""
    return [w for w in chuan(s).split() if w not in DEM]


def co_so(s):
    return bool(re.search(r"\d", s or ""))


# ---------------------------------------------------------------- tu dien
def nap_tu_dien():
    if not os.path.exists(TUDIEN):
        return {}, {}
    d = json.load(open(TUDIEN, encoding="utf-8"))
    return d.get("chac_chan", {}), d.get("can_kiem", {})


def sua_whisper(text, chac_chan):
    """Ap muc `chac_chan`. Cum DAI thay truoc de khong bi cum ngan an mat."""
    out = text
    for sai in sorted(chac_chan, key=len, reverse=True):
        out = re.sub(re.escape(sai), chac_chan[sai], out, flags=re.IGNORECASE)
    return out


def soi_can_kiem(text, can_kiem):
    """tra ve [(sai, dung, ghi chu)] cho nhung cum CO THE nghe nham."""
    n = chuan(text)
    return [(k, v["dung"], v.get("vi_sao", ""))
            for k, v in can_kiem.items() if chuan(k) in n]


# ---------------------------------------------------------------- kho
def nap():
    if not os.path.exists(KHO):
        return []
    return json.load(open(KHO, encoding="utf-8"))


def tra(said, kho, nguong=0.75, so_ket_qua=3, toi_thieu=3, bo_job=None):
    """Cum nao trong kho NAM TRON trong loi noi nay?

    diem = (so tu nghia cua cum co mat trong loi noi) / (tong tu nghia cua cum)
    Bo qua cum duoi `toi_thieu` tu nghia — ngan hon thi trung ngau nhien.

    `bo_job`: bo qua cum chi den tu job nay. BAT BUOC khi sinh lai khung cho
    mot job DA CO trong kho — khong thi no khop chinh no, diem 1.0, vo nghia.
    """
    co = set(tu_nghia(said))
    if not co:
        return []
    ra = []
    for e in kho:
        tu = e["tu"]
        if len(tu) < toi_thieu:
            continue
        if bo_job and e["job"] == [bo_job]:
            continue
        diem = sum(1 for t in tu if t in co) / len(tu)
        if diem >= nguong:
            ra.append((round(diem, 2), e))
    ra.sort(key=lambda x: (-x[0], -x[1]["lan"]))
    return ra[:so_ket_qua]


def gom():
    """Quet moi 04-du-an/*/edit/plan.json (+ duyet.json neu co) -> kho."""
    gop = {}
    n_job = n_dong = 0
    for f in sorted(glob.glob(os.path.join(ROOT, "04-du-an/*/edit/plan.json"))):
        job = f.split(os.sep)[-3]
        rows = json.load(open(f, encoding="utf-8"))
        n_job += 1

        # duyet.json (neu anh Thanh da cham) -> biet dong nao anh GIU nguyen
        dp = os.path.join(os.path.dirname(f), "..", "duyet.json")
        duyet = {}
        if os.path.exists(dp):
            try:
                duyet = {int(r["idx"]): r
                         for r in json.load(open(dp, encoding="utf-8"))}
            except Exception:
                duyet = {}

        for r in rows:
            d1 = (r.get("d1") or "").strip()
            d2 = (r.get("d2") or "").strip()
            if not d1:
                continue
            tu = tu_nghia(d1 + " " + d2)
            if len(tu) < 2:
                continue
            n_dong += 1
            k = chuan(d1 + " " + d2)
            e = gop.setdefault(k, {
                "chu": d1, "chu2": d2, "tu": tu, "variant": r.get("variant", ""),
                "clip": {}, "job": [], "lan": 0,
                "duyet_giu": 0, "duyet_sua": 0,
                "co_so": co_so(d1 + d2),
            })
            e["lan"] += 1
            if job not in e["job"]:
                e["job"].append(job)
            c = os.path.basename(r.get("path") or "") or "(trống)"
            e["clip"][c] = e["clip"].get(c, 0) + 1

            d = duyet.get(r.get("idx"))
            if d is not None:
                giu = all(str(d.get(fl, r.get(fl, ""))).strip() ==
                          str(r.get(fl, "")).strip()
                          for fl in ("d1", "d2", "variant"))
                e["duyet_giu" if giu else "duyet_sua"] += 1

    kho = sorted(gop.values(), key=lambda e: (-e["lan"], e["chu"]))
    json.dump(kho, open(KHO, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    lap = [e for e in kho if e["lan"] > 1]
    print(f"quet {n_job} job, {n_dong} dong caption")
    print(f"-> {len(kho)} cum trong kho, {len(lap)} cum da dung tu 2 lan tro len")
    print(f"-> {KHO}")
    return kho


def thong_ke(kho):
    print(f"kho: {len(kho)} cum")
    lap = [e for e in kho if e["lan"] > 1]
    print(f"dung >=2 lan : {len(lap)}")
    print(f"co chu so    : {sum(1 for e in kho if e['co_so'])}  (luon phai kiem tay)")
    print(f"anh da duyet : giu {sum(e['duyet_giu'] for e in kho)} · "
          f"sua {sum(e['duyet_sua'] for e in kho)}")
    print(f"\n{'lan':>4}  {'job':>4}  cum")
    for e in lap[:20]:
        c = ", ".join(f"{k} x{v}" for k, v in
                      sorted(e["clip"].items(), key=lambda x: -x[1])[:2])
        print(f"{e['lan']:>4}  {len(e['job']):>4}  {e['chu']}"
              + (f" / {e['chu2']}" if e["chu2"] else ""))
        print(f"              [{e['variant']}] {c}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gom", action="store_true", help="dung lai kho tu moi job")
    ap.add_argument("--tra", metavar="LOI_NOI", help="tra thu mot cau")
    ap.add_argument("--thong-ke", action="store_true")
    ap.add_argument("--nguong", type=float, default=0.75)
    a = ap.parse_args()

    if a.gom:
        kho = gom()
        if a.thong_ke:
            print()
            thong_ke(kho)
        return

    kho = nap()
    if not kho:
        sys.exit("kho rong — chay `--gom` truoc")

    if a.tra:
        cc, ck = nap_tu_dien()
        sua = sua_whisper(a.tra, cc)
        if sua != a.tra:
            print(f"sua whisper: {sua}\n")
        for sai, dung, vs in soi_can_kiem(a.tra, ck):
            print(f"NGO   '{sai}' -> '{dung}'  ({vs})")
        kq = tra(sua, kho, a.nguong)
        if not kq:
            print("khong co cum nao trong kho khop.")
            return
        for diem, e in kq:
            print(f"\n{diem}  dung {e['lan']} lan / {len(e['job'])} job"
                  + ("   [CO CHU SO — kiem tay]" if e["co_so"] else ""))
            print(f"      \"{e['chu']}\"" + (f" / \"{e['chu2']}\"" if e["chu2"] else ""))
            print(f"      variant: {e['variant']}")
            print("      clip da dung: " + ", ".join(
                f"{k} x{v}" for k, v in sorted(e["clip"].items(), key=lambda x: -x[1])))
        return

    if a.thong_ke:
        thong_ke(kho)
        return
    ap.print_help()


if __name__ == "__main__":
    main()
