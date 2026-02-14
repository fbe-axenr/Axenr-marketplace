#!/usr/bin/env python3
"""
Axelor Java Style Validator

Validates Java source files against Axelor code style rules.
CRITICAL checks: NO EMOJI, ENGLISH ONLY, naming conventions.

Usage:
    python3 java_style_validator.py <file_or_directory>

Examples:
    python3 java_style_validator.py Service.java
    python3 java_style_validator.py src/main/java/
    python3 java_style_validator.py . --verbose
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class StyleViolation:
    """Represents a style violation."""
    file_path: str
    line_number: int
    rule: str
    severity: str  # ERROR, WARNING
    message: str
    line_content: str = ""


class JavaStyleValidator:
    """Validates Java files against Axelor style rules."""

    # Emoji detection regex (comprehensive)
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols
        "\U00002600-\U000026FF"  # misc symbols
        "]+",
        flags=re.UNICODE
    )

    # Common French words to detect
    FRENCH_PATTERNS = [
        r'\bbon\b', r'\bmais\b', r'\bpour\b', r'\bvoir\b', r'\bici\b',
        r'\bétat\b', r'\bêtre\b', r'\bavoir\b', r'\bfaire\b', r'\bdire\b',
        r'\baller\b', r'\bvenir\b', r'\bpouvoir\b', r'\bvouloir\b',
        r'\bdevoir\b', r'\bsavoir\b', r'\bfalloir\b', r'\bcroire\b',
        r'\bcommande\b', r'\bproduit\b', r'\bclient\b', r'\bfacture\b',
        r'\bdate\b', r'\bmontant\b', r'\bprix\b', r'\bquantit[ée]\b',
        r'\bvalidé\b', r'\bconfirmé\b', r'\bannulé\b', r'\bbrouillon\b',
        r'\bcréé\b', r'\bmodifié\b', r'\bsupprimé\b',
        r'\bchamp\b', r'\bvaleur\b', r'\berr?eur\b', r'\bavertissement\b',
        r'\bsucc[èe]s\b', r'\béchec\b', r'\btraitement\b',
    ]

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.violations: List[StyleViolation] = []

    def validate_file(self, file_path: Path) -> List[StyleViolation]:
        """Validate a single Java file."""
        self.violations = []

        if not file_path.exists():
            print(f"ERROR: File not found: {file_path}", file=sys.stderr)
            return self.violations

        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            for line_num, line in enumerate(lines, start=1):
                self._check_emoji(file_path, line_num, line)
                self._check_french(file_path, line_num, line)
                self._check_naming(file_path, line_num, line)
                self._check_imports(file_path, line_num, line)

        except Exception as e:
            print(f"ERROR reading {file_path}: {e}", file=sys.stderr)

        return self.violations

    def _check_emoji(self, file_path: Path, line_num: int, line: str):
        """Check for emoji in code."""
        if self.EMOJI_PATTERN.search(line):
            self.violations.append(StyleViolation(
                file_path=str(file_path),
                line_number=line_num,
                rule="NO_EMOJI",
                severity="ERROR",
                message="Emoji detected in code (CRITICAL VIOLATION)",
                line_content=line.strip()
            ))

    def _check_french(self, file_path: Path, line_num: int, line: str):
        """Check for French text in code."""
        # Skip lines that are just imports or package declarations
        if line.strip().startswith('import ') or line.strip().startswith('package '):
            return

        # Skip lines with common English words that might false-positive
        if any(word in line.lower() for word in ['error', 'date', 'value', 'field']):
            return

        # Check for French patterns in strings and comments
        for pattern in self.FRENCH_PATTERNS:
            if re.search(pattern, line.lower()):
                # Only flag if in string literal or comment
                if '"' in line or "'" in line or '//' in line or '/*' in line or '*' in line:
                    self.violations.append(StyleViolation(
                        file_path=str(file_path),
                        line_number=line_num,
                        rule="ENGLISH_ONLY",
                        severity="ERROR",
                        message=f"Possible French text detected (pattern: {pattern})",
                        line_content=line.strip()
                    ))
                    break

    def _check_naming(self, file_path: Path, line_num: int, line: str):
        """Check naming conventions."""
        line_stripped = line.strip()

        # Skip comments
        if line_stripped.startswith('//') or line_stripped.startswith('*') or line_stripped.startswith('/*'):
            return

        # Check class names (should be PascalCase)
        class_match = re.search(r'\b(class|interface|enum)\s+([a-z][a-zA-Z0-9]*)', line_stripped)
        if class_match:
            class_name = class_match.group(2)
            self.violations.append(StyleViolation(
                file_path=str(file_path),
                line_number=line_num,
                rule="CLASS_NAMING",
                severity="ERROR",
                message=f"Class/Interface/Enum name must be PascalCase: {class_name}",
                line_content=line.strip()
            ))

        # Check method names (should be camelCase, not PascalCase)
        method_match = re.search(r'\b(public|protected|private)\s+\w+\s+([A-Z][a-zA-Z0-9]*)\s*\(', line_stripped)
        if method_match:
            method_name = method_match.group(2)
            self.violations.append(StyleViolation(
                file_path=str(file_path),
                line_number=line_num,
                rule="METHOD_NAMING",
                severity="ERROR",
                message=f"Method name should be camelCase, not PascalCase: {method_name}",
                line_content=line.strip()
            ))

        # Check constants (should be UPPER_SNAKE_CASE)
        const_match = re.search(r'static\s+final\s+\w+\s+([a-z][a-zA-Z0-9_]*)\s*=', line_stripped)
        if const_match:
            const_name = const_match.group(1)
            if not const_name.isupper():
                self.violations.append(StyleViolation(
                    file_path=str(file_path),
                    line_number=line_num,
                    rule="CONSTANT_NAMING",
                    severity="WARNING",
                    message=f"Constant should be UPPER_SNAKE_CASE: {const_name}",
                    line_content=line.strip()
                ))

    def _check_imports(self, file_path: Path, line_num: int, line: str):
        """Check import statements."""
        line_stripped = line.strip()

        # Check for wildcard imports (except java.util.*)
        if line_stripped.startswith('import ') and line_stripped.endswith('.*;'):
            if 'java.util.*' not in line_stripped:
                self.violations.append(StyleViolation(
                    file_path=str(file_path),
                    line_number=line_num,
                    rule="WILDCARD_IMPORT",
                    severity="WARNING",
                    message="Avoid wildcard imports (except java.util.*)",
                    line_content=line.strip()
                ))

    def validate_directory(self, directory: Path) -> Dict[str, List[StyleViolation]]:
        """Validate all Java files in a directory."""
        results = {}

        for java_file in directory.rglob('*.java'):
            if self.verbose:
                print(f"Validating: {java_file}")

            violations = self.validate_file(java_file)
            if violations:
                results[str(java_file)] = violations

        return results

    def print_report(self, results: Dict[str, List[StyleViolation]]):
        """Print validation report."""
        print("=" * 70)
        print("AXELOR JAVA STYLE VALIDATION REPORT")
        print("=" * 70)

        if not results:
            print("\n NO VIOLATIONS FOUND")
            print("\nAll files comply with Axelor style rules:")
            print("  ✓ NO EMOJI")
            print("  ✓ ENGLISH ONLY")
            print("  ✓ Naming conventions correct")
            print("  ✓ Import organization correct")
            print("=" * 70)
            return

        total_errors = 0
        total_warnings = 0

        for file_path, violations in sorted(results.items()):
            print(f"\n File: {file_path}")
            print("-" * 70)

            for violation in violations:
                icon = "❌" if violation.severity == "ERROR" else "⚠️"
                print(f"{icon} Line {violation.line_number}: [{violation.rule}] {violation.message}")
                if violation.line_content:
                    print(f"   → {violation.line_content}")

                if violation.severity == "ERROR":
                    total_errors += 1
                else:
                    total_warnings += 1

        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Files checked: {len(results)}")
        print(f"Errors: {total_errors}")
        print(f"Warnings: {total_warnings}")

        if total_errors > 0:
            print("\nCRITICAL: Fix all errors before committing!")
            print("\nMost common errors:")
            print("  1. Emoji in code → Remove all emoji")
            print("  2. French text → Translate to English")
            print("  3. Wrong naming → Use PascalCase/camelCase/UPPER_SNAKE_CASE")

        print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Validate Java files against Axelor style rules",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Critical Rules:
  - NO EMOJI anywhere in code (comments, strings, logs)
  - ENGLISH ONLY (no French or other languages)
  - PascalCase for classes/interfaces/enums
  - camelCase for methods and variables
  - UPPER_SNAKE_CASE for constants

Exit Codes:
  0 = No violations
  1 = Violations found
  2 = Error during validation

Examples:
  python3 java_style_validator.py Service.java
  python3 java_style_validator.py src/main/java/
  python3 java_style_validator.py . --verbose
        """
    )

    parser.add_argument(
        "path",
        help="File or directory to validate"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )

    args = parser.parse_args()

    path = Path(args.path)
    if not path.exists():
        print(f"ERROR: Path not found: {path}", file=sys.stderr)
        sys.exit(2)

    validator = JavaStyleValidator(verbose=args.verbose)

    if path.is_file():
        violations = validator.validate_file(path)
        results = {str(path): violations} if violations else {}
    else:
        results = validator.validate_directory(path)

    validator.print_report(results)

    # Exit with error if violations found
    if results:
        has_errors = any(
            v.severity == "ERROR"
            for violations in results.values()
            for v in violations
        )
        sys.exit(1 if has_errors else 0)

    sys.exit(0)


if __name__ == "__main__":
    main()
