# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — 06b-test-toc-do.

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

    python3 06b-test-toc-do/plan.py
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
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*TÊ TAY, TÊ CHÂN*" / "TÌM TRÊN MẠNG"
 #     clip da dung: dotquy-tebi-runtay-01.mp4 x1
 (   0.00, "TÊ TAY, TÊ CHÂN,",                              "KHI MÀ ANH CHỊ TÌM KIẾM TRÊN MẠNG",              "yellow",   "", 0, ""),   #?
 # KHO 0.75 · da dung 1x/1 job · yellow
 #     "AI CŨNG NÓI *THIẾU CHẤT*" / "*THIẾU CANXI*, *THIẾU MAGIE*"
 #     clip da dung: (trống) x1
 (   3.44, "THÌ Ở ĐÂU NGƯỜI TA CŨNG NÓI LÀ MÌNH",           "ĐANG BỊ THIẾU CHẤT, THIẾU CANXI",                "warning",  "", 0, ""),   #?
 (   7.42, "THIẾU MAGIE,",                                  "THIẾU VITAMIN NHÓM B, RỒI ANH",                  "yellow",   "", 0, ""),   #?
 (  10.54, "CHỊ MUA VỀ BỔ SUNG ĐÚNG",                       "KHÔNG? CÁI ĐÓ ĐÚNG NHÁ, NHƯNG ẤY",               "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · positive
 #     "CÁI ĐÓ *ĐÚNG*" / "THIẾU THÌ *BỔ SUNG LÀ ĐÚNG*"
 #     clip da dung: (trống) x1
 (  14.40, "KHI MÀ THIẾU ẤY, BỔ SUNG",                      "LÀ ĐÚNG NÀY, NHƯNG NÀY",                         "yellow",   "", 0, ""),   #?
 # KHO 0.86 · da dung 1x/1 job · yellow
 #     "NHƯNG CÓ MỘT CHUYỆN" / "*ÍT AI NÓI VỚI ANH CHỊ*"
 #     clip da dung: (trống) x1
 (  17.64, "CÓ MỘT CÁI CÂU CHUYỆN NÀY,",                    "ÍT AI NÓI VỚI ANH CHỊ",                          "yellow",   "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*TÊ TAY, TÊ CHÂN*" / "*KHÔNG CHỈ MỘT NGUYÊN NHÂN*"
 #     clip da dung: dotquy-tebi-runtay-01.mp4 x1
 (  21.10, "ĐÓ LÀ TÊ TAY, TÊ CHÂN ẤY,",                     "KHÔNG PHẢI CHỈ CÓ MỘT NGUYÊN NHÂN",              "warning",  "", 0, ""),   #?
 (  24.66, "TÊ CHÂN, CANXI",                                "VÀ MAGIE, CÁI KHẢ NĂNG",                         "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · yellow
 #     "*CANXI VÀ MAGIE*" / "LÀM VIỆC RA SAO?"
 #     clip da dung: (trống) x1
 (  28.96, "CÁI CHỨC NĂNG CỦA NÓ LÀM VIỆC RA SAO?",         "CANXI VÀ MAGIE LÀ THỨ GIỮ",                      "warning",  "", 0, ""),   #?
 # NGO whisper: "mảng của dây thần kinh" co the la "màng của dây thần kinh" — 'mang' vs 'mang' — nghe lai, ngu canh noi ve lop vo boc day than kinh.
 # KHO 0.75 · da dung 1x/1 job · product
 #     "*MÀNG CỦA DÂY THẦN KINH*"
 #     clip da dung: thankinh-neuron-xanh-01.mp4 x1
 (  32.78, "ỔN ĐỊNH CÁI MẢNG CỦA DÂY THẦN KINH.",           "ANH CHỊ HÌNH DUNG ẤY, LÀ",                       "yellow",   "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · yellow
 #     "DÂY THẦN KINH NHƯ *DÂY ĐIỆN*" / "CÓ *LỚP VỎ BỌC*"
 #     clip da dung: thankinh-xung-bungsang-01.mp4 x1
 # KHO 0.75 · da dung 1x/1 job · product
 #     "*MÀNG CỦA DÂY THẦN KINH*"
 #     clip da dung: thankinh-neuron-xanh-01.mp4 x1
 (  36.12, "DÂY THẦN KINH ẤY, NHƯ LÀ MỘT SỢI",              "DÂY ĐIỆN, CÓ MỘT CÁI LỚP VỎ BỌC",                "warning",  "", 0, ""),   #?
 (  40.40, "CANXI VÀ MAGIE CHÍNH",                          "LÀ LỚP VỎ ĐÓ, ĐỦ ẤY",                            "warning",  "", 0, ""),   #?
 (  43.42, "THÌ TÍN HIỆU CHẠY ĐÚNG ĐƯỜNG,",                 "THIẾU ẤY, THÌ LỚP VỎ MỎNG ĐI",                   "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*TỰ PHÁT TÍN HIỆU*" / "DÙ KHÔNG AI CHẠM VÀO"
 #     clip da dung: thankinh-diennao-dantruyen-01.mp4 x1
 (  47.24, "DÂY NHẠY QUÁ MỨC, TỰ PHÁT TÍN HIỆU",            "DÙ KHÔNG AI CHẠM VÀO. NÊN, MÌNH",                "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "NÊN THẤY *TÊ, GIẬT GIẬT*" / "*CHÂM CHÍCH*"
 #     clip da dung: dotquy-tebi-runtay-01.mp4 x1
 (  52.16, "THẤY TÊ, THẤY GIẬT GIẬT,",                      "THẤY CHÂM CHÍCH. KIỂU TÊ",                       "product",  "", 0, ""),   #?
 # KHO 0.8 · da dung 1x/1 job · warning
 #     "*TÊ ĐỐI XỨNG HAI BÊN*" / "ĐẦU NGÓN TAY, *CHUỘT RÚT*"
 #     clip da dung: dotquy-tebi-runtay-01.mp4 x1
 (  55.54, "MÀ THƯỜNG ĐỐI XỨNG HAI BÊN NÀY,",               "HAY LÀ TÊ QUANH MIỆNG, TÊ ĐẦU NGÓN TAY",         "product",  "", 0, ""),   #?
 (  59.40, "NGÓN CHÂN, HAY KÈM CHUỘT RÚT.",                 "NHƯNG, CÒN MỘT KIỂU TÊ NỮA",                     "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · positive
 #     "*MÁU ĐI TỚI NƠI CẦN TỚI*"
 #     clip da dung: machmau-longmach-nhindoc-01.mp4 x1
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*OXY KHÔNG TỚI ĐƯỢC NƠI CẦN*"
 #     clip da dung: mau-hongcau-bachcau-01.mp4 x1
 (  63.24, "ĐÓ LÀ KHI MÁU KHÔNG MANG",                      "ĐỦ OXY TỚI NƠI NÓ CẦN",                          "warning",  "", 0, ""),   #?
 # KHO 0.75 · da dung 1x/1 job · product
 #     "*MÀNG CỦA DÂY THẦN KINH*"
 #     clip da dung: thankinh-neuron-xanh-01.mp4 x1
 (  67.84, "MÀ. ĐÓ",                                        "LÀ KHI MÀ DÂY THẦN KINH LÀ THỨ",                 "yellow",   "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*THIẾU MỘT CHÚT LÀ BÁO NGAY*"
 #     clip da dung: thankinh-neuron-xanh-01.mp4 x1
 (  71.12, "MÀ TIÊU THỤ OXY RẤT LÀ NHIỀU,",                 "THIẾU MỘT CHÚT LÀ NÓ BÁO NGAY",                  "yellow",   "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*CŨNG TÊ Y HỆT*"
 #     clip da dung: (trống) x1
 (  75.66, "VÀ NÓ CŨNG BÁO BẰNG CẢM",                       "GIÁC TÊ Y HỆT NHƯ TRÊN. HAI",                    "product",  "", 0, ""),   #?
 # KHO 0.86 · da dung 1x/1 job · yellow
 #     "HAI CÁI KHÁC NHAU" / "*TỪ TẬN GỐC RỄ*"
 #     clip da dung: (trống) x1
 (  80.08, "CÁI NÀY KHÁC NHAU TỪ TẬN",                      "GỐC RỄ NHÉ. MỘT BÊN LÀ CÁI DÂY",                 "yellow",   "", 0, ""),   #?
 # KHO 0.89 · da dung 1x/1 job · warning
 #     "MỘT BÊN LÀ *DÂY BỊ MÒN VỎ*" / "MỘT BÊN LÀ *ỐNG BỊ HẸP*"
 #     clip da dung: machmau-hep-that-01.mp4 x1
 (  84.66, "BỊ MÒN ĐẾN LỚP VỎ.",                            "CÒN MỘT BÊN LÀ CÁI ỐNG DẪN. BỊ HẸP",             "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · positive
 #     "CANXI + MAGIE" / "*SỬA ĐƯỢC CÁI DÂY*"
 #     clip da dung: thankinh-toanthan-vang-01.mp4 x1
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "NHƯNG *KHÔNG SỬA ĐƯỢC ỐNG*"
 #     clip da dung: machmau-anddu-ongdong-01.mp4 x1
 (  88.82, "CANXI VÀ MAGIE SỬA ĐƯỢC CÁI DÂY,",              "NHƯNG NÓ KHÔNG SỬA ĐƯỢC CÁI ỐNG",                "warning",  "", 0, ""),   #?
 (  93.32, "ĐÓ LÀ LÝ DO VÌ SAO ẤY.",                        "CÓ NHỮNG ANH CHỊ UỐNG CANXI MÃI",                "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · yellow
 #     "*TỰ HỎI MÌNH MỘT CÂU*"
 #     clip da dung: (trống) x1
 (  97.46, "MÀ VẪN TÊ, ĐÚNG KHÔNG? CÓ MỘT CÂU",             "LÀ ANH CHỊ TỰ HỎI MÌNH",                         "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · yellow
 #     "THÀNH CHIA SẺ MỘT CÁCH" / "ĐỂ *TỰ PHÂN BIỆT*"
 #     clip da dung: (trống) x1
 ( 103.52, "THÀNH CHIA SẺ CHO ANH CHỊ MỘT CÁCH",            "ĐỂ MÌNH CÓ THỂ TỰ PHÂN BIỆT",                    "yellow",   "", 0, ""),   #?
 ( 107.40, "VÍ DỤ NHƯ LÀ, NẾU MÀ ĐI",                       "BỘ MỘT LÚC, CHÂN",                               "yellow",   "", 0, ""),   #?
 ( 110.48, "CÓ MỎI HAY LÀ ĐAU THÊM",                        "KHÔNG? HAY NGỒI MỘT TÍ",                         "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*ĐI THÌ ĐAU, NGHỈ THÌ ĐỠ*"
 #     clip da dung: (trống) x1
 ( 114.66, "THÌ CÓ ĐỠ HƠN KHÔNG? NẾU ĐI",                   "THÌ ĐAU, MÀ NGHỈ THÌ ĐỠ",                        "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "NGHIÊNG VỀ *MẠCH MÁU*" / "CHỨ KHÔNG PHẢI *THIẾU CHẤT*"
 #     clip da dung: machmau-catdoc-tim-01.mp4 x1
 ( 118.68, "THÌ CÁI ĐÓ NGHIÊNG VỀ MẠCH MÁU,",               "CHỨ KHÔNG PHẢI LÀ THIẾU CHẤT",                   "warning",  "", 0, ""),   #?
 # KHO 0.78 · da dung 1x/1 job · warning
 #     "LÚC ĐI, CƠ *CẦN NHIỀU MÁU*" / "*ỐNG HẸP* THÌ CẤP KHÔNG KỊP"
 #     clip da dung: machmau-hep-that-01.mp4 x1
 ( 122.90, "VÌ LÚC ĐI, CƠ CẦN NHIỀU",                       "MÁU HƠN. MÀ CÁI ỐNG HẸP ẤY",                     "warning",  "", 0, ""),   #?
 ( 127.52, "THÌ CUNG CẤP MÁU KHÔNG KỊP.",                   "NGHỈ THÌ NHU CẦU GIẢM XUỐNG",                    "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*ĐI THÌ ĐAU, NGHỈ THÌ ĐỠ*"
 #     clip da dung: (trống) x1
 # KHO 0.75 · da dung 1x/1 job · warning
 #     "CÒN TÊ DO *THIẾU CHẤT*" / "*ĐI HAY NGHỈ VẪN BỊ*"
 #     clip da dung: dotquy-tebi-runtay-01.mp4 x1
 ( 132.70, "NÊN LÀ MÌNH ĐỠ ĐAU HƠN. CÒN TÊ",                "DO THIẾU CHẤT THÌ ĐI HAY NGHỈ",                  "warning",  "", 0, ""),   #?
 ( 137.28, "MÌNH VẪN BỊ VẬY. THẬM CHÍ",                     "KHI NẰM NGHỈ BAN ĐÊM CÒN TÊ HƠN. THÊM",          "yellow",   "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "TAY CHÂN *HAY BỊ LẠNH*?"
 #     clip da dung: (trống) x1
 ( 141.72, "MỘT DẤU HIỆU NỮA, LÀ TAY CHÂN ANH",             "CHỊ CÓ HAY BỊ LẠNH KHÔNG? LẠNH",                 "warning",  "", 0, ""),   #?
 ( 145.92, "LÀ SAO? LẠNH LÀ KHI SỜ",                        "VÀO MÌNH THẤY MÁT HƠN PHẦN",                     "yellow",   "", 0, ""),   #?
 ( 149.66, "CÒN LẠI CỦA CƠ THỂ.",                           "ĐẤY LÀ BIỂU HIỆN CỦA VIỆC MÁU",                  "yellow",   "", 0, ""),   #?
 # KHO 0.8 · da dung 1x/1 job · warning
 #     "*MÁU NGOẠI VI TỚI KHÔNG ĐỦ*"
 #     clip da dung: cothe-hemach-longnguc-01.mp4 x1
 ( 153.00, "NGOẠI VI TỚI KHÔNG ĐỦ. BA,",                    "VỚI NHỮNG TRƯỜNG HỢP MÀ BỊ TÊ LIÊN",             "product",  "", 0, ""),   #?
 # KHO 0.78 · da dung 1x/1 job · product
 #     "TÊ LIÊN QUAN *MẠCH MÁU*" / "BÊN THÀNH CÓ *MỘT BỘ ĐÔI*"
 #     clip da dung: richnatto-01.mp4 x1
 ( 158.04, "QUAN ĐẾN CÁI MẠCH MÁU,",                        "THÌ BÊN THÀNH CÓ MỘT BỘ ĐÔI NÀY",                "yellow",   "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · product
 #     "ĐI *ĐÚNG HAI CHỖ*" / "THỨ NHẤT LÀ *NATTOKINASE*"
 #     clip da dung: natto-01.mp4 x1
 ( 161.60, "ĐI HỖ TRỢ ĐÚNG HAI CHỖ",                        "RỒI. THỨ NHẤT LÀ NATTOKINASE",                   "product",  "", 0, ""),   #?
 # KHO 0.83 · da dung 1x/1 job · product
 #     "LO *CÁI ĐƯỜNG ỐNG*" / "TỨC LÀ *MẠCH MÁU*"
 #     clip da dung: machmau-anddu-ongdong-01.mp4 x1
 ( 166.20, "LO CÁI ĐƯỜNG ỐNG LÀ CÁI ĐƯỜNG",                 "MẠCH MÁU CỦA MÌNH",                              "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · positive
 #     "ENZYME NÀY" / "*PHÂN GIẢI SỢI FIBRIN*"
 #     clip da dung: cucmau-khoi-fibrin-01.mp4 x1
 ( 169.46, "ENZYME NÀY GIÚP PHÂN GIẢI CÁI SỢI FIBRIN,",     "TỨC LÀ NHỮNG CÁI SỢI ẤY",                        "product",  "", 0, ""),   #?
 # KHO 0.89 · da dung 1x/1 job · warning
 #     "SỢI ĐANG GIỮ *TẾ BÀO MÁU*" / "THÀNH CỤC *TRONG LÒNG MẠCH*"
 #     clip da dung: cucmau-khoi-fibrin-01.mp4 x1
 # KHO 0.86 · da dung 1x/1 job · warning
 #     "GIỮ *TẾ BÀO MÁU* LẠI" / "TẠO THÀNH NHỮNG *CỤC*"
 #     clip da dung: cucmau-khoi-trongmach-01.mp4 x1
 ( 174.20, "NÓ ĐANG GIỮ LẠI TẾ BÀO MÁU THÀNH",              "CỤC CỦA MÌNH Ở TRONG LÒNG MẠCH",                 "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · positive
 #     "GỠ ĐƯỢC *CÁI LƯỚI* ĐÓ RA" / "*LÒNG MẠCH THÔNG THOÁNG*"
 #     clip da dung: machmau-longmach-nhindoc-01.mp4 x1
 ( 178.46, "GỠ ĐƯỢC CÁI LƯỚI ĐÓ RA ẤY,",                    "THÌ LÒNG MẠCH MÌNH THÔNG THOÁNG DẦN",            "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · positive
 #     "*MÁU ĐI TỚI NƠI CẦN TỚI*"
 #     clip da dung: machmau-longmach-nhindoc-01.mp4 x1
 # KHO 0.75 · da dung 1x/1 job · warning
 #     "*OXY KHÔNG TỚI ĐƯỢC NƠI CẦN*"
 #     clip da dung: mau-hongcau-bachcau-01.mp4 x1
 ( 181.56, "MÁU ĐI ĐƯỢC TỚI NƠI CẦN TỚI. THỨ HAI,",         "LÀ RICH COENZYME Q10",                           "yellow",   "", 0, ""),   #?
 ( 186.80, "LO CÁI PHẦN MÁY BƠM. CHỖ NÀY,",                 "THÀNH PHẢI NÓI KĨ MỘT CHÚT NHÉ",                 "warning",  "", 0, ""),   #?
 ( 189.90, "VÌ CÁI NÀY, NHIỀU ANH CHỊ CHƯA BIẾT ẤY.",       "TRONG MỖI TẾ BÀO CỦA MÌNH ẤY",                   "warning",  "", 0, ""),   #?
 ( 193.74, "CÓ MỘT BỘ PHẬN SINH RA NĂNG LƯỢNG,",            "VÀ COENZYME Q10 LÀ CHẤT XÚC TÁC",                "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · product
 #     "ĐỂ *TẠO RA NĂNG LƯỢNG*"
 #     clip da dung: coq10-cau-vang-01.mp4 x1
 ( 199.18, "BẮT BUỘC PHẢI CÓ Ở KHÂU CUỐI CÙNG,",            "ĐỂ TẠO RA NĂNG LƯỢNG ĐÓ",                        "product",  "", 0, ""),   #?
 ( 203.36, "KHÔNG CÓ NÓ THÌ TẾ BÀO",                        "KHÓ CÓ MỘT ĐỦ NGUYÊN LIỆU",                      "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · product
 #     "ĐỂ *TẠO RA NĂNG LƯỢNG*"
 #     clip da dung: coq10-cau-vang-01.mp4 x1
 ( 206.66, "ĐỂ TẠO RA NĂNG LƯỢNG ĐƯỢC. VẬY",                "THÌ CHO THÀNH HỎI",                              "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · product
 #     "*TẾ BÀO CƠ TIM*"
 #     clip da dung: tim-dap-nento-01.mp4 x1
 # KHO 1.0 · da dung 1x/1 job · yellow
 #     "TẾ BÀO NÀO CẦN" / "*NHIỀU NĂNG LƯỢNG NHẤT*?"
 #     clip da dung: (trống) x1
 ( 210.70, "TẾ BÀO NÀO CẦN NHIỀU NĂNG LƯỢNG",               "NHẤT TRONG CƠ THỂ Ạ? TẾ BÀO CƠ TIM",             "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · yellow
 #     "TIM ĐẬP *KHÔNG NGHỈ*" / "SUỐT CẢ ĐỜI"
 #     clip da dung: tim-dap-nento-01.mp4 x1
 ( 214.34, "VÌ QUẢ TIM ĐẬP KHÔNG NGHỈ",                     "MỘT GIÂY NÀO SUỐT CẢ ĐỜI",                       "product",  "", 0, ""),   #?
 ( 217.70, "VÀ NHẤT LÀ SAU 40 TUỔI,",                       "THÌ CƠ THỂ ẤY, CÁI KHẢ NĂNG TỔNG HỢP COENZYME",  "product",  "", 0, ""),   #?
 ( 222.08, "CREAM 10 GIẢM DẦN.",                            "NÊN TIM BƠM YẾU ĐI THEO THỜI GIAN",              "product",  "", 0, ""),   #?
 ( 225.62, "MÀ ÍT NGƯỜI NHẬN RA. CHỈ NHẬN",                 "RA KHI THẤY LÀ, BÂY",                            "yellow",   "", 0, ""),   #?
 # NGO whisper: "lau cầu thang" co the la "leo cầu thang" — 'lau cau thang' co that. Nhung ngu canh la dau hieu tim yeu -> gan nhu chac la 'leo'.
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "TAY CHÂN *HAY BỊ LẠNH*?"
 #     clip da dung: (trống) x1
 ( 229.76, "GIỜ MÌNH LAU CẦU THANG NÀY,",                   "BỊ MỆT HƠN XƯA NÀY, TAY CHÂN NÀY, LẠNH",         "yellow",   "", 0, ""),   #?
 # NGO whisper: "bể bỏ" co the la "bơ phờ" — 'be bo' khong co nghia; doan la 'bo pho' nhung chua chac — nghe lai doan do.
 ( 232.80, "HƠN XƯA NÀY, ĐÚNG KHÔNG? HƠI BỊ HỤT.",          "VÀ NGƯỜI LÚC NÀO CŨNG BỂ BỎ",                    "warning",  "", 0, ""),   #?
 # KHO 0.78 · da dung 1x/1 job · warning  [CO CHU SO — KIEM TAY]
 #     "LÚC NÀO CŨNG *MỆT MỎI*" / "DÙ *NGỦ ĐỦ 8 TIẾNG*"
 #     clip da dung: metmoi-bopmui-4k-01.mp4 x1
 ( 236.14, "MỆT MỎI, DÙ NGỦ ĐỦ 8 TIẾNG.",                   "VÂNG. HƠN NỮA ẤY",                               "warning",  "", 0, ""),   #?
 # NGO whisper: "Bến Thành" co the la "bên Thành" — Ben Thanh la ten cho that. O day anh xung 'ben Thanh' (ben minh).
 # KHO 0.8 · da dung 1x/1 job · product  [CO CHU SO — KIEM TAY]
 #     "Q10 BÊN THÀNH LÀ *DẠNG KHỬ*"
 #     clip da dung: richnatto-01.mp4 x1
 ( 239.36, "LÀ COENZYME Q10 CỦA BẾN THÀNH,",                "LÀ COENZYME Q10 DẠNG KHỬ",                       "yellow",   "", 0, ""),   #?
 ( 243.80, "COENZYME Q10 NHÉ, NÓ CÓ 2",                     "DẠNG. MỘT LÀ DẠNG OXY HÓA",                      "yellow",   "", 0, ""),   #?
 # KHO 0.8 · da dung 1x/1 job · positive
 #     "*DẠNG KHỬ*" / "CƠ THỂ *DÙNG ĐƯỢC NGAY*"
 #     clip da dung: coq10-cau-xanh-01.mp4 x1
 ( 247.70, "HAI LÀ DẠNG KHỬ.",                              "DẠNG OXY HÓA VÀO CƠ THỂ",                        "yellow",   "", 0, ""),   #?
 ( 251.26, "PHẢI CHUYỂN ĐỔI THÌ MỚI DÙNG",                  "ĐƯỢC. MÀ ẤY, NGƯỜI TRUNG NIÊN",                  "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*NGƯỜI TRUNG NIÊN*" / "HOẶC *ĐƯỜNG RUỘT KÉM*"
 #     clip da dung: cothe-tieuhoa-01.mp4 x1
 ( 254.92, "MÀ, MÀ NGƯỜI TRUNG NIÊN",                       "HOẶC NGƯỜI ĐƯỜNG RUỘT KÉM",                      "product",  "", 0, ""),   #?
 ( 259.28, "THÌ CÁI KHẢ NĂNG CHUYỂN ĐỔI,",                  "KHẢ NĂNG CHUYỂN HÓA KHÔNG CÓ TỐT. CÒN DẠNG KHỬ", "warning",  "", 0, ""),   #?
 # KHO 0.8 · da dung 1x/1 job · positive
 #     "*DẠNG KHỬ*" / "CƠ THỂ *DÙNG ĐƯỢC NGAY*"
 #     clip da dung: coq10-cau-xanh-01.mp4 x1
 # KHO 0.8 · da dung 1x/1 job · product
 #     "CÒN CÓ *ASTAXANTHIN*" / "*CHỐNG OXY HOÁ*"
 #     clip da dung: taodo-thanhphan-01.mp4 x1
 ( 263.14, "LÀ DẠNG CƠ THỂ MÌNH DÙNG ĐƯỢC NGAY. TRONG ĐÓ,", "CÒN CÓ ASTAXANTHIN, CHỐNG OXY HÓA",              "yellow",   "", 0, ""),   #?
 ( 268.56, "VÀ CỘNG THÊM MỘT CHÚT CHIẾT XUẤT",              "TIÊU ĐEN, ĐỂ TĂNG THÊM KHẢ",                     "yellow",   "", 0, ""),   #?
 ( 271.80, "NĂNG HẤP THỤ COENZYME",                         "10 VÀO CƠ THỂ. VÂNG",                            "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · yellow
 #     "*HIỂU ĐƠN GIẢN*"
 #     clip da dung: richnatto-01.mp4 x1
 ( 275.18, "NÊN HIỂU ĐƠN GIẢN ẤY, HAI CÁI SẢN PHẨM NÀY,",   "MỘT BÊN LÀ THÔNG ỐNG, MỘT",                      "product",  "", 0, ""),   #?
 # KHO 0.75 · da dung 1x/1 job · warning
 #     "*THÔNG ỐNG MÀ BƠM YẾU*" / "*BƠM KHOẺ MÀ ỐNG TẮC*"
 #     clip da dung: tim-do-xoay-01.mp4 x1
 ( 278.32, "BÊN LÀ TĂNG CÁI NĂNG LƯỢNG",                    "CHO CÁI MÁY BƠM. THÔNG ỐNG MÀ BƠM YẾU",          "product",  "", 0, ""),   #?
 ( 284.12, "BƠM KHỎE MÀ ỐNG TẮC,",                          "THÌ CÀNG TĂNG ÁP LỰC LÊN THÀNH MẠCH",            "warning",  "", 0, ""),   #?
 ( 287.32, "PHẢI CÓ ĐỦ CẢ HAI. THÀNH NÓI",                  "THÊM MỘT CHÚT NHÉ, CHO RÕ NHÉ",                  "yellow",   "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · positive
 #     "ĐANG UỐNG *CANXI HAY MAGIE*" / "THÌ *CỨ TIẾP TỤC UỐNG*"
 #     clip da dung: (trống) x1
 # KHO 1.0 · da dung 1x/1 job · yellow
 #     "ĐANG UỐNG *CANXI, MAGIE*"
 #     clip da dung: (trống) x1
 ( 291.72, "NẾU ANH CHỊ ĐANG UỐNG CANXI HAY MAGIE,",        "THÌ CỨ TIẾP TỤC UỐNG",                           "product",  "", 0, ""),   #?
 ( 295.54, "ĐÚNG KHÔNG? NHƯNG MÌNH PHẢI HIỂU,",             "LÀ HAI CÁI THỨ NÀY",                             "warning",  "", 0, ""),   #?
 ( 299.22, "NÓ KHÔNG CÓ PHẢN ỨNG VỚI NHAU.",                "ĐÚNG KHÔNG? NÓ KHÔNG CÓ ĐÁ NHAU",                "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · yellow
 #     "ĐANG UỐNG *CANXI, MAGIE*"
 #     clip da dung: (trống) x1
 ( 303.80, "VẬY NÊN, NẾU MÀ ANH CHỊ",                       "ĐANG UỐNG CANXI, MAGIE",                         "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*MÀ VẪN TÊ TAY*"
 #     clip da dung: dotquy-tebi-runtay-01.mp4 x1
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "TAY CHÂN *HAY BỊ LẠNH*?"
 #     clip da dung: (trống) x1
 ( 308.84, "MÀ VẪN THẤY MÌNH CÓ TRƯỜNG HỢP TÊ TAY,",        "HOẶC BỊ LẠNH TAY, LẠNH CHÂN",                    "product",  "", 0, ""),   #?
 ( 312.96, "THÌ MÌNH PHẢI LẤY MỘT CÁI, ĐỂ LƯU",             "Ý LÀ LIỆU MÌNH CÓ ĐANG BỊ",                      "yellow",   "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "CÓ *VẤN ĐỀ VỀ MẠCH MÁU*?"
 #     clip da dung: machmau-catdoc-tim-01.mp4 x1
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "MẠCH MÁU ĐANG" / "*GẶP VẤN ĐỀ*"
 #     clip da dung: machmau-hep-momau-01.mp4 x1
 ( 316.26, "GẶP VẤN ĐỀ VỀ MẠCH MÁU HAY KHÔNG. NẾU NÓ",      "ĐI KÈM VỚI CẢ NHỮNG NGƯỜI",                      "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "NHƯ *TIỂU ĐƯỜNG*, *MỠ MÁU*"
 #     clip da dung: momau-hatvang-xoay-01.mp4 x1
 ( 320.16, "CÓ BỆNH NỀN NHƯ LÀ TIỂU ĐƯỜNG",                 "HOẶC MỠ MÁU",                                    "product",  "", 0, ""),   #?
 # KHO 0.75 · da dung 1x/1 job · warning
 #     "MẠCH MÁU BỊ *TẮC*" / "BỊ *KẸT*, BỊ *BÍT*"
 #     clip da dung: xovua-mangbam-vang-02.mp4 x1
 # KHO 0.75 · da dung 1x/1 job · warning
 #     "THÌ *MẠCH MÁU TỔN THƯƠNG*" / "*ÁCH TẮC CÀNG NHIỀU HƠN*"
 #     clip da dung: cucmau-tacmach-01.mp4 x1
 ( 323.24, "THÌ CÁI PHẦN TRĂM MẠCH MÁU CỦA MÌNH",           "ĐANG BỊ TỔN THƯƠNG, ĐANG BỊ ÁCH TẮC",            "product",  "", 0, ""),   #?
 ( 327.26, "NÓ CÀNG NHIỀU HƠN NHÉ. VỀ LIỆU TRÌNH",          "THÌ MỖI THỨ SẼ LÀ HAI VIÊN",                     "product",  "", 0, ""),   #?
 # KHO 0.86 · da dung 1x/1 job · product  [CO CHU SO — KIEM TAY]
 #     "MỖI HỘP *120 VIÊN*" / "DÙNG ĐƯỢC *2 THÁNG*"
 #     clip da dung: natto-01.mp4 x1
 # KHO 0.83 · da dung 1x/1 job · product  [CO CHU SO — KIEM TAY]
 #     "MỘT HỘP *120 VIÊN*" / "DÙNG ĐƯỢC *2 THÁNG*"
 #     clip da dung: natto-01.mp4 x1
 ( 330.72, "MỘT NGÀY. MỖI MỘT HỘP SẼ LÀ GỒM 120 VIÊN,",     "DÙNG ĐƯỢC TRONG HAI THÁNG",                      "product",  "", 0, ""),   #?
 ( 334.68, "ĐỦ MƯỜI HAI THÁNG LÀ SÁU HỘP",                  "MỖI LOẠI. TRỌN MỘT NĂM ẤY",                      "product",  "", 0, ""),   #?
 ( 339.14, "NẾU MÀ ANH CHỊ",                                "MÀ MUA CẢ SÁU HỘP",                              "product",  "", 0, ""),   #?
 # NGO whisper: "Biên Thành" co the la "bên Thành" — nhu tren.
 ( 342.22, "THÌ BIÊN THÀNH SẼ TẶNG",                        "CHO ANH CHỊ MỖI LOẠI MỘT HỘP",                   "product",  "", 0, ""),   #?
 ( 347.06, "VÀ SÁU HỘP MỖI LOẠI",                           "THÌ SẼ CÓ GIÁ LÀ 31",                            "product",  "", 0, ""),   #?
 ( 351.62, "TRIỆU 080.000. CÒN NHƯ THÀNH",                  "NÓI Ở TRÊN, NHỮNG ANH CHỊ NÀO",                  "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "THÀNH KHUYÊN *ĐI KHÁM*"
 #     clip da dung: (trống) x1
 # KHO 0.8 · da dung 1x/1 job · warning
 #     "AI *TIỂU ĐƯỜNG LÂU NĂM*"
 #     clip da dung: (trống) x1
 ( 356.92, "MÀ ĐANG BỊ TIỂU ĐƯỜNG LÂU NĂM,",                "THÀNH KHUYÊN LÀ ĐI KHÁM NHÉ",                    "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "TIỂU ĐƯỜNG GÂY TÊ" / "*THEO NHIỀU CÁCH*"
 #     clip da dung: dotquy-tebi-runtay-01.mp4 x1
 ( 361.58, "BỞI VÌ TIỂU ĐƯỜNG CÓ THỂ",                      "GÂY TÊ THEO NHIỀU CÁCH",                         "product",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · warning
 #     "*KHÔNG THỂ ĐOÁN MÒ ĐƯỢC*"
 #     clip da dung: (trống) x1
 ( 366.52, "ĐÚNG KHÔNG? NHƯNG MÌNH KHÔNG THỂ ĐOÁN",         "MÒ ĐƯỢC, NHẤT LÀ NGƯỜI BỊ TIỂU ĐƯỜNG",           "product",  "", 0, ""),   #?
 ( 369.68, "NHÉ ANH CHỊ.",                                  "NÊN ANH CHỊ MUỐN",                               "yellow",   "", 0, ""),   #?
 # KHO 1.0 · da dung 2x/2 job · cta
 #     "HOẶC ĐỂ LẠI" / "*TÊN + SỐ ĐIỆN THOẠI*"
 #     clip da dung: DSCF0900.MOV x1, thankinh-neuron-xanh-01.mp4 x1
 # KHO 0.88 · da dung 1x/1 job · cta
 #     "MUỐN *ĐƯỢC TƯ VẤN*" / "ĐỂ LẠI *TÊN + SỐ ĐIỆN THOẠI*"
 #     clip da dung: (trống) x1
 # KHO 0.83 · da dung 2x/2 job · cta
 #     "ĐỂ LẠI *TÊN + SỐ ĐIỆN THOẠI*" / "DƯỚI VIDEO"
 #     clip da dung: richnatto-01.mp4 x1, natto-2hop.jpg x1
 ( 373.44, "ĐƯỢC TƯ VẤN, HÃY ĐỂ LẠI TÊN",                   "VÀ SỐ ĐIỆN THOẠI BÊN DƯỚI. THÀNH SẼ GỌI LẠI",    "cta",      "", 0, ""),   #?
 ( 376.46, "NGHE KỸ TÌNH TRẠNG",                            "RỒI MỚI TƯ VẤN NHÉ",                             "warning",  "", 0, ""),   #?
 ( 379.82, "VÀ NẾU MUỐN, ANH CHỊ CÓ THỂ GỌI",               "VÀO SỐ HOTLINE CỦA THÀNH ĐÓ LÀ 0862",            "cta",      "", 0, ""),   #?
 ( 384.16, "745 495. SẢN PHẨM NÀY",                         "KHÔNG PHẢI LÀ THUỐC",                            "warning",  "", 0, ""),   #?
 # KHO 1.0 · da dung 1x/1 job · product
 #     "VÀ KHÔNG CÓ TÁC DỤNG" / "*THAY THẾ THUỐC CHỮA BỆNH*"
 #     clip da dung: (trống) x1
 ( 387.36, "VÀ KHÔNG CÓ TÁC DỤNG",                          "THAY THẾ THUỐC CHỮA BỆNH",                       "warning",  "", 0, ""),   #?
]


if __name__ == "__main__":
    # Truyen fallback=<anh> neu muon may TU DOI clip qua ngan sang anh do.
    # Mac dinh la BO TRONG — may khong hieu nghia, doi lung tung la sai bai.
    build(HERE, R)
