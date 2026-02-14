# Refining Template - [Project Name]

**Date**: [Date]
**Version**: 1.0
**Status**: In Progress / To Validate / Validated

---

## 📋 Global Understanding

### Main Objective
[Reformulation of business objective in 2-3 sentences]

### Functional Scope
[Summary of main expected features]

### Target Users
[Who will use the system and how]

---

## 🔍 Business Entities

### Entity: [EntityName]

#### Identification
- **Technical Name**: [EntityName]
- **Business Role**: [In 1 sentence, what business concept]
- **Concrete Examples**: [1-2 examples of instances]

#### Fields

| Field | Type | Required | Unique | Constraints | Default Value | Description |
|-------|------|----------|--------|-------------|---------------|-------------|
| code | string | Yes | Yes | Max 64 char | - | Identifier code |
| name | string | Yes | No | Max 255 char | - | Full name |
| ... | ... | ... | ... | ... | ... | ... |

#### Relationships

| Relationship | Type | Target Entity | Cardinality | Cascade | Description |
|--------------|------|---------------|-------------|---------|-------------|
| company | many-to-one | Company | 0..1 | No | Attached company |
| ... | ... | ... | ... | ... | ... |

#### Business Rules
- [ ] Rule 1: [Description]
- [ ] Rule 2: [Description]

#### Workflow (if applicable)

**Statuses**: [List of statuses]

**Transitions**:
- [Status A] → [Status B]: [Condition]
- [Status B] → [Status C]: [Condition]

---

## 🖥️ Views and Interfaces

### Views for [EntityName]

#### Form View

**Field Organization**:

**Panel "General Information"**
- Field 1
- Field 2

**Panel "Details"**
- Field X
- Field Y

**Read-only Fields**: [List]

**Action Buttons**: [List]

#### Grid View

**Columns**:
1. [Column 1]
2. [Column 2]

**Filters**:
- Filter by: [Field]
- Filter by: [Field]

**Default Sort**: [Column], [ASC/DESC]

#### Dashboard View (optional)

**Indicators**:
- [KPI 1]
- [KPI 2]

---

## ⚙️ Features

### Feature: [Name]

- **Description**: [Detailed description]
- **Trigger**:
  - Who: [Role]
  - Where: [View/Button]
  - When: [Context]
- **Pre-conditions**:
  - [ ] Condition 1
  - [ ] Condition 2
- **Process**:
  1. Step 1
  2. Step 2
- **Post-conditions**:
  - Result 1
  - Result 2
- **Validations**:
  - Validation 1
  - Validation 2
- **Messages**:
  - Success: [Message]
  - Error: [Message]

---

## 🔒 Security

### User Roles
- **Role 1**: [Description and permissions]
- **Role 2**: [Description and permissions]

### Permission Matrix

| Entity | Create | Read | Update | Delete |
|--------|--------|------|--------|--------|
| [Entity1] | [Role] | [Role] | [Role] | [Role] |
| [Entity2] | [Role] | [Role] | [Role] | [Role] |

---

## 🌍 Cross-cutting Aspects

### Internationalization
- **Supported Languages**: [List]
- **Default Language**: [Language]

### Imports/Exports
- **Imports**: [Format, entities, frequency]
- **Exports**: [Format, entities]

---

## ✅ Validation

### Consistency Checklist
- [ ] All entities have a business identifier
- [ ] Bidirectional relationships are consistent
- [ ] Deletion cascades are defined
- [ ] Workflows are complete (no orphan states)
- [ ] Permissions cover all cases
- [ ] Views expose all relevant fields
- [ ] Required fields are consistent
- [ ] Business validations are complete and non-contradictory

### Open Questions
- [ ] Question 1: [To clarify]
- [ ] Question 2: [To clarify]

---

## 🚀 Next Steps

Once this document is validated:
1. Generation of EPICs and User Stories
2. Technical architecture design
3. Code generation
