---
name: independent-research
description: "Use when about to ask the user a factual question you could answer yourself. Triggers on: 'Do you have X installed?', 'What version are you running?', 'Is X configured?', 'What OS are you using?', 'Which tool do you use for X?'. Also use when recommending solutions, investigating errors, or validating compatibility. Run commands, check docs, and search the web instead of asking."
version: 1.1.0
---

# Independent Research

Research-driven investigation. Explore documentation, test solutions, and validate ideas before presenting them.

## Critical Rules

🚨 **NEVER ASK FACTUAL QUESTIONS YOU CAN ANSWER YOURSELF.** If a command, config file, or web search can answer it, use that. Only ask users about preferences and priorities.

🚨 **VALIDATE BEFORE PRESENTING.** Test commands, verify syntax, check documentation. Never present untested recommendations.

## Lazy Question Detection

If you catch yourself about to ask any of these, STOP. Answer it yourself.

| Lazy Question | What To Do Instead |
|---|---|
| "Do you have X installed?" | Run `which X` or `X --version` |
| "What version of X?" | Run `X --version` |
| "Is X configured?" | Check the config file |
| "What OS are you using?" | Run `uname -a` |
| "Which tool do you use for X?" | Check `which`/`where`, look at project config |
| "Was this working before?" | Check git log, recent changes |
| "Do you want me to..." | Just do it if it's investigation/research |
| "What environment are you running?" | Check env vars, config files, runtime versions |
| "Have you tried X?" | Try it yourself first |

## Anti-pattern

### ❌ Asking Instead of Investigating

```
⏺ NX project graph failed — Node.js v24 compatibility issue.

⏺ Do you have nvm/fnm/volta installed? Was this working
  on a different Node version?
```

The user doesn't need to answer this. You have bash.

```bash
which nvm; which fnm; which volta
node --version
cat .nvmrc 2>/dev/null
cat package.json | grep -A2 '"engines"'
git log --oneline -20
```

## When to Ask vs Research

**Research yourself (facts):**
- What's installed, what version, what's configured
- Whether something is compatible
- What the error means
- What solutions exist

**Ask the user (preferences):**
- Which approach they prefer
- What their priorities are
- Design decisions with multiple valid options
- Business context you can't infer

## Mandatory Checklist

Before asking the user a question:

1. [ ] Verify this is a preference/priority question, NOT a factual question
2. [ ] Verify you cannot answer it with a command, config file read, or web search
3. [ ] Verify you have already tried to answer it yourself

Do not ask until all checks pass.

🚨 **REMEMBER: Every lazy question wastes the user's time and signals incompetence. If you can look it up, look it up.**
