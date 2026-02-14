# Controller Patterns in Axelor

## Overview

Controllers in Axelor handle user interactions from the web interface. They receive ActionRequest objects, process business logic (delegating to services), and return ActionResponse objects that update the UI. Controllers should be thin - they orchestrate but don't contain business logic.

## Controller Purpose and Responsibilities

**Important Imports:**
All controller examples in this document use the Bean lookup pattern (`Beans.get()`). Make sure to include this import in your controllers:
```java
import com.axelor.inject.Beans;
```

### Thin Controllers Philosophy

> **IMPORTANT - Controller Instantiation:**
> - Controllers in Axelor are **NOT singletons** - do NOT use `@Singleton` annotation
> - Controllers are **NOT injected** like services
> - Always use `Beans.get()` to access services and repositories (not `@Inject`)

```java
package com.axelor.apps.sale.web;

import com.axelor.apps.sale.db.SaleOrder;
import com.axelor.apps.sale.db.repo.SaleOrderRepository;
import com.axelor.apps.sale.service.SaleOrderService;
import com.axelor.exception.service.TraceBackService;
import com.axelor.inject.Beans;
import com.axelor.rpc.ActionRequest;
import com.axelor.rpc.ActionResponse;

public class SaleOrderController {

    // GOOD: Thin controller - delegates to service
    public void confirmOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            // Delegate business logic to service
            saleOrder = Beans.get(SaleOrderService.class).confirm(saleOrder);

            response.setReload(true);
            response.setFlash("Order confirmed successfully");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // BAD: Fat controller - contains business logic
    public void confirmOrderBad(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            // DON'T DO THIS: Business logic in controller
            if (saleOrder.getCustomer() == null) {
                response.setError("Customer is required");
                return;
            }
            saleOrder.setStatusSelect(SaleOrderRepository.STATUS_ORDER_CONFIRMED);
            saleOrder.setConfirmationDateTime(LocalDateTime.now());
            // ... more business logic

            response.setReload(true);
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Controller Responsibilities

**Controllers SHOULD:**
- Extract data from ActionRequest
- Call service methods
- Handle exceptions and convert to UI feedback
- Set response values (setReload, setFlash, setNotify, etc.)
- Build action-view responses
- Validate user permissions (when needed)

**Controllers SHOULD NOT:**
- Contain business logic
- Perform calculations
- Access repositories directly (use services)
- Contain complex validation logic
- Manage transactions directly

## ActionRequest Handling

### getContext() Method

```java
public class SaleOrderController {

    // Get entire context
    public void processOrder(ActionRequest request, ActionResponse response) {
        Context context = request.getContext();

        // Context contains all form data
        Map<String, Object> contextData = context;
        // Access values from context
        Object value = context.get("fieldName");
    }
}
```

### asType() Method

```java
public class SaleOrderController {

    // Convert context to entity type
    public void confirmOrder(ActionRequest request, ActionResponse response) {
        try {
            // Convert entire context to SaleOrder
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            // IMPORTANT: This creates a new instance from form data
            // Always fetch from DB to get managed entity
            SaleOrder dbOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            // Work with dbOrder (managed entity)
            dbOrder = Beans.get(SaleOrderService.class).confirm(dbOrder);

            response.setReload(true);
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

}
```

### get() Method

```java
public class SaleOrderController {

    // Get individual fields from context
    public void calculateTotal(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();

            // Get simple field
            BigDecimal amount = (BigDecimal) context.get("amount");
            Integer quantity = (Integer) context.get("quantity");
            String description = (String) context.get("description");

            // Get entity reference
            Partner customer = (Partner) context.get("customer");
            if (customer != null && customer.getId() != null) {
                customer = Beans.get(PartnerRepository.class).find(customer.getId());
            }

            // Get nested field
            Context addressContext = (Context) context.get("deliveryAddress");
            if (addressContext != null) {
                String city = (String) addressContext.get("city");
            }

            // Get from parent context
            Context parentContext = context.getParent();
            if (parentContext != null) {
                SaleOrder parentOrder = parentContext.asType(SaleOrder.class);
            }

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

## Context Extraction Patterns

### Extracting Entity from Context

```java
public class SaleOrderController {

    public void confirmOrder(ActionRequest request, ActionResponse response) {
        try {
            // Method 1: asType (most common)
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            // Method 2: get + repository
            Long orderId = (Long) request.getContext().get("id");
            SaleOrder order = Beans.get(SaleOrderRepository.class).find(orderId);

            // Method 3: Direct entity from context (when passed as id reference)
            SaleOrder contextOrder = (SaleOrder) request.getContext().get("saleOrder");
            if (contextOrder != null && contextOrder.getId() != null) {
                order = Beans.get(SaleOrderRepository.class).find(contextOrder.getId());
            }

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Extracting Nested Objects

```java
public class SaleOrderController {

    public void updateCustomerInfo(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();

            // Get main entity
            SaleOrder saleOrder = context.asType(SaleOrder.class);

            // Get nested customer - prefer fetching from DB if ID exists
            Context customerContext = (Context) context.get("customer");
            if (customerContext != null) {
                Long customerId = (Long) customerContext.get("id");
                Partner customer = null;

                if (customerId != null) {
                    // Best: Fetch managed entity from DB
                    customer = Beans.get(PartnerRepository.class).find(customerId);
                } else {
                    // For new/transient entity: use Mapper.toBean
                    customer = Mapper.toBean(Partner.class, customerContext);
                }
            }

            // Get deeply nested object
            if (customerContext != null) {
                Context addressContext = (Context) customerContext.get("mainAddress");
                if (addressContext != null) {
                    Long addressId = (Long) addressContext.get("id");
                    Address address = null;

                    if (addressId != null) {
                        address = Beans.get(AddressRepository.class).find(addressId);
                    } else {
                        address = Mapper.toBean(Address.class, addressContext);
                    }

                    String city = (String) addressContext.get("city");
                    String zipCode = (String) addressContext.get("zip");
                }
            }

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Extracting Lists from Context

```java
public class SaleOrderController {

    public void computeLines(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();
            SaleOrder saleOrder = context.asType(SaleOrder.class);

            // Get list of lines from context
            @SuppressWarnings("unchecked")
            List<Map<String, Object>> linesList =
                (List<Map<String, Object>>) context.get("saleOrderLineList");

            if (linesList != null) {
                List<SaleOrderLine> lines = new ArrayList<>();

                for (Map<String, Object> lineMap : linesList) {
                    Long lineId = (Long) lineMap.get("id");
                    SaleOrderLine line = null;

                    if (lineId != null) {
                        // Fetch from DB if it has an ID
                        line = Beans.get(SaleOrderLineRepository.class).find(lineId);
                    }
                    lines.add(line);
                }

                // Process lines
                for (SaleOrderLine line : lines) {
                    Beans.get(SaleOrderLineService.class).compute(line);
                }
            }

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Extracting Parent Context

```java
public class SaleOrderLineController {

    public void computeLine(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();

            // Get current line
            SaleOrderLine line = context.asType(SaleOrderLine.class);

            // Get parent sale order
            Context parentContext = context.getParent();
            if (parentContext != null) {
                SaleOrder saleOrder = parentContext.asType(SaleOrder.class);

                // Use parent data
                Company company = saleOrder.getCompany();
                Partner customer = saleOrder.getCustomer();

                // Compute line with parent context
                line = Beans.get(SaleOrderLineService.class).compute(line, saleOrder);

                response.setValues(line);
            }

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

## ActionResponse Methods

### setReload()

```java
public class SaleOrderController {

    // Reload entire form
    public void confirmOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderService.class).confirm(saleOrder);

            response.setReload(true);  // Reload entire form with fresh data
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### setFlash()

```java
public class SaleOrderController {

    // Show success message
    public void confirmOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderService.class).confirm(saleOrder);

            response.setReload(true);
            response.setFlash("Order confirmed successfully");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Flash with order number
    public void generateOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = Beans.get(SaleOrderService.class).generateOrder();

            response.setReload(true);
            response.setFlash("Order " + saleOrder.getOrderNumber() + " generated");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### setNotify()

```java
public class SaleOrderController {

    // Info notification
    public void checkStock(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            boolean inStock = Beans.get(SaleOrderService.class).checkStock(saleOrder);

            if (inStock) {
                response.setNotify("All products are in stock");
            } else {
                response.setNotify("Some products are out of stock", "warning");
            }
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Error notification
    public void validateOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            Beans.get(SaleOrderService.class).validate(saleOrder);

            response.setNotify("Validation successful", "success");
        } catch (Exception e) {
            response.setNotify("Validation failed: " + e.getMessage(), "error");
            TraceBackService.trace(response, e);
        }
    }
}
```

### setError()

```java
public class SaleOrderController {

    // Set error message
    public void confirmOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            if (!Beans.get(SaleOrderService.class).canConfirm(saleOrder)) {
                response.setError("Cannot confirm this order");
                return;
            }

            saleOrder = Beans.get(SaleOrderService.class).confirm(saleOrder);
            response.setReload(true);
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Field-specific error
    public void validateCustomer(ActionRequest request, ActionResponse response) {
        try {
            Partner customer = (Partner) request.getContext().get("customer");

            if (customer == null) {
                response.setError("customer", "Customer is required");
                return;
            }

            if (customer.getBlocked()) {
                response.setError("customer", "Customer is blocked");
                return;
            }

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### setValue()

```java
public class SaleOrderController {

    // Set single value
    public void calculateTotal(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            BigDecimal total = Beans.get(SaleOrderService.class).computeTotal(saleOrder);

            response.setValue("exTaxTotal", total);
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Set multiple values
    public void onChangeCustomer(ActionRequest request, ActionResponse response) {
        try {
            Partner customer = (Partner) request.getContext().get("customer");

            if (customer != null) {
                response.setValue("priceList", customer.getSalePriceList());
                response.setValue("paymentMode", customer.getPaymentMode());
                response.setValue("paymentCondition", customer.getPaymentCondition());
                response.setValue("deliveryAddress", customer.getMainAddress());
                response.setValue("currency", customer.getCurrency());
            }
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### setValues()

```java
public class SaleOrderLineController {

    // Set all fields of an entity
    public void computeLine(ActionRequest request, ActionResponse response) {
        try {
            SaleOrderLine line = request.getContext().asType(SaleOrderLine.class);
            Context parentContext = request.getContext().getParent();
            SaleOrder saleOrder = parentContext.asType(SaleOrder.class);

            // Compute line
            line = Beans.get(SaleOrderLineService.class).compute(line, saleOrder);

            // Set all computed fields at once
            response.setValues(line);
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### setAttr()

```java
public class SaleOrderController {

    // Make field readonly
    public void onLoad(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            if (saleOrder.getStatusSelect() >= SaleOrderRepository.STATUS_ORDER_CONFIRMED) {
                response.setAttr("customer", "readonly", true);
                response.setAttr("orderDate", "readonly", true);
                response.setAttr("saleOrderLineList", "readonly", true);
            }
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Hide field
    public void onChangeOrderType(ActionRequest request, ActionResponse response) {
        try {
            String orderType = (String) request.getContext().get("orderType");

            if ("subscription".equals(orderType)) {
                response.setAttr("subscriptionPanel", "hidden", false);
                response.setAttr("deliveryPanel", "hidden", true);
            } else {
                response.setAttr("subscriptionPanel", "hidden", true);
                response.setAttr("deliveryPanel", "hidden", false);
            }
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Make field required
    public void setFieldRequired(ActionRequest request, ActionResponse response) {
        try {
            response.setAttr("deliveryDate", "required", true);
            response.setAttr("deliveryAddress", "required", true);
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Change field title
    public void updateFieldTitle(ActionRequest request, ActionResponse response) {
        try {
            response.setAttr("externalReference", "title", "Customer Reference");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Set domain filter
    public void setCustomerDomain(ActionRequest request, ActionResponse response) {
        try {
            Company company = (Company) request.getContext().get("company");

            if (company != null) {
                String domain = "self.isCustomer = true AND self.company = " + company.getId();
                response.setAttr("customer", "domain", domain);
            }
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### setView()

```java
public class SaleOrderController {

    // Open form view
    public void openInvoice(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            Invoice invoice = saleOrder.getInvoiceList().get(0);

            response.setView(ActionView
                .define("Invoice")
                .model(Invoice.class.getName())
                .add("form", "invoice-form")
                .add("grid", "invoice-grid")
                .param("forceEdit", "true")
                .context("_showRecord", invoice.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Open grid view with domain
    public void showCustomerOrders(ActionRequest request, ActionResponse response) {
        try {
            Partner customer = (Partner) request.getContext().get("customer");

            response.setView(ActionView
                .define("Customer Orders")
                .model(SaleOrder.class.getName())
                .add("grid", "sale-order-grid")
                .add("form", "sale-order-form")
                .domain("self.customer.id = " + customer.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

## Button Action Handlers

### Basic Button Action

```java
public class SaleOrderController {

    // Confirm button
    public void confirmOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            saleOrder = Beans.get(SaleOrderService.class).confirm(saleOrder);

            response.setReload(true);
            response.setFlash("Order confirmed successfully");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Cancel button
    public void cancelOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            saleOrder = Beans.get(SaleOrderService.class).cancel(saleOrder);

            response.setReload(true);
            response.setNotify("Order canceled");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Button with Validation

```java
public class SaleOrderController {

    public void finalizeQuotation(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            // Validate before processing
            if (!Beans.get(SaleOrderService.class).canFinalize(saleOrder)) {
                response.setError("Cannot finalize this quotation");
                return;
            }

            // Check conditions
            if (saleOrder.getSaleOrderLineList() == null ||
                saleOrder.getSaleOrderLineList().isEmpty()) {
                response.setError("Cannot finalize quotation without lines");
                return;
            }

            saleOrder = Beans.get(SaleOrderService.class).finalize(saleOrder);

            response.setReload(true);
            response.setFlash("Quotation finalized");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Button Opening New View

```java
public class SaleOrderController {

    // Generate invoice button
    public void generateInvoice(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            Invoice invoice = Beans.get(SaleOrderService.class).generateInvoice(saleOrder);

            response.setReload(true);
            response.setFlash("Invoice generated");

            // Open the generated invoice
            response.setView(ActionView
                .define("Generated Invoice")
                .model(Invoice.class.getName())
                .add("form", "invoice-form")
                .param("forceEdit", "true")
                .context("_showRecord", invoice.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Show related documents button
    public void showInvoices(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            response.setView(ActionView
                .define("Invoices")
                .model(Invoice.class.getName())
                .add("grid", "invoice-grid")
                .add("form", "invoice-form")
                .domain("self.saleOrder.id = " + saleOrder.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Button with Confirmation Dialog

```java
public class SaleOrderController {

    public void deleteOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            // Check if can delete
            if (!Beans.get(SaleOrderService.class).canDelete(saleOrder)) {
                response.setError("Cannot delete this order");
                return;
            }

            Beans.get(SaleOrderService.class).delete(saleOrder);

            response.setFlash("Order deleted");
            response.setCanClose(true);
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

## onChange Handlers

### Field onChange

```java
public class SaleOrderController {

    // Customer change
    public void onChangeCustomer(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();
            Partner customer = (Partner) context.get("customer");

            if (customer == null) {
                return;
            }

            // Fetch full customer
            customer = Beans.get(PartnerRepository.class).find(customer.getId());

            // Set related fields
            response.setValue("priceList", customer.getSalePriceList());
            response.setValue("paymentMode", customer.getPaymentMode());
            response.setValue("paymentCondition", customer.getPaymentCondition());
            response.setValue("deliveryAddress", customer.getMainAddress());
            response.setValue("currency", customer.getCurrency());

            // Set domain for contacts
            response.setAttr("contactPartner", "domain",
                "self.mainPartner.id = " + customer.getId());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Order date change
    public void onChangeOrderDate(ActionRequest request, ActionResponse response) {
        try {
            LocalDate orderDate = (LocalDate) request.getContext().get("orderDate");

            if (orderDate != null) {
                // Calculate expected delivery date
                LocalDate deliveryDate = orderDate.plusDays(7);
                response.setValue("expectedDeliveryDate", deliveryDate);
            }
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Line onChange (with Parent Context)

```java
public class SaleOrderLineController {

    // Product change on line
    public void onChangeProduct(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();
            Product product = (Product) context.get("product");

            if (product == null) {
                return;
            }

            // Get parent sale order
            Context parentContext = context.getParent();
            SaleOrder saleOrder = parentContext != null ? parentContext.asType(SaleOrder.class) : null;

            // Fetch full product
            product = Beans.get(ProductRepository.class).find(product.getId());

            // Set product-related fields
            response.setValue("productName", product.getName());
            response.setValue("description", product.getDescription());
            response.setValue("unit", product.getUnit());

            // Get price from price list
            if (saleOrder != null && saleOrder.getPriceList() != null) {
                BigDecimal price = Beans.get(SaleOrderLineService.class).getPrice(
                    product, saleOrder.getPriceList());
                response.setValue("price", price);
            } else {
                response.setValue("price", product.getSalePrice());
            }

            // Set tax
            response.setValue("taxLine", product.getSaleTaxLine());

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Quantity change on line
    public void onChangeQuantity(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();
            SaleOrderLine line = context.asType(SaleOrderLine.class);
            Context parentContext = context.getParent();
            SaleOrder saleOrder = parentContext != null ? parentContext.asType(SaleOrder.class) : null;

            // Compute line
            line = Beans.get(SaleOrderLineService.class).compute(line, saleOrder);

            // Set computed values
            response.setValues(line);

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Price change (recalculate totals)
    public void onChangePrice(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();
            SaleOrderLine line = context.asType(SaleOrderLine.class);
            Context parentContext = context.getParent();
            SaleOrder saleOrder = parentContext != null ? parentContext.asType(SaleOrder.class) : null;

            // Compute totals
            line = Beans.get(SaleOrderLineService.class).computeTotals(line, saleOrder);

            response.setValue("exTaxTotal", line.getExTaxTotal());
            response.setValue("inTaxTotal", line.getInTaxTotal());

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Multiple Field Dependencies

```java
public class SaleOrderController {

    // Company change affects multiple fields
    public void onChangeCompany(ActionRequest request, ActionResponse response) {
        try {
            Company company = (Company) request.getContext().get("company");

            if (company == null) {
                return;
            }

            company = Beans.get(CompanyRepository.class).find(company.getId());

            // Set company-related defaults
            response.setValue("currency", company.getCurrency());
            response.setValue("priceList", company.getDefaultSalePriceList());
            response.setValue("stockLocation", company.getDefaultStockLocation());

            // Update customer domain
            response.setAttr("customer", "domain",
                "self.isCustomer = true AND :company MEMBER OF self.companySet");

            // Update product domain
            response.setAttr("saleOrderLineList.product", "domain",
                "self.sellable = true");

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

## Form Load Handlers

### onNew Handler

```java
public class SaleOrderController {

    // Set defaults when creating new record
    public void onNew(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();

            // Get user's active company
            Company company = Beans.get(UserService.class).getActiveCompany();

            if (company != null) {
                response.setValue("company", company);
                response.setValue("currency", company.getCurrency());
                response.setValue("priceList", company.getDefaultSalePriceList());
            }

            // Set default dates
            LocalDate today = Beans.get(AppBaseService.class).getTodayDate(company);
            response.setValue("orderDate", today);
            response.setValue("creationDate", today);

            // Set default status
            response.setValue("statusSelect", SaleOrderRepository.STATUS_DRAFT_QUOTATION);

            // Set domain restrictions
            response.setAttr("customer", "domain", "self.isCustomer = true");

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### onLoad Handler

```java
public class SaleOrderController {

    // Set UI state when loading existing record
    public void onLoad(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            if (saleOrder.getId() == null) {
                return;
            }

            // Make fields readonly based on status
            if (saleOrder.getStatusSelect() >= SaleOrderRepository.STATUS_ORDER_CONFIRMED) {
                response.setAttr("customer", "readonly", true);
                response.setAttr("company", "readonly", true);
                response.setAttr("orderDate", "readonly", true);
                response.setAttr("saleOrderLineList", "readonly", true);
            }

            // Show/hide panels based on status
            if (saleOrder.getStatusSelect() == SaleOrderRepository.STATUS_ORDER_CONFIRMED) {
                response.setAttr("invoicePanel", "hidden", false);
                response.setAttr("deliveryPanel", "hidden", false);
            }

            // Set button visibility
            response.setAttr("confirmBtn", "hidden",
                saleOrder.getStatusSelect() >= SaleOrderRepository.STATUS_ORDER_CONFIRMED);
            response.setAttr("cancelBtn", "hidden",
                saleOrder.getStatusSelect() == SaleOrderRepository.STATUS_CANCELED);

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

## Action-View Generation

### Basic Action-View

```java
public class SaleOrderController {

    public void showCustomerOrders(ActionRequest request, ActionResponse response) {
        try {
            Partner customer = (Partner) request.getContext().get("customer");

            response.setView(ActionView
                .define("Customer Orders")
                .model(SaleOrder.class.getName())
                .add("grid", "sale-order-grid")
                .add("form", "sale-order-form")
                .domain("self.customer.id = " + customer.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Action-View with Context

```java
public class SaleOrderController {

    public void createInvoiceView(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            response.setView(ActionView
                .define("New Invoice")
                .model(Invoice.class.getName())
                .add("form", "invoice-form")
                .context("_saleOrder", saleOrder.getId())
                .context("customer", saleOrder.getCustomer())
                .context("company", saleOrder.getCompany())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Action-View with Custom Parameters

```java
public class SaleOrderController {

    public void openRelatedInvoices(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            response.setView(ActionView
                .define("Related Invoices")
                .model(Invoice.class.getName())
                .add("grid", "invoice-grid")
                .add("form", "invoice-form")
                .param("search-filters", "invoice-filters")
                .param("forceEdit", "false")
                .domain("self.saleOrder.id = :saleOrderId")
                .context("saleOrderId", saleOrder.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Action-View Opening Specific Record

```java
public class SaleOrderController {

    public void openInvoice(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            if (saleOrder.getInvoiceList() == null || saleOrder.getInvoiceList().isEmpty()) {
                response.setError("No invoice found for this order");
                return;
            }

            Invoice invoice = saleOrder.getInvoiceList().get(0);

            response.setView(ActionView
                .define("Invoice")
                .model(Invoice.class.getName())
                .add("form", "invoice-form")
                .add("grid", "invoice-grid")
                .param("forceEdit", "true")
                .context("_showRecord", invoice.getId())
                .map());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

## Domain Filter Creation

### Simple Domain Filters

```java
public class SaleOrderController {

    public void setCustomerDomain(ActionRequest request, ActionResponse response) {
        try {
            Company company = (Company) request.getContext().get("company");

            if (company != null) {
                // Simple domain
                String domain = "self.isCustomer = true AND self.company.id = " + company.getId();
                response.setAttr("customer", "domain", domain);
            }
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    public void setProductDomain(ActionRequest request, ActionResponse response) {
        try {
            // Domain with multiple conditions
            String domain = "self.sellable = true AND self.productTypeSelect = 'storable'";
            response.setAttr("saleOrderLineList.product", "domain", domain);
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Domain with Context Variables

```java
public class SaleOrderController {

    public void setContactDomain(ActionRequest request, ActionResponse response) {
        try {
            Partner customer = (Partner) request.getContext().get("customer");

            if (customer != null) {
                // Domain using context variable
                String domain = "self.mainPartner.id = :customerId";
                response.setAttr("contactPartner", "domain", domain);
                response.setAttr("contactPartner", "domain-context",
                    Map.of("customerId", customer.getId()));
            }
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Complex Domain Filters

```java
public class SaleOrderController {

    public void setAdvancedProductDomain(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();
            Company company = (Company) context.get("company");
            Partner customer = (Partner) context.get("customer");

            StringBuilder domain = new StringBuilder();
            domain.append("self.sellable = true");

            if (company != null) {
                domain.append(" AND self.company.id = ").append(company.getId());
            }

            if (customer != null && customer.getProductCategory() != null) {
                domain.append(" AND self.productCategory.id = ")
                      .append(customer.getProductCategory().getId());
            }

            domain.append(" AND self.endDate IS NULL OR self.endDate > '")
                  .append(LocalDate.now()).append("'");

            response.setAttr("saleOrderLineList.product", "domain", domain.toString());
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

## Error Handling with TraceBackService

### Basic Error Handling

```java
public class SaleOrderController {

    public void confirmOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            saleOrder = Beans.get(SaleOrderService.class).confirm(saleOrder);

            response.setReload(true);
            response.setFlash("Order confirmed");
        } catch (Exception e) {
            // Automatically logs error and sets response error
            TraceBackService.trace(response, e);
        }
    }
}
```

### Custom Error Messages

```java
public class SaleOrderController {

    public void processOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderService.class).process(saleOrder);

            response.setReload(true);
        } catch (AxelorException e) {
            // AxelorException with custom message
            TraceBackService.trace(response, e);
        } catch (Exception e) {
            // Wrap generic exception with custom message
            TraceBackService.trace(response, e, "Error processing sale order");
        }
    }
}
```

### Handling Multiple Operation Errors

```java
public class SaleOrderController {

    public void generateDocuments(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            List<String> errors = new ArrayList<>();

            // Try to generate invoice
            try {
                Beans.get(SaleOrderService.class).generateInvoice(saleOrder);
            } catch (Exception e) {
                errors.add("Invoice generation failed: " + e.getMessage());
                TraceBackService.trace(e);
            }

            // Try to generate delivery
            try {
                Beans.get(SaleOrderService.class).generateDelivery(saleOrder);
            } catch (Exception e) {
                errors.add("Delivery generation failed: " + e.getMessage());
                TraceBackService.trace(e);
            }

            if (!errors.isEmpty()) {
                response.setError(String.join("\n", errors));
            } else {
                response.setFlash("Documents generated successfully");
            }

            response.setReload(true);
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

## Complete Controller Examples

### Complete Button Action Example

```java
package com.axelor.apps.sale.web;

import com.axelor.apps.base.db.Company;
import com.axelor.apps.base.db.Partner;
import com.axelor.apps.sale.db.SaleOrder;
import com.axelor.apps.sale.db.repo.SaleOrderRepository;
import com.axelor.apps.sale.service.SaleOrderService;
import com.axelor.apps.sale.service.SaleOrderWorkflowService;
import com.axelor.exception.service.TraceBackService;
import com.axelor.inject.Beans;
import com.axelor.rpc.ActionRequest;
import com.axelor.rpc.ActionResponse;
import com.axelor.rpc.Context;

public class SaleOrderController {

    // Confirm order button
    public void confirmOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            if (!Beans.get(SaleOrderWorkflowService.class).canConfirm(saleOrder)) {
                response.setError("Cannot confirm this order");
                return;
            }

            saleOrder = Beans.get(SaleOrderWorkflowService.class).confirm(saleOrder);

            response.setReload(true);
            response.setFlash("Order " + saleOrder.getOrderNumber() + " confirmed successfully");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Finalize quotation button
    public void finalizeQuotation(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            saleOrder = Beans.get(SaleOrderWorkflowService.class).finalize(saleOrder);

            response.setReload(true);
            response.setNotify("Quotation finalized");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Cancel order button
    public void cancelOrder(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            saleOrder = Beans.get(SaleOrderWorkflowService.class).cancel(saleOrder);

            response.setReload(true);
            response.setNotify("Order canceled");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Compute totals button
    public void computeTotals(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);
            saleOrder = Beans.get(SaleOrderRepository.class).find(saleOrder.getId());

            saleOrder = Beans.get(SaleOrderService.class).computeTotals(saleOrder);

            response.setReload(true);
            response.setNotify("Totals computed");
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Complete onChange Example

```java
package com.axelor.apps.sale.web;

import com.axelor.apps.base.db.Company;
import com.axelor.apps.base.db.Partner;
import com.axelor.apps.base.db.repo.PartnerRepository;
import com.axelor.apps.sale.db.SaleOrder;
import com.axelor.apps.sale.service.SaleOrderService;
import com.axelor.exception.service.TraceBackService;
import com.axelor.inject.Beans;
import com.axelor.rpc.ActionRequest;
import com.axelor.rpc.ActionResponse;
import com.axelor.rpc.Context;
import java.time.LocalDate;

public class SaleOrderController {

    // Customer onChange
    public void onChangeCustomer(ActionRequest request, ActionResponse response) {
        try {
            Context context = request.getContext();
            Partner customer = (Partner) context.get("customer");

            if (customer == null) {
                return;
            }

            customer = Beans.get(PartnerRepository.class).find(customer.getId());

            // Set customer-related fields
            response.setValue("priceList", customer.getSalePriceList());
            response.setValue("paymentMode", customer.getPaymentMode());
            response.setValue("paymentCondition", customer.getPaymentCondition());
            response.setValue("deliveryAddress", customer.getMainAddress());
            response.setValue("currency", customer.getCurrency());
            response.setValue("fiscalPosition", customer.getFiscalPosition());

            // Set domains
            response.setAttr("contactPartner", "domain",
                "self.mainPartner.id = " + customer.getId());

            // Check if customer is blocked
            if (customer.getBlocked()) {
                response.setNotify("Warning: Customer is blocked", "warning");
            }

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Company onChange
    public void onChangeCompany(ActionRequest request, ActionResponse response) {
        try {
            Company company = (Company) request.getContext().get("company");

            if (company == null) {
                return;
            }

            response.setValue("currency", company.getCurrency());
            response.setValue("stockLocation", company.getDefaultStockLocation());

            // Update domains
            response.setAttr("customer", "domain",
                "self.isCustomer = true AND :company MEMBER OF self.companySet");

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // Order date onChange
    public void onChangeOrderDate(ActionRequest request, ActionResponse response) {
        try {
            LocalDate orderDate = (LocalDate) request.getContext().get("orderDate");

            if (orderDate != null) {
                LocalDate expectedDeliveryDate = orderDate.plusDays(7);
                response.setValue("expectedDeliveryDate", expectedDeliveryDate);
            }
        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### Complete Form Action Example

```java
package com.axelor.apps.sale.web;

import com.axelor.apps.base.service.app.AppBaseService;
import com.axelor.apps.base.service.user.UserService;
import com.axelor.apps.sale.db.SaleOrder;
import com.axelor.apps.sale.db.repo.SaleOrderRepository;
import com.axelor.exception.service.TraceBackService;
import com.axelor.inject.Beans;
import com.axelor.rpc.ActionRequest;
import com.axelor.rpc.ActionResponse;
import java.time.LocalDate;

public class SaleOrderController {

    // onNew - set defaults for new record
    public void onNew(ActionRequest request, ActionResponse response) {
        try {
            Company company = Beans.get(UserService.class).getActiveCompany();

            if (company != null) {
                response.setValue("company", company);
                response.setValue("currency", company.getCurrency());
                response.setValue("priceList", company.getDefaultSalePriceList());
                response.setValue("stockLocation", company.getDefaultStockLocation());
            }

            LocalDate today = Beans.get(AppBaseService.class).getTodayDate(company);
            response.setValue("orderDate", today);
            response.setValue("creationDate", today);
            response.setValue("statusSelect", SaleOrderRepository.STATUS_DRAFT_QUOTATION);

            response.setAttr("customer", "domain", "self.isCustomer = true");

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    // onLoad - set UI state for existing record
    public void onLoad(ActionRequest request, ActionResponse response) {
        try {
            SaleOrder saleOrder = request.getContext().asType(SaleOrder.class);

            if (saleOrder.getId() == null) {
                return;
            }

            // Readonly fields based on status
            boolean isConfirmed = saleOrder.getStatusSelect() >=
                SaleOrderRepository.STATUS_ORDER_CONFIRMED;

            if (isConfirmed) {
                response.setAttr("customer", "readonly", true);
                response.setAttr("company", "readonly", true);
                response.setAttr("orderDate", "readonly", true);
                response.setAttr("saleOrderLineList", "readonly", true);
            }

            // Show/hide buttons
            response.setAttr("confirmBtn", "hidden", isConfirmed);
            response.setAttr("finalizeBtn", "hidden",
                saleOrder.getStatusSelect() != SaleOrderRepository.STATUS_DRAFT_QUOTATION);

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

---

## Anti-Patterns to Avoid

### Do NOT Create moveUp/moveDown Methods

Axelor provides **automatic row reordering** via the `canMove` attribute on grids. Do NOT create custom `moveUp()` or `moveDown()` controller methods.

**Wrong approach:**
```java
// DO NOT DO THIS - Axelor handles this automatically
public void moveUp(ActionRequest request, ActionResponse response) {
    try {
        MyLine line = request.getContext().asType(MyLine.class);
        if (line.getSequence() > 0) {
            line.setSequence(line.getSequence() - 1);
            Beans.get(MyLineRepository.class).save(line);
        }
        response.setReload(true);
    } catch (Exception e) {
        TraceBackService.trace(response, e);
    }
}
```

**Correct approach - Use grid `canMove` attribute:**
```xml
<!-- In your grid view -->
<grid name="my-line-grid" model="com.axelor.apps.module.db.MyLine"
      orderBy="sequence" canMove="true" editable="true">
  <field name="sequence" width="50"/>
  <field name="product"/>
  <field name="quantity"/>
</grid>
```

With `canMove="true"`, Axelor automatically:
- Enables drag-and-drop reordering in the grid
- Updates the `sequence` field when rows are moved
- Persists the new order

**Requirements for automatic reordering:**
1. Entity must have an integer `sequence` field
2. Grid must have `orderBy="sequence"`
3. Grid must have `canMove="true"`

---

## Controller Extension and Overriding

### Important: Controllers Are NOT Injected

Unlike services, controllers in Axelor are **NOT injected via Guice**. They are referenced **by fully qualified class name** in action definitions.

**Consequences for extensions:**
1. You cannot simply extend a controller and have it automatically used
2. You must **modify all actions** that reference the original controller
3. This makes controller overriding **maintenance-heavy**

**Example - Original action:**
```xml
<action-method name="action-sale-order-confirm">
  <call class="com.axelor.apps.sale.web.SaleOrderController" method="confirm"/>
</action-method>
```

**To override, you must:**
1. Create your extension controller
2. Create an **action extension** that replaces the class reference

```xml
<!-- In your module's views -->
<action-method name="action-sale-order-confirm" id="custom-action-sale-order-confirm">
  <call class="com.axelor.apps.custom.web.SaleOrderControllerCustom" method="confirm"/>
</action-method>
```

> **Best Practice:** Avoid overriding controllers when possible. Instead:
> - Override the **service** called by the controller
> - Use **action-group** to add actions before/after existing ones
> - Use **view extensions** to add new buttons with new actions

---

This comprehensive controller documentation provides complete, working examples of all common controller patterns and best practices in Axelor applications.
