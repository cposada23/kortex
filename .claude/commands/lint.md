# /lint — Wiki Health Check

Run monthly. Output goes to output/lint-YYYY-MM-DD.md.

## Checklist

1. **Orphan pages** — wiki pages with no inbound wikilinks from other pages
2. **Distillation debt** — pages at distillation_level 0 or 1 (list top 10 by age)
3. **Stale content** — wiki/ pages with `updated:` older than 60 days (list all, sorted oldest first)
4. **Missing pages** — concepts mentioned in text but no dedicated page exists
5. **Broken wikilinks** — [[references]] with no corresponding file
6. **CLAUDE.md size** — flag any CLAUDE.md file over 150 lines
7. **Index gaps** — .md files in the project not listed in index.md
8. **Contradictions** — claims in one page that conflict with another page

## Steps

1. Read index.md — get full file list
2. Run all 8 checks above
3. Write report to output/lint-YYYY-MM-DD.md
4. Add report to index.md under Output section
5. Append to log.md: `## [DATE] lint | Health check complete`

## Report format

```markdown
# Lint Report — YYYY-MM-DD

## Summary
| Check | Count | Status |
|---|---|---|
| Orphan pages | N | ok / warning / critical |
| Distillation debt | N | ... |
| Stale content (60+ days) | N | ... |
...

## Findings by category
[actionable list per category]

## Top 3 recommended actions
1.
2.
3.
```

## After running

Present summary to owner. Ask which findings to address first.
Do not auto-fix anything — lint is diagnostic, not corrective.
