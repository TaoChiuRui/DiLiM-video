---
name: dilim-music-mood-library
description: "DiLiM Media NAS asset library — music classified by emotion into LIBRARY/NHAC, how it was done and where results live"
metadata: 
  node_type: memory
  type: project
  originSessionId: b19f5129-5be5-4a7a-a5fd-c120cab434be
---

Kho tài sản edit của DiLiM Media nằm ở NAS `\\NasSynolygo\Data\Tính` (~37.500 file, trộn nhạc + sound-effect + footage + template). Theo hướng dẫn (artifact "Hướng Dẫn Kho Nhạc · LUT · Hiệu Ứng"), nhạc phải chia theo **5 tâm trạng**: `cam-hung-nang-luong`, `cao-cap-diem-dam`, `nhe-nhang-chill`, `cam-xuc-story`, `vui-tuoi-tre`; SFX vào `SOUND-EFFECT`.

**Ngày 2026-07-04** đã phân loại nhạc theo cảm xúc bằng phân tích âm thanh:
- Giai đoạn A (mutagen, đọc thời lượng): tách được **8.464 nhạc thật** / **20.999 sound-effect** (lọc theo thời lượng <25s + từ khóa tên file).
- Giai đoạn B (librosa): tempo, RMS energy, spectral centroid, major/minor (Krumhansl), percussive ratio → chuẩn hóa **phân vị toàn kho** → chấm điểm 5 prototype tâm trạng.
- Kết quả copy (giữ nguyên gốc) vào `\\NasSynolygo\Data\Tính\LIBRARY\NHAC\<mood>\`. Báo cáo: `LIBRARY\_BAO_CAO_PHAN_LOAI_NHAC.csv` + `_TOM_TAT.txt`.
- SFX **chỉ index** (`LIBRARY\SOUND-EFFECT\_DANH_SACH_SFX.csv`), CHƯA copy để tránh nhân đôi ~20GB — có thể chạy lại để gom thật.

Python 3.12 cài ở `C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe` (librosa 0.11, numpy, soundfile, mutagen). Nhãn tâm trạng là **ước lượng**, ranh giới nhóm energetic (cam-hung vs cao-cap) chủ quan; bước gán nhãn tách khỏi trích đặc trưng nên **tinh chỉnh lại nhanh** mà không giải mã lại (`_features_raw.csv`). Xem [[user-dilim-supplement]].
