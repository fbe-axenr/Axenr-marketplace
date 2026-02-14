# CI/CD Administration Guide

Guide for setting up and administering GitLab CI/CD pipelines for Axelor projects with conventional commits enforcement and automated quality gates.

## Table of Contents

1. [Initial Setup](#initial-setup)
2. [Commitlint Configuration](#commitlint-configuration)
3. [MR Title Validation](#mr-title-validation)
4. [Squash Commits Enforcement](#squash-commits-enforcement)
5. [GitLab CI Configuration](#gitlab-ci-configuration)
6. [Quality Gates Administration](#quality-gates-administration)
7. [AI Integration Setup](#ai-integration-setup)
8. [Troubleshooting](#troubleshooting)

## Initial Setup

### Prerequisites

- GitLab repository for Axelor project
- GitLab Runner configured
- Access to project settings (Maintainer role or higher)

### Step 1: Project Structure

Ensure your project has this structure:

```
project-root/
├── .gitlab-ci.yml                 # Main CI/CD configuration
├── .commitlintrc.json             # Commitlint configuration
├── ci/
│   └── scripts/
│       ├── validate-mr-title.sh   # MR title validation script
│       └── check-squash.sh        # Squash commits check (optional)
├── package.json                   # For commitlint dependencies
└── git-cliff.toml                 # Changelog generation config (optional)
```

### Step 2: Install Required Files

Copy template files to your project:

```bash
# From axelor plugin
cp plugins/axelor/docs/cicd/templates/.gitlab-ci.yml .
cp plugins/axelor/docs/cicd/templates/.commitlintrc.json .
mkdir -p ci/scripts
cp plugins/axelor/docs/cicd/templates/validate-mr-title.sh ci/scripts/
chmod +x ci/scripts/validate-mr-title.sh
```

## Commitlint Configuration

### Install Commitlint

**Option 1: Using package.json** (Recommended):

```json
{
  "name": "axelor-project",
  "devDependencies": {
    "@commitlint/cli": "^18.4.3",
    "@commitlint/config-conventional": "^18.4.3"
  }
}
```

Install:
```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

**Option 2: Install in CI only**:

No local installation needed. Install in `.gitlab-ci.yml`:

```yaml
commitlint:
  stage: init
  image: node:20-alpine
  before_script:
    - npm install --save-dev @commitlint/cli @commitlint/config-conventional
  script:
    - npx commitlint --from=origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME --to=HEAD --verbose
```

### Configure Commitlint

Create `.commitlintrc.json`:

```json
{
  "extends": ["@commitlint/config-conventional"],
  "rules": {
    "type-enum": [2, "always", [
      "feat", "fix", "docs", "style", "refactor",
      "perf", "test", "build", "ci", "chore", "revert"
    ]],
    "type-case": [2, "always", "lower-case"],
    "type-empty": [2, "never"],
    "scope-case": [2, "always", "lower-case"],
    "subject-empty": [2, "never"],
    "subject-full-stop": [2, "never", "."],
    "subject-case": [2, "never", ["sentence-case", "start-case", "pascal-case", "upper-case"]],
    "header-max-length": [2, "always", 100],
    "body-leading-blank": [1, "always"],
    "body-max-line-length": [2, "always", 100],
    "footer-leading-blank": [1, "always"],
    "footer-max-line-length": [2, "always", 100]
  }
}
```

### Test Commitlint Locally

```bash
# Test last commit
git log -1 --pretty=%B | npx commitlint

# Test all commits in branch
npx commitlint --from=origin/main --to=HEAD

# Test specific message
echo "feat(sale): add order discount" | npx commitlint
```

## MR Title Validation

### Create Validation Script

Create `ci/scripts/validate-mr-title.sh`:

```bash
#!/bin/bash
#
# Validate MR title follows conventional commit format
#

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if running in MR context
if [ -z "$CI_MERGE_REQUEST_TITLE" ]; then
  echo -e "${YELLOW}Warning: Not in MR context. Skipping validation.${NC}"
  exit 0
fi

echo "==========================================="
echo "Validating Merge Request Title"
echo "==========================================="
echo ""
echo "MR Title: $CI_MERGE_REQUEST_TITLE"
echo ""

# Conventional commit regex pattern
PATTERN="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+"

if echo "$CI_MERGE_REQUEST_TITLE" | grep -Eq "$PATTERN"; then
  echo -e "${GREEN}✅ SUCCESS: MR title follows conventional commit format!${NC}"
  echo ""
  exit 0
else
  echo -e "${RED}❌ ERROR: MR title does NOT follow conventional commit format!${NC}"
  echo ""
  echo "Expected format:"
  echo "  <type>[optional scope]: <description>"
  echo ""
  echo "Examples of valid titles:"
  echo "  feat: add user authentication"
  echo "  feat(auth): add user authentication"
  echo "  fix: resolve login bug"
  echo "  docs: update README"
  echo ""
  echo "Allowed types:"
  echo "  feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
  echo ""
  echo "Your MR title: '$CI_MERGE_REQUEST_TITLE'"
  echo ""
  echo "Please update your MR title to follow this format."
  echo ""
  exit 1
fi
```

Make executable:
```bash
chmod +x ci/scripts/validate-mr-title.sh
```

### Test MR Title Validation

```bash
# Test locally
CI_MERGE_REQUEST_TITLE="feat(auth): add user login" bash ci/scripts/validate-mr-title.sh

# Should succeed
echo "Exit code: $?"

# Test invalid title
CI_MERGE_REQUEST_TITLE="Add feature" bash ci/scripts/validate-mr-title.sh

# Should fail
echo "Exit code: $?"
```

## Squash Commits Enforcement

### Configure Project Settings

**GitLab UI**:
1. Go to **Settings** > **Merge requests**
2. Enable **"Squash commits when merge request is accepted"**
3. Select **"Encourage"** or **"Require"**
4. Save changes

**Why Squash Commits?**:
- Clean git history (one commit per feature)
- MR title becomes the commit message
- Enables semantic versioning
- Simplifies changelog generation

### Verify Squash in CI (Optional)

Add check in `.gitlab-ci.yml`:

```yaml
check-squash-commits:
  stage: init
  image: alpine:latest
  before_script:
    - apk add --no-cache curl jq
  script:
    - |
      if [ -z "$CI_MERGE_REQUEST_IID" ]; then
        echo "Not in MR context"
        exit 0
      fi

      SQUASH=$(curl -s --header "PRIVATE-TOKEN: $CI_JOB_TOKEN" \
        "$CI_API_V4_URL/projects/$CI_PROJECT_ID/merge_requests/$CI_MERGE_REQUEST_IID" \
        | jq -r '.squash')

      if [ "$SQUASH" != "true" ]; then
        echo "❌ Squash commits must be enabled"
        exit 1
      fi

      echo "✅ Squash commits enabled"
  only:
    - merge_requests
  allow_failure: false
```

## GitLab CI Configuration

### Complete .gitlab-ci.yml Example

```yaml
stages:
  - init
  - build
  - test
  - quality
  - plan
  - deploy
  - cleanup

variables:
  GRADLE_OPTS: "-Dorg.gradle.daemon=false"
  GRADLE_USER_HOME: ${CI_PROJECT_DIR}/.gradle

# ==================== INIT STAGE ====================

commitlint:
  stage: init
  image: node:20-alpine
  before_script:
    - npm install --save-dev @commitlint/cli @commitlint/config-conventional
  script:
    - echo "Validating commits from $CI_MERGE_REQUEST_TARGET_BRANCH_NAME to HEAD"
    - npx commitlint --from=origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME --to=HEAD --verbose
  only:
    - merge_requests
  allow_failure: false

validate-mr-title:
  stage: init
  image: alpine:latest
  before_script:
    - apk add --no-cache bash grep
  script:
    - bash ci/scripts/validate-mr-title.sh
  only:
    - merge_requests
  allow_failure: false

# ==================== BUILD STAGE ====================

build:
  stage: build
  image: gradle:8.5-jdk17-alpine
  script:
    - gradle clean build -x test --build-cache --parallel
  artifacts:
    paths:
      - build/libs/*.jar
      - build/classes
    expire_in: 1 week
  cache:
    key: ${CI_COMMIT_REF_SLUG}-gradle
    paths:
      - .gradle
      - build/cache
  only:
    - branches
    - tags
    - merge_requests

# ==================== TEST STAGE ====================

test:unit:
  stage: test
  image: gradle:8.5-jdk17-alpine
  script:
    - gradle test --no-daemon
  artifacts:
    when: always
    reports:
      junit: build/test-results/test/**/TEST-*.xml
    paths:
      - build/reports/tests
  coverage: '/Total.*?([0-9]{1,3})%/'
  only:
    - branches
    - merge_requests

spotless-check:
  stage: test
  image: gradle:8.5-jdk17-alpine
  script:
    - gradle spotlessCheck
  allow_failure: false
  only:
    - merge_requests

# ==================== QUALITY STAGE ====================

sonarqube:
  stage: quality
  image: gradle:8.5-jdk17-alpine
  script:
    - gradle sonarqube -Dsonar.host.url=$SONAR_HOST_URL -Dsonar.login=$SONAR_TOKEN
  only:
    - merge_requests
    - main
  allow_failure: true

# ==================== PLAN STAGE ====================

publish:maven:
  stage: plan
  image: gradle:8.5-jdk17-alpine
  script:
    - gradle publish -Pversion=${CI_COMMIT_TAG:-SNAPSHOT}
  only:
    - tags
    - main
  when: manual

# ==================== DEPLOY STAGE ====================

deploy:dev:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Deploying to development"
    - ./scripts/deploy.sh dev
  environment:
    name: development
    url: https://dev.example.com
  only:
    - develop

deploy:prod:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Deploying to production"
    - ./scripts/deploy.sh prod
  environment:
    name: production
    url: https://example.com
  only:
    - tags
  when: manual
```

### Enable Pipeline

1. Commit `.gitlab-ci.yml` to repository
2. Push to GitLab
3. Pipeline runs automatically on push/MR

## Quality Gates Administration

### Configure Blocking Jobs

Set jobs to block merge on failure:

```yaml
job-name:
  allow_failure: false  # Job must pass (default for most jobs)
```

**Recommended blocking jobs**:
- `commitlint` (BLOCKING)
- `validate-mr-title` (BLOCKING)
- `build` (BLOCKING)
- `test:unit` (BLOCKING)
- `spotless-check` (BLOCKING)

**Optional blocking**:
- `sonarqube` (set threshold in SonarQube)
- `coverage` (if you want minimum coverage)

### Configure Merge Requirements

**GitLab UI**:
1. Go to **Settings** > **Merge requests**
2. Enable **"Pipelines must succeed"**
3. Set **"All discussions must be resolved"**
4. Set minimum approvals (1 or more)
5. Save changes

### Monitor Quality Gates

**In GitLab MR**:
- See pipeline status
- View failed jobs
- See detailed logs
- Fix issues and re-run

**Common Failures**:

| Job | Failure | Fix |
|-----|---------|-----|
| commitlint | Invalid commit message | Rebase and fix commit messages |
| validate-mr-title | Invalid MR title | Update MR title in UI |
| build | Compilation error | Fix code errors |
| test:unit | Test failure | Fix failing tests |
| spotless-check | Format error | Run `gradle spotlessApply` |

## AI Integration Setup

Optional AI-powered assistance for code review, test analysis, and pipeline debugging using Claude Code CLI and GitLab MCP server.

### Prerequisites

- GitLab project with CI/CD configured (Steps 1-6 completed)
- Anthropic API key (Claude API access)
- GitLab Runner with internet access (for npm packages)

### Step 1: Obtain Anthropic API Key

1. Sign up at [Anthropic Console](https://console.anthropic.com/)
2. Create API key
3. Copy API key for configuration

### Step 2: Configure GitLab Variables

**In GitLab UI**:
1. Go to **Settings** > **CI/CD** > **Variables**
2. Add required variable:

| Key | Value | Protected | Masked |
|-----|-------|-----------|--------|
| `ANTHROPIC_API_KEY` | [Your Claude API key] | ☐ | ☑ |

3. **(Optional)** Add feature flags to enable automatic triggers:

| Key | Value | Description |
|-----|-------|-------------|
| `ENABLE_AI_REVIEW` | `false` | Auto-run code review on MRs (default: manual) |
| `ENABLE_AI_ARCHITECTURE` | `false` | Auto-run architecture analysis (default: manual) |
| `ENABLE_AI_TEST_ANALYSIS` | `false` | Auto-run test analysis on failures (default: manual) |
| `ENABLE_AI_PIPELINE_DEBUG` | `false` | Auto-run debug on pipeline failure (default: manual) |

4. **(Optional)** Customize AI behavior:

| Key | Value | Description |
|-----|-------|-------------|
| `CLAUDE_MODEL` | `claude-sonnet-4` | AI model to use |
| `CLAUDE_DEBUG` | `false` | Enable verbose output |

### Step 3: Create AI CI/CD Configuration

#### Project Structure

```
project-root/
├── .gitlab-ci.yml                 # Main CI/CD (updated)
├── ci/
│   ├── base.gitlab-ci.yml        # Standard CI/CD jobs
│   ├── ai.gitlab-ci.yml          # AI jobs (new)
│   └── scripts/
│       ├── validate-mr-title.sh
│       ├── mcp-server-setup.sh   # MCP server setup (new)
│       └── ai-flow-runner.sh     # AI workflow runner (new)
```

#### Update .gitlab-ci.yml

Update main pipeline to include AI configuration:

```yaml
# .gitlab-ci.yml
include:
  - local: 'ci/base.gitlab-ci.yml'
  - local: 'ci/ai.gitlab-ci.yml'  # Add AI include

stages:
  - init
  - ai-review      # Add AI review stage
  - build
  - test
  - ai-assist      # Add AI assist stage
  - quality
  - plan
  - deploy
  - .post          # AI debugging runs here on failure
```

#### Create ci/ai.gitlab-ci.yml

Use the gitlab-ci-generator skill to create AI configuration:

```bash
# Using cicd-agent agent
claude -p "Use gitlab-ci-generator skill to create AI integration for my project" \
  --agent cicd-agent
```

Or manually copy from plugin templates:

```bash
cp plugins/axelor/skills/gitlab-ci-generator/reference/ai-stage-templates.yml \
   ci/ai.gitlab-ci.yml
```

#### Create Helper Scripts

Copy AI helper scripts:

```bash
# Create scripts directory if not exists
mkdir -p ci/scripts

# Copy MCP server setup script
cp plugins/axelor/skills/gitlab-ci-generator/reference/scripts/mcp-server-setup.sh \
   ci/scripts/

# Copy AI flow runner
cp plugins/axelor/skills/gitlab-ci-generator/reference/scripts/ai-flow-runner.sh \
   ci/scripts/

# Make executable
chmod +x ci/scripts/mcp-server-setup.sh
chmod +x ci/scripts/ai-flow-runner.sh
```

### Step 4: Test AI Integration

#### Test Locally (Optional)

Test AI scripts locally before pushing:

```bash
# Test MCP server setup (requires environment variables)
export CI_JOB_TOKEN="test-token"
export CI_API_V4_URL="https://gitlab.com/api/v4"
bash ci/scripts/mcp-server-setup.sh

# Verify configuration files created
ls -la .claude-code/
```

#### Test in CI

1. Commit AI configuration files:

```bash
git add .gitlab-ci.yml ci/ai.gitlab-ci.yml ci/scripts/
git commit -m "feat(ci): add AI integration with Claude Code"
git push
```

2. Create test MR
3. Verify AI stages appear in pipeline
4. Manually trigger "ai code review" job
5. Check job logs and artifacts
6. Verify review posted to MR (if MCP enabled)

### Step 5: AI Job Workflow

#### Code Review Workflow

1. Developer creates MR
2. Pipeline starts automatically
3. **Manual trigger**: Developer clicks "ai code review" job
4. AI analyzes changed files
5. Review posted as MR comment
6. Developer addresses feedback
7. Updates code and pushes

#### Test Failure Analysis Workflow

1. Pipeline runs tests
2. Tests fail
3. **Automatic trigger** (if `ENABLE_AI_TEST_ANALYSIS=true`):
   - AI analyzes test failures
   - Posts analysis to MR with fix suggestions
4. **Manual trigger** (default):
   - Developer manually runs "ai test failure analysis"
   - AI posts analysis

#### Pipeline Debugging Workflow

1. Pipeline fails
2. **.post stage runs**: "ai pipeline debug"
3. **Automatic trigger** (if `ENABLE_AI_PIPELINE_DEBUG=true`):
   - AI analyzes failure
   - Posts debug guide to MR
4. **Manual trigger** (default):
   - Developer manually triggers debug job

### Step 6: Monitor and Optimize

#### Monitor AI Usage

1. Check Anthropic Console for:
   - Token usage
   - Cost tracking
   - Rate limits

2. Review CI/CD artifacts:
   - `ai_*.md` files (analysis reports)
   - `*.ai.log` files (execution logs)

#### Optimize Costs

**Keep jobs manual** (default recommended):
```yaml
rules:
  - when: manual
```

**Limit to important branches**:
```yaml
rules:
  - if: '$CI_COMMIT_BRANCH == "main"'
    when: manual
  - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    when: manual
```

**Use smaller model for simple tasks**:
```yaml
variables:
  CLAUDE_MODEL: "claude-haiku-3"  # Faster, cheaper
```

### AI Job Reference

#### Available AI Jobs

| Job | Stage | Trigger | Permission | Purpose |
|-----|-------|---------|------------|---------|
| `ai code review` | ai-review | Manual | viewOnly | Review MR for quality, bugs, security |
| `ai architecture analysis` | ai-review | Manual | viewOnly | Analyze design patterns and architecture |
| `ai test failure analysis` | ai-assist | on_failure | viewOnly | Diagnose test failures, suggest fixes |
| `ai code generation` | ai-assist | Manual | acceptEdits | Generate code (write permissions) |
| `ai pipeline debug` | .post | on_failure | viewOnly | Debug pipeline failures |

#### Job Characteristics

All AI jobs have:
- `allow_failure: true` (never block pipeline)
- Artifacts expire in 1 week
- Timeout: 10 minutes (adjustable)
- Manual trigger by default

### Safety and Best Practices

#### Safety Guidelines

1. **Never enable auto-trigger in production** initially
   - Start with manual triggers
   - Monitor costs and quality
   - Gradually enable auto-triggers if beneficial

2. **Review AI suggestions carefully**
   - AI can make mistakes
   - Verify code changes
   - Use as guidance, not absolute truth

3. **Protect sensitive data**
   - AI has access to code
   - Don't expose secrets in code
   - Use GitLab secrets management

4. **Monitor costs**
   - Check Anthropic Console regularly
   - Set budget alerts
   - Disable if costs exceed budget

#### Best Practices

1. **Use descriptive MR descriptions**
   - AI uses MR context
   - Better descriptions = better analysis

2. **Keep code modular**
   - Smaller changes = better AI analysis
   - Easier to review and understand

3. **Leverage MR comments**
   - AI posts reviews as comments
   - Easy to track and respond

4. **Archive old artifacts**
   - AI generates markdown reports
   - Archive useful analyses

### Troubleshooting AI Integration

#### Issue: AI job fails with "ANTHROPIC_API_KEY not set"

**Solution**:
1. Verify variable set in Settings > CI/CD > Variables
2. Check variable name is exactly `ANTHROPIC_API_KEY`
3. Ensure variable is not protected (or branch is protected)
4. Re-run pipeline

#### Issue: MCP server setup fails

**Symptoms**:
```
⚠ MCP server setup failed, continuing without MCP
```

**Causes**:
- Network issues (npm package download)
- Missing environment variables
- GitLab API access denied

**Solution**:
```yaml
# Disable MCP if not needed
variables:
  GITLAB_MCP_ENABLED: "false"
```

#### Issue: AI review not posted to MR

**Check**:
1. Job ran in MR context (`CI_MERGE_REQUEST_IID` set)
2. `ai_review.md` file exists in artifacts
3. CI_JOB_TOKEN has MR comment permissions

**Debug**:
```bash
# In job logs
echo "MR IID: ${CI_MERGE_REQUEST_IID:-not set}"
ls -la ai_review.md
```

#### Issue: AI job times out

**Solution**:
```yaml
ai code review:
  timeout: 15 minutes  # Increase from 10 min default
```

#### Issue: High costs

**Solution**:
1. Keep jobs manual
2. Use smaller model (claude-haiku-3)
3. Limit to main branches only
4. Review usage in Anthropic Console

### Example AI Integration

**Complete workflow example**:

```yaml
# .gitlab-ci.yml
include:
  - local: 'ci/base.gitlab-ci.yml'
  - local: 'ci/ai.gitlab-ci.yml'

stages:
  - init
  - ai-review
  - build
  - test
  - ai-assist
  - quality
  - .post

variables:
  # AI configuration
  CLAUDE_MODEL: "claude-sonnet-4"
  GITLAB_MCP_ENABLED: "true"
```

**Usage**:
1. Developer creates MR: `feat(auth): add user login`
2. Init stage runs: commitlint + MR title validation ✅
3. Developer manually triggers: "ai code review"
4. AI analyzes code, posts review to MR
5. Developer addresses feedback, pushes fixes
6. Build + test stages run
7. If tests fail: "ai test failure analysis" available
8. Pipeline completes successfully ✅

## Troubleshooting

### Commitlint Fails in CI but Passes Locally

**Cause**: Different range of commits

**Solution**:
```bash
# Test same range as CI
npx commitlint --from=origin/main --to=HEAD

# Or test all commits
npx commitlint --from=HEAD~10
```

### MR Title Validation Fails

**Cause**: Title doesn't follow format

**Solution**:
1. Use mr-title-validator skill to validate title
2. Update MR title in GitLab UI
3. Re-run pipeline

### Squash Commits Not Working

**Cause**: Not enabled in project settings

**Solution**:
1. Go to **Settings** > **Merge requests**
2. Enable **"Squash commits when merge request is accepted"**
3. Set to **"Require"**

### Pipeline Doesn't Start

**Possible causes**:
- `.gitlab-ci.yml` syntax error
- Runner not available
- Branch not configured

**Solution**:
```bash
# Validate YAML syntax
cat .gitlab-ci.yml | docker run -i --rm alpine:latest sh -c "apk add --no-cache yamllint && yamllint -"

# Check in GitLab UI
# CI/CD > Pipelines > View pipeline errors
```

### Cache Issues

**Cause**: Stale cache causing failures

**Solution**:
```
1. Go to CI/CD > Pipelines
2. Clear runner caches
3. Re-run pipeline
```

## Summary

A properly configured CI/CD pipeline with quality gates:

1. **Validates commits**: Blocks invalid conventional commits
2. **Validates MR titles**: Ensures proper format
3. **Enforces squash**: Clean git history
4. **Builds reliably**: Consistent compilation
5. **Tests thoroughly**: Unit and integration tests
6. **Maintains quality**: Code coverage, formatting, analysis
7. **Automates releases**: Semantic versioning, changelogs

Follow this guide to set up and administer robust CI/CD pipelines for Axelor projects.

## References

- [GitLab CI Patterns](./gitlab-ci-patterns.md)
- [Conventional Commits](../git/conventional-commits.md)
- [Commitlint Documentation](https://commitlint.js.org/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
