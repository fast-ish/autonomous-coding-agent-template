# Autonomous Coding Agent

## Overview

This template creates an autonomous coding agent that can work on projects across multiple sessions using the Claude SDK.

## How It Works

### The Two-Phase Pattern

**Phase 1: Initialization**

The first session runs an "initializer" prompt that:
1. Reads the application specification
2. Creates `feature_list.json` with detailed test cases
3. Sets up project structure and `init.sh`
4. Optionally begins implementation

**Phase 2: Coding Sessions**

Subsequent sessions run a "coding" prompt that:
1. Orients to the current project state
2. Selects the highest-priority incomplete feature
3. Implements and tests the feature
4. Updates `feature_list.json` when tests pass
5. Commits progress and updates notes

### Progress Tracking

The `feature_list.json` file is the source of truth:

```json
[
  {
    "id": "auth-001",
    "name": "User can log in with email",
    "category": "functional",
    "priority": "high",
    "passes": false,
    "steps": ["Navigate to /login", "Enter credentials", "Click submit"],
    "expected": "User is redirected to dashboard"
  }
]
```

**Rules:**
- Tests can only change from `passes: false` to `passes: true`
- Never delete or modify test definitions
- Never reorder tests

## Security Model

### Three Layers of Protection

1. **OS Sandbox**: Container isolation for command execution
2. **File Permissions**: Restricted to project directory
3. **Command Allowlist**: Only approved bash commands can run

### Allowed Commands

Default allowlist includes safe development commands:
- File inspection: `ls`, `cat`, `grep`
- Version control: `git`
- Development: `npm`, `node`, `python`, `pip`

### Blocked Operations

- System commands (`shutdown`, `reboot`)
- Recursive deletes (`rm -rf`)
- Network tools (`curl`, `wget`) unless explicitly allowed
- Permission changes beyond `+x`

## Customization

### Adding New Tools

Edit `src/client.py` to add MCP servers or built-in tools.

### Modifying Security

Edit `src/security.py` to:
- Add commands to `ALLOWED_COMMANDS`
- Add validation for sensitive commands
- Customize blocking behavior

### Changing Prompts

Edit files in `prompts/`:
- `app_spec.txt` - Define what to build
- `initializer_prompt.md` - First session behavior
- `coding_prompt.md` - Continuation behavior

## Best Practices

1. **Start Small**: Begin with a simple app spec and iterate
2. **Review Output**: Check the agent's work regularly
3. **Commit Often**: The agent commits progress frequently
4. **Use Sandbox**: Always run with container sandbox in production
5. **Monitor Progress**: Watch `feature_list.json` for completion status
