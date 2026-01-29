---
name: Tactical DDD
description: "Design, refactor, analyze, and review code by applying the principles and patterns of tactical domain-driven design. Triggers on: domain modeling, aggregate design, 'entity', 'value object', 'repository', 'bounded context', 'domain event', 'domain service', code touching domain/ directories, rich domain model discussions."
version: 1.0.0
---

# Tactical DDD

Design, refactor, analyze, and review code by applying the principles and patterns of tactical domain-driven design.

## Principles

1. **Isolate domain logic**
2. **Use rich domain language**
3. **Orchestrate with use cases**
4. **Avoid anemic domain model**
5. **Separate generic concepts**
6. **Make the implicit explicit... like your life depends on it**
7. **Design aggregates around invariants**
8. **Extract immutable value objects liberally**

---

## 1. Isolate domain logic

**What:** Domain logic is not mixed with technical code like HTTP and database transactions.

**Why:** Easier to understand the most important part of the code, easier to validate with domain experts, easier to test and evolve, easier to plan and implement new features.

**Test:** Could a domain expert read the code? Can the code be unit tested without mocks or spinning up databases?

```typescript
// ❌ WRONG - domain polluted with infrastructure
class Delivery {
  async dispatch() {
    this.logger.info('Dispatching delivery', { id: this.id })  // Infrastructure!
    await this.db.beginTransaction()                           // Infrastructure!
    if (this.status !== 'ready') throw new Error('Not ready')
    this.status = 'dispatched'
    await this.db.save(this)                                   // Infrastructure!
    await this.db.commit()                                     // Infrastructure!
    await this.pushNotification.notifyDriver()                 // Infrastructure!
  }
}

// ✅ RIGHT - isolated domain logic
class Delivery {
  dispatch(): void {
    if (this.status !== DeliveryStatus.Ready) {
      throw new DeliveryNotReadyError(this.id)
    }
    this.status = DeliveryStatus.Dispatched
    this.dispatchedAt = new Date()
  }
}
```

---

## 2. Use rich domain language

**What:** Names in code match exactly what domain experts say. No programmer jargon. No generic names.

**Why:** Translation between code-speak and business-speak causes bugs. When a domain expert says "assess a claim" and the code says "processEntity", someone will misunderstand something.

**Test:** Would a domain expert recognize this name? If you'd need to translate it for them, it's wrong.

**Common generic terms to watch for:**
- `Manager`, `Handler`, `Processor`, `Helper`, `Util`
- `Data`, `Info`, `Item` (when domain terms exist)
- `process`, `handle`, `execute` (what does it actually DO?)

```typescript
// ❌ WRONG - programmer jargon
class ClaimHandler {
  processClaimData(claimData: ClaimDTO): ProcessingResult {
    return this.claimProcessor.handle(claimData)
  }
}

// ✅ RIGHT - domain language
class ClaimAssessor {
  assessClaim(claim: InsuranceClaim): AssessmentDecision {
    if (claim.exceedsCoverageLimit()) {
      return AssessmentDecision.deny(DenialReason.ExceedsCoverage)
    }
    return AssessmentDecision.approve()
  }
}
```

---

## 3. Orchestrate with use cases

**What:** A use case is a user goal—something a user would recognize as an action they can perform in your application.

**Why:** Use cases define the entry points to your domain. They answer "what can a user do?" If something isn't a user goal, it's supporting machinery that belongs elsewhere.

**Test (the menu test):** If you described your application's features to a user like a menu, would this be on it?

```
DELIVERY APP MENU:
├── Request Delivery     ← Use case: user goal
├── Track Delivery       ← Use case: user goal
├── Cancel Delivery      ← Use case: user goal
├── Calculate ETA        ← NOT a use case: internal machinery
└── Check Delivery Radius ← NOT a use case: domain rule
```

```typescript
// ❌ WRONG - not a user goal, this is internal machinery
// use-cases/calculate-eta.use-case.ts
async function calculateETA(deliveryId: DeliveryId) {
  const delivery = await deliveryRepository.find(deliveryId)
  const driver = await driverRepository.find(delivery.driverId)
  return routeService.estimateArrival(driver.location, delivery.destination)
}

// ✅ RIGHT - actual user goal (appears in menu)
// use-cases/cancel-delivery.use-case.ts
async function cancelDelivery(deliveryId: DeliveryId, reason: CancellationReason) {
  const delivery = await deliveryRepository.find(deliveryId)
  delivery.cancel(reason)
  await deliveryRepository.save(delivery)
}
```

---

## 4. Avoid anemic domain model

**What:** Domain logic lives in domain objects, not in use cases. Use cases orchestrate; domain objects decide.

**Why:** When business rules leak into use cases, they scatter across the codebase, duplicate, and diverge. The domain becomes a dumb data carrier.

**Test:** Is your use case making business decisions, or just coordinating? If the use case contains if/else business logic, you likely have an anemic model.

```typescript
// ❌ WRONG - business logic in use case (anemic domain)
async function confirmDropoff(deliveryId: DeliveryId, photo: ProofPhoto) {
  const delivery = await deliveryRepository.find(deliveryId)

  // Business rules leaked into use case!
  if (delivery.status !== 'in_transit') {
    throw new Error('Delivery not in transit')
  }
  if (!photo && delivery.requiresSignature) {
    throw new Error('Proof of delivery required')
  }

  delivery.status = 'delivered'
  delivery.proofPhoto = photo
  delivery.deliveredAt = new Date()
  await deliveryRepository.save(delivery)
}

// ✅ RIGHT - use case orchestrates, domain decides
async function confirmDropoff(deliveryId: DeliveryId, photo: ProofPhoto) {
  const delivery = await deliveryRepository.find(deliveryId)

  delivery.confirmDropoff(photo)  // Domain enforces the rules

  await deliveryRepository.save(delivery)
}
```

**Signs of anemic model:**
- Use cases full of if/else business logic
- Domain objects are just data with getters/setters
- Business rules duplicated across multiple use cases
- Validation logic outside the object being validated

---

## 5. Separate generic concepts

**What:** Generic capabilities that aren't specific to your domain live separately from domain-specific logic.

**Why:** A retry mechanism, a caching layer, a validation framework—these aren't YOUR domain. Mixing them with domain logic obscures what's actually specific to your business.

**Test:** Would this code exist in a completely different business domain? If yes, it's generic. If it's specific to YOUR business rules, it's domain.

```typescript
// ❌ WRONG - generic retry logic mixed with domain
// domain/driver-locator.ts
class DriverLocator {
  // Generic retry logic does not belong in domain!
  private async withRetry<T>(fn: () => Promise<T>, attempts: number): Promise<T> {
    for (let i = 0; i < attempts; i++) {
      try { return await fn() }
      catch (e) { if (i === attempts - 1) throw e }
    }
    throw new Error('Retry failed')
  }

  async findAvailableDriver(zone: Zone): Promise<Driver> {
    return this.withRetry(() => this.searchDriversInZone(zone), 3)
  }

  private async searchDriversInZone(zone: Zone): Promise<Driver> {
    // domain logic to find nearest available driver
  }
}

// ✅ RIGHT - same behavior, properly separated
// infra/retry.ts (generic, reusable in any project)
export async function withRetry<T>(fn: () => Promise<T>, attempts: number): Promise<T> {
  for (let i = 0; i < attempts; i++) {
    try { return await fn() }
    catch (e) { if (i === attempts - 1) throw e }
  }
  throw new Error('Retry failed')
}

// domain/driver-locator.ts (pure domain, no infra imports)
class DriverLocator {
  async findAvailableDriver(zone: Zone): Promise<Driver> {
    // domain logic to find nearest available driver
  }
}

// use-cases/dispatch-delivery.ts (orchestrates domain + infra)
async function dispatchDelivery(deliveryId: DeliveryId) {
  const delivery = await deliveryRepository.find(deliveryId)
  const driver = await withRetry(
    () => driverLocator.findAvailableDriver(delivery.zone), 3
  )
  delivery.assignDriver(driver)
  await deliveryRepository.save(delivery)
}
```

---

## 6. Make the implicit explicit... like your life depends on it

**What:** Strive for maximum expressiveness. Go as far as possible to identify and name domain concepts in code. Don't settle for "good enough"—push until the code speaks the domain fluently.

**Why:** Maximum alignment optimizes communication between engineers and domain experts. Easier to discuss nuances and avoid misconceptions. Easier to plan and implement features and detect when the design of code is causing unnecessary friction.

**Test:** Could you discuss this code with a domain expert without translation? Are there concepts they use that don't exist in your code?

```typescript
// This code looks fine - isolated, uses domain terms
class Delivery {
  status: DeliveryStatus
  driver: Driver | null
  pickupTime: Date | null
  dropoffTime: Date | null
  proofOfDelivery: Photo | null

  assignDriver(driver: Driver): void {
    if (this.status !== DeliveryStatus.Confirmed) throw new Error('...')
    this.driver = driver
    this.status = DeliveryStatus.Assigned
  }

  recordPickup(): void {
    if (this.status !== DeliveryStatus.Assigned) throw new Error('...')
    this.pickupTime = new Date()
    this.status = DeliveryStatus.InTransit
  }

  recordDropoff(photo: Photo): void {
    if (this.status !== DeliveryStatus.InTransit) throw new Error('...')
    this.proofOfDelivery = photo
    this.dropoffTime = new Date()
    this.status = DeliveryStatus.Delivered
  }
}

// But the TYPES can describe the domain! Each state is a distinct concept.
// Reading the types alone tells you how deliveries work.

type Delivery =
  | RequestedDelivery      // Customer placed request
  | ConfirmedDelivery      // Restaurant accepted
  | AssignedDelivery       // Driver assigned, heading to restaurant
  | InTransitDelivery      // Driver picked up, heading to customer
  | DeliveredDelivery      // Complete with proof

interface RequestedDelivery {
  kind: 'requested'
  customer: Customer
  restaurant: Restaurant
  items: MenuItem[]
}

interface ConfirmedDelivery {
  kind: 'confirmed'
  customer: Customer
  restaurant: Restaurant
  items: MenuItem[]
  estimatedPrepTime: Duration
}

interface AssignedDelivery {
  kind: 'assigned'
  customer: Customer
  restaurant: Restaurant
  items: MenuItem[]
  driver: Driver              // Now guaranteed to exist
  estimatedPickup: Time
}

interface InTransitDelivery {
  kind: 'in_transit'
  customer: Customer
  restaurant: Restaurant
  items: MenuItem[]
  driver: Driver
  pickupTime: Time            // Now guaranteed to exist
  estimatedDropoff: Time
}

interface DeliveredDelivery {
  kind: 'delivered'
  customer: Customer
  restaurant: Restaurant
  items: MenuItem[]
  driver: Driver
  pickupTime: Time
  dropoffTime: Time           // Now guaranteed to exist
  proofOfDelivery: Photo      // Now guaranteed to exist
}

// State transitions are explicit functions
function confirmDelivery(d: RequestedDelivery, prepTime: Duration): ConfirmedDelivery
function assignDriver(d: ConfirmedDelivery, driver: Driver): AssignedDelivery
function recordPickup(d: AssignedDelivery): InTransitDelivery
function recordDropoff(d: InTransitDelivery, photo: Photo): DeliveredDelivery
```

**Smaller improvements matter too:**

```typescript
// Extract an if statement to a named method
if (distance.kilometers > 10 && !driver.hasLongRangeVehicle) { ... }
if (delivery.exceedsDriverRange(driver)) { ... }

// Name a boolean expression
const canAssign = driver.isAvailable && driver.isInZone(delivery.zone) && !driver.atCapacity
const canAssign = driver.canAccept(delivery)

// Rename to use domain language
const fee = customFee ?? standardFee
const fee = customFee ?? defaultDeliveryFee
```

**Ways to increase expressiveness:**
- Model states as distinct types (Delivery with status → RequestedDelivery, ConfirmedDelivery, etc.)
- Make optional fields guaranteed at the right state (driver: Driver | null → driver: Driver)
- Extract conditionals to named methods (complex if → exceedsDriverRange)
- Rename variables to use domain language (standardFee → defaultDeliveryFee)

---

## 7. Design aggregates around invariants

**What:** An aggregate is a cluster of objects that must be consistent together. The aggregate root enforces the rules. External code cannot violate invariants.

**Why:** Without clear boundaries, inconsistent states creep in. One piece of code updates the delivery, another updates the route, and suddenly the ETA is wrong.

**Test:** What must be true at all times? What rules must never be broken? The objects involved in those rules form an aggregate.

```typescript
// ❌ WRONG - no aggregate boundary, invariants violated
class Delivery {
  stops: DeliveryStop[]  // Exposed!
  totalDistance: Distance
}

// External code can break invariants
delivery.stops.push(new DeliveryStop(location))
// Oops - totalDistance is now wrong!

// ✅ RIGHT - aggregate protects invariants
class Delivery {
  private stops: DeliveryStop[] = []
  private _totalDistance: Distance = Distance.zero()

  addStop(location: Location): void {
    if (this.status !== DeliveryStatus.Planning) {
      throw new DeliveryNotModifiableError(this.id)
    }
    const previousStop = this.stops[this.stops.length - 1]
    const stop = new DeliveryStop(location)
    this.stops.push(stop)
    this._totalDistance = this._totalDistance.add(
      previousStop.distanceTo(location)  // Invariant maintained!
    )
  }

  removeStop(stopId: StopId): void {
    if (this.stops.length <= 2) {
      throw new MinimumStopsRequiredError(this.id)
    }
    // Recalculate total distance after removal
    this.stops = this.stops.filter(s => !s.id.equals(stopId))
    this._totalDistance = this.calculateTotalDistance()  // Invariant maintained!
  }

  get totalDistance(): Distance {
    return this._totalDistance
  }
}
```

**Aggregate rules:**
- One root entity per aggregate
- External code accesses only through the root
- The root enforces all invariants
- Reference other aggregates by ID, not object
- Methods should operate on the same state—if they don't, split the aggregate

---

## 8. Extract immutable value objects liberally

**What:** When something is defined by its attributes (not identity), make it an immutable value object. Do this liberally—more value objects is usually better.

**Why:** Value objects are simple. They can't change unexpectedly. They're easy to test. They make domain concepts explicit. They're also a good way to extract logic from aggregates and entities that can easily get large—keep entities focused by pulling cohesive concepts into value objects.

**Test:** Does this need a unique ID to track it over time? No? It's probably a value object.

```typescript
// Entity with primitives that should be a value object
class Delivery {
  id: DeliveryId
  feeAmount: number
  feeCurrency: string
}

// Extract the value object
class Delivery {
  id: DeliveryId
  fee: Money
}

class Money {
  constructor(
    readonly amount: number,
    readonly currency: Currency
  ) {}

  add(other: Money): Money {
    if (this.currency !== other.currency) {
      throw new CurrencyMismatchError(this.currency, other.currency)
    }
    return new Money(this.amount + other.amount, this.currency)
  }

  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency
  }
}
```

**Good candidates for value objects:**
- Money, Currency, Percentage
- DateRange, TimeSlot, Duration
- Address, Coordinates, Distance
- EmailAddress, PhoneNumber, URL
- Quantity, Weight, Temperature
- PersonName, CompanyName

---

## Mandatory Checklist

When designing, refactoring, analyzing, or reviewing code:

1. [ ] Verify domain is isolated from infrastructure (no DB/HTTP/logging in domain; generic utilities in infra; domain doesn't import infra)
2. [ ] Verify names are from YOUR domain, not generic developer jargon
3. [ ] Verify use cases are intentions of users, human or automated (apply the menu test)
4. [ ] Verify business logic lives in domain objects, use cases only orchestrate
5. [ ] Verify states are modeled as distinct types where appropriate
6. [ ] Verify hidden domain concepts are extracted and named explicitly
7. [ ] Verify aggregates are designed around invariants, not naive mapping of domain nouns
8. [ ] Verify values are extracted into value objects expressing a domain concept

Do not proceed until all checks pass.
