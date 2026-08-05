# Tool 3 — DiLiM AutoCut v1.0

> Giới thiệu ngắn + con số: đọc `VERSION.md`

Nhận video (thô hoặc đã cắt) → ra một **project CapCut hoàn chỉnh**: A-roll đã cắt, dải B-roll trên đỉnh, caption style DiLiM, animation. Mở CapCut lên là sửa tiếp được.

Không chạy server, không mở cổng, không gửi gì ra ngoài. Chỉ import thư viện `pyJianYingDraft` rồi ghi thẳng file draft.

---

## Chạy

Mọi script dùng chung, **truyền `--job`** — không chép script vào từng job nữa.

```bash
cd ~/Desktop/DiLiM-video
J=04-du-an/03-2026-06-28-dscf0894
V=03-tool-capcut/VectCutAPI/.venv/bin/python
P=03-tool-capcut/pipeline
```

| Bước | Lệnh | Ra gì |
|---|---|---|
| ① tách tiếng + transcribe | `python3 $P/1_transcribe.py --job $J` | `edit/transcripts_words/`, `transcript_readable.txt` |
| — soạn bản cắt | *(tự viết `<job>/cuts.json`)* | |
| ② bảng duyệt bản cắt | `python3 $P/make_cut_table.py --job $J` | `edit/bang_cat.html` |
| ③ cắt A-roll | `python3 $P/2_cut.py --job $J` | `edit/final.mp4`, `edit/edl.json` |
| ④ chiếu mốc sang bản cắt | `python3 $P/3_map_words.py --job $J` | `edit/words_cut.json` |
| ⑤ sinh khung caption | `python3 $P/make_plan_draft.py --job $J` | **`<job>/plan.py`** — nhịp + mốc `t` sẵn |
| — soạn caption | *(cô đọng chữ, đánh `*từ khoá*`, soát `variant`)* | |
| ⑥ dựng plan | `python3 $J/plan.py` | `edit/plan.json` |
| ⑦ gợi ý B-roll | `python3 $P/suggest_clips.py --job $J --md` | `edit/goi_y_clip.md` |
| — chọn clip | *(điền clip vào `plan.py`, chạy lại ⑥)* | |
| ⑧ bắt cue theo từ khoá | `python3 $P/4_anchor.py --job $J --apply` | ghi đè `edit/plan.json` |
| ⑨ chống lặp B-roll | `python3 $P/4b_vary.py --job $J --apply` | ghi đè `edit/plan.json` |
| ⑩ bảng duyệt caption/B-roll | `python3 $P/make_review_table.py --job $J` | `edit/bang_duyet.html` |
| — anh duyệt | *(sửa bảng → «TẢI JSON VỀ» → `duyet.json`)* | |
| ⑪ chấm điểm + áp bản duyệt | `python3 $P/apply_duyet.py --job $J --apply` | `edit/diem.md`, `BAI_HOC.md` |
| ⑫ vẽ caption PNG | `python3 $P/5_render_captions.py --job $J` | `edit/captions_png/` |
| ⑬ dựng draft | `$V $P/6_to_capcut.py --job $J --install` | project trong CapCut |

Bước ⑬ **phải dùng `$V`** (venv của VectCutAPI), các bước khác dùng `python3` hệ thống.

Bước ⑤⑦⑨⑪ thêm ngày 04/08/2026. Bỏ qua vẫn chạy được, nhưng ⑤⑦ là hai bước rẻ nhất
trong cả chuỗi và ⑪ là thứ duy nhất cho biết tool đang tốt lên hay tệ đi.

Tên project CapCut = `DiLiM - <tên thư mục job>`.

## Hai file mỗi job phải tự viết

**`<job>/cuts.json`** — đoạn nào bị bỏ:

```json
[ {"t0": 0.0,   "t1": 2.38,  "why": "câu lạc, chưa vào bài"},
  {"t0": 190.9, "t1": null,  "why": "đuôi thừa"} ]
```
`t1: null` = cắt đến hết video.

**`<job>/plan.py`** — nội dung caption + chọn B-roll. **Không chép từ job cũ nữa** — chạy bước ⑤ để sinh khung rồi sửa. Định dạng mỗi dòng:
```python
(t, "DÒNG 1 CÓ *TỪ KHOÁ*", "DÒNG 2", "variant", CLIP, src_start, "ghi chú")
```
`t` do bước ⑤ đặt sẵn bằng `start` của chữ thật — đừng sửa tay; bước ⑧ còn neo lại lần nữa sau khi chữ được cô đọng. `variant`: `warning` `positive` `product` `cta` `yellow` `highlight`. Để `""` ở chỗ clip nghĩa là caption đó không có B-roll — **chấp nhận được**, tốt hơn nhét clip sai ý.

Phần logic dựng `plan.json` giờ nằm chung ở `pipeline/plan_build.py`; `plan.py` mới chỉ còn **bảng R + 3 dòng gọi**. Các `plan.py` cũ giữ bản chép riêng của chúng, vẫn chạy được.

Cách viết caption, bảng màu, 4 luật chọn clip: **skill `dilim-autocut`**.

---

## Bốn cái bẫy đã gỡ (đừng gỡ ra)

**1. `end` của whisper không đáng tin.** Nó kéo dài chữ để nuốt khoảng lặng phía sau — chữ *"những"* bị ghi dài 1 giây. Mọi tính toán **chỉ bám `start`**. Đây là lý do bước ⑤ tồn tại.

**2. Ảnh bị gán cứng `width=height=0`.** `Video_material` nhánh `photo` gán 0 rồi `return` ngay, bỏ qua tham số truyền vào ([local_materials.py:126](VectCutAPI/pyJianYingDraft/local_materials.py)). CapCut coi kích thước 0 là chưa link được. Phải đọc bằng PIL rồi ghi đè sau khi tạo object.

**3. Sandbox — nặng nhất.** macOS chặn `~/Desktop`, `~/Documents`, `~/Downloads` và ổ ngoài; **`~/Movies` thì không**. Ghi thẳng đường dẫn Desktop vào JSON thì CapCut có địa chỉ nhưng không có "vé" → *"File not accessible"*. Cách gỡ: bước ⑧ tự chép media vào `<draft>/dilim_media/` rồi trỏ đường dẫn dạng container. Desktop và `~/Movies` cùng ổ APFS nên là clone, tốn 0 byte.

**4. Template mang metadata máy tác giả gốc** (`draft_name` = "0707", `/Users/sunguannan/...`). Bước ⑧ tự sửa tên, đường dẫn, `draft_id`, thời gian, ảnh bìa.

## Thông số đã chốt

```
# dải B-roll (anh Thành chỉnh tay 03/08, 29/31 clip dùng bộ này)
mask Split · width 0.28 · height 0.0
centerX -0.107502 · centerY -0.705959 · feather 0.283066
transform_y 0.6834 · scale 1.0
^ so nay da doi 2 lan. Nguon dung: MASK_* trong 6_to_capcut.py

# caption
transform_y 0.154523          # UI CapCut hiện Y = 297
LEAD 0.5s                     # chữ hiện trước chữ đầu tiên 0.5 giây

# animation — tệp khách là người có tuổi, bỏ hết kiểu trượt
warning  -> Zoom_In  0.30s
còn lại  -> Fade_In  0.25s
                              # không dài quá 1/3 độ dài caption
```

Style caption (font Anton, 3 họ màu) lấy từ `02-tool-them-broll/pipeline/caption_style.py` — **không sửa ở đây**, sửa bên đó.

## Thư mục

```
03-tool-capcut/
├─ README.md          file này
├─ VERSION.md         phiên bản + còn thiếu gì
├─ BAI_HOC.md         anh Thành đã sửa gì, vì sao — apply_duyet.py tự gom vào
├─ VectCutAPI/        thư viện pyJianYingDraft + .venv
└─ pipeline/          script dùng chung, nhận --job
```

| Script | Việc |
|---|---|
| `1_transcribe` `2_cut` `3_map_words` | tách tiếng → cắt A-roll → chiếu mốc |
| `4_anchor` `4b_vary` | neo caption vào chữ thật · đổi clip bị lặp |
| `5_render_captions` `6_to_capcut` | vẽ PNG → ghi draft CapCut |
| `make_cut_table` `make_review_table` | 2 bảng HTML cho anh duyệt |
| `make_plan_draft` | sinh khung `plan.py` từ `words_cut.json` |
| `suggest_clips` | tra B-roll bằng `clips.TAGS` |
| `doc_capcut` | đọc số thật từ draft anh Thành đã chỉnh tay |
| `soi_plan` | máy soi `plan.json` — lỗi kiểm được bằng luật |
| `soi_frames` | ghép frame B-roll thành contact sheet cho agent nhìn |
| `apply_duyet` | chấm điểm bản duyệt + gom bài học |
| `clips` `plan_build` `sfx` | thư viện dùng chung, không chạy riêng |
