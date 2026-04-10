---
title: "Distillation Levels"
type: concept
layer: wiki
language: en
tags: [knowledge-management, system, capa/2-wiki]
updated: YYYY-MM-DD
distillation_level: 3
---

# Distillation Levels

**Summary:** A 5-level scale (0–4) that tracks how processed a piece of knowledge is — from raw capture to expression-ready content.

---

## What it is
Every wiki page in this system has a `distillation_level` field in its frontmatter. This tells you (and Claude) how mature the knowledge on that page is.

| Level | State | Description |
|---|---|---|
| 0 | Raw dump | Just captured, not processed |
| 1 | First pass | Read, key points identified |
| 2 | Distilled | Essential content in own words |
| 3 | Synthesized | Connected to other pages, implications drawn |
| 4 | Expression-ready | Can generate content directly from this page |

## Why it matters
- The `/lint` command uses distillation levels to find "debt" — pages stuck at level 0 or 1 that need work
- A page at level 0 is noise — it exists but adds no value yet
- A page at level 4 is an asset — you can generate a blog post, video script, or presentation directly from it
- The goal is to move pages up over time through regular review

## How it connects
- [Second Brain](second-brain.md) — distillation is the core activity that makes a second brain valuable
- [LLM Wiki Pattern](../references/llm-wiki-pattern.md) — the `/ingest` workflow creates pages at level 1 automatically

## Source
Inspired by Tiago Forte's "Progressive Summarization" technique, adapted for LLM-maintained wikis.
