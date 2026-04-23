---
scope: framework
---

# /bridge-recovery — Reconstruct Session State

Use when /bridge detects a stale session file (no session from today or yesterday),
or when the user knows a previous session ended without /bridge-out.

This command reconstructs **approximate** state from git history. It is not a
replacement for /bridge-out — it produces a best-effort reconstruction.

## Steps

1. Find the most recent session file in `output/sessions/`.
   Record its date as `LAST_SESSION_DATE`.

2. Run: `git log --stat --since="LAST_SESSION_DATE" --until="today" --format="%h %ad %s" --date=short`
   This shows all commits between the last known session and now.

3. Identify:
   - **Files changed** — group by zone (wiki/, projects/, sources/, inbox/, .claude/)
   - **Commit messages** — extract decisions and actions taken
   - **TODO changes** — diff TODO.md files to see what moved between states

4. Read the current state of:
   - `TODO.md` (root) — for current in-progress/blocked items
   - Any project TODO files that had commits in the gap period

5. Synthesize an approximate session state in the standard 4-field format:

```
## Recovery — [DATE RANGE]

⚠️ This is a reconstruction from git history, not a real /bridge-out.
Review before trusting.

**STATE:** [what the project looks like now, based on commits]
**DECISIONS:** [decisions implied by commit messages and file changes]
**NEXT:** [best guess at next action, based on TODO.md in-progress items]
**BLOCKERS:** [anything that looks stuck — items in TODO with no recent commits]
```

6. Write this to today's session file (`output/sessions/YYYY-MM-DD.md`).
   If the file already exists, append as a new section.

7. After writing, say:
   "Recovery written. Running /bridge now with fresh state."
   Then continue with the normal /bridge steps (skip step 0 sync and step 1 staleness check).

## Notes

- This command is invoked on demand only — zero overhead during normal sessions
- The reconstruction is approximate by design — git history shows what changed, not why
- Always include the ⚠️ warning so future /bridge reads know this was reconstructed
- If there are zero commits since the last session, say so and ask the user what happened
