# Idea Frontmatter Schema

Ideas captured in any `/inbox/` folder carry a specific frontmatter
schema — narrower than the wiki schema in [frontmatter.md](frontmatter.md),
but designed so the same YAML block flows through the full pipeline
(capture → triage → further processing) without re-interpretation.

This rule exists because ideas cross surfaces (Claude.ai mobile →
GitHub web → Claude Code desktop) and each re-interpretation costs a
copy-paste and drops context. Fixing the schema at capture time means
every downstream step reads the idea from the file instead of
re-inferring it from prose.

## Scope

Applies to `.md` files with `type: idea` that live in any inbox:

- Root capture inbox (cross-project ideas)
- Per-project inboxes (project-scoped ideas)
- Course inboxes (course-tied ideas)

After triage, an idea typically migrates out of `/inbox/` into a
destination path defined by the target project's own convention.
Once it leaves the inbox it picks up the normal `type: reference`
schema (or whatever type the destination uses) — this rule no longer
applies.

## Required fields

```yaml
title: "idea title (may be WIP)"
type: idea
layer: project
language: en                          # en | es | en-es
tags: [relevant-tags, capa/3-proyecto]
updated: YYYY-MM-DD
status: inbox                         # inbox | in-validation | in-production | published | rejected | archived | (project-specific states)
angle: "one-sentence editorial angle — why this idea is distinct"
target_channel: project-name          # the destination project key — one of your project folder names, or `cross-project`
```

The first six fields satisfy the base schema from
[frontmatter.md](frontmatter.md) so the validator hook passes. The
last three (`status`, `angle`, `target_channel`) are the idea-specific
additions.

## Optional fields

```yaml
why_it_works: "why this angle engages the target audience"
created_in: claude-ai-mobile          # claude-code | claude-ai-mobile | claude-ai-desktop | voice | other
created_date: YYYY-MM-DD              # capture date (if different from `updated`)
```

Add any other fields your project needs (scoring, round ID, execution
surface, etc.) — the schema is additive.

## Field explanations

| Field | Why it exists |
|-------|--------------|
| `title` | Candidate title. WIP is fine. |
| `status` | Pipeline state. Routes the item: `inbox` means needs triage; post-triage states tell downstream workflows how to handle it. |
| `angle` | One-sentence editorial angle. What makes this idea distinct from similar ones on the same topic. |
| `target_channel` | Destination project. **The ingest routes by this field, not by the inbox path.** An idea dropped in the root inbox with `target_channel: <project>` belongs to that project regardless of physical location. |
| `why_it_works` | Why the angle engages the target audience. |
| `created_in` | Surface where the idea was captured. Useful for measuring where you are most productive ideating. |
| `created_date` | Capture date (distinct from `updated`, which tracks last edit). |

## Default routing when `target_channel` is unclear

If an idea's destination is genuinely ambiguous at capture time, drop
it in the root `/inbox/` with `target_channel: cross-project` and tag
`needs-routing`. Next `/ingest` pass will flag it for manual triage.

## File naming in inbox

Pre-triage (inside any `/inbox/`): `<slug>.md`. No date prefix — the
`created_date` / `updated` field in frontmatter is the chronological
source of truth.

Post-triage naming follows the destination convention of the target
project — define that convention in that project's `CLAUDE.md`.

## Relationship to the general frontmatter schema

[frontmatter.md](frontmatter.md) defines the canonical schema for
content pages. This file narrows that schema for one case: inbox items
with `type: idea`. The required fields here (`status`, `angle`,
`target_channel`) are the minimum needed for routing; they are not
required on non-idea files.

## Claude.ai Project Instructions

The other half of this rule lives outside your repo: Claude.ai
Projects that generate ideas need a Project Instructions block telling
the model to emit this exact schema. Without that, ideas generated in
Claude.ai mobile/desktop re-interpret at capture time and the whole
rule is defeated.

This is a manual one-time setup per Claude.ai Project — Claude Code
cannot configure claude.ai from the repo. Paste the required-fields
block above into your Project Instructions and tell the model
"respond with YAML frontmatter only, no prose, no explanation."

## Enforcement

The `validate-frontmatter.py` hook requires the base fields
(`title`, `type`, `layer`, `language`, `tags`, `updated`) on any page
outside `/inbox/` soft-enforcement zones. For inbox items the hook
warns but does not block — friction-free capture is the priority. The
additional idea-specific fields (`status`, `angle`, `target_channel`)
are enforced socially by this rule and by whichever skills you add on
top (idea generation, cross-validation, `/ingest`).
