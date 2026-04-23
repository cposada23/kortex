# Template: projects/<name>/INDEX.md

Copy the block below into `projects/<name>/INDEX.md` and fill in the
placeholders (`{{...}}`). This file is the Nivel 3 index — **every
`.md` file and every persistent binary in the project must appear
here**, at any depth, in the most appropriate section.

**Entry format:**
- Top-level project files → short description + keywords.
- Files at depth 4+ (inside subfolders) → filename + keywords is enough; drop the description when the filename is self-explanatory.
- Keywords: 2–5 lowercase terms, comma-separated, **only terms NOT already in the filename**.

See the root `CLAUDE.md` → Auto-index Rule for the full exclusion list.

```markdown
---
title: "{{Project Name}} — Project Index"
tags:
  - capa/3-proyecto
  - tipo/index
layer: project
type: index
language: en-es
updated: YYYY-MM-DD
---

# {{Project Name}} — Project Index

{{One paragraph: what this project is, who it's for, what it produces.
Go one layer deeper than the zone-level description (pipeline,
audience, format, key decisions).}}

**Status:** {{active-shipping | planning | backlog | paused | meta-loop}} ·
**Language:** {{es | en | en-es}} ·
**Started:** {{YYYY-MM-DD}}

**Entry points (read in this order):**
1. [CLAUDE.md](CLAUDE.md) — project rules
2. [references/project-brief.md](references/project-brief.md) *(if exists)* — goal, audience, priorities, decisions
3. {{a third file specific to the project}}

---

## Top-level files

- **[CLAUDE.md](CLAUDE.md)** — project rules. `rules, policies`
- **[README.md](README.md)** — overview. `overview`
- **[TODO.md](TODO.md)** — active tasks + backlog. `tasks, backlog`
- {{List every remaining .md at project root with description + keywords.}}

## {{subfolder-name/}}

{{One-paragraph description of what lives here + current state.}}

- **[file-1.md](subfolder-name/file-1.md)** — what it is. `kw1, kw2`
- **[file-2.md](subfolder-name/file-2.md)** — `kw1, kw2`

### {{subfolder-name/nested-subfolder/}} *(if depth 4+)*

- **[deep-file.md](subfolder-name/nested-subfolder/deep-file.md)** — `kw1, kw2`

{{Repeat per subfolder. Include every nested path. Assets: index
.meta.md sidecars when present; index persistent binaries directly
with filename + type keyword (imagen | video | pdf | audio) when
no sidecar exists; skip transient WIP binaries.}}

## Inbox

[inbox/](inbox/) — project-specific capture zone. Cross-project ideas go to root `/inbox/` with `target_channel: <name>`.

List inbox files only if they describe a stable snapshot. Otherwise
the folder reference is enough — `/ingest` moves them to their final
destination.

## Archive *(if applicable)*

- **[archive/old-file.md](archive/old-file.md)** — `kw1, kw2`

---

## How this file is maintained

Updated by `/ingest` when processing inbox items (new pages registered here). Manual edits when a top-level file is added/removed. `/lint` flags drift (unlisted .md files; binaries without sidecars).

Zone entry: [../INDEX.md](../INDEX.md). Root entry: [../../index.md](../../index.md).
```
