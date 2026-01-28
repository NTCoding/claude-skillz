---
name: Separation of Concerns
description: "Enforces code organization using features/ (verticals), platform/ (horizontals), and shell/ (thin wiring). Triggers on: code organization, file structure, where does this belong, new file creation, refactoring."
version: 2.5.1
---

# Separation of Concerns

## Principles

1. **Separate external clients from domain-specific code**
2. **Separate feature-specific from shared capabilities**
3. **Separate intent from execution**
4. **Separate functions that depend on different state**
5. **Separate functions that don't have related names**

## Mental Model: Verticals and Horizontals

**Vertical** = all code for ONE feature, grouped together
**Horizontal** = capabilities used by MULTIPLE features

All three top-level folders are mandatory:
- `features/` — verticals, containing some combination of entrypoint/, commands/, queries/, domain/
  - commands/ orchestrates write operations; MUST go through domain/
  - queries/ handles read operations; MAY bypass domain/
  - domain/ contains business rules (required if commands/ exists)
  - entrypoint/ only needed when exposing external interface (HTTP, CLI, events)
- `platform/` — horizontals, only contains `domain/` and `infra/` (nothing else)
- `shell/` — thin wiring/routing only (no business logic)

infra/ lives in platform/infra/, not inside features.

```
features/              platform/              shell/
├── checkout/          ├── domain/            └── cli.ts
│   ├── entrypoint/    │   └── tax-calc/
│   ├── commands/      └── infra/
│   ├── queries/           └── ext-clients/
│   └── domain/
└── refunds/
    ├── entrypoint/
    ├── commands/
    ├── queries/
    └── domain/
```

---

## Entrypoint Responsibilities

**What:** Thin mapping layer between external world and commands/queries.

**Pattern:**
1. Parse external input into command or query object
2. Invoke command or query
3. Map result to external response

```typescript
class OrderController {
  constructor(
    private placeOrder: PlaceOrderCommand,
    private getOrderSummary: GetOrderSummaryQuery
  ) {}

  post(req: HttpRequest): HttpResponse {
    const cmd = parseOrderCommand(req.body)
    const result = this.placeOrder.execute(cmd)
    return mapToHttpResponse(result)
  }

  get(req: HttpRequest): HttpResponse {
    const orderId = req.params.id
    const summary = this.getOrderSummary.execute(orderId)
    return mapToHttpResponse(summary)
  }
}
```

**Dependency Rules:**
- ✅ CAN depend on: commands/, queries/, platform/infra/
- ❌ FORBIDDEN: domain/ (entrypoint never imports domain directly)

**Behavioral Rules:**
- ❌ NO orchestration (that's commands/)
- ❌ NO domain logic (that's domain/)
- ❌ NO data fetching (that's queries/)
- ✅ Owns input parsing and output mapping

---

## Commands

**What:** Orchestrate write operations that mutate state. Commands MUST go through the domain layer.

**Why strict layering:** Commands change state. Domain invariants must be enforced. Skipping domain/ means business rules can be violated.

**Pattern:**
1. Receive command input (already parsed by entrypoint)
2. Load domain aggregates/entities
3. Execute domain logic (validation, state transitions)
4. Persist changes
5. Return result

```typescript
class ApproveRefundCommand {
  constructor(private refundRepository: RefundRepository) {}

  execute(input: ApproveRefundInput): Refund {
    const refund = this.refundRepository.get(input.refundId)
    refund.approve(input.approvedBy, input.reason)
    this.refundRepository.save(refund)
    return refund
  }
}
```

Note: Commands should have a single transaction boundary. If you need external service calls (payment, email), use the outbox pattern—persist domain events in the same transaction, process them asynchronously.

**Dependency Rules:**
- ✅ MUST depend on: domain/ (this is the point)
- ✅ CAN depend on: platform/infra/, platform/domain/
- ❌ FORBIDDEN: other features' commands/, queries/, or domain/

**Behavioral Rules:**
- ✅ One command = one transaction boundary
- ✅ All business logic delegated to domain/
- ❌ NO direct database queries (use repositories from domain/)
- ❌ NO business rules in command itself

**Naming:** Verb phrase matching the action. `place-order.ts`, `cancel-subscription.ts`, `approve-refund.ts`. Menu test: would this appear on a UI menu?

---

## Queries

**What:** Handle read operations. Queries MAY bypass domain/ for simplicity and performance.

**Why minimal layering:** Queries don't mutate state. No invariants to protect. Optimize for read performance and simplicity.

**Pattern:**
1. Receive query input (already parsed by entrypoint)
2. Fetch data (directly from repository/database)
3. Map to response DTO
4. Return result

```typescript
class GetOrderSummaryQuery {
  constructor(private db: DatabaseClient) {}

  execute(orderId: string): OrderSummary {
    const row = this.db.query('SELECT ... FROM orders WHERE id = ?', [orderId])
    if (!row) throw new OrderNotFoundError(orderId)
    return new OrderSummary(row.id, row.status, Money.from(row.total))
  }
}
```

**Dependency Rules:**
- ✅ CAN depend on: platform/infra/, platform/domain/
- ✅ CAN import: domain/ value objects (for validation/typing)
- ❌ FORBIDDEN: domain/ services or aggregates
- ❌ FORBIDDEN: commands/

**Behavioral Rules:**
- ✅ Read-only, no side effects
- ✅ Can query database directly (no repository required)
- ✅ Can import value objects from domain/ for response typing
- ❌ NO state mutations
- ❌ NO business rule enforcement (queries trust the data)

**Naming:** Verb phrase describing what you're fetching. `get-order-summary.ts`, `list-pending-refunds.ts`, `search-products.ts`.

**Query-only features:** Features that only read data need only `queries/`. No entrypoint/ required if queries are consumed internally by other features. No domain/ required since no invariants to protect.

---

## Principle 1: Separate external clients from domain-specific code

**What:** Generic wrappers for external services (APIs, databases, SDKs) live separately from code that uses them in domain-specific ways.

**Why:** Domain logic mixed with external service details is harder to understand and evolve. Separating them keeps domain logic pure and focused.

**How:**
- Ask: "Would the creators of this external service recognize this code?"
- YES → external-clients/
- NO → your domain code

```
❌ BAD:
platform/infra/external-clients/order-total.ts   ← domain logic in infra
features/checkout/stripe-api.ts                  ← external client in feature

✅ GOOD:
platform/infra/external-clients/stripe.ts        ← generic: charge, refund, subscribe
features/checkout/payment-processing.ts          ← OUR domain logic using stripe
```

---

## Principle 2: Separate feature-specific from shared capabilities

**What:** Code that belongs to one feature stays in that feature's folder. Code used across features lives in a shared location named for what it IS.

**Why:** When shared logic is buried in one feature, other features either import across boundaries (coupling) or duplicate the logic (divergence). Both cause bugs.

**How:**
- Ask: "Does this conceptually belong to one feature?"
- YES → keep in features/
- NO → extract to platform/, name it for what it IS

```
❌ BAD - buried in one feature:
features/checkout/tax-calculator.ts
features/refunds/refund.ts           ← imports ../checkout/tax-calculator

❌ BAD - duplicated:
features/checkout/tax-calculator.ts
features/refunds/tax-calculator.ts   ← rules diverge over time

✅ GOOD - extracted to platform:
features/checkout/
features/refunds/
platform/domain/tax-calculation/     ← shared domain logic
```

---

## Principle 3: Separate intent from execution

**What:** High-level flow visible at one abstraction level. Implementation details in lower levels.

**Why:** When intent and execution are mixed, you can't see what the code does without reading every line. Changes to one step's implementation ripple through unrelated code.

**How:**
- Ask: "Can I see the high-level flow without reading every line?"
- NO → extract details into named functions/methods

```typescript
// ❌ BAD - can't see flow, details obscure intent
async function checkout(cart: Cart) {
  const ctx = new CheckoutContext()
  try {
    const validation = await validateCart(cart)
    if (!validation.success) { /* 10 lines of error handling */ }
    const payment = await processPayment(cart)
    if (!payment.success) { /* 10 lines of rollback */ }
    // ... 30 more lines
  } catch (e) { await cleanup(ctx); throw e }
}

// ✅ GOOD - flow visible, drill into details as needed
function checkout(cart: Cart, payment: PaymentDetails) {
  const validatedCart = cart.validate()
  const receipt = paymentService.process(validatedCart.total, payment)
  const order = Order.create(validatedCart, receipt)
  confirmationService.send(order)
  return order
}
```

---

## Principle 4: Separate functions that depend on different state

**What:** Functions that depend on different state (different fields, databases, services, config) belong in different modules.

**Why:** Different state dependencies mean different reasons to change, different testing strategies, and different failure modes.

**How:**
- List the fields/dependencies in a class
- For each method, note which it uses
- Methods cluster around different state? → split into separate classes

```
❌ BAD:
class OrderService {
  db, emailClient, templateEngine

  save()  → uses db
  find()  → uses db
  sendConfirmation() → uses emailClient, templateEngine
}

✅ GOOD:
class OrderRepository { db }
class OrderNotifications { emailClient, templateEngine }
```

---

## Principle 5: Separate functions that don't have related names

**What:** Functions in the same module should have names that relate to a common concept.

**Why:** Unrelated names signal unrelated responsibilities. If you can't name the module after what the functions have in common, they probably don't belong together.

**How:**
- Look at the function names in a module
- Can you describe what they have in common in one phrase?
- NO → split them into separate modules

```
❌ BAD - order-helpers.ts:
  calculateOrderTotal()
  formatOrderForInvoice()
  validateOrderForShipping()
  assessOrderFraudRisk()
  → all operate on "order" but change for different reasons:
    pricing rules, invoice formatting, shipping constraints, fraud detection

✅ GOOD - split by why they change:
  order-pricing.ts:      calculateTotal(), applyDiscounts()
  invoice-formatting.ts: formatForInvoice(), formatLineItems()
  shipping-validation.ts: validateForShipping(), checkWeightLimits()
  fraud-detection.ts:    assessFraudRisk(), flagSuspiciousPatterns()
```

---

## Package Structure

```
/food-delivery/
├── features/
│   ├── order-placement/
│   │   ├── entrypoint/        ← thin, invokes command or query
│   │   ├── commands/          ← write operations, strict layering
│   │   ├── queries/           ← read operations, minimal layering
│   │   └── domain/            ← business rules (required for commands)
│   │
│   ├── order-dashboard/       ← read-only feature with external API
│   │   ├── entrypoint/
│   │   └── queries/
│   │
│   └── reporting/             ← internal query library
│       └── queries/           ← no entrypoint needed, consumed by other features
│
├── platform/
│   ├── domain/                ← shared business rules
│   └── infra/                 ← technical concerns
│
└── shell/
    └── cli.ts
```

---

## Mandatory Checklist

When designing, implementing, refactoring, or reviewing code, complete this checklist:

**Structure:**
1. [ ] Verify features/, platform/, shell/ exist at the root
2. [ ] Verify platform/ contains only domain/ and infra/
3. [ ] Verify each feature contains only entrypoint/, commands/, queries/, domain/ (all optional; entrypoint/ only for external interfaces)
4. [ ] Verify shell/ contains no business logic

**Commands (write path):**
5. [ ] Verify commands/ exists if feature mutates state
6. [ ] Verify domain/ exists if commands/ exists
7. [ ] Verify every command imports from domain/ (commands MUST use domain)
8. [ ] Verify commands contain no business rules (delegated to domain/)
9. [ ] Verify commands/ contains only command files (no nested folders, no helpers)

**Queries (read path):**
10. [ ] Verify queries/ imports only value objects from domain/ (not services/aggregates)
11. [ ] Verify queries never mutate state
12. [ ] Verify queries/ contains only query files (no nested folders, no helpers)

**Entrypoint:**
13. [ ] Verify entrypoint/ is thin (parse → invoke command/query → map output)
14. [ ] Verify entrypoint/ never imports from domain/
15. [ ] Verify entrypoint/ only imports from commands/, queries/, platform/infra/

**General:**
16. [ ] Verify no dependencies between features
17. [ ] Verify shared business logic is in platform/domain/
18. [ ] Verify external service wrappers are in platform/infra/
19. [ ] Verify no generic type-grouping files (types.ts, errors.ts) spanning capabilities

Do not proceed until all checks pass.
