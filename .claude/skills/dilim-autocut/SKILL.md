---
name: dilim-autocut
description: >-
  Dựng video bán hàng DiLiM từ clip thô ra project CapCut hoàn chỉnh — cắt A-roll
  theo biên từ, caption style DiLiM, dải B-roll, SFX. Dùng skill này BẤT CỨ KHI NÀO
  anh Thành đưa một file quay vào `05-footage-moi/` hoặc `04-du-an/`, nói "dựng
  video này", "cắt video", "làm caption", "thêm B-roll", "ra CapCut", "dựng bán
  hàng", dán đường dẫn .mp4/.MOV, hoặc nhắc tên sản phẩm DiLiM (Nano Nattokinase,
  Rich Coenzyme Q10, Nano Sụn, Ellagic Acid, Inulin Fuji FF, Nghệ Mùa Thu Okinawa,
  Hàu Nano Gold…) trong ngữ cảnh dựng video. Cũng dùng khi sửa/dựng lại một job cũ
  trong `04-du-an/`, hoặc khi anh gửi lại `duyet.json` sau khi duyệt bảng.
---

# DiLiM AutoCut — dựng video ra project CapCut

Tool 3 (`03-tool-capcut/`). Ra **project CapCut sửa tiếp được**, không phải file render sẵn.
Thông số kỹ thuật đã chốt + 4 bẫy đã gỡ: `03-tool-capcut/README.md` — đọc khi đụng vào code, không cần đọc để dựng.

## Trước khi bắt đầu — 3 việc

1. **Cắm ổ T7 for Mac.** Không có ổ thì mọi đường dẫn B-roll chết. Kiểm: `ls "/Volumes/T7 for Mac"`
2. **Đọc `03-tool-capcut/BAI_HOC.md`** nếu có — đó là những gì anh Thành đã sửa trên các job trước, kèm lý do. Đừng lặp lại lỗi đã có trong đó.
3. **Đọc `00-huong-dan/01-style-noi-dung-dilim.md`** — công thức 10 khối và luật cấm từ. Luật quan trọng nhất: dùng **"phục hồi"/"bảo vệ"**, KHÔNG "chữa lành"/"điều trị"/"chữa bệnh".

Tạo job: `04-du-an/<số duy nhất>-<ngày quay yyyy-mm-dd>-<tên file gốc>/`, bên trong
`source.MOV` là **symlink** tới file gốc (`ln -s`, đừng chép).

## Chuỗi lệnh

```bash
J=04-du-an/<tên-job>
P=03-tool-capcut/pipeline
V=03-tool-capcut/VectCutAPI/.venv/bin/python
```

**Phần 1 — cắt A-roll**

```
python3 $P/1_transcribe.py --job $J          # word-level, chạy local, vài phút
```
Đọc `$J/edit/transcript_readable.txt` → viết `$J/cuts.json`: bỏ vấp, lặp, ậm ừ, đoạn lạc đề.
Format `[{"t0": 0.0, "t1": 2.38, "why": "câu lạc"}]`, `t1: null` = cắt đến hết.
Giữ trọn câu hook và câu CTA — đừng cắt cụt cảm xúc.

```
python3 $P/make_cut_table.py --job $J        # bang_cat.html — HỎI anh có cần duyệt không
python3 $P/2_cut.py         --job $J         # final.mp4 + edl.json
python3 $P/3_map_words.py   --job $J         # words_cut.json + transcript_cut.txt
```

**Phần 2 — caption**

```
python3 $P/make_plan_draft.py --job $J       # sinh khung plan.py: nhịp + mốc t sẵn
```
Giờ mới là việc thật: mở `$J/plan.py`, sửa từng dòng theo `references/viet-plan.md`.
Mốc `t` do máy đặt đã đúng — **đừng sửa tay**. Dòng nào còn `#?` là variant máy đoán.

```
python3 $J/plan.py                           # ra plan.json, báo lỗi nếu có
```

**Phần 3 — B-roll**

```
python3 $P/suggest_clips.py --job $J --md    # ra edit/goi_y_clip.md
```
Đọc file gợi ý (nhỏ, vài KB) → điền tên hằng clip vào `plan.py` → chạy lại `python3 $J/plan.py`.
Luật chọn và 4 câu hỏi phải tự trả lời: `references/chon-broll.md`.
Máy chỉ tra từ khoá — **nó không biết clip quay gì**. Không có gì khớp thật thì để `""`.

Tìm tay ra clip nào mà `suggest_clips` không tra ra → **thêm từ khoá vào `clips.TAGS`** ngay,
và nếu là clip mới thì khai hằng số trong `03-tool-capcut/pipeline/clips.py`.

**Phần 4 — chốt**

```
python3 $P/4_anchor.py  --job $J --apply     # neo caption vào chữ thật
python3 $P/4b_vary.py   --job $J --apply     # đổi clip bị lặp trong 25s
python3 $P/make_review_table.py --job $J     # bang_duyet.html
```
**HỎI anh Thành: "có cần duyệt bảng không?"** (anh chốt 03/08). Cần thì gửi đường dẫn
`bang_duyet.html` — **đừng tự Read file đó**, 600 KB ảnh base64.
Anh sửa xong bấm «TẢI JSON VỀ» → `~/Downloads/duyet.json`:

```
python3 $P/apply_duyet.py --job $J --apply   # chấm điểm + gom bài học
```

```
python3 $P/5_render_captions.py --job $J     # PNG trong suốt
$V       $P/6_to_capcut.py --job $J --install
```
Mở CapCut, project tên `DiLiM - <tên job>`.

## Luật không được phá

- **Không tự vẽ hình minh hoạ** — không PIL, không SVG, không sơ đồ. Không có footage thật khớp thì để trống lớp B-roll, giữ caption.
- **Không nhét clip cho đủ mật độ.** Tăng mật độ bằng cách tìm kỹ hơn, không phải bằng cách hạ chuẩn.
- **Không sửa `caption_style.py`** ở tool 3 — style nằm ở `02-tool-them-broll/pipeline/caption_style.py`, sửa bên đó.
- **Không đọc** `bang_duyet.html`, `bang_cat.html`, `broll_catalog.json`, `words_cut.json` — xem bảng cấm trong `CLAUDE.md`.
- **Báo cáo thật.** Nói rõ caption nào để trống và vì sao. Thấy mình vừa làm sai thì nói trước khi anh phải tự tìm ra.

## Còn thiếu (soát 05/08/2026)

**Nhạc nền** · **disclaimer** *"Sản phẩm này không phải là thuốc…"* chưa tự chèn (có sẵn
`05 Finish part/SP này k phải là thuốc.mp4` trên T7) · ẩn dụ **ống nước TẮC / máy bơm /
vỉ thuốc** chưa có clip (ống nước *chảy thông* và xe rác thì đã có) · chưa có clip
**"sống thiếu lành mạnh"** (ngồi lì, ăn uống thất thường) — đừng thay bằng clip mệt mỏi,
người xem đọc ra "đang bệnh" chứ không ra "lười vận động".

Kho mạch máu **đã chuẩn hoá xong** (78/78 file có tên đọc hiểu) — bỏ khỏi danh sách.

Cập nhật `03-tool-capcut/VERSION.md` khi làm xong.
