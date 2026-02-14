# Requirement Analysis - [Project/Module Name]

**Document analyzed**: [Title of source document]
**Analysis date**: [Date]
**Analyst**: [Agent/Person name]
**Status**: Draft / For Review / Validated

---

## 1. Document Overview

### 1.1 Source Document Information

**Document type**: [Cahier des charges / Functional specification / RFP / Meeting notes / etc.]
**Version**: [Document version]
**Date**: [Document date]
**Pages**: [Number of pages]
**Authors**: [Document authors]

### 1.2 Analysis Scope

[Brief description of what was analyzed - 2-3 sentences]

---

## 2. Business Understanding

### 2.1 Business Objectives

[Summarize the main business objectives of the project in 2-4 bullet points]

- **Primary objective**: [Main goal - why this project exists]
- **Secondary objectives**: [Supporting goals]
- **Success criteria**: [How success will be measured]

### 2.2 Business Context

[Describe the business context in 1-2 paragraphs: industry, current situation, problems to solve]

### 2.3 Target Users

| User Role | Description | Key Needs |
|-----------|-------------|-----------|
| [Role 1] | [Who they are] | [What they need from the system] |
| [Role 2] | [Who they are] | [What they need from the system] |
| ... | ... | ... |

### 2.4 Key Stakeholders

- **Product Owner**: [Name/role]
- **Technical Lead**: [Name/role]
- **Business Sponsor**: [Name/role]
- **End Users**: [Teams/departments]

---

## 3. Business Entities Identified

### 3.1 Entity Summary

| Entity Name | Business Role | Complexity | Priority |
|-------------|---------------|------------|----------|
| [Entity1] | [Brief description] | [Simple/Medium/Complex] | [High/Medium/Low] |
| [Entity2] | [Brief description] | [Simple/Medium/Complex] | [High/Medium/Low] |
| ... | ... | ... | ... |

### 3.2 Entity Details

#### Entity: [EntityName1]

**Business Role**: [What business concept this entity represents - 1 sentence]

**Known Fields**:
- `code` (String, unique, required) - Business identifier
- `name` (String, required) - Display name
- `status` (Selection, required) - Workflow status: DRAFT, VALIDATED, CANCELED
- [Additional fields identified from document]

**Known Relationships**:
- `[relationshipName]` (many-to-one → [TargetEntity]) - [Description]
- `[relationshipName]` (one-to-many ← [TargetEntity]) - [Description]

**Lifecycle/Workflow**: [If applicable, describe status transitions]
- DRAFT → VALIDATED (when all information complete)
- VALIDATED → CANCELED (if no longer needed)

**Mentioned in document**: [Pages/sections where discussed]

---

#### Entity: [EntityName2]

[Same structure as above]

---

[Repeat for all entities]

---

## 4. Features Identified

### 4.1 Feature Summary

| Feature ID | Feature Name | Entity | Priority | Complexity |
|------------|--------------|--------|----------|------------|
| F01 | [Feature name] | [Entity] | [High/Medium/Low] | [Simple/Medium/Complex] |
| F02 | [Feature name] | [Entity] | [High/Medium/Low] | [Simple/Medium/Complex] |
| ... | ... | ... | ... | ... |

### 4.2 Feature Details

#### Feature F01: [Feature Name]

**Description**: [What this feature does - 1-2 sentences]

**Business Value**: [Why this feature is needed - business justification]

**Trigger**:
- **Who**: [User role]
- **Where**: [From which view/screen]
- **When**: [In which context/state]

**Process** (high-level):
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Known Validations**:
- [Validation 1]
- [Validation 2]

**Known Business Rules**:
- [Rule 1]
- [Rule 2]

**Mentioned in document**: [Pages/sections where discussed]

---

#### Feature F02: [Feature Name]

[Same structure as above]

---

[Repeat for all features]

---

## 5. User Interface Requirements

### 5.1 Views Identified

| Entity | Form View | Grid View | Dashboard | Actions |
|--------|-----------|-----------|-----------|---------|
| [Entity1] | ✅ | ✅ | ❌ | [Button list] |
| [Entity2] | ✅ | ✅ | ✅ | [Button list] |
| ... | ... | ... | ... | ... |

### 5.2 View Details

#### [Entity1] Views

**Form View**:
- **Known panels**: [List of panels/sections mentioned]
- **Known fields to display**: [List from document]
- **Known read-only fields**: [List from document]
- **Known action buttons**: [List from document]

**Grid View**:
- **Known columns**: [List from document]
- **Known filters**: [List from document]
- **Known default sort**: [Field and order]

**Dashboard** (if applicable):
- **Known KPIs**: [List from document]
- **Known charts**: [List from document]

---

[Repeat for each entity]

---

## 6. Cross-Cutting Concerns

### 6.1 Security and Permissions

**Roles identified**:
- [Role 1]: [Description]
- [Role 2]: [Description]

**Permission requirements** (if specified):
- [Entity]: [CRUD permissions by role]

### 6.2 Internationalization

**Languages required**: [List, e.g., French, English]
**Default language**: [Language]

### 6.3 Integration

**Import requirements**:
- [Entity to import] from [Format] [Frequency]

**Export requirements**:
- [Entity to export] to [Format] [Purpose]

**External system integration**:
- [System name]: [Integration type and purpose]

### 6.4 Reporting

**Reports identified**:
- [Report 1]: [Description and format]
- [Report 2]: [Description and format]

---

## 7. Clear and Well-Defined Elements

[List what is already clear and well-defined in the document - no clarification needed]

### Entities with Complete Definitions
- **[Entity1]**: All fields defined with types, relationships clear
- [Add others if applicable]

### Features with Complete Specifications
- **[Feature X]**: Complete workflow, validations, and business rules documented
- [Add others if applicable]

### Well-Documented Aspects
- [Aspect 1]: [Why it's clear]
- [Aspect 2]: [Why it's clear]

---

## 8. Ambiguities and Missing Information

[List what needs clarification, organized by category]

### 8.1 Entity Ambiguities

#### Entity: [EntityName]

**Ambiguity 1**: [Description of what is unclear]
- **Found in**: [Document page/section]
- **Impact**: [Why this matters for implementation]

**Missing information**:
- [List of missing field definitions, relationships, etc.]

---

### 8.2 Feature Ambiguities

#### Feature: [FeatureName]

**Ambiguity 1**: [Description of what is unclear]
- **Found in**: [Document page/section]
- **Impact**: [Why this matters for implementation]

**Missing information**:
- Pre-conditions not specified
- Error handling strategy not defined
- [Other missing details]

---

### 8.3 UI Ambiguities

[List unclear or missing UI requirements]

---

### 8.4 Cross-Cutting Ambiguities

[List unclear security, i18n, integration requirements]

---

### 8.5 Contradictions Found

[If any contradictions were found between document sections]

**Contradiction 1**: [Topic]
- **Section X (page Y)** states: "[Quote]"
- **Section A (page B)** states: "[Quote]"
- **Resolution needed**: [What needs to be clarified]

---

## 9. Clarifying Questions

[Structured questions organized by topic, using templates from @docs/analysis/question-templates.md]

### 9.1 Questions on Business Entities

#### Entity: [EntityName]

##### Fields and Types

**Q1.1**: [Specific question]?
- **Context**: [Why this info is needed]
- **Suggested options**: [If applicable]
- **Priority**: ⚡ CRITICAL / 🔴 HIGH / 🟠 MEDIUM / 🟢 LOW
- **Reference**: [Document page/section]

**Q1.2**: [Specific question]?
- [Same structure]

##### Relationships

**Q1.3**: [Specific question about relationships]?
- [Same structure]

---

#### Entity: [EntityName2]

[Same structure]

---

### 9.2 Questions on Features

#### Feature: [FeatureName]

**Q2.1**: [Specific question]?
- **Context**: [Why this info is needed]
- **Suggested options**: [If applicable]
- **Priority**: ⚡ CRITICAL / 🔴 HIGH / 🟠 MEDIUM / 🟢 LOW
- **Reference**: [Document page/section]

---

### 9.3 Questions on User Interface

**Q3.1**: [UI-related question]?
- [Same structure]

---

### 9.4 Questions on Cross-Cutting Concerns

**Q4.1**: [Security/i18n/integration question]?
- [Same structure]

---

### 9.5 Question Summary

**Total questions**: [Number]
- ⚡ **CRITICAL** (blocks architecture): [Number]
- 🔴 **HIGH** (important for completeness): [Number]
- 🟠 **MEDIUM** (improves quality): [Number]
- 🟢 **LOW** (nice-to-have): [Number]

---

## 10. Initial Recommendations

[If applicable, suggest Axelor patterns that could be applied based on recognized patterns]

### 10.1 Applicable Axelor Patterns

**Entity Patterns**:
- [Entity X] could use **status workflow pattern** (DRAFT → VALIDATED → COMPLETED)
- [Entity Y] could use **hierarchical entity pattern** (parent-child tree)

**Relationship Patterns**:
- [Entity A - Entity B] appears to be **composition** (cascade delete recommended)
- [Entity C - Entity D] appears to be **many-to-many** (tags/categories pattern)

**View Patterns**:
- [Entity X] form could use **standard panel layout**: General Info, Details, Relationships
- [Entity Y] grid could use **status filter** for quick access

**Service Patterns**:
- [Feature X] appears to be **workflow service pattern** (state transitions)
- [Feature Y] appears to be **calculation service pattern** (amount computation)

### 10.2 Suggested Architecture Approach

[High-level architectural suggestions if patterns are clear]

---

## 11. Identified Risks and Constraints

### 11.1 Technical Risks

- **Risk 1**: [Description and mitigation suggestion]
- **Risk 2**: [Description and mitigation suggestion]

### 11.2 Business Constraints

- **Constraint 1**: [Description and impact]
- **Constraint 2**: [Description and impact]

### 11.3 Dependencies

- **Dependency 1**: [What this project depends on]
- **Dependency 2**: [External systems, data, etc.]

---

## 12. Estimated Complexity

### 12.1 Overall Assessment

**Complexity**: ⚫ Simple / 🟠 Medium / 🔴 Complex / ⚫⚫ Very Complex

**Justification**: [Why this complexity rating - number of entities, features, integration points]

### 12.2 Component Complexity

| Component | Count | Complexity | Estimated Effort |
|-----------|-------|------------|------------------|
| Business Entities | [X] | [Simple/Medium/Complex] | [Y person-days] |
| Features | [X] | [Simple/Medium/Complex] | [Y person-days] |
| Views | [X] | [Simple/Medium/Complex] | [Y person-days] |
| Integrations | [X] | [Simple/Medium/Complex] | [Y person-days] |
| **Total** | | | **[Z person-days]** |

*Note: This is a preliminary estimation based on initial analysis. Detailed estimation will be done after specification refinement.*

---

## 13. Next Steps

### 13.1 Immediate Actions

1. **Review this analysis** with stakeholders
2. **Collect answers** to clarifying questions (Section 9)
3. **Resolve contradictions** (if any found in Section 8.5)
4. **Prioritize questions** if not all can be answered immediately

### 13.2 After Questions Answered

Once clarifying questions are answered:

1. **Update this analysis** with new information
2. **Proceed to refinement phase** with `requirements-refiner` agent
3. **Generate detailed specifications** for development
4. **Create EPIC/User Story breakdown** with `agile-agent` agent

### 13.3 Timeline Suggestion

- **Analysis review + Q&A**: [X days]
- **Specification refinement**: [Y days]
- **Architecture design**: [Z days]
- **Start development**: [Target date]

---

## 14. Appendices

### 14.1 Document Reading Log

[If document was very large, log what was read and when]

| Session | Date | Pages/Sections Read | Key Findings |
|---------|------|---------------------|--------------|
| 1 | [Date] | [Pages] | [Summary] |
| 2 | [Date] | [Pages] | [Summary] |
| ... | ... | ... | ... |

### 14.2 Glossary

[Business terms and their definitions]

| Term | Definition | Used in Context |
|------|------------|-----------------|
| [Term1] | [Definition] | [Entity/Feature] |
| [Term2] | [Definition] | [Entity/Feature] |

### 14.3 References

- **Source document**: [Full path or link]
- **Related documents**: [List any additional documents consulted]
- **Axelor documentation**: [Links to relevant Axelor docs if consulted]

---

## Validation

**To be validated by**: [Stakeholder name/role]
**Validation deadline**: [Date]
**Validation status**: ⏳ Pending / ✅ Approved / ⚠️ Approved with comments / ❌ Rejected

**Comments**:
[Space for stakeholder feedback]

---

*This analysis was generated by the business-analyst agent following the methodology described in @docs/analysis/large-document-strategy.md*
