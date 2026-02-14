# Pattern Reference Mappings

This document defines which Axelor pattern documentation to reference for each type of code issue.

## Overview

When generating fix specifications, each issue should include a **Pattern Reference** that points developers to the relevant documentation section. This ensures they can learn the correct pattern while fixing the issue.

## Pattern File Structure

Axelor pattern documentation is organized in:
```
plugins/axelor/docs/java/
├── service-patterns.md      # Service layer patterns
├── repository-patterns.md   # Data access patterns
└── controller-patterns.md   # Web layer patterns
```

---

## Mapping Rules

### Service-Related Issues

**Keywords**: "service" + ("@Inject" | "injection" | "dependency")
**Reference**: `docs/java/service-patterns.md` - Dependency Injection
**Description**: How to properly inject dependencies in services using constructor injection

**Keywords**: "@Transactional" | "transaction"
**Reference**: `docs/java/service-patterns.md` - Transaction Management
**Description**: When and how to use @Transactional annotation with proper rollback configuration

**Keywords**: "logger" | "logging"
**Reference**: `docs/java/service-patterns.md` - Logging Best Practices
**Description**: Correct logger initialization and parameterized logging patterns

**Keywords**: "field injection"
**Reference**: `docs/java/service-patterns.md` - Dependency Injection
**Description**: Why constructor injection is preferred over field injection

---

### Repository-Related Issues

**Keywords**: "repository" + ("query" | "SQL" | "filter")
**Reference**: `docs/java/repository-patterns.md` - Query Parameters
**Description**: Using named parameters and parameterized queries safely

**Keywords**: "magic number" + "status"
**Reference**: `docs/java/repository-patterns.md` - Repository Best Practices
**Description**: Using repository constants instead of magic numbers for status values

**Keywords**: "N+1" | "query optimization" | "performance"
**Reference**: `docs/java/repository-patterns.md` - Query Optimization
**Description**: Avoiding N+1 queries and optimizing data access patterns

**Keywords**: "JPA.clear" | "batch" | "memory"
**Reference**: `docs/java/repository-patterns.md` - Batch Operations
**Description**: Proper batch processing with JPA.clear() to prevent memory leaks

**Keywords**: "positional parameter" | "?1" | "?2"
**Reference**: `docs/java/repository-patterns.md` - Query Parameters
**Description**: Using named parameters instead of positional parameters

**Keywords**: "SQL injection" | "string concatenation" + "query"
**Reference**: `docs/java/repository-patterns.md` - Query Parameters
**Description**: Preventing SQL injection with parameterized queries

---

### Controller-Related Issues

**Keywords**: "controller" + "@Inject"
**Reference**: `docs/java/controller-patterns.md` - Dependency Lookup
**Description**: Why controllers must use Beans.get() instead of @Inject

**Keywords**: "controller" + "business logic"
**Reference**: `docs/java/controller-patterns.md` - Thin Controllers
**Description**: Keeping controllers thin and delegating business logic to services

**Keywords**: "TraceBackService" | "exception" + "controller"
**Reference**: `docs/java/controller-patterns.md` - Error Handling
**Description**: Proper exception handling with TraceBackService in controllers

**Keywords**: "Beans.get" | "dependency lookup"
**Reference**: `docs/java/controller-patterns.md` - Dependency Lookup
**Description**: Using Beans.get() for service and repository lookup in controllers

**Keywords**: "moveUp" | "moveDown" | "reorder"
**Reference**: `docs/java/controller-patterns.md` - Grid Operations
**Description**: Using framework's canMove feature instead of custom move methods

**Keywords**: "asType" | "context entity" | "managed entity"
**Reference**: `docs/java/controller-patterns.md` - Entity Management
**Description**: Always fetching managed entities from database in controllers

---

## Special Cases

### Multiple Applicable Patterns

If an issue relates to multiple pattern categories, reference the most specific one first, then mention related patterns:

```markdown
**Pattern Reference**: `docs/java/controller-patterns.md` - Dependency Lookup
**Related Patterns**: See also `docs/java/service-patterns.md` - Dependency Injection
```

### No Specific Match

If keywords don't match any specific pattern, use the generic reference:

```markdown
**Pattern Reference**: See `docs/java/service-patterns.md`, `docs/java/repository-patterns.md`, and `docs/java/controller-patterns.md` for Axelor best practices
```

### Security Issues

**Keywords**: "security" | "SQL injection" | "credential" | "password"
**Reference**: `docs/java/owasp-security-guide.md`
**Description**: Security best practices and vulnerability prevention

### Performance Issues

**Keywords**: "performance" | "optimization" | "slow"
**Reference**: `docs/java/performance-guide.md`
**Description**: Performance optimization patterns and anti-patterns

---

## Reference Format

Always use this format in fix specifications:

```markdown
**Pattern Reference**: `path/to/pattern-doc.md` - Section Name
```

Examples:
- `docs/java/service-patterns.md` - Dependency Injection
- `docs/java/repository-patterns.md` - Query Optimization
- `docs/java/controller-patterns.md` - Thin Controllers

---

## Usage in Fix Specification Generator

When processing issues:

1. Extract issue title and description
2. Convert to lowercase for matching
3. Check keyword patterns in this document
4. Use the **most specific** matching reference
5. If multiple matches, use the first match and optionally add related patterns
6. If no match, use the generic multi-doc reference
7. Always include the section name after the dash

---

## Maintenance

When adding new pattern documentation:
1. Add the mapping rules here
2. Use clear, searchable keywords
3. Provide meaningful section names
4. Update the fix-spec-generator agent to reference this file
5. Ensure consistency with actual documentation structure
