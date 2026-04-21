# /handoff — Mid-session context compaction

Produce a structured summary of this conversation so the user can `/clear`
and paste it into a fresh chat, continuing without the bloated context.

## When to use

- **Pivot:** finished a topic in this session and moving to another —
  wiping the old context keeps the new work clean.
- **Preventive:** conversation is getting long and the user wants to
  avoid hallucinations before they happen, even if continuing the same
  topic. Fresh context window > accumulated drift.

This is NOT `/bridge-out`. Bridge-out is for "closing the laptop"
(end of day, persists a session file for future days). Handoff is for
"I want a clean chat window right now, same Claude Code session."

## Workflow

Execute these steps in order.

### Step 1 — Generate the summary

Build a markdown block with these 6 sections. Follow the fidelity
priority below.

```markdown
---
title: "Handoff — <slug>"
type: handoff
layer: wiki
language: <en | es | en-es>
tags: [handoff, capa/2-wiki]
updated: YYYY-MM-DD
---

## Handoff — YYYY-MM-DD HH:MM

### STATE
[2-3 lines — where the work stands right now. Concrete, not abstract.]

### FILES TOUCHED
[Bullet list of file:line pointers. NO file content. Just paths + line
numbers when relevant. Group by project/area if many.]

### DECISIONS
[Agreements closed in this conversation that the new chat must respect.
Preserve verbatim when possible. If the user said "always do X" or
"never do Y" or chose option A over B, capture it here with the reason.]

### OPEN QUESTIONS
[Anything unresolved. If none, write "None."]

### NEXT
[1-2 concrete next actions. Specific enough to execute immediately.]

### RESUME PROMPT
[Copy-paste ready paragraph for the new chat. Self-contained. Must
include: what the user is doing, relevant decisions from above, what
comes next. ~100-200 words max. The user pastes this after /clear.]
```

### Step 2 — Write the handoff file (safety net)

Write the exact same block to:

```
output/handoffs/YYYY-MM-DD-HHMM-<slug>.md
```

- `HHMM` = 24h local time, zero-padded (e.g. `0930`, `1545`). Prevents
  filename collision when multiple handoffs happen the same day.
- `<slug>` = kebab-case of the topic, truncated to ~30 chars. Should
  match the one-liner that goes to log.md.
- Create the `output/handoffs/` directory if it does not exist.

This directory is `.gitignored` — handoffs are a local safety net, not
shared content. If the terminal dies before the user pastes the
summary into a new chat, the file is still on disk.

### Step 3 — Display the summary inline

Output the same block to the chat so the user reads it and picks the
RESUME PROMPT to paste. Include the handoff file path at the top:

> `Saved to: output/handoffs/YYYY-MM-DD-HHMM-<slug>.md`

### Step 4 — Append to log.md

Add a two-line entry with pointer to the file:

```
## [YYYY-MM-DD] handoff | <one-liner describing what closed or what continues>

See: output/handoffs/YYYY-MM-DD-HHMM-<slug>.md
```

Keep log.md lean — the full summary lives in the handoff file, not
in log.md.

### Step 5 — Apply TODO changes (conditional)

Scan this conversation for changes that affect TODOs:

- New in-progress item (work started)
- Item moved to done
- Item moved to backlog or on-hold
- New backlog item discovered

If found: update the relevant `TODO.md` (project or area) and the root
`TODO.md` status counts. Commit is the user's call later — do not
auto-commit.

If no TODO changes: skip silently. Do NOT invent TODO changes to fill
the step.

### Step 6 — Tell the user what to do next

End with a short instruction:

> "Summary saved and shown above. Review it, then `/clear` and paste
> the RESUME PROMPT at the start of the new chat to continue."

## Fidelity priority

When output space is constrained, compress in this order:

**DECISIONS > STATE > OPEN QUESTIONS > FILES > NEXT > RESUME PROMPT body**

- **DECISIONS** is the most important section. Never sub-compress. If
  a decision took 10 messages to reach, it still lands here — losing it
  wastes all that back-and-forth.
- **STATE** must preserve enough context that the new chat understands
  what's in flight without reading the repo.
- **RESUME PROMPT** can be short as long as it points at the right
  starting action — it's an entry point, not a briefing.

## Not this command's job

- `/clear` — the user runs it manually after reading the summary.
- Session file — that's `/bridge-out`.
- Orienting the new chat with full-repo context (CLAUDE.md, artifacts,
  old sessions) — that's `/bridge`. The RESUME PROMPT is intentionally
  task-focused; the new chat only reads the repo when it needs to.
- Auto-commit of TODO changes — the user decides when to commit.

## Relationship to other commands

| Command | Use case | Persists |
|---|---|---|
| `/handoff` | Same session; pivot OR preventive compaction | handoff file in `output/handoffs/` (gitignored, local safety net) + log.md 1 line + conditional TODOs |
| `/bridge-out` | End of work day — will return hours/days later | session file (committed) + log + TODOs + index |
| `/bridge` | Start of new session (after bridge-out or cold) | nothing new — reads to orient |

Rule of thumb: `/handoff` is lighter than `/bridge-out`. If you're
about to close the laptop, use `/bridge-out`. If you're about to
`/clear` and keep working, use `/handoff`.

## Rules

- Output in the same language the user was using in this session.
- Be specific — vague summaries defeat the purpose.
- **DECISIONS and STATE are non-negotiable.** Everything else can be
  terse; these cannot.
- Do not re-dump the entire conversation. Summarize.
- The user reads the summary in the chat before `/clear` — they are
  the final judge of whether something got missed. If something is
  missing, they tell you before clearing.
