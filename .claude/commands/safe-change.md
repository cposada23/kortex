# Safe Change Workflow

Use this command for any significant file operation.

## Workflow
1. Ask the user to describe the change they want
2. Generate a branch name from the description
   format: feature/short-description (lowercase, hyphens)
3. Run: git checkout -b [branch-name]
4. Execute the requested changes on this branch
   (edits, moves, writes — but do NOT git add or commit yet)
5. Show the user a clear summary of everything that changed
6. Ask: "Review the changes in your IDE, then type YES to 
   merge to main or NO to go back"
   (The user reviews the actual files in their editor —
   much easier than reading a terminal diff)
7. If YES:
   - git add and commit the changes
   - Append entry to log.md
   - git add . && git commit -m "update log.md"
   - git checkout main
   - git merge [branch-name]
   - git push
   - git branch -d [branch-name]
8. Update TODOs:
   - Check which project(s) or areas were affected by the merge
   - For each affected area, update its TODO.md:
     move completed items to Done, update in-progress items
   - Update root TODO.md counts to match
   - git add and commit TODO changes
   - git push
9. Run post-merge checks:
   - Check git diff to see what changed
   - If any project has an `artifacts.md`, check if changed files
     match sync_triggers — warn if so
10. Confirm:
   "Merged and pushed to main successfully.
   log.md updated.
   TODOs updated: [list TODO files changed, or 'No TODO changes needed']
   [Artifact sync warnings if any]"
11. If NO:
   - Discard ALL changes and restore to pre-branch state:
     git checkout main -- .
     git clean -fd
     git checkout main
     git branch -D [branch-name]
   - Confirm: "All changes discarded. Back on main, 
     exactly as before."

## Rules
- Always create a branch before any bulk operation
- Never merge without explicit YES from user
- Always update log.md BEFORE merging so it is 
  included in the final commit to main
- Branch name must be descriptive not generic
- Never auto-delete a rejected branch — always ask first
