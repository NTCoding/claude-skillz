# Claude Skills & Composable Personas

Reusable skills and composable system prompts for Claude Code.

---

## Claude Launcher

**Interactive system prompt and model selector for Claude Code.**

Start Claude with your chosen persona and model in seconds:

```bash
# Interactive 2-step selection (persona → model)
$ cl

# Direct shortcuts (order-independent)
$ cl tdd opus        # Super TDD Developer + Opus
$ cl opt sonn        # Claude Code Optimizer + Sonnet
$ cl haik            # Generalist Robot + Haiku (default persona + model)

# Model-only (uses generalist-robot)
$ cl sonn
$ cl opus
```

**Features:**
- Order-independent shortcuts: `cl tdd sonn` = `cl sonn tdd`
- Frontmatter-based shortcuts (add your own personas instantly)
- Automatic skill loading via @ references
- Conflict detection with prominent warnings
- Exports CLAUDE_PERSONA for status line display

**Setup:**

```bash
alias cl='python3 /path/to/claude-skillz/claude-launcher/claude-launcher.py'

# Optional: Install rich for colored tables in interactive mode
pip install rich
```

### Persona Shortcuts

| Code | Persona | Purpose |
|------|---------|---------|
| `tdd` | Super TDD Developer | Red-green-refactor cycles with 11 enforced rules |
| `opt` | Claude Code Optimizer | Workflow optimization & Claude Code mastery |
| `prd` | PRD Expert | Product requirements & specifications |
| `arc` | Strategic Architect | System design for scale & evolution |
| `doc` | Documentation Expert | Clear technical documentation |
| `rct` | Super React Developer | React/frontend development |
| `inv` | Technical Investigator | Systematic debugging & investigation |
| `wrt` | Writing Tool | Structured writing assistance |
| `tsc` | Super TypeScript Developer | TypeScript type system mastery |
| `viz` | Frontend Visualization Expert | Data visualization & charts |
| `uix` | UI/UX Design Leader | Visual design & brand identity |
| `gen` | Generalist Robot | Neutral assistant (default persona) |

### Model Shortcuts

| Code | Model |
|------|-------|
| `haik` | Claude 3.5 Haiku |
| `sonn` | Claude 3.5 Sonnet |
| `opus` | Claude 3.5 Opus |

---

## Installation

### Per-project

Add the plugin to your `settings.json`. See [Claude Plugin Settings](https://code.claude.com/docs/en/settings#plugin-configuration).

### Globally Setup Marketplace

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

## Available Skills

Skills are reusable behavioral instructions loaded into personas. Load them with `@` references in your system prompts.

### Research & Evidence

- **independent-research** - Research-driven investigation. Never guess—validate solutions before presenting. Use WebFetch, WebSearch, testing.
- **confidence-honesty** - Force honest confidence assessment. Express confidence as percentage, explain gaps, validate assumptions before presenting.

### Communication & Output

- **concise-output** - Signal-over-noise. Eliminate verbose phrases, prioritize density. Every word must carry information.
- **critical-peer-personality** - Professional, skeptical communication. Challenge constructively, propose instead of asking, coach rather than serve.
- **questions-are-not-instructions** - Answer questions literally. Don't interpret as hidden instructions. STOP after answering, let user decide.

### Code & Design

- **software-design-principles** - Object calisthenics, dependency inversion, fail-fast error handling, feature envy detection, intention-revealing naming.
- **lightweight-implementation-analysis-protocol** - Trace execution paths before implementing. Create lightweight diagrams. Prevent wasted effort from assumptions.
- **lightweight-design-analysis** - Systematic design review across 8 dimensions: Naming, Object Calisthenics, Coupling & Cohesion, Immutability, Domain Integrity, Type System, Simplicity, Performance.

### Development Processes

- **tdd-process** - Strict TDD state machine: red-green-refactor with 11 enforced rules. Meaningful failures, minimum implementations, full verification.
- **writing-tests** - Principles for effective tests. Naming conventions, assertion best practices, comprehensive edge case checklists (based on BugMagnet).
- **observability-first-debugging** - Systematic debugging. Add instrumentation to gather specific data. Evidence before hypothesis.

### Workflows & Tools

- **switch-persona** - Mid-conversation persona switching without restart. Lists personas, reads file, switches immediately.
- **lightweight-task-workflow** - Task list state machine for multi-session work. Tracks status, prevents auto-advancement, enforces state transitions.
- **create-tasks** - Convert requirements into actionable tasks following a structured template. Engineering-ready work items.

### Specialized

- **data-visualization** - Build charts, graphs, dashboards. Visual execution, technical implementation, perceptual foundations, chart selection, layout algorithms, library guidance.
- **typescript-backend-project-setup** - NX monorepo setup for TypeScript backend projects optimized for AI-assisted development.

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

- **automatic-code-review** - Automatic semantic code review on session stop with configurable project-specific rules. Auto-initializes with default rules, supports any language.
- **track-and-improve** - Capture mistakes and improvement opportunities with automatic 5 whys root cause analysis

## Tools

- **claude-launcher** - Interactive system prompt selector for session start
