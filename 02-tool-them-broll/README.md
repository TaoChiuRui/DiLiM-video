# Gói workflow Tính Media — text + B-roll

Toàn bộ quy trình dựng overlay (chữ + B-roll + tiếng động) cho video DiLiM, đóng gói để chuyển
sang máy khác. Gói này chứa **code, quy tắc, bộ nhớ chọn clip và mẫu job** — không chứa kho footage.

Đọc theo thứ tự: `README.md` (file này) → `docs/WORKFLOW_TINH_MEDIA.md` → `docs/WORKFLOW_DUNG_VIDEO.md`.

---

## ⚠️ TRẠNG THÁI TRÊN MACBOOK NÀY — cập nhật 03/08/2026

Phần "Cài trên máy mới — 6 bước" bên dưới viết cho **máy Windows cũ**. Trên MacBook này
bước 4 và 5 **đã làm xong rồi**, đừng làm lại:

| Bước | Trạng thái |
|---|---|
| 1 · Chép gói | ✅ nằm ở `~/Desktop/DiLiM-video/02-tool-them-broll` |
| 2 · Chép kho footage | 🟡 **một phần** — ổ `T7 for Mac`, thiếu 9 nhóm (xem dưới) |
| 3 · Cài phần mềm | ✅ ffmpeg · ffprobe · PIL · **mlx-whisper** |
| 4 · Sửa `config.json` | ✅ đã trỏ `/Volumes/T7 for Mac/02. Dilim Footage` |
| 5 · Build catalog | ✅ **1.102 file / 21 nhóm** (03/08/2026) |
| 5b · Build broll_memory | ❌ **bỏ qua** — 63 mục đều trỏ file không có trên ổ Mac |
| 6 · Nạp skill + memory | ⬜ chưa làm |

`python3 pipeline/paths.py` → **`=> SAN SANG`**

**Transcribe trên Mac dùng `mlx-whisper`, KHÔNG dùng `faster-whisper`.** Bản Windows dùng
faster-whisper CPU/int8; máy này chạy MLX trên GPU Metal, nhanh hơn nhiều. Đã cài sẵn bằng
`uv tool install mlx-whisper` (v0.4.3), model `whisper-large-v3` + `turbo` đã tải về
(~4.4 GB trong `~/.cache/huggingface`). `paths.py` đã sửa để nhận cả hai.

**Cắm ổ T7 trước khi chạy.** Rút ổ ra là mọi đường dẫn clip trong catalog chết.

**Kho trên Mac ≠ kho Windows.** Đây là bộ file thô chưa đặt tên; kho Windows là bản đã
đổi tên kiểu `049 - Camera xoay quanh mô hình khớp gối…`. Hệ quả:

- Thiếu 9 nhóm: `Đã Chuẩn Hóa`, `Product Broll`, `CTA`, `Ho - Khó Thở`,
  `Nghiện Điện Thoại MXH`, `Thiền - Đọc sách`, `Hàu- Vợ chồng`, `AI`, `Lộn Xộn Xà bần`.
  `catalog.py` tự bỏ qua nhóm không có — sau này tạo nhóm nào thì nhóm đó tự vào catalog,
  không phải sửa code.
- **Không chép `Đã Chuẩn Hóa` cũ sang** — đó là bản chuẩn hoá của người làm trước.
  Sẽ tự chuẩn hoá lại từ kho thô. Chuẩn hoá xong nhớ đặt đúng tên `Đã Chuẩn Hóa`
  ngay dưới `02. Dilim Footage` là `catalog.py` nhận ngay ở priority 0.
- 5 nhóm đổi tên (thêm số đầu): `01 Đau đầu…`, `02 Mạch Máu…`, `04 Đột quỵ`,
  `06 Ngủ- Ngon- mất ngủ` — đã sửa trong `pipeline/catalog.py`.
- Thêm 4 nhóm mới chỉ có trên Mac: `03 Rich_Natto_product`, `Natto Xám`,
  `Khung hình chuyên gia`, `05 Finish part` — đã khai báo trong `pipeline/catalog.py`.
- Nhạc: `Nhạc video quảng cáo` (101 file) · SFX: `Âm Thanh` (28 file).
  Không có thư mục `Music` như kho Windows.

Kiểm tra bất cứ lúc nào:

```bash
python3 pipeline/paths.py
python3 pipeline/catalog.py build    # rebuild trước MỖI job
```

---

## 1. Cài trên máy mới — 6 bước

### Bước 1 — Chép gói
Chép cả thư mục `tinh-media-workflow` vào máy mới. Đặt ở đâu cũng được, không phụ thuộc đường dẫn.

### Bước 2 — Chép 2 kho dữ liệu ngoài (KHÔNG có trong gói)

| Kho | Đường dẫn hiện tại | Vì sao không đóng gói |
|---|---|---|
| **Footage B-roll** | `D:\download\Footage B-roll` | ~3.000 file video/ảnh, hàng trăm GB |
| **Nhạc + SFX** | `D:\download\Footage B-roll\Music` | nằm trong kho trên |

Chép nguyên vẹn **cấu trúc thư mục con** (`Đã Chuẩn Hóa`, `Product Broll`, `Xương khớp - Đau`,
`Mạch Máu - Thần Kinh - TẾ BÀO`, `Ngủ- Ngon- mất ngủ`, `Nhân Viên văn phòng`, `Music`, …) —
tên thư mục có dấu tiếng Việt là **khoá tra cứu** của catalog, đổi tên là hỏng.

### Bước 3 — Cài phần mềm
```bash
pip install -r requirements.txt
```
Thêm **ffmpeg + ffprobe** vào PATH (bắt buộc, không cài bằng pip):
```bash
winget install Gyan.FFmpeg
```

Transcribe chạy `faster-whisper`. Nếu máy mới có GPU NVIDIA và muốn chạy CUDA thì sửa
`config.json` thành `"whisper_device": "cuda"`, `"whisper_compute_type": "float16"` — kèm bẫy
đã gặp: thiếu `cublas64_12.dll` thì cài cuDNN/CUDA runtime hoặc quay về `cpu`/`int8`.

### Bước 4 — Sửa đường dẫn trong `config.json`
Chỉ **một file duy nhất** cần sửa khi đổi máy:
```json
{
  "broll_root": "E:\\Footage B-roll",
  "music_root": "",
  "jobs_root": "",
  "whisper_model": "medium",
  "whisper_device": "cpu",
  "whisper_compute_type": "int8"
}
```
`music_root` để trống = `<broll_root>\Music`. `jobs_root` để trống = `<gói>\jobs`.

Kiểm tra:
```bash
python pipeline/paths.py
```
Phải ra `=> SAN SANG`. Dòng nào `THIEU` thì sửa trước khi đi tiếp.

### Bước 5 — Dựng lại catalog và bộ nhớ B-roll
```bash
python pipeline/catalog.py build
```
`pipeline/broll_catalog.json` kèm theo gói là **ảnh chụp ngày 2026-07-31 với đường dẫn cũ** —
sang máy mới bắt buộc build lại, nếu không mọi đường dẫn clip đều sai.

```bash
python pipeline/broll_memory.py build
```
Ra 63 mục từ 2 job đã được duyệt (`pipeline/jobs/qc_sun_mon`, `pipeline/jobs/sun_khop_khong_biet_keu`).

### Bước 6 — Nạp skill + bộ nhớ cho Claude Code

**Skill** — chép vào thư mục skill của Claude Code:
```bash
cp -r skills/dilim-video-broll skills/vertical-topband-video ~/.claude/skills/
```
(Windows: `%USERPROFILE%\.claude\skills\`)

**Bộ nhớ** — 7 file trong `memory/` là những gì Claude đã học được qua các đợt dựng
(nguyên tắc chọn clip, bản đồ sản phẩm ↔ thư mục, checklist dựng, thư viện nhạc theo cảm xúc,
2 ghi chú về cách làm việc với bạn). Chép vào thư mục memory của project trên máy mới:

```
%USERPROFILE%\.claude\projects\<slug>\memory\
```
`<slug>` = đường dẫn thư mục làm việc, thay `:` và `\` bằng `-`.
Ví dụ mở Claude Code tại `D:\tinh-media-workflow` → slug là `D--tinh-media-workflow`.

Nhớ chép cả `MEMORY.md` (file index Claude đọc mỗi phiên).

**Câu mở đầu dán vào Claude Code trên máy mới:**
> Đọc `README.md`, `docs/WORKFLOW_TINH_MEDIA.md` và `docs/WORKFLOW_DUNG_VIDEO.md` trong thư mục này,
> rồi chạy `python pipeline/paths.py` để kiểm tra cài đặt. Sau đó báo tôi biết đã sẵn sàng và
> đợi tôi gửi video — chưa transcribe gì cả.

---

## 2. Vòng làm việc mỗi video

Chi tiết đầy đủ ở `docs/WORKFLOW_TINH_MEDIA.md`. Tóm tắt: **1 lần gửi file → 1 bảng duyệt gộp → 1 lần dựng**.

```
gửi file  ──►  ① rebuild catalog  ② transcribe word-level  ③ soạn caption + chọn B-roll + đề xuất SFX
          ◄──  ④ BẢNG DUYỆT GỘP (1 file HTML)
sửa bảng  ──►  ⑤ hỏi lại chỗ chưa rõ  ⑥ dựng kế hoạch cuối  ⑦ render + soi frame  ⑧ transcode + tách lớp
          ◄──  overlay_light.mov · text_only.mov · sfx_track.wav · overlay_PRORES4444.mov
```

Script mẫu nằm ở `templates/job/`, đánh số đúng thứ tự chạy. Cách dùng: tạo `jobs/<tên_job>/`,
chép 6 file vào đó, sửa phần đánh dấu `>>> SUA`:

| File | Việc |
|---|---|
| `1_transcribe.py` | faster-whisper, `word_timestamps=True` → `v<N>/{segments,words}.json` |
| `2_clips.py` | khai báo hằng số đường dẫn clip cho chủ đề (ưu tiên `Đã Chuẩn Hóa`) |
| `3_plan.py` | bảng caption + B-roll dạng tuple → `captions/broll_plan/meta/plan.json` |
| `4_make_table.py` | xuất bảng duyệt HTML kèm ảnh preview: `python 4_make_table.py v1 "Tiêu đề" bang_v1.html` |
| `5_build_from_review.py` | áp file JSON người dùng tải về → job files + `sfx_track.wav` |
| `6_render.py` | render 2 lớp riêng (B-roll / TEXT), ProRes 4444, chạy **tuần tự** |

`templates/vi_du_raydel_v1/` là bộ JSON thật của video Raydel V1 (89s, 31 caption) để đối chiếu định dạng.

`templates/extras/` là script tham khảo từ đợt 5 video VR 9.6.2026: dựng track SFX có bù khoảng lặng
đầu file (`vr_build_sfx.py`), gộp bản duyệt (`vr_merge_user.py`), và **vòng học sau mỗi 5 video**
(`vr_learn.py`) — đối chiếu clip Claude chọn vs clip bạn chọn rồi ghi quy luật vào memory.

---

## 3. Cấu trúc gói

```
tinh-media-workflow/
├─ README.md                  file này
├─ config.json                >>> đường dẫn, sửa khi đổi máy
├─ config.example.json        bản gốc để đối chiếu
├─ requirements.txt
├─ docs/
│   ├─ WORKFLOW_TINH_MEDIA.md quy trình chuẩn + cơ chế học sau mỗi 5 video
│   └─ WORKFLOW_DUNG_VIDEO.md 8 giai đoạn chi tiết, kèm lỗi thật đã gặp
├─ memory/                    7 file bộ nhớ Claude + MEMORY.md
├─ skills/
│   ├─ dilim-video-broll/     luật B-roll, style caption, bản đồ sản phẩm, thông số kỹ thuật
│   └─ vertical-topband-video/ format dọc 9:16 dải B-roll trên đỉnh (+ presets/dilim.json)
├─ pipeline/                  lõi dùng lại cho mọi job
│   ├─ paths.py               >>> mọi đường dẫn đọc từ config.json qua đây
│   ├─ catalog.py             build/search/stats kho B-roll
│   ├─ caption_style.py       vẽ caption PNG (font Anton, 6 variant màu)
│   ├─ render_overlay.py      ghép B-roll + caption → ProRes 4444 alpha thật
│   ├─ broll_memory.py/.json  ý → clip ĐÃ ĐƯỢC DUYỆT (63 mục)
│   ├─ concept_map.py         bảng tra ý → clip chủ đề xương khớp
│   ├─ broll_catalog.json     ảnh chụp catalog cũ — BUILD LẠI trên máy mới
│   ├─ fonts/Anton-Regular.ttf
│   └─ jobs/                  JSON của 2 job đã duyệt (nguồn của broll_memory)
├─ templates/
│   ├─ job/                   6 script mẫu, đánh số theo thứ tự chạy
│   ├─ extras/                script tham khảo đợt VR (SFX, merge, học)
│   └─ vi_du_raydel_v1/       bộ JSON thật của 1 video hoàn chỉnh
├─ tools/broll_cataloger.py   cataloger cũ dùng AI vision (tuỳ chọn, cần ANTHROPIC_API_KEY)
└─ jobs/                      thư mục làm việc, để trống
```

## 4. Những gì cố ý KHÔNG đóng gói

- **Kho Footage B-roll và Music** — chép riêng (bước 2)
- **Các bản render cũ** (`renders/`, các `jobs/*/**.mov`, ~440 GB) — không cần để chạy tiếp
- **Model faster-whisper** — tự tải về lần chạy đầu
- **Script one-off của các đợt cũ** (`tests/`, `modules/`) — đã bị thay bằng `pipeline/`,
  giữ lại chỉ gây nhầm. Bản gốc vẫn nằm ở `D:\Claude code\ai_editor` trên máy cũ nếu cần tra.

## 5. Ba luật không được quên

1. **Rebuild catalog trước mỗi job** — catalog là ảnh chụp tĩnh, có thể cũ hơn ổ đĩa.
2. **Quét nhiều mốc trong clip trước khi dùng** — clip hay đổi cảnh giữa chừng; tên file không
   cho biết clip quay gì.
3. **Render tuần tự, một tiến trình một lúc** — 2 tiến trình ghi cùng `render_tmp` sẽ treo máy.
