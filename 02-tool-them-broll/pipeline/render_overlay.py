# -*- coding: utf-8 -*-
"""Ghep B-roll (dai tren, 672px) + caption (style Dr Son, font Anton) thanh
1 file overlay ProRes 4444 (.mov, kenh alpha THAT, khong can chroma-key) de
nguoi dung tu cheo vao project cua ho. Dung ProRes 4444 thay vi HAP vi HAP
khong import duoc vao DaVinci Resolve tren Windows (bug that gap 2026-07-21,
rat co the do thieu QuickTime/component HAP) - ProRes 4444 la dinh dang
Resolve ho tro native, khong can cai them gi.

Usage:
    python render_overlay.py <job_dir>

<job_dir> phai co:
    captions.json   - [{"from": int, "durationInFrames": int, "text": str, "variant": str|null}, ...]
    broll_plan.json - [{"from": int, "durationInFrames": int, "path": str, "is_image": bool,
                        "src_start_s": float (optional, mac dinh 0.0 - diem bat dau LAY TU
                        NGUON, khong phai vi tri tren timeline)}, ...]
    meta.json       - {"total_frames": int, "fps": int}
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from caption_style import render_caption_png, StyleCounters, W, H  # noqa: E402

BAND_H = 672          # dai tren cho B-roll, khop voi thiet lap DiLiM da co
BLUR_BAND = 20
BLUR_RADIUS = 6
FADE_FRAMES = 9        # ~0.15s @ 60fps, fade in/out cho caption


def run(args, label=""):
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        print(f"FAILED [{label}]")
        print(r.stderr[-3000:])
        raise RuntimeError("ffmpeg failed: " + label)
    return r


ALPHA_CODEC_ARGS = ["-c:v", "prores_ks", "-profile:v", "4", "-pix_fmt", "yuva444p10le"]


# BUG THAT (2026-07-29): truoc day "-t" duoc tinh dung bang n_frames/fps roi
# format 4 chu so thap phan. Voi cac gia tri nhu 188/60 = 3.13333... -> "3.1333"
# nguon lavfi ket thuc SOM hon dung 1 frame, "-frames:v n" khong bu lai duoc ->
# chunk thieu 1 frame. Loi don lai qua tung chunk khien CA TRACK ngan dan va moi
# caption phia sau bi day len som hon so voi loi noi. Cach sua: cho "-t" du dai
# ra vai frame, de "-frames:v" cat chinh xac.
def _t_arg(n_frames: int, fps: int) -> str:
    return f"{(n_frames + 2) / fps:.4f}"


def transparent_chunk(n_frames: int, fps: int, out_path: Path):
    run([
        "ffmpeg", "-y", "-f", "lavfi",
        "-i", f"color=black@0.0:s={W}x{H}:r={fps},format=yuva444p10le",
        "-t", _t_arg(n_frames, fps),
        "-frames:v", str(n_frames),
        *ALPHA_CODEC_ARGS,
        str(out_path),
    ], f"transparent_{n_frames}")


def _native_duration_s(path: str) -> float:
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def _band_chain(src_label: str, out_label: str, fps: int, tag: str, crop_bias: float = 0.5) -> str:
    """Chuoi filter dua 1 nguon bat ky ve dung dai B-roll (WxBAND_H) roi pad
    xuong full khung, phan duoi trong suot. tag phai duy nhat trong 1 filter graph."""
    top_h = BAND_H - BLUR_BAND
    return (
        f"[{src_label}]scale={W}:{BAND_H}:force_original_aspect_ratio=increase,"
        f"crop={W}:{BAND_H}:0:(ih-oh)*{crop_bias},fps={fps},format=yuva444p10le,split=2[a{tag}][b{tag}];"
        f"[a{tag}]crop={W}:{top_h}:0:0[sharp{tag}];"
        f"[b{tag}]boxblur={BLUR_RADIUS}:2[blur{tag}];"
        f"[blur{tag}][sharp{tag}]overlay=x=0:y=0,pad={W}:{H}:0:0:color=black@0.0[{out_label}]"
    )


def _src_args(path: str, is_image: bool, src_start_s: float, loop_video: bool = False) -> list:
    if is_image:
        return ["-loop", "1", "-i", path]
    pre = ["-stream_loop", "-1"] if loop_video else []
    return [*pre, "-ss", f"{src_start_s:.4f}", "-i", path]


def broll_xfade_chunk(prev: dict, cur: dict, n_frames: int, fps: int, out_path: Path,
                      prev_src_at_cut: float):
    """N frame chuyen tiep Cross Dissolve: clip TRUOC chay tiep, clip SAU mo dan
    de len (alpha 0->1). Dung o cho hai doan B-roll SAN PHAM nam sat nhau, de
    khong bi giat khi cat cung (nguoi dung chot 2026-07-29)."""
    dur_s = n_frames / fps
    fc = (
        _band_chain("0:v", "pv", fps, "p", prev.get("crop_bias", 0.5)) + ";"
        + _band_chain("1:v", "cv0", fps, "c", cur.get("crop_bias", 0.5)) + ";"
        + f"[cv0]fade=t=in:st=0:d={dur_s:.4f}:alpha=1[cv];"
        + "[pv][cv]overlay=x=0:y=0:shortest=1[out]"
    )
    run([
        "ffmpeg", "-y",
        *_src_args(prev["path"], prev.get("is_image", False), prev_src_at_cut),
        *_src_args(cur["path"], cur.get("is_image", False), cur.get("src_start_s", 0.0)),
        "-filter_complex", fc, "-map", "[out]",
        "-frames:v", str(n_frames),
        *ALPHA_CODEC_ARGS, str(out_path),
    ], f"xfade_{Path(prev['path']).stem[:18]}_{Path(cur['path']).stem[:18]}")


def broll_chunk(path: str, is_image: bool, n_frames: int, fps: int, out_path: Path,
                src_start_s: float = 0.0, crop_bias: float = 0.5, key_black: bool = False):
    """crop_bias: vi tri cat theo CHIEU DOC khi nguon cao hon dai B-roll.
    0.5 = giua (mac dinh), 0 = lay phan tren cung. Can cho anh dang van ban/
    giay chung nhan - cat giua chi ra doan chu nho, mat het tieu de va dau moc.

    key_black: clip quay tren NEN DEN va KHONG co kenh alpha (vd 6 clip bubble
    thanh phan ing_*.mp4, pix_fmt yuv444p10le). Neu de nguyen, ca dai B-roll se
    thanh mot khoi den dac. Da test 2026-07-30: colorkey 0.30 + alpha 0.72 cho
    ra nen trong suot ma bong bong VAN giu duoc khoi cau (chi colorkey khong thi
    bong bong bi rong ruot thanh cai vong). Voi clip da key thi BO buoc blur dai
    vi khong con canh dai cung can lam mem."""
    top_h = BAND_H - BLUR_BAND
    pad_hold = "" if is_image else "tpad=stop_mode=clone:stop_duration=600,"
    if key_black:
        vf = (
            f"{pad_hold}scale={W}:{BAND_H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{BAND_H}:0:(ih-oh)*{crop_bias},fps={fps},format=yuva444p10le,"
            f"colorkey=0x000000:0.30:0.10,colorchannelmixer=aa=0.72,"
            f"pad={W}:{H}:0:0:color=black@0.0[padded]"
        )
    else:
        vf = (
            f"{pad_hold}scale={W}:{BAND_H}:force_original_aspect_ratio=increase,"
            f"crop={W}:{BAND_H}:0:(ih-oh)*{crop_bias},fps={fps},"
            f"format=yuva444p10le,split=2[a][b];"
            f"[a]crop={W}:{top_h}:0:0[sharp];"
            f"[b]boxblur={BLUR_RADIUS}:2[blurred];"
            f"[blurred][sharp]overlay=x=0:y=0,pad={W}:{H}:0:0:color=black@0.0[padded]"
        )
    if is_image:
        src_args = ["-loop", "1", "-i", path]
    else:
        # Diem bat dau lay tu nguon (src_start_s) - THIEU HOAN TOAN truoc day
        # (bug that gap 2026-07-21): moi clip luon bi cat tu giay 0 cua file
        # goc bat ke canh can dung nam o dau trong file, dan den chon dung
        # file nhung sai doan (VD file "cam dien thoai" nhung doan dien thoai
        # nam o giay 16-22/26, code cu luon lay 0-6.6s la doan khac hoan toan).
        needed_s = n_frames / fps
        native_s = _native_duration_s(path)
        available_s = max(native_s - src_start_s, 0) if native_s > 0 else 0
        # KHONG BAO GIO LAP LAI clip (nguoi dung chot 2026-07-31: thay clip
        # chay lai giua chung doan -> doc ra la "lap broll"). Neu doan can dai
        # hon phan phim con lai thi GIU NGUYEN FRAME CUOI (tpad clone) - khong
        # lap, khong de dai B-roll trong.
        src_args = ["-ss", f"{src_start_s:.4f}", "-i", path]
        if native_s > 0 and available_s < needed_s:
            print(f"    (giu frame cuoi {needed_s-available_s:.2f}s: {Path(path).name[:40]})")
    run([
        "ffmpeg", "-y", *src_args,
        "-filter_complex", vf,
        "-map", "[padded]",
        "-frames:v", str(n_frames),
        *ALPHA_CODEC_ARGS,
        str(out_path),
    ], f"broll_{Path(path).stem}")


PUSH_FRAMES = 10   # ~0.17s @ 60fps - thoi gian truot vao vi tri luc vao
PUSH_OFFSET = 90   # px - bat dau lech BEN TRAI vi tri cuoi bao nhieu, truot SANG PHAI vao cho
                   # (nguoi dung chot 2026-07-21: push tu trai sang phai, khong phai tu duoi len)


def caption_chunk(caption: dict, counters: StyleCounters, fps: int, tmp_dir: Path, out_path: Path, position_mode: str):
    n_frames = caption["durationInFrames"]
    png_path = tmp_dir / f"caption_frame_{out_path.stem}.png"
    render_caption_png(caption, counters, str(png_path), position_mode=position_mode)
    dur_s = n_frames / fps
    push_dur = min(PUSH_FRAMES, n_frames // 3 or 1) / fps
    fade_d = min(FADE_FRAMES, n_frames // 3 or 1) / fps
    fade_start = max(dur_s - fade_d, 0)
    x_expr = f"-{PUSH_OFFSET}*(1-min(t/{push_dur:.4f}\\,1))" if push_dur > 0 else "0"
    run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=black@0.0:s={W}x{H}:r={fps},format=yuva444p10le",
        "-t", _t_arg(n_frames, fps),
        "-loop", "1", "-i", str(png_path),
        "-filter_complex",
        f"[1:v]format=yuva444p10le,fps={fps}[capt];"
        f"[0:v][capt]overlay=x='{x_expr}':y=0:shortest=1,"
        f"fade=t=out:st={fade_start:.4f}:d={fade_d:.4f}:alpha=1[out]",
        "-map", "[out]",
        "-frames:v", str(n_frames),
        *ALPHA_CODEC_ARGS,
        str(out_path),
    ], f"caption_{n_frames}")


def build_track(items: list, total_frames: int, fps: int, chunk_dir: Path, track_out: Path, make_chunk):
    """items: list of (from, durationInFrames, payload) da sap xep, khong chong lap.
    make_chunk(payload, n_frames, out_path) -> ghi file chunk."""
    chunk_dir.mkdir(parents=True, exist_ok=True)
    chunks = []
    cursor = 0
    for idx, (start, dur, payload) in enumerate(items):
        if start > cursor:
            gap = start - cursor
            out = chunk_dir / f"gap_{idx}.mov"
            if not out.exists():
                transparent_chunk(gap, fps, out)
            chunks.append(out)
        out = chunk_dir / f"item_{idx}.mov"
        if not out.exists():
            make_chunk(payload, dur, out)
        chunks.append(out)
        cursor = start + dur
    if cursor < total_frames:
        out = chunk_dir / "gap_tail.mov"
        if not out.exists():
            transparent_chunk(total_frames - cursor, fps, out)
        chunks.append(out)

    listfile = chunk_dir / "list.txt"
    with open(listfile, "w", encoding="utf-8") as fh:
        for c in chunks:
            fh.write(f"file '{c.resolve()}'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile), "-c", "copy", str(track_out)],
        "concat_track")


def build_broll_track(plan: list, total_frames: int, fps: int, chunk_dir: Path, track_out: Path):
    """Nhu build_track nhung ho tro khoa "xfade_prev" (so frame Cross Dissolve
    voi doan LIEN TRUOC). Cach chia: doan truoc ngan lai N frame, chen 1 chunk
    chuyen tiep N frame, doan sau day diem lay nguon len N frame -> tong do dai
    timeline khong doi."""
    chunk_dir.mkdir(parents=True, exist_ok=True)
    plan = sorted(plan, key=lambda x: x["from"])
    chunks, cursor = [], 0

    # Vong 1: chot so frame chuyen tiep thuc te cho tung doan.
    # Chuyen tiep chiem N frame DAU cua doan hien tai; doan truoc phai con du
    # them N frame nguon de "chay tiep" trong luc doan sau mo dan de len.
    for i, cur in enumerate(plan):
        prev = plan[i - 1] if i else None
        xf = int(cur.get("xfade_prev", 0) or 0)
        if not (xf and prev and prev["from"] + prev["durationInFrames"] == cur["from"]):
            cur["_xf"] = 0
            continue
        xf = min(xf, prev["durationInFrames"] // 3, cur["durationInFrames"] // 3)
        if not prev.get("is_image"):
            native = _native_duration_s(prev["path"])
            spare = native - prev.get("src_start_s", 0.0) - prev["durationInFrames"] / fps
            xf = min(xf, max(int(spare * fps), 0))
        cur["_xf"] = max(xf, 0)

    for idx, item in enumerate(plan):
        xf = item["_xf"]
        if item["from"] > cursor:
            out = chunk_dir / f"gap_{idx}.mov"
            if not out.exists():
                transparent_chunk(item["from"] - cursor, fps, out)
            chunks.append(out)
            cursor = item["from"]

        if xf:
            prev = plan[idx - 1]
            prev_at_cut = prev.get("src_start_s", 0.0)
            if not prev.get("is_image"):
                prev_at_cut += prev["durationInFrames"] / fps
            out = chunk_dir / f"xfade_{idx}.mov"
            if not out.exists():
                broll_xfade_chunk(prev, item, xf, fps, out, prev_at_cut)
            chunks.append(out)
            cursor += xf

        dur = item["durationInFrames"] - xf
        if dur <= 0:
            continue
        src = item.get("src_start_s", 0.0) + (0.0 if item.get("is_image") else xf / fps)
        out = chunk_dir / f"item_{idx}.mov"
        if not out.exists():
            broll_chunk(item["path"], item.get("is_image", False), dur, fps, out, src,
                        item.get("crop_bias", 0.5), item.get("key_black", False))
        chunks.append(out)
        cursor += dur

    if cursor < total_frames:
        out = chunk_dir / "gap_tail.mov"
        if not out.exists():
            transparent_chunk(total_frames - cursor, fps, out)
        chunks.append(out)

    listfile = chunk_dir / "list.txt"
    with open(listfile, "w", encoding="utf-8") as fh:
        for c in chunks:
            fh.write(f"file '{c.resolve()}'\n")
    run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile), "-c", "copy", str(track_out)],
        "concat_broll")


def main(job_dir: str):
    job = Path(job_dir)
    captions = json.loads((job / "captions.json").read_text(encoding="utf-8"))
    broll_plan = json.loads((job / "broll_plan.json").read_text(encoding="utf-8"))
    meta = json.loads((job / "meta.json").read_text(encoding="utf-8"))
    total_frames, fps = meta["total_frames"], meta["fps"]
    # Vi tri text CO DINH cho ca video, dong bo voi vi tri B-roll cua video nay
    # (nguoi dung chot 2026-07-21: "b-roll o tren thi text LUON LUON o tren").
    position_mode = meta.get("broll_position", "top")

    out_dir = job / "render_tmp"
    out_dir.mkdir(exist_ok=True)

    print("=== B-roll track ===")
    broll_track = out_dir / "broll_track.mov"
    build_broll_track(broll_plan, total_frames, fps, out_dir / "broll_chunks", broll_track)

    print("\n=== Caption track ===")
    counters = StyleCounters()
    caption_items = [(c["from"], c["durationInFrames"], c) for c in sorted(captions, key=lambda x: x["from"])]
    caption_track = out_dir / "caption_track.mov"
    build_track(
        caption_items, total_frames, fps, out_dir / "caption_chunks", caption_track,
        lambda c, n, out: caption_chunk(c, counters, fps, out_dir, out, position_mode),
    )

    print("\n=== Ghep lop cuoi (nen trong suot + broll + caption) ===")
    final_out = job / "overlay_PRORES4444.mov"
    run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", f"color=black@0.0:s={W}x{H}:r={fps},format=yuva444p10le",
        "-t", f"{total_frames / fps:.4f}",
        "-i", str(broll_track),
        "-i", str(caption_track),
        "-filter_complex",
        "[0:v][1:v]overlay=x=0:y=0:shortest=1[a];"
        "[a][2:v]overlay=x=0:y=0:shortest=1[out]",
        "-map", "[out]",
        "-frames:v", str(total_frames),
        *ALPHA_CODEC_ARGS,
        str(final_out),
    ], "final_composite")

    print("\nXONG:", final_out)


if __name__ == "__main__":
    main(sys.argv[1])
