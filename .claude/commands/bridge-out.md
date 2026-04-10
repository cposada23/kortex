# /bridge-out — Hemingway Bridge: End of Session

Write a session note at the end of this session.

## Instructions

Read the conversation history of this session.

1. Create a new file at: output/sessions/YYYY-MM-DD.md
   (use today's date)

2. Write the following block:

---
title: "Session — YYYY-MM-DD"
type: reference
layer: wiki
language: en
tags: [session, bridge, capa/2-wiki]
updated: YYYY-MM-DD
---

## Session — YYYY-MM-DD

### Where we left off
[1-3 sentences. What were we working on? What was the last thing we did?]

### Decisions made
[Bullet list. What did we decide and why? Include the reasoning, not just the conclusion.]

### Open threads
[Bullet list. What came up but wasn't resolved? What's worth revisiting?]

### Context for next Claude
[What does the next session need to know to pick up without re-explanation?
Include: active project, current level/step, tools involved, anything non-obvious.]

### Next exact action
[One sentence. The single most concrete next step. Specific enough that
the next session can start executing immediately.]

---

3. Append a short pointer entry to log.md:
   ## [YYYY-MM-DD] session-end | [topic]
   See: output/sessions/YYYY-MM-DD.md

4. Add the new session file to index.md under ## Output > Sessions

5. Confirm to the user: "Bridge written. See you next session."

## Rules

- Write in the same language the user was using in this session
- Be specific — vague entries are useless
- "Next exact action" must be a real action, not a goal
  Good: "Run /lint in Claude Code and fix the top 3 issues"
  Bad: "Continue exploring memory systems"
- Do not summarize everything — capture what matters for continuity
- Never overwrite an existing session file — always use today's date
- Always update index.md after creating the session file
