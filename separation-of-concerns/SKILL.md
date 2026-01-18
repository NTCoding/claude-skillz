---
name: Separation of Concerns
description: "Enforces code organization using features/ (verticals), platform/ (horizontals), and shell/ (thin wiring). Triggers on: code organization, file structure, where does this belong, new file creation, refactoring."
version: 2.2.0
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
- `features/` — verticals, each with entrypoint/, use-cases/, domain/
- `platform/` — horizontals, only contains `domain/` and `infra/` (nothing else)
- `shell/` — thin wiring/routing only (no business logic)

infra/ lives in platform/infra/, not inside features.

```
features/              platform/              shell/
├── checkout/          ├── domain/            └── cli.ts
│   ├── entrypoint/    │   └── tax-calc/
│   ├── use-cases/     └── infra/
│   └── domain/            └── ext-clients/
└── refunds/
    ├── entrypoint/
    ├── use-cases/
    └── domain/
```

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
│   │   ├── entrypoint/        ← thin, invokes use-case
│   │   ├── use-cases/         ← orchestration
│   │   └── domain/            ← business rules
│   │
│   └── driver-tracking/
│       ├── entrypoint/
│       ├── use-cases/
│       └── domain/
│
├── platform/
│   ├── domain/                ← shared business rules
│   └── infra/                 ← technical concerns (infra lives here, not in features)
│
└── shell/
    └── cli.ts
```

---

## Mandatory Checklist

When designing, implementing, refactoring, or reviewing code, complete this checklist:

1. [ ] Verify features/, platform/, shell/ exist at the root of the package
2. [ ] Verify platform/ contains only domain/ and infra/
3. [ ] Verify each feature contains only entrypoint/, use-cases/, domain/
4. [ ] Verify shell/ contains no business logic
5. [ ] Verify code belonging to one feature is in features/[feature]/
6. [ ] Verify shared business logic is in platform/domain/ and no dependencies between features
7. [ ] Verify external service wrappers are in platform/infra/
8. [ ] Verify custom folders (steps/, handlers/) are inside use-cases/ or domain/, not at feature root
9. [ ] Verify each function relies on same state as others in its class/file and name aligns
10. [ ] Verify each file name relates to other files in its directory
11. [ ] Verify each directory name describes what all files inside have in common

Do not proceed until all checks pass.
