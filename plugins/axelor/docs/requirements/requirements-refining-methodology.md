# Requirements Refining Methodology

Complete methodology for refining functional requirements for Axelor projects. Used by **requirements-refiner** agent.

**Reference**: For business types, see @docs/requirements/business-types-reference.md
**Reference**: For final template, see @docs/requirements/functional-specification-template.md

---

## Overview

The requirements refining process consists of 6 phases:

1. **Phase 1**: Understanding Validation
2. **Phase 2**: Entity Refining
3. **Phase 3**: View Refining
4. **Phase 4**: Feature Refining
5. **Phase 5**: Cross-cutting Aspects Refining
6. **Phase 6**: Consistency Validation

**Important**: Progress gradually, refine entity by entity, ask clarifying questions, reformulate regularly.

---

## Phase 1: Understanding Validation

### Objective

Validate global understanding of the requirement before diving into details.

### Process

Start by **reformulating** your understanding:

```markdown
## Global Understanding

Based on the analysis report, here is my understanding of the requirement:

### Main Objective

[Reformulate business objective in 2-3 sentences]

**Example**: "The objective is to provide sales teams with a lead management system that tracks prospects from initial contact through conversion to customers. The system should support lead qualification, activity tracking, and automated reminders."

### Functional Scope

[Summarize main expected features]

**Example**:
- Lead creation and management
- Activity logging (calls, emails, meetings)
- Lead qualification workflow
- Conversion to opportunities
- Sales pipeline dashboard

### Target Users

[Who will use the system and how]

**Example**:
- **Sales Representatives**: Create leads, log activities, qualify prospects
- **Sales Managers**: Review pipeline, assign leads, generate reports
- **Administrators**: Configure settings, manage permissions

**Is this global understanding correct?**
If certain points need correction, please specify which aspects are incorrect or incomplete.
```

### Validation

- Wait for client confirmation
- Clarify any misunderstandings
- Update understanding based on feedback
- Only proceed to Phase 2 after validation

---

## Phase 2: Entity Refining

### Objective

Refine each business entity with complete field and relationship definitions.

### Template

For each entity, use this template:

```markdown
## Refining: Entity [EntityName]

### Identification and Role

- **Entity Name**: [Technical name, e.g., Lead, Order, Product]
- **Business Role**: [In 1 sentence, what business concept this represents]
- **Concrete Examples**:
  - Example 1: [e.g., "Lead: John Smith from Acme Corp interested in Product X"]
  - Example 2: [e.g., "Lead: Jane Doe from Beta Inc requesting a demo"]

### Data Fields

**IMPORTANT**: Use business types from @docs/requirements/business-types-reference.md

For each field, specify:
- **Name**: [Business field name, e.g., name, email, status]
- **Nature**: [Short text | Long text | Whole number | Decimal number | Amount | Yes/No | Date | Date and time | File attachment | Selection from list]
- **Required**: [yes/no - Is this field mandatory for business operations?]
- **Unique**: [yes/no - Must this value be unique across all records?]
- **Possible Values**: [If "Selection from list", enumerate ALL possible business values]
- **Business Constraints**: [Business rules, e.g., "Must be a valid professional email", "Must be positive", "Cannot be in the past"]
- **Default Value**: [If applicable - business default]
- **Business Description**: [What is this field for from a business perspective]

#### Example Fields

**Field: code**
- **Name**: code
- **Nature**: Short text
- **Required**: yes
- **Unique**: yes
- **Business Constraints**: Auto-generated, unique identifier, alphanumeric, pattern LEAD-YYYY-NNNN
- **Default Value**: Auto-generated
- **Description**: Unique reference code for the lead

**Field: status**
- **Name**: status
- **Nature**: Selection from list
- **Required**: yes
- **Unique**: no
- **Possible Values**: NEW (default), CONTACTED, QUALIFIED, CONVERTED, LOST
- **Business Constraints**: Cannot change from CONVERTED to other statuses
- **Default Value**: NEW
- **Description**: Current state of the lead in the sales process

**Field: estimatedRevenue**
- **Name**: estimatedRevenue
- **Nature**: Amount
- **Required**: no (but required when status = QUALIFIED or CONVERTED)
- **Unique**: no
- **Business Constraints**: Must be positive, required for QUALIFIED/CONVERTED status
- **Default Value**: none
- **Description**: Estimated annual revenue potential if lead converts to customer

### Relationships with Other Entities

For each relationship, specify:
- **Type**: [one-to-many | many-to-one | many-to-many]
- **Target Entity**: [Name of related entity]
- **Cardinality**: [0..1 | 0..* | 1..1 | 1..*]
- **Relationship Name**: [Business name of the relationship]
- **Deletion Behavior**: [Business rule describing what happens when related entity is deleted]
- **Description**: [Why this relationship exists from a business perspective]

#### Example Relationships

**Relationship: company**
- **Type**: many-to-one
- **Target Entity**: Company
- **Cardinality**: 0..1 (a Lead can be linked to 0 or 1 Company)
- **Relationship Name**: company
- **Deletion Behavior**: When a Company is deleted, associated Leads should remain in the system but lose their company link (set to null)
- **Description**: Company to which the lead is attached for organizational purposes

**Relationship: activities**
- **Type**: one-to-many
- **Target Entity**: Activity
- **Cardinality**: 0..* (a Lead can have zero or many Activities)
- **Relationship Name**: activities
- **Deletion Behavior**: When a Lead is deleted, all associated Activities should also be deleted (cascade delete)
- **Description**: Collection of interactions (calls, emails, meetings) logged for this lead

### Business Rules and Validations

List all business rules that apply to this entity:

- **Validation 1**: [Rule description]
- **Validation 2**: [Rule description]
- **Automatic Calculation**: [If certain fields are calculated from others]
- **Derived Values**: [If certain values depend on other fields]

#### Example Business Rules

- **Rule 1**: Code is auto-generated following pattern LEAD-YYYY-NNNN where YYYY is year and NNNN is sequence number
- **Rule 2**: Email must be unique within the same company (two leads from different companies can have same email)
- **Rule 3**: Status cannot transition from CONVERTED back to any other status (one-way transition)
- **Rule 4**: EstimatedRevenue is required when status changes to QUALIFIED or CONVERTED
- **Rule 5**: LastContactDate must be automatically updated when an activity is logged
- **Calculated Field**: FullName = concatenation of firstName + " " + lastName
- **Derived Value**: DaysSinceLastContact = today() - lastContactDate

### Workflow and Statuses

If the entity has a lifecycle (status field):

- **Possible Statuses**: [List all status values]
- **Transitions**: [Which transitions are allowed between statuses]
- **Conditions**: [Conditions required to change from one status to another]
- **Actions**: [Actions triggered automatically during transitions]

#### Example Workflow

**Statuses**: NEW → CONTACTED → QUALIFIED → CONVERTED | LOST

**Transitions**:
- **NEW → CONTACTED**: When first activity (call/email/meeting) is logged
  - **Condition**: At least one activity must be logged
  - **Action**: Set firstContactDate = today()

- **CONTACTED → QUALIFIED**: When lead meets qualification criteria
  - **Condition**: estimatedRevenue must be set, assignedTo must be set
  - **Action**: Send notification to sales manager, log qualification event

- **QUALIFIED → CONVERTED**: When opportunity is created from lead
  - **Condition**: Requires manager approval
  - **Action**: Create opportunity, link to lead, send notification to sales team

- **(any) → LOST**: At any time if lead is not interested
  - **Condition**: Must provide reason for loss (required field: lostReason)
  - **Action**: Send notification to assigned sales rep, archive lead
```

### Clarifying Questions

Ask specific questions if elements are missing or ambiguous:

**Examples**:
- "Should the email field be unique globally or only within the same company?"
- "When a Company is deleted, what should happen to associated Leads: delete them too, keep them orphaned, or prevent deletion?"
- "Is estimatedRevenue required immediately when creating a lead, or only when qualifying it?"

---

## Phase 3: View Refining

### Objective

Define UI views for each entity: form view, grid view, optional dashboard.

### Template: Form View

```markdown
## Views for Entity [EntityName]

### Form View

**Objective**: Creation and edition of a [EntityName] instance

#### Field Organization (Panels)

Organize fields in **logical panels**:

**Panel "[Panel Name]"** (colSpan [value])
- Row 1: field1 (colSpan X), field2 (colSpan Y), ...
- Row 2: field3 (colSpan X), ...
- ...

**Example**:

**Panel "General Information"** (colSpan 12)
- Row 1: code (colSpan 3, readonly), status (colSpan 3, badge widget), priority (colSpan 3), source (colSpan 3)
- Row 2: name (colSpan 6, required), email (colSpan 6, required)
- Row 3: phone (colSpan 6), company (colSpan 6, suggest widget)

**Panel "Sales Information"** (colSpan 12)
- Row 1: assignedTo (colSpan 6, suggest widget), estimatedRevenue (colSpan 6, currency widget)
- Row 2: lastContactDate (colSpan 6), createdDate (colSpan 6, readonly)

**Panel "Notes"** (colSpan 12)
- notes (colSpan 12, text area, height: 200px)

**Panel "Activities"** (colSpan 12)
- activities (one-to-many panel-related, grid view, allow add/edit/delete)

**Panel "Converted Opportunity"** (colSpan 12, showIf: status == CONVERTED)
- convertedOpportunity (many-to-one panel, form view, readonly)

#### Read-only Fields

List fields that cannot be edited by users:

- code (auto-generated by system)
- createdDate (auto-set on creation)
- modifiedDate (auto-updated on save)
- convertedOpportunity (set by system during conversion)

#### Required Fields (Visual Indication)

List fields that must be marked as required in UI:

- name (red asterisk)
- email (red asterisk)
- status (red asterisk)
- estimatedRevenue (red asterisk when status = QUALIFIED or CONVERTED)

#### Action Buttons (Toolbar)

List buttons available in the form toolbar:

- **Button: "Qualify Lead"**
  - Visible when: status = CONTACTED
  - Action: onClick → action-lead-qualify
  - Icon: fa-check-circle

- **Button: "Convert to Opportunity"**
  - Visible when: status = QUALIFIED
  - Action: onClick → action-lead-convert
  - Icon: fa-exchange

- **Button: "Mark as Lost"**
  - Visible when: status != CONVERTED and status != LOST
  - Action: onClick → action-lead-mark-lost
  - Icon: fa-times-circle
  - Confirmation: "Are you sure you want to mark this lead as lost?"
```

### Template: Grid View

```markdown
### Grid View

**Objective**: List and search of [EntityName] instances

#### Displayed Columns

List columns in display order with width and properties:

1. **code**
   - Width: 100px
   - Sortable: yes
   - Searchable: no
   - Widget: default (text)

2. **name**
   - Width: 200px
   - Sortable: yes
   - Searchable: yes (full-text)
   - Widget: default (text)

3. **status**
   - Width: 120px
   - Sortable: yes
   - Filterable: yes (dropdown)
   - Widget: badge with colors (NEW: blue, CONTACTED: yellow, QUALIFIED: orange, CONVERTED: green, LOST: red)

4. **estimatedRevenue**
   - Width: 150px
   - Sortable: yes
   - Widget: currency (EUR)

#### Available Filters

- **Filter by status**: Dropdown selector
  - Options: All, NEW, CONTACTED, QUALIFIED, CONVERTED, LOST
  - Default: All

- **Filter by priority**: Dropdown selector
  - Options: All, LOW, MEDIUM, HIGH
  - Default: All

- **Filter by assigned user**: Suggest selector (search users)
  - Allows searching/selecting user
  - Default: All users

- **Filter by date range**: Date range picker
  - Field: lastContactDate
  - Options: Today, This week, This month, This quarter, Custom range

- **Text search**: Full-text search
  - Fields: name, email, company
  - Behavior: Searches across all three fields simultaneously

#### Default Sort

- **Column**: lastContactDate
- **Order**: DESC (most recent first)

#### Row Highlighting (Conditional Formatting)

- **Condition: priority == HIGH**: Background light red (#ffe6e6)
- **Condition: status == CONVERTED**: Background light green (#e6ffe6)
- **Condition: daysSinceLastContact > 30**: Background light yellow (#ffffcc) - warning for stale leads

#### Inline Actions (Per Row)

- **Edit**: Pencil icon, opens form view
- **Qualify**: Visible when status = CONTACTED, opens qualification dialog
- **Convert**: Visible when status = QUALIFIED, opens conversion wizard
```

### Template: Dashboard View (Optional)

```markdown
### Dashboard View

**Objective**: Visual summary and KPIs

#### Widgets

**Widget 1: [Widget Name]** (colSpan [value])
- Type: [Funnel chart | Pie chart | Bar chart | Line chart | Metric card | Table]
- Data: [Data source and calculation]
- Interactions: [Clickable? Drilldown?]
- Format: [Display format]
- Colors: [Color scheme]

**Example**:

**Widget 1: Lead Pipeline** (colSpan 12)
- Type: Funnel chart
- Data: Count of leads by status (NEW, CONTACTED, QUALIFIED, CONVERTED)
- Interactions: Clickable - click on status opens filtered grid view
- Colors: Blue (NEW), Yellow (CONTACTED), Orange (QUALIFIED), Green (CONVERTED)

**Widget 2: Conversion Rate** (colSpan 4)
- Type: Metric card
- Data: (Count CONVERTED / Total leads) * 100
- Format: "X.X% conversion rate"
- Colors: Green if > 20%, Yellow if 10-20%, Red if < 10%

**Widget 3: Estimated Revenue** (colSpan 4)
- Type: Metric card
- Data: SUM(estimatedRevenue) for status IN (QUALIFIED, CONVERTED)
- Format: Currency (EUR) with thousands separator

**Widget 4: Top Sales Reps** (colSpan 6)
- Type: Horizontal bar chart
- Data: Count of CONVERTED leads grouped by assignedTo
- Limit: Top 10 users
- Sort: DESC by count
- Interactions: Click on user opens filtered grid (leads for that user)
```

---

## Phase 4: Feature Refining

### Objective

Detail each business feature/process with complete specifications.

### Template

```markdown
## Feature: [Feature Name]

### Description

[Detailed description of what this feature does from a business perspective, 2-3 paragraphs]

**Example**:
"Allow sales representatives to mark a contacted lead as qualified when it meets the company's qualification criteria. Qualification requires setting estimated revenue and confirming the lead has genuine interest. This process ensures only serious prospects enter the opportunity pipeline."

### Trigger

- **Who**: [Which user roles can trigger this feature]
- **Where**: [From which view/screen and what UI element (button, menu item, etc.)]
- **When**: [In which context/state is this feature available]

**Example**:
- **Who**: Sales Representative, Sales Manager
- **Where**: From Lead form view, toolbar button "Qualify Lead"
- **When**: When lead status is CONTACTED

### Pre-conditions

List all conditions that must be true BEFORE the feature can execute:

- [Condition 1 that must be true before execution]
- [Condition 2]
- ...

**Example**:
- Lead status must be CONTACTED
- Lead must have at least one activity logged
- Lead must have email and phone filled
- User must be the assigned sales rep OR have manager role

### Process (Step-by-Step)

Describe the exact steps that happen when the feature executes:

1. [Step 1 - what happens first]
2. [Step 2]
3. [Step 3]
...

**Example**:
1. System validates all pre-conditions
2. System opens qualification dialog with fields:
   - EstimatedRevenue (required, amount field)
   - QualificationNotes (optional, long text field, height: 100px)
3. User enters estimated revenue and notes
4. User clicks "Confirm Qualification" button
5. System validates:
   - EstimatedRevenue > 0
   - Qualification notes not empty (if provided)
6. System updates lead record:
   - Set status = QUALIFIED
   - Set estimatedRevenue = entered value
   - Append qualification notes to notes field with timestamp
   - Set qualifiedDate = now()
   - Set qualifiedBy = current user
7. System logs activity: "Lead qualified with estimated revenue {amount} by {user}"
8. System sends notification to sales manager: "Lead {name} has been qualified by {user}"
9. System refreshes lead form view
10. System displays success message

### Post-conditions

List all results/effects AFTER the feature executes:

- [Result 1 after execution]
- [Result 2]
- ...

**Example**:
- Lead status is QUALIFIED
- EstimatedRevenue field is filled with entered value
- QualifiedDate is set to current date/time
- Activity log contains qualification entry
- Sales manager receives email notification
- "Convert to Opportunity" button now visible in form

### Validations

List all validation rules that must be checked:

- [Validation 1 to perform]
- [Validation 2]
- ...

**Example**:
- EstimatedRevenue must be greater than zero
- EstimatedRevenue must not exceed 10,000,000 EUR (show warning if exceeded, but allow)
- User must have permission "sales.lead.qualify"
- Lead cannot be qualified if status is CONVERTED or LOST
- Lead must have at least one activity logged in the last 90 days

### User Messages

Define all messages shown to user:

- **Success**: [Message displayed on success]
- **Error - [Scenario]**: [Error message for specific scenario]
- **Warning - [Scenario]**: [Warning message for specific scenario]

**Example**:
- **Success**: "Lead successfully qualified with estimated revenue {amount} EUR. Sales manager has been notified."
- **Error - Not contacted**: "Cannot qualify lead. Lead must be in CONTACTED status first."
- **Error - No activities**: "Cannot qualify lead. At least one activity must be logged before qualification."
- **Error - No permission**: "You do not have permission to qualify leads. Please contact your manager."
- **Warning - High revenue**: "Estimated revenue exceeds 10M EUR. Please confirm this is correct before proceeding."
- **Warning - Stale lead**: "This lead has not been contacted in 60 days. Are you sure you want to qualify it?"

### Concrete Example (Scenario)

Provide a complete example with real data:

**Example**:
"Sales rep John qualifies a contacted lead"

**Context**:
- Lead: "Jane Doe - Acme Corp"
- Current status: CONTACTED
- Activities logged: 2 (phone call on 2025-01-15, email on 2025-01-18)
- Assigned to: John Smith

**Action**:
1. John opens the lead form
2. John clicks "Qualify Lead" button in toolbar
3. System displays qualification dialog

**Input**:
- EstimatedRevenue: 50,000 EUR
- QualificationNotes: "Confirmed budget allocated for Q2 2025. Decision maker identified. Strong interest in Product X."

**Validation**:
- System validates amount is positive (50,000 > 0) ✓
- System validates user has permission ✓
- System validates lead status is CONTACTED ✓

**Update**:
- Status: CONTACTED → QUALIFIED
- EstimatedRevenue: null → 50,000 EUR
- QualifiedDate: null → 2025-01-20 14:30:00
- QualifiedBy: null → John Smith
- Notes: [existing notes] + "\n\n[2025-01-20] Qualification: Confirmed budget allocated for Q2 2025. Decision maker identified. Strong interest in Product X."

**Activity Log**:
- New entry: "Lead qualified with estimated revenue 50,000 EUR by John Smith on 2025-01-20"

**Notification**:
- Email sent to Sales Manager (Mary Johnson): "Lead Jane Doe - Acme Corp has been qualified by John Smith with estimated revenue 50,000 EUR"

**Result**:
- Lead form refreshes with updated data
- "Convert to Opportunity" button now visible in toolbar
- Success message displayed: "Lead successfully qualified with estimated revenue 50,000 EUR. Sales manager has been notified."
```

---

## Phase 5: Cross-cutting Aspects Refining

### Objective

Define aspects that apply across all entities: security, i18n, imports/exports, reporting, audit.

### Template: Security and Permissions

```markdown
## Security and Permissions

### User Roles

| Role | Description | Main Responsibilities |
|------|-------------|----------------------|
| [Role 1] | [Description] | [Responsibilities] |
| [Role 2] | [Description] | [Responsibilities] |

**Example**:

| Role | Description | Main Responsibilities |
|------|-------------|----------------------|
| Sales Representative | Field sales team member | Create leads, log activities, qualify own leads, update own leads |
| Sales Manager | Sales team manager | All Sales Rep permissions + update all leads, delete leads, convert to opportunities, assign leads, view reports |
| Sales Director | Senior sales leadership | All Manager permissions + export data, configure settings, access audit logs |
| Administrator | System administrator | Full access to all entities, configuration, user management |

### Permission Matrix

| Entity | Create | Read | Update | Delete |
|--------|--------|------|--------|--------|
| [Entity 1] | [Role] | [Role] | [Role] | [Role] |
| [Entity 2] | [Role] | [Role] | [Role] | [Role] |

**Example**:

| Entity | Create | Read | Update | Delete |
|--------|--------|------|--------|--------|
| Lead | Sales Rep | All users | Owner or Manager | Manager only |
| Activity | Sales Rep | All users | Creator only | Creator or Manager |
| Opportunity | Manager | All users | Owner or Manager | Director only |

### Specific Security Rules

- **Rule 1**: [Detailed permission rule]
- **Rule 2**: [Detailed permission rule]

**Example**:
- **Rule 1**: Sales Rep can only modify leads where assignedTo = current user (owner check)
- **Rule 2**: Sales Manager can modify any lead assigned to their team members
- **Rule 3**: Only Sales Manager+ can convert leads to opportunities
- **Rule 4**: Only Sales Director+ can delete CONVERTED leads (protect historical data)
- **Rule 5**: Read access is open to all authenticated users (for transparency and collaboration)
- **Rule 6**: Export permission restricted to Manager+ roles

### Data Privacy

- **PII Fields**: [List personally identifiable information fields]
- **Access Control**: [Who can access PII]
- **Export Restrictions**: [Special rules for exporting PII]
- **Deletion Policy**: [What happens to PII when record is deleted]

**Example**:
- **PII Fields**: email, phone, mobilePhone, address
- **Access Control**: Requires "data.privacy.view" permission (Manager+ roles)
- **Export Restrictions**: Export of email/phone requires explicit user consent checkbox in export dialog
- **Deletion Policy**: When lead is deleted, PII must be anonymized (replace name/email/phone with "DELETED-{date}")
```

### Template: Internationalization

```markdown
## Internationalization (i18n)

### Supported Languages

- [Language 1 (code)] - [default/optional]
- [Language 2 (code)] - [default/optional]

**Example**:
- English (en) - default
- French (fr)
- Spanish (es)
- German (de)

### Elements to Translate

- Field labels (all entity fields)
- View titles (form, grid, dashboard titles)
- Button labels (action buttons)
- User messages (success, error, warning messages)
- Selection values (status, priority, type values)
- Menu items
- Report titles

### Default Language

- [Language]: [code]

**Example**: English (en)

### Translation Strategy

- **Who translates**: [Internal team, external agency, community]
- **When**: [During development, after release, continuously]
- **Tool**: [Axelor built-in i18n, external tool]

**Example**:
- **Who translates**: Internal team for en/fr, external agency for es/de
- **When**: French translations during development, other languages after first release
- **Tool**: Axelor CSV message files (messages.csv, messages_fr.csv, etc.)
```

### Template: Imports/Exports

```markdown
## Imports/Exports

### Data Imports

- **Format**: [CSV, Excel, XML, API]
- **Importable Entities**: [List of entities]
- **Frequency**: [One-time, recurring, on-demand]
- **Mapping**: [How columns map to fields]
- **Duplicate Handling**: [Strategy if data already exists]
- **Validation**: [Business rules applied during import]

**Example**:
- **Format**: CSV, Excel (.xlsx)
- **Importable Entities**: Lead, Activity, Company
- **Frequency**: On-demand (manual upload by user via UI)
- **Mapping**: User selects column → field mapping via import wizard
- **Duplicate Handling**:
  - Check by email (if email exists in same company, update existing lead)
  - Option: Skip duplicates OR Overwrite existing data
  - Show preview before import with duplicates highlighted
- **Validation**: Same business rules as manual entry (email format, required fields, status transitions)

### Data Exports

- **Format**: [CSV, Excel, PDF, API]
- **Exportable Entities**: [List of entities]
- **Filters**: [Can user filter before export?]
- **Permissions**: [Who can export]

**Example**:
- **Format**: CSV, Excel (.xlsx), PDF
- **Exportable Entities**: Lead (with current grid filters applied), Activity
- **Filters**: Export respects current grid filters (status, assigned user, date range)
- **Permissions**: Requires "sales.lead.export" permission (Manager+ roles)
- **PII Protection**: Requires explicit consent checkbox when exporting email/phone fields
```

### Template: Reporting

```markdown
## Reporting

### Required Reports

**Report 1: [Report Name]**
- **Format**: [PDF, Excel, Web]
- **Filters**: [Available filters]
- **Data**: [What data is shown]
- **Grouping**: [How data is grouped]
- **Charts**: [Visual elements]
- **Schedule**: [Can it be scheduled? Email delivery?]

**Example**:

**Report 1: Lead Pipeline Report**
- **Format**: PDF, Excel
- **Filters**: Date range (from/to), status (multi-select), assigned user (suggest), source (multi-select)
- **Data**: Lead count by status, conversion rate, average time in each status, estimated revenue by status
- **Grouping**: By month, by sales rep, by source
- **Charts**: Funnel chart (pipeline stages), line chart (trend over time)
- **Schedule**: Can be scheduled daily/weekly/monthly with email delivery to managers

**Report 2: Sales Rep Performance Report**
- **Format**: PDF, Excel
- **Filters**: Date range, team (select), user (multi-select)
- **Data**: Leads created, qualified, converted per user; conversion rate; total estimated revenue; average deal size
- **Grouping**: By user, by team, by month
- **Charts**: Bar chart (top performers), line chart (performance trend)
- **Schedule**: Weekly email to managers on Monday morning
```

---

## Phase 6: Consistency Validation

### Objective

Verify that the specification is complete, consistent, and ready for architect.

### Checklist

Use this checklist before finalizing:

- [ ] **Business objectives** are clear and accurately described
- [ ] **All entities** have complete field definitions with business types
- [ ] **All fields** use business types from @docs/requirements/business-types-reference.md (NO technical types)
- [ ] **All relationships** have cardinality and deletion behavior specified
- [ ] **Bidirectional relationships** are consistent (A → B implies B ← A)
- [ ] **Deletion behaviors** are defined and logical (no orphan records unless intentional)
- [ ] **Status workflows** are complete with no orphan states (every status can be reached and has valid transitions)
- [ ] **Business rules** are specified for all validations
- [ ] **Permissions** cover all cases (no feature without permission check)
- [ ] **Views** expose all relevant fields (no missing fields in forms/grids)
- [ ] **Required fields** are consistent with business use cases
- [ ] **Selection values** are all listed (no missing enum values)
- [ ] **Features** have complete specifications (pre/post-conditions, validations, messages)
- [ ] **User messages** are defined for all scenarios (success, errors, warnings)
- [ ] **Security rules** are complete (roles, permissions, data privacy)
- [ ] **i18n requirements** are specified (languages, elements to translate)
- [ ] **Import/export** requirements are documented
- [ ] **Reports** are defined with filters and data
- [ ] **NO XML code** is present in the document
- [ ] **NO Java code** is present in the document
- [ ] **NO SQL code** is present in the document
- [ ] **NO technical types** are used (string, integer, decimal → use business types instead)
- [ ] **NO technical constraints** are specified (VARCHAR, NOT NULL → use business constraints instead)

### Validation Tool

**Use the skill to automate validation**:

```
/skill functional-spec-consistency-checker
```

This skill will:
- Read the generated specification document
- Check all items in the consistency checklist
- Identify missing or inconsistent elements
- Report violations (technical code, technical types, missing fields)
- Generate validation report

### Handling Inconsistencies

If you identify inconsistencies during validation:

1. **List the inconsistency**: "I found that entity Order has a relationship to Customer, but Customer does not have the reverse relationship to Order."
2. **Ask for clarification**: "Should Customer have a one-to-many relationship to Order?"
3. **Wait for answer**: Do not proceed until inconsistency is resolved
4. **Update specification**: Incorporate the resolution
5. **Re-validate**: Run consistency check again

---

## Interaction Guidelines

### Conversational Process

1. **Progress gradually**: Don't ask everything at once. Refine entity by entity.
2. **Reformulate regularly**: Summarize what was understood and ask for validation
3. **Propose options**: Based on common Axelor patterns, offer choices
4. **Explain implications**: Why each choice matters for implementation

**Example**:
"For the 'company' relationship, I see two options:
- Option A: Required (1..1) - Every lead MUST be linked to a company
- Option B: Optional (0..1) - Lead can exist without a company

Option A is stricter and better for B2B scenarios. Option B is more flexible for B2C or mixed scenarios. Which approach fits your business?"

### Tone and Style

- **Educational**: Explain Axelor concepts when necessary
- **Collaborative**: "We will refine together step by step..."
- **Structured**: Follow logical progression (entities → views → features)
- **Pragmatic**: Adapt to real business needs, avoid over-engineering

### Handling Ambiguities

If client gives ambiguous or incomplete answer:

1. **Reformulate** what you understood
2. **Ask a specific clarification question**
3. **Propose concrete examples** to illustrate

**Example**:

**Client says**: "Documents must be categorized"

**You respond**:
"Understood, you want to categorize documents. To clarify, which approach do you need:

- **Option A: Simple label** - One document = one category selected from list (e.g., 'Contract', 'Invoice', 'HR Document')
- **Option B: Hierarchical classification** - Multi-level categories (e.g., HR > Contracts > Permanent Contract)
- **Option C: Multiple tags** - One document can have multiple tags (e.g., tags: 'Urgent' + 'Confidential' + 'Client X')

Each option has different implications:
- Option A: Simple selection field in form
- Option B: Tree selector widget, more complex data model
- Option C: Many-to-many relationship with Tag entity

Which option fits your workflow?"

---

## Summary: Full Process Flow

1. **Read analysis report** from {output_directory}/analysis-report.md
2. **Read gap analysis** from {output_directory}/gap-analysis-report.md (if exists)
3. **Phase 1**: Validate global understanding → get confirmation
4. **Phase 2**: Refine entities one by one → validate each
5. **Phase 3**: Refine views for each entity → validate layouts
6. **Phase 4**: Refine features → validate processes
7. **Phase 5**: Refine cross-cutting aspects → validate security/i18n/imports
8. **Phase 6**: Run consistency validation → use skill: functional-spec-consistency-checker
9. **Generate final document** using template from @docs/requirements/functional-specification-template.md
10. **Present to client** for final approval

**Output**: {output_directory}/detailed-specifications.md (purely functional, NO technical code)

This document is then consumed by:
- **architect** agent (transforms functional → technical)
- **agile-agent** agent (breaks down into user stories)

---

**Remember**: You are creating FUNCTIONAL specifications. The architect will handle ALL technical implementation (XML, Java, SQL).
