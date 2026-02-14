Resolve the following ticket using the ticket-solver-agent workflow.

## ARGUMENTS

$ARGUMENTS

Expected format: `<project> <branch> #<number> | <title> | <description>`

Examples:
- `axenr-app wip #750 | Add estimated power field | decimal field on Opportunity, calculated from numberOfModules * 400 / 1000`
- `axenr-app dev #733 | Fix project start date | Use current date instead of null in ProjectService`
- `axenr-mobile axenr #801 | Add timesheet duration filter | Filter by duration on TimesheetListScreen`

## PARSING

Parse $ARGUMENTS to extract:
1. **project**: first word (axenr-app or axenr-mobile)
2. **branch**: second word (dev, wip, axenr, or other)
3. **ticket_number**: the #XXX part
4. **title**: text between first and second |
5. **description**: text after second |

If any required field is missing, ASK the developer. Do not guess.

## WORKFLOW

Execute the full ticket-solver-agent pipeline:

### PHASE 1 : GIT PULL
- If axenr-app: `git pull origin <branch>` in modules/axenr THEN in axenr-app
- If axenr-mobile: `git pull origin axenr`
- This is the ONLY git operation allowed. The developer handles everything else.

### PHASE 2 : PRE-FLIGHT
- Call pre-flight-checker skill to load context:
  - Read LESSONS-LEARNED.md from the marketplace
  - Read CLAUDE.md from the project
  - Read axelor-dev-guide.md if axenr-app
  - Read gradle.properties and libs.versions.toml if axenr-app
  - Read i18n files to know existing translation keys
  - Identify reusable code in the project

### PHASE 3 : ANALYSIS
- Determine change type: domain, view, java, mobile, or mix
- List files to create or modify
- Identify reusable code (services, components, entities, i18n keys)
- Verify AOS API compatibility with version from libs.versions.toml
- If information is missing from the ticket: ASK the developer

### PHASE 4 : GENERATION
- Use Axelor partner agents (domain-agent, view-agent, java-agent) for axenr-app
- Generate code directly for axenr-mobile
- Follow ALL rules from the project CLAUDE.md
- Reuse existing code whenever possible
- Check i18n files before creating translation keys
- Use XSD matching the AOP version

### PHASE 5 : VALIDATION
- Use Axelor partner validation agents for BOTH projects:
  - axelor-xml-validator, axelor-view-semantic-validator
  - axelor-java-style-validator, axelor-naming-checker
  - code-reviewer, code-analyzer
- Collect all issues by severity (CRITICAL/HIGH/MEDIUM/LOW)

### PHASE 6 : CORRECTION + LEARNING (max 3 retries)
- For each CRITICAL/HIGH issue:
  - Fix the code in the project
  - Call error-learner to record the lesson in LESSONS-LEARNED.md
  - Call knowledge-updater to auto-promote if 3+ occurrences
- Re-run PHASE 5
- If 3 retries exhausted with remaining CRITICAL: STOP with full error report

### PHASE 7 : BUILD
- axenr-app: `./gradlew clean generateCode copyWebapp build`
- axenr-mobile: `yarn build && yarn lint`
- If build fails: parse error, learn, fix, retry (shared counter with PHASE 6)

### PHASE 8 : DELIVERY
- Generate TEST PLAN
- List all modified files with full paths
- Summarize what was done (3-5 lines)
- Show reused vs created code
- Show version compatibility report
- Do NOT commit, push, or create branches

## CRITICAL RULES

- NEVER delete existing code
- NEVER rename existing elements
- NEVER modify code not requested by the ticket
- NEVER write comments in generated code
- NEVER create duplicate i18n keys
- NEVER use deprecated APIs
- NEVER guess missing information
- The generated code MUST be senior-level quality
- Write lessons in the marketplace ONLY, never in the project
