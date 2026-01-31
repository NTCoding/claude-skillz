---
name: arc-prd
description: "Architecture review for a PRD. Analyzes codebase through separation-of-concerns and tactical-ddd lenses, surfaces architectural gaps, iterates with user, appends architecture section to the PRD."
---

# PRD Architecture Review

Read the PRD at `$ARGUMENTS`. Verify its status is "Awaiting Architecture Review".

You are adding the architecture section that makes this PRD implementable. The PRD defines *what* to build — you define *how to structure it* at the package, feature, and domain model level. Not implementation details. Not function signatures. Structural decisions and domain modeling only.

## Skills

Use skill `development-skills:separation-of-concerns` and skill `development-skills:tactical-ddd`. Apply both throughout all phases.

## Phase 1: Research

1. Read the PRD
2. Read project conventions — search for: `docs/architecture/`, `ARCHITECTURE.md`, ADRs, `package.json` files, existing folder structure at the project root
3. Understand the current codebase structure through Glob and Grep

## Phase 2: Analysis

Use both skills as **analytical lenses** — not just checklists to fill in, but tools to reveal what the PRD leaves architecturally ambiguous.

For each item in the architecture checklist below, do one of:
- **Propose a decision** — when the PRD + codebase provide enough signal. State the rationale grounded in a specific skill principle.
- **Surface a question** — when the skills reveal a gap, tension, or ambiguity the PRD didn't address. Include proposed options.

Present your analysis as:

```
## Proposed Decisions
[Concrete proposals with rationale citing specific skill principles]

## Open Questions
[Gaps/tensions discovered through skill analysis, each with proposed options]
```

### How to surface good questions

Questions should be grounded in specific skill principles and reference the PRD concretely:

- "PRD describes X as part of feature Y, but separation-of-concerns principle 2 says this is shared if multiple features use it. Does Z also use this? → determines features/ vs platform/domain/"
- "This introduces [concept] but doesn't define invariants. Tactical-DDD principle 7: what must always be true when [state change] happens?"
- "PRD mentions [interface] but doesn't say whether it's a domain concept or infrastructure. This affects where it lives."
- "The PRD has [component A] calling [component B] — is B a use case (menu test) or internal machinery?"
- "PRD introduces [term] without defining it. Is this a new domain concept? An existing one being extended? A generic utility?"

Don't ask questions you can answer from the codebase. Research first.

## Phase 3: Iterate

Discuss with user until all questions are resolved and decisions are agreed. Show, don't tell — use ASCII diagrams, folder structure sketches, before/after comparisons.

## Phase 4: Write

Append the `## Architecture` section to the PRD file (replacing the placeholder). Use diagrams where they add clarity. Update the PRD status to "Approved".

### Annotate deliverables

After writing the architecture section, go back through the PRD's milestone deliverables and add architecture references. Under each deliverable that is affected by an architecture decision, add:

```
Architecture: see §9.X ([decision summary])
```

This creates an explicit link from each deliverable to the architecture decisions that constrain it. Task creation will use these references to inject architecture context into each task.

Examples:
- Under a deliverable about a new extraction engine: `Architecture: see §9.1 (new riviere-connection-detection package), §9.3 (call graph as platform/domain)`
- Under a deliverable introducing an aggregate: `Architecture: see §9.5 (Builder aggregate invariants), §9.6 (upsert merge semantics)`

Every deliverable should have at least one architecture reference. If a deliverable has none, either the architecture section is incomplete or the deliverable is purely documentation.

## Architecture Checklist

The architecture section must answer all of these:

### Structural decisions (from separation-of-concerns)

- Which packages are modified vs created?
- What new features (verticals) are introduced?
- What shared capabilities (horizontals) are needed?
- For each feature: which layers apply? (entrypoint / commands / queries / domain)
- What goes in platform/domain vs platform/infra?
- What external clients are introduced or modified?
- Dependency direction between packages (ASCII diagram)

### Domain model (from tactical-ddd)

- What aggregates/entities are introduced or changed?
- What are the key invariants?
- What use cases exist? (apply the menu test)
- What value objects emerge?
- What state transitions matter?
- What domain language/terminology is introduced?

### Integration

- Key interfaces/contracts between new and existing code

### Flexibility markers

Mark each decision as:
- **Firm** — structural, hard to change later, get it right now
- **Flexible** — can iterate during implementation, direction is set but details may shift

## Rules

1. **Do not define implementation details** — no function signatures, no class hierarchies, no algorithms. Structure and domain model only.
2. **Do not duplicate the PRD** — reference it, don't repeat it.
3. **Do not prescribe the full solution** — leave room for implementation to iterate within the structural boundaries you define.
4. **Ground every decision in a skill principle** — if you can't cite why, it's opinion not architecture.
5. **Show, don't tell** — diagrams, folder trees, and concrete examples over prose.
