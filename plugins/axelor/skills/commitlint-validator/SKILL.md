---
name: commitlint-validator
description: Validates commit messages against conventional commits specification. Enforces type, scope, format, length limits. Aligns with @commitlint/config-conventional.
user-invocable: false
allowed-tools:
  - Bash
  - Read
---

# Commitlint Validator

## Mission

Validate commit messages against conventional commits specification before committing. Ensures compliance with project's commitlint configuration and prevents CI/CD pipeline failures.

## CRITICAL: Forbidden Elements

The following cause **IMMEDIATE VALIDATION FAILURE**:

1. **EMOJIS** - Any emoji anywhere (header, body, footer)
2. **CO-AUTHORED-BY** - Any Co-Authored-By trailer
3. **TOOL SIGNATURES** - "Generated with Claude Code" or similar

See @docs/git/conventional-commits.md for complete specification.

## Validation Checks

| Check | Rule | Severity |
|-------|------|----------|
| Type | Must be: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert | Error |
| Type case | Lowercase only | Error |
| Scope | Lowercase, parentheses, hyphen allowed | Error |
| Subject | Required, lowercase start, no period | Error |
| Header length | Max 100 chars (hard), 72 chars (soft) | Error/Warn |
| Body | Blank line before, max 100 chars/line, max 2 sentences | Warn |
| Footer | Blank line before, max 100 chars/line | Warn |
| Emojis | Forbidden (U+1F300-U+1F9FF) | Error |
| Co-Authored-By | Forbidden | Error |
| Language | English only | Error |

## Process

1. Load config from @skills/commitlint-validator/reference/commitlint-config.json
2. Parse commit message (header, body, footer)
3. Validate against rules
4. Output validation report

## Usage

```bash
# Validate a message
commitlint-validator "feat(auth): add authentication"

# Validate before committing
commitlint-validator "$(cat .git/COMMIT_EDITMSG)"

# Check last commit
commitlint-validator "$(git log -1 --pretty=%B)"
```

## Output Format

### Valid

```
COMMIT VALIDATION REPORT

MESSAGE: feat(auth): add user authentication
RESULT: VALID

Type: feat (valid)
Scope: auth (valid)
Subject: add user authentication (valid)
Header: 42/100 characters
```

### Invalid

```
COMMIT VALIDATION REPORT

MESSAGE: Feature: Add Auth
RESULT: INVALID

ERRORS: 2
1. Type "Feature" not in enum (did you mean: feat?)
2. Subject uses start-case (expected: lowercase)

FIX: feat: add auth
```

## Integration

```
Code changes -> commitlint-validator (local) -> git commit -> CI/CD commitlint (server)
```

See @docs/git/quick-start-guide.md for complete workflow.

## Configuration

Based on @commitlint/config-conventional. Full config at @skills/commitlint-validator/reference/commitlint-config.json.

Key limits:
- Header: 100 chars max (72 recommended)
- Body: 100 chars/line, 2 sentences max
- Footer: 100 chars/line

## Common Errors

See @docs/git/conventional-commits.md for complete examples and fixes.

Quick reference:

| Error | Bad | Good |
|-------|-----|------|
| Type case | `Feature:` | `feat:` |
| Subject case | `Add Auth` | `add auth` |
| Trailing period | `add auth.` | `add auth` |
| Emoji | `add auth ✨` | `add auth` |
| Header length | 80+ chars | <72 chars |

## Requirements

- Bash 4.0+
- grep with -E support
- @skills/commitlint-validator/reference/commitlint-config.json
- @docs/git/conventional-commits.md

## CI/CD Mirror

Mirrors validation from:
- `.gitlab-ci.yml` init stage (commitlint)
- `ci/scripts/validate-mr-title.sh`

Local validation matches CI/CD validation.
