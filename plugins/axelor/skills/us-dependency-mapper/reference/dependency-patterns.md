# Common Dependency Patterns

Reference guide for typical dependency patterns in Axelor projects.

## Entity Development Pattern

### Standard CRUD Entity

```
US-001: Define [Entity] Domain
  ├→ US-002: Create [Entity] Grid View
  ├→ US-003: Create [Entity] Form View
  └→ US-005: Implement [Entity] Service
     ├→ US-007: Add Grid Actions (search, filter)
     └→ US-008: Add Form Actions (save, validate)

US-002 + US-003 → US-004: Add [Entity] Menu Entry
```

**Dependencies**:
- US-002 depends on US-001 (grid displays domain fields)
- US-003 depends on US-001 (form edits domain fields)
- US-004 depends on US-002, US-003 (menu opens views)
- US-005 depends on US-001 (service operates on domain)
- US-007 depends on US-002, US-005 (grid actions call service)
- US-008 depends on US-003, US-005 (form actions call service)

**Parallel opportunities**: US-002, US-003, US-005 can be done in parallel after US-001.

---

## Master-Detail Pattern

### Parent-Child Entities

```
US-010: Define Customer Domain (parent)
  ├→ US-011: Customer Grid
  ├→ US-012: Customer Form
  └→ US-015: Define CustomerAddress Domain (child, FK to Customer)
     ├→ US-016: Address one-to-many grid in Customer form
     └→ US-017: Address inline edit panel
```

**Dependencies**:
- US-015 depends on US-010 (child references parent FK)
- US-016 depends on US-012, US-015 (embed in parent form)
- US-017 depends on US-015 (edit child entity)

**Pattern**: Parent domain → Child domain → Child integration in parent views

---

## Workflow Implementation Pattern

### Status-Driven Workflow

```
US-020: Define Order Domain (with statusSelect field)
  ├→ US-021: Order Grid/Form views
  └→ US-025: Implement Order Workflow Service
     ├→ US-026: Add "Submit" action (Draft → Submitted)
     ├→ US-027: Add "Approve" action (Submitted → Approved)
     ├→ US-028: Add "Reject" action (Submitted → Rejected)
     └→ US-029: Add "Cancel" action (any → Cancelled)

US-025 → US-030: Configure status-dependent button visibility
US-025 → US-031: Implement workflow notifications
US-025 → US-032: Add audit trail logging
```

**Dependencies**:
- US-025 depends on US-020 (workflow operates on statusSelect field)
- US-026-029 depend on US-025 (individual transitions use workflow service)
- US-030 depends on US-021, US-025 (buttons in views, call workflow)
- US-031 depends on US-025 (notifications triggered by status changes)

**Pattern**: Domain → Views → Workflow Service → Transitions → UI Integration

---

## Import/Export Pattern

```
US-040: Define Product Domain
  ├→ US-041: Product Grid/Form
  └→ US-045: Implement Product Import Service
     ├→ US-046: CSV parsing and validation
     ├→ US-047: Duplicate detection logic
     └→ US-048: Error reporting
        → US-049: Import action button in grid
        → US-050: Import UI dialog

US-040 → US-055: Implement Product Export Service
  └→ US-056: Export action button in grid
```

**Dependencies**:
- US-045 depends on US-040 (import creates domain entities)
- US-046-048 depend on US-045 (import service components)
- US-049 depends on US-041, US-045 (button in grid calls service)
- US-050 depends on US-049 (UI for import action)
- US-055 depends on US-040 (export reads domain entities)

**Pattern**: Domain → Service (with sub-tasks) → UI Integration

---

## Security Configuration Pattern

```
US-060: Define SaleOrder Domain
  ├→ US-061: Sale Order Views
  └→ US-065: Configure SaleOrder Permissions
     ├→ US-066: Define roles (User, Manager, Admin)
     ├→ US-067: Configure model-level permissions (CRUD matrix)
     ├→ US-068: Implement row-level security (domain filters)
     └→ US-069: Add field-level permissions (hide salary fields)
```

**Dependencies**:
- US-065 depends on US-060 (permissions for specific entity)
- US-066-069 depend on US-065 (permission aspects)
- All permission US can be done in parallel after US-065

**Pattern**: Domain → Permission Parent → Permission Components (parallel)

---

## Dashboard/Reporting Pattern

```
US-070: Define SaleOrder Domain
  ├→ US-071: Sale Order Service (with query methods)
  └→ US-075: Create Sales Dashboard
     ├→ US-076: Total Sales Dashlet (uses SaleOrderRepository)
     ├→ US-077: Sales by Category Dashlet
     ├→ US-078: Top Customers Dashlet
     └→ US-079: Sales Trend Chart Dashlet

US-075 → US-080: Add dashboard to main menu
US-075 → US-081: Implement dashboard filters (date range, team)
US-075 → US-082: Add export to PDF feature
```

**Dependencies**:
- US-075 depends on US-070 (dashboard queries domain data)
- US-075 depends on US-071 (dashboard calls service methods)
- US-076-079 depend on US-075 (dashlets part of dashboard)
- US-076-079 can be done in parallel
- US-080-082 depend on US-075 (enhance completed dashboard)

**Pattern**: Domain + Service → Dashboard Parent → Dashlets (parallel) → Enhancements

---

## External Integration Pattern

```
US-090: Define EmailAccount Domain (local storage)
  ├→ US-091: Email Account Views
  └→ US-095: Implement Office365 Integration Service
     ├→ US-096: OAuth2 Authentication
     ├→ US-097: Email synchronization (pull from Office365)
     ├→ US-098: Folder synchronization
     └→ US-099: Error handling and retry logic

US-095 → US-100: Define Message Domain (stores synced emails)
  └→ US-101: Message Views
     → US-105: Scheduled sync job (background)
     → US-106: Manual sync button
```

**Dependencies**:
- US-095 depends on US-090 (integration needs account config)
- US-096-099 depend on US-095 (integration service components)
- US-100 depends on US-095 (synced data structure)
- US-101 depends on US-100 (views for synced data)
- US-105 depends on US-095 (scheduler calls integration)
- US-106 depends on US-101, US-095 (button in view calls integration)

**Pattern**: Config Domain → Integration Service → Data Domain → Views → Triggers

---

## Cross-EPIC Dependencies

### EPIC-001 blocks EPIC-002

```
EPIC-001: Customer Management
  US-001: Customer Domain
  US-002: Customer Grid
  US-003: Customer Form
  [blocks]
  ↓
EPIC-002: Sale Order Management
  US-020: SaleOrder Domain (has FK to Customer)
  US-021: Sale Order Grid (displays customer.name)
  US-022: Sale Order Form (customer selector)
```

**Cross-EPIC dependency**: EPIC-002/US-020 depends on EPIC-001/US-001

**Implication**: EPIC-001 must be at least partially complete before EPIC-002 can start.

---

## Anti-Patterns (Avoid These)

### Circular Dependency

**INVALID**:
```
US-001 depends on US-002
US-002 depends on US-003
US-003 depends on US-001  ← CIRCULAR!
```

**Solution**: Break the cycle by splitting or reordering.

---

### Over-dependency

**INVALID**:
```
US-010: Customer Grid
  depends on: US-001 (Customer Domain) ← valid
  depends on: US-020 (Sale Order Domain) ← unnecessary!
```

**Reason**: Grid only displays Customer fields, doesn't need SaleOrder.

**Solution**: Remove false dependencies.

---

### Under-dependency

**INVALID**:
```
US-030: Customer Import Service
  depends on: (none)  ← missing!
```

**Missing**: Should depend on US-001 (Customer Domain).

**Solution**: Add missing dependencies.

---

### God Story

**INVALID**:
```
US-050: Implement Complete Order Management System
  includes: domain, views, workflow, import, export, dashboard
  blocks: 15 other stories
```

**Problem**: Too large, creates bottleneck.

**Solution**: Break down into smaller stories.

---

## Dependency Resolution Strategies

### Bottom-Up (Domain First)

1. All domain definitions (foundations)
2. All repositories (data access)
3. All services (business logic)
4. All views (UI)
5. All integrations (enhancements)

**Pros**: Stable foundation, enables parallel UI work
**Cons**: Delays business value delivery

---

### Top-Down (Feature First)

1. One complete feature (domain → views → logic)
2. Next complete feature
3. Continue until all features done

**Pros**: Incremental business value
**Cons**: May require refactoring if foundations change

---

### Critical Path (Unblock First)

1. Identify stories with most blocks
2. Complete critical path stories first
3. Parallelize remaining stories

**Pros**: Shortest project duration
**Cons**: May not deliver features in logical order

---

## Dependency Checklist

For each User Story, verify:

- [ ] All referenced entities exist (or are in dependencies)
- [ ] All referenced views exist (or are in dependencies)
- [ ] All referenced services exist (or are in dependencies)
- [ ] No circular dependencies
- [ ] No over-dependencies (unnecessary dependencies)
- [ ] No under-dependencies (missing dependencies)
- [ ] Blocking relationships identified
- [ ] Parallel opportunities noted

---

**Last Updated**: 2025-11-17
**Version**: 1.0
