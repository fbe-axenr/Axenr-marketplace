---
name: gitlab-ci-generator
description: Generate complete .gitlab-ci.yml pipeline configurations for Axelor projects based on project type, build tool, and required stages
allowed-tools: ["Bash", "Read", "Write"]
---

# GitLab CI Generator

## Mission

Generate production-ready `.gitlab-ci.yml` configurations for Axelor projects with proper stage ordering, quality gates, caching strategies, and artifact management. Ensures pipelines follow Axelor standards with blocking validation stages.

## Input Parameters

1. **Project Type** (required):
   - `standalone-rnd`: Standalone R&D module (e.g., axelor-ged)
   - `client-project`: Client/ERP module (inherits from parent)
   - `library`: Shared library

2. **Build Tool** (required):
   - `gradle`: Gradle build (specify version)
   - `maven`: Maven build (specify version)
   - `node`: Node.js/npm build

3. **Required Stages** (required):
   - `init`: Validation (commitlint, MR title) - BLOCKING
   - `build`: Compilation, artifact generation
   - `test`: Unit tests, integration tests
   - `quality`: Code quality (spotless, sonarqube)
   - `plan`: Publishing, changelog generation
   - `deploy`: Deployment (optional)
   - `cleanup`: Resource cleanup (optional)

4. **Optional Features**:
   - `commitlint`: Commit message validation (default: true)
   - `mr-title-validation`: MR title validation (default: true)
   - `squash-check`: Squash commits requirement (default: false)
   - `spotless`: Code formatting check (default: true for Java)
   - `sonarqube`: Code quality analysis (default: false)
   - `changelog`: Git-cliff changelog generation (default: false)
   - `coverage-threshold`: Test coverage minimum (default: 80%)

5. **AI Integration** (optional):
   - `ai-review`: AI-powered code review on MRs
   - `ai-architecture`: Architecture analysis
   - `ai-test-analysis`: Automatic test failure analysis
   - `ai-code-generation`: AI-assisted code generation (manual trigger)
   - `ai-pipeline-debug`: Pipeline failure debugging (.post stage)

## AI Stage Configuration

The gitlab-ci-generator skill now supports AI-powered assistance using Claude Code CLI and GitLab MCP server integration.

### AI Stages

**ai-review Stage** (runs early, before build):
- `ai code review`: Reviews MR for code quality, best practices, security issues
- `ai architecture analysis`: Analyzes design patterns, SOLID principles, architecture

**ai-assist Stage** (runs after build/test):
- `ai test failure analysis`: Analyzes test failures and suggests fixes (on_failure)
- `ai code generation`: Generates code based on MR description (manual)

**.post Stage** (runs on pipeline failure):
- `ai pipeline debug`: Analyzes pipeline failures and provides troubleshooting

### Required Variables

Must be configured in GitLab CI/CD Settings:
- `ANTHROPIC_API_KEY`: Claude API key (required for all AI jobs)

### Optional Configuration Variables

**Feature Flags** (enable automatic triggers):
- `ENABLE_AI_REVIEW`: Auto-run code review on MRs (default: false → manual)
- `ENABLE_AI_ARCHITECTURE`: Auto-run architecture analysis (default: false → manual)
- `ENABLE_AI_TEST_ANALYSIS`: Auto-run test analysis on failures (default: false → manual)
- `ENABLE_AI_PIPELINE_DEBUG`: Auto-run debug on pipeline failure (default: false → manual)

**Configuration**:
- `CLAUDE_MODEL`: AI model to use (default: claude-sonnet-4)
- `CLAUDE_DEBUG`: Enable verbose output (default: false)
- `CLAUDE_PERMISSION_MODE`: Permission mode (default: viewOnly)
- `GITLAB_MCP_ENABLED`: Enable GitLab MCP server (default: true)

**Customization**:
- `AI_FLOW_INPUT`: Custom prompt (overrides default)
- `AI_FLOW_CONTEXT`: Additional context information
- `AI_FLOW_EVENT`: Event type information

### AI Job Templates

When AI integration is enabled, the generator creates:

1. **ci/ai.gitlab-ci.yml**: Complete AI stage configuration
2. **ci/scripts/mcp-server-setup.sh**: GitLab MCP server setup script
3. **ci/scripts/ai-flow-runner.sh**: Generic AI workflow runner

Templates are loaded from:
- @skills/gitlab-ci-generator/reference/ai-stage-templates.yml
- @skills/gitlab-ci-generator/reference/scripts/

### Safety and Permissions

**Default Behavior** (safety-first):
- All AI jobs are **manual** by default
- All AI jobs have `allow_failure: true` (never block pipeline)
- Review/analysis jobs use `viewOnly` permission mode
- Code generation jobs require explicit manual trigger

**Permission Modes**:
- `viewOnly`: Read-only access (review, analysis, debugging)
- `acceptEdits`: Write access (code generation) - MANUAL ONLY

### AI Integration Example

```yaml
# In .gitlab-ci.yml
include:
  - local: 'ci/ai.gitlab-ci.yml'

stages:
  - init
  - ai-review      # AI jobs run early
  - build
  - test
  - ai-assist      # AI assistance after tests
  - quality
  - plan
  - .post          # AI debugging on failure
```

## Process

1. Load stage templates from @skills/gitlab-ci-generator/reference/stage-templates.yml
2. Load build tool patterns from reference/ (gradle-patterns.yml, maven-patterns.yml, or node-patterns.yml)
3. Generate complete .gitlab-ci.yml with:
   - Stage definitions in correct order
   - Init stage with blocking validations
   - Build stage with caching and artifacts
   - Test stage with coverage reporting
   - Quality stage with formatting/analysis
   - Optional plan/deploy/cleanup stages
4. Validate YAML syntax
5. Provide configuration explanation

## Output Format

```yaml
# Generated .gitlab-ci.yml for <project-name>
# Project Type: <type>
# Build Tool: <tool> <version>
# Generated: <timestamp>

stages:
  - init
  - build
  - test
  - quality
  [- plan]
  [- deploy]
  [- cleanup]

# Cache configuration
cache:
  [build-tool-specific cache config]

# Init Stage (BLOCKING)
commitlint:
  [job config]

validate-mr-title:
  [job config]

# Build Stage
build:
  [job config with caching and artifacts]

# Test Stage
test:
  [job config with coverage]

# Quality Stage
spotless:
  [job config]

[sonarqube]:
  [job config if enabled]

# Plan Stage (Optional)
[changelog]:
  [job config if enabled]

# Deploy Stage (Optional)
[deploy]:
  [job config if enabled]

# Cleanup Stage (Optional)
[cleanup]:
  [job config if enabled]
```

## Validation Rules

1. **YAML Syntax**: Valid YAML structure
2. **Stage Order**: Stages defined in correct dependency order
3. **Required Jobs**: Init stage has at least commitlint
4. **Blocking Jobs**: Init stage jobs have `allow_failure: false`
5. **Cache Paths**: Cache paths exist and are appropriate for build tool
6. **Artifact Paths**: Artifact paths valid
7. **Image Tags**: Docker images use specific version tags (not `latest`)

## Reference Files

**Standard CI/CD Templates**:
- @skills/gitlab-ci-generator/reference/stage-templates.yml: Individual stage templates
- @skills/gitlab-ci-generator/reference/job-templates.yml: Reusable job patterns
- @skills/gitlab-ci-generator/reference/gradle-patterns.yml: Gradle-specific configurations
- @skills/gitlab-ci-generator/reference/maven-patterns.yml: Maven-specific configurations
- @skills/gitlab-ci-generator/reference/node-patterns.yml: Node.js-specific configurations
- @skills/gitlab-ci-generator/reference/optimization-guide.md: Performance best practices

**AI Integration Templates**:
- @skills/gitlab-ci-generator/reference/ai-stage-templates.yml: AI job templates for Claude Code
- @skills/gitlab-ci-generator/reference/scripts/mcp-server-setup.sh: GitLab MCP server setup
- @skills/gitlab-ci-generator/reference/scripts/ai-flow-runner.sh: Generic AI workflow runner

## Examples

### Example 1: Standalone R&D Module with Gradle (AOP 8)

**Input**:
```
Project Type: standalone-rnd
Build Tool: gradle 8.5
Java Version: 21
Stages: init, build, test, quality
Features: commitlint, mr-title-validation, spotless
Coverage Threshold: 80%
```

**Output**: Complete .gitlab-ci.yml with:
- Init stage: commitlint + validate-mr-title (blocking)
- Build stage: Gradle build with dependency caching
- Test stage: Unit tests with JaCoCo coverage (80% threshold)
- Quality stage: Spotless formatting check

### Example 2: Client Project with Gradle (AOP 7)

**Input**:
```
Project Type: client-project
Build Tool: gradle 8.5
Java Version: 11
Stages: build, test
Features: none (inherits from parent)
```

**Output**: Minimal .gitlab-ci.yml with:
- Build stage: Maven build with .m2 caching
- Test stage: Unit tests only

### Example 3: Library with Node.js

**Input**:
```
Project Type: library
Build Tool: node 20
Stages: init, build, test, plan
Features: commitlint, changelog
```

**Output**: Complete .gitlab-ci.yml with:
- Init stage: commitlint
- Build stage: npm install + build with node_modules caching
- Test stage: npm test
- Plan stage: git-cliff changelog generation

### Example 4: Project with AI Integration

**Input**:
```
Project Type: standalone-rnd
Build Tool: gradle 8.5
Stages: init, ai-review, build, test, ai-assist, quality, .post
Features: commitlint, mr-title-validation, spotless
AI Features: ai-review, ai-test-analysis, ai-pipeline-debug
Trigger Mode: manual (default)
```

**Output**: Complete pipeline with AI integration:

**Main .gitlab-ci.yml**:
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
  - .post
```

**ci/ai.gitlab-ci.yml**:
- AI code review job (manual, viewOnly)
- AI architecture analysis job (manual, viewOnly)
- AI test failure analysis job (on_failure, viewOnly)
- AI pipeline debug job (on_failure in .post stage, viewOnly)

**ci/scripts/**:
- mcp-server-setup.sh: GitLab MCP server configuration
- ai-flow-runner.sh: Generic AI workflow runner

**Variables** (configured in GitLab UI):
- ANTHROPIC_API_KEY: [User's Claude API key]
- ENABLE_AI_REVIEW: "false" (manual by default)
- ENABLE_AI_TEST_ANALYSIS: "false" (manual by default)
- ENABLE_AI_PIPELINE_DEBUG: "false" (manual by default)

## Common Issues and Fixes

### Issue: Cache not working

**Problem**: Build downloads dependencies every time

**Solution**:
- Verify cache key includes lock file (package-lock.json, gradle.lockfile)
- Check cache paths match build tool conventions
- Ensure runners have cache storage configured

### Issue: Init stage not blocking

**Problem**: MR can be merged even with invalid commits

**Solution**:
- Verify `allow_failure: false` on all init stage jobs
- Check GitLab Settings > Merge requests > "Pipelines must succeed" is enabled

### Issue: Coverage not reported

**Problem**: Test coverage not visible in MR

**Solution**:
- Ensure coverage tool generates reports (JaCoCo for Java, coverage.py for Python)
- Add `coverage: '/Total.*?(\d+\.\d+)%/'` regex to job
- Configure `artifacts:reports:coverage_report` for GitLab 15+

## Integration

Used by:
- cicd-agent: Step 2 (Create GitLab CI Pipeline)
- axelor-project-initializer: Initial project setup
- axelor: Module scaffolding

## Requirements

- Bash 4.0+
- YAML parsing capability
- Access to reference templates
- Understanding of GitLab CI/CD syntax
