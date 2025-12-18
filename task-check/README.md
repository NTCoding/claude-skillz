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
- You have not yet run task-check for this task (or you've addressed issues from the last run)

### How to spawn task-check

Use the Task tool with subagent_type "task-check". Provide:

1. **Task ID**: The identifier for this task. Get this from:
   - The task file name (e.g., "task-42")
   - The task number the user mentioned
   - The issue/ticket number if referenced
   - If no ID exists, describe: "Task: [brief description from user's original request]"

2. **Work summary**: What you actually did. Include:
   - Files created or modified (list paths)
   - Key changes made
   - Any decisions or trade-offs you made
   - What you did NOT do (if you intentionally skipped something)

### Displaying the report

Copy the ENTIRE task-check report into your response to the user. Do not summarize or paraphrase. The user needs full visibility.

### Handling the response

**If STATUS = PASS:**
Work is complete. Tell the user.

**If STATUS = FAIL:**
Read the ISSUES section. For each issue:

- **Unfinished requirements** (task said to do X, you didn't do X): Fix immediately. No user approval needed.
- **Missing acceptance criteria**: Fix immediately. No user approval needed.
- **Bugs or broken code paths**: Fix immediately. No user approval needed.
- **Missing edge cases that a user would reasonably expect**: Fix immediately. No user approval needed.
- **Minor fixes** (typos, formatting, small improvements): Fix immediately. No user approval needed.
- **Significant changes** (different approach, architectural changes, adding features not in original task, substantial rework): STOP. Present the issue to the user. Ask if they want you to proceed.

After fixing, re-run task-check.

**If STATUS = NEED_INFO:**
Read the QUESTIONS section. For each question:

- If the answer is in the task definition, PRD, or codebase: Answer it yourself and re-run task-check with your answer.
- If the answer requires a decision only the user can make: Ask the user, wait for response, then re-run task-check.

### Loop behavior

Keep running task-check until:
- STATUS = PASS, or
- User explicitly says to stop (e.g., "that's fine", "skip the check", "move on"), or
- You have run task-check 3 times for the same task

**If 3 attempts and still FAIL:**
Stop. Tell the user: "task-check has failed 3 times. Here are the outstanding issues: [list]. I need your guidance on how to proceed."

Do NOT skip the first task-check because the task seems simple.
```

## Manual Trigger

If Claude forgets:

```
/check <task-id>
```
