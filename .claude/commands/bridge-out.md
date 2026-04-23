---
scope: framework
---

# /bridge-out — Hemingway Bridge: End of Session

Write a compact session note and update all TODO files at the end of this session.

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

### Step 3 — Project-to-Wiki check

Before writing session notes, ask:

> "Did this session produce any insight worth promoting to a wiki page?
> (New concept learned, tool evaluated, decision rationale, pattern discovered)
> If yes: create or update the wiki page now, before writing the session note.
>
> Did this session produce a significant decision? If yes: create a page in
> wiki/decisions/ (title, date, why, what it affects, alternatives considered, outcome)."

If the user says yes to either, create/update the pages following normal frontmatter
and index.md rules, then continue to Step 4.

### Step 4 — Write session notes

1. Check if `output/sessions/YYYY-MM-DD.md` already exists for today's date.
   - If it does NOT exist: create it with the frontmatter below.
   - If it DOES exist: skip frontmatter, append a new session block at the end.

2. Write (or append) the following block. **Cap the entire block at ~15 lines.**

---
title: "Session — YYYY-MM-DD"
type: reference
layer: wiki
language: en
tags: [session, bridge, capa/2-wiki]
updated: YYYY-MM-DD
---

## Session — YYYY-MM-DD

**STATE:** [One sentence — where things stand right now.]
**DECISIONS:** [Bullet list, max 5 — what changed and why.]
**NEXT:** [Single concrete next action — specific enough to execute immediately.]
**BLOCKERS:** [Anything blocking progress. Omit this line if none.]

---

### Step 5 — Update log.md

Append a short pointer entry to log.md:
  ## [YYYY-MM-DD] session-end | [topic]
  See: output/sessions/YYYY-MM-DD.md

### Step 6 — Update index.md

If new .md files were created during this session, add them to `index.md`
under the appropriate section.

### Step 7 — Check artifact sync triggers

Scan for `artifacts.md` files in projects touched this session.
For each artifact, check if any files matching its `sync_triggers` patterns
were changed during this session (use git diff to detect).

If sync-relevant files changed, add a warning to the session notes under
**Artifact sync needed** and remind the user in the confirmation message:
"Artifact [name] may need syncing — [list changed trigger files]."

### Step 8 — Commit and push

Stage everything this command modified or created in the previous
steps — session file, `log.md`, `index.md`, any `TODO.md` files,
and any wiki pages created in Step 3. Commit with a clear message
(e.g. `bridge-out — YYYY-MM-DD session end`) and `git push` to
origin.

Bridge-out is a session-close ritual. Session closure is not
complete until the commits are on origin — leaving the session
file, log entry, and TODO updates uncommitted or unpushed means
the next session (possibly on a different machine or days later)
won't see them.

Also push any pre-existing commits on main that were not yet
pushed (e.g. from `/safe-change` merges earlier in this session).
A single `git push` after the bridge-out commit handles both.

### Step 9 — Confirm

Tell the user: "Bridge written, committed, and pushed to origin. TODOs updated. See you next session."

## Rules

- Write in the same language the user was using in this session
- Be specific — vague entries are useless
- "NEXT" must be a real action, not a goal
  Good: "Run /lint in Claude Code and fix the top 3 issues"
  Bad: "Continue exploring memory systems"
- Do not summarize everything — capture what matters for continuity
- One file per day — append to existing file if today's session file already exists
- Only add to index.md if a new file was created (not on append)
- Only add to log.md if a new file was created (not on append)
- The 4-field format (STATE/DECISIONS/NEXT/BLOCKERS) replaces verbose prose.
  If you can't say it in 15 lines, you're over-explaining.
