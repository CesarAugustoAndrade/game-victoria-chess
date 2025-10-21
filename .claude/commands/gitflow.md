---
description: Automate git workflow - commit pending changes, push, and create new branch
---

You are tasked with automating a complete git workflow. Follow these steps EXACTLY in order:

## Step 1: Check for pending changes
Run `git status --porcelain` to check if there are any uncommitted changes.

## Step 2: Handle pending changes (if any exist)

### 2A: If there ARE pending changes:
1. Show the user what files have changes with `git status --short`
2. Stage all changes: `git add -A`
3. Create a commit with a descriptive message based on the changes:
   - Analyze the modified files to understand the nature of changes
   - Use conventional commit format: `type: description`
   - Common types: feat, fix, docs, refactor, test, chore, style
   - Include the Claude Code footer:
     ```
     🤖 Generated with [Claude Code](https://claude.com/claude-code)

     Co-Authored-By: Claude <noreply@anthropic.com>
     ```
4. Push to current branch: `git push origin <current-branch>`
5. Confirm push was successful

### 2B: If there are NO pending changes:
1. Inform the user: "✅ Working directory clean - no changes to commit"
2. Skip to Step 3

## Step 3: Get current branch name
Run `git branch --show-current` to get the current branch name.

## Step 4: Create and checkout new branch
1. Extract the branch name from user's command (argument after `/gitflow`)
2. Create and switch to new branch: `git checkout -b <new-branch-name>`
3. Confirm: "✅ Switched to new branch '<new-branch-name>'"

## Step 5: Show final status
Run `git status` to show the current state.

## Important Notes:
- If `git push` fails (e.g., branch doesn't exist on remote), inform user but continue with branch creation
- Use heredoc format for multi-line commit messages
- Do NOT use the Write or Edit tools - only use Bash commands
- Do NOT ask for confirmation - execute automatically
- Handle errors gracefully and inform the user

## Example Usage:
User: `/gitflow feature/new-combat-system`

Expected behavior:
1. Check for changes
2. If changes exist: stage, commit with analyzed message, push
3. Create and switch to `feature/new-combat-system`
4. Show status

## Error Handling:
- If branch already exists: Inform user and ask if they want to switch to it
- If push fails: Inform user but continue with branch creation
- If no branch name provided: Ask user to provide a branch name

**Arguments**: The branch name to create (required)

Now execute this workflow with the branch name provided by the user.
