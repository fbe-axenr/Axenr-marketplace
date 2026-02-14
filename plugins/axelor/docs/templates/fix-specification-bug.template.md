# Fix Specification

**Generated From**: {original-analysis-report-filename}
**Generated Date**: {YYYY-MM-DD HH:MM:SS}
**Bug Investigation**: ENABLED
**Total Issues**: {count}
**Files Affected**: {count}

---

## Summary

| Category | Count |
|----------|-------|
| Bug Fixes | {X}     |
| Conformity Fixes | {X} |
| **Total** | **{X}** |

### By Priority

| Priority | Count |
|----------|-------|
| CRITICAL | {X}     |
| HIGH     | {X}     |
| MEDIUM   | {X}     |
| LOW      | {X}     |

---

# PART 1: Bug Fix Specification

> **Priority**: HIGHEST - These fixes directly address the reported bug

## Overview

**Original Issue**: {brief summary from Bug Investigation section}

**Root Cause**: {summary of root cause from analysis}

**Files Affected by Bug**: {count}

---

## File: {relative-file-path-1}

**Bug-Related Issues in File**: {X}

### BUG-001: {Issue Title from Potential Causes}

**Location**: {filename}:{line}

**Problem**: {Description from Potential Causes Identified}

**Impact**: Directly contributes to the reported bug: {bug description}

**Solution**:
{Detailed fix steps}

**Pattern Reference**: `{path-to-pattern-doc}` - {Section Name}

**Testing**: Verify the original bug is resolved after applying this fix

---

### BUG-002: {Next Bug-Related Issue}

...

---

# PART 2: Conformity Fix Specification

> **Priority**: NORMAL - General code quality improvements

## Overview

**Purpose**: Address code quality issues discovered during bug investigation

**Files Affected**: {count}

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

#### CRIT-002: {Next Issue}

...

### HIGH Issues

#### HIGH-001: {Issue Title}

...

---

## File: {relative-file-path-2}

...

---

## Implementation Guidelines

### Priority Order for Bug Fixes

1. **BUG FIXES** - Fix FIRST (directly resolves reported bug)
2. **CRITICAL** - Fix immediately after bug fixes (security, stability, architectural violations)
3. **HIGH** - Fix before merge (correctness, performance, data integrity)
4. **MEDIUM** - Plan for upcoming sprint (maintainability, best practices)
5. **LOW** - Address incrementally (documentation, conventions)

### Testing Requirements for Bug Fixes

- **Reproduce the original bug** before applying fixes
- Apply bug fixes in order (BUG-001, BUG-002, etc.)
- **Verify bug is resolved** after each fix
- Add regression tests to prevent bug from reoccurring
- Then proceed with conformity fixes
