# Git & CI/CD Quick Start Guide

Quick reference guide for using the Axelor Git & CI/CD Manager with conventional commits and automated workflows.

## Table of Contents

1. [Quick Reference](#quick-reference)
2. [Common Workflows](#common-workflows)
3. [Agent Usage](#agent-usage)
4. [Cheat Sheet](#cheat-sheet)
5. [Troubleshooting](#troubleshooting)

## Quick Reference

### Conventional Commits Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Commit Types

| Type | Usage | Example |
|------|-------|---------|
| `feat` | New feature | `feat(sale): add order discount` |
| `fix` | Bug fix | `fix(auth): resolve token expiration` |
| `refactor` | Code restructure | `refactor(api): simplify endpoints` |
| `docs` | Documentation | `docs(readme): update installation` |
| `test` | Tests | `test(order): add unit tests` |
| `chore` | Maintenance | `chore(deps): update dependencies` |
| `style` | Formatting | `style: format code` |
| `perf` | Performance | `perf(db): optimize queries` |
| `build` | Build system | `build: update gradle` |
| `ci` | CI/CD | `ci: add quality gate` |

### Rules

- ✓ Type must be lowercase
- ✓ Scope is optional but recommended
- ✓ Subject starts with lowercase
- ✓ No trailing period
- ✓ Maximum 100 characters for header
- ✓ English only, no emojis

## Common Workflows

### Workflow 1: Simple Commit

**Scenario**: You've made changes and want to commit.

```bash
# 1. Check what changed
git status
git diff

# 2. Call the agent
# "I've made changes to SaleOrder domain and want to commit"

# Agent will:
# - Use file-safety-checker to validate files
# - Help you stage appropriate files
# - Use commitlint-validator to validate message
# - Create properly formatted commit

# Result: Clean conventional commit ready to push
```

### Workflow 2: Creating a Pull Request

**Scenario**: Feature complete, ready to create PR.

```bash
# 1. Ensure all committed
git status

# 2. Call the agent
# "I want to create a PR for my authentication feature"

# Agent will:
# - Use pr-analyzer to generate comprehensive description
# - Calculate risk assessment
# - Generate review checklist
# - Use mr-title-validator to validate title
# - Help create PR with gh CLI

# Result: Professional PR with full analysis
```

### Workflow 3: Fixing CI Failure

**Scenario**: CI failed on commitlint check.

```bash
# 1. Call the agent
# "My CI commitlint check failed, can you help fix it?"

# Agent will:
# - Check which commits failed
# - Use commitlint-validator to show correct format
# - Guide you through rebase to fix messages
# - Verify fixes before push

# Result: All commits pass conventional commits validation
```

### Workflow 4: Multiple Commits

**Scenario**: You want to split your work into multiple logical commits.

```bash
# Call the agent
# "I've added authentication and fixed a bug, need to commit separately"

# Agent will:
# - Analyze changes
# - Help stage files for first commit (feat)
# - Create first commit
# - Stage remaining files for second commit (fix)
# - Create second commit
# - Both using proper conventional format

# Result: Two clean, atomic commits
```

## Agent Usage

### Invoking the Agent

```bash
# In your Axelor project
# Simply describe what you want to do

Examples:
"Commit my changes to the sale order module"
"Create a PR for the authentication feature"
"I need to fix my commit message format"
"Help me stage files safely"
```

### Agent Capabilities

**Git Operations**:
- ✓ Status checking and analysis
- ✓ Safe file staging (with validation)
- ✓ Conventional commit creation
- ✓ Commit message validation
- ✓ Branch management
- ✓ PR/MR creation with analysis
- ✓ Push to remote

**Skills Orchestration**:
- ✓ file-safety-checker: Validates files before staging
- ✓ commitlint-validator: Validates commit messages
- ✓ pr-analyzer: Generates comprehensive PR descriptions
- ✓ mr-title-validator: Validates MR/PR titles

**CI/CD Integration**:
- ✓ Understands quality gates
- ✓ Ensures commits will pass CI
- ✓ Validates MR titles
- ✓ Verifies squash commits

### What the Agent Does Automatically

1. **File Safety Checks**: Prevents committing:
   - Build artifacts (build/, *.class)
   - IDE configs (.idea/, *.iml)
   - Sensitive data (.env, *.pem)
   - OS files (.DS_Store)

2. **Commit Validation**: Ensures:
   - Proper type (feat, fix, etc.)
   - Correct format
   - No emojis
   - Appropriate length

3. **PR Enhancement**: Generates:
   - Statistics and metrics
   - Risk assessment
   - File categorization
   - Review checklists
   - Test coverage analysis

4. **CI/CD Verification**: Confirms:
   - Commits pass commitlint
   - MR title is valid
   - Tests will likely pass
   - Format is correct

## Cheat Sheet

### Commit Message Templates

**New Feature**:
```
feat(module): add specific feature

Brief explanation of what was added and why it's needed.
```

**Bug Fix**:
```
fix(module): resolve specific issue

Explanation of the bug and how it was fixed.

Fixes #123
```

**Refactoring**:
```
refactor(module): improve specific aspect

Explanation of what was reorganized and why.
```

**Documentation**:
```
docs(section): update specific content

What was updated and why.
```

### Git Commands Reference

```bash
# Check status
git status

# View changes
git diff                    # Unstaged changes
git diff --staged           # Staged changes
git diff main...HEAD        # All branch changes

# Stage files
git add <file>              # Specific file
git add <directory>         # Directory
git add .                   # All (use carefully!)

# Unstage files
git reset HEAD <file>       # Unstage specific file
git reset HEAD .            # Unstage all

# Commit
git commit -m "type(scope): subject"

# View history
git log                     # Full history
git log --oneline          # Compact history
git log -3                 # Last 3 commits

# Amend last commit (before push)
git commit --amend

# Push
git push                    # Push current branch
git push -u origin branch   # Push and set upstream

# Branch management
git branch                  # List branches
git checkout -b feature/name  # Create and switch
git checkout main           # Switch branch
```

### File Patterns to Exclude

**Build Artifacts**:
```
build/
target/
bin/
*.class
*.jar
.gradle/
node_modules/
```

**IDE Configurations**:
```
.idea/
*.iml
.vscode/
.settings/
```

**Sensitive Data**:
```
.env
.env.*
credentials.*
secrets.*
*.pem
*.key
```

**OS Files**:
```
.DS_Store
Thumbs.db
```

### CI/CD Quality Gates

**Init Stage** (BLOCKING):
- ✓ Commitlint validation
- ✓ MR title validation
- ✓ Squash commits check

**Build Stage**:
- ✓ Compilation
- ✓ Artifact generation

**Test Stage**:
- ✓ Unit tests
- ✓ Code coverage (≥80%)
- ✓ Code formatting

**Quality Stage**:
- ✓ SonarQube analysis
- ✓ Security scanning

## Troubleshooting

### Problem: "My commit was rejected by CI"

**Solution**:
```bash
# Ask the agent:
"My commit failed CI validation, can you help?"

# Agent will check and fix commit messages
```

### Problem: "I accidentally committed build artifacts"

**Solution**:
```bash
# If not pushed yet:
git reset --soft HEAD~1   # Undo commit, keep changes
# Call agent to properly stage files

# If already pushed:
# Call agent:
"I need to remove build artifacts from my last commit"
```

### Problem: "I need to change my last commit message"

**Solution**:
```bash
# If not pushed:
git commit --amend

# If pushed to feature branch:
git commit --amend
git push --force-with-lease

# Call agent for help:
"I need to fix my last commit message"
```

### Problem: "My MR title is invalid"

**Solution**:
```bash
# Call agent:
"Validate my MR title: Add authentication feature"

# Agent uses mr-title-validator skill
# Provides: "feat(auth): add authentication feature"

# Update MR title in GitLab UI
```

### Problem: "I don't know which commit type to use"

**Solution**:
```bash
# Call agent:
"I added a new field to SaleOrder, what commit type should I use?"

# Agent will analyze and recommend:
# - feat: if it's a new feature
# - fix: if it's fixing a bug
# - refactor: if it's restructuring
# etc.
```

### Problem: "Code formatted incorrectly"

**Solution**:
```bash
# Run spotless
./gradlew spotlessApply

# Stage and commit
git add .
git commit -m "style: format code with spotless"
```

## Best Practices

### Do's

✓ **Commit often**: Small, focused commits
✓ **Use agent**: Let it validate and guide
✓ **Test first**: Run tests before committing
✓ **Review diffs**: Check what you're committing
✓ **Write clear messages**: Be specific and concise
✓ **Follow conventions**: Always use conventional commits
✓ **Enable squash**: Clean git history

### Don'ts

✗ **Don't commit build artifacts**: Use file-safety-checker
✗ **Don't use emojis**: Professional commits only
✗ **Don't be vague**: "fix bug" → "fix(auth): resolve token expiration"
✗ **Don't skip validation**: Always use commitlint-validator
✗ **Don't commit everything**: Stage specific files
✗ **Don't force push to main**: Only on feature branches
✗ **Don't ignore CI failures**: Fix issues promptly

## Quick Examples

### Example 1: Feature Commit

```bash
# Changes: Added discount field to SaleOrder

# Call agent:
"Commit my sale order discount changes"

# Agent creates:
feat(sale): add order discount field

Added discount field to SaleOrder domain with percentage and fixed
amount options. Updated form view and validation rules.
```

### Example 2: Bug Fix Commit

```bash
# Changes: Fixed null pointer in payment service

# Call agent:
"Commit my payment bug fix"

# Agent creates:
fix(payment): resolve null pointer in payment processing

Added null check for payment method before processing to prevent NPE.

Fixes #234
```

### Example 3: Creating PR

```bash
# Feature complete on feature/auth-jwt branch

# Call agent:
"Create PR for my JWT authentication feature"

# Agent:
# 1. Uses pr-analyzer to generate description
# 2. Validates MR title with mr-title-validator
# 3. Creates PR:
#    Title: feat(auth): add JWT authentication
#    Body: [Comprehensive description with analysis]
```

## Summary

**To commit changes**:
1. Call agent: "Commit my changes"
2. Agent validates files and message
3. Clean conventional commit created

**To create PR**:
1. Call agent: "Create PR for [feature]"
2. Agent generates comprehensive description
3. Professional PR ready for review

**To fix CI issues**:
1. Call agent: "Fix my CI failure"
2. Agent diagnoses and guides fixes
3. Pipeline passes

**Key Points**:
- Always use the agent for git operations
- Let skills validate automatically
- Follow conventional commits strictly
- Test before committing
- Keep commits atomic and focused

## References

- [Conventional Commits Full Guide](./conventional-commits.md)
- [PR Guidelines](./pr-guidelines.md)
- [CI/CD Patterns](../cicd/gitlab-ci-patterns.md)
- [Agent Documentation](../../agents/axelor-git-cicd-manager.md)
- [Skills Documentation](../../skills/)

**Need Help?** Call the axelor-git-cicd-manager agent and describe what you need!
