# -*- coding: utf-8 -*-
"""Dich TEN FILE -> MO TA tieng Viet co dau.

VI SAO CAN: `goi_y_broll.tu` tach tu bang khoang trang sau khi bo dau. Nen
chuoi dinh trong ten file KHONG khop truy van tieng Viet:

    tu("xuongkhop-bacsi-kham-lung") -> {xuongkhop, bacsi, kham, lung}
    tu("xương khớp bác sĩ khám lưng") -> {xuong, khop, bac, si, kham, lung}
                                          ^^ chi trung 'kham','lung'

Nen moi clip can mot `mo_ta` viet ROI, CO DAU. Ten file la thu duy nhat biet
clip quay gi (do nguoi nhin frame that roi dat, 05/08/2026) — bang nay dich
nguoc lai.

Tu nao khong co trong bang thi giu nguyen: van tot hon bo di.
"""

# tu viet tat -> tieng Viet co dau, tach tu
TU = {
    # --- nhom chu de (tien to dau ten file) ---
    "doan": "đồ ăn món ăn", "anlanh": "ăn uống lành mạnh thực phẩm",
    "theduc": "thể dục thể thao vận động", "xuongkhop": "xương khớp đau khớp",
    "khambenh": "khám bệnh bác sĩ bệnh viện", "vanphong": "dân văn phòng công sở",
    "noitang": "nội tạng", "giamcan": "giảm cân béo phì thừa cân",
    "tieuhoa": "tiêu hoá đường ruột dạ dày", "giadinh": "gia đình",
    "dilimquay": "DiLiM tự quay", "tocda": "tóc da làm đẹp",
    "biaruou": "bia rượu nhậu", "daudau": "đau đầu", "metmoi": "mệt mỏi",
    "dotquy": "đột quỵ", "xovua": "xơ vữa mảng bám", "machmau": "mạch máu",
    "matngu": "mất ngủ", "ngungon": "ngủ ngon", "chongmat": "chóng mặt",
    "momau": "mỡ máu", "cucmau": "cục máu đông", "thankinh": "thần kinh",
    "cothe": "cơ thể", "tebao": "tế bào", "phantu": "phân tử",
    "natto": "Nano Nattokinase", "rich": "Rich Coenzyme Q10",
    "richnatto": "combo hai hộp", "nano": "Nano", "sun": "sụn",
    "curcumin": "curcumin nghệ", "andu": "ẩn dụ ví von",

    # --- nguoi ---
    "nu": "nữ phụ nữ", "nam": "nam đàn ông", "ongcu": "ông cụ người lớn tuổi",
    "bacu": "bà cụ người lớn tuổi", "ongba": "ông bà người lớn tuổi",
    "be": "em bé trẻ con", "2be": "hai em bé", "tre": "trẻ con",
    "con": "con cái", "nhom": "nhóm nhiều người", "doi": "đôi hai người",
    "2nu": "hai nữ", "2nam": "hai nam", "2bacu": "hai bà cụ",
    "bacsi": "bác sĩ", "duocsi": "dược sĩ", "benhnhan": "bệnh nhân",
    "dieuduong": "điều dưỡng y tá", "adong": "châu Á", "trungnien": "trung niên",
    "sinhvien": "sinh viên", "nhanvien": "nhân viên", "su": "nhà sư",

    # --- hanh dong ---
    "an": "ăn", "uong": "uống", "uongnuoc": "uống nước", "ancom": "ăn cơm",
    "antao": "ăn táo", "anrau": "ăn rau", "ansalad": "ăn salad",
    "chay": "chạy", "chaybo": "chạy bộ", "dibo": "đi bộ", "leo": "leo",
    "ngoi": "ngồi", "nam2": "nằm", "guc": "gục xuống", "nga": "ngã",
    "om": "ôm", "omdau": "ôm đầu", "omgoi": "ôm gối", "omlung": "ôm lưng",
    "ombung": "ôm bụng", "omnguc": "ôm ngực", "omvai": "ôm vai",
    "omco": "ôm cổ", "xoa": "xoa bóp", "bop": "bóp", "bopmui": "bóp sống mũi",
    "bopbung": "bóp bụng", "bopcotay": "bóp cổ tay", "cham": "chạm",
    "cam": "cầm", "camhop": "cầm hộp", "lay": "lấy", "rot": "rót",
    "thai": "thái cắt", "bam": "băm", "nuong": "nướng", "chien": "chiên rán",
    "hap": "hấp", "kham": "khám", "tuvan": "tư vấn", "chiase": "chia sẻ",
    "vuonvai": "vươn vai", "xoay": "xoay", "gianco": "giãn cơ",
    "khoidong": "khởi động", "dapxe": "đạp xe", "boi": "bơi",
    "thien": "thiền định", "khicong": "khí công dưỡng sinh",
    "cuoi": "cười vui vẻ", "buon": "buồn", "nhau": "nhậu",
    "cungly": "cụng ly", "cungcoc": "cụng cốc", "do": "đỡ giúp",
    "dochop": "đọc hộp", "xemhop": "xem hộp", "duahop": "đưa hộp",
    "nhin": "nhìn", "nhintren": "nhìn từ trên", "hocbai": "học bài",
    "docsach": "đọc sách", "nauan": "nấu ăn", "donggoi": "đóng gói",
    "laumohoi": "lau mồ hôi", "ngap": "ngáp", "cuigap": "cúi gập",

    # --- bo phan co the ---
    "chan": "chân", "tay": "tay", "cotay": "cổ tay", "vai": "vai",
    "gay": "gáy", "lung": "lưng", "eo": "eo vòng eo", "bung": "bụng",
    "goi": "đầu gối", "co": "cổ", "mat": "mặt", "dau": "đầu",
    "tim": "tim", "gan": "gan", "phoi": "phổi", "than": "thận",
    "dady": "dạ dày", "ruot": "ruột", "longruot": "lòng ruột",
    "daitrang": "đại tràng", "cotsong": "cột sống", "dotsong": "đốt sống",
    "xuong": "xương", "xuongxop": "xương xốp loãng xương", "khophang": "khớp háng",
    "cobap": "cơ bắp", "co2": "cơ", "da": "da", "toc": "tóc",
    "nangtoc": "nang tóc chân tóc", "soitoc": "sợi tóc", "dadau": "da đầu",
    "mach": "mạch", "longmach": "lòng mạch", "hongcau": "hồng cầu",
    "mau": "máu", "banchan": "bàn chân", "bantay": "bàn tay",
    "cothe2": "cơ thể", "nguc": "ngực", "longnguc": "lồng ngực",

    # --- trieu chung / benh ---
    "hep": "hẹp tắc", "tac": "tắc nghẽn", "nhiemmo": "nhiễm mỡ",
    "mangbam": "mảng bám", "mo": "mỡ", "cucmaudong": "cục máu đông",
    "tebi": "tê bì", "runtay": "run tay", "nhanmat": "nhăn mặt đau",
    "met": "mệt", "chemat": "che mặt", "duimat": "dụi mắt",
    "onong": "ợ nóng", "ohoi": "ợ hơi", "tieuduong": "tiểu đường",
    "duonghuyet": "đường huyết", "vikhuan": "vi khuẩn", "loikhuan": "lợi khuẩn",
    "nepnhan": "nếp nhăn", "rung": "rụng", "bamtim": "bầm tím",
    "hauqua": "hậu quả", "dichung": "di chứng", "suynhuoc": "suy nhược",
    "tiendinh": "tiền đình", "hoathuyet": "hoạt huyết",

    # --- do vat / boi canh ---
    "ban": "bàn", "ghe": "ghế", "sofa": "ghế sofa", "giuong": "giường",
    "bep": "bếp", "phong": "phòng", "cuaso": "cửa sổ", "cua": "cửa",
    "tuong": "tường", "cauthang": "cầu thang", "lancan": "lan can",
    "duong": "đường", "pho": "phố", "vensong": "ven sông", "venho": "ven hồ",
    "venbien": "ven biển", "bobien": "bờ biển", "bien": "biển",
    "congvien": "công viên", "rung": "rừng", "nui": "núi", "co": "cỏ bãi cỏ",
    "baico": "bãi cỏ", "ngoaitroi": "ngoài trời", "trongnha": "trong nhà",
    "san": "sân", "gym": "phòng gym", "maychay": "máy chạy bộ",
    "xedaptap": "xe đạp tập", "daykhang": "dây kháng lực", "ta": "tạ",
    "tham": "thảm tập", "hoboi": "hồ bơi", "boncau": "bồn cầu nhà vệ sinh",
    "xelan": "xe lăn", "gay2": "gậy chống", "khungdi": "khung tập đi",
    "laptop": "máy tính laptop", "manhinh": "màn hình", "tablet": "máy tính bảng",
    "dienthoai": "điện thoại", "maytinh": "máy tính", "tainghe": "tai nghe",
    "hoso": "hồ sơ giấy tờ", "giay": "giấy", "vest": "vest công sở",
    "khan": "khăn", "ao": "áo", "quanrong": "quần rộng",
    "thuocdo": "thước dây", "can": "cân", "cannang": "cân nặng",
    "hop": "hộp sản phẩm", "2hop": "hai hộp", "lothuoc": "lọ thuốc",
    "vithuoc": "vỉ thuốc", "vien": "viên thuốc", "viennang": "viên nang",
    "thuoc": "thuốc", "ongmau": "ống máu xét nghiệm", "ongnghiem": "ống nghiệm",
    "xquang": "phim X-quang", "maylytam": "máy ly tâm", "pharmacy": "nhà thuốc",
    "thotgo": "thớt gỗ", "thot": "thớt", "dia": "đĩa", "bat": "bát",
    "chen": "chén", "ly": "ly cốc", "tach": "tách", "hu": "hũ",
    "khay": "khay", "thia": "thìa", "noi": "nồi", "chao": "chảo",
    "quay": "quầy", "cho": "chợ", "tulanh": "tủ lạnh", "logo": "logo",
    "khung": "khung hình", "sodo": "sơ đồ", "mohinh": "mô hình 3D",
    "dohoa": "đồ hoạ", "hoathinh": "hoạt hình", "anh": "ảnh tĩnh",
    "chu": "chữ", "disclaimer": "disclaimer",

    # --- thuc pham ---
    "rau": "rau", "raucu": "rau củ", "raucai": "rau cải", "raumuong": "rau muống",
    "cantay": "cần tây", "bongcai": "bông cải", "carot": "cà rốt",
    "traicay": "trái cây", "tao": "táo", "chuoi": "chuối", "bo": "quả bơ",
    "dau": "dâu", "vietquat": "việt quất", "cam": "cam", "chanh": "chanh",
    "khoailang": "khoai lang", "gao": "gạo", "gaolut": "gạo lứt",
    "com": "cơm", "comtrang": "cơm trắng", "yenmach": "yến mạch",
    "hat": "hạt", "hatchia": "hạt chia", "hatlanh": "hạt lanh",
    "macca": "hạt macca", "dauphu": "đậu phụ", "daunanh": "đậu nành",
    "ca": "cá", "cahoi": "cá hồi", "cangu": "cá ngừ", "ga": "gà",
    "thit": "thịt", "thitbo": "thịt bò", "thitnguoi": "thịt nguội",
    "trung": "trứng", "sua": "sữa", "suachua": "sữa chua", "phomai": "phô mai",
    "banh": "bánh", "banhmi": "bánh mì", "banhngot": "bánh ngọt",
    "burger": "burger", "pizza": "pizza", "donut": "bánh donut",
    "migoi": "mì gói", "mi": "mì", "lau": "lẩu", "canh": "canh",
    "salad": "salad", "sushi": "sushi", "sashimi": "sashimi",
    "caphe": "cà phê", "tra": "trà", "traxanh": "trà xanh", "matcha": "matcha",
    "duong": "đường", "dauan": "dầu ăn", "dauca": "dầu cá omega",
    "nghe": "nghệ", "gung": "gừng", "toi": "tỏi", "matong": "mật ong",
    "rongbien": "rong biển", "kimchi": "kim chi", "nuoc": "nước",
    "nuocngot": "nước ngọt", "nuocep": "nước ép", "trasua": "trà sữa",
    "whey": "whey protein", "mengaodo": "men gạo đỏ",
    "meninulin": "men Inulin", "dha": "DHA", "taodo": "tảo đỏ",
    "snack": "đồ ăn vặt", "lapxuong": "lạp xưởng", "xucxich": "xúc xích",

    # --- mo ta khac ---
    "canh2": "cận cảnh", "doc": "khung dọc", "nenden": "nền đen",
    "nenxanh": "nền xanh", "nentrang": "nền trắng", "nendo": "nền đỏ",
    "vang": "màu vàng", "xanh": "màu xanh", "do": "màu đỏ", "hong": "màu hồng",
    "trang": "màu trắng", "den": "màu đen", "toi": "tối",
    "sang": "sáng", "phatsang": "phát sáng", "hoanghon": "hoàng hôn",
    "dem": "ban đêm", "sauchay": "sau khi chạy", "sosanh": "so sánh",
    "truocsau": "trước sau", "lien": "liền", "day": "dày",
    "dong": "đống nhiều", "mieng": "miếng", "lat": "lát",
    "boidoi": "bổ đôi", "nai": "nải", "bo2": "bó",
    "vui": "vui vẻ", "hanhphuc": "hạnh phúc", "tiec": "tiệc",
    "nhieumon": "nhiều món", "buaan": "bữa ăn", "buacom": "bữa cơm",
    "antrua": "ăn trưa", "ansang": "ăn sáng", "andem": "ăn đêm",
    "hlv": "huấn luyện viên", "dongnghiep": "đồng nghiệp",
    "aplic": "áp lực", "stress": "căng thẳng stress", "deadline": "deadline",
    "3thehe": "ba thế hệ", "daigd": "đại gia đình", "3nguoi": "ba người",
    "khatthuc": "khất thực", "tinhtan": "tinh tấn",
    "pickleball": "pickleball", "tennis": "tennis", "karate": "võ karate",
    "dabong": "đá bóng", "vo": "võ", "plank": "plank", "yoga": "yoga",
    "squat": "squat", "plank2": "plank",

    # --- bo sung vong 2 (tu xuat hien >=2 lan con sot) ---
    "nao": "não", "treco": "trên cỏ", "bot": "bột", "ong": "ông",
    "khoi": "khối", "cau": "cầu", "dai": "dài", "may": "máy",
    "4k": "4K độ nét cao", "mangvang": "màng vàng", "cai": "cải",
    "bong": "bóng", "map": "mập béo", "luoc": "lược", "2tay": "hai tay",
    "dragon": "hiệu ứng", "studio": "studio", "chia": "chia",
    "mam": "mâm", "rotnuoc": "rót nước", "gang": "găng tay",
    "duongdo": "đường đất đỏ", "omtran": "ôm trán", "ngoiday": "ngồi dậy",
    "sot": "sốt", "so": "sờ", "coq10": "Coenzyme Q10",
    "hemach": "hệ mạch", "hinhthanh": "hình thành", "tacmach": "tắc mạch",
    "dna": "DNA", "catdoc": "cắt dọc", "soi": "soi", "bachcau": "bạch cầu",
    "nentoi": "nền tối", "hatvang": "hạt vàng", "giaiphau": "giải phẫu",
    "cautruc": "cấu trúc", "nhan": "nhân", "dantruyen": "dẫn truyền",
    "neuron": "nơ ron", "mangmo": "màng mỡ", "xerac": "xe rác",
    "cu": "củ", "atiso": "atisô", "rua": "rửa", "la": "lá",
    "daubap": "đậu bắp", "dat": "đất", "danh": "đánh",
    "damdong": "đám đông", "quan": "quán", "tren": "trên",
    "chitay": "chỉ tay", "balo": "ba lô", "chieucao": "chiều cao",
    "hanhlang": "hành lang", "cungnhau": "cùng nhau", "viet": "viết",
    "bungto": "bụng to", "aodo": "áo đỏ", "doeo": "đo vòng eo",
    "bopmo": "bóp mỡ", "anmi": "ăn mì", "ankieng": "ăn kiêng",
    "nghieng": "nghiêng", "phim": "phim chụp", "lo": "lọ",
    "thung": "thùng", "nho": "nhỏ", "chong": "chống",
    "lam": "làm việc", "tai": "tai", "trong": "trồng",
    "tongdai": "tổng đài", "vuontay": "vươn tay", "in": "in hình",
    "boc": "bóc", "nang": "nâng", "cotuoi": "người có tuổi",
    "duongmon": "đường mòn", "chantran": "chân trần", "aohong": "áo hồng",
    "tavai": "tạ vai", "diduong": "đi đường", "gheda": "ghế đá",
    "omchan": "ôm chân", "sofado": "ghế sofa đỏ", "gap": "gắp",
    "hopcom": "hộp cơm", "quandem": "quán đêm", "3d": "mô hình 3D",
    "vintuong": "vịn tường", "tuatuong": "tựa tường", "tachnen": "tách nền",
}


def mo_ta_tu_ten(ten_file):
    """`xuongkhop-bacsi-kham-lung-01.mp4` -> `xương khớp bác sĩ khám lưng`"""
    import os
    base = os.path.splitext(ten_file)[0]
    ra = []
    for s in base.split("-"):
        if s.isdigit():
            continue
        ra.append(TU.get(s, s))
    return " ".join(ra)
