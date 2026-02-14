#!/usr/bin/env python3
"""
Audit Documentation vs XSD Reference
Compares field-types-reference.md with domain-models-reference.md
"""

import sys
import re
from pathlib import Path
from typing import Dict, Set


def extract_attributes_from_xsd_ref(ref_path: Path) -> Dict[str, Set[str]]:
    """
    Extract attributes from domain-models-reference.md
    Returns: {element_name: set(attribute_names)}
    """
    elements = {}
    current_element = None
    current_attrs = set()

    with open(ref_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('## `<'):
                if current_element and current_attrs:
                    elements[current_element] = current_attrs

                match = re.search(r'<([^>]+)>', line)
                if match:
                    current_element = match.group(1)
                    current_attrs = set()

            elif line.startswith('- **`') and current_element:
                attr_match = re.match(r'- \*\*`([^`]+)`\*\*', line)
                if attr_match:
                    current_attrs.add(attr_match.group(1))

    if current_element and current_attrs:
        elements[current_element] = current_attrs

    return elements


def extract_attributes_from_docs(docs_path: Path) -> Dict[str, Set[str]]:
    """
    Extract attributes from field-types-reference.md
    Returns: {element_name: set(attribute_names)}
    """
    elements = {}
    current_element = None
    current_attrs = set()

    with open(docs_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Section header: ### String Field or ## String
            if line.startswith('###') or line.startswith('##'):
                if current_element and current_attrs:
                    elements[current_element] = current_attrs

                # Try to extract element name
                if 'String' in line or 'string' in line:
                    current_element = 'string'
                    current_attrs = set()
                elif 'Integer' in line or 'integer' in line:
                    current_element = 'integer'
                    current_attrs = set()
                elif 'Decimal' in line or 'decimal' in line:
                    current_element = 'decimal'
                    current_attrs = set()
                # Add more as needed

            # Table row: | attrName | ... |
            elif '|' in line and current_element:
                parts = line.split('|')
                if len(parts) >= 2:
                    attr_name = parts[1].strip()
                    if attr_name and attr_name != 'Attribute' and not attr_name.startswith('-'):
                        current_attrs.add(attr_name)

    if current_element and current_attrs:
        elements[current_element] = current_attrs

    return elements


def audit(xsd_ref_path: Path, docs_path: Path):
    """Compare and output audit report"""
    print("AUDIT REPORT: Documentation vs XSD Reference\n")

    xsd_attrs = extract_attributes_from_xsd_ref(xsd_ref_path)
    doc_attrs = extract_attributes_from_docs(docs_path)

    all_elements = set(xsd_attrs.keys()) | set(doc_attrs.keys())

    for element in sorted(all_elements):
        xsd_set = xsd_attrs.get(element, set())
        doc_set = doc_attrs.get(element, set())

        documented_valid = xsd_set & doc_set
        missing_in_doc = xsd_set - doc_set
        extra_in_doc = doc_set - xsd_set

        print(f"ELEMENT: {element}")
        print(f"  Documented and valid: {', '.join(sorted(documented_valid)) if documented_valid else 'none'} ({len(documented_valid)})")
        print(f"  Missing in doc: {', '.join(sorted(missing_in_doc)) if missing_in_doc else 'none'} ({len(missing_in_doc)})")
        print(f"  Documented but not in XSD: {', '.join(sorted(extra_in_doc)) if extra_in_doc else 'none'} ({len(extra_in_doc)})")
        print()


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 audit_docs_vs_xsd.py <field-types-reference.md> <domain-models-reference.md>")
        sys.exit(1)

    docs_path = Path(sys.argv[1])
    xsd_ref_path = Path(sys.argv[2])

    if not docs_path.exists():
        print(f"ERROR: Documentation file not found: {docs_path}")
        sys.exit(1)

    if not xsd_ref_path.exists():
        print(f"ERROR: XSD reference file not found: {xsd_ref_path}")
        sys.exit(1)

    audit(xsd_ref_path, docs_path)


if __name__ == '__main__':
    main()
