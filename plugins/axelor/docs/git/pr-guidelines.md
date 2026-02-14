# Pull Request Guidelines

Best practices for creating and reviewing pull requests in Axelor projects.

## Table of Contents

1. [Overview](#overview)
2. [Before Creating a PR](#before-creating-a-pr)
3. [PR Title](#pr-title)
4. [PR Description](#pr-description)
5. [PR Size](#pr-size)
6. [Code Review](#code-review)
7. [Merging Strategy](#merging-strategy)
8. [Common Pitfalls](#common-pitfalls)
9. [Automation](#automation)
10. [Examples](#examples)

## Overview

Pull Requests (PRs) are the primary mechanism for code review and integration in Axelor projects. A good PR:

- Is easy to review
- Has a clear purpose
- Includes comprehensive description
- Contains appropriate tests
- Follows project conventions
- Passes all CI/CD checks

### Benefits of Good PRs

- **Faster reviews**: Clear PRs get reviewed quickly
- **Better quality**: Thorough reviews catch issues
- **Knowledge sharing**: Team learns from each other
- **Documentation**: PRs document decisions
- **Traceability**: Link changes to requirements

## Before Creating a PR

### 1. Ensure Code Quality

Run local checks before creating PR:

```bash
# Format code
./gradlew spotlessApply

# Run tests
./gradlew test

# Check for errors
./gradlew check

# Build project
./gradlew build
```

### 2. Review Your Own Changes

Self-review before submitting:

```bash
# Review all changes
git diff main...HEAD

# Review specific files
git diff main...HEAD src/main/java/

# Check commit history
git log main..HEAD --oneline
```

**Checklist**:
- [ ] All changes are intentional
- [ ] No debug code left (console.log, print statements)
- [ ] No commented-out code
- [ ] No TODOs that should be resolved
- [ ] Code follows project style
- [ ] Tests are included

### 3. Update Documentation

Ensure documentation is current:

- Update README if setup changed
- Document new APIs or endpoints
- Update architecture docs if structure changed
- Add comments for complex logic
- Update CHANGELOG if applicable

### 4. Check CI Status

Verify CI passes locally:

```bash
# Run same checks as CI
npm run lint
npm test
./gradlew build
```

## PR Title

PR titles must follow conventional commits format.

### Format

```
<type>(<scope>): <subject>
```

### Examples

Good PR titles:
```
feat(sale): add order discount functionality
fix(auth): resolve token expiration issue
refactor(api): simplify user service
docs(readme): update installation guide
test(order): add integration tests
```

Bad PR titles:
```
Update           (vague, no type)
Fix bug          (no scope, not specific)
WIP              (not descriptive)
Misc changes     (meaningless)
```

### Why This Matters

- **Squash commits**: MR title becomes the commit message
- **Changelog**: Title appears in generated changelog
- **Semantic versioning**: Type determines version bump
- **CI validation**: Title is validated in pipeline

See [Conventional Commits](./conventional-commits.md) for detailed guidelines.

## PR Description

A comprehensive description helps reviewers understand your changes.

### Template Structure

```markdown
## Summary
Brief description of what this PR does and why.

## What Changed
- Added/Modified/Fixed feature X
- Updated component Y
- Refactored module Z

## Type of Change
- [x] New feature (feat)
- [ ] Bug fix (fix)
- [ ] Refactoring (refactor)
- [ ] Documentation (docs)
- [ ] Testing (test)
- [ ] Chore (chore)

## How Has This Been Tested?
1. How to test these changes
2. What scenarios were tested
3. Any special setup required

## Screenshots (if applicable)
[Add screenshots for UI changes]

## Breaking Changes
[List breaking changes or "None"]

## Dependencies
[List new/updated dependencies or "None"]

## Related Issues
Closes #<issue-number>
Related to #<issue-number>

## Checklist
- [ ] Code follows project conventions
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No build artifacts committed
- [ ] CI checks pass
```

### Enhanced Description with PR Analyzer

Use the `pr-analyzer` skill for comprehensive descriptions:

```bash
# Generate enhanced PR description
pr-analyzer

# Output includes:
# - Change statistics
# - Risk assessment
# - Test coverage analysis
# - Context-aware checklist
# - Performance impact analysis
```

See [PR Analyzer Skill](../skills/pr-analyzer/SKILL.md) for details.

## PR Size

Size matters for review quality and speed.

### Size Guidelines

| Size | Files | Lines | Review Time | Recommendation |
|------|-------|-------|-------------|----------------|
| Small | 1-5 | <200 | ~10 min | Ideal |
| Medium | 6-15 | 200-500 | ~30 min | Good |
| Large | 16-30 | 500-1000 | ~60 min | Consider splitting |
| Huge | 30+ | 1000+ | 2+ hours | Must split |

### Benefits of Small PRs

✓ Faster review
✓ Better focus
✓ Easier to test
✓ Lower risk
✓ Quicker iteration
✓ Easier to revert

### When to Split a PR

Split large PRs into smaller, logical units:

**Example - Authentication Feature**:

Instead of one huge PR:
```
feat(auth): implement complete authentication system (50 files, 2000 lines)
```

Split into smaller PRs:
```
1. feat(auth): add user domain and basic authentication
2. feat(auth): implement JWT token generation
3. feat(auth): add token refresh mechanism
4. feat(auth): implement OAuth2 integration
5. feat(auth): add authentication middleware
```

Each PR:
- Has clear scope
- Can be reviewed independently
- Can be deployed incrementally
- Reduces risk

### Exceptions

Large PRs acceptable for:
- Initial project setup
- Framework upgrades
- Generated code (Axelor domains)
- Large refactorings (with good description)
- Dependency updates

## Code Review

### For Authors

#### Before Requesting Review

- [ ] Self-review completed
- [ ] Tests passing locally
- [ ] CI checks passing
- [ ] Documentation updated
- [ ] No WIP commits

#### During Review

- Respond promptly to feedback
- Be open to suggestions
- Explain decisions clearly
- Update PR based on feedback
- Keep discussion professional

#### After Review

- Address all comments
- Update tests if needed
- Resolve conversations
- Request re-review
- Squash or clean up commits

### For Reviewers

#### Review Checklist

**General**:
- [ ] Purpose is clear
- [ ] Changes match description
- [ ] No unnecessary changes
- [ ] Code follows conventions

**Code Quality**:
- [ ] No code duplication
- [ ] Functions are focused
- [ ] Variable names are clear
- [ ] Complex logic is commented
- [ ] Error handling is adequate

**Testing**:
- [ ] Tests are included
- [ ] Tests cover main scenarios
- [ ] Edge cases are tested
- [ ] Tests are maintainable

**Security**:
- [ ] No hardcoded credentials
- [ ] Input validation present
- [ ] SQL injection prevented
- [ ] XSS vulnerabilities addressed

**Performance**:
- [ ] No N+1 queries
- [ ] Appropriate indexing
- [ ] Caching where beneficial
- [ ] No unnecessary loops

**Documentation**:
- [ ] Public APIs documented
- [ ] Complex logic explained
- [ ] README updated if needed

#### Review Best Practices

**Be Constructive**:
```
✗ Bad: "This is wrong"
✓ Good: "Consider using X pattern here for better readability"
```

**Ask Questions**:
```
✗ Bad: "Change this"
✓ Good: "Could we simplify this by...?"
```

**Praise Good Code**:
```
✓ "Great approach to handling this edge case"
✓ "Nice refactoring, much cleaner"
```

**Provide Context**:
```
✗ Bad: "Fix this"
✓ Good: "This could cause a race condition when multiple users access
simultaneously. Consider using a lock or transaction."
```

**Distinguish Blockers from Suggestions**:
```
BLOCKER: Missing null check will cause NPE
SUGGESTION: Consider extracting this to a helper method
NITPICK: Typo in comment
```

## Merging Strategy

### Squash and Merge (Recommended)

**When to use**: Feature branches, most PRs

**Benefits**:
- Clean main branch history
- One commit per feature
- MR title becomes commit message
- Easy to revert

**Process**:
```
Individual commits:
- wip: working on auth
- fix typo
- update tests
- final changes

After squash:
feat(auth): add JWT authentication
```

**GitLab Configuration**:
- Enable "Squash commits when merge request is accepted"
- Validate MR title (becomes commit message)

### Merge Commit

**When to use**: Complex features, long-running branches

**Benefits**:
- Preserves full history
- Shows all work
- Clear branch points

**Drawbacks**:
- Cluttered history
- Harder to follow

### Rebase and Merge

**When to use**: Clean commit history already exists

**Benefits**:
- Linear history
- Preserves individual commits
- No merge commit

**Requirements**:
- All commits follow conventions
- Each commit is atomic
- No fixup commits

## Common Pitfalls

### 1. Mixing Multiple Concerns

✗ **Bad** - PR does multiple things:
```
feat: add authentication, fix bugs, and update docs
- Add JWT authentication
- Fix order calculation bug
- Update README
- Refactor user service
```

✓ **Good** - Focused PRs:
```
PR 1: feat(auth): add JWT authentication
PR 2: fix(order): correct calculation logic
PR 3: docs: update README
PR 4: refactor(user): simplify user service
```

### 2. Incomplete Testing

✗ **Bad**:
```
"I tested it manually and it works"
```

✓ **Good**:
```
"Added unit tests covering:
- Happy path authentication
- Invalid credentials handling
- Token expiration scenario
- Edge cases for empty/null inputs

All tests passing with 95% coverage."
```

### 3. Missing Context

✗ **Bad** PR description:
```
Fixed the bug
```

✓ **Good** PR description:
```
fix(order): resolve incorrect tax calculation

Fixed issue where tax was calculated on discounted price instead of
original price. Now correctly applies discount after tax calculation.

Steps to reproduce bug:
1. Create order with 10% discount
2. Add 20% tax
3. Observe incorrect total

After fix:
- Tax calculated on original price
- Discount applied after tax
- Total matches expected value

Fixes #123
```

### 4. Ignoring Review Feedback

✗ **Bad**:
```
"I disagree" (without explanation)
*Merges without addressing*
```

✓ **Good**:
```
"I see your point. I initially chose X because of Y, but your suggestion
of Z is better because... I'll update the PR."

OR

"I understand your concern about performance, but after profiling
(results attached), this approach is actually faster. Happy to discuss
further if you have concerns."
```

### 5. Leaving Debug Code

✗ **Bad**:
```java
public void processOrder(Order order) {
    System.out.println("DEBUG: Order ID = " + order.getId());
    // TODO: Fix this later
    // Old implementation commented out
    // if (order.getTotal() > 1000) {
    //     ...
    // }
}
```

✓ **Good**:
```java
public void processOrder(Order order) {
    logger.debug("Processing order: {}", order.getId());
    // Clean, production-ready code
}
```

## Automation

### PR Analyzer Skill

Generate comprehensive PR descriptions:

```bash
# Analyze changes
pr-analyzer

# Output includes:
# - Statistics (files, lines, net change)
# - Risk assessment (size, complexity, coverage)
# - File categorization
# - Test coverage analysis
# - Review checklist
# - Breaking changes detection
```

### GitLab CI Integration

Automated checks on every PR:

```yaml
stages:
  - init      # Validate MR title, conventional commits
  - build     # Compile code
  - test      # Run tests, coverage
  - quality   # Code quality, security scans
```

**Init Stage**:
- MR title validation (conventional commits)
- Commit message validation (all commits)
- Squash commits enforcement

**Build Stage**:
- Compilation
- Dependency resolution
- Artifact creation

**Test Stage**:
- Unit tests
- Integration tests
- Code coverage (minimum threshold)

**Quality Stage**:
- SonarQube analysis
- Security scanning
- Dependency vulnerability check

### Required Checks

Before merge, ensure:
- [ ] All CI stages pass
- [ ] MR title is valid
- [ ] All commits follow conventions
- [ ] Squash commits enabled
- [ ] Minimum 1 approval (or more for high-risk)
- [ ] No unresolved conversations

## Examples

### Example 1: Small Feature PR

**Title**: `feat(sale): add order status field`

**Description**:
```markdown
## Summary
Add status field to SaleOrder domain to track order lifecycle.

## What Changed
- Added status enum (DRAFT, CONFIRMED, DELIVERED, CANCELLED)
- Updated SaleOrder domain with status field
- Modified order form view to display status
- Added status transition validation

## Type of Change
- [x] New feature (feat)

## How Has This Been Tested?
- Unit tests for status transitions
- Integration tests for order lifecycle
- Manual testing of UI updates

## Breaking Changes
None

## Related Issues
Closes #42
```

### Example 2: Bug Fix PR

**Title**: `fix(invoice): resolve null pointer in payment processing`

**Description**:
```markdown
## Summary
Fix NPE that occurs when processing payment without payment method
selected.

## What Changed
- Added null check for payment method in PaymentService
- Added validation error message for missing payment method
- Updated tests to cover null payment method scenario

## Type of Change
- [x] Bug fix (fix)

## How Has This Been Tested?
1. Attempt to process payment without selecting method
2. Verify error message displayed
3. Verify no NPE thrown
4. Added unit test for null payment method

## Root Cause
Payment method was optional in UI but code assumed it was always present.

## Fix
Added validation at service layer to check for null payment method
before processing.

## Related Issues
Fixes #234
```

### Example 3: Large Refactoring PR

**Title**: `refactor(api): extract service layer from controllers`

**Description**:
```markdown
## Summary
Extract business logic from REST controllers to dedicated service layer.
Improves testability and separation of concerns.

## What Changed
- Created 8 new service classes
- Moved business logic from controllers to services
- Updated controllers to use services
- Added unit tests for services
- Updated integration tests

## Type of Change
- [x] Refactoring (refactor)

## How Has This Been Tested?
- All existing tests still pass
- Added 45 new unit tests for services
- Integration tests verify same behavior
- Manual smoke testing of all endpoints

## Risk Assessment
- **Risk Level**: Medium
- **Size**: 28 files, 1200 lines net
- **Test Coverage**: +8% (now 85%)
- **Breaking Changes**: None (internal refactoring)

## Performance Impact
Negligible - added one layer but simplified logic overall.

## Review Guidance
Focus on:
1. Service layer design and patterns
2. Test coverage for new services
3. Controller simplification

## Related Issues
Related to #89 (technical debt reduction)
```

## Summary

Good pull requests:

- **Clear title**: Follows conventional commits
- **Comprehensive description**: Context, changes, testing
- **Appropriate size**: Small enough to review effectively
- **Well-tested**: Tests included and passing
- **CI-validated**: All checks passing
- **Documented**: Code and architecture docs updated
- **Reviewed**: Feedback addressed professionally

Follow these guidelines for efficient code review and high-quality codebase.

## References

- [Conventional Commits](./conventional-commits.md)
- [PR Analyzer Skill](../skills/pr-analyzer/SKILL.md)
- [MR Title Validator Skill](../skills/mr-title-validator/SKILL.md)
- [GitLab CI Patterns](../docs/cicd/gitlab-ci-patterns.md)
