---
name: mr-title-validator
description: Validates merge request (MR) and pull request (PR) titles against conventional commits format. Mirrors GitLab CI validation to prevent pipeline failures.
user-invocable: false
allowed-tools:
  - Bash
  - Read
---

# MR Title Validator

## Mission

Validate merge request and pull request titles against conventional commits specification before creating the MR/PR. Ensures titles follow the same format as commits, enabling semantic versioning and automated changelog generation upon merge.

## Validation Checks

1. **Format compliance**: `<type>[optional scope]: <description>`
2. **Type validity**: Must be from allowed list (feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert)
3. **Type case**: Must be lowercase
4. **Description presence**: Cannot be empty
5. **Colon and space**: Must have `: ` separator
6. **Scope format**: If present, must be in parentheses and lowercase
7. **Description case**: Should start lowercase
8. **Length**: Should be concise but descriptive

See @docs/git/conventional-commits.md for complete specification.

## Process

1. Load validation rules from @skills/mr-title-validator/reference/mr-title-rules.json
2. Parse title into components (type, scope, description)
3. Validate each component
4. Check against conventional commits pattern
5. Output validation result with suggestions if invalid

## Usage

```bash
# Validate a title before creating MR
mr-title-validator "feat(auth): add user authentication"

# Validate with detailed output
mr-title-validator "fix: resolve login bug" --verbose

# Check if title would pass CI validation
mr-title-validator "refactor(api): simplify user service" --ci-check

# Get suggestions for invalid title
mr-title-validator "Add authentication" --suggest
```

## Validation Pattern

The MR title must match this regex pattern:

```regex
^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+
```

## Output Format

### Valid Title

```
MR TITLE VALIDATION

TITLE: feat(auth): add user authentication

RESULT: VALID

Format: Conventional commits format
Type: feat (valid)
Scope: auth (valid format)
Description: add user authentication (valid)

This title will PASS GitLab CI validation.
```

### Invalid Title

```
MR TITLE VALIDATION

TITLE: Add authentication feature

RESULT: INVALID

ERRORS: 2

1. Missing conventional commit type
   Expected format: <type>[scope]: <description>

2. Title does not match conventional commits pattern

SUGGESTIONS:

Based on your title, you likely want:
- feat: add authentication feature
- feat(auth): add authentication feature

This title will FAIL GitLab CI validation.
```

## Suggestion Algorithm

When title is invalid, provide smart suggestions:

1. **Detect intent** from keywords:
   - "add", "implement", "create" -> `feat`
   - "fix", "resolve", "correct" -> `fix`
   - "update doc", "readme" -> `docs`
   - "refactor", "reorganize" -> `refactor`

2. **Extract potential scope** from module names

3. **Format description**: lowercase, imperative mood, no trailing punctuation

## Common Errors

| Error | Example | Fix |
|-------|---------|-----|
| No type prefix | `Add auth` | `feat: add auth` |
| Capital type | `Feat: add` | `feat: add` |
| Missing space | `feat:add` | `feat: add` |
| Capital description | `feat: Add` | `feat: add` |
| Trailing period | `feat: add.` | `feat: add` |

See @docs/git/conventional-commits.md for more examples.

## Integration

Used before creating MR/PR:

```
Feature development complete
  |
  v
Draft MR title
  |
  v
mr-title-validator (validate title)
  |
  v
If invalid: Show errors, provide suggestions
  |
  v
If valid: Create MR/PR
  |
  v
GitLab CI init stage validates title (passes)
```

## CI/CD Mirror

This skill mirrors the validation performed by `ci/scripts/validate-mr-title.sh` in GitLab CI.

**CI Script Pattern**:
```bash
PATTERN="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+"
echo "$CI_MERGE_REQUEST_TITLE" | grep -Eq "$PATTERN"
```

Local validation ensures CI will pass.

## Squash Commits Integration

When squash commits are enabled (recommended):
- MR title becomes the final commit message on merge
- All individual commits are squashed into one
- The MR title must follow conventional commits

See @docs/git/pr-guidelines.md for squash merge strategy.

## Requirements

- Bash 4.0+
- grep with extended regex support (-E)
- @skills/mr-title-validator/reference/mr-title-rules.json
- @docs/git/conventional-commits.md

## Best Practices

1. Validate before creating MR
2. Use scopes for clarity
3. Be specific in description
4. Match commit messages style
5. Enable squash commits
