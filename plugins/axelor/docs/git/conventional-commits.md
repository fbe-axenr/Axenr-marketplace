# Conventional Commits Guide

Complete guide to conventional commits specification for Axelor projects.

## Table of Contents

1. [Overview](#overview)
2. [Format Specification](#format-specification)
3. [Commit Types](#commit-types)
4. [Scope Guidelines](#scope-guidelines)
5. [Subject Guidelines](#subject-guidelines)
6. [Body Guidelines](#body-guidelines)
7. [Footer Guidelines](#footer-guidelines)
8. [Examples](#examples)
9. [Best Practices](#best-practices)
10. [Tools and Automation](#tools-and-automation)

## Overview

Conventional commits provide a standard format for commit messages that:
- Enables automated changelog generation
- Supports semantic versioning
- Improves commit readability
- Facilitates collaboration
- Enables automated release management

### Why Conventional Commits?

**Without conventional commits**:
```
Fixed bug
Updated files
WIP
misc changes
```

**With conventional commits**:
```
fix(auth): resolve token expiration issue
feat(order): add discount calculation
docs(readme): update installation instructions
refactor(api): extract service layer
```

Clear, semantic, and processable by automation tools.

## Format Specification

### Basic Format

```
<type>[optional scope]: <subject>

[optional body]

[optional footer(s)]
```

### Components

1. **Type**: Required - Describes the category of change
2. **Scope**: Optional - Indicates the area/module affected
3. **Subject**: Required - Brief description of the change
4. **Body**: Optional - Detailed explanation
5. **Footer**: Optional - Breaking changes, issue references

### Rules

- Type must be lowercase
- Scope must be lowercase, in parentheses
- Subject must start with lowercase, no trailing period
- Blank line between subject and body
- Blank line between body and footer
- Header (type + scope + subject) max 100 characters
- Body lines max 100 characters
- No emojis
- English only

## Commit Types

### feat - New Feature

A new feature or functionality added to the codebase.

**When to use**:
- Adding new domain models
- Creating new views (forms, grids)
- Implementing new services
- Adding new API endpoints
- Introducing new business logic

**Examples**:
```
feat(sale): add SaleOrder domain and views
feat(product): implement product catalog search
feat(api): add order export endpoint
feat(auth): implement JWT authentication
```

**Semantic Versioning**: Triggers MINOR version bump (1.x.0)

### fix - Bug Fix

A bug fix that corrects unintended behavior.

**When to use**:
- Fixing calculation errors
- Correcting validation logic
- Resolving runtime errors
- Fixing UI issues
- Addressing data inconsistencies

**Examples**:
```
fix(sale): correct total calculation for discounts
fix(invoice): resolve null pointer in payment processing
fix(ui): prevent duplicate form submissions
fix(validation): handle empty string in date field
```

**Semantic Versioning**: Triggers PATCH version bump (1.0.x)

### refactor - Code Refactoring

Code restructuring without changing external behavior.

**When to use**:
- Extracting methods or services
- Reorganizing package structure
- Improving code organization
- Optimizing existing logic
- Renaming for clarity

**Examples**:
```
refactor(sale): extract computation logic to service
refactor(product): reorganize package structure
refactor(api): simplify controller methods
refactor(db): optimize query structure
```

**Semantic Versioning**: No version bump (internal change)

### docs - Documentation

Documentation only changes, no code changes.

**When to use**:
- Updating README
- Adding/updating code comments
- Writing architecture documentation
- Creating user guides
- Updating API documentation

**Examples**:
```
docs(readme): update installation instructions
docs(api): add endpoint documentation
docs(architecture): document service layer design
docs(domain): add field descriptions
```

**Semantic Versioning**: No version bump

### test - Tests

Adding or updating tests.

**When to use**:
- Adding unit tests
- Creating integration tests
- Updating test fixtures
- Adding test utilities
- Improving test coverage

**Examples**:
```
test(sale): add unit tests for order computation
test(auth): add integration tests for login flow
test(api): update test fixtures for products
test(service): add edge case tests
```

**Semantic Versioning**: No version bump

### build - Build System

Changes to build system or external dependencies.

**When to use**:
- Updating Gradle configuration
- Modifying Maven POM
- Updating npm packages
- Changing build scripts
- Modifying compiler options

**Examples**:
```
build(gradle): update Axelor framework to 7.0.0
build(deps): bump spring-boot to 3.2.0
build(maven): configure multi-module project
build(npm): update react dependencies
```

**Semantic Versioning**: No version bump

### ci - CI/CD Configuration

Changes to CI/CD pipeline configuration.

**When to use**:
- Updating GitLab CI configuration
- Modifying Jenkins pipelines
- Adding CI checks
- Configuring deployment
- Adding quality gates

**Examples**:
```
ci(gitlab): add sonarqube integration
ci(pipeline): configure automated deployment
ci(quality): add test coverage check
ci(commitlint): enforce conventional commits
```

**Semantic Versioning**: No version bump

### chore - Maintenance

Other changes that don't modify src or test files.

**When to use**:
- Updating .gitignore
- Cleaning up unused files
- Updating configuration files
- Routine maintenance tasks
- Dependency updates (non-breaking)

**Examples**:
```
chore(gitignore): add build artifacts
chore(config): update IDE settings
chore(deps): update dev dependencies
chore(cleanup): remove unused imports
```

**Semantic Versioning**: No version bump

### style - Code Style

Code style/formatting changes with no functional impact.

**When to use**:
- Formatting code
- Fixing indentation
- Organizing imports
- Applying linter fixes
- Consistent spacing

**Examples**:
```
style(sale): format code with prettier
style(java): fix indentation
style(imports): organize import statements
style(whitespace): remove trailing spaces
```

**Semantic Versioning**: No version bump

### perf - Performance

Performance improvements without changing functionality.

**When to use**:
- Optimizing database queries
- Reducing memory usage
- Improving algorithm efficiency
- Adding caching
- Reducing load times

**Examples**:
```
perf(db): optimize product search query
perf(cache): add Redis caching for orders
perf(algorithm): improve sorting efficiency
perf(lazy): add lazy loading for relations
```

**Semantic Versioning**: No version bump (unless breaking change)

### revert - Revert

Reverting a previous commit.

**When to use**:
- Rolling back a problematic commit
- Undoing experimental changes
- Reverting broken features

**Examples**:
```
revert: revert "feat(auth): add biometric login"
revert(api): revert experimental caching
```

**Format**: Include "revert: " prefix and reference to reverted commit

**Semantic Versioning**: Depends on reverted commit

## Scope Guidelines

The scope provides additional context about which part of the codebase is affected.

### Module-Based Scopes

For Axelor projects, use module names:

```
sale, purchase, crm, hr, stock, invoice, product, customer, order, payment
```

**Examples**:
```
feat(sale): add order management
fix(purchase): correct supplier validation
refactor(crm): simplify contact service
```

### Feature-Based Scopes

Use feature names for cross-module changes:

```
auth, api, ui, db, config, search, export, import, workflow
```

**Examples**:
```
feat(auth): implement OAuth2
fix(api): handle rate limiting
perf(db): optimize query performance
```

### Component-Based Scopes

Use component types for specific changes:

```
domain, view, service, controller, repository, model, dto
```

**Examples**:
```
feat(domain): add SaleOrder entity
fix(service): correct calculation logic
refactor(controller): simplify REST endpoints
```

### Multiple Scopes

For changes affecting multiple areas, choose the primary scope:

```
# Good
feat(sale): add order discount (even if affects multiple files)

# Avoid (too general)
feat(sale,product,customer): update entities
```

### No Scope

Omit scope for truly global changes:

```
docs: update README
chore: update gitignore
build: upgrade framework version
```

## Subject Guidelines

The subject is a brief description of the change.

### Rules

1. **Start with lowercase**: `add feature`, not `Add feature`
2. **Use imperative mood**: `add`, not `added` or `adding`
3. **No trailing period**: `add feature`, not `add feature.`
4. **Be specific**: `add order discount calculation`, not `add feature`
5. **Maximum 72 characters**: Keep it concise
6. **No emojis**: Professional tone only

### Good Subjects

```
add user authentication
resolve login timeout issue
implement discount calculation
update installation guide
extract service layer
optimize database queries
```

### Bad Subjects

```
Added feature           (not imperative, vague)
Fix bug.                (period, not specific)
Updated files           (too vague)
WIP                     (not descriptive)
misc changes            (meaningless)
Add Feature             (capitalized)
add feature ✨          (emoji)
```

### Imperative Mood Guide

| ✓ Correct | ✗ Incorrect |
|-----------|-------------|
| add | added, adding |
| fix | fixed, fixing |
| update | updated, updating |
| remove | removed, removing |
| implement | implemented, implementing |
| refactor | refactored, refactoring |
| optimize | optimized, optimizing |

## Body Guidelines

The body provides additional context about the change.

### When to Include a Body

- Complex changes requiring explanation
- Non-obvious implementation decisions
- Important context for reviewers
- Breaking changes explanation
- Migration instructions

### Rules

1. **Separate from subject**: Blank line after subject
2. **Wrap at 72 characters**: Each line max 72 chars
3. **Explain WHAT and WHY**: Not HOW (code shows how)
4. **Multiple paragraphs**: Separate with blank lines
5. **No emojis**: Professional tone
6. **Maximum 2 sentences**: Keep it concise

### Examples

**Simple commit (no body needed)**:
```
feat(sale): add order status field
```

**Complex commit (body helpful)**:
```
feat(sale): implement complex discount calculation

Added support for tiered discounts based on order quantity and customer
loyalty level. Discounts are calculated before tax and cumulative.
```

**Breaking change (body essential)**:
```
feat(api): redesign order endpoint

Changed order endpoint from GET /order/:id to GET /api/v2/orders/:id.
Updated response format to include nested customer data.

BREAKING CHANGE: Old endpoint will be removed in v2.0.0
```

## Footer Guidelines

The footer contains metadata about the commit.

### Breaking Changes

Use `BREAKING CHANGE:` footer for breaking changes:

```
feat(api): redesign authentication

BREAKING CHANGE: JWT tokens now expire after 1 hour instead of 24 hours.
Update all clients to handle token refresh.
```

**Semantic Versioning**: Triggers MAJOR version bump (x.0.0)

### Issue References

Reference related issues:

```
fix(sale): correct total calculation

Fixes #123
Related to #45, #67
```

**Common keywords**:
- `Fixes #123` - Closes the issue
- `Closes #123` - Closes the issue
- `Resolves #123` - Closes the issue
- `Related to #123` - References without closing
- `See #123` - References without closing

### Multiple Footers

Combine multiple footers:

```
feat(auth): implement OAuth2

BREAKING CHANGE: Basic auth is no longer supported.
Migrate to OAuth2 before upgrading.

Fixes #89
Related to #12
```

## Examples

### Simple Feature Addition

```
feat(sale): add order status field
```

### Feature with Scope and Details

```
feat(product): implement product catalog search

Added full-text search for products with filtering by category, price
range, and availability. Implemented using Elasticsearch integration.
```

### Bug Fix

```
fix(invoice): resolve null pointer in payment processing

Added null check for payment method before processing. Prevents NPE
when payment method is not selected.

Fixes #234
```

### Refactoring

```
refactor(sale): extract computation logic to service

Moved order total computation from SaleOrderController to
SaleOrderComputeService. Improves testability and separation of
concerns.
```

### Documentation

```
docs(architecture): add service layer design documentation

Documented service layer architecture with class diagrams and
interaction flows. Includes patterns and best practices.
```

### Breaking Change

```
feat(api): redesign order endpoint structure

Changed endpoint from GET /order/:id to GET /api/v2/orders/:id.
Response format now includes nested customer and product data.

BREAKING CHANGE: Old endpoint structure removed. Update API clients to
use new v2 endpoints before upgrading.

Fixes #156
```

### Chore

```
chore(deps): update Axelor framework to 7.0.0

Updated Axelor framework and related dependencies. No breaking changes
in our usage.
```

### Multiple Files, Single Purpose

```
feat(sale): add order discount functionality

Implemented discount functionality with percentage and fixed amount
options. Updated domain model, views, service layer, and validation.

Closes #42
```

## Best Practices

### 1. Atomic Commits

Each commit should represent a single logical change:

✓ **Good**:
```
feat(sale): add discount field
feat(sale): implement discount calculation
feat(sale): add discount validation
```

✗ **Bad**:
```
feat(sale): add discount (combines 3 changes in one commit)
```

### 2. Commit Often

Commit frequently with small, focused changes:

- Easier to review
- Easier to revert
- Better git history
- Clearer change progression

### 3. Write for Others

Commit messages are for your team:

- Be clear and descriptive
- Provide context
- Explain non-obvious decisions
- Think: "Will this be clear in 6 months?"

### 4. Test Before Committing

Ensure code works before committing:

```bash
# Run tests
./gradlew test

# Check formatting
./gradlew spotlessCheck

# Verify build
./gradlew build

# Then commit
git commit -m "feat(sale): add order discount"
```

### 5. Use Interactive Staging

Stage only related changes:

```bash
# Stage specific files
git add src/main/java/SaleOrder.java
git add src/main/resources/views/SaleOrder.xml

# Not everything at once
git add .  # Avoid this
```

### 6. Review Before Pushing

Review commits before pushing:

```bash
# Review recent commits
git log -3 --oneline

# Check diff
git show HEAD

# Amend if needed (before push)
git commit --amend
```

## Tools and Automation

### Commitlint

Validates commit messages:

```bash
# Install
npm install --save-dev @commitlint/cli @commitlint/config-conventional

# Configure (.commitlintrc.json)
{
  "extends": ["@commitlint/config-conventional"]
}

# Use
echo "feat: add feature" | commitlint
```

### Git Hooks

Automate validation:

```bash
# .husky/commit-msg
#!/bin/sh
npx commitlint --edit $1
```

### GitLab CI

Validate in CI pipeline:

```yaml
commitlint:
  stage: init
  script:
    - npx commitlint --from=origin/main
  only:
    - merge_requests
```

### Git Cliff

Generate changelogs:

```bash
# Install
cargo install git-cliff

# Generate changelog
git-cliff --output CHANGELOG.md

# Preview
git-cliff --unreleased
```

### Standard Version

Automate versioning:

```bash
# Install
npm install --save-dev standard-version

# Bump version and generate changelog
npx standard-version

# First release
npx standard-version --first-release
```

## Integration with Axelor Workflow

### After Code Generation

```bash
# Generated Axelor components
git add axelor-sale/src/main/java/com/axelor/apps/sale/db/SaleOrder.java
git add axelor-sale/src/main/resources/domains/SaleOrder.xml
git add axelor-sale/src/main/resources/views/SaleOrder.xml

git commit -m "$(cat <<'EOF'
feat(sale): add SaleOrder domain and views

Implemented SaleOrder domain model with customer, order lines, and total
fields. Created form and grid views for order management.
EOF
)"
```

### After Refactoring

```bash
git commit -m "$(cat <<'EOF'
refactor(sale): extract computation logic to service

Moved order total computation from SaleOrderController to
SaleOrderComputeService. Improves testability and follows service layer
pattern.
EOF
)"
```

### After Bug Fix

```bash
git commit -m "$(cat <<'EOF'
fix(sale): correct total calculation for discounted items

Fixed issue where discount percentage was applied incorrectly. Now
properly calculates discounted price before computing order total.

Fixes #67
EOF
)"
```

## Common Mistakes to Avoid

### 1. Vague Messages

✗ **Bad**:
```
fix: bug fix
update: changes
misc: updates
```

✓ **Good**:
```
fix(auth): resolve token expiration issue
refactor(api): simplify user service
chore(deps): update spring-boot to 3.2.0
```

### 2. Multiple Changes in One Commit

✗ **Bad**:
```
feat: add authentication and fix bugs and update docs
```

✓ **Good**:
```
feat(auth): add user authentication
fix(login): resolve timeout issue
docs(auth): add authentication guide
```

### 3. Wrong Type

✗ **Bad**:
```
feat: fix bug in calculation
chore: add new feature
```

✓ **Good**:
```
fix: correct calculation logic
feat: add new feature
```

### 4. Poor Subject Format

✗ **Bad**:
```
feat: Added Feature.
feat: adding feature
feat: Feature Added
```

✓ **Good**:
```
feat: add feature
```

### 5. Missing Breaking Change Notice

✗ **Bad**:
```
feat(api): change endpoint structure
```

✓ **Good**:
```
feat(api): change endpoint structure

BREAKING CHANGE: Endpoint URLs have changed. Update all API clients.
```

## Summary

Conventional commits provide structure and meaning to your git history:

- **Automated changelog**: Generate changelogs automatically
- **Semantic versioning**: Determine version bumps automatically
- **Clear history**: Understand changes at a glance
- **Better collaboration**: Team knows what changed and why
- **Tooling support**: Many tools built around this standard

Follow the format consistently for maximum benefit.

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Commitlint](https://commitlint.js.org/)
- [Git Cliff](https://git-cliff.org/)
- [Standard Version](https://github.com/conventional-changelog/standard-version)
