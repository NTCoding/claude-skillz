# Claude Launcher

Simple bash script that wraps the Claude Code `--system-prompt` option. Start your claude session by choosing from available system prompts.

**Discovers system prompts from:**
- `~/.claude/system-prompts` (global)
- `<launcher-parent>/system-prompts` (project-local)

No symlinks needed. I have the command aliased as `cl`.

```bash
➜  code: cl
Select a Claude Code system prompt:
1) claude-code-optimizer	5) super-tdd-developer
2) d3-guru			        6) tdd-developer
3) ddd-cs-architect		    7) webstorm-productivity-coach
4) ddd-refactoring-planner	8) Cancel

Enter number: 2

Selected: d3-guru
Launching Claude Code with d3-guru system prompt...
```
