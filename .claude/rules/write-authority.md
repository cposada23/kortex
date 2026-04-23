# Write Authority Rule

Structural writes to your Kortex instance pass through Claude Code only.
Claude.ai chat and Cowork may read and propose captures; they do not
write to knowledge graph structure directly.

## What counts as "Claude Code"

Claude Code runs in three surfaces — **all three are equally the
authoritative write surface:**

- **CLI** — terminal invocation (`claude`).
- **VS Code extension** — same Claude Code embedded in the editor.
- **Desktop tab** — Claude Code mode inside the Claude Desktop app.

There is no hierarchy among them. What matters is that Code (any
surface) is driving the write, because Code is the only surface running
your repo's `.claude/` hooks, rules, and commands.

## What Claude Code owns

Claude Code is the sole authoritative writer for structural changes to
your Kortex instance:

- Wiki / synthesis layer edits (new pages, distillation, cross-refs)
- Project folders (TODOs, briefs, artifacts, specs, project `CLAUDE.md`)
- Source folders (ingest additions, cross-refs — never rewriting raw
  material)
- Schema — root `CLAUDE.md`, `.claude/rules/`, `.claude/commands/`,
  `.claude/skills/`, `.claude/hooks/`, `.claude/templates/`
- Indexes, logs, TODO registries
- Output artifacts (sessions, audits, handoffs, reports)
- Git commits and pushes

## What Claude.ai chat / Cowork may do

- **Read** your repo via GitHub sync (Claude.ai Project) or Filesystem
  MCP (Desktop, future/optional).
- **Propose captures** by creating files in your capture/inbox zone —
  only after you have verified your GitHub write-sync path end-to-end.
  Until then, treat Claude.ai + Cowork as read-only.
- **Synthesize across sources** in chat — prompts, cross-AI validation,
  ideation, research. The *output* of that work comes back to Claude
  Code as input, not as a direct write.

## What Claude.ai chat / Cowork must NOT do

- Commit to any branch.
- Edit wiki or project structure directly.
- Change schema files (`CLAUDE.md`, `.claude/rules/`, `.claude/commands/`,
  `.claude/skills/`, `.claude/hooks/`).
- Update TODOs, briefs, or logs.
- Modify validators or templates.

## Why one authority

- **No merge conflicts between surfaces.** If Code and Claude.ai both
  wrote, you would need distributed locking or constant rebases. One
  writer eliminates the class of problem.
- **Hooks + validators only run in Code.** Frontmatter validation, link
  validation, scope tagging — all enforced at commit time by
  `.claude/hooks/`. Writes outside Code bypass those checks.
- **Commit discipline + history quality.** Workflows like `/safe-change`,
  `/bridge-out`, `/handoff` shape commit messages and log entries
  consistently. A Claude.ai chat writing commits directly would drift
  in tone, scope, and format — and every drift compounds in the history.

## Narrow exception — capture zone

Once you have tested and verified GitHub write-sync from Claude.ai
Project end-to-end, you may allow Claude.ai to write to your capture
zone (the raw-input inbox) only — it has no schema requirements and
exists to collect ideas before they are triaged in Code. Structural
writes remain Code-only regardless of that test outcome.

Filesystem MCP, when used, is a *read* channel — it exposes local
folders to Claude Desktop for context. It does not change write
authority.

## Enforcement

This rule is social + rationale, not automated. The real enforcement
layer is the existing Claude Code pre-commit hooks:

- `validate-frontmatter.py` rejects malformed frontmatter.
- Link validator rejects broken internal links.
- Scope tag validation (see [scope.md](scope.md)) flags untagged
  `.claude/` files.

Any write that bypasses Code bypasses these checks too — which is
exactly what this rule is designed to prevent.
