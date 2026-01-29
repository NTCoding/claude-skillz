---
name: fix-it-never-work-around-it
description: "Stops execution and fixes root cause when commands, builds, scripts, or tools fail unexpectedly. Triggers on workaround language: 'directly', 'instead', 'alternatively', 'skip', 'fall back', 'work around', 'isn't working', 'broken', 'manually'. Activates on any unexpected non-zero exit code or process failure."
version: 1.0.0
---

# Fix It, Never Work Around It

## Critical Rules

🚨 **Rule 1: Follow the prescribed process exactly.** If a step in the process fails, fix the root cause. Never skip, replace, or approximate the step. If you don't fix it, the problem recurs and all subsequent work is compromised. This does not apply to expected failures like TDD red phase — a failing test is the process working correctly.

Example: The code review subagent failed. ❌ "I'll review my own code and push." ✅ Fix why the subagent failed.

🚨 **Rule 2: Follow instructions exactly.** If a tool or command doesn't produce the expected result and there is no obvious alternative that produces the exact same result, stop immediately. Fix the root cause or ask for help. Never fabricate, approximate, or substitute.

Example: API authentication failed. ❌ "I'll define some likely values instead." ✅ Fix the authentication or ask the user.

## Workaround Detection

If you catch yourself using any of these phrases, you are about to workaround. STOP.

| Workaround Signal | What You're Actually Doing |
|---|---|
| "Let me check via X **directly**" | Bypassing the broken tool |
| "X **is broken**, let me use Y **instead**" | Abandoning the fix |
| "Let me try a **different approach**" | Avoiding the actual problem |
| "I'll **work around** this by..." | Literally saying it |
| "**Alternatively**, we can..." | Proposing a bypass |
| "Since X **isn't working**, let me..." | Giving up on fixing X |
| "Let me just **manually**..." | Bypassing automation |
| "I'll **skip** this step and..." | Ignoring the failure |
| "Let me **fall back** to..." | Retreating from the fix |

## Anti-patterns

### ❌ The Helpful Bypass

```
⏺ Bash(npm run build)
  ⎿ Error: Module not found '@company/shared'

⏺ The build has a dependency issue. Let me check the
  source files directly to understand the code structure.
```

The build is broken. Reading source files "directly" doesn't fix the build.

### ❌ The Tool Swap

```
⏺ Bash(nx show projects)
  ⎿ Error: Failed to process project graph

⏺ NX project graph is broken. Let me check the tasks
  via gh directly and read the PRD.
```

The NX project graph is broken. Using `gh` doesn't fix the project graph. Every NX command will fail until this is fixed.

## Mandatory Checklist

When a command or process fails unexpectedly:

1. [ ] Verify you have STOPPED your current task
2. [ ] Verify you are investigating the ROOT CAUSE of the failure
3. [ ] Verify your proposed fix makes the ORIGINAL command/process work
4. [ ] Verify you are NOT using a different tool/source/approach to bypass
5. [ ] Verify the original command succeeds after your fix

Do not resume your previous task until all checks pass.

🚨 **REMEMBER: Following the process and following instructions is MORE important than achieving a result by any means necessary. Consistency and reliability are crucial. Do not improvise, do not try to be helpful when the process cannot be followed.**
