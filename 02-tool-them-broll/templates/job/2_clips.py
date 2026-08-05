# -*- coding: utf-8 -*-
"""Hang so clip cho chu de MO MAU / XO VUA (Raydel Policosanol + Rich Q10).
UU TIEN TUYET DOI kho 'Da Chuan Hoa' - clip nguoi dung tu dat ten theo Y."""
import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline")))
from paths import BROLL_ROOT  # noqa: E402

B = str(BROLL_ROOT)
DCH = os.path.join(B, "Đã Chuẩn Hóa")
MM = os.path.join(B, "Mạch Máu - Thần Kinh - TẾ BÀO")
DQ = os.path.join(B, "Đột quỵ")
DD = os.path.join(B, "Đau đầu - Chóng mặt - Mệt mõi - Bệnh")
LX = os.path.join(B, "Lộn Xộn Xà bần")
PB = os.path.join(B, "Product Broll")
RA = os.path.join(PB, "Raydel Policosanol")
RQ = os.path.join(PB, "Rich Coenzyme Q10")


def d(n):
    p = os.path.join(DCH, n)
    if not os.path.isfile(p):
        raise SystemExit("thieu Da Chuan Hoa: " + n)
    return p


def f(p):
    if not os.path.isfile(p):
        raise SystemExit("thieu: " + p)
    return p


# ---- SAN PHAM ----
RAYDEL = f(os.path.join(RA, "Video", "Raydel policosanol.mp4"))
RAY_NGUYENLIEU = f(os.path.join(RA, "Video", "Video chứa cảnh nguyên liệu, viện nghiên cứu, sáp mía cuba.mp4"))
RAY_VIEN = f(os.path.join(RA, "Video", "Viện nghiên cứu ở cuba+úc.mp4"))
RAY_KETQUA = f(os.path.join(RA, "Video", "kết quả nhiên cứu giảm mỡ xấu và tăng mỡ tốt.mp4"))
RAY_8CHUOI = f(os.path.join(RA, "Video", "sáp mia cuba chưa 8 chuỗi acohol.mp4"))
RAY_CHIETXUAT = f(os.path.join(RA, "Video", "sáp mía được chiết xuất.mp4"))
RAY_ANH = f(os.path.join(RA, "Ảnh", "Raydel Policosanol.JPG"))

# ---- mo mau / xo vua / mach mau (kho Da Chuan Hoa) ----
MO_MAU_CAO = d("mỡ-máu-cao,mỡ-máu,mỡ-trong-máu.mp4")
MO_XAU = d("mang-xo-vưa,mo-xau,moxau-trong-mau.mp4")
MO_TOT = d("Mỡ-tốt-trong máu, mỡ-máu.mp4")
XO_VUA1 = d("mảng-xơ-vữa-1.mp4")
XO_VUA3 = d("mảng-xơ-vữa-3.mp4")
XO_VUA_HINH_THANH = d("mo-mau,hinh-thanh-xo-vua-3.mp4")
MACH_THONG = d("mạch-máu-thông-thoáng-1.mp4")
MACH_THONG2 = d("mach-mau-thong-thoang-1,on-dinh-xo-vua.mp4")
MACH_DAN_HOI = d("mach-mau-dan-hoi,on-dinh-xo-vua,thanh-mach-dan-hoi-tot.mp4")
TUAN_HOAN = d("he-tuan-hoan,tuan-hoan,he-mach-mau.mp4")
TIM_MACH = d("Hệ-tim-mạch.mp4")
TIM_MACH1 = d("Hệ-tim-mạch-1.mp4")
CUC_MAU_DONG = d("Cục-máu-đông.mp4")
TAC_MACH = d("cuc-mau-dong-lam-tac-mach, tac-mach-mau-o-tim,tac-mach-dot-quy.mp4")
NHOI_MAU = d("nhoi-mau-co-tim-1,benh-tim-mạch.mp4")

# ---- Q10 / nang luong te bao ----
Q10_CAM = d("Coenzyme Q10 -mau-cam.mp4")
Q10_XANH = d("Coenzyme Q10- màu-xanh.mp4")
NANG_LUONG_TB = d("nang-luong-te-bao-1,nang-luong-ben-trong,san-xuat-nang-luong-atp.mp4")
NAO_THIEU_NL = d("Não-thiếu-năng-lượng.mp4")
NAO_TOT = d("nao-hoat-dong-tot,bao-ve-mo-than-kinh-1.mp4")

# ---- trieu chung ----
MET_MOI = d("met-moi,met-moi-khong-ro-nguyen-nhan.mp4")
MET_MOI2 = d("kem-tap-trung,met-moi,thieu-nang-luong.mp4")
DAU_DAU1 = d("dau-dau-1,chong-mat,.mp4")
DAU_DAU2 = d("dau-dau,chong-mat-2.mp4")
DAU_DAU3 = d("dau-dau-3,chong-mat.mp4")
VAI_GAY = d("dau-moi-vai-gay-1,dau-co-vai-gay.mp4")
VAI_GAY2 = d("dau-moi-vai-gay-2.mp4")
CHONG_MAT = d("Dau-dau,chong-mat.mp4")
MAT_NGU = d("Mat-ngủ-1,ngu-khong-sau-giac.mp4")
MAT_NGU2 = d("mat-ngu-2.mp4")
TE_BI1 = d("te-bi-chan-tay-1.mp4")
TE_BI2 = d("te-bi-chan-tay-2.mp4")
TIEN_DINH = d("dau-dau-2,chong-mat,Roi-loan-tien-dinh.mp4")
DOT_QUY1 = d("dot-quy-1.mp4")
DOT_QUY2 = d("dot-quy-2.mp4")
DOT_QUY3 = d("dot-quy-3.mp4")

# ---- khoe manh / ket ----
CHAY_BO_TN = d("Trung-nien-chay-bo,giam-met-moi-2.mp4")
GIAM_MET = d("giam-met-moi-1.mp4")
TIM_KHOE1 = d("tim-khỏe-1.mp4")
TIM_KHOE2 = d("tim-khỏe-2.mp4")
NGU_NGON = d("ngu-ngon,ngu-sau-giac.mp4")

# ---- an du flagship / nguyen lieu ----
MAYBACH = f(r"D:\download\mercedes-maybach-gls-480-4matic-noi-that-ngoai-that-gia-ban-mercedeshaxaco-com-vn-2023-2024-2025-3.jpg")
SIEU_XE = f(os.path.join(LX, "SIEU XE.mp4"))
MIA1 = f(os.path.join(LX, "cánh đồng mía.mp4"))
MIA2 = f(os.path.join(LX, "cánh đồng mía-2.mp4"))
MIA3 = f(os.path.join(LX, "MÍA.mp4"))
AFC_TOA_NHA = f(os.path.join(B, "Dilim", "afc-3.jpg"))
AFC_NHA_MAY = d("nha-may-afc-nhat-ban_1.10.1_1.10.1.jpg")

# ---- kham benh / xet nghiem ----
KB = os.path.join(B, "Khám bệnh - Bác Sĩ - uống Thuốc- bệnh khác")
BS_TU_VAN = f(os.path.join(KB, "007 - bác sĩ đang giải thíchtư vấn kết quả khám bệnh, tay.mp4"))
LAY_MAU = f(os.path.join(KB, "017 - Người dùng tự chích đầu ngón tay bằng bút lấy máu để.mp4"))
CTA = f(os.path.join(B, "CTA", "DE LAI TEN VA SDT.mov"))

PRODUCT_SET = {RAYDEL, RAY_NGUYENLIEU, RAY_VIEN, RAY_KETQUA, RAY_8CHUOI,
               RAY_CHIETXUAT, RAY_ANH, CTA}

# ---- bo sung cho V2 ----
TAO_DO = f(os.path.join(LX, "tao_do_nhat_ban_co_tac_dung_gi_va_mot_so_dieu_can_luu_y_khi_su_dung_tao_do_nhat_ban_0_bdc2715375.jpg"))
TE_BAO_MO = f(os.path.join(B, "Giảm cân - Mập, tăng cân", "download - 2026-06-10T133449.710.mp4"))     if os.path.isfile(os.path.join(B, "Giảm cân - Mập, tăng cân", "download - 2026-06-10T133449.710.mp4"))     else d("mo-noi-tang,tang-mo-noi-tang,mo-bao-quanh-noi-tang.mp4")
GAN = d("gan-nhiem-mo.mp4")
COMBO_RAY = f(os.path.join(PB, "Ảnh Combo Sản Phẩm", "Combo Raydel policosanol + Rich Coenzyme Q10.jpg"))
NHIEU_THUOC = d("uong-thuoc,uong-nhieu-loai-thuoc.mp4")
