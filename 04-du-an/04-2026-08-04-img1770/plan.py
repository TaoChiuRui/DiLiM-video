# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — IMG_1770 (ban da cat, 3:42).

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
 (  0.00, "CÔ CHÚ ĐANG BỊ *ĐAU ĐẦU*", "*MẤT NGỦ*",             "warning",  MAT_NGU,   2.0, "hook"),
 (  2.88, "ĐAU MỎI *CỔ VAI GÁY*", "*TÊ BÌ TAY CHÂN*",          "warning",  VAI_GAY,   1.0, ""),
 (  5.26, "*RỐI LOẠN TIỀN ĐÌNH*", "",                          "warning",  DAU_DAU3,  1.0, ""),
 (  8.80, "VÌ SAO *ĐAU ĐẦU, MẤT NGỦ*", "",                     "yellow",   DAU_DAU1,  2.0, ""),
 ( 14.86, "ĐAU MỎI *CỔ VAI GÁY*", "*TÊ BÌ TAY CHÂN*",          "warning",  VAI_GAY,   4.0, ""),
 ( 17.04, "LẠI RẤT DỄ GÂY", "*ĐỘT QUỴ, TAI BIẾN?*",            "warning",  DOT_QUY,   1.0, ""),
 ( 22.80, "ĐẦU TIÊN NÓ ĐẾN TỪ", "*MẠCH MÁU LÂU NGÀY*",         "warning",  MACH_MAU,  1.0, ""),
 ( 27.60, "MẠCH MÁU BẮT ĐẦU", "*LƯU THÔNG KÉM*",               "warning",  MACH_HEP,  1.0, ""),
 ( 33.34, "BẮT ĐẦU *THIẾU OXY*", "*THIẾU DƯỠNG CHẤT*",         "warning",  MACH_HEP,  9.0, ""),
 ( 39.34, "NUÔI DƯỠNG *TẾ BÀO NÃO*", "",                       "warning",  NAO,       2.0, ""),
 ( 44.84, "NÃO CHỈ CHIẾM", "*2% CƠ THỂ*",                      "yellow",   NAO,       8.0, ""),
 ( 51.44, "NHƯNG CẦN TỚI", "*20% OXY*",                        "yellow",   NAO21,     1.0, ""),
 ( 55.10, "ĐỂ NUÔI *TẾ BÀO NÃO*", "VÀ *HỆ THẦN KINH*",         "warning",  NEURON,    1.0, ""),
 ( 58.82, "MẠCH MÁU LÂU NGÀY", "CÓ *MẢNG MỠ XẤU*",             "warning",  MO_MAU,    1.0, ""),
 ( 65.50, "BÁM Ở *THÀNH MẠCH*", "*DÀY LÊN TỪNG NGÀY*",         "warning",  XO_VUA,    5.0, ""),
 ( 68.42, "HÌNH THÀNH *MẢNG XƠ VỮA*", "",                      "warning",  XO_VUA,   15.0, "mảng dày, máu đi qua bị tắc"),
 ( 71.52, "VÀ *CỤC MÁU ĐÔNG*", "",                             "warning",  CUC_MAU,   2.0, ""),
 ( 73.86, "LÀM *MẠCH MÁU HẸP LẠI*", "",                        "warning",  MACH_HEP, 15.0, ""),
 ( 76.36, "*KHÔNG ĐƯA MÁU ĐI ĐƯỢC*", "",                       "warning",  MACH_HEP, 19.0, ""),
 ( 78.58, "GIỐNG NHƯ", "*ĐƯỜNG ỐNG NƯỚC*",                     "yellow",   "",        0, "THIẾU CLIP: ống nước tắc — ẩn dụ chính của bài"),
 ( 82.00, "ỐNG NƯỚC LÂU NGÀY", "CÓ *RONG, RÊU, CẶN*",          "yellow",   "",        0, "THIẾU CLIP: ống nước bẩn"),
 ( 87.78, "ĐƯỜNG ỐNG *HẸP LẠI*", "*NƯỚC CHẢY CHẬM*",           "yellow",   "",        0, "THIẾU CLIP: ống nước"),
 ( 92.44, "DÙNG *MÁY BƠM*", "CŨNG KHÔNG ĐẨY ĐƯỢC",             "warning",  "",        0, "THIẾU CLIP: máy bơm"),
 ( 97.58, "DÙNG *HOẠT HUYẾT*", "HAY *BỔ NÃO*",                 "warning",  "",        0, "THIẾU CLIP: vỉ thuốc"),
 (102.84, "CHỈ CẢI THIỆN *LÚC ĐẤY*", "",                       "warning",  MACH_HEP,  1.0, ""),
 (105.36, "KHÔNG CẢI THIỆN ĐƯỢC", "*GỐC RỄ VẤN ĐỀ*",           "warning",  MACH_HEP,  6.0, ""),
 (110.56, "ĐỂ PHÒNG NGỪA", "*ĐỘT QUỴ, TAI BIẾN*",              "warning",  DOT_QUY,   6.0, ""),
 (113.14, "ĐẦU TIÊN *LÀM SẠCH*", "*CỤC MÁU ĐÔNG*",             "positive", CUC_MAU,  20.0, ""),
 (119.48, "SẠCH *MẢNG MỠ XẤU*", "TRONG THÀNH MẠCH",            "positive", MO_MAU,    3.0, ""),
 (124.38, "GIÚP *THÔNG THOÁNG MẠCH MÁU*", "",                  "positive", HE_MACH,   0, ""),
 (126.78, "VÀ PHÒNG NGỪA", "*ĐỘT QUỴ, TAI BIẾN*",              "positive", MAU_TIM,   0, ""),
 (131.74, "HIẾU KHUYÊN CÔ CHÚ DÙNG", "*NANO NATTOKINASE*",     "product",  NATTO1,    0.5, ""),
 (134.22, "*60.000 FU*", "CỦA *NỘI ĐỊA NHẬT*",                 "product",  NATTO2,    0.5, ""),
 (138.02, "HÀM LƯỢNG *ENZYME NATTO*", "LÊN ĐẾN *60.000 FU*",   "product",  NATTO_2HOP, 0, "ảnh 2 hộp — trọn sản phẩm"),
 (142.02, "LÀM TAN *CỤC MÁU ĐÔNG*", "",                        "positive", CUC_MAU,  35.0, ""),
 (145.04, "*MEN GẠO ĐỎ*", "VÀ *CỎ TRƯỜNG THỌ*",                "product",  MEN_GAO,   1.0, ""),
 (148.10, "LÀM SẠCH *MỠ XẤU*", "TRONG THÀNH MẠCH",             "positive", MO_MAU,    5.0, ""),
 (153.34, "MẠCH MÁU *THÔNG THOÁNG*", "PHÒNG *ĐỘT QUỴ*",        "positive", MAU_TIM,   4.0, ""),
 (157.98, "CÔ CHÚ NÀO ĐANG BỊ", "*ĐAU ĐẦU, MẤT NGỦ*",          "warning",  MAT_NGU,   8.0, ""),
 (160.76, "*ĐAU MỎI VAI GÁY*", "*TÊ BÌ TAY CHÂN*",             "warning",  VAI_GAY,   6.0, ""),
 (162.78, "ĐỂ LẠI *TÊN + SỐ ĐIỆN THOẠI*", "DƯỚI VIDEO",        "cta",      NATTO_2HOP, 0, ""),
 (168.16, "HOẶC GỌI *HOTLINE*", "*0862 188 681*",              "cta",      RICHNATTO, 0, ""),
 (174.00, "MỘT HỘP DÙNG", "*2 THÁNG* — *2.290.000Đ*",          "product",  NATTO1,    2.0, ""),
 (182.16, "MỖI NGÀY *38.000Đ*", "*CHƯA BẰNG MỘT BÁT PHỞ*",     "yellow",   NATTO_2HOP, 0, ""),
 (188.80, "SAU *15–20 NGÀY*", "*NGỦ NGON*, ĐẦU *NHẸ HƠN*",     "positive", NGU_NGON,  2.0, ""),
 (193.68, "ĐỂ *LÀM SẠCH HOÀN TOÀN*", "MẠCH MÁU",               "positive", HE_MACH,   0, ""),
 (197.00, "*PHỤC HỒI* LÂU DÀI", "PHÒNG *ĐỘT QUỴ*",             "positive", MAU_TIM,   4.0, ""),
 (199.82, "DUY TRÌ *LIỆU TRÌNH 1 NĂM*", "",                    "product",  RICHNATTO, 1.0, ""),
 (204.90, "*6 HỘP* — *13.740.000Đ*", "",                       "yellow",   NATTO_2HOP, 0, ""),
 (208.86, "DÙNG LUÔN MỘT NĂM", "ĐƯỢC *14 THÁNG*",              "product",  RICHNATTO, 4.0, ""),
 (215.62, "SỬ DỤNG NGAY", "ĐỂ LẠI *TÊN + SỐ ĐIỆN THOẠI*",      "cta",      NATTO_2HOP, 0, ""),
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
