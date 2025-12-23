# {{WORKSPACE_NAME}}

{{WORKSPACE_DESCRIPTION}}

> 🚨 **FAIL FAST:** If a command fails or doesn't work as expected, STOP and discuss with the user. Do not improvise or try workarounds. Fix the skill/docs so the problem doesn't happen again.

Read `docs/project/project-overview.md` then check `docs/project/prd/active/` for the current PRD.

## Monorepo Structure

```
apps/       - Deployable applications (not published)
packages/   - Shared libraries (publishable to npm)
```

Current packages:
- (none yet - use NX generators to add)

Key documents:
- `docs/project/prd/active/` - Current PRDs
- `docs/architecture/overview.md` - System design
- `docs/architecture/domain-terminology/contextive/definitions.glossary.yml`
- `docs/architecture/adr/` - Decision records

All code must follow `docs/conventions/codebase-structure.md`.

Use domain terminology from the contextive definitions. Do not invent new terms or use technical jargon when domain terminology exists.

When discussing domain concepts, clarify terminology with the user. Add new terms to `docs/architecture/domain-terminology/contextive/definitions.glossary.yml`.

## Commands

### Build & Test

```bash
# All projects
nx run-many -t build
nx run-many -t test
nx run-many -t lint

# Specific project
nx build [project-name]
nx test [project-name]
nx lint [project-name]

# Affected only (CI optimization)
nx affected -t build
nx affected -t test
```

### Single Test File

```bash
nx test [project-name] -- --testNamePattern "should validate"
```

### Verify (Full Gate)

```bash
nx run-many -t lint,typecheck,test --coverage
```

### Dependency Graph

```bash
nx graph
```

### Adding New Projects

**Before using a generator, ensure the plugin is installed:**

```bash
# Check available plugins
nx list

# Install plugins as needed
nx add @nx/node      # For Node.js applications
nx add @nx/js        # For TypeScript libraries (usually pre-installed)
```

🚨 **If a generator fails with "Unable to resolve"**: The plugin isn't installed. Run `nx add @nx/[plugin-name]` first. Do NOT improvise or try workarounds.

**Creating projects:**

```bash
# Add backend application (requires @nx/node)
# Note: @nx/node only supports --unitTestRunner=jest|none (NOT vitest)
nx g @nx/node:application apps/[app-name] --unitTestRunner=none

# Add shared library (publishable)
# Note: @nx/js supports --unitTestRunner=vitest
nx g @nx/js:library packages/[pkg-name] --publishable --importPath=@{{WORKSPACE_NAME}}/[pkg-name] --unitTestRunner=vitest
```

After generating a new project:
1. Update the project's package.json with correct name: `@{{WORKSPACE_NAME}}/[project-name]`
2. Create the 3-file tsconfig structure (tsconfig.json, tsconfig.lib.json, tsconfig.spec.json)
3. Add vitest.config.ts if tests are needed
4. If importing from another project, add `"@{{WORKSPACE_NAME}}/[pkg-name]": "workspace:*"` to dependencies
5. Run `nx sync` to update TypeScript project references
6. Update this CLAUDE.md "Current packages" section

## Task Workflow

Follow `docs/conventions/task-workflow.md` for all task management. Whenever you are told to "start task", "update task", "complete task" etc you MUST consult the workflow and follow the appropriate step.

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

## NX Guidelines

- **Use generators** - Don't manually create project folders. Use `nx g @nx/js:library` or `nx g @nx/node:application`.
- **Run `nx sync`** - After modifying tsconfig references or adding dependencies between projects.
- **Debugging stale cache** - If something seems stale, run `nx reset` to clear the cache.

## General Guidelines

- **Fail fast** - If a command fails or something doesn't work, STOP and discuss with the user. Do not improvise or try workarounds. Fix the underlying issue (or update the skill/docs) so it doesn't happen again.
- **Do not modify root configuration files** (eslint.config.mjs, tsconfig.base.json, nx.json). If you believe a change is genuinely necessary, provide the suggested changes and ask the user.
- **Do not use `--no-verify`, `--force`, or `--hard` flags.** These are blocked by hooks and will fail. All commits must pass the `verify` gate.
- **Use NX commands** for all build, test, and lint operations. Do not run npm/pnpm directly in project folders.
- **Cross-project imports** use package names (e.g., `import { X } from '@{{WORKSPACE_NAME}}/[pkg-name]'`), not relative paths.
- **Adding dependencies between projects** requires adding `"@{{WORKSPACE_NAME}}/[pkg-name]": "workspace:*"` to the consuming project's package.json.
