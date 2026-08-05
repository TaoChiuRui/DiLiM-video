# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — 06-2026-08-04-magie-canxi-combo-2.

Bai COMBO: Nano Nattokinase (lo duong ong = mach mau) + Rich Coenzyme Q10
(lo may bom = tim). Day la bai DUY NHAT duoc dung ca natto-* LAN rich-*
lan richnatto-* — vi kich ban ban ca hai.

Da sua cho whisper nghe sai:
  maze -> MAGIE · frevin -> FIBRIN · coenzyme cream 10 -> COENZYME Q10
  mang cua day than kinh -> MANG · lop vo bong -> LOP VO BOC
  cham trich -> CHAM CHICH · kem cho rut -> KEM CHUOT RUT · goc de -> GOC RE
  cai luoi -> CAI LUOI (mang fibrin) · Ben/Bien Thanh -> BEN THANH
  lau cau thang -> LEO CAU THANG · be bo -> met moi · sut tieu den -> CHIET XUAT TIEU DEN
  thong am -> THONG ONG · chon mun mot nam -> TRON MOT NAM
  du may hai thang -> DU 12 THANG · de len de y -> LUU Y

GIA: giu nguyen 31 TRIEU 080 NGHIN (take sau). Take truoc doc 28 trieu 790
va thieu khuyen mai — da cat o cuts.json.

    python3 04-du-an/06-2026-08-04-magie-canxi-combo-2/plan.py
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
 # --- HOOK: te tay te chan, ai cung bao thieu chat ------------------------
 (   0.00, "*TÊ TAY, TÊ CHÂN*",              "TÌM TRÊN MẠNG",                "warning",  DQ_TEBI, 0, "nu xoa co tay — te bi"),
 (   3.98, "AI CŨNG NÓI *THIẾU CHẤT*",       "*THIẾU CANXI*, *THIẾU MAGIE*", "yellow",   "", 0, ""),
 (   9.00, "THIẾU *VITAMIN NHÓM B*",         "RỒI MUA VỀ BỔ SUNG",           "yellow",   "", 0, ""),
 (  12.42, "CÁI ĐÓ *ĐÚNG*",                  "THIẾU THÌ *BỔ SUNG LÀ ĐÚNG*",  "positive", "", 0, ""),
 (  17.48, "NHƯNG CÓ MỘT CHUYỆN",            "*ÍT AI NÓI VỚI ANH CHỊ*",      "yellow",   "", 0, ""),
 (  21.88, "*TÊ TAY, TÊ CHÂN*",              "*KHÔNG CHỈ MỘT NGUYÊN NHÂN*",  "warning",  DQ_TEBI, 18, "lat goc re"),

 # --- CO CHE 1: canxi + magie = lop vo cua day than kinh ------------------
 (  25.74, "*CANXI VÀ MAGIE*",               "LÀM VIỆC RA SAO?",             "yellow",   "", 0, "cau hoi dan"),
 (  30.54, "CANXI + MAGIE GIỮ ỔN ĐỊNH",      "",                             "product",  "", 0, ""),
 (  33.66, "*MÀNG CỦA DÂY THẦN KINH*",       "",                             "product",  NEURON, 8, "neuron xanh"),
 (  37.70, "DÂY THẦN KINH NHƯ *DÂY ĐIỆN*",   "CÓ *LỚP VỎ BỌC*",              "yellow",   TK_XUNG, 0, "10+11 CUNG CLIP -> lien mach; mang than kinh = cai day dien"),
 (  41.82, "CANXI + MAGIE LÀ *LỚP VỎ ĐÓ*",   "ĐỦ THÌ *TÍN HIỆU CHẠY ĐÚNG*",  "positive", TK_XUNG, 0, ""),
 (  46.24, "THIẾU THÌ *LỚP VỎ MỎNG ĐI*",     "*DÂY NHẠY QUÁ MỨC*",           "warning",  TK_DIENNAO, 8, "12+13 CUNG CLIP -> lien mach"),
 (  49.26, "*TỰ PHÁT TÍN HIỆU*",             "DÙ KHÔNG AI CHẠM VÀO",         "warning",  TK_DIENNAO, 8, ""),
 (  53.02, "NÊN THẤY *TÊ, GIẬT GIẬT*",       "*CHÂM CHÍCH*",                 "warning",  DQ_TEBI, 28, "14+15 CUNG CLIP -> lien mach"),
 (  57.58, "*TÊ ĐỐI XỨNG HAI BÊN*",          "ĐẦU NGÓN TAY, *CHUỘT RÚT*",    "warning",  DQ_TEBI, 28, ""),

 # --- CO CHE 2: te do mau thieu oxy --------------------------------------
 (  61.96, "CÒN *MỘT KIỂU TÊ NỮA*",          "KHI *MÁU KHÔNG ĐỦ OXY*",       "warning",  MAU_HC_BC, 0, "16+17 CUNG CLIP -> lien mach; hong cau mang oxy"),
 (  66.98, "*OXY KHÔNG TỚI ĐƯỢC NƠI CẦN*",  "",                             "warning",  MAU_HC_BC, 0, ""),
 (  70.90, "DÂY THẦN KINH",                  "*TIÊU THỤ RẤT NHIỀU OXY*",     "yellow",   NEURON, 0, "18+19 CUNG CLIP -> lien mach"),
 (  74.32, "*THIẾU MỘT CHÚT LÀ BÁO NGAY*",   "",                             "warning",  NEURON, 0, ""),
 (  77.64, "*CŨNG TÊ Y HỆT*",               "",             "warning",  "", 0, "de trong — kho chi co 1 clip te bi, tranh lap qua day"),

 # --- PHAN BIET: cai day vs cai ong --------------------------------------
 (  81.30, "HAI CÁI KHÁC NHAU",              "*TỪ TẬN GỐC RỄ*",              "yellow",   "", 0, "y chot cua ca bai"),
 (  84.66, "MỘT BÊN LÀ *DÂY BỊ MÒN VỎ*",     "MỘT BÊN LÀ *ỐNG BỊ HẸP*",      "warning",  MM_HEP_THAT, 7, "long mach that hep = cai ong bi hep"),
 (  88.82, "CANXI + MAGIE",                  "*SỬA ĐƯỢC CÁI DÂY*",           "positive", TK_TOANTHAN, 0, "he than kinh toan than = cai day"),
 (  92.00, "NHƯNG *KHÔNG SỬA ĐƯỢC ỐNG*",     "",                             "warning",  MM_ONGDONG, 0, "bo ong dong — an du CAI ONG"),
 (  95.52, "CÓ NGƯỜI *UỐNG CANXI MÃI*",      "*MÀ VẪN TÊ*",                  "warning",  DQ_TEBI, 0, ""),

 # --- CACH TU PHAN BIET ---------------------------------------------------
 (  99.44, "*TỰ HỎI MÌNH MỘT CÂU*",         "",                             "yellow",   "", 0, ""),
 ( 103.52, "THÀNH CHIA SẺ MỘT CÁCH",         "ĐỂ *TỰ PHÂN BIỆT*",            "yellow",   "", 0, ""),
 ( 107.40, "NẾU *ĐI BỘ MỘT LÚC*",            "",                             "yellow",   KHO_THO, 0, "28+29 CUNG CLIP -> lien mach; di/leo la moi"),
 ( 110.48, "CHÂN CÓ *MỎI HAY ĐAU THÊM*?",    "",                             "warning",  KHO_THO, 0, ""),
 ( 114.12, "NGỒI MỘT TÍ *CÓ ĐỠ HƠN*?",       "",                             "yellow",   "", 0, ""),
 ( 117.16, "*ĐI THÌ ĐAU, NGHỈ THÌ ĐỠ*",      "",                             "warning",  "", 0, "dau hieu quan trong"),
 ( 120.52, "NGHIÊNG VỀ *MẠCH MÁU*",          "CHỨ KHÔNG PHẢI *THIẾU CHẤT*",  "warning",  MACH_MAU, 0, ""),
 ( 125.10, "LÚC ĐI, CƠ *CẦN NHIỀU MÁU*",     "*ỐNG HẸP* THÌ CẤP KHÔNG KỊP",  "warning",  MM_HEP_THAT, 0, ""),
 ( 129.60, "NGHỈ THÌ *NHU CẦU GIẢM*",        "NÊN *ĐỠ ĐAU HƠN*",             "positive", "", 0, "gop 2 dong: dong sau chi con 0.80s sau khi neo"),
 ( 136.50, "CÒN TÊ DO *THIẾU CHẤT*",         "*ĐI HAY NGHỈ VẪN BỊ*",         "warning",  DQ_TEBI, 18, ""),

 # --- DAU HIEU LANH TAY CHAN ---------------------------------------------
 ( 141.28, "THÊM *MỘT DẤU HIỆU NỮA*",        "",                             "yellow",   "", 0, ""),
 ( 144.46, "TAY CHÂN *HAY BỊ LẠNH*?",        "",                             "warning",  "", 0, ""),
 ( 149.38, "SỜ VÀO *MÁT HƠN*",               "PHẦN CÒN LẠI CỦA CƠ THỂ",      "warning",  CO_THE, 0, "co the + he mach do"),
 ( 153.54, "*MÁU NGOẠI VI TỚI KHÔNG ĐỦ*",    "",                             "warning",  CT_NGUC, 0, "co the trong suot, mach den chi"),

 # --- BO DOI: Nattokinase lo ONG ------------------------------------------
 ( 158.04, "TÊ LIÊN QUAN *MẠCH MÁU*",        "BÊN THÀNH CÓ *MỘT BỘ ĐÔI*",    "product",  RICHNATTO, 0, "HAI HOP — dung bo doi cua bai nay"),
 ( 162.26, "ĐI *ĐÚNG HAI CHỖ*",              "THỨ NHẤT LÀ *NATTOKINASE*",    "product",  NATTO1, 0, ""),
 ( 166.20, "LO *CÁI ĐƯỜNG ỐNG*",             "TỨC LÀ *MẠCH MÁU*",            "product",  MM_ONGDONG, 0, "ong dong — lo cai duong ong"),
 ( 170.68, "ENZYME NÀY",                     "*PHÂN GIẢI SỢI FIBRIN*",       "positive", CUC_MAU, 0, "44+45 CUNG CLIP -> lien mach. VUNG_CAM: chi 0-14s"),
 ( 175.80, "SỢI ĐANG GIỮ *TẾ BÀO MÁU*",      "THÀNH CỤC *TRONG LÒNG MẠCH*",  "warning",  CUC_MAU, 0, ""),
 ( 178.86, "GỠ ĐƯỢC *CÁI LƯỚI* ĐÓ RA",       "*LÒNG MẠCH THÔNG THOÁNG*",     "positive", MM_LONGMACH, 0, "46+47 CUNG CLIP -> lien mach; long mach thoang"),
 ( 182.28, "*MÁU ĐI TỚI NƠI CẦN TỚI*",       "",                             "positive", MM_LONGMACH, 0, ""),

 # --- BO DOI: Rich CoQ10 lo MAY BOM ---------------------------------------
 ( 185.36, "THỨ HAI LÀ *RICH COQ10*",        "LO *PHẦN MÁY BƠM*",            "product",  COQ10_XANH, 0, "phan tu Q10"),
 ( 189.02, "*ÍT AI BIẾT CHỖ NÀY*",           "",                             "yellow",   "", 0, ""),
 ( 192.64, "TRONG MỖI *TẾ BÀO*",             "CÓ BỘ PHẬN *SINH NĂNG LƯỢNG*", "product",  TEBAO, 0, "te bao cat ngang, thay ty the"),
 ( 196.30, "*COENZYME Q10* LÀ XÚC TÁC",      "*BẮT BUỘC* Ở KHÂU CUỐI",       "product",  COQ10_VANG, 0, "51+52 CUNG CLIP -> lien mach"),
 ( 201.86, "ĐỂ *TẠO RA NĂNG LƯỢNG*",         "",                             "product",  COQ10_VANG, 0, ""),
 ( 205.78, "KHÔNG CÓ NÓ, TẾ BÀO",            "*KHÓ TẠO RA NĂNG LƯỢNG*",      "warning",  TEBAO, 6, ""),
 ( 209.60, "TẾ BÀO NÀO CẦN",                 "*NHIỀU NĂNG LƯỢNG NHẤT*?",     "yellow",   "", 0, "cau hoi dan"),
 ( 213.06, "*TẾ BÀO CƠ TIM*",                "",                             "product",  TIM_DAP, 0, "55+56 CUNG CLIP -> lien mach"),
 ( 216.24, "TIM ĐẬP *KHÔNG NGHỈ*",          "SUỐT CẢ ĐỜI",                  "yellow",   TIM_DAP, 0, ""),
 ( 220.00, "*SAU 40 TUỔI*",                  "*TỔNG HỢP Q10 GIẢM DẦN*",      "warning",  COQ10_XANH, 0, ""),
 ( 223.04, "*TIM BƠM YẾU ĐI*",               "MÀ *ÍT NGƯỜI NHẬN RA*",        "warning",  TIM_DMC, 0, "tim + dong mach chu = MAY BOM"),
 ( 227.46, "CHỈ NHẬN RA KHI",                "*LEO CẦU THANG MỆT HƠN XƯA*",  "warning",  KHO_THO, 0, "59+60 CUNG CLIP -> lien mach; leo cau thang met"),
 ( 230.92, "*TAY CHÂN LẠNH HƠN XƯA*",        "HƠI BỊ *HỤT HƠI*",             "warning",  KHO_THO, 0, ""),
 ( 235.06, "LÚC NÀO CŨNG *MỆT MỎI*",         "DÙ *NGỦ ĐỦ 8 TIẾNG*",          "warning",  MM_4K, 0, "met moi keo dai"),

 # --- Q10 dang khu --------------------------------------------------------
 ( 238.08, "*CÒN MỘT ĐIỀU NỮA*",            "",                             "yellow",   "", 0, ""),
 ( 241.38, "Q10 BÊN THÀNH LÀ *DẠNG KHỬ*",    "",                             "product",  RICHNATTO, 0, ""),
 ( 246.06, "Q10 CÓ *2 DẠNG*",                "*OXY HOÁ* VÀ *DẠNG KHỬ*",      "product",  COQ10_VANG, 0, "64+65 CUNG CLIP -> lien mach"),
 ( 250.74, "*DẠNG OXY HOÁ* PHẢI",            "*CHUYỂN ĐỔI* MỚI DÙNG ĐƯỢC",   "warning",  COQ10_VANG, 0, ""),
 ( 256.34, "*NGƯỜI TRUNG NIÊN*",             "HOẶC *ĐƯỜNG RUỘT KÉM*",        "warning",  CT_TIEUHOA, 0, "66+67 CUNG CLIP -> lien mach; duong ruot"),
 ( 260.00, "*KHẢ NĂNG CHUYỂN HOÁ KÉM*",      "",                             "warning",  CT_TIEUHOA, 0, ""),
 ( 263.50, "*DẠNG KHỬ*",                     "CƠ THỂ *DÙNG ĐƯỢC NGAY*",      "positive", COQ10_XANH, 0, ""),
 ( 267.44, "CÒN CÓ *ASTAXANTHIN*",           "*CHỐNG OXY HOÁ*",              "product",  TAO_DO, 0, "tao do — nguon astaxanthin"),
 ( 271.10, "THÊM *CHIẾT XUẤT TIÊU ĐEN*",     "*TĂNG HẤP THỤ Q10*",           "product",  "", 0, ""),

 # --- CHOT: ONG + BOM phai du ca hai --------------------------------------
 ( 274.48, "*HIỂU ĐƠN GIẢN*",             "",           "yellow",   RICHNATTO, 0, "hai hop"),
 ( 277.64, "MỘT BÊN *THÔNG ỐNG*",            "MỘT BÊN *TIẾP SỨC CHO BƠM*",   "product",  MM_ONGDONG, 0, "ong dong = THONG ONG"),
 ( 281.16, "*THÔNG ỐNG MÀ BƠM YẾU*",         "*BƠM KHOẺ MÀ ỐNG TẮC*",        "warning",  TIM_XOAY, 8, "giay 0 la nen trang tron — bat tu 8"),
 ( 286.16, "*TĂNG ÁP LÊN THÀNH MẠCH*",   "*PHẢI CÓ ĐỦ CẢ HAI*",          "warning",  MACH_HEP, 0, ""),

 # --- TRAN AN: van uong canxi/magie duoc ----------------------------------
 ( 290.70, "*NÓI RÕ THÊM*",                 "",                             "yellow",   "", 0, ""),
 ( 294.78, "ĐANG UỐNG *CANXI HAY MAGIE*",    "THÌ *CỨ TIẾP TỤC UỐNG*",       "positive", "", 0, ""),
 ( 299.22, "HAI THỨ NÀY",                    "*KHÔNG PHẢN ỨNG VỚI NHAU*",    "positive", "", 0, ""),
 ( 305.40, "ĐANG UỐNG *CANXI, MAGIE*",      "",                             "yellow",   "", 0, ""),
 ( 308.40, "*MÀ VẪN TÊ TAY*",               "",                             "warning",  DQ_TEBI, 0, "79+80 CUNG CLIP -> lien mach"),
 ( 312.32, "HOẶC *LẠNH TAY, LẠNH CHÂN*",     "THÌ PHẢI *LƯU Ý*",             "warning",  DQ_TEBI, 0, ""),
 ( 315.44, "CÓ *VẤN ĐỀ VỀ MẠCH MÁU*?",       "",                             "warning",  MACH_MAU, 0, ""),
 ( 318.94, "NẾU ĐI KÈM *BỆNH NỀN*",          "",                             "warning",  "", 0, ""),
 ( 322.20, "NHƯ *TIỂU ĐƯỜNG*, *MỠ MÁU*",     "",                             "warning",  MO_MAU, 0, "hat mo vang trong mach"),
 ( 325.92, "THÌ *MẠCH MÁU TỔN THƯƠNG*",      "*ÁCH TẮC CÀNG NHIỀU HƠN*",     "warning",  MACH_TAC, 4, "MIN_START 4 — giay 0 den + logo"),

 # --- LIEU TRINH + GIA ----------------------------------------------------
 ( 329.06, "LIỆU TRÌNH: MỖI THỨ",            "*2 VIÊN 1 NGÀY*",              "product",  RICHNATTO, 0, "lieu — giu nguyen so"),
 ( 332.46, "MỖI HỘP *120 VIÊN*",             "DÙNG ĐƯỢC *2 THÁNG*",          "product",  NATTO1, 0, ""),
 ( 336.38, "ĐỦ *12 THÁNG* LÀ",               "*6 HỘP MỖI LOẠI*",             "product",  RICHNATTO, 0, ""),
 ( 341.96, "MUA CẢ *6 HỘP*",                 "*TẶNG MỖI LOẠI 1 HỘP*",        "product",  RN_ANH_CO, 0, "anh 2 hop tren co — clip richnatto 8.1s khong du 6.3s"),
 ( 348.30, "*GIÁ TRỌN BỘ*",                  "",                             "product",  RICHNATTO, 0, ""),
 ( 351.62, "GIÁ LÀ *31 TRIỆU 080 NGHÌN*",    "",                             "product",  RN_ANH_CO, 0, "gia — giu nguyen"),

 # --- LUU Y TIEU DUONG ----------------------------------------------------
 ( 356.52, "AI *TIỂU ĐƯỜNG LÂU NĂM*",        "",                             "warning",  "", 0, "canh bao an toan"),
 ( 360.94, "THÀNH KHUYÊN *ĐI KHÁM*",         "",                             "warning",  "", 0, ""),
 ( 364.98, "TIỂU ĐƯỜNG GÂY TÊ",              "*THEO NHIỀU CÁCH*",            "warning",  DQ_TEBI, 8, ""),
 ( 367.98, "*KHÔNG THỂ ĐOÁN MÒ ĐƯỢC*",       "",                             "warning",  "", 0, ""),

 # --- CTA -----------------------------------------------------------------
 ( 371.36, "MUỐN *ĐƯỢC TƯ VẤN*",             "ĐỂ LẠI *TÊN + SỐ ĐIỆN THOẠI*", "cta",      "", 0, ""),
 ( 375.94, "THÀNH *GỌI LẠI NGHE KỸ*",        "RỒI MỚI TƯ VẤN",               "cta",      "", 0, ""),
 ( 379.82, "HOẶC GỌI *HOTLINE*",             "",                             "cta",      "", 0, ""),
 ( 383.80, "*0862 745 495*",                 "",                             "cta",      RN_ANH_CO, 0, "hero combo dong bai"),
 ( 387.36, "*SẢN PHẨM NÀY KHÔNG PHẢI LÀ THUỐC*", "KHÔNG THAY THẾ THUỐC CHỮA BỆNH", "product", "", 0, "disclaimer bat buoc — PHAI DU CA HAI VE"),
]


if __name__ == "__main__":
    build(HERE, R)
