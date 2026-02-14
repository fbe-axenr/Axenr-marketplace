---
name: quality-gate-configurator
description: Configure quality gates and merge requirements for GitLab CI/CD with blocking/non-blocking jobs
allowed-tools: ["Read"]
---

# Quality Gate Configurator

## Mission

Configure GitLab CI/CD quality gates and merge requirements based on quality level (strict/standard/relaxed). Provides GitLab UI configuration steps, job `allow_failure` settings, protected branch policies, and approval rules.

## Input Parameters

1. **Quality Level** (required):
   - `strict`: All quality checks blocking (commitlint, MR title, tests, spotless)
   - `standard`: Core checks blocking (commitlint, tests), quality optional (spotless warning)
   - `relaxed`: Only critical checks blocking (commitlint), rest warnings

2. **Blocking Jobs** (required): List of jobs that must pass
   - Examples: `commitlint`, `validate-mr-title`, `test`, `spotless`, `sonarqube`

3. **Coverage Threshold** (optional): Minimum test coverage percentage (default: 80%)

4. **Approvals Required** (optional): Number of required approvals (default: 1)

## Output Format

```markdown
=== QUALITY GATE CONFIGURATION ===

Profile: Strict
Blocking Jobs: commitlint, validate-mr-title, test, spotless
Coverage Threshold: 80%
Approvals Required: 1

== GitLab Settings Configuration ==

### Step 1: Merge Request Settings
Settings > Merge requests:
- ☑ Pipelines must succeed
- ☑ Squash commits when merge request is accepted (Require)
- ☑ All discussions must be resolved
- Approvals: 1

### Step 2: Protected Branches
Settings > Repository > Protected branches:
Branch: main
- Allowed to merge: Maintainers
- Allowed to push: No one
- Require approval: Yes

### Step 3: CI/CD Job Configuration
Update .gitlab-ci.yml:

commitlint:
  allow_failure: false  # BLOCKING

validate-mr-title:
  allow_failure: false  # BLOCKING

test:
  allow_failure: false  # BLOCKING
  coverage: '/Total.*?([0-9]{1,3})%/'

spotless:
  allow_failure: false  # BLOCKING
```

## Quality Profiles

### Strict Profile
- **Blocking**: commitlint, MR title, tests (80%+ coverage), spotless, sonarqube quality gate
- **Use Case**: Production repos, team collaboration
- **Merge Requirements**: Pipeline success + 1 approval + discussions resolved

### Standard Profile
- **Blocking**: commitlint, MR title, tests (70%+ coverage)
- **Non-Blocking**: spotless (warning), sonarqube (optional)
- **Use Case**: Standard projects, balanced quality/velocity

### Relaxed Profile
- **Blocking**: commitlint
- **Non-Blocking**: tests, spotless, sonarqube
- **Use Case**: Rapid prototyping, learning environments

## Reference Files

- @skills/quality-gate-configurator/reference/quality-profiles.json
- @skills/quality-gate-configurator/reference/gitlab-settings-guide.md

## Integration

Used by: cicd-agent (Step 5 - Configure GitLab Settings)
