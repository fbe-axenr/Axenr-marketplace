---
name: aos-entity-searcher
description: Searches Axelor Open Suite (AOS) codebase for entities matching a given concept. Returns structured match data with scores, file paths, packages, and field lists. Automates entity discovery for gap analysis.
user-invocable: false
---

# AOS Entity Searcher

## Mission

Automate the discovery of entities in Axelor Open Suite (AOS) codebase that match a given business concept or entity name. Return structured, ranked results to enable efficient gap analysis.

## Input Parameters

When invoked, expect the following information:

1. **Entity Concept** (required): The business concept to search for (e.g., "Customer", "Invoice", "Product")
2. **Search Terms** (optional): Alternative or related terms to search (e.g., ["Partner", "Client", "Customer"])
3. **AOS Path** (required): Path to the AOS codebase (e.g., `/path/to/axelor-open-suite`)

## Search Strategy

### 1. Multi-Strategy Search

Execute searches in parallel using multiple strategies:

#### Strategy A: Exact Entity Name Match
```bash
grep -r "entity name=\"[EntityName]\"" {aos_path}/axelor-*/*/domains/
```

#### Strategy B: Case-Insensitive Concept Search
```bash
grep -ri "entity.*name=\".*[Concept]" {aos_path}/axelor-*/*/domains/
```

#### Strategy C: Alternative Terms Search
For each alternative term:
```bash
grep -ri "entity.*name=\".*[Term]" {aos_path}/axelor-*/*/domains/
```

### 2. File Discovery

Use Glob to find all domain XML files:
```bash
pattern: **/domains/*.xml
path: {aos_path}
```

### 3. Entity Extraction

For each matched file:
1. Use Read tool to parse the XML content
2. Extract:
   - Entity name
   - Package name
   - All field definitions (name, type, constraints)
   - Table name (if specified)
   - Extends clause (if present)

### 4. Scoring Algorithm

Calculate match score for each entity (0-100):

**Score Calculation:**
- Exact name match: 100 points
- Case-insensitive name match: 90 points
- Concept appears in entity name: 80 points
- Alternative term exact match: 85 points
- Alternative term partial match: 70 points
- Semantic similarity (same domain area): +10 bonus

**Examples:**
- Searching "Customer" finds "Customer": 100 points
- Searching "Customer" finds "Partner": 80 points (concept match)
- Searching "Invoice" finds "AccountingInvoice": 80 points (concept in name)

## Output Format

Return results as structured markdown with JSON-style data representation:

```markdown
# Entity Search Results

**Search concept**: [Concept]
**Search terms**: [Term1, Term2, ...]
**Matches found**: [N]

## Match 1: [EntityName] (Score: [X]/100)

**Entity**: [EntityName]
**File**: {aos_path}/[module-name]/src/main/resources/domains/[EntityName].xml
**Package**: [com.axelor.apps.module.db]
**Module**: [axelor-module-name]
**Table**: [table_name] (or "auto-generated")
**Extends**: [BaseEntity] (or "None")

**Fields** ([N] total):
- name (string, required)
- code (string, unique)
- emailAddress (string)
- mobilePhone (string)
- partnerCategory (many-to-one → PartnerCategory)
- addresses (one-to-many → Address)
- [... list all fields with type and key constraints]

**Documentation**: https://docs.axelor.com/aos/modules/[module]/

---

## Match 2: [EntityName] (Score: [X]/100)

[Same structure as Match 1]

---

[Continue for all matches]
```

## Ranking and Filtering

1. **Rank matches** by score (highest first)
2. **Limit results** to top 5 matches (unless user requests more)
3. **Exclude matches** with score < 50 (too irrelevant)
4. **Group by module** if multiple matches from same module

## Error Handling

**If no matches found:**
```markdown
# Entity Search Results

**Search concept**: [Concept]
**Matches found**: 0

No entities found in AOS matching "[Concept]".

**Suggestions**:
- Try alternative search terms
- Check if concept exists in AOS under different name
- Consider this entity may need to be developed from scratch (DEVELOP_NEW)
```

**If AOS path invalid:**
```markdown
ERROR: AOS path not found or inaccessible: [path]

Please verify:
1. Path exists
2. Path points to axelor-open-suite root directory
3. User has read permissions
```

## Performance Optimization

1. **Use parallel searches** when possible (multiple grep patterns simultaneously)
2. **Cache results** during same session (if searching multiple concepts)
3. **Limit Read operations** to top 10 matched files only
4. **Use Grep filters** to exclude test files, build artifacts

## Example Invocation

**User request:**
"Search AOS for an entity matching 'Customer' concept. Also check for 'Partner' and 'Client'."

**Skill execution:**
1. Run 3 parallel Grep searches (Customer, Partner, Client)
2. Find 8 matching files
3. Read top 5 matched files
4. Extract entity details
5. Calculate scores:
   - Partner: 85 (alternative term exact match)
   - Client: 80 (concept match)
   - Contact: 60 (low relevance)
6. Return top 3 ranked results with full field details

## Integration with Gap Analyzer

This skill is designed to be invoked by the `aos-analyzer` agent:

**Agent workflow:**
```
Agent: For requirement "Customer entity with fields: name, email, phone, industry"
Agent: [Invoke aos-entity-searcher skill]
  → Concept: "Customer"
  → Terms: ["Partner", "Client"]
  → AOS path: {aos_path} (from workflow context, e.g., ".axelor/aos")

Skill: [Returns ranked matches]
  → Match 1: Partner (85/100, 6 fields)
  → Match 2: Contact (60/100, 4 fields)

Agent: [Uses results for field comparison]
```

## Token Efficiency

**Output optimizations:**
- Limit field lists to first 20 fields (+ count if more)
- Omit verbose XML/Java code snippets
- Use concise field notation: `fieldName (type, constraint)`
- Group similar fields: `address1, address2, address3 (string)`

**Example optimized output:**
```markdown
**Fields** (24 total, showing key fields):
- name, code, emailAddress (string, required)
- mobilePhone, fax (string, optional)
- partnerCategory (many-to-one → PartnerCategory)
- addresses (one-to-many → Address, 6 related fields)
... (14 more standard fields)
```

## Success Criteria

**Successful execution returns:**
1. At least 1 match (or clear "no matches" message)
2. Complete field lists for each match
3. Accurate scoring
4. File paths and package names
5. Token-efficient output (< 2000 tokens for 5 matches)

**Quality checks:**
- All file paths are valid
- All entities actually exist in specified files
- Scores reflect match quality accurately
- Fields are complete and correctly typed
