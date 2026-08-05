# -*- coding: utf-8 -*-
"""BUOC 1 — Transcribe word-level. Chay 1 lan cho ca job.
Timestamp cap CAU lech vai giay, khong canh duoc diem chen -> BAT BUOC
word_timestamps=True. Ket qua: <job>/v<N>/{segments,words}.json
"""
import json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pipeline")))
from paths import WHISPER_MODEL, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE  # noqa: E402
from faster_whisper import WhisperModel  # noqa: E402

# >>> SUA: thu muc chua A-roll goc + danh sach file
SRC = r"D:\download\Video cho Claude test\Raydel policpsanol"
HERE = os.path.dirname(os.path.abspath(__file__))
VIDS = [f"Video{i}.mp4" for i in range(1, 10)]

m = WhisperModel(WHISPER_MODEL, device=WHISPER_DEVICE, compute_type=WHISPER_COMPUTE_TYPE)
for i, v in enumerate(VIDS, 1):
    d = os.path.join(HERE, f"v{i}")
    os.makedirs(d, exist_ok=True)
    if os.path.exists(os.path.join(d, "words.json")):
        print(f"v{i} da co, bo qua", flush=True)
        continue
    t0 = time.time()
    print(f"\n########## v{i}: {v}", flush=True)
    segs, _ = m.transcribe(os.path.join(SRC, v), language="vi",
                           vad_filter=True, word_timestamps=True)
    S, W = [], []
    for s in segs:
        S.append({"start": s.start, "end": s.end, "text": s.text.strip()})
        for w in (s.words or []):
            W.append({"start": w.start, "end": w.end, "word": w.word})
    json.dump(S, open(os.path.join(d, "segments.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    json.dump(W, open(os.path.join(d, "words.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"--> {len(S)} segment, {len(W)} tu  ({time.time()-t0:.0f}s)", flush=True)
print("\nXONG HET", flush=True)
