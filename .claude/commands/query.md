---
scope: framework
---

# /query — Knowledge Base Query (compounding loop)

Run when answering a question about any topic in the knowledge base.

## Hierarchical navigation (top-down)

The knowledge graph has a 3-level index hierarchy. **The INDEX files
are the source of truth for what exists.** Always navigate top-down —
read the smallest file that contains enough signal to decide what to
open next.

1. **Nivel 1 — [index.md](../../index.md)** (root, ~75 lines).
   Identify which zones are relevant. Usually 1–2 of: `wiki/`,
   `projects/`, `sources/`, `inbox/`, `output/`.
2. **Nivel 2 — zone INDEX.md** (`<zone>/INDEX.md`). Read only the
   zone indexes relevant to the question. Each zone INDEX lists its
   contents with rich descriptions. Identify specific pages (for
   `wiki/`) or specific projects/courses (for `projects/`, `sources/`).
3. **Nivel 3 — project/course INDEX.md** (`projects/<name>/INDEX.md`,
   `sources/courses/<name>/INDEX.md`). Read when the question scopes
   into a specific project or course. Nivel 3 INDEX lists **every file
   at every depth** inside that project/course with a description +
   keywords per entry. No Nivel 4.
4. **Target file.** Open only the files identified by the Nivel 3 INDEX.
   Targeted reads only.

For questions scoped to a single zone, Nivel 1 can be skipped after
the first time in a session.

### INDEX is the source of truth

- **Do not `ls` the filesystem to find content.** If a file is not in the relevant INDEX.md, treat it as not existing for the purposes of answering. This discipline is what makes indexes trustworthy.
- If you notice a file on disk that's not in the INDEX, **flag it as drift** in the response (so `/lint` catches it) and do not silently read it.
- **Search INDEX by keyword.** The per-file keywords in Nivel 3 INDEX entries (e.g. `` `shortcut, prompt, v8` ``) are the semantic hit target. `grep -n "<keyword>" projects/<name>/INDEX.md` surfaces candidate files fast.

## Workflow

1. Navigate the index hierarchy (above) to identify target pages
2. Read those pages — targeted reads only
3. Synthesize an answer with references to the source pages
4. **Required:** Update existing wiki page or create new one with
   the synthesis (the wiki gets smarter with every query — this is
   the compounding mechanism)
5. Update the relevant INDEX.md files and log.md after creating or
   updating wiki pages. When a new wiki page is created:
   - Add an entry to [wiki/INDEX.md](../../wiki/INDEX.md) in the
     correct section (areas / concepts / tools / playbooks /
     decisions / references).
   - If the page lives under a sub-folder with its own index page
     (e.g. `wiki/areas/claude-mastery/` has a hub), add it there too.
   - Append entry to log.md.

## Where knowledge goes

- **Lasting knowledge → wiki/** — investigations, research findings,
  strategies, concepts, reference material. One comprehensive page
  per topic. This is the default.
- **Ephemeral/temporal → output/** — lint reports, session notes,
  plans with deadlines, content drafts in progress. These are
  snapshots, not permanent knowledge.

**Rule:** If the answer will still be useful in 3 months, it belongs
in wiki/, not output/. Never create both an output/ file AND a wiki/
page for the same topic — that's duplication.

## Precision rule

For a focused question, Claude should read:

- Nivel 1 (if session-first query) + 1–2 Nivel 2 zone indexes + 1–3
  target pages.
- Optionally 1 Nivel 3 project/course index if the question scopes
  into a specific one.

If reading 10+ files for a simple question, one of the indexes needs
tightening — flag it during `/lint`.

## Filing rule

Good answers that disappear into chat are waste.

- Answer reveals lasting knowledge → create/update a wiki page in
  `/wiki` and register it in [wiki/INDEX.md](../../wiki/INDEX.md)
- Answer is a temporal snapshot (lint, draft, plan) → file to
  `/output` and register it in [output/INDEX.md](../../output/INDEX.md)
- Answer updates an existing page → update that page in place; update
  the `updated:` frontmatter
- Never duplicate: one topic, one page, one location
