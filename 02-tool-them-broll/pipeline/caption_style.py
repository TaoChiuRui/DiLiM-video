# -*- coding: utf-8 -*-
"""He thong mau/font caption "Dr Son" (giu nguyen theo STYLE.md cua bo
dr-son-toolkit) - font doi sang Anton theo yeu cau rieng cho DiLiM
(2026-07-18). Deterministic: cung input captions.json luon ra cung style.
"""
from __future__ import annotations

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = Path(__file__).resolve().parent / "fonts" / "Anton-Regular.ttf"

W, H = 1080, 1920
LINE_PAD_X = 28
LINE_PAD_Y = 14
FONT_SIZE_1LINE = 68
FONT_SIZE_2LINE = 58
MIN_FONT_SIZE = 34
SAFE_MARGIN_X = 40  # le an toan 2 ben, tranh chu dinh sat/tran canh khung hinh
CAPTION_CENTER_Y = 1420  # vi tri khi mode="bottom" (video co B-roll dat duoi khung)
BAND_H = 672             # chieu cao dai B-roll tren cung - phai khop render_overlay.py
# mode="top": vi tri CO DINH cho CA VIDEO (khong xet tung caption co B-roll hay
# khong tai thoi diem do) - nguoi dung chot 2026-07-21: "b-roll o tren thi text
# LUON LUON o tren". Text dat NGAY DUOI dai B-roll, KHONG de len B-roll (du 1
# hay 2 dong) - CAPTION_GAP_BELOW_BROLL la khoang cach tu mep duoi B-roll.
CAPTION_GAP_BELOW_BROLL = 10
CORNER_RADIUS = 14  # bo goc khung nen caption (nguoi dung chot 2026-07-22)

# ---- mau sac (giu nguyen hex tu STYLE.md) ----
WHITE_BG, WHITE_TEXT, WHITE_KW = "#FFFFFF", "#157A3F", "#D62828"
YELLOW_BG, YELLOW_TEXT, YELLOW_KW = "#FFF000", "#000000", "#D62828"
RED_BG, RED_TEXT, RED_KW = "#D62828", "#FFFFFF", "#FFEA00"
# Mau rieng cho noi dung nhac san pham/thanh phan/chung nhan/gia (nguoi dung
# chot 2026-07-23: "san pham thi khong dung mau do, den") - khong dung do/den
# o bat ky vi tri nao (bg/text/kw) trong nhom nay.
PRODUCT_BG, PRODUCT_TEXT, PRODUCT_KW = "#FFFFFF", "#157A3F", "#B8860B"

TWO_LINE_GREEN = [
    {"bg": "#FFFFFF", "text": "#157A3F", "kw": "#D62828"},
    {"bg": "#157A3F", "text": "#FFFFFF", "kw": "#FFEA00"},
]
TWO_LINE_YELLOW = [
    {"bg": "#FFF000", "text": "#000000", "kw": "#D62828"},
    {"bg": "#000000", "text": "#FFF000", "kw": "#D62828"},
]
TWO_LINE_RED = [
    {"bg": "#D62828", "text": "#FFFFFF", "kw": "#FFEA00"},
    # kw doi tu FFEA00 (vang) sang den: vang tren nen trang qua mo, kho doc
    # (bug nguoi dung bao 2026-07-23) - dong nay van thuoc nhom "tieu cuc"
    # (do/den duoc phep o day, chi cam rieng cho nhom san pham ben duoi).
    {"bg": "#FFFFFF", "text": "#D62828", "kw": "#000000"},
]
TWO_LINE_PRODUCT = [
    {"bg": "#FFFFFF", "text": "#157A3F", "kw": "#B8860B"},
    {"bg": "#157A3F", "text": "#FFFFFF", "kw": "#FFEA00"},
]
# nhip xoay deterministic ~50% Green / 30% Yellow / 20% Red (10 o) - chi con
# dung lam fallback khi 1 caption khong duoc gan variant ro rang.
TWO_LINE_FAMILY_CYCLE = [
    TWO_LINE_GREEN, TWO_LINE_GREEN, TWO_LINE_GREEN, TWO_LINE_GREEN, TWO_LINE_GREEN,
    TWO_LINE_YELLOW, TWO_LINE_YELLOW, TWO_LINE_YELLOW,
    TWO_LINE_RED, TWO_LINE_RED,
]
# nhip 1 dong thuong: White, White, Yellow
SINGLE_LINE_CYCLE = ["white", "white", "yellow"]


class StyleCounters:
    """Giu dem deterministic xuyen suot 1 job - tao 1 lan, dung cho ca video."""
    def __init__(self):
        self.two_line_idx = 0
        self.single_line_idx = 0


def _parse_keywords(raw_line: str):
    """Tach *keyword* trong 1 dong -> list segment (text, is_keyword). Uppercase toan bo."""
    segments = []
    pos = 0
    for m in re.finditer(r"\*(.+?)\*", raw_line):
        if m.start() > pos:
            segments.append((raw_line[pos:m.start()], False))
        segments.append((m.group(1), True))
        pos = m.end()
    if pos < len(raw_line):
        segments.append((raw_line[pos:], False))
    return [(seg.upper(), is_kw) for seg, is_kw in segments if seg != ""]


def resolve_style(caption: dict, counters: StyleCounters):
    """Tra ve list[{bg,text,kw}] - 1 phan tu neu 1 dong, 2 neu 2 dong.

    Mau sac theo Y NGHIA noi dung (nguoi dung chot 2026-07-23), khong con
    xoay ngau nhien cho tung caption co gan variant ro rang:
      - "warning"/"critical" (y TIEU CUC - trieu chung, canh bao, rui ro) -> do
      - "positive" (y TICH CUC - loi ich, ket qua tot, lifestyle khoe manh) -> xanh la
      - "product" (nhac san pham/thanh phan/chung nhan/gia) -> KHONG do/den
      - "yellow"/"highlight"/"cta" giu nguyen nhu cu cho cac truong hop con lai
    Chi caption KHONG duoc gan variant nao moi roi vao cycle xoay ngau nhien
    (fallback, khong nen dung cho noi dung co y nghia ro rang).
    """
    variant = caption.get("variant")
    lines = caption["text"].split("\n")
    is_two_line = len(lines) == 2

    if variant in ("warning", "critical"):
        if is_two_line:
            return TWO_LINE_RED
        style = {"bg": RED_BG, "text": RED_TEXT, "kw": RED_KW}
        return [style] * len(lines)

    if variant == "positive":
        if is_two_line:
            return TWO_LINE_GREEN
        return [{"bg": WHITE_BG, "text": WHITE_TEXT, "kw": WHITE_KW}]

    if variant == "product":
        if is_two_line:
            return TWO_LINE_PRODUCT
        return [{"bg": PRODUCT_BG, "text": PRODUCT_TEXT, "kw": PRODUCT_KW}]

    if variant == "yellow":
        if is_two_line:
            return TWO_LINE_YELLOW
        return [{"bg": YELLOW_BG, "text": YELLOW_TEXT, "kw": YELLOW_KW}]

    if variant in ("highlight", "cta"):
        style = {"bg": WHITE_BG, "text": WHITE_TEXT, "kw": WHITE_KW}
        return [style] * len(lines)

    if is_two_line:
        family = TWO_LINE_FAMILY_CYCLE[counters.two_line_idx % len(TWO_LINE_FAMILY_CYCLE)]
        counters.two_line_idx += 1
        return family

    choice = SINGLE_LINE_CYCLE[counters.single_line_idx % len(SINGLE_LINE_CYCLE)]
    counters.single_line_idx += 1
    if choice == "yellow":
        return [{"bg": YELLOW_BG, "text": YELLOW_TEXT, "kw": YELLOW_KW}]
    return [{"bg": WHITE_BG, "text": WHITE_TEXT, "kw": WHITE_KW}]


def render_caption_png(caption: dict, counters: StyleCounters, out_path: str, position_mode: str = "top"):
    """Ve 1 caption (1 hoac 2 dong) thanh PNG RGBA kich thuoc WxH, nen trong suot.
    position_mode ap dung CO DINH cho toan bo video (khong doi theo tung caption):
    "top" = ngay duoi dai B-roll, khong de len; "bottom" = vi tri mac dinh giua-duoi."""
    lines = caption["text"].split("\n")
    styles = resolve_style(caption, counters)
    max_font_size = FONT_SIZE_1LINE if len(lines) == 1 else FONT_SIZE_2LINE
    max_block_w = W - 2 * SAFE_MARGIN_X

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    all_segments = [_parse_keywords(raw_line) for raw_line in lines]

    # Tu dong thu nho font neu dong dai nhat vuot qua khung hinh - tranh
    # chu bi tran/cat mat o canh phai (bug that gap 2026-07-20).
    font_size = max_font_size
    font = ImageFont.truetype(str(FONT_PATH), font_size)
    while font_size > MIN_FONT_SIZE:
        widest = max(
            sum(draw.textlength(seg, font=font) for seg, _ in segs) + 2 * LINE_PAD_X
            for segs in all_segments
        )
        if widest <= max_block_w:
            break
        font_size -= 2
        font = ImageFont.truetype(str(FONT_PATH), font_size)

    line_blocks = []  # (segments, seg_widths, style, block_w, block_h)
    for i, segments in enumerate(all_segments):
        seg_widths = [draw.textlength(seg, font=font) for seg, _ in segments]
        text_w = sum(seg_widths)
        bbox = font.getbbox("HÂNGY")  # dong co ky tu cao/thap de lay chieu cao on dinh
        text_h = bbox[3] - bbox[1]
        block_w = min(text_w + 2 * LINE_PAD_X, max_block_w)
        block_h = text_h + 2 * LINE_PAD_Y
        line_blocks.append((segments, seg_widths, styles[i], block_w, block_h))

    total_h = sum(b[4] for b in line_blocks)
    if position_mode == "top":
        y_top = BAND_H + CAPTION_GAP_BELOW_BROLL
        if len(line_blocks) == 1:
            # Nguoi dung chot 2026-07-29: "text 1 dong se ha xuong giua text 2
            # dong". Truoc day caption 1 dong luon dinh sat mep duoi dai B-roll
            # con caption 2 dong chiem 2 hang -> mat nguoi xem bi nhay len/xuong
            # moi lan doi caption. Nay lay khoi 2-dong (o font 2-dong CHUAN,
            # khong phai font da bi auto-shrink) lam moc CO DINH cho ca video,
            # roi can giua khoi 1-dong vao trong moc do.
            ref_font = ImageFont.truetype(str(FONT_PATH), FONT_SIZE_2LINE)
            rb = ref_font.getbbox("HÂNGY")
            ref_h = 2 * ((rb[3] - rb[1]) + 2 * LINE_PAD_Y)
            y_top += max((ref_h - total_h) // 2, 0)
    else:
        y_top = CAPTION_CENTER_Y - total_h // 2

    y = y_top
    for segments, seg_widths, style, block_w, block_h in line_blocks:
        x0 = (W - block_w) // 2
        draw.rounded_rectangle([x0, y, x0 + block_w, y + block_h], radius=CORNER_RADIUS, fill=style["bg"])
        tx = x0 + LINE_PAD_X
        ty = y + LINE_PAD_Y - font.getbbox("HÂNGY")[1]
        for (seg, is_kw), sw in zip(segments, seg_widths):
            color = style["kw"] if is_kw else style["text"]
            draw.text((tx, ty), seg, font=font, fill=color)
            tx += sw
        y += block_h

    img.save(out_path)
