---
description: Three-phase design review (Architect → Refine → Critique)
---

# Architect-Refine-Critique

Chain three subagents sequentially from the main conversation.

## Usage

`/arc [name] [target]`

## Execution

Use the architect subagent to create the initial design for [target] with name=[name],
then use the refiner subagent to improve the design with name=[name],
then use the critique subagent to challenge the design with name=[name].

After all three complete, tell the user: "Run `/arc-review [name]` to discuss findings."

Do not analyze. Do not summarize. Do not add value. Just chain and hand off.
