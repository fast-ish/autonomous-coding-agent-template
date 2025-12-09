# Autonomous Coding Agent Template

Backstage template for creating autonomous coding agents using Claude SDK.

## Structure

```
/template.yaml          # Backstage scaffolder definition
/skeleton/              # Generated agent code
/docs/                  # Template documentation
```

## Key Files

- `template.yaml` - Template parameters and steps (scaffolder.backstage.io/v1beta3)
- `skeleton/` - Generated files:
  - `src/main.py` - Entry point with CLI
  - `src/agent.py` - Agent session loop
  - `src/client.py` - Claude SDK client configuration
  - `src/security.py` - Bash command allowlist and validation
  - `src/prompts.py` - Prompt loading utilities
  - `src/progress.py` - Progress tracking
  - `prompts/` - Agent prompt templates
  - `tests/` - Security tests

## Template Syntax

Uses Jinja2 via Backstage:
- Variables: `${{ values.name }}`, `${{ values.maxIterations }}`
- Conditionals: `{%- if values.enableBrowserTools %}...{%- endif %}`
- Loops: `{%- for cmd in values.allowedCommands %}...{%- endfor %}`

## Agent Architecture

### Two-Phase Pattern

1. **Initializer**: First session creates feature_list.json and project structure
2. **Coding Agent**: Subsequent sessions implement features from the list

### Security Layers

1. OS-level sandbox (container)
2. File permissions restricted to project directory
3. Bash command allowlist with validation hooks

### Progress Tracking

- `feature_list.json` - Source of truth for test status
- `claude-progress.txt` - Session notes and next steps
- Tests can only transition from `passes: false` to `passes: true`

## Template Parameters

### Component Info

| Parameter | Type | Description |
|-----------|------|-------------|
| name | string | Agent name (lowercase, alphanumeric with hyphens) |
| owner | string | Owning team from Backstage catalog |
| description | string | What the agent does |

### Runtime

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| pythonVersion | enum | 3.12 | Python version (3.13, 3.12, 3.11) |
| packageManager | enum | uv | Package manager (uv, poetry, pip) |

### Model & SDK

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| defaultModel | enum | claude-sonnet-4-5 | Claude model for agent tasks |
| maxTurns | integer | 100 | Max conversation turns per session (10-1000) |

### Tools & MCP Servers

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enableFileTools | boolean | true | Read, write, edit, glob, grep tools |
| enableBashTools | boolean | true | Command execution with allowlist |
| enableBrowserTools | boolean | false | Puppeteer MCP for web interaction |
| enableGitHubTools | boolean | false | GitHub MCP for PR/issue management |
| enableDatabaseTools | boolean | false | PostgreSQL MCP for database queries |

### Agent Behavior

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| agentPattern | enum | two-phase | Pattern: two-phase, single-session, multi-agent |
| progressTracking | enum | feature-list | Tracking: feature-list, git-commits, none |
| maxIterations | integer | 50 | Max iterations per session (1-200) |

### Security

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| sandboxMode | enum | container | Sandbox: container, none |
| allowedCommands | array | [ls, cat, grep, git, npm, node, python, pip] | Bash allowlist |

## Where Parameters Are Used

| Parameter | Files |
|-----------|-------|
| `name` | pyproject.toml, catalog-info.yaml, README.md, src/__init__.py |
| `pythonVersion` | pyproject.toml, .github/workflows/ci.yaml, README.md, docs/GETTING_STARTED.md |
| `packageManager` | Makefile |
| `defaultModel` | src/main.py, README.md |
| `maxTurns` | src/client.py |
| `maxIterations` | src/main.py, README.md |
| `enableFileTools` | src/client.py |
| `enableBashTools` | src/client.py |
| `enableBrowserTools` | src/client.py |
| `enableGitHubTools` | src/client.py |
| `enableDatabaseTools` | src/client.py |
| `sandboxMode` | src/client.py |
| `allowedCommands` | src/security.py, README.md |

## Conventions

- Entry point: `python -m src.main`
- Output: `./output/` or `--project-dir`
- Config: `.claude_settings.json` per project
- Dependencies: `pyproject.toml` with configurable package manager

## Don't

- Allow rm -rf or recursive deletes
- Skip sandbox in production
- Modify test definitions once created
- Allow arbitrary command execution
