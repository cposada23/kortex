# Frontmatter Schema

Every new .md file created in this project must include YAML frontmatter.

Exceptions (frontmatter is NOT required on these — they are schema or
operational files, not indexable content):

- `CLAUDE.md` files
- `README.md` files
- `INBOX.md`, `log.md`, `index.md`
- Any file under `.claude/rules/`, `.claude/hooks/`, `.claude/commands/`,
  `.claude/skills/`, or `.claude/templates/` (operational schema)

The pre-commit hook at `.claude/hooks/validate-frontmatter.py` enforces
this list — keep the two in sync when updating either.

Files under `.claude/commands/` and `.claude/skills/` carry a minimal
frontmatter block with a single `scope:` field (`framework` or
`project:<name>`) — not the full content schema. See [scope.md](scope.md)
for the scope tagging convention.

Items in any `/inbox/` folder with `type: idea` follow the narrower
schema in [idea-frontmatter.md](idea-frontmatter.md) — same base
fields, plus `status`, `angle`, and `target_channel` for routing.

## Required fields

```yaml
title: "Page Title"
type: concept | reference | playbook | area | project | tool | person | index | inbox | idea | todo | todo-index
layer: wiki
language: en | es | en-es
tags: [relevant-tags, capa/2-wiki]
updated: YYYY-MM-DD
```

## Optional fields

```yaml
status: active | draft | archived
distillation_level: 0-4
related_paths:                        # cross-references as relative paths
  - ../concepts/strategy/FICHA_NICHO.md
  - ../../tools/HERRAMIENTAS_IA.md
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

- **Start with new pages only.** Backfill existing pages during distillation reviews.
- **supersedes / superseded_by** — when new info contradicts old info, link both directions.
  Prevents silent contradictions sitting in the wiki.
- A page can be distillation_level 3 but confidence: low if based on a single unverified source.

## distillation_level values

Required on all wiki pages in /wiki. Used by /lint to track distillation debt.

| Level | State | Description |
|---|---|---|
| 0 | Raw dump | Just captured, not processed |
| 1 | First pass | Read, key points identified |
| 2 | Distilled | Essential content in own words |
| 3 | Synthesized | Connected to other pages, implications drawn |
| 4 | Expression-ready | Can generate Milo IA content directly from this page |

## Layer tags (required in tags field)

- `capa/1-fuente` — raw source files (course folders)
- `capa/2-wiki` — synthesized wiki pages (/wiki)
- `capa/3-proyecto` — applied project files (/projects)

## Cross-references rule

- Use `related_paths:` with relative paths for all frontmatter cross-references
- Each entry is a relative path from the source file's directory
- The old `related:` field (Obsidian wikilinks) is deprecated — do not use on new pages
- Existing pages with `related:` will be migrated opportunistically when touched
