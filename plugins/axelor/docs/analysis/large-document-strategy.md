# Large Document Handling Strategy

This document describes strategies for analyzing large requirement documents (PDF, DOCX, or text documents over 50-150 pages) such as cahiers des charges, functional specifications, or RFPs.

## Supported Formats

Claude Code's Read tool natively supports:
- **PDF files**: Directly readable with text and visual content extraction
- **Markdown/Text files**: Directly readable
- **DOCX files**: Readable via Read tool
- **Jupyter notebooks**: For technical specifications

All formats support files up to 150+ pages.

---

## Challenge: Analyzing Large Documents

### Context Window Limitations

Large documents present challenges:
- **Volume**: 100-150 pages can contain 50,000-100,000+ words
- **Context**: Need to maintain understanding across sections
- **Coherence**: Must identify cross-references and dependencies
- **Synthesis**: Must extract key information without getting lost in details

### Strategy: Progressive Analysis

The key is **progressive, structured analysis** rather than attempting to read everything at once.

---

## Step 1: Initial Overview (10-15 minutes)

### Goal
Get a high-level understanding of document structure and scope.

### Process

**1.1 Read Document Metadata**
- Title, version, date, authors
- Identifies document type and context

**1.2 Read Table of Contents**
```markdown
If document has table of contents:
- Read TOC completely
- Identify main sections and subsections
- Note section page numbers for targeted reading later
```

**1.3 Read Introduction/Executive Summary**
- Typically first 5-10 pages
- Understand: project objectives, scope, stakeholders, constraints
- Capture: business goals, success criteria

**1.4 Read Conclusion/Summary**
- Typically last 3-5 pages
- Understand: expected outcomes, next steps, key decisions

**1.5 Scan Section Headings**
```markdown
If no TOC available:
- Skim through document looking for main headings (H1, H2)
- Build mental map of document structure
```

### Output of Step 1

Create initial understanding document:

```markdown
# Initial Document Overview

**Document**: [Title]
**Type**: [Cahier des charges / Functional specs / RFP / etc.]
**Scope**: [Summary in 2-3 sentences]

## Main Sections Identified
1. [Section name] (pages X-Y) - [Brief description]
2. [Section name] (pages X-Y) - [Brief description]
...

## Business Objectives
- [Objective 1]
- [Objective 2]

## Key Stakeholders
- [Role 1]: [Name/team]
- [Role 2]: [Name/team]

## Constraints Noted
- [Constraint 1]
- [Constraint 2]
```

---

## Step 2: Section-by-Section Deep Analysis (30-60 minutes)

### Goal
Analyze each logical section of the document thoroughly.

### Process

**2.1 Prioritize Sections**

Read sections in this order:
1. **Functional requirements** (highest priority)
2. **Business entities/data model**
3. **User roles and permissions**
4. **Business processes/workflows**
5. **UI/UX requirements**
6. **Integration requirements**
7. **Technical constraints**
8. **Non-functional requirements** (performance, security)

**2.2 For Each Section**

```markdown
### Read Section Completely
- Use Read tool with offset/limit if section is very long
- Read all paragraphs, not just headings

### Extract Key Information
- **Entities mentioned**: What business objects?
- **Features described**: What operations/actions?
- **Rules specified**: What validations/constraints?
- **Relationships**: How entities connect?
- **Ambiguities**: What is unclear or contradictory?

### Document Findings
Create section summary:
- Clear requirements (no questions needed)
- Ambiguous requirements (need clarification)
- Missing information (need to ask)
- Cross-references to other sections (to verify later)
```

**2.3 Progressive Synthesis**

After each section, update the running analysis:
- Add new entities to entity list
- Add new features to feature list
- Add new questions to question list
- Note dependencies on other sections

### Handling Very Long Sections

If a single section spans 20+ pages:

**Break into sub-sections**:
```markdown
Read section 3.1 (pages 20-30)
→ Document findings
→ Read section 3.2 (pages 31-40)
→ Document findings
→ Synthesize section 3 overall
```

**Focus on structured content**:
- Tables (often contain entity field definitions)
- Lists (often contain feature requirements)
- Diagrams (business process flows, data models)
- Examples/scenarios (use case descriptions)

---

## Step 3: Cross-Reference Validation (15-20 minutes)

### Goal
Ensure consistency across document sections.

### Process

**3.1 Entity Consistency Check**

For each business entity identified:
```markdown
- Is it defined consistently across sections?
- Are field names/types consistent?
- Are relationships described the same way?
- Any contradictions between sections?
```

**3.2 Feature Consistency Check**

For each feature identified:
```markdown
- Is workflow described consistently?
- Are actors/permissions consistent?
- Any conflicting requirements?
```

**3.3 Business Rules Check**

For each business rule/validation:
```markdown
- Is rule stated clearly once or multiple times?
- Any contradictions in rule definitions?
- Are exceptions documented?
```

**3.4 Document Contradictions**

If contradictions found:
```markdown
### Contradiction: [Topic]

**Section X (page Y)** states:
"[Quote from document]"

**Section A (page B)** states:
"[Quote from document]"

**Question for clarification**:
Which requirement is correct, or should both be supported?
```

---

## Step 4: Gap Analysis (15-20 minutes)

### Goal
Identify missing information essential for Axelor implementation.

### Process

**4.1 Entity Completeness**

For each entity, verify:
- [ ] Entity name and business role defined
- [ ] Fields listed with types
- [ ] Required/optional fields specified
- [ ] Unique constraints specified
- [ ] Relationships to other entities defined
- [ ] Lifecycle/status workflow described (if applicable)

**4.2 Feature Completeness**

For each feature, verify:
- [ ] Feature trigger defined (who, where, when)
- [ ] Pre-conditions specified
- [ ] Process steps described
- [ ] Post-conditions/expected results specified
- [ ] Validations listed
- [ ] Error handling described
- [ ] Success/error messages defined

**4.3 UI Completeness**

For each entity, verify:
- [ ] Form view fields specified
- [ ] Grid view columns specified
- [ ] Filters specified
- [ ] Action buttons listed

**4.4 Cross-Cutting Completeness**

Verify:
- [ ] User roles defined
- [ ] Permissions matrix specified
- [ ] Internationalization languages specified
- [ ] Import/export requirements defined
- [ ] Integration points specified

**4.5 Document Gaps**

Create structured gap list:
```markdown
## Missing Information

### Entity: Customer
- Field data types not specified
- Relationship to Address not described
- Status workflow not defined

### Feature: Order Validation
- Pre-conditions not clear
- Error handling strategy not specified
```

---

## Step 5: Structured Question Generation (15-20 minutes)

### Goal
Create targeted, contextualized questions for clarification.

### Process

**5.1 Use Question Templates**

Consult @docs/analysis/question-templates.md for appropriate question formats.

**5.2 Group Questions Logically**

Organize questions by:
- Business entity
- Feature/workflow
- UI requirements
- Cross-cutting concerns

**5.3 Prioritize Questions**

Mark questions as:
- **CRITICAL**: Must be answered before proceeding (blocks architecture)
- **HIGH**: Important for complete specification
- **MEDIUM**: Clarifications that improve quality
- **LOW**: Nice-to-have details

**5.4 Provide Context**

For each question:
```markdown
### [Entity/Feature Name]

**Question**: [Specific question]?

**Context**: [Why this information is needed for Axelor]

**Suggested options**: [Propose options based on Axelor patterns]

**Priority**: [CRITICAL / HIGH / MEDIUM / LOW]

**Reference**: [Document section/page where ambiguity found]
```

---

## Step 6: Analysis Report Generation (15-20 minutes)

### Goal
Produce comprehensive analysis report using template.

### Process

Use @templates/analysis-report-template.md to structure the final report.

Include:
1. **Document Overview**: Summary of what was analyzed
2. **Business Understanding**: Objectives, scope, stakeholders
3. **Entities Identified**: Complete list with brief descriptions
4. **Features Identified**: Complete list with brief descriptions
5. **Clear Requirements**: What is well-defined
6. **Ambiguities**: What needs clarification
7. **Structured Questions**: Grouped and prioritized
8. **Initial Recommendations**: Applicable Axelor patterns (if relevant)
9. **Next Steps**: What happens after questions are answered

---

## Practical Tips

### Tip 1: Use Bookmarks and References

When reading large documents:
```markdown
- Note page numbers for important definitions
- Reference specific sections in your analysis
- Create index of where each entity/feature is discussed
```

This allows you to:
- Quickly return to relevant sections
- Provide precise references in questions
- Verify information across sections

### Tip 2: Use Incremental Reading

Don't try to read entire document in one pass:
```markdown
Session 1: Overview + Section 1-2 (60 min)
→ Synthesize findings
→ Break

Session 2: Section 3-4 (60 min)
→ Synthesize findings
→ Break

Session 3: Section 5-6 + Cross-reference check (60 min)
→ Complete analysis
```

### Tip 3: Focus on Structured Content

When document is very dense:
```markdown
Prioritize reading:
✅ Tables (often contain field definitions)
✅ Lists and bullet points (often contain requirements)
✅ Diagrams and flowcharts (often show relationships/workflows)
✅ Examples and use cases (often clarify intent)

Skim more quickly:
⚡ Long prose paragraphs (extract key points)
⚡ Background/context sections (understand but don't memorize)
⚡ Legal/contractual text (note constraints but don't analyze deeply)
```

### Tip 4: Build Progressive Understanding

Don't expect to understand everything on first read:
```markdown
First pass: What is this about? (high-level)
Second pass: What are the components? (entities, features)
Third pass: How do they relate? (relationships, workflows)
Fourth pass: What is missing? (gaps, ambiguities)
```

### Tip 5: Use Pattern Recognition

Leverage Axelor pattern knowledge:
```markdown
When you see:
- "List of X" → Probably an entity with grid view
- "User can create/edit X" → CRUD operations
- "X has status Y" → Workflow with state transitions
- "X belongs to Y" → Many-to-one relationship
- "X contains many Y" → One-to-many relationship

This accelerates understanding and helps identify gaps.
```

---

## Example: Analyzing a 120-Page Cahier des Charges

### Timeline

| Step | Activity | Duration | Output |
|------|----------|----------|--------|
| 1 | Initial overview (TOC, intro, conclusion) | 15 min | Document structure map |
| 2a | Functional requirements (pages 10-40) | 30 min | Entities + features list |
| 2b | Data model section (pages 41-70) | 30 min | Entity definitions |
| 2c | Business processes (pages 71-95) | 25 min | Workflow descriptions |
| 2d | UI requirements (pages 96-110) | 15 min | View requirements |
| 3 | Cross-reference validation | 15 min | Consistency check |
| 4 | Gap analysis | 20 min | Missing information list |
| 5 | Question generation | 20 min | Structured questions |
| 6 | Report generation | 15 min | Complete analysis report |
| **Total** | | **~3 hours** | Ready for refinement phase |

### Sample Workflow

```markdown
## Session 1: Initial Analysis (60 min)

1. Read pages 1-5 (introduction) → Understanding: CRM system for lead management
2. Read pages 6-7 (table of contents) → Structure: 8 main sections
3. Read pages 115-120 (conclusion) → Expected outcome: Integrated lead-to-opportunity workflow
4. Read pages 10-40 (functional requirements) → Identified 5 entities (Lead, Opportunity, Company, Contact, Activity)
5. First synthesis → Created initial entity list and feature list

## Session 2: Deep Dive (90 min)

6. Read pages 41-70 (data model) → Detailed field definitions for each entity
7. Read pages 71-95 (workflows) → Status transitions, validation rules
8. Read pages 96-110 (UI requirements) → Form layouts, grid columns
9. Second synthesis → Updated entity definitions, identified 12 features

## Session 3: Analysis Completion (60 min)

10. Cross-reference check → Found 3 contradictions between sections
11. Gap analysis → Identified 8 missing details (field types, permission rules)
12. Question generation → Created 15 prioritized questions grouped by entity
13. Report generation → Complete analysis report with questions

## Output

- **20-page analysis report** covering all requirements
- **15 clarifying questions** ready for stakeholder
- **5 entities** fully documented with known details and gaps
- **12 features** described with workflows and ambiguities noted
- **Ready for refinement** phase after questions answered
```

---

## Working with Different Document Types

### Cahier des Charges (Detailed Requirements)
- Usually **well-structured** with numbered sections
- Often includes **field-level details**
- May have **diagrams and mockups**
- Strategy: Follow linear section-by-section approach

### Functional Specifications
- Usually **feature-oriented** rather than data-oriented
- Often includes **use cases and scenarios**
- May lack detailed data model
- Strategy: Extract entities from features, ask data model questions

### RFP (Request for Proposal)
- Usually **outcome-focused** rather than detail-focused
- Often includes **business objectives and constraints**
- May lack implementation details
- Strategy: Extract requirements between the lines, ask many clarification questions

### Meeting Transcripts / Notes
- Usually **unstructured** with mixed topics
- Often includes **contradictory or incomplete information**
- May have **implicit assumptions**
- Strategy: Heavy gap analysis, group scattered information by topic

---

## Success Criteria

A successful large document analysis produces:

✅ **Complete entity list** with known fields and relationships
✅ **Complete feature list** with workflows and business rules
✅ **Structured clarifying questions** grouped logically and prioritized
✅ **Cross-reference validation** ensuring document consistency
✅ **Gap identification** highlighting missing information
✅ **Axelor pattern suggestions** where applicable
✅ **Ready for refinement** phase with clear next steps

---

## See Also

- @docs/analysis/axelor-patterns-for-analysis.md - Pattern recognition guide
- @docs/analysis/question-templates.md - Question format reference
- @templates/analysis-report-template.md - Output format
