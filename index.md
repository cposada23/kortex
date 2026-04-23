---
title: "Kortex — Master Index"
tags:
  - capa/2-wiki
  - tipo/index
layer: wiki
type: index
language: en
updated: YYYY-MM-DD
---

# Kortex — Master Index

Nivel 1 of the hierarchical index system. Entry point to your
knowledge graph. Each zone has its own `INDEX.md` (Nivel 2) with rich
detail of what lives there — navigate to the relevant zone index
before opening individual files.

---

<!-- SECTION: Zones -->
## Zonas (Nivel 2)

- **[projects/INDEX.md](projects/INDEX.md)** — Your active execution
  projects (Layer 3). One sub-folder per project, each with its own
  `CLAUDE.md`, `TODO.md`, and structure. Replace with a 1–2 line
  description per project once you have them.

- **[wiki/INDEX.md](wiki/INDEX.md)** — Synthesized knowledge (Layer 2).
  Atomic pages organized into areas (ongoing domains), concepts
  (discrete knowledge), tools (catalog), playbooks (reusable
  workflows), decisions (ADRs), references (operational guides).

- **[sources/INDEX.md](sources/INDEX.md)** — Immutable source material
  (Layer 1). Course notes, transcripts, original articles. Do not
  rewrite — synthesis lives in `/wiki`.

- **[inbox/INDEX.md](inbox/INDEX.md)** — Pending captures. Root inbox
  + per-project + per-course inboxes. `/ingest` routes items by
  `target_channel` in frontmatter, not by physical path.

- **[output/INDEX.md](output/INDEX.md)** — Ephemeral files: session
  notes, handoffs, audits, lint reports, drafts, schema history. No
  durable knowledge — that belongs in `/wiki`.

---

<!-- SECTION: Schema -->
## Schema

Kortex v1.0. Architecture and rules: [CLAUDE.md](CLAUDE.md). Always-loaded
rules: [.claude/rules/](.claude/rules/). On-demand commands:
[.claude/commands/](.claude/commands/).

## TODO

[TODO.md](TODO.md) — master TODO that points to per-project `TODO.md`.

## Log

[log.md](log.md) — chronological operation log (append-only).
