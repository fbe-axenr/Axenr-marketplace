#!/usr/bin/env python3
"""
Axelor View Extension Validator (Simplified)

Validates extension-specific rules NOT covered by XSD validation:
- extension="true" attribute with matching <extend> elements
- Unique and non-empty 'id' attribute for extension views
- Non-empty 'name' attribute for extension views

Note: Run XSD validation BEFORE this validator for complete validation.

Usage:
    python3 axelor_view_extension_validator.py <file_or_directory>

Exit codes:
    0 - All validations passed
    1 - Validation errors found
    2 - Invalid arguments or file not found
"""

import sys
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Set


class ViewExtensionValidator:
    """Validates Axelor view extension XML files."""

    # Only form and grid support extension="true" with <extend> elements
    # Other view types require full override with unique id
    EXTENSIBLE_VIEW_TYPES = {'form', 'grid'}
    OVERRIDE_VIEW_TYPES = {'tree', 'calendar', 'kanban', 'cards', 'gantt', 'chart', 'dashboard'}

    def __init__(self):
        self.seen_ids: Set[str] = set()
        self.errors: List[str] = []
        self.extension_count = 0
        self.valid_count = 0

    def _get_tag(self, elem: ET.Element) -> str:
        """Extract tag name without namespace."""
        return elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag

    def _has_extend_children(self, elem: ET.Element) -> bool:
        """Check if element has <extend> children."""
        return any(self._get_tag(child) == 'extend' for child in elem)

    def validate_file(self, file_path: str) -> bool:
        """Validate a single XML file. Returns True if valid."""
        if not file_path.endswith('.xml'):
            return True

        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            self.errors.append(f"{file_path}: XML parse error - {e}")
            return False

        file_valid = True
        for elem in root.iter():
            tag = self._get_tag(elem)
            extension_attr = elem.get('extension')
            view_id = elem.get('id')
            view_name = elem.get('name')
            has_extend = self._has_extend_children(elem)

            # Case 1: Extensible views (form, grid) with extension="true"
            if tag in self.EXTENSIBLE_VIEW_TYPES and extension_attr == 'true':
                self.extension_count += 1
                is_valid = True

                # Check id
                if view_id is None:
                    self.errors.append(f"{file_path}: {tag}[name='{view_name}'] - Missing 'id' attribute")
                    is_valid = False
                elif view_id.strip() == '':
                    self.errors.append(f"{file_path}: {tag}[name='{view_name}'] - Empty 'id' attribute")
                    is_valid = False
                elif view_id in self.seen_ids:
                    self.errors.append(f"{file_path}: {tag}[id='{view_id}'] - Duplicate id")
                    is_valid = False
                else:
                    self.seen_ids.add(view_id)

                # Check name
                if view_name is None:
                    self.errors.append(f"{file_path}: {tag}[id='{view_id}'] - Missing 'name' attribute")
                    is_valid = False
                elif view_name.strip() == '':
                    self.errors.append(f"{file_path}: {tag}[id='{view_id}'] - Empty 'name' attribute")
                    is_valid = False

                if is_valid:
                    self.valid_count += 1
                else:
                    file_valid = False

            # Case 2: Has <extend> but no extension="true" (form/grid only)
            elif tag in self.EXTENSIBLE_VIEW_TYPES and has_extend and extension_attr is None:
                self.errors.append(f"{file_path}: {tag}[name='{view_name}'] - Has <extend> but missing extension=\"true\"")
                file_valid = False

            # Case 3: Non-extensible views (tree, calendar, etc.) using extension="true" - ERROR
            elif tag in self.OVERRIDE_VIEW_TYPES and extension_attr == 'true':
                self.errors.append(f"{file_path}: {tag}[name='{view_name}'] - extension=\"true\" not supported for {tag}. Use full override with unique id instead.")
                file_valid = False

        return file_valid

    def validate_directory(self, dir_path: str) -> bool:
        """Validate all XML files in directory. Returns True if all valid."""
        path = Path(dir_path)
        if not path.exists():
            self.errors.append(f"Directory not found: {dir_path}")
            return False

        all_valid = True
        for xml_file in path.rglob('*.xml'):
            if not self.validate_file(str(xml_file)):
                all_valid = False
        return all_valid

    def print_report(self) -> bool:
        """Print report. Returns True if errors found."""
        print("\n" + "=" * 60)
        print("VIEW EXTENSION VALIDATION")
        print("=" * 60)

        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  - {error}")

        print(f"\nExtension views: {self.extension_count}")
        print(f"Valid: {self.valid_count}")
        print(f"Errors: {len(self.errors)}")

        if self.errors:
            print("\nSTATUS: FAILED")
        elif self.extension_count > 0:
            print("\nSTATUS: PASSED")
        else:
            print("\nSTATUS: No extension views found")

        print("=" * 60 + "\n")
        return len(self.errors) > 0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)

    target = sys.argv[1]
    if not os.path.exists(target):
        print(f"Error: '{target}' not found")
        sys.exit(2)

    validator = ViewExtensionValidator()

    if os.path.isfile(target):
        validator.validate_file(target)
    else:
        validator.validate_directory(target)

    has_errors = validator.print_report()
    sys.exit(1 if has_errors else 0)


if __name__ == '__main__':
    main()
