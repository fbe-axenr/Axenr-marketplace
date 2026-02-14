# Technical Architecture Plan - [Project Name]

**Version**: 1.0
**Date**: [Date]
**Architect**: [Name]
**Status**: Draft / To Validate / Validated

---

## 1. Architecture Overview

### 1.1 Axelor Architectural Principles

This project follows the Axelor layered architecture:

```
┌─────────────────────────────────────┐
│    PRESENTATION LAYER (XML Views)   │
│  Forms, Grids, Dashboards, Actions  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    CONTROLLER LAYER (Java)          │
│  Controllers, ActionHandlers        │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    SERVICE LAYER (Java)              │
│  Business Logic, Workflows          │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    REPOSITORY LAYER (Java)           │
│  Data Access, Queries                │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    DOMAIN LAYER (XML → JPA)         │
│  Entity Definitions                  │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│    DATABASE (PostgreSQL)             │
└─────────────────────────────────────┘
```

### 1.2 Module Structure

```
[module-name]/
├── src/main/resources/
│   ├── domains/               # XML entity definitions
│   │   ├── [Entity1].xml
│   │   ├── [Entity2].xml
│   │   └── ...
│   ├── views/                 # XML view definitions
│   │   ├── [Entity1].xml
│   │   ├── [Entity2].xml
│   │   └── ...
│   ├── i18n/                  # Translations
│   │   ├── messages.csv
│   │   ├── messages_fr.csv
│   │   └── messages_en.csv
│   └── data-init/            # Initial data (optional)
│       └── init-data.xml
├── src/main/java/
│   └── com/axelor/apps/[module]/
│       ├── db/               # (optional) Custom data access
│       │   └── repo/         # Custom repositories ONLY (entities are auto-generated)
│       ├── service/          # Business services
│       ├── web/              # Controllers
│       └── exception/        # Custom exceptions
└── build.gradle
```

---

## 2. Data Model (Domains)

### 2.1 Entity-Relationship Diagram

```
[Insert ER diagram - can be textual]

Example:
┌──────────────┐         ┌──────────────┐
│   Customer   │         │   Company    │
│──────────────│         │──────────────│
│ code         │         │ code         │
│ fullName     │◄────────│ name         │
│ email        │  N..1   │ address      │
│ company   ───┼─────────┤              │
└──────────────┘         └──────────────┘
       │
       │ 1..N
       ▼
┌──────────────┐
│    Order     │
│──────────────│
│ orderNo      │
│ orderDate    │
│ customer  ───┤
│ totalAmount  │
└──────────────┘
```

### 2.2 Domains to Create

#### Domain: [Entity1]

**File**: `domains/[Entity1].xml`

**Fields**:

| Field | Axelor Type | Java Type | Constraints | Description |
|-------|-------------|-----------|-------------|-------------|
| code | string | String | required, unique, max=64 | Identifier |
| name | string | String | required, max=255 | Full name |
| status | integer (selection) | Integer | required | Status |
| ... | ... | ... | ... | ... |

**Relationships**:

| Relationship | Type | Target | Mappedby | Cascade | Description |
|--------------|------|--------|----------|---------|-------------|
| company | many-to-one | Company | - | - | Company |
| orders | one-to-many | Order | customer | ALL | Orders |

**Selections**:

- **status**:
  - 1: "Draft"
  - 2: "Validated"
  - 3: "Canceled"

**Indexes**:
- Index on `code`
- Index on `status`
- Composite index on `(company, status)`

#### Domain: [Entity2]
[Same structure]

---

## 3. Views (User Interfaces)

### 3.1 Views to Create

#### View: [Entity1]-form

**File**: `views/[Entity1].xml`

**Type**: Form

**Organization**:

```xml
<form name="[entity1]-form" model="com.axelor.apps.[module].db.[Entity1]">
  <panel name="mainPanel" title="General Information">
    <field name="code" />
    <field name="name" />
    <field name="status" widget="selection" />
  </panel>

  <panel name="detailsPanel" title="Details">
    <field name="company" />
    <field name="description" widget="text" />
  </panel>

  <panel-related name="ordersPanel" field="orders" />
</form>
```

**Read-only Fields**: [List if applicable]

**Action Buttons**: [List of custom buttons]

#### View: [Entity1]-grid

**File**: `views/[Entity1].xml`

**Type**: Grid

**Columns**:
1. code
2. name
3. status
4. company
5. createdOn

**Filters**:
- By status
- By company
- By creation date

**Default Sort**: `createdOn DESC`

### 3.2 Actions and Menus

**Main Menu**: `[Module]`

**Sub-menus**:
- `[Entity1]` → Action `action-[entity1]-view`
- `[Entity2]` → Action `action-[entity2]-view`

---

## 4. Services and Business Logic

### 4.1 Services to Implement

#### Service: [Entity1]Service

**File**: `service/[Entity1]Service.java`

**Interface**:

```java
public interface [Entity1]Service {

  /**
   * Creates a new instance of [Entity1]
   * @param entity The entity to create
   * @return The created entity with ID
   * @throws AxelorException if validation fails
   */
  [Entity1] create([Entity1] entity) throws AxelorException;

  /**
   * Updates an existing instance
   * @param entity The entity to update
   * @return The updated entity
   * @throws AxelorException if validation fails
   */
  [Entity1] update([Entity1] entity) throws AxelorException;

  /**
   * Validates an instance (transition DRAFT → VALIDATED)
   * @param entity The entity to validate
   * @return The validated entity
   * @throws AxelorException if pre-conditions are not met
   */
  [Entity1] validate([Entity1] entity) throws AxelorException;

  /**
   * Computes a derived field
   * @param entity The entity
   * @return The calculation result
   */
  BigDecimal computeTotal([Entity1] entity);
}
```

**Implementation**: `service/[Entity1]ServiceImpl.java`

**Dependencies**:
- `[Entity1]Repository`
- Other services if necessary

#### Service: [Entity2]Service
[Same structure]

### 4.2 Repositories

**IMPORTANT:** Axelor auto-generates `[Entity]Repository extends JpaRepository<Entity>` in `build/src-gen/`.
Only create a custom repository when you need additional query methods or computed fields.

#### Custom Repository: [Entity1]Repo (only if needed)

**File**: `db/repo/[Entity1]Repo.java`

```java
// Custom repository extending the AUTO-GENERATED [Entity1]Repository
public class [Entity1]Repo extends [Entity1]Repository {

  public [Entity1] findByCode(String code) {
    return all()
      .filter("self.code = :code")
      .bind("code", code)
      .fetchOne();
  }

  public List<[Entity1]> findByStatus(Integer status) {
    return all()
      .filter("self.status = :status")
      .bind("status", status)
      .fetch();
  }
}
```

---

## 5. Controllers and Actions

### 5.1 Controllers

#### Controller: [Entity1]Controller

**File**: `web/[Entity1]Controller.java`

```java
public class [Entity1]Controller {

  @Inject
  private [Entity1]Service [entity1]Service;

  /**
   * Action: Validate
   */
  public void validate(ActionRequest request, ActionResponse response) {
    try {
      [Entity1] entity = request.getContext().asType([Entity1].class);
      entity = [entity1]Service.validate(entity);
      response.setReload(true);
      response.setFlash("Validation completed successfully");
    } catch (Exception e) {
      TraceBackService.trace(response, e);
    }
  }

  /**
   * Action: Compute total
   */
  public void computeTotal(ActionRequest request, ActionResponse response) {
    [Entity1] entity = request.getContext().asType([Entity1].class);
    BigDecimal total = [entity1]Service.computeTotal(entity);
    response.setValue("totalAmount", total);
  }
}
```

---

## 6. Configuration and Dependencies

### 6.1 build.gradle

```gradle
dependencies {
  // Dependent Axelor modules (if applicable)
  implementation project(":modules:axelor-base")

  // Other dependencies
}

## 7. Testing Strategy

### 7.1 Unit Tests

For each service, create unit tests:

**File**: `src/test/java/.../service/[Entity1]ServiceTest.java`

**Tests to Cover**:
- Creation with valid data
- Creation with invalid data (validation)
- Update
- Status transitions
- Business calculations

### 7.2 Integration Tests

End-to-end tests simulating complete user journeys.

---

## 8. Migration and Initial Data

### 8.1 Database Migration Script

**File**: `src/main/resources/db/migration/V1.0__initial_schema.sql`

[If custom schema changes are necessary]

### 8.2 Initial Data

**File**: `src/main/resources/data-init/init-data.xml`

Reference data (selections, parameters, etc.)

---

## 9. Security and Permissions

### 9.1 Groups and Roles

**Groups to Create**:
- `[module].user`: Standard user
- `[module].manager`: Manager
- `[module].admin`: Administrator

### 9.2 Access Rules (Object Access)

**File**: XML configuration in module

```xml
<object-views>
  <access-rule model="com.axelor.apps.[module].db.[Entity1]"
               groups="[module].user"
               perm="read,create,write"/>

  <access-rule model="com.axelor.apps.[module].db.[Entity1]"
               groups="[module].manager"
               perm="read,create,write,remove"/>
</object-views>
```

---

## 10. Implementation Checklist

### Phase 1: Domains
- [ ] Create XML file for [Entity1]
- [ ] Create XML file for [Entity2]
- [ ] Run `./gradlew generateCode`
- [ ] Verify compilation

### Phase 2: Repositories
- [ ] Implement [Entity1]Repository
- [ ] Implement [Entity2]Repository
- [ ] Unit tests for repositories

### Phase 3: Services
- [ ] Implement [Entity1]Service
- [ ] Implement [Entity2]Service
- [ ] Unit tests for services

### Phase 4: Views
- [ ] Create views for [Entity1]
- [ ] Create views for [Entity2]
- [ ] Create actions and menus

### Phase 5: Controllers
- [ ] Implement [Entity1]Controller
- [ ] Implement [Entity2]Controller
- [ ] Test actions in UI

### Phase 6: i18n
- [ ] Create translation files
- [ ] Translate all labels

### Phase 7: Tests
- [ ] Complete unit tests
- [ ] Integration tests
- [ ] Manual end-to-end tests

### Phase 8: Documentation
- [ ] Complete JavaDoc
- [ ] User documentation
- [ ] Deployment guide

---

## 11. Risks and Points of Attention

### Technical Risks
- [ ] Risk 1: [Description + mitigation]
- [ ] Risk 2: [Description + mitigation]

### Points of Attention
- [ ] Point 1: [Description]
- [ ] Point 2: [Description]

---

## 12. Estimated Schedule

| Phase | Tasks | Estimation | Dependencies |
|-------|-------|------------|--------------|
| Phase 1 | Domains | X days | - |
| Phase 2 | Repositories | X days | Phase 1 |
| Phase 3 | Services | X days | Phase 2 |
| Phase 4 | Views | X days | Phase 1 |
| Phase 5 | Controllers | X days | Phase 3, 4 |
| Phase 6 | i18n | X days | Phase 4 |
| Phase 7 | Tests | X days | Phase 5 |
| Phase 8 | Documentation | X days | Phase 7 |

**Total Estimated**: X person-days

---

## Validation

**To be Validated by**: [Architect, Tech Lead]
**Validation Date**: [Date]

**Signatures**:
- Architect: ____________ Date: ____
- Tech Lead: _____________ Date: ____
