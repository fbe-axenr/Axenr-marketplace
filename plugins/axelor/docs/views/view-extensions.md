# View Extensions Reference

Complete reference for extending existing Axelor views without modifying original files.

## Overview

**IMPORTANT:** Extension views (`extension="true"` with `<extend>` elements) are **only supported for `form` and `grid` views**.

For other view types (tree, calendar, kanban, cards, gantt, chart, dashboard), you must use **full override**: rewrite the entire view with a unique `id` attribute.

Extension views allow you to modify existing form and grid views defined in other modules without altering the original XML files. This is essential for:

- Adding custom fields to AOS (Axelor Open Suite) standard views
- Modifying behavior of existing views
- Conditional customization based on installed modules or features
- Maintaining upgrade compatibility

> **FILE NAMING CONVENTION:** When extending views for an entity (e.g., partner-form, partner-grid), it is recommended to create a file with the **SAME NAME** as the entity. For example, to extend Partner views, create `Partner.xml` in your views directory (NOT `PartnerExtension.xml` or `PartnerViews.xml`).

**Recommended file structure:**
```
src/main/resources/views/
├── Partner.xml          # Extensions of partner-form, partner-grid, etc.
├── Product.xml          # Extensions of product-form, product-grid, etc.
├── SaleOrder.xml        # Extensions of sale-order-form, sale-order-grid, etc.
└── MyNewEntity.xml      # Views for your own new entities
```

## Extension View Structure

### Basic Syntax

An extension view must have:
1. **Same `name`** as the original view
2. **Unique `id`** attribute
3. **`extension="true"`** attribute

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<object-views xmlns="http://axelor.com/xml/ns/object-views"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://axelor.com/xml/ns/object-views
              https://axelor.com/xml/ns/object-views/object-views_7.4.xsd">

  <!-- Extension of an existing form view -->
  <form name="partner-form" id="custom-partner-form-extension" extension="true">

    <extend target="//panel[@title='Contact']">
      <insert position="after">
        <panel name="customPanel" title="Custom Information">
          <field name="customField1"/>
          <field name="customField2"/>
        </panel>
      </insert>
    </extend>

  </form>

</object-views>
```

### Extension Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Must match the original view name exactly |
| `id` | Yes | Unique identifier for this extension |
| `extension` | Yes | Must be `"true"` |

## The `<extend>` Element

The `<extend>` element defines what to modify in the original view.

### Attributes

| Attribute | Required | Description |
|-----------|----------|-------------|
| `target` | Yes | XPath expression to select the target element |
| `if-feature` | No | Apply only if feature is enabled (via AppConfig) |
| `if-module` | No | Apply only if specified module is installed |

### XPath Target Examples

```xml
<!-- Target panel by title -->
<extend target="//panel[@title='Contact']">

<!-- Target panel by name -->
<extend target="//panel[@name='mainPanel']">

<!-- Target field by name -->
<extend target="//field[@name='fullName']">

<!-- Target button by name -->
<extend target="//button[@name='btnValidate']">

<!-- Target sidebar panel -->
<extend target="//panel[@sidebar='true']">

<!-- Target panel-tabs -->
<extend target="//panel-tabs[@name='mainTabs']">

<!-- Target root element (the form/grid itself) -->
<extend target="/">

<!-- Target toolbar -->
<extend target="//toolbar">

<!-- Target first panel -->
<extend target="//panel[1]">
```

### Conditional Extensions

```xml
<!-- Apply only if module is installed -->
<extend target="//panel[@name='contactPanel']" if-module="axelor-crm">
  <insert position="after">
    <field name="crmSpecificField"/>
  </insert>
</extend>

<!-- Apply only if feature is enabled -->
<extend target="//panel[@name='billingPanel']" if-feature="billing.advanced">
  <insert position="inside">
    <field name="advancedBillingField"/>
  </insert>
</extend>
```

## Extension Operations

### 1. Insert Operation

Inserts new elements at a position relative to the target element.

**Syntax:**
```xml
<insert position="before|after|inside">
  <!-- Elements to insert -->
</insert>
```

**Position Values:**

| Position | Description |
|----------|-------------|
| `before` | Insert before the target element |
| `after` | Insert after the target element |
| `inside` | Insert inside the target element (as last child) |

**Examples:**

```xml
<!-- Add a panel after an existing panel -->
<extend target="//panel[@title='General']">
  <insert position="after">
    <panel name="customPanel" title="Custom Details" colSpan="12">
      <field name="customCode"/>
      <field name="customName"/>
    </panel>
  </insert>
</extend>

<!-- Add fields inside an existing panel -->
<extend target="//panel[@name='mainPanel']">
  <insert position="inside">
    <field name="additionalField1" colSpan="6"/>
    <field name="additionalField2" colSpan="6"/>
  </insert>
</extend>

<!-- Add a button before another button -->
<extend target="//button[@name='btnConfirm']">
  <insert position="before">
    <button name="btnPreValidate" title="Pre-Validate"
            onClick="action-pre-validate"/>
  </insert>
</extend>

<!-- Add toolbar button (targeting root) -->
<extend target="/">
  <insert position="inside">
    <toolbar>
      <button name="btnCustomAction" title="Custom Action"
              onClick="action-custom"/>
    </toolbar>
  </insert>
</extend>
```

**Root Element Positioning:**

When targeting the root element (`/`):
- `before` means before the first child element
- `after` means after the last child element
- `<toolbar>` and `<menubar>` elements are automatically kept at the top

### 2. Replace Operation

Replaces the target element with new content.

**Syntax:**
```xml
<replace>
  <!-- Elements to replace the target with -->
</replace>
```

**Examples:**

```xml
<!-- Replace a field with a different widget -->
<extend target="//field[@name='description']">
  <replace>
    <field name="description" widget="html" colSpan="12" height="200"/>
  </replace>
</extend>

<!-- Replace a panel with a different structure -->
<extend target="//panel[@name='oldPanel']">
  <replace>
    <panel name="newPanel" title="Enhanced Panel" colSpan="12">
      <field name="field1"/>
      <field name="field2"/>
      <panel-related field="lines" colSpan="12"/>
    </panel>
  </replace>
</extend>

<!-- Remove an element entirely (empty replace) -->
<extend target="//field[@name='obsoleteField']">
  <replace/>
</extend>

<!-- Remove a button -->
<extend target="//button[@name='btnUnwanted']">
  <replace/>
</extend>
```

**Important Notes:**
- Only one replace operation applies per target element
- Empty `<replace/>` removes the target element entirely
- Use with caution as it completely overrides the original

### 3. Move Operation

Relocates an existing element to a new position.

**Syntax:**
```xml
<move position="before|after|inside" source="<XPath expression>"/>
```

**Examples:**

```xml
<!-- Move a panel before another panel -->
<extend target="//panel[@name='targetPanel']">
  <move position="before" source="//panel[@name='panelToMove']"/>
</extend>

<!-- Move a field inside a different panel -->
<extend target="//panel[@name='destinationPanel']">
  <move position="inside" source="//field[@name='fieldToMove']"/>
</extend>

<!-- Move sidebar panel to main area -->
<extend target="//panel[@name='mainPanel']">
  <move position="after" source="//panel[@sidebar='true' and @name='infoPanel']"/>
</extend>
```

### 4. Attribute Operation

Modifies attributes of the target element.

**Syntax:**
```xml
<attribute name="<attribute name>" value="<attribute value>"/>
```

**Examples:**

```xml
<!-- Make a field readonly -->
<extend target="//field[@name='code']">
  <attribute name="readonly" value="true"/>
</extend>

<!-- Change field colSpan -->
<extend target="//field[@name='name']">
  <attribute name="colSpan" value="12"/>
</extend>

<!-- Add a widget to a field -->
<extend target="//field[@name='status']">
  <attribute name="widget" value="NavSelect"/>
</extend>

<!-- Add showIf condition -->
<extend target="//panel[@name='conditionalPanel']">
  <attribute name="showIf" value="type == 'ADVANCED'"/>
</extend>

<!-- Remove an attribute (empty value) -->
<extend target="//field[@name='optionalField']">
  <attribute name="required" value=""/>
</extend>

<!-- Change panel title -->
<extend target="//panel[@name='detailsPanel']">
  <attribute name="title" value="Enhanced Details"/>
</extend>

<!-- Add CSS class to button -->
<extend target="//button[@name='btnAction']">
  <attribute name="css" value="btn-primary"/>
</extend>

<!-- Modify domain filter -->
<extend target="//field[@name='partner']">
  <attribute name="domain" value="self.isCustomer = true AND self.active = true"/>
</extend>
```

## Common Extension Patterns

### Pattern 1: Add Custom Fields to AOS Entity Form

```xml
<form name="partner-form" id="mymodule-partner-form-ext" extension="true">

  <!-- Add custom panel after Contact panel -->
  <extend target="//panel[@title='Contact']">
    <insert position="after">
      <panel name="customClassificationPanel" title="Customer Classification" colSpan="12">
        <field name="customerTier" widget="NavSelect"
               selection="mymodule.customer.tier.select"/>
        <field name="segmentCode"/>
        <field name="acquisitionDate"/>
        <field name="lifetimeValue" readonly="true"/>
      </panel>
    </insert>
  </extend>

</form>
```

### Pattern 2: Add Fields to Existing Panel

```xml
<form name="product-form" id="mymodule-product-form-ext" extension="true">

  <!-- Add fields inside the main panel -->
  <extend target="//panel[@name='mainPanel']">
    <insert position="inside">
      <field name="customSku" colSpan="4"/>
      <field name="customBarcode" colSpan="4"/>
      <field name="customOrigin" colSpan="4"/>
    </insert>
  </extend>

</form>
```

### Pattern 3: Add Tab to Existing Panel-Tabs

```xml
<form name="sale-order-form" id="mymodule-sale-order-form-ext" extension="true">

  <!-- Add new tab to existing tabs -->
  <extend target="//panel-tabs[@name='mainTabs']">
    <insert position="inside">
      <panel name="customAnalyticsTab" title="Analytics">
        <field name="marginPercent" readonly="true"/>
        <field name="profitabilityScore" widget="progress"/>
        <panel-dashlet name="salesTrendChart" action="action-chart-sales-trend"
                       colSpan="12" height="300"/>
      </panel>
    </insert>
  </extend>

</form>
```

### Pattern 4: Add Toolbar Buttons

```xml
<form name="invoice-form" id="mymodule-invoice-form-ext" extension="true">

  <!-- Add button to toolbar -->
  <extend target="//toolbar">
    <insert position="inside">
      <button name="btnCustomExport" title="Export to ERP"
              icon="fa-cloud-upload"
              showIf="statusSelect == 3"
              onClick="action-invoice-method-export-erp"/>
    </insert>
  </extend>

</form>
```

### Pattern 5: Extend Grid View

```xml
<grid name="partner-grid" id="mymodule-partner-grid-ext" extension="true">

  <!-- Add column after name -->
  <extend target="//field[@name='name']">
    <insert position="after">
      <field name="customerTier" width="100"/>
      <field name="segmentCode" width="80"/>
    </insert>
  </extend>

  <!-- Add hilite for customer tier -->
  <extend target="/">
    <insert position="inside">
      <hilite color="success" if="customerTier == 'GOLD'"/>
      <hilite color="warning" if="customerTier == 'SILVER'"/>
    </insert>
  </extend>

</grid>
```

### Pattern 6: Conditional Extension Based on Module

```xml
<form name="project-form" id="mymodule-project-form-ext" extension="true">

  <!-- Add CRM-specific fields only if CRM module is installed -->
  <extend target="//panel[@name='mainPanel']" if-module="axelor-crm">
    <insert position="inside">
      <field name="linkedOpportunity"/>
      <field name="salesPerson"/>
    </insert>
  </extend>

  <!-- Add HR-specific fields only if HR module is installed -->
  <extend target="//panel[@name='teamPanel']" if-module="axelor-human-resource">
    <insert position="inside">
      <field name="timesheet"/>
      <field name="expenses"/>
    </insert>
  </extend>

</form>
```

### Pattern 7: Modify Field Behavior

```xml
<form name="sale-order-line-form" id="mymodule-sol-form-ext" extension="true">

  <!-- Make price field readonly based on custom condition -->
  <extend target="//field[@name='price']">
    <attribute name="readonlyIf" value="priceLocked == true"/>
  </extend>

  <!-- Add domain filter to product field -->
  <extend target="//field[@name='product']">
    <attribute name="domain" value="self.sellable = true AND self.customApproved = true"/>
  </extend>

  <!-- Change widget for discount field -->
  <extend target="//field[@name='discountAmount']">
    <attribute name="widget" value="Slider"/>
    <attribute name="max" value="50"/>
  </extend>

</form>
```

### Pattern 8: Remove Unwanted Elements

```xml
<form name="partner-form" id="mymodule-partner-form-cleanup" extension="true">

  <!-- Remove a field not needed in this context -->
  <extend target="//field[@name='unusedField']">
    <replace/>
  </extend>

  <!-- Remove an entire panel -->
  <extend target="//panel[@name='deprecatedPanel']">
    <replace/>
  </extend>

</form>
```

## Best Practices

### 1. Naming Conventions

```
Extension ID format: {module}-{original-view-name}-ext

Examples:
- mymodule-partner-form-ext
- mymodule-sale-order-grid-ext
- crm-lead-form-custom-ext
```

### 2. XPath Validation - CRITICAL REQUIREMENTS

> **MANDATORY FOR AI AGENTS:** Before generating ANY view extension code, you MUST verify that the target XPath expression is **UNIQUE** and **CORRECTLY IDENTIFIES** the target element. Non-unique or incorrect XPath expressions cause runtime errors, silent failures, or modifications to wrong elements.

#### XPath Validation Workflow

**Step 1: Read the Source View XML**

Before creating any extension, you MUST:
1. Identify the module containing the original view
2. Read the complete source view XML file
3. Understand the view structure and element hierarchy

**Step 2: Identify the Target Element**

Examine the source view to find the exact element you want to target:

```xml
<!-- Source view: axelor-base/src/main/resources/views/Partner.xml -->
<form name="partner-form" title="Partner">
  <panel name="mainPanel" title="Main Information">
    <field name="code"/>
    <field name="name"/>
    <field name="partnerCategory"/>
  </panel>
  <panel name="contactPanel" title="Contact">
    <field name="email"/>
    <field name="phone"/>
  </panel>
  <panel name="addressPanel" title="Address">
    <field name="mainAddress"/>
  </panel>
</form>
```

**Step 3: Construct the XPath Expression**

Build an XPath that uniquely identifies the target:

```xml
<!-- GOOD: Target panel by unique name attribute -->
Target: <panel name="contactPanel" title="Contact">
XPath:  //panel[@name='contactPanel']
Matches: 1 element ✓

<!-- GOOD: Target field by name within context -->
Target: <field name="email"/>
XPath:  //field[@name='email']
Matches: 1 element ✓

<!-- BAD: Ambiguous - multiple panels exist -->
Target: <panel name="mainPanel">
XPath:  //panel
Matches: 3 elements ✗ (ambiguous!)

<!-- FIX: Add unique identifier -->
XPath:  //panel[@name='mainPanel']
Matches: 1 element ✓
```

**Step 4: Verify XPath Uniqueness**

**CRITICAL:** You MUST verify that the XPath matches exactly ONE element in the source view.

**Verification Method 1: Manual Count**
```xml
<!-- Source view analysis -->
Count occurrences of target attributes:
- How many <panel name="contactPanel"> exist? → Should be 1
- How many <field name="email"> exist? → Should be 1
- How many elements match //panel[@title='Contact']? → Could be multiple!
```

**Verification Method 2: XPath Expression Analysis**

```xml
<!-- UNIQUE: Using name attribute (usually unique) -->
//panel[@name='contactPanel']           ✓ SAFE

<!-- AMBIGUOUS: Using title only (may have duplicates) -->
//panel[@title='Contact']                ✗ RISKY

<!-- AMBIGUOUS: Generic tag without attributes -->
//panel                                  ✗ DANGEROUS

<!-- UNIQUE: Full path from root -->
//form[@name='partner-form']/panel[@name='contactPanel']  ✓ MOST SPECIFIC
```

**Step 5: Handle Non-Unique Scenarios**

If your initial XPath matches multiple elements, refine it:

```xml
<!-- Problem: Multiple fields named 'name' in different panels -->
Source:
<panel name="companyPanel">
  <field name="name"/>  <!-- Company name -->
</panel>
<panel name="contactPanel">
  <field name="name"/>  <!-- Contact name -->
</panel>

<!-- BAD: Ambiguous -->
<extend target="//field[@name='name']">  <!-- Which one? ✗ -->

<!-- SOLUTION 1: Add parent context -->
<extend target="//panel[@name='contactPanel']/field[@name='name']">  ✓

<!-- SOLUTION 2: Use full path -->
<extend target="//form[@name='partner-form']/panel[@name='contactPanel']/field[@name='name']">  ✓
```

#### XPath Uniqueness Checklist

Before generating extension code, verify:

- [ ] **Source view read**: Loaded and analyzed the original view XML
- [ ] **Target identified**: Know exactly which element to extend
- [ ] **XPath constructed**: Built an expression targeting that element
- [ ] **Uniqueness verified**: XPath matches EXACTLY 1 element (not 0, not multiple)
- [ ] **Attributes validated**: All attribute names and values are correct (case-sensitive!)
- [ ] **Position valid**: Insert position makes sense for the element type
- [ ] **Context checked**: Considered parent/sibling elements for context

#### Common XPath Uniqueness Patterns

**Pattern 1: Target by Unique Name Attribute**

```xml
<!-- BEST PRACTICE: name attribute is usually unique -->
<extend target="//panel[@name='contactPanel']">        ✓ RECOMMENDED
<extend target="//field[@name='email']">               ✓ RECOMMENDED
<extend target="//button[@name='btnValidate']">        ✓ RECOMMENDED
```

**Pattern 2: Combine Multiple Attributes**

```xml
<!-- When name alone isn't unique, add more attributes -->
<extend target="//panel[@name='detailPanel'][@title='Details']">  ✓ GOOD
<extend target="//field[@name='amount'][@widget='decimal']">      ✓ GOOD
```

**Pattern 3: Use Parent Context**

```xml
<!-- Scope the search within a specific parent -->
<extend target="//panel[@name='mainPanel']/field[@name='code']">           ✓ GOOD
<extend target="//panel-tabs[@name='tabs']/panel[@name='detailsTab']">     ✓ GOOD
<extend target="//form[@name='partner-form']/panel[@name='contactPanel']"> ✓ VERY SPECIFIC
```

**Pattern 4: Avoid Position-Based Selectors**

```xml
<!-- AVOID: Position can change with other extensions -->
<extend target="//panel[1]">                  ✗ FRAGILE
<extend target="//field[3]">                  ✗ FRAGILE

<!-- PREFER: Attribute-based selectors -->
<extend target="//panel[@name='firstPanel']"> ✓ STABLE
<extend target="//field[@name='thirdField']"> ✓ STABLE
```

#### XPath Validation Examples

**Example 1: Valid Unique XPath**

```xml
<!-- Source View -->
<form name="product-form">
  <panel name="mainPanel">
    <field name="code"/>
    <field name="name"/>
    <field name="salePrice"/>
  </panel>
</form>

<!-- Extension: Add field after salePrice -->
<!-- XPath Analysis: -->
<!--   //field[@name='salePrice'] → 1 match ✓ -->
<extend target="//field[@name='salePrice']">
  <insert position="after">
    <field name="costPrice"/>
  </insert>
</extend>
```

**Example 2: Non-Unique XPath - WRONG**

```xml
<!-- Source View -->
<form name="order-form">
  <panel name="headerPanel">
    <field name="status"/>  <!-- Order status -->
  </panel>
  <panel name="linePanel">
    <field name="status"/>  <!-- Line status -->
  </panel>
</form>

<!-- WRONG: Ambiguous XPath -->
<!-- XPath Analysis: -->
<!--   //field[@name='status'] → 2 matches ✗ AMBIGUOUS! -->
<extend target="//field[@name='status']">  <!-- ERROR: Which status field? -->
  <attribute name="readonly" value="true"/>
</extend>

<!-- CORRECT: Add parent context -->
<!-- XPath Analysis: -->
<!--   //panel[@name='headerPanel']/field[@name='status'] → 1 match ✓ -->
<extend target="//panel[@name='headerPanel']/field[@name='status']">
  <attribute name="readonly" value="true"/>
</extend>
```

**Example 3: Multiple Refinement Steps**

```xml
<!-- Source View: Complex nested structure -->
<form name="invoice-form">
  <panel name="mainPanel">
    <panel name="detailPanel" title="Invoice Details">
      <field name="invoiceDate"/>
      <field name="dueDate"/>
    </panel>
  </panel>
  <panel name="linePanel">
    <panel name="detailPanel" title="Line Details">
      <field name="description"/>
    </panel>
  </panel>
</form>

<!-- Problem: Two panels named 'detailPanel' -->

<!-- Attempt 1: Too generic -->
<extend target="//panel[@name='detailPanel']">
<!-- XPath matches: 2 elements ✗ AMBIGUOUS -->

<!-- Attempt 2: Add title attribute -->
<extend target="//panel[@name='detailPanel'][@title='Invoice Details']">
<!-- XPath matches: 1 element ✓ UNIQUE -->

<!-- Attempt 3: Use parent context (even better) -->
<extend target="//panel[@name='mainPanel']/panel[@name='detailPanel']">
<!-- XPath matches: 1 element ✓ UNIQUE and CONTEXT-AWARE -->
```

#### Tools for XPath Verification

**Method 1: Manual Source View Inspection**
```bash
# Read the source view XML
cat axelor-base/src/main/resources/views/Partner.xml

# Count occurrences of target attribute
grep -c 'name="contactPanel"' axelor-base/src/main/resources/views/Partner.xml
# Expected output: 1 (for unique)
```

**Method 2: XML Validation in IDE**
- Open source view in IDE with XML support
- Use "Find in File" to count matches for your target attributes
- Verify only one element matches your criteria

**Method 3: Browser Developer Tools (Runtime)**
- Open the form in Axelor application
- Inspect the rendered view using browser DevTools
- Use console to test XPath: `$x("//panel[@name='contactPanel']")`
- Verify only one element is returned

#### Critical Failure Scenarios

**Failure 1: XPath Matches Zero Elements**

```xml
<!-- CAUSE: Target element doesn't exist -->
<extend target="//field[@name='nonExistentField']">
  <!-- ERROR: No such field in source view! -->
</extend>

<!-- CONSEQUENCE: Extension silently ignored, no error logged -->
<!-- FIX: Read source view first, verify element exists -->
```

**Failure 2: XPath Matches Multiple Elements**

```xml
<!-- CAUSE: Ambiguous selector -->
<extend target="//panel[@title='Details']">
  <!-- ERROR: 3 panels have title='Details' -->
</extend>

<!-- CONSEQUENCE: Extension applied to ALL matches → unexpected behavior -->
<!-- FIX: Use unique identifier or add parent context -->
```

**Failure 3: Wrong Insert Position**

```xml
<!-- CAUSE: Invalid position for element type -->
<extend target="//field[@name='code']">
  <insert position="inside">  <!-- ERROR: Field can't have children! -->
    <field name="subField"/>
  </insert>
</extend>

<!-- CONSEQUENCE: Runtime error or ignored extension -->
<!-- FIX: Use 'after' or 'before' for field elements -->
```

#### Best Practices Summary

```xml
<!-- ✓ DO: Use unique name attributes -->
<extend target="//panel[@name='contactPanel']">

<!-- ✓ DO: Verify XPath uniqueness before generating code -->
<!-- Count matches: //panel[@name='contactPanel'] → must be 1 -->

<!-- ✓ DO: Use parent context for disambiguation -->
<extend target="//panel[@name='mainPanel']/field[@name='code']">

<!-- ✓ DO: Combine attributes for extra safety -->
<extend target="//panel[@name='detailPanel'][@title='Details']">

<!-- ✗ DON'T: Use position-based selectors -->
<extend target="//panel[1]">

<!-- ✗ DON'T: Use title-only selectors (i18n sensitive) -->
<extend target="//panel[@title='Contact']">

<!-- ✗ DON'T: Generate extensions without reading source view -->
<!-- ALWAYS read the source view XML first! -->

<!-- ✗ DON'T: Assume XPath is unique without verification -->
<!-- ALWAYS count matches before generating code! -->
```

### 3. Minimize Replace Operations

```xml
<!-- PREFER: Attribute modifications -->
<extend target="//field[@name='code']">
  <attribute name="readonly" value="true"/>
  <attribute name="colSpan" value="6"/>
</extend>

<!-- AVOID: Full replacement when not necessary -->
<extend target="//field[@name='code']">
  <replace>
    <field name="code" readonly="true" colSpan="6"/>
  </replace>
</extend>
```

### 4. Document Extension Purpose

```xml
<!--
  Extension: Add customer classification fields
  Target: Partner form view
  Requirement: EPIC-001-US-003
  Author: Development Team
-->
<form name="partner-form" id="mymodule-partner-form-ext" extension="true">
  ...
</form>
```

## Extension Priority

When multiple extensions target the same view:

1. Extensions are applied in order of module dependency
2. Extensions within the same module are applied in file load order
3. Computed views are regenerated automatically when base view or extensions change

## Troubleshooting

### Common Issues

**1. Extension not applied:**
- Verify `extension="true"` attribute is present
- Verify `name` matches original view exactly
- Verify `id` is unique
- Check module dependency order

**2. XPath not finding target:**
- Use browser developer tools to inspect the original view XML
- Verify attribute names and values match exactly
- Use `//` for descendant search if element depth varies

**3. Insert position unexpected:**
- Remember root target (`/`) has special positioning rules
- `before`/`after` are relative to target, not absolute

**4. Attribute modification not working:**
- Verify attribute name is correct for element type
- Empty value removes attribute, not sets it to empty string

## Related Documentation

- **View Reference**: @docs/views/view-reference.md
- **Action Patterns**: @docs/views/action-patterns.md
- **Domain Patterns**: @docs/domains/domain-patterns.md (for entity extension)
- **Official Documentation**: https://docs.axelor.com/adk/{aopVmajor.aopVminor}/dev-guide/views/extensions.html
