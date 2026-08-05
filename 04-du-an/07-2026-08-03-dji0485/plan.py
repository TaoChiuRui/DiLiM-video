# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — 07-2026-08-03-dji0485.

KHUNG NAY DO make_plan_draft.py SINH RA — chua phai ban dung duoc.
Con phai lam 4 viec, theo thu tu:

  1. CO DONG chu. Dong 1 + dong 2 hien dang la LOI NOI NGUYEN VAN. Caption la
     diem tua cho mat, khong phai phu de. Bo tu dem, bo lap, giu y va giu
     dung so lieu / ten san pham.
  2. Danh *TU KHOA*. Bo cap dau * quanh cum can nhan — dung do le mot dau.
  3. Soat `variant`. Dong nao con `#?` la MAY DOAN, chua ai xac nhan.
     warning = y tieu cuc · positive = y tich cuc · product = san pham/gia
     yellow = so lieu, vi von · cta = ket video
  4. Chon CLIP. Chay `suggest_clips.py --job <job> --md` roi dien vao cot
     thu 5. De "" nghia la caption do khong co B-roll — chap nhan duoc, tot
     hon la nhet clip sai y.

Moc `t` da la `start` cua chu that, khong phai uoc luong — dung sua tay tru
khi co ly do. Buoc 4_anchor.py se neo lai lan nua sau khi chu duoc co dong.

    python3 07-2026-08-03-dji0485/plan.py
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
 # --- KHOI 1: loi cam ket cua NGUOI KHAC (hook) ---
 # 4 dong dau de TRONG co chu y: day la loi NGUOI KHAC hua. Khong co hinh nao
 # minh hoa duoc "cam ket khoi han" ma khong bien no thanh loi hua cua DiLiM.
 (   0.00, "*CAM KẾT* VỚI CÔ CHÚ ANH CHỊ",   "KHI DÙNG *LỘ TRÌNH NÀY*",     "yellow",    "",             0,   ""),
 (   3.32, "SAU MỘT THỜI GIAN",              "LÀ *KHỎI HẲN* VẤN ĐỀ NÀY",    "yellow",    "",             0,   ""),
 (   6.55, "*ĐAU ĐẦU*, *CHÓNG MẶT*",         "",                            "warning",   DD_ONGCU1,      1.0, "ong cu om tran"),
 (   7.77, "*ĐAU MỎI VAI GÁY*",              "*TÊ BÌ CHÂN TAY*",            "warning",   VAI_GAY,        0.5, ""),

 # --- KHOI 2: cu lat — do la loi nguoi khac, Thinh khong cam ket ---
 # De trong ca khoi: day la doan anh nhin thang camera phu nhan. Cat sang
 # B-roll o day la lam loang cai nhin.
 (   9.64, "ĐÓ LÀ CÂU NÓI",                  "*CỦA NGƯỜI KHÁC*",            "yellow",    "",             0,   ""),
 (  11.70, "CÒN THỊNH *KHÔNG BAO GIỜ*",      "*CAM KẾT* ĐIỀU NÀY",          "highlight", "",             0,   ""),

 # --- KHOI 3: vi co chu chua lam phan cua minh ---
 (  15.50, "NẾU VẪN CÒN",                    "*THỨC KHUYA*",        "warning",   MM_DEM,         1.0, "met moi ban dem"),
 (  18.54, "VẪN CÒN KHÔNG",                  "*CHĂM SÓC SỨC KHỎE*",         "warning",   MM_CHEMAT1,     1.0, "ong cu met moi"),
 # KHONG dung clip the duc o day — cau nay noi ve viec KHONG tap. Kho chua co
 # clip "ngoi li khong van dong"; MM_SOFA nhin ra dau dau chu khong ra luoi
 # van dong. Cho MM_CHEMAT1 chay lien mach tu dong tren thay vi doi hinh sai y.
 (  20.28, "VẪN CÒN KHÔNG",                  "*THỂ DỤC THỂ THAO*",          "warning",   MM_CHEMAT1,     1.0, "chay tiep tu tren"),

 # --- KHOI 4: Thinh can khach, nhung khong ban su that ---
 (  29.60, "THỊNH *RẤT CẦN KHÁCH HÀNG*",     "",                            "highlight", "",             0,   ""),
 (  31.24, "NHƯNG THỊNH",                    "*KHÔNG BAO GIỜ BỎ QUA*",      "positive",  "",             0,   ""),
 # 34.29 + 36.38 CUNG clip -> dai B-roll chay lien mach qua 2 caption (luat 1).
 (  34.29, "*GIÁ TRỊ* CỦA VIỆC",             "*THỂ DỤC THỂ THAO*",          "positive",  TD_ONGBA_PHO,   2.0, "ong ba di bo the duc"),

 # --- KHOI 5: the duc la NEN TANG ---
 (  36.38, "TẠI VÌ *SỨC KHỎE*",              "VÀ *RÈN LUYỆN* THỂ THAO",     "positive",  TD_ONGBA_PHO,   2.0, "chay tiep tu tren"),
 (  39.46, "ĐÓ LÀ CÁI *NỀN TẢNG*",           "ĐỂ *TRAO ĐỔI CHẤT*",          "positive",  CT_TIEUHOA,     1.0, "he tieu hoa"),
 (  42.58, "CŨNG NHƯ *TUẦN HOÀN MÁU*",       "ĐƯỢC TỐT HƠN"            ,   "positive",  HE_MACH,        1.0, "he mach toan than"),

 # --- KHOI 6: nguoi mat ngu — phai thien dinh ---
 (  46.14, "NGAY CẢ NGƯỜI",                  "BỊ *MẤT NGỦ*",                "warning",   MN_ONGCU,       1.0, "ong cu mat ngu"),
 (  48.74, "TÌM ĐẾN THỊNH MÀ",               "KHÔNG *THIỀN ĐỊNH* ĐƯỢC",     "warning",   MN_ONGCU,       1.0, "chay tiep tu tren"),
 (  51.72, "KHÔNG CÓ *TINH TẤN*",            "",                            "warning",   TD_SU_KHATTHUC, 0.5, "su di khat thuc — 'tinh tan'"),
  (  53.18, "*THIỀN ĐỊNH* MỖI NGÀY",          "ĐỂ *TÂM TRÍ SÁNG SUỐT*",      "positive",  TD_KHICONG_O,   1.0, "ong cu tap khi cong"),

 # --- KHOI 7: dong bo sung la can thiet, nhung chua du ---
 (  60.05, "DÙNG *DÒNG BỔ SUNG*",            "BÊN THỊNH",                   "product",   RICHNATTO,      0.5, ""),
 (  64.51, "NHƯNG THỊNH LUÔN",               "*KHUYẾN KHÍCH* MỖI NGÀY",     "positive",  "",             0,   ""),
 (  67.79, "*DÙ BẬN RỘN* CỠ NÀO",            "",                            "yellow",    STRESS_VP,      1.0, "ban ron van phong"),
 (  69.89, "HÃY *THỂ DỤC THỂ THAO*",         "TỪ *5 ĐẾN 15 PHÚT* MỖI NGÀY", "positive",  TD_ONGCU_CO,    1.0, "ong cu chay bo bai co"),

 # --- KHOI 8: viec so 2 — thien + an uong thanh dam ---
 (  73.63, "CÁI *SỐ 2* NỮA LÀ GÌ?",          ""                     ,       "yellow",    "",             0,   ""),
 (  75.97, "DÀNH *THỜI GIAN* RA",            "ĐỂ MÌNH *THIỀN*",             "positive",  TD_KHICONG_B,   1.0, "ba cu tap tho bai co"),
 (  78.58, "*ĂN UỐNG THANH ĐẠM*",            "NHỮNG LOẠI RAU",              "positive",  AU_RAU_CHO,     2.0, "quay rau xanh o cho"),
 (  82.26, "*THỨC ĂN TỐT*",                  "CHO SỨC KHỎE",                "positive",  AU_MAM_LANH,    0.5, "mam do an lanh manh"),

 # --- KHOI 9: bo 3 — the duc / an uong / dong bo sung ---
 (  89.08, "HÃY *XUẤT PHÁT TỪ 3 CÁI*",       "",                            "yellow",    "",             0,   ""),
 (  91.30, "*MỘT*: THỂ DỤC THỂ THAO",        "",                            "positive",  TD_ONGBA_VUI,   1.0, "hai ong ba di bo, cuoi"),
 (  93.32, "*HAI*: ĂN UỐNG ĐIỀU ĐỘ",         "",                            "positive",  AU_BAN_TUVAN,   1.0, "ban rau cu, tu van"),
 (  94.44, "*BA*: DÙNG DÒNG BỔ SUNG",        "",                            "product",   RICHNATTO,      0.5, ""),

 # --- KHOI 10: thieu mot chan la hong ---
 (  96.68, "NẾU CHỈ *THỂ DỤC THỂ THAO*",     "",                            "yellow",    TD_NHOM_DIBO,   1.0, "nhom di bo ven bien"),
 # 98.70 de TRONG: y la "an uong KHONG dieu do". Kho chua co clip an uong
 # thieu lanh manh da khai; dung clip rau xanh o day la nguoc y.
 (  98.70, "MÀ KHÔNG",                       "*ĂN UỐNG ĐIỀU ĐỘ*",           "warning",   "",             0,   ""),
 ( 102.10, "CƠ THỂ SẼ NGÀY CÀNG",            "*TEO TÓP LẠI*",               "warning",   MM_XELAN,       1.0, "ong cu xe lan, yeu di"),
 ( 105.13, "CÒN *THỂ DỤC* CÓ",               "*ĂN UỐNG* TỐT",               "yellow",    TD_ONGBA_CHAY,  1.0, "hai ong ba chay bo"),
 ( 108.41, "*CŨNG CHƯA ĐỦ*",                 "",                            "warning",   "",             0,   "0.8s — qua ngan de kip nhan hinh"),

 # --- KHOI 11: co che — cang lon tuoi cang kho hap thu ---
 ( 109.23, "TẠI VÌ *CÀNG LỚN TUỔI*",         "",                            "warning",   MM_CHEMAT1,     6.0, "ong cu met — moc khac lan truoc"),
 # gop 2 nhip lam 1: tach ra thi dong "CANG BI CHAM DI" chi con 0.8s.
 # "chuyen hoa" quay lai o #52 nen bo o day khong mat y.
 ( 110.97, "*KHẢ NĂNG HẤP THU*",             "*CÀNG BỊ CHẬM ĐI*",           "warning",   CT_TIEUHOA,     8.0, "he tieu hoa, moc khac"),
 ( 114.41, "THÌ *DÙNG DÒNG BỔ SUNG*",        "",                            "product",   RICHNATTO,      0.5, ""),
 ( 118.91, "*HẤP THU, CHUYỂN HÓA*",          "ĐƯỢC TỐT HƠN",                "positive",  CO_THE,         1.0, "co the hap thu"),

 # --- KHOI 12: tu do ho tro cai thien trieu chung ---
 # gop 2 nhip: tach ra thi dong dau chi 0.8s, va ca hai deu trung het chu
 # voi #3/#4 o phan hook.
 ( 123.76, "*ĐAU ĐẦU*, CHÓNG MẶT",           "*VAI GÁY*, TÊ BÌ CHÂN TAY",   "warning",   VAI_GAY,        0.5, ""),

 # --- KHOI 13: chot — khong ai cam ket duoc neu co chu khong dong hanh ---
 # 5 dong lien tiep de TRONG. Day la doan anh noi thang vao camera ve chinh
 # kien cua minh — de mat khan gia o lai tren mat anh, dung cat di dau ca.
 ( 126.45, "CÓ AI TÌM ĐẾN THỊNH",            "MÀ BẢO *CAM KẾT*",            "yellow",    "",             0,   ""),
 ( 128.95, "LÀ *KHỎI HẲN*",                  "HAY *DỨT ĐIỂM*",              "yellow",    "",             0,   ""),
 ( 132.15, "*KHÔNG BAO GIỜ* THỊNH",          "*CAM KẾT* ĐƯỢC ĐIỀU ĐÓ",      "highlight", "",             0,   ""),
 ( 135.33, "NẾU CÔ CHÚ",                     "*KHÔNG CAM KẾT*",             "warning",   "",             0,   ""),
 ( 138.57, "*ĐỒNG HÀNH NGHIÊM TÚC*",         "CHO SỨC KHỎE",                "positive",  TD_ONGCU_TA,    1.0, "ong cu tap co HLV kem — 'dong hanh'"),

 # --- KHOI 14: CTA ---
 ( 143.57, "*HỖ TRỢ CẢI THIỆN*",             "ĐAU ĐẦU, MẤT NGỦ",            "warning",   DD_ONGCU2,      1.0, "ong cu om tran, take khac"),
 ( 147.01, "*ĐAU MỎI VAI GÁY*",              "*TÊ BÌ CHÂN TAY*",            "warning",   DQ_TEBI,        1.0, "te bi run tay"),
 # CM_TIENDINH cung la ong cu om dau — dat ngay sau DD_ONGCU2 thi hai hinh
 # nhin gan giong het nhau. CM_TUATUONG (vin tuong, mat thang bang) vua khac
 # hinh vua dung y "tien dinh" hon.
 ( 148.96, "*RỐI LOẠN TIỀN ĐÌNH*",           "",                            "warning",   CM_TUATUONG,    1.0, "vin tuong, mat thang bang"),
 ( 150.28, "KỂ CẢ *SUY NHƯỢC THẦN KINH*",    "",                            "warning",   TK_XUNG,        1.0, "xung than kinh"),
 ( 152.14, "MUỐN CẢI THIỆN",                 "THÌ *LIÊN HỆ THỊNH*",         "cta",       RICHNATTO,      0.5, ""),
 # tra lai 05/08: bo ca 3 dong cuoi thi CTA con MOT caption dung 8 giay.
 # CTA la khoi anh Thanh bao phai giu — cat o day la cat qua tay.
 ( 154.30, "ĐỂ ĐƯỢC *HỖ TRỢ TỐT NHẤT*",      "",                            "cta",       RICHNATTO,      0.5, "chay tiep tu tren"),
 ( 159.68, "*NHIỀU NIỀM VUI*",               "*ẤM ÁP BÊN GIA ĐÌNH*",        "positive",  TD_ONGBA_VUI,   3.0, "chay tiep tu tren"),
]


if __name__ == "__main__":
    # Truyen fallback=<anh> neu muon may TU DOI clip qua ngan sang anh do.
    # Mac dinh la BO TRONG — may khong hieu nghia, doi lung tung la sai bai.
    build(HERE, R)
