# Troubleshooting: analyze-redmine-tickets

## Common Issues

### Issue: "REDMINE_API not found"

**Cause**: Missing or misconfigured `.env` file.

**Solution**: Create `.env` file with your Redmine API key:
```env
REDMINE_API=your_api_key_here
REDMINE_PROJECT_URL=https://redmine.axelor.com/projects/your-project
```

### Issue: "No specs generated"

**Cause**: All requirements have `ready_for_develop: false`.

**Solution**:
1. Check `requirements-registry.json` for `needs_clarification` count
2. Review tickets with low `quality_score` (< 70)
3. Tickets may lack sufficient information for development

### Issue: "Analysis too superficial"

**Cause**: Skill not reading full ticket content.

**Solution**:
1. Verify tickets have description AND notes (not just titles)
2. Check that `ticket-deep-analyzer` skill is properly invoked
3. Review individual `analysis/ticket-{ID}.json` files

### Issue: "Too many requirements"

**Cause**: Low similarity threshold causing over-splitting.

**Solution**:
1. Current implementation: 1 ticket = 1 requirement
2. Future: adjust `grouping_threshold` parameter (default: 70)

### Issue: "Agent sampling instead of processing all tickets"

**Cause**: Agent bypassing orchestrator or "optimizing".

**Solution**:
1. Always use `orchestrate_ticket_analysis.py` for bulk processing
2. Never call the agent directly for > 50 tickets
3. The orchestrator guarantees 100% processing

### Issue: "Timeout during analysis"

**Cause**: Ticket too large or complex for 180s timeout.

**Solution**:
1. Check ticket size (very long descriptions may timeout)
2. Retry failed tickets with `--limit 1` to isolate issues
3. Consider splitting very complex tickets

### Issue: "JSON parse error in output"

**Cause**: Malformed JSON in analysis output.

**Solution**:
1. Check `analysis/ticket-{ID}.json` for syntax errors
2. Delete corrupted file and re-run (orchestrator will retry)
3. Use `--skip-analysis` to rebuild registry from existing valid files

## Verification Commands

```bash
# Count tickets in source
ls -1 Scrap/Anomaly/*.md | wc -l

# Count successful analyses
ls -1 output/analysis/ticket-*.json | wc -l

# Count generated specs
ls -1 output/specs/Anomaly/*.md | wc -l

# Verify registry statistics
jq '.statistics' output/requirements-registry.json
```

## Re-running Failed Analyses

The orchestrator supports resumability. Simply re-run with the same parameters:

```bash
python scripts/orchestrate_ticket_analysis.py \
  --scrap-dir ./Scrap/Anomaly \
  --output-dir ./output \
  --tracker Anomaly
```

Already-analyzed tickets (with valid JSON) will be skipped.

## Rebuilding Registry Only

To rebuild registry from existing analyses without re-analyzing:

```bash
python scripts/orchestrate_ticket_analysis.py \
  --scrap-dir ./Scrap/Anomaly \
  --output-dir ./output \
  --tracker Anomaly \
  --skip-analysis
```
