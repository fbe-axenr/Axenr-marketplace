---
description: Analyze code conformity and generate comprehensive report with bad practices, optimizations, performance issues, and security risks. Optionally generate fix specification that can be used to fix the issues.
skills:
  - axelor-java-style-validator
  - axelor-xml-validator
---

# Code Conformity Analysis Command

Analyze code quality and generate a detailed conformity report.

## Usage

```bash
/analyze-code <path> [--output <output-dir>] [--spec] [--issue <file>]
```

## Parameters

- **path** (required): File or directory to analyze
- **--output** (optional): Output directory path where reports will be saved (default: docs/analysis/)
- **--spec** (optional): Generate fix specification after analysis (default: disabled)
- **--issue** (optional): Path to bug/issue description file for targeted investigation

## Examples

```bash
# Analyze single file (outputs to docs/analysis/)
/analyze-code src/main/java/com/axelor/apps/crm/service/CustomerServiceImpl.java
# → docs/analysis/code-analysis-report.md

# Analyze directory with custom output directory
/analyze-code src/main/java/com/axelor/apps/crm/ --output reports/
# → reports/code-analysis-report.md

# Analyze directory to specific output directory
/analyze-code src/main/java/ --output analysis/
# → analysis/code-analysis-report.md

# Analyze and generate fix specification (docs/analysis/)
/analyze-code src/main/java/com/axelor/apps/crm/ --spec
# → docs/analysis/code-analysis-report.md
# → docs/analysis/fix-specification.md

# Analyze and generate spec in custom directory
/analyze-code src/main/java/com/axelor/apps/crm/ --spec --output reports/
# → reports/code-analysis-report.md
# → reports/fix-specification.md

# Full workflow: analyze and generate spec
/analyze-code src/main/java/com/axelor/apps/sale/ --spec --output reports/
# → reports/code-analysis-report.md
# → reports/fix-specification.md

# Investigate specific bug/issue
/analyze-code src/main/java/com/axelor/apps/sale/ --issue bug-description.txt
# → docs/analysis/code-analysis-report.md (with bug investigation section)

# Bug investigation with spec generation
/analyze-code src/main/java/com/axelor/apps/sale/ --issue bug-description.txt --spec --output reports/
# → reports/code-analysis-report.md (conformity + bug investigation)
# → reports/fix-specification.md
```

## What Gets Analyzed

### Single File
- Analyzes only the specified file
- File type detected automatically (Java, XML, etc.)
- Appropriate validators applied

### Directory
- Scans all relevant files recursively
- Filters by file type: `.java`, `.xml`, `.properties`
- Aggregates results across all files

## Report Structure

The generated markdown report includes:

1. **Bad Practices** (classified by criticality: CRITICAL, HIGH, MEDIUM, LOW)
2. **Optimization Opportunities**
3. **Performance Issues**
4. **Security Risks** (optional, in deep mode)

## Analysis Coverage

The analysis includes:
- Java style validation (emoji, French comments, naming)
- XML validation (XSD, semantic)
- Naming convention checks
- N+1 query detection
- SQL injection vulnerability scanning
- Performance anti-patterns
- Security risk assessment
- Code complexity analysis

---

## Task

Orchestrate code analysis and optionally generate fix specification.

**Step 1: Parse user input**

Extract from the command:
- `path`: The file or directory path (REQUIRED)
- `--output <directory>`: Output directory path (OPTIONAL, default: docs/analysis/)
- `--spec`: Flag to generate fix specification (OPTIONAL, default: false)
- `--issue <file>`: Path to bug/issue description file (OPTIONAL)

**Step 2: Set defaults and construct file paths**

```
If output not specified:
  output = "docs/analysis/"
Else:
  output = <user-provided-directory>
  Ensure output ends with / (add if missing)

Construct full file paths:
  analysis_report_path = output + "code-analysis-report.md"
  fix_spec_path = output + "fix-specification.md"
```

**Step 3: Validate inputs**

- Path must be provided (required parameter)
- If --issue is specified, verify the file exists and is readable
- If validation fails, show error message and usage example

**Step 4: Spawn the code analyzer agent**

Pass the following to the `code-analyzer` agent:
- **path**: The validated path to analyze
- **output**: The `analysis_report_path` from Step 2
- **issue_file**: The issue description file path (if --issue was provided, otherwise null)

The agent will handle:
- Path existence validation
- File/directory detection
- Bug/issue investigation (if issue_file provided)
- Full conformity analysis (always performed)
- Report generation to `analysis_report_path` with:
  - Bug Investigation section (if issue provided)
  - Full Conformity Analysis (always included)

**Step 5: Conditionally spawn fix spec generator**

If `--spec` flag is present:

1. Wait for the code analyzer agent to complete
2. Spawn the `spec-inspector` agent with:
   - **analysis_report_path**: The `analysis_report_path` from Step 2 (same path as the analysis report)
   - **output**: The `fix_spec_path` from Step 2 (in same directory as analysis report)

The fix-spec-generator agent will:
- Parse the analysis report at `analysis_report_path`
- Extract all issues
- Generate structured fix specification
- Write to `fix_spec_path` (same directory as analysis report)

**Step 6: Display completion summary**

Show user what was generated:
```
✓ Code analysis completed

Generated files:
  - Analysis report: <analysis_report_path>
  [if --spec was used]
  - Fix specification: <fix_spec_path>
```
