# Workflow Tính Media

Quy trình chuẩn cho việc dựng video: **1 lần gửi file → 1 bảng duyệt gộp → 1 lần dựng**.
Kèm cơ chế Claude tự học cách chọn clip của bạn sau mỗi 5 video.

---

## Vòng làm việc (mỗi video)

```
   BẠN                          CLAUDE
    │
    ├─ gửi file/thư mục ──────►  ① Rebuild catalog
    │                            ② Transcribe (word-level)
    │                            ③ Soạn caption + chọn B-roll + đề xuất SFX
    │                            ④ Xuất BẢNG GỘP (1 file HTML)
    │  ◄──────────────────────
    │
    ├─ sửa trên bảng ─────────►  ⑤ Hỏi lại chỗ chưa rõ
    │  ◄── hỏi ────────────────
    ├─ trả lời ───────────────►  ⑥ Dựng kế hoạch cuối
    │                            ⑦ Render + kiểm tra frame
    │                            ⑧ Transcode + tách lớp
    │  ◄── bàn giao ───────────
```

**Chỉ có MỘT vòng duyệt.** Bảng gộp cho phép sửa caption, B-roll, SFX, ghi chú cùng lúc —
không còn tách 2 lượt như trước.

---

## Bảng duyệt gộp — cấu trúc

Một dòng cho mỗi caption, **xếp đúng thứ tự thời gian**:

| Cột | Nội dung | Bạn sửa được |
|---|---|---|
| # / Giây | Số thứ tự, dải thời gian | — |
| **Lời thoại gốc** | Trích từ transcript, chữ nghiêng xám | — |
| **Dòng 1 / Dòng 2** | Chữ hiện trên video | ✏️ |
| **Màu** | Đỏ (tiêu cực) / Xanh (tích cực) / Vàng (CTA) | ✏️ dropdown |
| **Ảnh preview B-roll** | Đúng khung hình sẽ render | — |
| **Đường dẫn B-roll** | Dán path để đổi hoặc thêm | ✏️ |
| **Sound effect** | Dropdown kèm công năng + thời lượng | ✏️ |
| **Ghi chú** | Dặn dò tự do | ✏️ |

Tự lưu vào trình duyệt, đóng tab mở lại vẫn còn. Bấm **Tải quyết định** → gửi lại 1 file JSON.

### Quy ước viết caption
- Bọc `*từ*` bằng dấu sao để từ đó đổi màu nhấn
- Để trống **cả 2 dòng** = bỏ caption đó (không cần nhấn)
- Ghi **trùng nội dung ở 2 dòng liền nhau** = gộp 2 ý làm một

### Quy ước B-roll (đã chốt)
- Một clip cho nhiều ý → chạy **liền một mạch**, không cắt
- Clip ngắn hơn thời lượng cần → **không lặp**, chạy hết rồi tắt, ưu tiên phủ trọn ý đầu
- Không dùng lại cùng một clip trong cùng video (trừ B-roll sản phẩm)

---

## Bộ file bàn giao (mỗi video)

| File | Dùng để |
|---|---|
| `overlay_light.mov` | Bản gộp B-roll + chữ, ProRes 4444 alpha |
| `text_only.mov` | Chỉ chữ — chỉnh riêng vị trí/màu |
| `sfx_track.wav` | Tiếng động, thả từ giây 0 |
| `overlay_PRORES4444.mov` | Bản gốc dự phòng |

Tất cả bắt đầu từ giây 0, thả vào đầu timeline là khớp.

---

## Cơ chế học — chạy sau mỗi 5 video

Sau mỗi 5 video, Claude tự đối chiếu **clip mình chọn vs clip bạn chọn**, rút quy luật, ghi vào
memory `dilim-broll-selection-principles`. Chỉ số theo dõi:

| Chỉ số | Ý nghĩa | Đợt 1 (VR 9.6.2026) |
|---|---|---|
| **Tỷ lệ giữ** | % clip Claude chọn mà bạn giữ nguyên | **79%** |
| **Số clip bạn tự thêm** | Chỗ Claude để trống mà bạn muốn có hình | **89** |
| **Độ phủ Claude đề xuất** | % caption có B-roll trong bản nháp | **25%** |
| **Độ phủ cuối** | % caption có B-roll sau khi bạn sửa | **70%** |

**Mục tiêu các đợt sau:** tỷ lệ giữ ≥ 85%, và độ phủ đề xuất tiệm cận độ phủ cuối
(để bạn ít phải tự thêm clip).

### Đã học được từ đợt 1

**Lỗi lớn nhất không phải chọn sai, mà là đề xuất quá ít.** Claude để trống gấp 3 lần mức bạn muốn.
Từ đợt 2 sẽ nhắm ~70% caption có B-roll ngay từ bản nháp.

**Bảy quy luật chọn clip rút từ 10 lần bạn thay:**
1. Caption có động từ diễn tiến (tăng dần, tích lũy, mòn dần) → clip phải cho thấy **quá trình**, không phải trạng thái tĩnh
2. Tả đúng **hành động** được nói, không tả cảm xúc quanh nó
3. Caption mang tính quan hệ/cảm nhận → ưu tiên **người thật**; caption nói cơ chế → đồ hoạ 3D
4. Ưu tiên thư mục **đã phân loại**, `Lộn Xộn Xà bần` chỉ dùng khi hết cách
5. Ẩn dụ **lướt qua** (đơn vị so sánh) → bám chủ đề chính. Ẩn dụ **triển khai dài** → minh hoạ ẩn dụ
6. **Màu đồ hoạ** phải khớp sắc thái: đỏ = tổn thương, xanh = khoẻ mạnh
7. Bám đúng **thuật ngữ chuyên môn** (hệ vi sinh ≠ niêm mạc ruột)

**Hai kho hay bị bỏ quên:** `Nhân Viên văn phòng` và `Ngủ- Ngon- mất ngủ` — bạn lấy từ đây nhiều
hơn Claude hẳn, nhất là cho các ý về mệt mỏi, công việc, giấc ngủ.

---

## Những điều Claude phải luôn làm

- **Rebuild catalog trước mỗi job** — catalog là ảnh chụp tĩnh, có thể cũ hơn ổ đĩa
- **Quét nhiều mốc trong clip** trước khi dùng — clip hay đổi cảnh giữa chừng
- **Ảnh preview trích tại đúng giây sẽ render**, không phải giây 0
- **Render tuần tự**, một tiến trình một lúc
- **Hỏi hết thắc mắc trước khi dựng**, không tự đoán
- **Báo cáo trung thực** — sai chỗ nào nói chỗ đó, kể cả khi bạn chưa phát hiện
