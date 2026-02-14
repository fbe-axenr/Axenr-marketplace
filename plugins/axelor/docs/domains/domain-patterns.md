# Domain Patterns Guide

Advanced patterns for relationships, enumerations, sequences, tracking, and computed fields in Axelor domains.

> **Prerequisites**: See @docs/domains/domain-reference.md for basic syntax and field types
> **Real Examples**: See @docs/domains/examples/ for tested patterns from Axelor Open Suite

## Table of Contents

1. [Relationship Patterns](#relationship-patterns)
2. [Cascade and Orphan Removal](#cascade-and-orphan-removal)
3. [Bidirectional Relationships](#bidirectional-relationships)
4. [Enumerations](#enumerations)
5. [Sequences](#sequences)
6. [Change Tracking](#change-tracking)
7. [Computed Fields](#computed-fields)
8. [Common Domain Patterns](#common-domain-patterns)

## Relationship Patterns

### Many-to-One Best Practices

**Standard Reference:**
```xml
<entity name="SaleOrder">
  <many-to-one name="customer" ref="com.axelor.apps.base.db.Partner"
    title="Customer" required="true"/>
</entity>
```

**Database:** Creates foreign key column `customer_id` in `sale_order` table.

**Multiple References:**
```xml
<entity name="SaleOrder">
  <many-to-one name="customer" ref="Partner" title="Customer" required="true"/>
  <many-to-one name="currency" ref="Currency" title="Currency" required="true"/>
  <many-to-one name="priceList" ref="PriceList" title="Price List"/>
  <many-to-one name="paymentMode" ref="PaymentMode" title="Payment Mode"/>
</entity>
```

**Self-Referencing:**
```xml
<entity name="Category">
  <string name="name" title="Name"/>
  <many-to-one name="parentCategory" ref="Category" title="Parent Category"/>
  <one-to-many name="childCategoryList" ref="Category" mappedBy="parentCategory"/>
</entity>
```

> **Warning**: Self-referencing requires cycle prevention logic in service layer

### One-to-Many Best Practices

**Master-Detail Pattern:**
```xml
<!-- Master -->
<entity name="SaleOrder">
  <string name="orderNumber"/>
  <one-to-many name="orderLineList" ref="SaleOrderLine"
    mappedBy="saleOrder" title="Order Lines"
    cascade="all" orphanRemoval="true" orderBy="sequence"/>
</entity>

<!-- Detail -->
<entity name="SaleOrderLine">
  <integer name="sequence" default="0"/>
  <many-to-one name="saleOrder" ref="SaleOrder" required="true"/>
  <many-to-one name="product" ref="Product" title="Product" required="true"/>
  <decimal name="quantity" precision="10" scale="2" required="true"/>
  <decimal name="price" precision="10" scale="2" required="true"/>
</entity>
```

**Key Rules:**
1. Always use `mappedBy` pointing to many-to-one field in child entity
2. Add `orderBy` for line entities (typically `orderBy="sequence"`)
3. Use `cascade="all" orphanRemoval="true"` for composition (lines belong exclusively to parent)
4. Child entity must have `required="true"` on parent reference

**Multiple Collections:**
```xml
<entity name="Partner">
  <string name="name"/>

  <!-- Different collections -->
  <one-to-many name="saleOrderList" ref="SaleOrder" mappedBy="customer" orderBy="orderDate DESC"/>
  <one-to-many name="invoiceList" ref="Invoice" mappedBy="partner" orderBy="invoiceDate DESC"/>
  <one-to-many name="opportunityList" ref="Opportunity" mappedBy="partner"/>
</entity>
```

### Many-to-Many Best Practices

**Unidirectional:**
```xml
<entity name="Document">
  <string name="title"/>
  <many-to-many name="tagSet" ref="com.axelor.apps.base.db.Tag" title="Tags"/>
</entity>
```

**Database:** Creates join table `document_tag_set` with columns `document_id` and `tag_id`.

**Bidirectional with mappedBy:**
```xml
<!-- Owner side -->
<entity name="SaleOrderLine">
  <many-to-many name="taxLineSet" ref="com.axelor.apps.account.db.TaxLine"
    title="Taxes"/>
</entity>

<!-- Inverse side -->
<entity name="TaxLine">
  <many-to-many name="saleOrderLines" ref="SaleOrderLine"
    mappedBy="taxLineSet"/>
</entity>
```

> **Critical**: Always specify `mappedBy` for bidirectional many-to-many to ensure proper FK constraints.
> Without `mappedBy`, join table won't have proper bidirectional constraints.

**Association Entity Pattern:**

When you need extra attributes on the relationship:

```xml
<!-- Instead of simple many-to-many, use association entity -->
<entity name="ProductSupplier">
  <many-to-one name="product" ref="Product" required="true"/>
  <many-to-one name="supplier" ref="Partner" required="true"/>
  <decimal name="price" precision="10" scale="2"/>
  <integer name="deliveryDelay" title="Delivery Delay (days)"/>
  <unique-constraint columns="product,supplier"/>
</entity>

<entity name="Product">
  <one-to-many name="supplierList" ref="ProductSupplier" mappedBy="product"/>
</entity>

<entity name="Partner">
  <one-to-many name="suppliedProductList" ref="ProductSupplier" mappedBy="supplier"/>
</entity>
```

### One-to-One Best Practices

**Unidirectional:**
```xml
<entity name="User">
  <one-to-one name="preferences" ref="UserPreference"
    title="Preferences" cascade="all" orphanRemoval="true"/>
</entity>
```

**Bidirectional:**
```xml
<!-- Owner side -->
<entity name="Invoice">
  <one-to-one name="deliveryNote" ref="DeliveryNote"
    title="Delivery Note" unique="true"/>
</entity>

<!-- Inverse side -->
<entity name="DeliveryNote">
  <one-to-one name="invoice" ref="Invoice"
    mappedBy="deliveryNote"/>
</entity>
```

## Cascade and Orphan Removal

### Cascade Types

Controls which operations propagate to related entities.

**Cascade Values:**
- `PERSIST`: Save related entities
- `MERGE`: Update related entities
- `REMOVE`: Delete related entities
- `REFRESH`: Reload related entities
- `DETACH`: Detach related entities
- `ALL`: All operations

**Examples:**

```xml
<!-- Cascade persist and merge only -->
<many-to-one name="address" ref="Address"
  cascade="PERSIST,MERGE"/>

<!-- Full cascade (composition) -->
<one-to-many name="lineList" ref="OrderLine"
  mappedBy="order" cascade="ALL" orphanRemoval="true"/>

<!-- No cascade (independent entities) -->
<many-to-one name="customer" ref="Partner"/>
```

### Orphan Removal

**With orphanRemoval="true":**
- Removing entity from collection deletes it from database
- Use for composition (child cannot exist without parent)

**Example:**
```xml
<entity name="SaleOrder">
  <one-to-many name="lineList" ref="SaleOrderLine"
    mappedBy="saleOrder" cascade="all" orphanRemoval="true"/>
</entity>
```

**Behavior:**
```java
// Remove line from collection → line is DELETED from database
saleOrder.getLineList().remove(line);
repo.save(saleOrder); // Triggers DELETE on orphaned line
```

**Without orphanRemoval:**
- Removing from collection only nullifies foreign key
- Entity still exists in database

### When to Use Cascade

| Relationship Type | Cascade Recommendation | Reason |
|-------------------|----------------------|--------|
| Master → Lines | `cascade="all" orphanRemoval="true"` | Lines belong to master |
| Order → Customer | No cascade | Customer is independent |
| Document → Attachments | `cascade="all" orphanRemoval="true"` | Attachments belong to document |
| Product → Category | No cascade | Category is shared reference |
| Invoice → Address | `cascade="persist,merge"` | Save address with invoice, but don't delete |

## Bidirectional Relationships

### Coherence Rules

**Rule 1: mappedBy Must Match Field Name**

```xml
<!-- CORRECT -->
<entity name="SaleOrder">
  <one-to-many name="lineList" ref="SaleOrderLine" mappedBy="saleOrder"/>
</entity>

<entity name="SaleOrderLine">
  <many-to-one name="saleOrder" ref="SaleOrder" required="true"/>
</entity>

<!-- INCORRECT -->
<entity name="SaleOrder">
  <one-to-many name="lineList" ref="SaleOrderLine" mappedBy="order"/> <!-- Wrong! -->
</entity>

<entity name="SaleOrderLine">
  <many-to-one name="saleOrder" ref="SaleOrder"/> <!-- Field name is saleOrder -->
</entity>
```

**Rule 2: Only One Side Has mappedBy**

```xml
<!-- Owner side (has FK) - NO mappedBy -->
<entity name="SaleOrderLine">
  <many-to-one name="saleOrder" ref="SaleOrder"/>
</entity>

<!-- Inverse side - HAS mappedBy -->
<entity name="SaleOrder">
  <one-to-many name="lineList" ref="SaleOrderLine" mappedBy="saleOrder"/>
</entity>
```

**Rule 3: ref Must Point to Correct Entity**

```xml
<entity name="SaleOrder">
  <!-- ref must match target entity class -->
  <one-to-many name="lineList" ref="com.axelor.apps.sale.db.SaleOrderLine" mappedBy="saleOrder"/>
</entity>
```

## Enumerations

### Basic Enum

```xml
<enum name="OrderStatus">
  <item name="DRAFT"/>
  <item name="CONFIRMED"/>
  <item name="COMPLETED"/>
  <item name="CANCELED"/>
</enum>

<entity name="Order">
  <enum name="status" ref="OrderStatus" title="Status"/>
</entity>
```

### Numeric Enum (for Integer Fields)

```xml
<enum name="SaleOrderStatus" numeric="true">
  <item name="DRAFT_QUOTATION" value="1" title="Draft Quotation"/>
  <item name="FINALIZED_QUOTATION" value="2" title="Finalized Quotation"/>
  <item name="ORDER_CONFIRMED" value="3" title="Order Confirmed"/>
  <item name="ORDER_COMPLETED" value="4" title="Order Completed"/>
  <item name="CANCELED" value="5" title="Canceled"/>
</enum>

<entity name="SaleOrder">
  <integer name="statusSelect" title="Status" selection="sale.order.status.selection" default="1"/>
</entity>
```

> **Pattern**: Integer field with `selection` attribute links to numeric enum for type-safe status management.

### Enum with UI Metadata

```xml
<enum name="TaskStatus">
  <item name="TODO" title="To Do" icon="fa-circle-o" order="1"/>
  <item name="IN_PROGRESS" title="In Progress" icon="fa-spinner" order="2"/>
  <item name="REVIEW" title="Under Review" icon="fa-eye" order="3"/>
  <item name="DONE" title="Done" icon="fa-check-circle" order="4"/>
</enum>
```

**Attributes:**
- `name`: Enum constant (UPPER_SNAKE_CASE)
- `value`: Custom value
- `title`: Display label
- `icon`: Font Awesome icon class
- `order`: Display sequence
- `help`: Tooltip
- `hidden`: Hide from selection

## Sequences

> **CRITICAL: Sequences are AUTOMATIC - NO Java Code Needed**
>
> When you define a `sequence="..."` attribute on a string field, Axelor **automatically generates** the sequence number when the entity is saved. You do **NOT** need to write Java code (service, repository, or controller) to manage sequences.
>
> **Standard approach (99% of cases):** Define sequence attribute on field → Axelor handles it automatically.
>
> **Rare manual cases:** Only if you need the value BEFORE save, use `JpaSequence.nextValue("sequence.name")` in a `@Transactional` method.

### Sequence Definition

First, define the sequence in your domain model:

```xml
<sequence name="sale.order.seq"
         prefix="SO"
         suffix=""
         padding="5"
         initial="1"
         increment="1"/>
```

**Generates:** SO00001, SO00002, SO00003...

**Attributes:**
- `name`: Unique identifier (required)
- `prefix`: Text before number (optional)
- `suffix`: Text after number (optional)
- `padding`: Number of digits with leading zeros (optional)
- `initial`: Starting number (default: 1)
- `increment`: Step size (default: 1)

### Using Sequences - Automatic Generation (Recommended)

Then reference it in your entity field:

```xml
<entity name="SaleOrder">
  <many-to-one name="customer" ref="Partner" required="true"/>
  <string name="orderNumber" title="Order Number" sequence="sale.order.seq"/>
  <!-- Other fields -->
</entity>
```

**How it works automatically:**
1. User creates a new SaleOrder entity
2. User saves the entity (via UI or `repository.save()`)
3. **Axelor automatically detects** the `sequence="sale.order.seq"` attribute
4. **Axelor automatically generates** the next sequence value (e.g., SO00001)
5. The `orderNumber` field is populated automatically
6. **No Java code needed** - fully handled by the framework

**Best practices:**
- Add `readonly="true"` on UI views to prevent manual editing
- Add `unique="true"` to ensure uniqueness (optional but recommended)

### Real-World Sequence Examples

```xml
<!-- Invoice with year -->
<sequence name="invoice.seq"
         prefix="INV/"
         padding="6"
         initial="1000"/>
<!-- Generates: INV/001000, INV/001001 -->

<!-- Receipt with year suffix -->
<sequence name="receipt.seq"
         prefix="RCP-"
         suffix="-2024"
         padding="4"/>
<!-- Generates: RCP-0001-2024, RCP-0002-2024 -->

<!-- Simple counter -->
<sequence name="reference.seq"
         padding="10"
         initial="1"/>
<!-- Generates: 0000000001, 0000000002 -->
```

## Change Tracking

### Basic Tracking

```xml
<entity name="SaleOrder">
  <string name="orderNumber"/>
  <many-to-one name="customer" ref="Partner"/>
  <integer name="statusSelect" selection="sale.order.status.selection"/>
  <decimal name="totalAmount" precision="18" scale="2"/>

  <track>
    <field name="orderNumber"/>
    <field name="customer"/>
    <field name="statusSelect"/>
    <field name="totalAmount"/>
  </track>
</entity>
```

Creates audit trail timeline visible in UI showing field changes.

### Tracking with Events

```xml
<track>
  <!-- Track on creation only -->
  <field name="orderNumber" on="CREATE"/>
  <field name="creationDate" on="CREATE"/>

  <!-- Track on update only -->
  <field name="statusSelect" on="UPDATE"/>

  <!-- Track always (default) -->
  <field name="totalAmount" on="ALWAYS"/>
</track>
```

**Events:**
- `CREATE`: Only when record created
- `UPDATE`: Only when record updated
- `ALWAYS`: Both create and update (default)

### Tracking with Messages

```xml
<track>
  <field name="statusSelect"/>

  <!-- Conditional messages in timeline -->
  <message if="true" on="CREATE">Order created</message>
  <message if="statusSelect == 1" tag="important">Draft order</message>
  <message if="statusSelect == 2" tag="info">Order confirmed</message>
  <message if="statusSelect == 3" tag="success">Order in progress</message>
  <message if="statusSelect == 4" tag="warning">Order completed</message>
</track>
```

**Message Tags:**
- `important`: Red badge
- `success`: Green badge
- `warning`: Orange badge
- `info`: Blue badge

## Computed Fields

### Inline Java Code with CDATA (Recommended for Simple Logic)

**ESSENTIAL PATTERN** for concatenation, simple calculations and lightweight business logic:

```xml
<string name="simpleFullName" title="Full name">
  <![CDATA[
    if(firstName != null)
      return firstName+" "+name;
    else
      return name;
  ]]>
</string>
```

**Why this pattern is important:**
- **Simple and readable** - Direct Java code in domain
- **No separate class** - Logic close to definition
- **Computed on-the-fly** - No database storage
- **Type-safe** - Field type defines return type

**Règles CRITIQUES pour CDATA inline :**

1. **ALWAYS check null before access**
   ```xml
   <!-- CORRECT -->
   <string name="fullName">
     <![CDATA[
       if(firstName != null)
         return firstName + " " + name;
       else
         return name;
     ]]>
   </string>

   <!-- WRONG - NullPointerException risk -->
   <string name="fullName">
     <![CDATA[
       return firstName + " " + name;
     ]]>
   </string>
   ```

2. **ALWAYS return a value**
   ```xml
   <!-- CORRECT -->
   <![CDATA[
     if(condition)
       return value1;
     else
       return value2;
   ]]>

   <!-- WRONG - No return in all paths -->
   <![CDATA[
     if(condition)
       return value1;
   ]]>
   ```

3. **Field access: use field name directly**
   ```xml
   <![CDATA[
     // CORRECT - Direct field access
     return firstName + " " + name;

     // CORRECT - Using 'this'
     return this.firstName + " " + this.name;

     // CORRECT - Getter method
     return getFirstName() + " " + getName();
   ]]>
   ```

4. **Accès aux entités liées : vérifier null + getter**
   ```xml
   <![CDATA[
     String result = "";
     if(saleOrder != null && saleOrder.getSaleOrderSeq() != null) {
       result = saleOrder.getSaleOrderSeq();
     }
     if(productName != null) {
       result += " - " + productName;
     }
     return result;
   ]]>
   ```

**Cas d'usage typiques :**
- Concaténation de champs (nom complet, libellé composite)
- Calculs simples (score, statut dérivé)
- Formatage de valeurs
- Logique conditionnelle simple

### SQL Formula Fields

```xml
<entity name="SaleOrderLine">
  <decimal name="quantity" precision="10" scale="2"/>
  <decimal name="price" precision="10" scale="2"/>
  <decimal name="discount" scale="2" min="0" max="100" default="0"/>

  <!-- Computed total using SQL formula -->
  <decimal name="exclTaxTotal" title="Total (excl. tax)"
    formula="true"
    precision="18" scale="2" readonly="true">
    <![CDATA[
      self.quantity * self.price * (1 - (COALESCE(self.discount, 0) / 100))
    ]]>
  </decimal>
</entity>
```

**Rules:**
- **CRITICAL:** `formula` attribute is **BOOLEAN** (`true`/`false`), NOT a string
- SQL expression MUST be in `<![CDATA[...]]>` content
- Use `self.` to reference current entity fields in SQL
- Must be `readonly="true"`
- Use `COALESCE()` for NULL handling
- Formula is SQL, not Java

### Complex SQL Formulas with CDATA

```xml
<decimal name="inTaxTotal" title="Total (incl. tax)" readonly="true"
  precision="18" scale="2">
  <![CDATA[
    SELECT SUM(line.quantity * line.price * (1 + line.taxRate / 100))
    FROM SaleOrderLine line
    WHERE line.saleOrder = :id
  ]]>
</decimal>
```

Use CDATA for SQL when:
- Multi-line SQL queries
- Subqueries and aggregations
- Complex database calculations

### Choosing the Right Pattern

| Pattern | Use When | Example |
|---------|----------|---------|
| **Inline CDATA (Java)** | Simple logic, concatenation, conditionals | `firstName + " " + name` |
| **SQL Formula (inline)** | Single-line calculation with entity fields | `self.quantity * self.price` |
| **SQL Formula (CDATA)** | Aggregation from related tables | `SELECT MAX(date) FROM...` |
| **Service Layer** | Complex business logic, external calls | Calculate pricing with external API |

## Common Domain Patterns

### Index and Unique Constraint - Use Field Names

> **CRITICAL:** Always use **field names** (camelCase) in `columns` attribute, NOT SQL column names (snake_case).

**For simple single-field indexes, prefer `index="true"` on the field:**
```xml
<!-- CORRECT: Simple index on field -->
<many-to-one name="saleOrderLine" ref="SaleOrderLine" index="true"/>
<many-to-one name="customer" ref="Partner" index="true"/>

<!-- WRONG: Don't use <index> for simple single-field indexes -->
<!-- <index columns="sale_order_line_id"/> -->
```

**For composite indexes, use field names:**
```xml
<!-- CORRECT: Use field names (camelCase) -->
<index columns="customer,orderDate"/>
<unique-constraint columns="code,company"/>

<!-- WRONG: Don't use SQL column names (snake_case) -->
<!-- <index columns="customer_id,order_date"/> -->
<!-- <unique-constraint columns="product_id,optional_product_id"/> -->
```

**Complete example:**
```xml
<entity name="SaleOrderLineOption">
  <many-to-one name="saleOrderLine" ref="SaleOrderLine" required="true" index="true"/>
  <many-to-one name="selectedLine" ref="SaleOrderLine" index="true"/>
  <many-to-one name="productOption" ref="ProductOption" required="true"/>
  <boolean name="selected" default="false"/>

  <!-- Composite index: use field names -->
  <index columns="saleOrderLine,productOption"/>

  <!-- Unique constraint: use field names -->
  <unique-constraint columns="saleOrderLine,productOption"/>
</entity>
```

### Multi-Company Pattern

```xml
<entity name="Product">
  <string name="code" max="50"/>
  <string name="name" max="200"/>
  <many-to-one name="company" ref="com.axelor.apps.base.db.Company" title="Company"/>

  <!-- Unique per company -->
  <unique-constraint columns="code,company"/>
</entity>
```

### Status Workflow Pattern

```xml
<enum name="OrderStatus" numeric="true">
  <item name="DRAFT" value="1" title="Draft"/>
  <item name="VALIDATED" value="2" title="Validated"/>
  <item name="IN_PROGRESS" value="3" title="In Progress"/>
  <item name="COMPLETED" value="4" title="Completed"/>
  <item name="CANCELED" value="99" title="Canceled"/>
</enum>

<entity name="Order">
  <integer name="statusSelect" title="Status"
    selection="order.status.selection" default="1"/>
  <date name="validationDate" readonly="true"/>
  <date name="completionDate" readonly="true"/>

  <track>
    <field name="statusSelect"/>
    <message if="statusSelect == 1" tag="important">Draft</message>
    <message if="statusSelect == 2" tag="info">Validated</message>
    <message if="statusSelect == 3" tag="warning">In Progress</message>
    <message if="statusSelect == 4" tag="success">Completed</message>
    <message if="statusSelect == 99" tag="important">Canceled</message>
  </track>
</entity>
```

### Audit Fields - DO NOT CREATE MANUALLY

> **IMPORTANT:** Axelor Open Platform (AOP) **automatically provides** audit fields for ALL entities.
> Do NOT create these fields manually - they are inherited from the base Model class.

**Automatically available fields (DO NOT RECREATE):**
- `createdOn` (DateTime) - Creation timestamp
- `createdBy` (Many-to-one User) - Creator user
- `updatedOn` (DateTime) - Last update timestamp
- `updatedBy` (Many-to-one User) - Last modifier user
- `version` (Integer) - Optimistic locking version

```xml
<!-- WRONG: Do not create audit fields manually -->
<entity name="Customer">
  <string name="name" title="Name"/>
  <!-- DO NOT ADD THESE - they exist automatically! -->
  <!-- <datetime name="createdOn" readonly="true"/> -->
  <!-- <many-to-one name="createdBy" ref="com.axelor.auth.db.User"/> -->
</entity>

<!-- CORRECT: Just define your business fields -->
<entity name="Customer">
  <string name="name" title="Name" required="true"/>
  <string name="email" title="Email"/>
  <!-- Audit fields are automatically available -->
</entity>
```

**To access audit fields in views:**
```xml
<form name="customer-form" model="com.axelor.apps.base.db.Customer">
  <panel title="Information">
    <field name="name"/>
    <field name="email"/>
  </panel>
  <panel title="Audit" sidebar="true">
    <field name="createdOn" readonly="true"/>
    <field name="createdBy" readonly="true"/>
    <field name="updatedOn" readonly="true"/>
    <field name="updatedBy" readonly="true"/>
  </panel>
</form>
```

### Entity Extension Pattern

> **IMPORTANT:** To extend an existing entity from another module (e.g., add fields to `Product` from `axelor-base`), you must use the **same module name and package** as the original entity.

> **FILE NAMING RULE:** When extending an entity, the XML file must have the **SAME NAME** as the original entity file. For example, to extend `Product` entity, create a file named `Product.xml` in your module (NOT `ProductExtension.xml`).

**File structure example:**
```
src/main/resources/domains/
├── Product.xml          # Extension of Product entity from AOS
├── Partner.xml          # Extension of Partner entity from AOS
└── MyNewEntity.xml      # Your own new entity
```

**Correct way to extend an existing entity:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<domain-models xmlns="http://axelor.com/xml/ns/domain-models"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://axelor.com/xml/ns/domain-models
  https://axelor.com/xml/ns/domain-models/domain-models_7.4.xsd">

  <!-- Use the SAME module name and package as the original entity -->
  <module name="base" package="com.axelor.apps.base.db"/>

  <!-- Just redeclare the entity with the new fields to add -->
  <entity name="Product">
    <!-- Only add the NEW fields - existing fields are preserved -->
    <string name="customReference" title="Custom Reference" max="100"/>
    <boolean name="isSpecialProduct" title="Special Product" default="false"/>
  </entity>

</domain-models>
```

**Key points:**
- **File name:** Use the same name as the entity (e.g., `Product.xml`, NOT `ProductExtension.xml`)
- Use `<module name="base" package="com.axelor.apps.base.db"/>` (same as original)
- Do NOT use `extends="true"` or `extends="com.axelor.apps.base.db.Product"`
- Only declare the **new fields** you want to add
- Original fields are automatically preserved
- The extension is implicit - AOP merges the definitions

**WRONG approaches:**
```xml
<!-- WRONG: Don't use extends="true" -->
<entity name="Product" extends="true">

<!-- WRONG: Don't use extends with FQDN for extension -->
<entity name="Product" extends="com.axelor.apps.base.db.Product">

<!-- WRONG: Don't use your own module/package for extending existing entities -->
<module name="custom" package="com.axelor.apps.custom.db"/>
<entity name="Product">  <!-- This creates a NEW entity, not an extension! -->
```

### Line Sequence Pattern

```xml
<entity name="OrderLine">
  <integer name="sequence" title="Sequence" default="0"/>
  <many-to-one name="order" ref="Order" required="true"/>
  <!-- Other fields -->
</entity>

<entity name="Order">
  <one-to-many name="lineList" ref="OrderLine"
    mappedBy="order" orderBy="sequence" cascade="all" orphanRemoval="true"/>
</entity>
```

**Service layer code:**
```java
// Auto-assign sequence when adding lines
int seq = 0;
for (OrderLine line : order.getLineList()) {
    line.setSequence(seq++);
}
```

### Soft Delete Pattern

```xml
<entity name="Record">
  <boolean name="archived" title="Archived" default="false"/>
  <datetime name="archivedOn" readonly="true"/>
  <many-to-one name="archivedBy" ref="com.axelor.auth.db.User" readonly="true"/>
</entity>
```

**Query pattern:**
```java
// Filter out archived records
Query<Record> query = recordRepo.all().filter("self.archived = false");
```

### Decimal Precision Patterns

```xml
<entity name="Product">
  <!-- Money amounts: precision 18, scale 2 -->
  <decimal name="salePrice" precision="18" scale="2"/>
  <decimal name="costPrice" precision="18" scale="2"/>

  <!-- Quantities: precision 10, scale 2 or 4 -->
  <decimal name="stockQuantity" precision="10" scale="2"/>
  <decimal name="preciseQuantity" precision="10" scale="4"/>

  <!-- Percentages: scale 2, with min/max -->
  <decimal name="taxRate" scale="2" min="0" max="100"/>
  <decimal name="margin" scale="2"/>

  <!-- Exchange rates: precision 12, scale 6 -->
  <decimal name="exchangeRate" precision="12" scale="6"/>
</entity>
```

### Extra-Code - Use Carefully

> **WARNING:** `<extra-code>` adds Java code to the **generated Repository class**, NOT to the entity.
> This means the method should work with repository operations (find, save, etc.).

**CRITICAL: Extra-code methods are NOT automatically invoked!**

Methods added via `<extra-code>` will NOT be called automatically during save operations.
They are simply added to the repository class and must be explicitly invoked from:
- An overridden `save()` method
- A service method that calls the repository

**DO NOT use `<extra-code>` for:**
- Validation logic that checks multiple records (use service layer or repo `save()` override)
- Business rules (use services)
- Methods that need to be called outside the repository context

**WRONG - Method without parameters, never called:**
```xml
<extra-code><![CDATA[
  // This method will NEVER be called automatically!
  // It has no way to know which entity to validate
  public void validateOptions() {
    // Useless - no access to the entity being saved
  }
]]></extra-code>
```

**CORRECT - If you MUST use extra-code (prefer services instead):**

Step 1: Declare abstract repository and add method with entity parameter:
```xml
<entity name="ProductOption" repository="abstract">
  <!-- ... fields ... -->

  <extra-code><![CDATA[
    // Method takes entity as parameter
    public void validateProductOptions(ProductOption option) {
      if (option.getProducts() == null || option.getProducts().isEmpty()) {
        throw new AxelorException(TraceBackRepository.CATEGORY_INCONSISTENCY,
          "ProductOption must have at least one product");
      }
    }
  ]]></extra-code>
</entity>
```

Step 2: Create custom repository that calls the method:
```java
// Custom repository extending the AUTO-GENERATED ProductOptionRepository
public class ProductOptionRepo extends ProductOptionRepository {

  @Override
  public ProductOption save(ProductOption entity) {
    validateProductOptions(entity);  // Explicitly call the validation
    return super.save(entity);
  }
}
```

**BEST PRACTICE: Use services instead of extra-code for validation:**

Domain (no extra-code):
```xml
<entity name="ProductOption">
  <!-- ... fields only ... -->
</entity>
```

Service:
```java
public class ProductOptionServiceImpl implements ProductOptionService {

  private final ProductOptionRepository repository;

  @Inject
  public ProductOptionServiceImpl(ProductOptionRepository repository) {
    this.repository = repository;
  }

  @Override
  @Transactional
  public ProductOption validateAndSave(ProductOption option) throws AxelorException {
    validateProductOptions(option);
    return repository.save(option);
  }

  protected void validateProductOptions(ProductOption option) throws AxelorException {
    if (option.getProducts() == null || option.getProducts().isEmpty()) {
      throw new AxelorException(TraceBackRepository.CATEGORY_INCONSISTENCY,
        "ProductOption must have at least one product");
    }
  }
}
```

> **Summary:** Extra-code is useful for constants and simple repository helpers.
> For validation and business logic, always prefer the service layer.

### Table Name - DO NOT Specify Unless Required

> **IMPORTANT:** AOP automatically generates table names from entity names using snake_case conversion.
> Only specify `table=""` attribute when the entity name conflicts with Hibernate/SQL reserved words.

**Let AOP generate table names automatically:**
```xml
<!-- CORRECT - AOP generates table "optional_product_template" -->
<entity name="OptionalProductTemplate">
  ...
</entity>

<!-- CORRECT - AOP generates table "sale_order_line_option" -->
<entity name="SaleOrderLineOption">
  ...
</entity>
```

**WRONG - Unnecessary table specification:**
```xml
<!-- WRONG - Don't specify table unless required -->
<entity name="OptionalProductTemplate" table="optionalproduct_optional_product_template">
```

**When to specify table name:**
Only use `table=""` for **Hibernate/SQL reserved words** like:
- `User` → `table="auth_user"`
- `Order` → `table="sale_order"`
- `Group` → `table="auth_group"`
- `Table` → `table="meta_table"`

```xml
<!-- CORRECT - "Order" is SQL reserved word -->
<entity name="Order" table="sale_order">
  ...
</entity>
```

---

**Next Steps:**
- See @docs/domains/domain-reference.md for basic syntax reference
- See @skills/axelor-xml-validator/reference/domain-models-reference.md for exhaustive XSD attributes
- See @docs/domains/examples/ for real-world tested patterns from Axelor Open Suite
