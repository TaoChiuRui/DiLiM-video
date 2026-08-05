# Đọc tờ này khi cáp mới về

> Viết 05/08/2026, lúc ổ T7 hỏng giữa phiên làm việc.
> Làm đúng thứ tự dưới đây. **Đừng bỏ bước 0.**

---

## Ổ đang bị gì

Mount được, thấy tên file, thấy đúng dung lượng — **nhưng đọc nội dung ra 0 byte**.

```
ls "<kho>"                → Input/output error, thấy 0 thư mục
ls -la richnatto-01.mp4   → 12.459.014 bytes
dd if=… bs=1m count=1     → 0 bytes/sec
```

Trong một phiên: `187 co / 0 mat` → `12 co / 175 mat` → ổ rụng khỏi máy.

Phân vùng là **Apple_HFS** trên `/dev/disk4s3`. `T7 For win` (`disk4s2`) là **cùng một ổ
vật lý** — không phải bản sao lưu.

Chưa loại được 3 khả năng: **dây** · **mạch trong vỏ ổ** · **chính con SSD**.

---

## Bước 0 — ĐỪNG làm mấy việc này

- ❌ **Disk Utility → First Aid** hoặc `fsck`. Chúng **ghi lên ổ**. Trên ổ đang lỗi đọc,
  việc đó có thể mất luôn phần còn vớt được.
- ❌ Cắm qua hub, qua màn hình, qua dock. Cắm **thẳng vào máy**.
- ❌ Dựng video, chạy `xay_kho_broll.py`, hay bất cứ thứ gì đọc nhiều — **trước khi sao lưu xong**.

---

## Bước 1 — Cắm và kiểm

Cáp mới, cổng khác, cắm thẳng. Rồi:

```bash
cd ~/Desktop/DiLiM-video && python3 03-tool-capcut/pipeline/clips.py
```

| Kết quả | Nghĩa là |
|---|---|
| `187 co / 0 mat` | ổ đọc lại được → sang **bước 2 ngay** |
| vẫn nhiều `mat` | dây không phải nguyên nhân → xuống **bước 4** |

Kiểm bằng lệnh này chứ đừng nhìn Finder: đã gặp trường hợp `os.path.exists` trả True mà
đọc ra 0 byte.

---

## Bước 2 — SAO LƯU, và chỉ sao lưu

Việc đầu tiên và duy nhất. Chưa xong bước này thì chưa làm gì khác.

```bash
rsync -a --ignore-errors --info=progress2 \
  "/Volumes/T7 for Mac/02. Dilim Footage" ~/Desktop/backup-footage/
```

`--ignore-errors` để nó không dừng khi gặp file hỏng — vớt được bao nhiêu hay bấy nhiêu.
Kho 19,7 GB, ổ máy còn ~117 GB.

Chép xong đối chiếu:

```bash
find ~/Desktop/backup-footage -type f | wc -l      # mong đợi ~1177
```

---

## Bước 3 — Chạy nốt việc đang dở

Còn **43 clip chưa OCR**, toàn nằm trong `Đồ ăn - Ăn uống`:

```bash
python3 03-tool-capcut/pipeline/xay_kho_broll.py
```

Tự tiếp từ chỗ dở, ~1 phút. Chạy xong thì `kho_broll.json` đủ 1048 mục và kho dùng được trọn vẹn.

---

## Bước 4 — Nếu cáp mới không cứu được

Đã loại được khả năng dây. Còn hai:

- **Mạch trong vỏ ổ** — SSD bên trong có thể còn tốt. Tháo vỏ, gắn SSD vào vỏ/adapter khác.
  Đây là việc nên nhờ chỗ có kinh nghiệm, không nên tự cạy.
- **Chính con SSD** — việc của dịch vụ cứu dữ liệu. **Càng thao tác nhiều càng khó cứu**,
  nên dừng tay và mang đi.

---

## Cái KHÔNG mất, kể cả ổ chết hẳn

| Thứ | Ở đâu |
|---|---|
| `kho_broll.json` — 1009 clip đã OCR, có vùng cấm | GitHub |
| `danh_muc_kho.json` — 1048 clip có mô tả tiếng Việt | GitHub |
| Tên chuẩn hoá của 1053 file + nhật ký đổi tên | GitHub (`05-footage-moi/doi_ten_log/`) |
| Code, tài liệu, `cuts.json` + `plan.py` của 9 job | GitHub |
| **180 clip footage thật** (`dilim-footage.zip`, 2,56 GB) | **Google Drive** |

Danh mục còn nguyên nghĩa là **biết chính xác mất clip nào** để quay lại hoặc mua lại —
không phải mò từ đầu.

Và bài học đắt nhất: `T7 For win` cùng ổ vật lý với `T7 for Mac`. Kho footage cần một bản
sao **trên thiết bị khác**, không phải phân vùng khác.
