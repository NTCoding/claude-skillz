---
argument-hint: "[session-id|slug]"
description: Analyze a session transcript for optimization opportunities
---

# Optimize Session

Analyze a Claude Code session transcript to find concrete opportunities to work faster and better.

## Arguments

```
ARGUMENTS: $ARGUMENTS
```

- Optional: session ID (UUID) or session slug. Defaults to most recent session in current project.

## Procedure

### Step 1: Locate the Session File

Determine the current project's conversation directory:

```bash
# Encode current working directory path: replace / with -
# e.g., /Users/nicktune/code/my-project → -Users-nicktune-code-my-project
ls -t ~/.claude/projects/<encoded-path>/*.jsonl | head -5
```

If argument provided:
- If UUID: find `<session-id>.jsonl`
- If slug: search JSONL files for matching `slug` field

If no argument: use the most recently modified JSONL file.

Report: "Analyzing session: [slug or ID] ([message count] messages, [duration])"

### Step 2: Read the Session Transcript

Read the JSONL file. Extract:
- All user and assistant messages (skip file-history-snapshot, system errors)
- The system-reminder blocks (contain loaded skills and available tools)
- Basic stats: message count, first/last timestamp, tools used, model

### Step 3: Prepare Transcript for Subagents

Create a condensed version of the transcript suitable for subagent context:
- Include all user messages in full
- Include assistant text responses in full
- Include tool_use calls (name + input summary) but truncate large tool results to first 500 chars
- Include system-reminder blocks in full (skills and tools lists)
- Skip file-history-snapshot entries
- Skip duplicate/redundant system messages

Write the condensed transcript to a temporary file:
```bash
# Write to /tmp/session-optimizer-transcript-<session-id>.md
```

Also write the extracted context (loaded skills list, available tools list, session stats) to:
```bash
# Write to /tmp/session-optimizer-context-<session-id>.md
```

### Step 4: Launch Analysis Subagents

Launch ALL FOUR subagents IN PARALLEL using the Task tool:

1. **conversation-efficiency-analyzer** — finds wasted cycles, unnecessary back-and-forth, misinterpretations
2. **tool-and-skill-usage-analyzer** — finds unused tools, missed parallelism, underutilized capabilities
3. **skill-compliance-analyzer** — finds violations of loaded skills
4. **context-and-skills-gap-analyzer** — finds missing project context and skill-building opportunities

Each subagent receives the same prompt:
```
Analyze this Claude Code session transcript for optimization opportunities.

## Session Context
[Contents of /tmp/session-optimizer-context-<session-id>.md]

## Transcript
[Contents of /tmp/session-optimizer-transcript-<session-id>.md]
```

### Step 5: Collect and Present Report

Once all subagents return, compile their findings into a single report:

```markdown
# Session Optimization Report

**Session:** [slug or ID]
**Duration:** [time]
**Messages:** [count] ([user count] user, [assistant count] assistant)
**Model:** [model name]
**Tools used:** [list]
**Skills loaded:** [list]

---

## Findings

[All findings from all 4 subagents, numbered sequentially]
[Sorted by impact: high → medium → low]
[Deduplicate if multiple subagents found the same issue — keep the most detailed version]

---

**Total findings:** [count] ([high count] high, [medium count] medium, [low count] low impact)
```

### Step 6: Interactive Discussion

After presenting the report, say:

"Pick a finding number to discuss in detail, or 'all' to walk through each one."

For each finding discussed:
1. Show the full evidence
2. Explain the optimization opportunity
3. Propose the best action for this specific finding — whatever fits the context:
   - Edit CLAUDE.md with a new rule
   - Create a new skill file
   - Update project config or documentation
   - Create a GitHub issue (`gh issue create`)
   - Add to a todo list or backlog
   - Update an existing skill's trigger conditions or rules
   - Add a hook
   - Any other action that makes sense
4. Offer the user a choice:
   - **Do it now** — implement the change immediately
   - **Create a ticket** — create a GitHub issue capturing the finding and proposed action
   - **Note it** — just acknowledge, no action now
   - **Skip** — move to next finding

## Notes

- If the transcript is too large for subagent context windows, split it into overlapping chunks and give each subagent the full transcript in segments, instructing them to analyze all segments.
- Clean up temp files after analysis is complete.
