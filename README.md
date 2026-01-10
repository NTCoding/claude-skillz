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

You can [add your own personas](claude-launcher/README.md#adding-your-own-personas) with frontmatter metadata.

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

12 pre-built personas ready to use via `cl` shortcuts. Each auto-loads relevant skills:

| Shortcut | Persona | Skills Loaded |
|----------|---------|--------------|
| `tdd` | Super TDD Developer | tdd-process, software-design-principles, critical-peer-personality |
| `opt` | Claude Code Optimizer | independent-research, critical-peer-personality, concise-output |
| `prd` | PRD Expert | independent-research, concise-output |
| `arc` | Strategic Architect | software-design-principles, lightweight-design-analysis |
| `doc` | Documentation Expert | concise-output, questions-are-not-instructions |
| `rct` | Super React Developer | software-design-principles, critical-peer-personality |
| `inv` | Technical Investigator | observability-first-debugging, independent-research |
| `wrt` | Writing Tool | concise-output, questions-are-not-instructions |
| `tsc` | Super TypeScript Developer | software-design-principles, critical-peer-personality |
| `viz` | Frontend Visualization Expert | data-visualization, software-design-principles |
| `uix` | UI/UX Design Leader | software-design-principles, concise-output |
| `gen` | Generalist Robot | independent-research, questions-are-not-instructions, concise-output, software-design-principles, confidence-honesty |

### Composability

System prompts use @ references to load skills efficiently:

1. Add frontmatter metadata (name + shortcut):
   ```markdown
   ---
   name: My Custom Persona
   shortcut: cst
   ---
   ```

2. Add a `## Skills` section to reference skills:
   ```markdown
   ## Skills

   - @../independent-research/SKILL.md
   - @../concise-output/SKILL.md
   ```

3. Run `cl cst` - the launcher processes @ references before launching

**Why this matters:** @ reference processing during launcher startup means skills are embedded in the system prompt, not loaded via Read operations. This avoids wasting 18k+ tokens of context window.

## Plugins

- **track-and-improve** - Capture mistakes and improvement opportunities with automatic 5 whys root cause analysis
- **automatic-code-review** - Automatic semantic code review on session stop with configurable project-specific rules. Auto-initializes with default rules, supports any language.
