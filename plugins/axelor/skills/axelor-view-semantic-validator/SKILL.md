---
name: axelor-view-semantic-validator
description: Validates view semantic coherence - field existence, action coherence, widget compatibility. Use after XSD validation.
user-invocable: false
allowed-tools:
  - Bash
  - Read
---

# Axelor View Semantic Validator

**✅ PYTHON AUTOMATION AVAILABLE: `view_semantic_validator.py`**

Use this Python script for automated view semantic validation. See Usage section below.

## Mission

Validate view semantic coherence and cross-file integrity.

## Scope

Semantic validation NOT covered by XSD:
- Field existence in domain models (cross-file)
- Action existence (cross-file)
- Domain expression syntax
- Widget compatibility with field types
- Best practices warnings

**Note**: Basic syntax handled by XSD validator.

## Validation Categories

### 1. Cross-File Field Validation
- Scan domains/*.xml to build entity field index
- Verify each `<field name>` exists in model
- Error if field doesn't exist

### 2. Action Coherence
- Build action index from all view files
- Verify onClick/onChange/onLoad actions exist
- Cross-file validation

### 3. Widget Compatibility
- Verify widget type compatible with field type
- Examples: progress → decimal/integer, html → string
- Suggest appropriate widgets

### 4. Best Practices
- Grid without orderBy: WARNING
- one-to-many without panel-related: WARNING
- Actions without save in workflows: WARNING

## Usage

```bash
# Validate entire views directory
python3 view_semantic_validator.py views/ --domains domains/

# Validate specific file
python3 view_semantic_validator.py Project.xml --domains domains/

# Exit code: 0 = passed, 1 = failed
```

## Output Format

Token-optimized, no emojis:

```
SEMANTIC VALIDATION: Project.xml

ERRORS: 2
Line 45, <field name="unknownField">
  Field does not exist in model com.axelor.apps.project.db.Project

Line 78, <button onClick="action-project-nonexistent">
  Action not found: action-project-nonexistent

WARNINGS: 1
Line 23, <grid name="project-grid">
  Consider adding orderBy for consistent sorting

SUMMARY:
- Fields checked: 23
- Actions checked: 7
- Errors: 2
- Warnings: 1
- Status: FAILED
```

## Integration

Called by `view-agent` agent in Step 3.3:

```
XSD Validation
  ↓
Naming Checker
  ↓
Semantic Validator ← THIS
  ↓
./gradlew clean build
```

## Complementary with XSD Validator

**XSD**: Element validity, attribute correctness, required attributes
**Semantic**: Field existence, action coherence, widget compatibility

0% redundancy.

## Requirements

- Python 3.8+
- Standard library only
- @skills/axelor-view-semantic-validator/reference/semantic-rules.md
