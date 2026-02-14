# Solution Templates

This document provides detailed, step-by-step solution templates for common Axelor code issues.

## Overview

When generating fix specifications, use these templates to provide actionable, detailed solutions. Each template includes:
- Clear, numbered steps
- Specific code patterns to use
- Verification steps
- Common pitfalls to avoid

---

## Critical Issues

### SQL Injection

**Issue Pattern**: String concatenation in queries, unparameterized user input

**Solution Template**:
```
1. Locate the query with string concatenation in {FileName}:{line}
2. Replace string concatenation with parameterized query using named parameters
3. Use the pattern: .filter("field = :param").bind("param", value)
4. Never concatenate user input directly into queries
5. Test with special characters (', ", --, ;) to verify SQL injection is prevented

Example transformation:
  BEFORE: query.filter("name = '" + userName + "'")
  AFTER:  query.filter("name = :name").bind("name", userName)
```

**Verification**:
- Run the application with special characters in input
- Verify query executes safely without syntax errors
- Check logs to confirm parameterized query is used

---

### @Inject in Controller

**Issue Pattern**: Controller using @Inject instead of Beans.get()

**Solution Template**:
```
1. Remove all @Inject annotations from {ClassName}
2. Remove injected field declarations
3. In each method that needs the service, use: Beans.get(ServiceClass.class)
4. Add import: com.axelor.inject.Beans
5. Verify controller doesn't cache service instances in fields

Example transformation:
  BEFORE:
    @Inject private CustomerService customerService;

  AFTER:
    // In each method:
    CustomerService customerService = Beans.get(CustomerService.class);
```

**Verification**:
- Remove all @Inject annotations
- Run the application and verify no NullPointerException occurs
- Check that services are properly retrieved in each method

**Common Pitfalls**:
- Don't cache Beans.get() results in controller fields
- Don't forget to add the Beans import
- Don't use @Inject anywhere in controllers

---

### Hardcoded Credentials

**Issue Pattern**: Passwords, tokens, or secrets in source code

**Solution Template**:
```
1. Remove hardcoded credential from {FileName}:{line}
2. Move credential to application.properties or environment variable
3. In application.properties: add property (e.g., api.key=PLACEHOLDER)
4. Load property using AppSettings:
   String apiKey = AppSettings.get().get("api.key");
5. Document the required configuration in README.md
6. Add property to .env.example (never .env itself)

Example transformation:
  BEFORE:
    String apiKey = "sk_live_abc123xyz";

  AFTER:
    String apiKey = AppSettings.get().get("api.key");
```

**Verification**:
- Search codebase for any remaining hardcoded credentials
- Verify application reads from configuration correctly
- Test with different configuration values

---

## High Priority Issues

### Missing @Transactional

**Issue Pattern**: Write operations (save, persist, remove) without @Transactional

**Solution Template**:
```
1. Add @Transactional annotation to method {methodName} in {FileName}:{line}
2. Include parameter: rollbackOn = {Exception.class}
3. Ensure method is public (private methods cannot be transactional)
4. Verify exception handling doesn't catch and suppress exceptions
5. Import: com.google.inject.persist.Transactional

Example:
  @Transactional(rollbackOn = {Exception.class})
  public Customer saveCustomer(Customer customer) {
    return customerRepository.save(customer);
  }
```

**Verification**:
- Method is public
- Annotation includes rollbackOn parameter
- Test that transaction rolls back on errors

**Common Pitfalls**:
- Private methods are not transactional
- Catching exceptions without rethrowing prevents rollback
- Missing rollbackOn parameter may not rollback on all exceptions

---

### N+1 Query Pattern

**Issue Pattern**: Loop executing repository calls

**Solution Template**:
```
1. Identify the loop in {FileName}:{line} that calls repository
2. Replace loop + repository calls with single query using filter
3. Use IN clause or fetch join to load related data upfront
4. Process results in memory instead of additional queries

Example transformation:
  BEFORE:
    for (Order order : orders) {
      Customer customer = customerRepo.find(order.getCustomer().getId());
      // process customer
    }

  AFTER:
    List<Long> customerIds = orders.stream()
      .map(o -> o.getCustomer().getId())
      .collect(Collectors.toList());
    List<Customer> customers = customerRepo.all()
      .filter("self.id IN :ids")
      .bind("ids", customerIds)
      .fetch();
    Map<Long, Customer> customerMap = customers.stream()
      .collect(Collectors.toMap(Customer::getId, c -> c));
    for (Order order : orders) {
      Customer customer = customerMap.get(order.getCustomer().getId());
      // process customer
    }
```

**Verification**:
- Enable SQL logging: logging.level.org.hibernate.SQL=DEBUG
- Verify only 1-2 queries execute instead of N+1
- Performance test with large datasets

---

### Field Injection in Services

**Issue Pattern**: @Inject on fields instead of constructor

**Solution Template**:
```
1. Remove @Inject annotations from fields in {FileName}:{line}
2. Create a constructor with all dependencies as parameters
3. Add @Inject to the constructor
4. Assign constructor parameters to final fields
5. Ensure fields are declared final for immutability

Example transformation:
  BEFORE:
    public class CustomerServiceImpl implements CustomerService {
      @Inject private CustomerRepository customerRepository;
      @Inject private PartnerService partnerService;
    }

  AFTER:
    public class CustomerServiceImpl implements CustomerService {
      private final CustomerRepository customerRepository;
      private final PartnerService partnerService;

      @Inject
      public CustomerServiceImpl(
          CustomerRepository customerRepository,
          PartnerService partnerService) {
        this.customerRepository = customerRepository;
        this.partnerService = partnerService;
      }
    }
```

**Verification**:
- All dependencies are constructor parameters
- Fields are final
- No @Inject on fields
- Service can be unit tested with mock dependencies

---

### Business Logic in Controller

**Issue Pattern**: Complex calculations, loops, or business rules in controller

**Solution Template**:
```
1. Identify business logic in controller method {methodName} at {FileName}:{line}
2. Create a new service method to encapsulate this logic
3. Move the business logic to the service method
4. Update controller to call the service method via Beans.get()
5. Return ActionResponse with appropriate status/message

Example transformation:
  BEFORE (Controller):
    public void calculateTotal(ActionRequest request, ActionResponse response) {
      Customer customer = request.getContext().asType(Customer.class);
      BigDecimal total = BigDecimal.ZERO;
      for (Order order : customer.getOrders()) {
        total = total.add(order.getAmount());
      }
      response.setValue("totalOrders", total);
    }

  AFTER (Controller):
    public void calculateTotal(ActionRequest request, ActionResponse response) {
      Customer customer = request.getContext().asType(Customer.class);
      CustomerService service = Beans.get(CustomerService.class);
      BigDecimal total = service.calculateCustomerTotal(customer);
      response.setValue("totalOrders", total);
    }

  AFTER (Service):
    public BigDecimal calculateCustomerTotal(Customer customer) {
      return customer.getOrders().stream()
        .map(Order::getAmount)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
```

**Verification**:
- Controller method is < 10 lines
- Business logic is testable in service
- Service method can be reused elsewhere

---

### Missing JPA.clear() in Batch

**Issue Pattern**: Batch processing without clearing persistence context

**Solution Template**:
```
1. Locate the batch processing loop in {FileName}:{line}
2. Add counter variable to track processed items
3. Call JPA.clear() every 20-50 items (configurable based on entity size)
4. Optionally flush before clear to persist changes
5. Import: com.axelor.db.JPA

Example:
  int batchSize = 20;
  int counter = 0;

  for (Customer customer : customers) {
    // Process customer
    customerRepository.save(customer);

    counter++;
    if (counter % batchSize == 0) {
      JPA.flush();
      JPA.clear();
    }
  }

  // Final flush and clear for remaining items
  JPA.flush();
  JPA.clear();
```

**Verification**:
- Monitor memory usage during batch processing
- Verify no OutOfMemoryError with large datasets
- Check that all changes are persisted correctly

---

### Not Fetching Managed Entity

**Issue Pattern**: Using context entity directly without fetching from DB

**Solution Template**:
```
1. Identify where context entity is used in {FileName}:{line}
2. Extract the entity ID from context
3. Fetch managed entity from database using repository
4. Work with the fetched entity instead of context entity
5. Ensure repository is obtained via Beans.get()

Example transformation:
  BEFORE:
    Customer customer = request.getContext().asType(Customer.class);
    customer.setName("Updated");
    // Changes may not persist correctly

  AFTER:
    Customer customer = request.getContext().asType(Customer.class);
    CustomerRepository repo = Beans.get(CustomerRepository.class);
    Customer managedCustomer = repo.find(customer.getId());
    managedCustomer.setName("Updated");
    repo.save(managedCustomer);
```

**Verification**:
- Entity is fetched from database
- Changes are properly persisted
- No detached entity exceptions

---

## Medium Priority Issues

### French Comments

**Issue Pattern**: Comments in French

**Solution Template**:
```
1. Locate French comments in {FileName}:{line}
2. Translate comments to English
3. Verify technical terms are accurate
4. Use clear, concise English
5. Follow English comment conventions (// for single line, /** */ for JavaDoc)

Translation guidelines:
- "Récupère" → "Retrieves" or "Gets"
- "Sauvegarde" → "Saves"
- "Vérifie" → "Checks" or "Verifies"
- "Crée" → "Creates"
- "Supprime" → "Deletes" or "Removes"
```

---

### Emoji in Code

**Issue Pattern**: Emoji characters in source code

**Solution Template**:
```
1. Remove emoji from {FileName}:{line}
2. Replace with descriptive text or appropriate comment
3. If used for logging, use text-based severity indicators
4. Check file encoding is UTF-8 without BOM

Example:
  BEFORE: log.debug("Processing customer ✅");
  AFTER:  log.debug("Processing customer - success");
```

---

### String Concatenation in Logging

**Issue Pattern**: Using + operator in log statements

**Solution Template**:
```
1. Locate string concatenation in log statement at {FileName}:{line}
2. Replace concatenation with parameterized logging
3. Use {} placeholders for parameters
4. Pass parameters as additional arguments

Example transformation:
  BEFORE: log.debug("Customer: " + customer.getName() + " Total: " + total);
  AFTER:  log.debug("Customer: {} Total: {}", customer.getName(), total);
```

**Benefits**:
- Parameters only evaluated if log level is enabled
- Better performance in production
- Cleaner, more readable code

---

### Magic Numbers

**Issue Pattern**: Hardcoded numeric values in code

**Solution Template**:
```
1. Identify magic number in {FileName}:{line}
2. Create a static final constant with descriptive name
3. Place constant in appropriate location (Repository for status, class level for thresholds)
4. Replace all occurrences with constant reference

Example transformation:
  BEFORE:
    if (order.getStatusSelect() == 3) { ... }

  AFTER:
    // In OrderRepository interface:
    public static final int STATUS_VALIDATED = 3;

    // In code:
    if (order.getStatusSelect() == OrderRepository.STATUS_VALIDATED) { ... }
```

---

### Incorrect Logger Declaration

**Issue Pattern**: Logger not using MethodHandles pattern

**Solution Template**:
```
1. Locate logger declaration in {FileName}:{line}
2. Replace with MethodHandles.lookup().lookupClass() pattern
3. Import: java.lang.invoke.MethodHandles
4. Use private static final for the logger field

Example transformation:
  BEFORE:
    private static final Logger log = LoggerFactory.getLogger(CustomerServiceImpl.class);

  AFTER:
    private static final Logger log = LoggerFactory.getLogger(
      MethodHandles.lookup().lookupClass());
```

---

### Missing TraceBackService.trace()

**Issue Pattern**: Exception handling without TraceBackService

**Solution Template**:
```
1. Locate exception handling in {FileName}:{line}
2. Add TraceBackService.trace() call in catch block
3. Import: com.axelor.exception.service.TraceBackService
4. Obtain service via Beans.get(TraceBackService.class)
5. Call trace() with exception and optionally additional context

Example:
  try {
    // operation
  } catch (Exception e) {
    TraceBackService.trace(e);
    response.setError(e.getMessage());
  }
```

---

### Custom moveUp/moveDown Methods

**Issue Pattern**: Manual implementation of grid reordering

**Solution Template**:
```
1. Remove custom move methods from controller {FileName}:{line}
2. Open the corresponding grid view XML
3. Add canMove="true" attribute to <grid> element
4. Add sequence field to domain if not present
5. Remove action-method references to move methods from view

Example:
  Grid XML:
    <grid name="product-grid" title="Products"
          model="com.axelor.apps.Product"
          canMove="true">
      ...
    </grid>
```

---

## Low Priority Issues

### Missing JavaDoc

**Issue Pattern**: Public methods without documentation

**Solution Template**:
```
1. Add JavaDoc comment above method at {FileName}:{line}
2. Use /** */ style
3. Include @param for each parameter
4. Include @return for return value
5. Include @throws for declared exceptions

Example:
  /**
   * Calculates the total amount for all orders of a customer.
   *
   * @param customer the customer whose orders to calculate
   * @return the total amount of all orders
   * @throws IllegalArgumentException if customer is null
   */
  public BigDecimal calculateCustomerTotal(Customer customer) {
    ...
  }
```

---

### Naming Convention Violations

**Issue Pattern**: Class, method, or variable names not following conventions

**Solution Template**:
```
1. Identify naming violation in {FileName}:{line}
2. Rename using appropriate convention:
   - Classes: PascalCase (CustomerService, OrderRepository)
   - Methods: camelCase (calculateTotal, findByName)
   - Constants: UPPER_SNAKE_CASE (STATUS_DRAFT, MAX_ITEMS)
   - Variables: camelCase (customerList, totalAmount)
3. Use IDE refactoring (Rename) to update all references
4. Verify no compilation errors after rename

Specific conventions:
- Service interfaces: {Entity}Service
- Service implementations: {Entity}ServiceImpl
- Repositories: {Entity}Repository
- Controllers: {Entity}Controller
```

---

## Usage Guidelines

### For Fix Specification Generator

1. Match issue description to template above
2. Copy template text
3. Replace {FileName}, {line}, {methodName}, {ClassName} with actual values
4. Include example code transformation when applicable
5. Add verification steps at the end

### For Developers

1. Read the full solution template
2. Follow steps in order
3. Pay attention to verification steps
4. Review common pitfalls section
5. Test thoroughly after applying fix

---

## Maintenance

When adding new solution templates:
1. Use numbered steps for clarity
2. Include before/after code examples
3. Add verification steps
4. Document common pitfalls
5. Reference relevant pattern documentation
6. Keep solutions actionable and specific
