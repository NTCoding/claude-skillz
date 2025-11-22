---
description: Review active improvement reports
---

Review all active improvement reports:

1. Read all files from `~/.claude/trk-db/active/`
2. Parse YAML frontmatter from each report
3. Present organized summary:

```
Found X active reports:

Recent (last 7 days):
- [id]: [description] ([project])
- [id]: [description] ([project])

Older:
- [id]: [description] ([project])

By category:
- rule-violation: X
- improvement: X
- confusion: X
```

4. Ask user: "Which would you like to review in detail?"
5. When user selects, read and display full report
6. Discuss patterns, root causes, and potential resolutions
