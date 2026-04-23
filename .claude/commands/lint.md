---
scope: framework
---

# /lint — Wiki Health Check

Run monthly. Output goes to output/lint-YYYY-MM-DD.md.

## Checklist

1. **Orphan pages** — wiki pages with no inbound links from other pages
2. **Distillation debt** — pages at distillation_level 0 or 1 (list top 10 by age)
3. **Stale content** — wiki/ pages with `updated:` older than 60 days (list all, sorted oldest first)
4. **Missing pages** — concepts mentioned in text but no dedicated page exists
5. **Broken markdown links** — `[text](path)` with no corresponding file (pre-commit hook already blocks new ones — this catches legacy)
6. **CLAUDE.md size** — flag any CLAUDE.md file over 150 lines
7. **Index drift** — every non-excluded `.md` file on disk must appear in its most specific INDEX.md; every INDEX.md entry must point to a file that exists. See algorithm below. Closes layer 3 of the hierarchical index auto-update model.
8. **Sidecar debt** — persistent binary files with no `.meta.md` sidecar AND not covered by a folder-README aggregation. See algorithm below.
9. **Contradictions** — claims in one page that conflict with another page
10. **Orphan decisions** — pages in wiki/decisions/ not linked from any project or wiki page
11. **Deprecated fields** — pages still using `related:` instead of `related_paths:` (list all, for opportunistic migration)

## Index drift check — algorithm

Forward check (files missing from INDEX):

1. Find all `.md` files in the repo, **excluding** per root CLAUDE.md → Auto-index Rule exclusion list: `INDEX.md` itself, root `CLAUDE.md`/`index.md`/`log.md`, everything under `.claude/`, `.git/`, `node_modules/`, `processed/` folder contents, `kortex-template/`.
2. For each remaining file, determine its most specific INDEX.md:
   - `wiki/<...>/<file>.md` → [wiki/INDEX.md](../../wiki/INDEX.md)
   - `projects/<name>/<...>/<file>.md` → `projects/<name>/INDEX.md`
   - `sources/courses/<name>/<...>/<file>.md` → `sources/courses/<name>/INDEX.md`
   - `inbox/<file>.md` → `inbox/INDEX.md`
   - `output/<file>.md` → `output/INDEX.md`
3. Check whether the file's relative path appears in that INDEX.md.
4. If not present → flag as drift.

Reverse check (INDEX entries pointing at ghost files):

5. For each INDEX.md, parse markdown links and check each target resolves to an existing file.
6. If not → flag as stale entry.

## Sidecar debt check — algorithm

1. Find all binary files (extensions: png, jpg, jpeg, gif, svg, webp, mp4, mov, pdf, mp3, wav, ttf, woff, woff2) excluding `.claude/` and `kortex-template/`.
2. For each binary, check coverage:
   - Does a `<filename>.meta.md` sidecar exist in the same folder? ✓ covered
   - Does the parent folder contain a `README.md` that could aggregate this binary? ✓ covered (heuristic: folder has `README.md` AND contains ≥3 binaries of similar extension)
   - Is the binary listed by filename directly in its Nivel 3 INDEX? ✓ covered
3. If none of the above → flag as sidecar debt.

## Steps

1. Read root `index.md` + all zone and project/course `INDEX.md` files — get the authoritative file registry
2. Run all 10 checks above
3. **Log rotation** — if log.md has entries older than 90 days, move them to
   `output/archive/log-YYYY-Q[N].md` (create folder if needed). Keep only last 90 days in active log.
4. Write report to output/lint-YYYY-MM-DD.md
5. Add report to [output/INDEX.md](../../output/INDEX.md) under the lint section
6. Append to log.md: `## [DATE] lint | Health check complete`

## Report format

```markdown
# Lint Report — YYYY-MM-DD

## Summary
| Check | Count | Status |
|---|---|---|
| Orphan pages | N | ok / warning / critical |
| Distillation debt | N | ... |
| Stale content (60+ days) | N | ... |
| Broken markdown links | N | ... |
| Index drift (files missing from INDEX) | N | ... |
| Index drift (stale entries in INDEX) | N | ... |
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
