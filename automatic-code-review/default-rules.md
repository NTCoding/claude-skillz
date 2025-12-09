# Default Code Review Rules

These are sensible defaults for semantic code review. Copy this file to your project and customize as needed.

---

## Rule 1: No Code Comments

Code should be self-documenting through clear naming and structure.

❌ **Forbidden:**
- `// explanation` (inline comments)
- `/* block comments */`
- Comments explaining what code does

✅ **Exceptions:**
- Configuration files (`.eslintignore`, `.gitignore`)
- Package manifests (`package.json` descriptions)
- Documentation files (`.md`)

**Why:** Comments become outdated and lie. Names never lie.

---

## Rule 2: Maximum Type Safety

No escape hatches. Push for precise types that make illegal states unrepresentable.

❌ **Forbidden:**
- `any` type
- `as Type` (type assertions)
- `@ts-ignore` or `@ts-expect-error`
- `!` non-null assertions (`value!.property`)
- `eslint-disable` comments
- Types with many optional properties when a union would be more precise

✅ **Required:**
- Explicit types for all public APIs
- Discriminated unions over optional bags
- Dedicated types for domain concepts

**Example - optional bags → discriminated union:**

❌ Weak:
```typescript
interface GraphNode {
  id: string
  type: 'person' | 'company' | 'document'
  firstName?: string
  lastName?: string
  birthDate?: Date
  companyName?: string
  taxId?: string
  incorporationDate?: Date
  title?: string
  content?: string
  authorId?: string
}
```

✅ Strong:
```typescript
type GraphNode =
  | { type: 'person'; id: string; firstName: string; lastName: string; birthDate: Date }
  | { type: 'company'; id: string; companyName: string; taxId: string; incorporationDate: Date }
  | { type: 'document'; id: string; title: string; content: string; authorId: string }
```

**Why:** Type safety catches bugs at compile time. Precise types prevent invalid states.

---

## Rule 3: No Dangerous Fallback Values

Defaults hide bugs. Required values should fail fast.

❌ **Forbidden:**
- `value ?? 'default'` (without clear reason)
- `value || 'fallback'` (same)
- Guessing at defaults when value should be required

✅ **Allowed:**
- Optional parameters with documented defaults
- Configuration with explicit optional semantics
- Test data with placeholder values

**Examples:**

```typescript
const nodeType = config.nodeType ?? 'sync'

const radius = calculateRadius(node) ?? 15
```

**Why:** If a value is required, make it required. Don't hide missing data.

---

## Rule 4: Domain Modeling

Business logic belongs in domain objects, not scattered across code.

❌ **Forbidden:**
- Logic outside domain objects:
  ```typescript
  const canProcess = order.status === 'pending'
  ```

- Bare primitives for domain concepts:
  ```typescript
  function findUser(id: string)
  function calculatePrice(amount: number)
  ```

- Arrays without domain meaning:
  ```typescript
  nodes: Node[]
  ```

✅ **Required:**
- Domain objects make decisions:
  ```typescript
  const canProcess = order.canProcess()
  ```

- Typed domain values:
  ```typescript
  function findUser(id: UserId)
  function calculatePrice(amount: Money)
  ```

- Domain collections:
  ```typescript
  nodes: NodeGraph
  ```

**Why:** Domain-driven design prevents logic sprawl and makes intent explicit.

---

## Rule 5: No Generic Category Names

Names express domain purpose, not code organization.

❌ **Forbidden:**
- Files: `utils.ts`, `helpers.ts`, `types.ts`, `services.ts`, `handlers.ts`
- Classes: `NodeHelper`, `Utils`, `ServiceBase`
- Functions: `formatHelper()`, `nodeUtils()`
- Folders: `/utils`, `/helpers`, `/common`, `/core`, `/shared`

✅ **Required:**
- Purpose-driven names:
  - `calculateNodeRadius.ts`
  - `NodePositioning.ts`
  - `EdgeRenderingStrategy.ts`
  - `NodeGraphLayout.ts`

**Framework conventions:** Standard framework folders like `hooks/` or `components/` in React are acceptable.

**Why:** Generic names are mental dumping grounds. Specific names reveal intent.

---

## Review Procedure

For each file:

1. **Read complete file** 
2. **Search for violations** 
3. **Report findings** with file:line references

---

## Report Format

### If violations found:

```
❌ FAIL

Violations:
1. [NO CODE COMMENTS] - src/app.ts:42
   Issue: Inline comment explaining logic
   Fix: Rename variables to be self-documenting

2. [MAXIMUM TYPE SAFETY] - src/types.ts:15
   Issue: Using 'any' type for user parameter
   Fix: Define proper UserData interface
```

### If no violations:

```
✅ PASS

File meets all semantic requirements.
```

---

## Customization

This is a starting point. Customize these rules for your project:

1. Copy to your project: `cp default-rules.md .code-review-rules.md`
2. Edit rules to match your standards
3. Add project-specific rules
4. Remove rules that don't apply

The agent will enforce exactly what you define—nothing more, nothing less.

## Advice: 
Use this agent for rules that cannot be enforced with lint or other deterministic mechanisms. 

If you want to validate tests, you can combine with other tools like bugmagent-ai. Invoke them directly from the automatic-code-reviewer subagent. Also use code coverage thresholds in your testing framework.
