---
title: "Decision: Merge workflows into commands"
type: concept
layer: wiki
language: en
tags: [decision, framework, capa/2-wiki]
updated: 2026-04-13
distillation_level: 2
confidence: high
source_count: 1
---

# Decision: Merge workflows into commands

**Date:** 2026-04-13

**Why:** Commands referenced workflows, and both got loaded — doubling token cost per invocation. /ingest alone was 167 lines across 2 files. No command shared a workflow, so the split created duplication without reuse.

**What it affects:** `.claude/commands/` (absorbs workflow content), `.claude/workflows/` (deleted entirely).

**Alternatives considered:** Keep thin commands (~15 lines) that delegate to workflows. Rejected because the indirection still loads 2 files and the reuse never materialized.

**Outcome:** Token savings of ~1,700/ingest and ~400/lint per invocation. Simpler mental model — one file per operation.
