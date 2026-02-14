#!/bin/bash
set -e

# Script to generate changelog using git-cliff
# Usage:
#   ./scripts/generate-changelog.sh              # Generate full changelog
#   ./scripts/generate-changelog.sh v1.0.0       # Generate changelog for specific tag
#   ./scripts/generate-changelog.sh --unreleased # Generate unreleased changes only

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$ROOT_DIR"

# Check if git-cliff is installed
if ! command -v git-cliff &> /dev/null; then
    echo "❌ git-cliff is not installed"
    echo ""
    echo "Install with:"
    echo "  cargo install git-cliff"
    echo "  or"
    echo "  brew install git-cliff  (on macOS)"
    exit 1
fi

echo "🚀 Generating changelog with git-cliff..."
echo ""

# Generate changelog based on arguments
if [ "$1" = "--unreleased" ]; then
    echo "📝 Generating unreleased changes..."
    git-cliff --unreleased --prepend CHANGELOG.md
elif [ -n "$1" ]; then
    echo "📝 Generating changelog for $1..."
    git-cliff --tag "$1" --prepend CHANGELOG.md
else
    echo "📝 Generating full changelog..."
    git-cliff --output CHANGELOG.md
fi

echo ""
echo "✅ Changelog generated successfully!"
echo "📄 File: CHANGELOG.md"
echo ""
echo "Next steps:"
echo "  1. Review the generated changelog"
echo "  2. Edit manually if needed (add context, clarify breaking changes)"
echo "  3. Commit: git add CHANGELOG.md && git commit -m 'docs: update changelog'"
