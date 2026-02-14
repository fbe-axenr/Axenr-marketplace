#!/usr/bin/env python3
"""
Script to fetch Redmine tickets from a project and export them as markdown files.

This script supports two modes:
1. PROJECT MODE: Fetch all tickets from a Redmine project
2. SINGLE TICKET MODE: Fetch a single ticket by URL or ID

Fetched data includes:
- Project, Tracker, Priority, Status
- Target Version, Sprint, Module (custom fields)
- Description, Notes (journals)
- Related issues (relations)
- Title

Usage:
    python fetch_redmine_tickets.py [options]

Options:
    --project-url URL    Redmine project URL (project mode)
    --ticket-url URL     Single ticket URL (e.g., https://redmine.axelor.com/issues/104267)
    --ticket-id ID       Single ticket ID (requires --base-url)
    --base-url URL       Base Redmine URL (for --ticket-id mode)
    --env-file PATH      Path to .env file (default: .env in current directory)
    --output-dir PATH    Output directory (default: ./Analysis/Ticket/Scrap)
    --tracker TRACKER    Filter by tracker name (optional, project mode only)
    --status STATUS      Filter by status (optional, project mode only)
    --limit N            Limit number of tickets (optional, project mode only)
    --incremental        Only fetch new or updated tickets (default behavior)
    --force              Force re-fetch all tickets, ignoring cache
    --since DATE         Only fetch tickets updated since DATE (YYYY-MM-DD)
    --include-status     Comma-separated list of statuses to include (default: New,In Progress,Feedback,En cours)

Environment Variables (from .env):
    REDMINE_API          API key for authentication
    REDMINE_PROJECT_URL  Default project URL
    REDMINE_BASE_URL     Default base URL (for single ticket mode)

Example:
    # Project mode (multiple tickets)
    python fetch_redmine_tickets.py --project-url https://redmine.axelor.com/projects/axerp

    # Single ticket mode (by URL)
    python fetch_redmine_tickets.py --ticket-url https://redmine.axelor.com/issues/104267

    # Single ticket mode (by ID)
    python fetch_redmine_tickets.py --ticket-id 104267 --base-url https://redmine.axelor.com
"""

import sys
import os
import argparse
import requests
import json
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, urljoin

# Index file to track scraped tickets
INDEX_FILENAME = ".tickets-index.json"


def load_tickets_index(output_dir):
    """
    Load the tickets index file that tracks already scraped tickets.

    Args:
        output_dir: Output directory containing the index

    Returns:
        dict: Index with ticket IDs as keys and metadata as values
    """
    index_path = Path(output_dir) / INDEX_FILENAME
    if index_path.exists():
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_tickets_index(output_dir, index):
    """
    Save the tickets index file.

    Args:
        output_dir: Output directory for the index
        index: Dictionary with ticket metadata
    """
    index_path = Path(output_dir) / INDEX_FILENAME
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def needs_update(issue_summary, index):
    """
    Check if a ticket needs to be fetched/updated.

    Args:
        issue_summary: Issue summary from Redmine API
        index: Current tickets index

    Returns:
        tuple: (needs_update: bool, reason: str)
    """
    issue_id = str(issue_summary.get('id'))
    updated_on = issue_summary.get('updated_on', '')

    if issue_id not in index:
        return True, "new"

    cached_updated = index[issue_id].get('updated_on', '')
    if updated_on != cached_updated:
        return True, "modified"

    return False, "unchanged"


def load_env_file(env_path):
    """
    Load environment variables from a .env file.

    Args:
        env_path: Path to the .env file

    Returns:
        dict: Dictionary of environment variables
    """
    env_vars = {}
    if not os.path.exists(env_path):
        return env_vars

    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            # Parse KEY=VALUE or KEY="VALUE"
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                # Remove surrounding quotes
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                env_vars[key] = value
    return env_vars


def extract_project_identifier(project_url):
    """
    Extract the project identifier from a Redmine project URL.

    Args:
        project_url: Full URL to the Redmine project

    Returns:
        tuple: (base_url, project_identifier)
    """
    parsed = urlparse(project_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    # Extract project identifier from path
    # URL format: https://redmine.example.com/projects/project-name
    path_parts = parsed.path.strip('/').split('/')
    if 'projects' in path_parts:
        idx = path_parts.index('projects')
        if idx + 1 < len(path_parts):
            project_id = path_parts[idx + 1]
            return base_url, project_id

    raise ValueError(f"Cannot extract project identifier from URL: {project_url}")


def extract_ticket_id_from_url(ticket_url):
    """
    Extract the ticket ID and base URL from a Redmine issue URL.

    Args:
        ticket_url: Full URL to the Redmine issue (e.g., https://redmine.axelor.com/issues/104267)

    Returns:
        tuple: (base_url, ticket_id)
    """
    parsed = urlparse(ticket_url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"

    # Extract issue ID from path
    # URL format: https://redmine.example.com/issues/12345
    path_parts = parsed.path.strip('/').split('/')
    if 'issues' in path_parts:
        idx = path_parts.index('issues')
        if idx + 1 < len(path_parts):
            ticket_id = path_parts[idx + 1].split('?')[0]  # Remove query params
            if ticket_id.isdigit():
                return base_url, int(ticket_id)

    raise ValueError(f"Cannot extract ticket ID from URL: {ticket_url}")


def detect_input_type(url):
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


def fetch_project_info(base_url, project_id, api_key):
    """
    Fetch project information from Redmine.

    Args:
        base_url: Base Redmine URL
        project_id: Project identifier
        api_key: API key for authentication

    Returns:
        dict: Project information
    """
    url = f"{base_url}/projects/{project_id}.json"
    headers = {'X-Redmine-API-Key': api_key} if api_key else {}

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get('project', {})


def fetch_issues(base_url, project_id, api_key, tracker=None, status=None, limit=None):
    """
    Fetch all issues from a Redmine project.

    Args:
        base_url: Base Redmine URL
        project_id: Project identifier
        api_key: API key for authentication
        tracker: Optional tracker filter
        status: Optional status filter
        limit: Optional limit on number of issues

    Returns:
        list: List of issues
    """
    issues = []
    offset = 0
    page_limit = 100  # Redmine default max

    headers = {'X-Redmine-API-Key': api_key} if api_key else {}

    while True:
        url = f"{base_url}/issues.json"
        params = {
            'project_id': project_id,
            'offset': offset,
            'limit': page_limit,
            'status_id': '*' if status is None else status,  # '*' for all statuses
        }

        if tracker:
            params['tracker_id'] = tracker

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        batch = data.get('issues', [])
        if not batch:
            break

        issues.extend(batch)

        # Check if we've reached the limit
        if limit and len(issues) >= limit:
            issues = issues[:limit]
            break

        # Check if there are more pages
        total_count = data.get('total_count', 0)
        if offset + len(batch) >= total_count:
            break

        offset += page_limit
        print(f"  Fetched {len(issues)}/{total_count} issues...")

    return issues


def fetch_issue_details(base_url, issue_id, api_key):
    """
    Fetch detailed information for a single issue including journals and relations.

    Args:
        base_url: Base Redmine URL
        issue_id: Issue ID
        api_key: API key for authentication

    Returns:
        dict: Detailed issue information
    """
    url = f"{base_url}/issues/{issue_id}.json"
    params = {
        'include': 'journals,relations,attachments,children'
    }
    headers = {'X-Redmine-API-Key': api_key} if api_key else {}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json().get('issue', {})


def extract_custom_fields(issue):
    """
    Extract custom fields from an issue into a dictionary.

    Args:
        issue: Issue data

    Returns:
        dict: Custom fields by name
    """
    custom_fields = {}
    for cf in issue.get('custom_fields', []):
        name = cf.get('name', '')
        value = cf.get('value', '')
        if value:  # Only include non-empty values
            custom_fields[name] = value
    return custom_fields


def format_journals(journals):
    """
    Format issue journals (notes/comments) as markdown.

    Args:
        journals: List of journal entries

    Returns:
        str: Formatted markdown string
    """
    if not journals:
        return "_Aucune note_"

    notes = []
    for journal in journals:
        if journal.get('notes'):  # Only include entries with notes
            author = journal.get('user', {}).get('name', 'Inconnu')
            created = journal.get('created_on', '')
            note_text = journal.get('notes', '')

            notes.append(f"**{author}** - _{created}_\n\n{note_text}")

    if not notes:
        return "_Aucune note_"

    return "\n\n---\n\n".join(notes)


def format_relations(relations, base_url):
    """
    Format issue relations as markdown.

    Args:
        relations: List of relations
        base_url: Base Redmine URL for links

    Returns:
        str: Formatted markdown string
    """
    if not relations:
        return "_Aucune demande liée_"

    relation_types = {
        'relates': 'Lié à',
        'duplicates': 'Duplique',
        'duplicated': 'Dupliqué par',
        'blocks': 'Bloque',
        'blocked': 'Bloqué par',
        'precedes': 'Précède',
        'follows': 'Suit',
        'copied_to': 'Copié vers',
        'copied_from': 'Copié depuis'
    }

    lines = []
    for rel in relations:
        rel_type = relation_types.get(rel.get('relation_type', ''), rel.get('relation_type', ''))
        issue_id = rel.get('issue_id') or rel.get('issue_to_id')
        if issue_id:
            lines.append(f"- {rel_type} [#{issue_id}]({base_url}/issues/{issue_id})")

    return "\n".join(lines) if lines else "_Aucune demande liée_"


def create_issue_markdown(issue, base_url, project_info):
    """
    Create a markdown document from detailed issue data.

    Args:
        issue: Detailed issue data
        base_url: Base Redmine URL
        project_info: Project information

    Returns:
        str: Markdown content
    """
    # Extract basic fields
    issue_id = issue.get('id', 'N/A')
    subject = issue.get('subject', 'Sans titre')
    description = issue.get('description', '_Aucune description_') or '_Aucune description_'

    # Metadata
    project_name = issue.get('project', {}).get('name', project_info.get('name', 'N/A'))
    tracker = issue.get('tracker', {}).get('name', 'N/A')
    status = issue.get('status', {}).get('name', 'N/A')
    priority = issue.get('priority', {}).get('name', 'N/A')
    author = issue.get('author', {}).get('name', 'N/A')
    assigned_to = issue.get('assigned_to', {}).get('name', 'Non assigné')
    created_on = issue.get('created_on', 'N/A')
    updated_on = issue.get('updated_on', 'N/A')

    # Version and sprint (might be in fixed_version or custom fields)
    fixed_version = issue.get('fixed_version', {}).get('name', '')

    # Custom fields
    custom_fields = extract_custom_fields(issue)
    sprint = custom_fields.get('Sprint', custom_fields.get('sprint', ''))
    module = custom_fields.get('Module', custom_fields.get('module', ''))

    # Use fixed_version as target version if available
    target_version = fixed_version or custom_fields.get('Version cible', '')

    # Journals (notes)
    journals = issue.get('journals', [])
    notes_md = format_journals(journals)

    # Relations
    relations = issue.get('relations', [])
    relations_md = format_relations(relations, base_url)

    # Build custom fields section
    custom_fields_md = ""
    if custom_fields:
        cf_lines = []
        for name, value in custom_fields.items():
            if name not in ['Sprint', 'sprint', 'Module', 'module', 'Version cible']:
                cf_lines.append(f"| {name} | {value} |")
        if cf_lines:
            custom_fields_md = f"""
## Champs Personnalisés

| Champ | Valeur |
|-------|--------|
{chr(10).join(cf_lines)}
"""

    # Create markdown content
    markdown_content = f"""# {subject}

## Métadonnées

| Propriété | Valeur |
|-----------|--------|
| **ID Redmine** | #{issue_id} |
| **URL** | [{base_url}/issues/{issue_id}]({base_url}/issues/{issue_id}) |
| **Projet** | {project_name} |
| **Tracker** | {tracker} |
| **Statut** | {status} |
| **Priorité** | {priority} |
| **Auteur** | {author} |
| **Assigné à** | {assigned_to} |
| **Créé le** | {created_on} |
| **Mis à jour le** | {updated_on} |
| **Version cible** | {target_version or '_Non définie_'} |
| **Sprint** | {sprint or '_Non défini_'} |
| **Module** | {module or '_Non défini_'} |

## Description

{description}
{custom_fields_md}
## Demandes Liées

{relations_md}

## Notes et Commentaires

{notes_md}

---

_Document généré automatiquement le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}_
_Source: Redmine {base_url}/issues/{issue_id}_
"""

    return markdown_content


def sanitize_filename(filename):
    """
    Sanitize a filename to make it filesystem-compatible.

    Args:
        filename: Original filename

    Returns:
        str: Sanitized filename
    """
    # Replace invalid characters with hyphens
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '-')

    # Replace multiple hyphens with single
    filename = re.sub(r'-+', '-', filename)

    # Remove leading/trailing hyphens and spaces
    filename = filename.strip('- ')

    # Limit length
    if len(filename) > 80:
        filename = filename[:80]

    return filename


def save_issue(issue_md, issue_id, subject, tracker, output_dir):
    """
    Save an issue markdown to the appropriate directory.

    Args:
        issue_md: Markdown content
        issue_id: Issue ID
        subject: Issue subject
        tracker: Tracker name
        output_dir: Base output directory
    """
    # Sanitize tracker name for directory
    tracker_dir = sanitize_filename(tracker)

    # Create tracker directory
    tracker_path = Path(output_dir) / tracker_dir
    tracker_path.mkdir(parents=True, exist_ok=True)

    # Create filename (ID only, title is in metadata)
    filename = f"{issue_id:05d}.md"
    filepath = tracker_path / filename

    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(issue_md)

    return filepath


def fetch_single_ticket(base_url, ticket_id, api_key, output_path):
    """
    Fetch a single ticket and save it as markdown.

    Args:
        base_url: Base Redmine URL
        ticket_id: Issue ID to fetch
        api_key: API key for authentication
        output_path: Output directory path

    Returns:
        tuple: (filepath, tracker_name) or (None, None) on failure
    """
    print(f"Fetching ticket #{ticket_id} from {base_url}...")

    # Fetch detailed issue data
    issue_detail = fetch_issue_details(base_url, ticket_id, api_key)

    if not issue_detail:
        print(f"ERROR: Could not fetch ticket #{ticket_id}")
        return None, None

    # Extract info
    subject = issue_detail.get('subject', 'No subject')
    tracker = issue_detail.get('tracker', {}).get('name', 'Other')
    project_info = issue_detail.get('project', {})

    print(f"  Subject: {subject}")
    print(f"  Tracker: {tracker}")
    print(f"  Project: {project_info.get('name', 'Unknown')}")

    # Create markdown
    issue_md = create_issue_markdown(issue_detail, base_url, project_info)

    # Save to file
    filepath = save_issue(issue_md, ticket_id, subject, tracker, output_path)

    # Update index
    tickets_index = load_tickets_index(output_path)
    tickets_index[str(ticket_id)] = {
        'updated_on': issue_detail.get('updated_on', ''),
        'subject': subject,
        'tracker': tracker,
        'file': str(filepath),
        'scraped_at': datetime.now().isoformat()
    }
    save_tickets_index(output_path, tickets_index)

    print(f"  Saved to: {filepath}")
    return filepath, tracker


def run_project_mode(args, env_vars, api_key):
    """
    Run the project mode: fetch all tickets from a project.
    """
    project_url = args.project_url or env_vars.get('REDMINE_PROJECT_URL')
    if not project_url:
        print("Error: No project URL provided. Use --project-url or set REDMINE_PROJECT_URL in .env")
        sys.exit(1)

    # Determine mode
    incremental_mode = args.incremental and not args.force

    # Parse included statuses (whitelist approach - always applied)
    included_statuses = [s.strip().lower() for s in args.include_status.split(',')]

    print(f"Configuration:")
    print(f"  Mode: PROJECT (multiple tickets)")
    print(f"  Project URL: {project_url}")
    print(f"  Output directory: {args.output_dir}")
    print(f"  API key: {'***' + api_key[-4:] if api_key else 'Not set'}")
    print(f"  Fetch mode: {'Incremental (only new/modified)' if incremental_mode else 'Full (all tickets)'}")
    print(f"  Statuses filter: {', '.join(included_statuses)}")
    if args.since:
        print(f"  Since: {args.since}")
    print()

    # Extract base URL and project identifier
    base_url, project_id = extract_project_identifier(project_url)
    print(f"Fetching project: {project_id} from {base_url}")

    # Fetch project info
    project_info = fetch_project_info(base_url, project_id, api_key)
    print(f"Project: {project_info.get('name', project_id)}")
    print()

    # Load existing index for incremental mode
    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    tickets_index = load_tickets_index(output_path) if incremental_mode else {}
    if incremental_mode and tickets_index:
        print(f"Loaded index with {len(tickets_index)} previously scraped tickets")

    # Fetch issues
    print("Fetching issues list from Redmine...")
    issues = fetch_issues(base_url, project_id, api_key,
                         tracker=args.tracker, status=args.status, limit=args.limit)
    print(f"Found {len(issues)} issues in project")
    print()

    # Filter issues based on mode
    issues_to_process = []
    stats = {'new': 0, 'modified': 0, 'unchanged': 0, 'filtered_status': 0}

    for issue_summary in issues:
        # Filter by status inclusion (whitelist)
        if included_statuses:
            issue_status = issue_summary.get('status', {}).get('name', '').lower()
            if issue_status not in included_statuses:
                stats['filtered_status'] += 1
                continue

        # Filter by --since if provided
        if args.since:
            updated_on = issue_summary.get('updated_on', '')[:10]  # YYYY-MM-DD
            if updated_on < args.since:
                continue

        if incremental_mode:
            should_update, reason = needs_update(issue_summary, tickets_index)
            stats[reason] = stats.get(reason, 0) + 1
            if should_update:
                issues_to_process.append((issue_summary, reason))
        else:
            issues_to_process.append((issue_summary, 'force'))

    print(f"Filtering analysis:")
    print(f"  - Filtered out by status: {stats['filtered_status']}")
    if incremental_mode:
        print(f"  - New tickets: {stats['new']}")
        print(f"  - Modified tickets: {stats['modified']}")
        print(f"  - Unchanged (skipped): {stats['unchanged']}")
    print()

    if not issues_to_process:
        print("No tickets to process. All tickets are up to date.")
        return

    print(f"Processing {len(issues_to_process)} tickets...")
    print()

    # Process each issue
    trackers_count = {}
    processed_count = {'new': 0, 'modified': 0}

    for i, (issue_summary, reason) in enumerate(issues_to_process, 1):
        issue_id = issue_summary.get('id')
        subject = issue_summary.get('subject', 'No subject')
        tracker = issue_summary.get('tracker', {}).get('name', 'Other')
        updated_on = issue_summary.get('updated_on', '')

        status_icon = "+" if reason == 'new' else "~" if reason == 'modified' else " "
        print(f"[{i}/{len(issues_to_process)}] {status_icon} #{issue_id}: {subject[:50]}...")

        # Fetch detailed issue data
        issue_detail = fetch_issue_details(base_url, issue_id, api_key)

        # Create markdown
        issue_md = create_issue_markdown(issue_detail, base_url, project_info)

        # Save to file
        filepath = save_issue(issue_md, issue_id, subject, tracker, output_path)

        # Update index
        tickets_index[str(issue_id)] = {
            'updated_on': updated_on,
            'subject': subject,
            'tracker': tracker,
            'file': str(filepath),
            'scraped_at': datetime.now().isoformat()
        }

        # Count by tracker and status
        trackers_count[tracker] = trackers_count.get(tracker, 0) + 1
        if reason in processed_count:
            processed_count[reason] += 1

    # Save updated index
    save_tickets_index(output_path, tickets_index)

    print()
    print("=" * 50)
    print("Export completed!")
    print(f"Processed: {len(issues_to_process)} tickets")
    if incremental_mode:
        print(f"  - New: {processed_count['new']}")
        print(f"  - Updated: {processed_count['modified']}")
    print(f"Total in index: {len(tickets_index)} tickets")
    print(f"Output directory: {output_path.absolute()}")
    print()
    print("Issues by tracker:")
    for tracker, count in sorted(trackers_count.items()):
        print(f"  - {tracker}: {count}")


def run_single_ticket_mode(args, env_vars, api_key):
    """
    Run the single ticket mode: fetch one ticket by URL or ID.
    """
    # Determine base_url and ticket_id
    if args.ticket_url:
        base_url, ticket_id = extract_ticket_id_from_url(args.ticket_url)
    elif args.ticket_id:
        base_url = args.base_url or env_vars.get('REDMINE_BASE_URL')
        if not base_url:
            print("Error: --base-url is required when using --ticket-id")
            print("  Or set REDMINE_BASE_URL in .env")
            sys.exit(1)
        ticket_id = int(args.ticket_id)
    else:
        print("Error: Either --ticket-url or --ticket-id is required for single ticket mode")
        sys.exit(1)

    output_path = Path(args.output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"Configuration:")
    print(f"  Mode: SINGLE TICKET")
    print(f"  Ticket ID: #{ticket_id}")
    print(f"  Base URL: {base_url}")
    print(f"  Output directory: {args.output_dir}")
    print(f"  API key: {'***' + api_key[-4:] if api_key else 'Not set'}")
    print()

    filepath, tracker = fetch_single_ticket(base_url, ticket_id, api_key, output_path)

    if filepath:
        print()
        print("=" * 50)
        print("Export completed!")
        print(f"  Ticket: #{ticket_id}")
        print(f"  Tracker: {tracker}")
        print(f"  File: {filepath}")
    else:
        print("Export failed!")
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Fetch Redmine tickets and export as markdown files'
    )

    # Input modes (mutually exclusive in practice)
    parser.add_argument('--project-url', help='Redmine project URL (project mode)')
    parser.add_argument('--ticket-url', help='Single ticket URL (e.g., https://redmine.axelor.com/issues/104267)')
    parser.add_argument('--ticket-id', type=int, help='Single ticket ID (requires --base-url)')
    parser.add_argument('--base-url', help='Base Redmine URL (for --ticket-id mode)')

    # Common options
    parser.add_argument('--env-file', default='.env', help='Path to .env file')
    parser.add_argument('--output-dir', default='./Analysis/Ticket/Scrap',
                        help='Output directory')

    # Project mode options
    parser.add_argument('--tracker', help='Filter by tracker name (project mode only)')
    parser.add_argument('--status', help='Filter by status (project mode only)')
    parser.add_argument('--limit', type=int, help='Limit number of tickets (project mode only)')
    parser.add_argument('--incremental', action='store_true', default=True,
                        help='Only fetch new or updated tickets (default)')
    parser.add_argument('--force', action='store_true',
                        help='Force re-fetch all tickets, ignoring cache')
    parser.add_argument('--since', help='Only fetch tickets updated since DATE (YYYY-MM-DD)')
    parser.add_argument('--include-status', default='New,In Progress,Feedback,En cours',
                        help='Comma-separated statuses to include (default: New,In Progress,Feedback,En cours)')

    args = parser.parse_args()

    # Load environment variables from .env file
    env_vars = load_env_file(args.env_file)

    # Get API key
    api_key = env_vars.get('REDMINE_API') or os.environ.get('REDMINE_API')
    if not api_key:
        print("Warning: No REDMINE_API key found. Some tickets may not be accessible.")

    try:
        # Determine mode based on arguments
        if args.ticket_url or args.ticket_id:
            # Single ticket mode
            run_single_ticket_mode(args, env_vars, api_key)
        else:
            # Project mode (default)
            run_project_mode(args, env_vars, api_key)

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Redmine: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
