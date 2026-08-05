# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — Dilim Video test, .

Format bam theo templates/job/3_plan.py cua bo Tinh:
    (t0, t1, d1, d2, variant, path, src_start, note)
    *...*  = tu khoa duoc nhan mau
    path="" = CHUA CHON CLIP -> nguoi dung tu gan (xem cot GHI CHU)

MOC THOI GIAN lay THANG tu segment cua mlx-whisper (edit/transcripts/audio16k.json),
KHONG uoc luong tay — de caption/B-roll hien dung luc noi.
"""
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
B = "/Volumes/T7 for Mac/02. Dilim Footage"
FPS = 30
IMG_EXT = (".jpg", ".jpeg", ".png", ".JPG", ".PNG")

# --- clip da xac minh ton tai (03/08/2026) ---
MAT_NGU     = f"{B}/01 Đau đầu - Chóng mặt - Mệt mõi - Bệnh/matngu-nu-ngoiday-01.mp4"
DAU_DAU1    = f"{B}/01 Đau đầu - Chóng mặt - Mệt mõi - Bệnh/daudau-nu-tocvang-01.mp4"
DAU_DAU3    = f"{B}/01 Đau đầu - Chóng mặt - Mệt mõi - Bệnh/daudau-bopmui-nu-01.mp4"
VAI_GAY     = f"{B}/Footage Dilim Quay/dilimquay-vaigay-ong-01.mp4"
MACH_MAU    = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/machmau-catdoc-tim-01.mp4"
HE_MACH_MAU = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/machmau-hetoanthan-01.mp4"
MACH_HEP    = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/machmau-hep-momau-01.mp4"
XO_VUA      = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/xovua-quatrinh-dai-01.mp4"
MANG_MO2    = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/xovua-mangmo-trang-01.mp4"   # anh doi 03/08 (caption 11)
XO_VUA2     = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/xovua-mangbam-vang-02.mp4"
CUC_MAU     = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/cucmau-khoi-fibrin-01.mp4"
XO_VUA_CUC  = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO/momau-can-dongmau-dai-01.mp4"
NGU_NGON    = f"{B}/06 Ngủ- Ngon- mất ngủ/NGỦ NGON.mp4"
NGU         = f"{B}/06 Ngủ- Ngon- mất ngủ/ngungon-chiso-suckhoe-01.mp4"
MEN_GAO_DO  = f"{B}/Natto Xám/men gạo đỏ.mp4"
SP_VIDEO    = f"{B}/03 Rich_Natto_product/DSCF0921.MOV"
SP_VIDEO2   = f"{B}/03 Rich_Natto_product/DSCF0900.MOV"
SP_THONGSO  = f"{B}/03 Rich_Natto_product/DSCF0903.MOV"   # to thong so/nhan
SP_HERO     = f"{B}/03 Rich_Natto_product/richnatto-anh-nenxanh-03.jpg"   # anh hero 2 hop

# (t0, t1, dong1, dong2, variant, path, src_start, ghi chu)
R = [
 # --- KHOI 1: HOOK trieu chung (0-5.4) ---
 ( 0.00,  2.26, "MẤT NGỦ, *ĐAU ĐẦU*",            "ĐAU MỎI *VAI GÁY*",        "warning",  MAT_NGU,    2.0, ""),
 ( 2.26,  3.68, "UỐNG *HOẠT HUYẾT*",             "HOÀI KHÔNG HẾT",           "warning",  "",         0, "THIẾU CLIP: người uống thuốc / vỉ thuốc"),
 ( 3.68,  5.98, "CÓ CÁCH NÀO",                   "*HỖ TRỢ* ĐƯỢC KHÔNG?",     "yellow",   "",         0, "THIẾU CLIP: cô chú lo lắng / hỏi"),

 # --- KHOI 2: LAT GOC RE (6.6-11.6) ---
 ( 6.56,  9.24, "KHÔNG PHẢI DO",                 "*HOẠT HUYẾT*",             "warning",  "",         0, "THIẾU CLIP: dùng lại clip thuốc ở trên"),
 ( 9.24, 11.56, "MÀ NẰM Ở",                      "*LƯU THÔNG MÁU*",          "positive", MACH_MAU,   1.0, ""),

 # --- KHOI 3: RAC RUOI TRONG MACH (11.6-32.4) ---
 (11.56, 15.70, "TRIỆU CHỨNG KÉO DÀI",           "*LÂU NGÀY*",               "warning",  DAU_DAU1,   2.0, ""),
 (15.70, 18.40, "MẠCH MÁU ĐANG",                 "*GẶP VẤN ĐỀ*",             "warning",  MACH_HEP,   1.0, ""),
 (18.40, 21.40, "MẠCH MÁU CÓ QUÁ NHIỀU",         "*RÁC RƯỞI*",               "warning",  XO_VUA_CUC, 2.0, ""),
 (21.40, 23.02, "*RÁC RƯỞI* LÀ SAO?",            "",                         "yellow",   "",         0, "câu hỏi ngắn 1.6s — để chữ chạy một mình"),
 (23.02, 25.10, "RÁC RƯỞI TRONG",                "*MẠCH MÁU*",               "warning",  HE_MACH_MAU, 0, "clip chỉ 5.03s — đủ cho 2.08s"),
 (25.10, 26.54, "*MẢNG XƠ VỮA*",                 "",                         "warning",  MANG_MO2,   3.0, "anh đổi 03/08: Xơ vữa.mp4 -> mang-mo-2.mp4"),
 (26.54, 27.92, "*CỤC MÁU ĐÔNG*",                "",                         "warning",  CUC_MAU,    2.0, ""),
 (27.92, 30.74, "LÀM *TẮC*, LÀM *BÍT*",          "LÀM *NGHẼN* MẠCH MÁU",     "warning",  XO_VUA2,    1.0, "clip 12s"),
 (30.74, 32.36, "MÁU *KHÔNG LƯU THÔNG*",         "",                         "warning",  MACH_HEP,   8.0, "góc khác cùng clip"),

 # --- KHOI 4: HOAT HUYET/MAY BOM CUNG VO ICH (33.2-42.1) ---
 (33.16, 36.28, "MÁU KHÔNG LƯU THÔNG",           "DÙNG *HOẠT HUYẾT*",        "warning",  "",         0, "THIẾU CLIP: dùng lại clip thuốc"),
 (36.28, 38.68, "HAY ĐƯA *MÁY BƠM CAO ÁP*",      "",                         "warning",  "",         0, "THIẾU CLIP: máy bơm / ống nước tắc"),
 (38.68, 42.08, "CŨNG *KHÔNG ĐƯA MÁU ĐI ĐƯỢC*",  "",                         "warning",  MACH_HEP,   15.0, ""),

 # --- KHOI 5: SAN PHAM (42.1-52.5) ---
 (42.08, 45.38, "THÀNH HAY KHUYÊN",              "CÔ CHÚ *DÙNG SẢN PHẨM*",   "product",  SP_VIDEO2,  0.5, ""),
 (45.38, 48.92, "*NANO NATTOKINASE*",            "*60.000 FU*",              "product",  SP_VIDEO,   1.0, "hộp trên cỏ"),
 (48.92, 52.48, "HÀM LƯỢNG *60.000 FU*",         "*LỚN NHẤT* THỊ TRƯỜNG",    "product",  SP_THONGSO, 1.0, "tờ thông số"),

 # --- KHOI 6: ENZYME DANH TAN (53.4-59.0) ---
 (53.36, 56.28, "*NATTOKINASE*",                 "CÓ TÁC DỤNG",              "product",  SP_HERO,    0, "ảnh hero 2 hộp"),
 (56.28, 57.28, "LÀM TAN *CỤC MÁU ĐÔNG*",        "",                         "positive", CUC_MAU,    20.0, ""),
 (57.28, 59.00, "LÀM TAN *MẢNG XƠ VỮA*",         "",                         "positive", XO_VUA,     40.0, ""),

 # --- KHOI 7: MEN GAO DO + CO TRUONG THO (60.2-75.1) ---
 (60.20, 64.58, "NGOÀI HÀM LƯỢNG *RẤT CAO*",     "CỦA *ENZYME NATTO*",       "product",  SP_VIDEO,   5.0, ""),
 (64.58, 66.88, "CÒN CÓ *MEN GẠO ĐỎ*",           "",                         "product",  MEN_GAO_DO, 1.0, ""),
 (66.88, 69.60, "VÀ *CỎ TRƯỜNG THỌ*",            "TỪ *NHẬT BẢN*",            "product",  "",         0, "THIẾU CLIP: cỏ trường thọ / Nhật Bản"),
 (69.94, 71.08, "LÀM GIẢM *MỠ MÁU*",             "",                         "positive", "",         0, "THIẾU CLIP: mỡ máu — thư mục 02 có 'MỠ MAU 2.mp4', chưa xem nội dung"),
 (71.08, 73.56, "MÁU *BỚT ĐẶC*",                 "*BỚT DÍNH*",               "positive", "",         0, "THIẾU CLIP: máu loãng / dòng chảy"),
 (73.56, 75.14, "MÁU *LƯU THÔNG DỄ DÀNG HƠN*",   "",                         "positive", MACH_MAU,   6.0, ""),

 # --- KHOI 8: KHONG CAN HOAT HUYET NUA (76.5-81.6) ---
 (76.54, 78.32, "KHÔNG CẦN *HOẠT HUYẾT* NỮA",    "",                         "positive", "",         0, "THIẾU CLIP"),
 (78.32, 81.62, "MÁU TỰ LƯU THÔNG",              "*TRƠN TRU, DỄ DÀNG*",      "positive", HE_MACH_MAU, 0, ""),

 # --- KHOI 9: VITAMIN NHOM B — THAN KINH — GIAC NGU (82.7-101.3) ---
 (82.66, 85.30, "CÔ CHÚ *MẤT NGỦ LÂU NĂM*",      "",                         "warning",  MAT_NGU,    8.0, ""),
 (85.30, 88.36, "*HỆ THẦN KINH*",                "BỊ *ẢNH HƯỞNG*",           "warning",  "",         0, "THIẾU CLIP: hệ thần kinh — thư mục 02 có 'Thần Kinh', chưa xem"),
 (88.36, 91.66, "TRONG SẢN PHẨM CÒN CÓ",         "*VITAMIN NHÓM B*",         "product",  SP_THONGSO, 3.0, ""),
 (91.66, 94.14, "HỖ TRỢ *NUÔI LẠI*",             "*TRỤC THẦN KINH*",         "positive", "",         0, "THIẾU CLIP: thần kinh"),
 (94.14, 97.26, "KHI *TRỤC THẦN KINH*",          "ĐƯỢC *NUÔI LẠI*",          "positive", "",         0, "THIẾU CLIP: thần kinh"),
 (97.26,101.32, "GIẤC NGỦ *SÂU HƠN*",            "*DỄ DÀNG HƠN*",            "positive", NGU_NGON,   2.0, ""),

 # --- KHOI 10: LIEU TRINH (102.1-111.3) ---
 (102.06,106.98, "DÙNG *NANO NATTOKINASE*",      "TỪ *6 ĐẾN 12 THÁNG*",      "product",  SP_VIDEO,   3.0, ""),
 (106.98,111.32, "HỆ THỐNG MẠCH MÁU",            "ĐƯỢC *PHỤC HỒI*",          "positive", MACH_MAU,   9.0, ""),

 # --- KHOI 11: CTA (112.1-127.3) ---
 (112.14,116.14, "AI ĐANG GẶP",                  "*MẤT NGỦ*",                "warning",  MAT_NGU,    12.0, ""),
 (116.14,118.04, "*ĐAU ĐẦU*",                    "ĐAU MỎI *CỔ VAI GÁY*",     "warning",  VAI_GAY,    1.0, ""),
 (118.04,120.26, "*RỐI LOẠN TIỀN ĐÌNH*",         "MÃI KHÔNG KHỎI",           "warning",  DAU_DAU3,   1.0, ""),
 (120.26,123.98, "LIÊN HỆ *THÀNH*",              "*0862 745 495*",           "cta",      SP_HERO,    0, ""),
 (123.98,127.30, "HOẶC ĐỂ LẠI",                  "*TÊN + SỐ ĐIỆN THOẠI*",    "cta",      SP_VIDEO2,  0.0, "clip chỉ 4.0s — phải bắt đầu từ giây 0 mới đủ 3.32s"),
]


def main():
    segs = json.load(open(os.path.join(HERE, "edit/transcripts/audio16k.json"),
                         encoding="utf-8"))["segments"]

    rows, problems = [], []
    prev_end = None
    for i, (t0, t1, d1, d2, var, p, ss, note) in enumerate(R, 1):
        txt = d1 + ("\n" + d2 if d2 else "")
        if txt.count("*") % 2:
            problems.append(f"caption {i}: dau * le -> {txt!r}")
        if t1 <= t0:
            problems.append(f"caption {i}: t1<=t0 ({t0}-{t1})")
        if prev_end is not None and t0 < prev_end - 0.001:
            problems.append(f"caption {i}: CHONG LEN caption truoc ({t0} < {prev_end})")
        prev_end = t1

        need = t1 - t0
        if p:
            if not os.path.exists(p):
                problems.append(f"caption {i}: KHONG TIM THAY {p}")
            elif not p.endswith(IMG_EXT):
                dur = float(subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                     "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip() or 0)
                if dur - ss < need - 0.03:
                    problems.append(
                        f"caption {i}: CLIP NGAN — {os.path.basename(p)} can {need:.2f}s "
                        f"tu giay {ss}, chi con {dur-ss:.2f}s")

        # loi thoai that su noi trong khung gio nay (de doi chieu timestamp)
        said = " ".join(s["text"].strip() for s in segs
                        if s["end"] > t0 + 0.15 and s["start"] < t1 - 0.15)

        rows.append({
            "idx": i,
            "t": round(t0, 2), "t_end": round(t1, 2),
            "from": round(t0 * FPS), "durationInFrames": round(t1 * FPS) - round(t0 * FPS),
            "d1": d1, "d2": d2, "text": txt, "variant": var,
            "path": p, "src_start": ss, "note": note,
            "said": said,
        })

    out = os.path.join(HERE, "edit/plan.json")
    json.dump(rows, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    have = sum(1 for r in rows if r["path"])
    print(f"caption : {len(rows)}")
    print(f"co B-roll: {have}   |   DE TRONG cho anh gan: {len(rows)-have}")
    print(f"phu song : {rows[0]['t']:.2f}s -> {rows[-1]['t_end']:.2f}s")
    print(f"-> {out}")
    if problems:
        print("\n!!! CAN XEM LAI:")
        for x in problems:
            print("   ", x)
    else:
        print("\nKhong co loi timestamp / clip.")


if __name__ == "__main__":
    main()
