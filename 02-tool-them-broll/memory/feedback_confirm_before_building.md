---
name: feedback-confirm-before-building
description: "Before implementing a non-trivial visual/technical spec from this user, restate understanding and get confirmation first — don't just build and hope"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 441e0a4b-5a01-49c6-8a82-4500c8b8ce79
---

Before starting a non-trivial build (especially visual effects like blur/fade/positioning), restate the exact interpretation of the requirement in plain text and wait for confirmation before writing code. If any part of the request is ambiguous, ask rather than guess.

**Why:** In the DiLiM AI Editor "Rich Coenzyme Q10" ffmpeg rebuild (2026-07-17), the user asked for a "soft edge" (softness) on the bottom of B-roll clips. I implemented a 40px alpha-transparency gradient that faded B-roll into A-roll underneath (a dissolve/ghosting effect). The user rejected this — they wanted only a light blur on the edge, with B-roll staying fully opaque, not a transparency fade. Building the wrong interpretation burned a full render+verification cycle for nothing. See [[dilim-ai-editor-render-engine-decision]] for the broader ffmpeg-pipeline context this happened in.

**How to apply:** For this user specifically, when a request has room for multiple plausible technical implementations (e.g., "soft edge" could mean alpha fade, gaussian blur, drop shadow, feathered mask, etc.), explicitly describe the planned implementation in concrete terms (not just tool jargon) and pause for a yes before running anything expensive. Use plain text for this, not the AskUserQuestion tool — see [[feedback_no_structured_questions]]. Do this proactively even without being asked, since the user has now stated this as a standing expectation, not a one-off.
