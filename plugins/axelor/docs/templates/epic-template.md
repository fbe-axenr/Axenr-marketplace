# EPIC Structure Template (v2 - Markdown)

This template defines the standard structure for an EPIC in Axelor projects. Markdown format with integrated User Stories.

## Template

```markdown
# EPIC-XXX: [Business-oriented title]

## Objective

[Business value description - Why this EPIC is important]

## Target Users

- **[Role 1]**: [Expected benefit for this role]
- **[Role 2]**: [Expected benefit for this role]

## Overall Estimation

| Profile | Effort |
|---------|--------|
| Development | X days |
| QA/Tests | Y days |
| PM/BA | Z days |
| **Total** | **N days** |

### Calculation Detail

**Identified components:**
- [Component 1]: Dev Xh / QA Yh / PM Zh
- [Component 2]: Dev Xh / QA Yh / PM Zh

**Applied adjustment factors:**
- [Factor]: +X%

## EPIC Acceptance Criteria

- [ ] [Measurable business criterion 1]
- [ ] [Measurable business criterion 2]
- [ ] All User Stories completed
- [ ] Integration tests validated
- [ ] PO functional validation completed

---

## User Stories

### US-001: [Business value-oriented title]

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
| Dev | X h | [components: domain, view, service...] |
| QA | Y h | [planned test types] |
| PM/BA | Z h | [validation, documentation] |
| **Total** | **N h** | |

#### Dependencies

- Depends on: US-002 (reason)
- Blocks: US-005, US-006

---

### US-002: [Next title]

[Same structure...]

---

## EPIC Test Scenarios

### Scenario 1: Nominal path

1. [User action 1]
   - **Expected result**: [Observable]
2. [User action 2]
   - **Expected result**: [Observable]

### Scenario 2: Error handling

1. [Action causing an error]
   - **Expected result**: [Clear error message]

### Scenario 3: Edge case

1. [Edge situation]
   - **Expected result**: [Expected behavior]
```

---

## Guidelines

### EPIC Naming

- **Format**: Business-oriented title describing delivered value
- **Correct examples**:
  - "Product options management on quotes"
  - "Customer email synchronization"
  - "Sales dashboard"
- **To avoid**: Technical jargon or implementation details
  - ❌ "Create ProductOption domain"
  - ❌ "Implement synchronization service"

### Objective

The objective must answer:
- **What**: What business capability is delivered
- **Why**: What problem is solved
- **For whom**: Who benefits from this EPIC

**Good example**: "Enable sales representatives to automatically propose complementary products when creating quotes, thereby increasing average basket and reducing data entry time."

**Bad example**: "Create the ProductOption entity and associated views."

### Estimation with Profile Breakdown

Estimation must always include:

1. **Development**: Design + implementation + unit tests
2. **QA/Tests**: Functional tests + integration tests + test documentation
3. **PM/BA**: Specs validation + review + coordination

**Reference table**:

| Component | Dev | QA | PM/BA |
|-----------|-----|----|----|
| Simple domain (5-10 fields) | 1h | 0.5h | 0.25h |
| Complex domain (15+ fields) | 4h | 1.5h | 1h |
| Simple Grid view | 1h | 0.75h | 0.5h |
| Complex Grid view | 5h | 2h | 1h |
| Simple Form view | 1h | 0.75h | 0.25h |
| Complex Form view | 5h | 1.5h | 1h |
| Simple business service | 2h | 1h | 0.25h |
| Complex business service | 8h | 2.5h | 1h |
| Menu | 0.5h | 0.5h | 0h |

### User Stories - Writing Rules

#### The role must be a business user

**Correct**:
- Sales Representative
- Product Manager
- Stock Manager
- Accountant

**Incorrect**:
- ❌ Developer
- ❌ System Architect
- ❌ DBA
- ❌ Technical Admin

#### The action must describe what the user DOES

**Correct**: "I want to define default optional products"
**Incorrect**: ❌ "I want to create the ProductOption entity"

#### The benefit must be measurable

**Correct**: "So that I can reduce quote creation time by 30%"
**Incorrect**: ❌ "So that the system is improved"

### Acceptance Criteria - Given-When-Then Format

Each criterion must follow the format:

```
Given [context/precondition]
When [user action]
Then [observable result]
```

**Good example**:
```
Given a product with 3 configured options
When the sales representative adds this product to a quote
Then the 3 options are automatically proposed with their default quantities
```

**Bad example**:
```
Options should display correctly
```

### What MUST NOT appear in US

- ❌ XML, Java, SQL code
- ❌ Technical implementation details
- ❌ Database schemas
- ❌ Class or method names
- ❌ File paths

These elements belong in technical documentation, not User Stories.

---

## Output Structure

One single Markdown file per EPIC containing all its User Stories:

```
epic-us-breakdown/
├── EPIC-001-product-options-management.md
├── EPIC-002-quote-options-selection.md
└── EPIC-003-options-reporting.md
```

---

## Related Templates

- [User Story Template](user-story-template.md)

---

**Version**: 2.0 (Markdown, profile estimation, business value-oriented)
**Last Updated**: 2025-11-28
