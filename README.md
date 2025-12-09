# Autonomous Coding Agent Template

> Golden path template for building autonomous coding agents with Claude SDK.

[![Backstage](https://img.shields.io/badge/Backstage-Template-blue)](https://backstage.io)
[![Claude SDK](https://img.shields.io/badge/Claude-SDK-orange)](https://github.com/anthropics/claude-code-sdk)

## What's Included

| Category | Components |
|----------|------------|
| **Core** | Agent harness, session management, progress tracking |
| **Security** | Bash allowlist, command validation, sandbox support |
| **Tools** | File operations, bash commands, browser automation |
| **Testing** | Security hook tests, pytest configuration |
| **Prompts** | Initializer and coding agent templates |

## Quick Start

1. Go to [Backstage Software Catalog](https://backstage.yourcompany.com/create)
2. Select "Autonomous Coding Agent"
3. Configure your agent capabilities
4. Submit and start building

## Template Options

### Component Info

| Parameter | Description |
|-----------|-------------|
| `name` | Unique agent name (lowercase, alphanumeric with hyphens) |
| `owner` | Owning team from Backstage catalog |
| `description` | What the agent does |

### Runtime

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `pythonVersion` | 3.13, 3.12, 3.11 | 3.12 | Python version for the agent |
| `packageManager` | uv, poetry, pip | uv | Package manager for dependencies |

### Model & SDK

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `defaultModel` | claude-sonnet-4-5, claude-opus-4-5, claude-haiku-3-5 | claude-sonnet-4-5 | Default Claude model for agent tasks |
| `maxTurns` | 10-1000 | 100 | Maximum conversation turns per session |

### Tools & MCP Servers

| Parameter | Default | Description |
|-----------|---------|-------------|
| `enableFileTools` | true | Read, write, edit, glob, grep tools |
| `enableBashTools` | true | Command execution with allowlist |
| `enableBrowserTools` | false | Puppeteer MCP for web interaction |
| `enableGitHubTools` | false | GitHub MCP for PR/issue management |
| `enableDatabaseTools` | false | PostgreSQL MCP for database queries |

### Agent Behavior

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `agentPattern` | two-phase, single-session, multi-agent | two-phase | How the agent manages long-running tasks |
| `progressTracking` | feature-list, git-commits, none | feature-list | How to track task completion |
| `maxIterations` | 1-200 | 50 | Maximum agent iterations per session |

### Security

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `sandboxMode` | container, none | container | OS-level sandbox for command execution |
| `allowedCommands` | array | ls, cat, grep, git, npm, node, python, pip | Commands the agent can execute |

## What Gets Created

```
{name}/
├── src/
│   ├── __init__.py
│   ├── main.py           # Entry point
│   ├── agent.py          # Session logic
│   ├── client.py         # Claude SDK setup
│   ├── security.py       # Command validation
│   ├── prompts.py        # Prompt loading
│   └── progress.py       # Progress tracking
├── prompts/
│   ├── app_spec.txt      # Application spec
│   ├── initializer_prompt.md
│   └── coding_prompt.md
├── tests/
│   ├── __init__.py
│   └── test_security.py
├── docs/
│   ├── GETTING_STARTED.md
│   ├── architecture.md
│   ├── SECURITY.md
│   ├── PATTERNS.md
│   ├── EXTENDING.md
│   └── TROUBLESHOOTING.md
├── .github/
│   ├── workflows/ci.yaml
│   └── dependabot.yml
├── catalog-info.yaml
├── pyproject.toml
├── Makefile
├── README.md
└── .gitignore
```

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](./docs/GETTING_STARTED.md) | First steps |
| [Architecture](./docs/ARCHITECTURE.md) | How it works |
| [Security](./docs/SECURITY.md) | Safety guardrails |

## Based On

This template is based on [Anthropic's autonomous-coding quickstart](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding).

## Support

- **Slack**: #platform-help
- **Office Hours**: Thursdays 2-3pm
