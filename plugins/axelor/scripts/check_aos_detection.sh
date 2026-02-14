#!/bin/bash
# Helper script to check AOS path detection

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== AOS Path Detection Check ==="
echo ""

# Check environment variables
echo "Environment Variables:"
echo "  AOS_PATH: ${AOS_PATH:-<not set>}"
echo "  AXELOR_OPEN_SUITE_PATH: ${AXELOR_OPEN_SUITE_PATH:-<not set>}"
echo ""

# Run the detection logic from Python
python3 << 'EOF'
import sys
import os
from pathlib import Path

try:
    from analyze_all_tickets import detect_aos_path

    detected = detect_aos_path()

    if detected:
        print(f"✓ AOS path detected: {detected}")
        print("")

        # Verify it's valid
        aos_path = Path(detected)
        markers_found = []
        if (aos_path / "axelor-core").exists():
            markers_found.append("axelor-core")
        if (aos_path / "axelor-base").exists():
            markers_found.append("axelor-base")
        if (aos_path / "build.gradle").exists():
            markers_found.append("build.gradle")
        if (aos_path / "settings.gradle").exists():
            markers_found.append("settings.gradle")

        if markers_found:
            print(f"✓ Found markers: {', '.join(markers_found)}")

        print("")
        print("AOS enrichment will be ENABLED automatically!")
    else:
        print("✗ No AOS path detected")
        print("")
        print("To enable AOS enrichment, set one of:")
        print("  export AOS_PATH=/path/to/axelor-open-suite")
        print("  export AXELOR_OPEN_SUITE_PATH=/path/to/axelor-open-suite")
        print("")
        print("Or place axelor-open-suite in one of these locations:")
        print("  - ~/Project/AOS/axelor-open-suite")
        print("  - ~/axelor-open-suite")
        print("  - /opt/axelor-open-suite")

except ImportError as e:
    print(f"Error importing: {e}")
    sys.exit(1)
EOF
