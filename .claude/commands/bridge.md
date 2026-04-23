---
scope: framework
---

# /bridge — Session Start Ritual

Run at the start of every Claude Code session.

## Steps

0. **Sync with remote** — Before reading any local state, pull `main` so the
   session starts on the latest commits (another machine, Claude.ai mobile,
   another flow may have pushed since last session).
   - Run `git status` first. If current branch is NOT `main` (e.g., mid-`/safe-change`),
     skip the pull and note in the bridge output: "Skipped pull — on branch [X]".
   - If on `main`: run `git fetch origin && git pull origin main --ff-only`.
   - If `--ff-only` fails (local diverged from remote), stop and surface the
     conflict so the owner decides how to reconcile. Do NOT attempt a merge.
   - If the pull brought material changes, include a
     "**Changes pulled from remote:** N files updated" line in the bridge output.

1. **Staleness check** — Before reading any session file, find the most recent
   file in `output/sessions/`. If the most recent session file is NOT from today
   or yesterday, show:
   "No session file since [DATE]. Want to run /bridge-recovery? (y/n)"
   - If **y**: run /bridge-recovery, then continue from step 2 (skip steps 0 and 1 on re-entry)
   - If **n**: continue with normal bridge (the old session file will be read in step 6
     but the user has been warned it may be stale)

2. Read `CLAUDE.md` — get schema and strategic orientation
3. Read `index.md` (Nivel 1 overview) — the entry point to the hierarchical
   indexes. Then, based on where active work lives (inferred from step 4
   below), read the zone indexes relevant to that work:
   - Active work in a project → read `projects/INDEX.md`
   - Active work touches synthesis → read `wiki/INDEX.md`
   - Active work is course consumption → read `sources/INDEX.md`
   - Inbox triage pending → read `inbox/INDEX.md`
   - Output archaeology (finding an old session / audit / handoff) →
     read `output/INDEX.md`

   Do NOT read all zone indexes by default. Target only what the session
   needs. If the next action is unclear until step 4 completes, defer the
   zone-index reads until after TODOs are known.

4. Read `TODO.md` (root) — get full picture of all areas and their status
5. For every entry in the root TODO where status contains "in progress" or "blocked",
   read that area's TODO file in full
6. Read today's session file if it exists (`output/sessions/YYYY-MM-DD.md`)
7. Read `log.md` — last 5 entries for recent context
8. Scan for `artifacts.md` files in active projects (those with in-progress items).
   For each artifact entry, check if `local_path` exists on disk.
   If missing, add a warning to the bridge output under **Missing artifacts**.

9. **Resurface** — Find the wiki/ page with the oldest `updated:` frontmatter date.
   Show: title, path, days since last update.
   Ask: "Still accurate? (y = bump updated date, n = flag for review, skip = move on)"
   One page per session — keeps the wiki alive without dedicated review sprints.

## Output format

```
## Session Bridge — [DATE]

**Changes pulled from remote:** [N files updated — only if pull brought changes; omit otherwise]
**Last session:** [date + topic from log.md]
**Active work:**
  [list each in-progress item across all areas, with area name]
**Blocked:**
  [list each blocked item across all areas, with reason]
  (or "Nothing blocked" if none)
**Missing artifacts:**
  [list any artifacts whose local_path doesn't exist, with clone command]
  (or omit this section if all artifacts are present)
**Suggested next action:** [specific first step — one line, actionable]
**Files to open:** [specific files relevant to next action]
**Open questions:** [anything unresolved from last session]
```

Then ask: "Ready to continue? Or do you want to work on something else?"

## Notes

- If log.md has no session-end entry: say so and ask what the owner wants to work on
- Keep the bridge output concise — the goal is orientation in under 60 seconds
- Do not read every file in the project — targeted reads only
- Only read TODO files that have in-progress or blocked items (skip pure backlog areas)
