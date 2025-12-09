# Security

## Overview

This agent implements defense-in-depth with three security layers to prevent unauthorized or dangerous operations.

## Security Layers

### Layer 1: OS Sandbox

The Claude SDK runs bash commands in an isolated container sandbox by default.

```python
# In .claude_settings.json
{
    "sandbox": "${{ values.sandboxMode }}"
}
```

Options:
- `container` (recommended): Full container isolation
- `none`: No sandbox (development only)

### Layer 2: File Permissions

File operations are restricted to the project directory:

```python
{
    "permissions": {
        "allow": ["./**"],      # Only project directory
        "deny": ["../**", "~/**"]  # Block parent and home
    }
}
```

### Layer 3: Command Allowlist

Only explicitly permitted bash commands can execute:

```python
ALLOWED_COMMANDS = {
{%- for cmd in values.allowedCommands %}
    "${{ cmd }}",
{%- endfor %}
}
```

## Command Validation

### Allowed Commands

Default allowlist includes safe development commands:

| Category | Commands |
|----------|----------|
| File Inspection | `ls`, `cat`, `grep`, `head`, `tail` |
| Version Control | `git` |
| Node.js | `npm`, `node`, `npx` |
| Python | `python`, `pip` |
| Process | `ps`, `pkill` (restricted) |
| File Ops | `mkdir`, `cp`, `chmod` (restricted) |

### Blocked Commands

These are always blocked:

| Category | Examples | Reason |
|----------|----------|--------|
| System | `shutdown`, `reboot` | System damage |
| Network | `curl`, `wget` | Data exfiltration |
| Recursive Delete | `rm -rf` | Data loss |
| Permissions | `chmod 777` | Security weakening |
| Shells | `bash`, `sh`, `zsh` | Sandbox escape |

### Sensitive Command Validation

Some allowed commands have additional validation:

#### pkill

Only allowed for development processes:

```python
allowed_processes = {"node", "npm", "npx", "python", "uvicorn", "gunicorn"}

# Allowed
pkill node
pkill -f "node server.js"

# Blocked
pkill nginx
pkill -9 postgres
```

#### chmod

Only `+x` (execute permission) is allowed:

```python
# Allowed
chmod +x script.sh
chmod u+x init.sh

# Blocked
chmod 777 file
chmod +w file
chmod -R +x dir
```

#### rm

Recursive and force flags are blocked:

```python
# Allowed
rm file.txt
rm temp.log

# Blocked
rm -r directory
rm -f file
rm -rf *
```

## Adding New Commands

### 1. Add to Allowlist

Edit `src/security.py`:

```python
ALLOWED_COMMANDS = {
    # ... existing commands
    "my_command",
}
```

### 2. Add Validation (if needed)

For sensitive commands, add a validator:

```python
COMMANDS_NEEDING_EXTRA_VALIDATION.add("my_command")

def validate_my_command(command_string: str) -> tuple[bool, str]:
    # Parse and validate
    try:
        tokens = shlex.split(command_string)
    except ValueError:
        return False, "Could not parse command"

    # Your validation logic
    if dangerous_pattern(tokens):
        return False, "Dangerous pattern detected"

    return True, ""
```

### 3. Register in Hook

```python
async def bash_security_hook(...):
    # ... existing code

    if cmd == "my_command":
        allowed, reason = validate_my_command(command)
        if not allowed:
            return {"decision": "block", "reason": reason}
```

## Security Best Practices

### Do

- Use container sandbox in production
- Keep allowlist minimal
- Review agent output regularly
- Commit progress frequently (creates audit trail)
- Use read-only file mounts where possible

### Don't

- Disable sandbox in production
- Add network commands without review
- Allow recursive operations
- Give write access outside project directory
- Skip command validation for "convenience"

## Incident Response

### If Agent Runs Unexpected Command

1. Check the command in logs
2. Review `security.py` to understand why it was allowed
3. Add to blocked list or tighten validation
4. Review generated files for damage

### If Agent Accesses Wrong Files

1. Check `.claude_settings.json` permissions
2. Review file permission configuration
3. Verify sandbox is enabled
4. Check for path traversal in commands

## Testing Security

Run the security test suite:

```bash
pytest tests/test_security.py -v
```

Test cases cover:
- Allowed command execution
- Blocked command rejection
- Sensitive command validation
- Command parsing edge cases
