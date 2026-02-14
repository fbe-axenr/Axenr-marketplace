# Axelor Architecture Design Process

Complete guide for designing technical architecture for Axelor ERP projects.

**This document contains all detailed templates and examples for architecture design phases.**

---

## Overview

The architecture design process transforms refined specifications into detailed technical plans that guide implementation.

**Main Phases:**
1. Analyze Input Documents
2. Design Data Model (Domains)
3. Design Views (Forms, Grids, Dashboards)
4. Design Service Layer
5. Design Repository Layer
6. Design Controller Layer
7. Define Module Configuration
8. Create Implementation Roadmap
9. Perform Risk Analysis

---

## Phase 1: Analyze Input Documents

**Read and analyze:**
1. Refined specification: Extract all entities, relationships, features
2. EPIC/US breakdown: Understand implementation priorities
3. Existing codebase (if applicable): Ensure consistency with existing patterns

**Create mental model:**
- List all entities with complexity level
- Identify entity relationships and cardinalities
- Map features to technical components (domains, views, services)
- Identify cross-cutting concerns (security, i18n, workflows)

---

## Phase 2: Design Data Model

For complete domain design templates, see **@docs/domains/domain-reference.md** and **@docs/domains/domain-patterns.md**.

### Entity Structure Template

```markdown
#### Domain: [EntityName]

**File**: `src/main/resources/domains/[EntityName].xml`
**Package**: `com.axelor.apps.[module].db`
**Table**: `[module]_[entity_name]`
**Extends**: AuditableModel (or Model)

**Fields**:

| Field | Type | Java Type | Constraints | Selection | Default | Description |
|-------|------|-----------|-------------|-----------|---------|-------------|
| code | string | String | required, unique, max=64 | - | - | Business identifier |
| name | string | String | required, max=255 | - | - | Display name |
| status | integer | Integer | required | status.selection | 1 | Current status |

**Relationships**:

| Relationship | Type | Target Entity | Cardinality | Mappedby | Cascade | Description |
|--------------|------|---------------|-------------|----------|---------|-------------|
| partner | many-to-one | Partner | 1..1 | - | - | Required partner |
| items | one-to-many | [EntityName]Line | 0..* | [entityName] | ALL | Line items |

**Indexes**: code (unique), status, (company_id, status)

**Business Rules**: [List validation, calculation, workflow rules]
```

### Axelor Field Types

- `string`: Short text (VARCHAR)
- `text`: Long text (TEXT)
- `integer`, `long`: Integer numbers
- `decimal`: BigDecimal with precision
- `boolean`: True/false
- `date`: LocalDate
- `datetime`: LocalDateTime
- `time`: LocalTime
- `binary`: File/blob
- `many-to-one`: Foreign key
- `one-to-many`: Reverse FK
- `many-to-many`: Join table

### Relationship Guidelines

**many-to-one**: Most common, creates FK
- Use for parent references (company, partner, user)
- Cardinality: 0..1 (optional) or 1..1 (required)

**one-to-many**: Reverse side
- Always specify `mappedby`
- Use `cascade="all"` with `orphanRemoval="true"` for composition

**many-to-many**: Creates join table
- Use sparingly, prefer two many-to-one if business logic needed

### Entity Relationship Diagram

**Use skill**: `/skill axelor-er-diagram-generator` for automatic generation

---

## Phase 3: Design Views

For complete view design templates, see **@docs/views/view-reference.md** and **@docs/views/action-patterns.md**.

### Form View Template

```markdown
#### View: [EntityName] Form

**File**: `src/main/resources/views/[EntityName].xml`
**View Name**: `[entity-name]-form`
**Model**: `com.axelor.apps.[module].db.[EntityName]`

**Panels**:
1. General Information: code, status, name, partner
2. Details: dates, amounts, description
3. Line Items: related list (inline grid)
4. Additional Info (sidebar): audit fields

**Action Buttons**: save, cancel, validate, complete

**Field Attributes**: required, readonly, showIf, domain, onChange, widget
```

### Grid View Template

```markdown
#### View: [EntityName] Grid

**Columns**: code, name, partner, status, amount, date
**Editable**: false
**Default Sort**: date DESC, code
**Filters**: Status, date range, partner
```

### Actions Template

- `action-view-[entity-name]`: Open grid
- `action-view-[entity-name]-form`: Open form
- `action-[operation]`: Business operations (validate, compute, etc.)
- `action-attrs`: Dynamic field attributes
- `action-record`: Set default values

### Menu Template

```markdown
**Parent Menu**: [module-name]-menu
**Sub-menu**: [entity-name]-menu
- Title: "[EntityName] Management"
- Action: action-view-[entity-name]
- Groups: [required roles]
```

---

## Phase 4: Design Service Layer

For complete service patterns, see **@docs/java/service-patterns.md**.

### Service Template

```markdown
### Service: [EntityName]Service

**Interface**: `com.axelor.apps.[module].service.[EntityName]Service`
**Implementation**: `[EntityName]ServiceImpl`

**Dependencies** (@Inject):
- [EntityName]Repository
- Related services

**Methods**:
- validate([Entity]): void (@Transactional)
- computeTotal([Entity]): BigDecimal
- canDelete([Entity]): boolean

**Transaction Management**: @Transactional(rollbackOn = Exception.class)
**Error Handling**: Throw AxelorException for business rule violations
```

---

## Phase 5: Design Repository Layer

For complete repository patterns, see **@docs/java/repository-patterns.md**.

### Custom Repository Template

```markdown
### Repository: [Entity]Repo

**ONLY create if you need:**
- Custom query methods beyond CRUD
- Computed fields (double-save pattern)
- Complex business logic in data layer

**Class**: `com.axelor.apps.[module].db.repo.[Entity]Repo`
**Extends**: Generated `[Entity]Repository`

**Custom Methods**:
- findByStatusSelect(Integer): List<[Entity]>
- findByDateRange(LocalDate, LocalDate): List<[Entity]>

**Override Methods**:
- save([Entity]): [Entity] (for computed fields)
- remove([Entity]): void (for cleanup logic)
```

---

## Phase 6: Design Controller Layer

For complete controller patterns, see **@docs/java/controller-patterns.md**.

### Controller Template

```markdown
### Controller: [EntityName]Controller

**File**: `com.axelor.apps.[module].web.[EntityName]Controller`

**Methods**:
```java
public void validate(ActionRequest request, ActionResponse response) {
  try {
    [EntityName] entity = request.getContext().asType([EntityName].class);
    entity = repository.find(entity.getId());
    service.validate(entity);
    response.setReload(true);
    response.setFlash("Success message");
  } catch (Exception e) {
    TraceBackService.trace(response, e);
  }
}
```

**Guidelines**:
- Keep thin, delegate to services
- Always try-catch with TraceBackService
- Fetch from DB, don't trust context alone
```

---

## Phase 7: Module Configuration

**Reference:** See **@docs/gradle/module-build-gradle-guide.md** for complete build.gradle templates and rules

### Module Source Structure (CRITICAL)

**NEVER create entity Java files manually.** Entities are AUTO-GENERATED from XML.

```
addons/axelor-[module]/
├── src/main/
│   ├── java/com/axelor/apps/[module]/
│   │   ├── db/repo/           # Custom repositories ONLY
│   │   ├── service/           # Business logic
│   │   ├── web/               # Controllers
│   │   ├── exception/         # Exception classes
│   │   └── module/            # Guice module
│   └── resources/
│       ├── domains/           # Entity XML definitions → generates Java
│       ├── views/             # View XML files
│       └── i18n/              # Translations
├── build.gradle
└── README.md (optional)
```

**Generated code (in build/, NOT in src/):**
```
build/src-gen/java/com/axelor/apps/[module]/db/
├── [Entity].java              # AUTO-GENERATED from domains/*.xml
└── repo/
    └── [Entity]Repository.java    # AUTO-GENERATED base repository
```

### build.gradle

**CRITICAL:** Use `com.axelor.app` plugin (NEVER `java-library`)

```gradle
plugins {
  id 'com.axelor.app'
}

axelor {
  title = "[Module Display Name]"
}

dependencies {
  implementation project(':axelor-base')
}
```

**Important:**
- Plugin MUST be `com.axelor.app`
- NO Java version specification in module build.gradle
- See **@docs/gradle/module-build-gradle-guide.md** for examples

---

## Phase 8: Implementation Roadmap

### Roadmap Template

```markdown
## Implementation Roadmap

### Phase 1: Foundation (2-3 days)
- Create module structure
- Create domain XML files
- Run generateCode
- Set up unit tests

**Deliverables**: All domains created, entities generated, compiles

### Phase 2: UI Layer (3-4 days)
- Create all views (forms, grids)
- Create actions and menus
- Test basic CRUD

**Deliverables**: All views accessible, basic CRUD works

### Phase 3: Business Logic (4-6 days)
- Implement services
- Add validation and calculation logic
- Write unit tests

**Deliverables**: All services implemented, tests passing (>80%)

### Phase 4: Advanced Features (3-5 days)
- Workflows, imports/exports, reporting
- Integration with other modules

**Deliverables**: All features working, integration tests passing

### Phase 5: Security & Permissions (1-2 days)
- Configure groups/roles, meta permissions
- Test with different users

**Deliverables**: Permissions configured, security tests passing

### Phase 6: Testing & Quality (2-3 days)
- Complete test suite, code review

**Deliverables**: All tests passing, code approved

### Phase 7: Documentation & Deployment (1-2 days)
- Complete documentation, deploy to test

**Deliverables**: Deployed, UAT sign-off

**Total**: 16-25 person-days
```

---

## Phase 9: Risk Analysis

### Risk Matrix Template

```markdown
## Risks and Mitigation Strategies

### Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Complex data model with circular dependencies | High | Medium | Careful relationship design, lazy loading |
| Performance with large datasets | High | Medium | Indexes, optimize queries, pagination |
| Integration conflicts | Medium | High | Early integration testing, conventions |

### Business Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Requirement changes | Medium | High | Agile approach, iterative validation |
| Missing business rules | Medium | Medium | Regular clarification sessions |

### Project Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Underestimated complexity | High | Medium | Add 20% buffer, re-estimation |
| Developer unavailability | High | Low | Knowledge sharing, documentation |
```

---

## Best Practices

### Domain Design
- Extend `AuditableModel` for business entities
- Use `required="true"` sparingly
- Add `unique="true"` for business identifiers
- Use `selection` for status fields
- Always define indexes on filtered fields

### Relationship Design
- Prefer `many-to-one` over `many-to-many`
- Always specify `mappedby` on `one-to-many`
- Use `cascade="all"` with `orphanRemoval="true"` for composition
- Use `fetch="LAZY"` for large collections

### View Design
- Group related fields in panels
- Use sidebar for metadata
- Use `colSpan` to control width
- Add `showIf` for conditional fields
- Keep grids focused (5-8 columns)

### Service Design
- One service per entity/domain
- Keep methods focused
- Always throw `AxelorException` for business errors
- Use `@Transactional` on write operations
- Inject dependencies

### Controller Design
- Keep thin
- One method per action
- Always try-catch with TraceBackService
- Fetch from DB
- Return user feedback

---

## Quality Checklist

- [ ] All entities have proper domain XML
- [ ] All relationships bidirectional where appropriate
- [ ] All views follow Axelor patterns
- [ ] Services follow single responsibility
- [ ] Business logic in service layer
- [ ] Controllers are thin
- [ ] Proper transaction management
- [ ] Proper exception handling
- [ ] i18n keys defined
- [ ] Security considerations addressed
- [ ] Performance considerations (indexes, lazy loading)
- [ ] Testing strategy defined

---

**This guide provides all templates and examples needed for architecture design. Reference specific sections as needed during the design process.**
