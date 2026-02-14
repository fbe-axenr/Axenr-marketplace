# PR Risk Assessment Guide

This guide defines how to calculate and assess risk for pull requests.

## Risk Calculation Formula

```
Risk Score = (Size Weight * Size Score) +
             (Complexity Weight * Complexity Score) +
             (Test Coverage Weight * Test Coverage Score) +
             (Dependencies Weight * Dependencies Score) +
             (Security Weight * Security Score)
```

## Weights

```json
{
  "size": 0.2,
  "complexity": 0.25,
  "testCoverage": 0.2,
  "dependencies": 0.15,
  "security": 0.2
}
```

## Scoring Criteria

### Size Score (0-100)

Based on number of files and net lines changed:

| Files | Net Lines | Score | Level |
|-------|-----------|-------|-------|
| 1-3 | <50 | 10 | Very Small |
| 4-7 | 50-150 | 25 | Small |
| 8-15 | 150-350 | 50 | Medium |
| 16-25 | 350-700 | 75 | Large |
| 26+ | 700+ | 100 | Very Large |

### Complexity Score (0-100)

Based on multiple factors:

**File Distribution**: (weight: 0.4)
- Single module: 10
- 2-3 modules: 30
- 4-6 modules: 60
- 7+ modules: 100

**Change Patterns**: (weight: 0.3)
- Only additions: 20
- Mostly additions: 30
- Mixed add/delete: 50
- Mostly deletions: 40
- Refactoring (high churn): 70

**Logic Complexity**: (weight: 0.3)
- Config/docs only: 10
- Simple CRUD: 30
- Business logic: 60
- Complex algorithms: 80
- Distributed systems/async: 100

### Test Coverage Score (0-100)

Inverse scoring (higher coverage = lower risk):

| Test Ratio | Coverage Change | Score | Level |
|------------|-----------------|-------|-------|
| >80% | +5% or more | 10 | Excellent |
| 60-80% | +2% to +5% | 25 | Good |
| 40-60% | 0% to +2% | 50 | Fair |
| 20-40% | -2% to 0% | 75 | Poor |
| <20% | <-2% | 100 | Critical |

**Test Ratio**: (Test files / Source files) * 100

### Dependencies Score (0-100)

Based on dependency changes:

| Change Type | Count | Score | Level |
|-------------|-------|-------|-------|
| No changes | 0 | 0 | None |
| Patch updates | 1-3 | 10 | Low |
| Minor updates | 1-3 | 25 | Low-Medium |
| Major updates | 1-2 | 50 | Medium |
| New dependencies | 1-3 | 40 | Medium |
| New dependencies | 4+ | 70 | High |
| Major updates | 3+ | 80 | High |
| Removed core deps | Any | 90 | Critical |

### Security Score (0-100)

Based on type of code changed:

| Category | Score | Examples |
|----------|-------|----------|
| No security impact | 0 | UI only, docs, tests |
| Low impact | 20 | Internal business logic |
| Medium impact | 50 | API endpoints, validation |
| High impact | 80 | Authentication, authorization |
| Critical impact | 100 | Crypto, password handling, secrets |

**Additional Factors** (add to base score):
- SQL queries without parameterization: +30
- External API calls: +20
- File system operations: +15
- User input handling: +20
- Session management: +25
- Payment processing: +40

## Overall Risk Level

Final score determines risk level:

| Score Range | Risk Level | Action |
|-------------|------------|--------|
| 0-25 | Low | Standard review |
| 26-50 | Medium | Careful review, 1-2 approvals |
| 51-75 | High | Thorough review, 2+ approvals, security check |
| 76-100 | Critical | Extensive review, 3+ approvals, security audit, consider splitting |

## Review Time Estimation

Based on risk score and size:

```
Base Time = (Files * 2 minutes) + (Net Lines / 10)

Multipliers:
- Low Risk: 1.0x
- Medium Risk: 1.2x
- High Risk: 1.5x
- Critical Risk: 2.0x

Security multiplier: +0.3x if security score > 50
```

## Mitigation Strategies

### Size Mitigation
- **Large PRs (16+ files)**: Consider splitting into logical units
- **Very Large (26+ files)**: Strongly recommend splitting
- Create a tracking issue and link related PRs

### Complexity Mitigation
- **Cross-module changes**: Ensure module owners review
- **Complex algorithms**: Add detailed comments and diagrams
- **Refactoring**: Ensure test coverage is maintained

### Test Coverage Mitigation
- **Low coverage (<40%)**: Require additional tests before merge
- **Decreasing coverage**: Block merge until coverage improves
- **No tests**: Require tests for critical paths

### Dependencies Mitigation
- **New dependencies**: Review necessity, check maintenance, security
- **Major updates**: Review changelog for breaking changes
- **Multiple updates**: Test thoroughly, check compatibility

### Security Mitigation
- **High security impact**: Require security expert review
- **Critical security**: Full security audit, penetration testing
- **Authentication changes**: OWASP checklist review
- **Crypto operations**: Cryptographer review

## Examples

### Example 1: Small Bug Fix

```
Files: 2 (1 source, 1 test)
Net Lines: +15
Modules: 1
Test Ratio: 50%
Coverage Change: +2%
Dependencies: None
Security: Low

Calculation:
- Size Score: 10 (very small)
- Complexity Score: 20 (single module, simple)
- Test Coverage Score: 25 (good coverage)
- Dependencies Score: 0 (none)
- Security Score: 20 (low impact)

Final Score: (0.2*10) + (0.25*20) + (0.2*25) + (0.15*0) + (0.2*20) = 15

Risk Level: LOW
Review Time: ~5 minutes
```

### Example 2: Authentication Feature

```
Files: 15 (8 source, 4 test, 2 config, 1 doc)
Net Lines: +330
Modules: 3 (auth, user, api)
Test Ratio: 50%
Coverage Change: +3.8%
Dependencies: 2 new (jsonwebtoken, bcrypt)
Security: Critical (authentication)

Calculation:
- Size Score: 50 (medium)
- Complexity Score: 60 (cross-module, business logic)
- Test Coverage Score: 25 (good coverage)
- Dependencies Score: 40 (new dependencies)
- Security Score: 100 (authentication)

Final Score: (0.2*50) + (0.25*60) + (0.2*25) + (0.15*40) + (0.2*100) = 56

Risk Level: HIGH
Review Time: ~35 minutes
Recommendations:
- 2+ approvals required
- Security expert review
- Manual testing of auth flows
- Verify password hashing
- Check token security
```

### Example 3: Large Refactoring

```
Files: 28
Net Lines: +120 (high churn: +800, -680)
Modules: 6
Test Ratio: 40%
Coverage Change: 0%
Dependencies: None
Security: Low

Calculation:
- Size Score: 100 (very large)
- Complexity Score: 80 (many modules, high churn)
- Test Coverage Score: 50 (fair coverage, no improvement)
- Dependencies Score: 0
- Security Score: 20

Final Score: (0.2*100) + (0.25*80) + (0.2*50) + (0.15*0) + (0.2*20) = 54

Risk Level: HIGH
Review Time: ~75 minutes
Recommendations:
- Consider splitting into smaller PRs
- Ensure no functionality changes
- Run full regression tests
- Verify test coverage maintained
```

## Automation

This risk assessment should be:
1. Calculated automatically by pr-analyzer skill
2. Included in PR description
3. Used to determine review requirements
4. Integrated with CI/CD approval rules
5. Tracked over time for team metrics

## Continuous Improvement

Track PR risk metrics to improve processes:
- Average risk score per team/developer
- Time to review by risk level
- Defect rate by risk level
- Test coverage trends
- Review effectiveness by risk level

Use data to refine scoring weights and thresholds.
