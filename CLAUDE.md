# DiLiM-video

Dựng video bán hàng dọc 9:16 cho DiLiM Supplement. Đọc `README.md` để biết bản đồ thư mục.

**Luồng đang dùng là TOOL 3** (`03-tool-capcut/`) — ra project CapCut sửa tiếp được.
Tool 1 là đường lùi, tool 2 chỉ còn dùng làm engine vẽ caption. Đừng tự ý quay về tool 1.

Có skill `dilim-autocut` — **gọi nó trước khi dựng bất kỳ video nào.**

---

## ĐỪNG BAO GIỜ `Read` mấy file này

Đọc là nổ context, không được gì:

| File | Vì sao |
|---|---|
| `**/edit/bang_duyet.html` | 600 KB ảnh base64 — **dành cho mắt anh Thành**, không phải cho model |
| `**/edit/bang_cat.html` | như trên |
| `02-tool-them-broll/pipeline/broll_catalog.json` | 415 KB. Muốn tra clip thì chạy `suggest_clips.py`, đừng đọc catalog |
| `**/edit/words_cut.json`, `**/transcripts_words/*.json` | timestamp từng chữ, chỉ script đọc. Người đọc thì đọc `transcript_cut.txt` |
| `**/edit/plan.json` | bản sinh ra từ `plan.py`. Sửa thì sửa `plan.py` |
| `.venv/`, `node_modules/` | |

Cần biết trong file có gì thì `grep`/`python3 -c` lấy đúng phần cần, đừng đọc cả file.

## Chạy — Tool 3

```bash
J=04-du-an/<tên-job>
P=03-tool-capcut/pipeline
V=03-tool-capcut/VectCutAPI/.venv/bin/python
```

| # | Lệnh | Ra gì |
|---|---|---|
| ① | `python3 $P/1_transcribe.py --job $J` | transcript word-level |
| — | *tự viết `<job>/cuts.json`* | đoạn nào bỏ |
| ② | `python3 $P/make_cut_table.py --job $J` | `bang_cat.html` — anh duyệt |
| ③ | `python3 $P/2_cut.py --job $J` | `final.mp4`, `edl.json` |
| ④ | `python3 $P/3_map_words.py --job $J` | `words_cut.json`, `transcript_cut.txt` |
| ⑤ | `python3 $P/make_plan_draft.py --job $J` | **khung `plan.py`** — chia nhịp + mốc `t` sẵn |
| — | *cô đọng chữ, đánh `*từ khoá*`, soát `variant`* | |
| ⑥ | `python3 $J/plan.py` | `plan.json` |
| ⑦ | `python3 $P/suggest_clips.py --job $J --md` | `goi_y_clip.md` — gợi ý B-roll |
| — | *điền clip vào `plan.py`, chạy lại ⑥* | |
| ⑧ | `python3 $P/4_anchor.py --job $J --apply` | neo caption vào chữ thật |
| ⑨ | `python3 $P/4b_vary.py --job $J --apply` | đổi clip bị lặp trong 25s |
| ⑨b | `python3 $P/soi_plan.py --job $J` | máy soi: lỗi + chỗ ngờ (0 token) |
| ⑨c | *agent `dilim-soat-broll`* | nhìn frame thật, chỉ dòng sai ý + đề xuất |
| ⑩ | `python3 $P/make_review_table.py --job $J` | `bang_duyet.html` — **anh duyệt** |
| — | *anh sửa → bấm «TẢI JSON VỀ» → `duyet.json`* | |
| ⑪ | `python3 $P/apply_duyet.py --job $J --apply` | chấm điểm + ghi `BAI_HOC.md` |
| ⑫ | `python3 $P/5_render_captions.py --job $J` | `captions_png/` |
| ⑬ | `$V $P/6_to_capcut.py --job $J --install` | project trong CapCut |
| ⑭ | `python3 $P/kho_caption.py --gom` | nạp job vừa xong vào **kho caption** |
| ⑮ | `python3 $P/hoc_lich_su.py` | nạp job vào **kho B-roll** (tần suất, backlink) |

## Lệnh mới (05/08/2026) — dùng thay cho làm tay

```bash
python3 $P/chay_het.py <job1> <job2>          # chạy cả chuỗi, phiên âm SONG SONG
python3 $P/de_xuat_cat.py --job $J --ghi      # tự đề xuất cuts.json (trúng ~41-75%)
python3 $P/goi_y_broll.py --job $J --md       # gợi ý B-roll KÈM src_start an toàn
python3 $P/backtest.py                        # chấm bản máy dựng so với bản anh chốt
python3 $P/xay_kho_broll.py                   # OCR toàn kho -> vùng cấm tự động
```

**`goi_y_broll.py` thay `suggest_clips.py`** — v1 chỉ trả tên file, người vẫn phải đoán
`src_start`, và đó chính là chỗ đẻ ra 16 lỗi vùng cấm. v2 trả giây bắt đầu đã nằm trọn
trong đoạn sạch.

Chỉ bước ⑬ dùng `$V`. Bước ⑤⑦⑨⑪ là mới (04/08/2026) — bỏ qua được nhưng đừng bỏ.
**Bước ⑭ đừng quên** — không gom thì kho không dày lên, job sau lại viết lại từ đầu.

**Mỗi job tự viết 2 file:** `cuts.json` và `plan.py`. Còn lại script lo.

## Kho caption — cụm nào viết rồi thì khỏi viết lại

Bước ⑤ tự đọc `03-tool-capcut/kho_caption.json` + `tu_dien_whisper.json` rồi in vào
`plan.py` hai loại comment:

- `# KHO 0.86 · da dung 3x/2 job · warning` — cụm này viết rồi, kèm cách viết + clip đã dùng
- `# NGO whisper: "lau cầu thang" co the la "leo cầu thang"` — chỗ ngờ nghe nhầm

Gợi ý thôi, **không tự điền** — cùng một câu ở hai bài hay cần hai clip khác nhau
(đo được: variant trùng 21/22 nhưng clip chỉ trùng 16/22). Dòng có chữ số bị đánh dấu
`[CO CHU SO — KIEM TAY]`: giá và số hotline đổi theo thời gian, chép mù là sai.

Gặp lỗi whisper mới thì **thêm vào `tu_dien_whisper.json`** (không cần sửa code):
`chac_chan` = từ không tồn tại trong tiếng Việt, tự sửa · `can_kiem` = từ có thật
nhưng chắc là nghe nhầm, chỉ cảnh báo.

```bash
python3 03-tool-capcut/pipeline/kho_caption.py --tra "<câu bất kỳ>"   # tra lẻ
python3 03-tool-capcut/pipeline/kho_caption.py --thong-ke             # cụm nào dùng nhiều
```

## Thông số vị trí — đọc, đừng quy đổi

Mọi thông số vị trí/tỉ lệ (dải B-roll, caption, logo) đều đi một đường: **anh Thành kéo tay trong CapCut trước, rồi mới chép vào code.** Panel CapCut hiện đơn vị khác với file draft — tự quy đổi là đoán, và đã sai một lần ở logo.

Anh chỉnh xong thì hỏi **tên project**, rồi:

```bash
python3 03-tool-capcut/pipeline/doc_capcut.py --draft "DiLiM - <tên>" --track logo
```

Nó in ra số dạng chép thẳng vào `6_to_capcut.py`.

## Luật cứng

- Cắm ổ **T7 for Mac** trước khi chạy — mọi đường dẫn B-roll trỏ vào đó.
- `<job>/source.*` phải là **symlink** tới file gốc, không chép (file gốc vài GB).
- Giữ nguyên tên thư mục `edit/` trong mỗi job — cả 3 tool ghi output vào đó.
- Không đổi tên gì bên trong `01-tool-cat-video/` — đường dẫn hardcode khắp nơi.
- Đặt tên job: `04-du-an/<số thứ tự>-<ngày quay yyyy-mm-dd>-<tên file gốc>`. **Số phải duy nhất** (hiện có 3 job cùng số `04-`, đừng lặp lại lỗi đó).
- Không tự vẽ hình minh hoạ (PIL/SVG/sơ đồ). Không có clip thật khớp thì **để trống**.
- Luật nội dung ở `00-huong-dan/01-style-noi-dung-dilim.md` — cấm từ "chữa lành/điều trị", dùng "phục hồi/bảo vệ". Đọc trước mỗi lần dựng.

## Đọc thêm khi cần

| Cần gì | Đọc |
|---|---|
| dựng một video | skill `dilim-autocut` |
| bẫy kỹ thuật CapCut, thông số đã chốt | `03-tool-capcut/README.md` |
| lịch sử phiên bản + còn thiếu gì | `03-tool-capcut/VERSION.md` |
| anh Thành đã sửa gì, vì sao | `03-tool-capcut/BAI_HOC.md` |
| luật chọn B-roll đầy đủ | `02-tool-them-broll/skills/dilim-video-broll/SKILL.md` |
