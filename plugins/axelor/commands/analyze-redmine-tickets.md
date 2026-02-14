---
description: Scrape and analyze Redmine tickets to produce a requirements registry ready for /develop command
argument-hint: <redmine-url> [output-directory]
skills:
  - redmine-ticket-parser
  - ticket-deep-analyzer
  - ticket-duplicate-detector
---

# Analyze Redmine Tickets Command

Transform Redmine tickets into a structured requirements registry for development agents.

## Usage

Supports two input modes:

### Mode 1: Project (multiple tickets)
```
/analyze-redmine-tickets <redmine_project_url> [output-directory]
```

### Mode 2: Single ticket
```
/analyze-redmine-tickets <redmine_ticket_url> [output-directory]
```

**Parameters:**
- `<url>` (required): Either:
  - Project URL: `https://redmine.axelor.com/projects/axerp`
  - Ticket URL: `https://redmine.axelor.com/issues/104267`
- `[output-directory]` (optional): Output directory (default: `./Analysis/Ticket`)

The script **auto-detects** the URL type based on `/projects/` or `/issues/` in the path.

## Prerequisites

Create `.env` file:
```env
REDMINE_API=your_api_key_here
```

## Execution

**CRITICAL**: Use the single pipeline script that handles EVERYTHING automatically:

### Project mode (all tickets from a project)
```bash
python scripts/analyze_all_tickets.py \
  --project-url "https://redmine.axelor.com/projects/axerp" \
  --output-dir "{output_directory}"
```

### Single ticket mode
```bash
python scripts/analyze_all_tickets.py \
  --ticket-url "https://redmine.axelor.com/issues/104267" \
  --output-dir "{output_directory}"
```

### Auto-detect mode (recommended)
```bash
python scripts/analyze_all_tickets.py \
  --url "{any_redmine_url}" \
  --output-dir "{output_directory}"
```

This script:
1. **Phase 1**: Scrapes tickets from Redmine (project or single ticket)
2. **Phase 2**: Analyzes ALL trackers automatically (no interruption)
3. Generates registry, specs, and indexes

### If scraping already done

```bash
python scripts/analyze_all_tickets.py \
  --output-dir "{output_directory}" \
  --skip-scraping
```

## Output Structure

```
{output_directory}/
├── Scrap/{Tracker}/*.md           # Scraped tickets
├── analysis/ticket-*.json         # Individual analyses
├── requirements-registry.json     # Requirements registry
├── specs/{Tracker}/REQ-XXX.md     # Generated specs
└── index/by-{module,entity,tracker}.json
```

## Rules

### MANDATORY
1. **Use `analyze_all_tickets.py`** - single script for full pipeline
2. **DO NOT iterate manually** - the script handles all trackers
3. **DO NOT interrupt** - let the script complete all trackers

### FORBIDDEN
1. NO manual tracker iteration by the agent
2. NO stopping after first tracker
3. NO asking user to run commands manually

## Command Arguments

**USER ARGUMENTS**: $ARGUMENTS

Parse arguments:
- `$1`: Redmine URL - project OR ticket (required)
- `$2`: Output directory (default: "./Analysis/Ticket")

Detect URL type and execute:
```bash
cd /path/to/axelor

# Auto-detect mode (works with both project and ticket URLs)
python scripts/analyze_all_tickets.py --url "$1" --output-dir "$2"
```

## Examples

```bash
# Analyze all tickets from a project
/analyze-redmine-tickets https://redmine.axelor.com/projects/axerp

# Analyze a single ticket
/analyze-redmine-tickets https://redmine.axelor.com/issues/104267

# With custom output directory
/analyze-redmine-tickets https://redmine.axelor.com/issues/104267 ./my-analysis
```

## Reference Documentation

- [requirements-registry-schema.json](../docs/requirements/requirements-registry-schema.json)
- [spec-template.md](../docs/templates/spec-template.md)
- [redmine-ticket-troubleshooting.md](../docs/analysis/redmine-ticket-troubleshooting.md)

## See Also

- [@scripts/analyze_all_tickets.py](../scripts/analyze_all_tickets.py) - Main pipeline script
- [@scripts/fetch_redmine_tickets.py](../scripts/fetch_redmine_tickets.py) - Ticket scraper (project + single modes)
- [@scripts/orchestrate_ticket_analysis.py](../scripts/orchestrate_ticket_analysis.py) - Per-tracker orchestrator
- [@skills/ticket-deep-analyzer](../skills/ticket-deep-analyzer/SKILL.md)

## Version

- **Version**: 2.4.0
- **Last updated**: 2025-11-24
- **Changes**: Added single ticket mode support with auto-detection
