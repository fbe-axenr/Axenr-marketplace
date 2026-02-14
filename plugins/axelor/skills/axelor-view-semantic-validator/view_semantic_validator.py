#!/usr/bin/env python3
"""
Axelor View Semantic Validator
Validates view semantic coherence and cross-file integrity
"""

import sys
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Dict, List, Tuple
from collections import defaultdict


def remove_namespace(tag: str) -> str:
    """Remove XML namespace from tag"""
    return tag.split('}')[-1] if '}' in tag else tag


def scan_domains(domains_dir: Path) -> Dict[str, Dict]:
    """
    Scan domain XMLs to build entity index
    Returns: {entity_name: {package: str, fields: {field_name: field_type}}}
    """
    entities = {}

    if not domains_dir.exists():
        return entities

    for xml_file in domains_dir.glob('*.xml'):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for entity_elem in root.iter():
                tag = remove_namespace(entity_elem.tag)
                if tag == 'entity':
                    entity_name = entity_elem.get('name')
                    package = entity_elem.get('package', '')

                    if entity_name:
                        full_name = f"{package}.{entity_name}" if package else entity_name
                        entities[full_name] = {
                            'package': package,
                            'name': entity_name,
                            'fields': {}
                        }

                        for field_elem in entity_elem:
                            field_tag = remove_namespace(field_elem.tag)
                            field_name = field_elem.get('name')
                            if field_name and field_tag != 'entity':
                                entities[full_name]['fields'][field_name] = field_tag
        except Exception as e:
            print(f"Warning: Could not parse {xml_file}: {e}", file=sys.stderr)

    return entities


def scan_actions(views_dir: Path) -> Dict[str, str]:
    """
    Scan view XMLs to build action index
    Returns: {action_name: file_path}
    """
    actions = {}

    if not views_dir.exists():
        return actions

    for xml_file in views_dir.glob('*.xml'):
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            for elem in root.iter():
                tag = remove_namespace(elem.tag)
                if tag.startswith('action-'):
                    action_name = elem.get('name')
                    if action_name:
                        actions[action_name] = str(xml_file)
        except Exception as e:
            print(f"Warning: Could not parse {xml_file}: {e}", file=sys.stderr)

    return actions


# Widget compatibility mapping
WIDGET_COMPATIBILITY = {
    'progress': ['decimal', 'integer'],
    'slider': ['decimal', 'integer'],
    'html': ['string'],
    'binary-link': ['binary'],
    'image': ['binary'],
    'nav-select': ['integer', 'string'],
    'tag-select': ['many-to-many', 'one-to-many'],
    'toggle': ['boolean'],
    'boolean-switch': ['boolean'],
    'inline-checkbox': ['boolean'],
}


def validate_view_semantic(xml_path: Path, entities: Dict, actions: Dict) -> Tuple[List, List, int, int]:
    """
    Validate view semantics
    Returns: (errors, warnings, fields_checked, actions_checked)
    """
    errors = []
    warnings = []

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        errors.append((0, 'XML', f"XML parsing error: {e}"))
        return errors, warnings, 0, 0

    # Find model for this view
    view_model = None
    for elem in root.iter():
        tag = remove_namespace(elem.tag)
        if tag in ['form', 'grid', 'dashboard', 'calendar', 'gantt', 'cards', 'kanban']:
            view_model = elem.get('model')
            break

    entity_fields = {}
    if view_model and view_model in entities:
        entity_fields = entities[view_model]['fields']

    line = 0
    fields_checked = 0
    actions_checked = 0

    for elem in root.iter():
        line += 1
        tag = remove_namespace(elem.tag)

        # Validate field elements
        if tag == 'field':
            fields_checked += 1
            field_name = elem.get('name')
            widget = elem.get('widget')

            if field_name and not field_name.startswith('$'):
                if view_model and entity_fields:
                    if field_name not in entity_fields:
                        available = ', '.join(sorted(list(entity_fields.keys())[:10]))
                        errors.append((
                            line, tag,
                            f"Field '{field_name}' does not exist in model {view_model}\n"
                            f"  Available fields: {available}, ..."
                        ))
                    else:
                        field_type = entity_fields[field_name]
                        if widget and widget in WIDGET_COMPATIBILITY:
                            compatible_types = WIDGET_COMPATIBILITY[widget]
                            if field_type not in compatible_types:
                                suggested = [w for w, types in WIDGET_COMPATIBILITY.items() if field_type in types]
                                warnings.append((
                                    line, tag,
                                    f"Widget '{widget}' may be incompatible with field type {field_type}\n"
                                    f"  Suggested: {', '.join(suggested[:5]) if suggested else 'none'}"
                                ))

        # Validate button onClick actions
        if tag == 'button':
            on_click = elem.get('onClick')
            if on_click:
                actions_checked += 1
                action_names = [a.strip() for a in on_click.split(',')]
                for action_name in action_names:
                    if action_name.startswith('action-') and action_name not in actions and action_name != 'save':
                        errors.append((
                            line, tag,
                            f"Action not found: {action_name}"
                        ))

        # Validate grid orderBy
        if tag == 'grid' and 'orderBy' not in elem.attrib:
            warnings.append((
                line, tag,
                "Consider adding orderBy for consistent sorting"
            ))

    return errors, warnings, fields_checked, actions_checked


def print_report(xml_path: Path, errors: List, warnings: List, fields_checked: int, actions_checked: int):
    """Print semantic validation report"""
    print(f"SEMANTIC VALIDATION: {xml_path.name}\n")

    if errors:
        print(f"ERRORS: {len(errors)}\n")
        for line, tag, message in errors:
            print(f"Line {line}, <{tag}>")
            print(f"  {message}\n")

    if warnings:
        print(f"WARNINGS: {len(warnings)}\n")
        for line, tag, message in warnings:
            print(f"Line {line}, <{tag}>")
            print(f"  {message}\n")

    if not errors and not warnings:
        print("No errors or warnings found.\n")

    print("SUMMARY:")
    print(f"- Fields checked: {fields_checked}")
    print(f"- Actions checked: {actions_checked}")
    print(f"- Errors: {len(errors)}")
    print(f"- Warnings: {len(warnings)}")
    print(f"- Status: {'FAILED' if errors else 'PASSED'}")


def main():
    parser = argparse.ArgumentParser(description='Validate Axelor view XML semantics')
    parser.add_argument('target', type=Path, help='View XML file or directory')
    parser.add_argument('--domains', type=Path, default=Path('src/main/resources/domains'),
                        help='Path to domains directory')

    args = parser.parse_args()

    print(f"Scanning domains from: {args.domains}")
    entities = scan_domains(args.domains)
    print(f"Found {len(entities)} entities\n")

    views_dir = args.target if args.target.is_dir() else args.target.parent
    print(f"Scanning actions from: {views_dir}")
    actions = scan_actions(views_dir)
    print(f"Found {len(actions)} actions\n")

    has_errors = False

    if args.target.is_file():
        errors, warnings, fields_checked, actions_checked = validate_view_semantic(args.target, entities, actions)
        print_report(args.target, errors, warnings, fields_checked, actions_checked)
        has_errors = len(errors) > 0
    elif args.target.is_dir():
        for xml_file in sorted(args.target.glob('*.xml')):
            errors, warnings, fields_checked, actions_checked = validate_view_semantic(xml_file, entities, actions)
            print_report(xml_file, errors, warnings, fields_checked, actions_checked)
            if errors:
                has_errors = True
            print("\n" + "="*60 + "\n")
    else:
        print(f"ERROR: Path not found: {args.target}")
        sys.exit(1)

    sys.exit(1 if has_errors else 0)


if __name__ == '__main__':
    main()
