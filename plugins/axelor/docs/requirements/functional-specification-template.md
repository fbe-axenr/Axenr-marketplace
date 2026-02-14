# Functional Specification Template

This template is used by the **requirements-refiner** agent to generate the final functional specification document.

**IMPORTANT**: This template is for FUNCTIONAL specifications only. It contains NO technical implementation (XML, Java, SQL).

---

## Document Template

```markdown
# Detailed Functional Specifications - [Project/Module Name]

**Project**: [Project full name]
**Module**: [Module name]
**Version**: 1.0
**Date**: [Date]
**Author**: Axelor Requirements Refiner Agent
**Status**: Draft / To Validate / Validated

**IMPORTANT**: This document contains FUNCTIONAL specifications only. Technical implementation (domain XML, view XML, Java services) will be designed by the Technical Architect.

---

## 1. Overview

### 1.1 Business Objectives

[Describe the main business objectives in 2-3 paragraphs]

**Example**:
"The objective is to provide sales representatives with a comprehensive lead management system that enables tracking prospects from initial contact through conversion to customer. The system should support lead qualification, activity tracking, and automated follow-up reminders."

### 1.2 Functional Scope

**In Scope**:
- [Feature 1]
- [Feature 2]
- [Feature 3]

**Out of Scope** (Future phases):
- [Feature X]
- [Feature Y]

### 1.3 Target Users

| User Role | Description | Main Tasks |
|-----------|-------------|------------|
| Sales Representative | Field sales team | Create leads, log activities, convert to opportunities |
| Sales Manager | Sales team manager | Review pipeline, assign leads, generate reports |
| Administrator | System admin | Configure settings, manage permissions |

### 1.4 Constraints

- **Business Constraints**: [e.g., Must comply with GDPR, 30-day data retention policy]
- **Integration Constraints**: [e.g., Must integrate with existing CRM, Office 365 sync]
- **Performance Constraints**: [e.g., Grid must load in < 3 seconds with 10,000 records]
- **Regulatory Constraints**: [e.g., SOC 2 compliance required]

---

## 2. Data Model

### 2.1 Entity [EntityName1]

#### Description

[1-2 paragraphs describing what this entity represents from a business perspective]

**Business Role**: [In 1 sentence, what business concept this entity represents]

**Concrete Examples**:
- Example 1: [e.g., "Lead: John Smith from Acme Corp interested in Product X"]
- Example 2: [e.g., "Lead: Jane Doe from Beta Inc requesting a demo"]

#### Fields

**Use business types from @docs/requirements/business-types-reference.md**

| Field | Nature | Required | Unique | Business Constraints | Description |
|-------|--------|----------|--------|----------------------|-------------|
| code | Short text | Yes | Yes | Auto-generated, unique identifier | Lead reference code |
| name | Short text | Yes | No | Cannot be empty | Lead full name |
| email | Short text | Yes | No | Valid email format | Contact email address |
| phone | Short text | No | No | Valid phone format | Contact phone number |
| company | Short text | No | No | - | Company name |
| status | Selection from list | Yes | No | NEW, CONTACTED, QUALIFIED, CONVERTED, LOST | Current lead status |
| source | Selection from list | No | No | WEB, PHONE, EMAIL, REFERRAL, EVENT | Lead acquisition source |
| estimatedRevenue | Amount | No | No | Must be positive | Estimated annual revenue potential |
| priority | Selection from list | No | No | LOW, MEDIUM, HIGH | Lead priority level |
| assignedTo | Short text | No | No | Must be valid user | Sales rep assigned to this lead |
| notes | Long text | No | No | - | Internal notes and comments |
| createdDate | Date and time | Yes | No | Auto-set on creation | Record creation timestamp |
| lastContactDate | Date | No | No | Cannot be in the future | Date of last contact with lead |

#### Relationships

| Relationship | Type | Target Entity | Cardinality | Deletion Behavior | Description |
|--------------|------|---------------|-------------|-------------------|-------------|
| company | many-to-one | Company | 0..1 | Leads remain when Company deleted | Company to which lead is attached |
| activities | one-to-many | Activity | 0..* | Activities deleted when Lead deleted | Activities logged for this lead |
| convertedOpportunity | one-to-one | Opportunity | 0..1 | Link cleared when Opportunity deleted | Opportunity created from this lead |

#### Business Rules

- **Rule 1**: Code is auto-generated following pattern: LEAD-YYYY-NNNN
- **Rule 2**: Email must be unique within the same company
- **Rule 3**: Status cannot change from CONVERTED back to any other status
- **Rule 4**: EstimatedRevenue is required when status is QUALIFIED or CONVERTED
- **Rule 5**: LastContactDate must be updated when an activity is logged

#### Workflow

**Status Transitions**:

```
NEW → CONTACTED: When first activity (call/email) is logged
CONTACTED → QUALIFIED: When lead meets qualification criteria
QUALIFIED → CONVERTED: When opportunity is created from lead
* → LOST: At any time if lead is not interested
```

**Conditions for Transitions**:
- NEW → CONTACTED: At least one activity must be logged
- CONTACTED → QUALIFIED: Must have estimatedRevenue and assignedTo set
- QUALIFIED → CONVERTED: Requires manager approval
- * → LOST: Requires reason for loss (mandatory field)

---

## 3. Views and Interfaces

### 3.1 Views for [EntityName1]

#### Form View

**Objective**: Creation and edition of a [EntityName1] instance

**Field Organization** (Panels):

**Panel "General Information"** (colSpan 12)
- Row 1: code (colSpan 3, readonly), status (colSpan 3), priority (colSpan 3), source (colSpan 3)
- Row 2: name (colSpan 6, required), email (colSpan 6, required)
- Row 3: phone (colSpan 6), company (colSpan 6, suggest widget)

**Panel "Sales Information"** (colSpan 12)
- Row 1: assignedTo (colSpan 6, suggest widget), estimatedRevenue (colSpan 6)
- Row 2: lastContactDate (colSpan 6), createdDate (colSpan 6, readonly)

**Panel "Notes"** (colSpan 12)
- notes (colSpan 12, height: 200px)

**Panel "Activities"** (colSpan 12)
- activities (one-to-many panel-related, grid view, allow add/edit/delete)

**Panel "Converted Opportunity"** (colSpan 12, showIf: status == CONVERTED)
- convertedOpportunity (many-to-one panel, form view, readonly)

**Read-only Fields**:
- code (auto-generated)
- createdDate (auto-set)
- convertedOpportunity (set by system on conversion)

**Required Fields** (visual indication):
- name (red asterisk)
- email (red asterisk)
- status (red asterisk)
- estimatedRevenue (red asterisk when status = QUALIFIED or CONVERTED)

**Action Buttons** (toolbar):
- "Qualify Lead" (visible when status = CONTACTED, onClick: action-lead-qualify)
- "Convert to Opportunity" (visible when status = QUALIFIED, onClick: action-lead-convert)
- "Mark as Lost" (visible when status != CONVERTED and status != LOST, onClick: action-lead-mark-lost)

#### Grid View

**Objective**: List and search of [EntityName1] instances

**Displayed Columns**:
1. code (width: 100px, sortable)
2. name (width: 200px, sortable, searchable)
3. company (width: 150px, sortable)
4. status (width: 120px, sortable, filterable, badge widget with colors)
5. priority (width: 100px, sortable, filterable, icon widget)
6. estimatedRevenue (width: 150px, sortable, currency widget)
7. assignedTo (width: 150px, sortable, filterable)
8. lastContactDate (width: 120px, sortable)

**Available Filters**:
- **Filter by status**: Dropdown with options (All, NEW, CONTACTED, QUALIFIED, CONVERTED, LOST)
- **Filter by priority**: Dropdown with options (All, LOW, MEDIUM, HIGH)
- **Filter by assigned user**: Suggest selector (search users)
- **Filter by date range**: lastContactDate (date range picker)
- **Text search**: On fields: name, email, company (full-text search)

**Default Sort**: lastContactDate DESC (most recent first)

**Row Highlighting**:
- Priority HIGH: Light red background
- Status CONVERTED: Light green background
- No activity in 30+ days: Light yellow background (warning)

**Inline Actions** (per row):
- "Edit" (pencil icon)
- "Qualify" (visible when status = CONTACTED)
- "Convert" (visible when status = QUALIFIED)

#### Dashboard View (Optional)

**Objective**: Visual summary and KPIs

**Widgets**:

**Widget 1: Lead Pipeline** (colSpan 12)
- Type: Funnel chart
- Data: Count of leads by status (NEW, CONTACTED, QUALIFIED, CONVERTED)
- Clickable: Click on status opens filtered grid

**Widget 2: Conversion Rate** (colSpan 4)
- Type: Metric card
- Data: (CONVERTED count / Total leads) * 100
- Format: "X% conversion rate"
- Color: Green if > 20%, Yellow if 10-20%, Red if < 10%

**Widget 3: Estimated Revenue** (colSpan 4)
- Type: Metric card
- Data: SUM(estimatedRevenue) for QUALIFIED and CONVERTED leads
- Format: Currency (EUR)

**Widget 4: Activities This Week** (colSpan 4)
- Type: Metric card
- Data: Count of activities logged this week
- Format: "X activities"

**Widget 5: Top Sales Reps** (colSpan 6)
- Type: Bar chart (horizontal)
- Data: Count of CONVERTED leads per assignedTo
- Limit: Top 10 users
- Sort: DESC by count

**Widget 6: Lead Source Distribution** (colSpan 6)
- Type: Pie chart
- Data: Count of leads by source
- Colors: Distinct color per source

---

## 4. Features

### 4.1 [Feature Name]

**Example: Qualify Lead**

#### Description

Allow sales representatives to mark a contacted lead as qualified when it meets the company's qualification criteria. Qualification requires setting estimated revenue and confirming the lead has genuine interest.

#### Trigger

- **Who**: Sales Representative, Sales Manager
- **Where**: From Lead form view, toolbar button "Qualify Lead"
- **When**: When lead status is CONTACTED

#### Pre-conditions

- Lead status must be CONTACTED
- Lead must have at least one activity logged
- Lead must have email and phone filled
- User must be the assigned sales rep or have manager role

#### Process

1. System validates all pre-conditions
2. System opens qualification dialog with fields:
   - EstimatedRevenue (required, amount field)
   - QualificationNotes (optional, long text)
3. User enters estimated revenue and notes
4. User clicks "Confirm Qualification"
5. System validates:
   - EstimatedRevenue > 0
   - Qualification notes not empty (if entered)
6. System updates lead:
   - Set status = QUALIFIED
   - Set estimatedRevenue = entered value
   - Append qualification notes to notes field
   - Set qualifiedDate = now()
7. System logs activity: "Lead qualified with estimated revenue {amount}"
8. System sends notification to sales manager: "Lead {name} has been qualified"
9. System refreshes lead form

#### Post-conditions

- Lead status is QUALIFIED
- EstimatedRevenue field is filled
- QualifiedDate is set to current date/time
- Activity log contains qualification entry
- Sales manager receives notification

#### Validations

- EstimatedRevenue must be greater than zero
- EstimatedRevenue must not exceed 10,000,000 (validation warning)
- User must have permission "sales.lead.qualify"
- Lead cannot be qualified if already CONVERTED or LOST

#### User Messages

- **Success**: "Lead successfully qualified with estimated revenue {amount}. Sales manager has been notified."
- **Error - Not contacted**: "Cannot qualify lead. Lead must be in CONTACTED status first."
- **Error - No activities**: "Cannot qualify lead. At least one activity must be logged before qualification."
- **Error - No permission**: "You do not have permission to qualify leads."
- **Warning - High revenue**: "Estimated revenue exceeds 10M. Please confirm this is correct."

#### Concrete Example

**Scenario**: Sales rep John qualifies a contacted lead

1. **Context**: Lead "Jane Doe - Acme Corp" is in CONTACTED status, has 2 activities logged (phone call and email)
2. **Action**: John opens the lead form and clicks "Qualify Lead"
3. **Dialog**: System shows qualification dialog
4. **Input**: John enters estimatedRevenue = 50,000 EUR and notes = "Confirmed budget allocated for Q2"
5. **Validation**: System validates amount is positive
6. **Update**: System sets status = QUALIFIED, estimatedRevenue = 50,000
7. **Activity**: System logs "Lead qualified with estimated revenue 50,000 EUR by John Smith"
8. **Notification**: Sales manager receives email "Lead Jane Doe - Acme Corp has been qualified with 50K EUR"
9. **Result**: Lead form refreshes, "Convert to Opportunity" button now visible

---

## 5. Security and Permissions

### 5.1 User Roles

| Role | Description | Permissions |
|------|-------------|-------------|
| Sales Representative | Field sales team member | Create, read, update own leads; read all leads; qualify own leads |
| Sales Manager | Sales team manager | All Sales Rep permissions + update all leads, delete leads, convert to opportunity, assign leads |
| Sales Director | Senior sales leadership | All permissions + delete any lead, export data, configure settings |
| Administrator | System administrator | Full access to all entities and configuration |

### 5.2 Permission Matrix

| Entity | Create | Read | Update | Delete |
|--------|--------|------|--------|--------|
| **Lead** | Sales Rep | All users | Owner or Manager | Manager only |
| **Activity** | Sales Rep | All users | Creator only | Creator or Manager |
| **Opportunity** | Manager | All users | Owner or Manager | Director only |

### 5.3 Specific Rules

- **Rule 1**: Sales Rep can only modify leads assigned to them (assignedTo = current user)
- **Rule 2**: Sales Manager can modify any lead in their team
- **Rule 3**: Only Sales Manager+ can convert leads to opportunities
- **Rule 4**: Only Sales Director+ can delete CONVERTED leads
- **Rule 5**: Read access is open to all authenticated users (for transparency)
- **Rule 6**: Export permission restricted to Manager+ role

### 5.4 Data Privacy

- Email and phone fields are PII (Personal Identifiable Information)
- Access to these fields requires "data.privacy.view" permission
- Export of email/phone requires explicit user consent checkbox
- Deletion of lead must anonymize data (replace name/email/phone with "DELETED")

---

## 6. Cross-cutting Aspects

### 6.1 Internationalization

**Supported Languages**:
- English (en) - default
- French (fr)
- Spanish (es)

**Elements to Translate**:
- All field labels (name, email, status, etc.)
- All view titles (Lead Form, Lead Grid, etc.)
- All button labels (Qualify Lead, Convert to Opportunity, etc.)
- All user messages (success, error, warning)
- All selection values (Status: NEW/CONTACTED/QUALIFIED, Priority: LOW/MEDIUM/HIGH)

**Default Language**: English (en)

**Translation Keys** (examples):
- `lead.form.title` = "Lead"
- `lead.field.name` = "Name"
- `lead.status.new` = "New"
- `lead.action.qualify` = "Qualify Lead"
- `lead.message.qualified.success` = "Lead successfully qualified"

### 6.2 Imports/Exports

**Data Imports**:
- **Format**: CSV, Excel (.xlsx)
- **Importable Entities**: Lead, Activity
- **Frequency**: On-demand (manual upload by user)
- **Mapping**: User selects column → field mapping via wizard
- **Duplicate Handling**:
  - Check by email (if email exists, update existing lead)
  - Option to skip or overwrite existing data
- **Validation**: Same business rules as manual entry

**Data Exports**:
- **Format**: CSV, Excel (.xlsx), PDF
- **Exportable Entities**: Lead (with filters applied)
- **Filters**: Export respects current grid filters
- **Permissions**: Requires "sales.lead.export" permission
- **PII Protection**: Requires explicit consent checkbox for email/phone export

### 6.3 Reporting

**Required Reports**:

**Report 1: Lead Pipeline Report**
- **Format**: PDF, Excel
- **Filters**: Date range, status, assigned user, source
- **Data**: Lead count by status, conversion rate, average time in each status
- **Grouping**: By month, by user, by source
- **Charts**: Funnel chart, trend line

**Report 2: Sales Rep Performance Report**
- **Format**: PDF, Excel
- **Filters**: Date range, team, user
- **Data**: Leads created, qualified, converted per user; conversion rate; total estimated revenue
- **Grouping**: By user, by team
- **Charts**: Bar chart (top performers), line chart (trend over time)

**Report 3: Lead Source ROI Report**
- **Format**: PDF, Excel
- **Filters**: Date range, source
- **Data**: Leads by source, conversion rate by source, revenue by source
- **Grouping**: By source
- **Charts**: Pie chart (distribution), bar chart (revenue by source)

### 6.4 Audit Trail

**Tracked Changes**:
- All status changes (with user, date, old value, new value)
- Assignment changes (assignedTo field)
- Qualification events (date, user, estimated revenue)
- Conversion events (date, user, opportunity created)

**Retention**: 7 years (compliance requirement)

**Access**: Audit log visible to Manager+ roles only

---

## 7. Appendices

### 7.1 Glossary

| Term | Definition |
|------|------------|
| Lead | A potential customer who has expressed interest in products/services |
| Qualification | The process of determining if a lead meets criteria to become an opportunity |
| Conversion | The act of creating an opportunity from a qualified lead |
| Activity | An interaction with a lead (call, email, meeting) |
| Pipeline | The collection of leads at various stages of the sales process |
| Estimated Revenue | The potential annual revenue if lead converts to customer |

### 7.2 Detailed Use Cases

**Use Case 1: Sales Rep Creates and Qualifies a Lead**

**Actors**: Sales Rep (John Smith)

**Scenario**:
1. John receives inquiry from Jane Doe at Acme Corp via website form
2. John opens Axelor and navigates to Leads module
3. John clicks "New Lead" and fills in:
   - Name: Jane Doe
   - Email: jane.doe@acme.com
   - Phone: +1-555-1234
   - Company: Acme Corp
   - Source: WEB
   - Priority: MEDIUM
   - AssignedTo: John Smith (auto-filled)
4. System auto-generates code: LEAD-2025-00123
5. System sets status: NEW
6. John saves the lead
7. John logs first activity: Phone call, duration 15 minutes, notes: "Discussed product X requirements"
8. System changes status from NEW to CONTACTED
9. After call, John clicks "Qualify Lead"
10. John enters estimatedRevenue: 75,000 EUR, notes: "Budget confirmed for Q2 2025"
11. System validates and sets status: QUALIFIED
12. Sales Manager receives notification
13. John can now proceed to "Convert to Opportunity"

**Use Case 2: Sales Manager Reviews and Reassigns Leads**

[Additional use cases...]

### 7.3 Wireframes/Mockups

[Placeholder for UI mockups - to be provided by UX team]

---

## 8. Validation

**To be validated by**: [Client name or Product Owner]
**Validation deadline**: [Date]

### Validation Checklist

- [ ] Business objectives are clear and accurate
- [ ] All entities and fields are defined
- [ ] All business rules are specified
- [ ] All workflows are complete
- [ ] View layouts are described
- [ ] Features are detailed with examples
- [ ] Security permissions are defined
- [ ] Internationalization requirements are clear
- [ ] Import/export requirements are specified
- [ ] Reports are defined

### Signatures

- **Client/Product Owner**: ____________________ Date: ____
- **Technical Lead**: ____________________ Date: ____
- **Project Manager**: ____________________ Date: ____

---

## 9. Next Steps

Once this functional specification is validated:

1. **Technical Architect** will transform it into technical architecture (domain XML, view XML, Java services)
2. **EPIC/US Generator** will break it down into implementable user stories
3. **Development Team** will implement based on architecture plan
4. **Code Reviewer** will verify compliance with architecture and quality standards

**Estimated Effort**: [To be determined by architect]

**Target Completion**: [To be determined by project manager]

---

**END OF FUNCTIONAL SPECIFICATION**
```

---

## Usage Guidelines for Requirements Refiner Agent

### When to Use This Template

Use this template to structure the **final output** after all phases of refinement are complete:
- Phase 1: Understanding validation ✓
- Phase 2: Entity refining ✓
- Phase 3: View refining ✓
- Phase 4: Feature refining ✓
- Phase 5: Cross-cutting aspects ✓
- Phase 6: Consistency validation ✓

### How to Populate

1. **Start with Overview**: Reformulate business objectives from analysis report
2. **Build Data Model**: One entity at a time, using templates from requirements-refining-methodology.md
3. **Design Views**: For each entity, specify form/grid/dashboard views
4. **Detail Features**: For each major feature, use the feature template
5. **Add Cross-cutting**: Security, i18n, imports, reporting
6. **Complete Appendices**: Glossary, use cases, validation checklist

### What NOT to Include

❌ **NO XML code** (domain definitions, view definitions, selections)
❌ **NO Java code** (services, repositories, controllers)
❌ **NO SQL code** (CREATE TABLE, ALTER TABLE, indexes)
❌ **NO technical types** (string, integer, decimal) - use business types from business-types-reference.md
❌ **NO technical constraints** (VARCHAR, NOT NULL, CHECK) - use business constraints
❌ **NO file paths** (src/main/resources/domains/Entity.xml)

### Validation Before Finalizing

Before generating the final document, use:
```
/skill functional-spec-consistency-checker
```

This skill will verify:
- All entities have identifiers
- All relationships are bidirectional
- All status workflows are complete
- All permissions are defined
- All views expose relevant fields
- No technical code is present

---

## Template Sections Explained

| Section | Purpose | Key Elements |
|---------|---------|--------------|
| **1. Overview** | Set context and scope | Objectives, scope, users, constraints |
| **2. Data Model** | Define business entities | Fields (business types), relationships, rules, workflows |
| **3. Views** | Specify UI layout | Form panels, grid columns, dashboard widgets |
| **4. Features** | Detail business processes | Triggers, pre/post-conditions, validations, messages |
| **5. Security** | Define access control | Roles, permissions, data privacy |
| **6. Cross-cutting** | Address non-functional | i18n, imports/exports, reporting, audit |
| **7. Appendices** | Support documentation | Glossary, use cases, wireframes |
| **8. Validation** | Approval tracking | Checklist, signatures, next steps |

---

## Examples of Well-Written Sections

See **@docs/examples/** for complete functional specification examples:
- `lead-management-functional-spec.md` - Full example following this template
- `order-processing-functional-spec.md` - Complex workflow example
- `customer-portal-functional-spec.md` - Multi-role security example

---

This template ensures **clear, complete, and purely functional** specifications that the architect can transform into battle-tested technical implementation.
