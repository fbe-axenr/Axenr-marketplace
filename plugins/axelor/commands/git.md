---
description: Quick access to Git operations with automated validation through git-agent agent
argument-hint: <git-request>
skills:
  - file-safety-checker
  - commitlint-validator
  - pr-analyzer
  - mr-title-validator
---

# Git Command

Invoke the **git-agent** agent for all Git operations with automated validation through specialized skills.

## Usage

Use `/git` followed by your request:

```
/git commit my changes
/git create a PR for my authentication feature
/git push my changes
/git help me fix my commit message
/git stage files safely
```

## What This Does

This command directly invokes the **@agents/git-agent** agent which:

✅ **Validates files** before staging (file-safety-checker skill)
✅ **Validates commit messages** (commitlint-validator skill)
✅ **Generates comprehensive PR descriptions** (pr-analyzer skill)
✅ **Validates MR titles** (mr-title-validator skill)
✅ **Ensures conventional commits** format
✅ **Asks confirmation** before creating MR/PR

## Common Examples

### Commit Changes

```
/git commit my changes to the sale module
```

Agent will:
1. Check git status
2. Use file-safety-checker to validate files
3. Stage safe files
4. Use commitlint-validator to validate message
5. Create conventional commit
6. Verify commit

### Create Pull Request

```
/git create a PR for my authentication feature
```

Agent will:
1. Verify all changes committed
2. Use pr-analyzer to generate comprehensive description
3. Use mr-title-validator to validate title
4. Present validation summary
5. **Ask confirmation**: "Do you want to create this Merge Request? (yes/no)"
6. Create MR only if confirmed

### Push Changes

```
/git push my changes
```

Agent will:
1. Perform pre-push checks
2. Verify branch name
3. Check commits
4. Push safely

### Fix Commit Message

```
/git fix my commit message format
```

Agent will:
1. Use commitlint-validator to identify issues
2. Guide through rebase
3. Help reword commits
4. Validate new messages

### Stage Files Safely

```
/git stage files safely
```

Agent will:
1. Use file-safety-checker to validate all files
2. Identify unsafe files (artifacts, IDE, secrets)
3. Stage only safe files
4. Update .gitignore if needed

## Features

### Automated Validation

Every operation is validated through specialized skills:

- **file-safety-checker**: Prevents committing build artifacts, IDE configs, sensitive data
- **commitlint-validator**: Ensures conventional commits format
- **pr-analyzer**: Generates comprehensive PR descriptions with risk assessment
- **mr-title-validator**: Validates MR titles for CI compliance

### User Confirmation

Agent **ALWAYS asks** before creating MR/PR:
- Presents full validation summary
- Shows risk assessment
- Requests explicit "yes" or "no"
- Respects user decision

### Professional Commits

All commits follow conventional commits specification:
- Proper type (feat, fix, refactor, etc.)
- Correct format
- No emojis
- English only
- Maximum 2 sentences in body

## When NOT to Use

❌ **CI/CD Infrastructure Setup**: Use `cicd-agent` agent instead
❌ **Pipeline Troubleshooting**: Use `cicd-agent` agent instead

Use `/git` only for Git operations (commit, push, PR, branch management).

## See Also

- **@agents/git-agent**: Full agent documentation
- **@docs/git/quick-start-guide.md**: Quick reference guide
- **@docs/git/conventional-commits.md**: Commit format specification
- **@docs/git/pr-guidelines.md**: Pull request best practices

## Examples in Context

### Daily Development Workflow

```
# Morning: Start working on feature
/git create branch for sale discount feature

# During development: Regular commits
/git commit add discount field to SaleOrder
/git commit implement discount calculation
/git commit add discount validation

# End of day: Push progress
/git push changes

# Feature complete: Create PR
/git create PR for sale discount feature
```

### Fixing Issues

```
# Commit message wrong format
/git fix my last commit message

# Accidentally staged wrong files
/git unstage build artifacts

# Need to rebase
/git help me rebase my commits
```

## Quick Tips

💡 **Be natural**: Describe what you want in natural language
💡 **Trust the agent**: It will use appropriate skills automatically
💡 **Always confirm**: Agent will ask before creating MRs
💡 **Safe by default**: File safety checks prevent common mistakes
💡 **CI-ready**: Commits will pass CI validation

For detailed guidance, see @docs/git/quick-start-guide.md
