# Menu and Selection Reference

Complete guide to menus, menubar, toolbar, and selections in Axelor views.

## Menu System

### Application Menus (menuitem)

Application-level menus appear in the main navigation sidebar.

#### Basic Menu Structure

```xml
<menuitem name="menu-products-root" title="Products"
          order="10"/>

<menuitem name="menu-products" title="Products"
          parent="menu-products-root"
          action="action.view.products"
          order="10"/>

<action-view name="action.view.products" title="Products"
             model="com.axelor.apps.base.db.Product">
  <view type="grid" name="product-grid"/>
  <view type="form" name="product-form"/>
</action-view>
```

#### Menu Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| name | String | Unique menu identifier (required) |
| title | String | Menu label (required) |
| parent | String | Parent menu name for hierarchy |
| action | String | Action to execute when clicked |
| order | Integer | Display order (lower = first) |
| icon | String | FontAwesome icon class |
| groups | String | User groups allowed to see menu |
| module | String | Module name for conditional loading |
| hidden | Boolean | Hide menu item |
| tag | String | Badge tag (e.g., "new", "beta") |
| tagStyle | String | Badge style CSS |

#### Menu Hierarchy

```xml
<!-- Root menu (no parent, no action) -->
<menuitem name="menu-sales-root" title="Sales" order="20"/>

<!-- Submenu level 1 -->
<menuitem name="menu-sale-orders" title="Sale Orders"
          parent="menu-sales-root"
          action="action.view.sale.orders"
          order="10"/>

<!-- Submenu level 2 -->
<menuitem name="menu-sale-orders-draft" title="Draft Orders"
          parent="menu-sales-root"
          action="action.view.sale.orders.draft"
          order="11"/>

<menuitem name="menu-sale-orders-confirmed" title="Confirmed Orders"
          parent="menu-sales-root"
          action="action.view.sale.orders.confirmed"
          order="12"/>
```

#### Menu with Icons

```xml
<menuitem name="menu-products" title="Products"
          parent="menu-products-root"
          action="action.view.products"
          icon="fa-cube"
          order="10"/>

<menuitem name="menu-customers" title="Customers"
          parent="menu-crm-root"
          action="action.view.customers"
          icon="fa-users"
          order="20"/>

<menuitem name="menu-invoices" title="Invoices"
          parent="menu-accounting-root"
          action="action.view.invoices"
          icon="fa-file-invoice"
          order="30"/>
```

#### Menu with Permissions

```xml
<menuitem name="menu-admin-settings" title="Settings"
          parent="menu-admin-root"
          action="action.view.settings"
          groups="admins"
          order="100"/>

<menuitem name="menu-reports" title="Reports"
          parent="menu-root"
          action="action.view.reports"
          groups="managers,directors"
          order="50"/>
```

### Menubar in Forms

Menubar provides dropdown menus in forms for organizing related actions.

#### Basic Menubar

```xml
<form name="sale-order-form" title="Sale Order"
      model="com.axelor.apps.sale.db.SaleOrder">

  <menubar>
    <menu name="menuActions" title="Actions" icon="fa-cog">
      <item name="itemConfirm" title="Confirm Order"
            action="action-order-confirm"
            showIf="statusSelect == 1"/>
      <item name="itemCancel" title="Cancel Order"
            action="action-order-cancel"
            showIf="statusSelect in (1, 2)"/>
      <item name="itemDuplicate" title="Duplicate"
            action="action-order-duplicate"/>
    </menu>

    <menu name="menuReports" title="Reports" icon="fa-file-pdf">
      <item name="itemPrintOrder" title="Print Order"
            action="action-order-print"/>
      <item name="itemExportPDF" title="Export PDF"
            action="action-order-export-pdf"/>
    </menu>
  </menubar>

  <!-- Form content -->
</form>
```

#### Menubar Attributes

**Menu Attributes:**
- `name` - Unique menu identifier
- `title` - Menu label
- `icon` - FontAwesome icon
- `showIf` - Conditional display expression
- `hideIf` - Conditional hide expression

**Item Attributes:**
- `name` - Unique item identifier
- `title` - Item label
- `action` - Action to execute
- `showIf` - Conditional display
- `hideIf` - Conditional hide
- `readonlyIf` - Conditional disable
- `prompt` - Confirmation message

#### Nested Menubar

```xml
<menubar>
  <menu name="menuActions" title="Actions">
    <item name="itemConfirm" title="Confirm" action="action-confirm"/>

    <!-- Submenu -->
    <menu name="menuAdvanced" title="Advanced">
      <item name="itemMerge" title="Merge Orders"
            action="action-merge"/>
      <item name="itemSplit" title="Split Lines"
            action="action-split"/>
    </menu>

    <divider/>

    <item name="itemCancel" title="Cancel" action="action-cancel"/>
  </menu>

  <menu name="menuReports" title="Reports">
    <item name="itemPrint" title="Print" action="action-print"/>
    <item name="itemExport" title="Export" action="action-export"/>
  </menu>
</menubar>
```

#### Menubar with Conditional Items

```xml
<menubar>
  <menu name="menuActions" title="Actions">
    <!-- Show only in draft status -->
    <item name="itemEdit" title="Edit"
          action="action-edit"
          showIf="statusSelect == 1"/>

    <!-- Show only in confirmed status -->
    <item name="itemComplete" title="Complete"
          action="action-complete"
          showIf="statusSelect == 2"/>

    <!-- Show for admins only -->
    <item name="itemOverride" title="Override"
          action="action-override"
          showIf="$user.isAdmin"/>

    <!-- Confirmation prompt -->
    <item name="itemDelete" title="Delete"
          action="action-delete"
          prompt="Are you sure you want to delete this record?"/>
  </menu>
</menubar>
```

### Toolbar in Forms

Toolbar provides quick-access action buttons displayed prominently at the top of forms.

#### Basic Toolbar

```xml
<form name="sale-order-form" title="Sale Order"
      model="com.axelor.apps.sale.db.SaleOrder">

  <toolbar>
    <button name="btnConfirm" title="Confirm Order"
            onClick="action-order-confirm"
            showIf="statusSelect == 1"
            icon="fa-check" css="btn-success"/>

    <button name="btnComplete" title="Complete"
            onClick="action-order-complete"
            showIf="statusSelect == 2"
            icon="fa-check-circle" css="btn-primary"/>

    <button name="btnCancel" title="Cancel"
            onClick="action-order-cancel"
            showIf="statusSelect in (1, 2)"
            prompt="Are you sure you want to cancel?"
            icon="fa-times" css="btn-danger"/>

    <button name="btnPrint" title="Print"
            onClick="action-order-print"
            showIf="statusSelect >= 2"
            icon="fa-print"/>
  </toolbar>

  <!-- Form content -->
</form>
```

#### Toolbar Button Styles

```xml
<toolbar>
  <!-- Primary action (blue) -->
  <button name="btnSave" title="Save"
          onClick="action-save"
          css="btn-primary"/>

  <!-- Success action (green) -->
  <button name="btnConfirm" title="Confirm"
          onClick="action-confirm"
          css="btn-success"/>

  <!-- Danger action (red) -->
  <button name="btnDelete" title="Delete"
          onClick="action-delete"
          css="btn-danger"/>

  <!-- Warning action (yellow) -->
  <button name="btnAlert" title="Alert"
          onClick="action-alert"
          css="btn-warning"/>

  <!-- Info action (light blue) -->
  <button name="btnInfo" title="Information"
          onClick="action-info"
          css="btn-info"/>

  <!-- Default action (grey) -->
  <button name="btnCancel" title="Cancel"
          onClick="action-cancel"
          css="btn-default"/>
</toolbar>
```

### Menubar in Grids

Grid-level menus for batch operations and filtering.

```xml
<grid name="sale-order-grid" title="Sale Orders"
      model="com.axelor.apps.sale.db.SaleOrder">

  <menubar>
    <menu name="menuBatch" title="Batch Actions">
      <item name="itemBatchConfirm" title="Confirm Selected"
            action="action-batch-confirm"/>
      <item name="itemBatchCancel" title="Cancel Selected"
            action="action-batch-cancel"/>
      <item name="itemBatchExport" title="Export Selected"
            action="action-batch-export"/>
    </menu>

    <menu name="menuFilters" title="Filters">
      <item name="itemFilterDraft" title="Show Draft Only"
            action="action-filter-draft"/>
      <item name="itemFilterConfirmed" title="Show Confirmed Only"
            action="action-filter-confirmed"/>
    </menu>
  </menubar>

  <field name="orderNumber"/>
  <field name="customer"/>
  <field name="statusSelect"/>
</grid>
```

### Toolbar in Grids

Quick-access buttons for common grid operations.

```xml
<grid name="product-grid" title="Products"
      model="com.axelor.apps.base.db.Product">

  <toolbar>
    <button name="btnImport" title="Import Products"
            onClick="action-product-import"
            icon="fa-upload"/>

    <button name="btnExport" title="Export All"
            onClick="action-product-export"
            icon="fa-download"/>

    <button name="btnRefresh" title="Refresh"
            onClick="action-product-refresh"
            icon="fa-sync"/>
  </toolbar>

  <field name="name"/>
  <field name="code"/>
  <field name="category"/>
</grid>
```

## Selection System

Selections define option lists for dropdown fields.

### Basic Selection

```xml
<selection name="product.type.select">
  <option value="1">Goods</option>
  <option value="2">Service</option>
  <option value="3">Software</option>
</selection>
```

### Using Selections

```xml
<!-- In form field -->
<field name="productType" selection="product.type.select"/>

<!-- In grid field -->
<grid name="product-grid">
  <field name="productType" selection="product.type.select"/>
</grid>

<!-- With widget -->
<field name="statusSelect" selection="order.status.select"
       widget="nav-select"/>

<field name="tags" selection="tag.select"
       widget="multi-select"/>
```

### Common Selection Patterns

**Status Selection:**

```xml
<selection name="sale.order.status.select">
  <option value="1">Draft</option>
  <option value="2">Confirmed</option>
  <option value="3">Completed</option>
  <option value="4">Cancelled</option>
</selection>
```

**Priority Selection:**

```xml
<selection name="task.priority.select">
  <option value="1">Low</option>
  <option value="2">Normal</option>
  <option value="3">High</option>
  <option value="4">Urgent</option>
</selection>
```

**Type Selection:**

```xml
<selection name="product.type.select">
  <option value="1">Goods</option>
  <option value="2">Service</option>
  <option value="3">Software</option>
</selection>
```

**Boolean Selection:**

```xml
<selection name="yes.no.select">
  <option value="true">Yes</option>
  <option value="false">No</option>
</selection>
```

### Selection with i18n

Selections support internationalization with translation keys.

```xml
<selection name="order.status.select">
  <option value="1">Draft</option>          <!-- Translated as: sale.order.status.draft -->
  <option value="2">Confirmed</option>       <!-- Translated as: sale.order.status.confirmed -->
  <option value="3">Completed</option>       <!-- Translated as: sale.order.status.completed -->
</selection>
```

## Naming Conventions

### Application Menu Naming

```
menu-{module}-root              → menu-sales-root
menu-{entity}                   → menu-products
menu-{entity}-{filter}          → menu-orders-draft
menu-{module}-{entity}          → menu-crm-customers
```

### Form Menubar Naming

```
menuActions                     → Standard actions menu
menuReports                     → Reports menu
menuTools                       → Tools menu
menu{Purpose}                   → menuAdvanced
```

### Menu Item Naming

```
item{Action}                    → itemConfirm, itemCancel
item{Action}{Entity}            → itemPrintOrder
```

### Toolbar Button Naming

```
btn{Action}                     → btnConfirm, btnCancel, btnPrint
btn{Action}{Entity}             → btnCreateInvoice
```

### Selection Naming

```
{entity}.{field}.select         → product.type.select
{module}.{entity}.{field}.select → sale.order.status.select
{concept}.select                → priority.select, yes.no.select
```

## Menu Ordering Strategy

Menu order determines display position (lower numbers appear first).

### Standard Order Ranges

```xml
<!-- Primary modules -->
<menuitem name="menu-dashboard" order="0"/>
<menuitem name="menu-sales" order="10"/>
<menuitem name="menu-crm" order="20"/>
<menuitem name="menu-purchases" order="30"/>
<menuitem name="menu-inventory" order="40"/>
<menuitem name="menu-accounting" order="50"/>

<!-- Secondary modules -->
<menuitem name="menu-hr" order="60"/>
<menuitem name="menu-projects" order="70"/>

<!-- Configuration -->
<menuitem name="menu-configuration" order="90"/>
<menuitem name="menu-admin" order="100"/>
```

### Submenu Ordering

```xml
<menuitem name="menu-sales-root" order="10"/>

<!-- Primary actions (10-19) -->
<menuitem name="menu-sale-orders" order="10"/>
<menuitem name="menu-quotations" order="11"/>
<menuitem name="menu-invoices" order="12"/>

<!-- Secondary actions (20-29) -->
<menuitem name="menu-customers" order="20"/>
<menuitem name="menu-products" order="21"/>

<!-- Reports (80-89) -->
<menuitem name="menu-sales-reports" order="80"/>

<!-- Configuration (90-99) -->
<menuitem name="menu-sales-config" order="90"/>
```

## Best Practices

### Menu Organization

1. **Use hierarchical structure** - Root menus with logical submenus
2. **Follow order conventions** - Consistent ordering across modules
3. **Add icons to root menus** - Visual identification
4. **Group related actions** - Logical menu groupings
5. **Use meaningful names** - Clear, descriptive titles

### Menubar Usage

1. **Use menubar for secondary actions** - Not primary workflow
2. **Group related items** - Logical menu organization
3. **Add dividers** - Separate action groups
4. **Use conditional display** - Show only relevant items
5. **Provide confirmation prompts** - For destructive actions

### Toolbar Usage

1. **Use toolbar for primary actions** - Workflow buttons
2. **Limit button count** - 3-5 buttons maximum
3. **Use color coding** - Green for positive, red for negative
4. **Add icons** - Visual recognition
5. **Use conditional display** - Show only valid actions

### Selection Best Practices

1. **Use numeric values** - Easier for sorting and comparison
2. **Follow naming convention** - `{entity}.{field}.select`
3. **Keep options concise** - Short, clear labels
4. **Order logically** - By workflow or priority
5. **Support i18n** - Use translation keys

## Icon Reference

### Common FontAwesome Icons

**Actions:**
- `fa-check` - Confirm, approve, validate
- `fa-times` - Cancel, close, reject
- `fa-save` - Save
- `fa-edit` - Edit
- `fa-trash` - Delete
- `fa-copy` - Duplicate, copy

**Documents:**
- `fa-file` - Generic document
- `fa-file-pdf` - PDF document
- `fa-print` - Print
- `fa-download` - Download, export
- `fa-upload` - Upload, import

**Navigation:**
- `fa-arrow-left` - Back, previous
- `fa-arrow-right` - Forward, next
- `fa-home` - Home, dashboard
- `fa-cog` - Settings, configuration
- `fa-search` - Search, find

**Business Objects:**
- `fa-cube` - Product
- `fa-users` - Customers, contacts
- `fa-shopping-cart` - Orders
- `fa-file-invoice` - Invoices
- `fa-warehouse` - Inventory

**Status:**
- `fa-check-circle` - Success, completed
- `fa-exclamation-triangle` - Warning
- `fa-times-circle` - Error, cancelled
- `fa-info-circle` - Information
- `fa-clock` - Pending, waiting

## Examples

### Complete Menu Structure

```xml
<!-- Root menu -->
<menuitem name="menu-sales-root" title="Sales"
          icon="fa-shopping-cart" order="10"/>

<!-- Main entities -->
<menuitem name="menu-sale-orders" title="Sale Orders"
          parent="menu-sales-root"
          action="action.view.sale.orders"
          icon="fa-file-invoice"
          order="10"/>

<menuitem name="menu-quotations" title="Quotations"
          parent="menu-sales-root"
          action="action.view.quotations"
          order="11"/>

<!-- Filtered views -->
<menuitem name="menu-orders-draft" title="Draft Orders"
          parent="menu-sales-root"
          action="action.view.orders.draft"
          order="12"/>

<menuitem name="menu-orders-confirmed" title="Confirmed Orders"
          parent="menu-sales-root"
          action="action.view.orders.confirmed"
          order="13"/>

<!-- Supporting entities -->
<menuitem name="menu-customers" title="Customers"
          parent="menu-sales-root"
          action="action.view.customers"
          order="20"/>

<!-- Reports -->
<menuitem name="menu-sales-reports" title="Sales Reports"
          parent="menu-sales-root"
          action="action.view.sales.dashboard"
          order="80"/>

<!-- Configuration -->
<menuitem name="menu-sales-config" title="Sales Configuration"
          parent="menu-sales-root"
          action="action.view.sales.config"
          groups="admins"
          order="90"/>
```

### Complete Form with Menubar and Toolbar

```xml
<form name="sale-order-form" title="Sale Order"
      model="com.axelor.apps.sale.db.SaleOrder"
      width="large">

  <!-- Menubar for secondary actions -->
  <menubar>
    <menu name="menuActions" title="Actions" icon="fa-cog">
      <item name="itemDuplicate" title="Duplicate Order"
            action="action-order-duplicate"/>
      <item name="itemMerge" title="Merge with Another"
            action="action-order-merge"
            showIf="statusSelect == 1"/>
      <divider/>
      <item name="itemArchive" title="Archive"
            action="action-order-archive"
            showIf="statusSelect == 4"/>
    </menu>

    <menu name="menuReports" title="Reports" icon="fa-file-pdf">
      <item name="itemPrintOrder" title="Print Order"
            action="action-order-print"
            showIf="statusSelect >= 2"/>
      <item name="itemExportPDF" title="Export to PDF"
            action="action-order-export-pdf"/>
      <item name="itemSendEmail" title="Send by Email"
            action="action-order-send-email"
            showIf="customer.email != null"/>
    </menu>

    <menu name="menuGenerate" title="Generate" icon="fa-plus">
      <item name="itemGenerateInvoice" title="Generate Invoice"
            action="action-order-generate-invoice"
            showIf="statusSelect == 2"/>
      <item name="itemGenerateDelivery" title="Generate Delivery"
            action="action-order-generate-delivery"
            showIf="statusSelect == 2"/>
    </menu>
  </menubar>

  <!-- Toolbar for primary workflow actions -->
  <toolbar>
    <button name="btnConfirm" title="Confirm Order"
            onClick="action-group-order-confirm"
            showIf="statusSelect == 1"
            prompt="Confirm this order?"
            icon="fa-check" css="btn-success"/>

    <button name="btnComplete" title="Complete"
            onClick="action-order-complete"
            showIf="statusSelect == 2"
            icon="fa-check-circle" css="btn-primary"/>

    <button name="btnCancel" title="Cancel"
            onClick="action-order-cancel"
            showIf="statusSelect in (1, 2)"
            prompt="Are you sure you want to cancel?"
            icon="fa-times" css="btn-danger"/>

    <button name="btnPrint" title="Print"
            onClick="action-order-print"
            showIf="statusSelect >= 2"
            icon="fa-print"/>
  </toolbar>

  <!-- Form panels -->
  <panel name="mainPanel">
    <!-- Form content -->
  </panel>

</form>
```

## Related Documentation

- **View Structure**: @docs/views/view-reference.md
- **Actions**: @docs/views/action-patterns.md
- **XSD Schema**: @skills/axelor-xml-validator/reference/object-views-reference.md
