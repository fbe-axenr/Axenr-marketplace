# SOLID Principles for Axelor Architecture

This document explains how to apply SOLID principles when designing Axelor ERP architectures.

---

## Single Responsibility Principle (SRP)

**Each class has ONE responsibility.**

### Architecture Guidelines

- **Services**: ONE business domain per service
  - `SaleOrderService`: Order lifecycle, validation, computation
  - `InvoiceService`: Invoice generation, validation, finalization
  - NOT: `OrderInvoiceService` handling both orders and invoices
- **Repositories**: ONE entity per repository
  - `SaleOrderRepository`: Queries for SaleOrder only
- **Controllers**: ONE entity's actions per controller
  - `SaleOrderController`: Actions for SaleOrder views only

### Example 

```markdown
### Service Layer

#### SaleOrderService
- **Responsibility**: Sale order lifecycle management
- **Methods**:
  - createOrder(SaleOrder): Create and validate new order
  - confirmOrder(SaleOrder): Confirm draft order
  - computeTotals(SaleOrder): Compute amounts and taxes
  - validateBusinessRules(SaleOrder): Validate business constraints

#### InvoiceGenerationService
- **Responsibility**: Generate invoices from orders
- **Methods**:
  - generateInvoice(SaleOrder): Create invoice from order
  - generateInvoiceLines(SaleOrder): Convert order lines to invoice lines
```

---

## Open/Closed Principle (OCP)

**Classes open for extension, closed for modification.**

### Architecture Guidelines

- Use **interfaces** for services (allow different implementations)
- Use **inheritance** for entity specialization
- Use **strategy pattern** for variable algorithms
- Use **hooks/callbacks** for customization points

### Example

```markdown
#### Service Interfaces

**PricingStrategy** (interface):
- `computePrice(Product, Quantity): BigDecimal`

**Implementations**:
- StandardPricingStrategy: Regular price calculation
- DiscountPricingStrategy: Apply volume discounts
- PromotionalPricingStrategy: Apply promotional pricing

**SaleOrderService** uses PricingStrategy interface (injectable).
```

---

## Liskov Substitution Principle (LSP)

**Subtypes must be substitutable for base types.**

### Architecture Guidelines

- Entity inheritance must preserve base class contracts
- Overridden methods must respect base method contracts
- Service implementations must honor interface contracts

### Example 

```markdown
#### Entity Hierarchy

**Base**: Order (abstract)
- Fields: orderDate, customer, statusSelect
- Contracts: validate(), computeTotal()

**Subtypes**:
- SaleOrder: Extends Order (adds delivery address, shipping)
- PurchaseOrder: Extends Order (adds supplier, reception address)

Both subtypes respect Order contracts (can substitute Order).
```

---

## Interface Segregation Principle (ISP)

**Clients should not depend on interfaces they don't use.**

### Architecture Guidelines

- Create **specific interfaces** for different client needs
- Avoid **fat interfaces** with too many methods
- Group related methods into focused interfaces

### Example 

```markdown
#### Service Interfaces

**Readable** (interface):
- `findById(Long): Optional<T>`
- `findAll(): List<T>`

**Writable** (interface):
- `save(T): T`
- `remove(T): void`

**Computable** (interface):
- `computeTotals(T): void`
- `computeTaxes(T): void`

**SaleOrderService** implements Readable, Writable, Computable as needed.
```

---

## Dependency Inversion Principle (DIP)

**Depend on abstractions, not concretions.**

### Architecture Guidelines

- Services depend on **interfaces**, not implementations
- Use **dependency injection** (@Inject) everywhere
- Define **repository interfaces**, inject them into services
- Define **service interfaces**, inject them into controllers

### Example 

```markdown
### Dependency Graph

**SaleOrderController** (web layer)
  ↓ depends on (interface)
**SaleOrderService** (business layer)
  ↓ depends on (interface)
**SaleOrderRepository** (data layer)

**Dependency Injection**:
- Constructor injection with @Inject
- Google Guice bindings in module configuration
```

---

## Applying SOLID in Axelor Projects

### In Domain Design

- **SRP**: One domain XML per business entity
- **OCP**: Use inheritance for entity specialization
- **LSP**: Ensure subtype entities honor parent contracts
- **ISP**: Split large entities into smaller focused ones if needed
- **DIP**: Reference entities by interface when possible

### In Service Layer

- **SRP**: One service per business domain
- **OCP**: Define service interfaces for extensibility
- **LSP**: Service implementations must honor interface contracts
- **ISP**: Create focused service interfaces (avoid god services)
- **DIP**: Inject dependencies via @Inject, depend on interfaces

### In View Layer

- **SRP**: One view XML per entity, one action per purpose
- **OCP**: Use action inheritance and customization hooks
- **LSP**: Action overrides must respect parent behavior
- **ISP**: Create specific actions, avoid multi-purpose actions
- **DIP**: Actions call services, not repositories directly

---

## Common Violations and Fixes

| Violation | Fix |
|-----------|-----|
| Service handling multiple entities | Split into focused services per entity |
| Fat service interface with 20+ methods | Segregate into smaller interfaces (Readable, Writable, etc.) |
| Controller calling repository directly | Inject service, delegate to service layer |
| Service with concrete dependency | Define interface, inject interface instead |
| Entity with unrelated fields | Split into multiple focused entities |

---

## Checklist for SOLID Architecture

When designing Axelor architecture, verify:

- [ ] Each service has a single, well-defined responsibility
- [ ] Services are defined as interfaces (extensible)
- [ ] Service implementations honor interface contracts
- [ ] Service interfaces are focused (not fat)
- [ ] All dependencies are injected via @Inject
- [ ] Controllers depend on service interfaces
- [ ] Services depend on repository interfaces
- [ ] No direct repository calls from controllers
- [ ] Entity hierarchies respect substitutability
- [ ] Business logic is in services, not controllers or repositories

---

**Reference**: These principles are applied throughout Axelor architecture documentation and code generation agents.
