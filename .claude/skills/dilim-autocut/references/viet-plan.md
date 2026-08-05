# Viết `plan.py` — nội dung caption

`make_plan_draft.py` đã chia nhịp và đặt mốc `t` sẵn. Còn 4 việc phải làm tay.

Mỗi dòng: `(t, "DÒNG 1", "DÒNG 2", "variant", CLIP, src_start, "ghi chú")`

---

## 1. Cô đọng chữ — BẮT Ý, KHÔNG BẮT CHỮ

> Anh Thành 04/08/2026: *"đừng bắt full chữ, mà bắt ý chính, ngắn gọn dễ hiểu đủ ý —
> không cần full chữ như subtitle đâu"*.

Khung sinh ra chứa **lời nói nguyên văn**. Caption không phải phụ đề — nó là điểm tựa cho mắt.
Đọc cả nhịp, hỏi *"câu này nói cái gì?"*, rồi viết **cái đó** ra. Đừng chép rồi cắt bớt.

Bỏ: từ đệm ("à", "thì", "đúng không ạ", "nên là", "cái"), phần lặp, câu dẫn suông.
Giữ nguyên tuyệt đối: **số liệu, giá, tên sản phẩm, hàm lượng, tên riêng, thuật ngữ**.

### Viết GIÁ — dạng rút gọn, không viết bằng chữ

> Anh Thành 04/08/2026: *"khi ghi giá thay vì toàn chữ ghi 5.180K · 31.080K ví dụ như thế"*.

| Anh nói | ĐỪNG viết | VIẾT |
|---|---|---|
| "31 triệu 080 nghìn" | `31 TRIỆU 080 NGHÌN` | **`31.080K`** |
| "5 triệu 180 nghìn" | `5 TRIỆU 180 NGHÌN` | **`5.180K`** |
| "2 triệu 290 nghìn" | `2 TRIỆU 290 NGHÌN` | **`2.290K`** |

Quy tắc: đổi ra **nghìn đồng**, chấm ngăn hàng nghìn, hậu tố `K`. Dài bằng một phần ba,
mắt bắt được ngay — chữ "TRIỆU… NGHÌN" chiếm hết dòng mà chẳng thêm nghĩa.

Số nhỏ (giá lẻ, số viên, số hộp, hàm lượng) thì giữ nguyên: `120 VIÊN`, `6 HỘP`,
`60.000 FU`, `2 VIÊN 1 NGÀY`. **Chỉ tiền mới quy về `K`.**

Không được: thêm ý mới · đổi mức khẳng định · biến trải nghiệm cá nhân thành nhận định chung.

**⚠ Giới hạn của việc cô đọng — cái này đã vấp thật:** `4_anchor.py` neo caption vào
**chữ anh thật sự nói**. Viết xa quá thì không còn gì để bám và nó báo `KHÔNG NEO ĐƯỢC`,
mốc `t` rơi lại về ước lượng. Job `06-magie-canxi` dính 2 dòng vì tôi viết
`CHỖ NÀY QUAN TRỌNG` trong khi anh nói *"nhiều anh chị chưa biết"*.

> **Cô đọng thoải mái, nhưng chừa lại ít nhất một từ khoá anh thật sự nói.**
> `*ÍT AI BIẾT CHỖ NÀY*` (bám "biết") · `*GIÁ TRỌN BỘ*` (bám "giá") — vẫn gọn, vẫn neo được.

Tối đa **2 dòng**, mỗi dòng nên ≤ 26 ký tự (dài hơn thì engine tự thu nhỏ cỡ chữ).

### Chia 2 dòng thì cắt ở đâu

> Anh Thành: *"ghép caption kiểu theo cụm thôi, đừng làm word by word y hệt"*.

`make_plan_draft.py` đã chia sẵn bằng `ngat_cum.py`, nhưng khi sửa tay thì giữ đúng 3 luật
(nặng dần):

1. **Không tách đôi cụm ghép** — `mạch máu`, `cục máu đông`, `số điện thoại`, `coenzyme Q10`.
2. **Không để từ dính treo cuối dòng** — `của`, `những`, `cái`, `để`, `mà`, `là`, `có`.
3. **Nên cắt ngay trước từ mở cụm** — `nhưng`, `mà`, `thì`, `để`, `vì`, `nên`, `còn`.

Sai điển hình: `MÁU CÓ THỂ LƯU | THÔNG DỄ DÀNG HƠN` · `ĐANG CÓ NHỮNG | CÁI MẢNG XƠ VỮA`.
Gặp cụm ghép mới thì thêm vào `ngat_cum.CUM_GHEP`.

Chú ý whisper nghe sai tên riêng và thuật ngữ — `TỀN ĐÌNH` phải sửa thành `TIỀN ĐÌNH`,
`bản sơ vữa` → `MẢNG XƠ VỮA`. Bước `4_anchor.py` có dò gần đúng nên vẫn neo được sau khi sửa.

Luật cấm từ của DiLiM: **"phục hồi" / "bảo vệ"**, KHÔNG "chữa lành" / "điều trị" / "chữa bệnh".
Giữ giọng mộc mạc, xưng "cô chú" / "anh chị" như trong lời nói gốc.

## 2. Đánh `*từ khoá*`

Bọc cặp `*` quanh cụm cần nhấn — engine đổi màu cụm đó.

```
"CÔ CHÚ ĐANG BỊ *ĐAU ĐẦU*", "*MẤT NGỦ*"
```

Nhấn **cụm mang thông tin** (triệu chứng, con số, tên sản phẩm, kết quả), không nhấn
động từ nối. Mỗi dòng 1–2 cụm là đủ — nhấn hết thì thành không nhấn gì.

Số dấu `*` phải chẵn. `plan.py` sẽ báo `dau * le` nếu lẻ.

## 3. Soát `variant`

Máy đoán bằng từ khoá và đánh dấu `#?`. **Phải xem lại từng dòng** — màu mang nghĩa,
đoán sai là sai bài.

| variant | Dùng cho | Màu |
|---|---|---|
| `warning` | triệu chứng, cảnh báo, rủi ro, hậu quả, cơ chế bệnh | đỏ |
| `positive` | lợi ích, kết quả tốt, cải thiện, phòng ngừa | xanh lá |
| `product` | tên sản phẩm, thành phần, chứng nhận, giá, liều | trắng — **không đỏ, không đen** |
| `yellow` | số liệu, ví von, câu hỏi dẫn dắt | vàng |
| `cta` | kết video: để lại SĐT, hotline | riêng |
| `highlight` | nhấn lẻ | trắng |

Để trống `variant` là rơi vào vòng xoay màu ngẫu nhiên — `plan.py` sẽ báo `THIEU variant`.
`variant` còn quyết định **cả animation và pool tiếng động**:
`warning` → Zoom_In 0.30s + tiếng CAMERA · còn lại → Fade_In 0.25s.

## 4. Chọn clip

Xem `chon-broll.md`.

---

## Kiểm trước khi chạy tiếp

`python3 <job>/plan.py` in ra cảnh báo. Xử hết trước khi sang bước neo:

| Báo | Nghĩa |
|---|---|
| `chi 0.4s (<0.8s)` | caption quá ngắn — gộp với dòng bên cạnh |
| `dau * le` | thiếu một dấu `*` |
| `THIEU variant` | dòng chưa gán màu |
| `KHONG TIM THAY <file>` | sai đường dẫn, hoặc chưa cắm ổ T7 |
| `lui src_start -> x` | máy tự lùi vì clip không đủ dài — **soát lại**, giây mới có thể rơi vào cảnh khác |
| `-> BO TRONG` | clip ngắn hơn cả caption, đã bỏ. Tìm clip khác |
