# -*- coding: utf-8 -*-
"""LUOC loi noi -> ban nhap caption, bang cach XOA TU khoi chinh cau do.

    from luoc_caption import luoc
    luoc("Vẫn còn không có chăm sóc sức khỏe đúng không cô chú anh chị")
    -> "Vẫn còn không chăm sóc sức khỏe"

VI SAO XOA-TU chu khong phai viet-lai: thi nghiem dien san tu kho_caption da
CHET 05/08/2026 (54% chinh xac o gate chat nhat — xem VERSION.md "Da thu va BO").
No chet vi lay chu tu BAI KHAC: lech cach dien dat, lech ranh nhip, rot neo.
Luoc tu CHINH NHIP DO thi khong dinh ca ba: ket qua luon la TAP CON cua loi noi
that, nen `4_anchor.py` luon neo duoc (theo cach no van lam voi chu that).
Van de nay co ten trong hoc thuat: "sentence compression by deletion" — ky thuat
chuan cho phu de tu dong.

DANH SACH TU BO **HOC TU 434 cap (loi noi -> caption cuoi)** cua 8 job that,
khong viet tay: tu nao bi bo >=75% so lan gap (gap >=8 lan) thi vao danh sach.
Do duoc: `là` bo 79% · `cái` 93% · `mình` 97% · `ạ`/`nha`/`ấy` 100%.

BON TU BI LOAI KHOI DANH SACH DU SO LIEU BAO BO — vi "bo" cua chung la do
caption VIET LAI KHAC TOKEN, khong phai xoa: `natto`/`kinase` (said tach doi,
caption viet lien `NATTOKINASE`) · `sơ` (whisper nghe sai, caption sua `XƠ VỮA`)
· `hóa` (`chuyển hóa` viet lai). Xoa chung la mat ten san pham / thuat ngu.
"""
import re
import unicodedata as ud

# hoc tu 434 cap ngay 05/08/2026 — cap nhat bang: python3 luoc_caption.py --hoc
#
# HAI TANG, vi chi phi hai chieu KHONG can xung: xoa nham chu can dung thi phai
# go lai tu comment (dat); giu thua tu dem thi chi viec xoa (re). Nen tang MEM
# chi xoa khi dong con qua kho 2x26 ky tu — dung cach van lam tay: cau ngan
# thi tha, cau tran khung moi nen them.
#
# Backtest v1 (mot tang, nguong 25%): gan ban cuoi 44%->50% nhung MAT chu can
# dung o 78/434 dong — truot. v2 chia tang + xoa CUM truoc.

# xoa CA CUM truoc khi xet tung tu — "đúng không" ma xoa roi le thi con "không"
# cut lai giua cau
CUM_BO = [
    r"đúng không(\s+ạ)?(\s+cô chú anh chị)?",
    r"phải không(\s+ạ)?",
    r"cô chú anh chị(\s+nha|\s+nhé)?",
    r"quý cô chú",
    r"\banh chị(\s+nha|\s+nhé)\b",
]
# giu <= 10% — xoa luon
TU_BO_CHAC = {"cái", "mình", "nó", "thì", "sẽ", "như", "ấy", "nhé", "nha",
              "ạ", "các", "nên", "sơ_"} - {"sơ_"}
# 10% < giu <= 25% — chi xoa khi dong con dai qua kho, xoa dan tu it-giu nhat
TU_BO_MEM = ["là", "mà", "những", "này", "vậy", "cho", "của", "anh", "chị",
             "dưới", "rồi", "bên", "cô", "vào", "trạng", "tình", "chính",
             "chú", "đúng", "vì", "về", "và", "trên"]
KHO_2_DONG = 52          # 2 dong x 26 ky tu (viet-plan.md)
# khong bao gio xoa — ke ca sau nay danh sach hoc lai co bao bo
GIU_CHAC = {"natto", "kinase", "sơ", "hóa", "thịnh", "dilim", "nano", "rich",
            "q10", "fu", "hotline"}

_W = re.compile(r"[\w" "àáảãạăằắẳẵặâầấẩẫậèéẻẽẹêềếểễệìíỉĩị"
                "òóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵđ]+", re.I)


def _chuan(w):
    return ud.normalize("NFC", w.lower())


def luoc(said):
    """Xoa cum dem -> xoa tu chac -> neu van dai qua kho thi xoa dan tu mem."""
    t = said
    for rx in CUM_BO:
        t = re.sub(rx, " ", t, flags=re.I)

    def giu_lai(bo_them):
        ra = []
        for m in _W.finditer(t):
            w = _chuan(m.group(0))
            if any(ch.isdigit() for ch in w) or w in GIU_CHAC:
                ra.append(m.group(0)); continue
            if w in TU_BO_CHAC or w in bo_them:
                continue
            ra.append(m.group(0))
        return " ".join(ra)

    ket = giu_lai(set())
    bo = set()
    for w in TU_BO_MEM:                    # xoa dan tu it-giu nhat, du ngan thi dung
        if len(ket) <= KHO_2_DONG:
            break
        bo.add(w)
        ket = giu_lai(bo)
    return re.sub(r"\s+", " ", ket).strip()


if __name__ == "__main__":
    import argparse, glob, json, collections
    ap = argparse.ArgumentParser()
    ap.add_argument("--hoc", action="store_true", help="hoc lai ti le giu tu cac job")
    a = ap.parse_args()
    if a.hoc:
        giu, tong = collections.Counter(), collections.Counter()
        for f in sorted(glob.glob("04-du-an/*/edit/plan.json")):
            if "06b" in f:
                continue
            for r in json.load(open(f, encoding="utf-8")):
                said = r.get("said") or ""
                fin = {_chuan(x) for x in _W.findall((r["d1"] + " " + r["d2"]).replace("*", ""))}
                if not said or not fin:
                    continue
                for w in {_chuan(x) for x in _W.findall(said)}:
                    tong[w] += 1
                    giu[w] += w in fin
        print("tu nen BO (giu <=25%, gap >=8) — doi chieu tay roi sua TU_BO:")
        for w, c in tong.most_common():
            if c >= 8 and giu[w] / c <= 0.25:
                dau = "  (dang GIU_CHAC)" if w in GIU_CHAC else ""
                print(f"  {w:14} gap {c:3}  giu {giu[w]*100//c:3}%{dau}")
    else:
        vd = "Vẫn còn không có chăm sóc sức khỏe đúng không cô chú anh chị"
        print(f"  {vd}\n  -> {luoc(vd)}")
