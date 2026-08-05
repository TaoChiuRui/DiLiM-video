# -*- coding: utf-8 -*-
"""Xay KHO B-ROLL — index theo DOAN, khong theo file.

    python3 xay_kho_broll.py            # chay tiep, bo qua clip da lam
    python3 xay_kho_broll.py --lam-lai  # lam lai tu dau
    python3 xay_kho_broll.py --clip natto-01.mp4

VI SAO CO FILE NAY (04/08/2026):
`clips.py` la DANH BA: hang so -> duong dan -> tu khoa go tay. No biet
`CUC_MAU` la file nao, KHONG biet trong file do co gi o giay 20. Ma mot clip
50 giay thi giay 5 va giay 20 ke hai chuyen khac han, va co the co chu tieng
Anh chay vao hinh.

Hau qua do duoc: 157 clip khai trong TAGS, chi 4 clip co `VUNG_CAM`. 153 clip
CHUA AI NHIN. Test 04/08 tim ra 16 dong o 5 job dang hien `PLATELET`,
`RED BLOOD CELL`, `Buildup of plaque...` hoac man den tren dai B-roll.

BA TANG, hai tang dau MAY TU LAM:
  1. OCR tung frame bang macOS Vision -> biet chinh xac giay nao co chu.
     (da doi chieu: tai tao dung y bang VUNG_CAM lam tay, khong sai cho nao)
  2. Do doi canh (ffmpeg scene detect) -> cat clip dai thanh cac DOAN co moc that.
  3. Mo ta bang chu — nguoi/agent nhin MOT frame moi doan. Lam sau, file nay
     chua san cho `mo_ta`.

Ra `03-tool-capcut/kho_broll.json`.
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clips as C                                                # noqa: E402

KHO = os.path.join(os.path.dirname(HERE), "kho_broll.json")
OCR = os.path.join(HERE, "bin", "ocr")

BUOC = 1.5          # giay — lay mau moi 1.5s
MAX_FRAME = 80      # clip qua dai thi cung chi lay bay nhieu
SCENE_MIN = 20.0    # clip dai hon nguong nay moi do doi canh
SCENE_NGUONG = 0.30

# --- PHAN BIET WATERMARK VOI CHU THAT: dung TAN SUAT, khong dung danh sach tu ---
#
# Ban dau toi loc bang regex `helix|animation|...`. HONG: Vision doc logo
# "Helix Animation" ra moi frame mot kieu — `Helis`, `Heliy`, `Helz`, `Hells`,
# `ANINATIO`, `ANIMATE` — regex truot het, va vung cam bi gop tu 4 khoang
# thanh 12.3-43.0s (nuot ca doan sach).
#
# Cach chac hon, khong phu thuoc danh sach: WATERMARK LA CHU DUNG YEN CA CLIP.
#   chu co mat >= NGUONG_WM ti le frame  -> watermark / logo -> BO
#   chu chi co o vai frame               -> chu that chay vao hinh -> CAM
# Vi mot chuoi bi OCR doc sai moi frame mot kieu, phai GOM CUM gan giong nhau
# truoc roi moi dem.
NGUONG_WM = 0.35      # co mat tu 35% frame tro len = dung yen = watermark
GIONG = 0.62          # nguong gom cum chuoi bi doc sai
MIN_KY_TU = 4         # chu qua ngan la nhieu tu net anh
# DEN THAT vs NEN TOI CHU DE SANG — do bang PHAN VI 95, khong phai trung binh.
# Ban dau dung trung binh < 28: HONG NANG. Clip nen den chu de sang bi cam sach:
#   tim-dap-nento   cam 20.0/20.0s   (tim do tren nen den — dung tot tu lau)
#   tebao-cautruc   cam 13.4/13.4s
#   nao-xanh-phatsang cam 14.1/25s
# Do lai: MACH_TAC giay 0 (den that) co TB 1.4 / p95 3.  TIM_DAP giay 8 co
# TB 10.1 / p95 43.  Trung binh gan nhau, p95 cach nhau 14 lan.
NGUONG_P95 = 20       # p95 duoi muc nay = khung den/fade that su

BO_QUA = re.compile(r"^\W*$|all rights reserved|www\.|\.com|©|\(c\)", re.I)

# --- CLIP SAN PHAM: chu tren VO HOP la thu CAN KHOE, khong phai loi ----------
# Lan chay dau gan co nham 8 dong o job 06: `richnatto-01`, `natto-01` bi cam
# 0-4.8s vi OCR doc chu "NANO ナットウキナーゼ PREMIUM" in tren hop.
SAN_PHAM = re.compile(r"Rich_Natto_product|Natto Xám|/natto-|/rich-|/richnatto-", re.I)

# Vung chu ngan hon nguong nay la nhieu OCR, khong phai chu that
# (vd `thankinh-xung-bungsang` bi cam dung 0.2 giay).
VUNG_CHU_TOI_THIEU = 1.0


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def probe(path):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height,r_frame_rate",
            "-show_entries", "format=duration", "-of", "json", path])
    try:
        d = json.loads(r.stdout)
        st = d["streams"][0]
        num, _, den = st["r_frame_rate"].partition("/")
        return {"dai": round(float(d["format"]["duration"]), 2),
                "w": st["width"], "h": st["height"],
                "fps": round(float(num) / float(den or 1), 2)}
    except Exception:
        return None


def man_den(path):
    """khoang MAN DEN / gan den — OCR khong bat duoc loai nay.

    3/16 loi tim ra ngay 04/08 la man den chu khong phai chu:
    `cucmau-tacmach-01.mp4` giay 0-3, `xovua-mohinh-mach-01.mp4` giay 45.
    """
    r = sh(["ffmpeg", "-v", "info", "-i", path,
            "-vf", "blackdetect=d=0.15:pix_th=0.10", "-an", "-f", "null", "-"])
    out = []
    for m in re.finditer(r"black_start:([0-9.]+)\s+black_end:([0-9.]+)", r.stderr):
        out.append((round(float(m.group(1)), 1), round(float(m.group(2)), 1)))
    return out


def noi_bien(vung, dai, pad):
    """noi moi vung ra `pad` giay hai dau roi gop cac vung dinh nhau.

    Lay mau moi `BUOC` giay nen chu co the bat dau som hon frame dau tien
    thay no toi `BUOC` giay. Vung CAM thi tha rong con hon tha hep.
    """
    if not vung:
        return []
    v = sorted((max(0.0, a - pad), min(dai, b + pad)) for a, b in vung)
    gop = [list(v[0])]
    for a, b in v[1:]:
        if a <= gop[-1][1] + 0.05:
            gop[-1][1] = max(gop[-1][1], b)
        else:
            gop.append([a, b])
    return [(round(a, 1), round(b, 1)) for a, b in gop]


def doi_canh(path, dai):
    """moc doi canh — chi chay cho clip dai."""
    if dai < SCENE_MIN:
        return []
    r = sh(["ffmpeg", "-v", "info", "-i", path,
            "-vf", f"select='gt(scene,{SCENE_NGUONG})',showinfo",
            "-an", "-f", "null", "-"])
    return sorted({round(float(m), 2) for m in
                   re.findall(r"pts_time:([0-9.]+)", r.stderr)})


def ocr_loat(paths):
    """OCR nhieu anh trong MOT lan goi — 50ms/anh."""
    if not paths:
        return {}
    p = subprocess.run([OCR], input="\n".join(paths) + "\n",
                       capture_output=True, text=True)
    out = {}
    for line in p.stdout.splitlines():
        a, _, b = line.partition("\t")
        out[a] = b
    return out


def _chuan(s):
    return re.sub(r"[^a-z]", "", s.lower())


def loc_ca_clip(raw_theo_frame):
    """[(giay, chuoi_ocr)] -> [(giay, [chu that])]  — bo watermark bang tan suat."""
    from difflib import SequenceMatcher
    n = max(1, len(raw_theo_frame))

    tach = []
    for t, raw in raw_theo_frame:
        toks = [x.strip() for x in (raw or "").split(" | ")]
        toks = [x for x in toks if len(x) >= MIN_KY_TU and not BO_QUA.search(x)]
        tach.append((t, toks))

    # gom cum cac chuoi gan giong nhau (cung mot chu bi doc sai nhieu kieu)
    cum = []                       # [[dai dien_chuan, so frame xuat hien]]
    thuoc = {}                     # chuoi_chuan -> chi so cum
    for _, toks in tach:
        for x in {_chuan(y) for y in toks}:
            if not x or x in thuoc:
                continue
            for i, (dd, _) in enumerate(cum):
                if SequenceMatcher(None, x, dd).ratio() >= GIONG:
                    thuoc[x] = i
                    break
            else:
                cum.append([x, 0])
                thuoc[x] = len(cum) - 1
    for _, toks in tach:
        for i in {thuoc[_chuan(y)] for y in toks if _chuan(y) in thuoc}:
            cum[i][1] += 1

    wm = {i for i, (_, c) in enumerate(cum) if c / n >= NGUONG_WM}
    return [(t, [y for y in toks
                 if _chuan(y) in thuoc and thuoc[_chuan(y)] not in wm])
            for t, toks in tach]


def gop_vung(co_chu, moc):
    """[(giay, [chu])] -> cac khoang lien tiep co chu -> VUNG_CAM."""
    vung, dau = [], None
    for i, (t, chu) in enumerate(zip(moc, co_chu)):
        if chu and dau is None:
            dau = t
        elif not chu and dau is not None:
            vung.append((dau, t))
            dau = None
    if dau is not None:
        vung.append((dau, moc[-1] + BUOC))
    return [(round(a, 1), round(b, 1)) for a, b in vung]


def lam_mot_clip(path, tmp):
    info = probe(path)
    if not info:
        return None
    dai = info["dai"]
    n = min(MAX_FRAME, max(1, int(dai / BUOC)))
    buoc = dai / n if n else BUOC
    moc = [round(i * buoc, 2) for i in range(n)]

    files = []
    for i, t in enumerate(moc):
        o = os.path.join(tmp, "f%03d.jpg" % i)
        sh(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", path,
            "-frames:v", "1", "-vf", "scale=640:-1", o])
        if os.path.exists(o):
            files.append((t, o))
    kq = ocr_loat([f for _, f in files])
    loc = loc_ca_clip([(t, kq.get(f, "")) for t, f in files])
    chu = [c for _, c in loc]

    # do sang trung binh tung frame — `blackdetect` chi bat DEN TUYET DOI,
    # con loai "toi mo + logo" thi lot. Giay 0 cua cucmau-tacmach co YAVG 1.39
    # ma blackdetect chi thay 0.2 giay.
    toi = []
    for t, f in files:
        try:
            im = Image.open(f).convert("L")
            im.thumbnail((64, 64))
            px = sorted(im.getdata())
            if px[int(len(px) * 0.95)] < NGUONG_P95:
                toi.append(t)
        except Exception:
            pass

    for _, f in files:
        try:
            os.remove(f)
        except OSError:
            pass

    vung_chu = [] if SAN_PHAM.search(path) else \
        [v for v in noi_bien(gop_vung(chu, [t for t, _ in files]), dai, buoc)
         if v[1] - v[0] >= VUNG_CHU_TOI_THIEU + 2 * buoc]
    # vung TOI ngan hon 0.5s la nhip nhap nhay cua animation, khong phai fade
    # den. (`thankinh-xung-bungsang` bi cam dung 0.2s -> chan het ca clip.)
    vung_den = [v for v in (man_den(path)
                            + noi_bien([(t, t) for t in toi], dai, buoc))
                if v[1] - v[0] >= 0.5]
    mau = {}
    for (t, _), c in zip(files, chu):
        if c:
            mau.setdefault(" | ".join(c)[:70], round(t, 1))

    cam = noi_bien(vung_chu + vung_den, dai, 0.0)
    # doan DUNG DUOC = phan bu cua vung cam
    dung, pos = [], 0.0
    for a, b in cam:
        if a - pos >= 1.0:
            dung.append((round(pos, 1), round(a, 1)))
        pos = max(pos, b)
    if dai - pos >= 1.0:
        dung.append((round(pos, 1), round(dai, 1)))

    return {
        "file": os.path.basename(path), "path": path,
        "dai": dai, "w": info["w"], "h": info["h"], "fps": info["fps"],
        "doc": info["h"] > info["w"],
        "so_frame_soi": len(files),
        "vung_chu": vung_chu,
        "vung_den": vung_den,
        "vung_cam": cam,
        "doan_dung_duoc": dung,
        "dai_doan_dai_nhat": round(max([b - a for a, b in dung], default=dai), 1),
        "chu_doc_duoc": mau,
        "doi_canh": doi_canh(path, dai),
        "mo_ta": {},          # tang 3 — dien sau
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lam-lai", action="store_true")
    ap.add_argument("--clip")
    a = ap.parse_args()

    if not os.path.exists(OCR):
        sys.exit(f"chua bien dich OCR: swiftc -O -o {OCR} {OCR}.swift")

    kho = {} if a.lam_lai or not os.path.exists(KHO) else \
        {x["file"]: x for x in json.load(open(KHO, encoding="utf-8"))}

    # moi hang so chuoi trong clips.py tro toi file co that
    ds = []
    for k in dir(C):
        v = getattr(C, k)
        # `isfile` chu khong phai `exists`: clips.py co 8 hang so tro toi THU MUC
        # (B, MM, DD, NG, VM, DQ, TDTT, AULM). Truoc 05/08/2026 chung lot vao
        # danh sach OCR roi bao "! doc khong duoc: 02. Dilim Footage" moi lan chay.
        if isinstance(v, str) and os.path.sep in v and os.path.isfile(v) \
                and not k.startswith("_"):
            ds.append(v)
    # 05/08/2026: soi ca DANH MUC, khong chi hang so trong clips.py.
    # Truoc do vong tren chi lay `dir(C)` -> 874 clip trong kho khong bao gio
    # duoc OCR, nen khong co `doan_dung_duoc`, nen `goi_y_broll` de src_start=0
    # -> dung vao doan co chu tieng Anh / man den.
    _dm = os.path.join(os.path.dirname(HERE), "danh_muc_kho.json")
    if os.path.exists(_dm):
        for m in json.load(open(_dm, encoding="utf-8")):
            if os.path.exists(m["path"]):
                ds.append(m["path"])
    ds = sorted(set(ds))
    if a.clip:
        ds = [p for p in ds if a.clip in p]

    anh = C.IMG_EXT
    print(f"{len(ds)} file trong danh ba · da co {len(kho)} · OCR moi {BUOC}s")
    t0 = time.time()
    n_moi = 0
    with tempfile.TemporaryDirectory() as tmp:
        for i, p in enumerate(ds, 1):
            b = os.path.basename(p)
            if b in kho and not a.lam_lai:
                continue
            if not os.path.exists(p):
                print(f"  ! O T7 RUNG ROI o clip {i} ({b}) — dung lai, chay lai de tiep")
                break
            if p.endswith(anh):
                kho[b] = {"file": b, "path": p, "anh": True, "mo_ta": {}}
                continue
            r = lam_mot_clip(p, tmp)
            if r is None:
                print(f"  ! doc khong duoc: {b}")
                continue
            kho[b] = r
            n_moi += 1
            cx = len(r["vung_chu"])
            print(f"  [{i:3}/{len(ds)}] {b[:44]:44} {r['dai']:6.1f}s "
                  f"{'DOC' if r['doc'] else '   '} "
                  f"{'CHU:' + str(cx) if cx else '    '}")
            json.dump(sorted(kho.values(), key=lambda x: x["file"]),
                      open(KHO, "w", encoding="utf-8"),
                      ensure_ascii=False, indent=1)

    print(f"\n-> {KHO}  ({len(kho)} clip, moi {n_moi}, {time.time()-t0:.0f}s)")
    co = [x for x in kho.values() if x.get("vung_chu")]
    print(f"clip CO CHU chay vao hinh: {len(co)}/{len(kho)}")


if __name__ == "__main__":
    main()
