# DiLiM — Style Guide dựng video bán hàng (talking-head)

> Đọc file này TRƯỚC mỗi lần dựng video trong thư mục này.
> Người quay: chủ thương hiệu tự quay chính mình. Kiểu: video bán hàng theo "form bác Sơn".
> Nguồn công thức: `raw/content/ads-bac-son-*.md` trong vault DiLiM-Brain (7 bài đã phân tích).
> Bổ trợ giọng thương hiệu: `wiki/topics/voice-content-dilim.md` trong vault.

---

## 1. Công thức nội dung — 10 khối (kiểm khi cắt: giữ đúng thứ tự, đừng để hụt khối)

1. **Hook chạm đau** — nhắm đúng đối tượng + quan sát đời thường ("Anh chị có để ý không?", "soi gương giật mình"). Giữ trọn, đây là 3 giây quyết định.
2. **Lật gốc rễ** — "Không phải do ăn nhiều/ít, mà là gan yếu + mỡ nội tạng + đường ruột".
3. **Bộ 3 giải pháp — luôn đúng thứ tự này:**
   - ① Ellagic Acid AFC → *đẩy mỡ nội tạng ra* (hạt xoài đen châu Phi, nghiên cứu trên người 8–12 tuần, không ép gan)
   - ② Men Inulin chuỗi dài Fuji FF → *khóa cửa, chặn mỡ xấu nhập* (bằng sáng chế quốc tế, nuôi lợi khuẩn)
   - ③ Nghệ Mùa Thu Okinawa → *bảo vệ & phục hồi gan* (curcumin hấp thu gấp 35 lần nghệ thường)
4. **Ẩn dụ 3 động tác** — "tăng xuất mỡ – giảm nhập mỡ – hỗ trợ gan".
5. **Uy tín + an toàn** — AFC nhà máy 60–65 năm, "top 3 chất lượng chứ không phải doanh số", không lệ thuộc, không kích thích, không ép cân.
6. **Trấn an** — "khỏe trước gọn sau", người nhẹ dần / bụng nhỏ dần, không cần giảm cấp tốc.
7. **Phải dùng đủ bộ** — "dùng riêng lẻ rất khó → đủ bộ để cơ thể tự điều chỉnh".
8. **Liều** — "đúng đủ đều 6–12 tháng".
9. **CTA** — để lại tên + SĐT dưới video / gọi hotline — "nhà DiLiM Supplement".
10. **Disclaimer** (BẮT BUỘC giữ, thường ở cuối) — "Sản phẩm này không phải là thuốc và không có tác dụng thay thế thuốc chữa bệnh."

## 2. Giọng & từ ngữ (giữ khi làm phụ đề / cắt)

- Đệm thân mật: "anh chị nha / ha / nhé", hỏi tu từ "đúng không ạ?" — GIỮ, đừng cắt sạch (đó là chất mộc mạc, gần gũi).
- Mộc mạc, lặp để nhấn. Không "văn vẻ hoá".
- **Quy tắc DiLiM (không được phạm):** luôn dùng **"phục hồi" / "bảo vệ"** — KHÔNG dùng "chữa lành" / "điều trị" / "chữa bệnh".
- Xưng "anh/chị" với người xem.

## 3. Nhịp cắt

- Video bán hàng social → nhịp gọn, dồn. Cắt sạch khoảng lặng dài, giữ mạch nói liền.
- Nhưng KHÔNG cắt cụt cảm xúc: giữ trọn câu hook và câu chốt CTA.
- Chừa 30–200ms ở mỗi mối cắt (không cắt giữa chữ). Fade âm 30ms mỗi mối (chống "bụp").

## 4. Quyết định VISUAL — điền sau khi có clip đầu tiên

> Những mục dưới chưa chốt vì cần xem 1 clip mẫu của anh. Cập nhật vào đây khi đã chọn.

- **Tỉ lệ khung hình:** ⬜ 9:16 dọc (TikTok/Reels/Shorts) — mặc định cho bán hàng social · ⬜ 1:1 · ⬜ 16:9
- **Chỉnh màu (grade):** ⬜ neutral_punch (tăng nét nhẹ, giữ da tự nhiên — an toàn cho talking-head) · ⬜ warm_cinematic · ⬜ để mộc
- **Phụ đề:** kiểu chữ / vị trí / chữ hoa hay thường — *chốt theo hướng transcript đã chọn (A/B/C)*
- **Logo / khung / hotline overlay:** ⬜ có (đặt file logo vào `assets/`) · ⬜ không
- **Nhạc nền:** ⬜ có · ⬜ không

## 5. Quy trình mỗi lần dựng

1. Anh quay xong → bỏ file vào `footage/`
2. Mở terminal, `cd ~/Desktop/DiLiM-video`, gõ `claude`
3. Nhắn: "dựng video bán hàng từ clip mới trong footage/"
4. Tôi: đọc STYLE.md này → (phiên âm nếu bật) → đề xuất bản cắt theo 10 khối → anh duyệt → cắt → preview → sửa → xuất
5. Kết quả ra ở `edit/` — file gốc trong `footage/` không bị đụng
