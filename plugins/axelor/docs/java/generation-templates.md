# Code Templates Reference

This guide provides complete code templates for generating Axelor Java components.

## Code Templates Reference

### Module.java Template (GENERATE FIRST)

**CRITICAL:** Module.java must be created BEFORE any service or repository implementations.

**Location:** `src/main/java/com/axelor/apps/{module}/module/{Module}Module.java`

**Initial Template (Empty Module):**

```java
package com.axelor.apps.[module].module;

import com.axelor.app.AxelorModule;

/**
 * Module configuration for [Module]
 */
public class [Module]Module extends AxelorModule {

    @Override
    protected void configure() {
        // Service bindings will be added here
        // Repository bindings will be added here
    }
}
```

**Complete Example (Sales Module with Bindings):**

```java
package com.axelor.apps.sales.module;

import com.axelor.app.AxelorModule;
import com.axelor.apps.sales.db.repo.SaleOrderRepository;
import com.axelor.apps.sales.db.repo.SaleOrderRepo;
import com.axelor.apps.sales.service.SaleOrderLineService;
import com.axelor.apps.sales.service.SaleOrderLineServiceImpl;
import com.axelor.apps.sales.service.SaleOrderService;
import com.axelor.apps.sales.service.SaleOrderServiceImpl;

/**
 * Module configuration for Sales
 */
public class SalesModule extends AxelorModule {

    @Override
    protected void configure() {
        // Service bindings
        bind(SaleOrderService.class).to(SaleOrderServiceImpl.class);
        bind(SaleOrderLineService.class).to(SaleOrderLineServiceImpl.class);

        // Repository bindings
        bind(SaleOrderRepository.class).to(SaleOrderRepo.class);
    }
}
```

**Binding Rules:**

1. **Service Binding:**
   ```java
   bind([Entity]Service.class).to([Entity]ServiceImpl.class);
   ```
   - Add after creating service interface and implementation
   - Import both the interface and implementation class

2. **Repository Binding:**
   ```java
   bind([Entity]Repository.class).to([Entity]Repo.class);
   ```
   - Add after creating custom repository
   - Overrides the auto-generated repository
   - Import both the generated repository and custom repo

3. **NO Controller Bindings:**
   - Controllers are NOT added to Module.java
   - They are instantiated directly by Axelor's action framework

**Import Organization:**
- `com.axelor.app.AxelorModule` first
- Service interfaces and implementations (alphabetically)
- Repository classes (alphabetically)

**Binding Organization:**
- Group service bindings together (alphabetically)
- Group repository bindings together (alphabetically)
- Add comment headers: `// Service bindings` and `// Repository bindings`

### Complete Service Template

```java
package com.axelor.apps.[module].service;

import com.axelor.apps.[module].db.[Entity];
import com.axelor.exception.AxelorException;
import java.util.List;

public interface [Entity]Service {

  [Entity] create([Entity] [entity]) throws AxelorException;

  [Entity] update([Entity] [entity]) throws AxelorException;

  void validate([Entity] [entity]) throws AxelorException;

  [Entity] compute([Entity] [entity]);

  [Entity] confirm([Entity] [entity]) throws AxelorException;

  [Entity] cancel([Entity] [entity]) throws AxelorException;

  boolean canConfirm([Entity] [entity]);

  boolean canCancel([Entity] [entity]);

  List<[Entity]> findByStatus(String status);
}
```

### Complete Service Implementation Template

```java
package com.axelor.apps.[module].service.impl;

import com.axelor.apps.[module].db.[Entity];
import com.axelor.apps.[module].db.repo.[Entity]Repository;
import com.axelor.apps.[module].service.[Entity]Service;
import com.axelor.apps.base.service.app.AppBaseService;
import com.axelor.auth.AuthUtils;
import com.axelor.exception.AxelorException;
import com.axelor.exception.db.repo.TraceBackRepository;
import com.axelor.i18n.I18n;
import com.google.inject.Inject;
import com.google.inject.persist.Transactional;
import java.lang.invoke.MethodHandles;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class [Entity]ServiceImpl implements [Entity]Service {

  private static final Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());

  protected [Entity]Repository [entity]Repository;
  protected AppBaseService appBaseService;

  @Inject
  public [Entity]ServiceImpl(
      [Entity]Repository [entity]Repository,
      AppBaseService appBaseService) {
    this.[entity]Repository = [entity]Repository;
    this.appBaseService = appBaseService;
  }

  @Override
  @Transactional(rollbackOn = {Exception.class})
  public [Entity] create([Entity] [entity]) throws AxelorException {
    LOG.debug("Creating [entity]: {}", [entity]);
    validate([entity]);
    compute([entity]);
    [entity] = [entity]Repository.save([entity]);
    LOG.info("Created [entity] with id: {}", [entity].getId());
    return [entity];
  }

  @Override
  @Transactional(rollbackOn = {Exception.class})
  public [Entity] update([Entity] [entity]) throws AxelorException {
    LOG.debug("Updating [entity]: {}", [entity]);
    validate([entity]);
    compute([entity]);
    [entity] = [entity]Repository.save([entity]);
    LOG.info("Updated [entity] with id: {}", [entity].getId());
    return [entity];
  }

  @Override
  public void validate([Entity] [entity]) throws AxelorException {
    // Validation logic
  }

  @Override
  public [Entity] compute([Entity] [entity]) {
    // Computation logic
    return [entity];
  }

  @Override
  @Transactional(rollbackOn = {Exception.class})
  public [Entity] confirm([Entity] [entity]) throws AxelorException {
    validate([entity]);
    [entity].setStatus("CONFIRMED");
    return [entity]Repository.save([entity]);
  }

  @Override
  @Transactional(rollbackOn = {Exception.class})
  public [Entity] cancel([Entity] [entity]) throws AxelorException {
    [entity].setStatus("CANCELLED");
    return [entity]Repository.save([entity]);
  }

  @Override
  public boolean canConfirm([Entity] [entity]) {
    return [entity] != null && "DRAFT".equals([entity].getStatus());
  }

  @Override
  public boolean canCancel([Entity] [entity]) {
    return [entity] != null && !"CANCELLED".equals([entity].getStatus());
  }

  @Override
  public List<[Entity]> findByStatus(String status) {
    return [entity]Repository.findByStatus(status);
  }
}
```

### Complete Custom Repository Template

**IMPORTANT:** Axelor auto-generates `[Entity]Repository extends JpaRepository<Entity>` in `build/src-gen/`.
Only create a custom repository when you need additional query methods or computed fields.
Custom repositories extend the GENERATED repository, NOT JpaRepository directly.

```java
package com.axelor.apps.[module].db.repo;

import com.axelor.apps.[module].db.[Entity];
import java.util.List;

// Custom repository extending the AUTO-GENERATED [Entity]Repository
public class [Entity]Repo extends [Entity]Repository {

  public [Entity] findByCode(String code) {
    return all()
        .filter("self.code = :code")
        .bind("code", code)
        .fetchOne();
  }

  public List<[Entity]> findByStatus(String status) {
    return all()
        .filter("self.status = :status")
        .bind("status", status)
        .order("-createdOn")
        .fetch();
  }

  public long countByStatus(String status) {
    return all()
        .filter("self.status = :status")
        .bind("status", status)
        .count();
  }
}
```

### Complete Controller Template

```java
package com.axelor.apps.[module].web;

import com.axelor.apps.[module].db.[Entity];
import com.axelor.apps.[module].db.repo.[Entity]Repository;
import com.axelor.apps.[module].service.[Entity]Service;
import com.axelor.exception.service.TraceBackService;
import com.axelor.i18n.I18n;
import com.axelor.rpc.ActionRequest;
import com.axelor.rpc.ActionResponse;
import com.google.inject.Inject;
import com.google.inject.Singleton;

@Singleton
public class [Entity]Controller {


  public void confirm(ActionRequest request, ActionResponse response) {
    try {
      [Entity] [entity] = request.getContext().asType([Entity].class);
      [entity] = Beans.get([entity]Repository.class).find([entity].getId());
      [entity] = Beans.get([entity]Service.class).confirm([entity]);
      response.setReload(true);
      response.setNotify(I18n.get("[Entity] confirmed"));
    } catch (Exception e) {
      TraceBackService.trace(response, e);
    }
  }

  public void cancel(ActionRequest request, ActionResponse response) {
    try {
      [Entity] [entity] = request.getContext().asType([Entity].class);
      [entity] = Beans.get([entity]Repository.class).find([entity].getId());
      [entity] = Beans.get([entity]Service.class).cancel([entity]);
      response.setReload(true);
      response.setFlash(I18n.get("[Entity] cancelled"));
    } catch (Exception e) {
      TraceBackService.trace(response, e);
    }
  }

  public void computeTotals(ActionRequest request, ActionResponse response) {
    try {
      [Entity] [entity] = request.getContext().asType([Entity].class);
      [entity] = Beans.get([entity]Service.class).compute([entity]);
      response.setValue("totalAmount", [entity].getTotalAmount());
    } catch (Exception e) {
      TraceBackService.trace(response, e);
    }
  }
}
```
