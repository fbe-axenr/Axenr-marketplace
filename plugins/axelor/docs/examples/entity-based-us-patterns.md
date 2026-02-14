# Entity-Based User Story Patterns

This document provides reusable patterns for generating User Stories based on Axelor entity development. Use these patterns when decomposing entity-based EPICs.

## Overview

For each business entity in Axelor, the typical development follows this sequence:

1. **Domain Creation** → Defines the data structure
2. **Grid View** → Lists entity records
3. **Form View** → Creates/edits entity records
4. **Menu Integration** → Makes entity accessible from UI
5. **Business Logic** (optional) → Implements features beyond CRUD

Each step becomes a User Story following the patterns below.

---

## Pattern 1: Domain Creation

### Template

```textile
h3. US-XXX: Define [EntityName] Domain Model

*As a* developer
*I want* to create the [EntityName] domain definition
*So that* the data structure is generated and available for development

h4. Acceptance Criteria

* [ ] Domain XML created in src/main/resources/domains/[EntityName].xml
* [ ] All fields defined with correct types and constraints
* [ ] Relationships configured properly
* [ ] gradlew generateCode executes successfully
* [ ] Entity class generated in build/src-gen/

h4. Technical Details

* *Domain Fields:*
  - code: String (64) - required, unique
  - name: String (255) - required
  - status: Integer (selection) - required
  - [list all fields from specification]

* *Relationships:*
  - company: many-to-one Company (optional)
  - [list all relationships]

h4. Estimation

* *Complexity:* S
* *Estimated Effort:* 2-4 hours
```

### Usage Guidelines

**When to use**: For every new business entity

**Complexity factors**:
- **S (Small)**: 5-10 simple fields, 0-2 relationships
- **M (Medium)**: 10-20 fields, 3-5 relationships, some complex types
- **L (Large)**: 20+ fields, 6+ relationships, complex validations

**Field definition guidelines**:
- Always specify: type, max length, required/optional, unique constraint
- Use Axelor types: String, Integer, Boolean, BigDecimal, LocalDate, LocalDateTime
- Document selection lists with all possible values
- Specify cascade rules for relationships

### Complete Example

```textile
h3. US-001: Define Message Domain Model

*As a* developer
*I want* to create the Message entity domain definition with all required fields and relationships
*So that* the data structure for synchronized emails is available in Axelor

h4. Acceptance Criteria

* [ ] AC1: Domain XML created at src/main/resources/domains/Message.xml with correct namespace
* [ ] AC2: All core fields defined with correct types:
** messageId: String(255), required, unique
** subject: String(500), optional
** fromEmailAddress: String(255), required, email format
** receivedDateT: LocalDateTime, required
** statusSelect: Integer (selection), required, default=1
* [ ] AC3: Relationships configured:
** Many-to-many: emailAccountSet → EmailAccount
** One-to-many: attachments → MetaFile (cascade delete)
* [ ] AC4: Selection lists defined: statusSelect (1=Unread, 2=Read)
* [ ] AC5: Command "gradlew generateCode" executes without errors
* [ ] AC6: Entity class generated in build/src-gen/com/axelor/message/db/Message.java

h4. Technical Details

* *Module:* axelor-collaboration-connector
* *Domain XML Path:* src/main/resources/domains/Message.xml
* *Package:* com.axelor.message.db
* *Entity Name:* Message
* *Indexes Required:*
** Unique index on messageId
** Index on receivedDateT for sorting
** Index on statusSelect for filtering

h4. Estimation

* *Complexity:* M (Complex entity with many fields)
* *Estimated Effort:* 6 hours

h4. Dependencies

* Depends on: (None - foundational)
* Blocks: US-002 (Grid view), US-003 (Form view)
```

---

## Pattern 2: Grid View Creation

### Template

```textile
h3. US-XXX: Create [EntityName] Grid View

*As a* [user role]
*I want* to see a list of all [entities]
*So that* I can browse, search and select them

h4. Acceptance Criteria

* [ ] Grid displays columns: [list from specification]
* [ ] Filters available: [list from specification]
* [ ] Default sort: [field] [ASC/DESC]
* [ ] Search functionality works on [fields]
* [ ] Pagination works correctly
* [ ] Double-click opens form view

h4. Technical Details

* *View XML:* src/main/resources/views/[EntityName].xml
* *View type:* grid
* *Displayed columns:* [list with field types]
* *Filter fields:* [list]
* *Actions:* action-view to open form

h4. Estimation

* *Complexity:* S
* *Estimated Effort:* 2-3 hours
```

### Usage Guidelines

**When to use**: After domain creation, before form view

**Complexity factors**:
- **S (Small)**: 5-7 columns, basic filters, simple sort
- **M (Medium)**: 8-12 columns, advanced filters, custom formatting, conditional styling
- **L (Large)**: 12+ columns, complex filter logic, aggregations, custom widgets

**Column selection guidelines**:
- Include business identifier (code, name)
- Include key business fields (status, date, amount)
- Include relationship displays (company.name, customer.fullName)
- Limit to 8-10 columns for readability

### Complete Example

```textile
h3. US-002: Create Message Grid View for Email List

*As a* sales representative
*I want* to see a list of all my synchronized emails
*So that* I can quickly browse and select emails to read

h4. Acceptance Criteria

* [ ] AC1: Grid displays columns:
** Status Indicator (30px) - envelope icon
** From (200px, sortable) - fromName in bold if unread
** Subject (400px, sortable) - truncate at 50 chars
** Attachment (40px) - paperclip if hasAttachment=true
** Date (120px, sortable) - "Today 2:30 PM" format
* [ ] AC2: Default sort by receivedDateT descending
* [ ] AC3: Quick filters: "Unread Only", "With Attachments", "Important"
* [ ] AC4: Search bar filters by subject, fromEmailAddress, fromName
* [ ] AC5: Row click opens email detail form
* [ ] AC6: Right-click menu: "Mark as Read", "Delete"
* [ ] AC7: Grid respects user security (only own emails)

h4. Technical Details

* *View XML Path:* src/main/resources/views/Message.xml
* *View Name:* message-grid
* *Columns:*
** statusSelect: widget="image" with conditional icon
** fromName: widget="string" with CSS bold class
** hasAttachment: widget="boolean-icon"
** receivedDateT: widget="datetime" with smart formatting
* *Filters:*
** Quick filters: toolbar buttons with domain filters
** Search: searchFields="subject,fromEmailAddress,fromName"

h4. Estimation

* *Complexity:* M (Multiple filters, conditional formatting)
* *Estimated Effort:* 5 hours

h4. Dependencies

* Depends on: US-001 (Message domain)
* Blocks: (None)
```

---

## Pattern 3: Form View Creation

### Template

```textile
h3. US-XXX: Create [EntityName] Form View

*As a* [user role]
*I want* to create and edit [entity] records
*So that* I can manage [business concept]

h4. Acceptance Criteria

* [ ] Form organized in panels: [list panels from specification]
* [ ] All fields editable/read-only as specified
* [ ] Required fields marked with *
* [ ] Field validations work correctly
* [ ] Save and Cancel buttons functional
* [ ] [List any action buttons from specification]

h4. Technical Details

* *View XML:* src/main/resources/views/[EntityName].xml
* *View type:* form
* *Panels:*
  - General Information: [fields]
  - Details: [fields]
  - [other panels]
* *Actions:* save, cancel, [custom actions]

h4. Estimation

* *Complexity:* M
* *Estimated Effort:* 4-6 hours
```

### Usage Guidelines

**When to use**: After grid view, to enable creation/editing

**Complexity factors**:
- **S (Small)**: Single panel, 5-10 fields, basic layout
- **M (Medium)**: 2-3 panels, 10-20 fields, some conditional visibility
- **L (Large)**: 4+ panels, 20+ fields, complex widgets (html, many-to-many), conditional logic, custom actions

**Panel organization guidelines**:
- Group related fields logically
- Put most important fields in first panel
- Use collapsible panels for optional/advanced fields
- Separate read-only info panels from editable fields

### Complete Example

```textile
h3. US-003: Create Message Form View for Email Detail

*As a* sales representative
*I want* to open and read complete email content
*So that* I can view customer communications in full detail

h4. Acceptance Criteria

* [ ] AC1: Form organized in 4 panels:
** Panel 1 "Email Header": From, To, Cc, Subject, Date
** Panel 2 "Email Body": HTML-rendered body content
** Panel 3 "Attachments": Grid with download buttons
** Panel 4 "Related CRM": Hidden in Phase 1
* [ ] AC2: All fields read-only (emails not editable)
* [ ] AC3: Toolbar buttons:
** "Reply", "Forward" (visible if statusSelect=2)
** "Mark as Unread" (visible if statusSelect=2)
** "Delete", "Print" (always visible)
* [ ] AC4: Opening form auto-marks email as read
* [ ] AC5: HTML body renders securely (XSS prevention)

h4. Technical Details

* *View XML Path:* src/main/resources/views/Message.xml
* *View Name:* message-form
* *Panels:*
** panel-mail-header: colSpan="12", 2-column layout
** panel-mail-body: <field name="body" widget="html" readonly="true"/>
** panel-attachments: showIf="hasAttachment"
* *Actions:*
** action-message-auto-mark-read: OnLoad action
** action-message-reply, action-message-delete, etc.

h4. Estimation

* *Complexity:* L (Complex layout, HTML widget, conditional buttons)
* *Estimated Effort:* 8 hours

h4. Dependencies

* Depends on: US-001 (Message domain)
* Blocks: US-006 (Form button needs form)
```

---

## Pattern 4: Menu Integration

### Template

```textile
h3. US-XXX: Add [EntityName] Menu Entry

*As a* [user role]
*I want* to access [entities] from the main menu
*So that* I can navigate to the module easily

h4. Acceptance Criteria

* [ ] Menu entry visible in [module section]
* [ ] Menu opens grid view
* [ ] Icon displayed correctly
* [ ] Translation keys defined for all languages

h4. Technical Details

* *View XML:* src/main/resources/views/[EntityName].xml
* *Menu:* action-view + menu item
* *Parent menu:* [parent menu name]
* *Icon:* [icon name]

h4. Estimation

* *Complexity:* S
* *Estimated Effort:* 1 hour
```

### Usage Guidelines

**When to use**: After grid and form views exist

**Complexity**: Always S (Small) - 1 hour maximum

**Menu placement guidelines**:
- Place under logical parent menu (matching business domain)
- Use Font Awesome icons consistently
- Define order/priority for menu sorting
- Ensure translations for all supported languages

### Complete Example

```textile
h3. US-004: Add Message Menu Entry in Email Module

*As a* sales representative
*I want* to access email messages from the main menu
*So that* I can navigate to my inbox easily

h4. Acceptance Criteria

* [ ] Menu entry "Messages" visible under "Email" top menu
* [ ] Menu opens message-grid view
* [ ] Envelope icon (fa-envelope) displayed
* [ ] Translation keys defined for French and English

h4. Technical Details

* *View XML:* src/main/resources/views/Message.xml
* *Menu Item:*
** name: menu-message-all
** parent: menu-email
** action: action-message-view-grid
** icon: fa-envelope
** order: 10
* *Translations:*
** EN: "Messages"
** FR: "Messages"

h4. Estimation

* *Complexity:* S
* *Estimated Effort:* 1 hour

h4. Dependencies

* Depends on: US-002 (Grid view must exist)
* Blocks: (None)
```

---

## Pattern 5: Business Logic Implementation

### Template

```textile
h3. US-XXX: Implement [Feature Name] Logic

*As a* [user role]
*I want* [feature description]
*So that* [business benefit]

h4. Acceptance Criteria

* [ ] [List all acceptance criteria from feature specification]
* [ ] Validations implemented: [list]
* [ ] Error messages displayed: [list]
* [ ] Success message shown
* [ ] Unit tests written and passing

h4. Technical Details

* *Service:* [EntityName]Service
* *Methods:* [methodName](parameters) → return type
* *Business Logic:*
  - [Step 1 from specification]
  - [Step 2]
  - [Step 3]
* *Validations:* [list]
* *Exceptions:* [custom exceptions to throw]

h4. Estimation

* *Complexity:* [M or L depending on logic complexity]
* *Estimated Effort:* [X hours]
```

### Usage Guidelines

**When to use**: When entity requires business logic beyond CRUD

**Complexity factors**:
- **M (Medium)**: Single service method, simple validation, basic workflow
- **L (Large)**: Multiple service methods, complex validations, multi-step workflow, external integrations

**Service implementation guidelines**:
- One service class per entity (EntityNameService)
- Use dependency injection (@Inject)
- Implement transaction management (@Transactional)
- Write unit tests for all methods
- Document with JavaDoc

### Complete Example

```textile
h3. US-005: Implement Message Status Change Logic

*As a* sales representative
*I want* to mark emails as read or unread
*So that* I can manage my inbox and flag emails for follow-up

h4. Acceptance Criteria

* [ ] AC1: MessageService.markAsRead(message) updates statusSelect to 2
* [ ] AC2: MessageService.markAsUnread(message) updates statusSelect to 1
* [ ] AC3: Permission validation: user must have access to EmailAccount
* [ ] AC4: Audit trail logs status changes
* [ ] AC5: Bulk operations process multiple messages
* [ ] AC6: Error handling for permission denied
* [ ] AC7: Unit tests covering all methods

h4. Technical Details

* *Service:* com.axelor.message.service.MessageService
* *Dependencies:*
** @Inject MessageRepository messageRepository
** @Inject AuthService authService
** @Inject AuditTrailService auditTrailService
* *Methods:*
** markAsRead(Message message) → void
** markAsUnread(Message message) → void
** markAsReadBulk(List<Message> messages) → int
* *Business Logic:*
  1. Validate user permission on message's EmailAccount
  2. Update statusSelect field
  3. Set/clear readDateT timestamp
  4. Persist via repository
  5. Log audit trail
* *Validations:*
** User has READ permission on EmailAccount
** Message exists and is not null
** Sent emails (typeSelect=2) cannot be marked unread
* *Exceptions:*
** AxelorException(NO_ACCESS_PERMISSION) if permission denied
** AxelorException(CONFIGURATION_ERROR) for validation errors

h4. Estimation

* *Complexity:* M (Service with validation, permission checks, audit)
* *Estimated Effort:* 5 hours

h4. Dependencies

* Depends on: US-001 (Message domain)
* Blocks: US-006 (Grid actions need service)
```

---

## Typical Entity Development Sequence

For a complete entity, generate User Stories in this order:

```
1. US-XXX: Define [Entity] Domain Model           (S, 2-4h)
   ↓
2. US-XXX: Create [Entity] Grid View              (S-M, 2-5h)
   ↓
3. US-XXX: Create [Entity] Form View              (M-L, 4-8h)
   ↓
4. US-XXX: Add [Entity] Menu Entry                (S, 1h)
   ↓
5. US-XXX: Implement [Feature] Business Logic     (M-L, 4-8h per feature)
```

**Total typical effort per entity**: 1.5 - 3 days

---

## Related Documents

- [User Story Template](../templates/user-story-template.md)
- [EPIC Template](../templates/epic-template.md)
- [Special Case US Patterns](special-case-us-patterns.md)
