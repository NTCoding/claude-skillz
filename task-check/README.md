# Task Check

Verifies task completion before Claude finishes work. Catches incomplete work, bugs, and quality issues.

## Install

```
/plugin install task-check@claude-skillz
```

## Setup

Add to your project's CLAUDE.md:

```markdown
## Task Completion Protocol

### When to run task-check

Run task-check when ALL of these are true:
- You believe the task is complete
- You are about to tell the user the work is done
- You have not yet run task-check for this task

Do NOT skip task-check because the task seems simple.

### How to spawn task-check

Use the Task tool with subagent_type "task-check". Provide:
1. **Task ID**: From task file name, number, or issue reference
2. **Task location**: File path or CLI command to retrieve task details
3. **Work summary**: Files modified, changes made, decisions, what you skipped
4. **Attempt**: Which attempt (1, 2, or 3). Start with 1.

Follow the instructions in the task-check report exactly.
```

## Manual Trigger

If Claude forgets:

```
/check
```
