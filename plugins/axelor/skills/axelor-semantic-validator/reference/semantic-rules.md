# Axelor Domain Semantic Validation Rules

Consolidated semantic rules for domain validation.

## Inter-Attribute Validation

### Rule 1: Scale ≤ Precision

For `<decimal>` fields:

```xml
<!-- ERROR: scale > precision -->
<decimal name="amount" precision="10" scale="15"/>

<!-- VALID -->
<decimal name="amount" precision="20" scale="3"/>
```

**Rule**: `scale` must be ≤ `precision`

### Rule 2: Required + Default Conflict

Cannot combine `required="true"` with `default` attribute:

```xml
<!-- ERROR: conflicting attributes -->
<string name="code" required="true" default="AUTO"/>

<!-- VALID: choose one -->
<string name="code" required="true"/>
<string name="code" default="AUTO"/>
```

**Rule**: Fields cannot be both required and have a default value

## Cross-Entity Validation

### Rule 3: Ref Target Exists

All relationship `ref` attributes must point to existing entities:

```xml
<!-- ERROR: Company entity not found -->
<many-to-one name="company" ref="com.example.db.Company"/>

<!-- VALID: entity exists -->
<many-to-one name="company" ref="com.axelor.apps.base.db.Company"/>
```

**Rule**: `ref` must point to existing entity (simple name or fully qualified)

### Rule 4: MappedBy Field Exists

For `<one-to-many>`, the `mappedBy` field must exist in target entity:

```xml
<!-- In Order.xml -->
<one-to-many name="lines" ref="OrderLine" mappedBy="order"/>

<!-- OrderLine.xml MUST have field named "order" -->
<many-to-one name="order" ref="Order"/>
```

**Rule**: `mappedBy` field name must exist in target entity

### Rule 5: MappedBy Field Type

The `mappedBy` field must be `<many-to-one>` type:

```xml
<!-- In Order.xml -->
<one-to-many name="lines" ref="OrderLine" mappedBy="orderRef"/>

<!-- ERROR: orderRef is string, not many-to-one -->
<string name="orderRef"/>

<!-- VALID: must be many-to-one -->
<many-to-one name="orderRef" ref="Order"/>
```

**Rule**: `mappedBy` must point to `<many-to-one>` field

## Best Practices (Warnings)

### Warning 1: Email Without Unique

Email fields should have `unique="true"`:

```xml
<!-- WARNING: email without unique constraint -->
<string name="email"/>

<!-- BETTER -->
<string name="email" unique="true"/>
```

### Warning 2: Lines Without OrderBy

Line entities should specify `orderBy`:

```xml
<!-- WARNING: unpredictable order -->
<one-to-many name="orderLines" ref="OrderLine" mappedBy="order"/>

<!-- BETTER -->
<one-to-many name="orderLines" ref="OrderLine"
  mappedBy="order" orderBy="sequence"/>
```

### Warning 3: Composition Without Cascade

Parent-child composition should have cascade settings:

```xml
<!-- WARNING: lines won't be deleted with order -->
<one-to-many name="lines" ref="OrderLine" mappedBy="order"/>

<!-- BETTER for composition -->
<one-to-many name="lines" ref="OrderLine"
  mappedBy="order" cascade="all" orphanRemoval="true"/>
```

### Warning 4: Many-to-One Without Title

Many-to-one fields should have `title` for better UX:

```xml
<!-- WARNING: no UI label -->
<many-to-one name="company" ref="Company"/>

<!-- BETTER -->
<many-to-one name="company" ref="Company" title="Company"/>
```

## Validation Priority

1. **CRITICAL (Errors)**: Inter-attribute logic, missing entities, wrong field types
2. **RECOMMENDED (Warnings)**: Best practices for maintainability and UX

## Complementary with XSD Validation

**XSD Validator** handles syntactic validation:
- Element existence
- Attribute validity
- Required attributes
- Type correctness

**Semantic Validator** handles logic validation:
- Inter-attribute relationships
- Cross-entity coherence
- Best practices

Use both for complete validation coverage.
