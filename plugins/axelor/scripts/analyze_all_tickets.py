#!/usr/bin/env python3
"""
Complete Redmine Ticket Analysis Pipeline

This script orchestrates the FULL workflow:
1. Phase 1: Scrape tickets from Redmine (project or single ticket)
2. Phase 2: Analyze ALL trackers automatically (no interruption)

Supports two input modes:
- PROJECT MODE: Analyze all tickets from a Redmine project
- SINGLE TICKET MODE: Analyze a single ticket by URL

This ensures 100% automation without agent intervention.

Usage:
    # Project mode (multiple tickets)
    python analyze_all_tickets.py --project-url https://redmine.axelor.com/projects/axerp --output-dir <dir>

    # Single ticket mode
    python analyze_all_tickets.py --ticket-url https://redmine.axelor.com/issues/104267 --output-dir <dir>

    # With existing scraped data:
    python analyze_all_tickets.py --output-dir <dir> --skip-scraping
"""

import argparse
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def get_script_dir() -> Path:
    """Get the directory containing this script."""
    return Path(__file__).parent.resolve()


def detect_aos_path() -> Optional[str]:
    """
    Auto-detect AOS codebase path from environment or standard locations.

    Priority:
    1. Environment variable AOS_PATH
    2. Environment variable AXELOR_OPEN_SUITE_PATH
    3. Standard locations relative to project

    Returns:
        Path to AOS if found, None otherwise
    """
    # Check environment variables
    aos_env = os.environ.get('AOS_PATH')
    if aos_env and Path(aos_env).exists():
        return aos_env

    aos_env_alt = os.environ.get('AXELOR_OPEN_SUITE_PATH')
    if aos_env_alt and Path(aos_env_alt).exists():
        return aos_env_alt

    # Check standard locations relative to this script
    script_dir = get_script_dir()

    # Common patterns for AOS location
    standard_paths = [
        # Project-local .axelor/ directory (highest priority for local detection)
        Path.cwd() / ".axelor" / "aos",
        script_dir.parent.parent.parent / ".axelor" / "aos",
        # Project-specific paths
        Path.home() / "Project" / "AOS" / "axelor-open-suite",
        Path.home() / "Project" / "axelor-open-suite",
        # Relative to plugin location
        script_dir.parent.parent.parent.parent.parent / "axelor-open-suite",
        script_dir.parent.parent / "axelor-open-suite",
        script_dir.parent / "axelor-open-suite",
        # Standard home locations
        Path.home() / "axelor-open-suite",
        Path.home() / "AOS" / "axelor-open-suite",
        # Legacy system-wide locations (fallback)
        Path("/opt/axelor-open-suite"),
        Path("/opt/axelor/aos"),
    ]

    for path in standard_paths:
        if path.exists() and path.is_dir():
            # Verify it's actually an AOS directory by checking for marker files/directories
            # AOS has modules like axelor-base, axelor-account, etc.
            is_aos = (
                (path / "axelor-core").exists() or
                (path / "axelor-base").exists() or
                (path / "build.gradle").exists() or
                (path / "settings.gradle").exists()
            )
            if is_aos:
                return str(path.resolve())

    return None


def detect_input_type(url: str) -> str:
    """
    Detect whether the input URL is a project URL or a single ticket URL.

    Args:
        url: Input URL to analyze

    Returns:
        str: 'project' or 'ticket'
    """
    if '/issues/' in url:
        return 'ticket'
    elif '/projects/' in url:
        return 'project'
    else:
        raise ValueError(f"Cannot determine URL type. Expected /projects/ or /issues/ in URL: {url}")


def extract_ticket_id_from_url(ticket_url: str) -> int:
    """
    Extract the ticket ID from a Redmine issue URL.

    Args:
        ticket_url: Full URL to the Redmine issue

    Returns:
        int: Ticket ID
    """
    path_parts = urlparse(ticket_url).path.strip('/').split('/')
    if 'issues' in path_parts:
        idx = path_parts.index('issues')
        if idx + 1 < len(path_parts):
            ticket_id = path_parts[idx + 1].split('?')[0]
            if ticket_id.isdigit():
                return int(ticket_id)
    raise ValueError(f"Cannot extract ticket ID from URL: {ticket_url}")


def run_scraping(project_url: str, output_dir: Path) -> bool:
    """
    Phase 1: Scrape all tickets from Redmine project.
    Returns True if successful.
    """
    print("\n" + "=" * 60)
    print("PHASE 1: SCRAPING REDMINE TICKETS (PROJECT MODE)")
    print("=" * 60)

    script_path = get_script_dir() / "fetch_redmine_tickets.py"
    scrap_dir = output_dir / "Scrap"

    if not script_path.exists():
        print(f"ERROR: Scraping script not found: {script_path}")
        return False

    cmd = [
        sys.executable,
        str(script_path),
        "--project-url", project_url,
        "--output-dir", str(scrap_dir)
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(get_script_dir()))

    if result.returncode != 0:
        print(f"ERROR: Scraping failed with code {result.returncode}")
        return False

    print("Phase 1 completed successfully")
    return True


def run_single_ticket_scraping(ticket_url: str, output_dir: Path) -> bool:
    """
    Phase 1: Scrape a single ticket from Redmine.
    Returns True if successful.
    """
    print("\n" + "=" * 60)
    print("PHASE 1: SCRAPING SINGLE REDMINE TICKET")
    print("=" * 60)

    ticket_id = extract_ticket_id_from_url(ticket_url)
    print(f"Ticket ID: #{ticket_id}")

    script_path = get_script_dir() / "fetch_redmine_tickets.py"
    scrap_dir = output_dir / "Scrap"

    if not script_path.exists():
        print(f"ERROR: Scraping script not found: {script_path}")
        return False

    cmd = [
        sys.executable,
        str(script_path),
        "--ticket-url", ticket_url,
        "--output-dir", str(scrap_dir)
    ]

    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=str(get_script_dir()))

    if result.returncode != 0:
        print(f"ERROR: Scraping failed with code {result.returncode}")
        return False

    print("Phase 1 completed successfully")
    return True


def discover_trackers(scrap_dir: Path) -> list[str]:
    """Discover all tracker directories in Scrap/."""
    trackers = []
    if scrap_dir.exists():
        for item in scrap_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Check if it contains .md files
                md_files = list(item.glob("*.md"))
                if md_files:
                    trackers.append(item.name)
    return sorted(trackers)


def run_analysis_for_tracker(scrap_dir: Path, output_dir: Path, tracker: str,
                             workers: int = 8, aos_path: str = None) -> dict:
    """
    Run orchestrate_ticket_analysis.py for a single tracker.
    Returns dict with success count and failure count.
    """
    script_path = get_script_dir() / "orchestrate_ticket_analysis.py"
    tracker_scrap = scrap_dir / tracker

    ticket_count = len(list(tracker_scrap.glob("*.md")))
    print(f"\n--- Tracker: {tracker} ({ticket_count} tickets) ---")

    cmd = [
        sys.executable,
        str(script_path),
        "--scrap-dir", str(tracker_scrap),
        "--output-dir", str(output_dir),
        "--tracker", tracker,
        "--workers", str(workers)
    ]

    # Add AOS enrichment if path provided
    if aos_path:
        cmd.extend(["--aos-path", aos_path])

    result = subprocess.run(cmd, cwd=str(get_script_dir()))

    return {
        "tracker": tracker,
        "tickets": ticket_count,
        "success": result.returncode == 0
    }


def run_all_analyses(output_dir: Path, workers: int = 8, aos_path: str = None,
                     tracker_parallelism: int = 1) -> bool:
    """
    Phase 2: Analyze ALL trackers automatically.
    Returns True if all trackers were processed.

    Args:
        tracker_parallelism: Number of trackers to process in parallel (default: 1 for sequential)
    """
    print("\n" + "=" * 60)
    print("PHASE 2: ANALYZING ALL TRACKERS")
    print("=" * 60)
    print(f"Workers per tracker: {workers}")
    print(f"Tracker parallelism: {tracker_parallelism} ({'parallel' if tracker_parallelism > 1 else 'sequential'})")
    print(f"AOS enrichment: {'enabled' if aos_path else 'disabled'}")

    scrap_dir = output_dir / "Scrap"
    trackers = discover_trackers(scrap_dir)

    if not trackers:
        print(f"ERROR: No tracker directories found in {scrap_dir}")
        return False

    total_tickets = sum(len(list((scrap_dir / t).glob("*.md"))) for t in trackers)
    print(f"\nDiscovered {len(trackers)} trackers with {total_tickets} total tickets:")
    for t in trackers:
        count = len(list((scrap_dir / t).glob("*.md")))
        print(f"  - {t}: {count} tickets")

    print("\nStarting analysis (this may take a while)...\n")

    results = []

    if tracker_parallelism > 1:
        # Parallel processing of trackers
        def process_tracker_with_index(args):
            i, tracker = args
            print(f"\n[{i}/{len(trackers)}] Processing tracker: {tracker}")
            return run_analysis_for_tracker(scrap_dir, output_dir, tracker, workers, aos_path)

        with ThreadPoolExecutor(max_workers=tracker_parallelism) as executor:
            futures = {
                executor.submit(process_tracker_with_index, (i, tracker)): tracker
                for i, tracker in enumerate(trackers, 1)
            }

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    print(f"✓ Completed tracker: {result['tracker']}")
                except Exception as e:
                    tracker = futures[future]
                    print(f"✗ Failed tracker: {tracker} - {str(e)}")
                    results.append({
                        "tracker": tracker,
                        "tickets": 0,
                        "success": False
                    })
    else:
        # Sequential processing (original behavior)
        for i, tracker in enumerate(trackers, 1):
            print(f"\n[{i}/{len(trackers)}] Processing tracker: {tracker}")
            result = run_analysis_for_tracker(scrap_dir, output_dir, tracker, workers, aos_path)
            results.append(result)

    # Summary
    print("\n" + "=" * 60)
    print("PHASE 2 COMPLETE - SUMMARY")
    print("=" * 60)

    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]

    print(f"\nTrackers processed: {len(results)}")
    print(f"  Successful: {len(successful)}")
    print(f"  Failed: {len(failed)}")

    if failed:
        print("\nFailed trackers:")
        for r in failed:
            print(f"  - {r['tracker']} ({r['tickets']} tickets)")

    total_processed = sum(r["tickets"] for r in successful)
    print(f"\nTotal tickets processed: {total_processed}/{total_tickets}")

    return len(failed) == 0


def main():
    parser = argparse.ArgumentParser(
        description="Complete Redmine ticket analysis pipeline"
    )
    # Input modes
    parser.add_argument(
        "--project-url",
        help="Redmine project URL (e.g., https://redmine.axelor.com/projects/axerp)"
    )
    parser.add_argument(
        "--ticket-url",
        help="Single ticket URL (e.g., https://redmine.axelor.com/issues/104267)"
    )
    parser.add_argument(
        "--url",
        help="Auto-detect URL type (project or ticket)"
    )
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Output directory for all results"
    )
    parser.add_argument(
        "--skip-scraping",
        action="store_true",
        help="Skip Phase 1 (scraping), use existing Scrap/ data"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=8,
        help="Number of parallel workers per tracker (default: 8). Use 1 for sequential processing."
    )
    parser.add_argument(
        "--tracker-parallelism",
        type=int,
        default=2,
        help="Number of trackers to process in parallel (default: 2). Use 1 for sequential tracker processing."
    )
    parser.add_argument(
        "--aos-path",
        help="Path to AOS codebase for entity validation enrichment (auto-detected if not provided)"
    )
    parser.add_argument(
        "--no-aos-enrichment",
        action="store_true",
        help="Disable AOS enrichment even if AOS path is available"
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # Determine AOS path: explicit > auto-detect > None (if disabled)
    aos_path = None
    if not args.no_aos_enrichment:
        if args.aos_path:
            # Explicit path provided
            aos_path = args.aos_path
            print(f"Using provided AOS path: {aos_path}")
        else:
            # Try auto-detection
            detected_path = detect_aos_path()
            if detected_path:
                aos_path = detected_path
                print(f"Auto-detected AOS path: {aos_path}")
            else:
                print("No AOS path detected. Enrichment disabled.")
                print("Set AOS_PATH environment variable or use --aos-path to enable.")
    else:
        print("AOS enrichment explicitly disabled (--no-aos-enrichment)")

    print("=" * 60)
    print("REDMINE TICKET ANALYSIS PIPELINE")
    print("=" * 60)
    print(f"Output directory: {output_dir}")
    print(f"AOS enrichment: {'enabled (' + aos_path + ')' if aos_path else 'disabled'}")

    # Determine input mode
    input_url = args.url or args.project_url or args.ticket_url
    input_mode = None

    if args.ticket_url:
        input_mode = 'ticket'
        input_url = args.ticket_url
    elif args.project_url:
        input_mode = 'project'
        input_url = args.project_url
    elif args.url:
        # Auto-detect mode from URL
        input_mode = detect_input_type(args.url)
        input_url = args.url

    # Phase 1: Scraping
    if not args.skip_scraping:
        if not input_url:
            print("ERROR: --project-url, --ticket-url, or --url is required unless --skip-scraping is used")
            sys.exit(1)

        # Auto-detect if not already determined
        if not input_mode:
            input_mode = detect_input_type(input_url)

        print(f"Input URL: {input_url}")
        print(f"Mode: {input_mode.upper()}")

        if input_mode == 'ticket':
            ticket_id = extract_ticket_id_from_url(input_url)
            print(f"Ticket ID: #{ticket_id}")
            if not run_single_ticket_scraping(input_url, output_dir):
                print("\nPipeline failed at Phase 1 (scraping)")
                sys.exit(1)
        else:
            if not run_scraping(input_url, output_dir):
                print("\nPipeline failed at Phase 1 (scraping)")
                sys.exit(1)
    else:
        print("Skipping Phase 1 (using existing scraped data)")

    # Phase 2: Analysis
    if not run_all_analyses(output_dir, args.workers, aos_path, args.tracker_parallelism):
        print("\nPipeline completed with some failures in Phase 2")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)
    print(f"\nResults available in: {output_dir}")
    print("  - requirements-registry.json")
    print("  - specs/{Tracker}/REQ-XXX.md")
    print("  - index/by-*.json")


if __name__ == "__main__":
    main()
