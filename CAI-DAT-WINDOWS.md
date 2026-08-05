# Đưa bộ này chạy trên Windows

> **Tờ này viết để đưa cho Claude Code trên máy Windows.** Mở Claude Code trong thư mục repo,
> bảo nó *"đọc `CAI-DAT-WINDOWS.md` rồi làm theo"*.
>
> Soạn 05/08/2026. Mọi số dòng dưới đây đo trên bản v2.3 — code đổi thì số dòng lệch,
> tìm theo chuỗi chứ đừng tin số dòng.

---

## Đọc cái này trước khi bắt tay

Bộ này viết cho macOS và **chưa từng chạy trên Windows lần nào**. Có **5 chỗ** phải sửa.
Không phải "cài xong là chạy" — nó sẽ gãy ở bước ①, rồi ③, rồi ⑬.

**Nguy hiểm nhất không phải lỗi làm dừng chương trình.** Nguy hiểm là **thứ chạy trơn tru
mà kết quả sai** — ngày 05/08/2026 một lỗi kiểu đó (dải B-roll chạy dài quá phần người nói)
đi lọt qua **5 bản đã giao**, không script nào kêu, đến khi người xem lại mới thấy.

> **Vì vậy: sửa xong mỗi mục, phải MỞ CAPCUT NHÌN BẰNG MẮT.** Không có bài test nào thay được
> việc đó. Đừng báo "xong" khi mới chỉ thấy chương trình chạy không báo lỗi.

---

## Mục 1 — Phiên âm (bước ①)

**Chỗ sửa:** `03-tool-capcut/pipeline/1_transcribe.py`, tìm chuỗi `mlx_whisper`.

`mlx_whisper` chạy trên MLX — framework riêng của Apple, **không có bản Windows**. Phải thay engine.

Các bước phía sau **không quan tâm engine nào**. Chúng chỉ đọc một file JSON ở
`<job>/edit/transcripts_words/audio16k.json` với đúng cấu trúc này:

```json
{ "segments": [
    { "words": [ {"word": "Cam", "start": 0.0, "end": 0.24}, ... ] }
] }
```

**Bắt buộc phải có `words[].start`** — cả pipeline neo chữ vào mốc đó.
`end` thì có cũng được, code không tin nó (whisper kéo dài `end` để nuốt khoảng lặng).

Thay bằng `faster-whisper` là hợp lý nhất:

```powershell
pip install faster-whisper
```

Gọi với `word_timestamps=True`, `language="vi"`, model `large-v3`, rồi tự ghi ra JSON đúng
cấu trúc trên. Máy có GPU NVIDIA thì đặt `device="cuda"`, không thì `device="cpu"` (chậm hơn nhiều).

**Kiểm:** chạy bước ① trên một video ngắn, rồi:

```powershell
python -c "import json;d=json.load(open(r'<job>\edit\transcripts_words\audio16k.json'));w=[x for s in d['segments'] for x in s.get('words',[])];print(len(w),'chữ');print(w[:3])"
```

Phải in ra vài trăm chữ, mỗi chữ có `start` là số thực tăng dần.

---

## Mục 2 — Mã hoá video (bước ③)

**Chỗ sửa:** `03-tool-capcut/pipeline/2_cut.py`, tìm chuỗi `h264_videotoolbox`.

`h264_videotoolbox` là bộ mã hoá bằng chip Apple. Windows không có.

| Thay bằng | Khi nào |
|---|---|
| `libx264` | luôn chạy được, dùng CPU, chậm hơn |
| `h264_nvenc` | máy có card NVIDIA — nhanh gần bằng bản Mac |
| `h264_qsv` | chip Intel có Quick Sync |

Kiểm máy có gì:

```powershell
ffmpeg -encoders | findstr h264
```

Đổi `libx264` thì bỏ luôn `-b:v 12M`, thay bằng `-crf 18 -preset medium` cho chất lượng ổn định hơn.

**Kiểm:** chạy bước ③, rồi mở `<job>\edit\final.mp4` xem. Phải đúng độ dài dự kiến (script tự in
ra `dai ... du kien ... lech ...`, lệch phải dưới 0,5 giây) và **nghe không bị "bụp" ở mối cắt**.

---

## Mục 3 — Lệnh `cp` không tồn tại trên Windows ⚠

**Chỗ sửa:** `03-tool-capcut/pipeline/6_to_capcut.py`, tìm chuỗi `["cp", "-c"`.

```python
r = subprocess.run(["cp", "-c", src_p, dst], capture_output=True)
if r.returncode:
    shutil.copy2(src_p, dst); copied += 1
else:
    cloned += 1
```

**Đọc kỹ chỗ này.** Nhìn qua tưởng đã có đường lùi (`shutil.copy2`), nhưng đường lùi đó chỉ chạy
khi `cp` **tồn tại và trả mã lỗi**. Trên Windows **không có lệnh `cp`**, nên `subprocess.run` ném
`FileNotFoundError` — chương trình **chết hẳn**, không rơi vào nhánh `else`.

Sửa thành dùng thẳng `shutil.copy2`, hoặc bọc `try/except FileNotFoundError`.

`cp -c` trên macOS là clone kiểu APFS — chép mà tốn 0 byte. Windows không có, nên **mỗi job sẽ
chép thật khoảng 1,2 GB** media vào thư mục draft. Chạy vẫn đúng, chỉ chậm và tốn ổ. Nếu vướng
dung lượng thì cân nhắc hardlink (`os.link`) khi nguồn và đích cùng ổ.

---

## Mục 4 — Đường dẫn draft của CapCut (5 file)

Tìm chuỗi `Movies/CapCut` — có ở **5 file**:

```
6_to_capcut.py   backtest.py   de_xuat_cat.py   doc_capcut.py   hoc_lich_su.py
```

Đường dẫn hiện tại là của CapCut bản macOS:

```
~/Movies/CapCut/User Data/Projects/com.lveditor.draft
```

**Tôi không biết chắc CapCut Windows để draft ở đâu** — chưa kiểm được. Khả năng cao là dưới
`%LOCALAPPDATA%`, nhưng **phải tự xác minh**, đừng chép mù:

1. Mở CapCut, tạo một project bất kỳ, đặt tên dễ nhớ
2. Tìm thư mục tên `com.lveditor.draft` trong `C:\Users\<tên>\AppData\`
3. Bên trong phải thấy một thư mục trùng tên project vừa tạo, có file `draft_info.json`

Tìm nhanh bằng PowerShell:

```powershell
Get-ChildItem -Path $env:LOCALAPPDATA,$env:APPDATA -Recurse -Directory -Filter "com.lveditor.draft" -ErrorAction SilentlyContinue | Select-Object FullName
```

Sửa xong nên **gom về một chỗ** thay vì sửa rải rác 5 file: thêm hằng số vào
`pipeline/job_path.py` (file dùng chung sẵn có) rồi 5 file kia import vào. Đỡ lệch nhau về sau.

---

## Mục 5 — Đoạn chống sandbox của macOS

**Chỗ sửa:** `6_to_capcut.py`, tìm chuỗi `Containers/com.lemon.lvoverseas`.

Đoạn này giải một vấn đề **chỉ có trên macOS**: CapCut chạy trong sandbox, bị chặn đọc
`~/Desktop` và ổ ngoài, nên code phải chép media vào trong thư mục draft rồi viết đường dẫn
dạng container `~/Library/Containers/com.lemon.lvoverseas/Data/Movies/...`.

**Windows không có sandbox kiểu đó.** Nhưng code hiện tại **luôn luôn** đổi đường dẫn sang dạng
container — trên Windows sẽ ra đường dẫn vô nghĩa, CapCut mở lên báo mất file.

Vẫn nên **giữ việc chép media vào thư mục draft** (để project tự đứng một mình, rút ổ ngoài vẫn
chạy), chỉ **bỏ phần đổi sang đường dẫn container** — ghi thẳng đường dẫn thật của file đã chép.

---

## Sau khi sửa xong — kiểm theo thứ tự này

**Đừng bỏ bước nào.** Ba bước đầu máy tự kiểm được, bước 4 bắt buộc phải có người nhìn.

```powershell
python -m py_compile 03-tool-capcut\pipeline\*.py
python 03-tool-capcut\pipeline\test_logic.py      # phải ra "0 FAIL"
python 03-tool-capcut\pipeline\clips.py           # phải ra "187 co / 0 mat"
```

**4. Dựng lại một job mẫu và MỞ CAPCUT NHÌN.** Repo có sẵn 9 job mẫu với `cuts.json` và `plan.py`
thật, nhưng thiếu file quay gốc — nên phải dựng bằng video mới. Làm theo `BAT-DAU.md` bước 6.

Mở CapCut ra, soi 5 thứ:

| Nhìn gì | Đúng là thế nào |
|---|---|
| Số track | 5: `aroll` `broll` `caption` `logo` `sfx` |
| Mốc kết các track | **mọi track phải kết cùng lúc** — B-roll thừa ra là lỗi đã biết |
| Dải B-roll | nằm trên đỉnh khung, **không lộ viền** ở mép dưới |
| Chữ chạy | hiện đúng lúc người nói, không lệch nhịp |
| Media | không có clip nào báo "File not accessible" |

---

## Nếu bí

`03-tool-capcut/VERSION.md` ghi lại mọi lần vấp trước đây kèm lý do — nhiều lỗi trên Windows sẽ
có họ hàng với lỗi đã gặp trên Mac. Đặc biệt đọc mục **"Bốn cái bẫy đã gỡ"** trong
`03-tool-capcut/README.md` trước khi đụng vào `6_to_capcut.py`.

**Và nhắc lại điều quan trọng nhất:** thứ nguy hiểm không phải lỗi làm dừng chương trình, mà là
bản dựng chạy ngon nhưng sai. Mở CapCut nhìn bằng mắt, mỗi lần.
