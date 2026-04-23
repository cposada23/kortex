---
title: "Sources — Zone Index"
tags:
  - capa/1-fuente
  - tipo/index
layer: wiki
type: index
language: en
updated: YYYY-MM-DD
---

# Sources — Zone Index

Layer 1 — immutable source material. Whatever lands here is never
rewritten: course notes, transcripts, original articles. Synthesis
lives in `/wiki` (Layer 2); learnings promoted to the wiki are
tracked in per-course `INSIGHTS.md` files.

## Courses — [courses/](courses/)

_(Each course gets a sub-folder. Populate as you consume courses.)_

Example structure:

- **[courses/my-first-course/](courses/my-first-course/)** — One-line
  description of the course (instructor, format, why it matters).
  Entry: `README.md`, `CLAUDE.md` (course-specific note-taking policy),
  `TODO.md` (study tracker), `INSIGHTS.md` (promotion candidates),
  `notes/`, `inbox/`.

## Nivel 3 — Per-course indexes

When a course has more than a handful of notes, create its own
`INDEX.md` at `sources/courses/<name>/INDEX.md` listing notes,
assignments, resources, and insights. Update the entry above to link
to the per-course index.

Use the template at
[.claude/templates/course-index.md](../.claude/templates/course-index.md)
— copy it, rename to `INDEX.md`, fill in the placeholders.

## Articles — [articles/](articles/)

_(Source articles folder. Populate as you capture them.)_
