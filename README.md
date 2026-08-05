> ⚠ **Ổ T7 đang hỏng (05/08/2026)** — đọc [`DOC-KHI-CO-CAP-MOI.md`](DOC-KHI-CO-CAP-MOI.md) trước khi cắm ổ vào.

> **Người mới:** đọc [`BAT-DAU.md`](BAT-DAU.md) — cài đặt từ số 0, có phần "nếu hỏng" ở mỗi bước.
> Cài chi tiết + chỗ phụ thuộc máy: [`CAI-DAT.md`](CAI-DAT.md).

# DiLiM-video — bản đồ thư mục

> Đọc file này trước. Mỗi thư mục có **một** việc, không lẫn nhau.

```
DiLiM-video/
├─ README.md              ← file này
├─ CLAUDE.md              ← Claude đọc file này mỗi phiên: bảng lệnh + file cấm đọc
├─ .claude/skills/        ← skill `dilim-autocut` (đã nối vào ~/.claude/skills/)
├─ 00-huong-dan/          ← đọc trước khi dựng (style + quy trình)
├─ 01-tool-cat-video/     ← TOOL 1: cắt, ghép, grade, caption Dr Sơn
├─ 02-tool-them-broll/    ← TOOL 2: engine vẽ caption + kho B-roll
├─ 03-tool-capcut/        ← TOOL 3: dựng thẳng project CapCut  ★ dùng chính
├─ 04-du-an/              ← dữ liệu từng video đã/đang dựng
└─ 05-footage-moi/        ← thả clip mới quay vào đây
```

---

## Ba loại thư mục, đừng lẫn

| Loại | Thư mục | Nội dung |
|---|---|---|
| **Tài liệu** | `00-huong-dan/` | luật nội dung + quy trình. Không có code. |
| **Tool** | `01-…`, `02-…`, `03-…` | code chạy được. **Không bỏ video vào đây.** |
| **Dữ liệu** | `04-du-an/`, `05-footage-moi/` | video thô và bản dựng. |

**Luồng đang dùng là TOOL 3.** Nó gọi engine caption của tool 2. Tool 1 giữ làm đường lùi.

---

## 00-huong-dan/

| File | Nội dung |
|---|---|
| `01-style-noi-dung-dilim.md` | Công thức 10 khối video bán hàng "form bác Sơn", giọng văn, luật cấm từ ("phục hồi/bảo vệ", KHÔNG "chữa lành/điều trị"), nhịp cắt. **Đọc trước mỗi lần dựng.** |
| `02-quy-trinh-3-buoc.md` | Đi từ clip thô đến bản đăng: dùng tool nào ở bước nào. |

## 01-tool-cat-video/  (tên gốc: `video-use`)

Repo mã nguồn mở `browser-use/video-use` — **vẫn là git repo, có remote upstream**. Đã gộp thêm bộ caption **Dr Sơn** của DiLiM vào ngày 01/08/2026.

Làm 2 việc:

| Việc | Đọc file nào |
|---|---|
| Cắt / ghép / color grade / transcribe → `final.mp4` | `SKILL.md`, `helpers/` |
| Caption style Dr Sơn (màu, chia dòng, nhấn từ khoá, render overlay) | `SETUP_README.md`, `.claude/skills/dr-son/`, `batch/`, `remotion-video/` |

**Cầu nối 2 bộ:** `batch/tools/edl_map_transcript.py` — chiếu transcript gốc qua `edl.json` sang timeline bản đã cắt, khỏi transcribe lại.

⚠️ **Không đổi tên gì bên trong thư mục này.** Mọi đường dẫn trong tài liệu và script Dr Sơn đều tính từ gốc repo. Skill đã được nối vào Claude Code bằng symlink:
`~/.claude/skills/video-use` → `01-tool-cat-video/`

⚠️ **`01-tool-cat-video/queue/` là thư mục job của bộ Dr Sơn** — đường dẫn `REPO_ROOT/queue` bị hardcode trong `batch/webapp/jobs.py`, **không dời ra ngoài được**. 3 job `dscf1553-2207-*` đang nằm trong đó là **bản chạy thử**, không phải bản giao (chiếm 764 MB — xoá được khi cần chỗ).

## 02-tool-them-broll/  (tên gốc: `tinh-media-workflow`)

Bộ dựng overlay: **chữ + B-roll + tiếng động**, xuất ProRes 4444 có alpha thật. Gói mang từ máy Windows sang.

Đọc theo thứ tự: `README.md` → `docs/WORKFLOW_TINH_MEDIA.md` → `docs/WORKFLOW_DUNG_VIDEO.md`.

🟡 **Chạy được, nhưng kho B-roll trên Mac nhỏ hơn kho Windows cũ.** (Cập nhật 03/08/2026)

Đã trỏ sang ổ ngoài và build lại catalog: **1.102 file / 21 nhóm**.

```
broll_root  = /Volumes/T7 for Mac/02. Dilim Footage
music_root  = .../Nhạc video quảng cáo   (101 file)
SFX         = .../Âm Thanh               (28 file)
```

Kiểm tra bất cứ lúc nào: `python3 pipeline/paths.py`

**Còn thiếu so với kho Windows — 9 nhóm chưa chép sang**, trong đó 2 nhóm quan trọng nhất:

| Nhóm thiếu | Vai trò |
|---|---|
| `Đã Chuẩn Hóa` | kho tự đặt tên theo Ý, **priority 0 — luôn tìm ở đây trước** |
| `Product Broll` | ảnh/video sản phẩm thật, dùng khi caption nhắc tên sản phẩm |

Thiếu thêm: `CTA`, `Ho - Khó Thở`, `Nghiện Điện Thoại MXH`, `Thiền - Đọc sách`, `Hàu- Vợ chồng`, `AI`, `Lộn Xộn Xà bần`.
`catalog.py` tự bỏ qua nhóm không tồn tại — chép sang là chạy được ngay, không phải sửa code.

**Không cần chép `Đã Chuẩn Hóa` cũ sang** — đó là bản chuẩn hoá của người làm trước, sẽ tự chuẩn hoá lại từ kho thô trên ổ T7.

⚠️ **`pipeline/broll_memory.json` (63 clip đã duyệt) không dùng được trên máy này.** Bộ nhớ học từ 2 job xương khớp trên máy Windows, trỏ vào các file đã đổi tên kiểu `049 - Camera xoay quanh mô hình khớp gối…` — kho thô trên Mac không có file nào như vậy. Thử ánh xạ lại đường dẫn chỉ cứu được 3/63, nên để nguyên. Chuẩn hoá lại kho xong thì build bộ nhớ mới từ các job được duyệt trên máy này.

## 05-footage-moi/

Thả clip mới quay vào đây. File gốc không bao giờ bị sửa. Dựng xong thì chuyển sang một thư mục con trong `04-du-an/`.

## 03-tool-capcut/  ★ luồng đang dùng

Nhận video (thô hoặc đã cắt) → ra **project CapCut hoàn chỉnh**: A-roll đã cắt, dải B-roll trên đỉnh, caption style DiLiM, animation. Mở CapCut lên sửa tiếp được.

8 script trong `pipeline/`, **dùng chung cho mọi job**, truyền `--job <thư-mục>` — không chép script vào từng job.

Chi tiết + 4 cái bẫy đã gỡ: đọc `03-tool-capcut/README.md`.

Không chạy server, không mở cổng, không gửi gì ra ngoài.

## 04-du-an/

Mỗi video một thư mục, đặt tên `<số>-<ngày quay>-<tên file gốc>`:

```
04-du-an/
└─ 01-2026-07-22-dscf1553/
    ├─ README.md    ← job này gồm gì, output nào ở đâu
    └─ edit/        ← output của tool 1 (tên `edit/` là bắt buộc, tool ghi vào đây)
```

⚠️ Giữ nguyên tên thư mục con `edit/` — cả 2 tool đều quy ước ghi output vào `<thư-mục-video>/edit/`.
