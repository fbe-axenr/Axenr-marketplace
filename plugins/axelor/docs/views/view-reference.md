# View Reference

Complete reference for Axelor view types, XML structure, basic components, field attributes, and widgets.

## XML Structure and Namespaces

### Basic View File Structure

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<object-views xmlns="http://axelor.com/xml/ns/object-views"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://axelor.com/xml/ns/object-views
  http://axelor.com/xml/ns/object-views/object-views_6.1.xsd">

  <grid name="product-grid" title="Products" model="com.axelor.apps.base.db.Product">
    <!-- Grid definition -->
  </grid>

  <form name="product-form" title="Product" model="com.axelor.apps.base.db.Product">
    <!-- Form definition -->
  </form>

</object-views>
```

### Single Source of Truth

For exhaustive attribute definitions, refer to:
`@skills/axelor-xml-validator/reference/object-views-reference.md`

This document provides essential attributes and patterns used in production code.

## View Types

### 1. Form View

Displays a single record with detailed fields, panels, and actions.

```xml
<form name="product-form" title="Product"
      model="com.axelor.apps.base.db.Product"
      onNew="action-product-defaults"
      onLoad="action-product-onload"
      onSave="action-product-validate"
      width="large">

  <panel name="mainPanel" title="Product Details">
    <field name="name" required="true"/>
    <field name="code"/>
  </panel>
</form>
```

**Essential Attributes:**
- `name` - Unique identifier (required)
- `title` - Form title displayed in UI
- `model` - Domain model class (required)
- `width` - Form width: `large`, `mid`, `mini`
- `onNew` - Action on new record creation
- `onLoad` - Action when record loads
- `onSave` - Action before saving

**Permission Attributes:**
- `canNew` - Allow creating new records
- `canEdit` - Allow editing records
- `canSave` - Allow saving changes
- `canCopy` - Allow copying records
- `canDelete` - Allow deleting records
- `canAttach` - Show attachment button
- `canArchive` - Enable archive feature

**Conditional Attributes:**
- `readonlyIf` - Expression to make entire form readonly

### 2. Grid View

Displays multiple records in a tabular format with columns, sorting, filtering, and pagination.

```xml
<grid name="product-grid" title="Products"
      model="com.axelor.apps.base.db.Product"
      orderBy="name"
      editable="false"
      edit-icon="true">

  <field name="name" width="250"/>
  <field name="code" width="100"/>
  <field name="category"/>
  <field name="unitPrice" width="120"/>

  <hilite color="success" if="active == true"/>
  <hilite color="muted" if="active == false"/>
</grid>
```

**Essential Attributes:**
- `name` - Unique identifier (required)
- `title` - Grid title
- `model` - Domain model class (required)
- `orderBy` - Default sort order (prefix with `-` for descending)
- `editable` - Enable inline editing
- `edit-icon` - Show edit icon per row
- `groupBy` - Default grouping field

**Permission Attributes:**
- `canNew` - Show 'New' button
- `canEdit` - Allow editing records
- `canDelete` - Allow deleting records
- `canSave` - Allow saving inline edits
- `canMove` - Allow row reordering (see Row Reordering below)
- `canArchive` - Enable archive feature

#### Row Reordering with canMove

**IMPORTANT**: AOP handles row reordering automatically. Do NOT create custom moveUp/moveDown controllers.

When `canMove="true"` is set on a grid view:
1. AOP automatically adds drag-and-drop handles to each row
2. Users can drag rows to reorder them
3. AOP automatically updates the `sequence` field (or configured field) on save
4. **NO custom controller code is needed**

**Requirements:**
- The entity MUST have a `sequence` field (integer type)
- The grid view must have `canMove="true"`

**Example:**
```xml
<!-- Domain: Entity with sequence field -->
<entity name="SaleOrderLine">
  <integer name="sequence"/>
  <!-- other fields -->
</entity>

<!-- View: Grid with canMove -->
<grid name="sale-order-line-grid" title="Lines"
      model="com.axelor.apps.sale.db.SaleOrderLine"
      orderBy="sequence"
      canMove="true">
  <field name="product"/>
  <field name="quantity"/>
  <field name="unitPrice"/>
</grid>
```

**Anti-Pattern - DO NOT DO THIS:**
```java
// WRONG - AOP already handles this
public void moveUp(ActionRequest request, ActionResponse response) {
  // Custom reordering logic - UNNECESSARY
}

public void moveDown(ActionRequest request, ActionResponse response) {
  // Custom reordering logic - UNNECESSARY
}
```

**The AOP framework automatically:**
- Renders drag handles in the UI
- Handles drag-and-drop events
- Updates sequence values
- Persists the new order

**Display Attributes:**
- `customSearch` - Enable custom search
- `freeSearch` - Free search mode: `all`, `none`
- `x-selector` - Selection mode: `checkbox`, `false`

### 3. Dashboard View

Displays KPIs, charts, and dashlets for analytics and summary overview.

```xml
<dashboard name="sales-dashboard" title="Sales Dashboard">
  <dashlet name="salesByMonth" title="Sales by Month"
           action="chart.sales.by.month"
           colSpan="6" height="350"/>
  <dashlet name="topProducts" title="Top Products"
           action="chart.top.products"
           colSpan="6" height="350"/>
</dashboard>
```

### 4. Calendar View

Displays records in calendar format with date ranges for scheduling and time-based events.

```xml
<calendar name="event-calendar" title="Events"
          model="com.axelor.apps.base.db.Event"
          eventStart="startDate"
          eventStop="endDate"
          colorBy="status"
          mode="month">
  <field name="subject"/>
  <field name="status"/>
</calendar>
```

**Essential Attributes:**
- `eventStart` - Start date field
- `eventStop` - End date field
- `colorBy` - Field for color coding
- `mode` - View mode: `month`, `week`, `day`

### 5. Gantt View

Displays project tasks in Gantt chart format with timeline, dependencies, and resource allocation.

```xml
<gantt name="task-gantt" title="Project Tasks"
       model="com.axelor.apps.project.db.Task"
       start="startDate"
       finish="endDate"
       parent="parentTask">
  <field name="name"/>
  <field name="progress"/>
</gantt>
```

**Essential Attributes:**
- `start` - Start date field
- `finish` - End date field
- `parent` - Parent task field for hierarchy

### 6. Kanban View

Displays records as cards in a column-based workflow visualization with drag-and-drop between states.

```xml
<kanban name="task-kanban" title="Tasks"
        model="com.axelor.apps.project.db.Task"
        columnBy="status"
        sequenceBy="sequence">
  <field name="name"/>
  <field name="assignedTo"/>
  <field name="priority"/>
  <template><![CDATA[
    <div class="kanban-card">
      <h4>{{record.name}}</h4>
      <p>{{record.assignedTo.fullName}}</p>
    </div>
  ]]></template>
</kanban>
```

### 7. Cards View

Displays records as visual data cards in grid or list layout.

```xml
<cards name="product-cards" title="Products"
       model="com.axelor.apps.base.db.Product">
  <field name="name"/>
  <field name="description"/>
  <field name="image"/>
  <template><![CDATA[
    <div class="card-body">
      <h4>{{record.name}}</h4>
      <img ng-src="{{record.image}}"/>
      <p>{{record.description}}</p>
    </div>
  ]]></template>
</cards>
```

### 8. Chart View

Data visualization with bar, line, pie, and radar charts using aggregated data.

```xml
<chart name="sales-chart" title="Sales by Month"
       model="com.axelor.apps.sale.db.SaleOrder">
  <category key="orderMonth" type="month"/>
  <series key="totalAmount" aggregate="sum" title="Sales"/>
</chart>
```

### 9. Tree View

Displays hierarchical records in tree structure with parent-child relationships.

```xml
<tree name="category-tree" title="Categories"
      model="com.axelor.apps.base.db.Category">
  <column name="name" type="field"/>
  <column name="code" type="field"/>
  <node model="com.axelor.apps.base.db.Category"
        onClick="category.form.edit">
    <field name="name"/>
  </node>
</tree>
```

## Basic Components

### Field Element

The `<field>` element displays a domain model field.

```xml
<field name="name" title="Product Name" required="true" colSpan="6"/>
```

#### Essential Field Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| name | String | Field name from domain model (required) |
| title | String | Custom field label |
| colSpan | Integer | Column span (1-12 in form views) |
| widget | String | Custom widget type |
| required | Boolean | Makes field mandatory |
| readonly | Boolean | Makes field read-only |
| hidden | Boolean | Hides the field |

#### Conditional Field Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| showIf | Expression | Conditional display expression |
| hideIf | Expression | Conditional hide expression |
| readonlyIf | Expression | Conditional readonly expression |
| requiredIf | Expression | Conditional required expression |

#### Validation Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| validIf | Expression | Validation expression |
| min | Number | Minimum value for numeric fields |
| max | Number | Maximum value for numeric fields |
| precision | Integer | Total digits for decimals |
| scale | Integer | Decimal places |
| pattern | String | Regex pattern validation |

#### Display Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| showTitle | Boolean | Show/hide label |
| placeholder | String | Placeholder text |
| help | String | Help text tooltip |
| css | String | Custom CSS classes |
| icon | String | FontAwesome icon |
| height | Integer | Height for text-area/image |

#### Title and Help Convention (CRITICAL)

**1. Sentence Case**: Use **sentence case** for `title` and `help` attributes (capitalize only the first letter).

```xml
<!-- Correct -->
<field name="conversionCoefficient" title="Conversion coefficient"/>

<!-- Incorrect -->
<field name="conversionCoefficient" title="Conversion Coefficient"/>
```

**2. Avoid Duplication**: Do NOT add `title` or `help` attributes in views when they are already defined in the domain XML.

The `title` defined in the domain applies automatically everywhere. Adding it again in views:
- Creates maintenance burden (two places to update)
- Risks inconsistency (e.g., "Coefficient" in domain vs "Coef." in view)

```xml
<!-- Correct: Use domain title automatically -->
<field name="conversionCoefficient"/>

<!-- Incorrect: Redundant title -->
<field name="conversionCoefficient" title="Conversion coefficient"/>

<!-- Incorrect: Inconsistent abbreviation -->
<field name="conversionCoefficient" title="Coef."/>
```

**When to add title/help in views:**
- **Dummy fields** (`name="$calculated"`) - no domain definition exists
- **Explicit user request** for context-specific label
- **Different label needed** in specific view context (rare)

```xml
<!-- Correct: Dummy field needs title -->
<field name="$totalAmount" title="Total amount"/>
```

#### Relational Field Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| domain | String | Domain filter for options |
| target | String | Target model class |
| target-name | String | Display field name |
| onChange | String | Action on value change |
| onSelect | String | Custom selection action |
| canNew | Boolean | Allow creating new records |
| canEdit | Boolean | Allow editing records |
| canView | Boolean | Allow viewing records |
| form-view | String | Custom form view name |
| grid-view | String | Custom grid view name |

### Panel Element

The `<panel>` element groups related fields together.

```xml
<panel name="mainPanel" title="General Information" colSpan="12">
  <field name="name"/>
  <field name="code"/>
  <field name="description" colSpan="12"/>
</panel>
```

#### Panel Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| name | String | Unique panel identifier |
| title | String | Panel header title |
| colSpan | Integer | Column span (1-12) |
| showIf | Expression | Conditional display |
| hideIf | Expression | Conditional hide |
| readonly | Boolean | Makes all fields read-only |
| hidden | Boolean | Hides the panel |
| sidebar | Boolean | Places panel in sidebar |
| stacked | Boolean | Stacks panel elements vertically |
| itemSpan | Integer | Default colSpan for child elements |
| canCollapse | Boolean | Allows panel collapse |
| collapseIf | Expression | Auto-collapse condition |

### Button Element

Adds action buttons to forms and toolbars.

```xml
<button name="btnConfirm" title="Confirm"
        onClick="action-confirm-order"
        showIf="statusSelect == 1"
        icon="fa-check" css="btn-success"/>
```

#### Button Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| name | String | Unique button identifier |
| title | String | Button text |
| onClick | String | Action to execute |
| prompt | String | Confirmation message |
| showIf | Expression | Conditional display |
| hideIf | Expression | Conditional hide |
| readonlyIf | Expression | Conditional disable |
| icon | String | FontAwesome icon class |
| iconHover | String | Icon on hover |
| css | String | CSS classes |
| link | String | External link URL |
| colSpan | Integer | Column span in forms |

**Common Button CSS Classes:**
- `btn-primary` - Primary blue button
- `btn-success` - Green success button
- `btn-danger` - Red danger button
- `btn-warning` - Yellow warning button
- `btn-info` - Light blue info button

### Panel-Tabs Element

Creates tabbed panels for organizing content.

```xml
<panel-tabs name="mainTabs">
  <panel name="generalTab" title="General">
    <field name="name"/>
    <field name="code"/>
  </panel>
  <panel name="detailsTab" title="Details">
    <field name="description" colSpan="12" widget="html"/>
  </panel>
</panel-tabs>
```

### Separator Element

Adds visual separators and section titles.

```xml
<separator title="Address Information" colSpan="12"/>
```

### Label Element

Displays static text labels.

```xml
<label title="Please review the details before confirming."
       css="label-info" colSpan="12"/>
```

### Spacer Element

Adds empty space in layouts.

```xml
<spacer colSpan="6"/>
```

## Widgets Reference

For complete widget documentation, see @docs/views/menu-selection-reference.md

### Text Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| text | Single-line text input | `<field name="name"/>` |
| text-area | Multi-line text input | `<field name="notes" widget="text-area"/>` |
| html | HTML editor | `<field name="description" widget="html"/>` |
| password | Password input | `<field name="password" widget="password"/>` |
| email | Email with validation | `<field name="email" widget="email"/>` |
| url | URL with validation | `<field name="website" widget="url"/>` |
| phone | Phone number input | `<field name="phone" widget="phone"/>` |

### Numeric Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| integer | Integer input | `<field name="quantity"/>` |
| decimal | Decimal input | `<field name="price" x-scale="2"/>` |
| duration | Duration in seconds | `<field name="duration" widget="duration"/>` |
| progress | Progress bar (0-100) | `<field name="completion" widget="progress"/>` |
| rating | Star rating | `<field name="rating" widget="rating" max="5"/>` |

### Date/Time Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| date | Date picker | `<field name="orderDate"/>` |
| datetime | Date and time picker | `<field name="createdOn"/>` |
| time | Time picker | `<field name="startTime" widget="time"/>` |

### Boolean Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| checkbox | Standard checkbox | `<field name="active"/>` |
| boolean-switch | Toggle switch | `<field name="active" widget="boolean-switch"/>` |
| boolean-radio | Radio buttons (Yes/No) | `<field name="active" widget="boolean-radio"/>` |

### Selection Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| selection | Dropdown selection | `<field name="status" selection="status.select"/>` |
| radio-select | Radio button group | `<field name="type" widget="radio-select"/>` |
| multi-select | Multiple selection | `<field name="tags" widget="multi-select"/>` |

### Relational Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| many-to-one | Reference to single record | `<field name="category"/>` |
| ref-select | Dropdown for relations | `<field name="category" widget="ref-select"/>` |
| ref-text | Read-only reference display | `<field name="customer" widget="ref-text"/>` |

### Binary Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| binary | File upload | `<field name="attachment" widget="binary"/>` |
| binary-link | Download link for file | `<field name="document" widget="binary-link"/>` |
| image | Image upload/display | `<field name="photo" widget="image"/>` |

### Special Widgets

| Widget | Description | Example |
|--------|-------------|---------|
| color | Color picker | `<field name="color" widget="color"/>` |
| code-editor | Code editor with syntax | `<field name="script" widget="code-editor"/>` |
| json-field | JSON editor | `<field name="metadata" widget="json-field"/>` |

## Field Attributes Deep Dive

### Domain Filters

Domain filters restrict the available options for relational fields using SQL-like expressions.

```xml
<!-- Simple filter -->
<field name="customer" domain="self.isCustomer = true"/>

<!-- Multiple conditions -->
<field name="product"
       domain="self.active = true AND self.sellable = true AND self.category = :category"/>

<!-- Using parent field values -->
<field name="city"
       domain="self.country = :country AND self.state = :state"/>

<!-- Null checks -->
<field name="partner"
       domain="self.email IS NOT NULL AND self.blocked = false"/>

<!-- IN conditions -->
<field name="status"
       domain="self.statusSelect IN (1, 2, 3)"/>

<!-- Date comparisons -->
<field name="validFrom"
       domain="self.validUntil >= :today"/>

<!-- Self-referencing (exclude current record) -->
<field name="parentCategory"
       domain="self.id != :id"/>
```

### Conditional Expressions

Conditional expressions control field visibility and behavior dynamically.

**CRITICAL: NEVER USE `$get()` - IT IS DEPRECATED**

In recent versions of Axelor, `$get()` function is deprecated. Access properties directly.

```xml
<!-- WRONG - $get() is deprecated -->
<field name="discount" showIf="$get('totalAmount') > 1000"/>
<panel-related name="linesPanel" readonlyIf="$get('statusSelect') >= 3"/>

<!-- CORRECT - Direct property access -->
<field name="discount" showIf="totalAmount > 1000"/>
<panel-related name="linesPanel" readonlyIf="statusSelect >= 3"/>
```

**Available Variables:**
- `$user` - Current user object
- `$user.isAdmin` - Check if user is admin
- `$group` - Current user groups
- `$readonly` - Form readonly state
- `$popup` - True if in popup mode
- `record` - Current record
- `__parent__` - Parent record (in O2M context)
- `__this__` - Current record reference

**Expression Operators:**

```javascript
// Comparison
field == 'value'
field != 'value'
field > 100
field >= 100

// Logical
field1 == 'a' && field2 == 'b'
field1 == 'a' || field2 == 'b'
!field

// Null checks
field == null
field != null

// IN checks
status in [1, 2, 3]
status not in [4, 5]

// String operations
name.contains('test')
name.startsWith('ABC')
name.endsWith('.pdf')
```

**Examples:**

```xml
<!-- Status-based display -->
<field name="discount" showIf="totalAmount > 1000"/>
<field name="notes" hideIf="status == 'cancelled'"/>
<field name="amount" readonlyIf="status != 'draft'"/>

<!-- User permission-based display -->
<field name="adminField" showIf="$user.isAdmin"/>
<field name="groupField" showIf="$user.group == 'managers'"/>

<!-- Type-based display -->
<field name="weight" showIf="productType == '1'"/>
<field name="duration" showIf="productType == '2'"/>

<!-- Multiple conditions -->
<field name="specialDiscount"
       showIf="type == 'special' && active == true && $user.isAdmin"/>
```

## Layout System

### 12-Column Grid Layout

Forms use a 12-column grid system. Fields can span 1-12 columns using `colSpan`.

```xml
<panel name="mainPanel">
  <!-- Full width -->
  <field name="description" colSpan="12"/>

  <!-- Half width -->
  <field name="firstName" colSpan="6"/>
  <field name="lastName" colSpan="6"/>

  <!-- One-third width -->
  <field name="startDate" colSpan="4"/>
  <field name="endDate" colSpan="4"/>
  <field name="duration" colSpan="4"/>

  <!-- Two-thirds + one-third -->
  <field name="address" colSpan="8"/>
  <field name="postalCode" colSpan="4"/>

  <!-- Three columns -->
  <field name="city" colSpan="4"/>
  <field name="state" colSpan="4"/>
  <field name="country" colSpan="4"/>
</panel>
```

### Sidebar Layout

Sidebar panels display metadata, status, and secondary information.

```xml
<panel name="sidePanel" sidebar="true" title="Status">
  <field name="statusSelect" showTitle="false" widget="nav-select"/>
  <field name="active" widget="boolean-switch"/>
  <separator/>
  <field name="createdOn" readonly="true"/>
  <field name="createdBy" readonly="true"/>
  <field name="updatedOn" readonly="true"/>
  <field name="updatedBy" readonly="true"/>
</panel>
```

## Form Events

### onNew Event

Triggered when creating a new record.

```xml
<form name="sale-order-form" onNew="action-group-sale-order-onnew">
</form>
```

### onLoad Event

Triggered when loading an existing record.

```xml
<form name="sale-order-form" onLoad="action-sale-order-onload">
</form>
```

### onSave Event

Triggered before saving (for validation).

```xml
<form name="sale-order-form" onSave="action-group-sale-order-validate">
</form>
```

### onChange Event

Triggered when field value changes.

```xml
<field name="customer" onChange="action-group-customer-change"/>
```

### onSelect Event

Custom selection logic for relational fields.

```xml
<field name="product" onSelect="action-product-onselect"/>
```

## Grid-Specific Features

### Column Definition

```xml
<field name="name"              <!-- Field name (required) -->
       title="Product Name"     <!-- Custom column header -->
       width="200"              <!-- Column width in pixels -->
       hidden="false"           <!-- Hide column -->
       readonly="false"         <!-- Make column read-only -->
       aggregate="sum"          <!-- Aggregation function -->
/>
```

### Aggregation Functions

| Function | Description | Example |
|----------|-------------|---------|
| sum | Sum numeric values | `<field name="totalAmount" aggregate="sum"/>` |
| avg | Average values | `<field name="rating" aggregate="avg"/>` |
| count | Count records | `<field name="id" aggregate="count"/>` |
| min | Minimum value | `<field name="minPrice" aggregate="min"/>` |
| max | Maximum value | `<field name="maxPrice" aggregate="max"/>` |

### Order By Syntax

```xml
<!-- Ascending order -->
<grid orderBy="name"/>

<!-- Descending order (prefix with -) -->
<grid orderBy="-createdOn"/>

<!-- Multiple fields -->
<grid orderBy="category,name"/>
<grid orderBy="-orderDate,-orderNumber"/>

<!-- Mixed order -->
<grid orderBy="category,-createdOn,name"/>
```

## Critical View Limitations

### CSS Custom Not Supported

**CRITICAL:** Axelor Open Platform does **NOT** support custom CSS files in modules.

```xml
<!-- WRONG - CSS files are NOT loaded by AOP -->
<grid name="sale-order-line-grid" extension="true">
  <extend target="/">
    <attribute name="css" value="my-custom-styles"/>
  </extend>
</grid>

<!-- my-custom-styles.css will NOT be loaded -->
.my-custom-styles tr[data-field="true"] {
  background-color: #f8f9fa;
}
```

**CORRECT Alternatives:**

**1. Use `<hilite>` for row coloring:**
```xml
<grid name="sale-order-line-grid" extension="true">
  <hilite background="light-gray" if="isOptionLine"/>
  <hilite color="success" if="isActive"/>
  <hilite color="danger" if="isBlocked"/>
</grid>
```


**2. Use computed fields with inline `<viewer>` for custom styling:**
```xml
<field name="$statusBadge" readonly="true" width="120">
  <viewer><![CDATA[
    <>
      <Badge style={{
        backgroundColor: record.isActive ? '#d4edda' : '#f8f9fa',
        color: record.isActive ? '#155724' : '#6c757d'
      }}>
        {record.status}
      </Badge>
    </>
  ]]></viewer>
</field>
```

**3. Use widgets with built-in styling:**
```xml
<field name="priority" widget="rating" max="5"/>
<field name="progress" widget="progress"/>
<field name="active" widget="boolean-switch"/>
```

## Best Practices

### Naming Conventions

**Views:**
```
{model}-form          → contact-form
{model}-grid          → contact-grid
{model}-{purpose}     → contact-selection-form
```

**Fields:**
```
Use domain field names directly
```

**Buttons:**
```
btn{Action}          → btnConfirm, btnCancel, btnSave
```

### Layout Best Practices

1. **Use colSpan="12"** for full-width fields (HTML editors, images, grids)
2. **Group related fields** logically in panels
3. **Use sidebar="true"** for metadata and status information
4. **Use panel-tabs** for organizing extensive content
5. **Provide helpful placeholders** and help text

### Performance Best Practices

1. **Specify views explicitly** in panel-related for better performance
2. **Use domain filters** to limit data in relational fields
3. **Limit fields in grids** - don't include unnecessary columns
4. **Use hidden="true"** for search-only fields

### UX Best Practices

1. **Always provide icons** for buttons
2. **Use meaningful titles** with i18n keys
3. **Add confirmation prompts** for destructive actions
4. **Use appropriate column spans** for readable layouts
5. **Follow AOS naming conventions** for consistency

## View Extensions

For extending existing views without modifying originals, see **@docs/views/view-extensions.md**.

Extension views allow you to:
- Add custom fields to AOS standard views
- Modify behavior of existing views
- Maintain upgrade compatibility

**Quick Example:**
```xml
<form name="partner-form" id="mymodule-partner-form-ext" extension="true">
  <extend target="//panel[@name='contactPanel']">
    <insert position="after">
      <panel name="customPanel" title="Custom Fields">
        <field name="customField"/>
      </panel>
    </insert>
  </extend>
</form>
```

## Related Documentation

- **View Extensions**: @docs/views/view-extensions.md
- **Actions**: @docs/views/action-patterns.md
- **Menus and Selections**: @docs/views/menu-selection-reference.md
- **XSD Schema**: @skills/axelor-xml-validator/reference/object-views-reference.md
