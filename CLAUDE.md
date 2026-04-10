# CLAUDE.md — Knowledge Brain

## What This Is
A personal AI Knowledge Graph built on the LLM Wiki pattern.
A living brain that grows with every course, experiment, and
content creation session. Not a finished project — a system
that compounds over time.

## Owner
[Your name] — [your role or focus areas]

## Schema
Schema version 1.0. See output/schema-changelog.md for history.

## Five Zone Architecture

    /inbox      CAPTURE ZONE     Quick capture, zero friction
    /sources    SOURCE ZONE      Immutable course material (Layer 1)
    /wiki       SYNTHESIS ZONE   LLM-maintained atomic pages (Layer 2)
    /projects   PROJECT ZONE     Active execution per project
    /output     OUTPUT ZONE      Filed query results, drafts, reports

Layer 3 — The Schema: this file + .claude/rules/ + .claude/workflows/

## File Structure
- /sources/courses → raw course material (immutable, Layer 1)
- /wiki → shared synthesized knowledge brain (Layer 2)
- /projects → active project execution folders
- /inbox → quick capture zone, zero friction
- /output → query results, lint reports, content drafts (never in /projects)
- index.md → master catalog of entire wiki
- log.md → chronological operation log

## Auto-index Rule
Every new .md file must be added to index.md immediately.
No exceptions except CLAUDE.md and README.md files.

## Frontmatter Rule
Every new .md file must include YAML frontmatter per .claude/rules/frontmatter.md.
Required: title, type, layer, language, tags, updated.
Skip on CLAUDE.md and README.md only.

## Link Rule
All internal links use relative markdown: `[text](path/to/file.md)`.
No wikilinks. Pre-commit hook blocks broken links.

## Workflows
On-demand — loaded by commands when needed, not on every conversation.
- .claude/workflows/ingest.md — distributed inbox processing
- .claude/workflows/query.md — query + compounding loop
- .claude/workflows/lint.md — monthly health check

## Git Policy
Commit before any bulk operation. Delete freely — git preserves history.

## Active Priorities
1. [Your first priority]
2. [Your second priority]
