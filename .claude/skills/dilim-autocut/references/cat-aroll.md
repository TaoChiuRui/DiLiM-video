# Cắt A-roll — viết `cuts.json`

Rút từ **bản dựng chuẩn của anh Thành** (`06-magie-canxi-combo-2`, 04/08/2026). Tôi cắt
448.3s → 389.2s (bỏ 13.2%). Anh cắt thêm **16.0 giây nữa ở 7 chỗ** → 373.2s (bỏ 16.8%).

**Bảy chỗ đó không ngẫu nhiên — nó là bảy loại tôi đã bỏ sót.**

---

## 1. Khoảng lặng — ngưỡng là ~1.5s, không phải 2s

Tôi liệt kê mọi khoảng lặng > 0.7s nhưng chỉ cắt cái ≥ 2.2s. Anh cắt cả khoảng
**1.57 giây** (giây 234.37–235.94). Nhịp bán hàng dồn hơn tôi tưởng.

> Khoảng lặng ≥ **1.5s** giữa hai cụm → cắt.

## 2. "Vâng." và mọi tiếng đệm xác nhận → cắt sạch

Giây 303.73 anh cắt đúng một chữ **"Vâng."** (1.25s). Tôi đã *nhìn thấy* nó khi soi
transcript và vẫn để lại. Nó không mang thông tin, chỉ là quán tính lúc nói.

## 3. Câu dẫn bỏ lửng — cắt kể cả khi KHÔNG có take lặp lại

Giây 100.50–104.77: *"…một câu là anh chị tự hỏi mình. Thành"* rồi anh nói sang chuyện
khác. Tôi giữ vì **luật cũ của tôi chỉ cắt khi có take sau thay thế**. Sai.

> Câu mở ra mà **không dẫn tới đâu** thì cắt, dù không có bản nói lại.

## 4. Nói lại cùng ý bằng giọng suồng sã hơn → giữ bản rõ, cắt bản kia

Giây 339.73–341.90: *"nó không có phản ứng với nhau. Đúng không? **Nó không có đá nhau.**"*
Anh giữ "không có phản ứng với nhau", cắt "không có đá nhau".

Lưu ý: ngược với luật *"gặp lặp thì giữ take SAU"*. Luật giữ-take-sau áp dụng khi anh
**nói lại vì lỡ lời**; còn đây là **nói thêm một cách diễn đạt khác**, thì giữ cách rõ nhất.

## 5. Vấp giữa một đoạn đang giữ → cắt trong lòng đoạn

Giây 283.43–286.60: *"ấy, người trung niên mà, **mà người**"* — vấp ngay giữa một đoạn tôi
giữ nguyên. Cơ chế dò lặp của tôi chỉ chạy ở mức **take**, không soi trong lòng đoạn.

## 6. Chữ nối treo đầu đoạn giữ → xén

Giây 428.92–431.00: đoạn của tôi mở đầu bằng *"Nên anh chị muốn…"*. Anh bắt đầu muộn hơn
2 giây. Mở đầu bằng liên từ treo lơ lửng nghe như đang lỡ nhịp.

## 7. Cắt xong thì caption phải chết theo

Sáu caption anh xoá đều nằm đúng trong bảy chỗ trên — **không phải quyết định riêng**.
Cắt A-roll ở đâu thì bỏ caption ở đó.

---

## Kiểm nhanh trước khi chốt `cuts.json`

```bash
# liet ke moi khoang lang >= 1.5s
python3 -c "
import json,sys
W=[w for s in json.load(open(sys.argv[1]))['segments'] for w in s.get('words',[])]
for a,b in zip(W,W[1:]):
    if b['start']-a['end']>=1.5: print(f\"{a['end']:7.2f} -> {b['start']:7.2f}  ...{a['word']} | {b['word']}...\")
" <job>/edit/transcripts_words/audio16k.json
```

Rồi rà transcript tìm: `Vâng` · `Đúng không?` đứng một mình · câu mở bỏ lửng ·
cụm nói lại bằng từ khác · vấp lặp chữ trong lòng câu.

**Vẫn giữ luật cũ:** khoảng 30–200ms ở mỗi mối cắt, không cắt giữa chữ, giữ trọn câu hook
và câu CTA. Và mốc cắt lấy từ `start` của chữ — `end` của whisper không đáng tin.
