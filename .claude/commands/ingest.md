---
scope: framework
---

# /ingest — Process All Inboxes

Scan and process all inbox locations across the project.

## Distributed Inbox System

The project has multiple inboxes. Each one gives automatic context:

| Inbox | What goes here | Auto-tagged as |
|---|---|---|
| `inbox/INBOX.md` | Text entries — URLs, ideas, quick notes | General |
| `inbox/drop/` | Files — PDFs, images, articles, transcripts | General |
| `sources/courses/[course]/inbox/INBOX.md` | Course text entries | `course: [course-name]` |
| `sources/courses/[course]/inbox/` | Course files | `course: [course-name]` |
| `projects/[project]/inbox/INBOX.md` | Project text entries | `project: [project-name]` |
| `projects/[project]/inbox/` | Project files | `project: [project-name]` |

## Inbox scanning order

When run without arguments, scan all inboxes in this order:

1. `inbox/INBOX.md` — global text entries
2. `inbox/drop/` — general file drops
3. `sources/courses/*/inbox/INBOX.md` — course text entries
4. `sources/courses/*/inbox/` — course file drops
5. `projects/*/inbox/INBOX.md` — project text entries
6. `projects/*/inbox/` — project file drops

Skip empty inboxes silently. Only report inboxes that had items.

## Idea items — schema-driven routing

Markdown files with `type: idea` in their frontmatter follow a specific
schema defined in [../rules/idea-frontmatter.md](../rules/idea-frontmatter.md).
These files route differently from generic inbox items:

1. Read the frontmatter. Confirm `type: idea` and the required fields
   are present (`title`, `status`, `angle`, `target_channel`).
2. **Route by `target_channel`, not by the inbox path.** An idea in
   `/inbox/` with `target_channel: milo-ia` belongs to the Milo IA
   project regardless of which inbox it was dropped in.
3. Do NOT re-interpret the idea. The frontmatter is the source of
   truth — the ingest's job is to move the file and append a BANK/log
   entry, not to re-generate angle/why_it_works/status.
4. Destination is project-specific. For `target_channel: milo-ia`,
   follow the Milo IA ideation-bank flow (see that project's
   CLAUDE.md). For other projects, deposit into that project's
   appropriate folder based on `status`.
5. If `target_channel: cross-project` or the field is missing, leave
   the file in `/inbox/` and flag it `needs-routing` in the ingest
   report for manual triage.

## Workflow — Files (PDFs, articles, transcripts, etc.)

1. Read the file completely before doing anything
2. If the file is a `.md` with `type: idea`, use the schema-driven
   routing above — skip the rest of this workflow.
3. Determine context from the inbox location:
   - `inbox/drop/` → general, apply relevance filter
   - `sources/courses/[course]/inbox/` → tagged to that course automatically
   - `projects/[project]/inbox/` → tagged to that project automatically
4. Apply the relevance filter (general inbox only):
   - Does this connect to an active project or area?
   - If no: move to `processed/` and note SKIPPED in the ingest report
   - If yes: continue
   - Course and project inboxes skip this filter — they are relevant by definition
5. Determine destination based on inbox location:
   - `inbox/drop/` or `sources/courses/*/inbox/` → create page in `/wiki` (shared knowledge)
   - `projects/[project]/inbox/` → create page in that project's folder
     (use `references/`, `content/`, or `prompts/` based on content type)
   - Project-specific content stays in the project — it is not general knowledge
6. Write or update the page at the determined destination
   - One concept per page (atomic — not "everything about X")
   - Full frontmatter including distillation_level: 1
   - Add `course:` or `project:` field in frontmatter when applicable
   - Summary field: one sentence stating what and why it matters
   - Related links to connected existing pages
7. Move the source file to the `processed/` subfolder in the same inbox
8. **Update the INDEX hierarchy** so the new page is discoverable
   (see "Index update rule" below)
9. Append an entry to log.md: `## [DATE] ingest | [Page Title] (from [inbox location])`
10. Update related existing pages if the new content connects to them

## Workflow — Text entries (in INBOX.md files)

1. Read each unprocessed item in every INBOX.md
2. Apply relevance filter (general inbox only — course/project skip it)
3. Apply destination rule (same as files): general/course → /wiki, project → project folder
4. Create atomic page if relevant (distillation_level: 1)
5. **Update the INDEX hierarchy** (see rule below)
6. Update log.md
7. Mark item PROCESSED in the corresponding INBOX.md
8. Report results

## Index update rule

Every new `.md` file and every new persistent binary created during
ingest must be registered in the most specific INDEX.md for its
location — **before** the ingest report is generated. This closes the
first of three layers in the hierarchical index auto-update model.
See root [CLAUDE.md](../../CLAUDE.md) → Auto-index Rule for the
authoritative spec (routing table, entry format, exclusions, binary
rules). The rules below are the ingest-specific application.

### Entry format

```
- **[filename](full/relative/path)** — short description. `kw1, kw2, kw3`
```

- **Top-level files** of a project/course (directly under the Nivel 3 folder) get a one-line description + keywords.
- **Files at depth 4+** (inside subfolders) can drop the description when the filename is self-explanatory — keywords alone are enough.
- **Keywords:** 2–5 terms, lowercase, comma-separated, **only terms NOT already in the filename**. Keywords are how `/query` finds the file via grep.

Pull the description from the page's frontmatter `summary:` or `title:`
field, or the first prose line of its body. Pull keyword candidates
from frontmatter `tags:` (strip layer tags like `capa/X-*`).

### Routing

| New file path | Update this INDEX |
|---|---|
| `wiki/<sub>/<page>.md` | [wiki/INDEX.md](../../wiki/INDEX.md) (correct section) |
| `projects/<name>/<...>/<page>.md` | `projects/<name>/INDEX.md` (project Nivel 3) |
| `sources/courses/<name>/<...>/<page>.md` | `sources/courses/<name>/INDEX.md` (course Nivel 3) |
| `output/<page>.md` | [output/INDEX.md](../../output/INDEX.md) |

Zone-level indexes (`projects/INDEX.md`, `sources/INDEX.md`) are
**only** touched when structure changes at the zone level — a new
project folder, a new course folder, or a new zone. Otherwise go
straight to the Nivel 3 INDEX.

### Binary handling during ingest

If the file being ingested is a binary (image, video, pdf, audio):

1. **Prefer a sidecar** — generate a `<filename>.meta.md` sidecar in the same folder describing the asset (see "Asset sidecar pattern" below). Index the sidecar in the Nivel 3 INDEX.
2. **Folder-README aggregation** — if the destination folder already has a `README.md` describing the convention and the new binary fits that convention (e.g. a new size of an existing logo), **do not add a separate entry**. The folder-README already covers it.
3. **Loose persistent binary** (no sidecar, no folder-README) — index the binary directly with its filename + one type keyword (`imagen | video | pdf | audio`).

### Placement + hygiene

- **Place in the right section** of the parent INDEX.md. Section structure is defined by the INDEX itself (areas / concepts / tools / playbooks / decisions / references for wiki; top-level files / subfolders for project & course indexes). Do not invent new sections — flag if none fits.
- **Don't touch unrelated entries.** The goal is append-only during ingest. Restructuring happens during `/lint`.
- **Skip the zone index** if the new page is inside an existing subfolder already represented in the Nivel 3 INDEX. The Nivel 3 INDEX is the source of truth.

## Processed folder maintenance

- `processed/` folders are permanent — never delete their contents
- They serve as a browsable record of everything that was ingested
- To re-ingest a file: move it back from `processed/` to the inbox folder

## Report format

```
Ingest complete:

Global inbox:
- X text items: Y processed → Z pages, W skipped
- X files: Y processed → Z pages, W skipped

sources/courses/[name]/inbox:
- X files processed → Y pages

projects/[name]/inbox:
- X files processed → Y pages

INDEX updates:
- wiki/INDEX.md: X new entries
- projects/<name>/INDEX.md: X new entries
- ...

Total: X items processed, Y pages created, Z updated, W skipped
```

Ask if any skipped items should be reconsidered.

## Asset sidecar pattern

For binary assets (PNG, MP4, PDF, etc.) that are kept rather than ingested into wiki pages,
create a `[filename].meta.md` sidecar file in the same directory:

```yaml
---
title: "description of the asset"
asset_type: image | video | audio | document
created: YYYY-MM-DD
project: project-name
generated_by: "tool name + prompt (if AI-generated)"
tags: [relevant-tags]
---
```

This is a convention, not enforced by hooks. Create sidecars when assets are added
during ingest or when the user drops binary files into the project.

## Targeted ingest

If the user points to a specific file (e.g., "ingest sources/courses/ai-video-creators/lesson-5.pdf"),
process that single file using the same workflow. Context is inferred from the file path.
