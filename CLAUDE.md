# Claude Skillz Project Guidelines

## System Prompt Composability

System prompts follow a composable architecture where skills are loaded efficiently at session startup.

### Structure

System prompts should contain:

1. **Persona definition** - expertise, idols, philosophy, collaboration style
2. **Skills section** - @ references to skill files (processed by launcher)
3. **Domain-specific knowledge** - content NOT duplicated in any skill

### How It Works

**@ Reference Processing:**
- The `claude-launcher` pre-processes @ references before launching Claude Code
- Skills are embedded directly into the system prompt (not loaded via Read operations)
- A "Loaded Skills" manifest is added at the top showing what was loaded
- Debug output saved to `/tmp/claude-launcher-debug.md` for verification

**Token Efficiency:**
- Pre-processing avoids 18k+ tokens of message history overhead
- Near-zero overhead vs monolithic prompts (1% difference)
- Skills remain composable and reusable across personas

### Creating Composable System Prompts

**Pattern:**
```markdown
# Persona Name

## Persona
[Define expertise, philosophy, approach]

---

## Skills

- @~/.claude/skills/skill-name/SKILL.md
- @~/.claude/skills/another-skill/SKILL.md

---

## Domain Knowledge
[Domain-specific content not in skills]
```

**Rules:**
- Never duplicate skill content in system prompts
- Use @ references for reusable behavioral instructions
- Keep domain knowledge specific to this persona only

### Example

See `/system-prompts/super-tdd-developer.md` for the reference pattern.

## Marketplace Plugin Distribution

This repo is a Claude Code plugin marketplace. When adding new skills or plugins:

### Adding New Skills

1. Create skill directory with `SKILL.md`
2. Update `.claude-plugin/marketplace.json` - add to `development-skills.skills` array:
   ```json
   "skills": [
     "./tdd-process",
     "./your-new-skill"
   ]
   ```

### Adding New Plugins

1. Create plugin directory with `commands/`, `agents/`, or `hooks/`
2. Add plugin entry to `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "plugin-name",
     "source": "./plugin-directory",
     "description": "Brief description",
     "version": "1.0.0",
     "category": "productivity|development",
     "keywords": ["tag1", "tag2"]
   }
   ```

Keep marketplace.json updated so users can install via `/plugin install <name>@claude-skillz`.
