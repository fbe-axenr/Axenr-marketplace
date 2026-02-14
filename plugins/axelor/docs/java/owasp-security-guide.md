# OWASP Security Guidelines

This guide provides comprehensive security guidelines based on OWASP Top 10 for Axelor Java development.

## Security Guidelines (OWASP Top 10)

### Overview

**ALL generated Java code MUST follow OWASP security guidelines.**

This section covers the OWASP Top 10 security risks and how to prevent them in Axelor applications.

### A02:2021 - Cryptographic Failures

**Rule**: Use secure cryptography for sensitive data.

**Pattern**:
```java
import java.security.SecureRandom;
import java.util.Base64;

public class SecurityUtils {

    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    // Generate secure random token
    public static String generateSecureToken(int length) {
        if (length <= 0) {
            throw new IllegalArgumentException("Length must be positive");
        }

        byte[] bytes = new byte[length];
        SECURE_RANDOM.nextBytes(bytes);
        return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
    }
}
```

**FORBIDDEN**:
```java
// WRONG: Hardcoded secrets
private static final String API_KEY = "sk-1234567890abcdef"; // NEVER do this

// WRONG: Weak random
Random random = new Random(); // Use SecureRandom instead
```

### A03:2021 - Injection

**Rule**: ALWAYS use parameterized queries. NEVER concatenate user input into queries.

**CORRECT** (Parameterized queries):
```java
// Custom repository extending the AUTO-GENERATED SaleOrderRepository
public class SaleOrderRepo extends SaleOrderRepository {

    public List<SaleOrder> findByCustomerName(String customerName) {
        Objects.requireNonNull(customerName, "Customer name cannot be null");

        // Use parameterized query with :parameter syntax
        return all()
            .filter("self.customer.name = :customerName")
            .bind("customerName", customerName)
            .fetch();
    }

    public List<SaleOrder> findByDateRange(LocalDate startDate, LocalDate endDate) {
        Objects.requireNonNull(startDate, "Start date cannot be null");
        Objects.requireNonNull(endDate, "End date cannot be null");

        // Multiple parameters
        return all()
            .filter("self.orderDate >= :startDate AND self.orderDate <= :endDate")
            .bind("startDate", startDate)
            .bind("endDate", endDate)
            .order("-orderDate")
            .fetch();
    }
}
```

**FORBIDDEN** (SQL Injection vulnerable):
```java
// WRONG: String concatenation - SQL INJECTION RISK!
public List<SaleOrder> findByCustomerName(String customerName) {
    // NEVER DO THIS - vulnerable to SQL injection
    return all()
        .filter("self.customer.name = '" + customerName + "'") // DANGEROUS!
        .fetch();
}

// WRONG: Building queries with user input
public List<SaleOrder> searchOrders(String searchTerm) {
    // NEVER DO THIS
    String filter = "self.saleOrderSeq LIKE '%" + searchTerm + "%'"; // DANGEROUS!
    return all().filter(filter).fetch();
}
```

### A04:2021 - Insecure Design

**Rule**: Validate business logic and state transitions.

**Pattern**:
```java
public class SaleOrderServiceImpl implements SaleOrderService {

    public void confirmOrder(SaleOrder order) throws AxelorException {
        Objects.requireNonNull(order, "Order cannot be null");

        // Validate state transition is allowed
        if (order.getStatusSelect() != STATUS_DRAFT) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                String.format(
                    "Cannot confirm order %s: invalid status %d (must be DRAFT)",
                    order.getSaleOrderSeq(),
                    order.getStatusSelect()
                )
            );
        }

        // Validate business rules
        validateOrderForConfirmation(order);

        // Perform transition
        order.setStatusSelect(STATUS_CONFIRMED);
        order.setConfirmationDate(LocalDate.now());
        order.setConfirmedBy(authUtils.getUser());
    }

    private void validateOrderForConfirmation(SaleOrder order) throws AxelorException {
        // Check customer
        if (order.getCustomer() == null) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                String.format("Order %s has no customer", order.getSaleOrderSeq())
            );
        }

        // Check lines
        if (order.getSaleOrderLineList() == null || order.getSaleOrderLineList().isEmpty()) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                String.format("Order %s has no lines", order.getSaleOrderSeq())
            );
        }

        // Check credit limit
        if (exceedsCreditLimit(order)) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                String.format(
                    "Order %s exceeds customer credit limit",
                    order.getSaleOrderSeq()
                )
            );
        }
    }
}
```

### A05:2021 - Security Misconfiguration

**Rule**: Use secure defaults and validate configuration.

**Pattern**:
```java
public class ConfigService {

    // Secure defaults
    private static final int DEFAULT_MAX_LOGIN_ATTEMPTS = 5;
    private static final int DEFAULT_SESSION_TIMEOUT_MINUTES = 30;
    private static final boolean DEFAULT_ENABLE_2FA = true;

    public int getMaxLoginAttempts() {
        String value = AppSettings.get().get("auth.max.login.attempts");
        if (value == null || value.trim().isEmpty()) {
            return DEFAULT_MAX_LOGIN_ATTEMPTS;
        }

        try {
            int attempts = Integer.parseInt(value);
            if (attempts <= 0 || attempts > 10) {
                // Invalid value, use secure default
                return DEFAULT_MAX_LOGIN_ATTEMPTS;
            }
            return attempts;
        } catch (NumberFormatException e) {
            // Invalid format, use secure default
            return DEFAULT_MAX_LOGIN_ATTEMPTS;
        }
    }
}
```

### A08:2021 - Software and Data Integrity Failures

**Rule**: Validate data integrity and use transactions.

**Pattern**:
```java
import com.google.inject.persist.Transactional;

public class SaleOrderServiceImpl implements SaleOrderService {

    @Transactional(rollbackOn = Exception.class)
    public SaleOrder createOrder(SaleOrder order) throws AxelorException {
        Objects.requireNonNull(order, "Order cannot be null");

        // Validate before save
        validateOrder(order);

        // Save order
        return saleOrderRepo.save(order);
    }

    private void validateOrder(SaleOrder order) throws AxelorException {
        // Version check for concurrent modification
        if (order.getId() != null && order.getVersion() == null) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                "Order version is missing"
            );
        }
    }
}
```

### A09:2021 - Security Logging and Monitoring Failures

**Rule**: Log security-relevant events with sufficient detail.

**Pattern**:
```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SaleOrderServiceImpl implements SaleOrderService {

    private static final Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());

    public void deleteOrder(SaleOrder order) throws AxelorException {
        Objects.requireNonNull(order, "Order cannot be null");

        User currentUser = authUtils.getUser();

        // Log security event BEFORE action
        LOG.info(
            "User {} attempting to delete order {} (ID: {}, Amount: {})",
            currentUser.getCode(),
            order.getSaleOrderSeq(),
            order.getId(),
            order.getExTaxTotal()
        );

        // Perform deletion
        saleOrderRepo.remove(order);

        // Log successful action
        LOG.info(
            "User {} successfully deleted order {} (ID: {})",
            currentUser.getCode(),
            order.getSaleOrderSeq(),
            order.getId()
        );
    }
}
```

**FORBIDDEN**:
```java
// WRONG: Logging sensitive data
LOG.info("User logged in with password: {}", password); // NEVER log passwords

// WRONG: Logging without context
LOG.info("Order deleted"); // No user, no order ID, no context
```

### Summary: Security Enforcement Checklist

When generating Java code, VERIFY:

- [ ] Cryptography: Use SecureRandom, no hardcoded secrets
- [ ] Injection: Parameterized queries ONLY, NEVER string concatenation
- [ ] Business Logic: Validate state transitions and business rules
- [ ] Configuration: Secure defaults, validate configuration values
- [ ] Data Integrity: Use @Transactional, validate referential integrity
- [ ] Logging: Log security events with context (NO sensitive data)
- [ ] NO EMOJIS anywhere
- [ ] ALL code and comments in ENGLISH
