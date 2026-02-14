# Axelor Module Generation Workflow

## Overview

This guide provides the detailed workflow for generating complete Axelor modules including build configuration, Module.java, Services, Repositories, and Controllers.

**Reference by:** java-agent agent

---

## Generation Order (CRITICAL)

**MANDATORY ORDER:**
1. **build.gradle** - FIRST
2. **Module.java** - SECOND
3. **Services** - Interface + Implementation + Binding
4. **Repositories** - Only custom ones + Binding
5. **Controllers** - No binding needed

---

## Step 1: Generate build.gradle

### Location

Module root directory: `modules/[module-name]/build.gradle`

### Template

```gradle
plugins {
    id 'com.axelor.app'
}

axelor {
    title = "[Module Display Name]"
}

dependencies {
    implementation project(':axelor-base')
    // Add other dependencies
}
```

### Rules

- **Plugin:** MUST be `com.axelor.app` (NEVER `java-library`)
- **Title:** From architecture specification
- **Dependencies:** From architecture plan
- **NO Java version** in module build.gradle

### Reference

See **@docs/gradle/module-build-gradle-guide.md** for complete guide

---

## Step 2: Generate Module.java

### Location

`src/main/java/com/axelor/apps/{module}/module/{Module}Module.java`

### Template

```java
package com.axelor.apps.{module}.module;

import com.axelor.app.AxelorModule;

/**
 * Module configuration for {Module}
 */
public class {Module}Module extends AxelorModule {

    @Override
    protected void configure() {
        // Service bindings will be added here
        // Repository bindings will be added here
    }
}
```

### Example: Sales Module

```java
package com.axelor.apps.sales.module;

import com.axelor.app.AxelorModule;

/**
 * Module configuration for Sales
 */
public class SalesModule extends AxelorModule {

    @Override
    protected void configure() {
        // Service bindings will be added here
        // Repository bindings will be added here
    }
}
```

### Rules

- **Naming:** PascalCase - `SalesModule`, `ProjectModule`
- **Package:** Always `com.axelor.apps.{module}.module`
- **Created:** ONCE before any implementations
- **Updated:** Incrementally after each service/repository

### Reference

See **@docs/java/axelor-specific-patterns.md** for Module.java patterns

---

## Step 3: Generate Services

### 3.1 Service Interface

**Location:** `src/main/java/com/axelor/apps/{module}/service/`

**Example:**

```java
package com.axelor.apps.sales.service;

import com.axelor.apps.sales.db.Order;
import com.axelor.exception.AxelorException;
import java.math.BigDecimal;

public interface OrderService {

    /**
     * Validate the order and change status to VALIDATED.
     *
     * @param order the order to validate
     * @throws AxelorException if validation fails
     */
    void validate(Order order) throws AxelorException;

    /**
     * Compute total amount from line items.
     *
     * @param order the order to compute
     * @return the computed total
     */
    BigDecimal computeTotal(Order order);
}
```

### 3.2 Service Implementation

**Location:** `src/main/java/com/axelor/apps/{module}/service/`

**Example:**

```java
package com.axelor.apps.sales.service;

import com.axelor.apps.sales.db.Order;
import com.axelor.apps.sales.db.repo.OrderRepository;
import com.axelor.exception.AxelorException;
import com.google.inject.Inject;
import com.google.inject.persist.Transactional;
import java.lang.invoke.MethodHandles;
import java.math.BigDecimal;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class OrderServiceImpl implements OrderService {

    protected static final Logger log =
        LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());

    protected final OrderRepository orderRepository;

    @Inject
    public OrderServiceImpl(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    @Override
    @Transactional(rollbackOn = Exception.class)
    public void validate(Order order) throws AxelorException {
        log.debug("Validating order: {}", order.getOrderNo());

        // Business logic here
        order.setStatusSelect(2); // VALIDATED
        orderRepository.save(order);
    }

    @Override
    public BigDecimal computeTotal(Order order) {
        return order.getOrderLineList().stream()
            .map(line -> line.getTotal())
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

### 3.3 Update Module.java with Service Binding

**CRITICAL:** After creating interface + implementation, IMMEDIATELY update Module.java

**Steps:**

1. Read Module.java
2. Add imports:
   ```java
   import com.axelor.apps.sales.service.OrderService;
   import com.axelor.apps.sales.service.OrderServiceImpl;
   ```
3. Add binding in `configure()`:
   ```java
   bind(OrderService.class).to(OrderServiceImpl.class);
   ```

**Module.java after binding:**

```java
package com.axelor.apps.sales.module;

import com.axelor.app.AxelorModule;
import com.axelor.apps.sales.service.OrderService;
import com.axelor.apps.sales.service.OrderServiceImpl;

public class SalesModule extends AxelorModule {

    @Override
    protected void configure() {
        // Service bindings
        bind(OrderService.class).to(OrderServiceImpl.class);
    }
}
```

### Service Generation Rules

- Use SLF4J Logger with MethodHandles
- Use `@Transactional(rollbackOn = Exception.class)` for write operations
- Use `@Inject` constructor injection
- Use Optional chaining for null safety
- Delegate complex logic to helper classes
- English JavaDoc, no emoji

### Reference

See **@docs/java/service-patterns.md** and **@docs/java/generation-templates.md**

---

## Step 4: Generate Repositories (Only When Needed)

### 4.1 When to Create Custom Repository

**Axelor auto-generates** `[Entity]Repository` classes. Only create custom if you need:
- Custom query methods beyond CRUD
- Computed fields (double-save pattern)
- Complex business logic in data access

### 4.2 Custom Repository

**Location:** `src/main/java/com/axelor/apps/{module}/db/repo/`

**Naming:** `[Entity]Repo` (NOT `[Entity]ManagementRepository`)

**Example:**

```java
package com.axelor.apps.sales.db.repo;

import com.axelor.apps.sales.db.Order;
import com.axelor.apps.sales.service.OrderService;
import com.google.inject.Inject;
import javax.persistence.PersistenceException;

public class OrderRepo extends OrderRepository {

    protected final OrderService orderService;

    @Inject
    public OrderRepo(OrderService orderService) {
        this.orderService = orderService;
    }

    @Override
    public Order save(Order order) {
        try {
            // Compute total before save (double-save pattern)
            order.setTotal(orderService.computeTotal(order));

            // First save
            order = super.save(order);

            // Additional logic after save
            // Second save if needed
            return super.save(order);

        } catch (Exception e) {
            throw new PersistenceException(e);
        }
    }

    @Override
    public void remove(Order order) {
        // Cleanup logic before removal
        super.remove(order);
    }
}
```

### 4.3 Update Module.java with Repository Binding

**CRITICAL:** After creating custom repository, IMMEDIATELY update Module.java

**Steps:**

1. Read Module.java
2. Add imports:
   ```java
   import com.axelor.apps.sales.db.repo.OrderRepository;
   import com.axelor.apps.sales.db.repo.OrderRepo;
   ```
3. Add binding in `configure()`:
   ```java
   bind(OrderRepository.class).to(OrderRepo.class);
   ```

**Module.java after repository binding:**

```java
package com.axelor.apps.sales.module;

import com.axelor.app.AxelorModule;
import com.axelor.apps.sales.db.repo.OrderRepository;
import com.axelor.apps.sales.db.repo.OrderRepo;
import com.axelor.apps.sales.service.OrderService;
import com.axelor.apps.sales.service.OrderServiceImpl;

public class SalesModule extends AxelorModule {

    @Override
    protected void configure() {
        // Service bindings
        bind(OrderService.class).to(OrderServiceImpl.class);

        // Repository bindings
        bind(OrderRepository.class).to(OrderRepo.class);
    }
}
```

### Repository Generation Rules

- Extend generated `[Entity]Repository` (NOT JpaRepository)
- Use `@Inject` constructor injection
- Override save() for computed fields (double-save)
- Override remove() for cleanup logic
- Call services for business logic
- Use pagination for large datasets

### Reference

See **@docs/java/repository-patterns.md** and **@docs/java/generation-templates.md**

---

## Step 5: Generate Controllers

### 5.1 Controller Structure

**Location:** `src/main/java/com/axelor/apps/{module}/web/`

**Example:**

```java
package com.axelor.apps.sales.web;

import com.axelor.apps.sales.db.Order;
import com.axelor.apps.sales.db.repo.OrderRepository;
import com.axelor.apps.sales.service.OrderService;
import com.axelor.exception.service.TraceBackService;
import com.axelor.inject.Beans;
import com.axelor.rpc.ActionRequest;
import com.axelor.rpc.ActionResponse;

public class OrderController {

    // NO @Inject in controllers - use Beans.get() instead

    /**
     * Action method to validate the order.
     * Called from UI button action.
     */
    public void validate(ActionRequest request, ActionResponse response) {
        try {
            Order order = request.getContext().asType(Order.class);
            order = Beans.get(OrderRepository.class).find(order.getId());

            Beans.get(OrderService.class).validate(order);

            response.setReload(true);
            response.setFlash("Order validated successfully");

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    /**
     * Action method to compute total.
     * Called from UI onChange event.
     */
    public void computeTotal(ActionRequest request, ActionResponse response) {
        try {
            Order order = request.getContext().asType(Order.class);

            BigDecimal total = Beans.get(OrderService.class).computeTotal(order);

            response.setValue("total", total);

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }

    /**
     * Set default values for new record.
     */
    public void setDefaults(ActionRequest request, ActionResponse response) {
        try {
            response.setValue("orderDate", LocalDate.now());
            response.setValue("statusSelect", 1); // Draft

        } catch (Exception e) {
            TraceBackService.trace(response, e);
        }
    }
}
```

### 5.2 Controller Generation Rules

- **NO Module.java binding needed** - Controllers are directly instantiated
- **NO @Inject in controllers** - Use `Beans.get()` to access services and repositories
- **NO constructor injection** - Controllers are NOT managed by dependency injection
- All methods: `(ActionRequest request, ActionResponse response)`
- Extract entities with `asType()` or `get()`
- Fetch managed entities from repository using `Beans.get(Repository.class).find()`
- Delegate business logic to services using `Beans.get(Service.class)`
- Set response values: `setReload()`, `setFlash()`, `setValue()`
- Handle errors with `TraceBackService.trace()`

### Controller Method Patterns

**Validation/Action buttons:**
```java
public void validate(ActionRequest request, ActionResponse response) {
    try {
        Entity entity = request.getContext().asType(Entity.class);
        entity = Beans.get(EntityRepository.class).find(entity.getId());

        Beans.get(EntityService.class).validate(entity);

        response.setReload(true);
        response.setFlash("Success message");
    } catch (Exception e) {
        TraceBackService.trace(response, e);
    }
}
```

**onChange handlers:**
```java
public void computeField(ActionRequest request, ActionResponse response) {
    try {
        Entity entity = request.getContext().asType(Entity.class);

        Result result = Beans.get(EntityService.class).compute(entity);

        response.setValue("fieldName", result);
    } catch (Exception e) {
        TraceBackService.trace(response, e);
    }
}
```

**Default values:**
```java
public void setDefaults(ActionRequest request, ActionResponse response) {
    try {
        response.setValue("field1", defaultValue1);
        response.setValue("field2", defaultValue2);
    } catch (Exception e) {
        TraceBackService.trace(response, e);
    }
}
```

### Reference

See **@docs/java/controller-patterns.md** and **@docs/java/generation-templates.md**

---

## Complete Module.java Example

After generating all components, Module.java should look like:

```java
package com.axelor.apps.sales.module;

import com.axelor.app.AxelorModule;
import com.axelor.apps.sales.db.repo.OrderRepository;
import com.axelor.apps.sales.db.repo.OrderRepo;
import com.axelor.apps.sales.db.repo.OrderLineRepository;
import com.axelor.apps.sales.db.repo.OrderLineRepo;
import com.axelor.apps.sales.service.OrderService;
import com.axelor.apps.sales.service.OrderServiceImpl;
import com.axelor.apps.sales.service.OrderLineService;
import com.axelor.apps.sales.service.OrderLineServiceImpl;

/**
 * Module configuration for Sales
 */
public class SalesModule extends AxelorModule {

    @Override
    protected void configure() {
        // Service bindings (alphabetically)
        bind(OrderService.class).to(OrderServiceImpl.class);
        bind(OrderLineService.class).to(OrderLineServiceImpl.class);

        // Repository bindings (alphabetically)
        bind(OrderRepository.class).to(OrderRepo.class);
        bind(OrderLineRepository.class).to(OrderLineRepo.class);
    }
}
```

### Module.java Rules

- **Order imports:** AxelorModule, repositories, services
- **Group bindings:** Services first, then Repositories
- **Alphabetical:** Within each group
- **No controllers:** Controllers don't need bindings

---

## Binding Update Process (Summary)

### For Each Service

1. Create interface in `.service` package
2. Create implementation in `.service` package
3. **IMMEDIATELY** update Module.java:
   - Add imports
   - Add `bind(Service.class).to(ServiceImpl.class);`

### For Each Custom Repository

1. Create `[Entity]Repo` in `.db.repo` package
2. Extend generated `[Entity]Repository`
3. **IMMEDIATELY** update Module.java:
   - Add imports
   - Add `bind(EntityRepository.class).to(EntityRepo.class);`

### For Controllers

- **NO binding needed**
- Just create in `.web` package

---

## Generation Checklist

Before considering generation complete:

### Module Configuration
- [ ] build.gradle created FIRST with `com.axelor.app` plugin
- [ ] Module.java created SECOND
- [ ] All bindings added to Module.java

### Services
- [ ] Interface created with method signatures
- [ ] Implementation uses @Inject constructor
- [ ] Implementation uses @Transactional for writes
- [ ] SLF4J Logger with MethodHandles
- [ ] Binding added to Module.java

### Repositories
- [ ] Only created when custom logic needed
- [ ] Extends generated repository
- [ ] Uses @Inject constructor
- [ ] save() override for computed fields
- [ ] Binding added to Module.java

### Controllers
- [ ] Created in .web package
- [ ] All methods have (ActionRequest, ActionResponse)
- [ ] Delegates to services
- [ ] Uses TraceBackService for errors
- [ ] NO binding in Module.java

### Code Quality
- [ ] NO EMOJI anywhere
- [ ] ENGLISH ONLY
- [ ] Proper naming conventions
- [ ] Organized imports
- [ ] JavaDoc for public methods

---

## Troubleshooting

### Error: "No implementation was bound"

**Cause:** Missing binding in Module.java

**Fix:** Add `bind(Service.class).to(ServiceImpl.class);`

### Error: "Duplicate binding"

**Cause:** Binding added twice in Module.java

**Fix:** Remove duplicate binding

### Error: "Cannot inject repository"

**Cause:** Custom repository not bound in Module.java

**Fix:** Add `bind(EntityRepository.class).to(EntityRepo.class);`

---

## Summary

**CRITICAL WORKFLOW:**
1. build.gradle FIRST
2. Module.java SECOND
3. For each service: Interface → Implementation → Binding
4. For each custom repo: Repo → Binding
5. For each controller: Just create (no binding)

**GOLDEN RULE:** Update Module.java IMMEDIATELY after creating each service/repository!
