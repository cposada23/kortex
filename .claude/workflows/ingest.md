# Ingest Rules

Run when new material arrives — files, PDFs, text entries, links, or any raw input.

## Distributed Inbox System

The project has multiple inboxes. Each one gives automatic context:

| Inbox | What goes here | Auto-tagged as |
|---|---|---|
| `inbox/INBOX.md` | Text entries — URLs, ideas, quick notes | General |
| `inbox/drop/` | Files — PDFs, images, articles, transcripts | General |
| `sources/courses/[course]/inbox/` | Course-specific files | `course: [course-name]` |
| `projects/[project]/inbox/` | Project-specific files | `project: [project-name]` |

## Workflow

### For files (PDFs, articles, transcripts, etc.)

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
4. Write or update the relevant wiki page in /wiki
   - One concept per page (atomic — not "everything about X")
   - Full frontmatter including distillation_level: 1
   - Add `course:` or `project:` field in frontmatter when applicable
   - Summary field: one sentence stating what and why it matters
   - Related links to connected existing pages
5. Move the source file to the `processed/` subfolder in the same inbox
6. Update index.md with any new pages created (Auto-index Rule — no exceptions)
7. Append an entry to log.md: `## [DATE] ingest | [Page Title] (from [inbox location])`
8. Update related existing pages if the new content connects to them

### For text entries (in INBOX.md)

1. Read each unprocessed item in `inbox/INBOX.md`
2. Apply relevance filter — mark SKIPPED if not relevant
3. Create atomic wiki page if relevant (distillation_level: 1)
4. Update index.md and log.md
5. Mark item PROCESSED in INBOX.md
6. Report results

## Auto-index Rule

Every new .md file created anywhere in the project must be added to index.md
immediately. Applies to all operations. Never create a file without indexing it.
Exception: CLAUDE.md files and README.md files.

## Inbox scanning order

When `/ingest` is run without arguments, scan all inboxes in this order:

1. `inbox/INBOX.md` — text entries
2. `inbox/drop/` — general file drops
3. `sources/courses/*/inbox/` — course inboxes (one per course)
4. `projects/*/inbox/` — project inboxes (one per project)

Skip empty inboxes silently. Only report inboxes that had items.

## Processed folder maintenance

- `processed/` folders are staging areas, not permanent archives
- Git history is the real safety net — `processed/` is for visibility
- Clean out `processed/` folders periodically (monthly, during /lint, or whenever)
- To re-ingest a file: move it back from `processed/` to the inbox folder
