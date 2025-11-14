# Lightweight Task Workflow

Task list + session state for multi-session work.

## What It Does

Maintains three files in `.claude/`:
- `tasks.md` - numbered checklist
- `requirements.md` - implementation specs, verification steps
- `session.md` - current task, progress, context

Claude follows a strict state machine and **prefixes every message with the current state** (e.g., `🔵 STATE: WORKING`).

## Setup

Say "create a plan" and Claude will:
1. Ask you to describe your tasks
2. Ask about requirements, testing standards, and verification steps
3. Create `.claude/tasks.md` (checklist)
4. Create `.claude/requirements.md` (specs + verification)
5. Create `.claude/session.md` (current state)

Then say "continue" to start working.

## State Machine

```
                         user: "continue"
                                ↓
                       ┌────────────────┐
                   ┌───│ CHECK_STATUS   │←──────────┬──────────┐
                   │   │ Read session.md│           │          │
                   │   └────────┬───────┘           │          │
                   │            │                   │          │
        Status=    │            │ Status=           │          │
        "Complete" │            │ "in progress"     │          │
                   │            │                   │          │
                   ↓            ↓                   │          │
           ┌───────────┐  ┌──────────────┐         │          │
           │ AWAITING_ │  │ WORKING      │←────┐   │          │
           │ COMMIT    │  │              │     │   │          │
           │           │  │ Read:        │     │   │          │
           │ Ask       │  │ requirements │     │   │          │
           │ permission│  │ tasks.md     │     │   │          │
           │ STOP      │  │              │     │   │          │
           └─────┬─────┘  │ Write:       │     │   │          │
                 │        │ session.md   │     │   │          │
       user: yes │        └──────┬───────┘     │   │          │
                 │               │             │   │          │
                 │               │ task done   │   │          │
                 │               │             │   │          │
                 │               ↓             │   │          │
                 │        ┌──────────────┐     │   │          │
                 │        │ VERIFY       │     │   │          │
                 │        │              │     │   │          │
                 │        │ Run steps    │     │   │          │
                 │        │ from         │─────┘   │          │
                 │        │ requirements │ fail    │          │
                 │        └──────┬───────┘         │          │
                 │               │                 │          │
                 │               │ pass            │          │
                 │               │                 │          │
                 │               ↓                 │          │
                 │        ┌──────────────┐         │          │
                 │        │ COMPLETE     │         │          │
                 │        │              │         │          │
                 │        │ Write:       │         │          │
                 │        │ session.md   │         │          │
                 │        │ Status=      │─────────┘          │
                 │        │ "Complete"   │                    │
                 │        └──────────────┘                    │
                 │                                            │
                 ↓                                            │
           ┌──────────────────┐                              │
           │ MARK_TASK_       │                              │
           │ COMPLETE         │                              │
           │                  │                              │
           │ Write: tasks [x] │                              │
           │ Write: session.md│──────────────────────────────┘
           │ (next task)      │
           └──────────────────┘
```

**Note:** To ensure Claude uses the skill, you may want to @-mention it. Claude may deviate from the workflow based on hard-coded plan mode instructions, so it may be more compliant by exiting plan mode.

## Files

**tasks.md:**
```markdown
- [ ] Task 1: Extract UserService
- [x] Task 2: Add tests
- [ ] Task 3: Update documentation
```

**requirements.md:**
```markdown
## Global Guidelines
- No breaking changes to public APIs
- Add logging for error cases
- Follow existing code style

## Verification & Definition of Done
- npm test - all tests pass
- npm run lint - no errors
- npm run build - successful

## Task 1: Extract UserService
- Move user methods from AppService to new UserService
- Maintain backward compatibility
- Update dependency injection

## Task 2: Add tests
- Cover happy path and error cases
- Include null/undefined edge cases
- Mock external dependencies
```

**session.md:**
```markdown
**Current Task:** Task 3

## What's Done
- Extracted UserService (commit abc123)
- Added tests (commit def456)

## Next Steps
1. Update documentation

## Context
- Using npm for package management
- Found edge case: user.email can be null
```
