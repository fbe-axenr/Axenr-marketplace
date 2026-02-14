# Java Version Detection and Constraints

This guide provides comprehensive information about Java version detection, constraints, and feature compatibility in Axelor Open Platform (AOP) projects.

## Java Version Detection and Constraints

### Automatic Java Version Detection

**Java version is determined by Axelor Open Platform (AOP) version:**

| AOP Version | Java Version | Status |
|-------------|--------------|--------|
| AOP 7.x | Java 11 | Mandatory |
| AOP 8.x | Java 21 | Mandatory |

**Detection Strategy:**

1. Check `build.gradle` for AOP version dependency:
   ```gradle
    dependencies {
       implementation 'com.axelor:axelor-gradle:7.2.0' // → Java 11
       implementation 'com.axelor:axelor-gradle:8.0.0' // → Java 21
   }
    java.sourceCompatibility=11 // → Java 11
    java.sourceCompatibility=21 // → Java 21
   ```

2. Check `gradle.properties` for Java compatibility:
   ```properties
    aosVersion = 7.*.* // → Java 11
    aopVersion = 8.*.* // → Java 21

3. If unclear, **ask the user** to specify AOP version

**Default Assumption:** If AOP version cannot be determined, **generate Java 11 compatible code**.

### Java 11 Features (AOP 7.x - SAFE TO USE)

**String Methods:**
- `isBlank()`, `lines()`, `strip()`, `stripLeading()`, `stripTrailing()`
- `repeat(int count)`

**Collection Factories:**
- `List.of(elements...)`, `Set.of(elements...)`, `Map.of(k1, v1, ...)`
- `List.copyOf(collection)`, `Set.copyOf(collection)`, `Map.copyOf(map)`

**Optional Enhancements:**
- `isEmpty()`, `orElseThrow()`

**Files API:**
- `readString(Path)`, `writeString(Path, String)`

**HttpClient:**
- Standard `java.net.http.HttpClient`, `HttpRequest`, `HttpResponse`

**Local Variable Type Inference:**
- `var` for local variables (use judiciously)

**Example Java 11 code:**
```java
// ✅ SAFE for Java 11
public List<String> getActivePartnerNames(List<Partner> partners) {
    return partners.stream()
        .filter(Partner::getIsActive)
        .map(Partner::getFullName)
        .filter(name -> !name.isBlank())
        .collect(Collectors.toUnmodifiableList());
}

public Optional<SaleOrder> findByOrderNo(String orderNo) {
    SaleOrder order = repository.findOne(orderNo);
    return Optional.ofNullable(order);
}
```

### Java 11 FORBIDDEN Features

**DO NOT USE (Java 12+):**
- Switch expressions with yield
- Text blocks (Java 15)
- Records (Java 16)
- Sealed classes (Java 17)
- Pattern matching for switch (Java 17+)
- Virtual threads (Java 21)
- Sequenced collections (Java 21)

**Example FORBIDDEN for Java 11:**
```java
// ❌ FORBIDDEN: Text blocks (Java 15)
String query = """
    SELECT o FROM SaleOrder o
    WHERE o.status = :status
    """;

// ❌ FORBIDDEN: Records (Java 16)
public record OrderSummary(String orderNo, BigDecimal total) {}

// ❌ FORBIDDEN: Pattern matching (Java 17)
if (obj instanceof SaleOrder order && order.getStatus() == STATUS_DRAFT) {
    // ...
}

// ❌ FORBIDDEN: Switch expressions (Java 14)
int days = switch (status) {
    case DRAFT -> 0;
    case VALIDATED -> 30;
    default -> 60;
};
```

### Java 21 Features (AOP 8.x - AVAILABLE)

**Additional features available on Java 21:**

**Records (Java 16):**
```java
// ✅ AVAILABLE in Java 21
public record OrderSummary(String orderNo, BigDecimal total, LocalDate date) {
    // Compact constructor for validation
    public OrderSummary {
        Objects.requireNonNull(orderNo, "Order number cannot be null");
        Objects.requireNonNull(total, "Total cannot be null");
        Objects.requireNonNull(date, "Date cannot be null");
    }
}
```

**Sealed Classes (Java 17):**
```java
// ✅ AVAILABLE in Java 21
public sealed interface PaymentMethod permits CreditCard, BankTransfer, Cash {
    BigDecimal process(BigDecimal amount);
}

public final class CreditCard implements PaymentMethod {
    // ...
}
```

**Pattern Matching for Switch (Java 21):**
```java
// ✅ AVAILABLE in Java 21
public String getStatusLabel(Object obj) {
    return switch (obj) {
        case SaleOrder order when order.getStatus() == STATUS_DRAFT ->
            "Draft Order: " + order.getOrderNo();
        case SaleOrder order ->
            "Order: " + order.getOrderNo();
        case null -> "No order";
        default -> "Unknown";
    };
}
```

**Text Blocks (Java 15):**
```java
// ✅ AVAILABLE in Java 21
String jpqlQuery = """
    SELECT o
    FROM SaleOrder o
    WHERE o.status = :status
      AND o.orderDate >= :fromDate
    ORDER BY o.orderDate DESC
    """;
```

**Switch Expressions (Java 14):**
```java
// ✅ AVAILABLE in Java 21
int days = switch (status) {
    case DRAFT -> 0;
    case VALIDATED -> 30;
    case INVOICED -> 60;
    default -> throw new IllegalStateException("Unknown status: " + status);
};

// With yield for complex logic
String message = switch (orderType) {
    case SALE -> {
        String prefix = getPrefix();
        yield prefix + ": Sale Order";
    }
    case PURCHASE -> {
        String prefix = getPrefix();
        yield prefix + ": Purchase Order";
    }
    default -> "Unknown Order Type";
};
```

**instanceof Pattern Matching (Java 16):**
```java
// ✅ AVAILABLE in Java 21
// No need to cast after instanceof
if (entity instanceof SaleOrder order) {
    processOrder(order);  // 'order' is directly available
} else if (entity instanceof Partner partner && partner.getIsActive()) {
    processPartner(partner);  // Can combine with conditions
}

// Useful in switch expressions (Java 21)
String processEntity(Object entity) {
    return switch (entity) {
        case SaleOrder order -> "Order: " + order.getOrderNo();
        case Partner partner -> "Partner: " + partner.getFullName();
        case null -> "No entity";
        default -> "Unknown entity type";
    };
}
```

**Sequenced Collections (Java 21):**
```java
// ✅ AVAILABLE in Java 21
// New methods for List, Deque, SortedSet
List<SaleOrderLine> lines = new ArrayList<>();
lines.addFirst(firstLine);   // Add at beginning
lines.addLast(lastLine);      // Add at end

SaleOrderLine first = lines.getFirst();  // Get first element
SaleOrderLine last = lines.getLast();    // Get last element

lines.removeFirst();  // Remove first
lines.removeLast();   // Remove last

// Reverse view (no copy)
List<SaleOrderLine> reversed = lines.reversed();
```

**Virtual Threads (Java 21 - Use with caution):**
```java
// ✅ AVAILABLE but TEST PERFORMANCE
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    executor.submit(() -> process(order));
}
```

### Version-Specific Code Generation Examples

**AOP 7.x (Java 11) - Use traditional class:**
```java
public final class OrderSummary {
    private final String orderNo;
    private final BigDecimal total;
    private final LocalDate date;

    public OrderSummary(String orderNo, BigDecimal total, LocalDate date) {
        this.orderNo = Objects.requireNonNull(orderNo);
        this.total = Objects.requireNonNull(total);
        this.date = Objects.requireNonNull(date);
    }

    public String getOrderNo() { return orderNo; }
    public BigDecimal getTotal() { return total; }
    public LocalDate getDate() { return date; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        OrderSummary that = (OrderSummary) o;
        return Objects.equals(orderNo, that.orderNo) &&
               Objects.equals(total, that.total) &&
               Objects.equals(date, that.date);
    }

    @Override
    public int hashCode() {
        return Objects.hash(orderNo, total, date);
    }

    @Override
    public String toString() {
        return "OrderSummary{" +
               "orderNo='" + orderNo + '\'' +
               ", total=" + total +
               ", date=" + date +
               '}';
    }
}
```

**AOP 8.x (Java 21) - Can use Record:**
```java
public record OrderSummary(String orderNo, BigDecimal total, LocalDate date) {
    // Compact constructor for validation
    public OrderSummary {
        Objects.requireNonNull(orderNo, "Order number cannot be null");
        Objects.requireNonNull(total, "Total cannot be null");
        Objects.requireNonNull(date, "Date cannot be null");
    }
}
```
