# Quy trình dựng video DiLiM — từ lúc nhận file đến khi bàn giao

Đúc kết từ đợt dựng 5 video VR 9.6.2026 (195 caption, 116 đoạn B-roll, 65 tiếng động).
Mỗi bước ghi rõ **làm gì**, **vì sao**, và **lỗi thật đã gặp** nếu có.

---

## Nguyên tắc xuyên suốt

**Duyệt trước, dựng sau.** Render một video mất ~1 tiếng; sửa trên bảng mất 1 phút. Mọi quyết định
về nội dung (chữ, clip, tiếng động) phải được chốt trên bảng trước khi chạm vào render.

**Không đoán — kiểm tra.** Tên file không cho biết clip quay gì. Trí nhớ về thư viện không đáng tin.
Catalog có thể cũ hơn ổ đĩa. Mọi khẳng định đều phải mở ra xem.

---

## GIAI ĐOẠN 1 — Chuẩn bị (10 phút)

### 1.1 Rebuild catalog B-roll
```
python catalog.py build
```
**Bắt buộc làm trước khi tìm bất cứ thứ gì.** Catalog là ảnh chụp tĩnh, không phải index sống.

> **Lỗi thật:** search "nano sụn" ra rỗng → kết luận kho không có footage sản phẩm. Thực tế catalog
> build từ 2 ngày trước, thư mục sản phẩm mới thêm sau đó. Lần dựng 5 video này rebuild ra thêm
> 79 file so với lần trước, trong đó có ảnh đổ nhớt xe — thứ mà lần trước tôi kết luận "kho không có".

### 1.2 Quét thư mục nguồn, lấy thông số
Với mỗi video: `ffprobe` lấy duration + fps → tính `total_frames`.

### 1.3 Transcribe
`faster_whisper`, model `medium`, `language="vi"`, **`word_timestamps=True`**.

Timestamp cấp câu lệch tới vài giây — không dùng được để canh điểm chèn. Timestamp cấp từ là
bắt buộc, dùng ở bước tách dòng và canh tiếng động.

---

## GIAI ĐOẠN 2 — Caption (vòng duyệt 1)

### 2.1 Soạn caption nháp
- Bám sát ranh giới câu/cụm **thật** trong transcript, không gộp ý xa nhau
- Danh sách liệt kê dồn dập → **mỗi item một nhịp riêng**
- Câu ẩn dụ → minh hoạ đúng cái được ví von, không phải nội dung y khoa
- Gán màu theo **ý nghĩa**: đỏ = tiêu cực, xanh = tích cực, trắng/vàng đậm = sản phẩm (cấm đỏ/đen)

### 2.2 Xuất bảng duyệt
**Dạng HTML mở bằng trình duyệt**, không dùng Excel — người dùng có thể không có license Office.

Bảng phải có:
- Cột **câu nói gốc** để đối chiếu ngữ cảnh
- Ô sửa trực tiếp (contenteditable), tự lưu vào localStorage
- Nút tải về JSON

> **Lỗi thật:** lần đầu xuất .xlsx → người dùng không mở được. Lần hai xếp caption không theo
> thứ tự và không kèm lời thoại → người dùng không nhớ ngữ cảnh, không duyệt được.

### 2.3 Áp bản sửa
Quy ước người dùng đã chốt:
- **Để trống** = ý đó không cần nhấn → bỏ caption
- **Ghi trùng nội dung ở 2 dòng liền nhau** = gộp 2 ý làm một

Kiểm tra tự động sau khi áp:
- Dấu `*` lẻ (phải đi theo cặp, lẻ thì hiện dấu sao trên video)
- Caption chồng lấn thời gian

---

## GIAI ĐOẠN 3 — Sound effect

### 3.1 Phân tích kho SFX
Đo cho từng file: **thời lượng thật có tiếng**, **khoảng lặng đầu file**, **peak dB**.

Khoảng lặng đầu file là thứ quan trọng nhất — nếu đặt SFX đúng frame chữ hiện, tiếng sẽ kêu
**trễ** đúng bằng khoảng lặng đó.

> Thực tế đo được: Whoosh 05 lặng 0.09s, còn mouse-click lặng tới **1.09s** — nếu không bù trừ
> thì tiếng click nổ sau chữ hơn một giây.

### 3.2 Cho người dùng chọn
Thêm cột dropdown vào bảng caption, mỗi lựa chọn ghi kèm **công năng + thời lượng thật**
(vd: "Whoosh 05 · caption vào (0.48s)"), không chỉ tên file.

### 3.3 Dựng track âm thanh riêng
Xuất `sfx_track.wav` tách khỏi video, vì overlay là file alpha không có audio.
- Đẩy lùi mỗi tiếng đúng bằng khoảng lặng đầu file
- Chuẩn hoá tất cả về cùng peak (−6 dB) — kho có file 0.0 dB, có file −6.8 dB, trộn thẳng sẽ chỗ to chỗ nhỏ

---

## GIAI ĐOẠN 4 — B-roll (vòng duyệt 2)

### 4.1 Xác định ý nào cần B-roll
Không phải caption nào cũng cần. Ý trừu tượng ("tự lừa dối chính mình", "thay đổi kỳ vọng")
để chữ chạy một mình là đúng.

### 4.2 Tìm clip
- Tưởng tượng **cảnh cụ thể** trước, rồi mới rút từ khoá — đừng lấy thẳng thuật ngữ y khoa
- Thư mục nhiều file → **mở nhiều ứng viên ra xem**, đừng đọc tên rồi chọn đại
- Tra kỹ trước khi kết luận "kho không có" — lần này tra thêm một vòng ra thêm 4 clip

### 4.3 Xuất bảng duyệt B-roll — **bắt buộc có ảnh preview**

Tên file không cho biết clip quay gì. Ảnh phải trích **tại đúng giây sẽ render** (tính cả offset
trong file nguồn), không phải giây 0.

Bảng phải có, xếp **theo thứ tự thời gian**:
| Ảnh preview | Caption | Lời thoại gốc | Tên clip | Lý do chọn | Ô dán path | Ô ghi chú |

Kèm cảnh báo tự động: clip trùng, clip ngắn hơn thời lượng cần, chỗ cố ý để trống.

Phải liệt kê **cả những ý chưa tìm được clip**, ghi rõ *cần cảnh gì* để người dùng biết đường tìm.

### 4.4 Hỏi lại trước khi dựng
Sau khi nhận bản duyệt, **hỏi hết thắc mắc rồi mới làm**. Những chỗ cần hỏi:
- Path lỗi cú pháp (thừa ký tự, dán 2 path vào một ô)
- Clip trùng nhau ở vị trí cách xa — có chủ ý hay nhầm?
- Clip có watermark thương hiệu khác
- Caption ngắn mà gán 2 clip — chia thế nào?

---

## GIAI ĐOẠN 5 — Dựng kế hoạch cuối

### Luật đã chốt với người dùng
1. **B-roll cho nhiều ý** → chạy **liền một mạch** từ ý đầu, không cắt, không nối lại
2. **Clip ngắn hơn thời lượng cần** → **không lặp**, chạy hết rồi tắt. Ưu tiên phủ trọn ý đầu
3. **Không dùng lại cùng một clip** trong cùng video (trừ B-roll sản phẩm)

Kiểm tra sau khi dựng: không đoạn nào chồng lấn, không đoạn nào vượt quá độ dài clip nguồn.

---

## GIAI ĐOẠN 6 — Render

### 6.1 Chạy TUẦN TỰ, một tiến trình một lúc
> **Lỗi thật:** chạy 2 lệnh render chồng nhau (tưởng lệnh đầu chết vì output rỗng) → 2 tiến trình
> ghi cùng thư mục tạm, treo máy nhiều giờ, phải kill thủ công.

Nếu lệnh có vẻ không phản hồi: **kiểm tra tiến trình đang chạy trước**, đừng khởi động lại.

### 6.2 Thông số
ProRes 4444 (`prores_ks`, profile 4, `yuva444p10le`). Không dùng HAP — không import được Resolve.

`format=yuva444p10le` phải nằm **cùng chuỗi lavfi** với `color=...@0.0`, tách ra `-vf` riêng sẽ
âm thầm mất alpha.

---

## GIAI ĐOẠN 7 — Kiểm tra

Ghép overlay lên A-roll thật, trích frame tại **từng điểm B-roll/caption**, xem thật từng frame.

> **Lỗi thật (mắc 2 lần):** chọn clip đúng file nhưng chỉ xem frame đầu → clip đổi cảnh sau 1.5s
> sang nội dung khác kèm chữ tiếng Anh. Rút ra: clip nào cũng phải **quét nhiều mốc** trong đúng
> dải sẽ dùng, không tin một frame.

---

## GIAI ĐOẠN 8 — Xuất bản giao

### 8.1 Transcode bản nhẹ
ProRes 4444 `qscale 9` → nhẹ hơn **~6 lần**, chất lượng soi 2x không phân biệt được.

> **Lưu ý:** phải test lại theo **đúng loại nội dung**. Overlay chỉ có chữ nén được xuống
> 0.23 GB/phút; overlay có B-roll (hình thật nhiều chi tiết) chỉ xuống được 0.68 GB/phút.
> Đừng dùng lại con số của lần trước.

### 8.2 Test alpha
Chồng file lên nền đỏ, trích frame — nền đỏ phải xuyên qua vùng trong suốt.

### 8.3 Bộ file bàn giao (mỗi video)
| File | Dùng để |
|---|---|
| `overlay_light.mov` | Bản gộp B-roll + chữ |
| `text_only.mov` | Chỉ chữ — chỉnh riêng vị trí/màu |
| `sfx_track.wav` | Tiếng động, thả từ giây 0 |
| `overlay_PRORES4444.mov` | Bản gốc dự phòng |

Lớp chữ và lớp B-roll **đã được dựng riêng** trong `render_tmp/` rồi mới ghép — nên tách file
không tốn thời gian render lại, chỉ cần transcode (~3 phút/video).

---

## Tổng thời gian thực tế (5 video, ~11.6 phút thành phẩm)

| Giai đoạn | Thời gian |
|---|---|
| Chuẩn bị + transcribe | ~15 phút |
| Soạn caption + xuất bảng | ~30 phút |
| *Người dùng duyệt caption* | — |
| Phân tích SFX + dựng track | ~10 phút |
| Tìm B-roll + xuất bảng có ảnh | ~45 phút |
| *Người dùng duyệt B-roll* | — |
| Render 5 video | ~4 tiếng |
| Kiểm tra + transcode + tách lớp | ~45 phút |

Phần chiếm thời gian nhất là render — nên mọi thứ phải chốt xong trước khi bấm render.
