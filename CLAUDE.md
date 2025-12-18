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

## Version Management (MANDATORY)

When making ANY change to this repository, you MUST increment versions in `.claude-plugin/marketplace.json`:

### Which version to bump:

1. **Modifying a skill** (e.g., `tdd-process/SKILL.md`):
   → Bump the `version` of the plugin that contains it (e.g., `development-skills`)

2. **Modifying a plugin** (e.g., `track-and-improve/commands/`):
   → Bump that plugin's individual `version` field

3. **Adding a new plugin**:
   → Set new plugin version to "1.0.0"
   → Bump `metadata.version`

### Format:
- Semantic versioning (e.g., "1.0.0" → "1.0.1")
- Patch for fixes, minor for features, major for breaking changes

**Why:** Claude Code caches plugins by their INDIVIDUAL version. Bumping only `metadata.version` does nothing—clients check the plugin's own `version` field to detect updates.
