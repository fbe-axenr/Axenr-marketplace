# Performance Guidelines

This guide provides comprehensive performance best practices for Axelor Java development.

## Performance Guidelines

### Overview

**ALL generated Java code MUST follow performance best practices.**

This section covers common performance patterns and anti-patterns for Axelor applications.

### Database Performance

#### N+1 Query Problem

**Rule**: Avoid N+1 queries when accessing related entities.

**CORRECT**:
```java
// Custom repository extending the AUTO-GENERATED SaleOrderRepository
public class SaleOrderRepo extends SaleOrderRepository {

    public List<SaleOrder> findAllWithCustomer() {
        // Single query with JOIN FETCH
        return all()
            .filter("self.statusSelect != :cancelled")
            .bind("cancelled", STATUS_CANCELLED)
            .fetch();
    }

    public SaleOrder findByIdWithLines(Long id) {
        Objects.requireNonNull(id, "ID cannot be null");

        // Fetch order with lines in single query
        return all()
            .filter("self.id = :id")
            .bind("id", id)
            .fetchOne();
    }
}
```

**FORBIDDEN** (N+1 queries):
```java
// WRONG: This will cause N+1 queries
public void processOrders() {
    List<SaleOrder> orders = saleOrderRepo.all().fetch();

    for (SaleOrder order : orders) {
        // Each iteration triggers separate query for customer
        String customerName = order.getCustomer().getName(); // N+1!

        // Each iteration triggers separate query for lines
        List<SaleOrderLine> lines = order.getSaleOrderLineList(); // N+1!
    }
}
```

#### Batch Processing

**Rule**: Process large datasets in batches to avoid memory issues.

**Pattern**:
```java
public class SaleOrderServiceImpl implements SaleOrderService {

    private static final int BATCH_SIZE = 100;

    public void processPendingOrders() {
        int offset = 0;
        List<SaleOrder> batch;

        do {
            // Fetch batch
            batch = saleOrderRepo.all()
                .filter("self.statusSelect = :status")
                .bind("status", STATUS_PENDING)
                .order("id")
                .fetch(BATCH_SIZE, offset);

            // Process batch
            for (SaleOrder order : batch) {
                processOrder(order);
            }

            // Clear persistence context to free memory
            JPA.em().flush();
            JPA.em().clear();

            offset += BATCH_SIZE;

        } while (batch.size() == BATCH_SIZE);
    }
}
```

#### Query Optimization

**Rule**: Use indexes, limit results, and select only needed fields.

**Pattern**:
```java
// Custom repository extending the AUTO-GENERATED SaleOrderRepository
public class SaleOrderRepo extends SaleOrderRepository {

    public List<SaleOrder> findRecentOrders(int limit) {
        if (limit <= 0 || limit > 1000) {
            throw new IllegalArgumentException(
                String.format("Limit must be between 1 and 1000, got: %d", limit)
            );
        }

        return all()
            .filter("self.orderDate >= :thirtyDaysAgo")
            .bind("thirtyDaysAgo", LocalDate.now().minusDays(30))
            .order("-orderDate")
            .fetch(limit);
    }

    public long countOrdersByStatus(Integer status) {
        Objects.requireNonNull(status, "Status cannot be null");

        // Use count() instead of fetching all records
        return all()
            .filter("self.statusSelect = :status")
            .bind("status", status)
            .count();
    }
}
```

### Collection Performance

#### Use Appropriate Collection Types

**Rule**: Choose the right collection type for the use case.

**Pattern**:
```java
public class SaleOrderServiceImpl implements SaleOrderService {

    // Use ArrayList for frequent index access
    public List<SaleOrderLine> sortLinesBySequence(List<SaleOrderLine> lines) {
        Objects.requireNonNull(lines, "Lines cannot be null");

        List<SaleOrderLine> sorted = new ArrayList<>(lines);
        sorted.sort(Comparator.comparing(SaleOrderLine::getSequence));
        return sorted;
    }

    // Use HashSet for uniqueness and fast lookup
    public Set<Product> getUniqueProducts(List<SaleOrderLine> lines) {
        Objects.requireNonNull(lines, "Lines cannot be null");

        Set<Product> products = new HashSet<>();
        for (SaleOrderLine line : lines) {
            if (line.getProduct() != null) {
                products.add(line.getProduct());
            }
        }
        return products;
    }

    // Use HashMap for key-value lookups
    public Map<Product, BigDecimal> getTotalQuantityByProduct(List<SaleOrderLine> lines) {
        Objects.requireNonNull(lines, "Lines cannot be null");

        Map<Product, BigDecimal> quantities = new HashMap<>();
        for (SaleOrderLine line : lines) {
            if (line.getProduct() != null && line.getQuantity() != null) {
                quantities.merge(
                    line.getProduct(),
                    line.getQuantity(),
                    BigDecimal::add
                );
            }
        }
        return quantities;
    }
}
```

#### Stream API Performance

**Rule**: Use streams judiciously; traditional loops can be faster for simple operations.

**Pattern**:
```java
public class SaleOrderServiceImpl implements SaleOrderService {

    // Use streams for complex transformations
    public List<InvoiceLine> convertLinesToInvoiceLines(List<SaleOrderLine> orderLines) {
        Objects.requireNonNull(orderLines, "Order lines cannot be null");

        return orderLines.stream()
            .filter(line -> line.getProduct() != null)
            .filter(line -> line.getQuantity().compareTo(BigDecimal.ZERO) > 0)
            .map(this::convertToInvoiceLine)
            .collect(Collectors.toList());
    }

    // Use traditional loops for simple iterations
    public BigDecimal computeTotal(List<SaleOrderLine> lines) {
        Objects.requireNonNull(lines, "Lines cannot be null");

        BigDecimal total = BigDecimal.ZERO;
        for (SaleOrderLine line : lines) {
            if (line.getExTaxTotal() != null) {
                total = total.add(line.getExTaxTotal());
            }
        }
        return total;
    }
}
```

### String Performance

#### Avoid String Concatenation in Loops

**Rule**: Use StringBuilder for string concatenation in loops.

**CORRECT**:
```java
public String generateOrderSummary(List<SaleOrderLine> lines) {
    Objects.requireNonNull(lines, "Lines cannot be null");

    StringBuilder summary = new StringBuilder();
    summary.append("Order Summary:\n");

    for (SaleOrderLine line : lines) {
        summary.append("- ")
            .append(line.getProduct().getName())
            .append(": ")
            .append(line.getQuantity())
            .append(" x ")
            .append(line.getPrice())
            .append("\n");
    }

    return summary.toString();
}
```

**FORBIDDEN**:
```java
// WRONG: String concatenation in loop
public String generateOrderSummary(List<SaleOrderLine> lines) {
    String summary = "Order Summary:\n";

    for (SaleOrderLine line : lines) {
        // Each += creates a new String object
        summary += "- " + line.getProduct().getName() + ": " +
            line.getQuantity() + " x " + line.getPrice() + "\n";
    }

    return summary;
}
```

### BigDecimal Performance

#### Reuse BigDecimal Constants

**Rule**: Reuse common BigDecimal constants instead of creating new instances.

**CORRECT**:
```java
public class SaleOrderServiceImpl implements SaleOrderService {

    // Reusable constants
    private static final BigDecimal HUNDRED = new BigDecimal("100");
    private static final BigDecimal DISCOUNT_RATE = new BigDecimal("0.05");

    public BigDecimal applyDiscount(BigDecimal amount) {
        Objects.requireNonNull(amount, "Amount cannot be null");

        if (amount.compareTo(HUNDRED) < 0) {
            return amount;
        }

        // Reuse constant
        return amount.multiply(BigDecimal.ONE.subtract(DISCOUNT_RATE));
    }
}
```

**FORBIDDEN**:
```java
// WRONG: Creating new BigDecimal in each call
public BigDecimal applyDiscount(BigDecimal amount) {
    if (amount.compareTo(new BigDecimal("100")) < 0) { // Creates new object
        return amount;
    }
    return amount.multiply(new BigDecimal("0.95")); // Creates new object
}
```

### Caching

#### Use Caching for Expensive Operations

**Rule**: Cache results of expensive computations or database queries.

**Pattern**:
```java
public class ConfigService {

    private static final int CACHE_DURATION_SECONDS = 300; // 5 minutes

    private volatile Company defaultCompany;
    private volatile long defaultCompanyCacheTime;

    public Company getDefaultCompany() {
        long now = System.currentTimeMillis();

        // Check if cache is valid
        if (defaultCompany != null
            && (now - defaultCompanyCacheTime) < CACHE_DURATION_SECONDS * 1000) {
            return defaultCompany;
        }

        // Cache miss or expired, reload
        synchronized (this) {
            // Double-check after acquiring lock
            if (defaultCompany != null
                && (now - defaultCompanyCacheTime) < CACHE_DURATION_SECONDS * 1000) {
                return defaultCompany;
            }

            // Load from database
            defaultCompany = companyRepo.all()
                .filter("self.defaultCompany = true")
                .fetchOne();

            defaultCompanyCacheTime = System.currentTimeMillis();

            if (defaultCompany == null) {
                throw new IllegalStateException("No default company configured");
            }

            return defaultCompany;
        }
    }

    public void clearCache() {
        defaultCompany = null;
        defaultCompanyCacheTime = 0;
    }
}
```

### Lazy Initialization

#### Use Lazy Initialization for Expensive Resources

**Rule**: Initialize expensive resources only when needed.

**Pattern**:
```java
public class ReportService {

    private volatile ReportEngine reportEngine;

    private ReportEngine getReportEngine() {
        if (reportEngine == null) {
            synchronized (this) {
                if (reportEngine == null) {
                    reportEngine = createReportEngine();
                }
            }
        }
        return reportEngine;
    }

    private ReportEngine createReportEngine() {
        // Expensive initialization
        return new ReportEngine();
    }
}
```

### Summary: Performance Enforcement Checklist

When generating Java code, VERIFY:

- [ ] Database: Use JOIN FETCH to avoid N+1 queries
- [ ] Database: Process large datasets in batches (100-1000 records)
- [ ] Database: Use count() instead of fetching all records
- [ ] Database: Limit query results (max 1000)
- [ ] Collections: Use appropriate types (ArrayList, HashSet, HashMap)
- [ ] Collections: Use streams for complex transformations only
- [ ] Strings: Use StringBuilder for concatenation in loops
- [ ] BigDecimal: Reuse constants instead of creating new instances
- [ ] Caching: Cache expensive computations or database queries
- [ ] Lazy Init: Initialize expensive resources only when needed
- [ ] NO EMOJIS anywhere
- [ ] ALL code and comments in ENGLISH
