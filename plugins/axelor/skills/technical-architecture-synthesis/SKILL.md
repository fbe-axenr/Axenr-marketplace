---
name: technical-architecture-synthesis
description: Generates executive summary of technical architecture documents for team onboarding and review
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# Technical Architecture Synthesis

## Mission

Generate a concise, high-level summary (~800 words) from detailed architecture documents (`architecture-plan.md`). The synthesis provides architects and developers with a quick overview before diving into implementation details.

---

## Input

- **Source document**: `architecture-plan.md` or similar technical architecture document
- **Output path**: Specified by caller (typically `{output_directory}/architecture-synthesis.md`)

---

## Output Sections

Generate the following sections in order:

### 1. Header
```markdown
# Architecture Summary - [Feature Name]

**Module**: `[module-name]`
**Main Dependency**: `[primary-aos-module]`
```

### 2. Functional Objective
- 3 lines maximum
- Describe WHAT the feature does, not HOW
- Business-oriented language

### 3. Domain Model (Mermaid classDiagram)
- Include all entities (new and extended)
- Show relationships with cardinalities
- Use stereotypes to distinguish:
  - `<<AOS - module>>` for existing AOS entities
  - `<<New - Type>>` for new entities (e.g., Template, Instance)
- List key fields (no primitive types needed)

### 4. Main Flow (Mermaid sequenceDiagram)
- Show the PRIMARY use case only
- Participants: User, View, Controller, Service, Database
- Use technical names (class names, method names)
- Number steps with `autonumber`

### 5. AOS Integrations (Mermaid flowchart)
- Show service dependencies between modules
- Use `subgraph` to group by module
- Show call direction with arrows and labels

### 6. Module Structure (ASCII tree)
- **CRITICAL**: Extract EXACTLY from source document
- Do NOT simplify or modify the structure
- Include all directories and files as listed
- Preserve annotations (comments like `← Guice`, `← Extension`)

### 7. References
- Link to detailed architecture document

---

## Generation Rules

### CRITICAL - Source Fidelity
- Extract information EXACTLY from source document
- NEVER invent, simplify, or interpret structured data
- File trees, class names, field names must be reproduced verbatim

### Diagram Guidelines
- **classDiagram**: Sufficient detail without primitive types
- **sequenceDiagram**: Main flow only, technical language
- **flowchart**: Show service call chains between modules
- NO "Architecture Decisions" section unless choices are atypical

### Language
- Match source document language (typically English for technical docs)
- Technical terminology is appropriate

---

## Process

1. **Read** the source architecture document completely
2. **Identify** the key sections:
   - Domain model (entities, fields, relationships)
   - Service layer (services, controllers)
   - Module structure (directory tree)
   - Implementation phases (if present)
3. **Extract** information for each output section
4. **Generate** Mermaid diagrams from extracted data
5. **Verify** module structure matches source EXACTLY
6. **Write** synthesis to output path

---

## Example Invocation

```
Input: docs/development/architecture-plan.md
Output: docs/development/architecture-synthesis.md

The skill reads the architecture plan, extracts key information,
and generates a concise synthesis with UML diagrams.
```

---

## Validation Checklist

Before finalizing, verify:

- [ ] Functional objective is 3 lines or less
- [ ] classDiagram includes all entities with stereotypes
- [ ] sequenceDiagram shows main flow with technical names
- [ ] flowchart shows inter-module service calls
- [ ] Module structure EXACTLY matches source document
- [ ] No invented or simplified information
- [ ] References section points to source document

---

## Template Reference

See `reference/synthesis-template.md` for the expected output format.

---

## Integration

This skill is invoked by:
- **doc-synthesis-agent** agent (automatic detection)
- **develop.md** command (Phase 1.5)

Output is used for:
- Team onboarding
- Architecture review sessions
- Quick reference during implementation
