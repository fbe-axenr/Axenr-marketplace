---
name: axelor-xml-validator
description: Validates domain-models and object-views XML files against official Axelor XSD schemas using lxml. Automatically detects file type and version, downloads XSD from axelor.com, and provides comprehensive validation reports.
allowed-tools: ["Bash", "Read", "Write"]
---

# Axelor XML Validator

**✅ PYTHON AUTOMATION AVAILABLE: `axelor_validator.py`**

Use this Python script for automated XSD validation. See Usage section below.

## Mission

Automate comprehensive validation of generated domain and view XML files against official Axelor XSD schemas. This skill uses lxml and official XSD files from axelor.com for strict, production-grade validation.

## Key Features

1. **Automatic Detection**: Detects file type (domain-models vs object-views) and version from XML content
2. **Official XSD**: Downloads and caches official XSD schemas from axelor.com
3. **Comprehensive Validation**: Uses lxml for complete XSD validation (elements, attributes, types, enumerations)
4. **Smart Caching**: Caches XSD files locally to avoid repeated downloads
5. **Detailed Reports**: Provides line numbers, error descriptions, and validation paths

## Validation Coverage

- XML syntax correctness
- Element existence and hierarchy
- Attribute validity and types
- Required attribute presence
- Enumeration value correctness
- Type constraints (boolean, integer, string, patterns)
- Schema version compatibility

## Usage

### Validate Single File

```bash
python3 axelor_validator.py path/to/domain.xml
python3 axelor_validator.py path/to/view.xml
```

### Validate with Specific Parameters

```bash
# Force specific type and version
python3 axelor_validator.py domain.xml --type domain-models --version 7.4

# Use local XSD file
python3 axelor_validator.py domain.xml --xsd local-schema.xsd

# No caching
python3 axelor_validator.py domain.xml --no-cache

# Verbose output
python3 axelor_validator.py domain.xml -v
```

## Integration in Generation Workflow

Call this skill after domain or view generation:

```
domain-agent
  ↓
axelor-xml-validator (XSD strict validation - Official)
  ↓
axelor-naming-checker (naming conventions)
  ↓
axelor-semantic-validator (semantic + cross-entity)
  ↓
generateCode
```

```
view-agent
  ↓
axelor-xml-validator (XSD strict validation - Official)
  ↓
axelor-view-semantic-validator (semantic + field existence)
  ↓
generateCode
```

## Output Format

Comprehensive validation report with line numbers and detailed error messages:

```
======================================================================
VALIDATION AXELOR XML
======================================================================
Fichier: Customer.xml

Type detecte: domain-models
Version detectee: 7.4

Utilisation du schema en cache: .cache/domain-models_7.4.xsd

======================================================================
VALIDATION EN COURS...
======================================================================

======================================================================
RESULTAT DE LA VALIDATION
======================================================================

Le fichier XML N'EST PAS conforme au schema XSD

   Type: domain-models
   Version: 7.4
   Nombre d'erreurs: 2

----------------------------------------------------------------------

Erreur 1/2:
   Ligne 23, Colonne 15
   Element 'string': Invalid attribute 'precision' for element 'string'.
   Chemin: /domain-models/module/entity[1]/string[3]

Erreur 2/2:
   Ligne 45, Colonne 8
   Element 'decimal', attribute 'scale': 'abc' is not a valid value of the atomic type 'xs:integer'.
   Chemin: /domain-models/module/entity[2]/decimal[1]

======================================================================
```

## Requirements

### Python Version
- Python 3.8+

### Dependencies
- lxml (for XML/XSD processing)
- requests (for downloading XSD schemas)

Install dependencies:
```bash
pip install -r requirements.txt
```

## When to Use This Skill

**ALWAYS use this skill after generating:**
- Domain XML files (by domain-agent)
- View XML files (by view-agent)

**Use BEFORE:**
- Semantic validation skills
- Naming convention checks
- Code generation

## Error Categories

1. **Syntax Errors**: Malformed XML, unclosed tags
2. **Element Errors**: Unknown elements, invalid hierarchy
3. **Attribute Errors**: Invalid attributes, wrong types, missing required
4. **Type Errors**: Value type mismatches (integer, boolean, etc.)
5. **Enumeration Errors**: Invalid enumeration values
6. **Version Errors**: Schema version incompatibility

## Supported Versions

The validator supports all Axelor versions that have published XSD schemas:
- 7.0, 7.1, 7.2, 7.3, 7.4
- 8.0, 8.1, 8.2 (and future versions)

Version is auto-detected from XML or can be manually specified.

## Cache Management

XSD files are cached in `.cache/` directory to avoid repeated downloads:

```
.cache/
├── domain-models_7.4.xsd
├── domain-models_8.0.xsd
├── object-views_7.4.xsd
└── object-views_8.0.xsd
```

Use `--no-cache` to bypass caching for testing.

## Examples

### Example 1: Validate Generated Domain

```bash
# After domain generation
python3 axelor_validator.py src/main/resources/domains/Customer.xml
```

### Example 2: Validate All Views in Directory

```bash
# Validate multiple view files
for view in src/main/resources/views/*.xml; do
    python3 axelor_validator.py "$view"
done
```

### Example 3: Integration with Agent

In domain-agent or view-agent agent, after file generation:

```markdown
Step X: Validate generated XML
- Use axelor-xml-validator skill
- Command: python3 @skills/axelor-xml-validator/axelor_validator.py {generated_file}
- Check exit code: 0 = valid, 1 = invalid
- If invalid, report errors and fix generation
```

## Best Practices

1. **Always validate immediately after generation** to catch errors early
2. **Use automatic detection** for type and version when possible
3. **Check exit code** in automation scripts (0 = success, 1 = failure)
4. **Fix XSD errors first** before running semantic validators
5. **Keep XSD cache** to improve performance in CI/CD pipelines

**Recommendation**: Use axelor-xml-validator as primary validator for strict XSD compliance, then use semantic validators for business logic checks.
