# Detection Patterns

This document defines the grep patterns and bash commands used to detect Axelor code issues during analysis.

## Overview

The code analyzer uses grep-based pattern matching to detect violations of Axelor best practices. This document centralizes all detection patterns for maintainability and consistency.

---

## Service Pattern Violations

### Field Injection in Services (HIGH)

**Issue**: Services must use constructor injection, not field injection

**Detection Pattern**:
```bash
# Find @Inject on fields (not in constructor parameters)
grep -B 5 "class.*Service.*Impl" <file> | \
  grep -A 50 "class.*Service" | \
  grep "@Inject" | \
  grep -v "public.*("
```

**Report Message**:
```
HIGH: Field injection detected - use constructor injection instead
```

**Why It Matters**: Field injection makes testing difficult and hides dependencies

---

### Missing @Transactional on Write Operations (HIGH)

**Issue**: Methods with save/persist/remove should have @Transactional

**Detection Pattern**:
```bash
# Find write operations without @Transactional
grep -B 10 -E "\.(save|persist|remove)\(" <file> | \
  grep -L "@Transactional"
```

**Report Message**:
```
HIGH: Write operation without @Transactional annotation
```

**Why It Matters**: Data inconsistency if operation fails mid-execution

---

### String Concatenation in Logging (MEDIUM)

**Issue**: Use parameterized logging, not string concatenation

**Detection Pattern**:
```bash
# Find log statements with + operator
grep -nE 'log\.(debug|info|warn|error).*\+' <file>
```

**Report Message**:
```
MEDIUM: String concatenation in logging - use parameterized logging
```

**Why It Matters**: Performance overhead when log level is disabled

---

### Incorrect Logger Declaration (MEDIUM)

**Issue**: Logger should use MethodHandles pattern

**Detection Pattern**:
```bash
# Find getLogger not using MethodHandles
grep -n "getLogger\(" <file> | \
  grep -v "MethodHandles.lookup().lookupClass()"
```

**Report Message**:
```
MEDIUM: Use MethodHandles.lookup().lookupClass() for logger initialization
```

**Why It Matters**: Incorrect logger context in inheritance scenarios

---

## Repository Pattern Violations

### Repository Without Constructor Injection (MEDIUM)

**Issue**: Custom repos should use constructor injection

**Detection Pattern**:
```bash
# Find custom repository classes without @Inject
grep -l "class.*Repo extends.*Repository" <file> | \
  xargs grep -L "@Inject"
```

**Report Message**:
```
MEDIUM: Custom repository missing constructor injection
```

---

### Magic Numbers in Queries (MEDIUM)

**Issue**: Use constants instead of magic status values

**Detection Pattern**:
```bash
# Find numeric literals in status queries
grep -nE 'statusSelect.*=.*[0-9]' <file>
```

**Report Message**:
```
MEDIUM: Magic number in query - use repository constants (e.g., STATUS_DRAFT)
```

**Why It Matters**: Unclear meaning and hard to maintain

---

### Positional Parameters in Queries (LOW)

**Issue**: Prefer named parameters over positional

**Detection Pattern**:
```bash
# Find ?1, ?2 etc. in queries
grep -nE '\?[0-9]' <file>
```

**Report Message**:
```
LOW: Positional parameter - prefer named parameters for clarity
```

**Why It Matters**: Named parameters are more readable and maintainable

---

### Missing JPA.clear() in Batch (HIGH)

**Issue**: Batch processing should call JPA.clear() to prevent memory leaks

**Detection Pattern**:
```bash
# Check if batch loop has JPA.clear()
grep -B 20 -A 20 "for.*:" <file> | grep -c "JPA.clear()"
# If count is 0, report issue
```

**Report Message**:
```
HIGH: Batch processing without JPA.clear() - risk of memory leak
```

**Why It Matters**: OutOfMemoryError with large datasets

---

### SQL Injection Risk (CRITICAL)

**Issue**: String concatenation in queries allows SQL injection

**Detection Pattern**:
```bash
# Find string concatenation in filter/query
grep -nE '(filter|createQuery).*\+.*["\x27]' <file>
```

**Report Message**:
```
CRITICAL: SQL injection vulnerability - use parameterized queries
```

**Why It Matters**: Security vulnerability allowing database attacks

---

## Controller Pattern Violations

### @Inject in Controller (CRITICAL)

**Issue**: Controllers must use Beans.get(), not @Inject

**Detection Pattern**:
```bash
# Find @Inject in controller classes
grep -l "class.*Controller" <file> | \
  xargs grep -n "@Inject"
```

**Report Message**:
```
CRITICAL: @Inject in controller - use Beans.get() instead
```

**Why It Matters**: Controllers are NOT injected; dependencies will be null

---

### Missing Beans.get() Import (HIGH)

**Issue**: Controllers should import Beans for service lookup

**Detection Pattern**:
```bash
# Check if controller has Beans import
grep -l "class.*Controller" <file> | \
  xargs grep -L "import com.axelor.inject.Beans"
```

**Report Message**:
```
HIGH: Missing Beans import - controllers must use Beans.get()
```

---

### Business Logic in Controller (HIGH)

**Issue**: Controllers should delegate to services

**Detection Pattern**:
```bash
# Complex patterns suggesting business logic:
# 1. Multiple levels of nesting
grep -n "    .*if.*{" <file> | grep "class.*Controller"

# 2. Loops in controller methods
grep -B 5 "class.*Controller" <file> | grep -A 100 "public void" | grep "for\s*("

# 3. Mathematical calculations
grep -n "BigDecimal.*add\|subtract\|multiply\|divide" <file> | grep "Controller"
```

**Report Message**:
```
HIGH: Potential business logic in controller - delegate to service
```

**Why It Matters**: Violates separation of concerns, hard to test

---

### Missing TraceBackService.trace() (MEDIUM)

**Issue**: Exception handling should use TraceBackService

**Detection Pattern**:
```bash
# Find catch blocks without TraceBackService
grep -B 10 "catch.*Exception" <file> | \
  grep -L "TraceBackService.trace"
```

**Report Message**:
```
MEDIUM: Exception handling without TraceBackService.trace()
```

**Why It Matters**: Lost error context for debugging

---

### Custom moveUp/moveDown Methods (MEDIUM)

**Issue**: Should use canMove="true" on grid

**Detection Pattern**:
```bash
# Find move-related method names
grep -nE "(moveUp|moveDown|reorder|movePosition)" <file>
```

**Report Message**:
```
MEDIUM: Custom move methods - use canMove='true' on grid instead
```

**Why It Matters**: Framework provides this feature; custom code is unnecessary

---

### Not Fetching Managed Entity (HIGH)

**Issue**: Should fetch from DB, not use context entity directly

**Detection Pattern**:
```bash
# Find asType without subsequent find()
grep -nE "asType\(.*\.class\)" <file> | \
  grep -v "Repository.*find"
```

**Report Message**:
```
HIGH: Using context entity without fetching from DB - fetch managed entity
```

**Why It Matters**: Detached entities cause data integrity issues

---

## Naming Convention Violations

### Service Interface Naming (LOW)

**Issue**: Service interfaces should end with "Service"

**Detection Pattern**:
```bash
# Find interface declarations not ending with Service
grep -nE "interface.*(?<!Service)$" <file>
```

**Report Message**:
```
LOW: Service interface should end with 'Service'
```

---

### Service Implementation Naming (LOW)

**Issue**: Service implementations should end with "ServiceImpl"

**Detection Pattern**:
```bash
# Find service implementations not ending with ServiceImpl
grep -nE "class.*implements.*Service.*(?<!ServiceImpl)" <file>
```

**Report Message**:
```
LOW: Service implementation should end with 'ServiceImpl'
```

---

### Repository Naming (LOW)

**Issue**: Custom repos should follow [Entity]Repo pattern

**Detection Pattern**:
```bash
# Find Repository classes not following naming pattern
grep -nE "class.*Repository.*extends.*Repository" <file> | \
  grep -v "Repo extends"
```

**Report Message**:
```
LOW: Repository should follow naming pattern: [Entity]Repo
```

---

## Performance Anti-Patterns

### N+1 Query Detection (HIGH)

**Issue**: Loop executing repository calls

**Detection Pattern**:
```bash
# Pattern 1: for loop followed by find/all within method
grep -n "for\s*(" <file> | while read line; do
  line_num=$(echo $line | cut -d: -f1)
  tail -n +$line_num <file> | head -20 | grep -E "(\.find\(|\.all\(\))"
done

# Pattern 2: stream operations with repository calls
grep -nE "\.stream\(\).*\.map\(.*Repository" <file>
```

**Report Message**:
```
HIGH: Potential N+1 query detected - use single query with filter
```

**Why It Matters**: Exponential performance degradation with large datasets

---

### Inefficient Stream Operations (MEDIUM)

**Issue**: Multiple stream passes can be combined

**Detection Pattern**:
```bash
# Find multiple sequential stream operations
grep -n "\.collect(Collectors" <file> | while read line; do
  line_num=$(echo $line | cut -d: -f1)
  next_line=$((line_num + 1))
  sed -n "${next_line}p" <file> | grep "\.stream()"
done
```

**Report Message**:
```
MEDIUM: Multiple stream passes - combine into single stream operation
```

---

### String Concatenation in Loops (MEDIUM)

**Issue**: Use StringBuilder for string building in loops

**Detection Pattern**:
```bash
# Find string concatenation with + inside loops
grep -B 5 "for\s*(" <file> | \
  grep -A 20 "for\s*(" | \
  grep 'String.*+='
```

**Report Message**:
```
MEDIUM: String concatenation in loop - use StringBuilder
```

---

## Security Risks

### Hardcoded Credentials (CRITICAL)

**Issue**: Passwords or secrets in source code

**Detection Pattern**:
```bash
# Find suspicious hardcoded values
grep -nEi '(password|secret|apikey|token|credential)\s*=\s*["\x27]' <file> | \
  grep -v "null" | \
  grep -v '""' | \
  grep -v "PLACEHOLDER"
```

**Report Message**:
```
CRITICAL: Hardcoded credential detected - use configuration or environment variable
```

**Why It Matters**: Security risk exposing sensitive data

---

### Missing Input Validation (HIGH)

**Issue**: User input not validated before use

**Detection Pattern**:
```bash
# Find request parameter usage without validation
grep -n "request.getParameter" <file> | while read line; do
  line_num=$(echo $line | cut -d: -f1)
  # Check if followed by validation within 5 lines
  tail -n +$line_num <file> | head -5 | grep -q "if.*null\|isEmpty"
  if [ $? -ne 0 ]; then
    echo "$line"
  fi
done
```

**Report Message**:
```
HIGH: Missing input validation - validate before use
```

---

## Style and Convention Issues

### French Comments (MEDIUM)

**Issue**: Comments should be in English

**Detection Pattern**:
```bash
# Find French keywords in comments
grep -nE '//.*\b(récupère|vérifie|sauvegarde|crée|supprime|retourne)\b' <file>
```

**Report Message**:
```
MEDIUM: French comment detected - use English for international teams
```

---

### Emoji in Code (MEDIUM)

**Issue**: Emojis should not be in source code

**Detection Pattern**:
```bash
# Find emoji unicode ranges
grep -nP '[\x{1F300}-\x{1F9FF}]' <file>
```

**Report Message**:
```
MEDIUM: Emoji detected in code - replace with text
```

---

### Missing JavaDoc on Public Methods (LOW)

**Issue**: Public API methods should have documentation

**Detection Pattern**:
```bash
# Find public methods without preceding JavaDoc
grep -B 1 "public.*(" <file> | \
  grep -v "^\s*/\*\*" | \
  grep "public"
```

**Report Message**:
```
LOW: Missing JavaDoc on public method
```

---

## Complex Code Patterns

### Cyclomatic Complexity (MEDIUM)

**Issue**: Too many branches make code hard to understand

**Detection Pattern**:
```bash
# Count if/else/switch in method (rough complexity measure)
grep -n "public.*{" <file> | while read line; do
  line_num=$(echo $line | cut -d: -f1)
  # Count branches in next 50 lines
  tail -n +$line_num <file> | head -50 | \
    grep -cE "(if\s*\(|else|case\s+)"
done
# Report if > 10
```

**Report Message**:
```
MEDIUM: High cyclomatic complexity - consider refactoring
```

---

### Method Length (LOW)

**Issue**: Methods over 50 lines are hard to understand

**Detection Pattern**:
```bash
# Measure lines between method start and closing brace
# (Implementation depends on code structure analysis)
```

**Report Message**:
```
LOW: Long method detected - consider splitting into smaller methods
```

---

## Usage in Code Analyzer

### Pattern Execution Flow

1. Read file to analyze
2. Determine file type (Java, XML, properties)
3. For each applicable pattern in this document:
   - Execute detection command
   - If match found, record issue with:
     - Severity level
     - Line number
     - Description
     - Fix recommendation
4. Aggregate results by severity
5. Generate report

### Pattern Categories by Priority

Execute patterns in this order for efficiency:

1. **CRITICAL** - Security and stability (execute first)
2. **HIGH** - Correctness and performance
3. **MEDIUM** - Maintainability and style
4. **LOW** - Documentation and conventions

### Error Handling

- If grep fails: Log warning, continue with next pattern
- If file not readable: Skip file, report error
- If pattern returns no matches: Continue (no issue found)

---

## Maintenance

### Adding New Patterns

When adding a new detection pattern:

1. Define clear issue description
2. Write grep/bash command that reliably detects the issue
3. Test pattern on sample code (both positive and negative cases)
4. Assign appropriate severity level
5. Write clear report message
6. Add "Why It Matters" explanation
7. Document pattern in this file
8. Update code analyzer agent to reference this document

### Testing Patterns

Each pattern should be tested with:
- **Positive case**: Code that should trigger the pattern
- **Negative case**: Correct code that should NOT trigger
- **Edge cases**: Borderline situations

### Pattern Performance

- Prefer simple grep over complex regex when possible
- Avoid nested loops in pattern detection
- Cache file reads when checking multiple patterns
- Use grep -l (files only) before grep -n (with line numbers)

---

## Reference

### Grep Options Used

- `-n`: Show line numbers
- `-E`: Extended regex
- `-i`: Case insensitive
- `-l`: Files with matches only
- `-L`: Files without matches
- `-B N`: N lines before match
- `-A N`: N lines after match
- `-c`: Count matches only

### Common Regex Patterns

- `\s*`: Zero or more whitespace
- `\s+`: One or more whitespace
- `.*`: Any characters
- `\b`: Word boundary
- `(?<!X)`: Negative lookbehind
- `(?=X)`: Positive lookahead
