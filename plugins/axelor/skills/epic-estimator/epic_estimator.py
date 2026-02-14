#!/usr/bin/env python3
"""
Epic Estimator - Axelor Project Estimation Tool

Analyzes functional specifications and calculates Dev/QA/PM-BA effort.
Loads catalogs from external YAML files for easy maintenance.

Usage:
  python3 epic_estimator.py --spec path/to/detailed-specifications.md
  python3 epic_estimator.py --components '{"components": [...], "adjustments": [...]}'
  python3 epic_estimator.py --list-components   # List available components
  python3 epic_estimator.py --list-adjustments  # List available adjustments

Output: Formatted Markdown ready to insert into a User Story
"""

import re
import json
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    exit(1)


# =============================================================================
# PATH RESOLUTION
# =============================================================================

def find_plugin_path() -> Path:
    """Find the plugin path robustly."""
    # 1. First try relative to the script
    script_dir = Path(__file__).parent
    plugin_dir = script_dir.parent.parent  # skills/epic-estimator -> plugin root
    docs_dir = plugin_dir / "docs" / "estimation"

    if docs_dir.exists():
        return plugin_dir

    # 2. Otherwise search in /home
    try:
        result = subprocess.run(
            ['find', '/home', '-type', 'd', '-name', 'axelor', '-path', '*/plugins/*'],
            capture_output=True, text=True, timeout=10
        )
        if result.stdout.strip():
            return Path(result.stdout.strip().split('\n')[0])
    except Exception:
        pass

    raise FileNotFoundError("Cannot find axelor plugin")


PLUGIN_PATH = find_plugin_path()
DOCS_DIR = PLUGIN_PATH / "docs" / "estimation"


# =============================================================================
# CONFIGURATION LOADING
# =============================================================================

def load_config() -> Tuple[Dict, Dict, Dict]:
    """Load catalogs from YAML files in docs/estimation/."""
    components_path = DOCS_DIR / "components.yaml"
    adjustments_path = DOCS_DIR / "adjustments.yaml"

    if not components_path.exists():
        raise FileNotFoundError(f"Components config not found: {components_path}")
    if not adjustments_path.exists():
        raise FileNotFoundError(f"Adjustments config not found: {adjustments_path}")

    with open(components_path, 'r', encoding='utf-8') as f:
        components_raw = yaml.safe_load(f)

    with open(adjustments_path, 'r', encoding='utf-8') as f:
        adjustments_raw = yaml.safe_load(f)

    # Flatten structure for easy access: "domains.simple" -> data
    components = {}
    for category, items in components_raw.items():
        if category == 'complexity_thresholds':
            continue  # Handled separately
        if isinstance(items, dict):
            for name, data in items.items():
                if isinstance(data, dict):
                    key = f"{category}.{name}"
                    components[key] = data

    # Flatten adjustments
    adjustments = {}
    for category, items in adjustments_raw.items():
        if isinstance(items, dict):
            for name, data in items.items():
                if isinstance(data, dict):
                    key = f"{category}.{name}"
                    adjustments[key] = data

    thresholds = components_raw.get('complexity_thresholds', {'S': 4, 'M': 8, 'L': 16, 'XL': 999})

    return components, adjustments, thresholds


# Load configuration at startup
try:
    COMPONENTS, ADJUSTMENTS, THRESHOLDS = load_config()
except FileNotFoundError as e:
    print(f"ERROR: {e}")
    COMPONENTS, ADJUSTMENTS, THRESHOLDS = {}, {}, {'S': 4, 'M': 8, 'L': 16, 'XL': 999}


# =============================================================================
# SPECIFICATION PARSING - UTILITY FUNCTIONS
# =============================================================================

def extract_sections(content: str) -> Dict[str, str]:
    """Split document into main numbered sections."""
    sections = {}

    # Pattern for level 2 sections (## X. Title)
    section_pattern = r'^##\s+(\d+)\.\s+([^\n]+)(.*?)(?=^##\s+\d+\.|\Z)'

    for match in re.finditer(section_pattern, content, re.MULTILINE | re.DOTALL):
        section_num = match.group(1)
        section_title = match.group(2).strip()
        section_content = match.group(3)

        # Normalize title for key
        key = section_title.lower().replace(' ', '_')
        sections[key] = {
            'number': section_num,
            'title': section_title,
            'content': section_content
        }

    return sections


def count_fields_in_table(content: str) -> int:
    """Count fields in a markdown table of Fields type."""
    # Look for tables with "Field Name" or "Field" in header
    # Note: header may start with or without |
    table_pattern = r'\|?\s*Field\s*Name[^\n]*\|\n\|[\s\-:|]+\|\n((?:\|[^\n]+\|\n?)+)'

    match = re.search(table_pattern, content, re.IGNORECASE)
    if not match:
        # Try to find a "Fields" section with a table
        fields_section = re.search(r'####[^\n]*Fields[^\n]*\n((?:\|[^\n]+\|\n)+)', content, re.IGNORECASE)
        if not fields_section:
            return 0
        table_content = fields_section.group(1)
    else:
        table_content = match.group(1)

    # Count data rows (exclude separators)
    rows = table_content.strip().split('\n')
    data_rows = [r for r in rows if r.strip() and not re.match(r'^\|[\s\-:]+\|$', r.strip())]

    return len(data_rows)


def determine_view_type(view_title: str, view_content: str) -> str:
    """Determine view type based on its title and content."""
    title_lower = view_title.lower()
    content_lower = view_content.lower()

    # Dashboard
    if 'dashboard' in title_lower:
        dashlets = len(re.findall(r'dashlet', content_lower))
        return "views.dashboard_complex" if dashlets > 3 else "views.dashboard_simple"

    # Grid
    if 'grid' in title_lower:
        # Analyze complexity: advanced filters, conditional styles, etc.
        has_advanced = any(kw in content_lower for kw in ['filter', 'style', 'conditional', 'widget'])
        return "views.grid_complex" if has_advanced else "views.grid_simple"

    # Form (default if contains Panel, Tab, Form)
    if any(kw in title_lower for kw in ['form', 'panel', 'tab']):
        # Count panels/sections
        panels = len(re.findall(r'panel|onglet|tab', content_lower))
        if panels > 3:
            return "views.form_complex"
        elif panels > 1:
            return "views.form_medium"
        return "views.form_simple"

    # Default: simple form
    return "views.form_simple"


def classify_feature(feature_name: str, feature_content: str) -> str:
    """Classify a feature according to its name and content."""
    name_lower = feature_name.lower()
    content_lower = feature_content.lower()

    # Import/Export
    if any(kw in name_lower for kw in ['import', 'export']):
        return "integrations.import_complex" if 'complex' in content_lower else "integrations.import_simple"

    # Configuration/Definition (simple operations)
    if any(kw in name_lower for kw in ['define', 'configure', 'setup']):
        return "services.simple"

    # Copy/Clone operations (complex)
    if any(kw in name_lower for kw in ['copy', 'clone', 'duplicate']):
        return "services.complex"

    # Workflow/State management
    if any(kw in name_lower for kw in ['workflow', 'state']):
        steps = len(re.findall(r'^\d+\.\s+\*\*', feature_content, re.MULTILINE))
        if steps > 8:
            return "workflows.complex"
        elif steps > 4:
            return "workflows.medium"
        return "workflows.simple"

    # Auto/Automatic operations
    if any(kw in name_lower for kw in ['auto', 'automatic', 'recalcul']):
        return "services.medium"

    # Deletion with cascade
    if 'deletion' in name_lower or 'cascade' in content_lower:
        return "services.medium"

    # Select/Deselect operations
    if any(kw in name_lower for kw in ['select', 'deselect']):
        return "services.medium"

    # Display/View/Summary operations
    if any(kw in name_lower for kw in ['display', 'view', 'summary', 'manage']):
        return "services.medium"

    # Populate operations
    if 'populate' in name_lower:
        return "services.medium"

    # Default
    return "services.medium"


def parse_entities(data_model_content: str) -> List[Dict]:
    """Parse the Data Model section to extract entities and extensions."""
    components = []

    # Pattern for Entity and Entity Extension
    # Note: ^### with MULTILINE to avoid matching #### (4 #)
    entity_pattern = r'^###\s+\d+\.\d+\s+(Entity(?:\s+Extension)?)[:\s]+(\w+)(.*?)(?=^###\s+\d+\.\d+|\Z)'

    for match in re.finditer(entity_pattern, data_model_content, re.DOTALL | re.IGNORECASE | re.MULTILINE):
        entity_type = match.group(1).strip()  # "Entity" or "Entity Extension"
        entity_name = match.group(2).strip()
        entity_content = match.group(3)

        # Count fields in "Fields" table
        field_count = count_fields_in_table(entity_content)

        is_extension = "Extension" in entity_type

        # Classify according to type and field count
        if is_extension:
            # Extensions: proportional to added fields
            if field_count == 0:
                continue  # Skip extensions without fields
            comp_type = classify_domain(field_count)
        else:
            comp_type = classify_domain(field_count)

        components.append({
            "type": comp_type,
            "name": f"{entity_name} ({'extension' if is_extension else 'entity'})",
            "fields": field_count,
            "is_extension": is_extension
        })

    return components


def parse_views(views_content: str) -> List[Dict]:
    """Parse the Views section to extract distinct views (1 per section)."""
    components = []

    # Pattern for view subsections (### 3.X Title)
    # Note: ^### with MULTILINE to avoid matching #### (4 #)
    view_pattern = r'^###\s+(\d+\.\d+)\s+([^\n]+)(.*?)(?=^###\s+\d+\.\d+|\Z)'

    for match in re.finditer(view_pattern, views_content, re.DOTALL | re.MULTILINE):
        section_num = match.group(1)
        view_title = match.group(2).strip()
        view_content = match.group(3)

        # Determine view type
        view_type = determine_view_type(view_title, view_content)

        components.append({
            "type": view_type,
            "name": f"{view_title} ({section_num})",
            "section": section_num
        })

    return components


def parse_features(features_content: str) -> List[Dict]:
    """Parse the Features section to extract features."""
    components = []

    # Pattern for features (### X.X Feature: Title)
    # Note: ^### with MULTILINE to avoid matching #### (4 #)
    feature_pattern = r'^###\s+(\d+\.\d+)\s+Feature[:\s]+([^\n]+)(.*?)(?=^###\s+\d+\.\d+|\Z)'

    for match in re.finditer(feature_pattern, features_content, re.DOTALL | re.IGNORECASE | re.MULTILINE):
        section_num = match.group(1)
        feature_name = match.group(2).strip()
        feature_content = match.group(3)

        # Classify the feature
        comp_type = classify_feature(feature_name, feature_content)

        components.append({
            "type": comp_type,
            "name": f"{feature_name} ({section_num})"
        })

    return components


def parse_security(security_content: str) -> List[Dict]:
    """Parse the Security section to extract permissions."""
    components = []

    # Look for number of roles
    roles_pattern = r'\*\*([^*]+)\*\*:\s*(?:Configure|Create|View|Edit|Delete|Full|Read|None)'
    roles = set(re.findall(roles_pattern, security_content))
    role_count = len(roles)

    if role_count > 0:
        if role_count >= 4:
            perm_type = "security.permissions_complex"
        elif role_count >= 2:
            perm_type = "security.permissions_medium"
        else:
            perm_type = "security.permissions_simple"

        components.append({
            "type": perm_type,
            "name": f"Permissions ({role_count} roles)"
        })

    return components


def parse_crosscutting(crosscutting_content: str) -> List[Dict]:
    """Parse the Cross-cutting section to extract additional components."""
    components = []

    # BIRT Reports
    if re.search(r'(?:Reporting|BIRT)', crosscutting_content, re.IGNORECASE):
        # Determine report complexity
        is_complex = any(kw in crosscutting_content.lower() for kw in [
            'complex', 'graphique', 'chart', 'sub-report', 'sous-rapport'
        ])
        components.append({
            "type": "reports.birt_complex" if is_complex else "reports.birt_simple",
            "name": "BIRT Report"
        })

    # Import
    if re.search(r'####[^\n]*Import', crosscutting_content, re.IGNORECASE):
        components.append({
            "type": "integrations.import_simple",
            "name": "Data Import"
        })

    # Export
    if re.search(r'####[^\n]*Export', crosscutting_content, re.IGNORECASE):
        components.append({
            "type": "integrations.import_simple",
            "name": "Data Export"
        })

    # Stock Integration
    if re.search(r'###[^\n]*Stock', crosscutting_content, re.IGNORECASE):
        components.append({
            "type": "services.medium",
            "name": "Stock Integration"
        })

    return components


# =============================================================================
# SPECIFICATION PARSING - MAIN FUNCTION
# =============================================================================

def parse_specification(spec_path: str) -> Dict:
    """Parse a functional specification and extract components.

    Uses structured parsing by sections to precisely extract:
    - Section 2: Data Model (entities and extensions)
    - Section 3: Views (1 view per section)
    - Section 4: Features (classified services)
    - Section 5: Security (permissions)
    - Section 6: Cross-cutting (reports, imports, exports)
    """
    content = Path(spec_path).read_text(encoding='utf-8')
    components = []

    # Extract main sections
    sections = extract_sections(content)

    # Parse Section 2: Data Model (entities and extensions)
    data_model = sections.get('data_model', {})
    if data_model:
        entities = parse_entities(data_model.get('content', ''))
        components.extend(entities)

    # Parse Section 3: Views and User Interface
    # Note: "views" plural to avoid matching "overview"
    views_section = None
    for key in sections:
        if key.startswith('views') or 'user_interface' in key:
            views_section = sections[key]
            break

    if views_section:
        views = parse_views(views_section.get('content', ''))
        components.extend(views)

    # Parse Section 4: Features and Workflows
    features_section = None
    for key in sections:
        if key.startswith('features') or key.startswith('workflows'):
            features_section = sections[key]
            break

    if features_section:
        features = parse_features(features_section.get('content', ''))
        components.extend(features)

    # Parse Section 5: Security and Permissions
    security_section = None
    for key in sections:
        if 'security' in key or 'permission' in key:
            security_section = sections[key]
            break

    if security_section:
        security = parse_security(security_section.get('content', ''))
        components.extend(security)

    # Parse Section 6: Cross-cutting Aspects
    crosscutting_section = None
    for key in sections:
        if 'cross' in key:
            crosscutting_section = sections[key]
            break

    if crosscutting_section:
        crosscutting = parse_crosscutting(crosscutting_section.get('content', ''))
        components.extend(crosscutting)

    # Menu (search in entire document)
    if re.search(r'Menu|menu entry', content, re.IGNORECASE):
        components.append({
            "type": "misc.menu",
            "name": "Menu entries"
        })

    return {"components": components, "adjustments": []}


def classify_domain(field_count: int) -> str:
    """Classify a domain according to its field count."""
    if field_count <= 10:
        return "domains.simple"
    if field_count <= 15:
        return "domains.medium"
    return "domains.complex"


# =============================================================================
# ESTIMATION CALCULATION
# =============================================================================

def calculate_estimation(components: List[Dict], adjustments: List[str]) -> Dict:
    """Calculate total estimation."""
    totals = {"dev": 0.0, "qa": 0.0, "pm": 0.0}
    details = []

    for comp in components:
        comp_type = comp.get("type", "services.simple")
        comp_data = COMPONENTS.get(comp_type, {"dev": 2, "qa": 1, "pm": 0.25})

        # Multiply by count if specified
        count = comp.get("count", 1)

        dev = comp_data.get("dev", 0) * count
        qa = comp_data.get("qa", 0) * count
        pm = comp_data.get("pm", 0) * count

        totals["dev"] += dev
        totals["qa"] += qa
        totals["pm"] += pm

        details.append({
            "name": comp.get("name", comp_type),
            "type": comp_type,
            "dev": dev,
            "qa": qa,
            "pm": pm,
            "total": dev + qa + pm
        })

    # Save totals before adjustments
    base_totals = totals.copy()

    # Apply adjustments
    applied_adjustments = []
    for adj in adjustments:
        adj_data = ADJUSTMENTS.get(adj)
        if adj_data:
            dev_mult = adj_data.get("dev", 0)
            qa_mult = adj_data.get("qa", 0)
            pm_mult = adj_data.get("pm", 0)

            totals["dev"] *= (1 + dev_mult)
            totals["qa"] *= (1 + qa_mult)
            totals["pm"] *= (1 + pm_mult)

            applied_adjustments.append({
                "name": adj,
                "description": adj_data.get("description", ""),
                "dev": f"+{int(dev_mult * 100)}%",
                "qa": f"+{int(qa_mult * 100)}%",
                "pm": f"+{int(pm_mult * 100)}%"
            })

    total = totals["dev"] + totals["qa"] + totals["pm"]
    complexity = classify_complexity(total)

    result = {
        "totals": totals,
        "base_totals": base_totals,
        "details": details,
        "adjustments_applied": applied_adjustments,
        "total_hours": total,
        "total_days": total / 8,
        "complexity": complexity
    }

    # Generate split recommendation if XL
    if complexity == "XL":
        result["split_recommendation"] = generate_split_recommendation(details, total)

    return result


def classify_complexity(total_hours: float) -> str:
    """Classify complexity according to thresholds."""
    if total_hours < THRESHOLDS.get('S', 4):
        return "S"
    if total_hours < THRESHOLDS.get('M', 8):
        return "M"
    if total_hours < THRESHOLDS.get('L', 16):
        return "L"
    return "XL"


def generate_split_recommendation(details: List[Dict], total: float) -> List[Dict]:
    """Generate split recommendation for XL US."""
    recommendations = []

    # Sort by total descending
    sorted_details = sorted(details, key=lambda x: x.get('total', 0), reverse=True)

    # Group intelligently
    current_group = {"items": [], "total": 0, "dev": 0, "qa": 0, "pm": 0}
    us_number = 1
    max_per_us = 14  # Leave margin under 16h

    for item in sorted_details:
        item_total = item.get('total', 0)

        # If item alone exceeds threshold, it forms its own US
        if item_total > max_per_us:
            if current_group["items"]:
                recommendations.append(create_us_recommendation(us_number, current_group))
                us_number += 1
                current_group = {"items": [], "total": 0, "dev": 0, "qa": 0, "pm": 0}

            recommendations.append({
                "us_id": f"US-{us_number:03d}",
                "title": item["name"],
                "dev": round(item["dev"], 1),
                "qa": round(item["qa"], 1),
                "pm": round(item["pm"], 1),
                "total": round(item_total, 1),
                "components": [item["name"]],
                "note": "Large component - consider further splitting if possible"
            })
            us_number += 1
            continue

        # Otherwise, try to group
        if current_group["total"] + item_total <= max_per_us:
            current_group["items"].append(item)
            current_group["total"] += item_total
            current_group["dev"] += item.get("dev", 0)
            current_group["qa"] += item.get("qa", 0)
            current_group["pm"] += item.get("pm", 0)
        else:
            # Finalize current group and start a new one
            if current_group["items"]:
                recommendations.append(create_us_recommendation(us_number, current_group))
                us_number += 1

            current_group = {
                "items": [item],
                "total": item_total,
                "dev": item.get("dev", 0),
                "qa": item.get("qa", 0),
                "pm": item.get("pm", 0)
            }

    # Don't forget the last group
    if current_group["items"]:
        recommendations.append(create_us_recommendation(us_number, current_group))

    return recommendations


def create_us_recommendation(us_number: int, group: Dict) -> Dict:
    """Create a US recommendation from a group."""
    # Generate title based on components
    if len(group["items"]) == 1:
        title = group["items"][0]["name"]
    else:
        # Try to find a common theme
        types = [item.get("type", "").split(".")[0] for item in group["items"]]
        if len(set(types)) == 1:
            title = f"{types[0].capitalize()} Implementation"
        else:
            title = f"Implementation ({len(group['items'])} components)"

    return {
        "us_id": f"US-{us_number:03d}",
        "title": title,
        "dev": round(group["dev"], 1),
        "qa": round(group["qa"], 1),
        "pm": round(group["pm"], 1),
        "total": round(group["total"], 1),
        "components": [item["name"] for item in group["items"]]
    }


# =============================================================================
# OUTPUT FORMATTING
# =============================================================================

def format_markdown(result: Dict) -> str:
    """Format result as Markdown."""
    output = []

    # Header
    output.append("#### Estimation\n")

    # Main table
    output.append("| Profile | Effort | Justification |")
    output.append("|---------|--------|---------------|")

    # Details by profile
    dev_components = [d['name'] for d in result['details'][:3]]
    dev_justif = ", ".join(dev_components)
    if len(result['details']) > 3:
        dev_justif += f" (+{len(result['details']) - 3} others)"

    output.append(f"| Dev | {result['totals']['dev']:.1f}h | {dev_justif} |")
    output.append(f"| QA | {result['totals']['qa']:.1f}h | Functional tests |")
    output.append(f"| PM/BA | {result['totals']['pm']:.1f}h | Specs validation |")

    days = result['total_days']
    output.append(f"| **Total** | **{result['total_hours']:.1f}h ≈ {days:.1f}d** | Complexity **{result['complexity']}** |")

    # Calculation detail
    output.append("\n**Calculation detail:**")
    for detail in result['details']:
        output.append(f"- {detail['name']}: Dev {detail['dev']:.1f}h / QA {detail['qa']:.1f}h / PM {detail['pm']:.1f}h")

    # Applied adjustments
    if result.get('adjustments_applied'):
        output.append("\n**Applied adjustments:**")
        for adj in result['adjustments_applied']:
            output.append(f"- {adj['description']}: Dev {adj['dev']} / QA {adj['qa']} / PM {adj['pm']}")

    # Split recommendation if XL
    if result.get('split_recommendation'):
        output.append("\n---")
        output.append("\n### ⚠️ RECOMMENDATION: Split required (>16h)\n")
        output.append("| US | Title | Dev | QA | PM | Total |")
        output.append("|----|-------|-----|----|----|-------|")

        for rec in result['split_recommendation']:
            components = ", ".join(rec['components'][:2])
            if len(rec['components']) > 2:
                components += f" (+{len(rec['components']) - 2})"

            output.append(f"| {rec['us_id']} | {rec['title']} | {rec['dev']}h | {rec['qa']}h | {rec['pm']}h | **{rec['total']}h** |")

        output.append("\n**Components per US:**")
        for rec in result['split_recommendation']:
            output.append(f"- **{rec['us_id']}**: {', '.join(rec['components'])}")

    return "\n".join(output)


def format_json(result: Dict) -> str:
    """Format result as JSON."""
    return json.dumps(result, indent=2, ensure_ascii=False)


# =============================================================================
# UTILITIES
# =============================================================================

def list_components() -> str:
    """List all available components."""
    output = ["# Available Components\n"]

    current_category = None
    for key, data in sorted(COMPONENTS.items()):
        category = key.split('.')[0]
        if category != current_category:
            output.append(f"\n## {category.upper()}\n")
            current_category = category

        desc = data.get('description', '')
        dev = data.get('dev', 0)
        qa = data.get('qa', 0)
        pm = data.get('pm', 0)
        output.append(f"- **{key}**: Dev {dev}h / QA {qa}h / PM {pm}h")
        if desc:
            output.append(f"  - {desc}")

    return "\n".join(output)


def list_adjustments() -> str:
    """List all available adjustments."""
    output = ["# Available Adjustments\n"]

    current_category = None
    for key, data in sorted(ADJUSTMENTS.items()):
        category = key.split('.')[0]
        if category != current_category:
            output.append(f"\n## {category.upper()}\n")
            current_category = category

        desc = data.get('description', '')
        when = data.get('when', '')
        dev = data.get('dev', 0)
        qa = data.get('qa', 0)
        pm = data.get('pm', 0)

        output.append(f"- **{key}**: Dev +{int(dev*100)}% / QA +{int(qa*100)}% / PM +{int(pm*100)}%")
        if desc:
            output.append(f"  - {desc}")
        if when:
            output.append(f"  - *When*: {when}")

    return "\n".join(output)


def group_by_epic(details: List[Dict], sections: Dict[str, Dict]) -> Dict[str, Dict]:
    """Group components by section/EPIC.

    Mapping sections → EPICs:
    - Section 2 (Data Model) → EPIC-001 Configuration
    - Section 3 (Views) → EPIC-002 Interface
    - Section 4 (Features) → Business EPICs (distributed)
    - Section 5 (Security) → EPIC-001 (included in config)
    - Section 6 (Cross-cutting) → EPIC-003 Integrations
    """
    epics = {
        'EPIC-001-configuration': {'name': 'Configuration & Data Model', 'dev': 0, 'qa': 0, 'pm': 0, 'components': []},
        'EPIC-002-interface': {'name': 'Views & Interface', 'dev': 0, 'qa': 0, 'pm': 0, 'components': []},
        'EPIC-003-features': {'name': 'Business Features', 'dev': 0, 'qa': 0, 'pm': 0, 'components': []},
        'EPIC-004-integrations': {'name': 'Integrations & Reporting', 'dev': 0, 'qa': 0, 'pm': 0, 'components': []},
    }

    for detail in details:
        comp_type = detail.get('type', '')
        name = detail.get('name', '')

        # Classify by component type
        if comp_type.startswith('domains.'):
            epic_key = 'EPIC-001-configuration'
        elif comp_type.startswith('views.'):
            epic_key = 'EPIC-002-interface'
        elif comp_type.startswith('services.') or comp_type.startswith('workflows.'):
            epic_key = 'EPIC-003-features'
        elif comp_type.startswith('reports.') or comp_type.startswith('integrations.'):
            epic_key = 'EPIC-004-integrations'
        elif comp_type.startswith('security.'):
            epic_key = 'EPIC-001-configuration'
        else:
            epic_key = 'EPIC-003-features'  # Default

        epics[epic_key]['dev'] += detail.get('dev', 0)
        epics[epic_key]['qa'] += detail.get('qa', 0)
        epics[epic_key]['pm'] += detail.get('pm', 0)
        epics[epic_key]['components'].append(name)

    # Remove empty EPICs
    return {k: v for k, v in epics.items() if v['components']}


def format_per_epic(result: Dict, sections: Dict[str, Dict]) -> str:
    """Format results broken down by EPIC."""
    output = []

    # Group by EPIC
    epics = group_by_epic(result['details'], sections)

    output.append("# Estimation by EPIC\n")
    output.append("## Calibrated Total Budget\n")
    output.append(f"- **Dev**: {result['totals']['dev']:.1f}h")
    output.append(f"- **QA**: {result['totals']['qa']:.1f}h")
    output.append(f"- **PM/BA**: {result['totals']['pm']:.1f}h")
    output.append(f"- **Total**: {result['total_hours']:.1f}h ({result['total_days']:.1f}d)\n")

    output.append("## Breakdown by EPIC\n")
    output.append("| EPIC | Name | Dev | QA | PM | Total | % |")
    output.append("|------|------|-----|----|----|-------|---|")

    total = result['total_hours']
    for epic_id, epic_data in sorted(epics.items()):
        epic_total = epic_data['dev'] + epic_data['qa'] + epic_data['pm']
        pct = (epic_total / total * 100) if total > 0 else 0
        output.append(f"| {epic_id} | {epic_data['name']} | {epic_data['dev']:.1f}h | {epic_data['qa']:.1f}h | {epic_data['pm']:.1f}h | {epic_total:.1f}h | {pct:.0f}% |")

    output.append(f"| **TOTAL** | | **{result['totals']['dev']:.1f}h** | **{result['totals']['qa']:.1f}h** | **{result['totals']['pm']:.1f}h** | **{result['total_hours']:.1f}h** | **100%** |")

    output.append("\n## Components by EPIC\n")
    for epic_id, epic_data in sorted(epics.items()):
        output.append(f"### {epic_id}: {epic_data['name']}\n")
        for comp in epic_data['components']:
            output.append(f"- {comp}")
        output.append("")

    return "\n".join(output)


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Epic Estimator - Estimation calculation for Axelor projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a specification
  python3 epic_estimator.py --spec path/to/specification.md

  # Analyze with EPIC breakdown
  python3 epic_estimator.py --spec path/to/specification.md --per-epic

  # Explicit components with adjustments
  python3 epic_estimator.py --components '{"components": [
    {"type": "domains.complex", "name": "SaleOrderLineOption"},
    {"type": "views.form_complex", "name": "Options Panel"}
  ], "adjustments": ["testing.unit_tests", "context.legacy_code"]}'

  # List available components/adjustments
  python3 epic_estimator.py --list-components
  python3 epic_estimator.py --list-adjustments
        """
    )

    parser.add_argument('--spec', type=str, help='Path to the Markdown specification file')
    parser.add_argument('--components', type=str, help='JSON with components and adjustments')
    parser.add_argument('--list-components', action='store_true', help='List available components')
    parser.add_argument('--list-adjustments', action='store_true', help='List available adjustments')
    parser.add_argument('--per-epic', action='store_true', help='Break down estimates by EPIC')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Output format (default: markdown)')

    args = parser.parse_args()

    # List components
    if args.list_components:
        print(list_components())
        return

    # List adjustments
    if args.list_adjustments:
        print(list_adjustments())
        return

    # Specification mode
    sections = {}
    if args.spec:
        spec_path = Path(args.spec)
        if not spec_path.exists():
            print(f"ERROR: Specification file not found: {spec_path}")
            exit(1)

        # Parse the specification
        content = spec_path.read_text(encoding='utf-8')
        sections = extract_sections(content)

        parsed = parse_specification(str(spec_path))
        components = parsed.get('components', [])
        adjustments = parsed.get('adjustments', [])

        print(f"# Parsing: {spec_path.name}")
        print(f"# Found {len(components)} components\n")

    # Explicit components mode
    elif args.components:
        try:
            data = json.loads(args.components)
            components = data.get('components', [])
            adjustments = data.get('adjustments', [])
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON: {e}")
            exit(1)

    else:
        parser.print_help()
        return

    # Calculate estimation
    result = calculate_estimation(components, adjustments)

    # Display result
    if args.format == 'json':
        print(format_json(result))
    elif args.per_epic and sections:
        print(format_per_epic(result, sections))
    else:
        print(format_markdown(result))


if __name__ == "__main__":
    main()
