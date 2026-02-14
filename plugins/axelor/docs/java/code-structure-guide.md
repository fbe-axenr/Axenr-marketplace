# Code Structure and Conventions

This guide provides comprehensive information about code structure, package organization, and conventions for Axelor Java development.

## Code Structure and Conventions

### Package Organization

**Note**: The `db/` package is **optional**. Axelor auto-generates entity classes and repositories from XML domain files during `./gradlew generateCode`:
- Generated entities go to `build/src-gen/.../db/[Entity].java`
- Generated repositories go to `build/src-gen/.../db/repo/[Entity]Repository.java`

Only create `db/repo/` in your source if you need **custom repositories** with additional query methods or computed fields (double-save pattern). Custom repositories extend the generated ones, NOT JpaRepository directly.

```
com.axelor.apps.[module]/
├── db/                                    # (optional) Custom data access layer
│   └── repo/                              # Custom repositories ONLY (extends generated)
│       └── [Entity]Repo.java              # Extends auto-generated [Entity]Repository
├── service/
│   ├── [Entity]Service.java (interface)
│   └── impl/
│       └── [Entity]ServiceImpl.java
├── web/
│   └── [Entity]Controller.java
├── exception/
│   └── [Module]ExceptionMessage.java
└── module/
    └── [Module]Module.java
```

### Naming Conventions

**Classes:**
- Service interface: `[Entity]Service`
- Service implementation: `[Entity]ServiceImpl`
- Generated repository: `[Entity]Repository` (auto-generated in build/src-gen/)
- Custom repository: `[Entity]Repo` (extends generated [Entity]Repository)
- Controller: `[Entity]Controller`
- Exception messages: `[Module]ExceptionMessage`

**Methods:**
- Services: `create`, `update`, `validate`, `compute`, `check[Condition]`, `find[Criteria]`
- Repositories: `findBy[Field]`, `countBy[Field]`, `existsBy[Field]`
- Controllers: `methodName` (camelCase), `onChange[Field]`, `set[Attribute]`

**Variables:**
- Entity instances: `[entity]` (camelCase of entity name)
- Collections: `[entity]List`, `[entity]Set`
- Repository instances: `[entity]Repository`
- Service instances: `[entity]Service`

### Import Organization

**Order:**
1. Java standard library (`java.*`, `javax.*`)
2. Third-party libraries
3. Axelor framework (`com.axelor.*`)
4. Application packages (`com.axelor.apps.*`)
5. Current module packages

**Example:**
```java
// Java standard
import java.math.BigDecimal;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;
import javax.persistence.EntityManager;

// Third-party
import com.google.inject.Inject;
import com.google.inject.Singleton;
import com.google.inject.persist.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

// Axelor framework
import com.axelor.db.JpaRepository;
import com.axelor.db.Query;
import com.axelor.exception.AxelorException;
import com.axelor.exception.db.repo.TraceBackRepository;
import com.axelor.i18n.I18n;
import com.axelor.inject.Beans;
import com.axelor.rpc.ActionRequest;
import com.axelor.rpc.ActionResponse;

// Application
import com.axelor.apps.base.service.app.AppBaseService;

// Current module
import com.axelor.apps.[module].db.[Entity];
import com.axelor.apps.[module].db.repo.[Entity]Repository;
import com.axelor.apps.[module].service.[Entity]Service;
```

### JavaDoc Standards

**Service Interface:**
```java
/**
 * Service interface for managing [Entity] operations.
 * Provides CRUD operations and business logic for [Entity].
 *
 * @author [Author]
 * @version 1.0
 */
public interface [Entity]Service {

  /**
   * Creates a new [entity] with validation and default values.
   *
   * @param [entity] the entity to create
   * @return the created and persisted entity
   * @throws AxelorException if validation fails or business rules are violated
   */
  [Entity] create([Entity] [entity]) throws AxelorException;
}
```

**Service Implementation:**
```java
/**
 * Implementation of [Entity]Service.
 * Handles business logic, validation, and persistence for [Entity].
 */
public class [Entity]ServiceImpl implements [Entity]Service {

  /**
   * Creates a new [entity] with complete validation and computed fields.
   * Sets default values, validates business rules, and persists to database.
   *
   * @param [entity] the entity to create
   * @return the created entity with all computed fields set
   * @throws AxelorException if required fields are missing or business rules fail
   */
  @Override
  @Transactional(rollbackOn = {Exception.class})
  public [Entity] create([Entity] [entity]) throws AxelorException {
    // Implementation
  }
}
```

### Exception Handling Patterns

**Service Layer:**
```java
// Business rule violation
throw new AxelorException(
    TraceBackRepository.CATEGORY_INCONSISTENCY,
    I18n.get([Module]ExceptionMessage.BUSINES_RULE_VIOLATED),
    details);

// Missing required field
throw new AxelorException(
    TraceBackRepository.CATEGORY_MISSING_FIELD,
    I18n.get([Module]ExceptionMessage.MISSING_REQUIRED_FIELD),
    fieldName);

// Configuration error
throw new AxelorException(
    TraceBackRepository.CATEGORY_CONFIGURATION_ERROR,
    I18n.get([Module]ExceptionMessage.CONFIGURATION_ERROR),
    error);

// No unique key
throw new AxelorException(
    TraceBackRepository.CATEGORY_NO_UNIQUE_KEY,
    I18n.get([Module]ExceptionMessage.DEUPLICATE_RECORD));

// No value
throw new AxelorException(
    TraceBackRepository.CATEGORY_NO_VALUE,
    I18n.get([Module]ExceptionMessage.NO_VALUE_FOUND),
    field);
```

**Controller Layer:**
```java
// Standard error handling
try {
  // Controller logic
} catch (Exception e) {
  TraceBackService.trace(response, e);
}

// Specific error handling
try {
  // Controller logic
} catch (AxelorException e) {
  TraceBackService.trace(response, e);
  response.setError(e.getMessage());
} catch (Exception e) {
  TraceBackService.trace(response, e);
  response.setError(I18n.get([Module]ExceptionMessage.UNEXPECTED_ERROR));
}
```

### Dependency Injection Patterns

**Constructor Injection (Preferred):**
```java
@Inject
public [Entity]ServiceImpl(
    [Entity]Repository [entity]Repository,
    AppBaseService appBaseService,
    [Related]Service [related]Service) {
  this.[entity]Repository = [entity]Repository;
  this.appBaseService = appBaseService;
  this.[related]Service = [related]Service;
}
```

**Beans.get() for Optional Dependencies:**
```java
// Get service on-demand
AppBaseService appBaseService = Beans.get(AppBaseService.class);

// Avoid circular dependencies
[Related]Service [related]Service = Beans.get([Related]Service.class);
```
