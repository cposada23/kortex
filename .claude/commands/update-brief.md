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
   d. Read projects/project-context.md (now a hub).
      Follow its wikilinks to read the relevant atomic pages:
      - projects/sandbag-fuerza-tres-dias/references/brand-context.md → for Sandbag brief
      - projects/ai-influencer-nagual-arquetipo/references/character-context.md → for Nagual brief
      - projects/milo-ia/references/channel-context.md → for Milo IA brief
      - wiki/references/marketing-framework-context.md → for any brief needing strategy context
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

6. Tell the user which briefs were updated:
   "Updated briefs:
   - [project] → re-upload
     projects/[project-name]/references/[file] to Claude.ai Project
   No changes needed: [other projects]"

7. Append entry to log.md

## Why no hardcoded file lists
This command uses index.md and CLAUDE.md files
to discover project structure dynamically.
Adding a new project to /projects/ automatically
works — no need to edit this command.
The knowledge graph is the source of truth.
