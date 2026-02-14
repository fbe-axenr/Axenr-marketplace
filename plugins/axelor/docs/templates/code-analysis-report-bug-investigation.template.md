# Code Analysis Report

**Generated**: {YYYY-MM-DD HH:MM:SS}
**Path Analyzed**: {path}
**Files Analyzed**: {count}
**Report Location**: {output-path}
**Bug Investigation**: ENABLED

---

## 🐛 Bug Investigation

**Issue Description:**
{issue_description}

**Analysis Type:** {NullPointerException | Performance | Data Corruption | etc.}
**Affected Functionality:** {module/feature identified from issue}

### Root Cause Analysis

{Analyze the code in context of the bug description}

**Potential Causes Identified:**
1. [file:line] - {description of potential cause}
2. [file:line] - {description of potential cause}
3. ...

### Affected Code Sections

**Direct Impact:**
- [file:line] - {code section directly related to the bug}

**Indirect Impact:**
- [file:line] - {code sections that might be affected}

### Related Conformity Issues

{List any conformity issues from the analysis below that could contribute to this bug}

---

## ✓ Conformity Analysis

### Executive Summary

- Total Issues Found: {X}
- Critical: {X}
- High: {X}
- Medium: {X}
- Low: {X}

---

## 1. Bad Practices (Criticality: CRITICAL → LOW)

### CRITICAL
{List of critical issues with file:line references}

### HIGH
{List of high priority issues with file:line references}

### MEDIUM
{List of medium priority issues with file:line references}

### LOW
{List of low priority issues with file:line references}

---

## 2. Optimization Opportunities
{List of potential optimizations}

---

## 3. Performance Issues
{List of performance concerns}

---

## 4. Security Risks
{List of security vulnerabilities}

---

## Recommendations
1. Fix all CRITICAL issues immediately
2. Address HIGH priority issues before merging
3. Plan for MEDIUM issues in next sprint
4. LOW issues can be addressed incrementally

---

## Detailed Findings
{Detailed breakdown by file with code snippets if helpful}
