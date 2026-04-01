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

# Optional: Install fzf for interactive fuzzy search
brew install fzf  # macOS
```

See [available personas](#system-prompts) below. You can [add your own](claude-launcher/README.md#adding-your-own-personas).

---

## OpenCode Launcher

**Generates OpenCode agents from the same personas used by Claude Launcher.**

This repo contains system prompts that work with both Claude Code and OpenCode:
- **Claude Launcher** (`cl`) - for Claude Code
- **OpenCode Launcher** - generates agents for OpenCode

```bash
# Generate OpenCode agents (run once or after changing personas)
python3 opencode-launcher/generate-opencode-agents.py

# Then use OpenCode - agents appear in agent selector
opencode
```

See [opencode-launcher/README.md](opencode-launcher/README.md) for details.

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

12 pre-built personas ready to use via `cl` shortcuts:

| Shortcut | Persona |
|----------|---------|
| `tdd` | [Super TDD Developer](system-prompts/super-tdd-developer.md) |
| `opt` | [Claude Code Optimizer](system-prompts/claude-code-optimizer.md) |
| `prd` | [PRD Expert](system-prompts/prd-expert.md) |
| `arc` | [Strategic Architect](system-prompts/strategic-architect.md) |
| `doc` | [Documentation Expert](system-prompts/documentation-expert.md) |
| `rct` | [Super React Developer](system-prompts/super-react-developer.md) |
| `inv` | [Technical Investigator](system-prompts/technical-investigator.md) |
| `wrt` | [Writing Tool](system-prompts/writing-tool.md) |
| `tsc` | [Super TypeScript Developer](system-prompts/super-typescript-developer.md) |
| `viz` | [Frontend Visualization Expert](system-prompts/frontend-visualization-expert.md) |
| `uix` | [UI/UX Design Leader](system-prompts/ui-design-expert.md) |
| `gen` | [Generalist Robot](system-prompts/generalist-robot.md) |

### Composability

System prompts use @ references to load skills. See [CLAUDE.md](CLAUDE.md) for composability guidelines and [launcher docs](claude-launcher/README.md#adding-your-own-personas) for creating custom personas.a

## Plugins

- **track-and-improve** - Capture mistakes and improvement opportunities with automatic 5 whys root cause analysis
- **automatic-code-review** - Automatic semantic code review on session stop with configurable project-specific rules. Auto-initializes with default rules, supports any language.
text