# Quy trình 3 bước — từ clip thô đến bản đăng

> Trả lời một câu hỏi duy nhất: **bước nào dùng tool nào.**
> Luật nội dung nằm ở `01-style-noi-dung-dilim.md` — đọc trước, đọc mỗi lần.

```
clip thô                bản cắt sạch            bản có caption          bản có B-roll
03-footage-moi/  ──①──► 04-du-an/…/edit/  ──②──► queue/…/edit/    ──③──► overlay ProRes
                     final.mp4              captions_*.mp4          _PRORES4444.mov
                    (tool 1)                  (tool 1 – Dr Sơn)        (tool 2)
```

Bước ③ là tuỳ chọn — chỉ làm khi video cần B-roll minh hoạ.

---

## Bước ① — Cắt (tool `01-tool-cat-video`)

Cắt filler, cắt khoảng lặng, color grade, xuất `final.mp4`.

```bash
cd 04-du-an/<dự-án>
claude
```

Rồi nhắn: *"dựng video bán hàng từ clip trong thư mục này"*.

Output vào `<dự-án>/edit/`: `final.mp4`, `edl.json` (quyết định cắt), `takes_packed.md` (transcript), `verify/` (frame soi lỗi).

**Luật cứng không được phá** (xem đủ 12 luật ở `01-tool-cat-video/SKILL.md`):
- Không cắt giữa chữ — mọi mối cắt phải trùng biên từ trong transcript.
- Chừa 30–200ms mỗi mối cắt.
- Fade âm 30ms mỗi mối, nếu không sẽ nghe "bụp".
- Phụ đề luôn ghép **cuối cùng** trong filter chain, sau mọi overlay.
- Duyệt kế hoạch bằng lời trước, rồi mới đụng vào bản cắt.

## Bước ② — Caption Dr Sơn (vẫn tool `01-tool-cat-video`)

Caption style riêng: màu, chia dòng, nhấn từ khoá, render overlay nền xanh.

```bash
cd 01-tool-cat-video
python batch/new_job.py "<đường-dẫn-final.mp4>" --title "<tên>"
python batch/run_job.py queue/<job-id>
```

Đã có bản cắt ở bước ① rồi thì **không transcribe lại** — chiếu transcript gốc sang timeline đã cắt:

```bash
python batch/tools/edl_map_transcript.py 04-du-an/<dự-án>/edit
```

Output nằm ở `01-tool-cat-video/queue/<job-id>/edit/` (đường dẫn này hardcode trong tool, không dời được).

Luật caption đầy đủ: `01-tool-cat-video/.claude/skills/dr-son/CAPTION_RULES.md`.

## Bước ③ — Thêm B-roll (tool `02-tool-them-broll`)

Chèn B-roll + chữ + tiếng động, xuất ProRes 4444 có alpha thật.

🟡 **Chạy được từ 03/08/2026** — `paths.py` báo `=> SAN SANG`, catalog 1.102 file.
Nhưng kho trên Mac là **kho thô chưa chuẩn hoá**: chưa có `Đã Chuẩn Hóa` (priority 0) và
`Product Broll`, nên 63 mục `broll_memory.json` không dùng được.
Chi tiết ở `README.md` gốc, mục `02-tool-them-broll`.

**Cắm ổ T7 trước khi chạy.** Rút ổ ra là mọi đường dẫn clip trong catalog chết.

```bash
python3 pipeline/paths.py          # kiểm tra
python3 pipeline/catalog.py build  # rebuild trước MỖI job
```

Vòng làm việc — **1 lần gửi file → 1 bảng duyệt gộp → 1 lần dựng**:

```
gửi file ─► ① rebuild catalog  ② transcribe word-level  ③ soạn caption + chọn B-roll + đề xuất SFX
         ◄─ ④ BẢNG DUYỆT GỘP (1 file HTML)
sửa bảng ─► ⑤ hỏi lại chỗ chưa rõ  ⑥ kế hoạch cuối  ⑦ render + soi frame  ⑧ transcode + tách lớp
         ◄─ overlay_light.mov · text_only.mov · sfx_track.wav · overlay_PRORES4444.mov
```

Script mẫu: `02-tool-them-broll/templates/job/` — 6 file đánh số theo đúng thứ tự chạy. Tạo `jobs/<tên_job>/`, chép 6 file vào, sửa chỗ đánh dấu `>>> SUA`.

**Ba luật không được quên:**
1. Rebuild catalog trước mỗi job — catalog là ảnh chụp tĩnh, có thể cũ hơn ổ đĩa.
2. Quét nhiều mốc trong clip trước khi dùng — clip hay đổi cảnh giữa chừng, tên file không cho biết clip quay gì.
3. Render tuần tự, một tiến trình một lúc — 2 tiến trình ghi cùng `render_tmp` sẽ treo máy.

---

---

## Hai bộ transcribe — biết dùng cái nào

| | ElevenLabs Scribe | mlx-whisper |
|---|---|---|
| Chạy ở đâu | API, cần mạng + `ELEVENLABS_API_KEY` (đã có trong `01-tool-cat-video/.env`) | **local**, GPU Metal của Mac |
| Ai gọi | `01-tool-cat-video/helpers/transcribe.py` (mặc định của video-use) | gọi tay: `mlx_whisper` |
| Được gì | **timestamp từng chữ** + tách người nói + sự kiện âm thanh `(cười)` | `{text, segments, language}` — timestamp theo câu |
| Dùng khi | **bước ① cắt** — luật "không cắt giữa chữ" cần timestamp từng chữ | nội dung dài, không muốn tốn API, chỉ cần bản chữ để đọc |

Bản DSCF1553 tuần trước transcribe bằng **mlx-whisper** (`large-v3`), ra
`edit/transcripts_v2/audio16k.json`. Model đã tải sẵn ~4.4 GB trong `~/.cache/huggingface`.

```bash
mlx_whisper audio16k.wav --model mlx-community/whisper-large-v3-mlx \
  --language vi --output-format json --output-dir transcripts_v2
```

⚠️ mlx-whisper **không cho timestamp từng chữ**. Muốn cắt đúng biên từ thì phải dùng Scribe,
hoặc chấp nhận cắt theo biên câu.

---

## Đặt tên dự án mới

```
04-du-an/<số thứ tự>-<ngày quay yyyy-mm-dd>-<tên file gốc viết thường>/
```

Ví dụ: `02-2026-08-15-dscf1601/`

Bên trong **bắt buộc** giữ tên thư mục `edit/` — cả 2 tool đều quy ước ghi output vào `<thư-mục-video>/edit/`.
