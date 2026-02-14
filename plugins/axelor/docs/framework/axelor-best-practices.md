# Best Practices Développement Axelor

## Génération de code

### ✅ Bonnes pratiques

```bash
# Toujours générer après modification XML
./gradlew generateCode

# Vérifier que la génération a réussi
echo $?  # Doit retourner 0

# Régénérer + compiler + tester en une commande
./gradlew clean generateCode build
```

### ❌ Erreurs fréquentes

```bash
# ❌ Oublier de régénérer après changement XML
# → Code Java pas à jour avec modèle

# ❌ Modifier directement build/src-gen/
# → Changements écrasés à prochaine génération

# ❌ Commit build/src-gen/ dans Git
# → Conflits et code incohérent
```

### Pattern de travail recommandé

1. Modifier `domains/Customer.xml`
2. Lancer `./gradlew generateCode`
3. Vérifier compilation OK
4. Implémenter service si nécessaire
5. Tester
6. Commit (XML uniquement, pas src-gen)

## Design des domaines

### Héritage et réutilisation

```xml
<!-- ✅ CORRECT : Hériter de AuditableModel pour champs audit -->
<entity name="Customer">
  <string name="code"/>
  <!-- createdOn, createdBy, updatedOn, updatedBy auto-ajoutés -->
</entity>

<!-- ❌ INCORRECT : Redéfinir champs audit manuellement -->
<entity name="Customer">
  <string name="code"/>
  <datetime name="createdOn"/>  <!-- Déjà dans AuditableModel -->
  <many-to-one name="createdBy" ref="User"/>  <!-- Déjà inclus -->
</entity>
```

###Relations bidirectionnelles

```xml
<!-- ✅ CORRECT : Définir les deux côtés de la relation -->
<!-- Customer.xml -->
<entity name="Customer">
  <one-to-many name="orders" ref="Order" mappedBy="customer"/>
</entity>

<!-- Order.xml -->
<entity name="Order">
  <many-to-one name="customer" ref="Customer"/>
</entity>

<!-- ❌ INCORRECT : Oublier mappedBy -->
<entity name="Customer">
  <one-to-many name="orders" ref="Order"/>  <!-- Manque mappedBy -->
</entity>
```

### Performance : Lazy vs Eager loading

```xml
<!-- ✅ CORRECT : Lazy par défaut pour collections -->
<entity name="Customer">
  <one-to-many name="orders" ref="Order" mappedBy="customer"/>
  <!-- fetchType="LAZY" par défaut (bon) -->
</entity>

<!-- ⚠️ ATTENTION : Eager si besoin accès systématique -->
<entity name="Order">
  <many-to-one name="customer" ref="Customer" fetchType="EAGER"/>
  <!-- Charger customer avec order (peut être utile) -->
</entity>

<!-- ❌ INCORRECT : Eager sur collections volumineuses -->
<entity name="Customer">
  <one-to-many name="orders" ref="Order" mappedBy="customer" fetchType="EAGER"/>
  <!-- Performance problem si customer a 1000+ orders -->
</entity>
```

### Indexes pour performance

```xml
<!-- ✅ CORRECT : Index sur champs recherchés/filtrés fréquemment -->
<entity name="Customer">
  <string name="code" unique="true"/>
  <string name="fullName"/>
  <integer name="statusSelect"/>
  <many-to-one name="company" ref="Company"/>

  <!-- Index sur code (unique l'ajoute automatiquement) -->
  <index columns="code"/>

  <!-- Index sur champs de filtre -->
  <index columns="statusSelect"/>
  <index columns="company"/>

  <!-- Index composite pour requêtes complexes -->
  <index columns="company,statusSelect"/>
</entity>

<!-- ❌ INCORRECT : Trop d'index (ralentit INSERT/UPDATE) -->
<index columns="createdOn"/>  <!-- Rarement utilisé -->
<index columns="description"/>  <!-- Champ texte long -->
```

## Services métier

### Séparation des responsabilités

```java
// CORRECT: Service focused on business logic with constructor injection
public class CustomerServiceImpl implements CustomerService {

  private final CustomerRepository customerRepository;
  private final SequenceService sequenceService;

  @Inject
  public CustomerServiceImpl(
      CustomerRepository customerRepository,
      SequenceService sequenceService) {
    this.customerRepository = customerRepository;
    this.sequenceService = sequenceService;
  }

  @Transactional
  public Customer create(Customer customer) throws AxelorException {
    // Validation
    validate(customer);

    // Génération automatique
    if (customer.getCode() == null) {
      customer.setCode(sequenceService.getSequenceNumber("customer"));
    }

    // Logique métier
    customer.setStatusSelect(CustomerStatus.ACTIVE);

    // Persist
    return customerRepository.save(customer);
  }

  protected void validate(Customer customer) throws AxelorException {
    if (StringUtils.isEmpty(customer.getFullName())) {
      throw new AxelorException(
        TraceBackRepository.CATEGORY_MISSING_FIELD,
        "Customer name is required"
      );
    }

    // Vérifier unicité code si fourni
    if (customer.getCode() != null) {
      Customer existing = customerRepository.findByCode(customer.getCode());
      if (existing != null && !existing.getId().equals(customer.getId())) {
        throw new AxelorException(
          TraceBackRepository.CATEGORY_INCONSISTENCY,
          "Customer code already exists"
        );
      }
    }
  }
}

// ❌ INCORRECT : Mélange responsabilités
public class CustomerServiceImpl {

  public Customer create(Customer customer) {
    // ❌ Logique UI dans service
    if (request.getParameter("skipValidation") != null) { ... }

    // ❌ Requête SQL directe (passer par repository)
    em.createNativeQuery("INSERT INTO customer ...").executeUpdate();

    // ❌ Pas de validation
    return customerRepository.save(customer);
  }
}
```

### Gestion des transactions

```java
// ✅ CORRECT : Transaction au niveau service
public class OrderServiceImpl implements OrderService {

  @Transactional(rollbackOn = {AxelorException.class})
  public Order confirm(Order order) throws AxelorException {
    order.setStatusSelect(OrderStatus.CONFIRMED);
    order.setConfirmedDate(LocalDateTime.now());

    // Appels à d'autres services dans même transaction
    stockService.reserveStock(order);
    invoiceService.generateInvoice(order);

    return orderRepository.save(order);
  }
}

// ❌ INCORRECT : Transaction dans controller
public class OrderController {

  @Transactional  // ❌ Pas de transaction dans controller
  public void confirm(ActionRequest request, ActionResponse response) {
    // Déléguer au service
  }
}
```

### Exceptions métier

```java
// ✅ CORRECT : Exceptions typées et internationalisées
@Transactional(rollbackOn = {AxelorException.class})
public void delete(Customer customer) throws AxelorException {
  if (customer.getOrders() != null && !customer.getOrders().isEmpty()) {
    throw new AxelorException(
      TraceBackRepository.CATEGORY_INCONSISTENCY,
      I18n.get("Cannot delete customer with existing orders")
    );
  }
  customerRepository.remove(customer);
}

// ❌ INCORRECT : Exceptions génériques, messages hardcodés
public void delete(Customer customer) throws Exception {
  if (hasOrders(customer)) {
    throw new Exception("Cannot delete");  // Pas de catégorie, pas i18n
  }
}
```

## Repositories

**IMPORTANT:** Axelor auto-generates `[Entity]Repository extends JpaRepository<Entity>` in `build/src-gen/`.
Only create a custom repository when you need additional query methods or computed fields.
Custom repositories extend the GENERATED repository, NOT JpaRepository directly.

### Requêtes optimisées

```java
// ✅ CORRECT : Custom repository extending the AUTO-GENERATED CustomerRepository
public class CustomerRepo extends CustomerRepository {

  public List<Customer> findActiveByCompany(Company company, int limit) {
    return all()
      .filter("self.company = :company")
      .filter("self.statusSelect = :status")
      .bind("company", company)
      .bind("status", CustomerStatus.ACTIVE)
      .order("-createdOn")
      .fetch(limit);
  }

  public Customer findByCodeWithOrders(String code) {
    return all()
      .filter("self.code = :code")
      .bind("code", code)
      .fetchOne();
  }
}

// ❌ INCORRECT : Requête inefficace
public List<Customer> findAll() {
  // ❌ Charge TOUTE la table en mémoire
  return Query.of(Customer.class).fetch();
}

public Customer findById(Long id) {
  // ❌ Ne pas réinventer find()
  List<Customer> results = Query.of(Customer.class)
    .filter("self.id = :id")
    .bind("id", id)
    .fetch();
  return results.isEmpty() ? null : results.get(0);

  // ✅ Utiliser find() natif
  // return find(id);
}
```

### Éviter N+1 queries

```java
// ❌ INCORRECT : N+1 queries problem
public List<String> getCustomerCompanyNames(List<Customer> customers) {
  List<String> names = new ArrayList<>();
  for (Customer customer : customers) {
    // ❌ Requête pour CHAQUE customer.getCompany()
    names.add(customer.getCompany().getName());
  }
  return names;
}

// ✅ CORRECT : Fetch eager ou query avec join
public List<Customer> findAllWithCompany() {
  return Query.of(Customer.class)
    .fetch();  // Companies chargées en lazy mais optimisées par Hibernate
}

// Ou spécifier fetch explicite
String jpql = "SELECT c FROM Customer c LEFT JOIN FETCH c.company";
```

## Controllers

### Pattern standard

```java
// ✅ CORRECT : Controller délègue au service
public class CustomerController {


  /**
   * Action: Validate customer
   */
  public void validate(ActionRequest request, ActionResponse response) {
    try {
      // 1. Récupérer contexte
      Customer customer = request.getContext().asType(Customer.class);
      customer = Beans.get(CustomerRepository.class).find(customer.getId());

      customer = Beans.get(CustomerService.class).validate(customer);

      // 3. Réponse
      response.setReload(true);
      response.setFlash(I18n.get("Customer validated successfully"));

    } catch (Exception e) {
      // 4. Gestion erreur
      TraceBackService.trace(response, e);
    }
  }

  /**
   * Action: Compute total orders
   */
  public void computeTotal(ActionRequest request, ActionResponse response) {
    Customer customer = request.getContext().asType(Customer.class);

    // Use Beans.get() to access services
    BigDecimal total = Beans.get(CustomerService.class).computeTotalOrders(customer);

    response.setValue("totalOrders", total);
  }
}

// ❌ INCORRECT : Logique métier dans controller
public class CustomerController {

  public void validate(ActionRequest request, ActionResponse response) {
    Customer customer = request.getContext().asType(Customer.class);

    // ❌ Validation dans controller
    if (customer.getCode() == null) {
      response.setError("Code required");
      return;
    }

    // ❌ Logique métier dans controller
    customer.setStatusSelect(2);
    customer.setValidatedDate(LocalDateTime.now());

    // ❌ Accès direct repository
    Beans.get(CustomerRepository.class).save(customer);

    response.setReload(true);
  }
}
```

### Gestion des erreurs

```java
// ✅ CORRECT : TraceBackService pour logging + UI
public void action(ActionRequest request, ActionResponse response) {
  try {
    // Code métier
    customerService.doSomething();
  } catch (AxelorException e) {
    // Trace + message UI
    TraceBackService.trace(response, e, ResponseMessageType.ERROR);
  } catch (Exception e) {
    // Exception non prévue
    TraceBackService.trace(response, e);
  }
}

// ❌ INCORRECT : Ignorer ou logger seulement
public void action(ActionRequest request, ActionResponse response) {
  try {
    customerService.doSomething();
  } catch (Exception e) {
    // ❌ Pas de feedback utilisateur
    LOG.error("Error", e);
  }
}
```

## Vues XML

### Organisation forms

```xml
<!-- ✅ CORRECT : Organisation logique en panels -->
<form name="customer-form" model="com.axelor.apps.mymodule.db.Customer"
      width="large">

  <!-- Panel principal: Champs essentiels visibles immédiatement -->
  <panel name="mainPanel">
    <field name="code" readonly="true" showIf="id != null"/>
    <field name="fullName" colSpan="9"/>
    <field name="statusSelect" colSpan="3" widget="NavSelect"/>
  </panel>

  <!-- Panels secondaires : Grouper informations par thème -->
  <panel name="contactPanel" title="Contact Information">
    <field name="email"/>
    <field name="phone"/>
  </panel>

  <panel name="relationPanel" title="Relations">
    <field name="company" canEdit="false"/>
  </panel>

  <!-- Panel related : Collections en bas -->
  <panel-related name="ordersPanel" field="orders"/>

</form>

<!-- ❌ INCORRECT : Tout dans un seul panel, pas de structure -->
<form name="customer-form">
  <panel>
    <field name="code"/>
    <field name="email"/>
    <field name="fullName"/>
    <field name="orders"/>  <!-- Collection au milieu -->
    <field name="phone"/>
  </panel>
</form>
```

### Colonnes grid optimisées

```xml
<!-- ✅ CORRECT : Colonnes pertinentes, largeurs adaptées -->
<grid name="customer-grid" model="com.axelor.apps.mymodule.db.Customer">
  <field name="code" width="120"/>
  <field name="fullName" width="200"/>
  <field name="company" width="150"/>
  <field name="email" width="180"/>
  <field name="statusSelect" width="100"/>
  <field name="createdOn" width="120"/>
</grid>

<!-- ❌ INCORRECT : Trop de colonnes, pas de largeurs -->
<grid name="customer-grid">
  <field name="id"/>  <!-- Rarement utile -->
  <field name="code"/>
  <field name="fullName"/>
  <field name="email"/>
  <field name="phone"/>
  <field name="address"/>  <!-- Champ long -->
  <field name="company"/>
  <field name="statusSelect"/>
  <field name="createdOn"/>
  <field name="createdBy"/>
  <field name="updatedOn"/>
  <field name="updatedBy"/>
  <field name="version"/>  <!-- Technique, pas utile -->
</grid>
```

## Tests

### Structure tests

```java
// ✅ CORRECT : Tests clairs avec Given-When-Then
@RunWith(GuiceJUnitRunner.class)
@GuiceModules({MyModuleTest.class})
public class CustomerServiceTest {

  @Inject
  private CustomerService customerService;

  @Inject
  private CustomerRepository customerRepository;

  @Test
  public void testCreate_validCustomer_success() throws AxelorException {
    // Given
    Customer customer = new Customer();
    customer.setCode("CUST-001");
    customer.setFullName("John Doe");
    customer.setEmail("john@example.com");

    // When
    Customer result = customerService.create(customer);

    // Then
    assertNotNull(result.getId());
    assertEquals("CUST-001", result.getCode());
    assertEquals(CustomerStatus.ACTIVE, result.getStatusSelect());
  }

  @Test(expected = AxelorException.class)
  public void testCreate_missingName_throwsException() throws AxelorException {
    // Given
    Customer customer = new Customer();
    customer.setCode("CUST-002");
    // fullName manquant

    // When
    customerService.create(customer);

    // Then : exception attendue
  }

  @Test
  public void testValidate_draftCustomer_statusChanges() throws AxelorException {
    // Given
    Customer customer = createDraftCustomer();

    // When
    Customer result = customerService.validate(customer);

    // Then
    assertEquals(CustomerStatus.VALIDATED, result.getStatusSelect());
    assertNotNull(result.getValidatedDate());
  }

  private Customer createDraftCustomer() {
    Customer customer = new Customer();
    customer.setCode("CUST-TEST");
    customer.setFullName("Test Customer");
    customer.setStatusSelect(CustomerStatus.DRAFT);
    return customerRepository.save(customer);
  }
}
```

## Performance

### Requêtes en batch

```java
// ✅ CORRECT : Batch processing pour volumes importants
public void processAllCustomers() {
  int batchSize = 100;
  int offset = 0;

  List<Customer> customers;
  do {
    customers = Query.of(Customer.class)
      .filter("self.statusSelect = :status")
      .bind("status", CustomerStatus.ACTIVE)
      .fetch(batchSize, offset);

    for (Customer customer : customers) {
      processCustomer(customer);
    }

    JPA.clear();  // Libérer mémoire
    offset += batchSize;

  } while (!customers.isEmpty());
}

// ❌ INCORRECT : Charger tout en mémoire
public void processAllCustomers() {
  List<Customer> customers = Query.of(Customer.class).fetch();  // OOM risk
  for (Customer customer : customers) {
    processCustomer(customer);
  }
}
```

### Cache

```java
// ✅ CORRECT : Utiliser cache pour données référentielles
@Cacheable
public Company findCompanyByCode(String code) {
  return Query.of(Company.class)
    .filter("self.code = :code")
    .bind("code", code)
    .cacheable()  // Activer cache query
    .fetchOne();
}
```

## Résumé best practices

| Domaine | ✅ À FAIRE | ❌ À ÉVITER |
|---------|-----------|-------------|
| Génération | `./gradlew generateCode` après XML | Modifier src-gen/ |
| Domaines | Hériter AuditableModel | Redéfinir champs audit |
| Relations | mappedBy bidirectionnel | Oublier mappedBy |
| Services | Logique métier + @Transactional | Transaction dans controllers |
| Repositories | Queries filtrées + pagination | Fetch all sans limite |
| Controllers | Déléguer au service | Logique métier dans controller |
| Exceptions | AxelorException + i18n | Exception générique |
| Vues | Organisation panels logiques | Tout dans un panel |
| Tests | Given-When-Then pattern | Tests sans structure |
| Performance | Batch + pagination | Charger tout en mémoire |
