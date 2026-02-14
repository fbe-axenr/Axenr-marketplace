# Test Patterns for Axelor Services

## Overview

Patterns and best practices for unit testing **service public methods** (business logic core). Focus on services to maximize value and maintainability.

## Test Structure

**Directory layout:**
```
axelor-sale/src/
├── main/java/com/axelor/apps/sale/service/
│   ├── CustomerService.java
│   └── CustomerServiceImpl.java
└── test/java/com/axelor/apps/sale/service/
    └── CustomerServiceTest.java
```

Package structure mirrors main code. Use JUnit 5.

## Testing Approaches

### BaseTest (Integration - Recommended)

**Provides:** Real DB access, DI, complete Axelor context
**Use for:** Complex interactions, database operations, framework features

```java
import com.axelor.utils.junit.BaseTest;
import com.google.inject.Inject;

public class CustomerServiceTest extends BaseTest {
  protected final CustomerService service;
  protected final CustomerRepository repository;

  @Inject
  public CustomerServiceTest(CustomerService service, CustomerRepository repository) {
    this.service = service;
    this.repository = repository;
  }

  @Test
  void testCreateCustomer() throws AxelorException {
    // Given
    Customer customer = new Customer();
    customer.setFullName("John Doe");

    // When
    Customer result = service.create(customer);

    // Then
    assertNotNull(result.getId());
    assertEquals(CustomerStatus.DRAFT, result.getStatusSelect());
  }
}
```

### Mockito (Unit Testing)

**Use for:** External dependencies, error handling, isolated behavior

```java
@ExtendWith(MockitoExtension.class)
public class OrderServiceTest {
  @Mock protected OrderRepository repository;
  @Mock protected SequenceService sequenceService;
  @InjectMocks protected OrderServiceImpl orderService;

  @Test
  void testGenerateOrderNumber() throws AxelorException {
    Order order = new Order();
    when(sequenceService.getSequenceNumber("order")).thenReturn("ORD-001");

    orderService.generateOrderNumber(order);

    assertEquals("ORD-001", order.getOrderNumber());
    verify(sequenceService).getSequenceNumber("order");
  }
}
```

**Hybrid approach:** BaseTest for integration + Mockito for edge cases. Target >80% coverage.

## Given-When-Then Pattern

Structure tests for clarity:

```java
@Test
void testCreate_validCustomer_success() {
  // Given: Setup
  Customer customer = new Customer();
  customer.setFullName("John Doe");

  // When: Execute
  Customer result = service.create(customer);

  // Then: Verify
  assertNotNull(result.getId());
  assertEquals("John Doe", result.getFullName());
}
```

**Naming:** `test[Method]_[scenario]_[expected]`
- `testCreate_validCustomer_success()`
- `testCreate_nullName_throwsException()`
- `testValidate_draftCustomer_statusChanges()`

## Common Scenarios

**CRUD Operations:**
```java
@Test
void testDelete_draftCustomer_success() throws AxelorException {
  Customer customer = createDraftCustomer();
  Long id = customer.getId();

  service.delete(customer);

  assertNull(repository.find(id));
}
```

**Business Logic:**
```java
@Test
void testCalculateDiscount_vipCustomer_20Percent() {
  Customer customer = createVipCustomer();
  Order order = createOrder(customer, BigDecimal.valueOf(1000));

  BigDecimal discount = orderService.calculateDiscount(order);

  assertEquals(BigDecimal.valueOf(200.00).setScale(2), discount.setScale(2));
}
```

**Exception Testing:**
```java
@Test
void testCreate_nullName_throwsException() {
  Customer customer = new Customer();
  customer.setEmail("test@example.com");

  assertThrows(AxelorException.class, () -> service.create(customer));
}
```

## Helper Methods

Reduce duplication with reusable helpers:

```java
public class CustomerServiceTest extends BaseTest {

  protected Customer createDraftCustomer() {
    Customer customer = new Customer();
    customer.setCode("CUST-TEST-" + System.currentTimeMillis());
    customer.setFullName("Test Customer");
    customer.setStatusSelect(CustomerStatus.DRAFT);
    return repository.save(customer);
  }

  protected Customer createValidatedCustomer() throws AxelorException {
    return service.validate(createDraftCustomer());
  }

  protected Order createDraftOrder() {
    Order order = new Order();
    order.setCustomer(createDraftCustomer());
    order.setOrderDate(LocalDate.now());
    return orderRepository.save(order);
  }
}
```

## Running Tests

```bash
./gradlew test                          # All tests
./gradlew :modules:axelor-studio:test   # Specific module
./gradlew test --tests "ClassName"      # Specific class
./gradlew test --tests "Class.method"   # Specific method
```

## Code Coverage

**Target: >80%**

**Include:** Public service methods, business logic, exceptions, validation
**Exclude:** Getters/setters, simple constructors, logging

```bash
./gradlew test jacocoTestReport
open build/reports/jacoco/test/html/index.html
```

**Priority:**
1. Happy paths (normal operations)
2. Edge cases (boundaries, nulls, empty collections)
3. Error cases (exceptions, validation failures)
4. State transitions
5. Business rules

## Complete Example

```java
package com.axelor.apps.sale.service;

import com.axelor.apps.sale.db.Customer;
import com.axelor.apps.sale.db.repo.CustomerRepository;
import com.axelor.utils.junit.BaseTest;
import com.google.inject.Inject;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CustomerServiceTest extends BaseTest {
  protected final CustomerService service;
  protected final CustomerRepository repository;

  @Inject
  public CustomerServiceTest(CustomerService service, CustomerRepository repository) {
    this.service = service;
    this.repository = repository;
  }

  // CREATE
  @Test
  void testCreate_validCustomer_success() throws AxelorException {
    Customer customer = new Customer();
    customer.setFullName("John Doe");

    Customer result = service.create(customer);

    assertNotNull(result.getId());
    assertEquals(CustomerStatus.DRAFT, result.getStatusSelect());
  }

  @Test
  void testCreate_nullName_throwsException() {
    Customer customer = new Customer();
    assertThrows(AxelorException.class, () -> service.create(customer));
  }

  // VALIDATE
  @Test
  void testValidate_draftCustomer_success() throws AxelorException {
    Customer customer = createDraftCustomer();
    Customer result = service.validate(customer);
    assertEquals(CustomerStatus.VALIDATED, result.getStatusSelect());
  }

  // DELETE
  @Test
  void testDelete_draftCustomer_success() throws AxelorException {
    Customer customer = createDraftCustomer();
    Long id = customer.getId();
    service.delete(customer);
    assertNull(repository.find(id));
  }

  // HELPERS
  @Transactional
  protected Customer createDraftCustomer() {
    Customer customer = new Customer();
    customer.setCode("CUST-" + System.currentTimeMillis());
    customer.setFullName("Test");
    customer.setStatusSelect(CustomerStatus.DRAFT);
    return repository.save(customer);
  }
}
```

## Best Practices

**DO:**
- Test services only (business logic)
- Use Given-When-Then structure
- Use descriptive names: `method_scenario_expected`
- Test happy paths AND edge cases
- Use helper methods for test data
- Aim for >80% coverage
- Use BaseTest for integration tests

**DON'T:**
- Test repositories/controllers (thin wrappers)
- Test getters/setters
- Use vague test names
- Mix test scenarios
- Ignore edge cases or exceptions
- Duplicate test data creation
- Aim for 100% coverage (diminishing returns)

## References

**Internal:** [Service Patterns](service-patterns.md) | [Code Style](code-style-rules.md) | [Test Config](test-configuration-guide.md)
**External:** [JUnit 5](https://junit.org/junit5/docs/current/user-guide/) | [Mockito](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html) | [Axelor Docs](https://docs.axelor.com/)

