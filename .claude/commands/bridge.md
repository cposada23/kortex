# /bridge — Session Start Ritual

Run at the start of every Claude Code session.

## Steps

1. Read log.md — last 5 entries
2. Read CLAUDE.md root
3. Read Auto Memory (/memory)
4. Skim index.md for context

## Output format

```
## Session Bridge — [DATE]

**Last session:** [date + topic from log.md]
**Stopped at:** [exact file and task]
**Next action:** [specific first step — one line, actionable]
**Active projects:** [from CLAUDE.md Active Priorities]
**Files to open:** [specific files relevant to next action]
**Open questions:** [anything unresolved from last session]
```

Then ask: "Ready to continue? Or do you want to work on something else?"

## Notes

- If log.md has no session-end entry: say so and ask what the owner wants to work on
- Keep the bridge output concise — the goal is orientation in under 60 seconds
- Do not read every file in the project — targeted reads only
