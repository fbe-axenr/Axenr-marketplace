# Axelor Patterns for Business Analysis

This document describes common Axelor framework patterns that business analysts should recognize when analyzing requirements. These patterns help identify how business concepts map to Axelor technical structures.

## Domain Patterns

Common patterns for Axelor entity definitions:

### Entity with Business Code
- **Pattern**: `code` field (String, unique)
- **Purpose**: Business identification independent of technical ID
- **Usage**: Most business entities (Customer, Product, Order, etc.)
- **Example**: Customer with code "CUST-001", Product with code "PROD-XYZ"

### Entity with Name
- **Pattern**: `name` or `fullName` field (String)
- **Purpose**: Human-readable display name
- **Usage**: All entities that need to be displayed in lists/selects
- **Example**: Company name "Axelor SAS", Product name "Laptop Dell XPS"

### Entity with Status/Workflow
- **Pattern**: `status` field (Integer, Selection)
- **Purpose**: Track entity lifecycle states
- **Common values**: DRAFT, VALIDATED, CONFIRMED, CANCELED, COMPLETED
- **Usage**: Business processes with state transitions
- **Example**:
  - Order: DRAFT → CONFIRMED → VALIDATED → COMPLETED
  - Lead: NEW → CONTACTED → QUALIFIED → CONVERTED | LOST

### Entity with Audit Tracking
- **Pattern**: `createdOn`, `updatedOn` (DateTime), `createdBy`, `updatedBy` (User)
- **Purpose**: Automatic tracking of creation and modification
- **Usage**: Most business entities requiring audit trail
- **Framework**: Auto-populated by Axelor if fields present

### Entity with Owner/Assignment
- **Pattern**: Many-to-one relationship to `User` entity
- **Common field names**: `assignedTo`, `owner`, `responsible`, `salesperson`
- **Purpose**: Assign entity to specific user
- **Usage**: Tasks, leads, opportunities, tickets
- **Example**: Lead assigned to salesperson, Task assigned to developer

### Hierarchical Entity
- **Pattern**: Many-to-one relationship to self (`parent` field)
- **Purpose**: Tree structures and hierarchies
- **Usage**: Categories, departments, organizational units, product families
- **Example**:
  - Department (parent: Sales, children: Sales North, Sales South)
  - Product Category (parent: Electronics, children: Computers, Phones)

---

## Relationship Patterns

Common patterns for relationships between entities:

### One-to-Many (Parent-Children)
- **Pattern**: Parent entity has collection, child entity has reference to parent
- **Example**: One Customer has many Orders
  - In Customer: `orders` field (List of Order)
  - In Order: `customer` field (Many-to-one to Customer)
- **Usage**: Master-detail relationships
- **UI**: Typically displayed as inline grid in parent form

### Many-to-One (Child-Parent)
- **Pattern**: Child entity references parent entity
- **Example**: One Order belongs to one Customer
  - In Order: `customer` field (Many-to-one to Customer)
- **Usage**: Lookup relationships, foreign keys
- **UI**: Displayed as select/suggest widget

### Many-to-Many (Cross-Reference)
- **Pattern**: Both entities reference each other via collections
- **Example**: Product in multiple Categories, Category contains multiple Products
  - In Product: `categories` field (Many-to-many to Category)
  - In Category: `products` field (Many-to-many to Product)
- **Usage**: Tags, classifications, associations
- **UI**: Displayed as multi-select or tag widget

### Composition (Owned Collection)
- **Pattern**: One-to-many with cascade delete
- **Example**: One Order has many OrderLines (lines deleted when order deleted)
- **Usage**: Detail lines, sub-items that don't exist independently
- **Deletion**: Cascade (children deleted with parent)

### Aggregation (Referenced Collection)
- **Pattern**: One-to-many without cascade delete
- **Example**: One Customer has many Orders (orders not deleted when customer deleted)
- **Usage**: Independent entities with association
- **Deletion**: No cascade (children remain when parent deleted)

---

## View Patterns

Common patterns for Axelor user interface views:

### Standard Form View
- **Organization**: Fields organized in logical panels/groups
- **Common panels**:
  - "General Information": Basic identification (code, name)
  - "Details": Specific business fields
  - "Relationships": Related entities (inline grids, selects)
  - "Notes": Comments, description
  - "Administration": Audit fields (created by, updated on)
- **Layout**: Left-to-right, top-to-bottom reading order
- **Editable**: Most fields editable unless calculated/system

### Standard Grid View
- **Columns**: Key fields for identification and filtering
- **Common columns**: code, name, status, date, assigned user
- **Filters**: Available on status, date ranges, users
- **Search**: Full-text search on main fields (code, name)
- **Actions**: Double-click opens form, buttons for mass operations
- **Sorting**: Default by most recent or alphabetical

### Dashboard/Cards View
- **Purpose**: Aggregated view for reporting and KPIs
- **Common elements**:
  - Count cards (number of entities by status)
  - Charts (pie, bar, line for trends)
  - Summary tables
- **Usage**: Home screens, reporting modules
- **Refresh**: Real-time or periodic updates

---

## Service Patterns

Common patterns for Java business logic:

### CRUD Service
- **Methods**: `create()`, `update()`, `delete()`, `find()`
- **Purpose**: Basic entity lifecycle management
- **Validations**: Field constraints, business rules
- **Usage**: Standard entity management
- **Example**: CustomerService with create, update, delete, findByCode

### Business Logic Service
- **Methods**: Specific business operations
- **Purpose**: Implement domain-specific logic
- **Naming**: Verb-based (calculate, validate, generate, process)
- **Usage**: Complex calculations, workflow operations
- **Example**:
  - OrderService.calculateTotal()
  - LeadService.qualify()
  - InvoiceService.generate()

### Workflow Service
- **Methods**: State transition operations
- **Purpose**: Manage entity status changes
- **Naming**: Based on transitions (confirm, validate, cancel, complete)
- **Validations**: Pre-conditions, state consistency
- **Example**:
  - OrderService.confirm() - DRAFT → CONFIRMED
  - OrderService.validate() - CONFIRMED → VALIDATED
  - OrderService.cancel() - * → CANCELED

### Integration Service
- **Methods**: External system interactions
- **Purpose**: Import, export, synchronization
- **Naming**: Based on operation (import, export, sync)
- **Usage**: Data exchange with external systems
- **Example**:
  - CustomerService.importFromCSV()
  - OrderService.exportToPDF()
  - ProductService.syncFromERP()

---

## Validation Patterns

Common patterns for business validations:

### Field-Level Validation
- **Type**: Data type, format, constraints
- **Examples**:
  - Email format validation
  - Date range validation (startDate < endDate)
  - Numeric range (amount > 0)
  - Required field check

### Entity-Level Validation
- **Type**: Cross-field consistency
- **Examples**:
  - Total amount = sum of lines
  - Discount percentage between 0-100
  - Unique code within company
  - Status transition rules

### Business Rule Validation
- **Type**: Domain-specific constraints
- **Examples**:
  - Order minimum amount
  - Stock availability check
  - Credit limit verification
  - Permission checks (user can validate)

---

## Common Anti-Patterns to Avoid

### Over-Normalization
- **Issue**: Too many small entities with single fields
- **Better**: Combine related fields in coherent entities
- **Example**: Don't create separate entities for Address, Phone, Email if they're always used together

### Under-Normalization
- **Issue**: Duplicating data instead of using relationships
- **Better**: Extract repeated groups into separate entities
- **Example**: Don't repeat customer information in every order; use Customer entity

### Status as String
- **Issue**: Using String for status instead of Selection
- **Better**: Use Integer with Selection for status fields
- **Reason**: Better performance, consistency, i18n support

### Missing Audit Fields
- **Issue**: No tracking of who/when created/modified
- **Better**: Always include createdOn, updatedOn, createdBy, updatedBy
- **Reason**: Essential for business auditing and debugging

---

## Using This Document

When analyzing requirements:

1. **Identify business entities** → Check which domain patterns apply
2. **Identify relationships** → Determine type (one-to-many, many-to-one, many-to-many)
3. **Identify required views** → Map to standard view patterns
4. **Identify business logic** → Recognize service patterns needed
5. **Identify validations** → Document validation rules to implement

This pattern recognition helps:
- Ask more targeted questions during analysis
- Propose solutions based on proven patterns
- Ensure consistency with Axelor framework conventions
- Accelerate specification refinement

---

## See Also

- @docs/domains/domain-reference.md - Complete XML domain syntax
- @docs/domains/domain-patterns.md - Real examples from AOS
- @docs/views/view-reference.md - Complete XML view syntax
- @docs/java/service-patterns.md - Java implementation patterns
