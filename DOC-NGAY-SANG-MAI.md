# Đọc sáng mai — tóm tắt đêm 04→05/08

## 1. Câu anh hỏi: **có phải tôi làm rớt ổ T7 không?**

**Không phải.** Bằng chứng cứng:

| Giờ ổ rớt | Lúc đó tôi đang làm gì |
|---|---|
| **17:39:19** và **17:39:33** | **Chưa đụng vào T7 lần nào.** Tôi mới chỉ chạy phiên âm — đọc file trên Desktop. Lần đầu tôi chạm vào T7 là **17:55:06** (giờ ghi file `goi_y_clip.md`), tức **16 phút SAU** khi ổ đã rớt hai lần |
| **18:48:29** | **Tôi đang dừng hẳn.** Anh bảo tạm dừng lúc 18:44, tôi chạy tiếp lúc 19:25. Không có tiến trình nào của tôi chạy |
| 20:46:34 | có, tôi vừa dựng draft (chép media từ T7) khoảng 13 phút trước |
| 21:23:49 | có, đang chạy OCR toàn kho |
| 21:26:27 | ổ **đã biến mất trước** khi tôi gõ lệnh `diskutil` — lệnh trả về "Failed to find disk disk5" |

Hai mốc đầu là bằng chứng quyết định: **ổ rớt khi tôi chưa hề chạm vào nó**, và rớt khi
tôi đứng yên hoàn toàn.

**Nhưng nói cho công bằng:** đọc nhiều có làm nó rớt thường hơn. Tuy vậy đọc file tuần tự
là việc bình thường — **ổ khoẻ không rớt vì bị đọc.** Tôi làm lộ ra lỗi có sẵn, không tạo
ra lỗi.

**Điều đáng lo nhất** không phải rớt kết nối mà là lúc 21:20: ổ **vẫn mount**, `df` vẫn
báo 838 GB, nhưng `ls` thư mục gốc trả về `Input/output error`. Đọc không ra dữ liệu.
Cái đó không phần mềm nào gây ra được.

**Đề nghị:** đổi dây, cắm thẳng vào máy. Nếu còn lỗi I/O → **sao lưu trước, sửa sau**.
Tôi cố ý không chạy First Aid vì nó ghi lên ổ.

---

## 2. Kho index B-roll — xong

**159 mục · 145 clip video đều đã có mô tả bằng chữ.**

Máy tự OCR từng frame (macOS Vision, không cài gì) + đo độ sáng. Tôi nhìn thật 145 frame
để viết mô tả — tầng này máy không làm thay được.

Nó **bắt được 2 chỗ mắt tôi soi sót** tối qua:
- `cucmau-tacmach` có chữ ở giây 12–22.6 — tôi hoàn toàn không biết
- `xovua-mohinh-mach` có chữ từ giây 30.1 — tôi ghi "sạch tới 38", **sai**

Và tôi tự bắt được **4 lỗi của chính mình** khi đo lại (chi tiết ở `VERSION.md` v2.1):
lọc watermark bằng regex → hỏng · dùng độ sáng trung bình → cấm oan clip nền tối
(`tim-dap-nento` bị cấm sạch 20/20 giây) · cấm oan chữ in trên vỏ hộp sản phẩm · cấm
nhầm vùng 0.2 giây.

---

## 3. Con số thật — không tô vẽ

**Thước đo:** `backtest.py` chấm bản máy dựng so với bản anh chốt trong CapCut.

| `06-magie` | Cắt | Caption | B-roll |
|---|---|---|---|
| | 61% | 93% | 73% |

**Tự đề xuất cắt** (`de_xuat_cat.py`): 25% → 33% → **41%** qua ba vòng sửa.
Nới dung sai lên 1.5 giây thì 75%.

**Gợi ý B-roll** (`goi_y_broll.py`): dòng có gợi ý 62% → **98%**, kèm `src_start` an toàn.

> ⚠️ **Lần đo đầu ra 95% trúng — con số đó SAI.** Từ khoá học được lấy từ mọi job, kể cả
> job đang chấm, nên nó nhớ bài chứ không suy luận. Loại ra thì còn **11% top-1**.
> Thêm tầng mô tả nâng lên **14% top-1 / 43% top-3**.

**Nói thẳng: tra bằng chữ không thay được mắt.** 43% nghĩa là hơn một nửa số dòng anh
vẫn phải tự chọn. Giá trị chắc chắn của kho là **`src_start` an toàn** — xoá hẳn họ lỗi
16 chỗ hiện chữ tiếng Anh trên dải B-roll.

---

## 4. Còn 27 lỗi trong các bản cũ

`test_logic.py` chạy 4 giây, hiện **0 FAIL**. Nhưng máy soi tìm ra 27 lỗi trong 7 job:

| Job | Lỗi |
|---|---|
| `04-img1770` | 10 |
| `04-img1773` | 5 |
| `03-dscf0894` | 4 · `04-img1771` 4 · `02-video-test` 3 |
| `05-natto` | **0** |
| `06-magie` | 1 (clip ngắn hơn caption) |

Phần lớn là `src_start` đâm vùng có chữ tiếng Anh. Sửa thì mỗi dòng đổi một con số —
**anh quyết có đáng sửa không**, nếu mấy video đó đăng rồi thì thôi.

---

## 5. Lệnh mới

```bash
python3 03-tool-capcut/pipeline/test_logic.py              # test toàn bộ, 4 giây
python3 03-tool-capcut/pipeline/chay_het.py <j1> <j2>      # chạy chuỗi, phiên âm song song
python3 03-tool-capcut/pipeline/de_xuat_cat.py --job <j> --ghi
python3 03-tool-capcut/pipeline/goi_y_broll.py --job <j> --md
python3 03-tool-capcut/pipeline/backtest.py
```

## 6. Việc tôi CHƯA làm được

- **Chưa đo được tốc độ thật.** Tôi ước 2 video còn ~45 phút thay vì 1h15, nhưng chưa
  chạy trọn vẹn lần nào vì ổ chết giữa chừng. **Đừng tin con số đó** cho tới khi chạy thật.
- Tầng mô tả mới ở mức một câu mỗi clip. Chia theo từng **đoạn** trong clip dài thì tra
  sẽ sát hơn.
- Kho caption vẫn **0 dữ liệu duyệt** — chưa job nào có `duyet.json`.

Không xoá gì. 13 script kiểm cú pháp OK.
