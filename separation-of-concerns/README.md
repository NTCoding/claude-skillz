# Separation of Concerns — Automated Enforcement

The separation of concerns skill defines structural and dependency rules for organizing TypeScript projects into `features/`, `platform/`, and `shell/`. These rules can be automatically enforced using [dependency-cruiser](https://github.com/sverweij/dependency-cruiser).

## What It Enforces

dependency-cruiser statically analyzes your TypeScript imports and validates them against architectural rules. The example configuration below covers these checklist items from the skill:

| Rule | What it catches |
|------|----------------|
| `root-structure` | Files outside `features/`, `platform/`, `shell/` |
| `platform-structure` | Anything in `platform/` that isn't `domain/` or `infra/` |
| `feature-structure` | Feature subfolders that aren't `entrypoint/`, `commands/`, `queries/`, `domain/` |
| `entrypoint-no-domain` | Entrypoints importing directly from `domain/` |
| `entrypoint-restricted-deps` | Entrypoints importing from anything other than `commands/`, `queries/`, `platform/infra/` |
| `no-cross-feature-imports` | One feature importing from another feature |
| `commands-no-cross-feature` | Commands importing from other features |
| `commands-must-use-domain` | Commands that don't import from their feature's `domain/` (required rule) |
| `queries-no-commands` | Queries importing from `commands/` |
| `domain-no-upward-deps` | Domain importing from commands/, queries/, entrypoint/, or shell/ |
| `shell-no-domain` | Shell importing from domain/ (shell is thin wiring only) |
| `platform-no-features` | platform/domain/ or platform/infra/ importing from features/ |
| `commands-no-queries` | Commands importing from queries/ (write path cannot depend on read path) |
| `no-nested-commands` | Nested folders inside commands/ (should be flat command files only) |
| `no-nested-queries` | Nested folders inside queries/ (should be flat query files only) |
| `no-circular` | Circular dependencies anywhere |

Rules that require human judgment (e.g. "commands contain no business rules", "queries never mutate state", "entrypoint is thin") are not automatable and remain in the skill checklist.

## Setup

```bash
npm install --save-dev dependency-cruiser
```

Copy the example configuration below into `.dependency-cruiser.mjs` at your project root.

## Example Configuration

```javascript
export default {
  forbidden: [
    // --- Structure rules ---
    // Catches any file at the package root that isn't inside features/, platform/, or shell/.
    // Adjust the "src/" prefix to match your source layout.
    {
      name: "root-structure",
      severity: "error",
      comment: "Package root must only contain features/, platform/, shell/",
      from: { path: "src/(?!features/|platform/|shell/).+" },
      to: {}
    },
    // platform/ is for shared horizontals. Only two folders allowed: domain/ for shared
    // business logic and infra/ for external service wrappers.
    {
      name: "platform-structure",
      severity: "error",
      comment: "platform/ contains only domain/ and infra/",
      from: { path: "platform/(?!domain/|infra/)[^/]+/.+" },
      to: {}
    },
    // Each feature is a vertical slice. Only four subfolders are allowed.
    // entrypoint/ (external interface), commands/ (write ops), queries/ (read ops), domain/ (business rules).
    {
      name: "feature-structure",
      severity: "error",
      comment: "Features contain only entrypoint/, commands/, queries/, domain/",
      from: { path: "features/[^/]+/(?!entrypoint/|commands/|queries/|domain/)[^/]+/.+" },
      to: {}
    },
    // commands/ and queries/ must be flat — one file per command/query, no nested folders.
    // Catches any file inside a subfolder of commands/.
    {
      name: "no-nested-commands",
      severity: "error",
      comment: "commands/ must be flat — no nested folders",
      from: { path: "features/[^/]+/commands/[^/]+/.+" },
      to: {}
    },
    // Same for queries/ — flat files only.
    {
      name: "no-nested-queries",
      severity: "error",
      comment: "queries/ must be flat — no nested folders",
      from: { path: "features/[^/]+/queries/[^/]+/.+" },
      to: {}
    },

    // --- Entrypoint dependency rules ---
    // Entrypoint is a thin mapping layer. It invokes commands/queries and maps responses.
    // It must never reach into domain/ directly — that's what commands/ and queries/ are for.
    {
      name: "entrypoint-no-domain",
      severity: "error",
      comment: "Entrypoint must never import from domain/",
      from: { path: "features/[^/]+/entrypoint/.+" },
      to: { path: "(features/[^/]+/domain/|platform/domain/).+" }
    },
    // Entrypoint can only depend on commands/, queries/, and platform/infra/.
    // This prevents entrypoint from doing orchestration, data fetching, or business logic.
    {
      name: "entrypoint-restricted-deps",
      severity: "error",
      comment: "Entrypoint may only import from commands/, queries/, platform/infra/",
      from: { path: "features/([^/]+)/entrypoint/.+" },
      to: {
        path: "(features|platform|shell)/",
        pathNot: "(features/$1/(commands|queries)/|platform/infra/)"
      }
    },

    // --- Domain dependency rules ---
    // Domain contains business rules. It must not depend on anything above it in the stack.
    // Commands orchestrate domain, queries read data, entrypoint maps I/O, shell wires things up.
    // Domain knows about none of them.
    {
      name: "domain-no-upward-deps",
      severity: "error",
      comment: "Domain must not import from commands/, queries/, entrypoint/, or shell/",
      from: { path: "features/[^/]+/domain/.+" },
      to: { path: "(features/[^/]+/(commands|queries|entrypoint)/|shell/).+" }
    },

    // --- Feature isolation rules ---
    // Features are independent vertical slices. No feature may import from another.
    // The $1 capture group ensures imports within the same feature are allowed.
    {
      name: "no-cross-feature-imports",
      severity: "error",
      comment: "Features must not import from other features",
      from: { path: "features/([^/]+)/.+" },
      to: {
        path: "features/([^/]+)/.+",
        pathNot: "features/$1/.+"
      }
    },
    // Redundant with no-cross-feature-imports but gives a more specific error message
    // when the violation originates from a command file.
    {
      name: "commands-no-cross-feature",
      severity: "error",
      comment: "Commands forbidden from other features",
      from: { path: "features/([^/]+)/commands/.+" },
      to: {
        path: "features/([^/]+)/.+",
        pathNot: "features/$1/.+"
      }
    },

    // --- Read/write path separation ---
    // Queries are the read path. Commands are the write path. They must not depend on each other.
    {
      name: "queries-no-commands",
      severity: "error",
      comment: "Queries must not import from commands/",
      from: { path: "features/[^/]+/queries/.+" },
      to: { path: "features/[^/]+/commands/.+" }
    },
    {
      name: "commands-no-queries",
      severity: "error",
      comment: "Commands must not import from queries/",
      from: { path: "features/[^/]+/commands/.+" },
      to: { path: "features/[^/]+/queries/.+" }
    },

    // --- Shell rules ---
    // Shell is thin wiring/routing only. It must not import domain logic.
    // Shell re-exports the public API — it can import from entrypoint/, commands/, queries/,
    // and platform/infra/, but not from domain/.
    {
      name: "shell-no-domain",
      severity: "error",
      comment: "Shell must not import from domain/",
      from: { path: "shell/.+" },
      to: { path: "(features/[^/]+/domain/|platform/domain/).+" }
    },

    // --- Platform rules ---
    // Platform provides shared horizontals. It must never depend on features/ —
    // that would invert the dependency direction.
    {
      name: "platform-no-features",
      severity: "error",
      comment: "Platform must not import from features/",
      from: { path: "platform/.+" },
      to: { path: "features/.+" }
    },

    // --- General ---
    {
      name: "no-circular",
      severity: "error",
      comment: "No circular dependencies",
      from: {},
      to: { circular: true }
    }
  ],

  required: [
    // Commands orchestrate write operations. They MUST go through the domain layer —
    // that's the entire point. A command that doesn't import from domain/ is either
    // doing business logic inline (violation) or doing nothing useful.
    {
      name: "commands-must-use-domain",
      severity: "error",
      comment: "Every command MUST import from domain/",
      module: { path: "features/([^/]+)/commands/[^/]+\\.ts$" },
      to: { path: "features/$1/domain/.+" }
    }
  ],

  options: {
    doNotFollow: { path: "node_modules" },
    tsPreCompilationDeps: true,
    tsConfig: { fileName: "tsconfig.json" },
    exclude: ["dist/", "\\.spec\\.", "\\.test\\.", "\\.d\\.ts$"]
  }
};
```

## Usage

```bash
npx depcruise --config .dependency-cruiser.mjs src/
```

Clean output on a compliant project:

```
✔ no dependency violations found (46 modules, 111 dependencies cruised)
```

Violation output:

```
error no-cross-feature-imports: src/features/checkout/commands/place-order.ts
  → src/features/refunds/domain/refund.ts

error commands-must-use-domain: src/features/checkout/commands/cancel-order.ts

x 2 dependency violations (2 errors, 0 warnings). 46 modules, 111 dependencies cruised.
```

The process exits non-zero on violations, so it fails CI automatically.

## HTML Report

```bash
npx depcruise --config .dependency-cruiser.mjs --output-type err-html -f violations.html src/
```

Generates a standalone HTML page listing all violations grouped by rule, with violation counts and rule explanations.

## Adapting the Configuration

The `from.path` patterns use regex, not globs. Adjust them to match your source layout:

- **Monorepo with multiple packages:** Change `src/` to match your package paths (e.g. `packages/[^/]+/src/`)
- **Different source root:** Replace `src/` in the `root-structure` rule with your root
- **tsconfig location:** Update `options.tsConfig.fileName` to point to your tsconfig
