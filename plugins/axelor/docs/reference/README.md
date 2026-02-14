# Code Analysis Reference Documentation

This directory contains reference documentation extracted from the code analysis agents for better maintainability and reusability.

## Purpose

These reference documents centralize knowledge that was previously embedded in agent files, making it:
- Easier to maintain and update
- Reusable across multiple agents
- More accessible to developers
- Version-controlled in a single location

## Files

### [detection-patterns.md](detection-patterns.md)

**Purpose**: Defines grep patterns and bash commands to detect code issues

**Used by**: `code-analyzer` agent

**Contains**:
- Service pattern violations (field injection, missing @Transactional, logging issues)
- Repository pattern violations (magic numbers, positional parameters, SQL injection)
- Controller pattern violations (@Inject usage, business logic, entity management)
- Performance anti-patterns (N+1 queries, inefficient streams)
- Security risks (hardcoded credentials, missing validation)
- Style issues (French comments, emoji, JavaDoc)

**Format**: Each pattern includes:
- Issue description
- Detection command (grep/bash)
- Report message
- Severity level
- Explanation

---

### [issue-impact-mappings.md](issue-impact-mappings.md)

**Purpose**: Maps issue types to impact descriptions (why it matters)

**Used by**:
- `code-analyzer` agent (classification)
- `spec-inspector` agent (impact field generation)

**Contains**:
- CRITICAL impacts (security, runtime failures)
- HIGH impacts (performance, data integrity)
- MEDIUM impacts (maintainability, style)
- LOW impacts (documentation, conventions)
- Default impacts for unmatched patterns

**Format**: Keyword patterns → Impact description

**Example**:
```
Pattern: "@Inject" + "controller"
Impact: Controllers in Axelor are NOT injected. Using @Inject will cause
        the dependency to be null, resulting in NullPointerException at runtime.
```

---

### [pattern-reference-mappings.md](pattern-reference-mappings.md)

**Purpose**: Maps issue types to relevant Axelor pattern documentation

**Used by**: `spec-inspector` agent

**Contains**:
- Service-related issue → service-patterns.md sections
- Repository-related issue → repository-patterns.md sections
- Controller-related issue → controller-patterns.md sections
- Security issues → owasp-security-guide.md
- Performance issues → performance-guide.md

**Format**: Keyword patterns → Documentation path + section

**Example**:
```
Keywords: "@Transactional" | "transaction"
Reference: docs/java/service-patterns.md - Transaction Management
```

---

### [solution-templates.md](solution-templates.md)

**Purpose**: Provides detailed, step-by-step solutions for common issues

**Used by**: `spec-inspector` agent

**Contains**:
- Critical fixes (SQL injection, @Inject in controllers, hardcoded credentials)
- High priority fixes (missing @Transactional, N+1 queries, field injection)
- Medium priority fixes (French comments, emoji, logging issues)
- Low priority fixes (JavaDoc, naming conventions)

**Format**: Each template includes:
- Issue pattern
- Numbered solution steps
- Before/after code examples
- Verification steps
- Common pitfalls

**Example**:
```
### Missing @Transactional

Solution Template:
1. Add @Transactional annotation to method {methodName}
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

---

## Workflow Integration

### Code Analysis Workflow

```
┌─────────────────────────┐
│ code-analyzer    │
│                         │
│ 1. Scan files           │
│ 2. Apply patterns  ──────→ detection-patterns.md
│ 3. Classify issues ─────→ issue-impact-mappings.md
│ 4. Generate report      │
└─────────┬───────────────┘
          │
          │ Produces: code-analysis-report.md
          │
          ↓
┌─────────────────────────┐
│ axelor-fix-spec-gen     │
│                         │
│ 1. Parse report         │
│ 2. Determine impact ────→ issue-impact-mappings.md
│ 3. Map to patterns  ────→ pattern-reference-mappings.md
│ 4. Expand solutions ────→ solution-templates.md
│ 5. Generate spec        │
└─────────────────────────┘
          │
          │ Produces: fix-specification.md
          ↓
     (Developer fixes code using specification)
```

---

## Maintenance Guidelines

### When to Update Reference Docs

1. **detection-patterns.md**:
   - Adding new Axelor best practices
   - Discovering new anti-patterns
   - Updating grep commands for accuracy

2. **issue-impact-mappings.md**:
   - Adding new issue types
   - Refining impact descriptions based on real incidents
   - Updating severity classifications

3. **pattern-reference-mappings.md**:
   - New pattern documentation is created
   - Documentation structure changes
   - Section names are updated

4. **solution-templates.md**:
   - New solution patterns are discovered
   - Best practices evolve
   - Framework API changes require different approaches

### Update Process

1. Update the reference document
2. Test with sample code to verify patterns work
3. Update agent files if workflow changes
4. Commit with descriptive message
5. Document in CHANGELOG

### Testing Reference Updates

After updating reference docs, test with:

```bash
# Run code analysis on sample project
/analyze-code src/main/java/com/axelor/apps/sample/

# Verify patterns detect known issues
# Check report quality

# Generate fix specification
/analyze-code src/main/java/com/axelor/apps/sample/ --spec

# Verify solutions are actionable
# Check pattern references are correct
```

---

## Version History

- **2025-12-15**: Initial extraction from agent files
  - Created detection-patterns.md (comprehensive grep patterns)
  - Created issue-impact-mappings.md (impact descriptions by severity)
  - Created pattern-reference-mappings.md (doc path mappings)
  - Created solution-templates.md (step-by-step fixes)
  - Updated agents to reference these docs instead of embedding content

---

## Related Documentation

- [../java/service-patterns.md](../java/service-patterns.md) - Service layer best practices
- [../java/repository-patterns.md](../java/repository-patterns.md) - Data access patterns
- [../java/controller-patterns.md](../java/controller-patterns.md) - Web layer patterns
- [../java/owasp-security-guide.md](../java/owasp-security-guide.md) - Security guidelines
- [../java/performance-guide.md](../java/performance-guide.md) - Performance optimization

---

## Contributing

When contributing to reference documentation:

1. Keep examples concrete and actionable
2. Use consistent formatting
3. Include "Why it matters" explanations
4. Test patterns on real code
5. Cross-reference related documentation
6. Update this README if adding new files
