# Domain XML Reference

Complete reference for Axelor domain XML syntax, structure, and field types.

> **Source of Truth**: For exhaustive XSD attribute reference, see @skills/axelor-xml-validator/reference/domain-models-reference.md
> **Real Examples**: See @docs/domains/examples/ for annotated domain files from Axelor Open Suite

## Table of Contents

1. [File Structure](#file-structure)
2. [Root Elements](#root-elements)
3. [Entity Element](#entity-element)
4. [Field Types](#field-types)
5. [Common Field Attributes](#common-field-attributes)
6. [Simple Fields](#simple-fields)
7. [Relationship Fields](#relationship-fields)
8. [Index and Constraints](#index-and-constraints)
9. [Track Element](#track-element)
10. [Finder Methods](#finder-methods)
11. [Complete Examples](#complete-examples)

## File Structure

### File Naming Convention

- Location: `src/main/resources/domains/`
- File name: `{EntityName}.xml` (e.g., `Customer.xml`, `SaleOrder.xml`)
- One or more entities per file

### Basic Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<domain-models xmlns="http://axelor.com/xml/ns/domain-models"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://axelor.com/xml/ns/domain-models
  https://axelor.com/xml/ns/domain-models/domain-models_{version}.xsd">

  <module name="module-name" package="com.axelor.apps.module.db"/>

  <entity name="EntityName">
    <!-- fields, indexes, constraints, etc. -->
  </entity>

</domain-models>
```

> **CRITICAL: XSD Version MUST Match AOP Version**
>
> Replace `{version}` with your project's AOP major.minor version from gradle.properties:
> - AOP 7.1.x → use `domain-models_7.1.xsd`
> - AOP 7.4.x → use `domain-models_7.4.xsd`
> - AOP 8.0.x → use `domain-models_8.0.xsd`
> - AOP 8.1.x → use `domain-models_8.1.xsd`
>
> **There is NO unified schema** - each AOP version has its own XSD schema.

## Root Elements

### `<domain-models>`

Container for all entity definitions.

**Required attributes:**
- `xmlns`: `http://axelor.com/xml/ns/domain-models`
- `xmlns:xsi`: `http://www.w3.org/2001/XMLSchema-instance`
- `xsi:schemaLocation`: Schema URL

### `<module>`

Defines module and package for generated entities.

**Attributes:**
- `name` (required): Module name
- `package` (required): Java package (e.g., `com.axelor.apps.sale.db`)

**Example:**
```xml
<module name="axelor-sale" package="com.axelor.apps.sale.db"/>
```

## Entity Element

### `<entity>`

Defines a JPA entity (database table).

**Key Attributes:**
- `name` (required): Entity class name (PascalCase)
- `table`: Database table name (snake_case, optional)
- `sequential`: Enable sequential code generation (boolean)
- `cacheable`: Enable second-level cache (boolean)
- `repository`: Repository type (`default`, `abstract`, `none`)

**Example:**
```xml
<entity name="SaleOrder" sequential="true" cacheable="true">
  <!-- fields -->
</entity>
```

> **Note**: Only use `table=""` for SQL reserved words like `User`, `Order`, `Group`, `Table`. AOP auto-generates table names in snake_case (e.g., `SaleOrder` → `sale_order`).

**Inheritance:**
```xml
<entity name="Partner" strategy="SINGLE">
  <string name="partnerType" selection="partner.type.selection"/>
</entity>

<entity name="Customer" extends="Partner">
  <decimal name="creditLimit" scale="2"/>
</entity>
```

> **Reference**: For complete entity attributes, see @skills/axelor-xml-validator/reference/domain-models-reference.md (Entity section)

## Field Types

Axelor supports these field types:

### Simple Types
- `<string>` - Short text (VARCHAR)
- `<text>` - Large text (TEXT/CLOB)
- `<integer>` - 32-bit integer
- `<long>` - 64-bit integer
- `<decimal>` - Fixed-point decimal
- `<boolean>` - Boolean value
- `<date>` - Date (no time)
- `<datetime>` - Date with time
- `<time>` - Time only
- `<binary>` - Binary data/files

### Relationship Types
- `<many-to-one>` - N:1 relationship
- `<one-to-many>` - 1:N relationship
- `<many-to-many>` - N:N relationship
- `<one-to-one>` - 1:1 relationship

## Common Field Attributes

All field types support:

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | String | Field name (camelCase, required) |
| `title` | String | Display label |
| `help` | String | Help text/tooltip |
| `required` | Boolean | Field is mandatory |
| `readonly` | Boolean | Field is read-only |
| `hidden` | Boolean | Field is hidden |
| `unique` | Boolean | Value must be unique |
| `default` | String | Default value |
| `column` | String | Database column name (snake_case) |
| `insertable` | Boolean | Allow insert (default: true) |
| `updatable` | Boolean | Allow update (default: true) |
| `transient` | Boolean | Do not persist |
| `formula` | String | SQL formula for computed field |
| `json` | Boolean | Store as JSON |

### Title and Help Convention (Sentence Case)

**CRITICAL**: Use **sentence case** for `title` and `help` attributes (capitalize only the first letter of the first word).

**Correct:**
```xml
<string name="conversionCoefficient" title="Conversion coefficient"/>
<decimal name="unitPrice" title="Unit price" help="Price per unit in base currency"/>
<string name="tvaRate" title="TVA rate"/>  <!-- Acronyms keep their case -->
```

**Incorrect:**
```xml
<string name="conversionCoefficient" title="Conversion Coefficient"/>  <!-- Wrong: Title Case -->
<decimal name="unitPrice" title="Unit Price"/>  <!-- Wrong: Title Case -->
```

**Exceptions:**
- Acronyms: `TVA`, `ID`, `URL`, `API` keep their uppercase
- Proper nouns: `Axelor`, `Redmine` keep their case

> **Reference**: For complete attribute list per field type, see @skills/axelor-xml-validator/reference/domain-models-reference.md

## Simple Fields

### String Field

Short text field (VARCHAR).

**Specific Attributes:**
- `max`: Maximum length (default: 255)
- `min`: Minimum length
- `selection`: Selection reference
- `translatable`: Support translations (boolean)
- `large`: Use TEXT type instead (boolean)
- `password`: Password field (`true`, `false`, `encrypted`)
- `encrypted`: Encrypt field content (boolean)
- `sequence`: Auto-numbering sequence reference
- `namecolumn`: Use as entity name column (boolean)

**Examples:**
```xml
<!-- Basic string -->
<string name="name" title="Name" required="true" max="100"/>

<!-- Unique code -->
<string name="code" title="Code" unique="true" max="50"/>

<!-- String with selection (enum) -->
<string name="status" title="Status" selection="sale.order.status.selection" default="draft"/>

<!-- Large text (TEXT type) -->
<string name="notes" title="Notes" large="true"/>

<!-- Auto-numbered field -->
<string name="orderNumber" title="Order Number" sequence="sale.order.seq" readonly="true" unique="true"/>

<!-- Password -->
<string name="password" title="Password" password="encrypted"/>

<!-- Entity name field -->
<string name="fullName" title="Full Name" namecolumn="true"/>
```

### Integer Field

32-bit integer value.

**Specific Attributes:**
- `max`: Maximum value
- `min`: Minimum value
- `selection`: Selection reference

**Examples:**
```xml
<!-- Basic integer -->
<integer name="quantity" title="Quantity" required="true" min="0"/>

<!-- Integer with selection (status) -->
<integer name="statusSelect" title="Status" selection="sale.order.status.selection" default="1"/>

<!-- Sequence number -->
<integer name="sequence" title="Sequence" default="0"/>
```

### Decimal Field

Fixed-point decimal number.

**Specific Attributes:**
- `precision`: Total digits (default: 18)
- `scale`: Decimal places (default: 2)
- `max`: Maximum value
- `min`: Minimum value

**Rule**: `scale` ≤ `precision`

**Examples:**
```xml
<!-- Money amount (standard precision) -->
<decimal name="totalAmount" title="Total Amount" precision="18" scale="2"/>

<!-- Unit price -->
<decimal name="unitPrice" title="Unit Price" precision="10" scale="2" required="true"/>

<!-- Percentage -->
<decimal name="discountPercent" title="Discount %" scale="2" min="0" max="100"/>

<!-- Quantity with 4 decimals -->
<decimal name="quantity" title="Quantity" precision="10" scale="4"/>
```

> **Best Practice**: Use precision 18, scale 2 for money amounts

### Boolean Field

True/false value.

**Examples:**
```xml
<boolean name="active" title="Active" default="true"/>
<boolean name="confirmed" title="Confirmed" default="false"/>
```

### Date and DateTime Fields

**Date** (no time):
```xml
<date name="orderDate" title="Order Date" required="true"/>
<date name="deliveryDate" title="Delivery Date"/>
```

**DateTime** (with time):
```xml
<datetime name="createdOn" title="Created On"/>
<datetime name="scheduledAt" title="Scheduled At" tz="true"/>
```

**Time** (time only):
```xml
<time name="startTime" title="Start Time"/>
```

### Binary Field

File/blob storage.

**Specific Attributes:**
- `image`: Field stores an image (boolean)
- `max`: Maximum file size in MB

**Examples:**
```xml
<binary name="attachment" title="Attachment"/>
<binary name="photo" title="Photo" image="true" max="5"/>
```

## Relationship Fields

### Many-to-One

N:1 relationship (foreign key).

**Attributes:**
- `ref` (required): Referenced entity (fully qualified class name)
- `title`: Display label
- `required`: Mandatory relationship
- `readonly`: Read-only field
- `cascade`: Cascade operations
- `orphanRemoval`: Remove orphans (boolean)

**Examples:**
```xml
<!-- Basic many-to-one -->
<many-to-one name="customer" ref="com.axelor.apps.base.db.Partner"
  title="Customer" required="true"/>

<!-- Many-to-one with cascade -->
<many-to-one name="address" ref="com.axelor.apps.base.db.Address"
  cascade="all" orphanRemoval="true"/>

<!-- Same module reference (short form) -->
<many-to-one name="company" ref="Company" title="Company"/>
```

### One-to-Many

1:N relationship (collection).

**Attributes:**
- `ref` (required): Referenced entity
- `mappedBy` (required): Field name in referenced entity
- `title`: Display label
- `cascade`: Cascade operations
- `orphanRemoval`: Remove orphans (boolean)
- `orderBy`: Sort collection by field

**Examples:**
```xml
<!-- Basic one-to-many -->
<one-to-many name="orderLineList" ref="com.axelor.apps.sale.db.SaleOrderLine"
  mappedBy="saleOrder" title="Order Lines" orderBy="sequence"/>

<!-- One-to-many with cascade (composition) -->
<one-to-many name="lines" ref="OrderLine"
  mappedBy="order" cascade="all" orphanRemoval="true"/>
```

> **Best Practice**: Always use `mappedBy` for bidirectional relationships to ensure FK constraints

### Many-to-Many

N:N relationship (join table).

**Attributes:**
- `ref` (required): Referenced entity
- `mappedBy`: Inverse field name (optional, for bidirectional)
- `title`: Display label

**Examples:**
```xml
<!-- Unidirectional many-to-many -->
<many-to-many name="tagSet" ref="com.axelor.apps.base.db.Tag" title="Tags"/>

<!-- Bidirectional many-to-many (owner side) -->
<many-to-many name="productCategorySet" ref="ProductCategory" title="Categories"/>

<!-- Bidirectional many-to-many (inverse side) -->
<many-to-many name="productSet" ref="Product" mappedBy="productCategorySet"/>
```

### One-to-One

1:1 relationship.

**Attributes:**
- `ref` (required): Referenced entity
- `unique`: Enforce uniqueness (boolean, recommended)
- `mappedBy`: Inverse field name (for bidirectional)

**Examples:**
```xml
<one-to-one name="address" ref="com.axelor.apps.base.db.Address"
  title="Delivery Address" unique="true"/>
```

## Index and Constraints

### Index

Database index for query performance.

**Attributes:**
- `columns` (required): Comma-separated column names
- `name`: Index name (optional)
- `unique`: Unique index (boolean)

**Examples:**
```xml
<entity name="SaleOrder">
  <string name="orderNumber"/>
  <date name="orderDate"/>
  <many-to-one name="customer" ref="Partner"/>

  <!-- Unique index -->
  <index columns="orderNumber" unique="true"/>

  <!-- Composite index -->
  <index columns="customer,orderDate"/>

  <!-- Named index -->
  <index name="idx_order_status" columns="statusSelect"/>
</entity>
```

### Unique Constraint

Enforce uniqueness on one or more columns.

**Attributes:**
- `columns` (required): Comma-separated column names
- `name`: Constraint name (optional)

**Examples:**
```xml
<entity name="Product">
  <string name="code"/>
  <many-to-one name="company" ref="Company"/>

  <!-- Composite unique constraint -->
  <unique-constraint columns="code,company"/>
</entity>
```

## Track Element

Enable change tracking (audit trail).

**Child Elements:**
- `<field>`: Field to track
  - `name` (required): Field name
  - `on`: Track events (`CREATE`, `UPDATE`, `DELETE`)
- `<message>`: Custom message
  - `if`: Condition (expression)
  - `tag`: Message type (`info`, `success`, `warning`, `important`)

**Examples:**
```xml
<!-- Basic tracking -->
<track>
  <field name="statusSelect"/>
  <field name="customer"/>
  <field name="totalAmount"/>
</track>

<!-- Tracking with custom messages -->
<track>
  <field name="statusSelect"/>
  <message if="statusSelect == 1" tag="info">Order drafted</message>
  <message if="statusSelect == 2" tag="success">Order confirmed</message>
  <message if="statusSelect == 3" tag="warning">Order in progress</message>
  <message if="statusSelect == 4" tag="important">Order completed</message>
</track>

<!-- Track on specific events -->
<track>
  <field name="orderNumber" on="CREATE"/>
  <field name="statusSelect" on="UPDATE"/>
</track>
```

## Finder Methods

Generate custom repository finder methods.

**Attributes:**
- `name` (required): Method name
- `using` (required): Comma-separated field names
- `all`: Return list (boolean, default: false)
- `filter`: Additional JPQL filter
- `orderBy`: Sort clause
- `cacheable`: Cache results (boolean)

**Examples:**
```xml
<entity name="SaleOrder">
  <string name="orderNumber"/>
  <many-to-one name="customer" ref="Partner"/>
  <integer name="statusSelect"/>

  <!-- Find single entity -->
  <finder-method name="findByOrderNumber" using="orderNumber"/>

  <!-- Find all by customer -->
  <finder-method name="findByCustomer" using="customer" all="true"/>

  <!-- Find with filter and ordering -->
  <finder-method name="findActiveByCustomer" using="customer"
    filter="self.statusSelect != 99" all="true" orderBy="orderDate DESC"/>
</entity>
```

Generated methods:
```java
SaleOrder findByOrderNumber(String orderNumber);
List<SaleOrder> findByCustomer(Partner customer);
List<SaleOrder> findActiveByCustomer(Partner customer);
```

## Complete Examples

### Simple Entity

```xml
<?xml version="1.0" encoding="UTF-8"?>
<domain-models xmlns="http://axelor.com/xml/ns/domain-models"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://axelor.com/xml/ns/domain-models
  https://axelor.com/xml/ns/domain-models/domain-models_7.4.xsd">

  <module name="axelor-product" package="com.axelor.apps.product.db"/>

  <entity name="Product">
    <string name="code" title="Code" required="true" unique="true" max="50"/>
    <string name="name" title="Name" required="true" max="200"/>
    <string name="description" title="Description" large="true"/>
    <decimal name="salePrice" title="Sale Price" precision="10" scale="2" required="true"/>
    <boolean name="active" title="Active" default="true"/>
    <binary name="picture" title="Picture" image="true"/>

    <index columns="code" unique="true"/>
    <finder-method name="findByCode" using="code"/>
  </entity>

</domain-models>
```

### Entity with Relationships

```xml
<?xml version="1.0" encoding="UTF-8"?>
<domain-models xmlns="http://axelor.com/xml/ns/domain-models"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://axelor.com/xml/ns/domain-models
  https://axelor.com/xml/ns/domain-models/domain-models_7.4.xsd">

  <module name="axelor-sale" package="com.axelor.apps.sale.db"/>

  <entity name="SaleOrder" sequential="true">
    <string name="orderNumber" title="Order Number" readonly="true" unique="true" sequence="sale.order.seq"/>
    <date name="orderDate" title="Order Date" required="true"/>
    <integer name="statusSelect" title="Status" selection="sale.order.status.selection" default="1"/>
    <decimal name="totalAmount" title="Total Amount" precision="18" scale="2" readonly="true"/>

    <many-to-one name="customer" ref="com.axelor.apps.base.db.Partner"
      title="Customer" required="true"/>
    <many-to-one name="currency" ref="com.axelor.apps.base.db.Currency"
      title="Currency" required="true"/>

    <one-to-many name="orderLineList" ref="SaleOrderLine"
      mappedBy="saleOrder" title="Order Lines"
      cascade="all" orphanRemoval="true" orderBy="sequence"/>

    <many-to-many name="tagSet" ref="com.axelor.apps.base.db.Tag" title="Tags"/>

    <index columns="orderNumber" unique="true"/>
    <index columns="customer,orderDate"/>

    <track>
      <field name="statusSelect"/>
      <field name="customer"/>
      <field name="totalAmount"/>
    </track>

    <finder-method name="findByOrderNumber" using="orderNumber"/>
    <finder-method name="findByCustomer" using="customer" all="true" orderBy="orderDate DESC"/>
  </entity>

</domain-models>
```

### Entity with Computed Fields

```xml
<entity name="SaleOrderLine">
  <integer name="sequence" title="Sequence"/>
  <many-to-one name="product" ref="Product" title="Product" required="true"/>
  <decimal name="quantity" title="Quantity" precision="10" scale="2" required="true"/>
  <decimal name="price" title="Unit Price" precision="10" scale="2" required="true"/>
  <decimal name="discount" title="Discount %" scale="2" min="0" max="100" default="0"/>

  <!-- Computed field using SQL formula -->
  <decimal name="exclTaxTotal" title="Total (excl. tax)"
    formula="true"
    precision="18" scale="2" readonly="true">
    <![CDATA[
      self.quantity * self.price * (1 - (COALESCE(self.discount, 0) / 100))
    ]]>
  </decimal>

  <many-to-one name="saleOrder" ref="SaleOrder" title="Sale Order" required="true"/>
</entity>
```

## Best Practices

1. **Naming Conventions**
   - Entities: PascalCase (e.g., `SaleOrder`)
   - Fields: camelCase (e.g., `orderDate`)
   - Tables: snake_case (e.g., `sale_order`)

2. **Constraints**
   - Use `required="true"` for mandatory fields
   - Use `unique="true"` for unique values (codes, emails)
   - Add indexes on frequently queried fields
   - Use composite unique constraints for multi-company entities

3. **Relationships**
   - Always specify `mappedBy` for bidirectional relationships
   - Use `cascade="all" orphanRemoval="true"` for composition
   - Add `orderBy` on one-to-many collections (especially lines)
   - Use `ref` with fully qualified class names for cross-module references

4. **Decimal Fields**
   - Money amounts: `precision="18" scale="2"`
   - Quantities: `precision="10" scale="2"` or `scale="4"` for high precision
   - Percentages: `scale="2" min="0" max="100"`
   - Always ensure `scale` ≤ `precision`

5. **Documentation**
   - Provide `title` attribute for user-friendly labels
   - Use `help` attribute for field tooltips
   - Mark computed fields as `readonly="true"`

6. **Performance**
   - Add indexes on foreign keys and frequently searched fields
   - Enable caching (`cacheable="true"`) for reference data entities
   - Use finder methods for common queries

## Common Patterns

### Sequential Entity (Auto-numbering)
```xml
<entity name="Invoice" sequential="true">
  <string name="invoiceNumber" sequence="invoice.seq" readonly="true" unique="true"/>
</entity>
```

### Multi-Company Entity
```xml
<entity name="Product">
  <string name="code" max="50"/>
  <many-to-one name="company" ref="Company"/>
  <unique-constraint columns="code,company"/>
</entity>
```

### Master-Detail Pattern
```xml
<!-- Master -->
<entity name="SaleOrder">
  <one-to-many name="lineList" ref="SaleOrderLine"
    mappedBy="saleOrder" cascade="all" orphanRemoval="true" orderBy="sequence"/>
</entity>

<!-- Detail -->
<entity name="SaleOrderLine">
  <integer name="sequence" default="0"/>
  <many-to-one name="saleOrder" ref="SaleOrder" required="true"/>
</entity>
```

### Audit Fields - DO NOT CREATE

> **IMPORTANT:** Axelor Open Platform (AOP) **automatically provides** audit fields for ALL entities.
> Do NOT create these fields manually - they are inherited from the base Model class.

**Automatically available fields:**
- `createdOn` (DateTime) - Creation timestamp
- `createdBy` (Many-to-one User) - Creator user
- `updatedOn` (DateTime) - Last update timestamp
- `updatedBy` (Many-to-one User) - Last modifier user
- `version` (Integer) - Optimistic locking version

```xml
<!-- CORRECT: Just define your business fields -->
<entity name="Customer">
  <string name="name" title="Name" required="true"/>
  <string name="email" title="Email"/>
  <!-- Audit fields are automatically available -->
</entity>
```

---

**Next Steps:**
- See @docs/domains/domain-patterns.md for advanced patterns (enums, sequences, tracking, computed fields)
- See @skills/axelor-xml-validator/reference/domain-models-reference.md for exhaustive XSD attribute reference
- See @docs/domains/examples/ for real-world annotated examples from Axelor Open Suite
