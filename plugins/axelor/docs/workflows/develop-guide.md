# /develop Command Guide

Complete guide for the `/develop` command including examples, integration patterns, and usage recommendations.

## When to Use This Command

### Use `/develop` when:

- You have detailed specifications ready
- Starting implementation from EPIC/User Stories
- Need checkpoint commits for rollback capability
- Want modular workflow with resume capability
- Extending existing architecture with new features
- Implementing bug fixes requiring code generation

### Don't use when:

- You only need requirements analysis (use `/analyze-requirements`)
- You need full 19-step workflow with tests (use `/develop-complete-feature`)
- Making trivial changes (a few fields, single action)
- Only need architecture without code generation (use `architect` subagent directly)

---

## Examples

### Example 1: Simple Usage (Auto-detected Webapp)

```
/develop docs/detailed-specifications.md
```

- Webapp auto-detected from current directory
- Creates new architecture (Mode CREATE)
- Output directory: `docs/development` (default)

### Example 2: Custom Output Directory

```
/develop docs/inventory-specs.md docs/inventory-dev
```

- Architecture at: `docs/inventory-dev/architecture-plan.md`
- Review report at: `docs/inventory-dev/code-review-report.md`

### Example 3: Explicit Webapp Path

```
/develop docs/bugfix-spec.md --webapp=/path/to/webapp-template
```

- Use `--webapp` when running from outside the project directory
- Or when multiple webapps exist

### Example 4: Extend Existing Architecture (Bug Fix)

```
/develop docs/bugfix-spec.md docs/dev --architecture-file=docs/current-architecture.md
```

- Uses Mode EXTEND
- Analyzes existing architecture
- Generates only needed changes

### Example 5: Resume Interrupted Workflow

```
/develop docs/spec.md docs/dev --resume-from-phase=5
```

- Loads state from `.axelor-develop-state.json`
- Skips Phases 1-4 (already completed)
- Continues from Unit Test generation

### Example 6: Skip Test Generation

```
/develop docs/spec.md docs/dev --skip-tests
```

- Executes Phases 1-4 and 6-7
- Skips Phase 5 (Unit Test Generation)
- Useful for quick iterations or when tests will be added later

### Example 7: From EPIC/US Structure

```
/develop docs/epic-us-breakdown/ docs/sprint-1
```

- Reads EPIC and User Stories
- Generates architecture based on US technical details
- Implements all stories in single workflow

### Example 8: Enable Automatic Commits

```
/develop docs/spec.md docs/dev --auto-commit
```

- Enables automatic checkpoint commits after each phase approval
- Uses git-agent for all git operations
- Useful for automated workflows or when you want commits tracked automatically

---

## Integration with /analyze-requirements

### Complete Workflow

```bash
# Phase 1: Requirements Analysis
/analyze-requirements "Inventory management with stock tracking" docs/inventory

# Output:
# - docs/inventory/analysis-report.md
# - docs/inventory/gap-analysis-report.md
# - docs/inventory/detailed-specifications.md
# - docs/inventory/epic-us-breakdown.textile

# Phase 2: Development (run from webapp root directory)
/develop docs/inventory/detailed-specifications.md docs/inventory

# Output:
# - docs/inventory/architecture-plan.md
# - docs/inventory/code-review-report.md
# - {webapp}/modules/{module}/src/main/resources/domains/*.xml
# - {webapp}/modules/{module}/src/main/resources/views/*.xml
# - {webapp}/modules/{module}/src/main/java/**/*.java
```

### Standalone Usage

The `/develop` command can also be used independently with:
- Pre-existing specifications
- Manual architecture files
- Third-party specification documents

---

## See Also

- [State Management Schema](../state/develop-state-schema.md)
- [Troubleshooting Guide](./develop-troubleshooting.md)
- [Command Comparison](../commands/command-comparison.md)
- [analyze-requirements command](../../commands/analyze-requirements.md)
- [develop-complete-feature command](../../commands/develop-complete-feature.md)
