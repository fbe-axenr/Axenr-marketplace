# Axelor Development Conventions

## Naming Conventions

### Entities (Domains)

```
✅ CORRECT                  ❌ INCORRECT
Customer                    customer (lowercase)
SaleOrder                   saleorder (not camelCase)
ProductCategory             product_category (underscore)
```

- **PascalCase**: First letter capitalized, no underscore
- **Singular name**: `Customer`, not `Customers`
- **Explicit**: Name understandable without context

### Fields

```
✅ CORRECT                  ❌ INCORRECT
fullName                    full_name (underscore)
orderDate                   OrderDate (starts with capital)
totalAmount                 amt (obscure abbreviation)
```

- **camelCase**: First letter lowercase
- **No underscore**: Except for generated technical fields
- **Explicit name**: No ambiguous abbreviations

### Standard Technical Fields

Axelor automatically generates certain fields if you inherit from `AuditableModel`:

```xml
<entity name="Customer">
  <string name="code" />
  <!-- Auto-generated fields if extends AuditableModel: -->
  <!-- createdOn (LocalDateTime) -->
  <!-- createdBy (User) -->
  <!-- updatedOn (LocalDateTime) -->
  <!-- updatedBy (User) -->
  <!-- version (Integer) - optimistic locking -->
  <!-- archived (Boolean) - soft delete -->
</entity>
```

### Relationships

```
✅ CORRECT                  ❌ INCORRECT
customer                    customerId (no Id suffix)
company                     companyRef (no suffix)
orderLines                  orders (plural for collection)
```

- **Singular** for `many-to-one`: `customer`, `company`
- **Plural** for `one-to-many` and `many-to-many`: `orderLines`, `products`
- **No suffix**: No `Id`, `Ref`, etc.

### Java Packages

```
com/axelor/apps/[module]/
├── db/
│   └── repo/              # Repositories
├── service/               # Services
├── web/                   # Controllers
└── exception/             # Exceptions

✅ CORRECT
com.axelor.apps.mymodule.service.CustomerService
com.axelor.apps.mymodule.db.repo.CustomerRepository

❌ INCORRECT
com.axelor.apps.mymodule.services.CustomerService (services plural)
com.axelor.mymodule.CustomerService (missing apps/)
```

### Java Classes

```
✅ CORRECT                          ❌ INCORRECT
CustomerService (interface)         CustomerServiceInterface
CustomerServiceImpl (implem)        CustomerServiceImplementation
CustomerController                  CustomerCtrl (abbreviation)
```

### Repository Naming Convention (CRITICAL)

Axelor uses a **two-tier repository pattern**:

| Type | Name Pattern | Location | Created By |
|------|--------------|----------|------------|
| **Auto-generated** | `*Repository.java` | `build/src-gen/.../db/repo/` | `./gradlew generateCode` |
| **Custom** | `*Repo.java` | `src/main/java/.../db/repo/` | Developer (if needed) |

**NEVER create `*Repository.java` in source code** - this name is reserved for auto-generated files.

```
✅ CORRECT
build/src-gen/.../repo/[ENTITY]Repository.java   ← Auto-generated
src/main/java/.../db/repo/[ENTITY]Repo.java         ← Custom (extends Repository)

❌ WRONG
src/main/java/.../db/repo/[ENTITY]Repository.java   ← CONFLICT with auto-generated!
```

**Custom repository example:**
```java
// Custom repository extending the AUTO-GENERATED CustomerRepository
public class CustomerRepo extends CustomerRepository {

    @Override
    public Customer save(Customer entity) {
        // Custom save logic (computed fields, validation)
        Customer customer = super.save(entity);
        customer.setFullName(computeFullName(customer));
        return JPA.save(customer);
    }

    // Custom query methods
    public List<Customer> findByCompany(Company company) {
        return all()
            .filter("self.company = :company")
            .bind("company", company)
            .fetch();
    }
}
```

**When to create a custom `*Repo.java`:**
- Override `save()` for computed/derived fields (double-save pattern)
- Override `remove()` for cleanup logic
- Add custom query methods (findBy*, countBy*, etc.)
- Add complex JPQL queries

**When NOT to create a custom repository:**
- Basic CRUD operations (already in auto-generated repository)
- Simple queries (use service layer with injected auto-generated repository)

### XML Files

```
✅ CORRECT                  ❌ INCORRECT
domains/Customer.xml        domains/customer.xml (lowercase)
views/Customer.xml          views/CustomerViews.xml (suffix)
```

- **PascalCase**: Same name as entity
- **One file per entity**: For domains
- **Can group**: Views (form + grid in same file)

## Structure Conventions

### XML Domains

```xml
<domain-models xmlns="http://axelor.com/xml/ns/domain-models"
               xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <module name="axelor-mymodule" package="com.axelor.apps.mymodule.db"/>

  <!-- One entity per file (recommended) -->
  <entity name="Customer">

    <!-- 1. Identifier fields first -->
    <string name="code" required="true" unique="true" max="64"/>
    <string name="fullName" required="true" max="255"/>

    <!-- 2. Business fields -->
    <string name="email" max="255"/>
    <string name="phone" max="32"/>

    <!-- 3. Many-to-one relationships -->
    <many-to-one name="company" ref="Company"/>

    <!-- 4. Calculated / derived fields -->
    <decimal name="totalOrders" scale="2" precision="10"/>

    <!-- 5. One-to-many relationships (at the end) -->
    <one-to-many name="orders" ref="Order" mappedBy="customer"/>

    <!-- Indexes for performance -->
    <index columns="code"/>
    <index columns="company"/>

  </entity>
</domain-models>
```

### XML Views

```xml
<object-views xmlns="http://axelor.com/xml/ns/object-views">

  <!-- 1. Form first -->
  <form name="customer-form" title="Customer"
        model="com.axelor.apps.mymodule.db.Customer">
    <panel name="mainPanel" title="Main Information">
      <field name="code"/>
      <field name="fullName"/>
    </panel>
  </form>

  <!-- 2. Grid next -->
  <grid name="customer-grid" title="Customers"
        model="com.axelor.apps.mymodule.db.Customer">
    <field name="code"/>
    <field name="fullName"/>
  </grid>

  <!-- 3. Actions -->
  <action-view name="action-customer-view" title="Customers"
               model="com.axelor.apps.mymodule.db.Customer">
    <view type="grid" name="customer-grid"/>
    <view type="form" name="customer-form"/>
  </action-view>

</object-views>
```

### Java Services

```java
// Interface
package com.axelor.apps.mymodule.service;

public interface CustomerService {
  Customer create(Customer customer) throws AxelorException;
  Customer update(Customer customer) throws AxelorException;
  void delete(Customer customer) throws AxelorException;
}

// Implementation
package com.axelor.apps.mymodule.service;

public class CustomerServiceImpl implements CustomerService {

  private final CustomerRepository customerRepository;

  @Inject
  public CustomerServiceImpl(CustomerRepository customerRepository) {
    this.customerRepository = customerRepository;
  }

  @Override
  @Transactional(rollbackOn = {AxelorException.class})
  public Customer create(Customer customer) throws AxelorException {
    validate(customer);
    return customerRepository.save(customer);
  }

  protected void validate(Customer customer) throws AxelorException {
    // Business validation
  }
}
```

## Data Conventions

### Selections (enumerations)

Define in XML domain:

```xml
<entity name="Order">
  <integer name="status" selection="order.status.select" default="1"/>
</entity>

<!-- In same file or separate selections.xml file -->
<selection name="order.status.select">
  <option value="1">Draft</option>
  <option value="2">Confirmed</option>
  <option value="3">Completed</option>
  <option value="4">Canceled</option>
</selection>
```

Conventions:
- **Name**: `[entity].[field].select`
- **Values**: Positive integers (1, 2, 3...)
- **Labels**: In English by default, translations in i18n/

### Statuses and Workflows

Standard pattern for entities with lifecycle:

```xml
<entity name="Order">
  <!-- Integer status with selection -->
  <integer name="statusSelect" selection="order.status.select" default="1"/>

  <!-- Transition dates (optional) -->
  <datetime name="confirmedDate"/>
  <datetime name="completedDate"/>
</entity>

<selection name="order.status.select">
  <option value="1">Draft</option>        <!-- Initial state -->
  <option value="2">Confirmed</option>    <!-- In progress -->
  <option value="3">Completed</option>    <!-- Final state -->
  <option value="4">Canceled</option>     <!-- Alternative final state -->
</selection>
```

Transitions in service:

```java
public Order confirm(Order order) throws AxelorException {
  if (order.getStatusSelect() != OrderStatus.DRAFT) {
    throw new AxelorException("Can only confirm draft orders");
  }
  order.setStatusSelect(OrderStatus.CONFIRMED);
  order.setConfirmedDate(LocalDateTime.now());
  return orderRepository.save(order);
}
```

## Java Code Conventions

### Element Order in a Class

```java
public class CustomerServiceImpl implements CustomerService {

  // 1. Constants
  private static final String DEFAULT_PREFIX = "CUST-";

  // 2. Dependency injections (final fields - use constructor injection)
  private final CustomerRepository customerRepository;
  private final CompanyService companyService;

  // 3. Constructor with @Inject
  @Inject
  public CustomerServiceImpl(
      CustomerRepository customerRepository,
      CompanyService companyService) {
    this.customerRepository = customerRepository;
    this.companyService = companyService;
  }

  // 4. Public methods (interface)
  @Override
  @Transactional
  public Customer create(Customer customer) {
    // ...
  }

  @Override
  public Customer find(Long id) {
    // ...
  }

  // 5. Protected methods (helper methods)
  protected void validate(Customer customer) {
    // ...
  }

  protected String generateCode() {
    // ...
  }

  // 6. Private methods (internal logic)
  private boolean isDuplicate(String code) {
    // ...
  }
}
```

### Exception Handling

```java
// ✅ CORRECT: Specific business exception
@Transactional(rollbackOn = {AxelorException.class})
public Customer validate(Customer customer) throws AxelorException {
  if (customer.getCode() == null) {
    throw new AxelorException(
      TraceBackRepository.CATEGORY_MISSING_FIELD,
      I18n.get("Customer code is required")
    );
  }
  // ...
}

// ❌ INCORRECT: Generic exception
public Customer validate(Customer customer) throws Exception {
  if (customer.getCode() == null) {
    throw new Exception("Code required"); // No category, no i18n
  }
}
```

### Logging

```java
public class CustomerServiceImpl implements CustomerService {

  private static final Logger LOG = LoggerFactory.getLogger(
    MethodHandles.lookup().lookupClass()
  );

  public Customer create(Customer customer) {
    LOG.debug("Creating customer: {}", customer.getFullName());

    try {
      Customer saved = customerRepository.save(customer);
      LOG.info("Customer created: code={}, id={}", saved.getCode(), saved.getId());
      return saved;
    } catch (Exception e) {
      LOG.error("Error creating customer", e);
      throw e;
    }
  }
}
```

Levels:
- **TRACE**: Very fine details (rarely used)
- **DEBUG**: Debug information
- **INFO**: Important workflow events
- **WARN**: Abnormal but handled situations
- **ERROR**: Errors requiring attention

## Test Conventions

### Test Structure

```
src/test/java/
└── com/axelor/apps/mymodule/
    ├── service/
    │   ├── CustomerServiceTest.java
    │   └── OrderServiceTest.java
    └── web/
        └── CustomerControllerTest.java
```

### Test Method Naming

```java
public class CustomerServiceTest {

  // Pattern: test_[method]_[scenario]_[expectedResult]

  @Test
  public void test_create_validCustomer_returnsCustomerWithId() {
    // Given
    Customer customer = new Customer();
    customer.setCode("CUST-001");
    customer.setFullName("John Doe");

    // When
    Customer result = customerService.create(customer);

    // Then
    assertNotNull(result.getId());
    assertEquals("CUST-001", result.getCode());
  }

  @Test(expected = AxelorException.class)
  public void test_create_duplicateCode_throwsException() {
    // ...
  }
}
```

## Comment Conventions

### JavaDoc

```java
/**
 * Service for customer management.
 *
 * @author John Doe
 * @since 1.0.0
 */
public class CustomerServiceImpl implements CustomerService {

  /**
   * Creates a new customer with business validation.
   *
   * <p>Performs the following validations:
   * <ul>
   *   <li>Unique code</li>
   *   <li>Valid email (if provided)</li>
   *   <li>Active company (if linked)</li>
   * </ul>
   *
   * @param customer The customer to create
   * @return The created customer with ID
   * @throws AxelorException If validation fails
   */
  @Transactional(rollbackOn = {AxelorException.class})
  public Customer create(Customer customer) throws AxelorException {
    // ...
  }
}
```

### Inline Comments

```java
// ✅ CORRECT: Comment explaining the "why"
// We generate a temporary code because the final code
// depends on manager validation
customer.setCode(generateTemporaryCode());

// ❌ INCORRECT: Comment explaining the "what" (obvious in code)
// Set the code
customer.setCode(code);
```

## Key Conventions Summary

| Element | Convention | Example |
|---------|-----------|---------|
| Entity | PascalCase, singular | `Customer`, `SaleOrder` |
| Field | camelCase | `fullName`, `orderDate` |
| Relationship (1) | camelCase, singular | `customer`, `company` |
| Relationship (N) | camelCase, plural | `orderLines`, `products` |
| Package | lowercase, snake_case | `com.axelor.apps.mymodule` |
| Class | PascalCase | `CustomerService` |
| Interface | No suffix | `CustomerService` |
| Implementation | "Impl" suffix | `CustomerServiceImpl` |
| Method | camelCase, verb | `createCustomer()`, `validate()` |
| Constant | UPPER_SNAKE_CASE | `DEFAULT_STATUS` |
| XML domain file | PascalCase | `Customer.xml` |
| XML view file | PascalCase | `Customer.xml` |
| Test | "Test" suffix | `CustomerServiceTest` |
| Test method | `test_method_scenario_result` | `test_create_valid_success` |

## Resources

- **Java Style Guide**: Google Java Style Guide
- **JPA Conventions**: JPA 2.x specification
- **Hibernate Conventions**: Hibernate naming strategies
