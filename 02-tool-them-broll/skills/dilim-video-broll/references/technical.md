# Ghi chú kỹ thuật render

Các quyết định và bug đã trả giá để tìm ra. Không lặp lại chúng.

## 1. Codec xuất file overlay

**Dùng ProRes 4444** (`prores_ks`, profile 4, pix_fmt `yuva444p10le`, fourcc `ap4h`).

**Không dùng HAP Alpha.** Đã thử và thất bại: file HAP không import được vào DaVinci Resolve trên Windows (nhiều khả năng thiếu component QuickTime/HAP). ProRes 4444 là định dạng Resolve hỗ trợ native, không cần cài thêm gì, và giữ kênh alpha chính xác.

Đánh đổi: ProRes 4444 rất nặng — video 5.4 phút cho ra file ~16GB. Khi chỉ cần bản cho người dùng xem duyệt, xuất preview nhẹ (ghép sẵn lên A-roll, scale 540x960, crf 28) thay vì đưa file overlay gốc.

## 2. Bẫy alpha channel trong ffmpeg

Chuỗi `format=yuva444p10le` **phải nằm cùng một chuỗi filter lavfi** với nguồn `color=...@0.0`, ví dụ:

```
color=black@0.0:s=1080x1920:r=60,format=yuva444p10le
```

**Không** tách ra thành option `-vf` riêng phía sau. Nếu tách, giá trị alpha bị âm thầm loại bỏ (đặt về 255 = đục hoàn toàn) dù pix_fmt trên danh nghĩa vẫn hỗ trợ alpha. Lỗi này rất khó phát hiện vì file xuất ra trông "đúng định dạng".

Cách kiểm chứng đã dùng: ghép một đoạn trong suốt và một đoạn đục, overlay lên nền đỏ. Làm đúng thì nền đỏ xuyên qua đoạn trong suốt; làm sai thì ra khối đen đặc.

## 3. Ghép track — dùng concat theo frame, không dùng enable/between

Dựng track B-roll và track caption **độc lập**, mỗi track ghép bằng cách nối chính xác theo frame các đoạn trong suốt (gap) với các đoạn có nội dung. Sau đó overlay hai track lên một nền trong suốt.

Không dùng cơ chế bật/tắt theo thời gian (`enable=between(...)`) — đã chứng minh gây giật hình.

## 4. Offset điểm bắt đầu trong file nguồn

Mỗi clip B-roll cần một tham số **offset điểm bắt đầu lấy từ nguồn** (không phải vị trí trên timeline).

Bug đã gặp: ban đầu hàm cắt clip không có tham số này, luôn lấy từ giây 0 của file nguồn bất kể cảnh cần dùng nằm ở đâu. Hậu quả: một clip 26 giây có cảnh cầm điện thoại ở giây 16-22 lại render ra 6.6 giây đầu (cảnh vươn vai, không có điện thoại) — chọn đúng file, sai đoạn.

Đây là lỗi **hệ thống**, không phải một lần: nó ảnh hưởng mọi clip trong pipeline cho tới khi được sửa.

## 5. Clip nguồn ngắn hơn thời lượng cần

Nếu (native duration − offset) < thời lượng cần, phải **loop nguồn** (`-stream_loop -1`). Không làm thì thiếu frame — đã từng hụt ~291 frame trong một bản render vì clip nguồn chỉ 5.2s mà cần 10.05s.

## 6. Dải B-roll

- Chiều cao dải trên: **672px** trên khung 1080x1920 (~35% chiều cao).
- Mép dưới của dải: **làm mờ nhẹ** dải 20px cuối (boxblur), **không** fade alpha.

Người dùng đã bác bỏ cách làm fade alpha: *"chỉ làm mờ nhẹ... không phải fade cho lộ A-roll bên dưới"*. Fade alpha tạo hiệu ứng bóng ma chồng hai lớp hình; blur chỉ làm mềm đường cắt mà vẫn giữ B-roll đục hoàn toàn.

## 7. Tránh chạy chồng tiến trình render

Chỉ chạy **một** tiến trình render tại một thời điểm. Đã có lần vô tình chạy hai lệnh render chồng lên nhau (tưởng lệnh đầu không chạy vì output rỗng) — hai tiến trình giẫm lên nhau, ghi cùng thư mục tạm, treo máy nhiều giờ và phải kill thủ công.

Nếu lệnh render có vẻ không phản hồi, **kiểm tra tiến trình đang chạy trước** khi khởi động lại lệnh mới.

## 8. Môi trường

- Python 3.12 cho mọi thao tác liên quan pipeline. Python 3.11 (mặc định trong PATH) crash khi import thư viện DaVinci Resolve.
- Whisper: `faster_whisper`, model `medium`, `language="vi"`, `vad_filter=True`, **`word_timestamps=True`** (bắt buộc — xem lý do trong `broll-rules.md` phần timing).
- Xuất log/stdout tiếng Việt: đặt encoding UTF-8, nếu không sẽ lỗi `UnicodeEncodeError` với codepage mặc định của Windows.

## 9. Bug tìm kiếm catalog (đã sửa, ghi lại để tham chiếu)

Hàm tìm kiếm B-roll từng dùng phép so khớp **chuỗi con thô** làm phương án dự phòng, cho phép khớp xuyên qua ranh giới từ. Ví dụ tìm "ô tô" (chuẩn hóa thành "o to") lại khớp nhầm vào "mỡ **tố**t trong máu" vì chuỗi "o to" nằm vắt ngang giữa "mỡ" và "tốt".

Đã sửa bằng cách bỏ hẳn nhánh chuỗi con, chỉ giữ kiểm tra biên từ. Nếu gặp kết quả tìm kiếm vô lý trong tương lai, kiểm tra lại logic so khớp trước khi nghĩ tới việc đổi tên hàng nghìn file.
