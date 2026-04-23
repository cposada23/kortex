---
title: "Inbox — Zone Index"
tags:
  - capa/2-wiki
  - tipo/index
layer: wiki
type: index
language: en
updated: YYYY-MM-DD
---

# Inbox — Zone Index

Capture zone — zero-friction drop. Files here are pre-triage: the
`target_channel` in frontmatter decides the destination, not the
physical capture path (see
[.claude/rules/idea-frontmatter.md](../.claude/rules/idea-frontmatter.md)).

Processing: `/ingest` reads every inbox, routes by `target_channel`,
and moves each file to its final destination.

## Root inbox — [INBOX.md](INBOX.md)

Cross-project captures. Items without a clear `target_channel` at
capture time land here with `target_channel: cross-project` and the
`needs-routing` tag — `/ingest` flags them for manual triage.

- **[INBOX.md](INBOX.md)** — Quick text capture (URLs, ideas, notes).
- **[drop/](drop/)** — Binary file drop (PDFs, images, transcripts).
- **[processed/](processed/)** — Historical archive of items already
  processed by `/ingest`.

## Per-project inboxes

Each active project gets its own inbox for project-specific captures.
Update this list as you create projects.

- _(Example: `projects/my-first-project/inbox/` — captures for that
  project.)_

## Per-course inboxes

Each course gets its own inbox for course-specific captures (notes
while consuming the course, questions, learnings).

- _(Example: `sources/courses/my-first-course/inbox/` — captures for
  that course.)_

## Routing rules

- Idea with `target_channel: <project-name>` captured in any inbox →
  `/ingest` moves it to the destination defined by that project's
  convention.
- Idea without a clear `target_channel` → `target_channel: cross-project`
  + tag `needs-routing` → `/ingest` flags it for manual triage.
- Full schema:
  [.claude/rules/idea-frontmatter.md](../.claude/rules/idea-frontmatter.md).
