# Agent-Workflow Integration Guide

This document explains how the specialized Axelor agents integrate with the `develop-complete-feature` workflow command for seamless orchestration.

## Overview

The Axelor Dev Accelerator plugin uses a **command-driven orchestration** model:

- **Workflow Command**: `develop-complete-feature.md` orchestrates the entire 19-step process
- **Specialized Agents**: 10 domain-expert agents handle specific tasks
- **State Management**: `.axelor-workflow-state.md` tracks progress and context
- **Skills**: Validation and helper skills provide automation

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│         develop-complete-feature command                │
│              (Workflow Orchestrator)                     │
│                                                          │
│  - Manages 19-step workflow                             │
│  - Invokes sub-agents with explicit context             │
│  - Handles user validation gates                        │
│  - Manages state file                                   │
│  - Creates checkpoint commits                           │
│  - Coordinates error handling                           │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ Delegates to (via Task tool)
                  │
     ┌────────────┴────────────┐
     │                         │
     ▼                         ▼
┌─────────────┐           ┌──────────────┐
│Sub-Agents   │           │ Skills       │
│             │           │              │
│ • business  │           │ • xsd-valid  │
│ • refiner   │◄──────────┤ • naming     │
│ • architect │  Uses     │ • semantic   │
│ • domain-   │           │ • view-valid │
│   generator │           │ • test-help  │
│ • view-gen  │           │ • code-fixer │
│ • java-gen  │           └──────────────┘
│ • reviewer  │
│ • validator │
│ • git-mgr   │
└─────────────┘
```

## Orchestration Model

### Command-Driven (Not Agent-Driven)

**Key Principle**: The workflow command orchestrates; agents execute.

- Agents **do not** call each other directly
- Agents **do not** manage workflow state
- Agents **do not** know about the 19-step workflow
- Agents **focus only** on their specialized task

**The command does**:
- Invoke agents in the correct sequence
- Provide context from previous steps
- Handle transitions between agents
- Manage state tracking
- Handle user validations
- Coordinate error recovery

## Agent Invocation Pattern

### How Agents Are Invoked

**From workflow command:**
```markdown
## Step 2: Requirement Analysis

**Delegate to sub-agent**: `business-analyst`

**Instructions for sub-agent:**
```
Analyze the following requirement expression and provide:
1. Business objectives identification
2. Business entities identification
3. Main features list
4. Clear elements vs ambiguities
5. Structured clarifying questions

User requirement: [REQUIREMENT FROM USER]

Context from workflow:
- Project type: [standalone/webapp]
- Workflow ID: [id from state file]
- Output directory: [output_directory parameter, default: "docs"]
- Expected output location: {output_directory}/analysis-report.md
```

**Sub-agent will use:**
- Read tool for existing documentation
- Grep for similar patterns in codebase
- WebFetch for Axelor documentation if needed

**Expected Output:**
- {output_directory}/analysis-report.md with comprehensive analysis
- List of clarifying questions for user

**Note**: The `output_directory` parameter is provided by the `/analyze-requirements` command (default: "docs"). All analysis artifacts will be generated in this directory.
\```
```

### Context Handoff

Each agent receives:

1. **Task Description**: What to do
2. **Input Context**: What to read/use
3. **Expected Output**: What to produce
4. **Workflow Context** (optional): Workflow ID, project type
5. **Tool Access**: Which tools the agent can use

**Example - Step 6 to Step 7:**
```markdown
## Step 7: Domain XML Generation

**Delegate to sub-agent**: `domain-agent`

**Context handoff:**
```
Generate production-ready Axelor XML domain definitions.

Input context:
- File: docs/architecture-design.md (entity definitions section)
- AOP version: [from gradle.properties]
- Existing domains: [list existing domain files if any]

Process:
1. Parse architecture specification
2. Consult documentation (@docs/domains/)
3. Generate XML domain files in src/main/resources/domains/
4. Validate with skills (xsd, naming, semantic)
5. Report validation results

DO NOT execute generateCode yet - validation only.
```
\```
```

## State Management

### Who Manages State?

**The workflow command manages** `.axelor-workflow-state.md`:

- Creates state file at workflow start (Step 1)
- Updates state after each step completion
- Records user validations and feedback
- Tracks artifacts generated
- Logs errors and resolutions
- Updates status and timestamps

**Agents do NOT manage** the state file:

- Agents focus on their task
- Agents produce outputs (files, reports)
- Command reads agent outputs and updates state

### State Usage by Agents (Optional)

Agents CAN read state for context:

```markdown
## Optional: Read Workflow Context

If .axelor-workflow-state.md exists:
1. Read Project Context section
2. Check what artifacts already exist
3. Review previous user feedback
4. Consider previous iterations

This provides additional context but is not required.
```

**When useful**:
- Understanding previous user feedback
- Avoiding regeneration of existing artifacts
- Maintaining consistency with project setup

**When NOT needed**:
- Command already provides necessary context in prompt
- Agent task is self-contained

## Agent Roles in Workflow

### Analysis Phase (Steps 2-4)

#### business-analyst (Step 2)
- **Input**: User requirement expression
- **Task**: Analyze requirement, identify ambiguities, ask questions
- **Output**: `docs/analysis-report.md`
- **Next**: User Q&A, then requirements-refiner

#### requirements-refiner (Step 3)
- **Input**: Analysis report + user answers
- **Task**: Refine detailed specification through guided conversation
- **Output**: `docs/specification.md`
- **Next**: User validation (Step 4)

### Design Phase (Steps 5-6)

#### agile-agent (Step 5)
- **Input**: Specification document
- **Task**: Generate EPIC and User Stories for project management
- **Output**: `docs/epic-user-stories.md` (Textile or Markdown)
- **Next**: architect

#### architect (Step 6)
- **Input**: Specification + EPIC/US
- **Task**: Design complete technical architecture
- **Output**: `docs/architecture-design.md`
- **Next**: domain-agent

### Implementation Phase - Data Models (Steps 7-8)

#### domain-agent (Step 7)
- **Input**: Architecture design (entity definitions)
- **Task**: Generate XML domain files with validation
- **Output**: `src/main/resources/domains/*.xml`
- **Validation**: Uses axelor-xml-validator, axelor-naming-checker, axelor-semantic-validator skills
- **Next**: view-agent

#### view-agent (Step 8)
- **Input**: Architecture design (view requirements) + generated domains
- **Task**: Generate XML view files (forms, grids, menus)
- **Output**: `src/main/resources/views/*.xml`
- **Validation**: Uses axelor-view-validator skill
- **Next**: Build execution, then user validation

### Implementation Phase - Java (Step 12)

#### java-agent (Step 12)
- **Input**: Architecture design (service layer) + generated domains
- **Task**: Generate Java repositories, services, controllers
- **Output**: `src/main/java/**/*.java`
- **Next**: code-reviewer

#### code-reviewer (Step 12b)
- **Input**: Generated Java code
- **Task**: Review code quality, architecture compliance, best practices
- **Output**: `docs/code-review-report.md`
- **Next**: Present to user, then build

### Testing Phase (Steps 14-15)

#### test-agent (via skill)
- **Input**: Service classes + business rules
- **Task**: Generate unit and integration tests
- **Output**: `src/test/java/**/*Test.java`
- **Next**: Execute tests

### Finalization Phase (Steps 11, 13, 19)

#### git-agent (Steps 11, 13, 19)
- **Input**: Modified/generated files + context
- **Task**: Create conventional commits, optionally push and create PR
- **Output**: Git commits, optional remote push
- **Usage**: Called at checkpoint moments

#### functional-validator (Step 19)
- **Input**: Complete implementation + specification
- **Task**: Validate all requirements met, create traceability matrix
- **Output**: `docs/functional-validation-report.md`
- **Next**: Final user approval

## Agent Communication

### No Direct Communication

Agents do **NOT** communicate with each other:

❌ **Wrong**: Agent A calls Agent B directly
❌ **Wrong**: Agent A writes message for Agent B
❌ **Wrong**: Agent A manages handoff to Agent B

✅ **Right**: Command invokes Agent A, then Agent B
✅ **Right**: Command provides Agent B with Agent A's output
✅ **Right**: Command coordinates the handoff

### Indirect Communication via Artifacts

Agents communicate through **file artifacts**:

**Example Chain:**
```
business-analyst
  ↓ produces
docs/analysis-report.md
  ↓ read by
requirements-refiner
  ↓ produces
docs/specification.md
  ↓ read by
architect
  ↓ produces
docs/architecture-design.md
  ↓ read by
domain-agent
```

**The command orchestrates** this chain by:
1. Invoking business-analyst
2. Waiting for analysis-report.md
3. Invoking requirements-refiner with analysis-report.md as input
4. Waiting for specification.md
5. Invoking architect with specification.md as input
6. etc.

## Error Handling

### Agent Error Reporting

When an agent encounters an error:

**Agent responsibility**:
- Report the error clearly
- Explain what went wrong
- Suggest recovery options if possible
- Provide diagnostic information

**Command responsibility**:
- Catch the error
- Update state file with error details
- Present recovery options to user
- Coordinate retry or rollback

### Error Recovery Pattern

```markdown
## Error in Step 7 (Domain Generation)

**Agent (domain-agent) reports**:
```
❌ XSD Validation Failed in domains/Customer.xml:45
Error: Invalid element 'text' (use 'string' with large="true")

Suggested fix: Change <text name="notes"/> to <string name="notes" large="true"/>
```

**Command handles recovery**:
```markdown
Recovery options:
1. Auto-fix with axelor-code-fixer skill (if applicable)
2. Manual correction required
3. Rollback domain generation

Choose action: [1/2/3]
```

User chooses option, command executes recovery, updates state.
\```
```

## Validation Pattern

### Skills for Validation

Agents use specialized skills for validation:

**domain-agent** uses:
- `axelor-xml-validator`: XSD schema validation
- `axelor-naming-checker`: Naming conventions
- `axelor-semantic-validator`: Cross-entity semantic checks

**view-agent** uses:
- `axelor-view-validator`: View syntax and references

**Pattern**:
```markdown
1. Agent generates files
2. Agent invokes validation skills
3. Agent reports validation results
4. If errors: Agent suggests fixes
5. Command coordinates retry if needed
```

## User Interaction

### Validation Gates

The command manages 4 user validation gates:

**Gate 1 (Step 4)**: Specification approval
**Gate 2 (Step 8)**: Deployment testing
**Gate 3 (Step 12)**: E2E functional testing
**Gate 4 (Step 19)**: Final approval & push

**Agent role**: None - agents don't interact with user for approvals
**Command role**: Present validation gate, collect user feedback, proceed or retry

### User Feedback Loop

```
Command invokes Agent
  ↓
Agent produces output
  ↓
Command presents to user (validation gate)
  ↓
User provides feedback
  ↓
If approved: Continue to next step
If rejected: Command invokes Agent again with corrections
```

**Iteration tracking** in state file:
```markdown
## Phase 2 Iterations (Steps 7-9)
- Iteration 1: User feedback: "Missing email field in Customer"
  - Changes: Added email field
  - Result: Rejected (still missing phone)
- Iteration 2: User feedback: "Now looks good"
  - Changes: Added phone field
  - Result: Approved ✓
```

## Best Practices for Agents

### DO

✅ **Focus on your specialized task**
- Business analyst: Analyze requirements
- Domain generator: Generate domains
- Don't try to do multiple steps

✅ **Produce clear outputs**
- Write to specified output files
- Use clear structure
- Include all necessary information

✅ **Use provided tools**
- Read for documentation
- Grep for code search
- Write/Edit for file generation
- Bash for builds and validation

✅ **Invoke skills when appropriate**
- Use validation skills
- Use helper skills
- Don't reinvent validation logic

✅ **Report errors clearly**
- Explain what went wrong
- Provide diagnostic info
- Suggest recovery if possible

✅ **Read workflow context (optional)**
- Check .axelor-workflow-state.md if helpful
- Review previous feedback
- Maintain consistency

### DON'T

❌ **Don't manage workflow**
- Don't update state file
- Don't invoke other agents
- Don't manage user validations

❌ **Don't assume workflow context**
- Command provides all necessary context
- Don't require workflow knowledge to function
- Work independently as a specialized tool

❌ **Don't create circular dependencies**
- Don't reference future steps
- Don't wait for other agents
- Complete your task independently

## Workflow Resumption

### When Workflow Interrupted

**Command detects interruption**:
1. Reads .axelor-workflow-state.md
2. Identifies last completed step
3. Checks what artifacts exist
4. Presents resume options to user

**Agents don't need to know**:
- Workflow was interrupted
- Resuming from Step X
- Previous session details

**Agents just execute** their task with provided context.

### Example Resumption

```markdown
User resumes with: claude --resume

Command reads state:
- Last completed: Step 6 (Architecture design)
- Artifacts exist: analysis-report.md, specification.md, architecture-design.md
- Next step: Step 7 (Domain generation)

Command resumes:
- Picks up at Step 7
- Invokes domain-agent with architecture-design.md
- Agent doesn't know workflow was interrupted
- Agent executes normally
```

## Summary

### Orchestration Philosophy

**Command is the brain**:
- Knows the 19-step workflow
- Manages state and progress
- Handles user interactions
- Coordinates agents

**Agents are the hands**:
- Execute specialized tasks
- Produce quality outputs
- Validate their work
- Report results

### Integration is Seamless

- Agents don't need workflow knowledge
- Command provides all context
- State management is centralized
- Error handling is coordinated
- User interaction is managed

### Benefits

✅ **Maintainability**: Agents stay simple and focused
✅ **Flexibility**: Easy to add/modify agents
✅ **Testability**: Agents can be tested independently
✅ **Reliability**: Centralized error handling and state
✅ **Clarity**: Clear separation of concerns

---

**Document Version**: 1.0
**Last Updated**: 2025-10-29
**Maintained By**: Axelor Development Accelerator Plugin
