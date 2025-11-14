# Claude Skills

A collection of basic Claude skills for common tasks.

## Skills

### lightweight-task-workflow
Task list + session state for multi-session work. Maintains `.claude/tasks.md`, `requirements.md`, and `session.md` to track progress across Claude sessions. Never uses TodoWrite, never creates commits, user stays in control.

### lightweight-implementation-analysis-protocol
Forces Claude to trace code flow and verify understanding before implementing. Quick verification (trace → diagram → confirm) to prevent guessing-based implementations.
