#!/usr/bin/env python3
"""
Pre-commit hook: validate internal markdown links.
Scans all staged .md files for broken internal links.
Blocks commit if any are found.
"""
import os
import re
import subprocess
import sys

PROJECT_ROOT = subprocess.check_output(
    ["git", "rev-parse", "--show-toplevel"], text=True
).strip()

SKIP_DIRS = {".git", "node_modules", ".claude"}


def get_staged_md_files():
    """Return list of .md files that are staged for commit."""
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
        capture_output=True, text=True
    )
    return [f for f in result.stdout.strip().split("\n") if f.endswith(".md") and f]


def get_all_md_files():
    """Return set of all .md files in the project (for target resolution)."""
    files = set()
    for root, dirs, filenames in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in filenames:
            if f.endswith(".md"):
                rel = os.path.relpath(os.path.join(root, f), PROJECT_ROOT)
                files.add(rel)
    return files


def strip_code(content):
    """Remove fenced code blocks and inline code spans from content."""
    content = re.sub(r'```[\s\S]*?```', '', content)
    content = re.sub(r'`[^`]+`', '', content)
    return content


def check_file(filepath, all_files):
    """Check all internal markdown links in a file. Return list of broken links."""
    broken = []
    abs_path = os.path.join(PROJECT_ROOT, filepath)

    if not os.path.exists(abs_path):
        return broken

    try:
        with open(abs_path, "r") as f:
            content = f.read()
    except Exception:
        return broken

    file_dir = os.path.dirname(abs_path)

    clean_content = strip_code(content)
    clean_lines = clean_content.split("\n")

    for line_num, line in enumerate(clean_lines, 1):
        for match in re.finditer(r'\[([^\]]*)\]\(([^)]+)\)', line):
            target = match.group(2)

            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue

            media_ext = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp",
                         ".mp4", ".mov", ".pdf")
            if any(target.lower().endswith(ext) for ext in media_ext):
                continue

            target_path = target.split("#")[0]
            if not target_path:
                continue

            resolved = os.path.normpath(os.path.join(file_dir, target_path))

            if not os.path.exists(resolved):
                broken.append((line_num, target))

    return broken


def main():
    staged = get_staged_md_files()
    if not staged:
        sys.exit(0)

    all_files = get_all_md_files()
    total_broken = []

    for filepath in staged:
        broken = check_file(filepath, all_files)
        if broken:
            total_broken.append((filepath, broken))

    if total_broken:
        print("\n❌ BROKEN LINKS FOUND — commit blocked\n")
        for filepath, broken_links in total_broken:
            print(f"  {filepath}:")
            for line_num, target in broken_links:
                print(f"    line {line_num}: {target}")
        print(f"\n  Total: {sum(len(b) for _, b in total_broken)} broken link(s) "
              f"in {len(total_broken)} file(s)")
        print("  Fix broken links, then try committing again.\n")
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
