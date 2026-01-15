---
name: Writing Tests
description: "Principles for writing effective, maintainable tests. Covers naming conventions, assertion best practices, and comprehensive edge case checklists. Based on BugMagnet by Gojko Adzic."
version: 1.0.0
---

# Writing Tests

How to write tests that catch bugs, document behavior, and remain maintainable.

> Based on [BugMagnet](https://github.com/gojko/bugmagnet-ai-assistant) by Gojko Adzic. Adapted with attribution.

## Critical Rules

🚨 **Test names describe outcomes, not actions.** "returns empty array when input is null" not "test null input". The name IS the specification.

🚨 **Assertions must match test titles.** If the test claims to verify "different IDs", assert on the actual ID values—not just count or existence.

🚨 **Assert specific values, not types.** `expect(result).toEqual(['First.', ' Second.'])` not `expect(result).toBeDefined()`. Specific assertions catch specific bugs.

🚨 **One concept per test.** Each test verifies one behavior. If you need "and" in your test name, split it.

🚨 **Bugs cluster together.** When you find one bug, test related scenarios. The same misunderstanding often causes multiple failures.

## When This Applies

- Writing new tests
- Reviewing test quality
- During TDD RED phase (writing the failing test)
- Expanding test coverage
- Investigating discovered bugs

## Test Naming

**Pattern:** `[outcome] when [condition]`

### Good Names (Describe Outcomes)

```
returns empty array when input is null
throws ValidationError when email format invalid
calculates tax correctly for tax-exempt items
preserves original order when duplicates removed
```

### Bad Names (Describe Actions)

```
test null input           // What about null input?
should work               // What does "work" mean?
handles edge cases        // Which edge cases?
email validation test     // What's being validated?
```

### The Specification Test

Your test name should read like a specification. If someone reads ONLY the test names, they should understand the complete behavior of the system.

## Assertion Best Practices

### Assert Specific Values

```typescript
// ❌ WEAK - passes even if completely wrong data
expect(result).toBeDefined()
expect(result.items).toHaveLength(2)
expect(user).toBeTruthy()

// ✅ STRONG - catches actual bugs
expect(result).toEqual({ status: 'success', items: ['a', 'b'] })
expect(user.email).toBe('test@example.com')
```

### Match Assertions to Test Title

```typescript
// ❌ TEST SAYS "different IDs" BUT ASSERTS COUNT
it('generates different IDs for each call', () => {
  const id1 = generateId()
  const id2 = generateId()
  expect([id1, id2]).toHaveLength(2)  // WRONG: doesn't check they're different!
})

// ✅ ACTUALLY VERIFIES DIFFERENT IDs
it('generates different IDs for each call', () => {
  const id1 = generateId()
  const id2 = generateId()
  expect(id1).not.toBe(id2)  // RIGHT: verifies the claim
})
```

### Avoid Implementation Coupling

```typescript
// ❌ BRITTLE - tests implementation details
expect(mockDatabase.query).toHaveBeenCalledWith('SELECT * FROM users WHERE id = 1')

// ✅ FLEXIBLE - tests behavior
expect(result.user.name).toBe('Alice')
```

## Test Structure

### Arrange-Act-Assert

```typescript
it('calculates total with tax for non-exempt items', () => {
  // Arrange: Set up test data
  const item = { price: 100, taxExempt: false }
  const taxRate = 0.1

  // Act: Execute the behavior
  const total = calculateTotal(item, taxRate)

  // Assert: Verify the outcome
  expect(total).toBe(110)
})
```

### One Concept Per Test

```typescript
// ❌ MULTIPLE CONCEPTS - hard to diagnose failures
it('validates and processes order', () => {
  expect(validate(order)).toBe(true)
  expect(process(order).status).toBe('complete')
  expect(sendEmail).toHaveBeenCalled()
})

// ✅ SINGLE CONCEPT - clear failures
it('accepts valid orders', () => {
  expect(validate(validOrder)).toBe(true)
})

it('rejects orders with negative quantities', () => {
  expect(validate(negativeQuantityOrder)).toBe(false)
})

it('sends confirmation email after processing', () => {
  process(order)
  expect(sendEmail).toHaveBeenCalledWith(order.customerEmail)
})
```

## Edge Case Checklists

When testing a function, systematically consider these edge cases based on input types.

### Numbers

- [ ] Zero
- [ ] Negative numbers
- [ ] Very large numbers (near MAX_SAFE_INTEGER)
- [ ] Very small numbers (near MIN_SAFE_INTEGER)
- [ ] Decimal precision (0.1 + 0.2)
- [ ] NaN
- [ ] Infinity / -Infinity
- [ ] Boundary values (off-by-one at limits)

### Strings

- [ ] Empty string `""`
- [ ] Whitespace only `"   "`
- [ ] Very long strings (10K+ characters)
- [ ] Unicode: emojis 👨‍👩‍👧‍👦, RTL text, combining characters
- [ ] Special characters: quotes, backslashes, null bytes
- [ ] SQL/HTML/script injection patterns
- [ ] Leading/trailing whitespace
- [ ] Mixed case sensitivity

### Collections (Arrays, Objects, Maps)

- [ ] Empty collection `[]`, `{}`
- [ ] Single element
- [ ] Duplicates
- [ ] Nested structures
- [ ] Circular references
- [ ] Very large collections (performance)
- [ ] Sparse arrays
- [ ] Mixed types in arrays

### Dates and Times

- [ ] Leap years (Feb 29)
- [ ] Daylight saving transitions
- [ ] Timezone boundaries
- [ ] Midnight (00:00:00)
- [ ] End of day (23:59:59)
- [ ] Year boundaries (Dec 31 → Jan 1)
- [ ] Invalid dates (Feb 30, Month 13)
- [ ] Unix epoch edge cases
- [ ] Far future/past dates

### Null and Undefined

- [ ] `null` input
- [ ] `undefined` input
- [ ] Missing optional properties
- [ ] Explicit `undefined` vs missing key

### Domain-Specific

- [ ] Email: valid formats, edge cases (plus signs, subdomains)
- [ ] URLs: protocols, ports, special characters, relative paths
- [ ] Phone numbers: international formats, extensions
- [ ] Addresses: Unicode, multi-line, missing components
- [ ] Currency: rounding, different currencies, zero amounts
- [ ] Percentages: 0%, 100%, over 100%

### Violated Domain Constraints

These test implicit assumptions in your domain:

- [ ] Uniqueness violations (duplicate IDs, emails)
- [ ] Missing required relationships (orphaned records)
- [ ] Ordering violations (events out of sequence)
- [ ] Range breaches (age -1, quantity 1000000)
- [ ] State inconsistencies (shipped but not paid)
- [ ] Format mismatches (expected JSON, got XML)
- [ ] Temporal ordering (end before start)

### Typed Property Validation

When testing code that validates properties against type constraints (e.g., validating `route: string` in an interface):

**Wrong-type literals:**
- [ ] Numeric literal when string expected (`route = 123`)
- [ ] Boolean literal when string expected (`route = true`)
- [ ] String literal when number expected (`count = 'five'`)
- [ ] String literal when boolean expected (`enabled = 'yes'`)

**Non-literal expressions:**
- [ ] Template literal (`` route = `/path/${id}` ``)
- [ ] Variable reference (`route = someVariable`)
- [ ] Function call (`route = getRoute()`)
- [ ] Computed property (`route = config.path`)

**Correct type:**
- [ ] Valid literal of correct type (`route = '/orders'`)
- [ ] Edge values (empty string `''`, zero `0`, `false`)

**Why this matters:**
A common bug pattern is validating "is this a literal?" without checking "is this the RIGHT TYPE of literal?"
- `hasLiteralValue()` returns true for `123`, `true`, and `'string'`
- `hasStringLiteralValue()` returns true only for `'string'`

When an interface specifies `property: string`, validation must reject numeric and boolean literals, not just non-literal expressions.

## Bug Clustering

When you discover a bug, don't stop—explore related scenarios:

1. **Same function, similar inputs** - If null fails, test undefined, empty string
2. **Same pattern, different locations** - If one endpoint mishandles auth, check others
3. **Same developer assumption** - If off-by-one here, check other boundaries
4. **Same data type** - If dates fail at DST, check other time edge cases

## When Tempted to Cut Corners

- If your test name says "test" or "should work": STOP. What outcome are you actually verifying? Name it specifically.

- If you're asserting `toBeDefined()` or `toBeTruthy()`: STOP. What value do you actually expect? Assert that instead.

- If your assertion doesn't match your test title: STOP. Either fix the assertion or rename the test. They must agree.

- If you're testing multiple concepts in one test: STOP. Split it. Future you debugging a failure will thank you.

- If you found a bug and wrote one test: STOP. Bugs cluster. What related scenarios might have the same problem?

- If you're skipping edge cases because "that won't happen": STOP. It will happen. In production. At 3 AM.

## Integration with Other Skills

**With TDD Process:** This skill guides the RED phase—how to write the failing test well.

**With Software Design Principles:** Testable code follows design principles. Hard-to-test code often has design problems.
