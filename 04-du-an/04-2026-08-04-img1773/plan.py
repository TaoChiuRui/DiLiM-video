# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — IMG_1773 (ban da cat, 2:32).

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
 (  0.00, "KHÔNG AI *ĐỘT QUỴ*", "CHỈ VÌ *ĐAU ĐẦU, MẤT NGỦ*",   "warning",  DOT_QUY,   1.0, "hook — giữ trọn"),
 (  3.36, "ĐAU MỎI *CỔ VAI GÁY*", "*TÊ BÌ TAY CHÂN*",          "warning",  VAI_GAY,   1.0, ""),
 (  5.72, "MÀ VÌ ĐÃ *PHỚT LỜ QUÁ LÂU*", "",                    "warning",  DAU_DAU1,  2.0, ""),
 (  8.64, "CÁC *BIỂU HIỆN BÁO TRƯỚC*", "",                     "warning",  DAU_DAU1,  8.0, ""),
 ( 11.66, "MẠCH MÁU *LÂU NGÀY*", "",                           "warning",  MACH_MAU,  1.0, ""),
 ( 15.62, "VÌ SAO *HIẾU NÓI VẬY?*", "",                        "yellow",   "",        0, "câu hỏi — để chữ chạy một mình"),
 ( 17.60, "*ĐỘT QUỴ* LÀ DO", "MẠCH MÁU LÂU NGÀY",              "warning",  MACH_HEP,  1.0, ""),
 ( 20.10, "NÓ BỊ *TẮC NGHẼN*", "NÓ BỊ *VỠ RA*",                "warning",  MACH_HEP, 10.0, ""),
 ( 24.14, "MỚI GÂY *ĐỘT QUỴ, TAI BIẾN*", "",                   "warning",  DOT_QUY,   6.0, ""),
 ( 26.64, "MẠCH MÁU LÂU NGÀY", "CÓ *MẢNG MỠ XẤU*",             "warning",  MO_MAU,    1.0, ""),
 ( 29.74, "*DÀY LÊN TỪNG NGÀY*", "",                           "warning",  XO_VUA,    5.0, ""),
 ( 31.94, "LÀM *HẸP MẠCH MÁU*", "",                            "warning",  XO_VUA,   15.0, "mảng dày, máu đi qua bị tắc"),
 ( 34.68, "MÁU *KHÔNG LÊN ĐƯỢC NÃO*", "",                      "warning",  NAO,       2.0, ""),
 ( 37.48, "BÁO HIỆU BẰNG *ĐAU ĐẦU*", "*HOA MẮT, CHÓNG MẶT*",   "warning",  CHONG_MAT, 1.0, ""),
 ( 42.70, "TA THẤY LÀ *BÌNH THƯỜNG*", "",                      "yellow",   DAU_DAU3,  1.0, ""),
 ( 45.64, "NÊN *PHỚT LỜ* NÓ", "",                              "warning",  DAU_DAU3,  4.0, ""),
 ( 48.34, "MẠCH MÁU *DẦN DÀY LÊN*", "GÂY *TẮC MẠCH*",          "warning",  XO_VUA,   20.0, ""),
 ( 53.52, "VÀ GÂY *ĐỘT QUỴ*", "",                              "warning",  DOT_QUY,  10.0, ""),
 ( 56.36, "ĐỂ GIẢI QUYẾT", "*GỐC RỄ VẤN ĐỀ*",                  "positive", HE_MACH,   0, ""),
 ( 59.04, "LÀM SẠCH *MẢNG MỠ XẤU*", "TRONG THÀNH MẠCH",        "positive", MO_MAU,    3.0, ""),
 ( 62.06, "VÀ CÁC *MẢNG XƠ VỮA*", "",                          "positive", MANG_MO2,  3.0, ""),
 ( 64.94, "LÀM SẠCH *CỤC MÁU ĐÔNG*", "",                       "positive", CUC_MAU,   2.0, ""),
 ( 68.12, "GIÚP MẠCH MÁU", "*THÔNG THOÁNG*",                   "positive", MACH_MAU,  6.0, ""),
 ( 73.36, "HIẾU KHUYÊN CÔ CHÚ DÙNG", "*NANO NATTOKINASE*",     "product",  NATTO1,    0.5, ""),
 ( 77.50, "*60.000 FU* CỦA NHẬT", "",                          "product",  NATTO2,    0.5, ""),
 ( 81.36, "HÀM LƯỢNG *ENZYME NATTO*", "LÊN ĐẾN *60.000 FU*",   "product",  NATTO_2HOP, 0, "ảnh 2 hộp"),
 ( 85.26, "LÀM TAN *CỤC MÁU ĐÔNG*", "",                        "positive", CUC_MAU,  20.0, ""),
 ( 88.52, "KẾT HỢP *MEN GẠO ĐỎ*", "VÀ *CỎ TRƯỜNG THỌ*",        "product",  MEN_GAO,   1.0, ""),
 ( 91.84, "GIẢM *MỠ XẤU*", "VÀ *XƠ VỮA* THÀNH MẠCH",           "positive", MO_MAU,    5.0, ""),
 ( 97.26, "MẠCH MÁU *THÔNG THOÁNG*", "PHÒNG *ĐỘT QUỴ, TAI BIẾN*","positive", MAU_TIM, 0, ""),
 (101.46, "DÙNG NGAY", "*NANO NATTOKINASE 60.000 FU*",         "product",  RICHNATTO, 1.0, ""),
 (105.96, "MỘT HỘP *120 VIÊN*", "DÙNG ĐƯỢC *2 THÁNG*",         "product",  NATTO1,    2.0, ""),
 (110.10, "*2.290.000Đ*", "",                                  "yellow",   NATTO_2HOP, 0, ""),
 (113.10, "SAU *15–20 NGÀY*", "ĐẦU *NHẸ*, NGỦ *NGON*",         "positive", NGU_NGON,  2.0, ""),
 (118.84, "ĐỂ *PHÒNG NGỪA ĐỘT QUỴ*", "",                       "warning",  DOT_QUY,   3.0, ""),
 (121.76, "LÀM SẠCH *CỤC MÁU ĐÔNG*", "VÀ *XƠ VỮA*",            "positive", CUC_MAU,  35.0, ""),
 (126.42, "DUY TRÌ *ĐỦ 12 THÁNG*", "GỒM *6 HỘP*",              "product",  RICHNATTO, 4.0, "anh nói 'liệu trình' — giữ, không phải từ cấm"),
 (133.24, "*13.740.000Đ* MỘT NĂM", "",                         "yellow",   NATTO_2HOP, 0, ""),
 (136.00, "TẶNG THÊM *1 HỘP*", "*2.290.000Đ*",                 "product",  NATTO2,    1.0, ""),
 (139.36, "ĐỂ LẠI *TÊN + SỐ ĐIỆN THOẠI*", "DƯỚI VIDEO",        "cta",      NATTO_2HOP, 0, ""),
 (143.14, "HÀNG *CHÍNH HÃNG NỘI ĐỊA NHẬT*", "",                "cta",      RICHNATTO, 0, ""),
 (146.38, "HOẶC GỌI *HOTLINE*", "*0862 188 681*",              "cta",      NATTO_2HOP, 0, ""),
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
