---
name: TypeScript Backend Project Setup
description: "Sets up TypeScript backend projects optimized for AI-assisted development. Triggers on: 'set up typescript backend project', 'create backend project', 'initialize typescript backend', or when working in an empty project folder."
version: 1.0.0
---

# TypeScript Backend Project Setup

Set up TypeScript backend projects with maximum type safety, strict linting, 100% test coverage, and AI-optimized project structure which includes tight guardrails + context engineering patterns.

## When This Activates

- User requests: "set up typescript backend project", "create backend project", "initialize typescript backend"
- Working in an empty or near-empty project folder
- User asks for backend project scaffolding or boilerplate

## Setup Procedure

### Phase 1: Project Context

Ask the user:
1. **Project name** - What should this project be called?
2. **Primary domain** - What problem domain does this serve? (e.g., "order management", "user authentication")

### Phase 2: Create Checklist

Create `repository-setup-checklist.md` in the project root to track progress:

```markdown
# Repository Setup Checklist

Track setup progress. Resume anytime by reviewing unchecked items.

## Configuration Files
- [ ] package.json
- [ ] tsconfig.json
- [ ] eslint.config.mjs
- [ ] vitest.config.ts
- [ ] .gitignore

## Claude Code Integration
- [ ] CLAUDE.md
- [ ] AGENTS.md
- [ ] .claude/settings.json
- [ ] .claude/hooks/block-dangerous-commands.sh

## Documentation
- [ ] docs/conventions/codebase-structure.md
- [ ] docs/conventions/task-workflow.md
- [ ] docs/conventions/testing.md
- [ ] docs/conventions/software-design.md
- [ ] docs/architecture/overview.md
- [ ] docs/architecture/domain-terminology/contextive/definitions.glossary.yml
- [ ] docs/project/project-overview.md

## Git Hooks
- [ ] husky + lint-staged

## Content (Optional - Interview User)
- [ ] Architecture diagram and overview
- [ ] Domain terminology definitions
- [ ] Project vision and phases
```

Check off items as you complete them.

### Phase 3: Configuration Files

Create each file, explaining the key decisions.

---

#### package.json

```json
{
  "name": "[project-name]",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "build": "tsc",
    "lint": "eslint .",
    "pretest": "npm run lint",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "typecheck": "tsc --noEmit",
    "knip": "knip",
    "verify": "npm run typecheck && npm run build && npm run knip && npm run test:coverage",
    "prepare": "husky"
  },
  "devDependencies": {},
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

Then install latest versions:

```bash
npm install -D typescript vitest @vitest/coverage-v8 eslint typescript-eslint @eslint/js eslint-plugin-no-comments prettier husky lint-staged knip
```

**Why this setup:**
- `verify` is the hard gate - typecheck, build, knip, and tests with coverage. Pre-commit hook runs this. AI cannot bypass it.
- `pretest` runs lint before every test run - so verify gets lint automatically via test:coverage
- `lint-staged` formats staged files at commit time
- `knip` catches unused exports and dependencies - runs as part of verify, not build (too slow for every build)
- No runtime dependencies - this is scaffolding; add domain-specific deps as needed

---

#### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true,
    "skipLibCheck": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

Optimized for maximum strictness as guardrails for AI. Every flag that catches bugs at compile time is enabled. If you can make it stricter, do so.

---

#### eslint.config.mjs

```javascript
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';
import noComments from 'eslint-plugin-no-comments';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      'no-comments': noComments,
    },
    rules: {
      // No comments - code should be self-documenting
      'no-comments/no-comments': 'error',

      // Complexity limits
      'max-lines': ['error', { max: 400, skipBlankLines: true, skipComments: true }],
      'max-depth': ['error', 3],
      'complexity': ['error', 12],
      'no-else-return': ['error', { allowElseIf: false }],

      // TypeScript strictness - no escape hatches
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unused-vars': 'error',
      '@typescript-eslint/consistent-type-assertions': ['error', { assertionStyle: 'never' }],

      // Forbidden patterns
      'no-restricted-syntax': [
        'error',
        {
          selector: 'VariableDeclaration[kind="let"]',
          message: 'Use const. Avoid mutation.',
        },
        {
          selector: 'TSAsExpression',
          message: 'Type assertions are not allowed. Fix the types instead.',
        },
        {
          selector: 'LogicalExpression[operator="||"][right.type!="Identifier"]',
          message: 'Avoid || for fallbacks. Use explicit conditionals or fail fast.',
        },
        {
          selector: 'ImportExpression',
          message: 'Dynamic imports are not allowed. Use static imports.',
        },
        {
          selector: 'CatchClause:not([param])',
          message: 'Catch clause must define a variable to capture the error.',
        },
      ],

      // No generic folder names in imports
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            { group: ['*/utils/*', '*/utils'], message: 'No utils folders. Use domain-specific names.' },
            { group: ['*/helpers/*', '*/helpers'], message: 'No helpers folders. Use domain-specific names.' },
            { group: ['*/common/*', '*/common'], message: 'No common folders. Use domain-specific names.' },
            { group: ['*/shared/*', '*/shared'], message: 'No shared folders. Use domain-specific names.' },
            { group: ['*/core/*', '*/core'], message: 'No core folders. Use domain-specific names.' },
            { group: ['*/lib/*', '*/lib'], message: 'No lib folders. Use domain-specific names.' },
          ],
        },
      ],
    },
  },
  {
    ignores: ['dist/', 'node_modules/', 'coverage/', '*.config.*'],
  }
);
```

Optimized for maximum type safety and guards against common AI anti-patterns.

---

#### vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['src/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['**/*.test.ts', '**/index.ts'],
      thresholds: {
        statements: 100,
        branches: 100,
        functions: 100,
        lines: 100,
      },
    },
  },
});
```

Strive for 100% coverage as the default. Reduce if needed or exclude specific files.

**Examples:**

Exclude generated files:
```typescript
exclude: ['**/*.test.ts', '**/index.ts', '**/generated/**']
```

Different thresholds for specific paths:
```typescript
thresholds: {
  'src/domain/**': { statements: 100, branches: 100, functions: 100, lines: 100 },
  'src/infra/**': { statements: 80, branches: 80, functions: 80, lines: 80 },
}
```

---

#### .gitignore

```
# Dependencies
node_modules/

# Build outputs
dist/
build/
*.tsbuildinfo

# Test & coverage
coverage/

# Environment
.env
.env.*
!.env.example

# Logs
*.log
npm-debug.log*

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db

# Caches
.eslintcache
.parcel-cache/
```

---

### Phase 4: Claude Code Integration

#### CLAUDE.md

````markdown
# [Project Name]

[Short description - what it does, the problem it solves]

Before starting any task, read `docs/project/project-overview.md`.

## Architecture

- **[Domain Name]** - [Brief description of what it does]
- **infra** - Shared adapters for [services]

Key documents:
- `docs/architecture/overview.md` - System design
- `docs/architecture/domain-terminology/contextive/definitions.glossary.yml`
- `docs/architecture/adr/` - Decision records

All code must follow `docs/conventions/codebase-structure.md`.

Use domain terminology from the contextive definitions. Do not invent new terms or use technical jargon when domain terminology exists.

When discussing domain concepts, clarify terminology with the user. Add new terms to `docs/architecture/domain-terminology/contextive/definitions.glossary.yml`.

## Commands

Build: `npm run build`
Test: `npm run test`
Lint: `npm run lint`
Verify (full gate): `npm run verify`

Run single test file:
```bash
npx vitest run src/[feature]/domain/[file].test.ts
```

Run tests matching pattern:
```bash
npx vitest run -t "should validate"
```

## Task Workflow

Follow `docs/conventions/task-workflow.md` for all task management.

## Testing

Follow `docs/conventions/testing.md`.

## Code Conventions

Follow `docs/conventions/software-design.md`.

## Security

- Never commit secrets, API keys, or credentials
- Use environment variables for sensitive configuration
- Do not log sensitive data (passwords, tokens, PII)
- Validate and sanitize all external input

## Tools

Installed from `ntcoding/claude-skillz`:

**Skills:**
- `writing-tests` - Test naming, assertions, edge case checklists
- `software-design-principles` - Object calisthenics, fail-fast, dependency inversion

**Plugins:**
- `task-check` - Validates task completion before marking done
- `automatic-code-review` - Reviews code on session stop

## General Guidelines

- **Do not modify eslint, tsconfig, or vitest configuration.** If you believe a change is genuinely necessary, provide the suggested changes and ask the user to modify these files.
- **Do not use `--no-verify`, `--force`, or `--hard` flags.** These are blocked by hooks and will fail. All commits must pass the `verify` gate.
````

**Why this structure:**
- **Standard sections** - Grouped by concern. Conventions can be built around this structure.
- **Disclosure pattern** - Makes implicit knowledge explicit. What to read, where conventions live, what tools exist, what's forbidden. No tribal knowledge.
- **References over duplication** - Points to convention docs. Single source of truth.

---

#### AGENTS.md

```markdown
# AGENTS.md

Read and follow all instructions in `CLAUDE.md`.
```

---

#### .claude/settings.json

```json
{
  "permissions": {
    "deny": [
      "Edit(./tsconfig.json)",
      "Edit(./eslint.config.mjs)",
      "Edit(./vitest.config.ts)",
      "Edit(./.claude/settings.json)",
      "Read(./.env)",
      "Read(./.env.*)"
    ]
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PROJECT_DIR/.claude/hooks/block-dangerous-commands.sh"
        }]
      }
    ]
  },
  "enabledPlugins": {
    "task-check@claude-skillz": true,
    "automatic-code-review@claude-skillz": true,
    "development-skills@claude-skillz": true
  }
}
```

**Why these settings:**
- `permissions.deny` - AI cannot modify the quality gate configs (tsconfig, eslint, vitest) or read secrets. These are hard blocks, not suggestions.
- `hooks.PreToolUse` - Inspects every bash command before execution. Blocks dangerous patterns. See hook script below.

---

#### .claude/hooks/block-dangerous-commands.sh

```bash
#!/bin/bash
read -r input
command=$(echo "$input" | jq -r '.tool_input.command // ""')

# Block commands that bypass safety checks
if echo "$command" | grep -qE '(--no-verify|--force|-f\s|--hard)'; then
  echo "Blocked: This command bypasses safety checks (--no-verify, --force, --hard)" >&2
  exit 2
fi

exit 0
```

Make it executable: `chmod +x .claude/hooks/block-dangerous-commands.sh`

**Why this hook:**
- `--no-verify` bypasses git hooks - AI could skip the verify gate
- `--force` / `-f` on push overwrites remote history
- `--hard` on reset destroys uncommitted work

Pre-commit runs `verify`. This hook ensures AI can't bypass it. Instructions in CLAUDE.md are requests. This hook is enforcement.

---

### Phase 5: Documentation Structure

Create the docs folder structure:

```
docs/
├── conventions/
│   ├── codebase-structure.md
│   ├── task-workflow.md
│   ├── testing.md
│   └── software-design.md
├── architecture/
│   ├── overview.md
│   ├── adr/
│   └── domain-terminology/
│       └── contextive/
│           └── definitions.glossary.yml
└── project/
    ├── project-overview.md
    └── PRD/
```

---

#### docs/conventions/codebase-structure.md

````markdown
# Codebase Structure

## Directory Layout

```
src/
├── <feature>/
│   ├── domain/       # Domain model only. No dependencies on other layers.
│   ├── application/  # Use cases. Orchestrates domain.
│   ├── infra/        # Database, external services, frameworks.
│   └── api/          # Controllers, endpoints (often separate project).
└── infra/            # Shared: client libs, adapters
```

## Principles

**Feature-first, layer-second.** Group by business capability, then by architectural layer.

**Dependencies point inward.** Domain depends on nothing. Application depends on domain. Infra depends on application and domain.

**No generic folders.** Every folder has domain meaning. Forbidden: `utils/`, `helpers/`, `common/`, `shared/`, `core/`, `lib/`.

**API layer is often separate.** For microservices, API may be its own project that imports domain/application.

## Layer Responsibilities

| Layer | Contains | Depends On |
|-------|----------|------------|
| domain | Entities, value objects, domain services, domain events | Nothing |
| application | Use cases, application services, DTOs | domain |
| infra | Repositories, external clients, framework adapters | domain, application |
| api | Controllers, routes, request/response mapping | application |

## Shared Infrastructure

`src/infra/` contains shared adapters used across features:
- Database clients
- Message queue adapters
- External API clients
- Logging, monitoring

These are technical infrastructure, not business logic.
````

---

#### docs/conventions/task-workflow.md

```markdown
# Task Workflow

Choose an approach that fits your project:

## Taskmaster AI

Full-featured task management with AI integration.
- Structured task breakdown and tracking
- Good for larger projects with multiple contributors

## Lightweight Task Workflow

https://github.com/NTCoding/claude-skillz/tree/main/lightweight-task-workflow

Simple markdown-based session state.
- Lower overhead for smaller projects
- Tasks tracked in `.claude/session.md`

## Beads

https://github.com/steveyegge/beads

Git-backed task tracking for AI agents.
- Tasks stored as JSONL in `.beads/`
- Dependency tracking with hash-based IDs
- Good for multi-agent or long-horizon work
```

---

#### docs/conventions/testing.md

Copy content from `writing-tests/SKILL.md` in the claude-skillz repository. This includes:
- Test naming conventions ("outcome when condition")
- Assertion best practices (specific values, match titles)
- Edge case checklists (numbers, strings, collections, dates, null/undefined, domain-specific)
- Bug clustering principles

---

#### docs/conventions/software-design.md

Copy content from `software-design-principles/SKILL.md` in the claude-skillz repository. This includes:
- Object calisthenics rules
- Fail-fast error handling
- Dependency inversion
- Feature envy detection
- Intention-revealing names

---

#### docs/architecture/overview.md

```markdown
# Architecture Overview

## C4 Context

[Draw a simple sketch diagram showing the system in its environment]

- What systems does this interact with?
- Who are the users?
- What are the main data flows?

## C4 Containers

[Draw a simple sketch diagram showing high-level technical building blocks]

- What are the main deployable units?
- How do they communicate?
- What technologies are used?

## External Dependencies

[List external services, APIs, third-party systems]

- Service name: purpose, criticality, owner

## Legacy Systems

[Any legacy systems this interacts with or replaces]

- What are we migrating from?
- What integration points exist?

## Known Tech Debt & Migrations

[Current tech debt, planned migrations, known issues]

- Issue: impact, planned resolution
```

---

#### docs/architecture/domain-terminology/contextive/definitions.glossary.yml

```yaml
contexts:
  - name: [DomainName]
    domainVisionStatement: [Purpose of this domain]
    terms:
      - name: [Term]
        definition: [Clear definition in domain language]
```

---

#### docs/project/project-overview.md

```markdown
# [Project Name] - Project Overview

## Vision

[One sentence - what success looks like]

## Problem Statement

[What problem are we solving? Why does it matter?]

## Users

[Who uses this? What are their needs and pain points?]

## Solution

[How do we solve the problem? High-level approach]

## Guiding Principles

[Non-negotiables, technical constraints, philosophy]

- Principle 1: explanation
- Principle 2: explanation

## Project Phases

### Phase 1: [Name]

**Goal:** [What we're trying to achieve]

**Deliverables:**
- Deliverable 1
- Deliverable 2

**Success Criteria:**
- How we know this phase succeeded

### Phase 2: [Name]

[Same structure]

## Success Metrics

[How we measure overall project success]

## Related Documentation

- [Link to PRDs, architecture docs, etc.]
```

---

### Phase 6: Git Hooks

#### .husky/pre-commit

```bash
npx lint-staged && npm run verify
```

Run these commands to set up husky:
```bash
npm install
npx husky init
echo "npx lint-staged && npm run verify" > .husky/pre-commit
```

---

### Phase 7: Verification

After creating all files:

1. Run `npm install`
2. Run `npm run lint` - should pass (no source files yet)
3. Run `npm run typecheck` - should pass
4. Run `npm run test` - should pass (no tests yet)
5. Verify all checklist items are checked

---

### Phase 8: Content Interview (Optional)

Offer to interview the user to build content for:

1. **Architecture Overview**
   - "What systems does this interact with?"
   - "Who are the primary users?"
   - "What are the main technical components?"
   - Draw C4 Context and Container diagrams based on answers

2. **Domain Terminology**
   - "What are the key terms in this domain?"
   - "How would you define [term] to a new team member?"
   - Add to contextive definitions.glossary.yml

3. **Project Overview**
   - "What problem are you solving?"
   - "Who are the users and what do they need?"
   - "What are your non-negotiable principles?"
   - "What are the project phases?"
   - Build project-overview.md from answers

---

## Summary

This skill creates a TypeScript backend project with:

- **Maximum type safety** - strict tsconfig, no escape hatches
- **Strict linting** - no comments, no generic folders, no mutation
- **100% test coverage** - enforced thresholds
- **AI-optimized structure** - CLAUDE.md, domain terminology, clear conventions
- **Protected configuration** - AI cannot modify quality rules
- **Progress tracking** - checklist for resuming setup

The goal: a codebase where AI gets immediate, specific feedback on every iteration, reducing bugs and accelerating development.
