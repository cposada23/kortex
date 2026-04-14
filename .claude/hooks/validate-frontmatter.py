#!/usr/bin/env python3
"""
Frontmatter validator hook for Claude Code.

Modes:
  1. Single file (PostWrite hook): python3 validate-frontmatter.py <filepath>
     - HARD dirs (wiki/, output/): exits 1 on failure → blocks the Write
     - SOFT dirs (everything else): prints warning only
  2. Batch/pre-commit: python3 validate-frontmatter.py --staged
     - Validates all staged .md files
     - Exits 1 if any HARD dir file fails (blocks commit)
     - Prints warnings for SOFT dir files

Skipped files: CLAUDE.md, README.md, INBOX.md, log.md, index.md
"""
import sys
import os
import subprocess

REQUIRED_FIELDS = ["title", "type", "layer", "language", "tags", "updated"]
SKIP_PATTERNS = ["CLAUDE.md", "README.md", "INBOX.md", "log.md", "index.md"]

# Directories where frontmatter violations block the write
HARD_DIRS = ["/wiki/", "/output/"]
# All other dirs get soft warnings only


def check_file(filepath):
    # Only check .md files
    if not filepath.endswith(".md"):
        return 0

    filename = os.path.basename(filepath)
    if filename in SKIP_PATTERNS:
        return 0

    is_hard = any(d in filepath for d in HARD_DIRS)

    try:
        with open(filepath, "r") as f:
            content = f.read()
    except Exception:
        return 0

    # Must start with ---
    if not content.startswith("---"):
        label = "BLOCKED" if is_hard else "WARNING"
        print(f"\n⚠️  FRONTMATTER {label}: {filepath}")
        print(f"   This file needs YAML frontmatter. See .claude/rules/frontmatter.md")
        print(f"   Use template: .claude/templates/concept.md\n")
        return 1 if is_hard else 0

    # Extract frontmatter block
    parts = content.split("---", 2)
    if len(parts) < 3:
        label = "BLOCKED" if is_hard else "WARNING"
        print(f"\n⚠️  FRONTMATTER {label} (malformed): {filepath}")
        return 1 if is_hard else 0

    frontmatter = parts[1]
    missing = [f for f in REQUIRED_FIELDS if f + ":" not in frontmatter]

    if missing:
        label = "BLOCKED" if is_hard else "WARNING"
        print(f"\n⚠️  FRONTMATTER {label}: {filepath}")
        print(f"   Missing fields: {', '.join(missing)}")
        print(f"   Required: {', '.join(REQUIRED_FIELDS)}")
        if is_hard:
            print(f"   Fix these fields before writing to wiki/ or output/.\n")
            return 1
        else:
            print()

    return 0


def get_staged_md_files():
    """Return list of staged .md files (for pre-commit use)."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True, text=True
    )
    root = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], text=True
    ).strip()
    return [
        os.path.join(root, f)
        for f in result.stdout.strip().split("\n")
        if f.endswith(".md") and f
    ]


def check_staged():
    """Validate frontmatter on all staged .md files. Return exit code."""
    files = get_staged_md_files()
    if not files:
        return 0

    hard_failures = 0
    soft_warnings = 0

    for filepath in files:
        result = check_file(filepath)
        if result == 1:
            hard_failures += 1

    if hard_failures:
        print(f"\n❌ FRONTMATTER VALIDATION FAILED — {hard_failures} file(s) "
              f"in hard-enforced dirs (wiki/, output/)")
        print("   Fix frontmatter, then try committing again.\n")
        return 1

    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--staged":
            sys.exit(check_staged())
        else:
            sys.exit(check_file(sys.argv[1]))
