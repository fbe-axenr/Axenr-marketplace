# Axelor-Specific Patterns

## Overview

This document covers advanced patterns and conventions specific to the Axelor Open Platform that go beyond standard Java/JPA development. These patterns are commonly found in production Axelor codebases and represent best practices for the framework.

## Table of Contents

1. [JPA Lifecycle Listeners](#jpa-lifecycle-listeners)
2. [I18n Translation Interfaces](#i18n-translation-interfaces)
3. [Helper Classes Pattern](#helper-classes-pattern)
4. [Job Scheduling Patterns](#job-scheduling-patterns)
5. [View Processors](#view-processors)
6. [QuickMenu Integration](#quickmenu-integration)
7. [Async Audit Logging](#async-audit-logging)
8. [Batch Processing Patterns](#batch-processing-patterns)

---

## JPA Lifecycle Listeners

### Overview

Axelor supports JPA lifecycle listeners for automatic data enrichment, validation, and side effects during entity persistence operations.

### @PrePersist and @PreUpdate Pattern

Use these annotations to enrich data before saving to database:

```java
package com.axelor.apps.license.listener;

import com.axelor.apps.license.db.LicenseRequest;
import com.axelor.apps.license.db.License;
import com.axelor.apps.license.db.LicenseApplication;
import javax.persistence.PrePersist;
import javax.persistence.PreUpdate;

public class LicenseRequestListener {

    @PrePersist
    @PreUpdate
    public void preSave(LicenseRequest licenseRequest) {
        // Enrich denormalized fields from related entities
        if (licenseRequest.getLicense() != null) {
            License license = licenseRequest.getLicense();

            if (license.getCustomer() != null) {
                licenseRequest.setCustomerName(license.getCustomer().getName());
                licenseRequest.setCustomerEmail(license.getCustomer().getEmail());
                licenseRequest.setCustomerAddress(license.getCustomer().getAddress());
            }

            if (license.getApplication() != null) {
                licenseRequest.setApplicationName(license.getApplication().getApplicationName());
            }
        }
    }
}
```

**Key Points:**
- Both @PrePersist and @PreUpdate on same method ensures it runs on create AND update
- Used for denormalization (copying data for performance/reporting)
- Used for computed field population
- No explicit registration needed - Axelor discovers listeners automatically

### @PostPersist and @PostUpdate Pattern

Use these for side effects after successful persistence:

```java
package com.axelor.apps.license.listener;

import com.axelor.apps.license.db.LicenseConsumptionLine;
import com.axelor.apps.license.service.ConsumptionRecordingFactory;
import com.axelor.common.CollectionUtils;
import javax.persistence.PostPersist;
import javax.persistence.PostUpdate;

public class LicenseConsumptionLineListener {

    @PostPersist
    @PostUpdate
    public void save(LicenseConsumptionLine consumptionLine) {
        // Validate data exists
        if (consumptionLine.getConsumption() == null
            || CollectionUtils.isEmpty(consumptionLine.getConsumption().getConsumptionLineList())) {
            return;
        }

        // Trigger side effect (recording consumption)
        ConsumptionRecordingFactory.get(consumptionLine.getConsumption().getApplication())
            .accept(consumptionLine.getConsumption());
    }
}
```

**Key Points:**
- Runs AFTER entity is persisted to database
- Transaction is still open
- Used for notifications, event triggers, cascade operations
- Guard clauses prevent errors on incomplete data

### Listener Registration in Domain XML

Listeners must be declared in the domain XML file:

```xml
<entity name="LicenseRequest">
  <listener class="com.axelor.apps.license.listener.LicenseRequestListener"/>

  <!-- Fields -->
  <many-to-one name="license" ref="License"/>
  <string name="customerName" max="255"/>
  <string name="customerEmail" max="255"/>
  <!-- ... -->
</entity>
```

### Complete Listener Example

```java
package com.axelor.apps.license.listener;

import com.axelor.apps.license.db.LicenseTag;
import com.axelor.apps.license.db.License;
import com.axelor.common.StringUtils;
import javax.persistence.PrePersist;
import javax.persistence.PreUpdate;
import javax.persistence.PostRemove;
import java.util.stream.Collectors;

public class LicenseTagListener {

    @PrePersist
    @PreUpdate
    public void preSave(LicenseTag licenseTag) {
        // Validate required fields
        if (licenseTag.getName() == null || licenseTag.getName().trim().isEmpty()) {
            throw new IllegalArgumentException("License tag name is required");
        }

        // Normalize data
        licenseTag.setName(licenseTag.getName().trim().toLowerCase());

        // Compute derived fields
        updateLicenseCount(licenseTag);
    }

    @PostRemove
    public void postRemove(LicenseTag licenseTag) {
        // Clean up related data after deletion
        if (licenseTag.getLicenses() != null) {
            licenseTag.getLicenses().forEach(license -> {
                license.getTags().remove(licenseTag);
            });
        }
    }

    private void updateLicenseCount(LicenseTag licenseTag) {
        if (licenseTag.getLicenses() != null) {
            licenseTag.setLicenseCount(licenseTag.getLicenses().size());
        } else {
            licenseTag.setLicenseCount(0);
        }
    }
}
```

**Pattern Frequency:** COMMON - Used for data enrichment and cascade operations

---

## I18n Translation Interfaces

### Overview

Axelor uses Java interfaces with special comment markers for translation extraction. This pattern is cleaner than traditional ResourceBundle or properties files.

### Basic Translation Interface

```java
package com.axelor.apps.license.translation;

public interface LicenseTranslation {

    String LICENSE_RENEW_BAD_OBJECT = /*$$(*/ "Please select a License to renew!" /*)*/;

    String LICENSE_OPEN_APP_BAD_OBJECT = /*$$(*/ "Please select a License to open app!" /*)*/;

    String LICENSE_LINES_MUST_NOT_BE_EMPTY = /*$$(*/
        "No licenses defined. Must add at least one." /*)*/;

    String LICENSE_CUSTOMER_REQUIRED = /*$$(*/
        "Customer is required for license creation" /*)*/;

    String LICENSE_ALREADY_ACTIVE = /*$$(*/
        "License is already active for application: %s" /*)*/;
}
```

**Key Points:**
- Interface with public static final String constants
- Special comment markers `/*$$(*/` and `/*)*/` for extraction tool
- No implementation class needed
- Direct static reference in code
- Supports format placeholders (%s, %d, etc.)

### Using Translations in Code

```java
package com.axelor.apps.license.service;

import com.axelor.apps.license.translation.LicenseTranslation;
import com.axelor.exception.AxelorException;
import com.axelor.exception.db.repo.TraceBackRepository;
import com.axelor.i18n.I18n;

public class LicenseServiceImpl implements LicenseService {

    @Override
    public void validate(License license) throws AxelorException {
        // Simple message
        if (CollectionUtils.isEmpty(license.getLicenses())) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(LicenseTranslation.LICENSE_LINES_MUST_NOT_BE_EMPTY)
            );
        }

        // Message with parameters
        if (license.getStatus() == LicenseStatus.ACTIVE) {
            throw new AxelorException(
                TraceBackRepository.CATEGORY_INCONSISTENCY,
                I18n.get(LicenseTranslation.LICENSE_ALREADY_ACTIVE),
                license.getApplication().getName()
            );
        }
    }
}
```

### Exception Message Interface Pattern

Separate interface for exception messages:

```java
package com.axelor.apps.license.exception;

public interface LicenseExceptionMessage {

    String NEW_CERTIFICATE_NULL_LICENSE_ERROR = /*$$(*/
        "Error while trying to generate a certificate, the provided license is null!" /*)*/;

    String NEW_CERTIFICATE_LICENSE_STATUS_ERROR = /*$$(*/
        "Error while trying to generate a certificate, the license status is wrong!" /*)*/;

    String LICENSE_EXPIRED = /*$$(*/
        "License has expired on %s" /*)*/;

    String LICENSE_NOT_FOUND = /*$$(*/
        "License not found with id: %s" /*)*/;
}
```

**Usage:**

```java
import com.axelor.apps.license.exception.LicenseExceptionMessage;

public class LicenseHelper {

    public static void generateCertificate(License license) throws JsonProcessingException {
        if (license == null) {
            throw new IllegalArgumentException(
                I18n.get(LicenseExceptionMessage.NEW_CERTIFICATE_NULL_LICENSE_ERROR));
        }

        if (license.getLicenseStatus() == LicenseStatus.DRAFT
            || license.getLicenseStatus() == LicenseStatus.EXPIRED) {
            throw new IllegalArgumentException(
                I18n.get(LicenseExceptionMessage.NEW_CERTIFICATE_LICENSE_STATUS_ERROR));
        }

        // Generate certificate logic
    }
}
```

**Pattern Frequency:** VERY COMMON - All user-facing text should use this pattern

---

## Helper Classes Pattern

### Overview

Helper classes are utility classes with static methods that provide reusable functionality without state. They follow a specific pattern in Axelor projects.

### Standard Helper Pattern

```java
package com.axelor.apps.base.helpers;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ExampleHelper {

    // Private constructor prevents instantiation
    private ExampleHelper() {
        throw new UnsupportedOperationException("Utility class");
    }

    // Static methods only
    public static String formatName(String firstName, String lastName) {
        if (firstName == null && lastName == null) {
            return "";
        }
        if (firstName == null) {
            return lastName;
        }
        if (lastName == null) {
            return firstName;
        }
        return String.format("%s %s", firstName, lastName);
    }
}
```

### Standard SLF4J Logging Pattern

Axelor uses standard SLF4J logging with static logger fields:

```java
package com.axelor.apps.license.service;

import org.slf4j.Logger;
import java.lang.invoke.MethodHandles;
import org.slf4j.LoggerFactory;

public class LicenseServiceImpl implements LicenseService {

    protected static final Logger log = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());

    @Override
    public License confirm(License license) {
        log.debug("Confirming license: {}", license.getId());

        // Business logic

        log.info("License confirmed: {}", license.getName());
        return license;
    }
}
```

**Best Practices:**
- Declare logger as `protected static final`
- Name it `log` (lowercase) following modern conventions
- Use MethodHandles.lookup().lookupClass() for automatic class detection
- Use parameterized logging for efficiency

---

## Job Scheduling Patterns

### Overview

Axelor supports Quartz-based job scheduling for background tasks, batch processing, and scheduled operations.

### Basic Job Implementation

```java
package com.axelor.apps.license.job;

import com.axelor.apps.license.db.License;
import com.axelor.apps.license.service.LicenseService;
import com.axelor.db.JPA;
import com.google.inject.Inject;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.lang.invoke.MethodHandles;
import java.time.LocalDate;

public class LicenseExpirationWarningJob implements Job {

    private static final Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());

    private final LicenseService licenseService;
    private final AppGuardianService appGuardianService;

    @Inject
    public LicenseExpirationWarningJob(
        LicenseService licenseService,
        AppGuardianService appGuardianService) {
        this.licenseService = licenseService;
        this.appGuardianService = appGuardianService;
    }

    @Override
    public void execute(JobExecutionContext context) throws JobExecutionException {
        log.info("Starting license expiration warning job");

        try {
            int daysBeforeExpiration = appGuardianService.getAppGuardian().getDaysBeforeExpiration();
            Template template = appGuardianService.getAppGuardian().getExpirationWarningTemplate();

            LocalDate now = LocalDate.now();
            LocalDate endDate = now.plusDays(daysBeforeExpiration);

            // Process licenses
            processExpiringLicenses(now, endDate, template);

            log.info("License expiration warning job completed");
        } catch (Exception e) {
            log.error("Error in license expiration warning job", e);
            throw new JobExecutionException(e);
        }
    }

    private void processExpiringLicenses(LocalDate now, LocalDate endDate, Template template) {
        // Implementation
    }
}
```

### Job with Batch Processing Pattern

```java
package com.axelor.apps.license.job;

import com.axelor.apps.base.helpers.Loggers;
import com.axelor.apps.license.db.License;
import com.axelor.apps.license.db.repo.LicenseRepository;
import com.axelor.apps.license.service.LicenseService;
import com.axelor.db.JPA;
import com.google.inject.Inject;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import java.time.LocalDate;
import java.util.List;

public class LicenseExpirationWarningJob implements Job {

    private static final int BATCH_SIZE = 20;

    @Inject
    private LicenseService licenseService;

    @Inject
    private LicenseRepository licenseRepository;

    @Inject
    private AppGuardianService appGuardianService;

    @Override
    public void execute(JobExecutionContext context) {
        int daysNumber = appGuardianService.getAppGuardian().getDaysBeforeExpiration();
        Template template = appGuardianService.getAppGuardian().getExpirationWarningTemplate();

        LocalDate now = LocalDate.now();
        LocalDate endDate = now.plusDays(daysNumber);

        // Count total licenses to process
        long count = licenseRepository.countExpiringLicenses(now, endDate);

        log.debug("Found {} licenses expiring within the next {} days", count, daysNumber);

        // Process in batches to avoid memory issues
        int offset = 0;
        List<License> licenses;

        do {
            licenses = licenseRepository.findExpiringLicenses(now, endDate, BATCH_SIZE, offset);

            // Process batch
            for (License license : licenses) {
                try {
                    licenseService.sendExpirationWarning(license, template);
                } catch (Exception e) {
                    log.error("Error sending expiration warning for license: {}",
                        license.getId(), e);
                }
            }

            // Clear persistence context to free memory
            JPA.clear();

            offset += BATCH_SIZE;
        } while (!licenses.isEmpty());
    }
}
```

**Key Points:**
- Process in batches to avoid memory leaks
- Call `JPA.clear()` between batches
- Catch exceptions per-item so one failure doesn't stop batch
- Use repository methods for queries
- Log progress and errors

**Pattern Frequency:** RARE - Only for scheduled background tasks

---

## View Processors

### Overview

View processors allow dynamic modification of views (forms, grids) at runtime based on user context, permissions, or data.

### Basic View Processor

```java
package com.axelor.apps.license.meta.service;

import com.axelor.auth.AuthUtils;
import com.axelor.auth.db.User;
import com.axelor.auth.db.repo.UserRepository;
import com.axelor.db.JPA;
import com.axelor.meta.db.MetaView;
import com.axelor.meta.schema.views.AbstractView;
import com.axelor.meta.schema.views.FormView;
import com.axelor.meta.schema.views.GridView;
import com.axelor.meta.schema.views.Button;
import com.axelor.meta.service.ViewProcessorImpl;
import com.google.inject.Inject;
import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.ArrayList;
import java.lang.invoke.MethodHandles;
import java.util.List;
import java.util.Optional;

public class GuardianViewProcessor extends ViewProcessorImpl {

    protected static final Logger log = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());
    protected static final String GUARDIAN_PRINT_BUTTON_ICON = "mail";

    @Inject
    public GuardianViewProcessor(UserRepository userRepository) {
        super(userRepository);
    }

    @Override
    public void process(AbstractView view) {
        // Always call super first
        super.process(view);

        String model = view.getModel();
        String userLanguage = Optional.ofNullable(AuthUtils.getUser())
            .map(User::getLanguage)
            .orElse("unknown");

        // Check if template exists for this model
        if (!isTemplateExist(model, userLanguage)) {
            return;
        }

        // Add button to grid views
        if (view instanceof GridView) {
            GridView gridView = (GridView) view;
            gridView.setToolbar(addGuardianPrintButton(gridView.getToolbar()));
        }

        // Add button to form views
        if (view instanceof FormView) {
            FormView formView = (FormView) view;
            formView.setToolbar(addGuardianPrintButton(formView.getToolbar()));
        }
    }

    protected boolean isTemplateExist(String model, String userLanguage) {
        if (StringUtils.isBlank(model)) {
            return false;
        }

        return JPA.all(Template.class)
            .filter("self.metaModel.fullName = :model AND self.language = :userLanguage")
            .bind("model", model)
            .bind("userLanguage", userLanguage)
            .count() > 0;
    }

    protected List<Button> addGuardianPrintButton(List<Button> toolbar) {
        toolbar = Optional.ofNullable(toolbar).orElse(new ArrayList<>());

        Button guardianPrintButton = new Button();
        guardianPrintButton.setName("guardianPrintBtn");
        guardianPrintButton.setOnClick("action-guardian-send-mail");
        guardianPrintButton.setModuleToCheck("axelor-guardian");
        guardianPrintButton.setIcon(GUARDIAN_PRINT_BUTTON_ICON);

        // Add at beginning of toolbar
        toolbar.add(0, guardianPrintButton);

        return toolbar;
    }
}
```

### View Processor Registration

Register in Guice module:

```java
package com.axelor.apps.license;

import com.axelor.app.AxelorModule;
import com.axelor.apps.license.meta.service.GuardianViewProcessor;
import com.axelor.meta.service.ViewProcessorImpl;

public class LicenseModule extends AxelorModule {

    @Override
    protected void configure() {
        // Override default view processor
        bind(ViewProcessorImpl.class).to(GuardianViewProcessor.class);
    }
}
```

**Pattern Frequency:** RARE - Only for cross-cutting view customizations

---

## QuickMenu Integration

### Overview

QuickMenu provides a quick-access dropdown menu in the UI. Implement `QuickMenuCreator` to add custom menus.

### Basic QuickMenu Implementation

```java
package com.axelor.apps.license.quickmenu;

import com.axelor.auth.AuthUtils;
import com.axelor.auth.db.User;
import com.axelor.apps.license.db.LicensePartner;
import com.axelor.apps.license.web.GuardianUserController;
import com.axelor.i18n.I18n;
import com.axelor.rpc.Context;
import com.axelor.ui.QuickMenu;
import com.axelor.ui.QuickMenuCreator;
import com.axelor.ui.QuickMenuItem;
import java.util.Objects;
import java.util.stream.Collectors;

public class DefaultIntegratorQuickMenu implements QuickMenuCreator {

    @Override
    public QuickMenu create() {
        String action = GuardianUserController.class.getName() + ":updateDefaultIntegrator";
        User user = AuthUtils.getUser();

        LicensePartner defaultIntegrator = user.getDefaultIntegrator();
        if (defaultIntegrator == null) {
            return null;
        }

        return new QuickMenu(
            I18n.get(defaultIntegrator.getName()),
            0,  // Order
            true,  // Show divider
            user.getIntegrators().stream()
                .map(it -> create(it, action, defaultIntegrator))
                .collect(Collectors.toList())
        );
    }

    private QuickMenuItem create(
        LicensePartner integrator,
        String action,
        LicensePartner defaultIntegrator) {

        return new QuickMenuItem(
            integrator.getName(),
            action,
            new Context(integrator.getId(), LicensePartner.class),
            Objects.equals(integrator.getId(), defaultIntegrator.getId())  // Selected
        );
    }
}
```

### QuickMenu Registration

Register in Guice module:

```java
package com.axelor.apps.license;

import com.axelor.app.AxelorModule;
import com.axelor.apps.license.quickmenu.DefaultIntegratorQuickMenu;

public class LicenseModule extends AxelorModule {

    @Override
    protected void configure() {
        // Register quick menu
        addQuickMenu(DefaultIntegratorQuickMenu.class);
    }
}
```

**Pattern Frequency:** RARE - Only for global UI shortcuts

---

## Async Audit Logging

### Overview

Audit logging should not block business operations. Use ForkJoinPool for non-blocking audit trail creation.

### Async Audit Helper

```java
package com.axelor.apps.license.helpers;

import com.axelor.apps.license.db.LicenseAuditRecord;
import com.axelor.apps.license.db.repo.LicenseAuditRecordRepository;
import com.axelor.db.JPA;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.lang.invoke.MethodHandles;
import java.time.LocalDateTime;
import java.util.concurrent.ForkJoinPool;

public class AuditHelper {

    private static final Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());
    private static final ForkJoinPool POOL = ForkJoinPool.commonPool();

    private AuditHelper() {}

    /**
     * Log audit event asynchronously
     */
    public static void log(
        Long applicationId,
        Long licenseId,
        String ip,
        String status,
        String event,
        Object... args) {

        String message = String.format(event, args);

        // Submit to async pool (non-blocking)
        POOL.submit(() -> persist(create(applicationId, licenseId, ip, message, status)));

        // Also log synchronously for debugging
        log.info(message);
    }

    private static LicenseAuditRecord create(
        Long applicationId,
        Long licenseId,
        String ip,
        String message,
        String status) {

        LicenseAuditRecord auditRecord = new LicenseAuditRecord();
        auditRecord.setApplicationId(applicationId);
        auditRecord.setLicenseId(licenseId);
        auditRecord.setIpAddress(ip);
        auditRecord.setMessage(message);
        auditRecord.setStatus(status);
        auditRecord.setCreatedOn(LocalDateTime.now());

        return auditRecord;
    }

    private static void persist(LicenseAuditRecord auditRecord) {
        try {
            // Run in separate transaction
            JPA.runInTransaction(() -> JPA.save(auditRecord));
        } catch (Exception e) {
            log.error("Failed to persist audit record", e);
        }
    }
}
```

### Using Async Audit Logging

```java
package com.axelor.apps.license.service;

import com.axelor.apps.license.helpers.AuditHelper;
import com.axelor.apps.license.db.License;
import com.axelor.apps.license.db.repo.LicenseAuditRecordRepository;
import java.util.Optional;

public class LicenseServiceImpl implements LicenseService {

    @Override
    public Message confirm(License license) throws AxelorException {
        // Validate and confirm license
        checkLicences(license);
        confirmLicense(license);

        // Async audit logging (non-blocking)
        AuditHelper.log(
            Optional.of(license)
                .map(License::getApplication)
                .map(LicenseApplication::getId)
                .orElse(null),
            Optional.of(license).map(License::getId).orElse(null),
            "127.0.0.1",
            LicenseAuditRecordRepository.AUDIT_RECORD_TYPE_INFO,
            "License confirmed: %s, application: %s, customer: %s",
            license.getName(),
            license.getApplication().getName(),
            license.getCustomer().getName()
        );

        return buildMessage(license);
    }
}
```

**Benefits:**
- Non-blocking - doesn't slow down business operations
- Separate transaction - audit failure doesn't rollback business operation
- Automatic error handling

**Pattern Frequency:** COMMON - Used for all audit trail operations

---

## Batch Processing Patterns

### Overview

When processing large datasets, proper batch processing prevents memory leaks and performance issues.

### Batch Processing with JPA.clear()

```java
package com.axelor.apps.license.service;

import com.axelor.apps.license.db.License;
import com.axelor.apps.license.db.repo.LicenseRepository;
import com.axelor.db.JPA;
import com.axelor.db.JpaRepository;
import com.axelor.inject.Beans;
import com.google.inject.Inject;
import com.google.inject.persist.Transactional;
import com.google.inject.servlet.RequestScoper;
import com.google.inject.servlet.ServletScopes;
import java.lang.invoke.MethodHandles;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.Callable;

public class MassSaveServiceImpl implements Callable<Long> {

    private static final Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());
    private static final int BATCH_SIZE = 50;

    @Inject
    private LicenseRepository licenseRepository;

    private List<Long> licenseIds;

    public MassSaveServiceImpl(List<Long> licenseIds) {
        this.licenseIds = licenseIds;
    }

    @Override
    public Long call() {
        // Create request scope for batch operation
        final RequestScoper scope = ServletScopes.scopeRequest(Collections.emptyMap());

        try (RequestScoper.CloseableScope ignored = scope.open()) {
            return process();
        }
    }

    private Long process() {
        long processed = 0;

        for (int i = 0; i < licenseIds.size(); i++) {
            Long licenseId = licenseIds.get(i);

            try {
                processLicense(licenseId);
                processed++;
            } catch (Exception e) {
                log.error("Error processing license: {}", licenseId, e);
            }

            // Clear JPA context every BATCH_SIZE to free memory
            if (i > 0 && i % BATCH_SIZE == 0) {
                JPA.clear();
            }
        }

        return processed;
    }

    @Transactional(rollbackOn = Exception.class)
    protected void processLicense(Long licenseId) {
        License license = licenseRepository.find(licenseId);
        if (license != null) {
            // Process license
            license.setProcessed(true);
            licenseRepository.save(license);
        }
    }
}
```

### Batch Query Pattern

```java
package com.axelor.apps.license.service;

import com.axelor.apps.license.db.License;
import com.axelor.db.JPA;
import com.axelor.db.Query;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.lang.invoke.MethodHandles;
import java.util.List;

public class LicenseBatchProcessor {

    private static final Logger LOG = LoggerFactory.getLogger(MethodHandles.lookup().lookupClass());
    private static final int BATCH_SIZE = 100;

    public void processAllLicenses() {
        Query<License> query = Query.of(License.class)
            .filter("self.status = :status")
            .bind("status", "PENDING")
            .order("id");

        query.setMaxResults(BATCH_SIZE);
        List<License> licenses = query.fetch();

        while (!licenses.isEmpty()) {
            // Process batch
            for (License license : licenses) {
                try {
                    processLicense(license);
                } catch (Exception e) {
                    log.error("Error processing license: {}", license.getId(), e);
                }
            }

            // Clear persistence context
            JPA.clear();

            // Fetch next batch
            query.setFirstResult(query.getFirstResult() + BATCH_SIZE);
            licenses = query.fetch();
        }
    }

    private void processLicense(License license) {
        // Process logic
    }
}
```

**Key Points:**
- Always use `JPA.clear()` between batches
- Process in fixed batch sizes (50-100 typically)
- Catch exceptions per-item to continue processing
- Use RequestScoper for servlet context in background jobs

**Pattern Frequency:** COMMON - Required for all bulk operations

---

## Best Practices Summary

1. **JPA Listeners**: Use for data enrichment and cascade operations
2. **I18n Interfaces**: All user-facing text must use translation interfaces
3. **Helper Classes**: Use for reusable static utilities with private constructors
4. **Jobs**: Always batch process with JPA.clear() between batches
5. **View Processors**: Override only when needed for cross-cutting concerns
6. **QuickMenu**: Use sparingly for global shortcuts
7. **Async Audit**: Always async to avoid blocking business operations
8. **Batch Processing**: Mandatory JPA.clear() to prevent memory leaks

---

This document provides comprehensive coverage of Axelor-specific patterns found in production codebases and represents best practices for the framework.
