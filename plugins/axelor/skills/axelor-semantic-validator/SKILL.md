---
name: axelor-semantic-validator
description: Validates domain semantic coherence - inter-attribute logic, cross-entity relationships, and best practices. Use after XSD validation for semantic checks.
user-invocable: false
---

# Axelor Semantic Validator

**✅ PYTHON AUTOMATION AVAILABLE: `semantic_validator.py`**

Use this Python script for automated semantic validation. See Usage section below.

## Mission

Validate domain semantic coherence and cross-entity relationship integrity.

## Scope

This validator focuses on semantic validation NOT covered by XSD:
- Inter-attribute logic (scale ≤ precision, conflicts)
- Cross-entity validation (ref targets exist, mappedBy coherence)
- Bidirectional relationship consistency
- Best practices warnings

**Note**: Basic syntax validation (allowed attributes, required attributes) is handled by XSD validator.

## Embedded Documentation

@skills/axelor-semantic-validator/reference/semantic-rules.md - Semantic validation rules

## Validation Categories

### 1. Inter-Attribute Validation

**Scale vs Precision**:
```xml
<!-- ERROR: scale > precision -->
<decimal name="amount" precision="10" scale="15"/>

<!-- VALID -->
<decimal name="amount" precision="20" scale="3"/>
```

**Required + Default Conflict**:
```xml
<!-- ERROR: cannot be both required and have default -->
<string name="code" required="true" default="AUTO"/>

<!-- VALID: choose one -->
<string name="code" required="true"/>
```

### 2. Cross-Entity Validation

**Ref Target Exists**:
- many-to-one `ref` must point to existing entity
- one-to-many `ref` must point to existing entity
- many-to-many `ref` must point to existing entity

**MappedBy Field Exists**:
```xml
<!-- In Order.xml -->
<one-to-many name="lines" ref="OrderLine" mappedBy="order"/>

<!-- OrderLine.xml MUST have field named "order" -->
<many-to-one name="order" ref="Order"/>
```

### 3. Bidirectional Coherence

**mappedBy Field Type**:
- one-to-many mappedBy must point to many-to-one field
- Field name must match exactly

**Reverse Reference**:
- many-to-one target must match parent entity

### 4. Best Practices Warnings

- Email fields without `unique="true"`
- one-to-many lines without `orderBy` attribute
- Composition without `cascade="all"` and `orphanRemoval="true"`
- Many-to-one without `title` attribute

## Output Format

Token-optimized, concise, no emojis:

```
SEMANTIC VALIDATION: Customer.xml

ERRORS: 2
  Line 23, decimal "amount"
    scale (15) > precision (10)

  Line 45, one-to-many "lines"
    mappedBy="order" but CustomerLine has field "customer" not "order"

WARNINGS: 1
  Line 18, string "email"
    Consider unique="true" for email fields

SUMMARY:
- Fields checked: 12
- Errors: 2
- Warnings: 1
- Status: FAILED
```

## Cross-Entity Validation Process

1. **Scan all domain XMLs** in directory
2. **Build entity index**: {entity_name: {fields, package}}
3. **For each relationship field**:
   - Verify ref target exists
   - For one-to-many: verify mappedBy field exists and is correct type
   - Check bidirectional coherence
4. **Report issues** with line numbers and suggestions

## Usage

The skill automatically invokes Python automation:

```bash
# Validate entire domains directory
python3 semantic_validator.py src/main/resources/domains/

# Validate specific file (with context of all domains)
python3 semantic_validator.py Customer.xml
```

## Integration with Workflow

Called by `domain-agent` agent in Step 3:

```
Generate XML
  ↓
axelor-xml-validator (XSD strict validation)
  ↓
axelor-naming-checker (naming conventions)
  ↓
axelor-semantic-validator (semantic + cross-entity) ← THIS SKILL
  ↓
./gradlew generateCode
```

## Complementary with XSD Validator

**XSD Validator handles**:
- Element existence
- Attribute validity per element type
- Required attribute presence
- Attribute type correctness

**Semantic Validator handles**:
- Inter-attribute logic (scale ≤ precision)
- Attribute value conflicts (required + default)
- Cross-entity references (ref targets exist)
- Bidirectional coherence (mappedBy correctness)
- Best practices warnings

No redundancy - each validator has distinct role.
