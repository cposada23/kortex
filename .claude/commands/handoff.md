---
scope: framework
---

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

### Step 0 — Detect repo state (MANDATORY)

Before generating the summary, run these commands and record the
output — the result changes what Step 1 MUST include:

```
git branch --show-current
git status --short
git log origin/main..main --oneline
```

Classify the state into one of three buckets:

- **CLEAN-MAIN** — on `main`, no uncommitted changes, no unpushed commits.
  Normal handoff; nothing special to flag.
- **MID-SAFE-CHANGE** — on a feature branch (not `main`) AND there are
  uncommitted or uncommitted+staged changes. The user is mid `/safe-change`
  waiting for YES/NO. The new chat MUST NOT auto-commit, auto-merge, or
  switch branches.
- **DIRTY-MAIN-OR-OTHER** — any other state (uncommitted changes on main,
  feature branch with everything committed, unpushed commits on main, etc.).
  Flag the specific condition so the new chat knows what it's walking into.

Record the classification + the raw `git status --short` output for use in
Step 1. This detection is **mandatory** — skipping it is the #1 way a new
chat breaks a safe-change flow by committing to the wrong place.

### Step 1 — Generate the summary

Build a markdown block with these 6 sections. Follow the fidelity
priority below. **The STATE and RESUME PROMPT sections have mandatory
first-line rules driven by Step 0.**

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
[**FIRST LINE IS MANDATORY when Step 0 is MID-SAFE-CHANGE or DIRTY-MAIN-OR-OTHER.**
Format: `Git: <branch-name> — <clean | N uncommitted | mid /safe-change awaiting YES/NO | N unpushed on main>`.
Then 2-3 lines on where the work stands right now. Concrete, not abstract.
If MID-SAFE-CHANGE: state explicitly that the new chat must NOT commit,
merge, or switch branches until the user decides YES or NO.]

### CONTEXT
[2-4 sentences on *why* this conversation exists. What came before it,
what upstream goal it serves, what the user was trying to accomplish
when the session started. The new chat inherits only the RESUME PROMPT
by default — without context it cannot tell whether current state is
"almost done" or "early exploration". Include: the trigger for the
session, the parent project/goal, any prior session that led here.]

### DECISIONS
[Agreements closed in this conversation that the new chat must respect.
**Each decision must include the alternative considered and the reason**
— not just "chose A" but "chose A over B because C". If the user said
"always do X" or "never do Y", preserve the phrasing verbatim. If a
decision is load-bearing for future work, flag it. Also include
non-decision constraints the user mentioned (deadlines, tool
preferences, energy state) that shape how work should proceed.]

### REJECTED / EXPLORED
[Approaches we tried or considered and decided against, each with the
reason. This is the #1 section that protects the new chat from
wasting tokens re-trying failed paths. Format: `- <approach> — rejected because <reason>`.
If nothing was rejected in this session: "None."]

### FILES TOUCHED
[Bullet list of file:line pointers. NO file content. Just paths + line
numbers when relevant. Group by project/area if many.]

### OPEN QUESTIONS
[Anything unresolved — half-investigated rabbit holes, questions the
user asked that weren't fully answered, ambiguities the new chat needs
to know about. If none, write "None."]

### NEXT
[1-2 concrete next actions. Specific enough to execute immediately.
If MID-SAFE-CHANGE, the first NEXT action MUST be "ask the user for
YES/NO to close the pending /safe-change" — do not skip ahead.]

### RESUME PROMPT
[Self-contained briefing for the new chat. **250-400 words.** The user
pastes this after /clear and the new chat must be able to continue
productively from this alone. Must cover, in prose (not bullets):
1. Git state + any MID-SAFE-CHANGE warning (first sentence).
2. What the user is doing and why (the CONTEXT, compressed).
3. Key decisions already closed that the new chat must respect.
4. Approaches already rejected — "don't re-try X".
5. The immediate next action.

**MANDATORY when MID-SAFE-CHANGE:** the first sentence must name the
branch and warn that a /safe-change is pending YES/NO — e.g. "Estás
en rama `feature/...` a medio /safe-change esperando YES/NO; no
commitees ni hagas merge hasta que Camilo decida." This survives the
user copy-pasting only the RESUME PROMPT and skipping the rest.

Err on the side of more context. 400 words the user's eyes skim once
is much cheaper than 50 messages of the new chat rediscovering the
same ground.]
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

### Step 3 — Point the user at the file

Do NOT paste the summary block into the chat. The file already lives
on disk from Step 2 — the user opens it in their IDE, reads it there,
and copies the RESUME PROMPT from the file. Re-printing the full block
in the chat burns context and duplicates content they already have on
disk.

Output only the file path and a brief instruction:

> `Handoff saved to: output/handoffs/YYYY-MM-DD-HHMM-<slug>.md — open in your IDE to review and copy the RESUME PROMPT.`

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
`TODO.md` status counts. **Leave uncommitted** — the user needs to see
the edits in `git status` so they can review everything together before
merging.

If no TODO changes: skip silently. Do NOT invent TODO changes to fill
the step.

### Step 6 — No commit, no push

**`/handoff` never commits or pushes.** The log.md append (Step 4) and
any TODO edits (Step 5) stay uncommitted in the working tree. The
handoff file itself (Step 2) is gitignored.

This is intentional: if `/handoff` commits anything, those changes
disappear from `git status` — the user loses visibility into what's
pending review. Keeping everything uncommitted means the user can open
the IDE's source-control panel, see every modified file, and review
them all before deciding what to commit.

Commit and push both happen later via the user's explicit call:
- `/safe-change` YES → commits + merges + pushes
- Manual `git add` / `git commit` / `git push`
- `/bridge-out` → end-of-day ritual that commits + pushes

### Step 7 — Tell the user what to do next

End with a short instruction:

> "Handoff file ready. Open it in your IDE, review, then `/clear`
> and paste the RESUME PROMPT at the start of the new chat to continue."

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
- Committing or pushing anything. `/handoff` leaves log.md and TODO
  edits uncommitted in the working tree so the user can review them
  in the IDE's source-control panel. Commit + push are the user's
  call via `/safe-change` YES, `/bridge-out`, or manual git.

## Relationship to other commands

| Command | Use case | Persists |
|---|---|---|
| `/handoff` | Same session; pivot OR preventive compaction | handoff file in `output/handoffs/` (gitignored, local safety net) + log.md 1 line (uncommitted) + conditional TODO edits (uncommitted). **No commit, no push** — the user sees everything in `git status` and decides what to commit. |
| `/bridge-out` | End of work day — will return hours/days later | session file + log + TODOs + index (all committed and pushed to origin) |
| `/bridge` | Start of new session (after bridge-out or cold) | nothing new — reads to orient |

Rule of thumb: `/handoff` is lighter than `/bridge-out`. If you're
about to close the laptop, use `/bridge-out`. If you're about to
`/clear` and keep working, use `/handoff`.

## Rules

- Output in the same language the user was using in this session.
- Be specific — vague summaries defeat the purpose.
- **DECISIONS and STATE are non-negotiable.** Everything else can be
  terse; these cannot.
- **Step 0 (repo state detection) is mandatory.** Never generate a
  handoff without running the three git commands first. The
  classification drives what STATE and RESUME PROMPT must include.
- **If MID-SAFE-CHANGE, the RESUME PROMPT's first sentence must warn
  about the pending /safe-change.** Users often copy only the RESUME
  PROMPT — this is the one line guaranteed to reach the new chat.
- `/handoff` NEVER commits, pushes, merges, or switches branches. All
  log.md and TODO edits stay uncommitted so the user keeps visibility
  on them in the IDE's source-control panel. Commit + push happen via
  `/safe-change` YES, `/bridge-out`, or manual git.
- **When in doubt, include it.** The handoff is read once by the user
  and once by the new chat; the alternative is the new chat
  rediscovering the same info by trial and error, which costs 10x more
  tokens. Err on the side of more context.
- Do not re-dump the entire conversation. Summarize.
- Do NOT paste the handoff block into the chat after Step 2 writes it
  to disk. The user reads it in the IDE, not in the chat.
- The user reads the summary in their IDE before `/clear` — they are
  the final judge of whether something got missed. If something is
  missing, they tell you before clearing.
