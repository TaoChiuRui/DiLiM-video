# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — IMG_1771 (ban da cat, 1:52).

Moc `t` ben duoi la UOC LUONG; script tu SNAP vao `start` cua chu gan nhat
va dat `t_end` = `t` cua caption ke tiep. KHONG dung `end` cua whisper
(xem cut.py: `end` nuot ca khoang lang phia sau, khong dang tin).

    python3 plan.py
"""
import json, os, subprocess, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "../../03-tool-capcut/pipeline"))
from clips import *   # noqa: F401,F403

HERE = os.path.dirname(os.path.abspath(__file__))

# (t_uoc_luong, dong1, dong2, variant, path, src_start, ghi chu)
R = [
 (  0.40, "VÌ SAO *ĐAU ĐẦU*", "*MẤT NGỦ*",                     "warning",  MAT_NGU,   2.0, ""),
 (  3.40, "ĐAU MỎI *CỔ VAI GÁY*", "*TÊ BÌ TAY CHÂN*",          "warning",  VAI_GAY,   1.0, ""),
 (  5.52, "*RỐI LOẠN TIỀN ĐÌNH*", "",                          "warning",  DAU_DAU3,  1.0, ""),
 (  6.80, "LẠI GÂY", "*ĐỘT QUỴ, TAI BIẾN?*",                   "warning",  DOT_QUY,   1.0, ""),
 (  9.60, "*ĐỘT QUỴ* KHÔNG", "TỰ NHIÊN MÀ CÓ",                 "warning",  DOT_QUY,   6.0, ""),
 ( 12.16, "*ĐAU ĐẦU, MẤT NGỦ*", "CŨNG KHÔNG TỰ NHIÊN MÀ CÓ",   "warning",  DAU_DAU1,  2.0, ""),
 ( 14.50, "GỐC RỄ LÀ", "*MẠCH MÁU* LÂU NGÀY",                  "warning",  MACH_MAU,  1.0, ""),
 ( 17.80, "CÓ NHỮNG *MẢNG MỠ XẤU*", "",                        "warning",  MO_MAU,    1.0, ""),
 ( 20.12, "CÓ *XƠ VỮA*", "VÀ *CỤC MÁU ĐÔNG*",                  "warning",  XO_VUA,   15.0, "anh chọn clip này 03/08 — mảng dày, máu đi qua bị tắc"),
 ( 23.08, "LÀM *HẸP MẠCH MÁU*", "",                            "warning",  MACH_HEP,  1.0, ""),
 ( 26.12, "MÁU *KHÔNG LƯU THÔNG ĐƯỢC*", "",                    "warning",  MACH_HEP,  9.0, ""),
 ( 29.64, "*THIẾU OXY*", "*THIẾU DƯỠNG CHẤT*",                 "warning",  NAO,       2.0, ""),
 ( 32.52, "CUNG CẤP CHO *NÃO*", "",                            "warning",  NAO,       6.0, ""),
 ( 35.12, "MỚI GÂY *ĐAU ĐẦU*", "*MẤT NGỦ*",                    "warning",  MAT_NGU,   8.0, ""),
 ( 38.52, "DÙNG *HOẠT HUYẾT*", "HAY *BỔ NÃO*",                 "warning",  "",        0, "THIẾU CLIP: vỉ thuốc"),
 ( 41.14, "KHÔNG CẢI THIỆN ĐƯỢC", "*GỐC RỄ VẤN ĐỀ*",           "warning",  MACH_HEP, 15.0, ""),
 ( 46.00, "ĐẦU TIÊN PHẢI", "*LÀM SẠCH CỤC MÁU ĐÔNG*",          "positive", CUC_MAU,   2.0, ""),
 ( 48.64, "VÀ *LÀM SẠCH XƠ VỮA*", "TRONG THÀNH MẠCH",          "positive", XO_VUA,    0, ""),
 ( 54.26, "GIÚP MẠCH MÁU", "*THÔNG THOÁNG*",                   "positive", MACH_MAU,  2.0, "HE MẠCH MAU chỉ 5.0s, không đủ"),
 ( 59.48, "*LUYỆN TẬP* THỂ DỤC THỂ THAO", "",                  "positive", "",        0, "THIẾU CLIP: tập thể dục"),
 ( 63.12, "*HẠN CHẾ* ĐỒ CHIÊN XÀO", "DẦU MỠ",                  "warning",  "",        0, "THIẾU CLIP: đồ chiên rán"),
 ( 68.04, "VÀ *BỔ SUNG*", "*NANO NATTOKINASE 60.000 FU*",      "product",  NATTO1,    0.5, ""),
 ( 74.86, "*NỘI ĐỊA NHẬT*", "",                                "product",  NATTO2,    0.5, ""),
 ( 78.88, "*ENZYME NATTO* HỖ TRỢ", "LÀM TAN *CỤC MÁU ĐÔNG*",   "positive", CUC_MAU,  20.0, ""),
 ( 82.92, "MÓN ĂN TRUYỀN THỐNG", "CỦA NGƯỜI NHẬT",             "yellow",   NATTO_2HOP, 0, "ảnh 2 hộp — trọn sản phẩm, có khoảng thở"),
 ( 86.80, "*HÀNG NGHÌN NĂM* TRƯỚC", "",                        "yellow",   NATTO_2HOP, 0, ""),
 ( 92.22, "DÙNG *NANO NATTOKINASE*", "",                       "product",  RICHNATTO, 1.0, ""),
 ( 99.28, "KẾT HỢP *MEN GẠO ĐỎ*", "VÀ *CỎ TRƯỜNG THỌ*",        "product",  MEN_GAO,   1.0, ""),
 (102.32, "GIẢM *MỠ XẤU*", "TRONG THÀNH MẠCH",                 "positive", MO_MAU,    3.0, ""),
 (105.18, "MẠCH MÁU *THÔNG THOÁNG*", "PHÒNG NGỪA *ĐỘT QUỴ*",   "positive", MAU_TIM,   0, ""),
]

MIN_DUR = 0.80        # caption ngan nhat cho phep
LEAD_IN = 0.06        # bat som hon chu dau mot chut cho de doc


def main():
    words = json.load(open(os.path.join(HERE, "edit/words_cut.json"), encoding="utf-8"))
    end_all = max(w["s"] for w in words) + 1.2

    # SNAP moc bat dau vao `start` cua chu gan nhat
    rows, probs, fixed, swapped = [], [], [], []
    starts = []
    for i, (t, d1, d2, var, p, ss, note) in enumerate(R, 1):
        cand = min(words, key=lambda w: abs(w["s"] - t))
        starts.append(max(0.0, cand["s"] - LEAD_IN))

    for i, ((t, d1, d2, var, p, ss, note), t0) in enumerate(zip(R, starts), 1):
        t1 = starts[i] if i < len(starts) else end_all
        if t1 - t0 < MIN_DUR:
            probs.append(f"caption {i}: chi {t1-t0:.2f}s (<{MIN_DUR}s)")
        txt = d1 + ("\n" + d2 if d2 else "")
        if txt.count("*") % 2:
            probs.append(f"caption {i}: dau * le")

        if p:
            if not os.path.exists(p):
                probs.append(f"caption {i}: KHONG TIM THAY {os.path.basename(p)}")
            elif not p.endswith(IMG_EXT):
                dur = float(subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip() or 0)
                need = t1 - t0
                if dur - ss < need - 0.03:
                    if dur >= need:
                        # TU LUI src_start — clip du dai, chi la bat dau qua muon
                        ss = round(max(0.0, dur - need), 2)
                        fixed.append(f"caption {i}: lui src_start -> {ss} "
                                     f"({os.path.basename(p)})")
                    else:
                        # clip NGAN hon ca caption -> doi sang anh 2 hop
                        swapped.append(f"caption {i}: {os.path.basename(p)} chi {dur:.1f}s "
                                       f"< {need:.1f}s -> natto-2hop.jpg")
                        p, ss = NATTO_2HOP, 0

        said = " ".join(w["w"] for w in words if t0 - 0.05 <= w["s"] < t1 - 0.05)
        rows.append({"idx": i, "t": round(t0, 2), "t_end": round(t1, 2),
                     "d1": d1, "d2": d2, "text": txt, "variant": var,
                     "path": p, "src_start": ss, "note": note, "said": said,
                     "snap_drift": round(t0 - t, 2)})

    out = os.path.join(HERE, "edit/plan.json")
    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    have = sum(1 for r in rows if r["path"])
    print(f"caption   : {len(rows)}")
    print(f"co B-roll : {have}   |  de trong: {len(rows)-have}")
    print(f"phu song  : {rows[0]['t']:.2f} -> {rows[-1]['t_end']:.2f}s")
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


if __name__ == "__main__":
    main()
