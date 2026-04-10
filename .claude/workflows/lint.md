# Lint Rules

Run monthly. Save results to output/lint-YYYY-MM-DD.md. Update index.md with the report.

## Checklist

1. **Orphan pages** — wiki pages with no inbound wikilinks from other pages
2. **Distillation debt** — pages at distillation_level 0 or 1 (list top 10 by age)
3. **Stale content** — pages not updated in 60+ days that may need review
4. **Missing pages** — concepts mentioned in text but no dedicated page exists
5. **Broken wikilinks** — [[references]] with no corresponding file
6. **CLAUDE.md size** — flag any CLAUDE.md file over 150 lines
7. **Index gaps** — .md files in the project not listed in index.md
8. **Contradictions** — claims in one page that conflict with another page

## Report format

```markdown
# Lint Report — YYYY-MM-DD

## Summary
| Check | Count | Status |
|---|---|---|
| Orphan pages | N | ok / warning / critical |
...

## Findings by category
[actionable list per category]

## Top 3 recommended actions
1.
2.
3.
```

After running: ask owner to review and decide on priority fixes.
