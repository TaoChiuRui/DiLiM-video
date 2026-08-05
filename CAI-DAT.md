# Cài đặt trên máy khác

> Soạn 05/08/2026 khi soát lại luồng để đóng gói. Mọi con số dưới đây đo trên máy anh Thành, không phải ước lượng.

---

## 1. Bàn giao gồm HAI phần, đi hai đường khác nhau

| Phần | Cỡ | Đường đi |
|---|---:|---|
| **Code + tài liệu + kho kiến thức** | **12,7 MB · 360 file** | git (clone) |
| **Kho footage B-roll** | ~1.100 file, ổ ngoài | chép ổ cứng — không có cách khác |

> **Code chỉ là phần nhỏ.** `clips.py` khai 187 clip trỏ vào file cụ thể trong kho footage;
> `kho_broll.json` là chỉ mục của chính kho đó. **Có code mà không có kho thì pipeline vẫn
> chạy, vẫn ra project CapCut — nhưng mọi dải B-roll trống trơn.**

Cái gì **không** vào git (đã cấu hình sẵn trong `.gitignore`):
`04-du-an/` (15,8 GB job đã dựng) · `node_modules/` (1,3 GB) · `01-tool-cat-video/queue/`
(~700 MB render cũ) · `.venv/` · `05-footage-moi/`.

Riêng `04-du-an/` **giữ lại `cuts.json` + `plan.py` của 9 job** (17 file, 121 KB) — đó là hai
file duy nhất mỗi job phải viết tay, để lại làm ví dụ thật cho người mới.

> **Ba thư mục tool phải đi cùng nhau.** Tool 3 gọi thẳng sang tool 1 và tool 2 bằng đường dẫn
> tương đối (`../../01-tool-cat-video/...`, `../../02-tool-them-broll/...`). Bê mỗi
> `03-tool-capcut/` sang là gãy ngay bước ⑫ (vẽ caption) và mất hết SFX.

> **Ba thư mục phải đi cùng nhau.** Tool 3 gọi thẳng sang tool 1 và tool 2 bằng đường dẫn tương đối
> (`../../01-tool-cat-video/...`, `../../02-tool-them-broll/...`). Bê mỗi `03-tool-capcut/` sang là
> gãy ngay bước ⑫ (vẽ caption) và mất hết SFX.

---

## 2. Cần sẵn trên máy

| Thứ | Kiểm | Bắt buộc ở bước |
|---|---|---|
| **ffmpeg + ffprobe** | `ffmpeg -version` | ①②③⑩⑫ — gần như mọi bước |
| **python3 + Pillow** | `python3 -c "import PIL"` | ⑫ vẽ caption, ⑩ bảng duyệt |
| **mlx_whisper** | `mlx_whisper --help` | ① phiên âm |
| **CapCut** | có thư mục `~/Movies/CapCut/User Data/Projects/com.lveditor.draft` | ⑬ |
| **venv VectCutAPI** | `03-tool-capcut/VectCutAPI/.venv/bin/python -c "import imageio"` | ⑬ |
| `swiftc` (Xcode CLT) | `swiftc -version` | chỉ `xay_kho_broll.py` (OCR kho) |

### ⚠ `mlx_whisper` chỉ chạy trên Mac Apple Silicon

MLX là framework của Apple, **không có trên Intel Mac và Windows**. Máy khác phải đổi engine phiên âm.

Các bước sau **không quan tâm engine nào** — chúng chỉ cần file JSON có `segments[].words[].start`.
Thay bằng `openai-whisper` hoặc `faster-whisper` cũng được, miễn giữ đúng định dạng đó. Chỗ cần sửa
là `1_transcribe.py`, đã ghi comment ngay tại dòng gọi.

```bash
pip install mlx-whisper            # Mac Apple Silicon
export MLX_WHISPER=/duong/dan/khac # nếu cài chỗ khác
```

### venv của VectCutAPI

Chỉ bước ⑬ dùng. Đã có sẵn `imageio 2.37`, `Pillow 12.3`, `numpy 2.5`.
Thư viện `pyJianYingDraft` **nằm luôn trong `VectCutAPI/`**, không cài qua pip — nên đi theo repo, không lo phiên bản.

```bash
cd 03-tool-capcut/VectCutAPI && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

---

## 3. Hai biến môi trường

```bash
export DILIM_FOOTAGE="/Volumes/<tên ổ>/02. Dilim Footage"   # kho B-roll
export MLX_WHISPER="/duong/dan/toi/mlx_whisper"             # chỉ khi cài chỗ lạ
```

Không đặt `DILIM_FOOTAGE` thì mặc định `/Volumes/T7 for Mac/02. Dilim Footage`.

---

## 4. Kiểm máy mới — 4 lệnh

Chạy từ gốc repo. Cả 4 phải xanh thì mới dựng được.

```bash
python3 -m py_compile 03-tool-capcut/pipeline/*.py    # 1. cú pháp
python3 03-tool-capcut/pipeline/test_logic.py         # 2. phải ra "0 FAIL"
python3 03-tool-capcut/pipeline/clips.py              # 3. phải ra "187 co / 0 mat"
ffmpeg -version >/dev/null && python3 -c "import PIL" # 4. binary + thư viện
```

Lệnh 3 ra `MAT` nghĩa là **chưa thấy kho B-roll** — cắm ổ, hoặc đặt `DILIM_FOOTAGE`.

---

## 5. `--job` nhận cả 4 dạng

Từ 05/08/2026 mọi script dùng chung một bộ giải tên (`pipeline/job_path.py`).
Trước đó có **hai khuôn khác nhau** không ai ghi ra giấy, đưa nhầm là báo lỗi khó hiểu.

```bash
--job 04-du-an/07-2026-08-03-dji0485    # đường dẫn tương đối
--job /duong/dan/tuyet/doi/07-...       # đường dẫn tuyệt đối
--job 07-2026-08-03-dji0485             # tên thư mục trần
--job dji0485                           # một mảnh tên, miễn là duy nhất
```

Không tìm thấy thì nó in ra **đã thử những đường nào**; khớp nhiều job thì liệt kê để chọn lại.

---

## 6. Hai thư mục vốn là repo của người khác

`01-tool-cat-video/` và `03-tool-capcut/VectCutAPI/` là **bản clone từ upstream**, không phải
code nhà mình:

| Thư mục | Upstream | Commit khi lấy về |
|---|---|---|
| `01-tool-cat-video/` | `github.com/browser-use/video-use` | `92c2b34` |
| `03-tool-capcut/VectCutAPI/` | `github.com/sun-guannan/VectCutAPI` | `c12b8e3` |

`.git` của chúng đã **đổi tên thành `.git_upstream`** (không xoá) và bị ignore.

**Vì sao phải làm vậy:** để nguyên `.git` thì git cha coi cả thư mục là *gitlink* — commit chỉ
ghi một con trỏ, không ghi nội dung. Người nhận clone về sẽ thấy **thư mục trống rỗng**.
Đã vấp đúng lỗi này ngày 05/08/2026: **52 file SFX mà tool 3 cần lặng lẽ không vào commit**,
trong khi `git check-ignore` vẫn khẳng định chúng không bị chặn. Mất một lúc mới ra.

Muốn nối lại với upstream thì đổi tên ngược về `.git`.

## 7. Chỗ còn phụ thuộc máy anh Thành

Biết trước để khỏi mất công dò:

- **`~/Movies/CapCut/...`** — đường dẫn draft của CapCut bản macOS. CapCut Windows để chỗ khác.
  Nằm ở `6_to_capcut.py`, `backtest.py`, `doc_capcut.py`, `hoc_lich_su.py`, `de_xuat_cat.py`.
- **Tên file trong `clips.py`** gắn với cách anh Thành đặt tên kho. Kho khác thì phải khai lại.
- **Thông số vị trí** (dải B-roll, caption, logo) là số anh kéo tay trong CapCut rồi đọc ra.
  Khung hình khác 9:16 thì phải đo lại bằng `doc_capcut.py`.
- **Kho kiến thức tự dày lên sẽ phân nhánh.** `kho_caption.json`, `kho_broll.json` và
  `clips.py` lớn dần mỗi lần chạy `kho_caption.py --gom` / `hoc_lich_su.py`. Hai người chạy
  trên hai bộ job khác nhau là chúng tách đôi, merge rất khổ. **Chốt trước một người giữ**,
  hoặc chấp nhận mỗi máy một kho riêng.

---

## 8. Còn thiếu, biết rồi mà chưa làm

Danh sách đầy đủ ở `03-tool-capcut/VERSION.md` mục **Còn thiếu**. Hai cái ảnh hưởng người dùng mới nhiều nhất:

- **Không có regression check thật.** `test_logic.py` kiểm luật trên `plan.json`, **không** dựng lại
  draft rồi so với bản đã duyệt. Sửa `6_to_capcut.py` xong phải tự dựng lại vài job cũ mà đối chiếu:

  ```bash
  V=03-tool-capcut/VectCutAPI/.venv/bin/python
  for j in dscf0894 natto-hoat-huyet magie-canxi; do $V 03-tool-capcut/pipeline/6_to_capcut.py --job $j; done
  ```

  **Bỏ `--install`** — có nó là ghi đè lên draft anh Thành đang sửa dở trong CapCut.

- **Số thứ tự job đang trùng.** Hiện có 3 job số `04-` và 2 job số `05-`. Không làm chết script
  nhưng `--job 04` sẽ khớp nhiều cái. Đặt tên mới thì giữ số duy nhất.
