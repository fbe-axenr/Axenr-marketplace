---
description: Modular Axelor development workflow from specifications to production-ready code with user validation gates and checkpoint commits
argument-hint: <spec-file> [output-dir] [--webapp=<path>] [--architecture-file=<path>] [--resume-from-phase=N] [--skip-tests] [--auto-commit]
context: fork
skills:
  - axelor-xml-validator
  - axelor-naming-checker
  - axelor-semantic-validator
  - axelor-view-extension-validator
  - axelor-java-style-validator
  - file-safety-checker
  - commitlint-validator
---

# Develop Command

Execute a 7-phase development workflow with user validation gates.

## Workflow Chain

Use the **architect** subagent, then the **domain-agent** subagent, then the **view-agent** subagent, then the **java-agent** subagent, then the **test-agent** subagent, then the **code-reviewer** subagent, and finally the **git-agent** subagent.

---

## Validation Gates (All Phases)

After each phase, present artifacts and ask user to choose:

| Response | Action |
|----------|--------|
| **APPROVE** | Proceed to next phase. If `--auto-commit`, create checkpoint commit. |
| **ITERATE** | Apply smart resume logic (see below), then re-present for validation. |
| **REJECT** | Abort entire workflow immediately. |
| **SKIP** | Skip validation, proceed. If `--auto-commit`, create checkpoint commit. |

---

## ITERATE Handling (Smart Resume)

When user responds with **ITERATE** and provides feedback:

Check `state.agent_ids[current_phase].iteration`:

**If iteration == 0 AND agent_id exists (First ITERATE):**

Resume the subagent using the stored agentId. Pass the user's ITERATE feedback as the prompt. This saves ~87% tokens compared to fresh spawn. After completion, increment iteration to 1 and store new agentId.

**If iteration > 0 (Subsequent ITERATEs):**

Spawn a fresh subagent with full context:
- Read current artifacts (architecture-plan.md, domains/*.xml, views/*.xml, etc.)
- Include user's ITERATE feedback
- Include summary of previous iterations from state file

After completion, reset iteration to 0 and store new agentId.

**After any ITERATE completion:**

Update state file with new agentId and iteration count. Present validation gate again.

Reference **@docs/state/develop-state-schema.md** for full state schema and bug workaround details.

---

## Checkpoint Commits

When `--auto-commit` is enabled and user responds APPROVE or SKIP:

Use the **git-agent** subagent to commit changes. Apply `file-safety-checker` skill before staging. Apply `commitlint-validator` skill for message format. Use strict conventional commit format with no emojis and no Co-Authored-By.

When `--auto-commit` is NOT enabled (default): Inform user to commit manually when ready.

---

## Phase 1: Architecture Design

Use the **architect** subagent to design technical architecture from the specification file.

Pass the specification file path as input. If `--architecture-file` is provided or an existing `architecture-plan.md` is found, instruct the agent to EXTEND the existing architecture instead of creating from scratch.

The agent writes output to `{output_directory}/architecture-plan.md` with domain models, views, services, controllers, and implementation roadmap.

After completion, store the returned agentId in `state.agent_ids.phase_1`. Present validation gate. If approved with `--auto-commit`, commit with message: `docs(<module>): design technical architecture for [feature-name]`

---

## Phase 1.5: Technical Architecture Synthesis

Use the **doc-synthesis-agent** subagent to generate an executive summary with Mermaid diagrams.

Pass `{output_directory}/architecture-plan.md` as input. The agent writes `{output_directory}/architecture-synthesis.md`.

This phase runs automatically after Phase 1 approval. No validation gate required.

---

## Phase 2: Domain Generation

Use the **domain-agent** subagent to generate domain XML files.

Pass `{output_directory}/architecture-plan.md` as input. The agent generates entities to `src/main/resources/domains/*.xml` with XSD validation, naming conventions, and semantic checks. The agent builds with Gradle and fixes errors until build succeeds.

After completion, store the returned agentId in `state.agent_ids.phase_2`. Present validation gate. If approved with `--auto-commit`, commit with message: `feat(domain): generate domain models for [feature-name]`

---

## Phase 3: View Generation

Use the **view-agent** subagent to generate view XML files.

Pass `{output_directory}/architecture-plan.md` and `src/main/resources/domains/*.xml` as input. The agent generates forms, grids, actions, menus, and dashboards to `src/main/resources/views/*.xml`. The agent validates with XSD and semantic checker, builds and fixes until success.

After completion, store the returned agentId in `state.agent_ids.phase_3`. Present validation gate. If approved with `--auto-commit`, commit with message: `feat(views): generate views and actions for [feature-name]`

---

## Phase 4: Java Code Generation

Use the **java-agent** subagent to generate services, repositories, and controllers.

Pass `{output_directory}/architecture-plan.md`, domains, and views as input. The agent uses `axelor-controller-method-extractor` skill to extract controller methods from views. The agent generates services, repositories, controllers, and Module.java bindings to `src/main/java/**/*.java`. The agent validates style and builds until compilation succeeds.

After completion, store the returned agentId in `state.agent_ids.phase_4`. Present validation gate. If approved with `--auto-commit`, commit with message: `feat(java): implement services and controllers for [feature-name]`

---

## Phase 5: Unit Test Generation

Skip this phase if `--skip-tests` flag is provided.

Use the **test-agent** subagent to generate unit tests targeting >80% coverage.

Pass `{output_directory}/architecture-plan.md` and service implementations as input. The agent sets up test configuration, generates Given-When-Then tests to `src/test/java/**/*Test.java`, runs tests and fixes until all pass. The agent writes test report to `{output_directory}/test-report.md`.

After completion, store the returned agentId in `state.agent_ids.phase_5`. Present validation gate. If approved with `--auto-commit`, commit with message: `test(<module>): add unit tests for [feature-name] services`

---

## Phase 6: Code Review

Use the **code-reviewer** subagent to perform comprehensive code review.

Pass all generated files from Phases 2-5 as input. The agent reviews domains, views, Java code, and tests for quality, security, and performance. The agent writes report to `{output_directory}/code-review-report.md` with issues categorized as CRITICAL/HIGH/MEDIUM/LOW.

After completion, store the returned agentId in `state.agent_ids.phase_6`. Present validation gate. No checkpoint commit for this phase.

---

## Phase 7: Final Commit

If `--auto-commit` is enabled:

Use the **git-agent** subagent to create final feature commit. The agent verifies all checkpoints are in place, creates commit with message `feat(<module>): implement [feature-name]`, then deletes `.axelor-develop-state.json` and commits cleanup.

If `--auto-commit` is NOT enabled: Inform user that development is complete and they should commit manually when ready.

---

## Workflow Completion

After Phase 7 completes:
1. Delete `.axelor-develop-state.json`
2. If `--auto-commit`, commit the deletion
3. Display summary of all generated artifacts

---

## Argument Parsing

When this command is invoked, parse `$ARGUMENTS` as follows:

1. Extract `$1` as specification-file (required), `$2` as output-directory (default: `docs/development`)
2. Parse flags: `--webapp`, `--architecture-file`, `--resume-from-phase`, `--skip-tests`, `--auto-commit`
3. Auto-detect webapp if `--webapp` not provided using `detect_webapp.py` script
4. Detect architecture mode: CREATE if no existing architecture, EXTEND if `--architecture-file` or existing file found
5. Use Axelor repo paths from environment variables set by SessionStart hook ($AXELOR_AOP_PATH, $AXELOR_AOS_PATH, $AXELOR_REPO)
6. Initialize state file `.axelor-develop-state.json` with `agent_ids` for each phase (id: null, iteration: 0)
7. If `--resume-from-phase` provided, load state and resume from that phase
8. Start workflow at Phase 1 (or resume phase)

After each subagent completes, store the returned agentId in `state.agent_ids[phase].id` for future ITERATE resume.

Pass to each agent: specification_file, output_directory, architecture_mode, skip_tests, auto_commit, feature_name, webapp_root, webapp_name, aop_version, aos_version, java_version, aop_path, aos_path, addons_paths.
