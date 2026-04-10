# Link Rules

## Format

All internal links must use standard relative markdown links:
`[Display Text](relative/path/to/file.md)`

Do NOT use Obsidian wikilinks `[[FILENAME]]` — they only work in Obsidian.
Relative markdown links work in VS Code, Obsidian, GitHub, and Notion.

## When moving or renaming files

After moving or renaming any .md file:
1. Find all files that link TO the moved/renamed file
2. Update every link to use the new relative path
3. Update links INSIDE the moved file if its depth changed

Use grep to find references: `grep -r "FILENAME.md" --include="*.md"`

## When creating new links

- Always use relative paths from the source file's directory
- Always include the .md extension
- Count `../` levels carefully — verify mentally that the path resolves

## Frontmatter

- Use `related_paths:` (not `related:`) for cross-references
- Each entry is a relative path to the target file
- Format as a YAML list:
  ```yaml
  related_paths:
    - ../concepts/strategy/topic.md
    - ../../tools/tool-name.md
  ```

## Pre-commit validation

A pre-commit hook validates all internal links on every commit.
If broken links are found, the commit is blocked with a report.
Fix all broken links before committing.
