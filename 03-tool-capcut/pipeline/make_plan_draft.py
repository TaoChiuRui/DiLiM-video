# -*- coding: utf-8 -*-
"""Sinh KHUNG `<job>/plan.py` tu `edit/words_cut.json`.

    python3 make_plan_draft.py --job 04-du-an/<ten-job>

VI SAO CO BUOC NAY: viet tay 50 dong plan.py la buoc TON NHAT ca ve thoi gian
lan token — phai vua chia nhip, vua uoc luong moc `t`, vua go lai loi noi.
Chia nhip va moc `t` thi may lam duoc va lam dung hon (no bam `start` cua chu
that). Con lai — CO DONG chu, chon TU KHOA, chon MAU, chon CLIP — moi la viec
cua nguoi.

Khung sinh ra co san:
    moc `t` DUNG (start cua chu dau moi nhip, khong phai uoc luong bang mat)
    loi noi that, da viet hoa, da chia 2 dong
    variant DOAN theo tu khoa  <-- phai soat lai, danh dau `#?`
    clip de trong             <-- chay suggest_clips.py roi dien

Sau khi sinh:
    python3 make_plan_draft.py --job $J     # ra plan.py
    <sua noi dung caption trong plan.py>
    python3 $J/plan.py                      # ra edit/plan.json
    python3 suggest_clips.py --job $J --md  # goi y clip cho tung dong
"""
import argparse
import json
import os
import re
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kho_caption as KC        # noqa: E402
import luoc_caption as LC       # noqa: E402
import ngat_cum as NC           # noqa: E402

# Nhip do tu 5 job that: 3.6-4.3 giay/caption. Chia dai hon thi mat diem chen
# B-roll, chia ngan hon thi chu nhay lien tuc, nguoi co tuoi doc khong kip.
MINL, MAXL = 3.0, 6.5      # do dai mot nhip caption (giay)
MAXW = 16                  # so chu toi da mot caption (2 dong x ~8 chu)
WRAP = 6                   # tren bao nhieu chu thi chia 2 dong


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.replace("đ", "d")


# --- doan variant theo tu khoa. CHI LA PHONG DOAN, luon phai soat lai. ---
GUESS = [
    ("cta",      ["de lai ten", "so dien thoai", "hotline", "goi ngay", "inbox",
                  "duoi video", "dang ky", "lien he"]),
    ("product",  ["natto", "nattokinase", "men gao", "co truong tho", "fu",
                  "hop", "lieu trinh", "trieu", "gia", "noi dia nhat", "thanh phan",
                  "ham luong", "vien", "uong"]),
    ("warning",  ["dau", "moi", "te bi", "mat ngu", "chong mat", "tien dinh",
                  "dot quy", "tai bien", "nguy", "hep", "tac", "xo vua", "cuc mau",
                  "mo xau", "thieu oxy", "kem", "khong", "benh", "nang", "lo"]),
    ("positive", ["sach", "thong thoang", "phong ngua", "cai thien", "khoe",
                  "ngu ngon", "nhe hon", "phuc hoi", "giup", "tan cuc mau",
                  "tot hon", "de chiu"]),
]


def guess_variant(text):
    n = norm(text)
    for var, keys in GUESS:
        if any(k in n for k in keys):
            return var
    return "yellow"


def group(words):
    """Chia chuoi chu thanh cac nhip caption.

    Cho ngat = cho NGAT HOI dai nhat, NHUNG co cong them diem cum nghia
    (`ngat_cum.diem_ranh`). Truoc 04/08/2026 chi nhin khoang lang, nen nhip
    hay ket thuc bang tu treo lo lung ("...dang co nhung" | "cai mang xo vua").
    Mot moi ngat vo cum bi tru 5-8 diem — nang hon moi khac biet khoang lang
    thuc te giua hai lua chon (~0.1-0.5s), nen cum thang.
    """
    s = [w["s"] for w in words]
    ws = [w["w"] for w in words]
    n = len(words)
    out, i = [], 0
    while i < n:
        j, best = i, None
        while j < n - 1:
            dur = s[j + 1] - s[i]
            if dur > MAXL or (j - i + 1) > MAXW:
                break
            if dur >= MINL:
                diem = (s[j + 1] - s[j]) + NC.diem_ranh(ws, j + 1)
                if best is None or diem > best[1]:
                    best = (j, diem)
            j += 1
        end = best[0] if best else min(j, n - 1)
        out.append((i, end))
        i = end + 1
    return out


def two_lines(text):
    """Chia 2 dong tai moi ngat DEP NHAT — xem `ngat_cum.py`.

    Ban cu cat `len(ws)//2`, do tren 369 dong that thi 40% moi chia roi vao
    GIUA CUM ("MAU CO THE LUU | THONG DE DANG HON"). Ban nay con 0%.
    """
    return NC.chia_hai_dong(text, wrap=WRAP)


def esc(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


HEAD = '''# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — {job}.

KHUNG NAY DO make_plan_draft.py SINH RA — chua phai ban dung duoc.
Con phai lam 4 viec, theo thu tu:

  1. CO DONG chu. Dong 1 + dong 2 hien dang la LOI NOI NGUYEN VAN. Caption la
     diem tua cho mat, khong phai phu de. Bo tu dem, bo lap, giu y va giu
     dung so lieu / ten san pham.
  2. Danh *TU KHOA*. Bo cap dau * quanh cum can nhan — dung do le mot dau.
  3. Soat `variant`. Dong nao con `#?` la MAY DOAN, chua ai xac nhan.
     warning = y tieu cuc · positive = y tich cuc · product = san pham/gia
     yellow = so lieu, vi von · cta = ket video
  4. Chon CLIP. Chay `suggest_clips.py --job <job> --md` roi dien vao cot
     thu 5. De "" nghia la caption do khong co B-roll — chap nhan duoc, tot
     hon la nhet clip sai y.

Moc `t` da la `start` cua chu that, khong phai uoc luong — dung sua tay tru
khi co ly do. Buoc 4_anchor.py se neo lai lan nua sau khi chu duoc co dong.

    python3 {job}/plan.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "{rel}"))
from clips import *        # noqa: F401,F403
from plan_build import build

HERE = os.path.dirname(os.path.abspath(__file__))

# (t, dong1, dong2, variant, clip, src_start, ghi chu)
R = [
'''

TAIL = ''']


if __name__ == "__main__":
    # Truyen fallback=<anh> neu muon may TU DOI clip qua ngan sang anh do.
    # Mac dinh la BO TRONG — may khong hieu nghia, doi lung tung la sai bai.
    build(HERE, R)
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    ap.add_argument("--force", action="store_true",
                    help="ghi de plan.py da co")
    a = ap.parse_args()

    import job_path
    job = job_path.job_dir(a.job)
    if not os.path.isdir(job):
        sys.exit(f"khong thay job: {job}")
    wpath = os.path.join(job, "edit/words_cut.json")
    if not os.path.exists(wpath):
        sys.exit(f"chua co {wpath} — chay 3_map_words.py truoc")

    out = os.path.join(job, "plan.py")
    if os.path.exists(out) and not a.force:
        sys.exit(f"da co {out} — them --force neu that su muon ghi de")

    words = json.load(open(wpath, encoding="utf-8"))
    groups = group(words)

    chac_chan, can_kiem = KC.nap_tu_dien()
    kho = KC.nap()

    rows, n_sua, ngo, n_kho = [], 0, [], 0
    for i0, i1 in groups:
        t = words[i0]["s"]
        said = " ".join(w["w"] for w in words[i0:i1 + 1])
        said = re.sub(r"\s+([,.!?])", r"\1", said).strip(" ,.")

        # 1. tu dien whisper — muc `chac_chan` sua thang, `can_kiem` chi bao
        goc = said
        said = KC.sua_whisper(said, chac_chan)
        if said != goc:
            n_sua += 1
        nghi = KC.soi_can_kiem(said, can_kiem)
        ngo += nghi

        # 2. kho cum — CHI GOI Y, khong tu dien vao dong
        goi_y = KC.tra(said, kho, bo_job=os.path.basename(job)) if kho else []
        if goi_y:
            n_kho += 1

        # 3. LUOC — ban nhap la loi noi DA XOA tu dem (backtest 05/08/2026:
        # cong sua giam 23%, chi 13/434 dong te hon; xem luoc_caption.py).
        # NGUYEN VAN giu o comment `# noi:` — bai hoc tu thi nghiem dien-tu-kho
        # da chet: de mat nguyen lieu goc la loi cau truc.
        lc = LC.luoc(said)
        if len(lc.split()) < 2:
            # nhip toan tu dem ("Đúng không cô chú anh chị?") — theo luat khoi
            # noi dung (anh Thanh 05/08): cau dan/xung ho KHONG can caption.
            d1, d2 = two_lines(said.upper())
            rows.append((t, d1, d2, guess_variant(said), nghi, goi_y, said, True))
        else:
            d1, d2 = two_lines(lc.upper())
            rows.append((t, d1, d2, guess_variant(said), nghi, goi_y, said, False))

    w1 = max(len(esc(r[1])) for r in rows) + 2
    w2 = max(len(esc(r[2])) for r in rows) + 2
    body = []
    for t, d1, d2, var, nghi, goi_y, said_goc, toan_dem in rows:
        body.append(f' # noi: {said_goc}\n')
        if toan_dem:
            body.append(' # ^ nhip toan tu dem — ung vien BO/GOP (luat khoi noi dung)\n')
        for sai, dung, vs in nghi:
            body.append(f' # NGO whisper: "{sai}" co the la "{dung}" — {vs}\n')
        for diem, e in goi_y:
            clip = ", ".join(f"{k} x{v}" for k, v in
                             sorted(e["clip"].items(), key=lambda x: -x[1])[:3])
            canh = "  [CO CHU SO — KIEM TAY]" if e["co_so"] else ""
            body.append(f' # KHO {diem} · da dung {e["lan"]}x/{len(e["job"])} job'
                        f' · {e["variant"]}{canh}\n')
            body.append(f' #     "{e["chu"]}"'
                        + (f' / "{e["chu2"]}"' if e["chu2"] else "") + "\n")
            body.append(f' #     clip da dung: {clip}\n')
        c1 = f'"{esc(d1)}",'.ljust(w1 + 2)
        c2 = f'"{esc(d2)}",'.ljust(w2 + 2)
        cv = f'"{var}",'.ljust(12)
        body.append(f' ({t:7.2f}, {c1}{c2}{cv}"", 0, ""),   #?\n')

    pipe = os.path.dirname(os.path.abspath(__file__))
    rel = os.path.relpath(pipe, job)
    open(out, "w", encoding="utf-8").write(
        HEAD.format(job=os.path.basename(job), rel=rel) + "".join(body) + TAIL)

    total = words[-1]["s"] - words[0]["s"]
    print(f"chu        : {len(words)}")
    print(f"nhip caption: {len(rows)}  (trung binh {total/max(len(rows),1):.1f}s/caption)")
    print(f"variant doan: " + ", ".join(
        f"{v}={sum(1 for r in rows if r[3]==v)}"
        for v in ("warning", "positive", "product", "yellow", "cta")
        if any(r[3] == v for r in rows)))
    print(f"tu dien     : sua {n_sua} dong · {len(ngo)} cho NGO (comment `# NGO`)")
    print(f"kho cum     : {n_kho}/{len(rows)} dong co goi y (comment `# KHO`)"
          if kho else "kho cum     : chua co — chay kho_caption.py --gom")
    print(f"-> {out}")
    print("\nCON PHAI LAM TAY: co dong chu · danh *tu khoa* · soat variant · chon clip")


if __name__ == "__main__":
    main()
