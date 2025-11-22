---
description: Mark a report as resolved
---

Resolve an improvement report. Expected format: `/trk-resolve <id> <resolution description>`

1. Parse the report ID and resolution from the command
2. Read the report from `~/.claude/trk-db/active/<id>.md`
3. Update the report:
   - Change `status: active` to `status: resolved`
   - Add resolved timestamp to frontmatter
   - Fill in Resolution section with the description
4. Move file from `active/` to `resolved/`
5. Git add and commit with message: "Resolve: [id] - [resolution]"
6. Confirm to user: "Report resolved and moved to ~/.claude/trk-db/resolved/<id>.md"
