# Axelor Estimation Methodology

This document describes the User Story estimation process for Axelor projects.

## Overview

Estimation is broken down by profile:
- **Dev**: Development, unit tests, technical documentation
- **QA**: Functional tests, integration tests, validation
- **PM/BA**: Specs validation, coordination, functional documentation

## 4-Step Process

### Step 1: Identify Components

From the functional specification, identify all Axelor components involved.

**Sources in the specification:**
- Section 2 (Data Model) → Entities/Domains
- Section 3 (Views) → Grids, Forms, Dashboards
- Section 4 (Features) → Services, Workflows
- Section 6 (Cross-cutting) → Integrations, Reports, Security

**Example:**
```
Specification: "Product options management on quotes"

Identified components:
- ProductOption (medium domain, 5 fields)
- SaleOrderLineOption (complex domain, 9 fields)
- Product Options Grid (simple grid)
- Sale Order Line Options Panel (complex form)
- Option Selection Service (complex service)
- Menu (misc)
```

### Step 2: Evaluate Each Component

Use the `components.yaml` catalog to get estimates by profile.

| Component | Type | Dev | QA | PM |
|-----------|------|-----|----|----|
| ProductOption | domains.medium | 2.5h | 1h | 0.5h |
| SaleOrderLineOption | domains.complex | 4h | 1.5h | 1h |
| Product Options Grid | views.grid_simple | 1h | 0.75h | 0.5h |
| Options Panel | views.form_complex | 5h | 1.5h | 1h |
| Selection Service | services.complex | 8h | 2.5h | 1h |
| Menu | misc.menu | 0.5h | 0.5h | 0h |
| **Subtotal** | | **21h** | **7.75h** | **4h** |

### Step 3: Apply Adjustment Factors

Identify applicable context factors from `adjustments.yaml`.

**Common factors:**
- Thorough unit tests (+30% Dev)
- Integration tests (+50% QA)
- Legacy code (+25% Dev)
- Specs uncertainty (+10-20% all)

**Example with adjustments:**

| Factor | Dev | QA | PM |
|--------|-----|----|----|
| Subtotal | 21h | 7.75h | 4h |
| Unit tests (+30% Dev) | +6.3h | - | - |
| Integration tests (+50% QA) | - | +3.9h | - |
| **Adjusted total** | **27.3h** | **11.65h** | **4h** |

### Step 4: Classify and Recommend

**Total**: 27.3 + 11.65 + 4 = **43h ≈ 5.4 days**

**Classification**:
| Complexity | Threshold |
|------------|-----------|
| S (Small) | < 4h |
| M (Medium) | 4-8h |
| L (Large) | 8-16h |
| **XL (Extra Large)** | **> 16h** |

→ This US is **XL** and must be split.

**Split recommendation:**

| US | Title | Dev | QA | PM | Total |
|----|-------|-----|----|----|-------|
| US-001 | ProductOption & SaleOrderLineOption entities | 8.5h | 3.25h | 2h | 13.75h |
| US-002 | Grid & Form views | 7.8h | 2.9h | 2h | 12.7h |
| US-003 | Selection service | 10.4h | 5.15h | 0h | 15.55h |
| | **Split total** | 26.7h | 11.3h | 4h | **42h** |

## Important Rules

1. **Always detail the calculation**: The client must understand where the estimate comes from
2. **Be conservative**: Better to slightly overestimate than underestimate
3. **Include tests**: Tests represent 25-40% of total effort
4. **Never accept XL**: Always split into smaller stories (< 16h)
5. **Adjust for context**: Legacy code, uncertainty, new technologies

## Script Usage

The `epic_estimator.py` script automates this process:

```bash
# Plugin path resolution
PLUGIN_PATH=$(find /home -type d -name "axelor" -path "*/plugins/*" 2>/dev/null | head -1)

# Mode 1: Analyze a specification
python3 ${PLUGIN_PATH}/skills/epic-estimator/epic_estimator.py \
  --spec path/to/detailed-specifications.md

# Mode 2: Explicit components
python3 ${PLUGIN_PATH}/skills/epic-estimator/epic_estimator.py \
  --components '{"components": [...], "adjustments": [...]}'
```

## Reference Files

- `components.yaml`: Component catalog with estimates
- `adjustments.yaml`: Adjustment factors by context

These YAML files are editable to adjust estimates based on team experience.

---

**Version**: 2.0
**Last Updated**: 2025-11-28
