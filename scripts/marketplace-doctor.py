#!/usr/bin/env python3
"""
Marketplace Doctor - audits the AxENR marketplace integrity.

Usage:
    python3 scripts/marketplace-doctor.py [--strict] [--json]

Exit codes:
    0 - no issue (or only INFO in lax mode)
    1 - WARN/CRITICAL detected in strict mode, CRITICAL in lax mode
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F6FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA70-\U0001FAFF"
    "\U00002600-\U000027BF"
    "\U0001F1E0-\U0001F1FF"
    "]+",
    flags=re.UNICODE,
)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


class Check:
    def __init__(self, check_id: str, severity: str, message: str, fix: str = ""):
        self.id = check_id
        self.severity = severity
        self.message = message
        self.fix = fix

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "severity": self.severity,
            "message": self.message,
            "fix": self.fix,
        }


def load_json(path: Path) -> Any:
    with path.open() as fh:
        return json.load(fh)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    fm: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm


def run_checks() -> list[Check]:
    checks: list[Check] = []

    marketplace_json_path = ROOT / ".claude-plugin" / "marketplace.json"
    if not marketplace_json_path.exists():
        checks.append(Check("JSON-VALID", "CRITICAL", "marketplace.json missing"))
        return checks

    try:
        marketplace = load_json(marketplace_json_path)
    except json.JSONDecodeError as exc:
        checks.append(Check("JSON-VALID", "CRITICAL", f"marketplace.json invalid: {exc}"))
        return checks

    plugins_declared = marketplace.get("plugins", [])
    for plugin in plugins_declared:
        source_rel = plugin["source"].lstrip("./")
        plugin_dir = ROOT / source_rel
        plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"

        if not plugin_dir.exists():
            checks.append(
                Check(
                    "PLUGIN-REF",
                    "CRITICAL",
                    f"Plugin source not found: {plugin['source']}",
                    fix=f"Create directory {plugin_dir} or remove plugin from marketplace.json",
                )
            )
            continue

        if not plugin_json_path.exists():
            checks.append(
                Check(
                    "PLUGIN-REF",
                    "CRITICAL",
                    f"plugin.json missing for {plugin['name']}",
                    fix=f"Create {plugin_json_path}",
                )
            )
            continue

        try:
            plugin_json = load_json(plugin_json_path)
        except json.JSONDecodeError as exc:
            checks.append(
                Check(
                    "JSON-VALID",
                    "CRITICAL",
                    f"{plugin_json_path} invalid: {exc}",
                )
            )
            continue

        declared_version = plugin["version"]
        actual_version = plugin_json.get("version")
        if declared_version != actual_version:
            checks.append(
                Check(
                    "VER-SYNC",
                    "CRITICAL",
                    f"Version mismatch for {plugin['name']}: "
                    f"marketplace.json={declared_version} plugin.json={actual_version}",
                    fix="Run /axenr:bump-version or sync both files manually",
                )
            )

    axenr_plugin = ROOT / "plugins" / "axenr"
    if axenr_plugin.exists():
        names: dict[str, list[Path]] = {}
        for md_path in axenr_plugin.rglob("*.md"):
            parts = md_path.relative_to(axenr_plugin).parts
            if parts[0] not in {"agents", "skills", "commands"}:
                continue

            if parts[0] == "agents":
                if len(parts) != 2:
                    continue
            elif parts[0] == "commands":
                if len(parts) != 2:
                    continue
            elif parts[0] == "skills":
                if len(parts) != 3:
                    continue

            text = md_path.read_text(encoding="utf-8")

            if EMOJI_PATTERN.search(text):
                checks.append(
                    Check(
                        "EMOJI-DETECTED",
                        "WARN",
                        f"Emoji in {md_path.relative_to(ROOT)}",
                        fix="Remove emojis (AxENR rule: NO EMOJIS)",
                    )
                )

            line_count = len(text.splitlines())
            if parts[0] == "agents" and line_count > 800:
                checks.append(
                    Check(
                        "LARGE-AGENT",
                        "WARN",
                        f"{md_path.relative_to(ROOT)} has {line_count} lines (>800)",
                        fix="Consider splitting into multiple sub-agents or external includes",
                    )
                )

            fm = parse_frontmatter(text)
            if parts[0] in {"agents", "skills"}:
                if fm is None or "name" not in fm or "description" not in fm:
                    checks.append(
                        Check(
                            "FRONTMATTER",
                            "CRITICAL",
                            f"Missing or invalid frontmatter in {md_path.relative_to(ROOT)}",
                            fix="Add YAML frontmatter with 'name' and 'description'",
                        )
                    )
                else:
                    names.setdefault(fm["name"], []).append(md_path)

        for name, paths in names.items():
            if len(paths) > 1:
                checks.append(
                    Check(
                        "DUPLICATE-NAME",
                        "CRITICAL",
                        f"Duplicate name '{name}' in: "
                        + ", ".join(str(p.relative_to(ROOT)) for p in paths),
                        fix="Rename one of the components",
                    )
                )

    lessons_file = axenr_plugin / "docs" / "lessons" / "LESSONS-LEARNED.md"
    if lessons_file.exists():
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ct", str(lessons_file)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0 and result.stdout.strip():
                import time

                last_ts = int(result.stdout.strip())
                age_days = (time.time() - last_ts) / 86400
                if age_days > 30:
                    checks.append(
                        Check(
                            "STALE-LESSONS",
                            "WARN",
                            f"LESSONS-LEARNED.md not updated since {age_days:.0f} days",
                            fix="Run /axenr:consolidate-lessons or resolve tickets",
                        )
                    )
        except Exception:
            pass

    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true", help="Exit 1 on WARN too")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    args = parser.parse_args()

    checks = run_checks()

    summary = {"CRITICAL": 0, "WARN": 0, "INFO": 0}
    for check in checks:
        summary[check.severity] = summary.get(check.severity, 0) + 1

    if summary["CRITICAL"] > 0:
        status = "critical"
    elif summary["WARN"] > 0:
        status = "warnings"
    else:
        status = "ok"

    exit_code = 0
    if summary["CRITICAL"] > 0:
        exit_code = 1
    elif args.strict and summary["WARN"] > 0:
        exit_code = 1

    if args.json:
        print(
            json.dumps(
                {
                    "status": status,
                    "exit_code": exit_code,
                    "summary": summary,
                    "checks": [c.to_dict() for c in checks],
                },
                indent=2,
            )
        )
    else:
        print(f"Marketplace Doctor - status: {status}")
        print(
            f"  CRITICAL: {summary['CRITICAL']}  WARN: {summary['WARN']}  INFO: {summary['INFO']}"
        )
        for severity in ("CRITICAL", "WARN", "INFO"):
            items = [c for c in checks if c.severity == severity]
            if not items:
                continue
            print(f"\n{severity}:")
            for check in items:
                print(f"  [{check.id}] {check.message}")
                if check.fix:
                    print(f"    Fix: {check.fix}")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
