# Bắt đầu từ số 0

> Đọc file này nếu bạn vừa được giao bộ công cụ này và **chưa biết gì về nó**.
> Làm hết từ trên xuống, khoảng 30–45 phút (phần lớn là chờ tải).
> Kẹt ở đâu thì mỗi mục có phần **"Nếu hỏng"** ngay bên dưới.

---

## Nó là cái gì

Đưa vào **một video quay sẵn** (người nói trước camera, dọc 9:16).
Nhận về **một project CapCut mở lên sửa tiếp được**, đã có sẵn:

- lời nói đã cắt sạch chỗ vấp, lặp, im lặng
- chữ chạy (caption) đúng nhịp nói, đã tô màu theo ý nghĩa
- dải video minh hoạ (B-roll) chạy trên đỉnh khung
- tiếng động điểm nhấn

**Nó không xuất ra file video.** Nó ra một *project* — bạn vẫn mở CapCut sửa tiếp rồi mới xuất.
Đó là chủ ý: máy làm phần nhàm chán, người quyết phần còn lại.

---

## Bạn cần nhận đủ 2 thứ

| Thứ | Ở đâu | Cỡ |
|---|---|---|
| **1. Code** | link GitHub (repo riêng tư — phải được mời mới thấy) | 12,7 MB |
| **2. Kho video minh hoạ** | link Google Drive | 2,4 GB (bản gọn) |

Thiếu thứ 2 thì công cụ **vẫn chạy, vẫn ra project CapCut — nhưng dải B-roll trống trơn**.

---

## Bước 1 — Máy phải là Mac Apple Silicon

Bấm  Apple  → *About This Mac*. Dòng **Chip** phải là **Apple M1/M2/M3/M4…**

Nếu là **Intel** hoặc **Windows**: bước phiên âm sẽ không chạy được (nó dùng MLX, framework
riêng của Apple). Vẫn dùng được nhưng phải đổi engine phiên âm — xem `CAI-DAT.md` mục 2.

---

## Bước 2 — Cài 4 thứ

Mở **Terminal** (Cmd+Space, gõ "Terminal", Enter). Dán từng khối, Enter, chờ xong mới sang khối kế.

**a. Homebrew** — cái để cài mấy thứ còn lại. Đã có rồi thì bỏ qua.

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

**b. ffmpeg** — bộ xử lý video, gần như mọi bước đều cần.

```bash
brew install ffmpeg
```

**c. mlx_whisper** — nghe video rồi gõ ra chữ, kèm mốc thời gian từng từ.

```bash
pip3 install mlx-whisper
```

**d. Pillow** — thư viện vẽ chữ ra ảnh.

```bash
pip3 install Pillow
```

Và cài **CapCut** cho macOS từ trang chủ, mở lên một lần cho nó tạo thư mục dự án.

> **Nếu hỏng:** `command not found: brew` sau khi cài Homebrew → đóng Terminal, mở lại.
> `pip3: command not found` → thay `pip3` bằng `python3 -m pip`.

---

## Bước 3 — Tải code về

```bash
cd ~/Desktop
git clone <DÁN LINK GITHUB VÀO ĐÂY> DiLiM-video
cd DiLiM-video
```

> **Nếu hỏng:** báo `Repository not found` → repo riêng tư, bạn chưa được mời.
> Nhắn người giao thêm tài khoản GitHub của bạn vào repo.

Rồi dựng môi trường riêng cho bước cuối:

```bash
cd 03-tool-capcut/VectCutAPI
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cd ~/Desktop/DiLiM-video
```

---

## Bước 4 — Đặt kho video minh hoạ

Tải file zip từ Drive, giải nén. Bạn sẽ được một thư mục tên **`02. Dilim Footage`**.

Đặt nó ở đâu cũng được — ổ ngoài, hoặc ngay trong máy. Rồi **chỉ đường cho công cụ**:

```bash
echo 'export DILIM_FOOTAGE="/duong/dan/toi/02. Dilim Footage"' >> ~/.zshrc
source ~/.zshrc
```

Thay `/duong/dan/toi/` bằng chỗ bạn vừa để. Mẹo lấy đường dẫn: kéo thả thư mục
từ Finder vào cửa sổ Terminal, nó tự điền ra.

> **Đừng đổi tên thư mục con bên trong.** Công cụ nhớ đường dẫn tới từng file.

---

## Bước 5 — Kiểm xem đã xong chưa

Chạy từ thư mục `DiLiM-video`:

```bash
python3 -m py_compile 03-tool-capcut/pipeline/*.py
python3 03-tool-capcut/pipeline/test_logic.py
python3 03-tool-capcut/pipeline/clips.py
```

**Phải thấy:**

| Lệnh | Kết quả đúng |
|---|---|
| lệnh 1 | không in ra gì cả |
| lệnh 2 | `== 0 FAIL ==` |
| lệnh 3 | `187 co / 0 mat` |

> **Nếu hỏng:**
> - `khong thay kho B-roll` → sai `DILIM_FOOTAGE` ở bước 4. Kiểm bằng `echo $DILIM_FOOTAGE`.
> - `187 co / 0 mat` ra thành `150 co / 37 mat` → bạn tải **bản gọn**, thiếu vài clip.
>   Vẫn dựng được, chỉ là mấy dòng đó không có hình. Muốn đủ thì xin bản đầy đủ.
> - `ModuleNotFoundError: PIL` → chưa cài Pillow ở bước 2d.

---

## Bước 6 — Dựng thử một video

```bash
mkdir -p 04-du-an/thu-nghiem
ln -s "/duong/dan/toi/video-cua-ban.mp4" 04-du-an/thu-nghiem/source.mp4
```

**Dùng `ln -s` (tạo lối tắt), đừng chép.** File quay thường vài GB.

Rồi chạy lần lượt — mỗi lệnh xong mới chạy lệnh sau:

```bash
J=04-du-an/thu-nghiem
P=03-tool-capcut/pipeline
V=03-tool-capcut/VectCutAPI/.venv/bin/python

python3 $P/1_transcribe.py --job $J     # chậm nhất, ~2,5 lần thời lượng video
```

Giờ mở `04-du-an/thu-nghiem/edit/transcript_readable.txt`, đọc, rồi tự viết file
`04-du-an/thu-nghiem/cuts.json` — liệt kê đoạn nào bỏ:

```json
[ {"t0": 0.0, "t1": 2.4, "why": "câu lạc, chưa vào bài"} ]
```

```bash
python3 $P/2_cut.py          --job $J
python3 $P/3_map_words.py    --job $J
python3 $P/make_plan_draft.py --job $J   # sinh khung plan.py
```

Mở `04-du-an/thu-nghiem/plan.py`, sửa nội dung chữ chạy (đây là phần tốn công nhất, có
người làm cùng thì nhanh). Rồi:

```bash
python3 $J/plan.py
python3 $P/4_anchor.py       --job $J --apply
python3 $P/soi_plan.py       --job $J     # máy soi lỗi, miễn phí
python3 $P/5_render_captions.py --job $J
$V       $P/6_to_capcut.py   --job $J --install
```

**Thoát hẳn CapCut (Cmd+Q) rồi mở lại** — project tên `DiLiM - thu-nghiem`.

---

## Đọc tiếp cái gì

| Muốn gì | Đọc |
|---|---|
| Bảng lệnh đầy đủ + ý nghĩa từng bước | `CLAUDE.md` ở gốc repo |
| Chi tiết cài đặt, chỗ phụ thuộc máy | `CAI-DAT.md` |
| Cách viết chữ chạy cho hay | `.claude/skills/dilim-autocut/references/viet-plan.md` |
| Cách chọn video minh hoạ | `.claude/skills/dilim-autocut/references/chon-broll.md` |
| Cách cắt lời nói | `.claude/skills/dilim-autocut/references/cat-aroll.md` |
| Luật nội dung (từ nào cấm dùng) | `00-huong-dan/01-style-noi-dung-dilim.md` |
| Lịch sử, còn thiếu gì | `03-tool-capcut/VERSION.md` |

**Có 9 job mẫu** trong `04-du-an/` — mỗi cái có `cuts.json` và `plan.py` thật, đã dựng và
được duyệt. Bí chỗ nào thì mở ra xem người trước viết thế nào.

---

## Hai điều dễ làm sai nhất

**1. Chép file quay vào thư mục job.** Dùng `ln -s`. File gốc vài GB, chép là đầy ổ.

**2. Sửa thông số vị trí trong code.** Các con số về vị trí dải B-roll, chữ chạy, logo là
**đo từ CapCut ra**, không phải tính toán. Muốn đổi thì kéo tay trong CapCut trước, rồi đọc
số ra bằng `doc_capcut.py`. Tự quy đổi là đoán — và đã đoán sai một lần rồi.
