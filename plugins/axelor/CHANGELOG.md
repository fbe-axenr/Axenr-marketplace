# Changelog

All notable changes to the Axelor plugin will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [2.0.0] - 2026-01-09

### Added
- Explicit skills declaration in agents via `skills` field (12 agents)
- PreToolUse hooks for read-only agents (code-reviewer, spec-inspector, functional-validator, aos-analyzer, business-analyst)
- `context: fork` for multi-phase commands (analyze-requirements, develop)
- `user-invocable: false` for 17 internal skills
- Claude Code v2.1.0+ compatibility

### Changed
- Removed explicit `model: sonnet` from 16 agents to inherit user default model
- Only `architect` agent retains explicit `model: opus` for complex design tasks
- YAML format for `tools` field in all 17 agents
- YAML format for `allowed-tools` field in skills
- YAML format for `skills` field in cicd-agent
- Simplified bash permissions with wildcards (`Bash(git *)` instead of `Bash(git add:*)`)
- Renamed plugin from `axelor-dev-accelerator` to `axelor`
- Renamed all 17 agents with shorter names (removed `axelor-` prefix)
  - aos-analyzer, architect, business-analyst, cicd-agent, code-analyzer
  - code-reviewer, domain-agent, agile-agent, spec-inspector, functional-validator
  - git-agent, java-agent, redmine-agent, requirements-refiner, doc-synthesis-agent
  - test-agent, view-agent
- Added proactive descriptions to all agents for automatic invocation
- Added sentence case convention for title/help attributes in documentation
- Added rules to avoid title/help duplication between domains and views

### Fixed
- Documented bash `$()` syntax blocks in analyze-requirements.md as reference-only
- Removed conflicting MCP server configuration (enabledMcpjsonServers and disabledMcpjsonServers)

## [1.0.0] - 2024-12-01

### Added
- Initial release with 17 specialized agents
- 32 skills for validation, generation, and analysis
- 5 main commands: /develop, /analyze-requirements, /analyze-code, /git, /analyze-redmine-tickets
- Complete documentation for Axelor ERP 8.0 development
- XSD validation support for AOP 7.1, 7.4, 8.0, 8.1
- SessionStart hook for automatic Axelor repository detection
