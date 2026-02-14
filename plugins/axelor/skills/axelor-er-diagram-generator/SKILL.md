---
name: axelor-er-diagram-generator
description: Generate ASCII Entity Relationship diagrams from Axelor domain specifications or XML files. Creates visual representations of entities, fields, and relationships.
allowed-tools: ["Read", "Write", "Glob", "Grep"]
---

# Axelor ER Diagram Generator

## Mission

Generate clear, ASCII-based Entity Relationship diagrams from Axelor domain specifications or existing domain XML files. Create visual representations that show entities, their key fields, and relationships with proper cardinality notation.

## What This Skill Does

**Inputs:**
1. Domain XML files from `domains/*.xml`
2. Architecture specifications with entity descriptions
3. Entity lists with relationship information

**Outputs:**
- ASCII ER diagrams in markdown format
- Shows entities as boxes with key fields
- Displays relationships with cardinality (1..1, 0..1, 0..*, 1..*)
- Indicates relationship types (many-to-one, one-to-many, many-to-many)
- Marks composition relationships

## Usage Scenarios

### 1. Generate from Existing Domain XMLs

```bash
# User provides domain directory
"Generate ER diagram from domains in: src/main/resources/domains/"
```

**Process:**
1. Scan all XML files in domains directory
2. Parse entity definitions (name, fields, relationships)
3. Build entity graph with relationships
4. Generate ASCII diagram with proper layout

### 2. Generate from Architecture Specification

```bash
# User provides architecture plan document
"Generate ER diagram from architecture-plan.md"
```

**Process:**
1. Read architecture document
2. Extract entity definitions and relationships
3. Build entity graph
4. Generate ASCII diagram

### 3. Generate for Specific Entities

```bash
# User specifies entities
"Generate ER diagram for: SaleOrder, SaleOrderLine, Partner, Product"
```

**Process:**
1. Find specified entities in domain files
2. Include related entities referenced in relationships
3. Generate focused diagram

## ER Diagram Format

### Entity Box Structure

```
┌─────────────────┐
│   EntityName    │  ← Entity name (PascalCase)
│─────────────────│
│ field1          │  ← Key fields (4-6 most important)
│ field2          │
│ field3          │
└─────────────────┘
```

### Relationship Notation

**Many-to-One (N..1):**
```
┌─────────────┐         ┌──────────┐
│  SaleOrder  │────────►│ Partner  │
│             │  N..1   │          │
└─────────────┘         └──────────┘
```

**One-to-Many (1..N) - Composition:**
```
┌─────────────┐
│  SaleOrder  │
└─────────────┘
       │
       │ 1..N (composition)
       ▼
┌─────────────┐
│SaleOrderLine│
└─────────────┘
```

**Many-to-Many (N..M):**
```
┌─────────────┐         ┌──────────┐
│  Project    │◄───────►│   User   │
│             │  N..M   │          │
└─────────────┘         └──────────┘
```

### Cardinality Symbols

- `1..1` : Exactly one (required)
- `0..1` : Zero or one (optional)
- `1..*` or `1..N` : One to many (at least one required)
- `0..*` or `0..N` : Zero to many (optional, multiple)
- `N..1` : Many to one (from many side perspective)

### Relationship Indicators

- `►` : Direction of many-to-one
- `▼` : Direction of one-to-many (vertical)
- `◄─►` : Bidirectional many-to-many
- `(composition)` : Parent owns children (cascade delete)

## Implementation Guidelines

### Step 1: Parse Entities

**From XML:**
```xml
<entity name="SaleOrder">
    <string name="orderNo" required="true"/>
    <many-to-one name="partner" ref="com.axelor.apps.base.db.Partner"/>
    <one-to-many name="orderLines" ref="SaleOrderLine" mappedBy="saleOrder"/>
</entity>
```

**Extract:**
- Entity name: `SaleOrder` (table auto-generated as `sale_order`)
- Key fields: `orderNo`, `partner` (show 4-6 most important)
- Relationships: partner (many-to-one), orderLines (one-to-many)

### Step 2: Build Relationship Graph

**Data structure:**
```javascript
{
  "SaleOrder": {
    "fields": ["orderNo", "orderDate", "partner", "totalAmount"],
    "relationships": [
      {
        "field": "partner",
        "type": "many-to-one",
        "target": "Partner",
        "cardinality": "N..1"
      },
      {
        "field": "orderLines",
        "type": "one-to-many",
        "target": "SaleOrderLine",
        "cardinality": "1..*",
        "composition": true,
        "mappedBy": "saleOrder"
      }
    ]
  }
}
```

### Step 3: Layout Algorithm

**Principles:**
1. Place parent entities higher than children
2. Group related entities close together
3. Minimize crossing lines
4. Composition relationships vertical (parent above child)
5. Association relationships horizontal (side by side)

**Simple layout:**
```
Level 0: Independent entities (no parents)
Level 1: Entities that reference Level 0
Level 2: Entities that reference Level 1
...
```

### Step 4: Generate ASCII Art

**Box drawing characters:**
- `┌` `─` `┐` : Top border
- `│` : Vertical border
- `├` `─` `┤` : Separator
- `└` `─` `┘` : Bottom border
- `►` `▼` : Arrow heads
- `───` : Horizontal line
- `│` : Vertical line

### Step 5: Format Output

**Markdown structure:**
```markdown
## Entity Relationship Diagram

### Overview
[Brief description of the diagram]

### Diagram

[ASCII diagram here]

### Legend

- `N..1` : Many to one relationship
- `1..*` : One to many relationship
- `N..M` : Many to many relationship
- `(composition)` : Parent owns children

### Entities

**SaleOrder:**
- Main entity for sales orders
- Relationships: Partner (many-to-one), SaleOrderLine (one-to-many composition)

[List all entities with brief descriptions]
```

## Example Input/Output

### Input: Domain XML Files

**domains/SaleOrder.xml:**
```xml
<entity name="SaleOrder">
    <string name="orderNo"/>
    <date name="orderDate"/>
    <many-to-one name="partner" ref="Partner"/>
    <decimal name="totalAmount"/>
    <one-to-many name="orderLines" ref="SaleOrderLine" mappedBy="saleOrder"/>
</entity>
```

**domains/SaleOrderLine.xml:**
```xml
<entity name="SaleOrderLine">
    <integer name="sequence"/>
    <many-to-one name="saleOrder" ref="SaleOrder"/>
    <many-to-one name="product" ref="Product"/>
    <decimal name="quantity"/>
    <decimal name="price"/>
</entity>
```

### Output: ER Diagram

```markdown
## Entity Relationship Diagram

### Diagram

┌─────────────────┐         ┌──────────────┐
│   SaleOrder     │         │   Partner    │
│─────────────────│         │──────────────│
│ orderNo         │────────►│ code         │
│ orderDate       │  N..1   │ fullName     │
│ totalAmount     │         │              │
└─────────────────┘         └──────────────┘
       │
       │ 1..N (composition)
       ▼
┌─────────────────┐         ┌──────────────┐
│ SaleOrderLine   │         │   Product    │
│─────────────────│         │──────────────│
│ sequence        │────────►│ code         │
│ product         │  N..1   │ name         │
│ quantity        │         │ salePrice    │
│ price           │         │              │
└─────────────────┘         └──────────────┘

### Legend

- `N..1` : Many to one (required reference)
- `0..1` : Optional reference
- `1..*` : One to many (at least one)
- `(composition)` : Parent owns children (cascade delete)

### Entities

**SaleOrder**: Main sales order entity with order lines and partner reference
**SaleOrderLine**: Individual line items in a sales order
**Partner**: Customer or supplier reference
**Product**: Product catalog reference
```

## Quality Checks

Before outputting diagram, verify:

1. **Completeness**: All entities shown
2. **Relationships**: All relationships displayed with correct cardinality
3. **Layout**: No overlapping boxes or crossing lines (where possible)
4. **Consistency**: Entity names match domain definitions
5. **Readability**: Diagram fits in standard terminal width (80-120 chars)

## Handling Complex Diagrams

**If too many entities (>10):**
1. Offer to generate multiple focused diagrams
2. Group by module or functional area
3. Create overview diagram + detailed sub-diagrams

**If too many relationships:**
1. Show only direct relationships
2. Omit redundant paths
3. Focus on composition relationships first

## Error Handling

**Domain files not found:**
- Ask user for correct domain directory path
- Suggest common locations: `src/main/resources/domains/`, `domains/`

**No relationships found:**
- Show standalone entity boxes
- Suggest this might be incomplete architecture

**Circular dependencies:**
- Show with bidirectional arrows
- Add note about circular reference

## User Interaction

**After generating diagram:**
1. Show the complete diagram
2. Offer to:
   - Generate focused sub-diagrams
   - Export to file
   - Regenerate with different layout
   - Add/remove specific entities

**Example:**
```
Generated ER diagram with 5 entities and 8 relationships.

Would you like me to:
1. Export to architecture-plan.md
2. Generate separate diagram for Order module only
3. Include additional entities
```

## Best Practices

1. **Keep diagrams simple**: 5-8 entities per diagram is optimal
2. **Show key fields only**: 4-6 most important fields per entity
3. **Prioritize composition**: Show parent-child relationships prominently
4. **Use consistent layout**: Similar entities in similar positions
5. **Add context**: Include legend and entity descriptions

## Integration with Architecture Workflow

This skill can be invoked:
- **During architecture design**: Visualize entity relationships as you design
- **After domain generation**: Verify generated domains match architecture
- **For documentation**: Create visual documentation for architecture plans
- **During code review**: Understand existing entity structures

**Typical workflow:**
1. Architect designs entities → uses this skill to visualize
2. Validates relationships and cardinality
3. Exports diagram to architecture plan document
4. Domain generator uses architecture plan to generate XML
5. This skill verifies generated domains match design

---

**Note**: This skill focuses on ASCII diagrams for terminal/markdown compatibility. For presentation-quality diagrams, consider exporting to PlantUML or Mermaid format (future enhancement).
