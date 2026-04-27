---
scope: framework
---

# Update Project Brief

Automatically detects which briefs need updating
and regenerates them using the knowledge graph.
No hardcoded file lists — uses index.md and
CLAUDE.md files to discover what belongs where.

## Workflow

1. Run: git diff --name-only HEAD
   to see which files changed this session.
   If empty run: git diff --name-only HEAD~5

2. Read index.md to map each changed file
   to its project. The index tells you which
   project or section each file belongs to.

3. For each affected project:
   a. Find the project folder in /projects/
      or identify it as the shared /wiki layer
   b. Read that folder's CLAUDE.md to understand
      what the project is and what files matter
   c. Read project-instructions.md if it exists
      in that project folder
   d. Follow the project CLAUDE.md to discover which
      context files matter for this project's brief
      (e.g. brand context, audience context, channel
      context, strategy frameworks). Read each one the
      CLAUDE.md flags as relevant.
   e. Read any other files the CLAUDE.md identifies
      as important for that project

4. Generate or update the brief at:
   projects/[project-folder-name]/references/project-brief.md

   Structure every brief as:
   ## 1. What This Project Is
   ## 2. Character or Concept (if applicable)
   ## 3. Positioning and Strategy
   ## 4. Target Audience
   ## 5. Content Angles
   ## 6. Current Priorities
   ## 7. Key Workflows and Tools
   ## 8. Behavior Rules for Claude.ai

   YAML frontmatter:
   title: [Project Name] Brief
   type: context
   layer: wiki
   language: es-en
   tags: [brief, context, claude-ai-project, capa/2-wiki]
   status: active
   updated: [today's date]
   distillation_level: 3

5. Special cases:
   - If CLAUDE.md changed → regenerate ALL briefs
   - If project-context.md changed → regenerate ALL
   - If a new folder appears in /projects/ that has
     no brief yet → generate one automatically

6. Check Claude.ai Projects sync triggers:
   - Read `wiki/references/claude-ai-projects-roster.md` if it exists
     in your Kortex instance.
   - For each regenerated brief path, intersect against the roster's
     Active sync triggers.
   - For each Project whose trigger matched ≥1 regenerated brief,
     surface it in the confirm message.
   - If the roster file does NOT exist, skip the Claude.ai sync line.

7. Tell the user which briefs were updated:
   "Updated briefs:
   - [project] → projects/[project-name]/references/[file] regenerated
   No changes needed: [other projects]

   Claude.ai Projects to sync (click 'Sync now' in Project Knowledge):
   - [list each Project from Step 6, or 'None — no synced briefs changed']

   Note: GitHub sync is read-only — clicking syncs the latest commit.
   No manual file upload needed."

8. Append entry to log.md

## Why no hardcoded file lists
This command uses index.md and CLAUDE.md files
to discover project structure dynamically.
Adding a new project to /projects/ automatically
works — no need to edit this command.
The knowledge graph is the source of truth.
