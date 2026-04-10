# /lint — Wiki Health Check

Run monthly. Output goes to output/lint-YYYY-MM-DD.md.

## Steps

**Before starting:** Read `.claude/workflows/lint.md` for the full checklist.

1. Read index.md — get full file list
2. Run all 8 checks (orphans, distillation debt, stale, missing pages,
   broken wikilinks, CLAUDE.md size, index gaps, contradictions)
3. Write report to output/lint-[DATE].md
4. Add report to index.md under Output section
5. Append to log.md: `## [DATE] lint | Health check complete`

## After running

Present summary to owner. Ask which findings to address first.
Do not auto-fix anything — lint is diagnostic, not corrective.
