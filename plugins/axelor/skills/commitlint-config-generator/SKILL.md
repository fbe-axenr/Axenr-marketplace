---
name: commitlint-config-generator
description: Generate .commitlintrc.json configuration files and package.json dependencies for commit message validation aligned with Axelor standards
allowed-tools: ["Read", "Write"]
---

# Commitlint Config Generator

## Mission

Generate complete and valid `.commitlintrc.json` configuration files with matching `package.json` dependencies for commit message validation. Ensures configurations align with Axelor conventional commit standards and integrate seamlessly with GitLab CI/CD pipelines.

## Input Parameters

1. **Profile** (required):
   - `strict`: Axelor standard profile (recommended)
     - Header max 100 chars (hard limit), 72 recommended
     - Body max 100 chars per line
     - Body verbosity: max 2 sentences
     - No emojis, no Co-Authored-By
   - `standard`: Balanced profile
     - Header max 100 chars
     - Body max 100 chars per line
     - Standard conventional commits rules
   - `relaxed`: Lenient profile
     - Header max 120 chars
     - Body max 120 chars per line
     - Warnings instead of errors

2. **Allowed Types** (optional, defaults to standard):
   - Default: `feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert`
   - Custom: Provide comma-separated list

3. **Scope Enforcement** (optional):
   - `none`: Scope is optional (default)
   - `required`: Scope must be provided
   - `enum`: Scope must be from predefined list (provide list)

4. **Custom Scopes** (optional):
   - List of valid scopes (e.g., `auth, sale, purchase, inventory`)
   - Only used if scope enforcement is `enum`

5. **Additional Rules** (optional):
   - Subject case rules
   - Footer requirements
   - Custom patterns

## Process

1. Load base configuration from @skills/commitlint-config-generator/reference/default-config.json
2. Load rule definitions from @skills/commitlint-config-generator/reference/rule-definitions.json
3. Apply profile-specific rules (strict/standard/relaxed)
4. Merge custom rules if provided
5. Generate `.commitlintrc.json` with proper formatting
6. Generate matching `package.json` with commitlint dependencies
7. Validate JSON syntax
8. Provide test commands

## Output Format

### .commitlintrc.json

```json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "type-enum": [2, "always", [
      "feat", "fix", "docs", "style", "refactor",
      "perf", "test", "build", "ci", "chore", "revert"
    ]],
    "type-case": [2, "always", "lower-case"],
    "type-empty": [2, "never"],
    "scope-case": [2, "always", "lower-case"],
    "subject-empty": [2, "never"],
    "subject-full-stop": [2, "never", "."],
    "subject-case": [2, "never", ["sentence-case", "start-case", "pascal-case", "upper-case"]],
    "header-max-length": [2, "always", 100],
    "body-leading-blank": [1, "always"],
    "body-max-line-length": [2, "always", 100],
    "footer-leading-blank": [1, "always"],
    "footer-max-line-length": [2, "always", 100]
  },
  "ignores": [
    "(commit) => commit.startsWith('Merge branch')",
    "(commit) => commit.startsWith('Merge remote-tracking branch')",
    "(commit) => commit.startsWith('Revert \"')"
  ]
}
```

### package.json

```json
{
  "name": "axelor-module",
  "version": "1.0.0",
  "private": true,
  "devDependencies": {
    "@commitlint/cli": "^18.4.3",
    "@commitlint/config-conventional": "^18.4.3"
  },
  "scripts": {
    "commitlint": "commitlint --edit",
    "commitlint:check": "commitlint --from=HEAD~1 --to=HEAD --verbose"
  }
}
```

### Test Commands

```bash
# Install dependencies
npm install

# Test valid commit
echo "feat: add feature" | npx commitlint

# Test invalid commit
echo "Feature: add feature" | npx commitlint

# Check last commit
npx commitlint --from=HEAD~1 --to=HEAD --verbose

# Check range of commits
npx commitlint --from=main --to=HEAD --verbose
```

## Validation Rules

1. **JSON Syntax**: Valid JSON structure
2. **Rule Severity**: Values are 0 (disabled), 1 (warning), or 2 (error)
3. **Rule Names**: Match commitlint specification
4. **Type Enum**: All types are lowercase, no duplicates
5. **Scope Enum**: If provided, scopes are lowercase, no duplicates
6. **Dependencies**: Package versions are valid and compatible

## Profile Specifications

### Strict Profile (Axelor Standard)

```json
{
  "rules": {
    "type-enum": [2, "always", ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]],
    "type-case": [2, "always", "lower-case"],
    "type-empty": [2, "never"],
    "scope-case": [2, "always", "lower-case"],
    "scope-empty": [0],
    "subject-empty": [2, "never"],
    "subject-case": [2, "never", ["sentence-case", "start-case", "pascal-case", "upper-case"]],
    "subject-full-stop": [2, "never", "."],
    "header-max-length": [2, "always", 100],
    "body-leading-blank": [1, "always"],
    "body-max-line-length": [2, "always", 100],
    "footer-leading-blank": [1, "always"],
    "footer-max-line-length": [2, "always", 100]
  },
  "ignores": [
    "(commit) => commit.startsWith('Merge branch')",
    "(commit) => commit.startsWith('Merge remote-tracking branch')",
    "(commit) => commit.startsWith('Revert \"')"
  ]
}
```

**Characteristics**:
- Hard limit: 100 chars for header, body lines, footer lines
- Strict type enforcement (lowercase, from enum)
- Warnings for blank lines (leading-blank)
- Ignores automatic merge commits

### Standard Profile

```json
{
  "rules": {
    "type-enum": [2, "always", ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]],
    "type-case": [2, "always", "lower-case"],
    "type-empty": [2, "never"],
    "scope-case": [2, "always", "lower-case"],
    "subject-empty": [2, "never"],
    "subject-case": [2, "never", ["sentence-case", "start-case", "pascal-case", "upper-case"]],
    "subject-full-stop": [2, "never", "."],
    "header-max-length": [2, "always", 100],
    "body-max-line-length": [2, "always", 100],
    "footer-max-line-length": [2, "always", 100]
  }
}
```

**Characteristics**:
- Same as strict but no blank line warnings
- No merge commit ignores (suitable for squash-only workflows)

### Relaxed Profile

```json
{
  "rules": {
    "type-enum": [1, "always", ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]],
    "type-case": [1, "always", "lower-case"],
    "type-empty": [2, "never"],
    "subject-empty": [2, "never"],
    "subject-full-stop": [1, "never", "."],
    "header-max-length": [1, "always", 120],
    "body-max-line-length": [1, "always", 120]
  }
}
```

**Characteristics**:
- Warnings (1) instead of errors (2) for most rules
- Longer length limits (120 chars)
- Suitable for learning/transition period

## Reference Files

- @skills/commitlint-config-generator/reference/default-config.json: Base configuration template
- @skills/commitlint-config-generator/reference/rule-definitions.json: All available commitlint rules with descriptions
- @skills/commitlint-config-generator/reference/custom-configs/: Example project-specific configurations

## Examples

### Example 1: Standard Axelor Module

**Input**:
```
Profile: strict
Types: default
Scope: optional
```

**Output**: `.commitlintrc.json` with strict Axelor rules + `package.json` with dependencies

### Example 2: Custom Scopes Required

**Input**:
```
Profile: strict
Types: default
Scope: enum
Custom Scopes: auth, sale, purchase, inventory, production, stock
```

**Output**:
```json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "type-enum": [2, "always", ["feat", "fix", "docs", "style", "refactor", "perf", "test", "build", "ci", "chore", "revert"]],
    "scope-enum": [2, "always", ["auth", "sale", "purchase", "inventory", "production", "stock"]],
    "scope-empty": [2, "never"],
    ...
  }
}
```

### Example 3: Monorepo with Package Scopes

**Input**:
```
Profile: standard
Types: default
Scope: enum
Custom Scopes: axelor-core, axelor-web, axelor-mobile, axelor-api
```

**Output**: Configuration with package-based scope validation

## Common Issues and Fixes

### Issue: Type not recognized

**Problem**: `feat` is valid but `feature` is not

**Solution**: Ensure types match the enum exactly (use `feat`, not `feature`)

### Issue: Scope format error

**Problem**: Scope `Auth` rejected (uppercase)

**Solution**: All scopes must be lowercase (`auth`, not `Auth`)

### Issue: Header too long

**Problem**: Commit header exceeds 100 characters

**Solution**:
- Shorten subject
- Use abbreviations (authentication → auth)
- Move details to body

### Issue: Subject case error

**Problem**: "Add Feature" rejected

**Solution**: Use lowercase: "add feature"

## Integration

Used by:
- cicd-agent: Step 3 (Create Commitlint Configuration)
- git-agent: Validation checks
- axelor-project-initializer: Initial setup

## Requirements

- JSON parsing/validation
- Understanding of commitlint rule structure
- Access to reference configurations
