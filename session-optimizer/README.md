# Session Optimizer

Analyze Claude Code session transcripts for concrete optimization opportunities.

## Usage

```
/optimize-session [session-id|slug]
```

Defaults to most recent session in current project.

## What It Does

Spawns 4 parallel subagents, each analyzing the transcript from a different angle:

| Agent | Focus |
|-------|-------|
| conversation-efficiency-analyzer | Wasted cycles, back-and-forth, misinterpretations |
| tool-and-skill-usage-analyzer | Unused tools, missed parallelism, underutilized capabilities |
| skill-compliance-analyzer | Violations of loaded skills |
| context-and-skills-gap-analyzer | Missing project context, skill-building opportunities |

Produces a ranked report of findings with evidence and actionable recommendations, then enters interactive discussion mode.

## Output

- Structured report with findings sorted by impact
- Each finding includes: category, evidence (transcript quotes), recommendation
- Interactive walkthrough proposing specific actions (CLAUDE.md rules, new skills, config changes)
