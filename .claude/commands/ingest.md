# /ingest — Process All Inboxes

Scan and process all inbox locations across the project.

## Steps

**Before starting:** Read `.claude/workflows/ingest.md` for full workflow rules.

1. Scan all inboxes in order:
   a. `inbox/INBOX.md` — unprocessed text entries
   b. `inbox/drop/` — files dropped for general ingest
   c. `sources/courses/*/inbox/` — course-specific files
   d. `projects/*/inbox/` — project-specific files
2. For each item found:
   - Read it completely
   - Determine context from inbox location (course/project auto-tagged)
   - Apply relevance filter (global inbox only — course/project inboxes skip it)
   - If relevant: create atomic wiki page in appropriate /wiki subfolder
     - Full frontmatter with distillation_level: 1
     - Add course: or project: field when applicable
     - One concept per page
     - Summary field: one sentence
     - Related links to connected pages
   - If not relevant: mark SKIPPED with reason
3. Move processed files to their `processed/` subfolder
4. Mark text items PROCESSED in INBOX.md
5. Update index.md with all new pages
6. Update related existing pages with links to new pages
7. Append to log.md: `## [DATE] ingest | [Page Titles] (from [location])`

## Report after completion

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

## Targeted ingest

If the user points to a specific file (e.g., "ingest sources/courses/my-course/lesson-5.pdf"),
process that single file using the same workflow. Context is inferred from the file path.
