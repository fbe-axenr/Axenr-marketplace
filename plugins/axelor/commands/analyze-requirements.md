---
description: Complete requirement analysis workflow from initial requirement to EPICs/User Stories
argument-hint: <requirement|file-path> [output-directory]
context: fork
skills:
  - aos-entity-searcher
  - aos-field-comparator
  - aos-documentation-fetcher
---

# Analyze Requirements Command

Orchestrates the complete requirement analysis workflow through three specialized agents:
**business-analyst** → **requirements-refiner** → **agile-agent**

## Usage

```
/analyze-requirements [requirement] [output-directory]
```

**Parameters:**
- `[requirement]` (required): Text description OR path to PDF/DOCX document
- `[output-directory]` (optional): Output directory for artifacts (default: `docs`)

**Example:**
```
/analyze-requirements "CRM module with lead scoring and assignment" analysis/crm-2025
```

---

## Workflow Phases

### Phase 1: Business Analysis
**Agent**: business-analyst
**Output**: `{OUTPUT_DIR}/analysis-report.md`

Analyzes the requirement, identifies entities/features, detects ambiguities, generates clarifying questions.

**🔹 User Validation Gate**: Review analysis and answer clarifying questions (especially CRITICAL and HIGH priority).

### Phase 1.5: AOS Gap Analysis
**Agent**: aos-analyzer
**Output**: `{OUTPUT_DIR}/gap-analysis-report.md`

Identifies existing AOS components to reuse (REUSE/EXTEND/DEVELOP_NEW decisions).

**🔹 User Validation Gate**: Validate reuse decisions and AOS module dependencies.

### Phase 2: Requirements Refinement
**Agent**: requirements-refiner
**Output**: `{OUTPUT_DIR}/detailed-specifications.md`

Transforms analysis + answers into detailed, implementation-ready specifications through conversational refinement.

**🔹 User Validation Gate**: Review and approve detailed specifications.

### Phase 2.5: Functional Specification Synthesis
**Agent**: doc-synthesis-agent (skill: functional-spec-synthesis)
**Output**: `{OUTPUT_DIR}/functional-synthesis.md`

Generates executive summary of functional specifications for stakeholder review. Produces a concise (~800 words) overview with workflow diagrams, business constraints, and rules.

**Note**: This phase runs automatically after Phase 2 approval. No user validation gate required.

### Phase 3: EPIC & User Story Generation
**Agent**: agile-agent
**Output**: `{OUTPUT_DIR}/epic-us-breakdown.textile`

Decomposes specifications into actionable EPICs and User Stories (Redmine-compatible format).

**🔹 User Validation Gate**: Review EPIC structure and User Story breakdown.

---

## State Management

The workflow maintains state across phases:

- **Artifacts**: All intermediate documents saved in the specified output directory (default: `docs/`)
- **Context**: Each agent receives file paths only (not full content) to minimize context pollution
- **Resume**: Can pause and resume at any validation gate

---

## Context Optimization (CRITICAL)

### Problem Addressed

Multi-phase workflows accumulate context in the orchestrating conversation, consuming tokens unnecessarily. Each subagent has isolated context, but their **return values** pollute the parent context.

### Solution: Minimal Return Format

Each agent MUST return ONLY a minimal status report to the orchestrator. The detailed output is written to files.

### Agent Return Format Standard

When an agent completes its phase, it MUST return this exact format (and NOTHING more):

```
## Phase Complete: [Phase Name]

**Status**: ✅ SUCCESS | ❌ FAILURE
**Output File**: `{output_directory}/[filename]`
**Summary** (3 lines max):
- [Key insight 1]
- [Key insight 2]
- [Key insight 3, if needed]

**Next Phase Input**: `{output_directory}/[filename]`
```

### What Agents MUST NOT Return

- ❌ Full content of generated reports
- ❌ Detailed analysis text
- ❌ Large code blocks or XML
- ❌ Repeated information from input documents
- ❌ Verbose explanations

### Impact

- **Before**: Each phase adds ~20-50KB to parent context
- **After**: Each phase adds ~500 bytes to parent context
- **Savings**: ~90% token reduction on orchestrator context

### Phase-Specific Instructions

**Phase 1 (business-analyst)** returns:
```
## Phase Complete: Business Analysis

**Status**: ✅ SUCCESS
**Output File**: `{output_directory}/analysis-report.md`
**Summary**:
- Identified [N] business entities
- Generated [M] clarifying questions ([X] CRITICAL, [Y] HIGH)
- Recognized [Z] Axelor patterns

**Next Phase Input**: `{output_directory}/analysis-report.md`
```

**Phase 1.5 (aos-analyzer)** returns:
```
## Phase Complete: AOS Gap Analysis

**Status**: ✅ SUCCESS
**Output File**: `{output_directory}/gap-analysis-report.md`
**Summary**:
- Analyzed [N] entities: [X] REUSE, [Y] EXTEND, [Z] DEVELOP_NEW
- Estimated effort savings: [P]%
- Required AOS modules: [list]

**Next Phase Input**: `{output_directory}/gap-analysis-report.md`
```

**Phase 2 (requirements-refiner)** returns:
```
## Phase Complete: Requirements Refinement

**Status**: ✅ SUCCESS
**Output File**: `{output_directory}/detailed-specifications.md`
**Summary**:
- Refined [N] entities with [M] total fields
- Defined [X] features with complete workflows
- Validated consistency: PASS

**Next Phase Input**: `{output_directory}/detailed-specifications.md`
```

**Phase 2.5 (doc-synthesis-agent)** returns:
```
## Phase Complete: Functional Specification Synthesis

**Status**: ✅ SUCCESS
**Output File**: `{output_directory}/functional-synthesis.md`
**Summary**:
- Generated [N] workflow diagrams
- Extracted [M] business rules and [X] constraints
- Document size: ~800 words

**Synthesis File**: `{output_directory}/functional-synthesis.md`
```

**Phase 3 (agile-agent)** returns:
```
## Phase Complete: EPIC/US Generation

**Status**: ✅ SUCCESS
**Output Directory**: `{output_directory}/epic-us-breakdown/`
**Summary**:
- Generated [N] EPICs with [M] User Stories
- Total estimated effort: [X] days
- Ready for Redmine import

**Deliverables**: INDEX.textile + [N] EPIC directories
```

---

## Deliverables

| File | Content | Ready for |
|------|---------|-----------|
| `analysis-report.md` | Business analysis with answered questions | Refinement |
| `gap-analysis-report.md` | AOS reuse decisions (30-50% effort savings) | Architecture |
| `detailed-specifications.md` | Complete functional specifications | Implementation |
| `functional-synthesis.md` | Executive summary with workflows and rules (~800 words) | Stakeholder review |
| `epic-us-breakdown.textile` | EPICs, User Stories, estimations | Redmine import |

---

## Command Arguments

**USER ARGUMENTS**: $1 [requirement input] $2 [output-directory]

### Argument Parsing

```
$1 (required): Text description OR path to PDF/DOCX
$2 (optional): Output directory (default: "docs")
```

**Validation:**
- Reject path traversal patterns (`../../../`)
- Convert to relative path from workspace root

### Passing Output Directory Through Phases

All agents receive `output_directory` parameter:
- Phase 1: Generates `{output_directory}/analysis-report.md`
- Phase 1.5: Generates `{output_directory}/gap-analysis-report.md`
- Phase 2: Generates `{output_directory}/detailed-specifications.md`
- Phase 3: Generates `{output_directory}/epic-us-breakdown.textile`

### Step 0: Detect AOP/AOS/Addons Paths

Before delegating to agents, detect the paths to Axelor repositories.

> **Note:** The bash script below is for DOCUMENTATION REFERENCE ONLY.
> Do NOT execute this script directly - the paths are automatically detected
> by the SessionStart hook and injected as environment variables.

```bash
# REFERENCE ONLY - This script shows how path detection works internally
# The actual detection is performed by the SessionStart hook

# Find plugin installation path
PLUGIN_PATH=$(find /home -type d -name "axelor" -path "*/plugins/*" 2>/dev/null | head -1)

# Detect Axelor repositories (AOP, AOS, Addons) - no interactive prompt
axelor_repos_json=$(python3 ${PLUGIN_PATH}/scripts/detect_axelor_repos.py --no-prompt)

# Parse JSON result
detection_method=$(echo "$axelor_repos_json" | jq -r '.detection_method')

# If not found, ask user for path
if [ "$detection_method" = "not_found" ]; then
    echo "⚠️  Les dossiers AOP/AOS/Addons ne sont pas trouvés dans .axelor/"
    echo "Veuillez exécuter /axelor:setup ou fournir le chemin vers un répertoire contenant:"
    echo "  - aop/"
    echo "  - aos/"
    echo "  - axelor-utils/, axelor-message/, axelor-studio/ (optionnel)"
    echo ""
    read -p "Chemin du repo: " user_repo_path

    # Retry with user-provided path
    axelor_repos_json=$(python3 ${PLUGIN_PATH}/scripts/detect_axelor_repos.py "$user_repo_path")
    detection_method=$(echo "$axelor_repos_json" | jq -r '.detection_method')
fi

# Parse paths from JSON
axelor_repo=$(echo "$axelor_repos_json" | jq -r '.axelor_repo')
aop_path=$(echo "$axelor_repos_json" | jq -r '.paths.aop')
aos_path=$(echo "$axelor_repos_json" | jq -r '.paths.aos')
addons_message_path=$(echo "$axelor_repos_json" | jq -r '.paths.addons.message')
addons_studio_path=$(echo "$axelor_repos_json" | jq -r '.paths.addons.studio')
addons_utils_path=$(echo "$axelor_repos_json" | jq -r '.paths.addons.utils')

# Verify detection succeeded
if [ "$detection_method" = "error" ]; then
    error_msg=$(echo "$axelor_repos_json" | jq -r '.error')
    echo "❌ Failed to detect Axelor repositories: $error_msg"
    exit 1
fi

# Log detection
echo "✅ Axelor repos detected via: $detection_method"
echo "   - Repo: $axelor_repo"
echo "   - AOP: $aop_path"
echo "   - AOS: $aos_path"
```

### Delegation

**Delegate immediately to business-analyst agent** with:
```
Context:
- Requirement input: $1
- Output directory: {output_directory}
- Expected output: {output_directory}/analysis-report.md

Axelor Repositories (from Step 0):
- axelor_repo: {axelor_repo}
- detection_method: {detection_method}
- aop_path: {aop_path}
- aos_path: {aos_path}
- addons_message_path: {addons_message_path}
- addons_studio_path: {addons_studio_path}
- addons_utils_path: {addons_utils_path}

Instructions:
"Analyze the provided requirement and generate your analysis report at {output_directory}/analysis-report.md.
Create the directory if it doesn't exist.

When searching for AOS entities or AOP base entities, use the provided paths:
- AOS entities: {aos_path}/axelor-*/src/main/resources/domains/
- AOP entities: {aop_path}/axelor-core/src/main/resources/domains/"
```

---

## More Information

For detailed examples, tips, troubleshooting, and integration guidance:
**@docs/workflows/analyze-requirements-guide.md**

## See Also

- @agents/business-analyst.md - Phase 1 agent
- @agents/requirements-refiner.md - Phase 2 agent
- @agents/agile-agent.md - Phase 3 agent
- @commands/develop-complete-feature.md - Continue with full development workflow
