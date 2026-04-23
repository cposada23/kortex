# CLAUDE.md — Kortex

## What This Is
**Kortex** — a personal AI Knowledge Graph built on the LLM Wiki pattern.
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
- /wiki → shared synthesized knowledge (Layer 2)
- /projects → active project execution folders
- /inbox → quick capture zone, zero friction
- /output → ephemeral files only: lint reports, session notes, plans, drafts (never lasting knowledge — that goes to /wiki)
- index.md → master catalog of entire wiki
- log.md → chronological operation log

## Auto-index Rule

**Every `.md` file must appear in exactly one INDEX.md — the most
specific one for its location.** Files at any depth (Nivel 4, 5, 6, n)
are listed in their parent project/course Nivel 3 INDEX using the full
relative path from that INDEX. There is no Nivel 4+ of indexes.

### Routing table

| New file path | Update this INDEX |
|---|---|
| `wiki/<...>.md` | [wiki/INDEX.md](wiki/INDEX.md) (correct section) |
| `projects/<name>/<...>.md` | `projects/<name>/INDEX.md` (project Nivel 3) |
| `sources/courses/<name>/<...>.md` | `sources/courses/<name>/INDEX.md` (course Nivel 3) |
| `inbox/<file>.md` | [inbox/INDEX.md](inbox/INDEX.md) if it changes the snapshot |
| `output/<file>.md` | [output/INDEX.md](output/INDEX.md) |

**Whole new project or course folder** → create its Nivel 3 `INDEX.md`
(using [.claude/templates/project-index.md](.claude/templates/project-index.md)
or [.claude/templates/course-index.md](.claude/templates/course-index.md))
AND update the zone index. Update root [index.md](index.md) only when
a whole new zone appears.

### Entry format

```
- **[filename](full/relative/path)** — short description. `kw1, kw2, kw3`
```

- **Top-level files** of a project/course get a short one-line description + keywords.
- **Deep files** (Nivel 4+) can drop the description if the filename is self-explanatory — keywords alone are enough.
- **Keywords:** 2–5 terms, lowercase, comma-separated, **only terms NOT present in the filename** (avoids noise). Keywords are how `/query` finds the file via grep.

### Exclusions (never listed in any INDEX.md)

- `INDEX.md` itself (recursion)
- Root-of-repo: `CLAUDE.md`, `index.md`, `log.md`
- Everything under `.claude/` (framework layer, separate concern)
- Everything under `.git/`, `node_modules/`, system files (`.DS_Store`, `.gitkeep`, etc.)
- `processed/` folder **contents** (post-ingest historical — browsable via filesystem; the folder itself is mentioned with a file count)
- Binary files **without** a `.meta.md` sidecar, unless covered by a folder-README (see below)

**NOT excluded — listed in Nivel 3 INDEX:** `README.md`, `CLAUDE.md`,
`TODO.md`, `INBOX.md` of each project/course (they are content that
describes that project/course).

### Binary assets — three rules

1. **Binary with `.meta.md` sidecar** → index the **sidecar** (describes the binary + its metadata).
2. **Folder-README aggregation** — if a folder contains many binaries following a convention (naming, sizes, outputs) and the folder has its own `README.md` describing the convention, index **only the README.md** and mention the folder shape with a one-line summary. No individual binary entries.
3. **Loose persistent binary** (no sidecar, no folder-README) → index directly with filename + one type keyword (`imagen | video | pdf | audio`). If it ever becomes bulk, add a README.md + switch to aggregation.

Transient / WIP binaries are not listed; `/lint` flags binaries not covered by any of the three rules as "sidecar debt".

## Frontmatter Rule
Every new .md file must include YAML frontmatter per .claude/rules/frontmatter.md.
Required: title, type, layer, language, tags, updated.
Skip on CLAUDE.md and README.md only.

## Idea Schema Rule
Ideas captured in any `/inbox/` folder use `type: idea` and follow the
narrower schema in .claude/rules/idea-frontmatter.md — same base fields
plus `status`, `angle`, and `target_channel`. `/ingest` routes idea
items by `target_channel`, not by inbox path, so a cross-project idea
reaches the right destination even when dropped in the wrong inbox.

## Link Rule
All internal links use relative markdown: `[text](path/to/file.md)`.
No wikilinks. Pre-commit hook blocks broken links.

## Verification Rule
Claims about fast-changing external facts (AI product features, platform
UIs, metrics, legal events) require live web search with a recent date.
External AI output is a signal, not verification. See .claude/rules/verification.md
for full rules and categories.

## Scope Rule
Every file under `.claude/` declares a scope so the framework layer
stays cleanly separated from project-specific artifacts. See
.claude/rules/scope.md for declaration formats per file type.

## Write Authority Rule
Structural writes to your Kortex instance pass through Claude Code only
(CLI, VS Code extension, or Desktop tab — all three count equally).
Claude.ai chat and Cowork may read and (once you have verified GitHub
write-sync) propose captures to your inbox; they do not write directly
to knowledge graph structure or schema. See .claude/rules/write-authority.md
for the full rule and rationale.

## Commands
On-demand — loaded when invoked, not on every conversation.
- .claude/commands/ingest.md — distributed inbox processing
- .claude/commands/query.md — query + compounding loop
- .claude/commands/lint.md — monthly health check
- .claude/commands/bridge.md — session start ritual
- .claude/commands/bridge-out.md — session end / Hemingway bridge
- .claude/commands/bridge-recovery.md — reconstruct state after missed bridge-out
- .claude/commands/handoff.md — mid-session context compaction (lighter than bridge-out)
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
