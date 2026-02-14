# Business Types Reference for Functional Specifications

This document defines the business types to use when writing **functional specifications** for Axelor projects. These types are mapped to technical types by the architect agent.

---

## Business vs Technical Types Mapping

| Business Type | Description | Technical Mapping | Axelor XML Type | Examples |
|---------------|-------------|-------------------|-----------------|----------|
| **Short text** | Brief text field (single line) | string(255) | `<string name="..." />` | Name, Code, Email, Phone, Reference |
| **Long text** | Extended text field (multi-line) | text/clob | `<string name="..." large="true" />` | Description, Notes, Comments, Address |
| **Whole number** | Integer value (no decimals) | integer | `<integer name="..." />` | Quantity, Count, Age, Year, Index |
| **Decimal number** | Numeric value with decimals | decimal | `<decimal name="..." />` | Percentage, Rate, Ratio, Score |
| **Amount** | Monetary value (currency) | decimal(19,2) | `<decimal name="..." precision="19" scale="2" />` | Price, Total, Discount, Tax, Salary |
| **Yes/No** | Boolean value (true/false) | boolean | `<boolean name="..." />` | Active, Enabled, Approved, Sent, Archived |
| **Date** | Date only (no time) | date | `<date name="..." />` | BirthDate, DueDate, StartDate, EndDate |
| **Date and time** | Date with time | datetime | `<datetime name="..." />` | CreatedOn, ModifiedOn, SentAt, ValidatedAt |
| **File attachment** | Uploaded file reference | many-to-one MetaFile | `<many-to-one name="..." ref="com.axelor.meta.db.MetaFile" />` | Document, Photo, Contract, Invoice |
| **Selection from list** | Closed list of values (enum) | integer + selection | `<integer name="..." selection="..." />` | Status, Type, Priority, Category |

---

## When to Use Each Type

### Short Text
Use for brief identifiers, names, codes, or short descriptive text:
- **Examples**: Customer name, Product code, Email address, Phone number, City name
- **Business constraints**: "Must be unique", "Valid email format", "Alphanumeric only"
- **Avoid**: Long descriptions (use Long text instead)

### Long Text
Use for extended descriptions, notes, or multi-paragraph text:
- **Examples**: Product description, Meeting notes, Terms and conditions, Address
- **Business constraints**: "Cannot be empty", "Maximum 5000 characters"
- **Avoid**: Single-word or short values (use Short text)

### Whole Number
Use for countable items or integer values:
- **Examples**: Quantity ordered, Number of employees, Age, Stock level
- **Business constraints**: "Must be positive", "Between 0 and 100", "Cannot be negative"
- **Avoid**: Values with decimals (use Decimal number or Amount)

### Decimal Number
Use for percentages, rates, ratios, or non-monetary decimals:
- **Examples**: Discount percentage (10.5%), Tax rate (0.20), Performance score (3.75)
- **Business constraints**: "Between 0 and 100", "Maximum 2 decimal places", "Must be positive"
- **Avoid**: Monetary values (use Amount instead)

### Amount
Use ONLY for monetary values (prices, totals, costs):
- **Examples**: Unit price, Total amount, Discount amount, Tax amount, Salary
- **Business constraints**: "Must be positive", "Cannot exceed budget", "Required for invoicing"
- **Always specify**: Currency (EUR, USD, etc.) as separate field or context

### Yes/No
Use for binary states or flags:
- **Examples**: Is active, Is validated, Has attachment, Is sent, Is archived
- **Business constraints**: "Defaults to No", "Cannot be changed after validation"
- **Naming convention**: Use "is" prefix (isActive, isValidated)

### Date
Use for date-only values (no time component):
- **Examples**: Birth date, Due date, Start date, End date, Invoice date
- **Business constraints**: "Cannot be in the past", "Must be after start date", "Required"
- **Avoid**: When time is important (use Date and time)

### Date and Time
Use when both date AND time are important:
- **Examples**: Created on, Modified on, Sent at, Validated at, Meeting time
- **Business constraints**: "Automatically set on creation", "Cannot be modified", "Must be in the future"
- **Use**: For audit trails, timestamps, scheduled events

### File Attachment
Use for uploaded files or documents:
- **Examples**: Contract document, Product photo, Invoice PDF, User avatar
- **Business constraints**: "Required for validation", "Maximum 10 MB", "PDF format only"
- **Note**: Usually implemented as many-to-one relationship to MetaFile entity

### Selection from List
Use for closed lists of predefined values:
- **Examples**: Status (NEW, IN_PROGRESS, COMPLETED), Priority (LOW, MEDIUM, HIGH), Type (A, B, C)
- **Business constraints**: "Defaults to NEW", "Cannot change from COMPLETED to IN_PROGRESS"
- **Always list**: ALL possible values in specification

---

## Examples in Functional Specifications

### Correct Usage

```markdown
#### Fields

| Field | Nature | Required | Unique | Business Constraints | Description |
|-------|--------|----------|--------|----------------------|-------------|
| code | Short text | Yes | Yes | Unique identifier, alphanumeric | Order reference code |
| customerName | Short text | Yes | No | Cannot be empty | Customer full name |
| description | Long text | No | No | Maximum 5000 characters | Order description and notes |
| quantity | Whole number | Yes | No | Must be positive, minimum 1 | Number of items ordered |
| discountRate | Decimal number | No | No | Between 0 and 100 | Discount percentage |
| totalAmount | Amount | Yes | No | Must be positive | Total order amount in EUR |
| isValidated | Yes/No | Yes | No | Defaults to No | Validation status |
| orderDate | Date | Yes | No | Cannot be in the future | Order placement date |
| createdAt | Date and time | Yes | No | Auto-set on creation | Record creation timestamp |
| status | Selection from list | Yes | No | NEW, CONFIRMED, SHIPPED, DELIVERED, CANCELLED | Current order status |
| attachment | File attachment | No | No | PDF format, max 10 MB | Order confirmation document |
```

### Incorrect Usage (Technical Types)

```markdown
<!-- ❌ WRONG - Using technical types -->

| Field | Type | Constraints |
|-------|------|-------------|
| code | string(64) | NOT NULL, UNIQUE |
| totalAmount | decimal(19,2) | NOT NULL, CHECK (total_amount > 0) |
| isValidated | boolean | DEFAULT false |
| status | integer | REFERENCES selection |
```

**Why wrong?** This uses technical database types (string, decimal, boolean, integer) instead of business types. The architect will handle the technical mapping.

---

## Special Cases

### Computed/Calculated Fields

For fields that are calculated from other fields:

```markdown
#### Field: totalAmount
- **Nature**: Amount (calculated)
- **Required**: Yes (auto-calculated)
- **Business Constraints**: Always equals sum of line amounts
- **Calculation Rule**: totalAmount = SUM(orderLines.lineAmount)
- **Description**: Total order amount computed from order lines
```

### Multi-valued Fields

For fields that can have multiple values:

```markdown
#### Field: tags
- **Nature**: Multiple selections from list
- **Required**: No
- **Possible Values**: URGENT, CONFIDENTIAL, ARCHIVED, VIP, CRITICAL
- **Business Constraints**: Can select multiple tags
- **Description**: Classification tags for the record
```

### Reference Fields (Relationships)

Relationships are NOT described as field types but in the Relationships section:

```markdown
#### Relationships

| Relationship | Type | Target Entity | Cardinality | Description |
|--------------|------|---------------|-------------|-------------|
| customer | many-to-one | Customer | 1..1 | Customer who placed the order |
| orderLines | one-to-many | OrderLine | 0..* | Items included in this order |
```

---

## Validation Rules

When specifying business constraints, use business language:

### Good Business Constraints

✅ "Must be a valid professional email address"
✅ "Must be positive and greater than zero"
✅ "Cannot be in the past"
✅ "Must be after start date"
✅ "Required when status is VALIDATED"
✅ "Maximum 5000 characters"
✅ "Unique within the same company"

### Bad Technical Constraints

❌ "VARCHAR(255)"
❌ "CHECK (amount > 0)"
❌ "NOT NULL"
❌ "FOREIGN KEY REFERENCES"
❌ "INDEX idx_code"
❌ "@Column(length=255, nullable=false)"

---

## Summary

**For Requirements Refiner Agent**:
- ✅ Use ONLY business types from this reference
- ✅ Describe business constraints in business language
- ✅ Focus on WHAT the field represents, not HOW it's implemented

**For Architect Agent**:
- Will map business types → technical types
- Will add database constraints (NOT NULL, CHECK, etc.)
- Will create proper XML domain definitions
- Will design indexes and optimizations

This separation ensures clean functional specifications that the architect can properly transform into technical implementation.
