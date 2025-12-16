---
name: create-tasks
description: "Creates well-formed tasks following a template that engineers can implement. Use when creating tasks, defining work items, creating tasks from PRD, breaking down features, or converting requirements into actionable tasks."
version: 1.0.0
---

# Create Tasks

Creates well-formed tasks that provide large amounts of contexts so that engineers that weren't in conversations can implement the task without any prior knowledge and without asking questions.

Tasks should be created using the tools and documentation conventions in the project the skills is being applied to. If the conventions are not clear, ask the user to clarify and then document them.

## What Engineers Need

Every task must provide:
- What they're building (deliverable)
- Why it matters (context)
- Key decisions and principles they must follow
- Acceptance criteria
- Dependencies
- Related code/patterns
- How to verify it works

## Task Template

```markdown
## Deliverable: [What user/stakeholder sees]

### Context
[Where this came from and why it matters. PRD reference, bug report, conversation summary—whatever helps engineer understand WHY]

### Key Decisions and principles
- [Decision/Principle] — [rationale]

### Delivers
[Specific outcome in user terms]

### Acceptance Criteria
- [Condition] → [expected result]

### Dependencies
- [What must exist first]

### Related Code
- `path/to/file` — [what pattern/code to use]

### Verification
[Specific commands/tests that prove it works]
```

## Process

1. Understand what needs to be built
2. Gather context (from PRD, conversation, bug report, etc.)
3. Identify key decisions that affect implementation
4. Define clear acceptance criteria
5. Find related code/patterns in the codebase
6. Specify verification commands
7. Output task using template

## Checkpoint

Before finalizing any task, verify:

**Can an engineer who wasn't in this conversation implement it without asking questions?**

If no → add what's missing.
