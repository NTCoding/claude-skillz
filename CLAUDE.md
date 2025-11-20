# Claude Skillz Project Guidelines

## System Prompt Composability

System prompts should contain:

1. **Persona definition** - expertise, idols, philosophy
2. **Startup initialization** - load skills with @ references
3. **Domain-specific knowledge** - content NOT in any skill

**Never duplicate skill content in system prompts.**

Skills are loaded via @ references and provide their own complete instructions.

See `/system-prompts/super-tdd-developer.md` for the reference pattern.
