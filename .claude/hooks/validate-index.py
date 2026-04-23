#!/usr/bin/env python3
# scope: framework
"""
Index reminder hook for Claude Code.
Runs after any .md file is written. Checks if the file appears in index.md.
Prints a reminder if not — never blocks.
"""
import sys
import os

SKIP_PATTERNS = ["CLAUDE.md", "README.md", "INBOX.md", "log.md", "index.md", "MEMORY.md"]

# Only remind for files inside these project zones
WATCHED_DIRS = ["/wiki/", "/output/", "/projects/", "/sources/"]

# Find project root by walking up from this script's location
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
INDEX_PATH = os.path.join(PROJECT_ROOT, "index.md")


def check_file(filepath):
    if not filepath.endswith(".md"):
        return

    filename = os.path.basename(filepath)
    if filename in SKIP_PATTERNS:
        return

    # Only check files in watched directories
    if not any(d in filepath for d in WATCHED_DIRS):
        return

    # Read index.md and check if filename appears
    try:
        with open(INDEX_PATH, "r") as f:
            index_content = f.read()
    except Exception:
        return

    # Check by filename (not full path) — index.md uses relative paths
    if filename in index_content:
        return

    # Also check by relative path from project root
    try:
        rel_path = os.path.relpath(filepath, PROJECT_ROOT)
        if rel_path in index_content:
            return
    except ValueError:
        pass

    print(f"\n📋 INDEX REMINDER: {filename} is not in index.md")
    print(f"   Add it to the appropriate section in index.md.")
    print(f"   Path: {filepath}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_file(sys.argv[1])
