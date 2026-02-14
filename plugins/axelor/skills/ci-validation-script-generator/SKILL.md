---
name: ci-validation-script-generator
description: Generate bash validation scripts for CI/CD pipelines (MR title validation, squash checker, branch validator)
allowed-tools: ["Bash", "Read", "Write"]
---

# CI Validation Script Generator

## Mission

Generate production-ready bash validation scripts for GitLab CI/CD pipelines. Scripts validate MR titles, check squash commits, enforce branch naming conventions, and provide clear error messages with ANSI colors.

## Input Parameters

1. **Script Type** (required):
   - `mr-title-validator`: Validates MR/PR titles against conventional commits
   - `squash-checker`: Ensures MR has only 1 commit (squash required)
   - `branch-validator`: Validates branch naming conventions

2. **Validation Pattern** (required for mr-title and branch validators):
   - `conventional-commits`: Standard `<type>(<scope>): <description>` format
   - `custom-regex`: Provide custom regex pattern

3. **CI Platform** (required):
   - `gitlab`: Use GitLab CI environment variables
   - `github`: Use GitHub Actions environment variables
   - `generic`: Platform-agnostic bash script

4. **Output Format** (optional):
   - `color`: ANSI colored output (default)
   - `plain`: Plain text output (for CI logs)

5. **Error Handling** (optional):
   - `strict`: Exit 1 on any validation failure (default)
   - `lenient`: Show warnings but exit 0

## Process

1. Load script template from @skills/ci-validation-script-generator/reference/script-templates/
2. Load regex patterns from reference/regex-patterns.json
3. Apply CI platform-specific variables
4. Generate script with proper error handling
5. Add executable permissions
6. Provide test commands

## Output Format

### validate-mr-title.sh

```bash
#!/bin/bash
set -e

# ANSI Color Codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Check if running in MR context
if [ -z "$CI_MERGE_REQUEST_TITLE" ]; then
  echo -e "${YELLOW}⚠ Not in MR context. Skipping validation.${NC}"
  exit 0
fi

# Conventional commits pattern
PATTERN="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+"

# Validate MR title
if echo "$CI_MERGE_REQUEST_TITLE" | grep -Eq "$PATTERN"; then
  echo -e "${GREEN}✅ MR title is valid!${NC}"
  echo "Title: $CI_MERGE_REQUEST_TITLE"
  exit 0
else
  echo -e "${RED}❌ MR title is invalid!${NC}"
  echo ""
  echo "Expected format: <type>(<scope>): <description>"
  echo "Example: feat(auth): add JWT authentication"
  echo ""
  echo "Your title: '$CI_MERGE_REQUEST_TITLE'"
  echo ""
  echo -e "${BLUE}Valid types:${NC} feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
  exit 1
fi
```

### squash-checker.sh

```bash
#!/bin/bash
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

if [ -z "$CI_MERGE_REQUEST_DIFF_BASE_SHA" ]; then
  echo -e "${YELLOW}⚠ Not in MR context. Skipping.${NC}"
  exit 0
fi

# Count commits in MR
COMMITS_COUNT=$(git rev-list --count ${CI_MERGE_REQUEST_DIFF_BASE_SHA}..${CI_COMMIT_SHA})

if [ "$COMMITS_COUNT" -eq 1 ]; then
  echo -e "${GREEN}✅ MR has 1 commit (squashed)${NC}"
  exit 0
else
  echo -e "${RED}❌ MR has $COMMITS_COUNT commits${NC}"
  echo ""
  echo "This project requires squash commits before merging."
  echo "Please squash your commits to a single commit."
  echo ""
  echo "How to squash:"
  echo "  git rebase -i ${CI_MERGE_REQUEST_DIFF_BASE_SHA}"
  echo "  # Mark all commits except first as 'squash'"
  echo "  git push --force-with-lease"
  exit 1
fi
```

## Reference Files

- @skills/ci-validation-script-generator/reference/script-templates/: Template scripts
- @skills/ci-validation-script-generator/reference/regex-patterns.json: Validation patterns
- @skills/ci-validation-script-generator/reference/ci-variables-guide.md: CI/CD variable reference

## Examples

### Example 1: MR Title Validator for GitLab

**Input**:
```
Script Type: mr-title-validator
Pattern: conventional-commits
CI Platform: gitlab
Output Format: color
```

**Output**: validate-mr-title.sh with GitLab variables and colored output

### Example 2: Squash Checker

**Input**:
```
Script Type: squash-checker
CI Platform: gitlab
```

**Output**: squash-checker.sh that enforces single commit per MR

## Integration

Used by:
- cicd-agent: Step 4 (Create Validation Scripts)
- axelor-project-initializer: CI/CD setup

## Requirements

- Bash 4.0+
- Git (for squash-checker)
- Grep with extended regex (-E)
- Understanding of CI/CD environment variables
