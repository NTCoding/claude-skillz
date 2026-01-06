---
argument-hint: [--count <n>] [--state merged|closed|all]
description: Analyze PR feedback patterns and suggest config updates to catch issues locally
allowed-tools: Bash, Glob, Read, Grep
---

# Learn From PR Feedback

Analyze feedback from recent PRs (CodeRabbit, SonarQube, developer comments) and suggest updates to project configuration to catch these issues before PR review.

## Arguments

```
ARGUMENTS: $ARGUMENTS
```

- `--count <n>`: Number of PRs to analyze (default: 5)
- `--state <state>`: PR state to fetch - merged, closed, or all (default: merged)

## Procedure

### Step 1: Verify Prerequisites

Check that `gh` CLI is authenticated:

```bash
gh auth status
```

If not authenticated, stop and inform user to run `gh auth login`.

### Step 2: Fetch Recent PRs

```bash
gh pr list --state <state> --limit <count> --json number,title,url,mergedAt,closedAt
```

If no PRs found, report "No PRs found matching criteria" and stop.

Report:
```
Found X PRs to analyze:
1. #123: PR title
2. #124: PR title
...
```

### Step 3: Collect All Feedback

For each PR, fetch ALL comments and reviews:

**PR review comments (inline code comments):**
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments --paginate
```

**PR reviews (approval/request changes with body):**
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/reviews --paginate
```

**Issue-style comments (general discussion):**
```bash
gh api repos/{owner}/{repo}/issues/{pr_number}/comments --paginate
```

Extract from each comment:
- `body`: The actual feedback text
- `user.login`: Who wrote it (helps identify bots like CodeRabbit, SonarQube)
- `path` and `line`: Where in code (if applicable)
- `created_at`: When

**Categorize by source:**
- **Automated tools**: Identify by user.login or body markers (CodeRabbit, SonarQube, Codacy, DeepSource, etc.)
- **Human reviewers**: Everything else

Report:
```
Collected feedback from PR #X:
- [Tool name]: Y comments
- Human reviewers: Z comments
```

### Step 4: Analyze Patterns

Group all collected feedback and identify patterns:

**Look for recurring themes such as:**
- Code style and formatting issues
- Logic errors and edge cases
- Security concerns
- Performance issues
- Testing gaps
- Architecture and design feedback
- Documentation issues
- Language-specific best practices

For each pattern found:
- Count occurrences across all PRs
- Note specific examples (file, line, comment text)
- Identify the source (which tool/reviewer caught it)

**Prioritize by:**
1. Frequency (appears in multiple PRs)
2. Source consistency (caught by multiple reviewers/tools)
3. Severity (security > bugs > style)

Report top patterns:
```
## Feedback Patterns Found

### High Frequency (appeared in 3+ PRs)
1. [Pattern]: [X occurrences] - caught by [sources]
   Example: "[actual comment snippet]"

### Medium Frequency (appeared in 2 PRs)
...

### Single Occurrence (but notable)
...
```

### Step 5: Discover Current Config

Search the project for ANY configuration files that might be relevant:

```bash
find . -maxdepth 3 -type f \( \
  -name "CLAUDE.md" -o \
  -name ".claude" -o \
  -name ".*rc" -o \
  -name ".*rc.json" -o \
  -name ".*rc.yaml" -o \
  -name ".*rc.yml" -o \
  -name "*.config.js" -o \
  -name "*.config.ts" -o \
  -name "*.config.json" -o \
  -name ".pre-commit-config.yaml" -o \
  -name ".editorconfig" -o \
  -name "Makefile" -o \
  -name "pyproject.toml" -o \
  -name "setup.cfg" -o \
  -name "tox.ini" -o \
  -name ".rubocop.yml" -o \
  -name "Gemfile" -o \
  -name "go.mod" -o \
  -name "Cargo.toml" -o \
  -name "composer.json" \
\) 2>/dev/null | head -50
```

Also check for `.claude/` directory contents.

For each relevant config, note:
- What it currently enforces
- What gaps exist relative to PR feedback patterns

Report:
```
## Current Configuration

Found these config files:
- [file]: [brief summary of what it controls]
...
```

### Step 6: Generate Recommendations

For each high-frequency pattern, propose specific config updates:

**Format for each recommendation:**

```markdown
### [Pattern Name]

**Problem:** [What the PR feedback consistently caught]

**Frequency:** [X occurrences across Y PRs]

**Caught by:** [Tool names, specific reviewers]

**Examples from PRs:**
- PR #123: "[comment snippet]"
- PR #456: "[comment snippet]"

**Suggested fixes:**

**Option A: CLAUDE.md** (catches during Claude Code sessions)
```markdown
[Exact text to add to CLAUDE.md]
```

**Option B: [Relevant tool/config for this project]**
```
[Exact config to add, appropriate to the project's language/tooling]
```

**Option C: Pre-commit hook** (catches before commit)
```yaml
[Hook configuration if applicable]
```

**Recommended:** [Which option and why]
```

### Step 7: Present Summary

```markdown
# PR Feedback Analysis Complete

## PRs Analyzed
- Count: X
- Date range: [oldest] to [newest]
- Feedback sources: [list tools and reviewer count]

## Key Findings

### Patterns That Should Be Caught Locally

| Pattern | Frequency | Top Source | Recommended Fix |
|---------|-----------|------------|-----------------|
| [name]  | X times   | [source]   | [config type] |

## Detailed Recommendations

[Full recommendations from Step 6]

## Quick Wins (Copy-Paste Ready)

### Add to CLAUDE.md:
```markdown
[All CLAUDE.md additions consolidated]
```

### Add to [other relevant config]:
```
[Additions consolidated by config file]
```

---
*Analysis based on PRs: #X, #Y, #Z...*
*Run `/learn-from-prs` again after implementing changes to verify improvement*
```

## Notes

- This command only suggests changes, never modifies files
- Focus recommendations on issues that appeared multiple times
- For single-occurrence issues, mention them but deprioritize
- Recommend fixes appropriate to the project's actual language and tooling
- When a pattern could be caught by multiple tools, recommend the earliest in the pipeline
- If feedback is vague or unclear, note it but don't force a recommendation
