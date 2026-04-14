# /bridge — Session Start Ritual

Run at the start of every Claude Code session.

## Steps

0. **Staleness check** — Before reading any session file, find the most recent
   file in `output/sessions/`. If the most recent session file is NOT from today
   or yesterday, show:
   "No session file since [DATE]. Want to run /bridge-recovery? (y/n)"
   - If **y**: run /bridge-recovery, then continue from step 1 (skip step 0 on re-entry)
   - If **n**: continue with normal bridge (the old session file will be read in step 4
     but the user has been warned it may be stale)

1. Read `CLAUDE.md` — get schema and strategic orientation
2. Read `TODO.md` (root) — get full picture of all areas and their status
3. For every entry in the root TODO where status contains "in progress" or "blocked",
   read that area's TODO file in full
4. Read today's session file if it exists (`output/sessions/YYYY-MM-DD.md`)
5. Read `log.md` — last 5 entries for recent context
6. Scan for `artifacts.md` files in active projects (those with in-progress items).
   For each artifact entry, check if `local_path` exists on disk.
   If missing, add a warning to the bridge output under **Missing artifacts**.

7. **Resurface** — Find the wiki/ page with the oldest `updated:` frontmatter date.
   Show: title, path, days since last update.
   Ask: "Still accurate? (y = bump updated date, n = flag for review, skip = move on)"
   One page per session — keeps the wiki alive without dedicated review sprints.
   Threshold is configurable: default 60 days. Adjust based on wiki size and session frequency.

## Output format

```
## Session Bridge — [DATE]

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
