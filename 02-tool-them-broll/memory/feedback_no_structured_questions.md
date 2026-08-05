---
name: feedback-no-structured-questions
description: User dismisses AskUserQuestion prompts without answering; prefers plain-text back-and-forth instead of structured multiple-choice UI
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 441e0a4b-5a01-49c6-8a82-4500c8b8ce79
---

User has repeatedly dismissed AskUserQuestion tool calls (multiple times across sessions) without selecting an option, even when the question was relevant and blocking.

**Why:** User appears to not want to interact with the structured question/multiple-choice UI — likely prefers to just read plain text and reply in the chat in their own words, or finds the UI friction-y compared to typing.

**How to apply:** In this project (DiLiM AI Editor / D:\Claude code), avoid using AskUserQuestion for anything but the most genuinely blocking decisions. When leaning toward asking a question, prefer instead: state the tradeoff in plain text, pick the most sensible default/recommended option yourself, and proceed — let the user correct course via plain text reply if they disagree. If a question truly must block progress, ask it as plain text in the response rather than via the AskUserQuestion tool.
