# Chọn B-roll

## B-roll tồn tại để làm gì

Hai việc, kéo về hai hướng ngược nhau:
1. **Cho người xem hình dung được** điều đang nghe — cần đúng.
2. **Giữ nhịp** — vài giây phải có điểm nhấn mới, cần dày.

Giải quyết mâu thuẫn này **không phải bằng cách thoả hiệp ở giữa**, mà bằng cách tìm kỹ hơn:
nâng ngưỡng "đã tìm đủ" lên cao, giữ nguyên ngưỡng "đủ chính xác để dùng".
Không có clip khớp thật thì **để trống** — caption có animation vẫn đủ giữ nhịp.

## Cách tra

```bash
python3 03-tool-capcut/pipeline/suggest_clips.py --job $J --md    # cả bài
python3 03-tool-capcut/pipeline/suggest_clips.py --text "mạch máu hẹp lại"   # tra lẻ
```

Máy tra bằng **từ khoá trong `clips.TAGS`**. Nó không biết clip quay gì.
Điểm cao = khớp nhiều từ khoá hơn, **không có nghĩa là đúng ý**.

Tìm tay ra được clip nào mà máy không tra ra → **thêm từ khoá vào `clips.TAGS`** ngay lúc đó.
Đây là lý do 12 clip mạch máu bị bỏ sót ngày 03/08: tên file tiếng Anh
(`Arteriosclerosis`, `Blood clot`) nên tra tiếng Việt không ra.

Clip mới chưa khai trong `clips.py` thì thêm hằng số, ghi kèm độ dài vào comment.

## Bốn luật anh Thành dạy (bảng duyệt DSCF0894, 03/08/2026)

**1. Caption liên tiếp dùng cùng clip → B-roll chạy LIỀN MẠCH.**
Anh: *"2 cái liên tiếp là chạy hết cái này đến cái kia"*.
Không cắt ở ranh giới caption, không nhảy về đầu clip — hình giật lại là phá mạch kể.
*Đã cài trong `6_to_capcut.py`* — cứ để cùng `path` cho các caption liền nhau, máy tự gộp.

**2. `src_start` phải nhắm đúng khoảnh khắc minh hoạ câu đang nói.**
Anh đổi #11 sang `mang-xo-vua.mp4` **giây 15**: *"chỗ này nói mảng xơ vữa nó dày xong máu đi
qua bị tắc nên lấy đoạn này dễ hình dung hơn"*.
Clip dài **đổi cảnh giữa chừng** — cùng một file, giây 0 và giây 15 kể hai chuyện khác nhau.
`src_start` không phải điền cho có. Quét vài mốc rồi chọn.

**3. Ảnh sản phẩm phải lọt TRỌN trong dải, có khoảng thở.**
Dải B-roll là **1080×672**. Ảnh chụp cận bị cắt cụt ở mép dải.
Chọn ảnh toàn cảnh có khoảng trống — `natto-2hop.jpg` (2 hộp trên thớt gỗ) hơn `DSCF0907.JPG`
(chụp gần, hộp bị crop mất) dù hai ảnh tỉ lệ gần bằng nhau.

**4. Ưu tiên file có tên đọc hiểu.** File anh tự đặt tên (`mang-xo-vua.mp4`, `natto-01.mp4`,
`co-the-nguoi.mp4`) là file anh đã duyệt — hơn `DSCF####` hay `Thiết kế chưa có tên…`.

## Bốn câu hỏi phải trả lời được trước khi chốt một clip

Đây là nơi mọi lỗi nghiêm trọng đã xảy ra — hay bị bỏ qua khi đang vội tăng mật độ.

1. Clip này có đúng **cảnh cụ thể** tôi hình dung không? (không phải "có cùng chủ đề không")
2. **Không khí** có khớp sắc thái caption không? Cùng cảnh ăn uống, vẻ mặt vui và vẻ mặt chán là hai ý trái ngược.
3. Tôi đã xem frame tại **đúng giây sẽ dùng** chưa (tính cả `src_start`)? File dài hơn nhiều so với đoạn cần dùng là dấu hiệu nó chứa nhiều cảnh khác nhau.
4. Có phải clip **NGANG** không? Dải B-roll cần clip ngang. Clip dọc 1080×1920 nằm trong `clips.VERTICAL`, `suggest_clips.py` đã loại sẵn — đừng tự điền vào.

Xem frame tại đúng giây:
```bash
ffmpeg -ss <src_start> -i "<clip>" -frames:v 1 -vf scale=320:-1 /tmp/xem.jpg
```

## Ẩn dụ thì minh hoạ CÁI ĐƯỢC VÍ VON

Câu *"giống như đường ống nước lâu ngày có rong rêu cặn"* cần **clip ống nước bẩn thật**,
không phải clip mạch máu. Video mẫu của DiLiM làm rất rõ điều này: nói "quét sơn chống rỉ sét"
thì chèn cảnh thanh sắt rỉ thật.

Hiện kho **chưa có** nhóm ẩn dụ này (ống nước, máy bơm, vỉ thuốc) — 4 caption của IMG_1770
phải để trống vì vậy. Đây là khoảng thiếu đã biết, không phải lỗi.

## Chống lặp

Ý lặp lại thì tìm clip **thật sự khác**, đừng lặp hình. Kịch bản bán hàng tự lặp ý —
anh Hiếu nói "mạch máu thông thoáng, phòng ngừa đột quỵ" 4 lần trong một bài.

`4b_vary.py` tự xoay vòng trong `clips.FAMILIES` khi một clip sắp dùng lại trong vòng 25 giây.
Hết lựa chọn thì nó giữ nguyên — **thà lặp còn hơn dùng clip sai ý**.
B-roll sản phẩm được miễn trừ (thường chỉ có một clip chính hãng).

## Còn ngỏ — hỏi anh

**CTA cuối bài nên để B-roll gì?** Chưa thành luật. Trên DSCF0894 anh gắn `neuron-thankinh.mp4`
rồi bảo *"chả nhớ nữa, kệ đi, lần sau hỏi"*. Các lựa chọn từng dùng: ảnh hero sản phẩm,
hộp trên cỏ, hoặc để trống cho chữ chạy một mình.
