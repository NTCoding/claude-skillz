# Claude Skills & Composable Personas

Reusable skills and composable system prompts for Claude Code.

## Installation

### Setup Marketplace

**Local:**
```bash
/plugin marketplace add file:///absolute/path/to/claude-skillz
```

**GitHub:**
```bash
/plugin marketplace add ntcoding/claude-skillz
```

### Install Plugins

**Interactive:**
1. Run `/plugin`
2. Select `Browse and install plugins`
3. Select `claude-skillz` marketplace
4. Select desired plugin
5. Select `Install now`

**Direct:**
```bash
/plugin install <plugin-name>@claude-skillz
```

## Skills

### Process Orchestration

- **tdd-process** - Complete TDD state machine with red-green-refactor cycle and 11 enforced rules
- **lightweight-task-workflow** - Task lists and session state for multi-session work

### Tasks

- **switch-persona** - Mid-conversation persona switching without restart
- **lightweight-implementation-analysis-protocol** - Forces code flow tracing before implementing to prevent guessing
- **lightweight-design-analysis** - Identifies refactoring opportunities across 8 design quality dimensions

### Knowledge

- **software-design-principles** - Object calisthenics, dependency inversion, fail-fast, type-driven design, intention-revealing naming

### Personality

- **critical-peer-personality** - Professional, skeptical communication style that coaches rather than serves

## System Prompts

- **super-tdd-developer** - TDD/DDD expert that auto-loads tdd-process, software-design-principles, and critical-peer-personality skills
- **claude-code-optimizer** - Workflow optimization specialist for improving Claude Code productivity
- **requirements-expert** - Requirements analysis specialist for breaking down features into specifications

### Composability

System prompts use @ references to load skills efficiently:

1. Add a `## Skills` section to your system prompt
2. Reference skills: `- @~/.claude/skills/skill-name/SKILL.md`
3. Run `claude-launcher` - it imports skills before launching

This avoids Read operations that consume 18k+ tokens of context.

See `system-prompts/super-tdd-developer.md` for an example.

## Plugins

- **track-and-improve** - Capture mistakes and improvement opportunities with automatic 5 whys root cause analysis

## Tools

- **claude-launcher** - Interactive system prompt selector for session start
