---
name: pr-analyzer
description: Analyzes pull request changes and generates comprehensive PR descriptions with risk assessment, statistics, categorization, test coverage analysis, and context-aware review checklists.
allowed-tools: ["Bash", "Read", "Grep"]
---

# PR Analyzer

## Mission

Analyze pull request changes and generate enhanced PR descriptions with comprehensive analysis, risk assessment, statistics, file categorization, test coverage comparison, and context-aware review checklists.

## Analysis Components

1. **Change Statistics**: Files changed, insertions, deletions, net change
2. **File Categorization**: Source, test, config, docs, styles, build
3. **Risk Assessment**: Size, complexity, test coverage, dependencies, security
4. **Test Coverage Analysis**: Before/after comparison with percentage change
5. **Performance Impact**: Identify potential performance-critical changes
6. **Breaking Changes**: Detect API changes, schema modifications
7. **Dependencies**: Track added/updated/removed dependencies
8. **Review Checklist**: Context-aware checklist based on changed file types
9. **Visual Diagrams**: Mermaid diagrams for architecture changes

## Process

1. Analyze git diff and statistics
2. Categorize changed files by type
3. Calculate multi-factor risk score
4. Compare test coverage (if applicable)
5. Identify breaking changes and performance impacts
6. Generate context-aware review checklist
7. Output comprehensive PR description in markdown

## Usage

```bash
# Analyze current branch against main
pr-analyzer

# Analyze specific branch comparison
pr-analyzer main...feature-branch

# Analyze with base branch specified
pr-analyzer --base main --head feature-auth

# Generate description only
pr-analyzer --format description-only
```

## Output Format

```markdown
## Summary
Brief description of changes

**Impact**: 15 files (+450, -120, +330 net)
**Risk Level**: Medium
**Review Time**: ~25 minutes

## What Changed

### Source Code (8 files)
- `src/auth/jwt.service.ts` - JWT token generation
- `src/user/user.service.ts` - User authentication

### Tests (4 files)
- `tests/auth/jwt.service.test.ts` - Unit tests

### Configuration (2 files)
- `package.json` - Added dependencies

## Type of Change
- [x] New feature (feat)
- [x] Breaking change

## Risk Assessment

### Overall Risk: MEDIUM

**Factors**:
- Size: Medium (15 files)
- Complexity: Medium (cross-module)
- Test Coverage: Good (+3.8%)
- Security: Medium (auth logic)

### Mitigation
1. Security review required
2. Test token flows

## Review Checklist

### Security (Critical for auth changes)
- [ ] Password hashing uses bcrypt
- [ ] JWT secret from env variable
- [ ] No sensitive data in payload

### Testing
- [ ] Unit tests for new code
- [ ] Integration tests for flows
```

See @docs/git/pr-guidelines.md for complete PR structure and best practices.

## Risk Calculation

Risk score based on multiple factors:

| Factor | Weight | Criteria |
|--------|--------|----------|
| Size | 0.2 | Files and lines changed |
| Complexity | 0.25 | Cross-module, architecture |
| Test Coverage | 0.2 | Coverage change percentage |
| Dependencies | 0.15 | New/updated dependencies |
| Security | 0.2 | Auth, crypto, data handling |

**Risk Levels**:
- Low: Score < 30
- Medium: Score 30-60
- High: Score 60-80
- Critical: Score > 80

See @skills/pr-analyzer/reference/risk-assessment-guide.md for details.

## File Categorization

| Category | Patterns |
|----------|----------|
| Source | `src/**/*.{ts,js,java,py}` (excluding tests) |
| Tests | `**/*.{test,spec}.*`, `**/tests/**` |
| Config | `*.{json,yml,yaml,xml,properties}` |
| Docs | `*.md`, `docs/**` |
| Build | `build.gradle`, `pom.xml`, `package.json` |

## Context-Aware Checklist

Generate checklist based on changed file types:

- **Auth/security files** -> Security review section
- **Database files** -> Database review section
- **API files** -> API review section
- **Config files** -> Configuration review section

## Integration

```
Feature complete
  |
  v
pr-analyzer (generate analysis)
  |
  v
Review and adjust description
  |
  v
Create PR with enhanced description
  |
  v
Team review using checklist
```

## Requirements

- git 2.0+
- Bash 4.0+
- @skills/pr-analyzer/reference/pr-template.md
- @skills/pr-analyzer/reference/risk-assessment-guide.md
- @docs/git/pr-guidelines.md

## Best Practices

1. Generate description before creating PR
2. Adjust risk assessment based on context
3. Use checklist during review
4. Document breaking changes clearly
5. Track test coverage trends
