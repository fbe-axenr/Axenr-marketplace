#!/usr/bin/env python3
"""
Axelor Domain Semantic Validator
Validates inter-attribute logic, cross-entity references, and best practices
"""

import sys
import re
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import Dict, List, Tuple, Set


class EntityIndex:
    """Index of all entities and their fields"""
    def __init__(self):
        self.entities = {}  # {entity_name: {package, fields: {field_name: type}}}

    def add_entity(self, name: str, package: str, fields: Dict[str, str]):
        """Add entity to index"""
        self.entities[name] = {'package': package, 'fields': fields}

    def get_entity(self, name: str) -> Dict:
        """Get entity by name"""
        return self.entities.get(name)

    def entity_exists(self, ref: str) -> bool:
        """Check if entity exists by fully qualified name or simple name"""
        # Try simple name first
        simple_name = ref.split('.')[-1]
        if simple_name in self.entities:
            return True
        # Try full package match
        for entity_name, entity_data in self.entities.items():
            full_name = f"{entity_data['package']}.{entity_name}"
            if full_name == ref:
                return True
        return False

    def get_field_type(self, entity_name: str, field_name: str) -> str:
        """Get field type from entity"""
        entity = self.get_entity(entity_name)
        if not entity:
            return None
        return entity['fields'].get(field_name)


def build_entity_index(domains_dir: Path) -> EntityIndex:
    """Build index of all entities from domain XML files"""
    index = EntityIndex()

    xml_files = list(domains_dir.glob('*.xml')) if domains_dir.is_dir() else [domains_dir]

    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Remove namespace
            for elem in root.iter():
                if '}' in elem.tag:
                    elem.tag = elem.tag.split('}')[-1]

            # Get module package
            module_elem = root.find('.//module')
            package = module_elem.get('package', '') if module_elem is not None else ''

            # Index each entity
            for entity in root.findall('.//entity'):
                entity_name = entity.get('name')
                if not entity_name:
                    continue

                fields = {}
                # Index all fields with their types
                for child in entity:
                    field_name = child.get('name')
                    if field_name:
                        fields[field_name] = child.tag

                index.add_entity(entity_name, package, fields)

        except ET.ParseError:
            continue

    return index


def validate_inter_attribute(elem, line: int) -> Tuple[List, List]:
    """Validate inter-attribute logic"""
    errors = []
    warnings = []
    tag = elem.tag
    name = elem.get('name', 'unknown')

    # Rule 1: scale ≤ precision
    if tag == 'decimal':
        precision = elem.get('precision')
        scale = elem.get('scale')
        if precision and scale:
            try:
                if int(scale) > int(precision):
                    errors.append((
                        line, tag, name,
                        f"scale ({scale}) > precision ({precision})"
                    ))
            except ValueError:
                pass

    # Rule 2: required + default conflict
    required = elem.get('required')
    default = elem.get('default')
    if required == 'true' and default:
        errors.append((
            line, tag, name,
            f'cannot have both required="true" and default="{default}"'
        ))

    # Best practice: email without unique
    if tag == 'string' and 'email' in name.lower():
        if elem.get('unique') != 'true':
            warnings.append((
                line, tag, name,
                'Consider unique="true" for email fields'
            ))

    return errors, warnings


def validate_cross_entity(elem, line: int, entity_index: EntityIndex, current_entity: str) -> Tuple[List, List]:
    """Validate cross-entity references"""
    errors = []
    warnings = []
    tag = elem.tag
    name = elem.get('name', 'unknown')

    # Relationship fields
    relationship_types = ['many-to-one', 'one-to-many', 'many-to-many', 'one-to-one']

    if tag not in relationship_types:
        return errors, warnings

    # Check ref target exists
    ref = elem.get('ref')
    if ref and not entity_index.entity_exists(ref):
        errors.append((
            line, tag, name,
            f'ref="{ref}" - Entity not found'
        ))

    # Check mappedBy field exists and is correct type
    if tag == 'one-to-many':
        mapped_by = elem.get('mappedBy')
        if ref and mapped_by:
            target_entity = ref.split('.')[-1]
            field_type = entity_index.get_field_type(target_entity, mapped_by)

            if field_type is None:
                errors.append((
                    line, tag, name,
                    f'mappedBy="{mapped_by}" but {target_entity} has no field "{mapped_by}"'
                ))
            elif field_type != 'many-to-one':
                errors.append((
                    line, tag, name,
                    f'mappedBy="{mapped_by}" field is {field_type}, should be many-to-one'
                ))

        # Best practice: lines without orderBy
        if 'line' in name.lower() and not elem.get('orderBy'):
            warnings.append((
                line, tag, name,
                'Consider orderBy="sequence" for line fields'
            ))

    # Best practice: many-to-one without title
    if tag == 'many-to-one' and not elem.get('title'):
        warnings.append((
            line, tag, name,
            'Consider adding title attribute for better UX'
        ))

    return errors, warnings


def validate_domain(xml_path: Path, entity_index: EntityIndex) -> Tuple[List, List]:
    """
    Validate domain XML semantics
    Returns: (errors, warnings)
    """
    errors = []
    warnings = []

    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError as e:
        errors.append((0, 'XML', 'parse_error', f"XML parsing error: {e}"))
        return errors, warnings

    # Remove namespace
    for elem in root.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}')[-1]

    # Get current entity name
    entity_elem = root.find('.//entity')
    current_entity = entity_elem.get('name') if entity_elem is not None else 'unknown'

    # Track line numbers (approximation)
    line = 1

    # Validate each field
    for elem in root.iter():
        tag = elem.tag
        line += 1

        # Skip non-field elements
        if tag in ['domain-models', 'module', 'entity']:
            continue

        # Inter-attribute validation
        attr_errors, attr_warnings = validate_inter_attribute(elem, line)
        errors.extend(attr_errors)
        warnings.extend(attr_warnings)

        # Cross-entity validation
        cross_errors, cross_warnings = validate_cross_entity(elem, line, entity_index, current_entity)
        errors.extend(cross_errors)
        warnings.extend(cross_warnings)

    return errors, warnings


def print_report(xml_path: Path, errors: List, warnings: List):
    """Print concise validation report (token-optimized)"""
    print(f"SEMANTIC VALIDATION: {xml_path.name}\n")

    if errors:
        print(f"ERRORS: {len(errors)}\n")
        for line, tag, name, message in errors:
            print(f"  Line {line}, {tag} \"{name}\"")
            print(f"    {message}\n")

    if warnings:
        print(f"WARNINGS: {len(warnings)}\n")
        for line, tag, name, message in warnings:
            print(f"  Line {line}, {tag} \"{name}\"")
            print(f"    {message}\n")

    if not errors and not warnings:
        print("No issues found.\n")

    field_count = max(len(errors) + len(warnings), 1)
    print("SUMMARY:")
    print(f"- Fields checked: {field_count}")
    print(f"- Errors: {len(errors)}")
    print(f"- Warnings: {len(warnings)}")
    print(f"- Status: {'FAILED' if errors else 'PASSED'}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 semantic_validator.py <domain.xml|dir>")
        sys.exit(1)

    target = Path(sys.argv[1])

    # Determine domains directory
    if target.is_file():
        domains_dir = target.parent
    else:
        domains_dir = target

    print(f"Building entity index from: {domains_dir}")
    entity_index = build_entity_index(domains_dir)
    print(f"Indexed {len(entity_index.entities)} entities\n")

    has_errors = False

    # Validate file(s)
    if target.is_file():
        errors, warnings = validate_domain(target, entity_index)
        print_report(target, errors, warnings)
        has_errors = len(errors) > 0
    elif target.is_dir():
        for xml_file in sorted(target.glob('*.xml')):
            errors, warnings = validate_domain(xml_file, entity_index)
            print_report(xml_file, errors, warnings)
            if errors:
                has_errors = True
            print("\n" + "="*60 + "\n")
    else:
        print(f"ERROR: Path not found: {target}")
        sys.exit(1)

    # Exit code
    sys.exit(1 if has_errors else 0)


if __name__ == '__main__':
    main()
