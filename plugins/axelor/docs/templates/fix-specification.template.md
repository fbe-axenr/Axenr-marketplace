# Fix Specification

**Generated From**: {original-analysis-report-filename}
**Generated Date**: {YYYY-MM-DD HH:MM:SS}
**Total Issues**: {count}
**Files Affected**: {count}

---

## Summary

| Priority | Count |
|----------|-------|
| CRITICAL | {X}     |
| HIGH     | {X}     |
| MEDIUM   | {X}     |
| LOW      | {X}     |

---

## File: {relative-file-path-1}

**Total Issues in File**: {X} (CRITICAL: {X}, HIGH: {X}, MEDIUM: {X}, LOW: {X})

### CRITICAL Issues

#### CRIT-001: {Issue Title}

**Location**: {filename}:{line}

**Problem**: {Clear description}

**Impact**: {Why this is critical}

**Solution**:
{Multi-line solution with numbered steps}

**Pattern Reference**: `{path-to-pattern-doc}` - {Section Name}

---

### HIGH Issues

#### HIGH-001: {Issue Title}

...

---

## File: {relative-file-path-2}

...

---

## Implementation Guidelines

### Priority Order

1. **CRITICAL** - Fix immediately (security, stability, architectural violations)
2. **HIGH** - Fix before merge (correctness, performance, data integrity)
3. **MEDIUM** - Plan for upcoming sprint (maintainability, best practices)
4. **LOW** - Address incrementally (documentation, conventions)

### Testing Requirements

- Add or update unit tests for each fix
- Ensure all existing tests still pass
- Add integration tests for CRITICAL and HIGH fixes
- Verify no regressions
