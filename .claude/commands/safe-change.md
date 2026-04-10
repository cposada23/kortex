# Safe Change Workflow

Use this command for any significant file operation.

## Workflow
1. Ask the user to describe the change they want
2. Generate a branch name from the description
   format: feature/short-description (lowercase, hyphens)
3. Run: git checkout -b [branch-name]
4. Execute the requested changes on this branch
5. Run: git add . && git commit -m "description of changes"
6. Show the user a clear summary of everything that changed
7. Ask: "Everything looks good? Type YES to merge to main 
   or NO to go back"
8. If YES:
   - Append entry to log.md first
   - git add . && git commit -m "update log.md"
   - git checkout main
   - git merge [branch-name]
   - git push
   - git branch -d [branch-name]
9. Confirm:
   "Merged and pushed to main successfully.
   log.md updated."
10. If NO:
   - git checkout main
   - Ask the user: "Do you want to delete the branch 
     [branch-name] or keep it for later?"
   - If delete: git branch -D [branch-name]
   - If keep: confirm branch name so user can return to it

## Rules
- Always create a branch before any bulk operation
- Never merge without explicit YES from user
- Always update log.md BEFORE merging so it is 
  included in the final commit to main
- Branch name must be descriptive not generic
- Never auto-delete a rejected branch — always ask first
