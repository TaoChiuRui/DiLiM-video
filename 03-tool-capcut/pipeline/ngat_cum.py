# -*- coding: utf-8 -*-
"""Ngat caption theo CUM NGHIA, khong cat word-by-word.

    python3 ngat_cum.py --do          # do tren moi job that: cu vs moi
    python3 ngat_cum.py --thu "<cau>"

VI SAO CO FILE NAY (anh Thanh chot 04/08/2026): "ghep caption kieu theo cum
thoi, dung lam word by word y het".

Ban cu chia hai dong bang `k = len(ws)//2` — cat DUNG GIUA danh sach tu, khong
nhin nghia. Do tren 369 dong that: **35% moi chia roi vao giua cum**:

    MÁU CÓ THỂ LƯU   |   THÔNG DỄ DÀNG HƠN      <- vo doi "luu thong"
    ĐANG CÓ NHỮNG    |   CÁI MẢNG XƠ VỮA        <- "nhung" treo lo lung
    THÌ CÁI MẠCH MÁU CỦA | CÔ ĐANG GẶP VẤN ĐỀ   <- "cua" treo lo lung

Mat khoang mot phan ba giay de mat nhay lai — dung cai ma caption sinh ra de
tranh. Nguoi co tuoi doc cang met.

BA LUAT, theo thu tu nang dan:

  1. KHONG cat giua CUM GHEP ("mach mau", "cuc mau dong", "so dien thoai").
  2. KHONG de dong 1 ket thuc bang TU DINH TRUOC — tu bat buoc dinh vao chu
     dang sau ("cua", "nhung", "cai", "de", "ma"). Treo lo lung o cuoi dong.
  3. NEN cat NGAY TRUOC tu mo cum ("nhung", "ma", "thi", "de", "vi", "nen").
     Do la cho hoi tu nhien.

Con lai moi tinh den can bang hai dong va gioi han 26 ky tu (tren nguong do
`5_render_captions.py` thu nho co chu).
"""
import argparse
import glob
import json
import re

# --- tu KHONG duoc dung o cuoi dong: chung dinh vao chu dang sau ------------
DINH_TRUOC = {
    # dinh tu / luong tu
    "các", "những", "một", "cái", "con", "chiếc", "chút", "vài", "mỗi", "mọi",
    # gioi tu
    "của", "cho", "với", "trong", "ngoài", "trên", "dưới", "về", "từ", "đến",
    "tới", "bằng", "như", "theo", "tại", "qua", "sang", "vào", "ra",
    # tro dong tu / pho tu
    "là", "có", "bị", "được", "rất", "quá", "hơn", "không", "chưa", "đang",
    "sẽ", "đã", "vẫn", "cũng", "chỉ", "phải", "nên", "hay", "còn", "tự", "bắt",
    # lien tu (cat TRUOC chung, khong cat SAU)
    "mà", "thì", "và", "hoặc", "để", "vì", "nếu", "khi", "rồi", "chứ", "nhưng",
    "do", "bởi", "tức",
}

# --- tu NEN dung o dau dong: chung mo mot cum moi --------------------------
MO_CUM = {
    "nhưng", "mà", "thì", "và", "hoặc", "để", "vì", "nếu", "khi", "rồi", "nên",
    "chứ", "còn", "tức", "bởi", "do", "vậy", "thế", "cho", "sau", "trước",
}

# --- cum ghep KHONG duoc tach doi ------------------------------------------
# Gom tu kich ban DiLiM that. Them tu do khi gap cum moi.
CUM_GHEP = [
    "mạch máu", "lòng mạch", "thành mạch", "cục máu đông", "máu đông",
    "mảng xơ vữa", "xơ vữa", "mỡ máu", "mỡ xấu", "huyết khối", "hồng cầu",
    "tiểu cầu", "lưu thông", "tuần hoàn", "huyết áp", "tim mạch", "cơ tim",
    "tế bào", "thần kinh", "dây thần kinh", "trục thần kinh", "sợi trục",
    "đột quỵ", "tai biến", "tiền đình", "tiểu đường", "chuột rút", "tê bì",
    "vai gáy", "cổ vai gáy", "mất ngủ", "chóng mặt", "đau đầu", "buồn nôn",
    "ngoại vi", "châm chích", "đàn hồi", "áp lực", "áp suất", "oxy",
    "hoạt huyết", "dưỡng não", "hoạt huyết dưỡng não",
    "nano nattokinase", "nattokinase", "coenzyme q10", "men gạo đỏ",
    "cỏ trường thọ", "vitamin nhóm b", "astaxanthin", "tiêu đen", "đậu nành",
    "lên men", "chiết xuất", "hàm lượng", "liệu trình", "phân giải",
    "số điện thoại", "điện thoại", "hotline", "bác sĩ", "chuyên gia",
    "sản phẩm", "thay thế", "chữa bệnh", "bệnh nền", "phẫu thuật",
    "chống đông", "đường ruột", "trung niên", "năng lượng", "xúc tác",
    "oxy hoá", "oxy hóa", "dạng khử", "máy bơm", "đường ống", "ống dẫn",
    "vỏ bọc", "tín hiệu", "nguyên nhân", "gốc rễ", "dấu hiệu", "cầu thang",
]
_GHEP_N = sorted({len(g.split()) for g in CUM_GHEP})
_GHEP = set(CUM_GHEP)

MAX_KY_TU = 26        # tren muc nay `5_render_captions.py` thu nho co chu


def _sach(w):
    return re.sub(r"[^\wÀ-ỹ]", "", w.lower())


def _trong_cum_ghep(ws, i):
    """Cat truoc tu thu i co lam vo mot cum ghep khong?"""
    for n in _GHEP_N:
        for bat in range(max(0, i - n + 1), i + 1):
            if bat + n > len(ws):
                continue
            if bat < i < bat + n:                       # moi cat nam GIUA cum
                if " ".join(_sach(w) for w in ws[bat:bat + n]) in _GHEP:
                    return True
    return False


def diem_ranh(ws, i):
    """Cham diem mot moi ngat TRUOC tu thu i. Cao = ngat o day dep hon.

    Dung chung cho ca chia hai dong lan chia nhip caption (`group`).
    """
    if i <= 0 or i >= len(ws):
        return -99.0
    d = 0.0
    truoc, sau = _sach(ws[i - 1]), _sach(ws[i])
    if _trong_cum_ghep(ws, i):
        d -= 8.0                        # luat 1 — nang nhat
    if truoc in DINH_TRUOC:
        d -= 5.0                        # luat 2 — tu treo lo lung
    if sau in MO_CUM:
        d += 1.0                        # luat 3 — cho hoi tu nhien
    if ws[i - 1].rstrip().endswith((",", ".", "?", "!", ";", ":")):
        d += 1.2                        # dau cau la ranh that
    return d


def chia_hai_dong(text, wrap=6, max_ky_tu=MAX_KY_TU):
    """Chia mot caption thanh 2 dong tai moi ngat DEP NHAT.

    Ngan hon `wrap` tu thi de mot dong.
    """
    ws = text.split()
    if len(ws) <= wrap:
        return text, ""
    # Trong so da can (04/08/2026): luat cum (-5 / -8) LUON thang, nhung
    # thuong dau phay (+1.2) thi KHONG duoc thang can bang — neu khong no cat
    # ngay dau phay dau tien va de lai dong 2 con hai chu.
    tot, diem_tot = None, None
    for i in range(1, len(ws)):
        d = diem_ranh(ws, i)
        a, b = " ".join(ws[:i]), " ".join(ws[i:])
        d += 2.5 * (1 - abs(len(a) - len(b)) / max(len(a) + len(b), 1))
        for dong in (a, b):
            if len(dong) > max_ky_tu:
                d -= 0.15 * (len(dong) - max_ky_tu)
        if diem_tot is None or d > diem_tot:
            tot, diem_tot = i, d
    return " ".join(ws[:tot]), " ".join(ws[tot:])


# ---------------------------------------------------------------- do / thu
def _xau(a, b):
    """moi chia nay co roi vao giua cum khong? (dung de DO, khong dung de chia)"""
    if not b:
        return False
    ws = a.split() + b.split()
    return diem_ranh(ws, len(a.split())) < 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--do", action="store_true")
    ap.add_argument("--thu", metavar="CAU")
    a = ap.parse_args()

    if a.thu:
        d1, d2 = chia_hai_dong(a.thu.upper())
        print(f'"{d1}"\n"{d2}"')
        return

    if a.do:
        def cu(t, wrap=6):
            ws = t.split()
            if len(ws) <= wrap:
                return t, ""
            k = len(ws) // 2
            return " ".join(ws[:k]), " ".join(ws[k:])

        n = xc = xm = 0
        lc = lm = 0          # do lech hai dong (ky tu)
        tc = tm = 0          # so dong tran qua MAX_KY_TU
        vd = []
        for f in sorted(glob.glob("../../04-du-an/*/edit/plan.json")):
            for r in json.load(open(f, encoding="utf-8")):
                s = (r.get("said") or "").strip().upper()
                if not s:
                    continue
                ac, bc = cu(s)
                am, bm = chia_hai_dong(s)
                if not bc:
                    continue
                n += 1
                c, m = _xau(ac, bc), _xau(am, bm)
                xc += c
                xm += m
                lc += abs(len(ac) - len(bc))
                lm += abs(len(am) - len(bm))
                tc += (len(ac) > MAX_KY_TU) + (len(bc) > MAX_KY_TU)
                tm += (len(am) > MAX_KY_TU) + (len(bm) > MAX_KY_TU)
                if c and not m and len(vd) < 8:
                    vd.append((ac[-28:], bc[:28], am[-28:], bm[:28]))
        print(f"tren {n} dong that:")
        print(f"{'':22}{'cat giua cum':>14}{'lech TB (ky tu)':>18}{'dong tran 26':>15}")
        print(f"   ban cu (len//2)   {xc:>7} ({xc*100//n:>2}%){lc/n:>15.1f}"
              f"{tc:>12} ({tc*100//(2*n)}%)")
        print(f"   ban moi (cum)     {xm:>7} ({xm*100//n:>2}%){lm/n:>15.1f}"
              f"{tm:>12} ({tm*100//(2*n)}%)")
        print()
        for ac, bc, am, bm in vd:
            print(f"   cu  ...{ac} || {bc}...")
            print(f"   moi ...{am} || {bm}...\n")
        return
    ap.print_help()


if __name__ == "__main__":
    main()
