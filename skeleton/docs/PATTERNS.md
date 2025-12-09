# Patterns

## Agent Patterns

### Two-Phase Development

Split work into initialization and implementation phases:

```
Phase 1 (Initializer):
- Analyze requirements
- Create test suite (feature_list.json)
- Set up project structure
- Establish baseline

Phase 2 (Coding Agent):
- Implement features one at a time
- Test thoroughly before marking complete
- Commit progress frequently
```

**Why**: Separating planning from execution ensures comprehensive test coverage and prevents scope drift.

### Test-Driven Progress

Use tests as the source of truth:

```json
{
  "id": "auth-001",
  "name": "User can log in",
  "passes": false,  // Only changes to true
  "steps": [...]
}
```

**Rules**:
- Tests are immutable once created
- Only `passes` field changes (false → true)
- Never delete or reorder tests

**Why**: Prevents goal drift and provides clear progress metrics.

### Session Continuity

Each session ends with documented state:

```
claude-progress.txt:
- What was accomplished
- Which tests now pass
- Issues discovered
- Suggested next steps
```

**Why**: Enables seamless continuation across context windows.

## Security Patterns

### Allowlist Over Blocklist

Define what's allowed, not what's blocked:

```python
# Good: Explicit allowlist
ALLOWED_COMMANDS = {"ls", "cat", "git", "npm"}

# Bad: Trying to block everything dangerous
BLOCKED_COMMANDS = {"rm -rf", "curl", ...}  # Always incomplete
```

**Why**: Allowlists fail closed (safe by default).

### Layered Defense

Multiple independent security layers:

```
Layer 1: OS Sandbox (container isolation)
Layer 2: File Permissions (directory restrictions)
Layer 3: Command Validation (allowlist + validators)
```

**Why**: Defense in depth - if one layer fails, others protect.

### Sensitive Command Validation

Extra validation for potentially dangerous commands:

```python
def validate_pkill(cmd):
    # Only allow killing dev processes
    allowed = {"node", "npm", "python"}
    return target in allowed
```

**Why**: Fine-grained control over risky operations.

## Prompt Patterns

### Structured Workflow

Give the agent a clear step-by-step process:

```markdown
## Workflow

### Step 1: Orient
Read project state...

### Step 2: Select
Choose one feature...

### Step 3: Implement
Write code...
```

**Why**: Reduces decision fatigue and ensures consistency.

### Explicit Constraints

State what NOT to do:

```markdown
**NEVER**:
- Delete tests
- Modify test definitions
- Skip verification
```

**Why**: Prevents common mistakes and drift.

### Progress Checkpoints

Require status updates:

```markdown
### Step 9: Update Progress Notes
Record:
- What was accomplished
- Which tests now pass
- Issues discovered
```

**Why**: Creates audit trail and context for next session.

## Code Patterns

### Async Event Processing

Stream agent responses for real-time output:

```python
async for event in client.process_query(prompt):
    if event.type == "text":
        print(event.text, end="", flush=True)
    elif event.type == "tool_use":
        print(f"[Tool: {event.name}]")
```

**Why**: Shows progress during long operations.

### Graceful Continuation

Handle interrupts and allow resumption:

```python
try:
    await run_agent(...)
except KeyboardInterrupt:
    print("To resume, run the same command again")
```

**Why**: Work isn't lost on interruption.

### Configuration via Template

Use Jinja2 for configurable security:

```python
ALLOWED_COMMANDS = {
{%- for cmd in values.allowedCommands %}
    "${{ cmd }}",
{%- endfor %}
}
```

**Why**: Security settings defined at project creation.

## Anti-Patterns

### Don't: Infinite Loops Without Limits

```python
# Bad
while True:
    run_session()

# Good
while iteration < max_iterations:
    run_session()
    iteration += 1
```

### Don't: Mutable Test Definitions

```python
# Bad: Allows editing tests
test["description"] = "new description"

# Good: Only status changes
test["passes"] = True
```

### Don't: Broad Command Allowlists

```python
# Bad: Too permissive
ALLOWED_COMMANDS = {"bash", "sh", "eval"}

# Good: Minimal necessary
ALLOWED_COMMANDS = {"ls", "git", "npm"}
```

### Don't: Skip Verification

```python
# Bad: Trust without verify
test["passes"] = True

# Good: Verify first
if browser_test_passes():
    test["passes"] = True
```
