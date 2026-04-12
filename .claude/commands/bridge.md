# /bridge — Session Start Ritual

Run at the start of every Claude Code session.

## Steps

1. Read `CLAUDE.md` — get schema and strategic orientation
2. Read `TODO.md` (root) — get full picture of all areas and their status
3. For every entry in the root TODO where status contains "in progress" or "blocked",
   read that area's TODO file in full
4. Read today's session file if it exists (`output/sessions/YYYY-MM-DD.md`)
5. Read `log.md` — last 5 entries for recent context
6. Scan for `artifacts.md` files in active projects (those with in-progress items).
   For each artifact entry, check if `local_path` exists on disk.
   If missing, add a warning to the bridge output under **Missing artifacts**.

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
