# AOS Integration Guide for Requirements Refining

Guide for handling Axelor Open Suite (AOS) entity reuse, extension, and custom development when refining functional requirements.

**Reference**: This guide is used in **Phase 0** of requirements-refining-methodology.md

---

## Overview

When refining requirements for an Axelor project, some entities may already exist in AOS (Axelor Open Suite). The gap analysis report identifies which entities can be:

- **REUSED**: Use existing AOS entity as-is with configuration
- **EXTENDED**: Inherit from AOS entity and add custom fields
- **NEW**: Create completely custom entity

This guide explains how to handle each scenario in functional specifications.

---

## Phase 0: AOS Context Integration

### When to Use This Phase

**IF** a gap analysis report exists at `{output_directory}/gap-analysis-report.md`:
1. **Read the gap analysis** before starting entity refining
2. **Understand AOS opportunities** (REUSE/EXTEND/NEW)
3. **Adapt refinement approach** based on categorization

**IF** no gap analysis exists:
- Skip Phase 0, proceed directly to Phase 1 (Understanding Validation)
- All entities will be treated as NEW

### Reading Gap Analysis

The gap analysis report contains:

```markdown
## Entity Classification Summary

| Required Entity | AOS Entity | Strategy | Confidence | Module Dependencies |
|----------------|------------|----------|------------|---------------------|
| Customer | Partner | EXTEND | HIGH | axelor-base |
| Product | Product | REUSE | HIGH | axelor-base |
| Order | SaleOrder | EXTEND | MEDIUM | axelor-sale |
| Delivery | - | NEW | - | - |
```

**Key information**:
- **Required Entity**: The entity needed by the client
- **AOS Entity**: The matching AOS entity (if any)
- **Strategy**: REUSE, EXTEND, or NEW
- **Module Dependencies**: AOS modules to add to build.gradle

---

## Refinement Strategy by Classification

### REUSE: Use AOS Entity As-Is

**When**: Entity categorized as REUSE in gap analysis

**Refinement Approach**:
- **Do NOT specify fields** (they already exist in AOS)
- **Focus on configuration** (which fields to show/hide, default values)
- **Reference AOS documentation** for complete field list

**Example**:

```markdown
## Entity: Product (REUSE from AOS)

### AOS Base Entity

- **AOS Entity**: Product from axelor-base
- **Module**: com.axelor.apps.base
- **Documentation**: https://docs.axelor.com/aos/modules/base/product.html

### Inherited Fields (Standard AOS)

The Product entity inherits ALL standard fields from AOS Product:
- code (Short text) - Unique product code
- name (Short text) - Product name
- description (Long text) - Product description
- productCategory (Relationship → ProductCategory) - Category classification
- productFamily (Relationship → ProductFamily) - Family classification
- unit (Relationship → Unit) - Unit of measure
- salePrice (Amount) - Sale price
- costPrice (Amount) - Cost price
- isActive (Yes/No) - Active status
- [... 50+ other standard fields]

**See AOS documentation for complete field list.**

### Configuration Requirements

**Fields to show in form view**:
- code, name, productCategory, unit, salePrice (essential fields only)

**Fields to hide in form view**:
- Advanced procurement fields (not used in our business)
- Manufacturing fields (not used in our business)

**Default values**:
- isActive: Yes (default)
- productCategory: To be selected by user (no default)

**Required fields** (beyond AOS defaults):
- productCategory (make required for our business)

### Business Rules

- **Rule 1**: Product code must follow pattern: PROD-XXXX-YYYY
- **Rule 2**: Sale price must be greater than cost price (validation warning)
- **Rule 3**: Product cannot be deactivated if used in active orders

**Note**: These are ADDITIONAL rules beyond AOS standard validations.

### Views Configuration

**Form View**:
- Use standard AOS form view
- Hide panels: "Manufacturing", "Procurement", "MRP"
- Show panels: "General", "Sales", "Accounting"

**Grid View**:
- Use standard AOS grid view
- Display columns: code, name, productCategory, salePrice, isActive
- Hide columns: Technical fields, manufacturing fields

**No custom view creation needed** - configure existing AOS views.

### Rationale for REUSE

Why not create custom entity:
- AOS Product has 50+ fields covering all standard cases
- AOS Product integrates with Sale, Purchase, Stock, Accounting modules
- No custom fields needed for our business requirements
- Configuration is simpler than custom development
```

**Key Points for REUSE**:
- ✅ Reference AOS entity and documentation
- ✅ List configuration requirements (show/hide fields, defaults)
- ✅ Specify additional business rules
- ✅ Describe view configuration (not custom views)
- ❌ Do NOT specify individual fields (they exist in AOS)
- ❌ Do NOT create custom entity

---

### EXTEND: Inherit from AOS and Add Custom Fields

**When**: Entity categorized as EXTEND in gap analysis

**Refinement Approach**:
- **Inherit all AOS fields** (reference documentation)
- **Specify ONLY additional custom fields** beyond AOS
- **Describe extension strategy** (how custom fields integrate)

**Example**:

```markdown
## Entity: Customer (EXTEND from AOS Partner)

### AOS Base Entity

- **AOS Entity**: Partner from axelor-base
- **Module**: com.axelor.apps.base
- **Documentation**: https://docs.axelor.com/aos/modules/base/partner.html

### Inherited Fields (Standard AOS)

The Customer entity inherits ALL standard Partner fields:
- code (Short text) - Partner code
- name (Short text) - Partner name
- partnerCategory (Relationship → PartnerCategory) - Category
- emailAddress (Short text) - Email address
- mobilePhone (Short text) - Mobile phone
- fixedPhone (Short text) - Fixed phone
- mainAddress (Relationship → Address) - Main address
- isCustomer (Yes/No) - Is customer flag
- isSupplier (Yes/No) - Is supplier flag
- currency (Relationship → Currency) - Default currency
- [... 30+ other standard Partner fields]

**See AOS documentation for complete field list.**

### Additional Custom Fields

**Beyond standard Partner, add**:

| Field | Nature | Required | Unique | Business Constraints | Description |
|-------|--------|----------|--------|----------------------|-------------|
| industry | Selection from list | No | No | TECHNOLOGY, FINANCE, HEALTHCARE, MANUFACTURING, RETAIL, SERVICES, OTHER | Industry sector classification |
| companySize | Whole number | No | No | Must be positive | Number of employees |
| tier | Selection from list | Yes | No | BRONZE, SILVER, GOLD, PLATINUM | Customer tier for pricing and service level |
| annualRevenue | Amount | No | No | Must be positive | Annual company revenue |
| contractStartDate | Date | No | No | Cannot be in the future | Contract start date with us |
| contractEndDate | Date | No | No | Must be after contractStartDate | Contract end date |
| accountManager | Short text | Yes | No | Must be valid user | Dedicated account manager |

**Total custom fields**: 7 (beyond 30+ AOS Partner fields)

### Extension Strategy

**Technical Approach** (for architect):
- Create custom entity: CustomPartner extends Partner
- Add 7 custom fields above
- Inherit all Partner views and services
- Extend form view with new panel "Customer Classification"
- Extend grid view to include tier column

**Functional Requirements**:
- All standard Partner functionality remains available
- Custom fields appear in dedicated "Customer Classification" panel in form view
- Tier field visible in grid view for quick filtering

### Business Rules

**Standard AOS Partner rules apply** (email format, phone format, address validation, etc.)

**Additional custom rules**:
- **Rule 1**: Tier is required for all customers (isCustomer = Yes)
- **Rule 2**: AccountManager must be assigned within 24 hours of customer creation
- **Rule 3**: ContractEndDate must be after contractStartDate
- **Rule 4**: When tier changes, system sends notification to accountManager

### Views Extension

**Form View**:
- Inherit standard AOS Partner form view
- Add new panel "Customer Classification" after "General Information" panel:
  - Row 1: tier (colSpan 4), industry (colSpan 4), companySize (colSpan 4)
  - Row 2: annualRevenue (colSpan 6), accountManager (colSpan 6)
  - Row 3: contractStartDate (colSpan 6), contractEndDate (colSpan 6)

**Grid View**:
- Inherit standard AOS Partner grid view
- Add columns: tier (after name), accountManager (before phone)

### Rationale for EXTEND

Why extend instead of REUSE or NEW:
- **Reuse not sufficient**: Need custom fields (tier, accountManager, etc.) not in standard Partner
- **New entity too complex**: Partner has 30+ standard fields we need (addresses, contacts, categories, etc.)
- **Extension optimal**: Get all standard Partner features + custom classification fields
```

**Key Points for EXTEND**:
- ✅ Reference AOS base entity and documentation
- ✅ List ALL custom fields (only those beyond AOS)
- ✅ Describe extension strategy (how to integrate)
- ✅ Specify view extensions (new panels, additional columns)
- ❌ Do NOT re-specify AOS fields (they are inherited)
- ❌ Do NOT create fully independent entity

---

### NEW: Create Custom Entity

**When**: Entity categorized as NEW in gap analysis OR no gap analysis exists

**Refinement Approach**:
- **Specify all fields completely** (no inheritance)
- **Define all relationships** from scratch
- **Full entity specification** as per standard refinement methodology

**Example**:

```markdown
## Entity: Delivery (NEW - No AOS equivalent)

### Business Role

Represents a delivery of goods to a customer. Tracks delivery status, scheduled date, actual date, and delivery notes.

### Rationale for NEW

No suitable AOS entity exists:
- StockMove is too technical (warehouse-focused)
- Sale order doesn't track delivery separately
- Custom delivery workflow required

### Fields

| Field | Nature | Required | Unique | Business Constraints | Description |
|-------|--------|----------|--------|----------------------|-------------|
| code | Short text | Yes | Yes | Auto-generated, pattern DEL-YYYY-NNNN | Unique delivery reference |
| customer | Short text | Yes | No | Must be valid customer | Customer receiving delivery |
| scheduledDate | Date | Yes | No | Cannot be in the past | Planned delivery date |
| actualDate | Date | No | No | Cannot be before scheduledDate | Actual delivery date |
| status | Selection from list | Yes | No | SCHEDULED, IN_TRANSIT, DELIVERED, CANCELLED | Current delivery status |
| address | Long text | Yes | No | Cannot be empty | Delivery address |
| driverName | Short text | No | No | - | Name of delivery driver |
| vehiclePlate | Short text | No | No | Valid plate format | Vehicle license plate |
| notes | Long text | No | No | - | Delivery instructions and notes |
| signatureAttachment | File attachment | No | No | Image or PDF | Recipient signature proof |

### Relationships

| Relationship | Type | Target Entity | Cardinality | Deletion Behavior | Description |
|--------------|------|---------------|-------------|-------------------|-------------|
| order | many-to-one | Order | 1..1 | Delivery deleted when Order deleted | Order being delivered |
| deliveryLines | one-to-many | DeliveryLine | 1..* | Lines deleted when Delivery deleted | Items in this delivery |

### Business Rules

- **Rule 1**: Code auto-generated following pattern DEL-YYYY-NNNN
- **Rule 2**: Status cannot go from DELIVERED back to IN_TRANSIT
- **Rule 3**: ActualDate is required when status = DELIVERED
- **Rule 4**: SignatureAttachment is required when status = DELIVERED
- **Rule 5**: Delivery cannot be cancelled if status = DELIVERED

### Workflow

**Statuses**: SCHEDULED → IN_TRANSIT → DELIVERED | CANCELLED

**Transitions**:
- SCHEDULED → IN_TRANSIT: When driver starts delivery
- IN_TRANSIT → DELIVERED: When customer receives and signs
- * → CANCELLED: At any time before DELIVERED

[... complete specification continues as per standard methodology]
```

**Key Points for NEW**:
- ✅ Specify ALL fields completely
- ✅ Define all relationships
- ✅ Complete business rules and workflow
- ✅ Full view specifications
- ✅ Rationale for why no AOS entity fits

---

## Module Dependencies

### Understanding AOS Modules

If gap analysis identifies AOS entities to REUSE or EXTEND, the architect will need to add module dependencies.

**Common AOS Modules**:

| Module | Description | Entities |
|--------|-------------|----------|
| axelor-base | Core entities | Partner, Product, Company, Currency, Address, etc. |
| axelor-sale | Sales management | SaleOrder, SaleOrderLine, Quotation, etc. |
| axelor-purchase | Purchase management | PurchaseOrder, PurchaseOrderLine, etc. |
| axelor-stock | Stock/inventory | StockMove, StockLocation, Inventory, etc. |
| axelor-account | Accounting | Invoice, Payment, Account, Journal, etc. |
| axelor-crm | CRM | Lead, Opportunity, Event, etc. |
| axelor-human-resource | HR | Employee, Leave, Timesheet, Expense, etc. |

**In functional specification, simply note**:

```markdown
## AOS Module Dependencies

Based on gap analysis, the following AOS modules are required:
- axelor-base (for Partner, Product entities)
- axelor-sale (for SaleOrder entity)

**Note for architect**: Add these dependencies to build.gradle
```

**The architect will handle** adding to build.gradle:

```gradle
dependencies {
  implementation('com.axelor:axelor-base:7.0.0')
  implementation('com.axelor:axelor-sale:7.0.0')
}
```

---

## Decision Guide: REUSE vs EXTEND vs NEW

When gap analysis is NOT available, use this guide to decide:

### Use REUSE When

- ✅ AOS entity has ALL needed fields
- ✅ AOS business logic matches your requirements 100%
- ✅ No custom fields needed
- ✅ Minor configuration can adapt AOS entity to your needs

**Example**: Using AOS Product for a simple e-commerce catalog

### Use EXTEND When

- ✅ AOS entity has MOST needed fields (70%+)
- ✅ Need 5-15 custom fields beyond AOS
- ✅ AOS business logic is useful but incomplete
- ✅ Want to leverage AOS integrations (Sale, Purchase, Stock, etc.)

**Example**: Extending AOS Partner to add industry, tier, account manager for B2B CRM

### Use NEW When

- ✅ No suitable AOS entity exists
- ✅ Business requirements very different from AOS entities
- ✅ Need complete control over all fields and logic
- ✅ Entity is domain-specific (not generic)

**Example**: Creating custom Delivery entity for specialized logistics workflow

---

## Example: Combining All Three Strategies

**Scenario**: Building a real estate CRM

**Entities**:

1. **Customer** → **EXTEND Partner**
   - Inherit: code, name, email, phone, addresses
   - Add custom: preferredPropertyType, budgetRange, investorType

2. **Property Listing** → **NEW**
   - No AOS equivalent (real estate specific)
   - Custom fields: address, price, sqft, bedrooms, bathrooms, listingDate

3. **Visit** → **NEW**
   - No AOS equivalent (real estate specific)
   - Custom fields: customer, property, visitDate, feedback, interested

4. **Company** → **REUSE Company**
   - AOS Company has all needed fields
   - Just configure: show/hide relevant fields

**In functional specification**:

```markdown
## 2. Data Model

### 2.1 Entity: Customer (EXTEND from AOS Partner)
[Complete EXTEND specification]

### 2.2 Entity: Property Listing (NEW)
[Complete NEW specification]

### 2.3 Entity: Visit (NEW)
[Complete NEW specification]

### 2.4 Entity: Company (REUSE from AOS)
[Configuration specification]

## AOS Module Dependencies

- axelor-base (for Partner, Company)
```

---

## Summary Checklist

When handling AOS integration in requirements refining:

- [ ] **Read gap analysis** (if exists) before starting Phase 2 (Entity Refining)
- [ ] **For REUSE entities**:
  - [ ] Reference AOS entity and documentation
  - [ ] Specify configuration requirements (show/hide fields, defaults)
  - [ ] Define additional business rules
  - [ ] Do NOT specify individual fields
- [ ] **For EXTEND entities**:
  - [ ] Reference AOS base entity
  - [ ] List ONLY custom fields (beyond AOS)
  - [ ] Describe extension strategy
  - [ ] Specify view extensions (new panels/columns)
  - [ ] Do NOT re-specify inherited AOS fields
- [ ] **For NEW entities**:
  - [ ] Specify ALL fields completely
  - [ ] Define all relationships
  - [ ] Complete business rules and workflow
  - [ ] Provide rationale for why no AOS entity fits
- [ ] **Document module dependencies** for architect

**Remember**: For REUSE/EXTEND, the architect has access to full AOS source code and documentation. You only need to specify:
- **What to configure** (for REUSE)
- **What to add** (for EXTEND)
- **Why this approach** (rationale)

---

This guide ensures efficient requirements refining that leverages AOS capabilities while clearly identifying custom development needs.
