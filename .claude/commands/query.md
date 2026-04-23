---
scope: framework
---

# /query — Knowledge Base Query (compounding loop)

Run when answering a question about any topic in the knowledge base.

## Workflow

1. Read only the relevant section of index.md using `<!-- SECTION: X -->` markers (Capture, Output, Schema, Sources, Wiki, Projects, Archive) — never read the whole file
2. Read those specific pages (not everything — targeted reads only)
3. Synthesize an answer with references to the source pages
4. **Required:** Update existing wiki page or create new one with the synthesis
   (the wiki gets smarter with every query — this is the compounding mechanism)
5. Update index.md and log.md after creating/updating wiki pages

## Where knowledge goes

- **Lasting knowledge → wiki/** — investigations, research findings, strategies, concepts, reference material. One comprehensive page per topic. This is the default.
- **Ephemeral/temporal → output/** — lint reports, session notes, plans with deadlines, content drafts in progress. These are snapshots, not permanent knowledge.

**Rule:** If the answer will still be useful in 3 months, it belongs in wiki/, not output/. Never create both an output/ file AND a wiki/ page for the same topic — that's duplication.

## Precision rule

For a focused question, Claude should read index.md section + 1–3 relevant pages.
If reading 10+ files for a simple question: index.md summaries need improvement.

## Filing rule

Good answers that disappear into chat are waste.
- Answer reveals lasting knowledge → create/update a wiki page in /wiki
- Answer is a temporal snapshot (lint, draft, plan) → file to /output
- Answer updates an existing page → update that page in place
- Never duplicate: one topic, one page, one location
