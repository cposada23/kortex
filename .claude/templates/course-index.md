# Template: sources/courses/<name>/INDEX.md

Copy the block below into `sources/courses/<name>/INDEX.md` and fill
in the placeholders (`{{...}}`). This file is the Nivel 3 index —
**every `.md` note, assignment, and resource in the course must appear
here**, at any depth.

**Entry format:**
- Top-level course files → short description + keywords.
- Notes/assignments at depth 4+ → filename + keywords; drop description when filename is self-explanatory.
- Keywords: 2–5 lowercase, comma-separated, **only terms NOT already in the filename**.

See the root `CLAUDE.md` → Auto-index Rule for the full exclusion list.

```markdown
---
title: "{{Course Name}} — Course Index"
tags:
  - capa/1-fuente
  - tipo/index
layer: wiki
type: index
language: en-es
updated: YYYY-MM-DD
---

# {{Course Name}} — Course Index

{{One paragraph: what the course is, who teaches it, platform, format,
and what it feeds (which wiki areas or projects).}}

**Language:** {{es | en}} ·
**Platform:** {{YouTube | Skool | Hotmart | Udemy | ...}} ·
**Status:** {{in-progress | completed | paused | abandoned}} ·
**Feeds:** {{wiki/areas/<name>/, projects/<name>/, ...}}

**Entry points (read in this order):**
1. [CLAUDE.md](CLAUDE.md) — course rules
2. [README.md](README.md) *(if exists)* — overview, module/level map
3. {{first note file or TODO.md}}

---

## Top-level files

- **[CLAUDE.md](CLAUDE.md)** — course rules. `rules, tagging`
- **[TODO.md](TODO.md)** — study tracker. `progress`
- {{List every remaining .md at course root with description + keywords.}}

## notes/

{{How notes are organized + current depth of coverage.}}

- **[file-1.md](notes/file-1.md)** — what it is. `kw1, kw2`

### notes/{{step-or-module}}/ *(if depth 4+)*

- **[nested-note.md](notes/step-or-module/nested-note.md)** — `kw1, kw2`

## assignments/ *(if applicable)*

- **[file-1.md](assignments/file-1.md)** — `kw1, kw2`

### assignments/{{step-or-module}}/ *(if depth 4+)*

- **[assignment-file.md](assignments/step-or-module/assignment-file.md)** — `kw1, kw2`

## resources/ *(if applicable)*

- **[file-1.md](resources/file-1.md)** — what it is. `kw1, kw2`

## Insights — [INSIGHTS.md](INSIGHTS.md) *(if applicable)*

Promotion candidates log — claims verified in this course that rise to wiki/ or projects/.

## Inbox

[inbox/INBOX.md](inbox/INBOX.md) — course-specific captures.

---

## How this file is maintained

Updated by `/ingest` when processing course inbox items. Manual edits when completing a new level/module or adding assignments. `/lint` flags drift.

Zone entry: [../../INDEX.md](../../INDEX.md). Root entry: [../../../index.md](../../../index.md).
```
