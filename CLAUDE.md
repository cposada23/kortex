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

Layer 3 — The Schema: this file + .claude/rules/ + .claude/commands/

## File Structure
- /sources/courses → raw course material (immutable, Layer 1)
- /wiki → shared synthesized knowledge brain (Layer 2)
- /projects → active project execution folders
- /inbox → quick capture zone, zero friction
- /output → ephemeral files only: lint reports, session notes, plans, drafts (never lasting knowledge — that goes to /wiki)
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

## Commands
On-demand — loaded when invoked, not on every conversation.
- .claude/commands/ingest.md — distributed inbox processing
- .claude/commands/query.md — query + compounding loop
- .claude/commands/lint.md — monthly health check
- .claude/commands/bridge.md — session start ritual
- .claude/commands/bridge-out.md — session end / Hemingway bridge
- .claude/commands/bridge-recovery.md — reconstruct state after missed bridge-out
- .claude/commands/safe-change.md — branched change workflow

## Asset Sidecars
Binary files (images, videos, PDFs) get a `[filename].meta.md` sidecar describing the asset. Convention, not enforced.

## Log Rotation
log.md is append-only. When /lint runs, entries older than 90 days move to output/archive/log-YYYY-Q[N].md.

## Git Policy
Commit before any bulk operation. Delete freely — git preserves history.

## Active Priorities
1. [Your first priority]
2. [Your second priority]

Task details: see [TODO.md](TODO.md) → per-project TODO files.
