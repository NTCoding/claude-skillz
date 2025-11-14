# Lightweight Implementation Analysis Protocol

A Claude Code skill that enforces quick verification before implementation - **just enough to guide TDD, no more**.

## What It Does

Before Claude creates any implementation plan or writes code, it:
1. **Traces the flow** - Entry point → file:line where error occurs
2. **Creates simple diagram** - Class.method() flow with relevant data
3. **Verifies with you** - "Is this correct?"


## When to Use

Activate this skill when working on:
- Bug fixes
- Feature implementations
- TDD cycles
- Refactoring


## Example Flow

**Before (without this skill):**
```
You: "Fix the email validation error"
Claude: "I'll update the validation to use safeParse..."
*Creates plan based on assumptions*
*Implements wrong fix*
```

**After (with this skill):**
```
You: "Fix the email validation error"
Claude: "Let me trace where this occurs..."

Event: user.email.updated
  ↓ (email: "invalid@")
UpdateUserEmailHandler.execute() [line 281]
  ↓
EmailValidator.parse() ← 💥 Throws here

"Is this correct?"
You: "Yes"
Claude: "Now I'll implement the fix..."
*Implements correct fix*
```

## Philosophy

**Lightweight = Fast + Accurate**
- Not heavyweight analysis
- Not detailed documentation
- Just enough to know what to test
- Prevents wasted effort from guessing
