# Epic Estimator Skill

**✅ PYTHON AUTOMATION AVAILABLE: `epic_estimator.py`**

Use this Python script for automated effort estimation. See Usage section below.

Provides standardized estimation with Dev/QA/PM-BA breakdown for User Stories and EPICs in Axelor projects.

## Purpose

This skill automates estimation calculation for User Stories by:
- Automatically analyzing functional specifications
- Applying estimations by component type
- Calculating breakdown by profile (Dev / QA / PM-BA)
- Proposing splitting for oversized US (XL)

## Skills Path Resolution

**CRITICAL**: Before executing this skill, you MUST determine the absolute path.

**Step 1: Find the plugin installation path**
```bash
PLUGIN_PATH=$(find /home -type d -name "axelor" -path "*/plugins/*" 2>/dev/null | head -1)
SKILLS_PATH="${PLUGIN_PATH}/skills"
DOCS_PATH="${PLUGIN_PATH}/docs"
```

**Step 2: Invoke the estimator script**
```bash
# Mode 1: Analyze a specification
python3 ${SKILLS_PATH}/epic-estimator/epic_estimator.py --spec path/to/specification.md

# Mode 2: Explicit components (JSON)
python3 ${SKILLS_PATH}/epic-estimator/epic_estimator.py --components '{"components": [
  {"type": "domains.complex", "name": "SaleOrderLineOption"},
  {"type": "views.form_complex", "name": "Options Panel"}
], "adjustments": ["testing.unit_tests"]}'

# Mode 3: List available components/adjustments
python3 ${SKILLS_PATH}/epic-estimator/epic_estimator.py --list-components
python3 ${SKILLS_PATH}/epic-estimator/epic_estimator.py --list-adjustments
```

## Usage

### Input

**Specification Mode**: Path to a Markdown specification file
- The script automatically parses sections 2 (Data Model), 3 (Views), 4 (Features), 6 (Cross-cutting)
- Extracts entities, views, services and integrations

**Explicit Components Mode**: JSON with the list of identified components
```json
{
  "components": [
    {"type": "domains.complex", "name": "SaleOrderLineOption", "fields": 9},
    {"type": "views.form_complex", "name": "Options Panel"},
    {"type": "services.complex", "name": "Option Selection Service"},
    {"type": "misc.menu", "name": "Menu entries"}
  ],
  "adjustments": [
    "testing.unit_tests",
    "testing.integration_tests",
    "context.legacy_code"
  ]
}
```

### Output

Formatted Markdown ready to insert into a User Story:

```markdown
#### Estimation

| Profile | Effort | Justification |
|---------|--------|---------------|
| Dev | 13.65h | SaleOrderLineOption, Options Panel, Selection Service |
| QA | 4.25h | Functional tests |
| PM/BA | 2.5h | Specs validation |
| **Total** | **20.4h ≈ 2.5d** | Complexity **L** |

**Calculation detail:**
- SaleOrderLineOption: Dev 4h / QA 1.5h / PM 1h
- Options Panel: Dev 5h / QA 1.5h / PM 1h
- ...
```

## Complexity Levels

| Complexity | Threshold | Action |
|------------|-----------|--------|
| S (Small) | < 4h | OK |
| M (Medium) | 4-8h | OK |
| L (Large) | 8-16h | OK, monitor |
| XL (Extra Large) | > 16h | **SPLIT REQUIRED** |

## Configuration

Estimations are configurable via YAML files:
- `@docs/estimation/components.yaml`: Component catalog
- `@docs/estimation/adjustments.yaml`: Adjustment factors

## Documentation

See the complete methodology in: `@docs/estimation/estimation-methodology.md`

## Related Skills

- [US Dependency Mapper](../us-dependency-mapper/SKILL.md)
- [US Quality Validator](../us-quality-validator/SKILL.md)

---

**Version**: 2.0 (Python script with YAML config)
**Last Updated**: 2025-11-28
