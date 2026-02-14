# Issue Impact Mappings

This document defines how to determine the impact description for each type of code issue based on keywords in the title/description.

## Overview

When generating fix specifications, each issue needs an **Impact** field that explains why the issue matters and what problems it causes. This document provides standardized impact descriptions based on issue patterns.

## Impact Determination Process

Look for keywords in the issue title and description to match against the patterns below. Use the corresponding impact description in the fix specification.

---

## CRITICAL Impacts

### @Inject in Controller
**Pattern**: "@Inject" + "controller"
**Impact**: Controllers in Axelor are NOT injected. Using @Inject will cause the dependency to be null, resulting in NullPointerException at runtime. This is a critical pattern violation that breaks functionality completely.

### SQL Injection
**Pattern**: "SQL injection" OR ("string concatenation" + "query")
**Impact**: Security vulnerability allowing database attacks. Attackers can manipulate queries to access, modify, or delete unauthorized data, leading to data breaches and system compromise.

### Hardcoded Credentials
**Pattern**: "hardcoded" + ("password" | "credential" | "secret" | "token")
**Impact**: Security risk exposing sensitive data. Hardcoded credentials in source code can be discovered through repository access or decompilation, leading to unauthorized system access.

---

## HIGH Impacts

### N+1 Query Pattern
**Pattern**: "N+1 query" OR ("loop" + "repository call")
**Impact**: Performance degradation with large datasets. Each iteration executes a separate database query, causing exponential performance degradation. For 100 items, this results in 101 queries instead of 1-2 optimized queries.

### Missing @Transactional
**Pattern**: "Missing @Transactional" OR ("write operation" + "transaction")
**Impact**: Data inconsistency and integrity issues without proper transaction management. Write operations without transactions may not be properly rolled back on errors, leading to partial updates and corrupted data states.

### Field Injection
**Pattern**: "field injection" OR ("@Inject" + "field")
**Impact**: Testability issues and hidden dependencies. Field injection makes unit testing difficult, hides dependencies in the class API, and can cause subtle initialization order problems. Constructor injection makes dependencies explicit and testable.

### Business Logic in Controller
**Pattern**: "business logic" + "controller"
**Impact**: Poor maintainability and violation of separation of concerns. Business logic in controllers cannot be reused, makes testing difficult, and violates the MVC pattern. Controllers should delegate to services for all business operations.

### Not Fetching Managed Entity
**Pattern**: "context entity" OR "asType" OR "managed entity"
**Impact**: Data integrity issues when working with detached entities. Using entities directly from request context without fetching from database can lead to stale data, missed updates, and transaction management problems.

### Missing JPA.clear() in Batch
**Pattern**: "JPA.clear" OR ("batch" + "memory")
**Impact**: Memory leak and OutOfMemoryError in batch processing. Without periodic JPA.clear() calls, the persistence context accumulates all processed entities in memory, causing heap exhaustion and application crashes.

---

## MEDIUM Impacts

### French Comments
**Pattern**: "French comment" OR ("comment" + "language")
**Impact**: Code maintainability issues in international teams. Non-English comments create barriers for developers who don't speak French, reducing code comprehension and collaboration effectiveness.

### Emoji in Code
**Pattern**: "emoji" OR "emoticon"
**Impact**: Unprofessional code appearance and potential encoding issues. Emojis in source code can cause problems with different character encodings, break automated tools, and appear unprofessional in enterprise applications.

### String Concatenation in Logging
**Pattern**: ("string concatenation" + "log") OR "logging performance"
**Impact**: Performance overhead in high-volume logging scenarios. String concatenation for log messages executes even when the log level is disabled, wasting CPU cycles. Parameterized logging evaluates arguments only when needed.

### Magic Numbers
**Pattern**: "magic number" OR ("hardcoded" + "constant")
**Impact**: Code readability and maintainability issues. Magic numbers make code difficult to understand and maintain. Changes require finding all occurrences, increasing risk of bugs. Named constants provide semantic meaning and centralize values.

### Incorrect Logger Declaration
**Pattern**: "logger" + ("declaration" | "initialization")
**Impact**: Incorrect logger context and debugging difficulties. Logger should use MethodHandles.lookup().lookupClass() to ensure the logger is correctly associated with the actual class, especially in inheritance scenarios.

### Missing TraceBackService.trace()
**Pattern**: "TraceBackService" OR ("exception" + "handling")
**Impact**: Lost error context and debugging difficulties. Without TraceBackService.trace(), exceptions are not properly logged in Axelor's error tracking system, making debugging and error analysis much harder.

### Custom Move Methods
**Pattern**: "moveUp" OR "moveDown" OR "reorder"
**Impact**: Unnecessary custom code when framework feature exists. Axelor provides built-in grid reordering with canMove="true". Custom implementations are harder to maintain and may have bugs that the framework already handles.

---

## LOW Impacts

### Missing JavaDoc
**Pattern**: "JavaDoc" OR "documentation"
**Impact**: Reduced code documentation and developer comprehension. Missing JavaDoc makes it harder for new developers to understand method purpose, parameters, and return values, slowing down development and increasing bugs.

### Naming Convention Violations
**Pattern**: "naming convention" OR "naming standard"
**Impact**: Code consistency and readability issues. Inconsistent naming makes code harder to scan and understand. Following conventions helps developers quickly identify class types (Service, Repository, Controller) and their responsibilities.

### Positional Parameters in Queries
**Pattern**: "positional parameter" OR "?1"
**Impact**: Query readability and maintainability. Positional parameters (?1, ?2) are less readable than named parameters (:name, :status) and more error-prone when query structure changes.

---

## Default Impact

If no specific pattern matches, use a generic impact based on the severity level:

- **CRITICAL**: "Critical issue that must be fixed immediately to prevent system failures or security vulnerabilities."
- **HIGH**: "High-priority issue that affects correctness, performance, or data integrity and should be fixed before merge."
- **MEDIUM**: "Medium-priority issue affecting code maintainability, readability, or best practices. Should be addressed in upcoming sprint."
- **LOW**: "Low-priority improvement for code quality and consistency. Can be addressed incrementally."

---

## Usage in Fix Specification Generator

When processing issues from the analysis report:

1. Extract the issue title and description
2. Convert to lowercase for matching
3. Check for keyword patterns in order (CRITICAL → HIGH → MEDIUM → LOW)
4. Use the first matching impact description
5. If no match, use the default impact for the severity level
6. Include the impact in the generated fix specification

## Maintenance

When new issue types are added to the code analyzer:
1. Add corresponding impact mapping here
2. Update the fix-spec-generator agent to reference this file
3. Keep impact descriptions focused on business/technical consequences, not implementation details
