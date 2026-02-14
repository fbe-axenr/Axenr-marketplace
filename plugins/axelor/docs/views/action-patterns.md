# Action Patterns and Workflows

Complete guide to Axelor actions including all action types, workflows, conditional logic, and advanced components.

## Action Types Overview

Actions define behavior and business logic triggered by user interactions. Six main action types exist:

1. **action-view** - Opens a view with filters and context
2. **action-method** - Calls Java method
3. **action-record** - Sets field values
4. **action-attrs** - Changes field attributes dynamically
5. **action-group** - Executes multiple actions
6. **action-validate** - Validates data and shows messages

## 1. Action-View

Opens views (grid, form, calendar, etc.) with optional filters and context.

### Basic Syntax

```xml
<action-view name="action.view.products"
             title="Products"
             model="com.axelor.apps.base.db.Product">
  <view type="grid" name="product-grid"/>
  <view type="form" name="product-form"/>
</action-view>
```

### Complete Action-View

```xml
<action-view name="action.view.customer.orders"
             title="Customer Orders"
             model="com.axelor.apps.sale.db.SaleOrder">

  <!-- Views to display -->
  <view type="grid" name="sale-order-grid"/>
  <view type="form" name="sale-order-form"/>

  <!-- Domain filter -->
  <domain>self.customer.id = :customerId AND self.statusSelect in (2, 3)</domain>

  <!-- Context variables -->
  <context name="customerId" expr="eval: id"/>
  <context name="_showRecord" expr="eval: activeOrder?.id"/>
  <context name="_domain" expr="self.orderDate >= :startDate"/>
  <context name="startDate" expr="eval: $moment().startOf('year')"/>

</action-view>
```

### Domain Filters

```xml
<!-- Simple domain -->
<domain>self.active = true</domain>

<!-- Multiple conditions -->
<domain>self.active = true AND self.sellable = true AND self.category.id = :categoryId</domain>

<!-- Complex domain with OR -->
<domain>
  (self.customer.id = :customerId OR self.contactPartner.id = :contactId)
  AND self.statusSelect != 5
</domain>

<!-- Date comparisons -->
<domain>self.dueDate < :today AND self.paid = false</domain>

<!-- IN conditions -->
<domain>self.statusSelect IN (2, 3, 4)</domain>

<!-- NULL checks -->
<domain>self.parentCategory IS NULL</domain>
<domain>self.email IS NOT NULL</domain>
```

### Context Variables

```xml
<action-view name="action.view.related.products">
  <!-- Pass current record ID -->
  <context name="categoryId" expr="eval: category?.id"/>

  <!-- Pass multiple values -->
  <context name="startDate" expr="eval: $moment().startOf('month')"/>
  <context name="endDate" expr="eval: $moment().endOf('month')"/>

  <!-- Pass entire record -->
  <context name="_parent" expr="eval: __this__"/>

  <!-- Set default values for new records -->
  <context name="_customer" expr="eval: customer"/>
  <context name="_orderDate" expr="eval: $moment()"/>

  <!-- Show specific record -->
  <context name="_showRecord" expr="eval: id"/>

  <!-- Domain context -->
  <context name="_domain" expr="self.category = :category"/>
  <context name="category" expr="eval: category"/>
</action-view>
```

### View Params

```xml
<action-view name="action.view.orders">
  <!-- Popup mode -->
  <view-param name="popup" value="true"/>
  <view-param name="popup.maximized" value="true"/>
  <view-param name="show-toolbar" value="false"/>
  <view-param name="show-confirm" value="true"/>

  <!-- Grid params -->
  <view-param name="limit" value="50"/>
  <view-param name="search-limit" value="10"/>

  <!-- Form width -->
  <view-param name="width" value="large"/>
</action-view>
```

## 2. Action-Method

Calls a Java method in a controller or service class.

### Basic Syntax

```xml
<action-method name="action-product-compute-margin">
  <call class="com.axelor.apps.base.web.ProductController"
        method="computeMargin"/>
</action-method>
```

### Java Method Signature

```java
public class SaleOrderController {

  public void confirm(ActionRequest request, ActionResponse response) {
    SaleOrder order = request.getContext().asType(SaleOrder.class);

    // Business logic
    orderService.confirm(order);

    // Set response
    response.setReload(true);
    response.setFlash("Order confirmed successfully");
  }
}
```

### Response Methods

```java
// Reload current view
response.setReload(true);

// Show notifications
response.setFlash("Success message");  // Toast message (auto-disappears)
response.setNotify("Info message");    // Notification (auto-disappears)
response.setError("Error message");    // Error dialog (blocks, user must click OK)
response.setAlert("Warning message");  // Warning dialog (NON-BLOCKING - see note below)

// Set field values
response.setValue("fieldName", value);
response.setValues(mapOfValues);

// Set field attributes
response.setAttr("fieldName", "readonly", true);
response.setAttrs(mapOfAttrs);

// Navigate to another view
response.setView(actionViewBuilder.map());

// Close current popup
response.setCanClose(true);

// Set signal (for parent view)
response.setSignal("refresh", data);
```

> **IMPORTANT - response.setAlert() is NOT blocking:**
> `response.setAlert()` displays a dialog but does NOT wait for the user's response.
> The controller method returns immediately after calling setAlert().
>
> For confirmation dialogs that require user response, use `action-validate` with `<alert>` instead.
> See: https://docs.axelor.com/adk/{aopVmajor.aopVminor}/dev-guide/actions/action-validate.html

**For user confirmation, use action-validate:**
```xml
<action-validate name="action-confirm-delete">
  <alert message="Are you sure you want to delete this record?"/>
</action-validate>

<action-group name="action-group-delete">
  <action name="action-confirm-delete"/>
  <action name="action-method-delete"/>  <!-- Only runs if user clicks OK -->
</action-group>
```

### Common Method Patterns

**Compute Values:**

```xml
<action-method name="action-order-compute-total">
  <call class="com.axelor.apps.sale.web.SaleOrderController"
        method="computeTotal"/>
</action-method>
```

**Validation:**

```xml
<action-method name="action-order-validate">
  <call class="com.axelor.apps.sale.web.SaleOrderController"
        method="validate"/>
</action-method>
```

**Workflow Transition:**

```xml
<action-method name="action-order-confirm">
  <call class="com.axelor.apps.sale.web.SaleOrderController"
        method="confirm"/>
</action-method>
```

## 3. Action-Record

Sets field values directly without Java code using expressions.

### Basic Syntax

```xml
<action-record name="action-product-default-values"
               model="com.axelor.apps.base.db.Product">
  <field name="active" expr="eval: true"/>
  <field name="createdOn" expr="eval: $moment()"/>
</action-record>
```

### Expression Types

```xml
<!-- Direct value -->
<field name="active" expr="eval: true"/>
<field name="quantity" expr="eval: 1"/>
<field name="name" expr="eval: 'Default Name'"/>

<!-- Current date/time -->
<field name="createdOn" expr="eval: $moment()"/>
<field name="orderDate" expr="eval: $moment().toLocalDate()"/>

<!-- From related field -->
<field name="currency" expr="eval: customer?.currency"/>

<!-- Conditional expression -->
<field name="discount" expr="eval: totalAmount > 1000 ? 10 : 0"/>

<!-- Calculation -->
<field name="total" expr="eval: quantity * unitPrice"/>

<!-- Call static method -->
<field name="code" expr="call: com.axelor.apps.base.service.ProductService.generateCode()"/>

<!-- Current user -->
<field name="assignedTo" expr="eval: $user"/>

<!-- Select from database -->
<field name="defaultCategory"
       expr="select: com.axelor.apps.base.db.Category
              where code = 'DEFAULT'"/>
```

### Conditional Fields

```xml
<action-record name="action-order-type-change"
               model="com.axelor.apps.sale.db.SaleOrder">

  <!-- Only set if condition is true -->
  <field name="deliveryMode" expr="eval: 'express'"
         if="orderType == 'urgent'"/>

  <field name="priority" expr="eval: 1"
         if="customer?.vip == true"/>

  <!-- Multiple conditions -->
  <field name="discount" expr="eval: 15"
         if="totalAmount > 1000 && customer?.category == 'gold'"/>

</action-record>
```

### Common Patterns

**Default Values on New:**

```xml
<action-record name="action-sale-order-default"
               model="com.axelor.apps.sale.db.SaleOrder">
  <field name="orderDate" expr="eval: $moment().toLocalDate()"/>
  <field name="statusSelect" expr="eval: 1"/>
  <field name="currency" expr="eval: $user.activeCompany?.currency"/>
  <field name="salesperson" expr="eval: $user"/>
  <field name="active" expr="eval: true"/>
</action-record>
```

**Copy Values from Related:**

```xml
<action-record name="action-order-customer-change"
               model="com.axelor.apps.sale.db.SaleOrder">
  <field name="currency" expr="eval: customer?.currency"/>
  <field name="priceList" expr="eval: customer?.priceList"/>
  <field name="paymentMode" expr="eval: customer?.paymentMode"/>
  <field name="invoicingAddress" expr="eval: customer?.mainAddress"/>
  <field name="deliveryAddress"
         expr="eval: customer?.deliveryAddress ?: customer?.mainAddress"/>
</action-record>
```

**Computed Values:**

```xml
<action-record name="action-order-line-compute"
               model="com.axelor.apps.sale.db.SaleOrderLine">
  <field name="totalWithoutTax"
         expr="eval: (quantity * unitPrice) * (1 - discount / 100)"/>
  <field name="totalWithTax"
         expr="eval: totalWithoutTax * (1 + taxRate / 100)"/>
</action-record>
```

## 4. Action-Attrs

Dynamically changes field attributes (hidden, readonly, required, domain, value, title).

### Basic Syntax

```xml
<action-attrs name="action-order-attrs">
  <attribute name="readonly" for="unitPrice" expr="eval: locked"/>
  <attribute name="hidden" for="discount" expr="eval: !customer?.allowDiscount"/>
</action-attrs>
```

### Attribute Types

| Attribute | Description | Value Type |
|-----------|-------------|------------|
| hidden | Hide/show field | Boolean expression |
| readonly | Make field read-only | Boolean expression |
| required | Make field required | Boolean expression |
| domain | Filter options for relational fields | Domain string |
| value | Set field value | Any value |
| title | Change field label | String |
| css | Add CSS classes | String |
| collapse | Collapse/expand panel | Boolean expression |
| help | Set help text | String |
| scale | Set decimal scale | Integer |
| precision | Set decimal precision | Integer |

### Common Patterns

**Conditional Readonly:**

```xml
<action-attrs name="action-order-readonly-attrs">
  <!-- Make entire form readonly if confirmed -->
  <attribute name="readonly" for="mainPanel"
             expr="eval: statusSelect >= 2"/>

  <!-- Specific fields readonly -->
  <attribute name="readonly" for="customer"
             expr="eval: orderLines?.size() > 0"/>

  <attribute name="readonly" for="priceList"
             expr="eval: statusSelect != 1"/>
</action-attrs>
```

**Conditional Required:**

```xml
<action-attrs name="action-order-required-attrs">
  <!-- Required based on status -->
  <attribute name="required" for="confirmDate"
             expr="eval: statusSelect >= 2"/>

  <!-- Required based on type -->
  <attribute name="required" for="deliveryAddress"
             expr="eval: orderType == 'delivery'"/>

  <!-- Required based on field value -->
  <attribute name="required" for="cancelReason"
             expr="eval: statusSelect == 5"/>
</action-attrs>
```

**Dynamic Domain:**

```xml
<action-attrs name="action-order-line-domain-attrs">
  <!-- Filter products by category -->
  <attribute name="domain" for="product"
             expr="eval: &quot;self.category.id = ${category?.id} AND self.active = true&quot;"
             if="category != null"/>

  <!-- Filter contacts by customer -->
  <attribute name="domain" for="contactPartner"
             expr="eval: &quot;self.mainPartner.id = ${customer?.id}&quot;"
             if="customer != null"/>
</action-attrs>
```

**Conditional Visibility:**

```xml
<action-attrs name="action-order-visibility-attrs">
  <!-- Show discount only for certain customers -->
  <attribute name="hidden" for="discount"
             expr="eval: !customer?.allowDiscount"/>

  <!-- Show admin fields -->
  <attribute name="hidden" for="adminPanel"
             expr="eval: !$user.isAdmin"/>

  <!-- Show based on status -->
  <attribute name="hidden" for="confirmButton"
             expr="eval: statusSelect != 1"/>

  <attribute name="hidden" for="cancelReason"
             expr="eval: statusSelect != 5"/>
</action-attrs>
```

## 5. Action-Group

Executes multiple actions in sequence.

### Basic Syntax

```xml
<action-group name="action-group-order-confirm">
  <action name="action-order-validate"/>
  <action name="action-order-method-confirm"/>
  <action name="action-order-attrs-readonly"/>
</action-group>
```

### Conditional Actions

```xml
<action-group name="action-group-order-customer-change">
  <action name="action-order-record-customer-data"/>
  <action name="action-order-attrs-customer" if="customer != null"/>
  <action name="action-order-clear-customer-data" if="customer == null"/>
  <action name="action-order-method-compute-taxes"/>
</action-group>
```

### Common Patterns

**Form onNew:**

```xml
<action-group name="action-group-sale-order-onnew">
  <action name="action-sale-order-record-defaults"/>
  <action name="action-sale-order-attrs-new"/>
  <action name="action-sale-order-method-init"/>
</action-group>
```

**Form onSave:**

```xml
<action-group name="action-group-sale-order-validate">
  <action name="action-sale-order-validate-dates"/>
  <action name="action-sale-order-validate-lines"/>
  <action name="action-sale-order-validate-totals"/>
  <action name="action-sale-order-method-compute-final"/>
</action-group>
```

**Field onChange:**

```xml
<action-group name="action-group-order-line-product-change">
  <action name="action-order-line-record-product-data"/>
  <action name="action-order-line-attrs-product"/>
  <action name="action-order-line-method-compute-price"/>
  <action name="action-order-line-method-compute-total"/>
  <action name="save"/>
</action-group>
```

**Button Click:**

```xml
<action-group name="action-group-order-confirm">
  <action name="action-order-validate-confirm"/>
  <action name="action-order-method-confirm" if-module="axelor-sale"/>
  <action name="action-order-attrs-confirmed"/>
  <action name="save"/>
  <action name="action-order-method-send-notification"/>
</action-group>
```

## 6. Action-Validate

Validates data and shows messages.

### Message Types

```xml
<action-validate name="action-order-validate">
  <!-- Error (blocks save) -->
  <error message="Order lines are required"
         if="orderLines == null || orderLines.empty"/>

  <!-- Alert (shows warning but allows save) -->
  <alert message="Total amount is very high"
         if="totalAmount > 100000"/>

  <!-- Info (shows information) -->
  <info message="Discount applied based on customer category"
        if="discount > 0"/>

  <!-- Notify (toast notification) -->
  <notify message="Customer address updated"
          if="customer?.addressChanged"/>
</action-validate>
```

### Common Patterns

**Required Field Validation:**

```xml
<action-validate name="action-order-validate-required">
  <error message="Customer is required" if="customer == null"/>
  <error message="Order date is required" if="orderDate == null"/>
  <error message="At least one order line is required"
         if="orderLines == null || orderLines.empty"/>
</action-validate>
```

**Business Rule Validation:**

```xml
<action-validate name="action-order-validate-rules">
  <error message="Order date cannot be in the future"
         if="orderDate != null &amp;&amp; orderDate &gt; $moment().toLocalDate()"/>

  <error message="Expected date must be after order date"
         if="expectedDate != null &amp;&amp; expectedDate &lt; orderDate"/>

  <alert message="Customer has overdue invoices"
         if="customer?.hasOverdueInvoices == true"/>

  <alert message="Product stock is low"
         if="product?.stock &lt; 10"/>
</action-validate>
```

## Advanced Components

### Panel-Related

Displays related records (one-to-many, many-to-many) with inline grid or master-detail view.

```xml
<panel-related name="orderLinesPanel"
               field="orderLines"
               title="Order Lines"
               form-view="sale-order-line-form"
               grid-view="sale-order-line-grid"
               editable="true"
               orderBy="sequence"
               canNew="true"
               canEdit="true"
               canRemove="true"
               canSelect="true"
               onChange="action-order-compute-total"
               colSpan="12">

  <!-- Optional: Define inline grid columns -->
  <field name="product" onChange="action-order-line-product-change"/>
  <field name="quantity"/>
  <field name="unitPrice"/>
  <field name="total" readonly="true"/>

</panel-related>
```

**Panel-Related Attributes:**

| Attribute | Type | Description |
|-----------|------|-------------|
| field | String | Relational field name (required) |
| form-view | String | Form view to use for editing |
| grid-view | String | Grid view to display in panel |
| editable | Boolean | Enables inline editing |
| orderBy | String | Default ordering |
| canNew | Boolean | Allows creating new records |
| canEdit | Boolean | Allows editing records |
| canRemove | Boolean | Allows removing records |
| canSelect | Boolean | Allows selecting existing records |
| onChange | String | Action on value change |
| colSpan | Integer | Column span |

### Panel-Dashlet

Embeds views (grids, charts) within forms for contextual information display.

```xml
<panel-dashlet name="relatedOrdersDashlet"
               title="Related Orders"
               action="action.view.customer.orders"
               canSearch="true"
               height="350"
               colSpan="12"/>
```

**Panel-Dashlet Attributes:**
- `action` - Action-view to display
- `canSearch` - Enable search in dashlet
- `height` - Dashlet height in pixels
- `colSpan` - Column span

### Panel-Include

Includes another form/view within the current form for reusability.

```xml
<panel-include view="address-embedded-form"/>
```

**Naming Convention:**
```
incl-{section}-panel-form → incl-address-panel-form (reusable panels)
```

### Panel-Mail

Displays email messaging and comments with followers.

```xml
<panel-mail field="emailMessages" limit="4"/>
```

## Conditional Logic

### showIf, hideIf, readonlyIf

Control field and panel visibility/behavior based on expressions.

```xml
<!-- Status-based display -->
<panel name="draftPanel" showIf="statusSelect == 1">
  <field name="editableField"/>
</panel>

<panel name="confirmedPanel" showIf="statusSelect >= 2">
  <field name="confirmDate" readonly="true"/>
  <field name="confirmedBy" readonly="true"/>
</panel>

<!-- User permission-based display -->
<field name="adminOnlyField" showIf="$user.isAdmin"/>

<button name="btnApprove"
        showIf="statusSelect == 2 && $user.group == 'managers'"
        onClick="action-approve"/>

<!-- Type-based display -->
<field name="productType" selection="product.type.select"/>

<panel name="goodsPanel" showIf="productType == '1'" title="Goods Information">
  <field name="weight"/>
  <field name="dimensions"/>
</panel>

<panel name="servicePanel" showIf="productType == '2'" title="Service Information">
  <field name="duration"/>
  <field name="hourlyRate"/>
</panel>
```

### Domain Expressions

Dynamic filtering in action-view domains.

```xml
<action-view name="action.view.filtered.products">
  <!-- Date range filtering -->
  <domain>
    self.createdOn &gt;= :startDate
    AND self.createdOn &lt;= :endDate
  </domain>

  <!-- Complex conditions -->
  <domain>
    (self.statusSelect IN (1, 2) OR self.priority = 'high')
    AND self.assignedTo.id = :userId
    AND self.project.active = true
  </domain>

  <!-- Null handling -->
  <domain>
    self.completedDate IS NULL
    AND self.dueDate &lt; :today
  </domain>
</action-view>
```

### validIf Expressions

Field-level validation expressions.

```xml
<field name="endDate" validIf="endDate >= startDate"/>
<field name="quantity" validIf="quantity > 0"/>
<field name="email" validIf="email.contains('@')"/>
```

## Event Handlers

### onLoad Event Handler

```xml
<form name="sale-order-form" onLoad="action-sale-order-onload">
</form>

<action-method name="action-sale-order-onload">
  <call class="com.axelor.apps.sale.web.SaleOrderController"
        method="onLoad"/>
</action-method>
```

### onSave Event Handler

```xml
<form name="sale-order-form" onSave="action-group-sale-order-validate">
</form>

<action-group name="action-group-sale-order-validate">
  <action name="action-sale-order-validate-dates"/>
  <action name="action-sale-order-validate-lines"/>
  <action name="action-sale-order-method-compute-totals"/>
</action-group>
```

### onChange Event Handler

```xml
<field name="customer" onChange="action-group-customer-change"/>

<action-group name="action-group-customer-change">
  <action name="action-order-record-customer"/>
  <action name="action-order-attrs-customer"/>
  <action name="action-order-method-compute-taxes"/>
</action-group>
```

### onClick Event Handler

```xml
<button name="btnConfirm" title="Confirm"
        onClick="action-group-order-confirm"
        prompt="Are you sure you want to confirm this order?"/>

<action-group name="action-group-order-confirm">
  <action name="action-order-validate-confirm"/>
  <action name="action-order-method-confirm"/>
  <action name="action-order-attrs-confirmed"/>
  <action name="save"/>
</action-group>
```

## Workflow Patterns

### Status Transition Pattern

```xml
<!-- Button triggers workflow -->
<button name="btnConfirm" title="Confirm"
        onClick="action-group-order-confirm"
        showIf="statusSelect == 1"/>

<!-- Action group orchestrates transition -->
<action-group name="action-group-order-confirm">
  <action name="action-order-validate-confirm"/>
  <action name="action-order-method-confirm"/>
  <action name="action-order-attrs-confirmed"/>
  <action name="save"/>
</action-group>

<!-- Validation ensures transition is valid -->
<action-validate name="action-order-validate-confirm">
  <error message="Cannot confirm without customer" if="customer == null"/>
  <error message="Cannot confirm without lines"
         if="orderLines == null || orderLines.empty"/>
</action-validate>

<!-- Method performs business logic -->
<action-method name="action-order-method-confirm">
  <call class="com.axelor.apps.sale.web.SaleOrderController"
        method="confirm"/>
</action-method>

<!-- Attrs updates UI after transition -->
<action-attrs name="action-order-attrs-confirmed">
  <attribute name="readonly" for="mainPanel" expr="eval: true"/>
  <attribute name="hidden" for="btnConfirm" expr="eval: true"/>
</action-attrs>
```

### Action Chaining Pattern

Execute actions in specific order with conditional logic.

```xml
<action-group name="action-group-complex-workflow">
  <!-- 1. Validate first -->
  <action name="action-validate-prerequisites"/>

  <!-- 2. Compute values -->
  <action name="action-record-compute-values"/>

  <!-- 3. Call business method -->
  <action name="action-method-process"/>

  <!-- 4. Update UI conditionally -->
  <action name="action-attrs-success" if="processingSucceeded"/>
  <action name="action-attrs-error" if="!processingSucceeded"/>

  <!-- 5. Save if successful -->
  <action name="save" if="processingSucceeded"/>

  <!-- 6. Send notification -->
  <action name="action-method-notify" if="processingSucceeded"/>
</action-group>
```

## Naming Conventions

### Recommended Pattern

```
action-{type}-{model}-{purpose}
```

### Examples

```xml
<!-- action-view -->
<action-view name="action.view.customer.orders"/>
<action-view name="action.view.overdue.invoices"/>

<!-- action-method -->
<action-method name="action-order-method-confirm"/>
<action-method name="action-invoice-method-compute-total"/>

<!-- action-record -->
<action-record name="action-order-record-defaults"/>
<action-record name="action-order-record-customer-data"/>

<!-- action-attrs -->
<action-attrs name="action-order-attrs-readonly"/>
<action-attrs name="action-order-attrs-domain"/>

<!-- action-group -->
<action-group name="action-group-order-onnew"/>
<action-group name="action-group-order-customer-change"/>

<!-- action-validate -->
<action-validate name="action-order-validate-dates"/>
<action-validate name="action-order-validate-confirm"/>
```

## Best Practices

1. **Use action-group** to sequence multiple actions
2. **Always validate** before executing business logic
3. **Use meaningful names** following conventions
4. **Use conditional actions** with `if` attribute
5. **Separate concerns** - validation, computation, UI updates
6. **Leverage action-record** for simple value assignments
7. **Use action-attrs** for dynamic UI changes
8. **Add confirmation prompts** for destructive actions
9. **Chain related actions** logically
10. **Document complex workflows** in code comments

## Related Documentation

- **View Structure**: @docs/views/view-reference.md
- **Menus and Selections**: @docs/views/menu-selection-reference.md

