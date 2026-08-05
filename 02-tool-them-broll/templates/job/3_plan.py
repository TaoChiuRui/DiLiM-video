# -*- coding: utf-8 -*-
"""Ke hoach caption + B-roll — Raydel V1 (89s, combo Raydel + Rich Q10)."""
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from clips_raydel import *  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
FPS, TOTAL = 60, 5337
IMG = (".jpg", ".jpeg", ".png")

# (t0, t1, d1, d2, variant, path, src_start, note)
R = [
 (0.00,  2.60, "ĐANG BỊ *MỠ MÁU CAO*", "",                        "warning", MO_MAU_CAO,    1.0, ""),
 (2.60,  4.90, "HOẶC *MỆT MỎI KHÔNG RÕ NGUYÊN NHÂN*", "",         "warning", MET_MOI,       1.0, ""),
 (5.46,  8.20, "*RAYDEL POLICOSANOL*", "",                        "product", RAYDEL,        3.0, "hộp trên nền cây xanh"),
 (8.20, 10.70, "SẢN PHẨM CỦA *ÚC*", "NGUYÊN LIỆU TỪ *CUBA*",      "product", RAY_VIEN,      1.0, "viện nghiên cứu Cuba"),
 (11.50,13.80, "BÁN CHẠY *TOP 1 TẠI ÚC*", "",                     "product", RAY_ANH,         0, ""),
 (13.80,16.26, "TOP 1 TẠI HÀN QUỐC", "*5 NĂM LIỀN*",              "product", RAY_KETQUA,    1.0, "biểu đồ nghiên cứu"),
 (16.26,18.30, "GIẢM *MỠ XẤU* TRONG MÁU", "",                     "warning", MO_XAU,        1.0, ""),
 (18.30,20.28, "TĂNG *MỠ TỐT* TRONG MÁU", "",                     "positive",MO_TOT,        1.0, ""),
 (20.50,21.76, "ĐÂY LÀ ĐIỀU *QUAN TRỌNG*", "",                    "warning", "",              0, "câu ngắn 0.7s, để chữ chạy một mình"),
 (21.76,25.22, "CHỈ GIẢM MỠ XẤU", "THÌ *KHÔNG BỀN VỮNG*",         "warning", XO_VUA_HINH_THANH, 1.0, ""),
 (25.22,30.28, "VỪA GIẢM *MỠ XẤU*", "VỪA TĂNG *MỠ TỐT*",          "positive",MACH_THONG,    1.0, ""),
 (30.42,33.20, "*RICH COENZYME Q10*", "",                         "product", AFC_TOA_NHA,     0, "toà nhà AFC"),
 (33.20,35.62, "DẠNG KHỬ CỦA *AFC NHẬT BẢN*", "",                 "product", AFC_NHA_MAY,     0, "nhà máy AFC"),
 (35.70,41.02, "TĂNG CƯỜNG", "*NĂNG LƯỢNG TẾ BÀO*",               "positive",NANG_LUONG_TB, 1.0, ""),
 (41.24,44.60, "*90%* Q10 NGOÀI KIA", "LÀ *DẠNG OXY HÓA*",        "warning", Q10_CAM,       1.0, ""),
 (44.60,47.92, "ĐÂY LÀ *DẠNG KHỬ*", "DÙNG ĐƯỢC *NGAY*",           "positive",Q10_XANH,      1.0, ""),
 (47.92,51.50, "CÒN CÓ *ASTAXANTHIN*", "TỪ *TẢO ĐỎ NHẬT BẢN*",    "product", "",              0, "THIẾU CLIP: tảo đỏ / astaxanthin"),
 (51.50,55.50, "CHỐNG OXY HÓA *TẾ BÀO MỠ*", "",                   "positive",XO_VUA1,       1.0, ""),
 (55.50,60.22, "BẢO VỆ THÀNH MẠCH", "*TRƠN LÁNG, BỀN CHẮC*",      "positive",MACH_DAN_HOI,  1.0, ""),
 (60.34,65.12, "GIẢM *MỠ XẤU*", "TĂNG *MỠ TỐT*",                  "positive",MACH_THONG2,   1.0, ""),
 (65.38,67.88, "TĂNG *NĂNG LƯỢNG TẾ BÀO*", "",                    "positive",TIM_KHOE1,     1.0, ""),
 (67.88,69.58, "LÀM SẠCH *LÒNG MẠCH*", "",                        "positive",TUAN_HOAN,     1.0, ""),
 (69.58,71.98, "HỖ TRỢ *MỆT MỎI KHÔNG RÕ NGUYÊN NHÂN*", "",       "positive",MET_MOI2,      1.0, ""),
 (71.98,73.18, "*ĐAU ĐẦU — VAI GÁY*", "",                         "warning", VAI_GAY,       1.0, "6 triệu chứng, mỗi cái 1 nhịp"),
 (73.18,73.86, "*CHÓNG MẶT — MẤT NGỦ*", "",                       "warning", MAT_NGU,       1.0, ""),
 (73.86,74.40, "*TÊ BÌ TAY CHÂN*", "",                            "warning", TE_BI1,        1.0, ""),
 (74.40,75.00, "*RỐI LOẠN TIỀN ĐÌNH*", "",                        "warning", TIEN_DINH,     1.0, ""),
 (75.00,77.72, "PHÒNG NGỪA NGUY CƠ *ĐỘT QUỴ*", "",                "warning", DOT_QUY1,      1.0, ""),
 (78.12,81.68, "BỘ ĐÔI *CHÍNH HÃNG*", "TỪ SƠN & *DILIM SUPPLEMENT*","product",RAYDEL,      12.0, "góc khác"),
 (81.68,84.02, "ĐỂ LẠI *TÊN + SỐ ĐIỆN THOẠI*", "",                "cta",     CTA,           2.0, ""),
 (84.02,88.66, "HOẶC GỌI *HOTLINE*", "",                          "cta",     CTA,           7.0, "chạy tiếp cùng clip"),
]

caps, segs = [], []
for t0, t1, d1, d2, var, p, ss, note in R:
    f0, f1 = round(t0 * FPS), round(t1 * FPS)
    txt = d1 + ("\n" + d2 if d2 else "")
    assert txt.count("*") % 2 == 0, txt
    caps.append({"from": f0, "durationInFrames": f1 - f0, "text": txt, "variant": var})
    if p:
        isimg = p.lower().endswith(IMG)
        need = t1 - t0
        if not isimg:
            dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                        "-of", "csv=p=0", p], capture_output=True, text=True).stdout.strip() or 0)
            if dur - ss < need - 0.03:
                print(f"  ! NGAN {os.path.basename(p)[:40]} can {need:.2f}s con {dur-ss:.2f}s -> lui src")
                ss = max(dur - need, 0)
        segs.append({"from": f0, "durationInFrames": f1 - f0, "path": p, "is_image": isimg,
                     "src_start_s": round(ss, 2), "xfade_prev": 0, "crop_bias": 0.5, "key_black": False})

merged = []
for b in segs:
    m = merged[-1] if merged else None
    if m and m["path"] == b["path"] and m["from"] + m["durationInFrames"] == b["from"]:
        cont = m["src_start_s"] + m["durationInFrames"] / FPS
        if b["is_image"] or abs(b["src_start_s"] - cont) < 0.05:
            m["durationInFrames"] += b["durationInFrames"]; continue
        if b["path"] in PRODUCT_SET:
            b = dict(b); b["xfade_prev"] = 15
    merged.append(dict(b))

for a, b in zip(caps, caps[1:]):
    assert a["from"] + a["durationInFrames"] <= b["from"], "caption chong lan"
from collections import Counter
for p, n in Counter(b["path"] for b in merged if b["path"] not in PRODUCT_SET).items():
    if n > 1:
        print("  ! TRUNG CLIP", n, "x", os.path.basename(p))

d = os.path.join(HERE, "v1")
json.dump(caps, open(os.path.join(d, "captions.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(merged, open(os.path.join(d, "broll_plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"total_frames": TOTAL, "fps": FPS, "broll_position": "top"},
          open(os.path.join(d, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump([{"t": r[0], "t_end": r[1], "d1": r[2], "d2": r[3], "variant": r[4],
            "path": r[5], "src_start": r[6], "note": r[7], "idx": i + 1} for i, r in enumerate(R)],
          open(os.path.join(d, "plan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
cov = sum(b["durationInFrames"] for b in merged) / TOTAL * 100
print(f"v1: {len(caps)} caption | {len(merged)} doan B-roll | phu {cov:.0f}%")
