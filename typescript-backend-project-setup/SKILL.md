---
name: NX Monorepo TypeScript Backend Project Setup
description: "Sets up NX monorepo for TypeScript backend projects optimized for AI-assisted development. Delegates to NX commands where possible, patches configs as last resort. Triggers on: 'set up typescript backend project', 'create backend project', 'initialize typescript backend', 'create monorepo', or when working in an empty project folder."
version: 3.0.9
---

# NX Monorepo TypeScript Backend Project Setup

> 🚨 **DO NOT USE PLAN MODE.** This skill IS the plan. Follow the steps exactly as written.

> 🚨 **FAIL FAST:** If ANYTHING unexpected happens or you need to do something NOT in this skill, STOP and discuss with the user. Do not improvise or add extra steps. Update this skill instead.

> ⚠️ **Check NX docs for latest conventions:** https://nx.dev/docs/getting-started/start-new-project
> NX evolves quickly. Verify these instructions against current NX best practices before use.

Set up NX monorepo for TypeScript backend projects with maximum type safety, strict linting, 100% test coverage, and AI-optimized project structure.

## Contents

1. [Phase 1: Define Project Context](#phase-1-define-project-context) - Gather requirements
2. [Phase 2: Create NX Workspace](#phase-2-create-nx-workspace) - Run NX generator
3. [Phase 3: Install Dependencies](#phase-3-install-dependencies) - Add plugins and tools
4. [Phase 4: Create Initial Projects](#phase-4-create-initial-projects) - Generate packages and apps
5. [Phase 5: Add Claude Code Integration](#phase-5-add-claude-code-integration) - Copy AI guardrails and docs
6. [Phase 6: Enforce Strict Standards](#phase-6-enforce-strict-standards) - Patch configs
7. [Phase 7: Establish Coding Conventions](#phase-7-establish-coding-conventions) - Add skill content
8. [Phase 8: Activate Git Hooks](#phase-8-activate-git-hooks) - Enable pre-commit checks
9. [Phase 9: Verify Setup](#phase-9-verify-setup) - Confirm everything works
10. [Phase 10: Document Architecture](#phase-10-document-architecture-optional) - Optional interview

## When This Activates

- User requests: "set up typescript backend project", "create backend project", "initialize typescript backend", "create monorepo"
- Working in an empty or near-empty project folder
- User asks for backend project scaffolding or boilerplate

## Template Location

This skill uses a template located at: `typescript-backend-project-setup/template/`

The template contains only files NX cannot create: Claude Code integration, documentation structure, and git hooks.

Before starting, ask the user for the full path to the claude-skillz repository so you can locate the template.

## Setup Procedure

### Phase 1: Define Project Context

Ask the user:
1. **Workspace name** - What should this monorepo be called? (lowercase, hyphens ok)
2. **Domain description** - Brief description of what this project does
3. **Claude-skillz path** - What is the full path to the claude-skillz repository on your system?
4. **Target directory** - Where should the project be created? (defaults to current directory)
5. **Initial packages** - List any publishable packages to create (e.g., "query, builder, cli")
6. **Initial apps** - List any applications to create (e.g., "api, docs")

### Phase 2: Create NX Workspace

**Priority: Commands > Installs > Patch files (last resort)**

Run the NX workspace generator:

```bash
npx create-nx-workspace@latest [workspace-name] --preset=ts --pm=pnpm --nxCloud=skip --interactive=false
```

This creates:
- `nx.json` - NX configuration
- `tsconfig.base.json` - Base TypeScript config
- `package.json` - Root package with NX scripts
- `pnpm-workspace.yaml` - Workspace definition
- `.gitignore` - Standard ignores

**Patch .gitignore - Add test-output:**

Add `test-output` to `.gitignore` (vitest coverage output):
```
test-output
```

**Checkpoint:** Verify `nx report` shows NX version.

### Phase 3: Install Dependencies

Add testing and code quality tools:

```bash
# Add NX plugins
nx add @nx/vitest
nx add @nx/eslint
nx add @nx/node  # Required for creating applications

# Install testing dependencies
pnpm add -D vitest @vitest/coverage-v8

# Install ESLint dependencies (required for strict config)
pnpm add -D typescript-eslint @nx/eslint-plugin eslint-plugin-functional

# Install git hooks
pnpm add -D husky lint-staged
```

Adding `@nx/vitest`. Provides integrated test runner with coverage reporting.

Adding `@nx/eslint`. Provides consistent linting across all projects.

Adding `@nx/node`. Required for creating Node.js applications.

Adding `husky` and `lint-staged`. Provides pre-commit verification gate.

### Phase 4: Create Initial Projects

**If user specified packages in Phase 1, create them:**

```bash
# For each package (publishable library with vitest)
nx g @nx/js:library packages/[pkg-name] --publishable --importPath=@[workspace-name]/[pkg-name] --bundler=tsc --unitTestRunner=vitest
```

**If user specified apps in Phase 1, create them:**

```bash
# For each app (node application - vitest NOT supported, use none)
nx g @nx/node:application apps/[app-name] --unitTestRunner=none
```

🚨 **IMPORTANT:**
- `@nx/js:library` supports `--unitTestRunner=vitest`
- `@nx/node:application` only supports `--unitTestRunner=jest|none` (NOT vitest)

After creating projects, run `nx sync` to update TypeScript project references.

### Phase 5: Add Claude Code Integration

Copy template files (only what NX can't create):

**Claude Code Integration:**

```bash
cp -r [claude-skillz-path]/typescript-backend-project-setup/template/CLAUDE.md [target-directory]/
cp -r [claude-skillz-path]/typescript-backend-project-setup/template/AGENTS.md [target-directory]/
cp -r [claude-skillz-path]/typescript-backend-project-setup/template/.claude [target-directory]/
```

Adding `CLAUDE.md`. Provides AI context, commands, and project conventions.

Adding `.claude/settings.json`. Provides permission guardrails and hook configuration.

Adding `.claude/hooks/block-dangerous-commands.sh`. Prevents destructive git operations (--force, --hard, --no-verify).

**Documentation Structure:**

```bash
cp -r [claude-skillz-path]/typescript-backend-project-setup/template/docs [target-directory]/
cp [claude-skillz-path]/typescript-backend-project-setup/template/repository-setup-checklist.md [target-directory]/
```

Adding `docs/conventions/`. Provides coding standards and workflow documentation.

Adding `docs/architecture/`. Provides system design and domain terminology templates.

Adding `docs/project/`. Provides project vision and planning templates.

**Git Hooks:**

```bash
cp -r [claude-skillz-path]/typescript-backend-project-setup/template/.husky [target-directory]/
```

Adding `.husky/pre-commit`. Provides pre-commit verification (lint, typecheck, test).

**Custom ESLint Rules:**

```bash
cp -r [claude-skillz-path]/typescript-backend-project-setup/template/.eslint-rules [target-directory]/
```

Adding `.eslint-rules/no-generic-names.js`. Custom rule that bans generic names (utils, helpers, service, manager) in filenames and class names.

**Make scripts executable:**

```bash
chmod +x [target-directory]/.claude/hooks/block-dangerous-commands.sh
```

**Replace placeholders in copied files:**

| Placeholder | Replace With |
|-------------|--------------|
| `{{WORKSPACE_NAME}}` | User's workspace name |
| `{{WORKSPACE_DESCRIPTION}}` | User's domain description |
| `{{DOMAIN_NAME}}` | User's workspace name (used as context name in glossary) |
| `{{DOMAIN_DESCRIPTION}}` | User's domain description |

Files with placeholders:
- `CLAUDE.md`
- `docs/conventions/codebase-structure.md`
- `docs/architecture/domain-terminology/contextive/definitions.glossary.yml`
- `docs/project/project-overview.md`

### Phase 6: Enforce Strict Standards

These patches add our strict standards to NX-generated configs.

**Patch nx.json - Add lint dependency to build/test:**

Add to `targetDefaults.build.dependsOn`:
```json
"dependsOn": ["lint", "^build"]
```

Add to `targetDefaults.test`:
```json
"dependsOn": ["lint"]
```

This ensures AI gets immediate lint feedback on any change.

**Patch tsconfig.base.json - Add strict TypeScript flags:**

Add these to `compilerOptions`:
```json
{
  "noUncheckedIndexedAccess": true,
  "noImplicitOverride": true,
  "noFallthroughCasesInSwitch": true,
  "noPropertyAccessFromIndexSignature": true,
  "noUnusedLocals": true,
  "noUnusedParameters": true,
  "noImplicitReturns": true,
  "exactOptionalPropertyTypes": true,
  "verbatimModuleSyntax": true
}
```

**Patch eslint.config.mjs - Add strict rules:**

**IMPORTANT:** Completely overwrite `eslint.config.mjs` with this exact content (do not merge, do not patch - replace the entire file):

```javascript
import nx from '@nx/eslint-plugin';
import tseslint from 'typescript-eslint';
import noGenericNames from './.eslint-rules/no-generic-names.js';

const customRules = {
  plugins: {
    custom: {
      rules: {
        'no-generic-names': noGenericNames,
      },
    },
  },
};

export default tseslint.config(
  ...nx.configs['flat/base'],
  ...nx.configs['flat/typescript'],
  ...nx.configs['flat/javascript'],
  {
    ignores: ['**/dist', '**/out-tsc', '**/node_modules', '**/.nx', '*.config.ts', '*.config.mjs', '*.config.js', 'vitest.workspace.ts'],
  },
  customRules,
  {
    files: ['**/*.ts', '**/*.tsx'],
    rules: {
      // Custom rule: no generic names
      'custom/no-generic-names': 'error',

      // No comments - forces self-documenting code
      'no-warning-comments': 'off',
      'multiline-comment-style': 'off',
      'capitalized-comments': 'off',
      'no-inline-comments': 'error',
      'spaced-comment': 'off',

      // Ban let - use const only
      'no-restricted-syntax': [
        'error',
        {
          selector: 'VariableDeclaration[kind="let"]',
          message: 'Use const. Avoid mutation.',
        },
      ],
      'prefer-const': 'error',
      'no-var': 'error',

      // No any types
      '@typescript-eslint/no-explicit-any': 'error',
      '@typescript-eslint/no-unsafe-assignment': 'error',
      '@typescript-eslint/no-unsafe-member-access': 'error',
      '@typescript-eslint/no-unsafe-call': 'error',
      '@typescript-eslint/no-unsafe-return': 'error',

      // No type assertions - fix the types instead
      '@typescript-eslint/consistent-type-assertions': ['error', { assertionStyle: 'never' }],

      // Ban generic folder imports (not lib - that's NX convention)
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            { group: ['*/utils/*', '*/utils'], message: 'No utils folders. Use domain-specific names.' },
            { group: ['*/helpers/*', '*/helpers'], message: 'No helpers folders. Use domain-specific names.' },
            { group: ['*/common/*', '*/common'], message: 'No common folders. Use domain-specific names.' },
            { group: ['*/shared/*', '*/shared'], message: 'No shared folders. Use domain-specific names.' },
            { group: ['*/core/*', '*/core'], message: 'No core folders. Use domain-specific names.' },
          ],
        },
      ],

      // Complexity limits
      'max-lines': ['error', { max: 400, skipBlankLines: true, skipComments: true }],
      'max-depth': ['error', 3],
      'complexity': ['error', 12],

      // Naming conventions
      '@typescript-eslint/naming-convention': [
        'error',
        {
          selector: 'variable',
          format: ['camelCase'],
        },
        {
          selector: 'variable',
          modifiers: ['const'],
          format: ['camelCase', 'UPPER_CASE'],
        },
        {
          selector: 'function',
          format: ['camelCase'],
        },
        {
          selector: 'parameter',
          format: ['camelCase'],
          leadingUnderscore: 'allow',
        },
        {
          selector: 'typeLike',
          format: ['PascalCase'],
        },
        {
          selector: 'enumMember',
          format: ['PascalCase'],
        },
        {
          selector: 'objectLiteralProperty',
          format: null,
        },
      ],
    },
  },
  {
    files: ['**/*.ts', '**/*.tsx'],
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
  }
);
```

This enforces:
- **No generic names** - Custom rule bans utils, helpers, service, manager, etc. in filenames and class names
- **No `let`** - Only `const` allowed via no-restricted-syntax
- **No type assertions** - Fix the types, don't cast
- **No generic folders** - Bans imports from utils/, helpers/, common/, shared/, core/
- **Complexity limits** - Max 400 lines, max depth 3, cyclomatic complexity 12
- **No inline comments** - Forces self-documenting code
- **No `any` types** - Anywhere
- **Naming conventions** - camelCase for variables/functions, PascalCase for types

**Patch package.json - Add scripts and lint-staged:**

Add these to the root package.json:
```json
{
  "scripts": {
    "build": "nx run-many -t build",
    "test": "nx run-many -t test",
    "lint": "nx run-many -t lint",
    "typecheck": "nx run-many -t typecheck",
    "verify": "nx run-many -t lint,typecheck && nx run-many -t test --coverage",
    "prepare": "husky"
  },
  "lint-staged": {
    "*.ts": ["eslint --fix"]
  }
}
```

**Patch vitest.config.mts files - Add 100% coverage thresholds:**

For EACH project created in Phase 4 that has a `vitest.config.mts`, add thresholds to the coverage block:

```typescript
coverage: {
  reportsDirectory: './test-output/vitest/coverage',
  provider: 'v8' as const,
  thresholds: {
    lines: 100,
    statements: 100,
    functions: 100,
    branches: 100,
  },
},
```

This enforces 100% test coverage - tests will FAIL if coverage drops below 100%.

### Phase 7: Establish Coding Conventions

Copy content from claude-skillz skills to the docs:

**Testing conventions:**
- Read: `[claude-skillz-path]/writing-tests/SKILL.md`
- Write to: `docs/conventions/testing.md`

Adding `docs/conventions/testing.md`. Provides test naming, assertion patterns, and edge case checklists.

**Software design conventions:**
- Read: `[claude-skillz-path]/software-design-principles/SKILL.md`
- Write to: `docs/conventions/software-design.md`

Adding `docs/conventions/software-design.md`. Provides object calisthenics, fail-fast, and dependency inversion patterns.

### Phase 8: Activate Git Hooks

Initialize husky, then overwrite the default pre-commit with our version:

```bash
cd [target-directory]
npx husky init
# husky init creates a default pre-commit - overwrite it with ours:
cp [claude-skillz-path]/typescript-backend-project-setup/template/.husky/pre-commit .husky/pre-commit
```

### Phase 9: Verify Setup

```bash
# Check NX is working
nx report

# View empty workspace
nx graph
```

Review the `repository-setup-checklist.md` and ensure all items are checked.

**Checkpoint:** All verification commands pass. Ready for first commit.

### Phase 10: Document Architecture (Optional)

Offer to interview the user to fill in placeholder content:

**Architecture Overview** (`docs/architecture/overview.md`):
- "What systems does this interact with?"
- "Who are the primary users?"
- "What are the main technical components?"

**Domain Terminology** (`docs/architecture/domain-terminology/contextive/definitions.glossary.yml`):
- "What are the key terms in this domain?"
- "How would you define [term] to a new team member?"

**Project Overview** (`docs/project/project-overview.md`):
- "What problem are you solving?"
- "Who are the users and what do they need?"
- "What are your non-negotiable principles?"
- "What are the project phases?"

---

## Summary

This skill creates an NX monorepo using a command-first approach:

1. `create-nx-workspace` for foundation
2. `nx add` for plugins
3. `pnpm add` for dependencies
4. Copy template files (only what NX can't create)
5. Patch configs (last resort)
6. Verify setup

The result provides:
- **Maximum type safety** - strict tsconfig, TypeScript project references
- **Strict linting** - no comments, naming conventions, no mutation
- **100% test coverage** - with sensible excludes
- **NX orchestration** - caching, affected commands, dependency graph
- **AI guardrails** - protected configs, blocked dangerous commands
- **Scalable structure** - apps and packages pattern with workspace:* dependencies

For adding projects after setup, see `docs/conventions/codebase-structure.md`.

---

## Verification Mode

Trigger: "verify typescript setup", "check project setup", "audit monorepo config"

Use this to verify an existing repo has all required configurations.

### Step 1: Discover all projects

```bash
find . -name "package.json" -not -path "*/node_modules/*" -not -path "*/.nx/*"
```

### Step 2: ESLint Config Verification

Read `eslint.config.mjs` and verify it contains:
- [ ] Import of `.eslint-rules/no-generic-names.js`
- [ ] Rule `custom/no-generic-names: 'error'`
- [ ] Rule `no-restricted-syntax` with `VariableDeclaration[kind="let"]` selector
- [ ] Rule `@typescript-eslint/consistent-type-assertions` with `assertionStyle: 'never'`
- [ ] Rule `no-restricted-imports` with patterns for utils, helpers, common, shared, core
- [ ] Rules `max-lines: 400`, `max-depth: 3`, `complexity: 12`

**If any missing:** List what's missing and offer to fix.

### Step 3: Vitest Config Verification

For EACH project discovered in Step 1:
1. Check if `vitest.config.mts` exists in that project directory
2. If exists, read it and verify `coverage.thresholds` contains:
   - `lines: 100`
   - `statements: 100`
   - `functions: 100`
   - `branches: 100`

**If any project missing thresholds:** List which projects are non-compliant and offer to fix.

### Step 4: Git Hooks Verification

- [ ] `.husky/pre-commit` contains `lint-staged` and `verify`
- [ ] `package.json` has `lint-staged` config

### Step 5: Gitignore Verification

- [ ] `.gitignore` contains `test-output` on its own line

### Step 6: Report

Output a summary:
```
✓ ESLint: All rules configured
✗ Vitest: 2/6 projects missing coverage thresholds
  - apps/eclair
  - apps/docs
✓ Git Hooks: Configured
✓ Gitignore: test-output ignored
```

**If failures:** Offer to fix all issues automatically.
