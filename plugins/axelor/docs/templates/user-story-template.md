# User Story Template (v2 - Markdown, Given-When-Then)

This template defines the standard structure for User Stories in Axelor projects. Business value-oriented format with Given-When-Then criteria.

## Template

```markdown
### US-XXX: [Business value-oriented title]

**As a** [business role - end user]
**I want** [desired action/capability]
**So that** [measurable benefit for the user]

#### Acceptance Criteria

1. **Given** [initial context / precondition]
   **When** [user action]
   **Then** [observable and measurable result]

2. **Given** [other context]
   **When** [other action]
   **Then** [other result]

3. **Given** [error context]
   **When** [erroneous action]
   **Then** [explicit error message]

#### Estimation

| Profile | Effort | Justification |
|---------|--------|---------------|
| Dev | X h | [involved components] |
| QA | Y h | [test types] |
| PM/BA | Z h | [validation, doc] |
| **Total** | **N h** | |

#### Dependencies

- Depends on: US-YYY (reason)
- Blocks: US-ZZZ
```

---

## Guidelines

### User Story Title

- **Format**: Value-oriented, describes user benefit
- **Correct examples**:
  - "Automatically propose product options on a quote"
  - "View summary of selected options"
  - "Configure default option quantities"
- **Incorrect examples**:
  - ❌ "Create ProductOption domain"
  - ❌ "Implement Grid view"
  - ❌ "Add calculation service"

### User Story Statement

#### The role (As a...)

Must be a **business user**, not a technical profile.

| Correct | Incorrect |
|---------|-----------|
| Sales Representative | ❌ Developer |
| Product Manager | ❌ Architect |
| Stock Manager | ❌ DBA |
| Accountant | ❌ System Admin |
| Buyer | ❌ DevOps |

#### The action (I want...)

Describes what the user **does**, not what is being developed.

| Correct | Incorrect |
|---------|-----------|
| Define default options for my products | ❌ Create ProductOption entity |
| See available options on a quote | ❌ Display options Grid view |
| Modify option quantity | ❌ Implement update service |

#### The benefit (So that...)

Must be **measurable** and **business-oriented**.

| Correct | Incorrect |
|---------|-----------|
| Reduce data entry time by 30% | ❌ Improve the system |
| Increase average basket | ❌ Have better UX |
| Avoid configuration errors | ❌ Follow best practices |

---

### Acceptance Criteria - Given-When-Then Format

Each acceptance criterion must follow the structure:

```
Given [context/precondition]
When [user action]
Then [observable result]
```

#### Examples by Type

**Standard functionality:**
```markdown
1. **Given** a "Laptop" product with 3 configured options (mouse, bag, warranty extension)
   **When** the sales representative adds this product to a new quote
   **Then** the 3 options automatically appear in the "Proposed Options" section with their default quantities
```

**Business validation:**
```markdown
2. **Given** an option with default quantity = 2 and "multiply by line quantity" enabled
   **When** the sales representative modifies the main product quantity to 5
   **Then** the option quantity is automatically recalculated to 10 (2 × 5)
```

**Error handling:**
```markdown
3. **Given** a quote in "Validated" status
   **When** the sales representative tries to add a new option
   **Then** an error message displays: "Cannot modify a validated quote"
```

**Edge case:**
```markdown
4. **Given** a product with no configured options
   **When** the sales representative adds this product to a quote
   **Then** the "Proposed Options" section does not appear (no empty section)
```

#### What to Avoid

```markdown
❌ Bad examples:

- "Options should display correctly"
  → No Given/When/Then, not measurable

- "User can modify options"
  → Too vague, no context

- "System must save data in the sale_order_line_option table"
  → Technical detail, not user-oriented
```

---

### Estimation with Profile Breakdown

Each estimation must detail effort by profile:

| Profile | Effort | Justification |
|---------|--------|---------------|
| **Dev** | X h | Components: domain, view, service... |
| **QA** | Y h | Test types: functional, integration... |
| **PM/BA** | Z h | Specs validation, coordination, documentation |
| **Total** | **N h** | |

#### Reference Table

| Component | Dev | QA | PM/BA | Notes |
|-----------|-----|----|----|-------|
| Simple domain (5-10 fields) | 1h | 0.5h | 0.25h | Unit tests included |
| Complex domain (15+ fields) | 4h | 1.5h | 1h | Validations included |
| Simple Grid view | 1h | 0.75h | 0.5h | |
| Complex Grid view | 5h | 2h | 1h | Advanced filters |
| Simple Form view | 1h | 0.75h | 0.25h | |
| Complex Form view | 5h | 1.5h | 1h | Tabs, widgets |
| Simple business service | 2h | 1h | 0.25h | |
| Complex business service | 8h | 2.5h | 1h | Workflow, integrations |
| Menu | 0.5h | 0.5h | 0h | |

#### Adjustment Factors

| Factor | Multiplier | When to Apply |
|--------|------------|---------------|
| Unit tests | Dev +30% | Complex services |
| Integration tests | QA +50% | Workflows |
| Documentation | PM/BA +20% | Complex features |
| Legacy/Tech debt | Dev +25% | Existing code |
| Uncertainty | All +20% | Unclear specs |

#### Calculation Example

```markdown
### US-003 Estimation Detail

**Identified components:**
- 1× Complex domain (ProductOption, 12 fields)
- 1× Complex Form view with tab

**Calculation:**

| Component | Dev | QA | PM/BA |
|-----------|-----|----|----|
| Complex domain | 4h | 1.5h | 1h |
| Complex form | 5h | 1.5h | 1h |
| **Subtotal** | 9h | 3h | 2h |
| Unit tests (+30% Dev) | +2.7h | - | - |
| **Total** | 11.7h | 3h | 2h |

**Total effort:** 16.7h ≈ 2 days
```

---

### Dependencies

#### Types of Dependencies

1. **Functional**: A US requires another to be completed
   - "Depends on: US-001 (options configuration needed before selection)"

2. **Blocking**: This US blocks other US
   - "Blocks: US-005, US-006 (summary uses selected options)"

#### Notation

```markdown
#### Dependencies

- Depends on: US-002 (product options configuration must be available)
- Blocks: US-005 (summary requires selected options)
- Blocks: US-006 (PDF export includes options)
```

If no dependency:
```markdown
#### Dependencies

None
```

---

## What MUST NOT Appear in a User Story

### Technical Elements to Exclude

- ❌ XML, Java, SQL code
- ❌ Database schemas
- ❌ Class or method names
- ❌ File paths
- ❌ Technical configurations
- ❌ API details

These elements belong in **technical documentation**, not User Stories.

### Transformation Example

**Before (too technical):**
```
As a system architect
I want to create the ProductOption domain entity with fields:
  - product (many-to-one, required)
  - optionalProduct (many-to-one, required)
  - defaultQuantity (decimal, precision 20, scale 10)
So that the data model supports product options

Technical Details:
- Path: src/main/resources/domains/ProductOption.xml
- Package: com.axelor.sale.db
- Index: idx_product_option on (product, optionalProduct)
```

**After (business-oriented):**
```markdown
### US-001: Configure default optional products

**As a** product manager
**I want** to define which products can be offered as options with a main product
**So that** sales representatives can automatically propose relevant accessories

#### Acceptance Criteria

1. **Given** a "Laptop" product
   **When** I configure "Wireless Mouse" as an option with default quantity 1
   **Then** this option appears in the product's options list

2. **Given** an already configured option for a product
   **When** I try to add the same option a second time
   **Then** an error message indicates that this option already exists

3. **Given** multiple options configured for a product
   **When** I modify the options order
   **Then** the order is saved and respected when displayed on quotes
```

---

## INVEST Criteria Checklist

Before validating a User Story, check that it meets INVEST:

- [ ] **I - Independent**: Can be developed independently
- [ ] **N - Negotiable**: Details can be discussed (AC focus on "what", not "how")
- [ ] **V - Valuable**: Provides business value (explicit "So that" clause)
- [ ] **E - Estimable**: Can be estimated precisely (effort by profile provided)
- [ ] **S - Small**: Achievable in a sprint (≤ 16 hours / ≤ 2 days)
- [ ] **T - Testable**: Measurable acceptance criteria (Given-When-Then)

---

## Related Templates

- [EPIC Template](epic-template.md)

---

**Version**: 2.0 (Markdown, Given-When-Then, profile estimation)
**Last Updated**: 2025-11-28
