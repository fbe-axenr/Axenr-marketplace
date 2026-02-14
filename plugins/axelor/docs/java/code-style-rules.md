# Java Code Style Rules for Axelor

## Overview

This document defines STRICT code style rules that MUST be followed when generating Java code for Axelor projects. These are ZERO TOLERANCE rules - any violation is considered a critical failure.

---

## NO EMOJI RULE (ZERO TOLERANCE - CRITICAL)

**EMOJIS ARE STRICTLY FORBIDDEN** in all generated Java code.

**This is a CRITICAL requirement. Any emoji found = immediate failure.**

### Forbidden Locations

Emojis are FORBIDDEN in:
- Java source code (any .java file)
- Comments (// or /* */ or /** */)
- JavaDoc documentation (@param, @return, @throws, class/method descriptions)
- String literals ("text")
- Log messages (logger.info, logger.debug, logger.error, etc.)
- Exception messages (throw new Exception("message"))
- Constants (names or values)
- Variable names, method names, class names, package names

### Common Emojis to NEVER Use

❌ ✅ ✓ ✗ ☑ ☒ 🎉 👍 👎 📦 🚀 💡 ⚡ ⚠ 🔥 💾 📝 📊 💰 ✨ 🔧 🎯 📈 📉 ⏰ 🌟

### Example Violations (FORBIDDEN)

```java
// ❌ CRITICAL VIOLATION: Emojis in code
logger.info("Order validated ✅");
logger.error("Processing failed ❌: {}", error);
String message = "Success 🎉";
throw new AxelorException("Error ❌: Invalid status");
// Process order 📦
// Calculate total 💰

/**
 * Validates order ✅
 * @return true if valid ✓
 */
public void validate() { }
```

### Correct Code (MANDATORY)

```java
// ✅ CORRECT: Plain text only
logger.info("Order validated successfully");
logger.error("Processing failed: {}", error);
String message = "Operation completed successfully";
throw new AxelorException("Validation error: Invalid status");
// Process order and update status
// Calculate total amount

/**
 * Validates the sale order and updates its status to VALIDATED.
 * @return true if order is valid, false otherwise
 */
public void validate() { }
```

---

## ENGLISH ONLY RULE (ZERO TOLERANCE - HIGH)

**All code and comments MUST be in English.**

**This is a HIGH priority requirement. Any non-English code = immediate fix required.**

### English Required In

- Class names: `SaleOrder` not `CommandeVente`
- Method names: `computeTotal()` not `calculerTotal()`
- Variable names: `totalAmount` not `montantTotal`
- Parameter names: `orderDate` not `dateCommande`
- Field names: `lineCount` not `nombreLignes`
- Comments: `// Validate input` not `// Valider l'entrée`
- JavaDoc: English descriptions
- Exception messages: English
- Log messages: English
- Constants: `MAX_RETRY_COUNT` not `NOMBRE_MAX_ESSAIS`

### Example Violations (FORBIDDEN)

```java
// ❌ HIGH VIOLATION: French in code
public class CommandeVente {
    private BigDecimal montantTotal;
    private Integer nombreLignes;

    // Calcule le total avec remise
    public BigDecimal calculerTotal() {
        logger.info("Début du calcul");
        throw new AxelorException("Erreur de validation");
    }
}
```

### Correct Code (MANDATORY)

```java
// ✅ CORRECT: English only
public class SaleOrder {
    private BigDecimal totalAmount;
    private Integer lineCount;

    /**
     * Computes the total amount applying discount.
     * @return the computed total
     */
    public BigDecimal computeTotal() {
        logger.info("Starting total computation");
        throw new AxelorException("Validation error");
    }
}
```

### i18n Note

User-facing labels are translated via i18n CSV files, but code MUST remain English:

```java
// ✅ CORRECT: English code + i18n for UI
response.setFlash(I18n.get("order.validated.successfully"));
// i18n key "order.validated.successfully" will display:
// - "Order validated successfully" in English UI
// - "Commande validée avec succès" in French UI
```

---

## Naming Conventions

### Classes and Interfaces

**Rule**: Use PascalCase for class and interface names.

```java
public class SaleOrderService { }
public interface InvoiceRepository { }
public class CustomerDTO { }
```

### Methods and Variables

**Rule**: Use camelCase for method names and variables.

```java
private BigDecimal totalAmount;
private LocalDate orderDate;

public void computeTotalAmount() { }
public Customer findCustomerById(Long customerId) { }
```

### Constants

**Rule**: Use UPPER_SNAKE_CASE for constants.

```java
public static final int STATUS_DRAFT = 1;
public static final int STATUS_CONFIRMED = 2;
public static final String DEFAULT_CURRENCY_CODE = "EUR";
private static final int MAX_RETRY_ATTEMPTS = 3;
```

### Packages

**Rule**: Use lowercase for package names.

```java
package com.axelor.apps.sale.service;
package com.axelor.apps.account.db.repo;
```

---

## Magic Numbers and String Literals

**Rule**: NEVER use magic numbers or magic strings. Use named constants.

### Correct Pattern

```java
public class SaleOrder {

    // Named constants for status
    public static final int STATUS_DRAFT = 1;
    public static final int STATUS_CONFIRMED = 2;
    public static final int STATUS_FINISHED = 3;
    public static final int STATUS_CANCELLED = 4;

    // Named constants for business rules
    private static final BigDecimal MIN_ORDER_AMOUNT = new BigDecimal("100.00");
    private static final int MAX_LINES_PER_ORDER = 1000;
    private static final int DISCOUNT_THRESHOLD_DAYS = 30;

    public void validateOrder() throws AxelorException {
        if (this.statusSelect != STATUS_DRAFT) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                String.format("Cannot validate order in status %d", this.statusSelect)
            );
        }

        if (this.exTaxTotal.compareTo(MIN_ORDER_AMOUNT) < 0) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                String.format(
                    "Order amount %.2f is below minimum %.2f",
                    this.exTaxTotal,
                    MIN_ORDER_AMOUNT
                )
            );
        }
    }
}
```

### Forbidden Pattern

```java
// ❌ WRONG: Magic numbers and strings
public void validateOrder() throws AxelorException {
    if (this.statusSelect != 1) { // What is 1?
        throw new AxelorException(
            TraceBackRepository.CATEGORY_INCONSISTENCY,
            "Cannot validate order"
        );
    }

    if (this.exTaxTotal.compareTo(new BigDecimal("100.00")) < 0) { // What is 100.00?
        throw new AxelorException(
            TraceBackRepository.CATEGORY_INCONSISTENCY,
            "Order amount too low"
        );
    }
}
```

---

## Code Style Enforcement Checklist

When generating Java code, VERIFY:

- [ ] NO EMOJIS anywhere (CRITICAL)
- [ ] ALL code and comments in ENGLISH (HIGH)
- [ ] PascalCase for classes and interfaces
- [ ] camelCase for methods and variables
- [ ] UPPER_SNAKE_CASE for constants
- [ ] lowercase for packages
- [ ] NO magic numbers (use named constants)
- [ ] NO magic strings (use constants or i18n keys)
- [ ] Descriptive variable names (no abbreviations like `amt`, use `amount`)
- [ ] Consistent formatting (indentation, spacing)

---

## Common Violations and Fixes

| Violation | Fix |
|-----------|-----|
| `logger.info("✅ Success")` | `logger.info("Operation successful")` |
| `// Valider l'entrée` | `// Validate input` |
| `if (status == 1)` | `if (status == STATUS_DRAFT)` |
| `BigDecimal amt` | `BigDecimal amount` |
| `private String Nom` | `private String name` |
| `public void PROCESS()` | `public void process()` |

---

**Remember**: Code style violations are immediate failures. Always double-check before committing generated code.
