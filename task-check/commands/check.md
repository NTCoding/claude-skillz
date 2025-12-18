---
argument-hint: <task-id>
description: Verify task completion with task-check agent
---

Spawn the task-check agent to verify work is complete.

Task ID: $ARGUMENTS

Provide the task-check agent with:
1. The task ID above
2. A summary of what work was done for this task

Display the full task-check report to the user.

Handle the response:
- PASS → Work complete.
- FAIL → Address issues per the report.
- NEED_INFO → Answer questions and re-run task-check.
