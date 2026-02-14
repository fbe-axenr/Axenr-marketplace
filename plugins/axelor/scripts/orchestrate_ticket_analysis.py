#!/usr/bin/env python3
"""
Orchestrator for Redmine Ticket Analysis (v2.1 - With Git Regression)

This script controls the workflow externally to guarantee 100% ticket processing.
It uses Claude SDK directly (not subprocess) for performance and parallelizes
analysis with ThreadPoolExecutor.

Improvements over v2.0:
    - Git regression analysis for bugs (find commit that introduced the bug)
    - Integration with aos-git-regression-finder skill

Improvements over v1.0:
    - Claude SDK instead of subprocess (30s overhead eliminated per ticket)
    - Parallel processing with configurable workers (4-8x faster)
    - AOS codebase integration for entity validation
    - Extended tools: Read, Write, Bash, Grep, WebFetch

Architecture:
    orchestrate_ticket_analysis.py
        │
        ├── ThreadPoolExecutor (N workers)
        │   │
        │   ▼  (parallel tickets)
        │   Claude SDK
        │   │
        │   ▼
        │   @skills/ticket-deep-analyzer (enriched)
        │   │
        │   ├── aos-entity-searcher (validate entities)
        │   ├── aos-field-comparator (validate fields)
        │   ├── aos-documentation-fetcher (context)
        │   └── aos-git-regression-finder (for bugs: find origin commit)
        │
        ▼
    JSON analysis output (enriched with regression_analysis for bugs)

Skills used:
    - @skills/ticket-deep-analyzer: Deep analysis with AOS enrichment
    - @skills/aos-entity-searcher: Entity validation
    - @skills/aos-field-comparator: Field validation
    - @skills/aos-documentation-fetcher: Module documentation
    - @skills/aos-git-regression-finder: Git regression search (bugs only)

Usage:
    python orchestrate_ticket_analysis.py --scrap-dir ./Scrap/Anomaly --output-dir ./output --aos-path /path/to/axelor-open-suite

See also:
    - @agents/redmine-agent
    - @commands/analyze-redmine-tickets
"""

import argparse
import json
import os
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional


def list_tickets(scrap_dir: Path) -> list[Path]:
    """List all ticket markdown files in the scrap directory."""
    tickets = sorted(scrap_dir.glob("*.md"))
    print(f"Found {len(tickets)} tickets in {scrap_dir}")
    return tickets


def extract_ticket_id(filename: str) -> str:
    """Extract ticket ID from filename like '05789.md'."""
    return filename.replace(".md", "")


# Global lock for thread-safe progress reporting
_progress_lock = threading.Lock()
_progress_counter = {"analyzed": 0, "failed": 0, "skipped": 0}


def _retry_with_backoff(func, max_retries=3, initial_delay=2.0, backoff_factor=2.0):
    """
    Retry a function with exponential backoff.

    Args:
        func: Function to retry (should return tuple of (success: bool, result))
        max_retries: Maximum number of retry attempts
        initial_delay: Initial delay in seconds
        backoff_factor: Multiplier for delay after each retry

    Returns:
        Result from func or None if all retries exhausted
    """
    delay = initial_delay

    for attempt in range(max_retries):
        success, result = func()

        if success:
            return result

        if attempt < max_retries - 1:
            print(f"    [RETRY] Attempt {attempt + 1}/{max_retries} failed, retrying in {delay:.1f}s...")
            time.sleep(delay)
            delay *= backoff_factor
        else:
            print(f"    [FAILED] All {max_retries} retry attempts exhausted")

    return None


def analyze_single_ticket(ticket_path: Path, output_dir: Path, tracker: str, aos_path: Optional[str] = None) -> Optional[dict]:
    """
    Analyze a single ticket using Claude SDK (or subprocess fallback).
    Returns the analysis result or None if failed.

    This function uses the official skill for consistency with the agent workflow.
    Now enriched with AOS entity validation via additional skills.
    """
    ticket_id = extract_ticket_id(ticket_path.name)
    output_file = output_dir / f"ticket-{ticket_id}.json"

    # Skip if already analyzed (for resumability)
    if output_file.exists():
        try:
            with open(output_file, 'r') as f:
                existing = json.load(f)
                if existing.get("ticket_id") == ticket_id:
                    with _progress_lock:
                        _progress_counter["skipped"] += 1
                    return existing
        except:
            pass  # Re-analyze if file is corrupted

    # Build AOS enrichment section if path provided
    aos_enrichment = ""
    if aos_path:
        aos_enrichment = f'''

## AOS Enrichment (IMPORTANT)
After extracting entities from the ticket, validate them against the actual AOS codebase:

1. **Entity Validation** (use @skills/aos-entity-searcher):
   - For each entity identified, search in: {aos_path}
   - Verify the entity exists in AOS domains
   - Get the exact file path and package name

2. **Field Validation** (use @skills/aos-field-comparator):
   - For fields mentioned in the ticket, verify they exist on the entity
   - Note any type mismatches or missing fields

3. **Module Context** (use @skills/aos-documentation-fetcher):
   - Fetch documentation for the identified modules
   - Add integration points and dependencies

Add an "aos_validation" section to the output:
```json
"aos_validation": {{
  "entities_validated": [
    {{"name": "Entity", "exists": true, "file": "path/to/Entity.xml", "package": "com.axelor.apps.module.db"}}
  ],
  "fields_validated": [
    {{"entity": "Entity", "field": "fieldName", "exists": true, "type": "String"}}
  ],
  "validation_score": 0-100
}}
```
'''

    # Add Git regression analysis for bugs
    git_regression = ""
    if aos_path and tracker.lower() == "anomaly":
        git_regression = f'''

## Git Regression Analysis (FOR BUGS ONLY)
After AOS validation, if the ticket is a bug (tracker: Anomaly), search for the regression origin:

4. **Git Regression Search** (use @skills/aos-git-regression-finder):
   - For each validated entity, construct suspect file paths:
     - Domain: `{{module}}/src/main/resources/domains/{{Entity}}.xml`
     - Service: `{{module}}/src/main/java/.../service/{{Entity}}ServiceImpl.java`
   - Use git log to find commits modifying these files
   - Use git blame on suspect lines if mentioned in the ticket
   - Calculate confidence scores for each commit

Add a "regression_analysis" section to the output (only for bugs):
```json
"regression_analysis": {{
  "search_scope": {{
    "repository": "{aos_path}",
    "files_analyzed": ["EntityServiceImpl.java"],
    "date_range": "1 year before ticket creation"
  }},
  "suspect_commits": [
    {{
      "hash": "abc1234",
      "date": "YYYY-MM-DD",
      "author": "Developer Name",
      "message": "commit message",
      "confidence": 0-100,
      "confidence_reason": "why this commit is suspected"
    }}
  ],
  "most_likely_cause": {{
    "commit": "abc1234",
    "confidence": 85,
    "evidence": ["reason1", "reason2"],
    "recommendation": "what to do"
  }},
  "contacts": [
    {{"name": "Developer", "email": "dev@axelor.com", "role": "Commit author"}}
  ]
}}
```
'''

    # Prepare the prompt using the ticket-deep-analyzer skill
    prompt = f'''Apply the ticket-deep-analyzer skill to analyze this Redmine ticket.

## Input Parameters
- ticket_path: {ticket_path}
- tracker_type: {tracker.lower()}

## Task
Use @skills/ticket-deep-analyzer to perform a deep analysis of this ticket.

Follow the skill's process:
1. Read the complete ticket content (description + all notes)
2. Identify the main need (title, type, description)
3. Extract the scope (modules, entities with fields, workflows)
4. Extract business rules with conditions
5. Analyze bug behavior if applicable (current vs expected, reproduction steps)
6. Derive acceptance criteria
7. Calculate priority score
{aos_enrichment}{git_regression}
## Output
Write the analysis result as JSON to: {output_file}

The JSON must include:
- ticket_id: "{ticket_id}"
- source_file: "{ticket_path.name}"
- tracker: "{tracker}"
- need: {{title, type, description, summary}}
- scope: {{modules, entities, workflows, ui_elements}}
- business_rules: [{{id, type, description, conditions, expected_behavior, source}}]
- acceptance_criteria: [{{id, description, type, derived_from}}]
- priority_score: {{value, factors}}
- ready_for_develop: boolean
- quality_score: 0-100
{f'- aos_validation: {{entities_validated, fields_validated, validation_score}}' if aos_path else ''}
{f'- regression_analysis: {{search_scope, suspect_commits, most_likely_cause, contacts}} (ONLY if tracker is Anomaly)' if aos_path and tracker.lower() == 'anomaly' else ''}

IMPORTANT:
- Read the FULL ticket content, not just the title
- Use the entity mapping from the skill (e.g., "facture" → Invoice)
- Derive acceptance criteria from business rules
- Only set ready_for_develop: true if quality_score >= 70'''

    # Extended tools for AOS enrichment
    allowed_tools = "Read,Write,Bash,Grep,WebFetch" if aos_path else "Read,Write"

    try:
        # Use Claude CLI subprocess for analysis
        result = _analyze_with_subprocess(prompt, output_file, ticket_id, allowed_tools)

        if result:
            with _progress_lock:
                _progress_counter["analyzed"] += 1
            return result
        else:
            with _progress_lock:
                _progress_counter["failed"] += 1
            return None

    except Exception as e:
        print(f"  [ERROR] Ticket {ticket_id}: {str(e)}")
        with _progress_lock:
            _progress_counter["failed"] += 1
        return None


def _analyze_with_subprocess(prompt: str, output_file: Path, ticket_id: str, allowed_tools: str) -> Optional[dict]:
    """Analyze using Claude CLI subprocess with retry logic."""
    # Increase timeout for AOS enrichment (5 minutes base, +2 for each extra tool)
    base_timeout = 300
    extra_tools = allowed_tools.count(',')
    timeout = base_timeout + (extra_tools * 120)  # Up to 9 minutes with all tools

    def attempt_analysis():
        """Single analysis attempt. Returns (success: bool, result: Optional[dict])."""
        try:
            result = subprocess.run(
                ["claude", "-p", prompt, "--allowedTools", allowed_tools, "--print"],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            # Check for rate limiting errors in stderr
            if result.stderr and ("rate limit" in result.stderr.lower() or "429" in result.stderr):
                print(f"  [RATE_LIMIT] Ticket {ticket_id}: Hit API rate limit")
                return (False, None)  # Trigger retry

            # Check for other API errors that should be retried
            if result.returncode != 0 and result.stderr:
                if "overloaded" in result.stderr.lower() or "503" in result.stderr:
                    print(f"  [OVERLOADED] Ticket {ticket_id}: API overloaded")
                    return (False, None)  # Trigger retry

        except subprocess.TimeoutExpired:
            print(f"  [TIMEOUT] Ticket {ticket_id}: Analysis timed out after {timeout}s")
            # Don't retry on timeout, but check if file was created anyway

        # Always check if output file exists (even after timeout or error)
        if output_file.exists():
            try:
                with open(output_file, 'r') as f:
                    analysis = json.load(f)
                    if analysis.get("ticket_id") == ticket_id:
                        print(f"  [OK] Ticket {ticket_id} analyzed")
                        return (True, analysis)  # Success
                    else:
                        print(f"  [ERROR] Ticket {ticket_id}: Invalid ticket_id in output")
                        return (False, None)  # Failure, but don't retry (bad output)
            except json.JSONDecodeError:
                print(f"  [ERROR] Ticket {ticket_id}: Invalid JSON in output file")
                return (False, None)  # Failure, but don't retry (corrupted output)
        else:
            # Output file not created - could be rate limit or other transient error
            return (False, None)

    # Use retry with exponential backoff
    return _retry_with_backoff(attempt_analysis, max_retries=3, initial_delay=5.0, backoff_factor=2.0)


def calculate_similarity(ticket1: dict, ticket2: dict) -> float:
    """
    Calculate similarity score between two tickets (0-100).
    Uses entity overlap, module match, and type match.
    """
    score = 0.0

    # Extract data from tickets
    scope1 = ticket1.get("scope", {})
    scope2 = ticket2.get("scope", {})
    need1 = ticket1.get("need", {})
    need2 = ticket2.get("need", {})

    # Entity overlap (40 points max)
    entities1 = set(e.get("name", e) if isinstance(e, dict) else e for e in scope1.get("entities", []))
    entities2 = set(e.get("name", e) if isinstance(e, dict) else e for e in scope2.get("entities", []))
    if entities1 and entities2:
        intersection = len(entities1 & entities2)
        union = len(entities1 | entities2)
        if union > 0:
            score += 40 * (intersection / union)

    # Module match (30 points max)
    modules1 = set(m.get("name", m) if isinstance(m, dict) else m for m in scope1.get("modules", []))
    modules2 = set(m.get("name", m) if isinstance(m, dict) else m for m in scope2.get("modules", []))
    if modules1 and modules2:
        intersection = len(modules1 & modules2)
        union = len(modules1 | modules2)
        if union > 0:
            score += 30 * (intersection / union)

    # Type match (15 points)
    type1 = need1.get("type", ticket1.get("type", ""))
    type2 = need2.get("type", ticket2.get("type", ""))
    if type1 and type2 and type1 == type2:
        score += 15

    # Workflow overlap (15 points max)
    workflows1 = set(w.get("name", w) if isinstance(w, dict) else w for w in scope1.get("workflows", []))
    workflows2 = set(w.get("name", w) if isinstance(w, dict) else w for w in scope2.get("workflows", []))
    if workflows1 and workflows2:
        intersection = len(workflows1 & workflows2)
        union = len(workflows1 | workflows2)
        if union > 0:
            score += 15 * (intersection / union)

    return score


def group_similar_tickets(tickets: list[dict], threshold: float = 70.0) -> list[list[dict]]:
    """
    Group tickets by similarity score.

    Thresholds:
    - >= 80%: Automatic merge (same requirement)
    - 60-79%: Parent requirement with sub-needs
    - < 60%: Separate requirements

    Returns list of groups, each group is a list of similar tickets.
    """
    if not tickets:
        return []

    # Start with each ticket in its own group
    groups = [[t] for t in tickets]

    # Merge groups with high similarity
    merged = True
    while merged:
        merged = False
        new_groups = []
        used = set()

        for i, group1 in enumerate(groups):
            if i in used:
                continue

            current_group = list(group1)

            for j, group2 in enumerate(groups):
                if j <= i or j in used:
                    continue

                # Check similarity between any ticket in group1 and any in group2
                max_sim = 0.0
                for t1 in group1:
                    for t2 in group2:
                        sim = calculate_similarity(t1, t2)
                        max_sim = max(max_sim, sim)

                if max_sim >= threshold:
                    current_group.extend(group2)
                    used.add(j)
                    merged = True

            new_groups.append(current_group)
            used.add(i)

        groups = new_groups

    return groups


def build_registry(analyzed_tickets: list[dict], output_dir: Path, tracker: str,
                   enable_grouping: bool = False, similarity_threshold: float = 70.0) -> dict:
    """
    Build the requirements registry from analyzed tickets.

    Handles both the new skill-based format (with 'need', 'scope' objects)
    and legacy format for backward compatibility.

    Args:
        analyzed_tickets: List of analyzed ticket dictionaries
        output_dir: Output directory path
        tracker: Tracker type (e.g., "Anomaly")
        enable_grouping: If True, group similar tickets into single requirements
        similarity_threshold: Minimum similarity score for grouping (default: 70%)
    """
    requirements = []

    if enable_grouping:
        # Group similar tickets
        groups = group_similar_tickets(analyzed_tickets, similarity_threshold)
        print(f"\n  Grouping: {len(analyzed_tickets)} tickets → {len(groups)} groups")

        for i, group in enumerate(groups, 1):
            req_id = f"REQ-{i:03d}"

            # Use the first ticket as primary, others as related
            primary = group[0]
            related = group[1:] if len(group) > 1 else []

            # Merge data from all tickets in group
            merged_entities = {}
            merged_modules = {}
            merged_workflows = set()
            all_rules = []
            all_criteria = []
            ticket_ids = []

            for ticket in group:
                ticket_ids.append(ticket["ticket_id"])
                scope = ticket.get("scope", {})

                # Merge entities
                for e in scope.get("entities", []):
                    name = e.get("name", e) if isinstance(e, dict) else e
                    if name not in merged_entities:
                        merged_entities[name] = e if isinstance(e, dict) else {"name": name, "role": "primary"}

                # Merge modules
                for m in scope.get("modules", []):
                    name = m.get("name", m) if isinstance(m, dict) else m
                    if name not in merged_modules:
                        merged_modules[name] = m if isinstance(m, dict) else {"name": name, "confidence": 80}

                # Merge workflows
                for w in scope.get("workflows", []):
                    wname = w.get("name", w) if isinstance(w, dict) else w
                    merged_workflows.add(wname)

                # Collect all business rules
                all_rules.extend(ticket.get("business_rules", []))

                # Collect all acceptance criteria
                all_criteria.extend(ticket.get("acceptance_criteria", []))

            # Use primary ticket for main fields
            need = primary.get("need", {})
            primary_scope = primary.get("scope", {})

            title = need.get("title") or primary.get("title", "Unknown")
            if len(group) > 1:
                title = f"[GROUP] {title}"

            req_type = need.get("type") or primary.get("type", "bug")
            description = need.get("description") or primary.get("description", "")
            summary = need.get("summary") or description

            modules_list = list(merged_modules.values())
            primary_module = modules_list[0]["name"] if modules_list else "Unknown"

            priority_score_obj = primary.get("priority_score", {})
            if isinstance(priority_score_obj, dict):
                priority_value = priority_score_obj.get("value", 50)
            else:
                priority_value = priority_score_obj if isinstance(priority_score_obj, (int, float)) else 50

            # Average quality score across group
            avg_quality = sum(t.get("quality_score", 0) for t in group) / len(group)

            requirements.append({
                "requirement_id": req_id,
                "ticket_id": primary["ticket_id"],  # Primary ticket
                "tracker": tracker,
                "title": title,
                "type": req_type,
                "module": primary_module,
                "description": {
                    "summary": summary,
                    "problem_statement": description,
                },
                "scope": {
                    "modules": modules_list,
                    "entities": list(merged_entities.values()),
                    "workflows": list(merged_workflows),
                    "ui_elements": primary_scope.get("ui_elements", [])
                },
                "business_rules": all_rules[:10],  # Limit to avoid bloat
                "acceptance_criteria": all_criteria[:10],  # Limit to avoid bloat
                "bug_analysis": primary.get("bug_analysis"),
                "regression_analysis": primary.get("regression_analysis"),  # For bugs
                "source_tickets": [{"id": tid, "contribution": "primary" if tid == primary["ticket_id"] else "related"}
                                  for tid in ticket_ids],
                "grouped_tickets_count": len(group),
                "priority": {
                    "score": priority_value,
                    "level": "high" if priority_value >= 70 else "medium" if priority_value >= 50 else "low"
                },
                "ready_for_develop": primary.get("ready_for_develop", False),
                "quality_score": round(avg_quality, 1)
            })
    else:
        # Original behavior: 1 ticket = 1 requirement
        for i, ticket in enumerate(analyzed_tickets, 1):
            req_id = f"REQ-{i:03d}"

            # Handle new skill-based format vs legacy format
            need = ticket.get("need", {})
            scope = ticket.get("scope", {})

            # Extract title from new format or fallback to legacy
            title = need.get("title") or ticket.get("title", "Unknown")
            req_type = need.get("type") or ticket.get("type", "bug")
            description = need.get("description") or ticket.get("description", "")
            summary = need.get("summary") or description

            # Extract modules from new format or fallback
            modules = scope.get("modules", [])
            if not modules and ticket.get("module"):
                modules = [{"name": ticket.get("module"), "confidence": 80}]
            primary_module = modules[0]["name"] if modules else "Unknown"

            # Extract entities from new format or fallback
            entities = scope.get("entities", [])
            if not entities and ticket.get("entities"):
                entities = [{"name": e, "role": "primary"} for e in ticket.get("entities", [])]

            # Extract business rules (already structured in new format)
            business_rules = ticket.get("business_rules", [])
            if business_rules and isinstance(business_rules[0], str):
                # Legacy format: convert strings to objects
                business_rules = [{"id": f"BR{j:03d}", "description": rule}
                                 for j, rule in enumerate(business_rules, 1)]

            # Extract acceptance criteria (already structured in new format)
            acceptance_criteria = ticket.get("acceptance_criteria", [])
            if acceptance_criteria and isinstance(acceptance_criteria[0], str):
                # Legacy format: convert strings to objects
                acceptance_criteria = [{"id": f"AC{j:03d}", "description": ac}
                                       for j, ac in enumerate(acceptance_criteria, 1)]

            # Extract priority score from new format or fallback
            priority_score_obj = ticket.get("priority_score", {})
            if isinstance(priority_score_obj, dict):
                priority_value = priority_score_obj.get("value", 50)
            else:
                priority_value = priority_score_obj if isinstance(priority_score_obj, (int, float)) else 50

            requirements.append({
                "requirement_id": req_id,
                "ticket_id": ticket["ticket_id"],
                "tracker": tracker,
                "title": title,
                "type": req_type,
                "module": primary_module,
                "description": {
                    "summary": summary,
                    "problem_statement": description,
                },
                "scope": {
                    "modules": modules,
                    "entities": entities,
                    "workflows": scope.get("workflows", []),
                    "ui_elements": scope.get("ui_elements", [])
                },
                "business_rules": business_rules,
                "acceptance_criteria": acceptance_criteria,
                "bug_analysis": ticket.get("bug_analysis"),  # Preserve if present
                "regression_analysis": ticket.get("regression_analysis"),  # Preserve if present (bugs only)
                "source_tickets": [{"id": ticket["ticket_id"], "contribution": "primary"}],
                "priority": {
                    "score": priority_value,
                    "level": "high" if priority_value >= 70 else "medium" if priority_value >= 50 else "low"
                },
                "ready_for_develop": ticket.get("ready_for_develop", False),
                "quality_score": ticket.get("quality_score", 0)
            })

    ready_count = sum(1 for r in requirements if r["ready_for_develop"])

    # Count grouped requirements (more than 1 source ticket)
    grouped_count = sum(1 for r in requirements if r.get("grouped_tickets_count", 1) > 1)
    total_tickets_in_groups = sum(r.get("grouped_tickets_count", 1) for r in requirements if r.get("grouped_tickets_count", 1) > 1)

    registry = {
        "registry_version": "3.0",
        "generated_at": datetime.now().isoformat(),
        "source": {
            "scrap_directory": str(output_dir.parent / "Scrap" / tracker),
            "tickets_analyzed": len(analyzed_tickets),
            "requirements_created": len(requirements)
        },
        "statistics": {
            "by_type": {},
            "by_module": {},
            "by_priority": {"high": 0, "medium": 0, "low": 0},
            "ready_for_develop": ready_count,
            "needs_clarification": len(requirements) - ready_count,
            "grouping": {
                "enabled": enable_grouping,
                "threshold": similarity_threshold if enable_grouping else None,
                "grouped_requirements": grouped_count,
                "tickets_in_groups": total_tickets_in_groups,
                "compression_ratio": round(len(analyzed_tickets) / len(requirements), 2) if requirements else 1.0
            }
        },
        "requirements": requirements,
        "groupings": [
            {
                "requirement_id": r["requirement_id"],
                "tickets": [t["id"] for t in r.get("source_tickets", [{"id": r["ticket_id"]}])],
                "count": r.get("grouped_tickets_count", 1)
            }
            for r in requirements
        ]
    }

    # Calculate statistics
    for req in requirements:
        req_type = req["type"]
        registry["statistics"]["by_type"][req_type] = registry["statistics"]["by_type"].get(req_type, 0) + 1

        module = req["module"]
        registry["statistics"]["by_module"][module] = registry["statistics"]["by_module"].get(module, 0) + 1

        level = req["priority"]["level"]
        registry["statistics"]["by_priority"][level] = registry["statistics"]["by_priority"].get(level, 0) + 1

    return registry


def generate_spec(requirement: dict, specs_dir: Path) -> Path:
    """
    Generate a spec file for a ready requirement.

    The spec format is compatible with the /develop command and includes
    all information extracted by the ticket-deep-analyzer skill.
    """
    # Build entities section with fields if available
    entities_lines = []
    for e in requirement["scope"].get("entities", []):
        entity_line = f'- `{e["name"]}` ({e.get("role", "primary")})'
        if e.get("fields"):
            entity_line += f': {", ".join(e["fields"])}'
        entities_lines.append(entity_line)
    entities_section = chr(10).join(entities_lines) if entities_lines else "- Not identified"

    # Build modules section with confidence
    modules_lines = []
    for m in requirement["scope"].get("modules", []):
        if isinstance(m, dict):
            conf = m.get("confidence", "")
            conf_str = f' ({conf}% confidence)' if conf else ""
            modules_lines.append(f'- {m["name"]}{conf_str}')
        else:
            modules_lines.append(f'- {m}')
    modules_section = chr(10).join(modules_lines) if modules_lines else f'- {requirement["module"]}'

    # Build workflows section
    workflows = requirement["scope"].get("workflows", [])
    workflows_section = chr(10).join(f'- {w}' for w in workflows) if workflows else "- None identified"

    # Build business rules section with full details
    rules_lines = []
    for i, rule in enumerate(requirement.get("business_rules", []), 1):
        if isinstance(rule, dict):
            rule_line = f'{i}. **{rule.get("id", f"BR{i:03d}")}** ({rule.get("type", "validation")}): {rule.get("description", "")}'
            if rule.get("conditions"):
                rule_line += f'\n   - Conditions: {", ".join(rule["conditions"])}'
            if rule.get("expected_behavior"):
                rule_line += f'\n   - Expected: {rule["expected_behavior"]}'
            rules_lines.append(rule_line)
        else:
            rules_lines.append(f'{i}. {rule}')
    business_rules_section = chr(10).join(rules_lines) if rules_lines else "- None identified"

    # Build acceptance criteria section
    ac_lines = []
    for ac in requirement.get("acceptance_criteria", []):
        if isinstance(ac, dict):
            ac_type = f' [{ac.get("type", "functional")}]' if ac.get("type") else ""
            ac_lines.append(f'- [ ] {ac.get("description", "")}{ac_type}')
        else:
            ac_lines.append(f'- [ ] {ac}')
    acceptance_criteria_section = chr(10).join(ac_lines) if ac_lines else "- None identified"

    # Build bug analysis section if present
    bug_analysis_section = ""
    if requirement.get("bug_analysis"):
        ba = requirement["bug_analysis"]
        bug_analysis_section = f'''
## Bug Analysis

### Current Behavior
{ba.get("current_behavior", "Not specified")}

### Expected Behavior
{ba.get("expected_behavior", "Not specified")}

### Reproduction Steps
{chr(10).join(f'{i}. {step}' for i, step in enumerate(ba.get("reproduction_steps", []), 1)) if ba.get("reproduction_steps") else "- Not specified"}

### Affected Scenarios
{chr(10).join(f'- {s}' for s in ba.get("affected_scenarios", [])) if ba.get("affected_scenarios") else "- Not specified"}
'''

    # Build regression analysis section if present
    regression_section = ""
    if requirement.get("regression_analysis"):
        ra = requirement["regression_analysis"]
        most_likely = ra.get("most_likely_cause", {})
        suspects = ra.get("suspect_commits", [])
        contacts = ra.get("contacts", [])

        suspects_text = chr(10).join(
            f'- **{s.get("hash", "N/A")}** ({s.get("date", "N/A")}) by {s.get("author", "N/A")}: {s.get("message", "")} (confidence: {s.get("confidence", 0)}%)'
            for s in suspects[:5]
        ) if suspects else "- No suspect commits identified"

        contacts_text = chr(10).join(
            f'- {c.get("name", "N/A")} ({c.get("email", "N/A")}) - {c.get("role", "")}'
            for c in contacts
        ) if contacts else "- No contacts identified"

        regression_section = f'''
## Regression Analysis

### Most Likely Cause
- **Commit**: {most_likely.get("commit", "N/A")}
- **Confidence**: {most_likely.get("confidence", "N/A")}%
- **Evidence**:
{chr(10).join(f'  - {e}' for e in most_likely.get("evidence", [])) if most_likely.get("evidence") else "  - None"}
- **Recommendation**: {most_likely.get("recommendation", "N/A")}

### Suspect Commits
{suspects_text}

### Contacts
{contacts_text}
'''

    spec_content = f'''# Specification: {requirement["requirement_id"]} - {requirement["title"]}

## Metadata
- **Requirement ID**: {requirement["requirement_id"]}
- **Source Ticket**: #{requirement["ticket_id"]}
- **Tracker**: {requirement["tracker"]}
- **Module**: {requirement["module"]}
- **Type**: {requirement["type"]}
- **Priority Score**: {requirement["priority"]["score"]}
- **Quality Score**: {requirement.get("quality_score", "N/A")}
- **Status**: Ready for Development

## Summary
{requirement["description"]["summary"]}

## Problem Statement
{requirement["description"]["problem_statement"]}

## Technical Scope

### Modules
{modules_section}

### Entities
{entities_section}

### Impacted Workflows
{workflows_section}

## Business Rules
{business_rules_section}
{bug_analysis_section}{regression_section}
## Acceptance Criteria
{acceptance_criteria_section}

## Source Tickets
- #{requirement["ticket_id"]}

## Priority
- **Score**: {requirement["priority"]["score"]}
- **Level**: {requirement["priority"]["level"]}
'''

    spec_path = specs_dir / f'{requirement["requirement_id"]}.md'
    with open(spec_path, 'w') as f:
        f.write(spec_content)

    return spec_path


def analyze_tickets_parallel(tickets: list[Path], analysis_dir: Path, tracker: str,
                             aos_path: Optional[str], workers: int) -> tuple[list[dict], list[str]]:
    """
    Analyze tickets in parallel using ThreadPoolExecutor.
    Returns (analyzed_list, failed_list).
    """
    analyzed = []
    failed = []
    total = len(tickets)

    print(f"\n{'='*60}")
    print(f"PHASE 1: PARALLEL TICKET ANALYSIS ({workers} workers)")
    print(f"{'='*60}")

    # Reset progress counter
    global _progress_counter
    _progress_counter = {"analyzed": 0, "failed": 0, "skipped": 0}

    def process_ticket(args):
        """Worker function for parallel processing."""
        idx, ticket_path = args
        return (idx, ticket_path, analyze_single_ticket(ticket_path, analysis_dir, tracker, aos_path))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit all tickets
        futures = {executor.submit(process_ticket, (i, t)): t for i, t in enumerate(tickets, 1)}

        completed = 0
        for future in as_completed(futures):
            completed += 1
            try:
                idx, ticket_path, result = future.result()
                if result:
                    analyzed.append(result)
                else:
                    failed.append(ticket_path.name)
            except Exception as e:
                ticket_path = futures[future]
                print(f"  [EXCEPTION] {ticket_path.name}: {str(e)}")
                failed.append(ticket_path.name)

            # Progress update every 10 tickets
            if completed % 10 == 0:
                with _progress_lock:
                    print(f"\n--- PROGRESS: {completed}/{total} | "
                          f"analyzed: {_progress_counter['analyzed']} | "
                          f"skipped: {_progress_counter['skipped']} | "
                          f"failed: {_progress_counter['failed']} ---\n")

    return analyzed, failed


def analyze_tickets_sequential(tickets: list[Path], analysis_dir: Path, tracker: str,
                               aos_path: Optional[str]) -> tuple[list[dict], list[str]]:
    """
    Analyze tickets sequentially (original behavior).
    Returns (analyzed_list, failed_list).
    """
    analyzed = []
    failed = []
    total = len(tickets)

    print(f"\n{'='*60}")
    print(f"PHASE 1: SEQUENTIAL TICKET ANALYSIS")
    print(f"{'='*60}")

    for i, ticket_path in enumerate(tickets, 1):
        print(f"\n[{i}/{total}] Processing {ticket_path.name}")
        result = analyze_single_ticket(ticket_path, analysis_dir, tracker, aos_path)

        if result:
            analyzed.append(result)
        else:
            failed.append(ticket_path.name)

        # Progress checkpoint every 10 tickets
        if i % 10 == 0:
            print(f"\n--- CHECKPOINT: {i}/{total} processed, {len(analyzed)} success, {len(failed)} failed ---\n")

    return analyzed, failed


def main():
    parser = argparse.ArgumentParser(
        description="Orchestrate Redmine ticket analysis (v2.0 - Optimized)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (sequential, no AOS enrichment)
  python orchestrate_ticket_analysis.py --scrap-dir ./Scrap/Anomaly --output-dir ./output

  # Parallel with 4 workers
  python orchestrate_ticket_analysis.py --scrap-dir ./Scrap/Anomaly --output-dir ./output --workers 4

  # With AOS enrichment (parallel, 6 workers)
  python orchestrate_ticket_analysis.py --scrap-dir ./Scrap/Anomaly --output-dir ./output \\
      --aos-path /path/to/axelor-open-suite --workers 6

  # With similarity grouping (reduces 1705 tickets to ~400 requirements)
  python orchestrate_ticket_analysis.py --scrap-dir ./Scrap/Anomaly --output-dir ./output \\
      --workers 6 --group-similar --similarity-threshold 70

  # Full optimization: parallel + AOS enrichment + grouping
  python orchestrate_ticket_analysis.py --scrap-dir ./Scrap/Anomaly --output-dir ./output \\
      --aos-path /path/to/axelor-open-suite --workers 6 --group-similar

  # Test with limit
  python orchestrate_ticket_analysis.py --scrap-dir ./Scrap/Anomaly --output-dir ./output --limit 10 --workers 4
        """
    )
    parser.add_argument("--scrap-dir", required=True, help="Directory containing scraped tickets")
    parser.add_argument("--output-dir", required=True, help="Output directory for results")
    parser.add_argument("--tracker", default="Anomaly", help="Tracker type (default: Anomaly)")
    parser.add_argument("--limit", type=int, help="Limit number of tickets to process (for testing)")
    parser.add_argument("--skip-analysis", action="store_true", help="Skip analysis, only build registry from existing")
    parser.add_argument("--aos-path", help="Path to AOS codebase for entity validation enrichment")
    parser.add_argument("--workers", type=int, default=1,
                        help="Number of parallel workers (default: 1 = sequential). Recommended: 4-8")
    parser.add_argument("--group-similar", action="store_true",
                        help="Enable grouping of similar tickets into single requirements")
    parser.add_argument("--similarity-threshold", type=float, default=70.0,
                        help="Similarity threshold for grouping (0-100, default: 70)")
    args = parser.parse_args()

    scrap_dir = Path(args.scrap_dir)
    output_dir = Path(args.output_dir)
    tracker = args.tracker
    aos_path = args.aos_path
    workers = args.workers

    # Validate input
    if not scrap_dir.exists():
        print(f"ERROR: Scrap directory not found: {scrap_dir}")
        sys.exit(1)

    if aos_path and not Path(aos_path).exists():
        print(f"ERROR: AOS path not found: {aos_path}")
        sys.exit(1)

    # Info about mode
    enable_grouping = args.group_similar
    similarity_threshold = args.similarity_threshold

    print(f"\n{'='*60}")
    print(f"TICKET ANALYSIS ORCHESTRATOR v2.1 (Optimized)")
    print(f"{'='*60}")
    print(f"Mode: Claude CLI subprocess")
    print(f"Workers: {workers} ({'parallel' if workers > 1 else 'sequential'})")
    print(f"AOS Enrichment: {'enabled (' + aos_path + ')' if aos_path else 'disabled'}")
    print(f"Grouping: {'enabled (threshold: ' + str(similarity_threshold) + '%)' if enable_grouping else 'disabled'}")
    print(f"{'='*60}")

    # Create output directories
    analysis_dir = output_dir / "analysis"
    specs_dir = output_dir / "specs" / tracker
    index_dir = output_dir / "index"

    analysis_dir.mkdir(parents=True, exist_ok=True)
    specs_dir.mkdir(parents=True, exist_ok=True)
    index_dir.mkdir(parents=True, exist_ok=True)

    # List tickets
    tickets = list_tickets(scrap_dir)
    if args.limit:
        tickets = tickets[:args.limit]
        print(f"Limited to {args.limit} tickets for testing")

    total = len(tickets)

    if not args.skip_analysis:
        # Phase 1: Analyze tickets
        start_time = datetime.now()

        if workers > 1:
            analyzed, failed = analyze_tickets_parallel(tickets, analysis_dir, tracker, aos_path, workers)
        else:
            analyzed, failed = analyze_tickets_sequential(tickets, analysis_dir, tracker, aos_path)

        end_time = datetime.now()
        duration = end_time - start_time

        print(f"\n{'='*60}")
        print(f"PHASE 1 COMPLETE")
        print(f"  Processed: {total}")
        print(f"  Success: {len(analyzed)}")
        print(f"  Failed: {len(failed)}")
        print(f"  Duration: {duration}")
        print(f"  Speed: {total / duration.total_seconds():.2f} tickets/second")
        print(f"{'='*60}")

        if failed:
            print(f"\nFailed tickets:")
            for f in failed:
                print(f"  - {f}")

    else:
        # Load existing analysis
        print("Loading existing analysis files...")
        analyzed = []
        for json_file in analysis_dir.glob("ticket-*.json"):
            try:
                with open(json_file, 'r') as f:
                    analyzed.append(json.load(f))
            except:
                pass
        print(f"Loaded {len(analyzed)} existing analyses")

    # Phase 2: Build registry
    print(f"\n{'='*60}")
    print(f"PHASE 2: BUILD REQUIREMENTS REGISTRY")
    print(f"{'='*60}")

    registry = build_registry(analyzed, output_dir, tracker, enable_grouping, similarity_threshold)

    registry_path = output_dir / "requirements-registry.json"
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    print(f"Registry saved to: {registry_path}")
    print(f"  Requirements: {len(registry['requirements'])}")
    print(f"  Ready for develop: {registry['statistics']['ready_for_develop']}")

    # Phase 3: Generate specs
    print(f"\n{'='*60}")
    print(f"PHASE 3: GENERATE SPECS")
    print(f"{'='*60}")

    specs_generated = 0
    for req in registry["requirements"]:
        if req["ready_for_develop"]:
            generate_spec(req, specs_dir)
            specs_generated += 1

    print(f"Generated {specs_generated} specs in {specs_dir}")

    # Phase 4: Generate indexes
    print(f"\n{'='*60}")
    print(f"PHASE 4: GENERATE INDEXES")
    print(f"{'='*60}")

    by_module = {}
    by_entity = {}
    by_tracker_idx = {tracker: []}

    for req in registry["requirements"]:
        # By module
        module = req["module"]
        if module not in by_module:
            by_module[module] = []
        by_module[module].append(req["requirement_id"])

        # By entity
        for entity in req["scope"]["entities"]:
            ent_name = entity["name"]
            if ent_name not in by_entity:
                by_entity[ent_name] = []
            by_entity[ent_name].append(req["requirement_id"])

        # By tracker
        by_tracker_idx[tracker].append(req["requirement_id"])

    with open(index_dir / "by-module.json", 'w') as f:
        json.dump(by_module, f, indent=2)

    with open(index_dir / "by-entity.json", 'w') as f:
        json.dump(by_entity, f, indent=2)

    with open(index_dir / "by-tracker.json", 'w') as f:
        json.dump(by_tracker_idx, f, indent=2)

    print(f"Indexes saved to {index_dir}")

    # Final verification
    print(f"\n{'='*60}")
    print(f"VERIFICATION")
    print(f"{'='*60}")

    specs_count = len(list(specs_dir.glob("*.md")))
    ready_count = registry['statistics']['ready_for_develop']

    print(f"Tickets in source: {total}")
    print(f"Tickets analyzed: {len(analyzed)}")
    print(f"Requirements created: {len(registry['requirements'])}")
    print(f"Ready for develop: {ready_count}")
    print(f"Specs generated: {specs_count}")

    if len(analyzed) == total:
        print(f"\n[OK] 100% tickets processed")
    else:
        print(f"\n[WARNING] Only {len(analyzed)}/{total} tickets processed ({100*len(analyzed)/total:.1f}%)")

    if specs_count == ready_count:
        print(f"[OK] Specs match ready requirements")
    else:
        print(f"[WARNING] Specs ({specs_count}) != Ready ({ready_count})")

    print(f"\n{'='*60}")
    print(f"DONE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
