# Special Case User Story Patterns

This document provides patterns for User Stories that don't follow the standard entity CRUD workflow. Use these patterns for security, integration, import/export, and workflow features.

---

## Pattern 1: Security and Permissions

### Template

```textile
h3. US-XXX: Configure [EntityName] Permissions

*As a* system administrator
*I want* to configure access permissions for [EntityName]
*So that* users only see data they're authorized to access

h4. Acceptance Criteria

* [ ] Roles defined: [list roles from specification]
* [ ] Permission rules created for each role
* [ ] CRUD permissions configured: [permission matrix]
* [ ] Row-level security implemented (if needed)
* [ ] Tested with each role

h4. Technical Details

* *MetaPermissions XML:* src/main/resources/views/[EntityName].xml
* *Permission rules:* [list rules]
* *Roles:* [list roles]

h4. Estimation

* *Complexity:* M
* *Estimated Effort:* 3-4 hours
```

### Usage Guidelines

**When to use**: When entity requires role-based access control

**Security levels in Axelor**:
1. **Model-level**: CREATE, READ, WRITE, REMOVE permissions
2. **Field-level**: Hide/show specific fields by role
3. **Row-level (domain filter)**: Filter records by criteria (e.g., user's company)
4. **Action-level**: Enable/disable buttons by role

**Permission matrix example**:

| Role | CREATE | READ | WRITE | REMOVE | Domain Filter |
|------|--------|------|-------|--------|---------------|
| User | Yes | Own only | Own only | No | createdBy = $currentUser |
| Manager | Yes | Team | Team | No | team = $currentUser.team |
| Admin | Yes | All | All | Yes | (none) |

### Complete Example

```textile
h3. US-015: Configure Message Permissions and Security

*As a* system administrator
*I want* to configure access permissions for Message entity
*So that* users only see their own emails and managers can view team emails

h4. Acceptance Criteria

* [ ] AC1: Roles defined: Email User, Email Manager, System Admin
* [ ] AC2: Permission rules created:
** Email User: READ own messages (domain filter on EmailAccount)
** Email Manager: READ team messages (EmailAccount with manager access)
** System Admin: Full access (no restrictions)
* [ ] AC3: CRUD permissions configured per role:
** CREATE: System only (sync process) - no user can manually create
** READ: Role-based (User=own, Manager=team, Admin=all)
** WRITE: No direct write (read-only entity)
** REMOVE: Role-based (User=own, Manager=team, Admin=all)
* [ ] AC4: Domain-level security enforces email filtering:
** Received emails: toRecipients/ccRecipients contains user's email
** Sent emails: fromEmailAddress matches user's email
* [ ] AC5: Tested with all three roles, verified isolation

h4. Technical Details

* *MetaPermissions XML:* src/main/resources/domains/Message.xml
* *Permission Rules:*
** rule.message.user: READ if (typeSelect=1 AND toRecipients contains $user.email) OR (typeSelect=2 AND fromEmailAddress = $user.email)
** rule.message.manager: READ if emailAccountSet contains EmailAccount where manager=$user
** rule.message.admin: No restrictions
* *Roles:*
** axelor.role.email.user (base role)
** axelor.role.email.manager (extends user role)
** axelor.role.system.admin (full access)
* *Domain Filters:*
** User filter: self.emailAccountSet.owner = :__user__ OR self.emailAccountSet.managers.user = :__user__
** Manager filter: self.emailAccountSet.managers.user = :__user__

h4. Estimation

* *Complexity:* M (Multiple roles, domain filtering, row-level security)
* *Estimated Effort:* 4 hours

h4. Dependencies

* Depends on: US-001 (Message domain must exist)
* Depends on: US-010 (EmailAccount entity must exist)
* Blocks: (None - can be added after views)

h4. Testing Checklist

* Login as User role: can only see own emails
* Login as Manager role: can see team emails
* Login as Admin role: can see all emails
* Verify users cannot bypass domain filter via API
* Verify CREATE permission blocked for all users
```

---

## Pattern 2: Import/Export Features

### Template

```textile
h3. US-XXX: Implement [EntityName] CSV Import

*As a* [user role]
*I want* to import [entities] from CSV file
*So that* I can bulk load data efficiently

h4. Acceptance Criteria

* [ ] Import action available in menu/button
* [ ] CSV file upload and validation
* [ ] Column mapping configurable
* [ ] Duplicate detection: [strategy from specification]
* [ ] Error report generated for failed rows
* [ ] Success message with import summary

h4. Technical Details

* *Import Config:* data-import XML configuration
* *CSV Columns:* [list expected columns]
* *Validation Rules:* [list]
* *Duplicate Strategy:* [update/skip/error]

h4. Estimation

* *Complexity:* L
* *Estimated Effort:* 1-2 days
```

### Usage Guidelines

**When to use**: When bulk data loading is required

**Import complexity factors**:
- **M (Medium)**: Simple CSV, fixed columns, basic validation
- **L (Large)**: Complex CSV, configurable mapping, lookups, transformations
- **XL (Extra Large)**: Multiple file types, relationships, complex validations, rollback on error

**Import workflow**:
1. User uploads CSV file
2. System validates file format and columns
3. User maps CSV columns to entity fields (if configurable)
4. System validates data (format, required fields, relationships)
5. System imports valid rows, logs errors for invalid rows
6. System generates report: X rows imported, Y rows failed

### Complete Example

```textile
h3. US-020: Implement Customer CSV Import with Duplicate Detection

*As a* sales manager
*I want* to import customer records from CSV file
*So that* I can bulk load customer data from legacy system

h4. Acceptance Criteria

* [ ] AC1: Import action button available in Customer grid toolbar
* [ ] AC2: CSV file upload dialog accepts .csv files up to 10MB
* [ ] AC3: CSV columns validated:
** Required: code, name, email
** Optional: phone, address, city, country, companyCode
* [ ] AC4: Column mapping interface allows user to map CSV headers to fields
* [ ] AC5: Duplicate detection by customer code:
** If code exists: update existing record (default)
** User can choose: skip, update, or error on duplicates
* [ ] AC6: Company lookup by companyCode (must exist, error if not found)
* [ ] AC7: Email format validation (must be valid email address)
* [ ] AC8: Error report generated for failed rows with reason
* [ ] AC9: Success message: "Imported 150 customers, 5 failed. Download error report."
* [ ] AC10: Transaction rollback if critical error (optional config)

h4. Technical Details

* *Import Config XML:* src/main/resources/data-import/customer-import-config.xml
* *CSV Columns Expected:*
  - code (required, unique identifier)
  - name (required)
  - email (required, email format)
  - phone (optional)
  - address (optional)
  - city (optional)
  - country (optional)
  - companyCode (optional, FK lookup)
* *Validation Rules:*
  - code: max 64 chars, alphanumeric
  - email: valid email format
  - companyCode: must exist in Company table
* *Duplicate Strategy Options:*
  - UPDATE: Update existing record (default)
  - SKIP: Skip duplicate, continue with next row
  - ERROR: Fail import if duplicate found
* *Error Logging:*
  - CSV row number
  - Field name that failed validation
  - Error message
  - Rejected value
* *Success Report:*
  - Total rows processed
  - Rows imported successfully
  - Rows failed
  - Download link for error CSV

h4. Estimation

* *Complexity:* L (CSV parsing, mapping, validation, duplicate handling, error reporting)
* *Estimated Effort:* 1.5 days

h4. Dependencies

* Depends on: US-001 (Customer domain)
* Depends on: US-005 (Company entity for lookup)
* Blocks: (None)

h4. Testing Checklist

* Upload valid CSV: all rows imported
* Upload CSV with duplicates: update strategy works
* Upload CSV with invalid email: row rejected, error logged
* Upload CSV with non-existent companyCode: row rejected
* Upload large CSV (1000 rows): performance acceptable
* Upload malformed CSV: clear error message
* Download error report: contains all failed rows with reasons
```

---

## Pattern 3: Workflow Implementation

### Template

```textile
h3. US-XXX: Implement [EntityName] Workflow

*As a* [user role]
*I want* [entity] to follow a defined workflow
*So that* business process is enforced and tracked

h4. Acceptance Criteria

* [ ] Workflow states defined: [list states]
* [ ] State transitions configured: [list transitions]
* [ ] Transition validations implemented
* [ ] Workflow actions (buttons) visible based on state
* [ ] Notification sent on state changes
* [ ] Audit trail logs state transitions

h4. Technical Details

* *Workflow Service:* [EntityName]WorkflowService
* *States:* [list with codes]
* *Transitions:* [list with conditions]
* *Notifications:* [list recipients and triggers]

h4. Estimation

* *Complexity:* L-XL
* *Estimated Effort:* 1-3 days
```

### Usage Guidelines

**When to use**: When entity follows a business process with states

**Workflow complexity**:
- **M (Medium)**: 3-4 states, linear flow, simple validations
- **L (Large)**: 5-7 states, branches, parallel paths, approvals
- **XL (Extra Large)**: 8+ states, complex rules, external integrations, escalations

**Workflow definition**:
1. Define states (Draft, Submitted, Approved, Rejected, Completed)
2. Define transitions (Submit, Approve, Reject, Cancel)
3. Define transition conditions (who can transition, when)
4. Define side effects (notifications, logs, integrations)

### Complete Example

```textile
h3. US-025: Implement Purchase Order Approval Workflow

*As a* purchasing manager
*I want* purchase orders to follow an approval workflow
*So that* all purchases are reviewed before processing

h4. Acceptance Criteria

* [ ] AC1: Workflow states defined:
** 1=Draft (initial state)
** 2=Submitted (awaiting approval)
** 3=Approved (ready for processing)
** 4=Rejected (denied by approver)
** 5=Cancelled (cancelled by creator)
* [ ] AC2: State transitions configured:
** Draft → Submitted: User clicks "Submit" (if total amount > 0)
** Submitted → Approved: Manager clicks "Approve" (if manager role)
** Submitted → Rejected: Manager clicks "Reject" (if manager role)
** Draft/Submitted → Cancelled: Creator clicks "Cancel"
* [ ] AC3: Workflow buttons visible based on state:
** "Submit" button: visible in Draft state only
** "Approve"/"Reject" buttons: visible in Submitted state, only for managers
** "Cancel" button: visible in Draft/Submitted states, only for creator
* [ ] AC4: Transition validations:
** Submit: total amount > 0, all line items valid
** Approve: user has manager role, order not expired
** Reject: rejection reason required
* [ ] AC5: Notifications sent:
** Submit: notify assigned manager
** Approve: notify creator and purchasing department
** Reject: notify creator with rejection reason
* [ ] AC6: Audit trail logs:
** State change timestamp
** User who performed transition
** Previous and new state
** Rejection reason (if applicable)

h4. Technical Details

* *Workflow Service:* com.axelor.purchase.service.PurchaseOrderWorkflowService
* *Methods:*
** submit(PurchaseOrder order) → void
** approve(PurchaseOrder order) → void
** reject(PurchaseOrder order, String reason) → void
** cancel(PurchaseOrder order) → void
* *States (statusSelect):*
** 1 = Draft
** 2 = Submitted
** 3 = Approved
** 4 = Rejected
** 5 = Cancelled
* *Transition Matrix:*
| From | To | Action | Condition |
|------|----|----- --|-----------|
| Draft | Submitted | submit() | totalAmount > 0 |
| Submitted | Approved | approve() | user has Manager role |
| Submitted | Rejected | reject() | user has Manager role, reason provided |
| Draft/Submitted | Cancelled | cancel() | user is creator |
* *Notifications:*
** Template: purchase-order-submitted.ftl
** Recipients: order.assignedManager
** Trigger: statusSelect changes to 2 (Submitted)
* *Audit Fields:*
** submittedDate: LocalDateTime
** submittedBy: User
** approvedDate: LocalDateTime
** approvedBy: User
** rejectionReason: String

h4. Estimation

* *Complexity:* L (Multiple states, role-based transitions, notifications)
* *Estimated Effort:* 2 days

h4. Dependencies

* Depends on: US-030 (PurchaseOrder domain)
* Depends on: US-032 (PurchaseOrder form view)
* Depends on: US-040 (Notification service)
* Blocks: US-050 (Purchase processing requires approved orders)

h4. State Diagram

```
[Draft] --submit()--> [Submitted] --approve()--> [Approved]
   |                      |
   |                      +--reject()--> [Rejected]
   |                      |
   +------cancel()--------+
```

h4. Testing Checklist

* Create PO in Draft, submit: transitions to Submitted, manager notified
* Manager approves: transitions to Approved, creator notified
* Manager rejects without reason: validation error
* Manager rejects with reason: transitions to Rejected, creator notified with reason
* Non-manager tries to approve: button hidden/disabled
* Creator cancels Draft PO: transitions to Cancelled
* Audit trail logs all transitions with user and timestamp
```

---

## Pattern 4: Dashboard and Reporting

### Template

```textile
h3. US-XXX: Create [ReportName] Dashboard

*As a* [user role]
*I want* to view [metrics/KPIs] on a dashboard
*So that* I can monitor [business objective]

h4. Acceptance Criteria

* [ ] Dashboard displays: [list metrics]
* [ ] Charts/graphs configured: [list visualizations]
* [ ] Filters available: [date range, company, etc.]
* [ ] Data refreshes automatically
* [ ] Export to PDF/Excel available

h4. Technical Details

* *Dashboard XML:* src/main/resources/views/dashboards/[Name].xml
* *Data source:* [repository methods or custom queries]
* *Charts:* [chart types and configurations]

h4. Estimation

* *Complexity:* M-L
* *Estimated Effort:* 4-8 hours
```

### Usage Guidelines

**When to use**: When users need analytical views or KPIs

**Dashboard complexity**:
- **M (Medium)**: 2-3 dashlets, simple queries, basic charts
- **L (Large)**: 5+ dashlets, complex aggregations, custom visualizations
- **XL (Extra Large)**: Interactive dashboards, drill-down, real-time data

### Complete Example

```textile
h3. US-030: Create Sales Performance Dashboard

*As a* sales manager
*I want* to view team sales metrics on a dashboard
*So that* I can monitor performance and identify trends

h4. Acceptance Criteria

* [ ] AC1: Dashboard displays 5 dashlets:
** Total Sales (current month vs. last month)
** Sales by Product Category (pie chart)
** Sales Trend (line chart, last 12 months)
** Top 10 Customers (bar chart)
** Open Opportunities (count and total value)
* [ ] AC2: Filters available:
** Date range picker (default: current month)
** Team/User selector (default: current user's team)
** Company selector (if multi-company)
* [ ] AC3: Data refreshes every 5 minutes automatically
* [ ] AC4: Export button generates PDF report
* [ ] AC5: Clicking chart elements drills down to detail view

h4. Technical Details

* *Dashboard XML:* src/main/resources/views/dashboards/sales-performance-dashboard.xml
* *Dashlets:*
** sales-total-dashlet: Custom repository method getTotalSales(dateRange, team)
** sales-by-category-dashlet: Chart type="pie", dataset from SaleOrder.category aggregation
** sales-trend-dashlet: Chart type="line", dataset from monthly aggregation
** top-customers-dashlet: Chart type="bar", dataset from top 10 query
** open-opportunities-dashlet: Simple count from Opportunity where status=Open
* *Repository Methods:*
** SaleOrderRepository.getTotalSales(LocalDate start, LocalDate end, Team team)
** SaleOrderRepository.getSalesByCategory(LocalDate start, LocalDate end)
** SaleOrderRepository.getMonthlySalesTrend(int months)
** SaleOrderRepository.getTopCustomers(int limit, LocalDate start, LocalDate end)

h4. Estimation

* *Complexity:* L (Multiple dashlets, complex queries, charts)
* *Estimated Effort:* 8 hours

h4. Dependencies

* Depends on: US-100 (SaleOrder entity)
* Depends on: US-105 (Opportunity entity)
* Blocks: (None)
```

---

## Pattern 5: Integration with External Systems

### Template

```textile
h3. US-XXX: Integrate with [SystemName] API

*As a* [user role]
*I want* data synchronized with [external system]
*So that* [business benefit of integration]

h4. Acceptance Criteria

* [ ] API connection configured
* [ ] Authentication implemented
* [ ] Data mapping defined
* [ ] Sync process scheduled
* [ ] Error handling and retry logic
* [ ] Sync status dashboard

h4. Technical Details

* *Integration Service:* [ServiceName]
* *API Endpoint:* [URL]
* *Authentication:* [OAuth2/API Key/etc.]
* *Sync Schedule:* [frequency]

h4. Estimation

* *Complexity:* L-XL
* *Estimated Effort:* 2-5 days
```

### Usage Guidelines

**When to use**: When integrating with external APIs or systems

**Integration complexity**:
- **L (Large)**: REST API, simple auth, one-way sync, basic error handling
- **XL (Extra Large)**: Multiple APIs, OAuth, bi-directional sync, complex mappings, webhook listeners

---

## Related Documents

- [Entity-Based US Patterns](entity-based-us-patterns.md)
- [User Story Template](../templates/user-story-template.md)
- [EPIC Template](../templates/epic-template.md)
