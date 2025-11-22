# Track and Improve

Capture mistakes and improvement opportunities with automatic 5 whys root cause analysis.

## Installation

```bash
/plugin marketplace add file:///path/to/claude-skillz
/plugin install track-and-improve@claude-skillz
```

## Usage

**Capture a mistake:**
```
/trk Added comments when CLAUDE.md forbids them
```

Claude performs 5 whys analysis, extracts session context, creates report in `~/.claude/trk-db/active/`, and auto-commits to git.

**Review reports:**
```
/trk-review
```

Shows summary of active reports organized by recency and category.

**Resolve a report:**
```
/trk-resolve 2025-01-15-10-30-00 Added PreToolUse hook to block comments
```

Moves report to `resolved/` and commits resolution.

## Storage

Reports stored in `~/.claude/trk-db/` with git version control:
- `active/` - Unresolved reports
- `resolved/` - Completed improvements

Each report contains:
- Your description
- Claude's 5 whys root cause analysis
- Last 5 messages of conversation context
- Metadata (timestamp, project, category)
- Resolution (when resolved)

## Workflow

1. Spot a mistake during session
2. Type `/trk <description>`
3. Continue working
4. Weekly: `/trk-review` to analyze patterns
5. Update CLAUDE.md, create hooks, or add skills based on insights
