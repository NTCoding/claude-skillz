# OpenCode Launcher

Generates OpenCode agent definitions from system prompts.

## Setup

1. **Generate agents** from your system prompts:
   ```bash
   python3 /path/to/opencode-launcher/generate-opencode-agents.py
   ```

2. **Run OpenCode** - agents will appear in the agent selector:
   ```bash
   opencode
   ```

3. **Switch agents** using Tab or `@agent-name`

## What it does

- Scans `system-prompts/` for persona definitions
- Processes `@` imports (same as Claude launcher)
- Creates agent markdown files in `~/.config/opencode/agents/`
- Each persona becomes a primary agent in OpenCode

## Re-run after changes

Run `generate-opencode-agents.py` whenever you:
- Add new personas to `system-prompts/`
- Modify existing personas
- Add new skills

## Usage

```bash
# Generate/update agents
python3 opencode-launcher/generate-opencode-agents.py

# Then use OpenCode normally
opencode
```
