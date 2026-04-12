# Frontmatter Schema

Every new .md file created in this project must include YAML frontmatter.
Exception: CLAUDE.md files and README.md files — skip frontmatter on these.

## Required fields

```yaml
title: "Page Title"
type: concept | reference | playbook | area | project | tool | person | index | inbox | todo | todo-index
layer: wiki
language: en | es | en-es
tags: [relevant-tags, capa/2-wiki]
updated: YYYY-MM-DD
```

## Optional fields

```yaml
status: active | draft | archived
distillation_level: 0-4
related: [[Wikilink]], [[Another]]   # Obsidian wikilinks — no path, no .md extension
related_paths: relative/path.md      # for README files and non-wiki links
course: course-name
step: step-name
project: project-name
```

## Confidence scoring fields (optional — wiki pages)

Track how trustworthy a wiki page's claims are. Orthogonal to distillation_level:
distillation tracks **maturity** (how processed); confidence tracks **trust** (how reliable).

```yaml
confidence: high | medium | low      # how well-supported are the claims?
source_count: 3                       # how many independent sources back it?
last_verified: 2026-04-10             # when was this last confirmed accurate?
supersedes: old-page-name.md          # if this page replaces/updates an older one
superseded_by: newer-page-name.md     # if a newer page has replaced this one
```

## distillation_level values

Required on all wiki pages in /wiki. Used by /lint to track distillation debt.

| Level | State | Description |
|---|---|---|
| 0 | Raw dump | Just captured, not processed |
| 1 | First pass | Read, key points identified |
| 2 | Distilled | Essential content in own words |
| 3 | Synthesized | Connected to other pages, implications drawn |
| 4 | Expression-ready | Can generate content directly from this page |

## Layer tags (required in tags field)

- `capa/1-fuente` — raw source files (course folders)
- `capa/2-wiki` — synthesized wiki pages (/wiki)
- `capa/3-proyecto` — applied project files (/projects)

## Wikilinks rule

- `related` uses `[[FILENAME]]` format — filename only, no path, no .md extension
- README files must NOT appear in `related`; use `related_paths` only
