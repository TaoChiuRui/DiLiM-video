# DiLiM AutoCut — v2.3

**Từ video thô ra project CapCut sửa được.** Không phải file render sẵn — mà là dự án đầy đủ track, mở lên chỉnh tiếp bằng tay.

Chốt ngày **03/08/2026** sau 2 video thật (`DSCF1553`, `Dilim Video test`, `DSCF0894`).

---

## Nó làm gì

Đưa vào một file quay thô. Nhận về một project CapCut có sẵn:

| Track | Nội dung |
|---|---|
| **A-roll** | đã cắt sạch vấp, lặp, ậm ừ — mối cắt trùng biên từ, fade âm 30ms |
| **B-roll** | dải trên đỉnh, mask `Split` + feather, tự chọn clip theo nội dung câu |
| **Caption** | PNG style DiLiM — font Anton, 3 họ màu, nhấn từ khoá, animation theo ý nghĩa |
| **SFX** | 1 tiếng động mỗi caption, pool chia theo nội dung, −16 dB |

Mỗi caption là **một layer riêng** — kéo, sửa, xoá từng cái. Không phải một khối phẳng.

## Con số của bản v1.0

Đo trên `DSCF0894` (3:13 thô → 2:58,8):

```
caption          49 PNG,  0,87 MB        ← so với nền xanh ~120 MB, alpha ~5 GB
B-roll           36 đoạn
SFX              45 cue
dựng draft       vài giây                ← so với ~20 phút render Remotion
sửa 1 chữ        vài giây                ← so với render lại 20–40 phút
```

## Ba quyết định làm nên bản này

**1. Caption là PNG, không phải video.** Engine của Tính vẽ sẵn từng caption ra ảnh trong suốt, 18 KB/cái. Nhẹ hơn nền xanh 158 lần, không phải key, mép chữ sạch, và sửa được từng caption trong CapCut.

**2. Bắt cue theo từ khoá, không ước lượng.** Đối chiếu chữ trong caption với chữ thật trong transcript, neo vào chữ đầu tiên, cho hiện sớm 0,5 giây. Trước khi có bước này, 39/49 caption lệch quá 0,4 giây.

**3. Nhúng media vào chính thư mục draft.** macOS chặn Desktop và ổ ngoài với app sandbox. Chép vào `~/Movies` (không bị chặn) thì CapCut mở thẳng, không hỏi link, và project tự đứng một mình — rút ổ T7 vẫn chạy.

## Lấy thông số từ anh Thành — cách duy nhất

**Không quy đổi từ panel CapCut.** Panel và file draft dùng hai đơn vị khác nhau, chỉ có
một mốc đối chiếu, nên quy đổi là đoán — và đã đoán sai một lần ở logo (v1.4 dùng bộ số
quy đổi, anh xem bảo *"hơi sai"*; v1.7 đọc lại từ draft anh kéo tay mới đúng).

Anh chỉnh tay trong CapCut xong, hỏi tên project rồi:

```bash
python3 03-tool-capcut/pipeline/doc_capcut.py --draft "DiLiM - <tên>" --track logo
```

Chép thẳng số nó in ra vào `6_to_capcut.py`. Dùng cho **mọi thông số vị trí**, không riêng
logo. Logo hiện đã chốt từ v1.7 (`scale 0.332886 · x −0.667114 · y 0.866834` + mask bo góc).

## Chạy

Bảng lệnh đầy đủ 13 bước: `README.md`. Cách dựng một video: skill `dilim-autocut`.

Mỗi job tự viết 2 file: `cuts.json` (đoạn nào bỏ) và `plan.py` (nội dung caption + chọn B-roll).

## Thông số đã chốt

```
dải B-roll   mask Split · width 0.28 · height 0.0
             centerX -0.107502 · centerY -0.705959 · feather 0.283066
             transform_y 0.6834 · scale 1.0
             ^ SO NAY DOI 2 LAN (v1.7, v1.9). Nguon dung duy nhat la
               MASK_* trong 6_to_capcut.py — doc o day thi doi chieu lai.
caption      transform_y 0.154523 · hiện sớm 0.5s trước chữ đầu
animation    warning -> Zoom_In 0.30s ·  còn lại -> Fade_In 0.25s
             không dài quá 1/3 caption. Bỏ hết kiểu trượt — tệp khách người có tuổi.
SFX          mỗi caption 1 cue · cách nhau tối thiểu 1.5s · −16 dB
             warning->CAMERA · positive/product->TING,BUTTON · còn lại->WHOOSE,POP,CLICKS
             8 giây đầu không dùng pool benefit
```

## Còn thiếu

*(soát lại 05/08/2026 — mục nào xong thì bỏ, mục nào xong một nửa thì thu hẹp lại)*

- **Nhạc nền** chưa làm — mới có SFX. `6_to_capcut.py` không có track nhạc.
- **Disclaimer** *"Sản phẩm này không phải là thuốc…"* — STYLE.md bắt buộc, vẫn **chưa tự
  chèn**. Có sẵn `05 Finish part/SP này k phải là thuốc.mp4` trên ổ T7. `soi_plan.py` chỉ
  báo khi anh CÓ nói mà caption sót, không tự thêm.
- **Regression check còn nửa vời.** `test_logic.py` (v2.1, 0 FAIL) kiểm **luật trên
  `plan.json`** — không dựng lại draft rồi so với bản đã duyệt. Nên sửa `6_to_capcut.py`
  vẫn không có gì bảo đảm job cũ ra y như cũ. Hôm nay vừa sửa `6_to_capcut.py` (kẹp đuôi)
  và phải mở `draft_info.json` đếm tay để kiểm.
- **Ẩn dụ — còn thiếu vế XẤU.** `ANDU_ONGNUOC` (ống nước chảy thông) và `ANDU_XERAC`
  (xe rác dọn rác) đã có. Vẫn chưa có: **ống nước TẮC / đóng cặn**, **máy bơm**,
  **vỉ thuốc**. Tra "đường ống bị tắc nghẽn cặn bám" hiện chỉ ra clip xơ vữa mạch máu —
  đúng chủ đề nhưng **sai ẩn dụ**: ví von cái gì thì phải quay cái đó, không quay cái được
  ví.
- **Chưa có clip "sống thiếu lành mạnh"** — ngồi lì không vận động, ăn uống thất thường.
  Job 07 có 2 dòng phải để trống vì kho chỉ có clip *mệt mỏi / đau đầu*, thả vào thì người
  xem đọc ra "đang bệnh" chứ không đọc ra "lười vận động".
- **`de_xuat_cat.py` gãy trên văn nói lặp tu từ** — xem v2.2. Chưa phân biệt được "lặp vì
  lỡ lời" với "lặp để nhấn".
- `plan.py` vẫn phải **viết tay nội dung caption** — máy chỉ chia được nhịp và đặt mốc.

**Đã xong, bỏ khỏi danh sách:**

- ~~Kho B-roll chưa chuẩn hoá~~ — thư mục mạch máu giờ **78/78 file có tên đọc hiểu**,
  không còn `Thiết kế chưa có tên`. (Thư mục `Thể dục thể thao` và `Ăn uống lành mạnh`
  thì vẫn tên gốc, nhưng 21 clip cần dùng đã khai vào `clips.py` kèm mô tả — xem v2.2.)
- ~~Vị trí logo chưa đúng ý~~ — chốt từ v1.7 bằng `doc_capcut.py`.

## Lịch sử

### Đã thử và BỎ (05/08/2026 tối): điền sẵn caption từ kho

Ý tưởng: nhịp nào khớp cụm trong `kho_caption.json` thì điền thẳng chữ + màu vào
khung `plan.py` (thay vì in comment), biến "viết" thành "duyệt". Backtest leave-one-out
trên 7 job (đã vá rò rỉ cặp `06`/`06b` — `bo_job` cũ chỉ bỏ cụm có ĐÚNG MỘT job,
cụm nằm trong cả bản sao thì tự khớp chính mình):

| ngưỡng | dùng ≥ | điền | TRÚNG bản cuối | SAI | chính xác |
|---|---|---|---|---|---|
| 0.75 | 1 lần | 122 | 38 | 84 | 31% |
| 1.0 | 2 lần | 31 | 17 | 14 | **54%** |

Kể cả gate chặt nhất cũng **sai gần một nửa**, mà điền sai ĐẮT hơn để trống:
khung mặc định chứa lời nói thật (nguyên liệu để cô đọng) — điền đè lên là mất nó,
và nếu không phát hiện thì caption sai đi thẳng vào bản dựng.

**Vì sao hỏng có tính cấu trúc, không phải chỉnh ngưỡng được:** (1) cùng một ý nhưng
mỗi bài diễn đạt khác — kho có `LÀM HẸP MẠCH MÁU`, bản cuối là `LÀM TẮC, LÀM BÍT,
LÀM NGHẼN`; (2) ranh nhịp mỗi bài chia khác, caption cuối phủ nhiều/ít lời nói hơn
cụm lưu trong kho.

**Giữ nguyên version cũ** (gợi ý bằng comment `# KHO`). Giá trị thật của kho nằm ở:
từ điển whisper (tự sửa 16% dòng), cờ `[CO CHU SO — KIEM TAY]`, và tính tự dày
theo họ kịch bản — video Thịnh #2 sẽ trúng cao hơn hẳn vì job 07 đã vào kho.

**v2.3 — 05/08/2026 (chiều).** Soát cả luồng để **đóng gói cho máy khác**. Viết `CAI-DAT.md`
ở gốc repo — cần gì, mang gì, kiểm bằng 4 lệnh.

### `--job` từng có HAI khuôn, không ai ghi ra giấy

13 script nhận **đường dẫn** (`04-du-an/<tên>`), 5 script nhận **tên trần** (`<tên>`). Đưa nhầm
thì báo `thieu --job` hoặc `khong thay thu muc job` — cả hai đều **không gợi ý là sai DẠNG**.
Tôi vấp đúng chỗ này khi dựng job 07, và `de_xuat_cat.py` thì docstring ghi một dạng còn code
đọc dạng khác.

Gom về một bộ giải duy nhất `pipeline/job_path.py`. Giờ mọi script nhận **cả 4 dạng**: đường
dẫn tương đối · tuyệt đối · tên thư mục trần · một mảnh tên (miễn duy nhất). Không tìm thấy
thì in ra **đã thử những đường nào**; khớp nhiều job thì liệt kê ra để chọn lại.

### `--help` chết ở 7 script

Khuôn `_job_dir()` dùng `ArgumentParser(add_help=False)` + `required=True` ở mức module, nên
`--help` không bao giờ chạy tới — người mới không có cách nào hỏi script cần gì. Giờ 31/32
script chạy `--help` được (`6_to_capcut.py` vẫn phải dùng venv, đúng như tài liệu).

### `1_transcribe.py` ghi cứng `~/.local/bin/mlx_whisper`

Máy khác không có thì chết bằng `FileNotFoundError` trần, **không nói thiếu cái gì**. Giờ dò
theo `MLX_WHISPER` → `PATH` → chỗ quen, không thấy thì báo rõ cách cài.

Ghi thẳng vào code cái điều trước giờ chỉ nằm trong đầu: **MLX chỉ chạy trên Mac Apple Silicon.**
Các bước sau không quan tâm engine nào, chúng chỉ cần JSON có `segments[].words[].start`.

### `clips.py` — kho B-roll đọc từ `DILIM_FOOTAGE`

Ghi cứng `/Volumes/T7 for Mac` thì máy khác, hay ổ mount tên khác, là chết.

**Và vá luôn một lỗi tự tay tôi tạo ra khi sửa chỗ này:** vòng tự kiểm lọc hằng số bằng
`v.startswith("/Volumes")` — cũng ghi cứng. Đổi biến xong thì không hằng số nào lọt lưới, nó in
`0 co / 0 mat`. Máy mới nhìn vào **tưởng xong, thật ra chưa soi gì cả** — đúng loại báo xanh giả
nguy hiểm nhất. Giờ lọc theo chính `B`, và thiếu gốc kho thì dừng hẳn kèm cách sửa.

### Regression: lỗi đuôi B-roll có ở **5/7 job đã giao**, không riêng job 07

Đo `plan.json` với độ dài A-roll thật trên cả 9 job:

| Job | plan hết | A-roll | thừa |
|---|---:|---:|---:|
| `03-dscf0894` | 179.64 | 178.82 | **+0.82s** |
| `04-img1770` | 223.46 | 222.32 | **+1.14s** |
| `05-natto` | 273.21 | 272.14 | **+1.07s** |
| `06-magie` | 390.06 | 389.32 | **+0.74s** |
| `07-dji0485` | 163.60 | 163.08 | **+0.52s** |

Anh Thành bắt được ở job 07, nhưng nó nằm im trong gần như mọi bản đã giao. Dựng lại 4 job với
bản vá: **rc=0 cả 4, clamp xén đúng 1 caption cuối mỗi job, không bỏ dòng nào.**

**Còn nợ:** đây vẫn là regression chạy tay. Chưa có gì tự so bản dựng lại với bản đã duyệt.

**v2.2 — 05/08/2026 (trưa).** Dựng job `07-2026-08-03-dji0485` (bài "Thịnh không cam kết",
3:06 → 2:43). Ba lỗi thật lộ ra khi làm, đều đã vá.

### Anh Thành bắt: **A-roll hết là B-roll phải hết luôn**

*"đoạn kết, b-roll dư ra so với a-roll… về sau a-roll hết là b-roll phải hết luôn"*.

`plan_build.py` kéo caption cuối tới `t + thời lượng ước lượng`, nó **không biết A-roll dài
bao nhiêu**. Job 07 lệch 0.52s → nửa giây cuối chỉ còn dải B-roll trôi trên nền trống,
nhìn như lỗi render.

Vá ở `6_to_capcut.py` chứ **không** ở `plan_build.py`: chỉ đến bước dựng draft mới biết độ
dài THẬT của A-roll (tổng các đoạn `keeps`, sau khi từng mốc đã làm tròn về frame). Kẹp
`t_end` của mọi track phủ trên — B-roll, caption, SFX, logo — và bỏ hẳn caption nào bắt
đầu sau khi A-roll đã hết. In ra rõ đã xén dòng nào.

Kiểm lại draft job 07: cả 5 track kết đúng 162.740s.

### `2_cut.py` hardcode `source.MOV`

Job này quay bằng DJI, nguồn là `.MP4` → chết ngay bước ③ với `ValueError` khó đoán
(`could not convert string to float: ''`). Ba script khác đã có sẵn danh sách fallback
`source.mp4 / .MOV / .mov`, riêng `2_cut.py` bị bỏ sót. Mọi job trước đều là `.MOV` nên
lỗi nằm im.

### Khai 21 clip **thể dục / thiền / ăn uống** — 166 → 187

Bài này nói *"thể dục thể thao"* 6 lần, *"ăn uống điều độ / thanh đạm"* 4 lần,
*"thiền định"* 3 lần. Cả ba nhóm nằm trong hai thư mục `Thể dục thể thao` +
`Ăn uống lành mạnh` mà **chưa clip nào được khai** — nên `goi_y_broll` trả về toàn clip
mạch máu lệch ý dù báo "100% dòng có gợi ý".

Soi frame 3 mốc (5%/40%/75%) trên **209 clip ngang**, chọn 21. Ưu tiên clip có người lớn
tuổi. Thêm 3 họ chống lặp: `the_duc`, `thien`, `an_lanh`.

Bắt được 1 clip **đổi cảnh giữa chừng**: `download (20).mp4` là bà cụ tập dây kháng lực,
nhưng giây 25 nhảy sang phụ nữ trẻ trong phòng gym → loại, ghi lý do vào comment.

### Giới hạn đã biết: `de_xuat_cat.py` gãy trên văn nói lặp tu từ

Anh Thịnh lặp có chủ ý (*"vẫn còn… vẫn còn… vẫn còn"*, danh sách triệu chứng nhắc 3 lần).
Luật R4 "take lặp" đọc ra là quay lại nhiều lần, đề xuất bỏ **78.2s/188s — trong đó có cả
hook 29 giây**. Phải viết `cuts.json` tay hoàn toàn.

Chưa vá: chưa biết cách phân biệt "lặp vì lỡ lời" với "lặp để nhấn" bằng luật. Trước mắt
**đọc kỹ đề xuất R4 trước khi ghi**, đừng chạy `--ghi` thẳng trên bài nhiều điệp ngữ.

**v2.1 — 05/08/2026 (rạng sáng).** Ổ T7 nối lại được → **hoàn thành kho index B-roll**.

### Kho B-roll: 159 mục, 145 clip video đều có mô tả

Ba tầng đã đủ. Tầng 1–2 máy tự làm (OCR + độ sáng), tầng 3 tôi nhìn 145 frame thật.

**Bốn lần bắt được lỗi của chính mình khi đo lại:**

1. **Lọc watermark bằng regex → hỏng.** Vision đọc logo "Helix Animation" mỗi frame một
   kiểu (`Helis`, `Heliy`, `Helz`, `ANINATIO`). **Sửa: lọc bằng TẦN SUẤT** — chữ có mặt
   ≥35% frame là watermark đứng yên; kèm gom cụm gần giống.
2. **Dùng độ sáng trung bình → cấm oan clip nền tối.** `tim-dap-nento` bị cấm 20/20 giây,
   `tebao-cautruc` 13.4/13.4 — đều là clip dùng tốt từ lâu. Đo lại: khung đen thật có
   **p95 = 3**, còn nền tối chủ đề sáng có **p95 = 43–152**. Trung bình thì gần nhau,
   p95 cách nhau 14 lần. **Sửa: dùng phân vị 95.**
3. **Cấm oan clip sản phẩm.** Chữ `NANO ナットウキナーゼ PREMIUM` in trên vỏ hộp chính là
   thứ cần khoe, OCR đọc thành "chữ cháy vào hình" → 8 dòng job 06 bị báo sai.
4. **Vùng cấm 0.2 giây** — nhịp nhấp nháy của animation, không phải fade đen.

Kết quả: 5/145 clip thật sự có chữ tiếng Anh cháy vào hình. `soi_plan.py` giờ đọc kho này
thay cho bảng tay 4 clip.

### `goi_y_broll.py` — và con số thật

| | v1 (`suggest_clips`) | v2 |
|---|---|---|
| dòng có gợi ý | 62% | **98%** |
| gợi ý kèm `src_start` an toàn | không | **có** |
| gợi ý số 1 trúng | — | **14%** |
| trúng trong top 3 | — | **43%** |

**Đo lần đầu ra 95% — sai, vì rò rỉ.** Từ khoá học được lấy từ *mọi* job kể cả job đang
chấm, nên nó nhớ bài. Loại chính job đó ra thì còn **11% top-1 / 29% top-3**. Thêm tầng
mô tả nâng lên **14% / 43%**.

Thử thêm lời nói vào truy vấn: **tệ đi** (43% → 32%) — lời nói đầy từ đệm làm loãng tín
hiệu. Giữ nguyên cách tra bằng caption.

**Nói thẳng:** tra bằng chữ không thay được mắt. 43% nghĩa là hơn một nửa số dòng vẫn
phải tự tìm. Giá trị chắc chắn của kho là **`src_start` an toàn** — xoá hẳn họ lỗi 16 chỗ.

### `test_logic.py` — bộ test nằm trong repo

7 nhóm kiểm, chạy 4 giây, hiện **0 FAIL**.

**v2.0 — 04/08/2026 (đêm, chạy tự chủ).** Anh Thành giao tự làm qua đêm: *"tự làm tự chạy
tự test, tự backtest, tự lưu version tự ra quyết định"*. **Ổ T7 hỏng giữa chừng** nên phần
B-roll dở dang — xem `DOC-NGAY-SANG-MAI.md` ở gốc repo.

### Thước đo mới: `backtest.py` — chấm trên bản anh đã chốt

Mọi con số trước đây (32% trúng kho, 70% neo đúng, 0% cắt giữa cụm) đều đo **trên chính
dữ liệu tôi tạo ra** — chúng nói "tốt lên bao nhiêu so với chính nó", không nói "đúng bao
nhiêu so với ý anh". Draft anh sửa tay trong CapCut mới là chuẩn độc lập.

| Job | Cắt | Caption | B-roll |
|---|---|---|---|
| `06-magie` (bản anh dựng chuẩn) | **61%** | **93%** | **73%** |
| `05-natto` | — | 97% | 87% |

### `xay_kho_broll.py` — index theo ĐOẠN, không theo file

OCR từng frame bằng **macOS Vision** (`swiftc` biên dịch sẵn, 50ms/frame, không cài gì).
Đối chiếu: **tái tạo đúng bảng `VUNG_CAM` tôi làm tay**, và bắt thêm 2 chỗ tôi soi sót —
`cucmau-tacmach` có chữ ở giây 12–22.6, `xovua-mohinh-mach` có chữ từ 30.1 (tôi ghi 38).

Hai lần làm hỏng trước khi làm đúng:
1. Lọc watermark bằng regex `helix|animation` → Vision đọc logo ra `Helis`, `Heliy`,
   `Helz`, `ANINATIO` mỗi frame một kiểu, regex trượt hết, vùng cấm phình từ 4 khoảng
   thành một khối 12.3–43.0s. **Sửa: lọc bằng TẦN SUẤT** — chữ có mặt ≥35% frame là
   watermark (đứng yên), chữ chỉ có ở vài frame mới là chữ thật. Kèm gom cụm gần giống
   vì OCR đọc sai mỗi lần một kiểu.
2. Chỉ dùng `blackdetect` → bỏ sót khung tối mờ (giây 0 của `cucmau-tacmach` sáng trung
   bình 1.39/255 mà `blackdetect` chỉ thấy 0.2 giây). **Sửa: đo độ sáng từng frame lấy mẫu.**

Chạy được **41/166 clip** thì ổ hỏng. Resume được.

### `de_xuat_cat.py` — tự đề xuất `cuts.json`

Đánh vào khâu tệ nhất (cắt 61%). 5 luật máy làm được: khoảng lặng ≥1.5s (đo RMS thật,
không tin `end` của whisper) · tiếng đệm đứng một mình · vấp lặp chữ · take lặp · nối treo.

Đo trên `06-magie`, ba vòng sửa: **25% → 33% → 41%** (nới dung sai lên 1.5s thì 75%).

- +8 điểm: **snap mốc về đầu cụm** — 6/9 chỗ trượt đều muộn hơn anh 2.0–3.0s, đúng bệnh
  đã gặp ở caption. Cùng một gốc: mốc rơi giữa cụm.
- +8 điểm: **chặn gộp quá tay** — hai cặp lặp kề nhau bị gộp thành mảng 23 giây, nuốt
  luôn mốc anh giữ ở giữa. Cắt thừa tệ hơn cắt thiếu.

### `hoc_lich_su.py` — backlink / frontlink / tần suất

Học **341 từ khoá** từ 381 dòng đã dựng (so với TAGS gõ tay ~157 clip × 3–5 từ).
Thêm `con_lai_sau_khi_anh_sua` — số lần một clip **sống sót** qua bản dựng cuối của anh.
Đó là phiếu bầu thật, khác hẳn từ khoá tôi tự gõ.

### `chay_het.py` — chạy chuỗi, phiên âm SONG SONG

Phiên âm chiếm ~40% thời gian và là bước duy nhất vừa lâu vừa không cần người. Tối 04/08
tôi khởi động job 2 **muộn 8 phút** vì làm tuần tự. Kèm **chốt chặn T7**: bước nào cần ổ
mà ổ không đọc được thì dừng, không chạy tiếp để B-roll hỏng âm thầm.

### `soi_plan.py` — hai chốt mới

- **Đọc `clips.VUNG_CAM` / `MIN_START`.** Bảng có sẵn từ trước, comment ghi thẳng
  *"chưa script nào đọc nó"*. Chạy thử: **16 dòng ở 5 job** đang hiện chữ tiếng Anh/màn đen.
- **Disclaimer** — sửa theo anh chặn lại: *"thêm hay bỏ là do tôi"*. Giờ chỉ báo khi
  **anh có nói mà caption sót** (đúng lỗi job 06), anh không nói thì máy im.

**v1.10 — 04/08/2026 (khuya).** Chạy **test giả lập logic** trên toàn bộ 7 job / 381 dòng
caption (3.2 giây, không đụng CapCut). Bắt được **28 lỗi thật trong 5 bản đã giao**.

| Loại lỗi | Số dòng | Ghi chú |
|---|---|---|
| `src_start` đâm **vùng cấm** (chữ tiếng Anh / màn đen) | 16 | `VUNG_CAM` có sẵn nhưng **chưa script nào đọc** |
| **Thiếu disclaimer** bắt buộc | 5 job | chỉ 2 job dựng tối nay là đủ |
| clip ngắn hơn caption → hụt hình | 5 | |

- `soi_plan.py` giờ **đọc `clips.VUNG_CAM` và `clips.MIN_START`**. Bảng này tồn tại từ
  trước, comment ghi thẳng *"chua script nao doc no"* — nên nó chỉ là ghi chú cho người,
  và người thì quên. 16 dòng ở 5 job đang hiện chữ `PLATELET` / `RED BLOOD CELL` /
  `Buildup of plaque…` hoặc màn đen trên dải B-roll.
- Test tự nó cũng lộ một **báo xanh giả**: lần chạy đầu tôi đọc `soi()` như tuple trong
  khi nó trả về dict → mọi job đều "0 lỗi". Sửa xong mới ra 5 job thiếu disclaimer.

**v1.9 — 04/08/2026 (tối).** Học từ **bản dựng chuẩn** của anh Thành
(`06-magie-canxi-combo-2`) — anh chốt *"cái magie là 1 cái tôi dựng khá chuẩn, vào học"*.

**Số đọc thẳng từ draft anh đã kéo tay:**

- **Mask dải B-roll bị đặt thấp quá, lộ viền.** `centerY −0.842027 → −0.705959`
  (kèm `centerX −0.107572 → −0.107502`). Số cũ dùng suốt 6 job đều lộ viền dưới.
- **Normalize loudness cho A-roll.** Mỗi đoạn A-roll một material `loudness` riêng:
  `enable: true, target_loudness: −14.0`. Cờ toàn cục `normalize_loudness` **vẫn là
  false** — đây là thiết lập theo TỪNG ĐOẠN, không phải công tắc chung. Thư viện không
  có API, nhét thẳng vào JSON ở bước hậu kỳ.
- **Giá viết dạng `31.080K`, không viết bằng chữ.** Xem `references/viet-plan.md`.

**Bộ luật cắt A-roll — chỗ học được nhiều nhất.** Tôi cắt 448.3s → 389.2s (bỏ 13.2%).
Anh cắt thêm **16.0 giây ở 7 chỗ** → 373.2s (bỏ 16.8%). Bảy chỗ đó là bảy loại tôi bỏ sót:

| Anh cắt | Tôi sai ở chỗ |
|---|---|
| khoảng lặng **1.57s** | tôi chỉ cắt ≥2.2s — ngưỡng đúng là **~1.5s** |
| *"Vâng."* | tôi nhìn thấy rồi vẫn để lại |
| *"…một câu là anh chị tự hỏi mình. Thành"* | câu dẫn **bỏ lửng** — luật cũ của tôi chỉ cắt khi CÓ take sau thay thế |
| *"Nó không có đá nhau"* | nói lại cùng ý bằng giọng suồng sã hơn → giữ bản rõ. **Ngược** với luật giữ-take-sau |
| *"ấy, người trung niên mà, mà người"* | vấp **trong lòng** một đoạn đang giữ — dò lặp của tôi chỉ chạy ở mức take |
| *"Nên anh chị muốn"* ở đầu đoạn | chữ nối treo lơ lửng đầu đoạn giữ → xén |
| 6 caption tương ứng | cắt A-roll ở đâu thì caption ở đó phải chết theo |

Chép thành `references/cat-aroll.md` trong skill, kèm lệnh liệt kê khoảng lặng ≥1.5s.

Anh cũng **ripple-delete đúng cách**: caption dịch trái luỹ tiến −4.25s → −16.00s, track
A-roll không có lỗ hổng nào. *(Không dựng lại — anh đã dựng xong bản của anh.)*

**v1.8 — 04/08/2026 (tối).** **Caption bám nhịp nói — dùng DẤU CÂU.**

Anh Thành: *"text ở 2:53 2:54 nó bị lệch nhịp nói… kiểu text bị kéo ở đuôi chữ phát âm
đoạn sau chứ không phải phát âm đoạn đầu"*, và anh tự đoán hai nguyên nhân:
*"1 là timestamp của bạn bắt chưa sát đầu câu, 2 là bạn phân biệt chưa đủ đầu câu"*.
**Đo ra thì cả hai đều đúng.**

Whisper **có** trả về dấu câu, gắn liền vào chữ (`' không?'`, `' nhá,'`, `' bệnh.'`), và nó
sống sót tới tận `words_cut.json` — job 06 có **202/1276 chữ** mang dấu. Nhưng
`4_anchor.norm()` xoá sạch bằng `re.sub(r"[^a-z0-9]", "")`, nên **bước neo chưa từng
nhìn thấy một dấu phẩy nào**.

| | Trước | Sau |
|---|---|---|
| nhịp caption bắt đầu đúng đầu cụm (`group`) | 27% | **67%** |
| mốc neo rơi vào chữ mở đầu cụm (`4_anchor`) | 44% | **70%** |

- `group()` — đã có từ v1.7 qua `ngat_cum.diem_ranh`; job 06 dựng trước nên chưa hưởng.
- `4_anchor.snap_dau_cum()` — neo đang ở giữa cụm thì **nhích về chữ mở đầu cụm gần nhất**.
- Vá luôn lỗi cũ: nhánh dò lại chỉ quét **về phía sau** (`range(best[1], best[1]+12)`),
  không bao giờ lùi — nên mỗi lần trượt là trượt **muộn**, lệch một chiều. Giờ quét hai chiều.

**Hai lần làm hỏng trước khi làm đúng — ghi lại để đừng lặp:**

1. Cộng `+0.12` cho chữ đầu cụm thẳng vào `score`. Hỏng: chữ khớp kém nhưng đứng đầu cụm
   thắng ngược — `LO CÁI ĐƯỜNG ỐNG` nhảy từ `'lo'` sang `'đi'` (−3.8s), số caption neo được
   tụt 95→91.
2. Cho ưu tiên đầu cụm chạy trên **toàn cửa sổ tìm kiếm**. Hỏng y hệt: neo bị kéo lùi
   nhiều giây sang **câu khác**.

Cách đúng là **nhích CỤC BỘ**: tối đa 3 chữ / 0.7 giây. Ngoài ngưỡng đó thì cái "đầu cụm"
gần nhất thường thuộc một câu khác. Kết quả: 26/98 caption nhích, **lệch lớn nhất 0.68s**.

*(Không dựng lại job 06 — anh chốt "không cần chạy lại, chỉ cần learn là được".)*

**v1.7 — 04/08/2026 (tối, sau vòng duyệt đầu của anh Thành).** Sáu góp ý, áp lên
`06-magie-canxi-combo-2`. `05-natto-hoat-huyet` giữ nguyên vì anh đang sửa dở trong đó.

- **A-roll giờ là NHIỀU ĐOẠN thả từ file nguồn**, không còn một cục `final.mp4`.
  Anh: *"cho hẳn vào timeline cut rồi tôi dễ dàng kéo thả chỉnh sửa thì tiện cho tôi hơn"*.
  Lợi thêm: không encode lại (giữ nguyên HEVC, bớt ~1 phút/video), và phần bị bỏ vẫn nằm
  trong nguồn để kéo ra lại. Danh sách đoạn lấy sẵn từ `edl.json`.
  `Video_segment` của thư viện **không có API fade** — phải tự tạo `Audio_fade` rồi nhét
  `fade_id` vào `extra_material_refs`, giữ nguyên 30ms chống tiếng "bụp" của `2_cut.py`.
  **Đánh đổi:** caption neo theo dòng thời gian sau khi cắt — anh kéo mối cắt thì chữ
  không tự chạy theo.
- **Logo — đọc số thật từ draft anh đã kéo tay.** `scale 0.332886 · x −0.667114 ·
  y 0.866834` (số cũ tôi tự quy đổi từ panel: `0.37 / −0.694444 / 0.931771` — sai).
  Anh còn đặt **MASK Rectangle bo góc** cho logo: `width 0.814261 · height 0.466553 ·
  roundCorner 0.5065625 · feather 0 · tâm 0,0`. `add_mask` nhận feather/round_corner theo
  thang 0–100 rồi tự chia 100 → phải truyền `round_corner=50.65625`.
  **Ba bẫy gỡ được ở đây:**
  1. `doc_capcut.py --track logo` không thấy gì vì **CapCut xoá tên track khi lưu lại**.
     Phải dò theo tên file material.
  2. Lần đầu đọc tôi chỉ lấy `clip` nên **bỏ sót mask** — mask nằm ở `extra_material_refs`,
     phải tra ngược sang `materials.common_mask`.
  3. **Vòng patch cuối `6_to_capcut.py` ghi đè số của MỌI mask** bằng số dải B-roll. Viết
     từ hồi chỉ B-roll có mask nên không sao; vừa thêm mask logo là nó đè luôn — logo ra
     mask hình Split (width 0.28, tâm lệch xuống −0.842). Giờ chỉ patch mask tên `Split`.
- **Không có gì lệch ở dải B-roll.** Draft hiện `feather 0.532039` trong khi code truyền
  `0.283066` — đó là **CapCut tự chuẩn hoá khi lưu**, không phải anh sửa (bản tôi vừa ghi
  ra cũng 0.283066, bản CapCut lưu lại thành 0.532039). Tương tự, trường `expansion` là do
  CapCut thêm vào, thư viện không bao giờ ghi.
- **SFX bỏ `click_bell*` và `BuzzerButton`** (anh: *"nghe khó chịu quá"*). Bẫy:
  `click_bell1_*.wav` nằm **ngay trong thư mục TING** (5/8 file) nên bỏ thư mục BUTTON
  thôi là chưa đủ — phải lọc theo tên file (`sfx.BO_FILE`). Pool tích cực còn 3 tiếng ting.
- **`soi_plan.py` kiểm DISCLAIMER.** Job 06 đã đi thiếu vế *"sản phẩm này không phải là
  thuốc"* — tiếng nói còn đủ, chỉ caption sót, và không ai bắt được vì máy không kiểm.
  Giờ thiếu vế nào là báo **LỖI**.
- **`ngat_cum.py` — ngắt caption theo CỤM NGHĨA.** Anh: *"ghép caption kiểu theo cụm thôi,
  đừng làm word by word"*. Bản cũ cắt `len(ws)//2`; đo trên 369 dòng thật thì **40% mối
  chia rơi vào giữa cụm** (`MÁU CÓ THỂ LƯU | THÔNG DỄ DÀNG HƠN`). Bản mới **0%**.
  Ba luật nặng dần: không tách cụm ghép (−8) · không để từ dính treo cuối dòng (−5) ·
  nên cắt trước từ mở cụm (+1). Ăn vào cả `two_lines` lẫn chỗ chia nhịp của `group()`.
- **Caption bắt Ý, không bắt chữ.** Anh: *"đừng bắt full chữ, mà bắt ý chính, ngắn gọn dễ
  hiểu đủ ý — không cần full chữ như subtitle đâu"*.
  **Giới hạn phải biết:** cô đọng xa quá thì `4_anchor.py` mất chỗ bám — 2 dòng trong job
  06 không neo được vì tôi viết chữ anh không hề nói (`CHỖ NÀY QUAN TRỌNG`). Luật:
  **cô đọng thoải mái, nhưng chừa lại ít nhất một từ khoá anh thật sự nói.**

**v1.6 — 04/08/2026 (tối).** **Kho caption** — cụm nào viết rồi thì khỏi viết lại.

Anh Thành làm ngách hẹp nên nhiều đoạn lặp. Đo trên 381 dòng của 7 job trước khi viết:

| Cách tra | Trúng |
|---|---|
| theo **caption đã cô đọng** | 12–19% |
| theo **cả câu lời nói** | **1%** |
| theo **cụm** (cách đã chọn) | **28%** |

Mỗi lần anh nói một khác — dài ngắn khác, từ đệm khác, ranh caption máy chia cũng rơi
chỗ khác — nên so nguyên câu gần như không bao giờ khớp. Nhưng ý thì lặp thật: **124 cụm
5 từ có mặt ở ≥2 job**, riêng *"để lại tên và số điện thoại"* có ở **6/7 job**.

- `kho_caption.py --gom` quét mọi `plan.json` → `kho_caption.json` (354 cụm).
  `--tra "<câu>"` tra lẻ. `--thong-ke` xem cụm nào dùng nhiều.
- `tu_dien_whisper.json` — **hai mức, cố ý khác nhau**:
  `chac_chan` (32 cụm) **tự động sửa**, chỉ chứa từ không tồn tại trong tiếng Việt
  (`sơ vữa`, `chết xuất`, `bất ngủ`, `frevin`) nên sửa nhầm là không thể ·
  `can_kiem` (8 cụm) **chỉ cảnh báo**, là từ có thật nhưng ở đây chắc là nghe nhầm
  (`biết tay`→`đứt tay`, `lau cầu thang`→`leo cầu thang`). Từ điển sửa được **16%** số dòng.
- `make_plan_draft.py` tự áp từ điển và in gợi ý thành comment `# KHO` / `# NGO`.

**Ba chỗ cố ý KHÔNG tự động:**

1. **Không tự điền clip.** Trong 22 cụm chữ trùng nhau, variant giống 21/22 nhưng
   **clip chỉ giống 16/22** — cùng một câu ở hai bài cần hai hình khác nhau.
2. **Dòng có chữ số bị đánh dấu `[CO CHU SO — KIEM TAY]`.** Kho hiện đang giữ cụm
   *"HOẶC GỌI HOTLINE / 0862 188 681"* — **số cũ**, khác số đang dùng (0862 745 495).
   Đúng loại bẫy: 04/08 anh đọc giá sai (28tr790) rồi nói lại (31tr080) trong cùng một bài.
3. **`tra(bo_job=…)`** — dựng lại khung cho job đã có trong kho thì phải loại nó ra,
   không nó khớp chính nó, điểm 1.0, vô nghĩa.

Trúng nhiều hay ít tuỳ **cùng họ kịch bản hay không**: job `04-img1773` trúng 47%, còn
job `06-magie-canxi` chỉ 5% vì là kịch bản mới hoàn toàn. Kho càng dùng càng dày.

**v1.5 — 04/08/2026 (chiều).** Hai job đầu tiên phải **ghép nhiều file quay rồi mới cắt**
(`05 natto-hoat-huyet`: 2 file · `06 magie-canxi-combo-2`: 3 file). Vá 3 lỗi lộ ra khi làm.

- **`4b_vary.py` đang phá luật 1 của anh Thành.** Bước chống lặp thấy hai caption liền nhau
  dùng cùng clip là "lặp sau 4 giây" rồi đổi mất một cái — trong khi `6_to_capcut.py`
  đang cố **gộp đúng hai cái đó** thành một dải chạy liền mạch. Thêm ngoại lệ: nếu lần
  dùng trước là caption ngay liền trước thì để yên. Thêm ngoại lệ thứ hai: **miễn trừ họ
  `san_pham`** (`chon-broll.md` đã ghi luật này từ 03/08, code chưa bao giờ cài). Không có
  nó thì giữa đoạn báo giá 6 hộp Natto nó xoay trúng `richnatto-01.mp4` — hai hộp, sai bài.
- **`MIN_START[XO_VUA_MODEL] = 6.0` là số SAI.** Nhìn frame thật ở giây 6 vẫn còn nguyên câu
  *"Buildup of plaque in the arteries can lead to peripheral arterial disease (PAD)."*
  Chữ chạy tới ~8s, và **cuối clip (giây 40, 50) còn hai đoạn chữ nữa** mà không bảng nào
  ghi. Sửa thành 9.0 và thêm `VUNG_CAM[XO_VUA_MODEL]` — dùng được 9–38s.
- **`MACH_TAC` thiếu `MIN_START`.** Giây 0–3 gần như đen + logo Helix. `4b_vary.py` khi đổi
  clip sang đây lấy `MIN_START` làm `src_start`, không có số thì ra 3 giây hình đen giữa
  bài. Đặt 4.0.

Kinh nghiệm: **soi frame trước khi chốt `src_start`** bắt được cả 3 lỗi trên trong ~10 phút.
Ba lỗi này đều thuộc loại "chạy vẫn ra file, xem mới biết sai".

**v1.4 — 04/08/2026.** Tách phần **soi** ra khỏi phần **dựng**. Thêm logo.

- **LOGO** — mọi job đều có, track riêng trên caption, trải suốt bài. Số anh Thành chốt: `scale 37%`, UI `X=-750 Y=1789` → `transform_x=-0.694444 transform_y=0.931771` (quy đổi UI ÷ cạnh khung, đối chiếu mốc caption `Y=297 ↔ 0.154523`). File `05 Finish part/dilim logo .png` 447×447 → 165×165 px trên khung. Đổi bằng `--logo <path>`.
- `doc_capcut.py` — **đọc số thật từ draft anh Thành đã chỉnh tay.** Mọi thông số vị trí trong tool này đều đi một đường: anh kéo tay trong CapCut trước, rồi chép vào code. Trước đây tôi đọc số trên *panel* CapCut rồi tự quy đổi sang đơn vị thư viện — panel và file draft dùng hai đơn vị khác nhau, chỉ có **một** mốc đối chiếu (`Y=297 ↔ 0.154523`), nên quy đổi là đoán và đã đoán sai ở logo. Giờ đọc thẳng từ `draft_info.json`, không còn phép đổi nào ở giữa.
- Xem xét rồi bỏ: `clips.WATERMARK`. `cuc-mau-dong.mp4` có logo HelixAnimation cháy vào hình, dùng 12 chỗ trong cả 5 job — **anh Thành chốt không sao, cứ dùng**. Giữ lại cơ chế (dict rỗng) phòng khi gặp watermark thật sự không dùng được.

- **LỖI THẬT đã vá trong `6_to_capcut.py`:** `plan.py` kiểm độ dài clip **trước** khi `4_anchor.py` đổi mốc, rồi không ai kiểm lại. Sau khi neo, caption dài ra — và các caption cùng clip còn bị gộp thành một cụm — nên `source_timerange` đòi vượt quá hết file. Trước đây cứ thế mà ghi. **4 đoạn trong 2 draft đã dựng dính lỗi này** (IMG_1770 #29 #33 #50, IMG_1773 #37). Giờ tự lùi `src_start`, không đủ thì cắt ngắn đoạn B-roll và báo — thà dải kết sớm còn hơn đứng hình giữa chừng.
- `soi_plan.py` — soi `plan.json` bằng luật, 0 token. Ngưỡng lấy từ phân bố thật của 369 dòng caption đã dựng.
- `soi_frames.py` — ghép frame B-roll tại đúng giây sẽ dùng thành contact sheet 12 ô. 41 dòng → 4 tấm thay vì 41 ảnh.
- Agent `dilim-soat-broll` — người soi tách khỏi người dựng. Chỉ đọc và đề xuất, không sửa file.

**v1.3 — 04/08/2026.** Không đụng vào phần dựng; vá phần **con người tốn công nhất** và phần **không đo được**.

- `make_plan_draft.py` — sinh khung `plan.py` từ `words_cut.json`: chia nhịp theo chỗ ngắt hơi dài nhất, đặt `t` bằng `start` của chữ thật (không còn ước lượng bằng mắt), điền sẵn lời nói viết hoa và đoán `variant`. Còn lại người làm: cô đọng chữ, đánh `*từ khoá*`, soát màu, chọn clip.
- `suggest_clips.py` + `clips.TAGS` — tra B-roll bằng từ khoá tiếng Việt thay vì lục 1.102 file trên ổ T7. Loại sẵn clip dọc (`clips.VERTICAL`), clip ngắn hơn caption, và hạ điểm clip vừa dùng trong 25 giây.
- `apply_duyet.py` — **đọc `duyet.json`**. Bảng duyệt xuất được file này từ 03/08 nhưng chưa có gì đọc nó, nên góp ý của anh bay mất sau mỗi job. Giờ nó chấm điểm (**% dòng anh không phải sửa** — con số backtest thật sự), ghi `edit/diem.md`, và gom mọi ô «VÌ SAO» vào `BAI_HOC.md`.
- `plan_build.py` — gỡ ~60 dòng logic bị chép lại trong mỗi `plan.py`. Đổi một mặc định: clip ngắn hơn cả caption giờ **bỏ trống** thay vì tự đổi sang ảnh sản phẩm (chính là lỗi gán nhầm caption "mạch máu thông thoáng" ở v1.2). Muốn hành vi cũ thì truyền `fallback=<ảnh>`.
- `make_review_table.py` — tên job và số caption trước đây bị ghi cứng `"Dilim Video test"` / `44` từ job đầu tiên, mọi bảng duyệt đều hiện sai tên.
- Tài liệu: `CLAUDE.md` ở gốc repo (kèm danh sách file **không được đọc** — `bang_duyet.html` 600 KB base64, `broll_catalog.json` 415 KB) và skill `dilim-autocut`. Trước đó skill duy nhất nối vào Claude Code trỏ vào tool 1 — đường lùi.
- `4b_vary.py` (viết 04/08) được đưa vào bảng chạy — trước đó tồn tại nhưng không tài liệu nào nhắc, nên `IMG_1773` vẫn lặp `dọt quỵ 1.mp4` 4 lần.

**v1.2 — 04/08/2026.** Chạy tự động hoàn toàn 3 video (`test hiếu 1/2/3`, 8m39s thô) trong **1 giờ 05**, không dừng hỏi. Vá 3 lỗi thật lộ ra khi gặp footage khác loại:

- **`ffprobe` trả `120/1,`** có dấu phẩy đuôi → hàm đọc fps vỡ. Giờ lọc bằng regex, không phụ thuộc định dạng. (Footage iPhone 120fps cũng được hạ về 30 ngay ở bước cắt.)
- **Lệch 1 micro giây do làm tròn** — `int(8.04e6)` ra `8039999` trong khi đoạn trước kết thúc ở `8040000` → CapCut từ chối vì `SegmentOverlap`. **Lỗi này nằm im trong mọi project trước đó**, chỉ chưa rơi trúng cạnh làm tròn. Giờ mọi mốc qua hàm `us()` dùng `round`, độ dài = hiệu hai mốc đã làm tròn.
- **Clip ngắn hơn caption** — kho sản phẩm mới chỉ 4–8 giây. Thêm bước tự lùi `src_start`; clip ngắn hơn cả caption thì đổi sang ảnh. Cảnh báo: bước đổi tự động không hiểu ngữ nghĩa, đã có 1 lần đổi caption "mạch máu thông thoáng" sang ảnh sản phẩm — phải soát lại.

Thêm: `clips.py` khai báo clip dùng chung (29 clip, tự kiểm) · `1_transcribe.py` · `cuts.json` cho từng job · `--name` đặt tên project.

**v1.1 — 03/08/2026.** Anh Thành duyệt bảng `DSCF0894`, sửa 13/49 dòng kèm lý do → rút 4 luật chọn B-roll (xem memory `dilim-broll-chon-clip`). Cài luật "caption liên tiếp cùng clip thì chạy liền mạch" vào code — 36 đoạn gộp còn 32. Thêm track SFX theo luật 15/07.

**v1.0 — 03/08/2026.** Bản đầu chạy được đầu-cuối. Gồm: cắt A-roll theo biên từ · bắt cue theo từ khoá · caption PNG của Tính · mask B-roll theo số anh Thành chốt · animation theo ý nghĩa · SFX theo luật 15/07 · nhúng media chống sandbox.
