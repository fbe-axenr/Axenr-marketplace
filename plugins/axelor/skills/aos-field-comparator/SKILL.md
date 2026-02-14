---
name: aos-field-comparator
description: Compares required entity fields against AOS entity fields. Calculates match percentage, identifies matched/missing fields, detects type mismatches. Returns structured comparison data without making categorization decisions.
user-invocable: false
---

# AOS Field Comparator

## Mission

Perform detailed field-by-field comparison between client requirements and AOS entity definitions. Return structured comparison data to enable informed decision-making about reuse, extension, or new development.

**CRITICAL: This skill performs analysis and comparison ONLY. It does NOT make categorization decisions (REUSE/EXTEND/DEVELOP_NEW). Decision-making is reserved for the user.**

## Input Parameters

When invoked, expect the following information:

1. **Required Fields** (required): List of fields the client needs
   - Field name
   - Field type
   - Constraints (required, unique, readonly, etc.)
   - Relationships (if any)

2. **AOS Entity Details** (required): The AOS entity to compare against
   - Entity name
   - Complete field list
   - Field types and constraints
   - File path (for reference)

3. **Comparison Mode** (optional):
   - `strict` (default): Exact name and type matching
   - `semantic`: Allow semantically similar names (e.g., "email" matches "emailAddress")

## Comparison Process

### Step 1: Field Name Matching

For each required field, search AOS entity for:

1. **Exact match**: Same name exactly (e.g., "name" → "name")
2. **Semantic match**: Semantically equivalent names
   - "email" → "emailAddress"
   - "phone" → "mobilePhone"
   - "customer" → "partner"
   - "status" → "statusSelect"

3. **No match**: Field not found in AOS entity

### Step 2: Type Compatibility Check

For matched fields, verify type compatibility:

**Compatible types:**
- String ↔ String (exact)
- Integer ↔ Integer (exact)
- Decimal ↔ BigDecimal (compatible)
- Boolean ↔ Boolean (exact)
- Date ↔ LocalDate (compatible)
- DateTime ↔ LocalDateTime (compatible)
- Selection ↔ Selection (check values separately)
- many-to-one ↔ many-to-one (check target entity)
- one-to-many ↔ one-to-many (check target entity)

**Incompatible types:**
- String ↔ Integer
- Date ↔ String
- Selection ↔ String (if selection not defined)

### Step 3: Constraint Verification

For matched fields with compatible types, check constraints:

**Constraints to verify:**
- `required`: Field must not be null
- `unique`: Field must be unique in database
- `readonly`: Field cannot be modified after creation
- `min/max`: Numeric constraints
- `minSize/maxSize`: String length constraints

**Match levels:**
- Full match: All constraints identical
- Partial match: Some constraints differ (note differences)
- No match: Constraints incompatible

### Step 4: Relationship Analysis

For relationship fields (many-to-one, one-to-many, many-to-many):

**Check:**
1. Relationship type matches (many-to-one vs one-to-many)
2. Target entity exists
3. Target entity is compatible with requirement
4. Bidirectional relationships configured correctly

### Step 5: Calculate Match Percentage

**Formula:**
```
Match % = (Exact matches + 0.8 × Semantic matches) / Total required fields × 100
```

**Example:**
- Required fields: 10
- Exact matches: 6
- Semantic matches: 2
- Missing fields: 2
- Match % = (6 + 0.8 × 2) / 10 × 100 = 76%

## Output Format

Return structured comparison results in markdown format:

```markdown
# Field Comparison Results

**Client Entity**: [EntityName]
**AOS Entity**: [AOSEntityName] ([module])
**Comparison Mode**: [strict/semantic]

## Summary

**Match Score**: [X]% ([n]/[total] fields)
- Exact matches: [n]
- Semantic matches: [n]
- Missing fields: [n]
- Type mismatches: [n]

---

## Detailed Field Comparison

### Matched Fields ([n] fields)

| Required Field | AOS Field | Type Match | Constraints Match | Notes |
|----------------|-----------|------------|-------------------|-------|
| name | name | ✓ exact (string) | ✓ full (required, unique) | Perfect match |
| email | emailAddress | ✓ exact (string) | ⚠ partial (unique, not required in AOS) | AOS field is optional |
| phone | mobilePhone | ✓ exact (string) | ✓ full (optional) | Semantic name match |
| status | statusSelect | ✓ exact (selection) | ⚠ values differ | Need to verify selection values |
| customer | partner | ✓ exact (many-to-one) | ✓ full | Target: Partner entity |

### Missing Fields ([n] fields)

| Field Name | Type | Required | Description | Impact |
|------------|------|----------|-------------|--------|
| industry | Selection | Yes | Industry classification | High - Key business field |
| companySize | Integer | No | Number of employees | Medium - Useful metric |
| website | String | No | Company website URL | Low - Nice to have |

### Type Mismatches ([n] fields)

| Required Field | Required Type | AOS Field | AOS Type | Compatibility | Resolution |
|----------------|---------------|-----------|----------|---------------|------------|
| discount | Decimal | discount | Integer | ✗ Incompatible | Cast or redefine |
| createdOn | Date | createdOn | DateTime | ⚠ Partial | Truncate time portion |

### Extra AOS Fields (not in requirements)

**Additional fields available in AOS entity** ([n] fields):
- partnerSeq (string): Partner sequence number
- companySet (one-to-many → Company): Related companies
- contactSet (one-to-many → Contact): Related contacts
- currency (many-to-one → Currency): Default currency
- [... list notable extra fields]

**Benefit**: These fields provide additional functionality that may be useful even if not explicitly required.

---

## Relationship Analysis

### Required Relationships

| Relationship | Type | Target | Status | AOS Equivalent |
|--------------|------|--------|--------|----------------|
| addresses | one-to-many | Address | ✓ Available | partnerAddressList (one-to-many → PartnerAddress) |
| primaryContact | many-to-one | Contact | ✓ Available | contactPartner (many-to-one → Partner) |
| orders | one-to-many | Order | ✗ Missing | No equivalent, needs development |

---

## Constraint Comparison Details

### Field: email / emailAddress

**Required constraints:**
- unique: true
- required: true
- email validation: true

**AOS constraints:**
- unique: true
- required: false ⚠
- email validation: true

**Impact**: AOS allows null emails, requirement mandates email. Need to add required constraint or validation.

### Field: status / statusSelect

**Required values:**
- ACTIVE
- INACTIVE
- PENDING

**AOS values:**
- CUSTOMER
- SUPPLIER
- COMPETITOR

**Impact**: ✗ Incompatible selection values. Need to:
1. Use AOS values (adapt requirement), OR
2. Create custom selection, OR
3. Map values in code

---

## Semantic Similarity Notes

**Name variations detected:**
- "email" → "emailAddress" (common Axelor pattern)
- "phone" → "mobilePhone" (AOS uses specific phone types)
- "customer" → "partner" (AOS generic term for customers/suppliers)

**Recommendation**: Use AOS naming conventions for consistency with ecosystem.

---

## Token Efficiency Summary

For presentation to user, use this concise format:

**Match: [X]% ([n]/[total] fields)**

**Matched**: name, email (→emailAddress), phone (→mobilePhone), status (⚠values differ)
**Missing**: industry, companySize
**Mismatches**: discount (Decimal→Integer)
**Bonus**: +12 extra AOS fields (addresses, contacts, currency...)
```

## Analysis Without Decision

**IMPORTANT:** This skill provides comparison data but does NOT output:
- ❌ "Recommendation: EXTEND"
- ❌ "Action: Use AOS entity"
- ❌ "Category: REUSE"

**Instead, provide neutral analysis:**
- ✅ "Match score: 76%"
- ✅ "2 fields missing, moderate extension effort"
- ✅ "All matched fields have compatible types"

The **agent** or **user** makes categorization decisions based on this data.

## Error Handling

**If required fields not provided:**
```markdown
ERROR: Required fields list is empty or malformed.

Please provide required fields in format:
- fieldName (type, constraints)
```

**If AOS entity details incomplete:**
```markdown
WARNING: AOS entity field list incomplete.

Comparison may be inaccurate. Ensure AOS entity data includes:
- All fields
- Field types
- Constraints
```

## Performance Optimization

1. **Field lookup**: Use hash map for O(1) AOS field lookup
2. **Semantic matching**: Predefined mapping table for common variations
3. **Output limiting**: If > 30 matched fields, summarize groups
4. **Relationship analysis**: Only for explicitly requested relationships

## Example Invocation

**Agent request:**
"Compare required Customer entity fields against AOS Partner entity."

**Required fields:**
```
- name (string, required, unique)
- email (string, required, unique)
- phone (string, optional)
- industry (selection, required)
- companySize (integer, optional)
- status (selection, required, values: ACTIVE/INACTIVE)
```

**AOS Partner fields:**
```
- name (string, required, unique)
- emailAddress (string, unique)
- mobilePhone (string)
- partnerCategory (many-to-one → PartnerCategory)
- statusSelect (selection, values: CUSTOMER/SUPPLIER/COMPETITOR)
- [... 18 other fields]
```

**Skill output:**
```markdown
# Field Comparison Results

**Match Score**: 60% (3.6/6 fields)
- Exact matches: 2 (name, status)
- Semantic matches: 2 (email, phone)
- Missing fields: 2 (industry, companySize)
- Type mismatches: 0

### Matched Fields (4 fields)
[Detailed table as shown in Output Format]

### Missing Fields (2 fields)
[Detailed table as shown in Output Format]

### Selection Value Issue
statusSelect: Required (ACTIVE/INACTIVE) vs AOS (CUSTOMER/SUPPLIER/COMPETITOR)
⚠ Need to define custom selection or map values
```

## Integration with Gap Analyzer

**Workflow:**
```
Gap Analyzer: [Invokes aos-entity-searcher]
  → Finds: Partner entity (85% name match)

Gap Analyzer: [Invokes aos-field-comparator]
  → Required fields: [Customer fields]
  → AOS entity: [Partner details from searcher]

Field Comparator: [Returns comparison data]
  → 60% field match
  → 2 missing fields
  → 1 constraint mismatch

Gap Analyzer: [Uses data to present options to user]
  → Option 1: REUSE (skip 2 fields)
  → Option 2: EXTEND (add 2 fields) ← Recommended based on 60%
  → Option 3: DEVELOP_NEW (full control)
  → User decides
```

## Success Criteria

**Complete comparison includes:**
1. Match percentage calculated
2. All matched fields identified (exact + semantic)
3. All missing fields listed
4. Type compatibility checked
5. Constraint differences noted
6. Relationship analysis performed
7. Token-efficient output (< 1500 tokens for typical entity)

**Quality indicators:**
- Semantic matching catches common variations
- Type compatibility logic is accurate
- Constraint analysis is thorough
- Extra AOS fields are noted (bonus features)
