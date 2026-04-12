# /bridge-out — Hemingway Bridge: End of Session

Write a session note and update all TODO files at the end of this session.

## Instructions

Read the conversation history of this session, then execute all steps below.

### Step 1 — Update TODO files

Identify which project(s), courses, or areas were touched this session.
For each touched area, update its TODO.md:

- Move completed items to **Done (last 30 days)** with today's date
- Update in-progress items if status changed
- Add any new tasks discovered during the session
- Drop Done items older than 30 days
- Omit any section that would be empty

### Step 2 — Update root TODO.md

For each area that changed in Step 1, recount the status summary line:
count in progress, backlog, and blocked items. Update the root TODO.md.

### Step 3 — Write session notes

1. Check if `output/sessions/YYYY-MM-DD.md` already exists for today's date.
   - If it does NOT exist: create it with the frontmatter below.
   - If it DOES exist: skip frontmatter, append a new session block at the end.

2. Write (or append) the following block:

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

### Step 4 — Update log.md

Append a short pointer entry to log.md:
  ## [YYYY-MM-DD] session-end | [topic]
  See: output/sessions/YYYY-MM-DD.md

### Step 5 — Update index.md

If new .md files were created during this session, add them to `index.md`
under the appropriate section.

### Step 6 — Check artifact sync triggers

Scan for `artifacts.md` files in projects touched this session.
For each artifact, check if any files matching its `sync_triggers` patterns
were changed during this session (use git diff to detect).

If sync-relevant files changed, add a warning to the session notes under
**Artifact sync needed** and remind the user in the confirmation message:
"Artifact [name] may need syncing — [list changed trigger files]."

### Step 7 — Confirm

Tell the user: "Bridge written. TODOs updated. See you next session."

## Rules

- Write in the same language the user was using in this session
- Be specific — vague entries are useless
- "Next exact action" must be a real action, not a goal
  Good: "Run /lint in Claude Code and fix the top 3 issues"
  Bad: "Continue exploring memory systems"
- Do not summarize everything — capture what matters for continuity
- One file per day — append to existing file if today's session file already exists
- Only add to index.md if a new file was created (not on append)
- Only add to log.md if a new file was created (not on append)
