---
title: "LLM Wiki Pattern"
type: reference
layer: wiki
language: en
tags: [knowledge-management, architecture, capa/2-wiki]
updated: YYYY-MM-DD
distillation_level: 3
---

# LLM Wiki Pattern

**Summary:** A knowledge management architecture where an LLM maintains a persistent, compiled wiki instead of relying on RAG retrieval — the AI reads, writes, and connects pages on your behalf.

---

## What it is
The LLM Wiki pattern treats your knowledge base as a living wiki that the LLM actively maintains. Instead of dumping documents into a vector database and hoping retrieval finds the right chunks, you build a structured wiki where:

- **Layer 1 (Sources)** — immutable raw material (courses, articles, PDFs)
- **Layer 2 (Wiki)** — synthesized atomic pages maintained by the LLM
- **Layer 3 (Schema)** — rules that govern how the system behaves (CLAUDE.md, rules, workflows)

## Core operations

| Operation | What it does |
|---|---|
| **Ingest** | New material → read → create/update wiki pages → index |
| **Query** | Question → find relevant pages → synthesize answer → update wiki |
| **Lint** | Monthly health check → find orphans, debt, gaps → report |

## Why it matters
- Personal knowledge bases work better as compiled wikis than RAG systems
- The wiki compounds: every ingest and every query makes it smarter
- The LLM has context about your entire knowledge structure, not just retrieved chunks
- The system is portable: markdown files + git, no vendor lock-in

## How it connects
- [Second Brain](../concepts/second-brain.md) — this is a second brain implementation
- [Distillation Levels](../concepts/distillation-levels.md) — the maturity tracking system

## Source
LLM Wiki pattern — community pattern for AI-maintained knowledge bases.
