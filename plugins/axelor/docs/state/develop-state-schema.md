# /develop State Management Schema

State management for the `/develop` command workflow.

## State File

Location: `.axelor-develop-state.json` in workspace root

### Schema

```json
{
  "command": "develop",
  "specification_file": "docs/detailed-specifications.md",
  "output_directory": "docs/development",
  "architecture_mode": "create",
  "architecture_file": null,
  "skip_tests": false,
  "auto_commit": false,
  "current_phase": 3,
  "phases_completed": [1, 2],
  "checkpoints": {
    "phase_1": "abc123",
    "phase_2": "def456"
  },
  "agent_ids": {
    "phase_1": { "id": "arch-abc123", "iteration": 0 },
    "phase_2": { "id": "domain-def456", "iteration": 0 },
    "phase_3": { "id": null, "iteration": 0 }
  },
  "feature_name": "inventory-management",
  "webapp_root": "/path/to/webapp",
  "webapp_name": "axelor-erp",
  "aop_version": "7.4",
  "aos_version": "8.2",
  "java_version": "11",
  "xsd_version": "7.4",
  "axelor_repos": {
    "axelor_repo": ".axelor",
    "detection_method": "local-axelor-dir",
    "paths": {
      "aop": ".axelor/aop",
      "aos": ".axelor/aos",
      "addons": {
        "message": ".axelor/axelor-message",
        "studio": ".axelor/axelor-studio",
        "utils": ".axelor/axelor-utils"
      }
    }
  },
  "started_at": "2025-01-21T10:30:00Z",
  "last_updated": "2025-01-21T11:45:00Z"
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `command` | string | Always "develop" |
| `specification_file` | string | Path to input specifications |
| `output_directory` | string | Directory for generated reports |
| `architecture_mode` | string | "create" or "extend" |
| `architecture_file` | string/null | Path if extending existing architecture |
| `skip_tests` | boolean | Whether to skip Phase 5 |
| `auto_commit` | boolean | Whether automatic commits are enabled |
| `current_phase` | number | Current phase (1-7) |
| `phases_completed` | array | List of completed phase numbers |
| `checkpoints` | object | Commit hashes per phase |
| `agent_ids` | object | Agent IDs and iteration counts per phase (for resumable subagents) |
| `feature_name` | string | Extracted from specifications |
| `webapp_root` | string | Path to webapp directory |
| `webapp_name` | string | Webapp name from gradle |
| `aop_version` | string | AOP version (major.minor) |
| `aos_version` | string | AOS version if present |
| `java_version` | string | Java version from gradle |
| `xsd_version` | string | XSD schema version |
| `axelor_repos` | object | Axelor repository paths (flat structure for .axelor/, nested for /opt/axelor/) |
| `started_at` | string | ISO timestamp of workflow start |
| `last_updated` | string | ISO timestamp of last update |

---

## Resumable Subagents (ITERATE Optimization)

When a user responds with ITERATE, the workflow uses smart resume to optimize token usage.

### Agent IDs Structure

```json
"agent_ids": {
  "phase_1": { "id": "arch-abc123", "iteration": 0 },
  "phase_2": { "id": "domain-def456", "iteration": 0 }
}
```

- `id`: The agentId returned by Task tool after subagent completion
- `iteration`: Counter tracking how many ITERATEs have occurred for this phase

### Smart Resume Logic

When user responds with **ITERATE**:

```
iteration = state.agent_ids[current_phase].iteration

If iteration == 0 AND agent_id exists:
    # First ITERATE: Use resume parameter (~87% token savings)
    Resume the agent using stored agentId
    Increment iteration to 1
    Update state file
Else:
    # Subsequent ITERATEs: Fresh spawn with full context (workaround for bug #10856)
    Spawn new agent with:
      - Current artifacts (architecture-plan.md, domains/*.xml, etc.)
      - User's ITERATE request
      - Summary of previous iterations
    Store new agentId, reset iteration to 0
```

### Why This Pattern?

Due to Claude Code bug [#10856](https://github.com/anthropics/claude-code/issues/10856), resumed agents don't accumulate context across multiple resumes. Each resume forks from the original checkpoint.

**Token savings:**
| Scenario | Without Resume | With Smart Resume | Savings |
|----------|----------------|-------------------|---------|
| 1st ITERATE | ~15K tokens | ~2K tokens | **-87%** |
| 2nd ITERATE | ~15K tokens | ~15K tokens | 0% (fresh spawn) |
| 3rd ITERATE | ~15K tokens | ~15K tokens | 0% (fresh spawn) |

### After Agent Completion

After each subagent completes (initial run or ITERATE):
1. Store the returned `agentId` in `state.agent_ids[phase].id`
2. Update `state.agent_ids[phase].iteration` accordingly
3. Write updated state to `.axelor-develop-state.json`

---

## Resume Capability

To resume at a specific phase:

```
/develop docs/spec.md docs/dev --resume-from-phase=3
```

The workflow will:
1. Load state from `.axelor-develop-state.json`
2. Verify checkpoints are intact
3. Resume from specified phase
4. Continue workflow normally

---

## Rollback

If needed, rollback to any checkpoint:

```bash
git reset --hard <checkpoint-commit-hash>
```

Checkpoint hashes are stored in the `checkpoints` field of the state file.

---

## Workflow Completion and Cleanup

After Phase 7 completes, the `/develop` command MUST:

1. **Delete the state file**:
   ```bash
   rm -f .axelor-develop-state.json
   ```

2. **Commit the deletion** (only if `--auto-commit` is enabled):
   ```bash
   git add .axelor-develop-state.json
   git commit -m "chore: clean up development state file"
   ```

3. **Inform the user** with summary of generated artifacts.

### Why cleanup is important:

- The state file is only needed during active development
- Keeping it after completion clutters the repository
- Each new feature should start with a clean state
- The state file contains workflow metadata that's no longer relevant once complete

---

## Context Passing Through Phases

Each agent receives the following context:

```
Context:
- specification_file: Path to specifications
- output_directory: Where to write outputs
- architecture_mode: "create" or "extend"
- architecture_file: Path if extending (null otherwise)
- skip_tests: true or false
- auto_commit: true or false (default: false)
- feature_name: Extracted from specifications
- state_file: .axelor-develop-state.json

Project Structure:
- webapp_root: Path to webapp root directory
- webapp_name: Webapp name from appName
- aop_version: AOP major.minor version (e.g., "7.4")
- aos_version: AOS version if present
- java_version: Java version from javaVersion
- xsd_version: XSD schema version (same as aop_version)

Axelor Repositories:
- axelor_repo: Base path to repo containing aop/, aos/, addons/
- detection_method: How paths were detected
- aop_path: Path to Axelor Open Platform
- aos_path: Path to Axelor Open Suite
- addons paths: Paths to addon modules
```

### Usage in Agents

- Agents use `webapp_root` as base path for file generation
- Domain files: `{webapp_root}/modules/{module}/src/main/resources/domains/`
- View files: `{webapp_root}/modules/{module}/src/main/resources/views/`
- Java files: `{webapp_root}/modules/{module}/src/main/java/`
