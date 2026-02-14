# Question Templates for Business Analysis

This document provides templates for asking effective clarifying questions during requirement analysis. Use these templates to gather precise information while explaining why each detail matters for Axelor development.

## Question Format

**Recommended structure**:
```markdown
## Questions on [Topic/Entity Name]

### [Specific Aspect]
1. **[Clear, specific question]?**
   - Context: [Why this information is important for Axelor]
   - Suggested options: [If applicable, propose options based on Axelor patterns]
   - Impact: [How this choice affects implementation]
```

---

## Questions on Business Entities

### Entity Identification

**1. What is the business identifier for [Entity]?**
- Context: Axelor entities typically need a unique business code for user identification (separate from technical ID)
- Options:
  - Automatic sequential code (e.g., CUST-001, CUST-002)
  - User-entered code with validation
  - Code based on business rule (e.g., first 3 letters + date)
  - No code needed (display by name only)
- Impact: Affects domain definition (code field required/unique) and user workflow

**2. What is the primary display name for [Entity]?**
- Context: Entities need a human-readable name for display in lists, selects, and reports
- Options:
  - Simple name field
  - Full name (concatenated from multiple fields)
  - Name with code (e.g., "[CUST-001] Axelor SAS")
- Impact: Affects UI display throughout the application

### Entity Fields

**3. What data type should be used for [field name]?**
- Context: Axelor supports specific data types that affect storage, validation, and UI widgets
- Options:
  - String (text) - for names, descriptions, codes
  - Integer - for whole numbers, counts, selections
  - Decimal - for amounts, prices, percentages
  - Boolean - for yes/no, true/false flags
  - Date - for dates without time
  - DateTime - for dates with time
  - Binary - for file storage
- Impact: Determines validation rules and UI widget type

**4. Is [field name] required or optional?**
- Context: Required fields must be filled before saving, affecting user workflow and validation
- Options:
  - Required (cannot save without this field)
  - Optional (can be filled later)
  - Conditionally required (depends on other fields/status)
- Impact: Affects domain definition, UI validation, and user experience

**5. Should [field name] be unique?**
- Context: Unique constraint prevents duplicate values in database
- Options:
  - Globally unique (no duplicates allowed)
  - Unique per company/context (duplicates allowed in different companies)
  - No uniqueness constraint
- Impact: Database constraint and validation logic

**6. What are the possible values for [field name]?**
- Context: Closed lists (selections) provide better data consistency and UI
- Options:
  - Fixed selection list (e.g., status: NEW, IN_PROGRESS, DONE)
  - Reference to another entity (e.g., category links to Category entity)
  - Free text (user can enter any value)
- Impact: Domain definition (Selection vs. many-to-one) and data consistency

**7. Are there length or format constraints for [field name]?**
- Context: Constraints ensure data quality and prevent errors
- Examples:
  - Maximum length (e.g., 255 characters for name)
  - Format pattern (e.g., email format, phone number format)
  - Value range (e.g., percentage between 0-100)
- Impact: Validation rules in domain and service layer

**8. Should [field name] have a default value?**
- Context: Default values improve user experience by pre-filling common values
- Options:
  - Static default (e.g., status = DRAFT)
  - Calculated default (e.g., date = today)
  - No default (user must fill)
- Impact: Domain definition and form initialization

### Entity Relationships

**9. What is the relationship between [Entity A] and [Entity B]?**
- Context: Axelor supports typed relationships that affect both data model and UI
- Options:
  - **One-to-many**: One A has many Bs (e.g., Customer → Orders)
  - **Many-to-one**: Many As belong to one B (e.g., Order → Customer)
  - **Many-to-many**: As related to multiple Bs and vice versa (e.g., Product ↔ Category)
  - **One-to-one**: Each A linked to exactly one B (rare)
- Impact: Domain definition, cascade rules, and UI widgets

**10. What happens when [related entity] is deleted?**
- Context: Cascade behavior must be defined for relationships
- Options:
  - **Cascade delete**: Delete related entities (e.g., delete Order deletes OrderLines)
  - **Prevent deletion**: Cannot delete if related entities exist (e.g., cannot delete Customer with Orders)
  - **Nullify**: Set relationship to null (e.g., delete Category keeps Products but removes category link)
- Impact: Database constraints and deletion workflow

**11. Is the relationship mandatory or optional?**
- Context: Cardinality affects data integrity and user workflow
- Options:
  - **0..1**: Optional, at most one (e.g., Lead can optionally link to one Company)
  - **1..1**: Required, exactly one (e.g., Order must have exactly one Customer)
  - **0..* **: Optional, multiple allowed (e.g., Customer can have zero or many Orders)
  - **1..* **: Required, at least one (e.g., Order must have at least one OrderLine)
- Impact: Validation rules and UI requirements

---

## Questions on Features and Business Logic

### Feature Trigger

**12. Who can trigger [feature name]?**
- Context: Access control and permissions must be defined
- Options:
  - All users
  - Specific roles (e.g., only Sales Manager)
  - Record owner/assignee only
  - Based on business rule (e.g., user from same department)
- Impact: Permission configuration and UI button visibility

**13. Where is [feature name] triggered from?**
- Context: Determines UI placement and workflow integration
- Options:
  - Button on form view
  - Button on grid view (mass action)
  - Menu action
  - Automatic trigger (scheduled, event-based)
- Impact: View definition and action configuration

**14. When can [feature name] be executed?**
- Context: Pre-conditions affect validation and workflow
- Examples:
  - Only in specific status (e.g., validate only if status = DRAFT)
  - Only if certain fields filled (e.g., cannot confirm order without lines)
  - Only during specific time period
- Impact: Service validation logic

### Feature Process

**15. What are the exact steps of [feature name]?**
- Context: Detailed process flow needed for service implementation
- Format:
  1. [First step with input/output]
  2. [Second step with conditions]
  3. [Final step with result]
- Impact: Service method implementation and error handling

**16. What validations should occur before [feature name] executes?**
- Context: Pre-condition validation prevents invalid operations
- Examples:
  - Field values (e.g., amount > 0)
  - Related entities (e.g., customer must be active)
  - Business rules (e.g., stock available)
  - Permissions (e.g., user authorized)
- Impact: Service validation method implementation

**17. What should happen after [feature name] completes?**
- Context: Post-conditions define expected outcome
- Examples:
  - Status change (e.g., DRAFT → VALIDATED)
  - Field updates (e.g., validation date = now)
  - Related entity creation (e.g., create invoice from order)
  - Notification/email sent
- Impact: Service implementation and workflow

**18. What should happen if [feature name] fails?**
- Context: Error handling and recovery strategy
- Options:
  - Display error message and abort
  - Display warning and ask user confirmation
  - Log error and continue partially
  - Rollback all changes
- Impact: Exception handling and transaction management

### Feature Messages

**19. What message should be displayed on success/error?**
- Context: User feedback is essential for good UX
- Examples:
  - Success: "Order validated successfully"
  - Error: "Cannot validate order: missing customer information"
  - Warning: "Order total is below minimum amount. Continue?"
- Impact: i18n message definitions and UI feedback

---

## Questions on User Interface

### Form View

**20. How should fields be organized on the [Entity] form?**
- Context: Logical grouping improves user experience
- Options:
  - By business logic (General Info, Details, Relationships)
  - By workflow stage (Data Entry, Validation, Completion)
  - By user role (visible to all vs. admin only)
- Impact: Form view layout definition

**21. Which fields should be read-only on the form?**
- Context: Some fields are calculated or system-managed
- Examples:
  - Calculated fields (e.g., total amount)
  - System fields (e.g., creation date, created by)
  - Status-dependent (e.g., editable only in DRAFT status)
- Impact: View definition with readonly conditions

**22. Should [related entities] be displayed inline or as popup?**
- Context: Affects user workflow and data entry efficiency
- Options:
  - **Inline grid**: Edit related entities directly in form (e.g., OrderLines in Order)
  - **Select widget**: Choose from existing entities (e.g., Customer in Order)
  - **Suggest widget**: Search and select with autocomplete
  - **Popup/modal**: Open related entity in new window
- Impact: View definition and widget choice

### Grid View

**23. What columns should be displayed in the [Entity] grid?**
- Context: Grid columns should show key information for identification and decision
- Typical columns:
  - Business identifier (code)
  - Display name
  - Status
  - Key dates (creation, validation)
  - Key relationships (customer, assigned user)
  - Key amounts/metrics
- Impact: Grid view column definition

**24. What filters should be available in the [Entity] grid?**
- Context: Filters help users find relevant records quickly
- Common filters:
  - By status (e.g., show only DRAFT orders)
  - By date range (e.g., orders from last month)
  - By user (e.g., my orders, orders assigned to me)
  - By relationship (e.g., orders for specific customer)
- Impact: Grid view filter definition

**25. What should be the default sort order?**
- Context: Initial sort order affects user perception
- Options:
  - Most recent first (by creation date DESC)
  - Alphabetical (by code or name ASC)
  - By status priority
  - By business rule (e.g., urgent first)
- Impact: Grid view orderBy attribute

### Dashboard/Cards

**26. What KPIs/metrics should be displayed on the [Entity] dashboard?**
- Context: Dashboards provide quick insights for decision-making
- Common metrics:
  - Count by status (e.g., 10 draft orders, 5 validated)
  - Sum of amounts (e.g., total order value this month)
  - Conversion rates (e.g., % of leads converted)
  - Trend charts (e.g., orders over time)
- Impact: Dashboard view definition and computation

---

## Questions on Cross-Cutting Concerns

### Security and Permissions

**27. What roles should exist for [module name]?**
- Context: Role-based access control is essential for security
- Common roles:
  - User (basic access)
  - Manager (validation rights)
  - Admin (full access including configuration)
- Impact: Permission rules definition

**28. What permissions should each role have on [Entity]?**
- Context: Fine-grained permissions control CRUD operations
- Permission matrix:
  - **Create**: Who can create new records?
  - **Read**: Who can view records?
  - **Update**: Who can modify records?
  - **Delete**: Who can delete records?
- Additional rules:
  - Can user modify only their own records?
  - Can user see only records from their department/company?
- Impact: MetaPermission XML configuration

### Internationalization

**29. What languages should be supported?**
- Context: Axelor supports multi-language applications
- Common languages:
  - French (fr)
  - English (en)
  - Spanish (es)
  - German (de)
- Impact: i18n message file generation

**30. What should be the default language?**
- Context: Fallback language for untranslated content
- Impact: Application configuration

### Import/Export

**31. What data needs to be imported, and in what format?**
- Context: Data migration and integration requirements
- Options:
  - CSV (simple, most common)
  - Excel (XLSX) (business user friendly)
  - XML (structured, system integration)
  - API (real-time integration)
- Details needed:
  - Column mapping
  - Frequency (one-time, daily, real-time)
  - Duplicate handling (update, skip, error)
- Impact: Data import configuration

**32. What data needs to be exported, and in what format?**
- Context: Reporting and external system needs
- Options:
  - CSV (data export)
  - Excel (business reports)
  - PDF (printable documents)
  - API (system integration)
- Impact: Export action configuration

---

## Questions on Workflow and Status

**33. What are the possible statuses for [Entity]?**
- Context: Status-driven workflows are common in business applications
- Format: List all statuses with business meaning
- Example: DRAFT, SUBMITTED, VALIDATED, COMPLETED, CANCELED
- Impact: Selection definition in domain

**34. What are the allowed status transitions?**
- Context: State machine defines valid workflow
- Format: A → B (condition)
- Example:
  - DRAFT → SUBMITTED (when all required fields filled)
  - SUBMITTED → VALIDATED (by manager only)
  - * → CANCELED (by admin at any time)
- Impact: Service validation logic and UI button visibility

**35. What actions are triggered during status changes?**
- Context: Status transitions often trigger side effects
- Examples:
  - Send email notification
  - Update related entities
  - Generate document (invoice, receipt)
  - Create audit log entry
- Impact: Service implementation in transition methods

---

## Using These Templates

### During Initial Analysis
1. Use templates as checklist to ensure no critical information is missed
2. Customize questions based on specific business domain
3. Group related questions for better conversation flow

### During Clarification
1. Present questions with context to help stakeholder understand why information is needed
2. Offer options based on Axelor patterns to guide decision
3. Explain impact to help stakeholder make informed choices

### During Documentation
1. Record answers with reference to questions asked
2. Document why certain choices were made
3. Create traceability between requirements and technical decisions

---

## See Also

- @docs/analysis/axelor-patterns-for-analysis.md - Common patterns to recognize
- @docs/analysis/large-document-strategy.md - Handling large specifications
- @templates/analysis-report-template.md - Output format
