---
name: functional-spec-consistency-checker
description: Validates functional specification documents for completeness, consistency, and absence of technical code. Ensures specifications use business types and remain purely functional.
---

# Functional Specification Consistency Checker

Validates that a functional specification document is:
- **Complete**: All required sections present
- **Consistent**: No logical contradictions
- **Purely functional**: No technical code (XML, Java, SQL)
- **Using business types**: No technical types (string, integer, decimal)

---

## Expected Input

Ask the user for the specification file path, or if invoked by requirements-refiner agent:
- **Input file**: Path to functional specification document (usually `{output_directory}/detailed-specifications.md`)

---

## Validation Checklist

### 1. Document Structure Validation

**Check presence of required sections**:

- [ ] Title and metadata (Project name, Version, Date, Status)
- [ ] Section 1: Overview (Business Objectives, Functional Scope, Target Users, Constraints)
- [ ] Section 2: Data Model (At least one entity defined)
- [ ] Section 3: Views and Interfaces (Form/Grid views for entities)
- [ ] Section 4: Features (At least one feature detailed)
- [ ] Section 5: Security and Permissions (Roles, permissions defined)
- [ ] Section 6: Cross-cutting Aspects (i18n, imports/exports, reporting)
- [ ] Section 7: Appendices (Glossary, use cases)
- [ ] Section 8: Validation (Checklist, signatures)

**Report missing sections** with severity: ERROR

---

### 2. Entity Completeness Validation

For each entity in Section 2:

- [ ] Entity has a description (business role)
- [ ] Entity has at least one field defined
- [ ] Each field has: Name, Nature, Required, Unique, Description
- [ ] Selection fields list ALL possible values
- [ ] Relationships specify: Type, Target Entity, Cardinality, Deletion Behavior
- [ ] Business rules are specified (if applicable)
- [ ] Workflow is specified for entities with status fields

**Report incomplete entities** with severity: ERROR

---

### 3. Business Types Validation

**Check that ALL fields use business types** (NOT technical types):

**✅ Allowed business types**:
- Short text
- Long text
- Whole number
- Decimal number
- Amount
- Yes/No
- Date
- Date and time
- File attachment
- Selection from list

**❌ Forbidden technical types** (report as ERROR if found):
- string, String, varchar, VARCHAR, CHAR, TEXT
- integer, Integer, int, INT, BIGINT, SMALLINT
- decimal, Decimal, DECIMAL, NUMERIC, FLOAT, DOUBLE
- boolean, Boolean, BOOLEAN, BIT
- datetime, timestamp, TIMESTAMP, DATE, TIME
- blob, BLOB, CLOB

**Validation process**:
1. Extract all field definitions from tables
2. Check "Nature" or "Type" column
3. If technical type found, report ERROR with:
   - Entity name
   - Field name
   - Found type (technical)
   - Suggestion: "Use business type instead (see @docs/requirements/business-types-reference.md)"

---

### 4. Technical Code Detection

**Search for forbidden technical code blocks**:

**❌ XML Code** (report as ERROR if found):
- `<entity name="...">` (domain definitions)
- `<field name="...">` or `<string name="...">` or `<integer name="...">` (field definitions)
- `<selection name="...">` (selection definitions)
- `<form name="...">` or `<grid name="...">` (view definitions)
- `<action-method name="...">` or `<action-view name="...">` (action definitions)
- Any other XML tags (except code examples in markdown code blocks showing WRONG approach)

**❌ Java Code** (report as ERROR if found):
- `public class` or `public interface` (class/interface definitions)
- `@Inject`, `@Transactional`, `@Service`, `@Repository` (Java annotations)
- `public void method()` or `public String method()` (method signatures)
- `import com.axelor` or `import java` (Java imports)
- Java method bodies with `{...}` containing actual implementation code

**❌ SQL Code** (report as ERROR if found):
- `CREATE TABLE` or `ALTER TABLE` (table definitions)
- `VARCHAR`, `INTEGER`, `NOT NULL`, `PRIMARY KEY` (SQL constraints)
- `INDEX`, `FOREIGN KEY`, `REFERENCES` (SQL structures)
- `SELECT`, `INSERT`, `UPDATE`, `DELETE` (SQL queries - except in examples)

**Exception**: Allow code blocks that are explicitly marked as "WRONG" or "Incorrect" examples.

**Validation process**:
1. Search document for code blocks (```xml, ```java, ```sql)
2. Analyze content of each code block
3. If block is not marked as "WRONG" or "INCORRECT", report ERROR
4. If block contains implementation code, report ERROR with:
   - Location (section, entity name)
   - Type of code (XML/Java/SQL)
   - Snippet (first 100 chars)
   - Message: "Functional specifications must NOT contain technical code. Remove this and describe functionally instead."

---

### 5. Technical Constraints Detection

**Search for technical database constraints**:

**❌ Forbidden technical constraints** (report as WARNING if found):
- VARCHAR(255), CHAR(64), TEXT (database types)
- Max 255 characters, Max 64 char (instead of business constraint)
- NOT NULL (instead of "Required: Yes")
- CHECK (amount > 0) (instead of "Must be positive")
- UNIQUE CONSTRAINT (instead of "Unique: Yes")
- FOREIGN KEY REFERENCES (instead of relationship description)

**✅ Allowed business constraints**:
- Must be a valid professional email
- Must be positive
- Cannot be in the past
- Must be after start date
- Required when status is VALIDATED
- Unique within the same company

**Validation process**:
1. Search for database-specific keywords in "Constraints" or "Business Constraints" columns
2. If found, report WARNING with suggestion to rephrase as business constraint

---

### 6. Relationship Consistency Validation

**Check bidirectional relationship consistency**:

For each relationship A → B:
- [ ] Check if reverse relationship B → A exists
- [ ] Verify cardinalities are consistent

**Examples of consistency**:
- Lead (many-to-one) → Company: Company should have (one-to-many) → Leads
- Order (one-to-many) → OrderLines: OrderLine should have (many-to-one) → Order
- Student (many-to-many) → Courses: Course should have (many-to-many) → Students

**Validation process**:
1. Extract all relationships from all entities
2. For each relationship A → B (many-to-one), check if B has A (one-to-many)
3. For each relationship A → B (one-to-many), check if B has A (many-to-one)
4. For each relationship A → B (many-to-many), check if B has A (many-to-many)
5. Report ERROR if bidirectional relationship is missing or inconsistent

---

### 7. Workflow Completeness Validation

For entities with status/workflow:

- [ ] All status values are listed
- [ ] All transitions are defined (from → to)
- [ ] No orphan statuses (every status reachable)
- [ ] Conditions for transitions are specified
- [ ] Terminal states are identified (e.g., CANCELLED, COMPLETED)

**Validation process**:
1. Identify entities with "status" field (Selection from list)
2. Extract all possible values
3. Extract all transitions
4. Build state machine graph
5. Check for unreachable states
6. Report ERROR if orphan states found

---

### 8. View Completeness Validation

For each entity:

- [ ] Form view is defined
- [ ] Grid view is defined
- [ ] Form view exposes all required fields
- [ ] Grid view exposes relevant fields for list/search
- [ ] Required fields are marked in form view

**Validation process**:
1. For each entity in Section 2, check if corresponding views exist in Section 3
2. For each required field, check if it appears in form view
3. Report WARNING if views are missing or incomplete

---

### 9. Security Validation

**Check security coverage**:

- [ ] User roles are defined
- [ ] Permission matrix covers all entities (Create, Read, Update, Delete)
- [ ] Specific security rules address edge cases
- [ ] Data privacy/PII is addressed (if applicable)

**Validation process**:
1. Extract list of entities from Section 2
2. Extract permission matrix from Section 5
3. Verify each entity appears in permission matrix
4. Report ERROR if entity missing from security

---

### 10. Feature Specification Validation

For each feature in Section 4:

- [ ] Feature has description
- [ ] Trigger is specified (Who, Where, When)
- [ ] Pre-conditions are listed
- [ ] Process steps are detailed
- [ ] Post-conditions are specified
- [ ] Validations are defined
- [ ] User messages are provided (success, errors, warnings)

**Validation process**:
1. For each feature, check presence of required subsections
2. Report WARNING if any subsection is missing or empty

---

## Validation Report Format

Generate a structured validation report:

```markdown
# Functional Specification Consistency Validation Report

**Specification File**: {file_path}
**Validation Date**: {date}
**Validation Status**: PASS | FAIL | WARNINGS

---

## Summary

| Category | Status | Errors | Warnings |
|----------|--------|--------|----------|
| Document Structure | PASS/FAIL | 0 | 0 |
| Entity Completeness | PASS/FAIL | 0 | 0 |
| Business Types | PASS/FAIL | 0 | 0 |
| Technical Code | PASS/FAIL | 0 | 0 |
| Technical Constraints | PASS/FAIL | 0 | 1 |
| Relationship Consistency | PASS/FAIL | 0 | 0 |
| Workflow Completeness | PASS/FAIL | 0 | 0 |
| View Completeness | PASS/FAIL | 0 | 2 |
| Security Coverage | PASS/FAIL | 0 | 0 |
| Feature Specifications | PASS/FAIL | 0 | 1 |

**Total Errors**: {count}
**Total Warnings**: {count}

---

## Details

### Document Structure Validation

✅ **PASS**: All required sections present

### Business Types Validation

❌ **FAIL**: 3 errors found

**Error 1**: Entity "Lead", field "email" uses technical type "string"
- **Location**: Section 2.1, Lead entity, email field
- **Found**: Type = "string"
- **Fix**: Change to business type "Short text"
- **Reference**: @docs/requirements/business-types-reference.md

**Error 2**: Entity "Order", field "totalAmount" uses technical type "decimal(19,2)"
- **Location**: Section 2.3, Order entity, totalAmount field
- **Found**: Type = "decimal(19,2)"
- **Fix**: Change to business type "Amount"
- **Reference**: @docs/requirements/business-types-reference.md

**Error 3**: Entity "Product", field "isActive" uses technical type "boolean"
- **Location**: Section 2.5, Product entity, isActive field
- **Found**: Type = "boolean"
- **Fix**: Change to business type "Yes/No"
- **Reference**: @docs/requirements/business-types-reference.md

### Technical Code Detection

❌ **FAIL**: 1 error found

**Error 1**: XML domain definition found in Section 2.1
- **Location**: Section 2.1, after Lead entity field table
- **Code snippet**: `<entity name="Lead"><integer name="statusSelect"...`
- **Fix**: Remove XML code. Describe status field functionally in the field table using business type "Selection from list" with possible values.
- **Rule**: Functional specifications must NOT contain XML domain definitions. The architect will create technical implementations.

### Relationship Consistency Validation

⚠️ **WARNING**: 1 warning found

**Warning 1**: Missing bidirectional relationship
- **Relationship**: Lead (many-to-one) → Company
- **Issue**: Company entity does not have reverse relationship (one-to-many) → Leads
- **Fix**: Add relationship in Company entity: leads (one-to-many) → Lead, cardinality 0..*

### Workflow Completeness Validation

✅ **PASS**: All workflows complete, no orphan states

### View Completeness Validation

⚠️ **WARNING**: 2 warnings found

**Warning 1**: Dashboard view missing for Lead entity
- **Issue**: Lead entity has no dashboard view defined in Section 3
- **Fix**: Consider adding dashboard view with KPIs (lead pipeline, conversion rate)

**Warning 2**: Required field "estimatedRevenue" not in form view
- **Entity**: Lead
- **Field**: estimatedRevenue (Required: Yes when status = QUALIFIED)
- **Issue**: Field not listed in form view panels
- **Fix**: Add estimatedRevenue field to "Sales Information" panel

---

## Recommendations

1. **Fix all ERRORS before proceeding** to architect phase
   - Replace all technical types with business types
   - Remove all XML/Java/SQL code blocks
   - Add missing reverse relationships

2. **Address WARNINGS** (optional but recommended)
   - Complete bidirectional relationships
   - Add missing views for better user experience
   - Ensure all required fields appear in forms

3. **Re-run validation** after fixes to verify PASS status

---

## Next Steps

- **IF PASS**: Specifications ready for architect agent
- **IF FAIL**: Fix errors and re-run skill
- **IF WARNINGS ONLY**: Can proceed but address warnings for completeness

**Command to fix and re-validate**:
```
1. Fix errors in specification document
2. Run: /skill functional-spec-consistency-checker
```

---

**Validation completed on {date} at {time}**
```

---

## Output Instructions

1. **Read the specification file** provided by user or agent
2. **Run all validation checks** (1-10)
3. **Generate validation report** in markdown format
4. **Return report** to user/agent
5. **Suggest fixes** for each error/warning with specific line numbers if possible

---

## Usage

**By user**:
```
/skill functional-spec-consistency-checker
```
Then provide file path when asked.

**By requirements-refiner agent**:
Agent automatically invokes this skill in Phase 6 (Consistency Validation) before finalizing the specification document.

---

This skill ensures functional specifications are ready for the architect agent to transform into technical implementation with confidence.
