# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — 05-2026-08-04-natto-hoat-huyet.

San pham: Nano Nattokinase 60.000FU (natto-*). KHONG dung rich-* (CoQ10 — bai khac).

Da sua cho whisper nghe sai:
  so vua -> XO VUA · Nato Kinase/engine/chet xuat -> NATTOKINASE/ENZYME/CHIET XUAT
  co truong thot -> CO TRUONG THO · biet tay -> DUT TAY · biet het thuong -> BIT VET THUONG
  khuyen cao thap -> HUYET AP THAP · cuc ngu dong -> CUC MAU DONG
  uong 6 bua toi -> UONG SAU BUA TOI · trong mat -> CHONG MAT · bat ngu -> MAT NGU
  manh mau -> MACH MAU · theo 5 thang -> THEO NAM THANG

DA SOI FRAME 04/08 — ba cai bay tranh duoc (da vao clips.py cho job sau):
  XO_VUA_MODEL  MIN_START cu ghi 6.0 nhung giay 6 VAN con nguyen cau tieng Anh
                "Buildup of plaque in the arteries...". Giay 40 va 50 cung co
                chu. Sach: 9-38s. Bai nay khong dung.
  CUC_MAU       VUNG_CAM: 14-20.5 PLATELET · 22-28.5 RED BLOOD CELL ·
                31-38.5 FIBRIN · 45.5-50.7 logo. Chi dung 0-14s va 38.5-45.5s.
  MACH_TAC      giay 0-3 gan nhu den + logo Helix. Bat tu giay 4 tro di.

DE TRONG 15/67 dong — phan lon la an du ONG NUOC TAC / BOM AP LUC / VI THUOC,
kho chua co (VERSION.md da ghi). Khong nhet clip sai y de lay mat do.

    python3 04-du-an/05-2026-08-04-natto-hoat-huyet/plan.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "../../03-tool-capcut/pipeline"))
from clips import *        # noqa: F401,F403
from plan_build import build

HERE = os.path.dirname(os.path.abspath(__file__))

# (t, dong1, dong2, variant, clip, src_start, ghi chu)
R = [
 # --- HOOK: uong hoat huyet mai ma khong do --------------------------------
 (   0.00, "UỐNG *HOẠT HUYẾT DƯỠNG NÃO*",        "MÃI MÀ *KHÔNG ĐỠ*",                "warning",  NAO,           0, "hook cham dau"),
 (   3.16, "VIDEO NÀY *THÀNH LÀM*",               "CHO ANH CHỊ",                                  "yellow",   "",            0, "noi thang camera — de trong"),
 (   7.18, "*CHÓNG MẶT*, *BUỒN NÔN*",             "HAY LÀ *MẤT NGỦ*",                  "warning",  CM_TUATUONG,   0, "nu tua tuong, tay len tran"),
 (  12.42, "UỐNG HOÀI *KHÔNG ĐỠ*",                "CỨ *THI THOẢNG LÀ BỊ LẠI*",         "warning",  DD_BACU,       0, "ba cu om dau — bi lai"),
 (  15.68, "THÀNH *CHIA SẺ THẬT*",                "*KHÔNG PHẢI HOẠT HUYẾT XẤU*", "yellow",   "",            0, "noi thang camera"),
 (  20.44, "NÓ VẪN *LÀM ĐÚNG VIỆC CỦA NÓ*",       "*NHƯNG CHƯA ĐỦ*",                   "yellow",   "",            0, ""),

 # --- LAT GOC RE: thuc manh cung vo ich neu long mach con tac --------------
 (  24.30, "CHƯA ĐỦ *VIỆC ANH CHỊ ĐANG CẦN*",     "*HOẠT HUYẾT* THÚC MÁU MẠNH", "yellow", MAU_CHAY_2,    5, "dong mau chay xiet"),
 (  29.27, "NHƯNG NẾU *LÒNG MẠCH*",               "CÒN NHIỀU *MẢNG XƠ VỮA*",           "warning",  XO_VUA,       15, "giay 15 = mang vang day, hong cau chen qua (anh Thanh chon 03/08)"),
 (  32.85, "CÒN *CỤC MÁU ĐÔNG*",                  "HAI THỨ LÀM *MẠCH MÁU HẸP*",  "warning",  CUC_MAU,       8, "cuc mau da ket khoi. VUNG_CAM: chi dung 0-14s"),
 (  37.05, "THÌ THÚC MẠNH CỠ NÀO",                "*MÁU CŨNG KHÔNG QUA ĐƯỢC*",         "warning",  MM_HEP_VANG,   0, "hong cau chui qua khe hep"),

 # --- AN DU ONG NUOC (kho chua co clip ong tac — de trong 3 dong) ----------
 (  41.43, "GIỐNG *ỐNG NƯỚC ĐÓNG CẶN DÀY*",       "CÓ TĂNG ÁP, *BƠM GẤP ĐÔI*",         "yellow",   "",            0, "THIEU CLIP: ong nuoc dong can"),
 (  45.49, "*NƯỚC VẪN CHẢY NHỎ GIỌT*",            "*ỐNG CÀNG CHỊU KHÔNG NỔI*", "warning", "",       0, "THIEU CLIP: bom ap luc"),
 (  50.21, "VỚI NGƯỜI MÀ *ỐNG NƯỚC CỦA HỌ*",      "",                                  "yellow",   "",            0, "THIEU CLIP: ong nuoc cu"),
 (  53.43, "CÓ *MẢNG XƠ VỮA LÂU NĂM*",            "ỐNG *MẤT ĐỘ ĐÀN HỒI*",              "warning",  XV_VANG2,      0, "mang vang hai ben thanh mach"),
 (  56.87, "BƠM ÁP SUẤT MẠNH",                    "NHIỀU KHI CÒN *GÂY NGUY HIỂM*",     "warning",  DOT_QUY,       0, "nam om nguc tren sofa"),
 (  60.65, "VIỆC CẦN LÀM KHÔNG PHẢI BƠM", "MÀ LÀ *PHẢI LÀM SẠCH CÁI ỐNG*",    "positive", ANDU_ONGNUOC,  0, "ong nuoc chay thong — chot y an du"),

 # --- CO CHE: cuc mau dong hinh thanh the nao -----------------------------
 (  64.17, "*CỤC MÁU ĐÔNG*",                      "NÓ HÌNH THÀNH THẾ NÀO?",            "yellow",   CM_TRONGMACH,  8, "cau hoi dan"),
 (  67.81, "TRONG MÁU CÓ MỘT CHẤT TÊN LÀ",        "*FIBRIN*",                          "product",  MAU_HC_BC,     0, "hong cau + bach cau troi"),
 (  71.77, "KHI ANH CHỊ *ĐỨT TAY*",               "FIBRIN *ĐAN LẠI THÀNH LƯỚI*",       "yellow",   CUC_MAU,       0, "19+20 CUNG CLIP -> chay lien mach (luat 1). 0-9.2s: hong cau troi roi ket cuc — dung y"),
 (  76.67, "GIỮ *TIỂU CẦU* LẠI",                  "*BỊT VẾT THƯƠNG* LẠI", "positive", CUC_MAU,       0, "Fibrin binh thuong la TOT"),
 (  81.01, "KHÔNG CÓ NÓ THÌ",                     "*CHẢY MÁU KHÓ MÀ CẦM ĐƯỢC*",        "yellow",   "",            0, "THIEU CLIP: vet thuong chay mau"),
 (  85.93, "*MÁU NHIỀU MỠ*, CHẢY CHẬM", "THÀNH MẠCH CÓ *MẢNG XƠ VỮA*",       "warning",  MO_DAY,        0, "mo day hai ben thanh mach — buoc ngoat sang xau"),
 (  89.69, "*LƯỚI FIBRIN* LẠI ĐAN",               "*NGAY TRONG LÒNG MẠCH*",            "warning",  CM_TRONGMACH,  0, "23+24 CUNG CLIP -> chay lien mach"),
 (  93.23, "GIỮ *TẾ BÀO MÁU* LẠI",                "TẠO THÀNH NHỮNG *CỤC*",             "warning",  CM_TRONGMACH,  0, ""),
 (  97.39, "NẰM SẴN Ở ĐÓ",                        "*CẢN TRỞ LƯU THÔNG MÁU*",           "warning",  MACH_TAC,      8, "bat tu giay 8 — giay 0 gan nhu den"),
 ( 101.77, "CƠ THỂ *TỰ TIÊU ĐƯỢC FIBRIN*",        "NHƯNG *SAU TUỔI 40*",               "yellow",   CT_NGUC,       0, "co the trong suot + he mach"),
 ( 107.15, "CHẤT ĐÓ *CÀNG NGÀY CÀNG ÍT DẦN*",     "",                                  "warning",  "",            0, "y truu tuong — de trong"),
 ( 112.27, "*ĐAN VÀO NHANH, GỠ RA CHẬM*", "NÓ CỨ TÍCH TỤ THEO NĂM THÁNG",      "warning",  XV_HINHTHANH,  6, "ca qua trinh hinh thanh mang — dung y 'tich tu'"),

 # --- GIAI PHAP: Nattokinase ----------------------------------------------
 ( 117.25, "VẬY NÊN *NATTOKINASE*",               "CHIẾT TỪ *ĐẬU NÀNH LÊN MEN*", "product", NATTO_2HOP, 0, "anh 2 hop tren tho go (clip natto ngan hon caption 6.2s)"),
 ( 123.45, "THEO CÁCH CỦA *NGƯỜI NHẬT*",          "",                                  "product",  NATTO1,        0, "hop NANO Nattokinase"),
 ( 126.55, "NHIỆM VỤ CỦA NÓ LÀ",                  "*PHÂN GIẢI NHỮNG SỢI FIBRIN*",      "positive", CUC_MAU,      40, "khoi fibrin — giay 40 sach chu"),
 ( 129.87, "HÀM LƯỢNG Ở ĐÂY LÀ TẬN",              "*60.000 FU / GRAM*",                "product",  NATTO2,        0, "so lieu — giu nguyen"),
 ( 133.05, "FIBRIN ĐƯỢC TIÊU ĐI",                 "*LÒNG MẠCH THOÁNG DẦN*",            "positive", MM_LONGMACH,   0, "33+34 CUNG CLIP -> chay lien mach"),
 ( 138.31, "*MÁU TỰ LƯU THÔNG*",                  "KHÔNG CẦN BƠM ÁP LỰC",    "positive", MM_LONGMACH,   0, ""),
 ( 142.97, "THÀNH NÓI *LÀM SẠCH MẠCH MÁU*",       "CHỨ KHÔNG NÓI *HOẠT HUYẾT*",        "yellow",   MANG_MO,       0, "so sanh mach sach / mach mo — y chot ca bai"),
 ( 146.75, "*HAI VIỆC LÀ KHÁC NHAU*",             "",                                  "yellow",   "",            0, "MANG_MO chi 5s, khong keo them duoc"),

 # --- 2 thanh phan it ai de y ---------------------------------------------
 ( 151.07, "TRONG HỘP NATTO CÒN *2 THỨ NỮA*",     "MÀ MỌI NGƯỜI ÍT KHI ĐỂ Ý",          "product",  MEN_GAO,       0, "37+38 CUNG CLIP -> lien mach; natto-01 chi 4.9s < 5.0s"),
 ( 154.71, "*MEN GẠO ĐỎ* VÀ *CỎ TRƯỜNG THỌ*",     "GIÚP *GIẢM MỠ MÁU*",                "product",  MEN_GAO,       0, "men gao do that"),
 ( 159.55, "MÁU *BỚT ĐẶC, BỚT NHỚT*",             "*CHẢY DỄ DÀNG HƠN*",                "positive", MAU_HC_BC,     0, "hong cau troi thong thoang"),
 ( 162.67, "ĐÂY LÀ *XỬ LÝ NGUYÊN NHÂN*",          "LÀM *FIBRIN DỄ ĐAN LẠI*",           "positive", MO_MAU,        0, "hat mo vang trong mach = nguyen nhan"),
 ( 167.33, "THỨ 2 LÀ *VITAMIN NHÓM B*",           "GIÚP *ỔN ĐỊNH HỆ THẦN KINH*",       "product",  TK_DIENNAO,    8, "mang neuron sang — giay 8"),
 ( 171.97, "*BẢO VỆ SỢI TRỤC THẦN KINH*",         "NHIỀU ANH CHỊ *NGỦ SÂU HƠN*",  "positive", NG_CANMAT,     0, "nam trung nien ngu ngon"),

 # --- LIEU DUNG ------------------------------------------------------------
 ( 175.77, "TRƯỚC KHI THẤY *HẾT CHÓNG MẶT*",      "CÁCH DÙNG: *2 VIÊN 1 NGÀY*",        "product",  NATTO1,        0, "natto-02 chi 4.0s < 4.1s"),
 ( 179.71, "UỐNG *SAU BỮA TỐI*",                  "HOẶC *TRƯỚC KHI ĐI NGỦ*",           "product",  NG_DENDEM,     0, "phong ngu, den am — dung gio uong"),
 ( 182.75, "LÝ DO: *CỤC MÁU ĐÔNG*",               "*DỄ HÌNH THÀNH NHẤT*",              "warning",  CM_TRONGMACH,  0, ""),
 ( 186.31, "TỪ *NỬA ĐÊM TỚI SÁNG SỚM*", "",                                  "warning",  NG_NAM_TREN,   0, "nam ngu anh xanh = ban dem"),
 ( 190.47, "ĐỂ SẢN PHẨM *LÀM VIỆC ĐÚNG LÚC*",     "",                                  "product",  NATTO_2HOP,    0, ""),

 # --- TRAN AN: can du thoi gian -------------------------------------------
 ( 193.53, "MỘT ĐIỀU *PHẢI NÓI CHO HẾT*", "",                                "yellow",   "",            0, "noi thang camera"),
 ( 196.55, "*KHÔNG THỂ NHANH ĐƯỢC*",  "",                                  "warning",  "",            0, ""),
 ( 200.43, "*MẠCH MÁU XẤU ĐI*",                   "NÓ CẦN *NHIỀU NĂM*",                "warning",  XV_HINHTHANH,  0, "50+51 CUNG CLIP -> chay lien mach, ca qua trinh"),
 ( 204.61, "KHÔNG CÁCH NÀO *LÀM SẠCH*",    "*TRONG VÀI TUẦN*",                  "warning",  XV_HINHTHANH,  0, ""),
 ( 208.57, "CHUYÊN GIA *NHẬT* KHUYẾN CÁO",    "DÙNG ĐỦ *TỪ 6 ĐẾN 12 THÁNG*",       "product",  NATTO_2HOP,    0, "lieu — giu nguyen so"),
 ( 211.93, "*TÙY VÀO TÌNH TRẠNG*",                "",                                  "yellow",   "",            0, ""),

 # --- CHI PHI --------------------------------------------------------------
 ( 215.03, "VỀ CHI PHÍ: *MỘT HỘP 120 VIÊN*",      "DÙNG ĐƯỢC *2 THÁNG*",               "product",  NATTO_2HOP,    0, "can 6.9s — clip natto deu ngan hon"),
 ( 219.87, "ĐỦ LIỆU TRÌNH *12 THÁNG*",            "LÀ *6 HỘP*",                        "product",  NATTO1,        0, ""),
 ( 223.33, "LẤY ĐỦ LIỆU TRÌNH",                   "BÊN THÀNH *TÍNH 5 HỘP*",            "product",  NATTO_2HOP,    0, "natto-02 chi 4.0s < 4.1s -> dung anh"),
 ( 227.47, "*TẶNG ANH CHỊ HỘP THỨ 6*",            "TỨC LÀ *11 TRIỆU 450 NGHÌN*",       "product",  NATTO_2HOP,    0, "gia — giu nguyen; natto-02 chi 4.0s < 4.6s"),
 ( 231.41, "CHO *TRỌN 1 NĂM*",                    "MỖI NGÀY KHOẢNG *32 NGHÌN ĐỒNG*",   "product",  NATTO1,        0, ""),

 # --- LUU Y AN TOAN --------------------------------------------------------
 ( 235.75, "AI UỐNG *THUỐC CHỐNG ĐÔNG*", "HOẶC *HUYẾT ÁP THẤP*",              "warning",  "",            0, "THIEU CLIP: vi thuoc"),
 ( 239.69, "HOẶC *SẮP PHẪU THUẬT*",               "*HÃY HỎI BÁC SĨ TRƯỚC*",            "warning",  "",            0, "THIEU CLIP: bac si / benh vien"),
 ( 244.83, "ĐỂ ANH CHỊ HIỂU",                     "*ĐIỀU KIỆN MÌNH CẦN DÙNG*",         "yellow",   "",            0, ""),

 # --- CTA ------------------------------------------------------------------
 ( 248.53, "NẾU AI GẶP *ĐAU ĐẦU*, *CHÓNG MẶT*",   "*MẤT NGỦ*",                         "warning",  DD_NU_TN,      0, "nu trung nien xoa thai duong"),
 ( 252.85, "MÀ LIÊN QUAN ĐẾN *MẠCH MÁU*",         "*ĐANG BỊ LƯU THÔNG KÉM*",           "warning",  MACH_HEP,      0, "mang vang lam hep long mach"),
 ( 257.87, "THÌ HÃY *LIÊN HỆ NGAY*",              "QUA *HOTLINE*",                     "cta",      "",            0, "de trong cho so dt noi bat"),
 ( 262.03, "*0862 745 495*",                      "ĐỂ LẠI *TÊN + SỐ ĐIỆN THOẠI*", "cta",     "",            0, "hotline — giu nguyen so"),
 ( 267.03, "DƯỚI VIDEO NÀY CHO THÀNH NHÉ",        "*SẢN PHẨM NÀY KHÔNG PHẢI LÀ THUỐC*", "cta",     NATTO_2HOP,    0, "hero san pham dong CTA"),
 ( 270.35, "VÀ KHÔNG CÓ TÁC DỤNG",                "*THAY THẾ THUỐC CHỮA BỆNH*",        "product",  "",            0, "disclaimer bat buoc"),
]


if __name__ == "__main__":
    build(HERE, R)
