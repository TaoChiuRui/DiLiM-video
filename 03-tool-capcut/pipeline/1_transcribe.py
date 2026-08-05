# -*- coding: utf-8 -*-
"""BUOC 1 — tach tieng + transcribe word-level.

    python3 1_transcribe.py --job 04-du-an/<ten-job>

Trong job phai co san `source.mp4` / `source.MOV` (nen la SYMLINK toi file goc,
dung chep — file goc thuong vai GB).

BAT BUOC dung --word-timestamps True. Do that tren video DiLiM: moc theo
`segment` lech so voi chu that tu -0.44s den +1.02s, khong deu nen khong co
hang so nao bu duoc. Cham hon ~3 lan nhung khong co duong nao khac.
Xem memory: dilim-caption-timestamp-snap.
"""
import argparse, os, shutil, subprocess, sys

p = argparse.ArgumentParser()
p.add_argument("--job", required=True)
p.add_argument("--model", default="mlx-community/whisper-large-v3-mlx")
a = p.parse_args()

HERE = os.path.abspath(os.path.expanduser(a.job))
if not os.path.isdir(HERE):
    sys.exit(f"khong thay job: {HERE}")

src = next((os.path.join(HERE, n) for n in ("source.mp4", "source.MOV", "source.mov")
            if os.path.exists(os.path.join(HERE, n))), None)
if not src:
    sys.exit(f"job thieu source.mp4 / source.MOV trong {HERE}")

edit = os.path.join(HERE, "edit")
os.makedirs(edit, exist_ok=True)
wav = os.path.join(edit, "audio16k.wav")

print(f"nguon : {os.path.basename(src)}")
if not os.path.exists(wav):
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vn",
                    "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav], check=True)
    print(f"audio : {os.path.getsize(wav)/1048576:.0f} MB")
else:
    print("audio : da co, bo qua")

out = os.path.join(edit, "transcripts_words")
if os.path.exists(os.path.join(out, "audio16k.json")):
    print("transcript word-level da co — xoa thu muc transcripts_words/ neu muon chay lai")
    sys.exit(0)

# Tim `mlx_whisper`: bien moi truong -> PATH -> cho quen thuoc. Truoc 05/08/2026
# chi ghi cung `~/.local/bin/mlx_whisper`, may khac khong co thi chet bang
# `FileNotFoundError` tran, khong noi thieu cai gi va cai bang lenh nao.
#
# LUU Y KHI DONG GOI: mlx_whisper chay tren MLX — CHI CHAY DUOC TREN MAC APPLE
# SILICON. May Intel/Windows phai thay bang openai-whisper hoac faster-whisper;
# cac buoc sau chi can file JSON co `segments[].words[].start`, doi engine nao
# cung duoc mien la giu dung dinh dang do.
mlx = (os.environ.get("MLX_WHISPER")
       or shutil.which("mlx_whisper")
       or next((p for p in (os.path.expanduser("~/.local/bin/mlx_whisper"),
                            "/opt/homebrew/bin/mlx_whisper")
                if os.path.exists(p)), None))
if not mlx:
    sys.exit("khong thay `mlx_whisper`.\n"
             "  cai   : pip install mlx-whisper   (chi Mac Apple Silicon)\n"
             "  hoac  : dat bien MLX_WHISPER=/duong/dan/toi/mlx_whisper\n"
             "  may khong phai Apple Silicon thi doi engine phien am — xem\n"
             "  comment ngay tren dong nay trong 1_transcribe.py")

print("transcribe word-level (cham, ~2.5x thoi luong video) ...")
subprocess.run([mlx, wav, "--model", a.model, "--language", "vi",
                "--word-timestamps", "True", "--output-format", "json",
                "--output-dir", out, "--verbose", "False"], check=True)

import json
d = json.load(open(os.path.join(out, "audio16k.json"), encoding="utf-8"))
n = sum(len(s.get("words", [])) for s in d["segments"])
print(f"-> {len(d['segments'])} segment, {n} chu")

txt = os.path.join(edit, "transcript_readable.txt")
with open(txt, "w", encoding="utf-8") as f:
    for i, s in enumerate(d["segments"]):
        f.write(f"{i:3} [{s['start']:6.2f}-{s['end']:6.2f}] {s['text'].strip()}\n")
print(f"-> {txt}")
