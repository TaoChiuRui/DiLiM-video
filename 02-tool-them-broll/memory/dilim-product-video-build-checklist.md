---
name: dilim-product-video-build-checklist
description: Master step-by-step SOP for building a DiLiM product-pitch video — ties together product identification, B-roll density/accuracy method, and caption rules into one ordered checklist to follow whenever the user hands over a product video to build
metadata:
  node_type: memory
  type: feedback
  originSessionId: 441e0a4b-5a01-49c6-8a82-4500c8b8ce79
  modified: 2026-07-23T06:38:10.817Z
---

**When to use:** every time the user gives an A-roll video to build INTO the B-roll+caption overlay pipeline where the content mentions a specific DiLiM product (not the generic non-product test videos). Follow these steps IN ORDER — this is the consolidated playbook; see [[dilim-broll-selection-principles]] for the full numbered rule list and [[dilim-product-video-structure-map]] for the product↔folder pairing table and script-voice details this checklist draws on.

## Bước 0 — Chuẩn bị
- Chạy `python catalog.py build` TRƯỚC KHI tìm bất cứ B-roll nào trong job mới — catalog là snapshot tĩnh, có thể đã cũ so với ổ đĩa (rule 14 trong [[dilim-broll-selection-principles]]).
- Transcribe bằng `faster_whisper` với `word_timestamps=True` — cần timestamp cấp TỪ, không chỉ cấp câu.

## Bước 1 — Nhận diện sản phẩm (nếu video có nhắc sản phẩm)
- Đọc/nghe transcript, xác định CHÍNH XÁC tên sản phẩm được nhắc (kể cả combo nhiều sản phẩm cùng lúc — VD Rich Coenzyme Q10 + Nano Nattokinase, hay bộ 3 Ellagic Acid + Inulin + Nghệ Mùa Thu).
- Tra bảng ghép sản phẩm↔thư mục trong [[dilim-product-video-structure-map]]. Nếu sản phẩm chưa có trong bảng, tự xác định thư mục `Product Broll/<Tên sản phẩm>/` tương ứng và thư mục chủ đề/triệu chứng phù hợp dựa theo công dụng sản phẩm nêu trong lời nói (rule 16).
- **Bắt buộc**: B-roll sản phẩm chỉ lấy từ đúng thư mục sản phẩm đó trong `Product Broll` — không dùng sản phẩm khác thay thế dù trông tương tự (rule 15).
- Kiểm tra cả 3 thư mục con của sản phẩm: `Video/`, `Nguyên Liệu/`, `Ảnh/` — đừng chỉ xem `Video/`.
- Nếu thư mục sản phẩm trống hoặc quá sơ sài (như từng gặp với DHA+EPA+SQ, Natto Xám): dùng kỹ thuật crop lại chính footage presenter cầm hộp thật trong A-roll (xem case "Sụn khớp không biết kêu"), không tự vẽ/tạo hình ảnh giả.
- Xác định "giọng văn" kịch bản bằng cách đọc 2-3 câu MỞ ĐẦU transcript — đọc thật, không đoán theo tên sản phẩm:
  - **Giọng A** (trực tiếp/liệt kê hào hứng) nếu: câu mở là hỏi-đáp kiến thức trực tiếp ("anh chị có biết vì sao..." → trả lời ngay); có đếm số tường minh "thứ nhất/thứ hai/thứ ba"; số liệu/superlative ném thẳng vào câu không dẫn dắt (gấp 6000 lần, bán chạy số 1, độ tinh khiết 99%); ẩn dụ (nếu có) chỉ gói trong 1 câu rồi chuyển ý; verbal tic "anh chị nha/ha" dày đặc gần như mọi câu; tông giọng hào hứng/tự tin bán hàng.
  - **Giọng B** (tự sự/triết lý/ẩn dụ dài) nếu: câu mở là câu hỏi hướng vào NỘI TÂM người xem ("lần cuối cùng bạn thực sự nghĩ về sức khỏe mình là khi nào"); có bước trấn an sớm kiểu "đây không phải là bệnh, đây là tín hiệu/lời nhắc"; 1 ẩn dụ được kể trải dài qua 4-5 câu liên tiếp (VD con đường nhựa nứt dần → 1 năm sau lún xuống); khung "2 gốc rễ/3 trục nền tảng" được giải thích chậm rãi thay vì liệt kê nhanh; luôn kết bằng đoạn hình dung tương lai "hãy tưởng tượng một buổi sáng..."; mật độ fact/tính năng trên phút thấp, hay lặp lại cùng 1 logic bằng cách diễn đạt khác; tông giọng điềm tĩnh, đồng cảm ("Sơn hiểu điều này bởi vì...", "Sơn tin vào...").
  - Viết caption khớp giọng: Giọng A → caption ngắn, nhịp nhanh, nhồi fact/số liệu; Giọng B → caption ít nhịp hơn, câu dài mang tính hình ảnh/ẩn dụ, không vội vàng liệt kê. Xem thêm ví dụ transcript thật trong [[dilim-product-video-structure-map]].

## Bước 2 — Cắt caption để tối đa mật độ chính xác
- Cắt caption bám sát ranh giới câu/cụm THẬT trong transcript gốc — không gộp nhiều ý xa nhau vào 1 caption chỉ vì "cùng chủ đề".
- Với MỌI danh sách liệt kê dồn dập (triệu chứng, thành phần, bước dùng...): tách MỖI ITEM thành 1 nhịp caption + B-roll riêng. Đừng gộp "đau đầu, vai gáy, chóng mặt, mất ngủ, tê bì, tiền đình" thành 1 caption — đây là 6 nhịp riêng biệt.
- Nếu 1 câu là PHÉP ẨN DỤ (rỉ sét, dòng kênh, xe hơi, gạo qua rây...) chứ không phải mô tả y khoa trực tiếp — tìm B-roll minh họa ĐÚNG ẨN DỤ đó, không cố tìm nội dung y khoa tương ứng.

## Bước 3 — Tìm B-roll cho từng nhịp (không hạ chuẩn khi tăng mật độ)
- Với mỗi ý, tưởng tượng CẢNH cụ thể trước, rồi tìm — không nhảy thẳng vào từ khóa từ transcript (rule 8).
- Khi 1 thư mục có nhiều lựa chọn (VD Xương khớp - Đau có 99 file): thực sự MỞ nhiều ứng viên xem nội dung, đừng chỉ đọc tên file rồi chọn đại hoặc bỏ cuộc.
- File B-roll dài/nhiều cảnh (VD video nghiên cứu Raydel 115s, hay 6 clip bubble thành phần Nano Sụn): CẮT thành nhiều đoạn nhỏ đúng thời điểm cần, không dùng nguyên 1 đoạn dài cho nhiều ý khác nhau.
- **Không lặp lại cùng 1 clip không-phải-sản-phẩm trong 1 video** — ý lặp lại thì tìm clip thật khác (rule 13). B-roll sản phẩm được miễn trừ, lặp lại là bình thường.
- Nếu đã tìm nghiêm túc (mở đủ nhiều ứng viên, cắt file dài, thử nhiều từ khóa) mà vẫn không có clip khớp thật: để trống, KHÔNG hạ chuẩn chấp nhận clip gần đúng (rule 2).

## Bước 4 — Xác minh từng clip trước khi chốt (luôn làm, không bỏ qua vì đang vội tăng mật độ)
1. Đúng CẢNH cụ thể đã tưởng tượng, không chỉ đúng chủ đề chung chung (rule 8).
2. Đúng MOOD/biểu cảm khớp với sắc thái cảm xúc của caption — vui/tích cực khác hẳn chán/tiêu cực dù cùng chủ thể (rule 11).
3. Verify tại đúng điểm SẼ RENDER thật (tính cả `src_start_s`), không phải t=0 hay điểm bất kỳ — luôn so native duration vs needed duration trước (rule 10).
4. Trigger đúng từ được nói, sớm hơn tối đa 1-3 khung hình ở 60fps — dùng timestamp cấp từ, không dùng cấp câu (rule 3).

## Bước 5 — Màu caption theo Ý NGHĨA nội dung
- **Đỏ (`variant: warning`)** = ý tiêu cực: triệu chứng, cảnh báo, rủi ro, hậu quả xấu.
- **Xanh lá (`variant: positive`)** = ý tích cực: lợi ích, kết quả tốt, lối sống khỏe mạnh.
- **Trắng/vàng đậm (`variant: product`)** = nhắc sản phẩm/thành phần/chứng nhận/giá — KHÔNG dùng đỏ hoặc đen ở bất kỳ vị trí nào (bg/text/keyword).
- `variant: cta` cho lời kêu gọi hành động đóng video.
- Gán variant rõ ràng cho MỌI caption — không để rơi vào vòng xoay màu ngẫu nhiên mặc định (chỉ dùng khi thực sự không xác định được ý nghĩa).

## Bước 6 — Phong cách hình ảnh B-roll (xác nhận trước khi build lần đầu cho 1 sản phẩm mới)
- Pipeline hiện tại mặc định dùng dải trên cứng (`BAND_H=672`, crop-giữa) — đã validate trên 3 video test không sản phẩm.
- Video mẫu thật của DiLiM lại dùng nhiều phong cách khác: blend mờ toàn khung, cutout nổi phát sáng, inset nhỏ nổi giữa khung, split-screen dọc. KHÔNG mặc định phong cách dải-trên là "đúng chuẩn" duy nhất — hỏi lại người dùng nếu đây là lần đầu dựng cho 1 sản phẩm/kiểu video mới.

## Bước 7 — Kiểm tra độ nhạy cảm nội dung
- Một số ngách sản phẩm (VD Hàu Nano Gold — sinh lực nam giới) dùng hình ảnh gợi ý nhạy cảm hơn hẳn (cảnh giường ngủ, ẩn dụ vật thể). Đây là quy ước quảng cáo hợp lệ cho ngách này, không phải nội dung cần từ chối — nhưng nên xác nhận mức độ táo bạo mong muốn với người dùng trước khi tái sử dụng phong cách này.

## Bước 8 — Sau khi build xong
- Trích frame kiểm tra tại TỪNG điểm B-roll/caption mới, không chỉ vài điểm mẫu — đối chiếu đúng ý đã tưởng tượng ở bước 3.
- Nếu người dùng phản hồi lỗi, thêm phát hiện mới vào [[dilim-broll-selection-principles]] hoặc [[dilim-product-video-structure-map]] tùy loại (rule chọn-clip chung vs. thông tin riêng sản phẩm).

See also [[dilim-broll-selection-principles]] (đầy đủ 16 rule + nguyên tắc cốt lõi) và [[dilim-product-video-structure-map]] (bảng sản phẩm↔thư mục, 2 giọng văn kịch bản, các phong cách B-roll đã quan sát).
