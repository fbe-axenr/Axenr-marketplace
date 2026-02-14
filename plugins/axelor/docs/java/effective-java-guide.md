# Effective Java Guidelines

This guide contains strict enforcement guidelines based on Effective Java (3rd Edition) best practices for Axelor development.

## Effective Java Guidelines (STRICT ENFORCEMENT)

### Overview

**ALL generated Java code MUST strictly follow Effective Java (3rd Edition) best practices.**

This section contains the most critical items from the 87 Effective Java guidelines, organized by importance for Axelor development.

### Chapter 2: Creating and Destroying Objects

#### Item 1: Consider Static Factory Methods Instead of Constructors

**Rule**: Prefer static factory methods with descriptive names over constructors.

**Benefits**:
- More readable names (unlike constructors)
- Can return cached instances
- Can return subtypes

**Pattern**:
```java
public class SaleOrder {

    private SaleOrder() {
        // Private constructor
    }

    // Static factory method with descriptive name
    public static SaleOrder createDraft(Customer customer) {
        Objects.requireNonNull(customer, "Customer cannot be null");
        SaleOrder order = new SaleOrder();
        order.setCustomer(customer);
        order.setStatusSelect(STATUS_DRAFT);
        order.setOrderDate(LocalDate.now());
        return order;
    }

    public static SaleOrder createFromQuotation(Quotation quotation) {
        Objects.requireNonNull(quotation, "Quotation cannot be null");
        SaleOrder order = new SaleOrder();
        order.setCustomer(quotation.getCustomer());
        order.setStatusSelect(STATUS_DRAFT);
        // Copy quotation lines
        return order;
    }
}
```

#### Item 2: Consider a Builder When Faced with Many Parameters

**Rule**: Use Builder pattern for classes with more than 4 parameters.

**Pattern**:
```java
public class InvoiceBuilder {

    private final Customer customer;
    private final LocalDate invoiceDate;
    private Company company;
    private Currency currency;
    private PaymentMode paymentMode;
    private PaymentCondition paymentCondition;

    // Required parameters in constructor
    public InvoiceBuilder(Customer customer, LocalDate invoiceDate) {
        this.customer = Objects.requireNonNull(customer, "Customer cannot be null");
        this.invoiceDate = Objects.requireNonNull(invoiceDate, "Invoice date cannot be null");
    }

    // Optional parameters with fluent setters
    public InvoiceBuilder company(Company company) {
        this.company = company;
        return this;
    }

    public InvoiceBuilder currency(Currency currency) {
        this.currency = currency;
        return this;
    }

    public InvoiceBuilder paymentMode(PaymentMode paymentMode) {
        this.paymentMode = paymentMode;
        return this;
    }

    public InvoiceBuilder paymentCondition(PaymentCondition paymentCondition) {
        this.paymentCondition = paymentCondition;
        return this;
    }

    public Invoice build() {
        Invoice invoice = new Invoice();
        invoice.setCustomer(customer);
        invoice.setInvoiceDate(invoiceDate);
        invoice.setCompany(company != null ? company : customer.getCompany());
        invoice.setCurrency(currency != null ? currency : customer.getCurrency());
        invoice.setPaymentMode(paymentMode);
        invoice.setPaymentCondition(paymentCondition);
        return invoice;
    }
}

// Usage:
Invoice invoice = new InvoiceBuilder(customer, LocalDate.now())
    .company(company)
    .currency(euro)
    .paymentMode(bankTransfer)
    .build();
```

#### Item 5: Prefer Dependency Injection to Hardwiring Resources

**Rule**: ALWAYS use dependency injection via Google Guice with @Inject.

**CORRECT** (with dependency injection):
```java
public class SaleOrderServiceImpl implements SaleOrderService {

    private final SaleOrderRepository saleOrderRepo;
    private final SaleOrderLineService saleOrderLineService;
    private final TaxService taxService;

    @Inject
    public SaleOrderServiceImpl(
            SaleOrderRepository saleOrderRepo,
            SaleOrderLineService saleOrderLineService,
            TaxService taxService) {
        this.saleOrderRepo = saleOrderRepo;
        this.saleOrderLineService = saleOrderLineService;
        this.taxService = taxService;
    }
}
```

**FORBIDDEN** (hardwired resources):
```java
public class SaleOrderServiceImpl implements SaleOrderService {

    // WRONG: Direct instantiation
    private final SaleOrderRepository saleOrderRepo = new SaleOrderRepository();
    private final TaxService taxService = new TaxServiceImpl();
}
```

### Chapter 8: Methods

#### Item 49: Check Parameters for Validity

**Rule**: Validate ALL method parameters at the beginning of the method.

**Pattern**:
```java
public Invoice createInvoice(Customer customer, LocalDate invoiceDate, List<InvoiceLine> lines) {
    // Parameter validation FIRST
    Objects.requireNonNull(customer, "Customer cannot be null");
    Objects.requireNonNull(invoiceDate, "Invoice date cannot be null");
    Objects.requireNonNull(lines, "Invoice lines cannot be null");

    if (lines.isEmpty()) {
        throw new IllegalArgumentException("Invoice must have at least one line");
    }

    if (invoiceDate.isAfter(LocalDate.now())) {
        throw new IllegalArgumentException("Invoice date cannot be in the future");
    }

    // Method logic after validation
    Invoice invoice = new Invoice();
    invoice.setCustomer(customer);
    invoice.setInvoiceDate(invoiceDate);
    invoice.setInvoiceLineList(lines);
    return invoice;
}
```

#### Item 54: Return Empty Collections or Arrays, Not Nulls

**Rule**: NEVER return null for collections. Always return empty collections.

**CORRECT**:
```java
public List<SaleOrderLine> findLinesByProduct(Product product) {
    Objects.requireNonNull(product, "Product cannot be null");

    List<SaleOrderLine> lines = saleOrderLineRepo.findByProduct(product).fetch();

    // Return empty list if no results, NEVER null
    return lines != null ? lines : Collections.emptyList();
}
```

**FORBIDDEN**:
```java
public List<SaleOrderLine> findLinesByProduct(Product product) {
    List<SaleOrderLine> lines = saleOrderLineRepo.findByProduct(product).fetch();
    // WRONG: returning null
    return lines;
}
```

#### Item 55: Return Optionals Judiciously

**Rule**: Use Optional<T> for methods that may not return a value (except collections).

**Creating Optionals**:
```java
public Optional<SaleOrder> findOrderByReference(String reference) {
    Objects.requireNonNull(reference, "Reference cannot be null");

    SaleOrder order = saleOrderRepo.findByReference(reference);
    return Optional.ofNullable(order);
}
```

**CORRECT Usage - Modern Optional APIs**:
```java
// Use ifPresent() for side effects
service.findOrderByReference("SO12345")
    .ifPresent(order -> processOrder(order));

// Use orElse() for default value
SaleOrder order = service.findOrderByReference("SO12345")
    .orElse(createDefaultOrder());

// Use orElseGet() for lazy default value
SaleOrder order = service.findOrderByReference("SO12345")
    .orElseGet(() -> createDefaultOrder());

// Use orElseThrow() when value is required
SaleOrder order = service.findOrderByReference("SO12345")
    .orElseThrow(() -> new AxelorException(
        String.format("Order not found: %s", "SO12345")
    ));

//  Use map() for transformation
String customerName = service.findOrderByReference("SO12345")
    .map(SaleOrder::getCustomer)
    .map(Customer::getFullName)
    .orElse("Unknown");

// Use filter() for conditional logic
Optional<SaleOrder> confirmedOrder = service.findOrderByReference("SO12345")
    .filter(order -> order.getStatusSelect() == STATUS_CONFIRMED);

// Use isEmpty() for null check
if (service.findOrderByReference("SO12345").isEmpty()) {
    throw new AxelorException("Order not found");
}

// Use ifPresentOrElse() for both cases
service.findOrderByReference("SO12345")
    .ifPresentOrElse(
        order -> processOrder(order),
        () -> handleOrderNotFound()
    );
```

**FORBIDDEN - Antipatterns**:
```java
// WRONG: isPresent() + get() defeats the purpose of Optional
Optional<SaleOrder> orderOpt = service.findOrderByReference("SO12345");
if (orderOpt.isPresent()) {
    SaleOrder order = orderOpt.get();  // Use orElseThrow() instead!
    processOrder(order);
}

// WRONG: Calling get() without checking isPresent()
SaleOrder order = service.findOrderByReference("SO12345")
    .get();  //Can throw NoSuchElementException!

// WRONG: Using Optional as method parameter
public void processOrder(Optional<SaleOrder> order) {
    // BAD! Use nullable parameter instead
}

// WRONG: Using Optional as entity field
public class SaleOrder {
    private Optional<Customer> customer;  // BAD! Use nullable field instead
}

// WRONG: Returning Optional.of() with potentially null value
public Optional<SaleOrder> findOrder(Long id) {
    return Optional.of(repository.find(id));  // Use ofNullable() instead!
}
```

**When NOT to use Optional**:
- Collections (use empty collections instead)
- Primitive types (use OptionalInt, OptionalLong, OptionalDouble)
- Fields in entities (use nullable fields instead)
- Method parameters (use nullable parameters instead)

### Chapter 9: General Programming

#### Item 62: Avoid Strings Where Other Types Are More Appropriate

**Rule**: Use appropriate types instead of strings for typed data.

**CORRECT**:
```java
// Use enums for status
public enum SaleOrderStatus {
    DRAFT,
    CONFIRMED,
    FINISHED,
    CANCELLED
}

public class SaleOrder {
    private SaleOrderStatus status;

    public void setStatus(SaleOrderStatus status) {
        this.status = Objects.requireNonNull(status, "Status cannot be null");
    }
}

// Use BigDecimal for money
private BigDecimal totalAmount;

// Use LocalDate for dates
private LocalDate orderDate;

// Use Integer for database selection fields
private Integer statusSelect;
```

**FORBIDDEN**:
```java
// WRONG: Using strings for typed data
private String status; // Should be enum or Integer (statusSelect)
private String totalAmount; // Should be BigDecimal
private String orderDate; // Should be LocalDate
```

#### Item 64: Refer to Objects by Their Interfaces

**Rule**: Use interface types for parameters, return types, and variables.

**CORRECT**:
```java
public class SaleOrderServiceImpl implements SaleOrderService {

    // Use interface type
    private final SaleOrderRepository saleOrderRepository;

    @Inject
    public SaleOrderServiceImpl(SaleOrderRepository saleOrderRepository) {
        this.saleOrderRepository = saleOrderRepository;
    }

    // Parameters and return types use interfaces
    public List<SaleOrder> filterOrders(List<SaleOrder> orders, Predicate<SaleOrder> filter) {
        Objects.requireNonNull(orders, "Orders cannot be null");
        Objects.requireNonNull(filter, "Filter cannot be null");

        return orders.stream()
            .filter(filter)
            .collect(Collectors.toList());
    }
}
```

**FORBIDDEN**:
```java
// WRONG: Using concrete types
public ArrayList<SaleOrder> filterOrders(ArrayList<SaleOrder> orders) {
    // Wrong
}
```

### Chapter 10: Exceptions

#### Item 69: Use Exceptions Only for Exceptional Conditions

**Rule**: Exceptions are for exceptional conditions, not normal control flow.

**CORRECT**:
```java
// Use normal control flow for empty collections
public void processOrders(List<SaleOrder> orders) {
    Objects.requireNonNull(orders, "Orders cannot be null");

    // Use normal control flow for empty list
    if (orders.isEmpty()) {
        return; // Normal case, no exception
    }

    for (SaleOrder order : orders) {
        processOrder(order);
    }
}

// Explicit null check instead of catching NullPointerException
public void processOrderCustomer(SaleOrder order) {
    Objects.requireNonNull(order, "Order cannot be null");

    if (order.getCustomer() != null) {
        processCustomer(order.getCustomer());
    } else {
        // Handle missing customer (normal case)
        handleMissingCustomer(order);
    }
}

//  Use Optional to avoid null checks
public void processOrderCustomer(SaleOrder order) {
    Objects.requireNonNull(order, "Order cannot be null");

    Optional.ofNullable(order.getCustomer())
        .ifPresentOrElse(
            this::processCustomer,
            () -> handleMissingCustomer(order)
        );
}

// Check Map.containsKey() before accessing value
public void applyProductPrice(Long productId, Map<Long, BigDecimal> priceMap) {
    Objects.requireNonNull(productId, "Product ID cannot be null");
    Objects.requireNonNull(priceMap, "Price map cannot be null");

    if (priceMap.containsKey(productId)) {
        BigDecimal price = priceMap.get(productId);
        applyPrice(price);
    } else {
        handleMissingPrice(productId);
    }
}

// Use Map.getOrDefault() for default values
public BigDecimal getProductPrice(Long productId, Map<Long, BigDecimal> priceMap) {
    Objects.requireNonNull(productId, "Product ID cannot be null");
    Objects.requireNonNull(priceMap, "Price map cannot be null");

    return priceMap.getOrDefault(productId, BigDecimal.ZERO);
}
```

**FORBIDDEN**:
```java
// WRONG: Using IndexOutOfBoundsException for control flow
public void processOrders(List<SaleOrder> orders) {
    try {
        // WRONG: Using exception for control flow
        for (int i = 0; ; i++) {
            processOrder(orders.get(i));
        }
    } catch (IndexOutOfBoundsException e) {
        // WRONG: Exception for normal loop termination
    }
}

// WRONG: Using NullPointerException for control flow
public void processOrderCustomer(SaleOrder order) {
    try {
        processCustomer(order.getCustomer());
    } catch (NullPointerException e) {
        // WRONG: null check should be explicit
        handleMissingCustomer(order);
    }
}

// WRONG: Exceptions are expensive (100-1000x slower than normal flow)
public BigDecimal calculateDiscount(SaleOrder order) {
    try {
        return order.getCustomer().getDefaultDiscount();
    } catch (NullPointerException e) {
        return BigDecimal.ZERO;  // WRONG: Use explicit checks instead
    }
}

// WRONG: Using try/catch with Map.get() for missing keys
public void applyProductPrice(Long productId, Map<Long, BigDecimal> priceMap) {
    try {
        BigDecimal price = priceMap.get(productId);
        applyPrice(price);  // NPE if productId not in map
    } catch (NullPointerException e) {
        // WRONG: Use containsKey() or getOrDefault() instead
    }
}
```

**Performance Note**: Exceptions are 100-1000x slower than normal control flow due to stack trace creation and exception handling overhead. Use them only for truly exceptional conditions.

#### Item 72: Favor the Use of Standard Exceptions

**Rule**: Use standard Java exceptions and AxelorException appropriately.

**Standard Exceptions to Use**:
- `IllegalArgumentException`: Invalid parameter value
- `IllegalStateException`: Invalid object state
- `NullPointerException`: Null parameter (use Objects.requireNonNull instead)
- `UnsupportedOperationException`: Unsupported operation
- `AxelorException`: Axelor business logic errors

**Pattern**:
```java
public void confirmOrder(SaleOrder order) throws AxelorException {
    // Parameter validation: IllegalArgumentException
    Objects.requireNonNull(order, "Order cannot be null");

    if (order.getId() == null) {
        throw new IllegalArgumentException("Order must be saved before confirmation");
    }

    // State validation: IllegalStateException
    if (order.getStatusSelect() != STATUS_DRAFT) {
        throw new IllegalStateException(
            String.format("Cannot confirm order in status %d", order.getStatusSelect())
        );
    }

    // Business validation: AxelorException
    if (order.getSaleOrderLineList() == null || order.getSaleOrderLineList().isEmpty()) {
        throw new AxelorException(
            "Order must have at least one line"
        );
    }

    // Confirmation logic
    order.setStatusSelect(STATUS_CONFIRMED);
    order.setConfirmationDate(LocalDate.now());
}
```

#### Item 75: Include Failure-Capture Information in Detail Messages

**Rule**: Exception messages MUST include all relevant information for debugging.

**CORRECT**:
```java
public void validateOrderLine(SaleOrderLine line) throws AxelorException {
    Objects.requireNonNull(line, "Sale order line cannot be null");

    if (line.getQuantity() == null || line.getQuantity().compareTo(BigDecimal.ZERO) <= 0) {
        throw new AxelorException(
            String.format(
                "Invalid quantity for line %d: %s (must be > 0)",
                line.getId(),
                line.getQuantity()
            )
        );
    }

    if (line.getPrice() == null || line.getPrice().compareTo(BigDecimal.ZERO) < 0) {
        throw new AxelorException(
            String.format(
                "Invalid price for line %d, product '%s': %s (must be >= 0)",
                line.getId(),
                line.getProduct() != null ? line.getProduct().getName() : "null",
                line.getPrice()
            )
        );
    }
}
```

**FORBIDDEN**:
```java
// WRONG: Vague error message
if (line.getQuantity().compareTo(BigDecimal.ZERO) <= 0) {
    throw new AxelorException("Invalid quantity" // Too vague, no context
    );
}
```

### Naming Conventions (Effective Java Item 68)

**Rule**: Follow Java naming conventions strictly.

**Classes and Interfaces**: PascalCase
```java
public class SaleOrderService { }
public interface InvoiceRepository { }
public class CustomerDTO { }
```

**Methods and Variables**: camelCase
```java
private BigDecimal totalAmount;
private LocalDate orderDate;

public void computeTotalAmount() { }
public Customer findCustomerById(Long customerId) { }
```

**Constants**: UPPER_SNAKE_CASE
```java
public static final int STATUS_DRAFT = 1;
public static final int STATUS_CONFIRMED = 2;
public static final String DEFAULT_CURRENCY_CODE = "EUR";
private static final int MAX_RETRY_ATTEMPTS = 3;
```

**Packages**: lowercase
```java
package com.axelor.apps.sale.service;
package com.axelor.apps.account.db.repo;
```

### Magic Numbers and String Literals

**Rule**: NEVER use magic numbers or magic strings. Use named constants.

**CORRECT**:
```java
public class SaleOrder {

    // Named constants for status
    public static final int STATUS_DRAFT = 1;
    public static final int STATUS_CONFIRMED = 2;
    public static final int STATUS_FINISHED = 3;
    public static final int STATUS_CANCELLED = 4;

    // Named constants for business rules
    private static final BigDecimal MIN_ORDER_AMOUNT = new BigDecimal("100.00");
    private static final int MAX_LINES_PER_ORDER = 1000;
    private static final int DISCOUNT_THRESHOLD_DAYS = 30;

    public void validateOrder() throws AxelorException {
        if (this.statusSelect != STATUS_DRAFT) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                String.format("Cannot validate order in status %d", this.statusSelect)
            );
        }

        if (this.exTaxTotal.compareTo(MIN_ORDER_AMOUNT) < 0) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                String.format(
                    "Order amount %.2f is below minimum %.2f",
                    this.exTaxTotal,
                    MIN_ORDER_AMOUNT
                )
            );
        }
    }
}
```

**FORBIDDEN**:
```java
// WRONG: Magic numbers and strings
public void validateOrder() throws AxelorException {
    if (this.statusSelect != 1) { // What is 1?
        throw new AxelorException(
            TraceBackRepository.CATEGORY_INCONSISTENCY,
            "Cannot validate order"
        );
    }

    if (this.exTaxTotal.compareTo(new BigDecimal("100.00")) < 0) { // What is 100.00?
        throw new AxelorException(
            TraceBackRepository.CATEGORY_INCONSISTENCY,
            "Order amount too low"
        );
    }
}
```

### Summary: Effective Java Enforcement Checklist

When generating Java code, VERIFY:

- [ ] Static factory methods used instead of public constructors when appropriate
- [ ] Builder pattern used for classes with 4+ parameters
- [ ] Dependency injection with @Inject (NEVER direct instantiation)
- [ ] ALL method parameters validated with Objects.requireNonNull() or checks
- [ ] Collections: return empty instead of null (Collections.emptyList())
- [ ] Optional<T> used for methods that may not return a value
- [ ] Appropriate types: BigDecimal for money, LocalDate for dates, enums for status
- [ ] Interface types for parameters/return types/variables
- [ ] Exceptions only for exceptional conditions (not control flow)
- [ ] Standard exceptions used (IllegalArgumentException, IllegalStateException, AxelorException)
- [ ] Exception messages include ALL relevant debugging information
- [ ] Naming: PascalCase (classes), camelCase (methods/vars), UPPER_SNAKE_CASE (constants)
- [ ] NO magic numbers or strings (use named constants)
- [ ] NO EMOJIS anywhere
- [ ] ALL code and comments in ENGLISH
