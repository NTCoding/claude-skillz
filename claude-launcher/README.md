# Claude Launcher

Python CLI that launches Claude Code with system prompts and models. Two-step interactive selection or direct shortcuts.

**Features:**
- Interactive 2-step selection (persona → model)
- Shortcut mode: `cl tdd opus` (persona + model, order-independent)
- Model shortcuts: `cl haik`, `cl sonn`, `cl opus` (uses default persona)
- Conflict detection with prominent warnings
- System prompt composability with @ skill imports
- Exports CLAUDE_PERSONA for status line display

**Discovers system prompts from:**
- `~/.claude/system-prompts` (global)
- `<launcher-parent>/system-prompts` (project-local)

Alias as `cl` in your shell for easy access.

## Setup

### Install

```bash
# Alias in ~/.zshrc or ~/.bashrc
alias cl='python3 /path/to/claude-launcher/claude-launcher.py'
```

Or use the full path: `python3 claude-launcher.py`

### Optional: Rich for Better UX

For beautifully formatted tables in interactive mode:

```bash
pip install rich
```

Without `rich`, the launcher works with plain text tables. With it, you get colored output and styled tables.

### Configuration

The launcher automatically detects your Claude Code binary in this order:

1. `$CLAUDE_CMD` environment variable (if set)
2. `which claude` (works for npm/nvm installations)
3. `~/.claude/local/claude` (local installation)

**For npm/nvm installations (recommended):**

Add to your `~/.zshrc` or `~/.bashrc`:

```bash
export CLAUDE_CMD="$(which claude)"
```

**For custom installation paths:**

```bash
export CLAUDE_CMD="/path/to/your/claude"
```

## Usage

### Interactive Mode

No arguments = 2-step interactive selection:

```bash
$ cl

Select persona (or 'q' to cancel):
  1) arc  → Strategic Architect
  2) doc  → Documentation Expert
  3) gen  → Generalist Robot
  ... (more personas)

Enter number: 1

Select model (or 'q' to cancel):
  1) haik → claude-3-5-haiku-20241022
  2) sonn → claude-3-5-sonnet-20241022
  3) opus → claude-3-5-opus-20241022

Enter number: 3

Selected: Strategic Architect
Model: opus

Persona: Strategic Architect
Launching Claude Code...
```

### Shortcut Mode

Combine persona and model shortcuts (order-independent):

```bash
# Persona only (default opus)
$ cl tdd
$ cl opt
$ cl arc

# Model only (default generalist-robot)
$ cl haik
$ cl sonn
$ cl opus

# Combined (any order)
$ cl tdd sonn
$ cl sonn tdd        # Same result
$ cl opt haik
$ cl haik opt        # Same result
```

Shortcuts:
- **Personas (3 chars):** `tdd`, `opt`, `prd`, `arc`, `doc`, `rct`, `inv`, `wrt`, `tsc`, `viz`, `uix`, `gen`
- **Models (4 chars):** `haik`, `sonn`, `opus`

### Conflict Detection

Multiple personas or models are caught with prominent warnings:

```
⚠️  SHORTCUT CONFLICT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Multiple personas specified: tdd and opt
Using: tdd (first match)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Adding Your Own Personas

1. Create `system-prompts/your-persona.md` with frontmatter:

```markdown
---
name: Your Persona Name
shortcut: ypr
---

[Your system prompt content...]

## Skills

- @../skill-name/SKILL.md
```

2. Your shortcut is immediately available: `cl ypr`
