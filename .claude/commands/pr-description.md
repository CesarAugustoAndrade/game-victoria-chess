---
description: Generate comprehensive pull request descriptions
tools: [Read, Grep, Glob, Bash]
---

Please analyze the changes with diff origin main and generate a comprehensive pull request description with the following format:

### What's Changed

- **Brief category**: Brief description of what changed and why it matters
- **Another category**: More details about specific changes
- Use bullet points for each major change
- Group related changes together
- Include file paths and key technical details
- Mention any breaking changes, new features, bug fixes, or refactoring
- Be specific about configuration changes, dependency updates, or structural improvements

### Why

Provide context for the changes. Ideally it should be expressed in one paragraph.

Guidelines:

1. Analyze git diffs, file changes, and directory structure
2. Group changes logically (config, features, refactoring, etc.)
3. Use bold formatting for change categories
4. Be concise but descriptive
5. Include technical context that helps reviewers understand the impact
6. Mention any testing, performance, or compatibility considerations

Analyze the current git status and recent commits to understand what has changed making a diff agains origin main

After generating the description, always create a markdown file named `PR_DESCRIPTION.md` in the project root with the complete pull request description.
