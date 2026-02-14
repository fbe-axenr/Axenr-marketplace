---
description: Setup Axelor reference repositories (AOS, AOP, addons) in project .axelor/ directory based on version detection
argument-hint: [project-path] [--force] [--dry-run]
exit-plan-mode: true
---

# Setup Command

Use the **repo-setup-agent** subagent to setup Axelor reference repositories autonomously.

## Arguments

- `project-path`: Path to Axelor webapp (default: current directory)
- `--force`: Re-clone existing repositories
- `--dry-run`: Show plan only, do not clone

## Execution

**CRITICAL**: Use the Task tool with `subagent_type="axelor:repo-setup-agent"` immediately.

```
Task tool parameters:
- subagent_type: "axelor:repo-setup-agent"
- prompt: "Setup Axelor reference repositories. Arguments: $ARGUMENTS"
- description: "Setup Axelor repositories"
```

Pass the following context to the agent:
- `$ARGUMENTS`: All command arguments (project-path, --force, --dry-run)
- Working directory context

Do NOT use Explore agent. Do NOT use general-purpose agent. Do NOT enter plan mode.
Use ONLY `subagent_type="axelor:repo-setup-agent"`.

The agent autonomously handles (no user interaction):
1. Prerequisites verification (git installed)
2. Webapp detection
3. Version extraction from gradle.properties
4. Two-phase repository cloning (AOP/AOS then addons)
5. Gitignore update
6. Success reporting (or error with details)

## What Gets Cloned

| Repository | Source | Destination |
|------------|--------|-------------|
| axelor-open-platform | GitHub | .axelor/aop/ |
| axelor-open-suite | GitHub | .axelor/aos/ |
| axelor-utils | GitHub | .axelor/axelor-utils/ |
| axelor-message | GitHub | .axelor/axelor-message/ |
| axelor-studio | GitHub | .axelor/axelor-studio/ |

Note: Addons are only cloned if they exist as separate repos (detected from libs.gradle).
