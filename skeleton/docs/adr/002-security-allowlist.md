# ADR 002: Bash Command Allowlist

## Status

Accepted

## Context

Autonomous agents executing bash commands pose security risks:
- System damage (rm -rf, shutdown)
- Data exfiltration (curl, wget)
- Privilege escalation (sudo, chmod)
- Sandbox escape (bash, sh)

We need to balance:
- Agent capability (needs to run commands)
- Security (prevent dangerous operations)
- Flexibility (different projects need different commands)

## Decision

Implement an allowlist-based security model with three layers:

### Layer 1: OS Sandbox
- Container isolation for command execution
- Prevents access to host system

### Layer 2: File Permissions
- Restrict operations to project directory
- Block parent and home directory access

### Layer 3: Command Allowlist
- Only explicitly permitted commands execute
- Sensitive commands have additional validation
- Unknown commands are blocked by default

### Allowlist Structure
```python
ALLOWED_COMMANDS = {"ls", "cat", "git", ...}
COMMANDS_NEEDING_EXTRA_VALIDATION = {"pkill", "chmod", "rm"}
```

### Validation Hooks
```python
async def bash_security_hook(input_data, ...):
    # Extract commands
    # Check against allowlist
    # Validate sensitive commands
    # Return block/allow decision
```

## Consequences

### Positive
- Fails closed (unknown = blocked)
- Configurable per project
- Extra validation for risky commands
- Defense in depth with three layers

### Negative
- May block legitimate commands
- Requires maintenance as needs evolve
- Validation logic can have bugs
- Performance overhead for command parsing

### Mitigations
- Template configures allowlist at creation
- Clear documentation for adding commands
- Comprehensive test suite for validation
- Logging of blocked commands for debugging

## Alternatives Considered

### Blocklist Approach
- Block known dangerous commands
- Problem: Can never block everything dangerous
- Rejected: Fails open is unacceptable

### No Restrictions
- Trust the agent completely
- Problem: Too risky for production
- Rejected: Security is non-negotiable

### Capability-Based
- Fine-grained permissions per operation
- Problem: Complex to configure correctly
- Rejected: Too complex for golden path

## References

- [OWASP Command Injection](https://owasp.org/www-community/attacks/Command_Injection)
- [Principle of Least Privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)
