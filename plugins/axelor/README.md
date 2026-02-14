# Axelor Development Accelerator

Claude Code plugin for accelerating Axelor ERP 8.0 development.

**Version**: 1.0.0
**Repository**: git@git.axelor.com:aop/addons/axelor-enterprise/ia/axelor-claude-marketplace.git

---

## Quick Reference Guide

| Need | Command |
|------|---------|
| Develop a feature from scratch | `/develop-complete-feature` |
| Implement from existing specs | `/develop` |
| Analyze requirements (text or PDF/DOCX) | `/analyze-requirements` |
| Analyze Redmine tickets | `/analyze-redmine-tickets` |
| Analyze code conformity & quality | `/analyze-code` |
| Git operations (commit, PR, push) | `/git` |

---

## Commands

### /develop-complete-feature

**Complete development workflow** - From requirement expression to production-ready code.

```bash
/develop-complete-feature "Feature description"
```

**Features:**
- **19 steps** orchestrated in **6 phases**
- **4 mandatory user validation** gates
- **Checkpoint commits** for rollback
- **Duration**: 4-8 hours (including interactions)

**Phases:**
1. **Analysis & Specification** (30-60 min) - Business analysis, AOS gap analysis, refinement
2. **Models & Views** (1-2h) - Architecture, XML domains, XML views
3. **Corrections** (variable) - Iterative loop based on feedback
4. **Java** (2-3h) - Services, repositories, controllers
5. **Tests & Data** (1-2h) - Unit tests, demo data
6. **Finalization** (15-30 min) - Functional validation, push

**Workflow summary:**
```
Module setup → Business analysis → AOS gap analysis → Specification refinement
→ [VALIDATION 1] → Architecture → Domains → Views → [VALIDATION 2]
→ Corrections → Java code → Code review → Build → [VALIDATION 3]
→ Tests → Demo data → Functional validation → [VALIDATION 4] → Push
```

**Resume after interruption:**
```bash
claude --resume
```

---

### /develop

**Modular development workflow** - From existing specifications.

```bash
/develop [specification-file] [output-directory] [options]
```

**Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `specification-file` | Path to specs (`.md` or `epic-us/` directory) | *required* |
| `output-directory` | Directory for architecture/reports | `docs/development` |
| `--architecture-file=path` | Existing architecture to extend | *auto-detect* |
| `--resume-from-phase=N` | Resume from phase N (1-7) | - |
| `--skip-tests` | Skip test generation | - |
| `--auto-commit` | Enable automatic checkpoint commits | *disabled* |

**7 phases with validation:**
1. Architecture Design (conditional: CREATE or EXTEND)
2. Domain Generation (XML + XSD/naming/semantic validation)
3. View Generation (forms, grids, menus, actions)
4. Java Code Generation (services, repos, controllers)
5. Unit Test Generation (optional, >80% coverage)
6. Code Review & Validation
7. Final Commit

**Modes:**
- **CREATE**: New complete architecture
- **EXTEND**: Extend existing architecture

**Examples:**
```bash
# New feature
/develop docs/detailed-specifications.md

# With custom directory
/develop docs/inventory-specs.md docs/inventory-dev

# Extend existing architecture
/develop docs/bugfix-spec.md docs/dev --architecture-file=docs/architecture.md

# Resume interrupted workflow
/develop docs/spec.md docs/dev --resume-from-phase=5

# Without tests
/develop docs/spec.md docs/dev --skip-tests

# With automatic commits enabled
/develop docs/spec.md docs/dev --auto-commit
```

---

### /analyze-requirements

**Complete requirements analysis** - From raw requirement to EPICs/User Stories.

```bash
/analyze-requirements [requirement] [output-directory]
```

**Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `requirement` | Text OR path to PDF/DOCX (up to 150+ pages) | *required* |
| `output-directory` | Output directory | `docs` |

**4 phases:**
1. **Business Analysis** → `analysis-report.md`
2. **AOS Gap Analysis** → `gap-analysis-report.md` (identifies 30-50% reuse)
3. **Requirements Refinement** → `detailed-specifications.md`
4. **EPIC/US Generation** → `epic-us-breakdown.textile` (Redmine format)

**Examples:**
```bash
# From text
/analyze-requirements "CRM module with leads and opportunities" analysis/crm

# From document
/analyze-requirements path/to/requirements.pdf analysis/project
```

**Deliverables:**
| File | Content |
|------|---------|
| `analysis-report.md` | Business analysis with clarifying questions |
| `gap-analysis-report.md` | REUSE/EXTEND/DEVELOP_NEW decisions |
| `detailed-specifications.md` | Detailed specifications |
| `epic-us-breakdown.textile` | EPICs and User Stories (Redmine import) |

---

### /analyze-redmine-tickets

**Redmine ticket scraping and analysis** - Generates a requirements registry.

```bash
/analyze-redmine-tickets <url> [output-directory]
```

**Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `url` | Project OR ticket Redmine URL | *required* |
| `output-directory` | Output directory | `./Analysis/Ticket` |

**Modes (auto-detection):**
- **Project**: `https://redmine.axelor.com/projects/axerp` → all tickets
- **Ticket**: `https://redmine.axelor.com/issues/104267` → single ticket

**Prerequisites:**
```env
# .env
REDMINE_API=your_api_key_here
```

**Examples:**
```bash
# Analyze all tickets from a project
/analyze-redmine-tickets https://redmine.axelor.com/projects/axerp

# Analyze a single ticket
/analyze-redmine-tickets https://redmine.axelor.com/issues/104267

# With custom directory
/analyze-redmine-tickets https://redmine.axelor.com/issues/104267 ./my-analysis
```

**Output structure:**
```
{output}/
├── Scrap/{Tracker}/*.md           # Scraped tickets
├── analysis/ticket-*.json         # Individual analyses
├── requirements-registry.json     # Requirements registry
├── specs/{Tracker}/REQ-XXX.md     # Generated specs
└── index/by-{module,entity,tracker}.json
```

---

### /analyze-code

**Code conformity and quality analysis** - Comprehensive code audit with optional fix specification generation.

```bash
/analyze-code <path> [--output <output-dir>] [--mode quick|deep] [--spec] [--priority level] [--issue <file>]
```

**Parameters:**
| Parameter | Description | Default |
|-----------|-------------|---------|
| `path` | File or directory to analyze | *required* |
| `--output` | Output directory for reports | `docs/analysis/` |
| `--mode` | Analysis depth (quick or deep) | `deep` |
| `--spec` | Generate fix specification after analysis | disabled |
| `--priority` | Priority filter for spec (critical/high/medium/all) | `all` |
| `--issue` | Path to bug/issue description file for investigation | disabled |

**Analysis Modes:**
- **quick**: Fast analysis using existing validators (style, naming, XML validation)
- **deep**: Comprehensive analysis including performance and security checks

**Examples:**
```bash
# Analyze single file (outputs to docs/analysis/)
/analyze-code src/main/java/com/axelor/apps/crm/service/CustomerServiceImpl.java
# → docs/analysis/code-analysis-report.md

# Analyze directory with custom output directory
/analyze-code src/main/java/com/axelor/apps/crm/ --output reports/
# → reports/code-analysis-report.md

# Quick analysis to specific directory
/analyze-code src/main/java/ --mode quick --output analysis/
# → analysis/code-analysis-report.md

# Analyze and generate fix specification (docs/analysis/)
/analyze-code src/main/java/com/axelor/apps/crm/ --spec
# → docs/analysis/code-analysis-report.md
# → docs/analysis/fix-specification.md

# Analyze and generate spec in custom directory
/analyze-code src/main/java/com/axelor/apps/crm/ --spec --output reports/
# → reports/code-analysis-report.md
# → reports/fix-specification.md

# Complete workflow: analyze deeply and prepare fixes for high+ priority
/analyze-code src/main/java/com/axelor/apps/sale/ --mode deep --spec --priority high --output reports/
# → reports/code-analysis-report.md
# → reports/fix-specification.md

# Investigate specific bug/issue
/analyze-code src/main/java/com/axelor/apps/sale/ --issue bug-description.txt
# → docs/analysis/code-analysis-report.md (with Bug Investigation section + full conformity analysis)

# Bug investigation with spec generation
/analyze-code src/main/java/com/axelor/apps/sale/ --issue bug-description.txt --spec --output reports/
# → reports/code-analysis-report.md (bug investigation + conformity analysis)
# → reports/fix-specification.md
```

**Report Categories:**
1. **Bad Practices** (CRITICAL → HIGH → MEDIUM → LOW)
   - Style violations (emoji, French comments)
   - Code smells and anti-patterns
   - Naming convention violations

2. **Optimization Opportunities**
   - Code duplication
   - Inefficient algorithms
   - Refactoring suggestions

3. **Performance Issues**
   - N+1 query patterns
   - Missing @Transactional annotations
   - Inefficient data structures
   - Complex methods

4. **Security Risks** (deep mode only)
   - SQL injection vulnerabilities
   - Hardcoded credentials
   - Missing input validation
   - Sensitive data in logs

**Use Cases:**
- **Pre-commit**: Quick mode on changed files
- **Code Review**: Deep mode for PR analysis
- **CI/CD**: Automated quality gates
- **Refactoring**: Identify technical debt
- **Onboarding**: Learn code quality standards

**Generated Files:**
- **Analysis report**: `code-analysis-report.md` (in --output directory or `docs/analysis/` by default)
- **Fix specification** (if --spec used): `fix-specification.md` (same directory as analysis report)

**Workflow Integration:**
```bash
# Option 1: Analyze only (default: docs/analysis/)
/analyze-code src/main/java/com/axelor/apps/crm/
# → docs/analysis/code-analysis-report.md

# Option 2: Analyze to custom directory
/analyze-code src/main/java/com/axelor/apps/crm/ --output reports/
# → reports/code-analysis-report.md

# Option 3: Analyze and generate fix spec (default directory)
/analyze-code src/main/java/com/axelor/apps/crm/ --spec --priority high
# → docs/analysis/code-analysis-report.md
# → docs/analysis/fix-specification.md

# Option 4: Use fix spec with /develop
/analyze-code src/main/java/com/axelor/apps/crm/ --spec
/develop docs/analysis/fix-specification.md
```

---

### /git

**Git operations with automatic validation** - Secure commits, PR, push.

```bash
/git <natural language request>
```

**Supported operations:**
| Action | Example |
|--------|---------|
| Commit | `/git commit my changes to sale module` |
| Create PR | `/git create a PR for my authentication feature` |
| Push | `/git push my changes` |
| Fix message | `/git fix my commit message` |
| Safe stage | `/git stage files safely` |

**Automatic validations:**
- **file-safety-checker**: Blocks artifacts, IDE configs, secrets
- **commitlint-validator**: Conventional commits format
- **pr-analyzer**: Generates PR description with risk analysis
- **mr-title-validator**: Validates MR titles for CI

**Features:**
- Conventional commits required
- No emojis
- English only
- Confirmation before MR/PR creation
- Maximum 2 sentences in body

**Daily workflow example:**
```bash
/git create branch for sale discount feature
/git commit add discount field to SaleOrder
/git commit implement discount calculation
/git push changes
/git create PR for sale discount feature
```

---

## Agents (13)

| Agent | Role |
|-------|------|
| `business-analyst` | Initial requirements analysis |
| `aos-analyzer` | Comparison with existing AOS |
| `requirements-refiner` | Conversational spec refinement |
| `agile-agent` | EPIC/User Story generation |
| `architect` | Technical architecture design |
| `domain-agent` | XML domain generation |
| `view-agent` | XML view generation |
| `java-agent` | Java code generation |
| `code-reviewer` | Code quality review |
| `functional-validator` | Functional validation |
| `git-agent` | Git operations |
| `cicd-agent` | CI/CD setup and troubleshooting |
| `redmine-agent` | Redmine ticket analysis |

---

## Skills (33)

### XML Validation
- `axelor-xml-validator` - Official XSD validation (domains & views)
- `axelor-naming-checker` - Naming conventions
- `axelor-semantic-validator` - Domain semantic coherence
- `axelor-view-semantic-validator` - View semantic coherence
- `axelor-view-extension-validator` - View extension rules

### AOS Analysis
- `aos-documentation-fetcher` - AOS documentation
- `aos-entity-searcher` - AOS entity search
- `aos-field-comparator` - Field comparison
- `aos-git-regression-finder` - Regression analysis

### Generation & Analysis
- `axelor-controller-method-extractor` - Controller method extraction
- `axelor-er-diagram-generator` - ASCII ER diagrams
- `axelor-java-style-validator` - Java style validation

### Git & Commits
- `commitlint-validator` - Commit message validation
- `commitlint-config-generator` - Commitlint configuration
- `mr-title-validator` - MR title validation
- `file-safety-checker` - File safety before staging
- `pr-analyzer` - PR analysis with risks

### CI/CD
- `gitlab-ci-generator` - .gitlab-ci.yml generation
- `ci-validation-script-generator` - CI validation scripts
- `git-cliff-config-generator` - Changelog configuration
- `quality-gate-configurator` - Quality gates configuration
- `pipeline-troubleshooter` - Pipeline diagnostics

### Requirements & Tickets
- `functional-spec-consistency-checker` - Spec consistency
- `redmine-ticket-parser` - Redmine ticket parsing
- `ticket-deep-analyzer` - Deep ticket analysis
- `ticket-duplicate-detector` - Duplicate detection
- `requirements-registry-builder` - Registry building

### Estimation & Planning
- `epic-estimator` - Dev/QA/PM-BA estimation
- `us-dependency-mapper` - US dependency mapping
- `us-quality-validator` - US/EPIC quality validation

---

## Installation

### Via Marketplace (Recommended)

```bash
# Add Axelor internal marketplace
/plugin marketplace add git@git.axelor.com:aop/addons/axelor-enterprise/ia/axelor-claude-marketplace.git

# Install plugin
/plugin install axelor
```

### Via DevContainer

If your Axelor project uses DevContainer, the plugin is automatically installed.

### Python Dependencies

Some skills require Python:

```bash
pip install lxml requests
```

Required for: `axelor-xml-validator`, `axelor-semantic-validator`

---

## Support

**Repository**: git@git.axelor.com:aop/addons/axelor-enterprise/ia/axelor-claude-marketplace.git
**Contact**: ai-team@axelor.com

---

## License

Proprietary - Axelor Internal Use Only
