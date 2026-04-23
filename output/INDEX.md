---
title: "Output — Zone Index"
tags:
  - capa/2-wiki
  - tipo/index
layer: wiki
type: index
language: en
updated: YYYY-MM-DD
---

# Output — Zone Index

Ephemeral artifacts zone. Sessions, handoffs, audits, lint reports,
drafts, schema history. **Never durable knowledge** — that lives in
`/wiki`. Files here accumulate chronologically, serve as evidence
or checkpoints, and eventually rotate to `archive/`.

## Sessions — [sessions/](sessions/)

Daily notes from `/bridge-out` and `/handoff`. Append-only per day
(one file per date, multiple sessions can append). Format:
`YYYY-MM-DD.md`.

## Handoffs — [handoffs/](handoffs/)

Preventive / mid-session compaction checkpoints (`/handoff`). Format:
`YYYY-MM-DD-HHMM-<topic>.md`. Distinct from `sessions/` — handoffs
are checkpoints to resume with fresh context, sessions are append-only
per day.

## Audits — [audits/](audits/)

Results of applied cross-AI validations (Claude + ChatGPT + Gemini +
Perplexity, or whichever you use). Each audit documents validators
used, consensus findings, disagreements resolved, changes applied,
rejects preserved.

## Drafts — [drafts/](drafts/)

Work-in-progress documents not yet ready for their final location.

## Lint Reports — [lint-*.md](.)

Output of `/lint` (monthly health check).

## Framework audits & schema

- **[schema-changelog.md](schema-changelog.md)** — Schema version
  history (v1.0 → latest).

## Archive policy

Old files rotate to `output/archive/` via `/lint` — `log.md` entries
older than 90 days move to `archive/log-YYYY-Q[N].md`; sessions older
than 6 months group by quarter. Folder created on demand.
