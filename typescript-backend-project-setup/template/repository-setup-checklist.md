# Repository Setup Checklist

Track setup progress. Resume anytime by reviewing unchecked items.

## NX Workspace Creation
- [ ] `npx create-nx-workspace@latest` (creates base structure)
- [ ] `nx add @nx/vitest` (adds testing plugin)
- [ ] `nx add @nx/eslint` (adds linting plugin)

## Dependencies
- [ ] `pnpm add -D vitest @vitest/coverage-v8`
- [ ] `pnpm add -D husky lint-staged`

## Claude Code Integration
- [ ] CLAUDE.md (copied from template, placeholders replaced)
- [ ] AGENTS.md (copied from template)
- [ ] .claude/settings.json (copied from template)
- [ ] .claude/hooks/block-dangerous-commands.sh (copied, made executable)

## Documentation
- [ ] docs/conventions/codebase-structure.md
- [ ] docs/conventions/task-workflow.md
- [ ] docs/conventions/testing.md (content copied from writing-tests skill)
- [ ] docs/conventions/software-design.md (content copied from software-design-principles skill)
- [ ] docs/architecture/overview.md
- [ ] docs/architecture/domain-terminology/contextive/definitions.glossary.yml
- [ ] docs/project/project-overview.md

## Config Patches
- [ ] nx.json: Add lint dependency to build/test targets
- [ ] tsconfig.base.json: Add strict TypeScript flags
- [ ] eslint.config.mjs: Add strict rules (no-comments, naming conventions)

## Git Hooks
- [ ] `npx husky init`
- [ ] .husky/pre-commit (copied from template)

## Verification
- [ ] `nx report` (shows NX version and plugins)
- [ ] `nx graph` (renders workspace structure)
- [ ] `git commit` (pre-commit hook runs)

## Content (Optional - Interview User)
- [ ] Architecture diagram and overview
- [ ] Domain terminology definitions
- [ ] Project vision and phases
