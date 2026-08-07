# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — 08-2026-08-02-img0205 (em Hang — tieu hoa).

Da co dong tay tu khung make_plan_draft (ban LUOC v2, commit a8e2190).
Sua whisper: kien khem->kieng khem · buong chay->buon chai · nong rac->nong rat
viem hong(f)->viem hong · mang tinh->man tinh · ba ret->Barrett · goc re->goc re
can bac->can bang · hai khon->hai khuan · chat so->chat xo · Noi quen->Thoi quen
vet tuc tay->vet dut tay · xem->SEM (S.E.M)

Gia doc tu chinh video nay: 3 thang 16.650K (6 men + 9 nghe) ·
6 thang 33.300K (12 men + 18 nghe + tang 1 thang: 2 men + 3 nghe = 14 men + 21 nghe)

    python3 04-du-an/08-2026-08-02-img0205/plan.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "../../03-tool-capcut/pipeline"))
from clips import *        # noqa: F401,F403
from plan_build import build

HERE = os.path.dirname(os.path.abspath(__file__))

# Tra duong dan clip theo TEN FILE tu danh muc kho (1048 clip, co mo ta).
# Cac clip tieu hoa chua co hang so trong clips.py — bai dau tien dung nhom nay.
import json as _json
_KHO = {c["file"]: c["path"] for c in _json.load(open(os.path.join(
    HERE, "../../03-tool-capcut/danh_muc_kho.json"), encoding="utf-8"))}
def K(n):
    return _KHO[n]

# (t, dong1, dong2, variant, clip, src_start, ghi chu)
R = [
 (   0.86, "TIỀN NHIỀU ĐỂ LÀM GÌ",           "*ĐƯỜNG RUỘT* KHÔNG NGHE LỜI",   "yellow",   "", 0, "hook"),
 (   7.54, "BƯƠN CHẢI",                      "CHỊU RẤT NHIỀU *ÁP LỰC*",       "warning",  K("vanphong-aplic-dongnghiep-01.mp4"), 0, ""),
 (  10.90, "CHỈ ĐỂ CÓ ĐƯỢC",                 "PHÚT GIÂY *THOẢI MÁI*",         "positive", K("giadinh-bong-hoanghon-01.mp4"), 0, ""),
 (  14.84, "BÊN GIA ĐÌNH",                   "NHỮNG *BỮA ĂN NGON*",           "positive", K("giadinh-ancom-bep-01.mp4"), 0, ""),
 (  18.36, "VẬY MÀ CŨNG KHÔNG THỂ",          "*TẬN HƯỞNG* ĐƯỢC",              "warning",  K("tieuhoa-nu-onong-sauan-01.mp4"), 0, ""),
 (  22.04, "LẠI LÀ *TRÀO NGƯỢC*",            "*Ợ HƠI, KHÓ THỞ*",              "warning",  K("tieuhoa-nu-ohoi-ban-01.mp4"), 0, ""),
 (  27.14, "BỮA ĂN PHẢI",                    "*KIÊNG KHEM* ĐỦ THỨ",           "warning",  K("anlanh-nu-ansalad-01.mp4"), 0, ""),
 (  34.18, "ĂN UỐNG KHÔNG THOẢI MÁI",        "ĂN LÀ PHẢI CANH *TOILET*",      "warning",  K("tieuhoa-nam-voi-boncau-01.mp4"), 0, ""),
 (  39.20, "ĂN VÀO LÀ *ĐAU BỤNG*",           "ĂN VÀO LÀ *ĐI NGOÀI*",          "warning",  K("tieuhoa-nu-ombung-sofa-01.mp4"), 0, ""),
 (  42.76, "CÒN Ý NGHĨA GÌ NỮA?",            "",                              "yellow",   "", 0, ""),
 (  49.06, "CÔNG SỨC MÌNH BỎ RA",            "",                              "yellow",   K("metmoi-chemat-vanphong-01.mp4"), 0, ""),
 (  52.10, "KHÔNG ĐẠT ĐƯỢC",                 "CHẤT LƯỢNG SỐNG MONG MUỐN",     "warning",  K("metmoi-guc-toi-01.mp4"), 0, ""),
 (  55.72, "HẰNG ĐÃ *HỖ TRỢ* RẤT NHIỀU",      "",                              "positive", "", 0, ""),
 (  60.10, "CŨNG GẶP *TÌNH TRẠNG NÀY*",       "",                              "yellow",   K("tieuhoa-nu-ombung-01.mp4"), 0, ""),
 (  67.08, "HƠN *95%*",                      "CẢI THIỆN TỪNG NGÀY",           "positive", K("ngungon-chiso-suckhoe-01.mp4"), 0, ""),
 (  70.78, "ĐẦU TIÊN PHẢI BIẾT",             "*NGUYÊN NHÂN GỐC RỄ*",          "yellow",   K("noitang-tieuhoa-bung-01.mp4"), 0, ""),
 (  76.98, "TẠI SAO ĂN VÀO",                 "LÀ *ĐI NGOÀI* NGAY?",           "yellow",   K("tieuhoa-nam-ombung-wc-01.mp4"), 0, ""),
 (  80.70, "VẤN ĐỀ KHÔNG NẰM Ở",             "*DẠ DÀY* ĐÂU",                  "yellow",   K("noitang-dady-do-cothe-01.mp4"), 0, ""),
 (  83.68, "MÀ PHẢI ĐI TỪ *ĐẠI TRÀNG*",      "",                              "yellow",   K("noitang-daitrang-cothe-01.mp4"), 0, ""),
 (  86.74, "*HỆ VI SINH* DƯỚI RUỘT",         "ĐÃ *MẤT CÂN BẰNG* LÂU RỒI",     "warning",  K("tieuhoa-longruot-vikhuan-01.mp4"), 120, "giay 2.2 gan nhu trang"),
 (  89.78, "*HẠI KHUẨN* LÊN MEN",            "SINH HƠI, SINH KHÍ",            "warning",  K("tieuhoa-longnhung-loikhuan-01.mp4"), 0, ""),
 (  93.14, "TẤN CÔNG *NIÊM MẠC*",            "ĐẠI TRÀNG",                     "warning",  K("tieuhoa-sodo-daitrang-01.mp4"), 0, ""),
 (  96.30, "NIÊM MẠC NGÀY CÀNG",             "*MỎNG DẦN ĐI*",                 "warning",  K("tieuhoa-longruot-can-01.mp4"), 0, ""),
 ( 100.40, "DỄ *KÍCH THÍCH*",                "KHI THỨC ĂN ĐI QUA",            "warning",  K("noitang-longruot-trong-01.mp4"), 0, ""),
 ( 103.98, "*CO BÓP LIÊN TỤC*",              "VÀ ĐẨY RA NGAY",                "warning",  K("noitang-obung-ruot-01.mp4"), 0, ""),
 ( 107.90, "GIỐNG NHƯ ĐỤNG VÀO",             "*VẾT ĐỨT TAY*",                 "yellow",   "", 0, "vi von"),
 ( 114.16, "ĐẠI TRÀNG CŨNG VẬY",             "LẬP TỨC *ĐẨY THỨC ĂN RA*",      "yellow",   K("noitang-daitrang-cothe-01.mp4"), 0, ""),
 ( 118.16, "NÊN ĂN VÀO LÀ",                  "*ĐI NGOÀI NGAY*",               "warning",  K("tieuhoa-nam-ombung-boncau-01.mp4"), 0, ""),
 ( 121.72, "THỨ 2: HẠI KHUẨN",               "*LÊN MEN ĐỒ ĂN*, SINH KHÍ",     "warning",  K("tieuhoa-vikhuan-canh-01.mp4"), 60, "giay 0 la LOGO ABBOTT - hang khac"),
 ( 125.42, "TĂNG ÁP LỰC Ở BỤNG",             "CẢ *KHOANG BỤNG*",              "warning",  K("tieuhoa-nam-ombung-do-01.mp4"), 0, ""),
 ( 129.68, "CHỊU MỘT *LỰC RẤT LỚN*",          "",                              "warning",  "", 0, ""),
 ( 132.98, "*DẠ DÀY* BỊ ÉP QUÁ MỨC",         "",                              "warning",  K("noitang-dady-do-cothe-02.mp4"), 0, ""),
 ( 137.10, "LÀM BẬT *VAN* DẠ DÀY",           "THỰC QUẢN",                     "warning",  K("noitang-sodo-dady-mangvang-01.mp4"), 16, "giay 0 la co-hong"),
 ( 143.62, "*CHẶN AXIT* TỪ DẠ DÀY",          "ĐI LÊN",                        "yellow",   K("noitang-sodo-dady-hong-01.mp4"), 10, "clip cu la GAN hoat hinh, sai bo phan"),
 ( 150.56, "AXIT *TRÀO NGƯỢC*",              "TỪ DẠ DÀY LÊN",                 "warning",  K("noitang-sodo-dady-vikhuan-01.mp4"), 0, ""),
 ( 153.94, "*Ợ CHUA*",                       "*NÓNG RÁT* THƯỢNG VỊ",          "warning",  K("tieuhoa-nu-onong-ban-01.mp4"), 0, ""),
 ( 159.72, "NGỦ DẬY *ĐẮNG MIỆNG*",           "KHÔ MIỆNG, *VIÊM HỌNG*",        "warning",  K("matngu-nu-ngoiday-01.mp4"), 0, ""),
 ( 164.14, "*KHÓ THỞ*, ĐAU TỨC",             "THỰC QUẢN LIÊN TỤC",            "warning",  K("dotquy-omnguc-ongcu-01.mp4"), 0, ""),
 ( 170.60, "*ĐẠI TRÀNG* KHÔNG ỔN",           "ẢNH HƯỞNG LÊN *DẠ DÀY*",        "yellow",   K("cothe-tieuhoa-01.mp4"), 0, ""),
 ( 179.64, "AXIT *ĂN MÒN THỰC QUẢN*",        "",                              "warning",  K("noitang-dady-mach-01.mp4"), 0, ""),
 ( 182.72, "VIÊM THỰC QUẢN MÃN TÍNH",        "BARRETT, THẬM CHÍ *UNG THƯ*",   "warning",  K("khambenh-ongcu-ombung-01.mp4"), 0, ""),
 ( 187.72, "NGUYÊN TẮC: ĐI TỪ *GỐC RỄ*",     "",                              "yellow",   "", 0, ""),
 ( 194.20, "LÀ MUA THUỐC *GIẢM*",            "TRIỆU CHỨNG Ở ĐÓ",              "yellow",   K("khambenh-duocsi-lothuoc-01.mp4"), 0, ""),
 ( 198.20, "CÓ *TÁI LẠI* KHÔNG?",            "VẪN CÓ",                        "yellow",   K("tieuhoa-nu-ombung-01.mp4"), 0, ""),
 ( 201.80, "THÓI QUEN NUÔI BỆNH",            "VẪN SẼ *TÁI LẠI*",              "warning",  K("doan-nu-burger-quan-01.mp4"), 0, ""),
 ( 205.06, "GỐC RỄ: *HỆ VI SINH*",           "*MẤT CÂN BẰNG*",                "warning",  K("tieuhoa-longruot-vikhuan-01.mp4"), 30, "giay 2.2 gan nhu trang"),
 ( 208.10, "CHƯA GIẢI QUYẾT",                 "VẪN *TÁI LẠI*",                 "warning",  "", 0, ""),
 ( 214.92, "PHẢI *THAY ĐỔI LỐI SỐNG*",       "",                              "yellow",   K("giadinh-nauan-cungnhau-01.mp4"), 0, ""),
 ( 218.42, "HẰNG ÁP DỤNG *BA TRỤ*",          "CHO KHÁCH HÀNG",                "yellow",   "", 0, ""),
 ( 221.68, "LỐI SỐNG *S.E.M*",               "S LÀ *SUPPLEMENT*",             "yellow",   K("anlanh-viennang-vang-01.mp4"), 0, ""),
 ( 229.44, "GIÚP *HỆ TIÊU HÓA*",             "KHỎE HƠN",                      "positive", K("cothe-tieuhoa-01.mp4"), 0, ""),
 ( 233.04, "*NGHỆ MÙA THU OKINAWA*",         "VÀ *MEN INULIN*",               "product",  K("dilimquay-ong-camhop-meninulin-sofa-01.mp4"), 0, ""),
 ( 236.46, "CHẤT XƠ HÒA TAN",                "",                              "product",  K("anlanh-hatchia-rot-01.mp4"), 0, ""),
 ( 240.14, "SUPPLEMENT CÒN MỘT GÓC:",        "*DINH DƯỠNG*",                  "yellow",   K("anlanh-mam-lanhmanh-01.mp4"), 0, ""),
 ( 243.34, "NGƯNG NẠP THỨC ĂN",              "CÓ LỢI CHO *HẠI KHUẨN*",        "warning",  K("doan-xucxich-nuong-01.mp4"), 0, ""),
 ( 247.04, "NẠP *THỊT, CÁ, TRỨNG, SỮA*",     "*ĐẠM, CHẤT XƠ*, THỨC ĂN SẠCH",                              "positive", K("anlanh-raucu-nenxanh-01.mp4"), 0, ""),
 ( 257.40, "E LÀ *EXERCISE* — THỂ THAO",     "TỐT NHẤT: *ĐI BỘ NHANH*",       "positive", K("theduc-bacu-dibo-bobien-01.mp4"), 0, ""),
 ( 260.76, "ỔN ĐỊNH *NHU ĐỘNG RUỘT*",        "VÀ *XẢ STRESS*",                              "positive", K("theduc-bacu-dibo-bobien-01.mp4"), 0, ""),
 ( 268.16, "M LÀ *MEDITATION*",              "NGHỆ THUẬT QUẢN LÝ TÂM TRÍ",    "yellow",   K("theduc-ongcu-khicong-01.mp4"), 0, ""),
 ( 271.38, "KHI *THIỀN*",                    "LÀM CHỦ *CẢM XÚC*",             "positive", K("theduc-ongcu-khicong-01.mp4"), 0, ""),
 ( 278.26, "*ĐƯỜNG RUỘT* SẼ ÊM THEO",        "",                              "positive", K("noitang-longruot-trong-01.mp4"), 0, ""),
 ( 281.46, "LIÊN KẾT QUA",                   "*HỆ TRỤC NÃO - RUỘT*",          "yellow",   K("tieuhoa-truc-nao-ruot-01.png"), 0, ""),
 ( 285.64, "RUỘT LÀ *BỘ NÃO THỨ 2*",         "",                              "yellow",   K("tieuhoa-truc-nao-ruot-01.png"), 0, ""),
 ( 289.08, "TA *CĂNG THẲNG*",                "RUỘT CĂNG THẲNG THEO",          "warning",  K("stress-vanphong-nam-01.mp4"), 0, ""),
 ( 296.11, "NÊN CHỌN LOẠI CÓ",               "*NGUỒN GỐC RÕ RÀNG*",           "product",  "", 0, ""),
 ( 299.43, "CÓ *GIẤY TỜ CHỨNG TỪ*",          "",                              "product",  K("vanphong-nam-dienthoai-hoso-01.mp4"), 0, ""),
 ( 303.89, "ĐẶC BIỆT LÀ HÀNG",               "*NHẬT NỘI ĐỊA*",                "product",  K("dilimquay-meninulin-sofa-01.mp4"), 0, ""),
 ( 307.85, "NGƯỜI NHẬT CŨNG DÙNG",           "ĐỂ *BẢO VỆ* HỆ TIÊU HÓA",       "positive", K("dilimquay-meninulin-sofa-01.mp4"), 0, ""),
 ( 310.99, "NGAY TẠI *NƯỚC SỞ TẠI*",          "",                              "yellow",   "", 0, ""),
 ( 313.99, "HÀNG NHẬT: *AN TOÀN*",           "*CHẤT LƯỢNG* HÀNG ĐẦU",         "product",  K("khambenh-duocsi-donggoi-01.mp4"), 0, ""),
 ( 317.73, "KHI DÙNG *BỘ SẢN PHẨM* NÀY",      "",                              "product",  K("dilimquay-ong-camhop-meninulin-sofa-01.mp4"), 0, ""),
 ( 320.99, "KHẮC PHỤC *TRÀO NGƯỢC*",         "",                              "positive", K("ngungon-vuonvai-cuaso-01.mp4"), 0, ""),
 ( 324.67, "ĂN VÀO ĐI NGOÀI, *TÁO BÓN*",     "TIÊU CHẢY, PHÂN LỎNG",          "positive", K("tieuhoa-cuongiay-01.mp4"), 0, ""),
 ( 327.87, "CÒN GIÚP *TRẢ LẠI*",             "NIÊM MẠC KHỎE",                 "positive", K("tieuhoa-longruot-can-01.mp4"), 0, ""),
 ( 334.61, "ĂN GÌ CŨNG *THẤY NGON*",         "",                              "positive", K("giadinh-anuong-vui-01.mp4"), 0, ""),
 ( 337.87, "ĐỒNG TIỀN KIẾM RA",              "*XỨNG ĐÁNG*",                   "positive", K("giadinh-daigd-ancom-01.mp4"), 0, ""),
 ( 344.26, "*BỘ ĐÔI CHÍNH HÃNG*",             "",                              "product",  K("dilimquay-meninulin-sofa-01.mp4"), 0, ""),
 ( 348.06, "GIÁ *3 THÁNG*",                  "*16.650K*",                     "product",  K("dilimquay-meninulin-sofa-01.mp4"), 0, "gia doc tu video nay"),
 ( 351.18, "GỒM *6 HỘP MEN INULIN*",         "",                              "product",  K("dilimquay-ong-camhop-meninulin-sofa-01.mp4"), 0, ""),
 ( 354.60, "VÀ *9 HỘP NGHỆ MÙA THU*",        "",                              "product",  K("tieuhoa-nghe-bat-01.mp4"), 0, ""),
 ( 358.10, "LIỆU TRÌNH *6 THÁNG*",           "",                              "product",  K("tieuhoa-dohoa-curcumin-sosanh-01.png"), 0, ""),
 ( 361.40, "GIÁ *33.300K*",                  "",                              "product",  "", 0, "gia doc tu video nay"),
 ( 365.42, "NHẬN *12 HỘP MEN*",              "*18 HỘP NGHỆ*",                 "product",  K("dilimquay-meninulin-sofa-01.mp4"), 0, ""),
 ( 371.50, "CỘNG THÊM *1 THÁNG DÙNG*",       "2 HỘP MEN + 3 HỘP NGHỆ",        "product",  K("tieuhoa-nghe-bot-thia-01.mp4"), 0, ""),
 ( 376.82, "TỔNG CỘNG NHẬN",                 "*14 HỘP MEN INULIN*",           "product",  K("dilimquay-ong-camhop-meninulin-sofa-01.mp4"), 0, ""),
 ( 380.76, "VÀ *21 HỘP NGHỆ MÙA THU*",       "",                              "product",  K("tieuhoa-nghe-bat-01.mp4"), 0, ""),
 ( 386.40, "TỔNG: 3 THÁNG *16.650K*",        "",                              "product",  "", 0, ""),
 ( 391.36, "6 THÁNG *33.300K*",              "",                              "product",  "", 0, ""),
 ( 398.72, "ĐỂ NHẬN ĐÚNG *CHÍNH HÃNG*",      "NHẬT BẢN TỪ HẰNG",              "cta",      K("dilimquay-meninulin-sofa-01.mp4"), 0, ""),
 ( 401.90, "ĐỂ LẠI *TÊN + SỐ ĐIỆN THOẠI*",   "DƯỚI VIDEO NÀY",                "cta",      "", 0, ""),
 ( 405.62, "HẰNG HỖ TRỢ LIỆU TRÌNH",         "*CÁ NHÂN HÓA*",                 "cta",      "", 0, ""),
 ( 411.82, "*NỘI ĐỊA NHẬT BẢN*",             "",                              "cta",      K("dilimquay-ong-camhop-meninulin-sofa-01.mp4"), 0, ""),
]


if __name__ == "__main__":
    # Truyen fallback=<anh> neu muon may TU DOI clip qua ngan sang anh do.
    # Mac dinh la BO TRONG — may khong hieu nghia, doi lung tung la sai bai.
    build(HERE, R, giu=True)
