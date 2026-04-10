# Query Workflow

Run when answering a question about any topic in the knowledge base.

## Workflow (compounding loop)

1. Read only the relevant section of index.md using `<!-- SECTION: X -->` markers (Capture, Output, Schema, Sources, Wiki, Projects, Archive) — never read the whole file
2. Read those specific pages (not everything — targeted reads only)
3. Synthesize an answer with references to the source pages
4. **Required:** Update existing wiki page or create new one with the synthesis
   (the wiki gets smarter with every query — this is the compounding mechanism)
5. File a copy to /output as the receipt
6. Update index.md and log.md after filing

## Precision rule

For a focused question, Claude should read index.md section + 1–3 relevant pages.
If reading 10+ files for a simple question: index.md summaries need improvement.

## Filing rule

Good answers that disappear into chat are waste.
- Synthesis answer valuable for future reference → file to /output/[descriptive-name].md
- Answer reveals a missing concept → create a new wiki page in /wiki
- Answer updates an existing page → update that page in place

## Output zone

Query results, synthesis, and content drafts → /output
Never file query results in /projects (that folder is for project execution assets).
