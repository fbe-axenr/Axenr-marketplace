---
name: axelor-java-style-validator
description: Validates Java files against Axelor code style rules. CRITICAL checks for NO EMOJI and ENGLISH ONLY. Enforces naming conventions (PascalCase, camelCase, UPPER_SNAKE_CASE) and import organization.
allowed-tools: ["Bash", "Read"]
---

# Axelor Java Style Validator

**✅ PYTHON AUTOMATION AVAILABLE: `java_style_validator.py`**

Use this Python script for automated validation. See Usage section below.

## Mission

Validate generated Java code against Axelor code style rules with CRITICAL focus on:
1. **NO EMOJI** anywhere in code (comments, strings, logs, documentation)
2. **ENGLISH ONLY** (no French or other languages)
3. **Naming conventions** (PascalCase, camelCase, UPPER_SNAKE_CASE)
4. **Import organization** (no wildcards except java.util.*)

## Critical Rules

### Rule 1: NO EMOJI (CRITICAL)

**Severity**: ERROR

**What it checks**:
- ❌ Emoji in comments
- ❌ Emoji in string literals
- ❌ Emoji in log messages
- ❌ Emoji in JavaDoc
- ❌ Emoji anywhere in Java files

**Examples**:
```java
// WRONG
LOG.info("Order created successfully ✅");
throw new AxelorException("Invalid data ⚠️");

// CORRECT
LOG.info("Order created successfully");
throw new AxelorException("Invalid data");
```

### Rule 2: ENGLISH ONLY (CRITICAL)

**Severity**: ERROR

**What it checks**:
- ❌ French text in comments
- ❌ French text in strings
- ❌ French text in log messages
- ❌ French text in exception messages

**Common French patterns detected**:
- "Commande créée", "Erreur", "Succès", "Échec"
- "Client", "Produit", "Facture", "Montant"
- "Créé", "Modifié", "Supprimé", "Validé"

**Examples**:
```java
// WRONG
LOG.info("Commande créée avec succès");
throw new AxelorException("Le champ est obligatoire");

// CORRECT
LOG.info("Order created successfully");
throw new AxelorException(I18n.get("Field is required"));
```

### Rule 3: Naming Conventions

**Class Names**: PascalCase (ERROR if violated)
```java
// WRONG
public class saleOrder { }

// CORRECT
public class SaleOrder { }
```

**Method Names**: camelCase (ERROR if PascalCase)
```java
// WRONG
public void CreateOrder() { }

// CORRECT
public void createOrder() { }
```

**Constants**: UPPER_SNAKE_CASE (WARNING if violated)
```java
// WARNING
private static final int maxRetries = 3;

// CORRECT
private static final int MAX_RETRIES = 3;
```

### Rule 4: Import Organization

**No Wildcard Imports** (except java.util.*)

**Severity**: WARNING

```java
// ⚠️ WARNING
import com.axelor.apps.sale.*;

// ✅ CORRECT
import com.axelor.apps.sale.db.SaleOrder;
import com.axelor.apps.sale.service.SaleOrderService;

// ✅ ALLOWED
import java.util.*;
```

## Usage

### Validate Single File

```bash
python3 java_style_validator.py src/main/java/com/axelor/apps/sale/service/SaleOrderService.java
```

### Validate Directory (Recursive)

```bash
python3 java_style_validator.py src/main/java/
```

### Validate Current Directory

```bash
python3 java_style_validator.py .
```

### Verbose Mode

```bash
python3 java_style_validator.py src/ --verbose
```

## Integration in Java Generation Workflow

```
axelor-service-generator (generate service)
  ↓
✅ axelor-java-style-validator (validate style)
  ↓
✅ axelor-java-pattern-validator (validate patterns)
  ↓
./gradlew build
```

## Output Format

### No Violations

```
======================================================================
AXELOR JAVA STYLE VALIDATION REPORT
======================================================================

✅ NO VIOLATIONS FOUND

All files comply with Axelor style rules:
  ✓ NO EMOJI
  ✓ ENGLISH ONLY
  ✓ Naming conventions correct
  ✓ Import organization correct
======================================================================
```

### With Violations

```
======================================================================
AXELOR JAVA STYLE VALIDATION REPORT
======================================================================

📁 File: src/main/java/com/axelor/apps/sale/service/impl/SaleOrderServiceImpl.java
----------------------------------------------------------------------
❌ Line 45: [NO_EMOJI] Emoji detected in code (CRITICAL VIOLATION)
   → LOG.info("Order created ✅");
❌ Line 67: [ENGLISH_ONLY] Possible French text detected (pattern: \bcréé\b)
   → throw new AxelorException("Commande créée");
⚠️ Line 23: [CONSTANT_NAMING] Constant should be UPPER_SNAKE_CASE: maxRetries
   → private static final int maxRetries = 3;

======================================================================
SUMMARY
======================================================================
Files checked: 1
❌ Errors: 2
⚠️  Warnings: 1

🚨 CRITICAL: Fix all errors before committing!

Most common errors:
  1. Emoji in code → Remove all emoji
  2. French text → Translate to English
  3. Wrong naming → Use PascalCase/camelCase/UPPER_SNAKE_CASE
======================================================================
```

## Exit Codes

- `0` = No violations (all checks passed)
- `1` = Violations found (errors or warnings)
- `2` = Error during validation (file not found, permission error, etc.)

## Command Line Options

```
usage: java_style_validator.py [-h] [-v] path

positional arguments:
  path           File or directory to validate

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Verbose output
```

## Integration Examples

### In Bash Script

```bash
#!/bin/bash

# Validate style
python3 java_style_validator.py src/main/java/com/axelor/apps/sale/

# Check exit code
if [ $? -ne 0 ]; then
  echo "Style validation failed!"
  exit 1
fi

echo "Style validation passed!"
```

### In Python

```python
import subprocess

# Generate service
subprocess.run([
    "python3", "service_generator.py",
    "SaleOrder", "sale"
])

# Validate style
result = subprocess.run([
    "python3", "java_style_validator.py",
    "src/main/java/"
])

if result.returncode != 0:
    print("Style validation failed!")
    sys.exit(1)
```

## What Gets Validated

✅ **Checked**:
- Emoji presence (anywhere in file)
- French text patterns (in strings/comments)
- Class naming (PascalCase)
- Method naming (camelCase vs PascalCase)
- Constant naming (UPPER_SNAKE_CASE)
- Import wildcards (except java.util.*)

❌ **Not Checked** (use other validators):
- Logger pattern (use axelor-java-pattern-validator)
- @Transactional placement (use axelor-java-pattern-validator)
- Security patterns (use axelor-security-validator)
- Module bindings (use axelor-module-binding-validator)

## Common Violations and Fixes

### Violation 1: Emoji in Logs

```java
// ❌ WRONG
LOG.info("Operation completed successfully ✅");
LOG.error("Operation failed ❌");

// ✅ FIX
LOG.info("Operation completed successfully");
LOG.error("Operation failed");
```

### Violation 2: French Messages

```java
// ❌ WRONG
throw new AxelorException(
    TraceBackRepository.CATEGORY_MISSING_FIELD,
    "Le champ est obligatoire");

// ✅ FIX
throw new AxelorException(
    TraceBackRepository.CATEGORY_MISSING_FIELD,
    I18n.get("Field is required"));
```

### Violation 3: Wrong Class Naming

```java
// ❌ WRONG
public class saleOrderService { }

// ✅ FIX
public class SaleOrderService { }
```

### Violation 4: Wrong Method Naming

```java
// ❌ WRONG
public void CreateOrder() { }

// ✅ FIX
public void createOrder() { }
```

### Violation 5: Wrong Constant Naming

```java
// ⚠️ WARNING
private static final int maxRetries = 3;

// ✅ FIX
private static final int MAX_RETRIES = 3;
```

## False Positives

The French detection may occasionally flag English words that look like French. Review warnings carefully:

```java
// May be flagged (false positive)
String error = "Invalid date format";  // "date" exists in French

// To avoid false positives
String error = "Invalid datetime format";  // Use "datetime" instead
```

## Performance

- **Fast**: ~1000 files/second
- **Memory**: Low memory footprint
- **Recursive**: Scans entire directory trees

## Dependencies

- Python 3.6+
- No external libraries (standard library only)

## Related Skills

- **axelor-service-generator**: Generate services (to be validated)
- **axelor-java-pattern-validator**: Validate Axelor patterns (Logger, @Transactional)
- **axelor-security-validator**: Validate security patterns (OWASP)
- **axelor-module-binding-validator**: Validate Module.java bindings

## Notes

- This validator runs BEFORE compilation
- Catches style issues early in the development cycle
- Prevents NO EMOJI and ENGLISH ONLY violations from reaching production
- Complements other validators (pattern, security, binding)

## Testing

Test the validator with intentionally bad code:

```java
// test-bad-style.java
public class saleOrder {  // Wrong: camelCase class
  private static final int maxRetries = 3;  // Wrong: not UPPER_SNAKE_CASE

  public void CreateOrder() {  // Wrong: PascalCase method
    LOG.info("Commande créée ✅");  // Wrong: French + emoji
  }
}
```

Run validator:
```bash
python3 java_style_validator.py test-bad-style.java
```

Expected: 4 violations (class naming, method naming, constant naming, emoji + French)
