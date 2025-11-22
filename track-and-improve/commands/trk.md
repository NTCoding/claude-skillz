---
description: Capture mistake or improvement opportunity with 5 whys analysis
---

Capture a mistake or improvement opportunity. Follow these steps:

1. Extract the description from the user's `/trk` command
2. Identify your current persona/role (what system prompt you're operating under)
3. Perform 5 whys root cause analysis of why this mistake happened
4. Extract last 5 message exchanges from the current conversation
5. Create a report in `~/.claude/trk-db/active/` with format:

```markdown
---
id: YYYY-MM-DD-HH-MM-SS
created: ISO8601 timestamp
project: current project name
persona: current persona/role
status: active
category: rule-violation|improvement|confusion
---

# [User's description]

## 5 Whys Analysis

1. **Why did this happen?** [Your analysis]
2. **Why did that happen?** [Your analysis]
3. **Why did that happen?** [Your analysis]
4. **Why did that happen?** [Your analysis]
5. **Root cause:** [Your conclusion]

## Context (Last 5 Messages)

[Extracted conversation]

## Resolution

[Empty - filled when resolved]
```

6. Initialize git repo if `~/.claude/trk-db/.git` doesn't exist
7. Git add and commit with message: "Add report: [description]"
8. Confirm to user: "Report captured: ~/.claude/trk-db/active/[id].md"
