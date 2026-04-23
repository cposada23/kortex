# Scope Tagging for `.claude/` Files

Every file under `.claude/` declares a scope so the framework layer
(this file + its siblings) can stay cleanly separated from project-specific
artifacts you add on top.

## Values

- `framework` — portable; part of the Kortex framework itself
- `project:<name>` — bound to a specific project in your repo
- `user` — reserved for future personal overrides; not in use today

Keeping these tagged makes it safe to upstream framework improvements
without sweeping your project-specific commands/skills, and makes it
obvious at a glance which `.claude/` files are "yours" vs "the framework's".

## How to declare

### `.md` files (`commands/`, `skills/`)

Minimal YAML frontmatter at the top:

```yaml
---
scope: framework
---
```

Or for project-scoped files:

```yaml
---
scope: project:my-project
---
```

The frontmatter validator hook (`.claude/hooks/validate-frontmatter.py`)
exempts `.claude/commands/`, `.claude/skills/`, and `.claude/templates/`
from the full content-frontmatter schema — `scope:` is the only required
field on commands/skills. Adding title/tags/etc. for human readability is
allowed and the hook will not complain.

### `.py` files (`hooks/`)

Top-of-file comment (after the shebang):

```python
#!/usr/bin/env python3
# scope: framework
```

### `rules/` and `templates/` files

No declaration needed. Both layers are framework-scoped by convention:

- A project-specific "rule" belongs in that project's `CLAUDE.md`, not in
  `.claude/rules/`.
- Templates under `.claude/templates/` are themselves prototypes for
  content-bearing wiki pages — their body frontmatter is intentionally
  the frontmatter of the *new file* being created, not metadata about
  the template. Tagging the template file itself with `scope:` would
  leak into every new page. Path is the scope marker instead.

### Settings files

`settings.json` and `settings.local.json` are out of scope for this
system — they belong to the Claude Code CLI runtime.

## When creating a new file under `.claude/`

1. Decide its scope:
   - Does it reference a specific project folder or data? → `project:<name>`
   - Is it a general workflow, validator, or skill reusable across
     projects? → `framework`
2. Add the scope declaration per the format above.
