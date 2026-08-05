---
name: dilim-ai-editor-render-engine-decision
description: "DiLiM AI Editor project — decided to drop DaVinci Resolve Scripting API as render engine, use custom ffmpeg + local Whisper + Claude Code pipeline instead"
metadata: 
  node_type: memory
  type: project
  originSessionId: 441e0a4b-5a01-49c6-8a82-4500c8b8ce79
---

Confirmed direction (2026-07-16): the DiLiM Supplement "AI Editor" project (D:\Claude code\ai_editor\, brain doc D:\Claude code\Editor_OS.md) is moving away from DaVinci Resolve Scripting API as the render engine, toward a custom pipeline: ffmpeg (rendering: B-roll overlay, text via drawtext/PIL, audio/music mix via amix/sidechain) + faster-whisper local GPU (transcription, already working) + Claude Code as the reasoning/EDL-decision layer.

**Why:** Resolve Scripting API produced many hard-to-predict bugs across sessions (silent ripple-insert, centerCrop confusion, track collisions, timeline lag) and a real incident where concurrent GPU processes crashed `explorer.exe` during the user's live Resolve export. ffmpeg has been reliable throughout the project (audio/frame extraction, YAVG exposure measurement) and is free/scriptable/headless, unlike the evaluated alternative `browser-use/video-use` (same transcribe→EDL→ffmpeg→self-eval architecture, but needs paid ElevenLabs Scribe transcription — redundant given the free local Whisper already in use — and has no built-in B-roll-insertion or music-mixing support, the two core needs here).

**How to apply:** Treat Resolve-Scripting-API render/timeline-assembly work (Editor_OS.md Section 9, Phase 1/5, `full_pipeline_v2_fixed.py`) as deprecated for the render role — don't propose extending it as the path to final output. The pure decision/reasoning modules (B-roll matching = Phase 2, color/graphic rules = Phase 4, exposure logic = Phase 6, and the full Rule R001-R017 system) remain valid and should be retargeted to feed parameters into an ffmpeg render script instead of Resolve API calls. Before trusting the new direction is production-ready, the first real test should be a short segment combining all 3 layers (B-roll overlay + Vietnamese diacritic text + background music) rendered and eyeballed — this hasn't been done yet, only decided. Review/intervention checkpoints agreed for this new pipeline: (1) a text decision-file (idea/B-roll/text/timestamp table) editable before render, (2) a low-res draft render with debug labels before final export, (3) optional EDL/XML export importable into Resolve/CapCut if the user wants a familiar timeline GUI for final review. See also [dilim-music-mood-library] for the related NAS asset library.
