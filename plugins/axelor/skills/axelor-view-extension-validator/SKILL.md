---
name: axelor-view-extension-validator
description: Validates Axelor view extension XML files - checks XPath expressions, extension syntax, and target element existence.
user-invocable: false
---

# Axelor View Extension Validator

**✅ PYTHON AUTOMATION AVAILABLE: `axelor_view_extension_validator.py`**

Use this Python script for automated view extension validation. See Usage section below.

Validates extension-specific rules NOT covered by XSD validation.

## Purpose

Ensures extension views follow Axelor conventions:
- `extension="true"` only supported for **form** and **grid** views
- `id` attribute is non-empty and unique
- `name` attribute is non-empty (must match original view name)
- Other view types (tree, calendar, kanban, etc.) require full override with unique id

**Note:** Run XSD validation BEFORE this validator for complete validation.

## Usage

```bash
# Validate a single file
python3 axelor_view_extension_validator.py src/main/resources/views/Partner.xml

# Validate all XML files in views directory
python3 axelor_view_extension_validator.py src/main/resources/views/
```

## Validation Rules

| Rule | Description |
|------|-------------|
| Missing `extension="true"` | View with `<extend>` elements must have `extension="true"` |
| Missing `id` | Extension view must have unique `id` attribute |
| Empty `id` | `id` attribute cannot be empty |
| Duplicate `id` | Each extension view must have unique `id` |
| Missing `name` | Extension view must have `name` attribute |
| Empty `name` | `name` attribute cannot be empty |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All validations passed |
| 1 | Validation errors found |
| 2 | Invalid arguments or file not found |

## Example Output

```
============================================================
VIEW EXTENSION VALIDATION
============================================================

Errors:
  - src/main/resources/views/Partner.xml: form[name='partner-form'] - Missing 'id' attribute

Extension views: 2
Valid: 1
Errors: 1

STATUS: FAILED
============================================================
```

## Integration

### In View Generator Agent (Step 3.2)

After XSD validation, validate extension views:

```bash
python3 @skills/axelor-view-extension-validator/axelor_view_extension_validator.py src/main/resources/views/
```

### Validation Order

1. **XSD Validation** (axelor-xml-validator) - Schema compliance
2. **Extension Validation** (this skill) - Extension-specific rules
3. **Naming Conventions** (axelor-naming-checker)
4. **Semantic Validation** (axelor-view-semantic-validator)

## Related

- @docs/views/view-extensions.md - View extension documentation
- @skills/axelor-xml-validator - XSD schema validation
- @skills/axelor-naming-checker - naming checker 
- @skills/axelor-view-semantic-validator - Semantic validation
