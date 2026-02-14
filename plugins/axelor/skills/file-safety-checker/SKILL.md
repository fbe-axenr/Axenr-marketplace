---
name: file-safety-checker
description: Validates files before staging to prevent committing build artifacts, IDE configurations, sensitive data, and merge conflicts.
user-invocable: false
allowed-tools:
  - Bash
  - Read
  - Grep
---

# File Safety Checker

## Mission

Validate files before git staging to ensure no build artifacts, IDE configurations, sensitive data, or merge conflicts are committed. Prevents common mistakes that pollute Git history and expose sensitive information.

## Safety Checks

1. **Build Artifacts**: Detect compiled code, build outputs, caches
2. **IDE Configurations**: Identify IDE-specific files and settings
3. **Sensitive Data**: Find credentials, secrets, environment variables
4. **Merge Conflicts**: Detect unresolved conflict markers
5. **OS-Specific Files**: Identify operating system artifacts
6. **Gitignore Compliance**: Verify files respect .gitignore patterns

## Process

1. Load exclusion patterns from @skills/file-safety-checker/reference/exclusion-patterns.json
2. Analyze staged or modified files
3. Check each file against safety rules
4. Categorize issues by severity (blocking, warning)
5. Output structured safety report with recommendations

## Usage

```bash
# Check currently staged files
file-safety-checker

# Check specific files before staging
file-safety-checker file1.java file2.xml

# Check all modified files
file-safety-checker --all

# Auto-exclude unsafe files
file-safety-checker --auto-exclude
```

## Output Format

### Clean Result

```
FILE SAFETY CHECK REPORT

FILES CHECKED: 8
STATUS: SAFE

All files passed safety checks.
No issues found.
```

### Issues Detected

```
FILE SAFETY CHECK REPORT

FILES CHECKED: 12
STATUS: UNSAFE - 5 ISSUES FOUND

BLOCKING ISSUES: 3

1. Build artifacts detected
   Files:
   - build/classes/java/main/SaleOrder.class
   - build/libs/axelor-sale-1.0.0.jar
   Risk: Pollutes repository, causes merge conflicts
   Action: Exclude from staging

2. Sensitive data detected
   Files:
   - .env
   Risk: CRITICAL - May expose credentials
   Action: Never commit. Add to .gitignore.

3. Merge conflicts detected
   Files:
   - src/main/java/SaleOrder.java (lines 45-52)
   Risk: Broken code
   Action: Resolve conflicts before committing

WARNINGS: 2

1. IDE configuration detected
   Files:
   - .idea/workspace.xml
   - axelor-sale.iml
   Recommendation: Exclude, add to .gitignore

2. OS-specific files detected
   Files:
   - .DS_Store
   Recommendation: Exclude from staging

RECOMMENDATIONS:

1. Unstage blocking files:
   git reset HEAD build/ .env

2. Add to .gitignore:
   echo "build/" >> .gitignore
   echo ".env" >> .gitignore
   echo ".idea/" >> .gitignore
```

## Exclusion Patterns

See @skills/file-safety-checker/reference/exclusion-patterns.json for complete patterns.

**Summary of excluded patterns:**

| Category | Examples |
|----------|----------|
| Build artifacts | `build/`, `target/`, `*.class`, `*.jar` |
| IDE configs | `.idea/`, `*.iml`, `.vscode/` |
| Sensitive data | `.env`, `*.pem`, `*.key`, `credentials.*` |
| OS files | `.DS_Store`, `Thumbs.db` |

## Severity Levels

### Blocking (Must Fix)
- Build artifacts
- Sensitive data (credentials, keys)
- Merge conflict markers
- Compiled code

**Action**: Cannot proceed with commit until fixed.

### Warning (Should Review)
- IDE configurations
- OS-specific files
- Large binary files

**Action**: Review and decide. Usually should exclude.

## Integration

Used in git workflow before staging:

```
Code changes complete
  |
  v
file-safety-checker (validate files)
  |
  v
If issues found:
  - Blocking: Fix required
  - Warnings: Review and decide
  |
  v
If safe:
  |
  v
Stage files -> commitlint-validator -> Git commit
```

See @docs/git/quick-start-guide.md for complete workflows.

## Requirements

- Bash 4.0+
- git 2.0+
- grep with extended regex support (-E)
- @skills/file-safety-checker/reference/exclusion-patterns.json
- @skills/file-safety-checker/reference/gitignore-templates.txt

## Best Practices

1. Run before every commit
2. Keep .gitignore updated
3. Review warnings, don't ignore them
4. Never force unsafe files
5. Educate team on common mistakes

## Error Prevention

This skill prevents:
- Committing compiled code (merge conflicts, repo bloat)
- Exposing API keys and passwords (security breach)
- Breaking builds (unresolved conflicts)
- Personal IDE configs (portability issues)
- Repository pollution (OS files, caches)
