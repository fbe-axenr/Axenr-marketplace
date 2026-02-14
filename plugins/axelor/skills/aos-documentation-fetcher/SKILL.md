---
name: aos-documentation-fetcher
description: Fetches and parses Axelor Open Suite (AOS) documentation for modules, entities, and features. Extracts module capabilities, entity information, and integration details. Caches results for efficiency.
user-invocable: false
---

# AOS Documentation Fetcher

## Mission

Retrieve and parse Axelor Open Suite (AOS) documentation to provide context about modules, entities, features, and integration capabilities. Enable informed decisions about reusing AOS components vs developing custom solutions.

## Input Parameters

When invoked, expect one of the following:

1. **Module Documentation Request**
   - Module name (e.g., "axelor-base", "axelor-crm", "axelor-sale")
   - Information needed: capabilities, entities, features

2. **Entity Documentation Request**
   - Entity name (e.g., "Partner", "Invoice", "Product")
   - Module context (if known)

3. **Feature Documentation Request**
   - Feature description (e.g., "address management", "email integration")
   - Related modules

## Documentation Sources

### Primary Sources (in order of preference)

1. **Official AOS Documentation**
   - Base URL: `https://docs.axelor.com/`
   - Module docs: `https://docs.axelor.com/aos/modules/{module}/`
   - API reference: `https://docs.axelor.com/adk/`

2. **GitHub README Files**
   - AOS Repository: `https://github.com/axelor/axelor-open-suite`
   - Module READMEs: `https://github.com/axelor/axelor-open-suite/tree/dev/axelor-{module}`

3. **Javadoc/Code Comments**
   - If AOS codebase accessible locally
   - Parse entity/service comments for inline documentation

### Documentation URLs by Module

**Core Modules:**
- axelor-base: `https://docs.axelor.com/aos/modules/base/`
- axelor-crm: `https://docs.axelor.com/aos/modules/crm/`
- axelor-sale: `https://docs.axelor.com/aos/modules/sale/`
- axelor-purchase: `https://docs.axelor.com/aos/modules/purchase/`
- axelor-account: `https://docs.axelor.com/aos/modules/account/`
- axelor-stock: `https://docs.axelor.com/aos/modules/stock/`
- axelor-production: `https://docs.axelor.com/aos/modules/production/`
- axelor-human-resource: `https://docs.axelor.com/aos/modules/human-resource/`

**ADK Documentation:**
- Development guide: `https://docs.axelor.com/adk/dev-guide/`
- Data model: `https://docs.axelor.com/adk/dev-guide/data-model/`

## Fetch Process

### Step 1: Determine Documentation URL

Based on input, construct appropriate URL:

**For module:**
```
https://docs.axelor.com/aos/modules/{module-name}/
```

**For entity (if module known):**
```
https://docs.axelor.com/aos/modules/{module-name}/#{entity-name-lowercase}
```

**For general search:**
```
https://docs.axelor.com/aos/search/?q={search-term}
```

### Step 2: Fetch Content

Use WebFetch tool with appropriate prompt:

**For module capabilities:**
```
WebFetch URL: [module_doc_url]
Prompt: "Extract module capabilities, key entities, main features, and integration points. List all entities defined in this module with brief descriptions."
```

**For entity details:**
```
WebFetch URL: [entity_doc_url]
Prompt: "Extract entity purpose, key fields, relationships, business rules, and usage examples. Include information about services and repositories if available."
```

**For feature search:**
```
WebFetch URL: [search_url]
Prompt: "Find information about [feature]. Which modules provide this capability? List relevant entities and services."
```

### Step 3: Parse and Structure Results

Transform fetched content into structured format:

```markdown
# [Module/Entity Name] Documentation

**Source**: [URL]
**Last fetched**: [timestamp]

## Overview
[Brief description of module/entity purpose]

## Key Capabilities
- Capability 1: [description]
- Capability 2: [description]
- [...]

## Entities
1. **EntityName**: [Brief description]
   - Key fields: field1, field2, field3
   - Relationships: [related entities]

2. **EntityName**: [Brief description]
   [...]

## Features
- Feature 1: [description and usage]
- Feature 2: [description and usage]
[...]

## Integration Points
- Integrates with: [other modules]
- Provides: [APIs, services, events]
- Depends on: [required modules]

## Use Cases
[Common scenarios where this module/entity is used]
```

## Output Format

Return documentation summary optimized for gap analysis:

```markdown
# AOS Documentation: [Module/Entity Name]

**Documentation URL**: [url]
**Module**: [module-name]
**Status**: ✓ Available | ⚠ Partial | ✗ Not Found

---

## Module Capabilities

**Purpose**: [One-line description]

**Core Functionality**:
1. [Feature 1]: [Description]
2. [Feature 2]: [Description]
3. [Feature 3]: [Description]

**Business Value**:
- [Benefit 1]
- [Benefit 2]

---

## Entities in Module ([n] total)

### Primary Entities

1. **[EntityName]** (com.axelor.apps.{module}.db.{Entity})
   - **Purpose**: [Brief description]
   - **Key fields**: name, code, status, [...]
   - **Relationships**:
     - → [RelatedEntity1] (many-to-one)
     - ← [RelatedEntity2] (one-to-many)
   - **Services**: [ServiceName]Service (CRUD, compute, validate)

2. **[EntityName]**
   [Same structure]

[Continue for relevant entities]

### Supporting Entities
- [Entity1], [Entity2], [Entity3]: [Brief group description]

---

## Features Provided

**Feature: [Feature Name]**
- **Description**: [What it does]
- **Entities involved**: [Entity1, Entity2]
- **Configuration**: [How to enable/configure]
- **Limitations**: [Known constraints]

[Repeat for each feature]

---

## Integration & Dependencies

**Depends on modules**:
- axelor-base (required)
- axelor-message (optional, for email integration)

**Provides to other modules**:
- Partner management → Used by CRM, Sale, Purchase
- Address model → Used by Stock, HR

**Extension points**:
- [How to extend this module]
- [Which entities commonly extended]

---

## Reuse Considerations

**Benefits of reusing this module**:
✓ [Benefit 1: e.g., "Mature codebase, well-tested"]
✓ [Benefit 2: e.g., "Integrates with 5+ other AOS modules"]
✓ [Benefit 3: e.g., "Active development, regular updates"]

**Constraints**:
✗ [Constraint 1: e.g., "Requires specific workflow engine"]
✗ [Constraint 2: e.g., "Not compatible with external CRM systems"]

**Licensing**:
- License: AGPL-3.0 (or commercial for Enterprise)
- Implications: [Brief explanation for commercial use]

---

## Examples & Use Cases

**Example 1: [Use case name]**
```
[Brief code example or configuration]
```

**Example 2: [Use case name]**
```
[Brief code example or configuration]
```

---

## Additional Resources

- Module source: https://github.com/axelor/axelor-open-suite/tree/dev/axelor-{module}
- API reference: [link if available]
- Related forum discussions: [link if relevant]
```

## Caching Strategy

**Cache documentation results** during session to avoid redundant fetches:

**Cache key**: `{module_name}` or `{entity_name}@{module_name}`

**Cache duration**: Session lifetime (or 1 hour for long sessions)

**Cache invalidation**: User can request fresh fetch with `force_refresh: true`

**Benefits**:
- Faster subsequent lookups
- Reduced WebFetch calls
- Token efficiency

## Error Handling

**If documentation not found:**
```markdown
# AOS Documentation: [Module/Entity Name]

**Status**: ✗ Not Found

Unable to retrieve documentation for "[name]".

**Possible reasons**:
1. Module/entity does not exist in AOS
2. Documentation not yet published for this version
3. Name spelling variation (try alternative names)

**Suggestions**:
- Search AOS GitHub: https://github.com/axelor/axelor-open-suite
- Check AOS forum: https://discuss.axelor.com/
- Review local AOS codebase if available

**Impact on gap analysis**:
- Cannot assess module capabilities from documentation
- Recommend code analysis if codebase accessible
- Consider DEVELOP_NEW if component not found in AOS
```

**If documentation is partial:**
```markdown
**Status**: ⚠ Partial

Documentation found but incomplete.

**Available information**:
[List what was found]

**Missing information**:
[List what's missing]

**Recommendation**: Supplement with code analysis or team knowledge.
```

**If WebFetch fails:**
```markdown
**Status**: ✗ Fetch Failed

Error fetching documentation: [error message]

**Fallback options**:
1. Retry with alternative URL
2. Search GitHub README files
3. Analyze local codebase directly
```

## Performance Optimization

1. **Parallel fetches**: If multiple modules requested, fetch in parallel
2. **Lazy loading**: Only fetch entity details on demand
3. **Selective parsing**: Extract only relevant sections for gap analysis
4. **Token budget**: Limit output to 1500 tokens per module (summarize if longer)

## Example Invocation

**Agent request:**
"Fetch documentation for axelor-base module, specifically Partner entity capabilities."

**Skill execution:**
1. Construct URL: `https://docs.axelor.com/aos/modules/base/#partner`
2. Fetch with WebFetch
3. Parse content, extract:
   - Partner entity purpose and fields
   - Related entities (Address, Contact, etc.)
   - Services available (PartnerService)
   - Integration points
4. Format structured output
5. Cache result with key `Partner@axelor-base`
6. Return markdown summary (< 1500 tokens)

**Output:**
```markdown
# AOS Documentation: Partner (axelor-base)

**Purpose**: Core entity representing customers, suppliers, and generic partners

**Key fields**: name, code, emailAddress, mobilePhone, partnerCategory, addresses (one-to-many), contacts (one-to-many)

**Services**: PartnerService (address validation, duplicate detection, email formatting)

**Integration**: Used by CRM, Sale, Purchase, Project modules

**Reuse value**: ✓ High - Central to AOS ecosystem, well-tested, extensive features

[Full structured output as per template]
```

## Integration with Gap Analyzer

**Workflow:**
```
Gap Analyzer: Entity "Customer" needs analysis
Gap Analyzer: [Invokes aos-entity-searcher]
  → Finds: Partner entity in axelor-base

Gap Analyzer: [Invokes aos-documentation-fetcher]
  → Request: Partner entity documentation

Documentation Fetcher: [Fetches and parses]
  → Returns: Partner capabilities, integration points, reuse value

Gap Analyzer: [Uses documentation in user presentation]
  → "Partner entity provides address management, contact lists, category classification..."
  → "Integrates with CRM, Sale, Purchase modules"
  → "Recommendation: EXTEND for compatibility with AOS ecosystem"
```

## Token Efficiency Guidelines

**Output length targets:**
- Module overview: 500-800 tokens
- Entity details: 300-500 tokens
- Feature documentation: 200-300 tokens per feature

**Truncation strategies:**
- Limit entity list to top 10 most relevant
- Summarize less critical features
- Use bullet points over paragraphs
- Omit code examples unless specifically requested

## Success Criteria

**Successful fetch includes:**
1. Module/entity purpose clearly stated
2. Key capabilities listed (3-10 items)
3. Primary entities identified with brief descriptions
4. Integration points noted
5. Reuse considerations provided (benefits + constraints)
6. Token-efficient output (< 1500 tokens for module, < 800 for entity)

**Quality indicators:**
- Information is current (latest AOS version)
- Links are valid and accessible
- Content is relevant to gap analysis decisions
- Licensing implications noted for commercial use
