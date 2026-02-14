#!/bin/bash
#
# Validate MR title follows conventional commit format
# Usage: ./validate-mr-title.sh
#

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in MR context
if [ -z "$CI_MERGE_REQUEST_TITLE" ]; then
  echo -e "${YELLOW}Warning: Not running in merge request context. Skipping validation.${NC}"
  exit 0
fi

echo "==========================================="
echo "Validating Merge Request Title"
echo "==========================================="
echo ""
echo "MR Title: $CI_MERGE_REQUEST_TITLE"
echo ""

# Conventional commit regex pattern
# Format: type(scope): description
# or: type: description
PATTERN="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+"

if echo "$CI_MERGE_REQUEST_TITLE" | grep -Eq "$PATTERN"; then
  echo -e "${GREEN}✅ SUCCESS: MR title follows conventional commit format!${NC}"
  echo ""
  exit 0
else
  echo -e "${RED}❌ ERROR: MR title does NOT follow conventional commit format!${NC}"
  echo ""
  echo "Expected format:"
  echo "  <type>[optional scope]: <description>"
  echo ""
  echo "Examples of valid titles:"
  echo "  feat: add new domain validation skill"
  echo "  feat(skills): add domain validation skill"
  echo "  fix: resolve agent configuration issue"
  echo "  fix(agents): correct code reviewer logic"
  echo "  docs: update README with skill usage"
  echo "  refactor(ci): simplify release pipeline"
  echo ""
  echo "Allowed types:"
  echo "  - feat:     A new feature"
  echo "  - fix:      A bug fix"
  echo "  - docs:     Documentation only changes"
  echo "  - style:    Code style/formatting (no functional change)"
  echo "  - refactor: Code refactoring (no functional change)"
  echo "  - perf:     Performance improvements"
  echo "  - test:     Adding or updating tests"
  echo "  - build:    Changes to build system or dependencies"
  echo "  - ci:       Changes to CI/CD configuration"
  echo "  - chore:    Other changes (maintenance, etc.)"
  echo "  - revert:   Revert a previous commit"
  echo ""
  echo "Your MR title: '$CI_MERGE_REQUEST_TITLE'"
  echo ""
  echo "Please update your MR title to follow this format."
  echo ""
  exit 1
fi
