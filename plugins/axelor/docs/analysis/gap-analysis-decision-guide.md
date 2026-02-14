# Gap Analysis Decision Guide

Quick reference guide for making REUSE/EXTEND/DEVELOP_NEW/HYBRID recommendations based on match percentage, entity type, and strategic factors.

---

## Decision Matrix

### Primary: Match Percentage Thresholds

| Match % | Primary Recommendation | Rationale |
|---------|------------------------|-----------|
| **95-100%** | REUSE | Perfect or near-perfect match, no reason to customize |
| **85-94%** | REUSE or EXTEND | Very high match, evaluate missing fields criticality |
| **70-84%** | EXTEND | Good foundation, moderate customization needed |
| **50-69%** | EXTEND or DEVELOP_NEW | Borderline, depends on strategic factors |
| **30-49%** | DEVELOP_NEW or HYBRID | Low match, significant custom development needed |
| **<30%** | DEVELOP_NEW | Very different concept, not worth forcing AOS fit |

**Note**: These are guidelines, not strict rules. Strategic factors (below) can override match percentage.

---

## Secondary: Strategic Factors

These factors can shift recommendation up or down by one category:

### Factor: AOS Ecosystem Integration

**Impact**: High integration need → Prefer REUSE/EXTEND (even with lower match)

| Integration Level | Recommendation Shift |
|-------------------|---------------------|
| **High** (3+ modules integrate with entity) | +1 category toward REUSE/EXTEND |
| **Medium** (1-2 modules) | No shift |
| **Low** (standalone) | -1 category toward DEVELOP_NEW |

**Examples**:
- Customer → integrates with Sale, CRM, Project, Purchase → High integration
- Product → integrates with Sale, Purchase, Stock, Production → High integration
- Custom concept (e.g., "ResearchProject") → Low integration

---

### Factor: Timeline/Speed to Market

**Impact**: Urgent timeline → Prefer faster options

| Timeline | Recommendation Shift |
|----------|---------------------|
| **Critical** (<1 week) | Strongly prefer REUSE |
| **Urgent** (1-2 weeks) | Prefer REUSE or EXTEND |
| **Normal** (2-4 weeks) | No shift |
| **Flexible** (>1 month) | DEVELOP_NEW acceptable |

---

### Factor: Team AOS Expertise

**Impact**: Low expertise → Avoid EXTEND complexity

| Expertise Level | Recommendation Shift |
|-----------------|---------------------|
| **Expert** (AOS core contributor) | EXTEND always manageable |
| **Experienced** (Extended AOS before) | No shift |
| **Intermediate** (Used AOS, no extensions) | -0.5 category away from EXTEND |
| **Novice** (New to AOS) | Avoid EXTEND, prefer REUSE or DEVELOP_NEW |

---

### Factor: Customization Trajectory

**Impact**: Heavy future customization → Prefer DEVELOP_NEW

| Expected Customization | Recommendation Shift |
|------------------------|---------------------|
| **Heavy** (>10 custom fields, complex logic) | -1 category toward DEVELOP_NEW |
| **Moderate** (5-10 fields, standard logic) | No shift |
| **Light** (1-4 fields, simple logic) | +0.5 category toward REUSE/EXTEND |

---

### Factor: Licensing Sensitivity

**Impact**: AGPL concerns → Prefer DEVELOP_NEW

| Licensing Stance | Recommendation Shift |
|------------------|---------------------|
| **AGPL problematic, no commercial license** | Strongly prefer DEVELOP_NEW |
| **Prefer to avoid AGPL** | -1 category toward DEVELOP_NEW |
| **AGPL acceptable or have commercial license** | No shift |

---

## Entity Type Patterns

Certain entity types have predictable patterns:

### High-Value AOS Entities (Usually REUSE/EXTEND)

These AOS entities are mature, feature-rich, and worth reusing even at 60-70% match:

1. **Partner** (axelor-base)
   - Customer, Supplier, Client concepts
   - Extremely well-integrated with entire AOS suite
   - **Recommendation bias**: +1 category toward REUSE/EXTEND

2. **Product** (axelor-base)
   - Product, Item, SKU concepts
   - Integrates with Sale, Purchase, Stock, Production
   - **Recommendation bias**: +1 category toward REUSE/EXTEND

3. **Order** (axelor-sale), **Invoice** (axelor-account)
   - Standard business transactions
   - Complex workflows already implemented
   - **Recommendation bias**: +1 category toward REUSE/EXTEND

4. **Employee** (axelor-hr)
   - HR, resource management concepts
   - Payroll, leave, expense integrations
   - **Recommendation bias**: +1 category toward REUSE/EXTEND

### Domain-Specific Entities (Often DEVELOP_NEW)

These concepts are typically custom to the business:

1. **Industry-specific entities**
   - ResearchProject, ClinicalTrial, LegalCase, InsurancePolicy
   - **Recommendation bias**: -1 category toward DEVELOP_NEW

2. **Workflow-specific entities**
   - ApprovalWorkflow, CustomNotification, ReportConfiguration
   - **Recommendation bias**: -1 category toward DEVELOP_NEW

3. **Integration entities**
   - ExternalSystemSync, APIMapping, DataTransformation
   - **Recommendation bias**: -1 category toward DEVELOP_NEW

---

## Example Scenarios

### Scenario 1: Customer Entity

**Input**:
- Match: 65% with AOS Partner
- Missing fields: industry (Selection), companySize (Integer)
- Integration: Will use Sale, CRM modules (High)
- Timeline: 2 weeks (Normal)
- Team: Intermediate AOS experience
- Customization: Moderate (6 custom fields total)

**Analysis**:
- Base recommendation: EXTEND (match 65%)
- Integration factor: +1 toward REUSE/EXTEND → Still EXTEND
- Timeline: No shift
- Team: -0.5, but not enough to change
- **Final Recommendation**: EXTEND

**Rationale**: 65% match + high AOS integration need = clear EXTEND case

---

### Scenario 2: ResearchProject Entity

**Input**:
- Match: 75% with AOS Project
- Missing fields: researchPhase (Selection), ethicsApprovalDate (Date), fundingSource (many-to-one)
- Integration: Standalone module, no AOS integration (Low)
- Timeline: Flexible (3 months)
- Team: Novice with AOS
- Customization: Heavy (15+ custom fields expected, complex workflow)

**Analysis**:
- Base recommendation: EXTEND (match 75%)
- Integration factor: -1 toward DEVELOP_NEW → EXTEND/DEVELOP_NEW borderline
- Timeline: Flexible, no urgency → DEVELOP_NEW acceptable
- Team: Novice → Avoid EXTEND complexity
- Customization: Heavy → -1 toward DEVELOP_NEW
- **Final Recommendation**: DEVELOP_NEW

**Rationale**: Despite 75% match, strategic factors (low integration, novice team, heavy customization) override match percentage

---

### Scenario 3: Invoice Entity

**Input**:
- Match: 55% with AOS Invoice
- Missing fields: customTaxCalculation, multiplePaymentTerms, invoiceAttachments
- Integration: Will use Account, Sale modules (High)
- Timeline: Urgent (1 week)
- Team: Expert AOS developers
- Customization: Moderate (8 custom fields)

**Analysis**:
- Base recommendation: EXTEND (match 55%, borderline)
- Integration factor: +1 toward REUSE/EXTEND → EXTEND (stronger)
- Timeline: Urgent → Prefer faster options, but EXTEND still viable
- Team: Expert → EXTEND very manageable
- **Final Recommendation**: EXTEND (with urgency note)

**Rationale**: AOS Invoice is battle-tested, high-value entity. Expert team can extend quickly to meet timeline.

---

## Red Flags: When to Override Match Percentage

### Red Flag 1: Business Logic Conflicts

**Situation**: AOS entity has 80% field match BUT fundamentally different business logic

**Example**:
- Client needs: Customer status (ACTIVE, SUSPENDED, TERMINATED, REACTIVATED)
- AOS Partner: Category (CUSTOMER, SUPPLIER, COMPETITOR, PARTNER)
- **Conflict**: Status is lifecycle, Category is type classification

**Override**: Recommend DEVELOP_NEW despite 80% match

---

### Red Flag 2: Incompatible Relationships

**Situation**: Entity has good field match BUT relationships are incompatible

**Example**:
- Client needs: Order → multiple Customers (many-to-many)
- AOS Order: Order → single Partner (many-to-one)
- **Conflict**: Fundamental relationship structure differs

**Override**: Recommend DEVELOP_NEW or HYBRID, not EXTEND

---

### Red Flag 3: Selection Values Mismatch

**Situation**: Match looks good BUT critical selection field has incompatible values

**Example**:
- Client needs: Priority (LOW, MEDIUM, HIGH, CRITICAL, EMERGENCY)
- AOS uses: Integer priority field (1-10)
- **Conflict**: Different priority systems, hard to map

**Evaluation**: If only this field differs, EXTEND is still viable (add custom selection). If many selection fields differ, DEVELOP_NEW.

---

## HYBRID Decision Logic

HYBRID is typically chosen in these specific scenarios:

### When to Suggest HYBRID

1. **AOS entity is valuable BUT highly customized needs exist**
   - Match: 60-80%
   - Want AOS benefits (e.g., Partner address management)
   - But have 10+ very specific custom fields
   - Solution: Use AOS Partner + CustomerExtension entity linked 1-to-1

2. **Phased approach**
   - Start with AOS entity immediately (speed)
   - Add custom entity later (flexibility)
   - Keep separation for future evolution

3. **Mixed user populations**
   - Standard users use AOS entity
   - Power users use extended custom entity
   - Example: Partner for general contacts, CustomerProfile for sales team

### When to AVOID HYBRID

1. **Adds complexity without benefit**
   - If custom needs are simple (2-3 fields) → Just EXTEND, don't split
   - If AOS entity provides no value → Just DEVELOP_NEW, don't use AOS

2. **User confusion risk**
   - If users will struggle with "Why are there two customer entities?"
   - If queries across both entities are common (performance hit)

---

## Recommendation Template

Use this template when providing recommendation:

```markdown
### Agent Recommendation for [EntityName]

**Suggested Option**: Option [N] - [REUSE/EXTEND/DEVELOP_NEW/HYBRID]

**Match Analysis**:
- Field match: [X]%
- AOS entity: [EntityName] from [module]

**Strategic Factors**:
- **Integration**: [High/Medium/Low] - [Explanation]
- **Timeline**: [Critical/Urgent/Normal/Flexible] - [Explanation]
- **Team expertise**: [Expert/Experienced/Intermediate/Novice]
- **Customization trajectory**: [Heavy/Moderate/Light]
- **Licensing**: [Concerns or no concerns]

**Rationale**:
[2-3 sentences explaining why this option balances match percentage and strategic factors]

**Trade-offs**:
- **Benefit**: [Key advantage of chosen option]
- **Cost**: [What user gives up with this choice]

**Alternative**: If [specific condition changes], consider [alternative option]
```

---

## Final Notes

- **Match percentage is starting point**, not final answer
- **Listen to user priorities**, they know their business
- **Don't fight for your recommendation**, present it but accept user override
- **Document reasoning**, especially for overrides
- **When in doubt**, ask clarifying questions (see @docs/analysis/gap-analysis-clarifying-questions.md)
