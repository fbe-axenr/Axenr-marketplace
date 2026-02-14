---
name: functional-spec-synthesis
description: Generates executive summary of functional specification documents for stakeholder review
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Functional Spec Synthesis

## Mission

Generate a concise, high-level summary (~800 words) from detailed functional specification documents (`detailed-specifications.md`). The synthesis provides stakeholders with a quick overview of business requirements, constraints, and rules.

---

## Input

- **Source document**: `detailed-specifications.md` or similar functional specification document
- **Output path**: Specified by caller (typically `{output_directory}/functional-synthesis.md`)

---

## Output Sections

Generate the following sections in order:

### 1. Header
```markdown
# Functional Summary - {Feature Name}

**Module**: `{module-name}`
**AOS Version**: {version}
```

### 2. Business Objectives
- Bullet points (4-6 items)
- Focus on WHAT the feature achieves for users
- Business-oriented language, no technical terms

### 3. Scope (Table)
| In Scope | Out of Scope |
|----------|--------------|
| Features included | Features explicitly excluded |

### 4. Main Flow (Mermaid sequenceDiagram)
- Participants: `actor User` and `participant System` ONLY
- NO technical names (no controllers, services, classes)
- Use business language for interactions
- 4-6 key interactions maximum

### 5. Workflow Overview (Mermaid flowchart LR)
- Horizontal layout (Left to Right)
- High-level process stages
- 4-6 stages maximum
- Short labels with line breaks (`\n`)

### 6. Detailed Workflow (Mermaid flowchart TB with subgraphs)
- **MUST use subgraphs** to avoid crossing arrows
- Structure: Trigger → Actions → Results
- Top-to-bottom flow ONLY
- NO backward arrows or loops

### 7. Business Constraints (Table)
| Constraint | Description | Business Impact |
|------------|-------------|-----------------|
| Name | Full explanation of the constraint | Impact on users/business |

- **Description**: Complete sentence explaining WHAT and WHEN
- **Business Impact**: Consequence for users, workarounds if any

### 8. Business Rules (Table)
| Rule | Trigger | Behavior |
|------|---------|----------|
| Name | Event that activates the rule | Complete description of system behavior |

- **Trigger**: When does this rule apply?
- **Behavior**: Detailed explanation (2-3 sentences minimum)

### 9. AOS Integration Points (Table)
| Functional Capability | Usage in this Feature |
|-----------------------|-----------------------|
| Business capability name | How it's used (functional language) |

- **CRITICAL**: NO Java class names, NO technical identifiers
- Use functional descriptions only (e.g., "Parent-child line hierarchy" not "SaleOrderLine.parentSaleOrderLine")

### 10. References
- Link to detailed specification document

---

## Generation Rules

### Language
- **ALL content in English** (strict consistency)
- Business-oriented vocabulary
- NO technical jargon (no class names, method names, XML references)

### Diagram Guidelines

**sequenceDiagram**:
- Only `actor User` and `participant System`
- Business actions, not technical calls
- Example: "Add product to quotation" NOT "onClick(product)"

**flowchart LR** (Overview):
- Horizontal, left-to-right
- Stage names only
- Use `\n` for line breaks in labels

**flowchart TB** (Detailed):
- MUST use `subgraph` blocks to organize
- Structure:
  ```
  subgraph trigger [Trigger]
  end
  subgraph actions [Available Actions]
  end
  subgraph results [System Response]
  end
  ```
- Downward flow ONLY - NO backward arrows
- This prevents crossing lines

### Table Guidelines
- Constraints: Include Business Impact column
- Rules: Include Trigger and detailed Behavior
- Integrations: Functional language only

### Exclusions
- **NO "Actors" section** (considered superfluous)
- **NO ERD/data model diagrams** (too technical for functional summary)
- **NO class diagrams** (technical, not functional)

---

## Process

1. **Read** the source specification document completely
2. **Identify** business objectives and scope boundaries
3. **Extract** constraints and rules with their impacts
4. **Map** the main user workflow
5. **Translate** technical integrations to functional capabilities
6. **Generate** diagrams using proper structure (subgraphs for flowcharts)
7. **Verify** no technical terms leaked into functional content
8. **Write** synthesis to output path

---

## Validation Checklist

Before finalizing, verify:

- [ ] All content is in English
- [ ] sequenceDiagram uses only User/System participants
- [ ] flowchart TB uses subgraphs (no crossing arrows)
- [ ] Business Constraints table has Description + Business Impact
- [ ] Business Rules table has Trigger + detailed Behavior
- [ ] AOS Integrations use functional names (no class names)
- [ ] No technical jargon anywhere
- [ ] No Actors section
- [ ] No data model/ERD diagrams

---

## Template Reference

See `reference/synthesis-template.md` for the expected output format.

---

## Integration

This skill is invoked by:
- **doc-synthesis-agent** agent (automatic detection)
- **analyze-requirements.md** command (Phase 2.5)

Output is used for:
- Stakeholder review
- Requirements validation
- Onboarding business analysts
