# Codebase Structure

## Monorepo Layout

```
{{WORKSPACE_NAME}}/
├── apps/                    # Deployable applications
│   └── <app-name>/
│       ├── src/
│       │   ├── <feature>/
│       │   │   ├── domain/       # Domain model only
│       │   │   ├── application/  # Use cases
│       │   │   ├── infra/        # Database, external services
│       │   │   └── api/          # Controllers, endpoints
│       │   └── main.ts           # Application entry point
│       ├── package.json
│       ├── tsconfig.json
│       ├── tsconfig.lib.json
│       ├── tsconfig.spec.json
│       └── vitest.config.ts
├── packages/                # Shared libraries (publishable)
│   └── <pkg-name>/
│       ├── src/
│       │   └── index.ts          # Public exports
│       ├── package.json
│       ├── tsconfig.json
│       ├── tsconfig.lib.json
│       └── tsconfig.spec.json
├── docs/                    # Documentation
├── nx.json                  # NX configuration
├── tsconfig.base.json       # Shared TypeScript config
├── tsconfig.json            # Root references (for editor)
├── eslint.config.mjs        # Shared ESLint config
└── pnpm-workspace.yaml      # Workspace definition
```

## Principles

**Apps vs Packages.** Apps are deployable units (APIs, CLIs, workers). Packages are shared code published to npm and consumed by apps or other packages.

**Feature-first, layer-second.** Within each app, group by business capability, then by architectural layer.

**Dependencies point inward.** Domain depends on nothing. Application depends on domain. Infra depends on application and domain.

**No generic folders.** Every folder has domain meaning. Forbidden: `utils/`, `helpers/`, `common/`, `shared/`, `core/`, `lib/`.

**Cross-project imports use package names.** Import from `@{{WORKSPACE_NAME}}/[pkg-name]`, not relative paths like `../../packages/[pkg-name]`.

**Add workspace dependencies explicitly.** When importing from another project, add `"@{{WORKSPACE_NAME}}/[pkg-name]": "workspace:*"` to package.json.

## Layer Responsibilities

| Layer | Contains | Depends On |
|-------|----------|------------|
| domain | Entities, value objects, domain services, domain events | Nothing |
| application | Use cases, application services, DTOs | domain |
| infra | Repositories, external clients, framework adapters | domain, application |
| api | Controllers, routes, request/response mapping | application |

## Package Guidelines

**When to create a package:**
- Code is used by 2+ apps
- Code represents a distinct domain concept
- Code needs to be published to npm

**Package types:**
- **Domain packages:** Pure domain logic, no external dependencies
- **Feature packages:** Complete vertical slice (domain + application + infra)
- **Utility packages:** Technical utilities (logging, http-client wrappers)

**Naming:**
- Use domain language, not technical jargon
- `@{{WORKSPACE_NAME}}/order-processing` not `@{{WORKSPACE_NAME}}/order-utils`

## Per-Project Configuration

Each app/package needs a 3-file tsconfig structure:

**tsconfig.json** (editor entry point):
```json
{
  "extends": "../../tsconfig.base.json",
  "files": [],
  "references": [
    { "path": "./tsconfig.lib.json" },
    { "path": "./tsconfig.spec.json" }
  ]
}
```

**tsconfig.lib.json** (production build):
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src",
    "tsBuildInfoFile": "./dist/.tsbuildinfo"
  },
  "include": ["src/**/*.ts"],
  "exclude": ["src/**/*.test.ts"],
  "references": []
}
```

**tsconfig.spec.json** (tests):
```json
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist-test",
    "rootDir": "./src",
    "types": ["vitest/globals"]
  },
  "include": ["src/**/*.test.ts"],
  "references": [
    { "path": "./tsconfig.lib.json" }
  ]
}
```

The `references` arrays are automatically maintained by `nx sync`.

## Adding Projects

Use NX generators - don't create project folders manually.

**Add application:**
```bash
nx g @nx/node:application apps/[app-name]
```

**Add publishable package:**
```bash
nx g @nx/js:library packages/[pkg-name] --publishable --importPath=@{{WORKSPACE_NAME}}/[pkg-name]
```

After generation:
1. Verify/update package.json name: `@{{WORKSPACE_NAME}}/[project-name]`
2. Create 3-file tsconfig structure (see above)
3. Add vitest.config.ts with 100% coverage thresholds
4. Run `nx sync`
5. Update CLAUDE.md "Current packages" section

**Adding dependencies between projects:**
```json
{
  "dependencies": {
    "@{{WORKSPACE_NAME}}/[pkg-name]": "workspace:*"
  }
}
```
Then run `pnpm install` and `nx sync`.
