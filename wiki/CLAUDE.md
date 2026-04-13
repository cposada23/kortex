# CLAUDE.md — /wiki

## Purpose

The synthesis zone. This is **Layer 2** of the architecture — LLM-maintained compiled knowledge.
Claude Code writes here; humans read here. Content is distilled from /sources and project work
into permanent, cross-referenced atomic wiki pages.

This folder does NOT contain raw course material. Everything here is synthesized.

## Rules for Working Here

- **Synthesize, never copy.** Distill insights, extract patterns, write original wiki pages.
- **One concept per page.** Atomic notes. Large pages should be split.
- **Update index.md** at the root after creating any new page.
- **Update log.md** at the root after any ingest or structural operation.
- **Claude Code owns this layer.** Create pages, update them, add cross-references.
- **Cross-reference freely.** Link both directions when pages relate.

## Subfolders

As your wiki grows, add subfolders and document their special rules here:

| Path | Contents | Special rules |
|---|---|---|
| `concepts/` | Concept pages and strategic frameworks | Keep templates generic — instantiate in `/projects/`. |
| `tools/` | Tool catalog + tutorials | Two-tier: catalog entries (short) vs tutorials (full guides). |
| `areas/` | Operational pages, learning paths | Operational logs are human-facing — plain language. |
| `playbooks/` | How-to guides, prompt tools | Interactive tools (HERRAMIENTA_*) are instructions for AI, not static docs. |
| `decisions/` | Architecture and strategy decisions | One page per significant decision: why, what it affects, alternatives. Created during /bridge-out. |
| `references/` | Glossary, foundational documents | Add freely. Read when needed for context. |

## Relationships

| Direction | Zone | Role |
|---|---|---|
| Fed by | `/sources/courses/` | Course lessons → tool pages, concept pages |
| Fed by | `/inbox/` | Captured ideas → atomic pages via /ingest |
| Consumed by | `/projects/` | Projects pull tools, templates, and guides from here |
| Governed by | `/CLAUDE.md` (root) | Root schema defines the full architecture |
