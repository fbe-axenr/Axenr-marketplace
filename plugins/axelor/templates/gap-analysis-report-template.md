# Gap Analysis Report - [Project/Module Name]

**Project type**: [Client Module / R&D AOS Module]
**Analysis date**: [Date]
**Analyst**: [Agent/Person name]
**Based on**: Analysis report v[X] (docs/analysis-report.md)
**Status**: Draft / For Review / Validated

---

## Executive Summary

### Reuse Opportunities Identified

**Entities**:
- Total analyzed: [X]
- **REUSE** (use as-is): [Y] ([Z]%)
- **EXTEND** (add custom fields): [A] ([B]%)
- **DEVELOP_NEW** (custom entity): [C] ([D]%)

**Features**:
- Total analyzed: [X]
- **REUSE** (configure): [Y] ([Z]%)
- **ADAPT** (customize): [A] ([B]%)
- **DEVELOP_NEW** (implement): [C] ([D]%)

### Effort Impact

| Metric | Without AOS Reuse | With AOS Reuse | Savings |
|--------|-------------------|----------------|---------|
| Total Entities | [X] days | [Y] days | [Z] days ([%]) |
| Total Features | [X] days | [Y] days | [Z] days ([%]) |
| **TOTAL PROJECT** | **[X] person-days** | **[Y] person-days** | **[Z] person-days ([%])** |

### Key Findings

- 🟢 **High reuse potential**: [List entities/features that match AOS well]
- 🟡 **Extension opportunities**: [List entities needing minor customization]
- 🔴 **Custom development required**: [List unique requirements not in AOS]

---

## 1. Entity Gap Analysis

### 1.1 Entity: [EntityName1]

**Business Role**: [What this entity represents - 1 sentence]

**Client Requirements** (from analysis report):
- Fields: [List required fields]
- Relationships: [List required relationships]
- Business rules: [Key validations/constraints]

**AOS Equivalent Found**: ✅ YES / ❌ NO

**AOS Entity**: `[EntityName]` from module `[axelor-module-name]`
**AOS File Reference**: `/path/to/axelor-open-suite/axelor-[module]/src/main/resources/domains/[Entity].xml`

**Field-by-Field Comparison**:

| Client Field | Type | Required | AOS Match | AOS Field | Match? |
|--------------|------|----------|-----------|-----------|--------|
| code | String | Yes | ✅ | code | 100% |
| name | String | Yes | ✅ | name / fullName | 100% |
| email | String | No | ✅ | emailAddress | 90% (different name) |
| industry | Selection | Yes | ❌ | - | 0% (missing) |
| companySize | Integer | No | ❌ | - | 0% (missing) |

**Match Percentage**: [X]% ([Y] out of [Z] fields match)

**Categorization Decision**: **[REUSE / EXTEND / DEVELOP_NEW]**

**Rationale**:
[Explain why this categorization based on match percentage, business logic compatibility, and technical constraints]

**Implementation Recommendation**:

[REUSE case example]
```markdown
**Recommended Strategy**: Use AOS entity directly with configuration

1. Add module dependency:
   dependencies {
     implementation 'com.axelor:axelor-[module]:8.0.0'
   }

2. Use com.axelor.apps.[module].db.[Entity] in code

3. Configure via application properties or UI customization

4. No custom code required
```

[EXTEND case example]
```markdown
**Recommended Strategy**: Extend AOS entity in custom module

1. Add module dependency (same as above)

2. Create extended domain:
   <entity name="Custom[Entity]" extends="com.axelor.apps.[module].db.[Entity]">
     <string name="industry" selection="industry.selection"/>
     <integer name="companySize"/>
   </entity>

3. Inherit all AOS views and services automatically

4. Create additional views for new fields:
   - Add panel in form for custom fields
   - Add columns in grid if needed

5. Override service methods only if custom business logic needed

6. Estimated effort: 1-2 days (vs 3-5 days new entity)
```

[DEVELOP_NEW case example]
```markdown
**Recommended Strategy**: Develop custom entity from scratch

Rationale:
- No suitable AOS entity found
- Business concept is unique to client
- Match percentage too low (<50%) to justify extension

Implementation:
1. Create domain XML following Axelor conventions
2. Create views (form, grid, menu)
3. Implement services for business logic
4. Estimated effort: 3-5 days
```

**AOS Documentation Reference**: [Link to https://docs.axelor.com/aos/modules/[module]/]

**Related AOS Entities**: [List other AOS entities that might be relevant]

---

### 1.2 Entity: [EntityName2]

[Same structure as above]

---

[Repeat for all entities]

---

## 2. Feature Gap Analysis

### 2.1 Feature: [FeatureName1]

**Business Description**: [What this feature does - 1-2 sentences]

**Client Requirements** (from analysis report):
- Trigger: [Who, where, when]
- Process: [Step-by-step workflow]
- Validations: [Business rules]
- Expected outcome: [Results]

**AOS Equivalent Found**: ✅ YES / ❌ NO

**AOS Feature**: [Feature name in AOS module]
**AOS Module**: axelor-[module-name]
**AOS Service Reference**: `/path/to/axelor-open-suite/axelor-[module]/src/main/java/.../[Service].java`

**Capability Comparison**:

| Client Requirement | AOS Capability | Match? | Notes |
|--------------------|----------------|--------|-------|
| Status workflow DRAFT→CONFIRMED | Standard workflow | ✅ | Exactly matches |
| Email notification on status change | Message service | ✅ | Template customizable |
| PDF generation | Report engine | ✅ | Template needs creation |
| Custom discount calculation | Basic discount | 🟡 | Needs custom logic |
| Multi-currency support | Native currency | ✅ | Fully supported |

**Match Percentage**: [X]% ([Y] out of [Z] capabilities match)

**Categorization Decision**: **[REUSE / ADAPT / DEVELOP_NEW]**

**Rationale**:
[Explain decision based on capability match and customization needed]

**Implementation Recommendation**:

[REUSE case example]
```markdown
**Recommended Strategy**: Configure AOS feature

1. Use existing [Service] from axelor-[module]

2. Configure parameters:
   - Workflow statuses: Define in meta-module or code
   - Email templates: Customize for branding
   - PDF template: Create custom BIRT template

3. No Java code customization required

4. Estimated effort: 0.5-1 day (configuration only)
```

[ADAPT case example]
```markdown
**Recommended Strategy**: Override AOS service method

1. Extend [Service] class in custom module

2. Override specific method:
   @Override
   public [ReturnType] [methodName]([params]) {
     // Add custom logic here
     // Call super for standard behavior if needed
     return super.[methodName]([params]);
   }

3. Register custom service in module configuration

4. Estimated effort: 2-3 days (customization + testing)
```

[DEVELOP_NEW case example]
```markdown
**Recommended Strategy**: Implement custom service

Rationale:
- No equivalent AOS feature
- Business logic is unique
- Cannot adapt existing AOS service

Implementation:
1. Create [Service] interface and implementation
2. Implement business logic from scratch
3. Create unit tests (>80% coverage)
4. Integrate with domain/views
5. Estimated effort: 4-6 days
```

**AOS Documentation Reference**: [Link to feature documentation]

---

### 2.2 Feature: [FeatureName2]

[Same structure as above]

---

[Repeat for all features]

---

## 3. Relationship Gap Analysis

### Standard AOS Relationships Found

| Client Relationship | AOS Equivalent | Module | Reusable? |
|---------------------|----------------|--------|-----------|
| Customer → Orders | Partner → SaleOrder | axelor-sale | ✅ Yes |
| Employee → Department | Employee → Department | axelor-hr | ✅ Yes |
| Product → Category | Product → ProductCategory | axelor-base | ✅ Yes |
| [Custom] → [Custom] | - | - | ❌ No, implement |

### Missing Relationships

- **[Entity A] → [Entity B]**: [Description, must be implemented]
- **[Entity C] → [Entity D]**: [Description, must be implemented]

---

## 4. Module Dependencies & Integration

### 4.1 For Client/Standalone Module

**Recommended AOS Module Dependencies**:

Add to `build.gradle`:
```gradle
dependencies {
  implementation 'com.axelor:axelor-base:8.0.0' // Always required (Partner, Company, User)
  implementation 'com.axelor:axelor-crm:8.0.0' // For Lead, Opportunity
  implementation 'com.axelor:axelor-sale:8.0.0' // For Order, Quote, Invoice
  // Add others as needed
}
```

**Version Compatibility**: Axelor Open Suite 8.0.x

**Configuration Files**:
- `axelor-config.properties`: [Specific configurations needed]
- `application.properties`: [Module-specific settings]

**Extension Strategy Summary**:
```
Custom Module: [module-name]
├── Extends: [List of extended AOS entities]
├── New Entities: [List of custom entities]
├── Overridden Services: [List of customized services]
└── Dependencies: [List of AOS modules]
```

---

### 4.2 For R&D AOS Module

**AOS Integration Strategy**:

**Module Type**: ☐ Standalone AOS module / ☐ Contribution to existing module

**Dependencies on Existing AOS Modules**:
- `axelor-base`: [Why - e.g., uses Partner, Company, User]
- `axelor-[module]`: [Why - e.g., extends [Feature]]

**Integration Points**:
- **Entities**: [List shared/extended entities]
- **Services**: [List service dependencies or hooks]
- **Views**: [List view integration points]
- **Actions**: [List action integrations]

**AOS Contribution Decision**:

**Recommended**: [Standalone module / Contribution to axelor-[existing]]

**Rationale**:
- [Factor 1: e.g., Domain-specific vs generic feature]
- [Factor 2: e.g., Optional vs core functionality]
- [Factor 3: e.g., Maintenance and release cycle]

**AOS Pattern Compliance**:
- ✅ Follows AOS naming conventions (axelor-[name])
- ✅ Uses standard AOS view patterns
- ✅ Integrates with AOS security (MetaPermission)
- ✅ Supports AOS i18n framework
- ✅ Compatible with AOS multi-company
- ✅ Uses AOS standard workflows

**Contribution Checklist** (if contributing to AOS):
- [ ] Code follows AOS conventions
- [ ] Unit tests included (>80% coverage)
- [ ] Documentation provided
- [ ] i18n translations included
- [ ] Compatible with PostgreSQL and MySQL
- [ ] No breaking changes to existing APIs

---

## 5. Implementation Recommendations

### 5.1 Priority Order

**Phase 1: Reuse (Quick Wins)** - [X] days
1. [Entity/Feature to reuse] - Configure AOS module
2. [Entity/Feature to reuse] - Add dependency, configure

**Phase 2: Extend (Moderate Effort)** - [Y] days
1. [Entity to extend] - Create extension domain
2. [Feature to adapt] - Override service method

**Phase 3: Develop New (High Effort)** - [Z] days
1. [Custom entity] - Full development
2. [Custom feature] - Full implementation

**Total Estimated Effort**: [X+Y+Z] person-days

---

### 5.2 Risk Assessment

**Low Risk** (AOS Reuse):
- ✅ Battle-tested AOS components
- ✅ Regular AOS updates and bug fixes
- ✅ Community support

**Medium Risk** (AOS Extension):
- ⚠️ Dependency on AOS API stability
- ⚠️ Need to test with AOS upgrades
- ⚠️ Extension complexity manageable

**High Risk** (Custom Development):
- 🔴 Full responsibility for maintenance
- 🔴 No AOS update benefits
- 🔴 Higher testing burden

---

### 5.3 Maintenance Considerations

**With AOS Reuse**:
- Regular AOS updates may include bug fixes for reused components
- Need to test compatibility with AOS version upgrades
- Benefit from AOS security patches

**With Extensions**:
- Monitor AOS API changes across versions
- Maintain compatibility layer if needed
- Regression testing after AOS upgrades

**With Custom Code**:
- Full maintenance responsibility
- Independent of AOS release cycle (pro and con)
- Ensure long-term support plan

---

## 6. Effort Comparison Summary

### Detailed Effort Breakdown

| Component | Type | Without Reuse | With Reuse | Savings |
|-----------|------|---------------|------------|---------|
| [Entity 1] | REUSE | 3 days | 0.5 days | 2.5 days (83%) |
| [Entity 2] | EXTEND | 4 days | 1.5 days | 2.5 days (63%) |
| [Entity 3] | NEW | 5 days | 5 days | 0 days (0%) |
| [Feature 1] | REUSE | 4 days | 0.5 days | 3.5 days (88%) |
| [Feature 2] | ADAPT | 5 days | 2 days | 3 days (60%) |
| [Feature 3] | NEW | 6 days | 6 days | 0 days (0%) |
| **TOTAL** | - | **27 days** | **15.5 days** | **11.5 days (43%)** |

### Cost-Benefit Analysis

**Initial Development**:
- Effort saved: [X] person-days
- Cost saved: [Y] € (assuming [Z] €/day)

**Long-term Maintenance** (over 3 years):
- Reused components: Maintained by AOS team (zero cost)
- Extended components: Minimal maintenance (estimated [A] person-days/year)
- Custom components: Full maintenance (estimated [B] person-days/year)

**Total 3-year TCO reduction**: [C]% with AOS reuse strategy

---

## 7. Documentation References

### AOS Modules Documentation

- **axelor-base**: https://docs.axelor.com/aos/modules/base/
- **axelor-crm**: https://docs.axelor.com/aos/modules/crm/
- **axelor-sale**: https://docs.axelor.com/aos/modules/sale/
- **axelor-hr**: https://docs.axelor.com/aos/modules/hr/
- [Add others as relevant]

### AOS Source Code References

- **AOS Repository**: [Path in devcontainer]
- **Key Entities**: [List important entity files examined]
- **Key Services**: [List important service files examined]

### Internal Documentation

- Business Analysis Report: @docs/analysis-report.md
- Axelor Patterns Catalog: @docs/analysis/axelor-patterns-for-analysis.md
- AOS Modules Reference: @docs/aos-modules-reference.md

---

## 8. Next Steps

### Immediate Actions

1. **Review gap analysis** with stakeholders
   - Confirm reuse decisions
   - Validate extension strategies
   - Approve custom development scope

2. **Update module dependencies**
   - Add AOS modules to build.gradle
   - Verify version compatibility
   - Test dependency resolution

3. **Proceed to requirements refinement**
   - Inform refiner agent with gap analysis
   - Refine only custom/extended components in detail
   - Reference AOS documentation for reused components

### Before Architecture Design

- [ ] All reuse decisions validated by stakeholder
- [ ] Module dependencies finalized
- [ ] Extension strategies agreed upon
- [ ] Custom development scope locked

### Questions for Stakeholder

1. **Reuse Strategy**: Do you approve using AOS modules [list] as dependencies?
2. **Extension Approach**: Are you comfortable extending AOS entities vs creating custom?
3. **Version Lock**: Can we commit to AOS 8.0.x for this project?
4. **Maintenance Plan**: Who will handle AOS upgrade testing?

---

## Validation

**To be validated by**: [Stakeholder name/role]
**Validation deadline**: [Date]
**Validation status**: ⏳ Pending / ✅ Approved / ⚠️ Approved with changes / ❌ Rejected

**Stakeholder Comments**:
[Space for feedback]

---

**Analysis completed by aos-analyzer agent**
**This gap analysis will save an estimated [X]% development effort by leveraging existing AOS capabilities.**
