---
name: axelor-naming-checker
description: Checks Axelor naming conventions for entities, fields, packages, and tables. Enforces PascalCase, camelCase, and snake_case standards. Use to verify code follows Axelor conventions.
user-invocable: false
---

# Axelor Naming Convention Checker

**⚠️ SKILL TYPE: INSTRUCTION-ONLY (No Python automation)**

This skill provides instructions to follow manually. There is no Python script to execute.

## Mission

Verify that all code elements follow Axelor naming conventions.

## Naming Conventions

### Entities
- **Format**: PascalCase
- **Pattern**: `^[A-Z][a-zA-Z0-9]*$`
- **Examples**:
  - ✅ `Customer`
  - ✅ `SaleOrder`
  - ✅ `OrderLine`
  - ❌ `customer` (lowercase)
  - ❌ `sale_order` (snake_case)

### Fields
- **Format**: camelCase
- **Pattern**: `^[a-z][a-zA-Z0-9]*$`
- **Examples**:
  - ✅ `name`
  - ✅ `orderDate`
  - ✅ `totalAmount`
  - ❌ `Name` (PascalCase)
  - ❌ `order_date` (snake_case)

### Packages
- **Format**: `com.axelor.apps.{module}.{layer}`
- **Layers**: `db`, `service`, `repo`, `web`, `exception`
- **Examples**:
  - ✅ `com.axelor.apps.crm.db`
  - ✅ `com.axelor.apps.sale.service`
  - ❌ `com.mycompany.crm.db` (wrong root)

### Tables (Database)
- **Rule**: DO NOT specify `table=""` unless entity name is a Hibernate reserved word
- **AOP auto-generates**: `SaleOrder` → `sale_order`, `ProductCategory` → `product_category`
- **Reserved words requiring explicit table**: `User`, `Order`, `Group`, `Key`, `Index`, `Table`, `Column`
- **Examples**:
  - ✅ `<entity name="SaleOrder">` (no table attribute - CORRECT)
  - ✅ `<entity name="User" table="auth_user">` (reserved word - CORRECT)
  - ❌ `<entity name="SaleOrder" table="sale_order">` (unnecessary table)
  - ❌ `<entity name="Customer" table="crm_customer">` (unnecessary table)

### Constants
- **Format**: UPPER_SNAKE_CASE
- **Pattern**: `^[A-Z][A-Z0-9_]*$`
- **Examples**:
  - ✅ `STATUS_DRAFT`
  - ✅ `MAX_ITEMS`
  - ❌ `statusDraft` (camelCase)

### Methods (Java)
- **Format**: camelCase
- **Prefix**: `get`, `set`, `is`, `has`, `compute`, `validate`
- **Examples**:
  - ✅ `getName()`
  - ✅ `setOrderDate()`
  - ✅ `computeTotalAmount()`
  - ✅ `validateOrder()`
  - ❌ `GetName()` (PascalCase)

## Validation Process

1. Check entity names → PascalCase
2. Check field names → camelCase
3. Check package structure → com.axelor.apps.*
4. Check table attribute → SHOULD NOT be specified (unless reserved word)
5. Check constants → UPPER_SNAKE_CASE
6. Check method names → camelCase with appropriate prefix

## Output Format

```
✅ CONVENTIONS FOLLOWED | ❌ VIOLATIONS FOUND

Entity: Customer
✅ Entity name valid: PascalCase
✅ Package valid: com.axelor.apps.crm.db

Fields:
✅ customerName: camelCase
❌ CustomerEmail: should be camelCase (customerEmail)
❌ phone_number: should be camelCase (phoneNumber)

Table:
✅ No table attribute (CORRECT - AOP will auto-generate)

Entity: User
✅ Entity name valid: PascalCase
✅ Table attribute specified for reserved word: auth_user (CORRECT)

Entity: SaleOrder
❌ Unnecessary table attribute: table="sale_order" (REMOVE IT - AOP auto-generates)
```

## Common Violations

**Entity name:**
```xml
<!-- ❌ WRONG -->
<entity name="customer">  <!-- lowercase -->

<!-- ✅ CORRECT -->
<entity name="Customer">
```

**Field name:**
```xml
<!-- ❌ WRONG -->
<string name="CustomerName"/>  <!-- PascalCase -->
<string name="customer_name"/>  <!-- snake_case -->

<!-- ✅ CORRECT -->
<string name="customerName"/>
```

**Package:**
```xml
<!-- ❌ WRONG -->
<module package="com.mycompany.crm.db"/>

<!-- ✅ CORRECT -->
<module package="com.axelor.apps.crm.db"/>
```

**Table attribute (CRITICAL):**
```xml
<!-- ❌ WRONG - Unnecessary table specification -->
<entity name="SaleOrder" table="sale_order">
<entity name="Customer" table="crm_customer">
<entity name="OptionalProductTemplate" table="optionalproduct_optional_product_template">

<!-- ✅ CORRECT - No table attribute (AOP auto-generates) -->
<entity name="SaleOrder">
<entity name="Customer">
<entity name="OptionalProductTemplate">

<!-- ✅ CORRECT - Table ONLY for Hibernate reserved words -->
<entity name="User" table="auth_user">
<entity name="Order" table="sale_order">
```
