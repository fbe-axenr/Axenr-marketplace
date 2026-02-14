# Unit Test Configuration Guide

## Overview

Complete configuration guide for unit tests in Axelor projects based on production examples (reference: axelor-utils addon from Maven Central).

**Note:** axelor-utils is an external addon (`com.axelor.addons:axelor-utils:3.5.0`), not part of core AOP/AOS.

## ⚠️ Quick Version Reference

| Axelor Version | Persistence API | Configuration Location |
|----------------|----------------|------------------------|
| **AOP 7.x+** | JavaX 2.1 (`javax.persistence.*`) | Database in persistence.xml |
| **AOP 8.x+** | Jakarta EE 3.0 (`jakarta.persistence.*`) | Database in axelor-config.properties |

**Check version:** `cat version.txt` in your Axelor directory

## Test Dependencies

**Required:** Two dependencies for testing setup:
1. `com.axelor:axelor-test:${aopVersion}` - JUnit 5, GuiceExtension, JpaSupport
2. `axelor-utils` - BaseTest class for integration testing

### Module build.gradle Template

```gradle
plugins {
    id 'com.axelor.app'
    id 'com.adarshr.test-logger' version '4.0.0'  // Optional
    id 'jacoco'  // Optional
}

dependencies {
    implementation "com.axelor:axelor-test:${aopVersion}"
    implementation project(':axelor-utils')  // or com.axelor.addons:axelor-utils:3.5.0
}

test {
    useJUnitPlatform()
    finalizedBy jacocoTestReport
    maxHeapSize = '1G'
}
```

### What's Included

| Component | Provides | Import |
|-----------|----------|--------|
| axelor-test | JUnit 5, GuiceExtension, JpaSupport | `com.axelor.test.*` |
| axelor-utils | BaseTest integration class | `com.axelor.utils.junit.BaseTest` |

**BaseTest structure** (DO NOT recreate - use from axelor-utils):
```java
@ExtendWith(GuiceExtension.class)
@GuiceModules(JpaTestModule.class)
public abstract class BaseTest extends JpaSupport {
  @AfterAll
  public static void tearDownClass() {
    EntityManagerFactory managerFactory = JPA.em().getEntityManagerFactory();
    if (managerFactory != null) managerFactory.close();
  }
}
```

## Test Framework Setup

### BaseTest Framework (Integration Tests)

**BaseTest** extends `JpaSupport` and provides:
- Real database access (JPA)
- Dependency injection (Guice)
- Complete Axelor application context
- Transaction management with auto-rollback

**Usage example:**

```java
import com.axelor.utils.junit.BaseTest;
import com.google.inject.Inject;

class ResponseMessageComputeServiceTest extends BaseTest {
  protected final ResponseMessageComputeService service;

  @Inject
  public ResponseMessageComputeServiceTest(ResponseMessageComputeService service) {
    this.service = service;
  }

  @Test
  void computeCreateMessage_modelWithNameColumn() {
    Contact contact = new Contact();
    contact.setFirstName("First");
    contact.setLastName("Last");
    assertEquals("The object Contact First Last has been created",
        service.computeCreateMessage(contact));
  }
}
```

**With test data loading:**

```java
class UtilsRestServiceImplTest extends BaseTest {
  protected final UtilsRestService service;
  protected final MetaModelRepository repository;

  @Inject
  UtilsRestServiceImplTest(UtilsRestService service, MetaModelRepository repository) {
    this.service = service;
    this.repository = repository;
  }

  @BeforeAll
  @Transactional
  static void setUp() {
    Beans.get(LoaderHelper.class).importCsv("data/metamodel-input.xml");
  }

  @Test
  void getModel_whenModelExists_shouldReturnModel() {
    MetaModel existing = repository.findByName("MetaModel");
    MetaModel result = service.getModel(existing.getFullName());
    assertNotNull(result);
    assertEquals(existing.getName(), result.getName());
  }
}
```

**Simple utility tests** (no BaseTest needed):

```java
class ListHelperTest {
  @Test
  void testIntersection() {
    List<String> list1 = Arrays.asList("element1", "element2", "element3");
    List<String> list2 = Arrays.asList("element2", "element3", "element4");
    assertEquals(Arrays.asList("element2", "element3"),
        ListHelper.intersection(list1, list2));
  }
}
```

## Test Resources Configuration

### Directory Structure

```
src/test/
├── java/com/axelor/utils/
│   ├── api/ResponseMessageComputeServiceTest.java
│   └── helpers/ControllerCallableHelperTest.java
└── resources/
    ├── META-INF/persistence.xml
    ├── axelor-config.properties
    └── data/test-data.csv
```

### persistence.xml Configuration

**Location:** `src/test/resources/META-INF/persistence.xml`

| Axelor | Persistence API | Namespace |
|--------|----------------|-----------|
| AOS 6.x-8.x | JavaX 2.1 | `javax.persistence.*` |
| AOP 7.x+ | Jakarta EE 3.0 | `jakarta.persistence.*` |

#### JavaX Persistence 2.1 (AOS 6.x - 8.x)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<persistence version="2.1" xmlns="http://xmlns.jcp.org/xml/ns/persistence"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/persistence http://xmlns.jcp.org/xml/ns/persistence/persistence_2_1.xsd">
  <persistence-unit name="testUnit" transaction-type="RESOURCE_LOCAL">
    <provider>org.hibernate.jpa.HibernatePersistenceProvider</provider>
    <exclude-unlisted-classes/>
  </persistence-unit>
</persistence>
```

#### Jakarta EE Persistence 3.0 (AOP 7.x+)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<persistence version="3.0" xmlns="https://jakarta.ee/xml/ns/persistence"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="https://jakarta.ee/xml/ns/persistence https://jakarta.ee/xml/ns/persistence/persistence_3_0.xsd">
  <persistence-unit name="testUnit" transaction-type="RESOURCE_LOCAL">
    <provider>org.hibernate.jpa.HibernatePersistenceProvider</provider>
    <exclude-unlisted-classes/>
  </persistence-unit>
</persistence>
```

**Note:** Database config goes in `axelor-config.properties` for both versions

### axelor-config.properties

**Location:** `src/test/resources/axelor-config.properties`
**Required for:** Jakarta EE 3.0 | **Optional for:** JavaX 2.1

```properties
application.name = Tests
application.mode = dev

# Database (HSQLDB or H2)
db.test.driver = org.hsqldb.jdbc.JDBCDriver
db.test.ddl = create
db.test.url = jdbc:hsqldb:mem:test
db.test.user = sa
db.test.password =

# Optional settings
session.timeout = 60
data.upload.dir = {java.io.tmpdir}/.axelor/test-attachments
data.upload.max-size = 5
quartz.enable = true
quartz.thread-count = 3
```

## Code Coverage (JaCoCo)

```gradle
plugins {
    id 'jacoco'
}

jacoco { toolVersion = '0.8.14' }

test {
    useJUnitPlatform()
    finalizedBy jacocoTestReport
}

jacocoTestReport {
    reports {
        xml.required = true
        html.required = true
    }

    // Exclude generated/config code
    afterEvaluate {
        classDirectories.setFrom(files(classDirectories.files.collect {
            fileTree(dir: it, exclude: ['**/db/**', '**/module/**', '**/web/**'])
        }))
    }
}

jacocoTestCoverageVerification {
    violationRules {
        rule { limit { minimum = 0.80 } }
    }
}
```

**Reports location:** `build/reports/jacoco/test/html/index.html`

## Test Execution

```bash
./gradlew test                                    # All tests
./gradlew :modules:axelor-utils:test              # Specific module
./gradlew test --tests "ClassName"                # Specific class
./gradlew test --tests "ClassName.methodName"     # Specific method
./gradlew test jacocoTestReport                   # With coverage
./gradlew test --continuous                       # Watch mode
```

### Test Configuration

```gradle
test {
    useJUnitPlatform()
    maxHeapSize = '1G'
    finalizedBy jacocoTestReport

    // Optional: Parallel execution
    maxParallelForks = Runtime.runtime.availableProcessors().intdiv(2) ?: 1

    testLogging {
        events "passed", "skipped", "failed"
        exceptionFormat "full"
        showStackTraces = true
    }
}
```

### Pretty Output (Optional)

```gradle
plugins {
    id 'com.adarshr.test-logger' version '4.0.0'
}

testlogger {
    theme = 'mocha'
    slowThreshold = 2000
}
```

## Best Practices

1. **Test naming:** `methodName_scenario_expectedBehavior`
2. **Use descriptive assertions:** Add failure messages
3. **Load data with @BeforeAll:** Use `LoaderHelper.importCsv()`
4. **Constructor injection:** Use `@Inject` with BaseTest
5. **Test isolation:** Create unique data per test (use timestamps)

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| "No tests found" | Missing JUnit config | Add `test { useJUnitPlatform() }` |
| "BaseTest not found" | Missing axelor-utils | Add `implementation project(':axelor-utils')` |
| "Database not found" | Missing persistence.xml | Create in `src/test/resources/META-INF/` |
| "No Persistence provider" | Wrong persistence version | Match version to your Axelor (see Quick Reference) |
| "Cannot inject services" | Not using BaseTest | Extend BaseTest + use `@Inject` constructor |

## Setup Checklist

**Dependencies:**
- [ ] `implementation "com.axelor:axelor-test:${aopVersion}"`
- [ ] `implementation project(':axelor-utils')` or Maven Central version
- [ ] `test { useJUnitPlatform() }` configured
- [ ] JaCoCo plugin added (optional)

**Test Resources:**
- [ ] Check Axelor version: `cat version.txt`
- [ ] Create `src/test/resources/META-INF/persistence.xml` (correct version)
- [ ] Add database config (persistence.xml or axelor-config.properties)

**Test Patterns:**
- [ ] Use BaseTest for integration tests (DI + database)
- [ ] Use plain JUnit for utility classes
- [ ] Follow naming: `method_scenario_expected`
- [ ] Use `@Inject` constructor with BaseTest
- [ ] Target >80% coverage

## References

**Internal:** [Test Patterns](test-patterns.md) | [Service Patterns](service-patterns.md)
**External:** [JUnit 5](https://junit.org/junit5/docs/current/user-guide/) | [Mockito](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html) | [JaCoCo](https://www.jacoco.org/jacoco/trunk/doc/)
**Examples:** axelor-utils addon (production reference)
