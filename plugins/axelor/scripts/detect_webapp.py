#!/usr/bin/env python3
"""
Auto-detection of Axelor webapp root directory.
Used by /develop command to locate the project root.

Detection strategy:
1. Start from current directory
2. Walk up the tree looking for build.gradle with com.axelor.app plugin
3. Validate the structure (modules/, gradle.properties)

Usage:
    python3 detect_webapp.py                # Auto-detect from current directory
    python3 detect_webapp.py /path/to/dir   # Auto-detect from specified directory
    python3 detect_webapp.py --validate /path/to/webapp  # Validate a specific path
"""

import sys
import re
from pathlib import Path
import json
import argparse


def is_axelor_webapp(path: Path) -> bool:
    """
    Check if the given path is an Axelor webapp root.

    Criteria:
    - Has build.gradle with 'com.axelor.app' plugin
    - Has modules/ directory
    - Has gradle.properties
    """
    build_gradle = path / "build.gradle"
    modules_dir = path / "modules"
    gradle_props = path / "gradle.properties"

    if not build_gradle.exists():
        return False

    if not modules_dir.exists() or not modules_dir.is_dir():
        return False

    if not gradle_props.exists():
        return False

    # Check for com.axelor.app plugin in build.gradle
    try:
        content = build_gradle.read_text()
        # Match patterns like: id 'com.axelor.app' or id "com.axelor.app"
        if re.search(r"id\s+['\"]com\.axelor\.app['\"]", content):
            return True
        # Also match: apply plugin: 'com.axelor.app'
        if re.search(r"apply\s+plugin:\s+['\"]com\.axelor\.app['\"]", content):
            return True
    except Exception:
        return False

    return False


def extract_webapp_metadata(webapp_root: Path) -> dict:
    """
    Extract metadata from the webapp.

    Returns:
        dict with webapp_name, aop_version, aos_version, java_version
    """
    metadata = {
        "webapp_name": None,
        "aop_version": None,
        "aos_version": None,
        "java_version": "11"  # Default
    }

    # Read gradle.properties
    gradle_props = webapp_root / "gradle.properties"
    if gradle_props.exists():
        try:
            content = gradle_props.read_text()
            for line in content.splitlines():
                line = line.strip()
                if line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()

                if key == "aopVersion":
                    # Extract major.minor from version like "7.4.+" or "7.4.0"
                    match = re.match(r"(\d+\.\d+)", value)
                    if match:
                        metadata["aop_version"] = match.group(1)
                elif key == "aosVersion":
                    metadata["aos_version"] = value
                elif key == "javaVersion":
                    metadata["java_version"] = value
        except Exception:
            pass

    # Read build.gradle for appName
    build_gradle = webapp_root / "build.gradle"
    if build_gradle.exists():
        try:
            content = build_gradle.read_text()
            # Match appName = "MyApp" or appName "MyApp"
            match = re.search(r"appName\s*[=]?\s*['\"]([^'\"]+)['\"]", content)
            if match:
                metadata["webapp_name"] = match.group(1)
        except Exception:
            pass

    return metadata


def find_webapp_root(start_path: Path) -> tuple[Path | None, str | None]:
    """
    Walk up the directory tree from start_path looking for an Axelor webapp.

    Returns:
        (webapp_path, None) if found
        (None, error_message) if not found
    """
    current = start_path.resolve()

    # Limit search depth to prevent infinite loops
    max_depth = 20
    depth = 0

    while depth < max_depth:
        if is_axelor_webapp(current):
            return current, None

        parent = current.parent
        if parent == current:
            # Reached filesystem root
            break
        current = parent
        depth += 1

    return None, f"No Axelor webapp found from {start_path} (searched {depth} levels up)"


def validate_webapp(path: str) -> dict:
    """
    Validate that a specific path is an Axelor webapp.

    Returns:
        dict with validation result
    """
    webapp_path = Path(path).resolve()

    if not webapp_path.exists():
        return {
            "valid": False,
            "webapp_root": None,
            "error": f"Path does not exist: {path}",
            "metadata": None
        }

    if not is_axelor_webapp(webapp_path):
        return {
            "valid": False,
            "webapp_root": None,
            "error": f"Not a valid Axelor webapp: {path} (missing build.gradle with com.axelor.app, modules/, or gradle.properties)",
            "metadata": None
        }

    metadata = extract_webapp_metadata(webapp_path)

    return {
        "valid": True,
        "webapp_root": str(webapp_path),
        "error": None,
        "metadata": metadata
    }


def detect_webapp(start_path: str = None) -> dict:
    """
    Auto-detect Axelor webapp from current directory or specified path.

    Args:
        start_path: Optional starting directory (defaults to current directory)

    Returns:
        dict with detection result
    """
    if start_path:
        start = Path(start_path)
    else:
        start = Path.cwd()

    if not start.exists():
        return {
            "detected": False,
            "webapp_root": None,
            "detection_method": "error",
            "error": f"Start path does not exist: {start}",
            "metadata": None
        }

    webapp_root, error = find_webapp_root(start)

    if error:
        return {
            "detected": False,
            "webapp_root": None,
            "detection_method": "not_found",
            "error": error,
            "metadata": None
        }

    metadata = extract_webapp_metadata(webapp_root)

    return {
        "detected": True,
        "webapp_root": str(webapp_root),
        "detection_method": "auto",
        "error": None,
        "metadata": metadata
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Detect Axelor webapp root directory"
    )
    parser.add_argument(
        'path',
        nargs='?',
        default=None,
        help="Starting directory for detection (defaults to current directory)"
    )
    parser.add_argument(
        '--validate',
        metavar='PATH',
        help="Validate a specific path as an Axelor webapp"
    )

    args = parser.parse_args()

    if args.validate:
        result = validate_webapp(args.validate)
    else:
        result = detect_webapp(args.path)

    print(json.dumps(result, indent=2))
