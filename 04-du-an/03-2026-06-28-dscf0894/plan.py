# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — DSCF0894 (ban da cat, 2:58.4).

Moc `t` ben duoi la UOC LUONG; script tu SNAP vao `start` cua chu gan nhat
va dat `t_end` = `t` cua caption ke tiep. KHONG dung `end` cua whisper
(xem cut.py: `end` nuot ca khoang lang phia sau, khong dang tin).

    python3 plan.py
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = "/Volumes/T7 for Mac/02. Dilim Footage"
IMG_EXT = (".jpg", ".jpeg", ".png", ".JPG", ".PNG")

# --- clip da xac minh ton tai ---
MAT_NGU   = f"{B}/01 Đau đầu - Chóng mặt - Mệt mõi - Bệnh/matngu-nu-ngoiday-01.mp4"
DAU_DAU1  = f"{B}/01 Đau đầu - Chóng mặt - Mệt mõi - Bệnh/daudau-nu-tocvang-01.mp4"
DAU_DAU3  = f"{B}/01 Đau đầu - Chóng mặt - Mệt mõi - Bệnh/daudau-bopmui-nu-01.mp4"
VAI_GAY   = f"{B}/Footage Dilim Quay/dilimquay-vaigay-ong-01.mp4"
MACH_MAU  = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/machmau-catdoc-tim-01.mp4"
HE_MACH   = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/machmau-hetoanthan-01.mp4"
MACH_HEP  = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/machmau-hep-momau-01.mp4"
XO_VUA    = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/xovua-quatrinh-dai-01.mp4"
XO_VUA2   = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/xovua-mangbam-vang-02.mp4"
MANG_MO2  = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/xovua-mangmo-trang-01.mp4"
CUC_MAU   = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/cucmau-khoi-fibrin-01.mp4"
XO_CUC    = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/momau-can-dongmau-dai-01.mp4"
NGU_NGON  = f"{B}/06 Ngủ- Ngon- mất ngủ/NGỦ NGON.mp4"
MEN_GAO   = f"{B}/Natto Xám/men gạo đỏ.mp4"
SP_CO     = f"{B}/03 Rich_Natto_product/DSCF0921.MOV"
SP_LA     = f"{B}/03 Rich_Natto_product/DSCF0900.MOV"
SP_THONGSO= f"{B}/03 Rich_Natto_product/DSCF0903.MOV"
SP_HERO   = f"{B}/03 Rich_Natto_product/richnatto-anh-nenxanh-03.jpg"

# (t_uoc_luong, dong1, dong2, variant, path, src_start, ghi chu)
R = [
 # --- 1. HOOK trieu chung ---
 (  0.00, "CÔ BỊ *MẤT NGỦ*", "*ĐAU ĐẦU*",                    "warning",  MAT_NGU,   2.0, ""),
 (  4.44, "ĐAU MỎI *CỔ VAI GÁY*", "*TÊ BÌ TAY CHÂN*",         "warning",  VAI_GAY,   1.0, ""),
 (  6.10, "UỐNG *HOẠT HUYẾT*", "HOÀI KHÔNG HẾT",              "warning",  "",        0, "THIẾU CLIP: vỉ thuốc / uống thuốc"),
 (  7.14, "CÓ CÁCH NÀO", "*HỖ TRỢ* ĐƯỢC KHÔNG?",              "yellow",   "",        0, "THIẾU CLIP: cô chú lo lắng"),

 # --- 2. LAT GOC RE ---
 ( 10.16, "TÌNH TRẠNG NÀY", "*HOẠT HUYẾT* KHÔNG XỬ LÝ ĐƯỢC",  "warning",  "",        0, "THIẾU CLIP: dùng lại clip thuốc"),
 ( 12.90, "KHÔNG XỬ LÝ ĐƯỢC", "*TẬN GỐC RỄ*",                 "warning",  MACH_HEP,  1.0, ""),
 ( 20.46, "VẤN ĐỀ CHÍNH", "KHÔNG PHẢI *HOẠT HUYẾT*",          "warning",  "",        0, "THIẾU CLIP"),
 ( 23.94, "MÀ LÀ", "*LƯU THÔNG MẠCH MÁU*",                    "positive", MACH_MAU,  1.0, ""),

 # --- 3. RAC RUOI TRONG MACH ---
 ( 27.16, "MẤT NGỦ, ĐAU ĐẦU", "ĐAU MỎI *CỔ VAI GÁY*",         "warning",  DAU_DAU1,  2.0, ""),
 ( 30.62, "*TÊ BÌ TAY CHÂN*", "LÂU NGÀY",                     "warning",  DAU_DAU3,  1.0, ""),
 ( 33.54, "MẠCH MÁU ĐÃ CÓ", "RẤT NHIỀU *RÁC RƯỞI*",           "warning",  XO_CUC,    2.0, ""),
 ( 36.30, "*RÁC RƯỞI* Ở ĐÂY LÀ GÌ?", "",                      "yellow",   "",        0, "câu hỏi ngắn — để chữ chạy một mình"),
 ( 37.60, "LÀ NHỮNG *CỤC MÁU ĐÔNG*", "",                      "warning",  CUC_MAU,   2.0, ""),
 ( 38.88, "LÀ NHỮNG *MẢNG XƠ VỮA*", "",                       "warning",  MANG_MO2,  3.0, "anh chọn clip này ở job trước"),
 ( 41.96, "MẠCH MÁU BỊ *TẮC*", "BỊ *KẸT*, BỊ *BÍT*",          "warning",  XO_VUA2,   1.0, ""),
 ( 46.24, "MÁU *KHÔNG LƯU THÔNG*", "ĐƯỢC BÌNH THƯỜNG",        "warning",  MACH_HEP,  8.0, ""),

 # --- 4. SAN PHAM ---
 ( 48.64, "VỚI TÌNH TRẠNG NÀY", "THÀNH LUÔN *GIỚI THIỆU*",    "product",  SP_HERO,   0, "đổi từ DSCF0900 (chỉ 4.0s, cần 5.3s) sang ảnh hero"),
 ( 53.90, "*NANO NATTOKINASE*", "*60.000 FU*",                "product",  SP_CO,     1.0, "hộp trên cỏ"),
 ( 62.00, "HÀM LƯỢNG *60.000 FU*", "TRÊN GRAM",               "product",  SP_THONGSO, 1.0, "tờ thông số"),
 ( 66.14, "*CAO NHẤT* THỊ TRƯỜNG", "HIỆN NAY",                "product",  SP_HERO,   0, "ảnh hero 2 hộp"),

 # --- 5. ENZYME DANH TAN ---
 ( 71.32, "*NATTOKINASE* HỖ TRỢ", "LÀM TAN *CỤC MÁU ĐÔNG*",   "positive", CUC_MAU,   20.0, ""),
 ( 74.84, "LÀM TAN", "*MẢNG XƠ VỮA*",                         "positive", XO_VUA,    40.0, ""),

 # --- 6. MEN GAO DO + CO TRUONG THO ---
 ( 77.78, "CÒN CÓ *MEN GẠO ĐỎ*", "",                          "product",  MEN_GAO,   1.0, ""),
 ( 80.60, "VÀ *CỎ TRƯỜNG THỌ*", "CHIẾT XUẤT TỪ *NHẬT BẢN*",   "product",  "",        0, "THIẾU CLIP: cỏ trường thọ / Nhật Bản"),
 ( 84.60, "GIÚP *HẠ MỠ MÁU*", "",                             "positive", "",        0, "THIẾU CLIP: mỡ máu"),
 ( 87.86, "MÁU *BỚT ĐẶC*", "CHẢY *TRƠN TRU HƠN*",             "positive", MACH_MAU,  6.0, ""),

 # --- 7. VITAMIN B - THAN KINH - NGU ---
 ( 93.20, "CÔ CHÚ *MẤT NGỦ LÂU NĂM*", "VÔ CÙNG *MỆT MỎI*",    "warning",  MAT_NGU,   8.0, ""),
 ( 97.42, "CÒN CÓ ĐẦY ĐỦ", "*VITAMIN NHÓM B*",                "product",  SP_THONGSO, 3.0, ""),
 (101.28, "*NUÔI DƯỠNG LẠI*", "*HỆ THẦN KINH*",               "positive", "",        0, "THIẾU CLIP: hệ thần kinh"),
 (104.62, "KHI *TRỤC THẦN KINH*", "ĐƯỢC *NUÔI DƯỠNG*",        "positive", "",        0, "THIẾU CLIP: hệ thần kinh"),
 (107.30, "*NGỦ SÂU* LÀ ĐIỀU", "*HIỂN NHIÊN, DỄ DÀNG*",       "positive", NGU_NGON,  2.0, ""),

 # --- 8. LIEU TRINH + AN DU 100.000 KM ---
 (112.08, "NHƯNG PHẢI *LƯU Ý*", "MỘT ĐIỀU",                   "yellow",   "",        0, "THIẾU CLIP"),
 (116.28, "ĐỂ *LÀM SẠCH MẠCH MÁU*", "MỘT CÁCH *TOÀN DIỆN*",   "positive", MACH_HEP,  12.0, "đổi từ HE MẠCH MAU (5.0s, cần 6.3s)"),
 (122.50, "NÊN *DÙNG ĐỦ*", "*6 ĐẾN 12 THÁNG*",                "product",  SP_CO,     3.0, "anh nói 'điều trị' — STYLE.md CẤM, đổi thành 'dùng đủ'"),
 (126.52, "HỆ THỐNG MẠCH MÁU", "TRONG CƠ THỂ *RẤT DÀI*",      "positive", MACH_MAU,  9.0, ""),
 (129.72, "DÀI KHOẢNG", "*100.000 KM*",                       "yellow",   "",        0, "THIẾU CLIP: bản đồ / trái đất"),
 (134.18, "GẤP *2,5 LẦN*", "*VÒNG TRÁI ĐẤT*",                 "yellow",   "",        0, "THIẾU CLIP: trái đất"),

 # --- 9. KET QUA SOM ---
 (137.00, "KHI DÙNG SẢN PHẨM", "",                            "product",  SP_CO,     5.0, "đổi từ DSCF0900 (còn 2.5s, cần 4.0s)"),
 (141.02, "*ĐAU ĐẦU, MẤT NGỦ*", "GIẢM *20–30%*",              "positive", MAT_NGU,   12.0, ""),
 (144.54, "TRONG *5 ĐẾN 15 NGÀY ĐẦU*", "",                    "positive", NGU_NGON,  8.0, ""),
 (148.58, "NHƯNG ĐỂ *ĐI SÂU TOÀN DIỆN*", "",                  "warning",  "",        0, "THIẾU CLIP"),
 (152.12, "LÀM *HỆ TUẦN HOÀN*", "*TƯƠI MỚI LẠI*",             "positive", HE_MACH,   0, ""),
 (155.80, "VẪN PHẢI *ĐỦ 6–12 THÁNG*", "",                     "product",  SP_CO,     6.0, ""),

 # --- 10. CTA ---
 (158.84, "AI ĐANG GẶP", "*MẤT NGỦ, ĐAU ĐẦU*",                "warning",  MAT_NGU,   4.0, ""),
 (161.94, "*ĐAU MỎI VAI GÁY*", "*TÊ BÌ TAY CHÂN*",            "warning",  VAI_GAY,   3.0, ""),
 (164.82, "HAY *RỐI LOẠN TIỀN ĐÌNH*", "MÃI KHÔNG KHỎI",       "warning",  DAU_DAU3,  1.0, ""),
 (167.52, "GỌI NGAY CHO THÀNH", "*0862 745 495*",             "cta",      SP_HERO,   0, ""),
 (173.90, "HOẶC ĐỂ LẠI", "*TÊN + SỐ ĐIỆN THOẠI*",             "cta",      SP_LA,     0, ""),
 (176.54, "ĐỂ THÀNH *HỖ TRỢ KỊP THỜI*", "",                   "cta",      SP_HERO,   0, ""),
]

MIN_DUR = 0.80        # caption ngan nhat cho phep
LEAD_IN = 0.06        # bat som hon chu dau mot chut cho de doc


def main():
    words = json.load(open(os.path.join(HERE, "edit/words_cut.json"), encoding="utf-8"))
    end_all = max(w["s"] for w in words) + 1.2

    # SNAP moc bat dau vao `start` cua chu gan nhat
    rows, probs = [], []
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
                if dur - ss < (t1 - t0) - 0.03:
                    probs.append(f"caption {i}: CLIP NGAN {os.path.basename(p)} "
                                 f"can {t1-t0:.2f}s tu giay {ss}, con {dur-ss:.2f}s")

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
    if probs:
        print("\n!!! CAN XEM LAI:")
        for x in probs:
            print("   ", x)
    else:
        print("\nKhong co loi.")


if __name__ == "__main__":
    main()
