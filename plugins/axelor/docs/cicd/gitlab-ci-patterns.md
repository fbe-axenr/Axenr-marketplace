# GitLab CI/CD Patterns for Axelor Projects

Comprehensive guide to GitLab CI/CD pipeline patterns and best practices for Axelor projects.

## Table of Contents

1. [Overview](#overview)
2. [Pipeline Structure](#pipeline-structure)
3. [Quality Gates](#quality-gates)
4. [Conventional Commits Validation](#conventional-commits-validation)
5. [Build and Test](#build-and-test)
6. [Release Management](#release-management)
7. [Deployment](#deployment)
8. [AI Automation](#ai-automation)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)

## Overview

GitLab CI/CD pipelines automate the software delivery process from code commit to deployment. A well-designed pipeline ensures:

- Code quality
- Automated testing
- Consistent builds
- Semantic versioning
- Reliable deployments

### Pipeline Philosophy

1. **Fail Fast**: Validate early in the pipeline
2. **Quality Gates**: Block merges on failures
3. **Automation**: Minimize manual intervention
4. **Transparency**: Clear status and logs
5. **Reproducibility**: Same results every time

## Pipeline Structure

### Standard Stage Flow

```yaml
stages:
  - init        # Validation (blocking)
  - build       # Compilation, artifacts
  - test        # Testing, coverage
  - quality     # Code quality, security
  - plan        # Publishing, releases
  - deploy      # Deployment
  - cleanup     # Resource cleanup
```

### Stage Purposes

**Init Stage** (BLOCKING):
- Validate conventional commits
- Validate MR title
- Check squash commits enabled
- Verify basic requirements

**Build Stage**:
- Compile code
- Generate artifacts
- Create changelog (for releases)
- Prepare for testing

**Test Stage**:
- Unit tests
- Integration tests
- Code coverage
- Test reports

**Quality Stage**:
- Static code analysis (SonarQube)
- Security scanning
- Dependency vulnerability checks
- Code smells detection

**Plan Stage**:
- Publish to artifact repository (Maven/NPM)
- Create release notes
- Tag versions
- Prepare deployment artifacts

**Deploy Stage**:
- Deploy to environments (dev, staging, prod)
- Database migrations
- Configuration updates
- Health checks

**Cleanup Stage**:
- Remove temporary resources
- Clean up old artifacts
- Update status

## Quality Gates

Quality gates are blocking checks that must pass before merge.

### Init Stage Quality Gates

#### 1. Commit Message Validation

**Purpose**: Ensure all commits follow conventional commits format

**Implementation**:
```yaml
commitlint:
  stage: init
  image: node:20-alpine
  before_script:
    - npm install --save-dev @commitlint/cli @commitlint/config-conventional
  script:
    - npx commitlint --from=origin/$CI_MERGE_REQUEST_TARGET_BRANCH_NAME --to=HEAD --verbose
  only:
    - merge_requests
  allow_failure: false
```

**What it checks**:
- Commit type is valid (feat, fix, docs, etc.)
- Format follows `<type>(<scope>): <subject>`
- Subject is present and properly formatted
- No emojis in commit messages

**Example output**:
```
✓ All commits valid
✗ Commit 'abc123' fails: type must be lowercase
✗ Commit 'def456' fails: subject may not be empty
```

**Fix**:
```bash
# Amend last commit message
git commit --amend -m "feat(sale): add order discount"

# Rebase to fix older commits
git rebase -i origin/main
```

#### 2. MR Title Validation

**Purpose**: Ensure MR title follows conventional commits (becomes commit message on squash)

**Implementation**:
```yaml
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
```

**Script** (`ci/scripts/validate-mr-title.sh`):
```bash
#!/bin/bash
set -e

PATTERN="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+"

if [ -z "$CI_MERGE_REQUEST_TITLE" ]; then
  echo "Not in MR context, skipping"
  exit 0
fi

if echo "$CI_MERGE_REQUEST_TITLE" | grep -Eq "$PATTERN"; then
  echo "✅ MR title valid: $CI_MERGE_REQUEST_TITLE"
  exit 0
else
  echo "❌ MR title invalid: $CI_MERGE_REQUEST_TITLE"
  echo "Expected format: <type>[scope]: <description>"
  echo "Examples:"
  echo "  feat(auth): add user login"
  echo "  fix(api): resolve timeout issue"
  exit 1
fi
```

**Fix**:
```
Update MR title in GitLab UI to follow conventional commits format
```

#### 3. Squash Commits Check

**Purpose**: Ensure squash commits is enabled (MR title becomes commit message)

**Implementation**:
```yaml
check-squash-commits:
  stage: init
  image: alpine:latest
  before_script:
    - apk add --no-cache curl jq
  script:
    - |
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

**Fix**:
```
Enable "Squash commits when merge request is accepted" in MR settings
```

### Build Stage Quality Gates

#### Code Compilation

**Purpose**: Ensure code compiles successfully

**Java/Gradle Example**:
```yaml
build:
  stage: build
  image: gradle:8.5-jdk17-alpine
  script:
    - gradle clean build -x test
  artifacts:
    paths:
      - build/libs/*.jar
    expire_in: 1 week
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - .gradle
      - build
```

### Test Stage Quality Gates

#### 1. Unit Tests

**Purpose**: Verify code functionality

```yaml
unit-tests:
  stage: test
  image: gradle:8.5-jdk17-alpine
  script:
    - gradle test
  artifacts:
    reports:
      junit: build/test-results/test/TEST-*.xml
    paths:
      - build/reports/tests
  coverage: '/Total.*?([0-9]{1,3})%/'
```

#### 2. Code Coverage

**Purpose**: Ensure minimum test coverage

```yaml
coverage:
  stage: test
  image: gradle:8.5-jdk17-alpine
  script:
    - gradle jacocoTestReport
    - |
      COVERAGE=$(grep -oP '(?<=Total.*?<td>)[0-9]+(?=%)' build/reports/jacoco/test/html/index.html | head -1)
      echo "Coverage: $COVERAGE%"
      if [ "$COVERAGE" -lt 80 ]; then
        echo "❌ Coverage below 80%"
        exit 1
      fi
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: build/reports/jacoco/test/jacocoTestReport.xml
  coverage: '/Total.*?([0-9]{1,3})%/'
```

#### 3. Code Formatting

**Purpose**: Ensure consistent code style

```yaml
spotless-check:
  stage: test
  image: gradle:8.5-jdk17-alpine
  script:
    - gradle spotlessCheck
  allow_failure: false
```

**Fix**:
```bash
# Format code locally
gradle spotlessApply

# Commit formatted code
git add .
git commit -m "style: apply code formatting"
```

## Conventional Commits Validation

### Why Validate Conventional Commits?

1. **Semantic Versioning**: Determine version bumps automatically
2. **Changelog Generation**: Generate changelogs from commits
3. **Clear History**: Understand changes at a glance
4. **Tooling Support**: Enable automation

### Validation Workflow

```
Developer commits code
  ↓
Push to GitLab
  ↓
MR created
  ↓
Init stage: commitlint
  ├─ Valid → Continue pipeline
  └─ Invalid → Fail pipeline (BLOCKING)
  ↓
Init stage: MR title validator
  ├─ Valid → Continue pipeline
  └─ Invalid → Fail pipeline (BLOCKING)
  ↓
Build, test, quality stages
  ↓
Merge with squash
  ↓
MR title becomes commit message
  ↓
Clean git history with conventional commits
```

### Complete Commitlint Configuration

**.commitlintrc.json**:
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
    "subject-case": [2, "never", [
      "sentence-case", "start-case", "pascal-case", "upper-case"
    ]],
    "header-max-length": [2, "always", 100],
    "body-leading-blank": [1, "always"],
    "body-max-line-length": [2, "always", 100],
    "footer-leading-blank": [1, "always"],
    "footer-max-line-length": [2, "always", 100]
  }
}
```

### GitLab CI Integration

```yaml
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
```

## Build and Test

### Gradle Build Configuration

**Build Job**:
```yaml
build:
  stage: build
  image: gradle:8.5-jdk17-alpine
  before_script:
    - export GRADLE_USER_HOME=`pwd`/.gradle
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
      - build
    policy: pull-push
  only:
    - branches
    - tags
    - merge_requests
```

### Test Execution

**Unit Tests**:
```yaml
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
```

**Integration Tests**:
```yaml
test:integration:
  stage: test
  image: gradle:8.5-jdk17-alpine
  services:
    - postgres:15-alpine
  variables:
    POSTGRES_DB: testdb
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
  script:
    - gradle integrationTest --no-daemon
  artifacts:
    when: always
    reports:
      junit: build/test-results/integrationTest/**/TEST-*.xml
```

## Release Management

### Semantic Versioning with Git Cliff

**Changelog Generation**:
```yaml
changelog:
  stage: build
  image: alpine:latest
  before_script:
    - apk add --no-cache git curl
    - curl -L https://github.com/orhun/git-cliff/releases/latest/download/git-cliff-linux-amd64.tar.gz | tar xz
    - mv git-cliff /usr/local/bin/
  script:
    - git-cliff --output CHANGELOG.md
  artifacts:
    paths:
      - CHANGELOG.md
  only:
    - tags
    - main
```

**git-cliff.toml** configuration:
```toml
[changelog]
header = """
# Changelog\n
All notable changes to this project will be documented in this file.\n
"""
body = """
{% for group, commits in commits | group_by(attribute="group") %}
    ### {{ group | upper_first }}
    {% for commit in commits %}
        - {{ commit.message | upper_first }} ({{ commit.id | truncate(length=7, end="") }})\
    {% endfor %}
{% endfor %}\n
"""

[git]
conventional_commits = true
filter_unconventional = true
commit_parsers = [
    { message = "^feat", group = "Features"},
    { message = "^fix", group = "Bug Fixes"},
    { message = "^doc", group = "Documentation"},
    { message = "^perf", group = "Performance"},
    { message = "^refactor", group = "Refactoring"},
    { message = "^style", group = "Styling"},
    { message = "^test", group = "Testing"},
    { message = "^chore", skip = true},
    { message = "^ci", skip = true},
    { message = "^build", skip = true},
]
```

### Automated Versioning

**Version Bump**:
```yaml
version:bump:
  stage: plan
  image: node:20-alpine
  before_script:
    - npm install --save-dev standard-version
  script:
    - npx standard-version
    - git push --follow-tags origin HEAD:main
  only:
    - main
  when: manual
```

### Publishing Artifacts

**Maven Repository**:
```yaml
publish:maven:
  stage: plan
  image: gradle:8.5-jdk17-alpine
  script:
    - gradle publish -Pversion=${CI_COMMIT_TAG}
  only:
    - tags
  environment:
    name: maven-central
```

## Deployment

### Environment Strategy

**Development**:
```yaml
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
```

**Staging**:
```yaml
deploy:staging:
  stage: deploy
  image: alpine:latest
  script:
    - echo "Deploying to staging"
    - ./scripts/deploy.sh staging
  environment:
    name: staging
    url: https://staging.example.com
  only:
    - main
  when: manual
```

**Production**:
```yaml
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

## AI Automation

AI-powered assistance using Claude Code CLI and GitLab MCP server integration for automated code review, test analysis, and pipeline debugging.

### Overview

AI automation adds intelligent assistance to your GitLab CI/CD pipeline:

- **Code Review**: Automated MR review for quality, security, and best practices
- **Architecture Analysis**: Design patterns and SOLID principles review
- **Test Failure Analysis**: Intelligent test failure diagnosis and fix suggestions
- **Pipeline Debugging**: Automatic troubleshooting of pipeline failures
- **Code Generation**: AI-assisted code implementation (manual trigger)

**Key Principles**:
1. **Safety First**: All AI jobs manual by default, never block pipeline
2. **Read-Only Default**: Analysis jobs use viewOnly permission mode
3. **Explicit Triggers**: Code generation requires manual confirmation
4. **Fail Gracefully**: AI failures logged but don't break pipeline

### Pipeline Structure with AI

```yaml
stages:
  - init            # Validation (blocking)
  - ai-review       # AI code review (manual)
  - build           # Compilation
  - test            # Testing
  - ai-assist       # AI assistance (on_failure)
  - quality         # Code quality
  - plan            # Publishing
  - deploy          # Deployment
  - .post           # AI debugging (on_failure)
```

### AI Stage Configuration

#### 1. AI Review Stage (Early Feedback)

Runs early in pipeline, before build, for fast feedback on MR quality.

**ai code review**:
```yaml
ai code review:
  stage: ai-review
  image: node:24-alpine3.21
  variables:
    CLAUDE_MODEL: "claude-sonnet-4"
    GITLAB_MCP_ENABLED: "true"
  before_script:
    - apk add --no-cache git curl bash jq
    - npm install -g @anthropic-ai/claude-code
    - chmod +x ci/scripts/mcp-server-setup.sh
    - ci/scripts/mcp-server-setup.sh
  script:
    - |
      REVIEW_PROMPT="Review this merge request and provide detailed feedback:

      1. **Code Quality**: Check adherence to best practices and coding standards
      2. **Potential Issues**: Identify bugs, security vulnerabilities, or performance problems
      3. **Architecture**: Assess design patterns and SOLID principles
      4. **Documentation**: Verify code comments and documentation completeness
      5. **Testing**: Review test coverage and test quality

      Focus on files changed in this MR.
      Provide actionable, specific feedback with code examples."

      claude -p "$REVIEW_PROMPT" \
        --permission-mode viewOnly \
        --allowedTools "Read(*) Grep(*) Glob(*) mcp__gitlab" \
        > ai_review.md 2> ai_review.ai.log
    # Post results to MR
    - |
      if [ -n "${CI_MERGE_REQUEST_IID}" ] && [ -f ai_review.md ]; then
        REVIEW_BODY="## 🤖 AI Code Review

$(cat ai_review.md)

---
*Generated by Claude Code in pipeline [#${CI_PIPELINE_ID}](${CI_PIPELINE_URL})*"

        curl -s -X POST \
          --header "PRIVATE-TOKEN: ${CI_JOB_TOKEN}" \
          --header "Content-Type: application/json" \
          --data "$(jq -n --arg body "$REVIEW_BODY" '{body: $body}')" \
          "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/merge_requests/${CI_MERGE_REQUEST_IID}/notes"
      fi
  artifacts:
    paths:
      - "ai_review.md"
      - "*.ai.log"
    expire_in: 1 week
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event" && $ENABLE_AI_REVIEW == "true"'
      when: always
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
      when: manual
  allow_failure: true
```

**What it checks**:
- Code quality and adherence to standards
- Potential bugs and security vulnerabilities
- Architecture and design patterns
- Documentation completeness
- Test coverage adequacy

**ai architecture analysis**:
```yaml
ai architecture analysis:
  stage: ai-review
  extends: .claude-code-base
  script:
    - |
      ARCH_PROMPT="Analyze the architecture and design of this project:

      1. **Module Structure**: Review package organization and dependencies
      2. **Design Patterns**: Identify patterns used and their appropriateness
      3. **SOLID Principles**: Check adherence to SOLID principles
      4. **Scalability**: Assess potential scaling issues
      5. **Maintainability**: Evaluate code maintainability and technical debt

      Focus on files changed in this MR and their impact on overall architecture."

      claude -p "$ARCH_PROMPT" \
        --permission-mode viewOnly \
        --allowedTools "Read(*) Grep(*) Glob(*) mcp__gitlab" \
        > ai_architecture.md
  rules:
    - if: '$ENABLE_AI_ARCHITECTURE == "true"'
      when: always
    - when: manual
  allow_failure: true
```

#### 2. AI Assist Stage (Post-Build Help)

Runs after build/test stages to provide assistance with failures.

**ai test failure analysis**:
```yaml
ai test failure analysis:
  stage: ai-assist
  extends: .claude-code-base
  needs:
    - job: "unit test"
      artifacts: true
      optional: true
  script:
    - |
      if [ ! -d "build/test-results" ]; then
        echo "No test results found, skipping analysis"
        exit 0
      fi
    - |
      FAILURE_PROMPT="Analyze the test failures in this pipeline:

      1. **Failed Tests**: Review test failure messages and stack traces
      2. **Root Causes**: Identify underlying causes of failures
      3. **Fix Suggestions**: Provide specific code fixes with examples
      4. **Prevention**: Suggest improvements to prevent similar failures

      Test results are in: build/test-results/ and build/reports/tests/
      Provide actionable fixes with code snippets."

      claude -p "$FAILURE_PROMPT" \
        --permission-mode viewOnly \
        --allowedTools "Read(*) Grep(*) Glob(*)" \
        > ai_test_analysis.md
  rules:
    - if: '$ENABLE_AI_TEST_ANALYSIS == "true"'
      when: on_failure
    - when: on_failure
      allow_failure: true
```

**ai code generation**:
```yaml
ai code generation:
  stage: ai-assist
  extends: .claude-code-base
  script:
    - echo "⚠ WARNING: This job has write permissions"
    - |
      GEN_PROMPT="${AI_FLOW_INPUT:-"Implement the requested feature based on MR description:

      1. **Requirements**: Understand the feature requirements
      2. **Implementation**: Write clean, well-documented code
      3. **Conventions**: Follow project coding standards
      4. **Testing**: Include unit tests if applicable
      5. **Documentation**: Update relevant documentation"}"

      claude -p "$GEN_PROMPT" \
        --permission-mode acceptEdits \
        --allowedTools "Read(*) Edit(*) Write(*) Grep(*) Glob(*)" \
        > ai_generation.md
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web" && $RUN_AI_GENERATION == "true"'
      when: always
    - when: manual
  allow_failure: true
```

#### 3. AI Debugging (.post Stage)

Runs on pipeline failure to analyze and provide troubleshooting guidance.

**ai pipeline debug**:
```yaml
ai pipeline debug:
  stage: .post
  extends: .claude-code-base
  script:
    - |
      DEBUG_PROMPT="Analyze this failed pipeline and provide troubleshooting guidance:

      1. **Failed Jobs**: Identify which jobs failed and their error messages
      2. **Root Cause**: Determine the underlying cause of failures
      3. **Fix Steps**: Provide step-by-step resolution guide
      4. **Prevention**: Suggest changes to prevent future failures

      Pipeline ID: ${CI_PIPELINE_ID}
      Pipeline URL: ${CI_PIPELINE_URL}
      Commit: ${CI_COMMIT_SHA}
      Branch: ${CI_COMMIT_REF_NAME}

      Use GitLab MCP to access pipeline logs and job details."

      claude -p "$DEBUG_PROMPT" \
        --permission-mode viewOnly \
        --allowedTools "Read(*) Grep(*) mcp__gitlab" \
        > ai_debug.md
  rules:
    - if: '$ENABLE_AI_PIPELINE_DEBUG == "true"'
      when: on_failure
    - when: on_failure
      allow_failure: true
```

### Configuration

#### Required Variables

Configure in GitLab Settings > CI/CD > Variables:

- `ANTHROPIC_API_KEY`: Claude API key (masked, required for all AI jobs)

#### Optional Feature Flags

Enable automatic triggers (default: manual):

- `ENABLE_AI_REVIEW`: Auto-run code review on MRs
- `ENABLE_AI_ARCHITECTURE`: Auto-run architecture analysis
- `ENABLE_AI_TEST_ANALYSIS`: Auto-run test analysis on failures
- `ENABLE_AI_PIPELINE_DEBUG`: Auto-run debug on pipeline failure

#### Configuration Variables

Customize AI behavior:

- `CLAUDE_MODEL`: AI model (default: claude-sonnet-4)
- `CLAUDE_DEBUG`: Enable verbose output (default: false)
- `CLAUDE_PERMISSION_MODE`: Permission mode (default: viewOnly)
- `GITLAB_MCP_ENABLED`: Enable GitLab MCP server (default: true)
- `AI_FLOW_INPUT`: Custom prompt (overrides default)
- `AI_FLOW_CONTEXT`: Additional context information
- `AI_FLOW_EVENT`: Event type information

### Safety and Permissions

#### Permission Modes

**viewOnly** (default for analysis):
- Read files
- Search codebase
- Access GitLab API via MCP
- Cannot modify code
- Used for: review, analysis, debugging

**acceptEdits** (code generation only):
- All viewOnly permissions
- Write/edit files
- Create new files
- Requires manual trigger
- Used for: code generation

#### Safety Guarantees

1. **Never Blocking**: All AI jobs have `allow_failure: true`
2. **Manual by Default**: Automatic triggers require explicit flag
3. **Read-Only Default**: Analysis jobs cannot modify code
4. **Explicit Write**: Code generation requires manual confirmation
5. **Isolated Execution**: AI jobs run in isolated containers

### GitLab MCP Server Integration

The GitLab MCP (Model Context Protocol) server enables Claude Code to interact with GitLab API.

**Setup Script** (`ci/scripts/mcp-server-setup.sh`):
```bash
#!/bin/bash
set -euo pipefail

mkdir -p .claude-code

# Create MCP server configuration
cat > .claude-code/mcp-config.json <<EOF
{
  "mcpServers": {
    "gitlab": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-gitlab"],
      "env": {
        "GITLAB_PERSONAL_ACCESS_TOKEN": "${CI_JOB_TOKEN}",
        "GITLAB_API_URL": "${CI_API_V4_URL}"
      }
    }
  }
}
EOF

# Create Claude Code configuration
cat > .claude-code/config.yml <<EOF
mcp:
  enabled: true
  servers:
    - name: gitlab
      config_file: .claude-code/mcp-config.json

settings:
  model: "${CLAUDE_MODEL:-claude-sonnet-4}"
  permission_mode: "${CLAUDE_PERMISSION_MODE:-viewOnly}"
EOF

echo "✅ MCP server setup completed"
```

**Capabilities**:
- Read MR details and diff
- Post comments to MR
- Access pipeline logs
- Query project files
- Search issues and commits

### Complete AI Integration Example

**Project Structure**:
```
project/
├── .gitlab-ci.yml           # Main pipeline with AI include
├── ci/
│   ├── base.gitlab-ci.yml   # Standard CI/CD jobs
│   ├── ai.gitlab-ci.yml     # AI jobs configuration
│   └── scripts/
│       ├── mcp-server-setup.sh
│       └── ai-flow-runner.sh
└── .commitlintrc.json
```

**.gitlab-ci.yml**:
```yaml
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
  - plan
  - .post
```

**Workflow**:
```
Developer creates MR
  ↓
Init stage: commitlint, MR title (blocking)
  ↓
AI Review stage: code review (manual, viewOnly)
  ├─ ai code review → Posts review to MR
  └─ ai architecture analysis → Posts analysis to MR
  ↓
Build stage: compile code
  ↓
Test stage: run tests
  ├─ Success → Continue to quality
  └─ Failure → AI test analysis (automatic if enabled)
        └─ Posts failure analysis to MR
  ↓
Quality stage: spotless, sonarqube
  ↓
[If pipeline fails]
  ↓
.post stage: ai pipeline debug (automatic if enabled)
  └─ Posts debug analysis to MR
```

### AI Job Artifacts

All AI jobs produce artifacts for review:

```yaml
artifacts:
  paths:
    - "ai_*.md"          # AI analysis markdown reports
    - "*.ai.log"         # Execution logs
  expire_in: 1 week
  when: always
```

**Artifact Contents**:
- `ai_review.md`: Code review feedback
- `ai_architecture.md`: Architecture analysis
- `ai_test_analysis.md`: Test failure analysis
- `ai_generation.md`: Code generation report
- `ai_debug.md`: Pipeline debug analysis
- `*.ai.log`: Execution logs and errors

### Troubleshooting AI Jobs

#### Issue: AI job fails with "ANTHROPIC_API_KEY not set"

**Problem**: API key not configured

**Fix**:
```
1. Go to Settings > CI/CD > Variables
2. Add variable:
   - Key: ANTHROPIC_API_KEY
   - Value: [your Claude API key]
   - Masked: ☑
   - Protected: ☐
3. Re-run pipeline
```

#### Issue: MCP server setup fails

**Problem**: GitLab MCP server cannot connect

**Check**:
- CI_JOB_TOKEN has API access
- CI_API_V4_URL is correct
- Network allows outbound npm requests

**Fix**:
```yaml
# Disable MCP if not needed
variables:
  GITLAB_MCP_ENABLED: "false"
```

#### Issue: AI review not posted to MR

**Problem**: Comment posting fails

**Check**:
- Running in MR context (CI_MERGE_REQUEST_IID set)
- CI_JOB_TOKEN has MR comment permissions
- ai_review.md file exists

**Debug**:
```bash
# Check MR context
echo "MR IID: ${CI_MERGE_REQUEST_IID:-not set}"

# Check artifact
ls -la ai_review.md

# Test API access
curl -s --header "PRIVATE-TOKEN: ${CI_JOB_TOKEN}" \
  "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/merge_requests/${CI_MERGE_REQUEST_IID}"
```

#### Issue: AI job times out

**Problem**: Claude Code execution exceeds timeout

**Fix**:
```yaml
ai code review:
  timeout: 15 minutes  # Increase from default 10 min
```

#### Issue: Cost concerns

**Problem**: AI jobs consuming too many tokens

**Solution**:
```yaml
# Keep AI jobs manual (default)
rules:
  - when: manual

# Or limit to specific branches
rules:
  - if: '$CI_COMMIT_BRANCH == "main"'
    when: manual
```

**Monitor usage**:
- Review Anthropic Console for usage
- Analyze `*.ai.log` artifacts for token counts
- Adjust CLAUDE_MODEL to smaller model if needed

## Best Practices

### 1. Fail Fast

Place quick, blocking checks early:

```yaml
stages:
  - init        # Fast validations (< 1 min)
  - build       # Compilation (2-5 min)
  - test        # Tests (5-15 min)
  - quality     # Deep analysis (10-30 min)
```

### 2. Cache Dependencies

Cache to speed up builds:

```yaml
cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .gradle
    - node_modules
    - .m2
  policy: pull-push
```

### 3. Parallel Execution

Run independent jobs in parallel:

```yaml
test:unit:
  stage: test
  script: gradle test

test:integration:
  stage: test
  script: gradle integrationTest

# Both run simultaneously
```

### 4. Meaningful Artifacts

Save useful artifacts:

```yaml
artifacts:
  paths:
    - build/libs/*.jar      # Build outputs
    - build/reports/        # Test reports
    - CHANGELOG.md          # Generated changelog
  reports:
    junit: build/test-results/test/**/TEST-*.xml
    coverage_report:
      coverage_format: cobertura
      path: build/reports/jacoco/test/jacocoTestReport.xml
  expire_in: 1 week
```

### 5. Clear Job Names

Use descriptive job names:

```yaml
✓ Good:
- commitlint
- build:gradle
- test:unit
- test:integration
- deploy:production

✗ Bad:
- job1
- validate
- run-tests
- deploy
```

### 6. Environment Variables

Use CI/CD variables for configuration:

```yaml
variables:
  GRADLE_OPTS: "-Dorg.gradle.daemon=false"
  MAVEN_OPTS: "-Dmaven.repo.local=.m2/repository"

# Or use GitLab CI/CD variables (Settings > CI/CD > Variables)
script:
  - gradle build -Pversion=${CI_COMMIT_TAG} -PmavenUser=${MAVEN_USER} -PmavenPassword=${MAVEN_PASSWORD}
```

## Troubleshooting

### Commitlint Failures

**Problem**: Commits fail validation

**Check**:
```bash
# Test locally
npx commitlint --from=origin/main --to=HEAD

# Test specific commit
echo "feat: add feature" | npx commitlint
```

**Fix**:
```bash
# Rebase to fix commits
git rebase -i origin/main

# Change commit messages to follow conventional commits
```

### MR Title Validation Fails

**Problem**: MR title doesn't follow format

**Check**: Does title match pattern?
```
^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+
```

**Fix**: Update MR title in GitLab UI

### Build Cache Issues

**Problem**: Stale cache causing failures

**Fix**:
```yaml
# Clear cache for branch
# Settings > CI/CD > Pipelines > Clear runner caches

# Or disable cache temporarily
cache: []
```

### Coverage Below Threshold

**Problem**: Coverage drops below minimum

**Check**:
```bash
# Run locally
gradle jacocoTestReport

# View report
open build/reports/jacoco/test/html/index.html
```

**Fix**: Add tests to increase coverage

## Summary

A well-configured GitLab CI/CD pipeline:

- **Validates early**: Conventional commits, MR titles (init stage)
- **Builds reliably**: Consistent compilation, caching
- **Tests thoroughly**: Unit, integration, coverage
- **Ensures quality**: Code analysis, security scans
- **Automates releases**: Versioning, changelog, publishing
- **Deploys safely**: Staged deployments, manual gates

Follow these patterns for robust, automated delivery.

## References

- [Conventional Commits](../git/conventional-commits.md)
- [PR Guidelines](../git/pr-guidelines.md)
- [Commitlint](https://commitlint.js.org/)
- [Git Cliff](https://git-cliff.org/)
- [GitLab CI/CD Documentation](https://docs.gitlab.com/ee/ci/)
