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

## Workflow — Files (PDFs, articles, transcripts, etc.)

1. Read the file completely before doing anything
2. Determine context from the inbox location:
   - `inbox/drop/` → general, apply relevance filter
   - `sources/courses/[course]/inbox/` → tagged to that course automatically
   - `projects/[project]/inbox/` → tagged to that project automatically
3. Apply the relevance filter (general inbox only):
   - Does this connect to an active project or area?
   - If no: move to `processed/` and note SKIPPED in the ingest report
   - If yes: continue
   - Course and project inboxes skip this filter — they are relevant by definition
4. Determine destination based on inbox location:
   - `inbox/drop/` or `sources/courses/*/inbox/` → create page in `/wiki` (shared knowledge)
   - `projects/[project]/inbox/` → create page in that project's folder
     (use `references/`, `content/`, or `prompts/` based on content type)
   - Project-specific content stays in the project — it is not general knowledge
5. Write or update the page at the determined destination
   - One concept per page (atomic — not "everything about X")
   - Full frontmatter including distillation_level: 1
   - Add `course:` or `project:` field in frontmatter when applicable
   - Summary field: one sentence stating what and why it matters
   - Related links to connected existing pages
6. Move the source file to the `processed/` subfolder in the same inbox
7. Update index.md with any new pages created
8. Append an entry to log.md: `## [DATE] ingest | [Page Title] (from [inbox location])`
9. Update related existing pages if the new content connects to them

## Workflow — Text entries (in INBOX.md files)

1. Read each unprocessed item in every INBOX.md
2. Apply relevance filter (general inbox only — course/project skip it)
3. Apply destination rule (same as files): general/course → /wiki, project → project folder
4. Create atomic page if relevant (distillation_level: 1)
5. Update index.md and log.md
6. Mark item PROCESSED in the corresponding INBOX.md
7. Report results

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
