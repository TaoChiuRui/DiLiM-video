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

## 1b. ĐỪNG chẻ nhỏ nhịp máy đã chia

> Anh Thành 05/08/2026: *"caption bạn làm là chữ nào cũng làm. Giảm bớt lại 20%,
> chỉ đoạn quan trọng cần thiết để đỡ rối, tăng tốc độ"*.

**Đo được:** job `07-dji0485` — `make_plan_draft.py` đề xuất **45 nhịp (3,6 s/caption)**,
tôi viết ra **68 nhịp (2,4 s/caption)**. Nhiều hơn máy đề xuất **51%**.

Đối chiếu 8 job khác: trung bình **3,6–4,4 s/caption**. Job 07 là bài dày nhất kho, và
nó dày vì tôi tự tách thêm chứ không phải máy chia sai.

| | |
|---|---|
| Máy chia | bám khoảng lặng + dấu câu, đã chỉnh theo 5 job thật |
| Tôi hay làm sai | thấy một câu dài thì tách đôi cho "dễ đọc" |

**Luật:** `MINL, MAXL = 3.0, 6.5` trong `make_plan_draft.py` là ngưỡng đã đo, không phải
gợi ý. **Giữ nguyên số nhịp máy chia.** Chỉ tách thêm khi nhịp đó chứa **hai ý tách bạch**
mà gộp lại sẽ sai nghĩa — không phải vì nó dài.

**Được phép GỘP, hiếm khi được TÁCH.** Gộp khi:
- nhịp dưới 1,5 s (chớp mắt là mất, mắt chưa kịp bắt)
- là tiếng đệm không mang tin: *"Đúng không cô chú anh chị?"*, *"Vâng"*, *"Nên á"*
- lặp lại ý của nhịp ngay trước

**Vì sao thưa lại tốt hơn:** caption là **điểm tựa cho mắt**, không phải phụ đề. Dày quá thì
mắt bận đọc, không kịp nhìn hình — mà hình mới là thứ giữ người xem. Bỏ bớt caption ở đoạn
lời nói đã rõ thì mấy caption còn lại đập mạnh hơn.

## 1c. Chữ KHÔNG phủ kín 100% thời lượng — bật `giu=True`

> Anh Thành 06/08/2026: *"tôi thấy bạn dùng vẫn full dòng caption… có cắt bớt được một
> cách logic không?"* rồi chốt lại: *"chữ để dài hơn chút, dài đến sát cái caption sau
> cũng được. vì mình đang nói ý key mà"*.

Mặc định `t_end` của caption này = `t` của caption kế tiếp → **chữ phủ 100% thời lượng
theo thiết kế**. Xoá bớt dòng KHÔNG tạo khoảng thở, nó chỉ làm dòng trước phình ra
(job 08: 6 caption thành 8–13 giây). Đây là chỗ tôi sửa sai tầng hai vòng liền.

Cuối bảng `R`, gọi:

```python
build(HERE, R, giu=True)
```

Nó tách `cap_end` (lúc CHỮ tắt) khỏi `t_end` (B-roll vẫn chạy liền mạch — **đừng cho
B-roll tắt theo chữ**). Luật: giữ tới sát dòng sau, chừa `NHAY` = 0.30s, chặn trên
`GIU_MAX` = 7.0s.

Số đối chiếu job 08: 92 caption · **93% chữ trên màn** · mỗi cái hiện 0.8–7.0s
(trung vị 3.9) · hở 0.30–0.90s giữa hai caption.

**Đã thử và BỎ:** tính thời gian đọc (`0.9 + số ký tự/14`, kẹp 1.6–4.2s) → 65% chữ trên
màn, anh thấy chữ tắt quá sớm. Caption đã lọc còn toàn ý key thì không có lý do bắt nó
tắt sớm.

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
