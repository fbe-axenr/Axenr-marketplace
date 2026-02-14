# Gap Analysis Decision Options Template

This template provides the standard 4 options to present to users when analyzing entity matches between requirements and Axelor Open Suite (AOS).

Use this template when presenting options in section 2.5 of the gap analysis workflow.

---

## How to Use This Template

1. Replace placeholders in square brackets with entity-specific data
2. Enrich Option 1 and 2 with AOS features from `aos-documentation-fetcher` skill
3. Adjust effort estimates based on entity complexity
4. Present all 4 options objectively, let user decide

---

## Decision Options for [EntityName]

Based on **[X]% match** analysis from `aos-field-comparator` skill, here are your options:

### Option 1: REUSE (Use AOS [AOSEntityName] as-is)

**Approach**: Use existing AOS entity without modifications, configure as needed.

✓ **Advantages**:
- **Zero development time** for entity (0.5 days configuration only)
- **Inherits all AOS features**: [List key features from aos-documentation-fetcher]
  - Example: address management, contact lists, multi-company support, etc.
- **Future AOS updates** benefit you automatically (bug fixes, new features)
- **Full integration** with other AOS modules: [List related modules]
  - Example: CRM, Sale, Purchase modules can use this entity directly
- **Battle-tested code**: Used in production by many Axelor clients
- **Documentation available**: Official AOS docs and community support

✗ **Disadvantages**:
- **Missing fields**: [List missing fields from comparison]
  - Would need to store these elsewhere (custom JSON, separate entity) or skip them
- **Field constraints may differ**: [List any constraint mismatches]
  - Example: AOS field is optional but requirement needs it required
- **Selection values may differ**: [If applicable]
  - Example: Status values don't match requirement
- **Less flexibility**: Cannot change core entity structure
- **Dependency on AOS**: Locked into AOS data model and conventions

**Estimated effort**: **0.5 days** (configuration only)

**Best for**: High match (≥85%), standard business concept, want rapid deployment

---

### Option 2: EXTEND (Extend AOS [AOSEntityName] with custom fields)

**Approach**: Create custom entity extending AOS entity, add missing fields in extension.

✓ **Advantages**:
- **Get all AOS features PLUS custom fields**: Best of both worlds
- **Standard Axelor extension pattern**: Well-documented, maintainable approach
- **Maintains AOS ecosystem compatibility**: Can still use AOS services, views, integrations
- **Moderate development effort**: Only implement what's missing
- **Inherit future AOS improvements**: Core entity benefits from updates
- **Clear separation**: Custom fields clearly identified in extension

✗ **Disadvantages**:
- **Dependency on AOS entity structure**: Changes to base entity may require adjustments
- **Potential upgrade conflicts**: AOS version upgrades may need migration work
- **Need to understand AOS internals**: Must know how base entity works
- **Extension complexity**: Managing inheritance, overriding methods if needed
- **Testing overhead**: Must test both inherited and custom behavior

**Estimated effort**: **1-2 days** (extension module + custom fields + testing)

**Code example**:
```xml
<entity name="Custom[EntityName]" extends="com.axelor.apps.[module].db.[AOSEntityName]">
  <string name="[missingField1]" selection="[selection-name]" title="[Field Title]"/>
  <integer name="[missingField2]" title="[Field Title]"/>
  <!-- Add all missing fields from comparison -->
</entity>
```

**Best for**: Medium match (50-84%), need specific custom fields, want AOS integration

---

### Option 3: DEVELOP_NEW (Create custom [EntityName] entity from scratch)

**Approach**: Create entirely new custom entity with exact requirements, no AOS dependency.

✓ **Advantages**:
- **Full control** over entity structure, naming, and behavior
- **No dependency on AOS**: Independent evolution, no upgrade concerns
- **Optimized for exact requirements**: Only what you need, nothing extra
- **Clear ownership**: Your team owns entire codebase
- **No compatibility concerns**: Can diverge completely from AOS patterns if needed
- **Simpler mental model**: No inheritance complexity

✗ **Disadvantages**:
- **High development effort**: 3-5 days for complete implementation
  - Domain definition
  - Views (form, grid, search)
  - Services (CRUD, business logic)
  - Repository methods
  - Complete testing
- **Implement all features from scratch**: No inherited functionality
  - Address management, contacts, sequences, etc. must be built
- **Miss out on AOS integrations**: Other AOS modules won't recognize entity
  - CRM, Sale, Purchase modules won't integrate automatically
- **Higher maintenance burden**: Your team maintains everything
- **Reinventing the wheel**: May duplicate functionality AOS already provides
- **No community support**: Custom entity, no shared knowledge base

**Estimated effort**: **3-5 days** (domain + views + services + testing)

**Best for**: Low match (<50%), highly specific business concept, no AOS integration needed

---

### Option 4: HYBRID (Use AOS [AOSEntityName] + separate custom entity)

**Approach**: Keep AOS entity pristine, create separate custom entity for specific needs, link via relationship.

✓ **Advantages**:
- **Keeps AOS entity pristine**: No modification, no upgrade conflicts
- **Separation of concerns**: AOS handles standard stuff, custom entity handles specific needs
- **Flexibility**: Can evolve custom entity independently
- **Clear boundaries**: Easy to understand what's AOS vs custom
- **Best for phased approach**: Use AOS immediately, add custom later
- **Reversible**: Can remove custom entity without affecting AOS entity

✗ **Disadvantages**:
- **Complexity: managing two entities**: More complex data model
  - Need to understand both entities
  - Relationships between entities to manage
- **More complex queries**: Must join entities to get complete data
  - Performance considerations
  - More complex HQL/SQL queries
- **More complex views**: Need to display data from two entities
  - Form design challenges
  - Grid columns from multiple sources
- **May confuse end users**: "Why are there two Customer entities?"
- **Relationship maintenance**: Keep many-to-one/one-to-many in sync

**Estimated effort**: **2-3 days** (custom entity + relationship setup + integration)

**Example structure**:
```xml
<!-- Use AOS Partner as-is -->
<!-- Create separate custom entity -->
<entity name="[EntityName]Extension">
  <many-to-one name="partner" ref="com.axelor.apps.base.db.Partner" required="true"/>
  <string name="[missingField1]"/>
  <integer name="[missingField2]"/>
</entity>
```

**Best for**: Want AOS entity benefits but have very specific additional needs, phased approach

---

## Decision Factors Summary

| Factor | REUSE | EXTEND | DEVELOP_NEW | HYBRID |
|--------|-------|--------|-------------|--------|
| **Match %** | ≥85% | 50-84% | <50% | Any |
| **Effort** | 0.5d | 1-2d | 3-5d | 2-3d |
| **AOS Integration** | Full | Full | None | Partial |
| **Flexibility** | Low | Medium | High | High |
| **Maintenance** | Low | Medium | High | Medium-High |
| **Upgrade Risk** | Low | Medium | None | Low |
| **Complexity** | Low | Medium | Medium | High |

---

## Next Steps After Decision

Once user selects an option:

1. **Record decision** with rationale in gap analysis report
2. **Document implementation approach** specific to chosen option
3. **Update effort estimates** in project timeline
4. **Identify dependencies** (modules, libraries, configurations needed)
5. **Plan validation** (how to test the implementation)

---

## Common Decision Patterns

**User prioritizes speed**: Usually choose REUSE or EXTEND
**User prioritizes control**: Usually choose DEVELOP_NEW
**User prioritizes AOS ecosystem**: Usually choose REUSE or EXTEND
**User has licensing concerns**: May choose DEVELOP_NEW to avoid AGPL
**User has complex custom needs**: May choose HYBRID or DEVELOP_NEW
**User has AOS expertise**: More comfortable with EXTEND
**User lacks AOS expertise**: May prefer REUSE or DEVELOP_NEW (simpler)
