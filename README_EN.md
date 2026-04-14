# Knowledge Brain

A personal AI knowledge base that grows with you. Powered by [Claude Code](https://claude.ai/claude-code).

Drop in raw material — courses, articles, PDFs, ideas. Claude reads it, distills it into atomic wiki pages, links them together, and keeps everything indexed. Every session makes the system smarter.

## The Hemingway Bridge

The #1 problem with AI-assisted knowledge work: **you lose context between sessions.** Every new chat starts from zero. You re-explain your project, re-establish your preferences, and waste the first 10 minutes getting oriented.

This framework solves it with the **Hemingway Bridge** — a session continuity system inspired by Hemingway's writing habit of stopping mid-sentence so he'd know exactly where to pick up the next day.

```
/bridge-out   ← End of session: captures where you stopped,
                decisions made, and the exact next action

/bridge       ← Start of session: reads the bridge note,
                orients you in under 60 seconds
```

**The result:** Every session picks up exactly where the last one ended. No re-explaining. No context loss. Your AI assistant has full continuity across sessions.

## How It Works

This is a **three-layer knowledge system** maintained by Claude Code:

| Layer | Location | Purpose |
|---|---|---|
| Layer 1 — Sources | `/sources` | Immutable raw material (courses, articles, PDFs) |
| Layer 2 — Wiki | `/wiki` | Synthesized atomic pages — the actual "brain" |
| Layer 3 — Schema | `.claude/` + `CLAUDE.md` | Rules that govern how the system behaves |

You add raw material. Claude reads it, distills it into wiki pages, connects them, and keeps the index current.

```
                         +--------------+
                         |  inbox/      |
                         |  INBOX.md    |  capture zone
                         |  drop/       |  (text + files)
                         +------+-------+
                                |
                                v
+-------------+     /ingest      +-------------+    pulled by    +-------------+
|   SOURCES   | ----------------> |    WIKI      | <------------ |  PROJECTS   |
|  (Layer 1)  |  read & distill  |  (Layer 2)   |   tools, refs  |  (Layer 3)  |
|  immutable  |                  |  atomic pages |               |  execution  |
|  + inbox/   |                  +-------------+                |  + inbox/   |
+-------------+                        ^                        +-------------+
  course inbox                    index.md                      project inbox
  auto-tagged                   master catalog                  auto-tagged

                    +----------------------------------+
                    |         .claude/ (SCHEMA)         |
                    |  rules - commands - hooks - skills |
                    |     governs all three layers       |
                    +----------------------------------+
```

## Quick Start (5 minutes)

### Prerequisites

| Tool | Required | Purpose |
|---|---|---|
| [Claude Code](https://claude.ai/claude-code) | Yes | Primary interface — reads, writes, and maintains the knowledge base |
| [Git](https://git-scm.com/) | Yes | Version control and safety net |
| Python 3 | Yes | Runs validation hooks (frontmatter, links) |
| Any markdown editor (VS Code, Obsidian, etc.) | Optional | Browsing and editing wiki pages |

### Setup

```bash
# 1. Create your knowledge brain from this template
#    (click "Use this template" on GitHub, or clone directly)
git clone <your-repo-url> my-knowledge-brain
cd my-knowledge-brain

# 2. Install the pre-commit hook (validates links + frontmatter on every commit)
cat > .git/hooks/pre-commit << 'HOOK'
#!/bin/sh
ROOT="$(git rev-parse --show-toplevel)"
python3 "$ROOT/.claude/hooks/validate-links.py" || exit 1
python3 "$ROOT/.claude/hooks/validate-frontmatter.py" --staged
HOOK
chmod +x .git/hooks/pre-commit

# 3. Customize CLAUDE.md
#    Open CLAUDE.md and fill in the [Owner] and [Active Priorities] sections

# 4. Open Claude Code
claude

# 5. Start your first session
/bridge
```

That's it. Claude reads `CLAUDE.md` and `.claude/rules/` automatically.

## The Four Habits

Build these four habits and the system compounds on its own:

| Habit | When | Command | What happens |
|---|---|---|---|
| **Capture** | Anytime you find something interesting | Drop it in `inbox/` | Zero friction — just dump it |
| **Ingest** | When inbox has items | `/ingest` | Claude reads, distills, creates wiki pages, indexes |
| **Bridge** | Start and end of every session | `/bridge` + `/bridge-out` | Full context continuity across sessions |
| **Lint** | Monthly | `/lint` | Health check — finds orphans, debt, gaps |

## Commands

| Command | What it does |
|---|---|
| `/bridge` | **Start of session.** Reads log, memory, and index. Orients you in 60 seconds. |
| `/bridge-out` | **End of session.** Creates a Hemingway Bridge — captures where you stopped and the exact next action. |
| `/ingest` | **Process all inboxes.** Scans global, course, and project inboxes. Creates wiki pages. Updates index. |
| `/lint` | **Monthly health check.** Finds orphan pages, distillation debt, stale content, broken links. |
| `/query` | **Knowledge base query.** Asks a question, searches the wiki, synthesizes an answer. |
| `/safe-change` | **Branch workflow.** Creates a feature branch, makes changes, shows summary, merges on approval. |

## Folder Structure

```
my-knowledge-brain/
+-- inbox/           Capture zone
|   +-- INBOX.md     Text entries (URLs, ideas, quick notes)
|   +-- drop/        Drop files here (PDFs, articles, transcripts)
|   +-- processed/   Files move here after ingest
+-- sources/         Raw immutable material
|   +-- courses/     Course folders (standard structure below)
|       +-- notes/       Lesson notes, module summaries
|       +-- assignments/ Homework and exercises
|       +-- resources/   Reference material, cheat sheets
|       +-- inbox/       Course-specific inbox for ingest
+-- wiki/            Synthesized knowledge — the brain
|   +-- areas/       Ongoing areas of focus
|   +-- concepts/    Atomic concept pages
|   +-- tools/       Tools catalog and tutorials
|   +-- playbooks/   Step-by-step workflows
|   +-- decisions/   Architecture and strategy decisions
|   +-- references/  Reference docs and guides
+-- projects/        Active project execution (standard structure below)
|   +-- references/  Briefs, brand context, research
|   +-- prompts/     Project-specific prompts
|   +-- content/     Scripts, drafts, campaign plans
|   +-- assets/      Generated images, videos, media
|   +-- inbox/       Project-specific inbox for ingest
+-- output/          Query results, lint reports, session notes
|   +-- sessions/    Hemingway Bridge session notes
+-- archive/         Superseded documents
+-- .claude/         System schema (Layer 3)
|   +-- commands/    Slash commands (/bridge, /ingest, /lint, etc.)
|   +-- rules/       Operational rules (frontmatter, links, language)
|   +-- hooks/       Validation scripts (frontmatter, links, index)
|   +-- templates/   Page templates for new files
+-- index.md         Master catalog — Claude reads this to find anything
+-- log.md           Chronological operation log (append-only)
+-- CLAUDE.md        Root schema — governs all Claude behavior
```

## Distillation Levels

Every wiki page tracks how processed its knowledge is:

| Level | State | What it means |
|---|---|---|
| 0 | Raw dump | Just captured, not processed |
| 1 | First pass | Read, key points identified |
| 2 | Distilled | Essential content rewritten in own words |
| 3 | Synthesized | Connected to other pages, implications drawn |
| 4 | Expression-ready | Can generate content directly from this page |

Pages start at level 1 (after ingest) and move up through review. A page at level 4 is an asset — you can generate a blog post, video script, or presentation directly from it.

## Adding Content

### Add new knowledge
Drop material in the right inbox — context is automatic:

| What you have | Where to put it |
|---|---|
| A quick idea or URL | `inbox/INBOX.md` |
| A PDF, article, or transcript | `inbox/drop/` |
| Material from a specific course | `sources/courses/[course]/inbox/` |
| Material for a specific project | `projects/[project]/inbox/` |

Then run `/ingest`.

### Add a new course
1. Create `sources/courses/[course-name]/`
2. Add a `CLAUDE.md` describing the course
3. Create `inbox/` and `inbox/processed/` subfolders
4. Drop course files and run `/ingest`

### Add a new project
1. Create `projects/[project-name]/`
2. Add a `CLAUDE.md` describing the project
3. Create `references/`, `prompts/`, `inbox/`, and `inbox/processed/` subfolders
4. Start working — Claude will build the project brief as you go

## What NOT to Do

| Mistake | Why it breaks things |
|---|---|
| Edit files in `/sources` | Layer 1 is immutable. Synthesize into `/wiki` instead. |
| Put query results in `/projects` | `/projects` is for execution. Query results go to `/output`. |
| Use wikilinks `[[like this]]` | They aren't portable. Use `[text](relative/path.md)` instead. |
| Create a `.md` file without indexing | The auto-index rule ensures Claude can find everything via `index.md`. |
| Skip frontmatter | Every `.md` file (except CLAUDE.md/README.md) needs YAML frontmatter. |
| Delete files without committing first | Git is the safety net. Commit, then delete freely. |

## Feature Comparison

| Feature | Knowledge Brain | Notion | Obsidian alone | RAG / Vector DB |
|---|---|---|---|---|
| Session continuity (Hemingway Bridge) | Yes | No | No | No |
| AI maintains the wiki for you | Yes | No | Partial (plugins) | No |
| Works offline | Yes | No | Yes | Depends |
| Portable (plain markdown + git) | Yes | No | Yes | No |
| Auto-distillation tracking | Yes | No | Manual | No |
| Distributed inbox system | Yes | No | No | No |
| Pre-commit link validation | Yes | No | No | No |
| Zero vendor lock-in | Yes | No | Mostly | No |

## Built With

- [Claude Code](https://claude.ai/claude-code) — AI interface that reads, writes, and maintains the knowledge base
- [Git](https://git-scm.com/) — version control and safety net
- Markdown — universal, portable, human-readable
- Python — lightweight validation hooks

## License

MIT
