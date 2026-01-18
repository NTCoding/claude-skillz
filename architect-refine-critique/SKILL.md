---
name: Architect-Refine-Critique
description: "Three-phase design review workflow using sub-agents. Architect designs (separation-of-concerns), Refiner analyzes (tactical-ddd), Critique challenges. Main agent orchestrates and facilitates user discussion."
version: 1.0.1
---

# Architect-Refine-Critique

Three-phase design review with dedicated sub-agents. Each agent works independently, producing their best work. Main agent is thin orchestrator only.

**CRITICAL: Phases run SEQUENTIALLY. Each phase MUST complete before the next begins.**

## Roles

| Role | Skill | Output |
|------|-------|--------|
| **Architect** | separation-of-concerns | plan.md |
| **Refiner** | separation-of-concerns + tactical-ddd | refined.md |
| **Critique** | separation-of-concerns + tactical-ddd | critique.md |

## Invoking

User says: `/arc [name] [target]`

- `[name]` — review name (used for folder)
- `[target]` — what to review (codebase path, PRD reference, etc.)

Example: `/arc payment-refactor src/payments/`

## Main Agent Checklist

Follow this checklist exactly. Do not skip steps. Do not run phases in parallel.

### Phase 1: Architect

1. [ ] Spawn a **general-purpose** sub-agent with write permissions
2. [ ] Use this exact prompt (replace [name] and [target]):

```
You are the Architect. Produce the best possible design for this codebase/requirements.

Target: [target]

Skills to apply:
- separation-of-concerns

Your job:
1. Analyze the codebase or requirements provided
2. Apply the separation-of-concerns skill thoroughly
3. Produce a complete design plan
4. IMPORTANT: Write your plan to: docs/design-reviews/[name]/plan.md

Be thorough. Produce your best work. You MUST write the file before finishing.
```

3. [ ] **WAIT** for the sub-agent to complete
4. [ ] **VERIFY** docs/design-reviews/[name]/plan.md exists before proceeding

### Phase 2: Refiner

5. [ ] Spawn a **general-purpose** sub-agent with write permissions
6. [ ] Use this exact prompt (replace [name]):

```
You are the Refiner. Improve this design by applying tactical DDD patterns.

Read the design at: docs/design-reviews/[name]/plan.md

Skills to apply:
- separation-of-concerns
- tactical-ddd

Your job:
1. Read the plan.md file first
2. Apply the separation-of-concerns and tactical-ddd skills thoroughly
3. Improve any aspects of the design that you feel can be improved
4. IMPORTANT: Write your refined design to: docs/design-reviews/[name]/refined.md

Be thorough. Produce your best work. You MUST write the file before finishing.
```

7. [ ] **WAIT** for the sub-agent to complete
8. [ ] **VERIFY** docs/design-reviews/[name]/refined.md exists before proceeding

### Phase 3: Critique

9. [ ] Spawn a **general-purpose** sub-agent with write permissions
10. [ ] Use this exact prompt (replace [name]):

```
You are the Critique. Challenge this design ruthlessly.

Read the refined design at: docs/design-reviews/[name]/refined.md

Skills to apply:
- separation-of-concerns
- tactical-ddd

Your job:
1. Read the refined.md file first
2. Find violations of design principles
3. Question assumptions
4. Identify ambiguities and gaps
5. Group findings by severity: CRITICAL, HIGH, MEDIUM, LOW
6. IMPORTANT: Write your critique to: docs/design-reviews/[name]/critique.md

Be ultra-critical. Include uncertain findings. False positives are better than missed issues.
You MUST write the file before finishing.
```

11. [ ] **WAIT** for the sub-agent to complete
12. [ ] **VERIFY** docs/design-reviews/[name]/critique.md exists before proceeding

### Phase 4: Facilitated Discussion

13. [ ] Tell user: "Design review complete. Files are at docs/design-reviews/[name]/"
14. [ ] Ask user to read the documents
15. [ ] When user is ready, walk through each critique finding one by one
16. [ ] For each finding: present it, discuss validity and context with user
17. [ ] Record user's decision and rationale to decisions.md
18. [ ] Continue until all findings are addressed
19. [ ] Produce final implementation plan: implementation-plan.md

## Main Agent Behavior

**You are the orchestrator.** You coordinate sub-agents and facilitate discussion. You do NOT summarize or filter sub-agent output.

**You do NOT:**
- Run phases in parallel
- Summarize sub-agent output
- Filter or interpret findings
- Add your own analysis to sub-agent work
- Write files that sub-agents should write

## Output Structure

```
docs/design-reviews/
└── [review-name]/
    ├── plan.md                 ← Architect writes this
    ├── refined.md              ← Refiner writes this
    ├── critique.md             ← Critique writes this
    ├── decisions.md            ← Main agent writes this
    └── implementation-plan.md  ← Main agent writes this
```
