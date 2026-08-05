# -*- coding: utf-8 -*-
"""Do VUNG HONG trong mot clip dai — chu de len, fade den, logo outro.

    python3 do_doan.py --clip CUC_MAU
    python3 do_doan.py --clip MO_HEP --buoc 0.25
    python3 do_doan.py --dai            # moi clip dai hon 30s da khai

VI SAO: clip stock y khoa hay co chu tieng Anh (PLATELET, FIBRIN...) va logo
hang o cuoi. `cuc-mau-dong.mp4` — clip dung NHIEU NHAT kho — co chu o 14-20.5s,
22-28.5s, 31-38.5s va logo tu 45.5s. Sau job da dung dung vao vung do.

Do bang so, khong nhin mat:
  - CHU  : % pixel rat sang o goc tren-trai (chu stock gan nhu luon o day)
  - DEN  : do sang trung binh ca khung tut xuong (fade/outro)

May chi CHI CHO. Van phai mo xem frame that truoc khi tin.
"""
import argparse
import io
import os
import subprocess
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import clips as C   # noqa: E402

NGUONG_CHU = 1.0     # % pixel rat sang o vung nghi, TRU vung doi chung
NGUONG_DEN = 25.0    # do sang trung binh ca khung
SANG = 240           # nguong "trang nhu chu", khong phai "nen sang"

# BAY DA SAP MOT LAN (04/08): chi dem pixel sang o goc tren-trai thi clip NEN
# SANG (nguoi ngoi truoc cua so, mo hinh tren nen trang) bi bao nham la "chu de
# gan het clip". Cach chua: do them mot VUNG DOI CHUNG o goc duoi-phai — cho
# thuong khong co chu. Nen sang thi CA HAI cung cao va hieu so ~0; chu that thi
# chi vung tren-trai cao. Diem so = hieu, khong phai tri tuyet doi.


def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", p],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def do(p, ss):
    """-> (diem_chu, do_sang_trung_binh)

    Chia khung thanh luoi 4x3, do %trang tung o.
      diem_chu = o_sang_nhat - trung_vi_cac_o
    Chu overlay chi chiem vai o -> hieu lon. Nen sang deu -> moi o cung cao ->
    hieu ~0. Bat duoc chu o BAT KY vi tri nao, khong chi goc tren-trai.

    BAY DA SAP HAI LAN (04/08):
      1. chi dem pixel sang -> clip nen sang bao nham "chu de gan het clip"
      2. chi soi goc tren-trai -> BO SOT chu o giua khung (`MO_HEP` co dong
         "Atherosclerotic plaque disruption...", `XV_DAI` co "Arteriosclerosis
         (Hardening of the arteries)" — deu nam giua/duoi, khong phai goc)
    """
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(ss), "-i", p,
                        "-frames:v", "1", "-vf", "scale=640:-1",
                        "-f", "image2", "-c:v", "png", "-"], capture_output=True)
    if not r.stdout:
        return None, None
    im = Image.open(io.BytesIO(r.stdout)).convert("L")
    w, h = im.size
    COLS, ROWS = 4, 3
    o = []
    for r_ in range(ROWS):
        for c in range(COLS):
            box = (c * w // COLS, r_ * h // ROWS,
                   (c + 1) * w // COLS, (r_ + 1) * h // ROWS)
            px = list(im.crop(box).getdata())
            o.append(sum(1 for v in px if v > SANG) * 100.0 / len(px))
    o.sort()
    trung_vi = o[len(o) // 2]
    return o[-1] - trung_vi, sum(im.getdata()) / (w * h)


def khoang(marks, key, nguong, tren=True):
    runs, cur = [], None
    for ss, v in marks:
        xau = (v >= nguong) if tren else (v <= nguong)
        if xau and cur is None:
            cur = ss
        elif not xau and cur is not None:
            runs.append((cur, ss))
            cur = None
    if cur is not None:
        runs.append((cur, marks[-1][0]))
    return runs


NEN_SANG = 90.0   # do sang trung binh — tren muc nay coi la clip NEN SANG


def quet(ten, p, buoc):
    d = dur(p)
    print(f"\n=== {ten}  {os.path.basename(p)}  {d:.1f}s ===")
    marks_chu, marks_den = [], []
    ss = 0.0
    while ss < d:
        a, b = do(p, ss)
        if a is None:
            break
        marks_chu.append((ss, a))
        marks_den.append((ss, b))
        ss += buoc
    # CHOT CHAN: heuristic "o sang nhat troi hon phan con lai" chi dung voi clip
    # NEN TOI + chu trang (stock y khoa). Voi clip nen sang — nguoi ngoi truoc
    # cua so, mo hinh trang tren nen trang — vat the sang tu no da lam mot o
    # troi len, va may bao nham "chu de gan het clip". Da sap bay nay 2 lan.
    tb = sum(v for _, v in marks_den) / max(1, len(marks_den))
    if tb > NEN_SANG:
        print(f"  KHONG KET LUAN DUOC — clip nen sang (do sang tb {tb:.0f}).")
        print("  Cach do nay chi dung voi clip nen toi. Phai tu mo xem frame.")
        return

    chu = khoang(marks_chu, "chu", NGUONG_CHU, True)
    den = khoang(marks_den, "den", NGUONG_DEN, False)
    hong = sorted(chu + den)
    if not hong:
        print("  khong thay vung hong — dung ca clip")
        return
    for a, b in chu:
        print(f"  CHU ĐÈ    {a:6.1f}s → {b:6.1f}s")
    for a, b in den:
        print(f"  ĐEN/LOGO  {a:6.1f}s → {b:6.1f}s")
    # vung sach = phan bu
    sach, t = [], 0.0
    for a, b in hong:
        if a - t > 1.0:
            sach.append((t, a))
        t = max(t, b)
    if d - t > 1.0:
        sach.append((t, d))
    print("  --- DÙNG ĐƯỢC ---")
    for a, b in sach:
        print(f"  {a:6.1f}s → {b:6.1f}s   ({b-a:.1f}s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--clip", help="ten hang so trong clips.py")
    ap.add_argument("--dai", action="store_true", help="moi clip >30s")
    ap.add_argument("--buoc", type=float, default=0.5)
    a = ap.parse_args()

    paths = {k: v for k, v in vars(C).items()
             if k.isupper() and isinstance(v, str) and v.startswith("/Volumes")
             and os.path.isfile(v) and not v.lower().endswith(C.IMG_EXT)}
    if a.clip:
        if a.clip not in paths:
            sys.exit(f"khong co hang so {a.clip}")
        quet(a.clip, paths[a.clip], a.buoc)
    elif a.dai:
        for k, v in sorted(paths.items()):
            if dur(v) > 30:
                quet(k, v, a.buoc)
    else:
        sys.exit("can --clip hoac --dai")


if __name__ == "__main__":
    main()
