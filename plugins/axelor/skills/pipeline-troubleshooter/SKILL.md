---
name: pipeline-troubleshooter
description: Analyze GitLab CI pipeline failures and provide specific fix recommendations based on error patterns
allowed-tools: ["Read", "Grep", "Bash"]
---

# Pipeline Troubleshooter

## Mission

Analyze failed GitLab CI pipeline jobs, identify root causes from error logs, and provide specific actionable fix recommendations. Recognizes common error patterns (commitlint, build, test, formatting) and maps them to solutions.

## Input Parameters

1. **Failed Job Name** (required): e.g., `commitlint`, `build`, `test`, `spotless`
2. **Error Logs** (required): Error output from pipeline job
3. **Pipeline Stage** (required): `init`, `build`, `test`, `quality`
4. **Project Context** (optional): Build tool (Gradle, Maven, Node), project type

## Process

1. Load error patterns from @skills/pipeline-troubleshooter/reference/error-patterns.json
2. Analyze error logs to identify pattern match
3. Determine root cause category
4. Load fix guide from reference/ (commitlint-errors.md, build-errors.md, etc.)
5. Provide specific fix steps
6. Include prevention recommendations

## Output Format

```
=== PIPELINE FAILURE ANALYSIS ===

Job: commitlint
Stage: init
Status: FAILED

ROOT CAUSE:
Invalid commit type 'Feature' (should be lowercase 'feat')

AFFECTED COMMITS:
- a1b2c3d: Feature: add authentication (INVALID)
- d4e5f6g: fix: resolve bug (VALID)

SPECIFIC FIX:
1. Rebase and edit commit messages:
   git rebase -i HEAD~2

2. Change 'Feature' to 'feat':
   feat: add authentication

3. Force push:
   git push --force-with-lease

PREVENTION:
- Use commitlint locally before pushing
- Install pre-commit hook
- Reference: @docs/git/conventional-commits.md
```

## Error Pattern Categories

1. **Commitlint Errors**: Invalid type, missing scope, header too long
2. **Build Errors**: Compilation failures, dependency resolution
3. **Test Errors**: Test failures, coverage below threshold
4. **Formatting Errors**: Spotless check failures
5. **Cache/Artifact Errors**: Permission issues, missing files

## Reference Files

- @skills/pipeline-troubleshooter/reference/error-patterns.json
- @skills/pipeline-troubleshooter/reference/commitlint-errors.md
- @skills/pipeline-troubleshooter/reference/build-errors.md
- @skills/pipeline-troubleshooter/reference/cache-issues.md

## Integration

Used by: cicd-agent (Pipeline Troubleshooting workflow)
