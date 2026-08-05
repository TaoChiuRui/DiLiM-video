# -*- coding: utf-8 -*-
"""Hang so duong dan B-roll — dung chung cho moi job, khong khai bao lai.

Kiem lai bang `python3 clips.py` sau moi lan anh Thanh don kho.

QUY UOC TEN SAN PHAM (anh doi ten 04/08/2026):
    natto-*      Nano Nattokinase 60.000FU   <- san pham cua kich ban "mach mau"
    rich-*       Rich Coenzyme Q10           <- SAN PHAM KHAC, dung nham la sai bai
    richnatto-*  hai hop chung
"""
import os

IMG_EXT = (".jpg", ".jpeg", ".png", ".JPG", ".PNG")

# Kho B-roll. Mac dinh la o T7 cua anh Thanh; may khac / o mount ten khac thi
# dat bien moi truong DILIM_FOOTAGE, KHONG sua dong nay:
#     export DILIM_FOOTAGE="/Volumes/<ten o>/02. Dilim Footage"
B = os.environ.get("DILIM_FOOTAGE", "/Volumes/T7 for Mac/02. Dilim Footage")
MM = f"{B}/02 Mạch Máu - Thần Kinh - TẾ BÀO"
DD = f"{B}/01 Đau đầu - Chóng mặt - Mệt mõi - Bệnh"

# --- trieu chung ---
MAT_NGU    = f"{DD}/matngu-nu-ngoiday-01.mp4"           # 17.0s
DAU_DAU1   = f"{DD}/daudau-nu-tocvang-01.mp4"         # 19.0s
DAU_DAU3   = f"{DD}/daudau-bopmui-nu-01.mp4"         #  8.2s
CHONG_MAT  = f"{DD}/chongmat-vintuong-nam-01.mp4"
VAI_GAY    = f"{B}/Footage Dilim Quay/VAI GÁY (1).mp4"   # 9.7s
NGU_NGON   = f"{B}/06 Ngủ- Ngon- mất ngủ/ngungon-chiso-suckhoe-01.mp4"        # anh doi ten 04/08

# --- FOLDER 01 don ngay 04/08/2026 -----------------------------------------
# 44 file -> bo 5 (2 cap trung + 1 do phan giai thap + 1 hinh hoat hinh +
# 1 anh tinh thua), doi ten 39 file con lai theo quy uoc <chu de>-<mo ta>-<so>.
# TRUOC KHI DON: 6/40 clip duoc khai -> 34 clip nam chet vi suggest_clips.py
# chi tra ra clip co trong TAGS. Gio khai het.

# dau dau
DD_ONGCU1  = f"{DD}/daudau-ongcu-omtran-01.mp4"       # 19.7s ong cu A Dong om tran
DD_ONGCU2  = f"{DD}/daudau-ongcu-omtran-02.mp4"       # 18.0s cung dien vien, take khac
DD_ONGCU3  = f"{DD}/daudau-ongcu-ngoaitroi-01.mp4"    #  6.4s ong cu rau bac, ngoai troi
DD_BACU    = f"{DD}/daudau-bacu-omdau-01.mp4"         # 10.4s ba cu om dau, nhan nho
DD_NU_TN   = f"{DD}/daudau-nu-trungnien-01.mp4"       # 15.8s nu trung nien xoa thai duong
DD_VP1     = f"{DD}/daudau-vanphong-nu-01.mp4"        # 27.0s nu vest om dau ban giay
DD_VP2     = f"{DD}/daudau-vanphong-nu-02.mp4"        # 22.8s nu van phong xoa thai duong
DD_VP3     = f"{DD}/daudau-vanphong-nu-03.mp4"        # 20.0s nu tre van phong om dau
DD_SV      = f"{DD}/daudau-giangduong-sinhvien-01.mp4"  # 10.0s sinh vien giang duong
DD_GIUONG1 = f"{DD}/daudau-nam-giuong-01.mp4"         # 18.0s nam nam giuong om dau
DD_GIUONG2 = f"{DD}/daudau-nam-giuong-02.mp4"         # 14.0s — RUNG NHOE 2/3 khung
DD_GIUONG3 = f"{DD}/daudau-nam-giuong-03.mp4"         # 20.0s nam nam giuong nhan nho
DD_DEM     = f"{DD}/daudau-nam-giuong-dem-01.mp4"     # 18.0s ong trung nien ngoi giuong dem
DD_TACHNEN = f"{DD}/daudau-bacu-tachnen-01.png"       # anh PNG tach nen — dung overlay
DD_VUNGDO  = f"{DD}/daudau-vungdau-do-01.jpg"         # anh, vung dau phat sang do

# chong mat
CM_TUATUONG = f"{DD}/chongmat-nu-tuatuong-01.mp4"     # 18.3s nu tua tuong, tay len tran
CM_BEP      = f"{DD}/chongmat-bep-nu-01.mp4"          # 14.0s choang trong bep, vin tuong
CM_TIENDINH = f"{DD}/chongmat-tiendinh-ongcu-01.mp4"  # 18.6s ong cu om dau — tien dinh

# met moi
MM_4K       = f"{DD}/metmoi-bopmui-4k-01.mp4"         # 24.7s 3840x2160
MM_VP       = f"{DD}/metmoi-duimat-vanphong-01.mp4"   # 11.9s nam vest dui mat
MM_NGUGAT   = f"{DD}/metmoi-ngugat-cuaso-01.mp4"      # 12.5s ngu gat ben cua so
MM_BANPHIM  = f"{DD}/metmoi-guc-banphim-01.mp4"       #  8.2s guc dau xuong ban phim
MM_NGAP     = f"{DD}/metmoi-ngap-maytinh-01.mp4"      # 31.0s uong oai truoc may tinh
MM_CHEMAT1  = f"{DD}/metmoi-chemat-ongcu-01.mp4"      # 15.1s ong cu hai tay che mat
MM_CHEMAT2  = f"{DD}/metmoi-chemat-nam-01.mp4"        # 13.0s nam tre che mat
MM_CHEMAT3  = f"{DD}/metmoi-chemat-vanphong-01.mp4"   # 18.0s nam A Dong che mat o ban
MM_GUCBAN   = f"{DD}/metmoi-guc-ban-01.mp4"           # 14.0s guc xuong ban, tay om dau
MM_SOFA     = f"{DD}/metmoi-duimat-sofa-01.mp4"       # 16.0s nam trung nien dui mat
MM_LAPTOP   = f"{DD}/metmoi-bopmui-laptop-01.mp4"     #  5.1s bop song mui truoc laptop
MM_DEM      = f"{DD}/metmoi-bopmui-dem-01.mp4"        # 11.0s bop song mui, den tim ban dem
MM_XELAN    = f"{DD}/metmoi-ongcu-xelan-01.mp4"       #  8.8s ong cu xe lan, chong dau
MM_GUCTOI   = f"{DD}/metmoi-guc-toi-01.mp4"           # 44.0s — TONG TOI, lech style DiLiM

# khac
STRESS_VP  = f"{DD}/stress-vanphong-nam-01.mp4"       # 22.8s nga ghe, om dau — cang thang
KHO_THO    = f"{DD}/khotho-leothang-01.mp4"           # 13.7s leo cau thang, vin tay, tho doc
SOT_TRAN   = f"{DD}/sot-so-tran-01.mp4"               # 10.2s so tran nguoi nam — sot/cham soc

# --- mach mau / benh ly ---
MACH_MAU   = f"{MM}/machmau-catdoc-tim-01.mp4"          # 13.9s
HE_MACH    = f"{MM}/machmau-hetoanthan-01.mp4"       #  5.0s
MACH_HEP   = f"{MM}/machmau-hep-momau-01.mp4"      # 23.7s
XO_VUA     = f"{MM}/xovua-mangbam-vang-01.mp4"       # 29.8s  (anh chon 03/08)
MANG_MO2   = f"{MM}/xovua-mangmo-trang-01.mp4"         # 13.2s
CUC_MAU    = f"{MM}/cucmau-khoi-fibrin-01.mp4"      # 50.7s
MO_MAU     = f"{MM}/momau-hatvang-xoay-01.mp4"            #  8.9s
NAO        = f"{MM}/nao-xanh-phatsang-01.mp4"               # 25.0s
NAO21      = f"{MM}/nao-xanh-manh-vo-01.mp4"            # 15.0s
MAU_TIM    = f"{MM}/tim-mau-ve-tim-01.mp4"           # 10.0s
CO_THE     = f"{MM}/cothe-hemach-do-01.mp4"      # 15.0s
NEURON     = f"{MM}/thankinh-neuron-xanh-01.mp4"   # 16.7s
DOT_QUY    = f"{B}/04 Đột quỵ/dotquy-omnguc-sofa-01.mp4"   # 15.5s

# --- BO SUNG 04/08: 12 clip mach mau BI BO SOT o lan truoc.
# Ly do sot: catalog tra bang tu khoa TIENG VIET nen khong khop ten tieng Anh
# ("Arteriosclerosis", "Blood clot", "Clogged blood vessel"). Da them tu dong
# nghia Anh-Viet vao catalog.py de lan sau tra ra.
MAU_CHAY_1 = f"{MM}/mau-chay-longmach-01.mp4"      # 10.2s  máu chạy trong lòng mạch
MAU_CHAY_2 = f"{MM}/mau-chay-4k-01.mp4"           # 20.0s
TIM_DAP    = f"{MM}/tim-dap-nento-01.mp4"            # 20.0s
# TRAI_TIM da bo 04/08: `Trái Tim.mp4` TRUNG y het `tim-dap.mp4` (van tay lech
# 0.3/256, cung 20.0s). Truoc do CA HAI cung nam trong FAMILIES["tim"] — tuc la
# buoc chong lap xoay vong giua hai ban cua CUNG MOT clip, xoay xong van ra hinh
# y het. Dung TIM_DAP.
MANG_MO    = f"{MM}/xovua-sosanh-sach-mo-01.mp4"            #  5.0s  so sanh mach sach/mach mo
MANG_MO3   = f"{MM}/xovua-mangmo-4k-01.mp4"          # 15.0s
MO_MAU2    = f"{MM}/momau-hatvang-mach-01.mp4"           #  5.0s
XO_VUA3    = f"{MM}/xovua-mangbam-day-01.mp4"           # 12.0s
CUC_MAU2   = f"{MM}/cucmau-hinhthanh-doc-01.mp4"   # 16.7s — DỌC 1080x1920, KHONG dung cho dai B-roll
MO_HEP     = f"{MM}/momau-can-dongmau-dai-01.mp4"   # 57.7s
MACH_TAC   = f"{MM}/cucmau-tacmach-01.mp4"  # 24.0s
XO_VUA_MODEL = f"{MM}/xovua-mohinh-mach-01.mp4"  # 51.2s (giay 0-4 la chu, bat dau tu 6s)


# --- FOLDER 02 don ngay 04/08/2026 -----------------------------------------
# 109 file -> bo 36 (12 nhom TRUNG do bang van tay anh + clip quang cao hang
# khac + do phan giai thap + chu tieng Anh de suot + chu de khong lien quan
# mach mau), doi ten 73 file con lai. Truoc khi don: 23/109 duoc khai.
MM_HEP_THAT = f"{MM}/machmau-hep-that-01.mp4"        # 15.0s long mach that hep dan
MM_HEP_VANG = f"{MM}/machmau-hep-mangvang-01.mp4"    # 10.2s hong cau chui qua khe hep
MM_TINHMACH = f"{MM}/machmau-tinhmach-duoida-01.mp4" # 14.9s tinh mach noi duoi da
MM_LONGMACH = f"{MM}/machmau-longmach-nhindoc-01.mp4"  # 15.0s nhin doc long mach
MM_KINHLUP  = f"{MM}/machmau-kinhlup-soi-01.mp4"     # 14.0s kinh lup soi mach
MM_ONGDONG  = f"{MM}/machmau-anddu-ongdong-01.mp4"   # 12.0s an du: ong dong thong thoang

XV_VANG2    = f"{MM}/xovua-mangbam-vang-02.mp4"      # 12.0s — da dung 2x nhung chua khai
XV_CATMO    = f"{MM}/xovua-catmo-mangvang-01.mp4"    # 12.0s mach cat mo, mang vang trong
XV_DAI      = f"{MM}/xovua-quatrinh-dai-01.mp4"      # 117.5s — DAI, co watermark + chu Anh
XV_DOC      = f"{MM}/xovua-cholesterol-doc-01.mp4"   # 15.0s DOC 1080x1920
XV_HINHTHANH = f"{MM}/xovua-hinhthanh-01.mp4"        # 13.4s — 768x432, DO PHAN GIAI
# THAP (phong len dai 1080 rong la ~1.4x, hinh se mem). Anh Thanh xem va giu lai
# 04/08 vi noi dung dung: ca qua trinh HINH THANH mang xo vua tu dau den cuoi.
# Dung khi caption noi ve qua trinh, dung khi can hinh net.

MO_4K       = f"{MM}/momau-4k-longmach-01.mp4"       #  8.3s 3840x2160
MO_CATDOC   = f"{MM}/momau-catdoc-vang-01.mp4"       #  8.4s mach cat doc, mo vang
MO_DAY      = f"{MM}/momau-day-hongcau-01.mp4"       # 12.0s mo day hai ben thanh mach
MO_TINHTHE  = f"{MM}/momau-tinhthe-vang-01.mp4"      #  8.0s tinh the vang lan hong cau

CM_TRONGMACH = f"{MM}/cucmau-khoi-trongmach-01.mp4"  # 20.0s CUC MAU DONG thu hai —
# truoc day FAMILIES["cuc_mau"] chi co DUNG MOT clip nen 4b_vary khong xoay duoc gi.

MAU_HC_XANH = f"{MM}/mau-hongcau-machxanh-01.mp4"    #  5.0s hong cau trong mach xanh
MAU_HC_BC   = f"{MM}/mau-hongcau-bachcau-01.mp4"     # 10.0s hong cau + bach cau
MAU_BACHCAU = f"{MM}/mau-bachcau-trang-01.mp4"       # 10.0s bach cau trang noi bat
MAU_HC_TOI  = f"{MM}/mau-hongcau-nentoi-01.mp4"      #  7.2s hong cau nen toi
MAU_HC_TROI = f"{MM}/mau-hongcau-troi-01.mp4"        # 20.0s hong cau troi cham

TIM_XOAY    = f"{MM}/tim-do-xoay-01.mp4"             # 20.4s tim do xoay nen trang
TIM_DMC     = f"{MM}/tim-dongmachchu-01.mp4"         # 16.9s tim + dong mach chu
TIM_TOI     = f"{MM}/tim-giaiphau-nentoi-01.mp4"     # 16.7s tim giai phau nen toi
TIM_VONG    = f"{MM}/tim-vongxanh-xoay-01.mp4"       #  8.0s tim + vong sang xoay
TIM_NHOIMAU = f"{MM}/tim-nhoimau-cotim-01.mp4"       # 33.8s 4K nhoi mau co tim
TIM_DIEN_D  = f"{MM}/tim-mohinh-nhipdien-doc-01.mp4" # 21.1s DOC 720x1280
TIM_MAUDAC_D = f"{MM}/tim-maudac-mat-nuoc-doc-01.mp4"  # 12.1s DOC — mat nuoc lam mau dac

NAO_NAU     = f"{MM}/nao-giaiphau-nau-01.mp4"        #  8.3s nao giai phau mau nau
NAO_HONG    = f"{MM}/nao-hong-xoay-01.mp4"           # 16.0s nao hong xoay nen tim
NAO_DAI     = f"{MM}/nao-tinhieu-dai-trang-01.mp4"   # 12.0s dai sang chay qua nao
NAO_CAM     = f"{MM}/nao-cam-ruc-01.mp4"             # 10.0s nao cam ruc, mang luoi
NAO_TIM_TR  = f"{MM}/nao-tim-nentrang-01.mp4"        # 15.0s nao tim nen trang
NAO_TIM_DEN = f"{MM}/nao-tim-nenden-01.mp4"          # 15.0s nao tim nen den
NAO_SET     = f"{MM}/nao-tiaset-01.mp4"              #  8.0s nao + tia set dien
NAO_EEG     = f"{MM}/nao-quet-eeg-01.mp4"            # 11.2s quet dien nao, nhan P3/T5/Cz

TK_TIM      = f"{MM}/thankinh-neuron-tim-01.mp4"     #  6.3s mang neuron tim/xanh
TK_DIENNAO  = f"{MM}/thankinh-diennao-dantruyen-01.mp4"  # 20.0s — anh Thanh chot:
# "dien nao, dan truyen, neuron than kinh"
TK_SYNAPSE  = f"{MM}/thankinh-synapse-dantruyen-01.mp4"  # 13.0s synapse + chat dan truyen
TK_XUNG     = f"{MM}/thankinh-xung-bungsang-01.mp4"  # 30.0s xung than kinh bung sang
TK_TOANTHAN = f"{MM}/thankinh-toanthan-vang-01.mp4"  #  5.0s he than kinh toan than

CT_NGUC     = f"{MM}/cothe-hemach-longnguc-01.mp4"   # 24.0s co the trong suot + he mach
CT_TIEUHOA  = f"{MM}/cothe-tieuhoa-01.mp4"           # 14.0s co the + duong tieu hoa

COQ10_XANH  = f"{MM}/coq10-cau-xanh-01.mp4"          # 14.0s — SAN PHAM Rich CoQ10,
COQ10_VANG  = f"{MM}/coq10-cau-vang-01.mp4"          # 14.0s   KHONG phai natto
PHANTU_XANH = f"{MM}/phantu-cautruc-xanh-01.mp4"     #  5.0s cau truc phan tu xanh
PHANTU_DEN  = f"{MM}/phantu-mohinh-denrang-01.mp4"   #  5.0s mo hinh phan tu den/trang
DNA         = f"{MM}/dna-chuoi-xoan-01.mp4"          #  8.0s chuoi xoan kep
TEBAO       = f"{MM}/tebao-cautruc-nhan-01.mp4"      # 13.4s te bao cat ngang, nhan + ty the
DA_LOPCAT   = f"{MM}/da-lopcat-momo-01.mp4"          #  5.0s da cat lop, mo duoi da
DA_BEMAT    = f"{MM}/da-bemat-tebao-01.mp4"          #  7.0s be mat te bao da

# ANH TINH (giu 3/10, bo 7: 2 anh AI sinh kieu cong nghe, 1 so do co chu,
# 1 clipart 2 bo nao, 1 anh 650x433, 1 u nao, 1 te bao khong lien quan).
# Anh dung duoc vi dai B-roll dung yen — nhung phai soi ky khung: anh ti le la
# se bi cat tren duoi (luat 3 cua anh Thanh).
XV_ANH_HEP  = f"{MM}/xovua-anh-manghep-01.jpg"       # mang vang lam hep long mach
XV_ANH_TAC  = f"{MM}/xovua-anh-tacmach-01.jpg"       # nhin doc long mach bi tac
CM_ANH_KHOI = f"{MM}/cucmau-anh-khoi-01.jpg"         # khoi hong cau ket cuc


# --- FOLDER 06 / 07 don ngay 04/08/2026 ------------------------------------
NG = f"{B}/06 Ngủ- Ngon- mất ngủ"
VM = f"{B}/07 Video minh họa"

NG_DENDEM   = f"{NG}/ngungon-nu-dendem-01.mp4"       # 16.0s nu ngu, den ngu am
NG_NHINTREN = f"{NG}/ngungon-nu-nhintren-01.mp4"     # 23.0s nhin tu tren xuong
NG_CANMAT   = f"{NG}/ngungon-nam-canmat-01.mp4"      # 15.0s nam trung nien, can mat
NG_VV_CUASO = f"{NG}/ngungon-vuonvai-cuaso-01.mp4"   #  8.9s vuon vai ben cua so sang
NG_VV_GIUONG = f"{NG}/ngungon-vuonvai-giuong-01.mp4" #  9.9s vuon vai tren giuong
NG_NAM_TREN = f"{NG}/ngungon-nam-nhintren-01.mp4"    # 13.0s nam ngu, anh xanh
NG_NU_AM    = f"{NG}/ngungon-nu-anham-01.mp4"        # 18.0s nu ngu, anh am
NG_DONGHO_D = f"{NG}/ngungon-dongho-doc-01.mp4"      # 14.0s DOC 1080x1920

MN_TRANROC  = f"{NG}/matngu-nu-tranroc-01.mp4"       # 26.0s nam mo mat, tran roc
MN_TROMINH  = f"{NG}/matngu-nu-tro-minh-01.mp4"      # 24.7s tro minh, tinh giac
MN_NGOIDAY_D = f"{NG}/matngu-ngoiday-doc-01.mp4"     # 11.6s DOC — ngoi day giua dem
MN_ONGCU    = f"{NG}/matngu-ongcu-dem-01.mp4"        # 20.2s ong cu ngoi tram ngam dem

# an du — khong phai giai phau, dung khi caption noi bong
ANDU_ONGNUOC = f"{VM}/andu-ongnuoc-chay-01.mp4"      #  7.8s ong nuoc chay thong
ANDU_XERAC   = f"{VM}/andu-xerac-do-01.mp4"          # 45.0s xe rac do rac
ANDU_XERAC2  = f"{VM}/andu-xerac-nhintren-01.mp4"    # 26.6s nhin tu tren xuong


# --- san pham (chi dung natto-* cho kich ban mach mau) ---
NATTO1     = f"{B}/03 Rich_Natto_product/natto-01.mp4"      # 4.9s
NATTO2     = f"{B}/03 Rich_Natto_product/natto-02.mp4"      # 4.0s
RICHNATTO  = f"{B}/03 Rich_Natto_product/richnatto-01.mp4"  # 8.1s
NATTO_2HOP = f"{B}/Natto Xám/natto-2hop.jpg"                # anh, 2 hop tren tho go
MEN_GAO    = f"{B}/Natto Xám/men gạo đỏ.mp4"                # 28.9s
# rich-* la Rich Coenzyme Q10 — SAN PHAM KHAC, dung nham la sai bai.
RICH1      = f"{B}/03 Rich_Natto_product/rich-01.mp4"       # 3.6s hop RICH hong
RICH2      = f"{B}/03 Rich_Natto_product/rich-02.mp4"       # 2.0s — NGAN, chi 2s
RICH3      = f"{B}/03 Rich_Natto_product/rich-03.mp4"       # 3.1s
TAO_DO     = f"{B}/03 Rich_Natto_product/taodo-thanhphan-01.mp4"  # 13.2s tao do duoi nuoc

# ANH SAN PHAM 6240x4160 (may Fuji) — 2 hop Rich + Nano Nattokinase.
# Anh ti le 3:2, dai B-roll la 1080x672 (~16:10) -> BI CAT TREN DUOI.
# Luat 3 anh Thanh: anh san pham phai soi ky, hop phai lot TRON trong dai.
RN_ANH_XANH = f"{B}/03 Rich_Natto_product/richnatto-anh-nenxanh-01.jpg"  # nen vai xanh
RN_ANH_CO   = f"{B}/03 Rich_Natto_product/richnatto-anh-treco-01.jpg"    # tren co
# (con 2 ban nenxanh-02/03 va 9 ban treco-02..10 — chua khai, xem so_kho.html)

# --- FOLDER 04 Dot quy: anh minh hoa ---
DQ = f"{B}/04 Đột quỵ"
DQ_NGA1     = f"{DQ}/dotquy-anh-nga-bacu-01.jpg"     # ba cu nga trong nha, kinh roi
DQ_NGA2     = f"{DQ}/dotquy-anh-nga-bacu-02.png"     # cung buoi chup, goc rong hon
DQ_NGA_DUONG = f"{DQ}/dotquy-anh-nga-duong-01.png"   # nga tren duong, nguoi do
DQ_MEO      = f"{DQ}/dotquy-anh-meo-mieng-01.png"    # meo mieng — dau hieu dot quy
DQ_PHUCHOI  = f"{DQ}/dotquy-anh-phuchoi-tay-01.png"  # tap van dong tay sau dot quy
DQ_TAPDI    = f"{DQ}/dotquy-anh-tapdi-khung-01.png"  # tap di voi khung

# --- FOLDER 04 Dot quy: clip ---
DQ_NGA_GUC  = f"{DQ}/dotquy-nga-guc-01.mp4"          # 17.7s nga guc, con do day
DQ_OMNGUC1  = f"{DQ}/dotquy-omnguc-ongcu-01.mp4"     # 17.8s ong cu om nguc kho tho
DQ_OMNGUC2  = f"{DQ}/dotquy-omnguc-canh-01.mp4"      # 16.0s can canh tay len nguc
DQ_TEBI     = f"{DQ}/dotquy-tebi-runtay-01.mp4"      # 34.8s xoa ban tay te, run
DQ_XELAN    = f"{DQ}/dotquy-xelan-dichung-01.mp4"    # 33.6s ba cu xe lan — di chung
DQ_CAPCUU   = f"{DQ}/dotquy-capcuu-bangca-01.mp4"    # 11.4s e-kip day bang ca
DQ_NAMVIEN  = f"{DQ}/dotquy-namvien-truyendich-01.mp4"  # 14.0s nam vien truyen dich

# --- ket bai ---
DISCLAIMER = f"{B}/05 Finish part/SP này k phải là thuốc.mp4"   # DOC 1080x1920 — la clip TOAN KHUNG cuoi bai, khong phai B-roll dai
LOGO       = f"{B}/05 Finish part/dilim logo .png"


# Clip co the/chu o dau -> phai bat dau sau moc nay.
# Do bang `python3 do_doan.py --dai` (04/08/2026), so chot da nhin frame that.
MIN_START = {
    XO_VUA_MODEL: 9.0,   # SUA 04/08 (job natto-hoat-huyet): so cu 6.0 SAI —
                         # nhin frame that o giay 6 van con nguyen cau
                         # "Buildup of plaque in the arteries..." Chu chay
                         # toi ~8s. Xem them VUNG_CAM: cuoi clip cung co chu.
    MACH_TAC:     4.0,   # giay 0-3 gan nhu den + logo Helix. 4b_vary.py doi
                         # clip sang day roi lay MIN_START lam src_start, khong
                         # co so nay thi ra 3 giay hinh den giua bai.
    MM_NGAP:      4.0,   # chu 0-4.0s
    CUC_MAU:      0.0,   # xem VUNG_CAM ben duoi — clip nay phuc tap
}

# --- VUNG CAM: doan KHONG duoc dung, du clip du dai ------------------------
# MIN_START chi noi duoc "bat dau tu dau", khong noi duoc "giua clip co ho".
# Bang nay la de NGUOI DOC biet khi viet plan.py; chua script nao doc no.
# (Neu sau nay lam bang DOAN thi thay ca hai bang mot.)
#
# LOI THAT 04/08/2026: `cuc-mau-dong.mp4` la clip dung nhieu nhat kho (12 lan).
# Cac job da dat src_start = 20.0s (4 job) va 35.0s (2 job) — ca hai deu roi vao
# vung chu tieng Anh. Tuc 6 dong caption trong 5 ban dung dang hien PLATELET /
# RED BLOOD CELL / FIBRIN tren dai B-roll. CHUA SUA.
VUNG_CAM = {
    CUC_MAU: [(14.0, 20.5),    # PLATELET
              (22.0, 28.5),    # RED BLOOD CELL
              (31.0, 38.5),    # FIBRIN
              (45.5, 50.7)],   # fade den + logo Helix
    # dung duoc: 0-14.0s (dai nhat, sach) va 38.5-45.5s

    # them 04/08 (job natto-hoat-huyet), da nhin frame 0/6/10/14/20/25/30/40/45/50:
    XO_VUA_MODEL: [(0.0, 9.0),      # fade den + "Buildup of plaque... (PAD)"
                   (38.0, 51.2)],   # "To Learn More Visit LoveYourLimbs.com"
                                    # + den + doan disclaimer tieng Anh
    # dung duoc: 9.0-38.0s (29s, mo hinh mach sach chu)

    MO_HEP:  [(7.5, 12.0), (15.0, 22.0), (24.0, 29.0),
              (31.0, 38.0), (53.0, 56.0)],
    # dung duoc: 0-7.5s va 38.0-53.0s (15s, dai nhat)

    XV_DAI:  [(1.0, 5.0), (22.5, 29.5), (41.5, 46.5), (52.0, 54.5),
              (58.5, 60.0), (64.0, 67.5), (85.0, 90.0), (93.0, 97.0),
              (100.5, 105.5)],
    # dung duoc: 5-22.5s · 29.5-41.5s · 67.5-85s (3 khoang dai nhat).
    # 2 job dang dung src_start=40.0s -> 40-43.2s, DINH vung cam 41.5-46.5s.

    # XO_VUA_MODEL va MM_NGAP: do_doan.py KHONG KET LUAN DUOC (clip nen sang).
    # XO_VUA_MODEL da co MIN_START=6.0 anh Thanh chot tu truoc, cu theo do.
}

# --- FOLDER "The duc the thao" + "An uong lanh manh" — khai ngay 05/08/2026 ---
# Job 07-dji0485 (bai "Thinh khong cam ket") noi "the duc the thao" 6 lan,
# "an uong dieu do / thanh dam" 4 lan, "thien dinh" 3 lan. Ca ba nhom nam trong
# hai folder nay va CHUA CO clip nao duoc khai -> suggest_clips tra ra toan clip
# mach mau lech y. Da soi frame 3 moc (5%/40%/75%) tren 209 clip NGANG.
# Uu tien clip CO NGUOI LON TUOI — dung chan dung khach hang DiLiM.
TDTT = f"{B}/Thể dục thể thao"
AULM = f"{B}/Ăn uống lành mạnh"

TD_ONGBA_PHO  = f"{TDTT}/theduc-ongba-dibo-pho-01.mp4"              # 31.4s ong ba A Dong di bo the duc via he
TD_ONGCU_VUON = f"{TDTT}/theduc-ongcu-vuontay-01.mp4"                     # 19.0s ong cu vuon tay khoi dong, cong vien
TD_ONGCU_XANH = f"{TDTT}/theduc-ongcu-chay-canh-01.mp4" # 29.9s ong cu rau bac ao xanh chay bo, can canh
TD_ONGBA_CHAY = f"{TDTT}/theduc-ongba-chaybo-01.mp4" # 13.6s hai ong ba chay bo song doi
TD_SU_KHATTHUC= f"{TDTT}/theduc-su-khatthuc-01.mp4" #  6.0s su chan tran di khat thuc — minh hoa "tinh tan"
TD_ONGBA_VUI  = f"{TDTT}/theduc-ongba-dibo-vui-01.mp4" # 20.0s hai ong ba di bo, cuoi tuoi
TD_KHICONG_O  = f"{TDTT}/theduc-ongcu-khicong-01.mp4" # 13.4s ong cu ao trang tap khi cong / thai cuc quyen
TD_KHICONG_B  = f"{TDTT}/theduc-bacu-khicong-01.mp4" # 26.7s ba cu ao trang tap tho, bai co
TD_ONGCU_CO   = f"{TDTT}/theduc-ongcu-chay-baico-01.mp4"                                      # 11.6s ong cu chay bo tren bai co
TD_NHOM_DIBO  = f"{TDTT}/theduc-nhom-dibo-venbien-01.mp4"                                 # 14.8s ba nguoi trung/cao nien di bo duong ven bien
TD_BACU_BIEN  = f"{TDTT}/theduc-bacu-dibo-bobien-01.mp4"                                 # 12.0s ba cu ao xanh di bo bo bien
TD_ONGCU_TA   = f"{TDTT}/theduc-ongcu-tata-hlv-01.mp4"              # 19.1s ong cu tap ta tay, CO HLV KEM — minh hoa "dong hanh"
# TD_DAYKHANG (download (20).mp4) DA LOAI: giay 25 doi sang phu nu tre trong
# phong gym, khong con la ba cu. Neu dung thi src_start phai < 18s.

AU_RAU_CHO    = f"{AULM}/RỨNG (67).mp4"                                    # 25.0s quay rau xanh bay ban o cho
AU_RUONG_CAI  = f"{AULM}/RỨNG (69).mp4"                                    # 12.0s ruong cai xanh, mua roi
AU_RAUCU_XANH = f"{AULM}/5857694-uhd_3840_2160_25fps (1).mp4"              # 16.7s rau cu qua bay tren nen xanh, flatlay
AU_BAN_TUVAN  = f"{AULM}/OĂDAWD.mp4"                                       # 21.2s ban rau cu + nuoc cam + thuoc do — tu van dinh duong
AU_AN_SALAD   = f"{AULM}/Thiết kế chưa có tên - 2024-12-28T154710.251.mp4" #  9.5s nguoi ngoi an salad
AU_ONGCU_NUOC = f"{AULM}/Thiết kế chưa có tên - 2026-05-07T160729.244.mp4" # 10.6s ong cu A Dong uong nuoc, ngoi ghe
AU_MAM_LANH   = f"{AULM}/download (89).mp4"                                #  7.6s mam do an lanh manh: salad, trai cay, hat

# --- HO CLIP: dung cho buoc chong lap (4b_vary.py) ---
# Khi mot y bi noi lai nhieu lan trong bai, xoay vong trong ho thay vi lap
# lai dung mot clip. Thu tu trong list = thu tu uu tien.
FAMILIES = {
    "luu_thong":  [MACH_MAU, MAU_CHAY_1, MAU_CHAY_2, HE_MACH, MAU_TIM,
                   MM_LONGMACH, MAU_HC_XANH, MAU_HC_BC, MAU_HC_TROI, MAU_HC_TOI],
    "mach_hep":   [MACH_HEP, MACH_TAC, MO_HEP, XO_VUA_MODEL,
                   MM_HEP_THAT, MM_HEP_VANG],
    "xo_vua":     [XO_VUA, MANG_MO2, XO_VUA3, MANG_MO3, MANG_MO,
                   XV_VANG2, XV_CATMO, XV_DAI, XV_HINHTHANH],
    # CUC_MAU2 va XV_DOC bi loai khoi ho: clip DOC, dai B-roll can clip NGANG.
    # 04/08: them CM_TRONGMACH — truoc do ho nay chi co DUNG MOT clip nen
    # 4b_vary.py khong co gi de xoay, y "cuc mau dong" bi lap hinh ca bai.
    "cuc_mau":    [CUC_MAU, CM_TRONGMACH, MACH_TAC],
    "mo_mau":     [MO_MAU, MO_MAU2, MO_HEP, MO_4K, MO_CATDOC, MO_DAY, MO_TINHTHE],
    "tim":        [MAU_TIM, TIM_DAP, TIM_XOAY, TIM_TOI, TIM_DMC, TIM_VONG],
    "nao":        [NAO, NAO21, NAO_TIM_DEN, NAO_TIM_TR, NAO_CAM, NAO_HONG,
                   NAO_DAI, NAO_NAU],
    "than_kinh":  [NEURON, TK_TIM, TK_DIENNAO, TK_SYNAPSE, TK_XUNG, NAO_SET],
    "trieu_chung":[MAT_NGU, DAU_DAU1, DAU_DAU3, VAI_GAY, CHONG_MAT],
    "san_pham":   [NATTO1, NATTO2, RICHNATTO, NATTO_2HOP],
    "san_pham_rich": [RICH1, RICH3, RICH2],   # Rich CoQ10 — KHAC natto
    "ngu_ngon":   [NGU_NGON, NG_DENDEM, NG_CANMAT, NG_NU_AM, NG_NAM_TREN,
                   NG_NHINTREN],
    "mat_ngu":    [MAT_NGU, MN_TRANROC, MN_ONGCU, MN_TROMINH],
    "tinh_day":   [NG_VV_GIUONG, NG_VV_CUASO],
    "dot_quy":    [DOT_QUY, DQ_NGA_GUC, DQ_OMNGUC1, DQ_OMNGUC2, DQ_NGA_DUONG],
    "di_chung":   [DQ_XELAN, DQ_TAPDI, DQ_PHUCHOI, DQ_NAMVIEN, DQ_CAPCUU],

    # --- them 04/08: folder 01 da don, gio du clip de XOAY VONG ---
    # Truoc day "dau dau" chi co 2 clip nen bai nao nhac dau dau nhieu lan la
    # lap hinh. Thu tu = uu tien: ong/ba cu truoc (dung chan dung khach hang),
    # roi den trung nien, van phong sau cung.
    "dau_dau":    [DAU_DAU1, DD_ONGCU1, DD_BACU, DD_NU_TN, DD_ONGCU2,
                   DAU_DAU3, DD_VP1, DD_VP3, DD_ONGCU3, DD_VP2, DD_SV],
    "dau_dau_dem":[DD_DEM, DD_GIUONG1, DD_GIUONG3, DD_GIUONG2],
    "chong_mat":  [CHONG_MAT, CM_TIENDINH, CM_TUATUONG, CM_BEP],
    "met_moi":    [MM_CHEMAT1, MM_SOFA, MM_4K, MM_CHEMAT3, MM_VP,
                   MM_LAPTOP, MM_DEM, MM_CHEMAT2, MM_XELAN],
    "kiet_suc":   [MM_GUCBAN, MM_BANPHIM, MM_NGUGAT, MM_NGAP, MM_GUCTOI],
    "cang_thang": [STRESS_VP, DD_VP1, MM_GUCBAN],

    # --- them 05/08: y "the duc / an uong / thien" bi noi lai nhieu lan ---
    "the_duc":    [TD_ONGBA_PHO, TD_ONGCU_CO, TD_ONGBA_VUI, TD_ONGBA_CHAY,
                   TD_ONGCU_XANH, TD_NHOM_DIBO, TD_ONGCU_VUON, TD_BACU_BIEN],
    "thien":      [TD_KHICONG_O, TD_KHICONG_B, TD_SU_KHATTHUC],
    "an_lanh":    [AU_RAU_CHO, AU_MAM_LANH, AU_RAUCU_XANH, AU_RUONG_CAI,
                   AU_BAN_TUVAN, AU_AN_SALAD],
}

# --- CLIP DOC 1080x1920: KHONG dung cho dai B-roll (dai can clip NGANG) ---
VERTICAL = {CUC_MAU2, DISCLAIMER,
            XV_DOC,          # 1080x1920
            TIM_DIEN_D,      #  720x1280
            TIM_MAUDAC_D,    # 1080x1920
            NG_DONGHO_D,     # 1080x1920
            MN_NGOIDAY_D}    # 1080x1920

# --- CLIP CO WATERMARK HANG KHAC ---
# ANH THANH CHOT 04/08/2026: watermark HelixAnimation tren `cuc-mau-dong.mp4`
# KHONG SAO, cu dung. Nen de TRONG — dung khai lai clip do.
# Chi them vao day neu gap watermark that su khong dung duoc.
WATERMARK = {}

# --- TU KHOA -> CLIP: dung cho suggest_clips.py ---
# Viet bang tieng Viet co dau; suggest_clips.py tu bo dau khi so khop.
# Cum DAI hon duoc cham diem cao hon (khop "mach mau hep" > khop "mach mau").
# Them tu khoa vao day mỗi lần phải tự tay đi tìm một clip — lần sau máy tra ra.
TAGS = {
    MAT_NGU:   ["mất ngủ", "khó ngủ", "trằn trọc", "thao thức", "ngủ không sâu"],
    DAU_DAU1:  ["đau đầu", "nhức đầu", "đau nửa đầu"],
    DAU_DAU3:  ["đau đầu", "rối loạn tiền đình", "tiền đình", "choáng"],
    CHONG_MAT: ["chóng mặt", "hoa mắt", "choáng váng", "mệt mỏi"],
    VAI_GAY:   ["cổ vai gáy", "vai gáy", "đau mỏi vai", "tê bì tay chân", "tê bì", "mỏi cổ"],
    NGU_NGON:  ["ngủ ngon", "ngủ sâu", "ngủ được", "giấc ngủ"],

    # --- folder 01 khai ngay 04/08/2026 ---
    DD_ONGCU1:  ["đau đầu", "người già đau đầu", "ông bà đau đầu", "tuổi già"],
    DD_ONGCU2:  ["đau đầu", "nhức đầu", "người lớn tuổi", "cao tuổi"],
    DD_ONGCU3:  ["đau đầu", "ông cụ", "người già"],
    DD_BACU:    ["đau đầu", "nhức đầu", "bà cụ", "phụ nữ lớn tuổi", "đau nhức"],
    DD_NU_TN:   ["đau đầu", "xoa thái dương", "phụ nữ trung niên", "nhức đầu"],
    DD_VP1:     ["đau đầu", "căng thẳng công việc", "áp lực công việc", "dân văn phòng"],
    DD_VP2:     ["đau đầu", "xoa thái dương", "dân văn phòng", "căng thẳng"],
    DD_VP3:     ["đau đầu", "nhân viên văn phòng", "làm việc máy tính"],
    DD_SV:      ["đau đầu", "học hành căng thẳng", "áp lực học tập"],
    DD_GIUONG1: ["đau đầu", "đau đầu ban đêm", "nằm không yên", "trằn trọc"],
    DD_GIUONG2: ["đau đầu", "nằm ôm đầu"],
    DD_GIUONG3: ["đau đầu", "đau đầu ban đêm", "khó chịu khi nằm"],
    DD_DEM:     ["đau đầu", "tỉnh giấc giữa đêm", "đau đầu ban đêm", "ngồi dậy giữa đêm"],
    DD_TACHNEN: ["đau đầu", "ôm đầu", "tách nền"],
    DD_VUNGDO:  ["đau đầu", "vùng đau", "cơn đau bùng lên", "đau nhói"],

    CM_TUATUONG: ["chóng mặt", "choáng váng", "đứng lên là choáng", "mất thăng bằng"],
    CM_BEP:      ["chóng mặt", "hoa mắt", "loạng choạng", "mất thăng bằng"],
    CM_TIENDINH: ["rối loạn tiền đình", "tiền đình", "chóng mặt", "quay cuồng"],

    MM_4K:      ["mệt mỏi", "kiệt sức", "mỏi mắt", "bóp sống mũi"],
    MM_VP:      ["mệt mỏi", "mỏi mắt", "dụi mắt", "làm việc quá sức"],
    MM_NGUGAT:  ["ngủ gật", "buồn ngủ ban ngày", "uể oải", "thiếu ngủ"],
    MM_BANPHIM: ["kiệt sức", "gục xuống bàn", "quá tải", "mệt rã rời"],
    MM_NGAP:    ["uể oải", "buồn ngủ ban ngày", "ngáp", "thiếu năng lượng"],
    MM_CHEMAT1: ["mệt mỏi", "kiệt sức", "người già mệt", "suy nhược"],
    MM_CHEMAT2: ["mệt mỏi", "che mặt", "bế tắc"],
    MM_CHEMAT3: ["mệt mỏi", "kiệt sức", "làm việc quá sức", "cạn năng lượng"],
    MM_GUCBAN:  ["kiệt sức", "gục xuống bàn", "mệt rã rời", "quá tải"],
    MM_SOFA:    ["mệt mỏi", "mỏi mắt", "dụi mắt", "về nhà mệt"],
    MM_LAPTOP:  ["mỏi mắt", "bóp sống mũi", "mệt mỏi", "nhìn màn hình lâu"],
    MM_DEM:     ["mệt mỏi", "thức khuya", "làm việc ban đêm", "mỏi mắt"],
    MM_XELAN:   ["mệt mỏi", "suy nhược", "xe lăn", "sức khỏe giảm sút"],
    MM_GUCTOI:  ["kiệt sức", "suy sụp", "mệt mỏi kéo dài"],

    STRESS_VP:  ["căng thẳng", "stress", "áp lực công việc", "quá tải"],
    KHO_THO:    ["khó thở", "leo cầu thang", "hụt hơi", "mệt khi vận động", "thở dốc", "leo vài bậc thang", "lên cầu thang là mệt"],
    SOT_TRAN:   ["sốt", "sờ trán", "chăm sóc người ốm", "người thân lo lắng"],

    MACH_MAU:  ["mạch máu", "lòng mạch", "thành mạch", "lưu thông máu"],
    HE_MACH:   ["hệ mạch máu", "thông thoáng mạch máu", "mạch máu thông thoáng", "toàn hệ mạch"],
    MACH_HEP:  ["mạch máu hẹp", "hẹp lại", "lưu thông kém", "máu khó đi", "tắc mạch", "thiếu oxy"],
    XO_VUA:    ["mảng xơ vữa", "xơ vữa", "mảng bám", "bám thành mạch", "dày lên"],
    XO_VUA3:   ["xơ vữa", "mảng bám động mạch"],
    XO_VUA_MODEL: ["xơ vữa", "mô hình mạch máu", "mảng xơ vữa dày"],
    MANG_MO:   ["mảng mỡ", "so sánh mạch sạch", "mạch sạch"],
    MANG_MO2:  ["mảng mỡ", "mỡ bám thành mạch"],
    MANG_MO3:  ["mảng mỡ", "mỡ xấu bám"],
    MO_MAU:    ["mỡ máu", "mỡ xấu", "cholesterol", "mỡ trong máu"],
    MO_MAU2:   ["mỡ máu", "mỡ xấu"],
    MO_HEP:    ["mỡ làm hẹp", "cholesterol", "cản trở dòng máu", "mỡ bám"],
    MACH_TAC:   ["tắc mạch", "mạch máu tắc", "nghẽn mạch", "tắc nghẽn", "bị tắc"],
    CUC_MAU:   ["cục máu đông", "máu đông", "huyết khối", "làm tan cục máu"],
    MAU_CHAY_1:["máu di chuyển", "máu chạy", "dòng máu", "máu lưu thông"],
    MAU_CHAY_2:["máu chạy", "dòng máu", "lưu thông"],
    TIM_DAP:   ["tim đập", "nhịp tim", "trái tim", "tim mạch"],
    MAU_TIM:   ["máu về tim", "tim mạch", "phòng ngừa đột quỵ", "tuần hoàn"],
    NAO:       ["tế bào não", "não", "nuôi dưỡng não", "lên não"],
    NAO21:     ["não cần oxy", "oxy lên não", "não", "dưỡng chất"],
    NEURON:    ["hệ thần kinh", "thần kinh", "tế bào thần kinh", "neuron"],
    CO_THE:    ["cơ thể", "toàn cơ thể", "cơ thể người"],
    DOT_QUY:   ["đột quỵ", "tai biến", "phòng ngừa đột quỵ", "nguy hiểm"],

    # --- folder 02 khai ngay 04/08/2026 ---
    MM_HEP_THAT: ["mạch máu hẹp", "hẹp lại", "thắt lại", "lòng mạch thu hẹp"],
    MM_HEP_VANG: ["mạch máu hẹp", "máu khó đi", "chui qua khe hẹp", "lưu thông kém"],
    MM_TINHMACH: ["tĩnh mạch", "mạch máu dưới da", "nổi gân xanh"],
    MM_LONGMACH: ["lòng mạch", "trong lòng mạch", "dòng máu chảy"],
    MM_KINHLUP:  ["soi kỹ mạch máu", "nhìn vào lòng mạch", "quan sát mạch máu"],
    MM_ONGDONG:  ["đường ống", "ống dẫn", "thông thoáng", "ví như đường ống"],

    XV_VANG2:   ["mảng xơ vữa", "xơ vữa", "mảng bám", "bám thành mạch"],
    XV_CATMO:   ["mảng xơ vữa", "cắt mạch ra xem", "mảng bám bên trong"],
    XV_DAI:     ["xơ vữa", "quá trình xơ vữa", "mảng bám hình thành"],
    XV_DOC:     ["cholesterol tăng", "xơ vữa", "mỡ xấu tăng"],
    XV_HINHTHANH: ["hình thành xơ vữa", "xơ vữa hình thành", "mảng bám dày lên",
                   "tích tụ lâu ngày", "quá trình xơ vữa", "lâu ngày dày lên"],

    MO_4K:      ["mỡ máu", "mỡ trong lòng mạch", "mỡ xấu"],
    MO_CATDOC:  ["mỡ máu", "mỡ bám thành mạch", "cắt dọc mạch máu"],
    MO_DAY:     ["mỡ máu", "mỡ dày", "mỡ bám hai bên", "thành mạch dày"],
    MO_TINHTHE: ["cholesterol", "tinh thể mỡ", "mỡ xấu trong máu"],

    CM_TRONGMACH: ["cục máu đông", "máu đông", "huyết khối", "cục máu trong mạch"],

    MAU_HC_XANH: ["hồng cầu", "tế bào máu", "máu lưu thông"],
    MAU_HC_BC:   ["hồng cầu", "bạch cầu", "tế bào máu"],
    MAU_BACHCAU: ["bạch cầu", "tế bào miễn dịch", "sức đề kháng"],
    MAU_HC_TOI:  ["hồng cầu", "tế bào máu", "dòng máu"],
    MAU_HC_TROI: ["hồng cầu", "máu chảy chậm", "máu đặc"],

    TIM_XOAY:    ["trái tim", "tim mạch", "quả tim"],
    TIM_DMC:     ["động mạch chủ", "tim mạch", "mạch lớn"],
    TIM_TOI:     ["trái tim", "tim mạch", "giải phẫu tim"],
    TIM_VONG:    ["nhịp tim", "tim khỏe", "tuần hoàn"],
    TIM_NHOIMAU: ["nhồi máu cơ tim", "đau tim", "biến chứng tim"],
    TIM_DIEN_D:  ["nhịp tim", "điện tim", "mô hình tim"],
    TIM_MAUDAC_D: ["máu đặc", "mất nước", "thiếu nước máu đặc"],

    NAO_NAU:     ["não", "bộ não", "giải phẫu não"],
    NAO_HONG:    ["não", "bộ não", "tế bào não"],
    NAO_DAI:     ["não", "tín hiệu não", "hoạt động não"],
    NAO_CAM:     ["não", "não hoạt động", "não cần năng lượng"],
    NAO_TIM_TR:  ["não", "tế bào não", "nuôi dưỡng não"],
    NAO_TIM_DEN: ["não", "tế bào não", "oxy lên não"],
    NAO_SET:     ["xung điện não", "tín hiệu thần kinh", "não phóng điện"],
    NAO_EEG:     ["đo điện não", "sóng não", "kiểm tra não"],

    TK_TIM:      ["hệ thần kinh", "tế bào thần kinh", "neuron"],
    TK_DIENNAO:  ["điện não", "dẫn truyền thần kinh", "neuron thần kinh",
                  "tín hiệu thần kinh", "dẫn truyền"],
    TK_SYNAPSE:  ["dẫn truyền thần kinh", "synapse", "chất dẫn truyền"],
    TK_XUNG:     ["xung thần kinh", "thần kinh", "tín hiệu lan truyền"],
    TK_TOANTHAN: ["hệ thần kinh", "thần kinh toàn thân", "dây thần kinh"],

    CT_NGUC:     ["cơ thể", "hệ mạch toàn thân", "khắp cơ thể", "lồng ngực"],
    CT_TIEUHOA:  ["tiêu hóa", "đường ruột", "hấp thu", "dạ dày"],

    COQ10_XANH:  ["coenzyme q10", "coq10", "q10"],
    COQ10_VANG:  ["coenzyme q10", "coq10", "q10"],
    PHANTU_XANH: ["phân tử", "hoạt chất", "cấu trúc phân tử"],
    PHANTU_DEN:  ["phân tử", "hoạt chất", "thành phần"],
    DNA:         ["dna", "di truyền", "tế bào gốc"],
    TEBAO:       ["tế bào", "cấu trúc tế bào", "ty thể", "nhân tế bào"],
    DA_LOPCAT:   ["da", "mỡ dưới da", "lớp da"],
    DA_BEMAT:    ["da", "bề mặt da", "tế bào da"],

    XV_ANH_HEP:  ["xơ vữa", "mảng bám làm hẹp", "lòng mạch hẹp"],
    XV_ANH_TAC:  ["tắc mạch", "lòng mạch tắc", "mạch máu bị bít"],
    CM_ANH_KHOI: ["cục máu đông", "khối máu đông", "huyết khối"],

    NG_DENDEM:    ["ngủ ngon", "ngủ sâu", "giấc ngủ ngon", "ngủ được"],
    NG_NHINTREN:  ["ngủ ngon", "giấc ngủ", "ngủ sâu giấc"],
    NG_CANMAT:    ["ngủ ngon", "ngủ sâu", "người lớn tuổi ngủ"],
    NG_VV_CUASO:  ["tỉnh dậy sảng khoái", "buổi sáng", "vươn vai", "dậy khỏe khoắn"],
    NG_VV_GIUONG: ["tỉnh dậy sảng khoái", "sáng dậy", "vươn vai", "tỉnh táo"],
    NG_NAM_TREN:  ["ngủ ngon", "ngủ sâu", "giấc ngủ"],
    NG_NU_AM:     ["ngủ ngon", "giấc ngủ", "ngủ yên"],
    NG_DONGHO_D:  ["ngủ ngon", "đồng hồ báo thức", "giấc ngủ"],

    MN_TRANROC:   ["mất ngủ", "trằn trọc", "thao thức", "ngủ không sâu",
                   "nằm mãi không ngủ được"],
    MN_TROMINH:   ["trằn trọc", "trở mình", "ngủ chập chờn", "tỉnh giấc"],
    MN_NGOIDAY_D: ["mất ngủ", "tỉnh giấc giữa đêm", "ngồi dậy giữa đêm"],
    MN_ONGCU:     ["mất ngủ", "khó ngủ", "người già mất ngủ", "thức đêm"],

    ANDU_ONGNUOC: ["đường ống", "thông thoáng", "nước chảy thông", "ống thông"],
    ANDU_XERAC:   ["dọn rác", "đào thải", "loại bỏ chất thải", "rác thải"],
    ANDU_XERAC2:  ["dọn rác", "đào thải", "chất cặn bã"],

    DQ_NGA_GUC:  ["đột quỵ", "ngã gục", "ngã quỵ", "tai biến", "đổ gục"],
    DQ_OMNGUC1:  ["đau tức ngực", "ôm ngực", "khó thở", "tức ngực"],
    DQ_OMNGUC2:  ["đau tức ngực", "ôm ngực", "nhói ngực"],
    DQ_TEBI:     ["tê bì tay chân", "tê tay", "run tay", "tê bì"],
    DQ_XELAN:    ["di chứng đột quỵ", "xe lăn", "liệt", "sau tai biến"],
    DQ_CAPCUU:   ["cấp cứu", "vào viện", "băng ca", "nhập viện"],
    DQ_NAMVIEN:  ["nằm viện", "truyền dịch", "điều trị", "vào viện"],
    DQ_NGA1:     ["đột quỵ", "ngã quỵ", "tai biến"],
    DQ_NGA2:     ["đột quỵ", "ngã trong nhà", "tai biến"],
    DQ_NGA_DUONG: ["đột quỵ", "ngã ngoài đường", "tai biến bất ngờ"],
    DQ_MEO:      ["méo miệng", "dấu hiệu đột quỵ", "méo mặt", "liệt mặt"],
    DQ_PHUCHOI:  ["phục hồi chức năng", "tập vận động", "sau đột quỵ"],
    DQ_TAPDI:    ["tập đi", "phục hồi chức năng", "di chứng"],

    RN_ANH_XANH: ["hai hộp", "2 hộp", "combo", "sản phẩm"],
    RN_ANH_CO:   ["hai hộp", "2 hộp", "combo", "sản phẩm", "liệu trình"],

    RICH1:      ["rich coenzyme q10", "rich q10", "hộp rich"],
    RICH2:      ["rich coenzyme q10", "rich q10"],
    RICH3:      ["rich coenzyme q10", "rich q10", "hộp rich"],
    TAO_DO:     ["tảo đỏ", "thành phần", "nguyên liệu tự nhiên"],

    NATTO1:     ["nano nattokinase", "nattokinase", "sản phẩm", "hộp"],
    NATTO2:     ["nattokinase", "nội địa nhật", "sản phẩm nhật"],
    NATTO_2HOP: ["hai hộp", "2 hộp", "liệu trình", "giá", "combo", "sản phẩm"],
    RICHNATTO:  ["liệu trình", "6 hộp", "dùng một năm", "combo"],
    MEN_GAO:    ["men gạo đỏ", "cỏ trường thọ", "thành phần", "nguyên liệu"],

    # --- the duc / thien / an uong, khai 05/08/2026 ---
    TD_ONGBA_PHO:  ["thể dục thể thao", "thể dục", "đi bộ", "rèn luyện", "vận động",
                    "người lớn tuổi tập thể dục", "ông bà đi bộ"],
    TD_ONGCU_VUON: ["khởi động", "vươn vai", "thể dục buổi sáng", "giãn cơ", "thể dục"],
    TD_ONGCU_XANH: ["chạy bộ", "thể dục thể thao", "ông cụ khỏe mạnh", "rèn luyện"],
    TD_ONGBA_CHAY: ["chạy bộ", "thể dục thể thao", "vợ chồng già", "cùng nhau tập"],
    TD_SU_KHATTHUC:["tinh tấn", "thiền", "tu tập", "đi trong chánh niệm", "tâm tĩnh"],
    TD_ONGBA_VUI:  ["đi bộ", "thể dục thể thao", "vui vẻ", "khỏe mạnh", "tuổi già vui"],
    TD_KHICONG_O:  ["thiền định", "thiền", "khí công", "thái cực quyền", "tĩnh tâm",
                    "tâm trí sáng suốt", "hít thở"],
    TD_KHICONG_B:  ["thiền định", "thiền", "khí công", "hít thở", "tĩnh tâm", "dưỡng sinh"],
    TD_ONGCU_CO:   ["chạy bộ", "thể dục thể thao", "vận động mỗi ngày", "rèn luyện"],
    TD_NHOM_DIBO:  ["đi bộ", "thể dục thể thao", "đi bộ mỗi ngày", "vận động"],
    TD_BACU_BIEN:  ["đi bộ", "thể dục thể thao", "bà cụ đi bộ", "vận động nhẹ"],
    TD_ONGCU_TA:   ["đồng hành", "có người hướng dẫn", "tập luyện", "kiên trì",
                    "nghiêm túc", "tập tạ", "thể dục thể thao"],

    AU_RAU_CHO:    ["rau", "rau xanh", "ăn uống thanh đạm", "ăn rau", "chợ rau",
                    "thực phẩm tươi"],
    AU_RUONG_CAI:  ["rau", "rau xanh", "rau sạch", "ăn uống thanh đạm"],
    AU_RAUCU_XANH: ["rau củ", "ăn uống thanh đạm", "thực phẩm lành mạnh", "ăn xanh"],
    AU_BAN_TUVAN:  ["ăn uống điều độ", "chế độ ăn", "dinh dưỡng", "tư vấn dinh dưỡng"],
    AU_AN_SALAD:   ["ăn uống thanh đạm", "ăn salad", "bữa ăn lành mạnh", "ăn rau"],
    AU_ONGCU_NUOC: ["uống nước", "người lớn tuổi", "sinh hoạt điều độ"],
    AU_MAM_LANH:   ["thức ăn tốt cho sức khỏe", "bữa ăn lành mạnh", "ăn uống điều độ",
                    "thực phẩm tốt", "đồ ăn lành mạnh"],
}


if __name__ == "__main__":
    import subprocess
    # Kiem GOC KHO truoc. Truoc 05/08/2026 vong duoi loc bang
    # `v.startswith("/Volumes")` — ghi cung, nen khi kho doi cho (DILIM_FOOTAGE
    # tro di dau khac, hay o mount ten khac) thi khong hang so nao lot luoi va
    # no in ra "0 co / 0 mat". May moi nhin vao tuong LA XONG, that ra la
    # CHUA SOI GI CA. Gio loc theo chinh `B`.
    if not os.path.isdir(B):
        raise SystemExit(
            f"khong thay kho B-roll:\n  {B}\n\n"
            "  - cam o ngoai vao, hoac\n"
            "  - dat bien:  export DILIM_FOOTAGE=\"/Volumes/<ten o>/02. Dilim Footage\"")
    ok = bad = 0
    for k, v in sorted(globals().items()):
        if k.isupper() and isinstance(v, str) and v.startswith(B):
            if os.path.exists(v):
                d = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                    "format=duration", "-of", "csv=p=0", v],
                                   capture_output=True, text=True).stdout.strip()
                print(f"  OK  {k:12} {d[:6] if d else 'anh':>7}s  {os.path.basename(v)}")
                ok += 1
            else:
                print(f"  MAT {k:12}         {v}")
                bad += 1
    print(f"\n{ok} co / {bad} mat")
