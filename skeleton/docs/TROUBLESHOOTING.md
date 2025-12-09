# Troubleshooting

## Common Issues

### API Key Not Set

**Error:**
```
Error: ANTHROPIC_API_KEY environment variable not set
```

**Solution:**
```bash
export ANTHROPIC_API_KEY='sk-ant-...'

# Or in .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

---

### Command Blocked

**Error:**
```
Command 'curl' not in allowed list
```

**Solution:**

1. Check if the command is necessary
2. Add to allowlist in `src/security.py`:

```python
ALLOWED_COMMANDS = {
    # ... existing
    "curl",  # Add if needed
}
```

3. Add validation if command is sensitive:

```python
COMMANDS_NEEDING_EXTRA_VALIDATION.add("curl")

def validate_curl_command(cmd: str) -> tuple[bool, str]:
    # Only allow specific URLs
    if "internal.company.com" not in cmd:
        return False, "Only internal URLs allowed"
    return True, ""
```

---

### Agent Stuck in Loop

**Symptoms:**
- Same actions repeated
- No progress on tests
- Iteration count increasing without results

**Solutions:**

1. **Check progress notes:**
```bash
cat ./my_project/claude-progress.txt
```

2. **Review feature_list.json:**
```bash
# Find failing tests
cat ./my_project/feature_list.json | jq '[.[] | select(.passes == false)]'
```

3. **Look for impossible tests:**
- Vague acceptance criteria
- Dependencies on unavailable services
- Contradictory requirements

4. **Reduce iterations and review:**
```bash
python -m src.main --project-dir ./my_project --max-iterations 3
```

---

### Tests Not Updating

**Symptoms:**
- Agent says feature works
- `passes` field stays `false`

**Causes:**

1. **Verification failed:**
   - Check browser automation output
   - Look for console errors
   - Verify UI matches expectations

2. **JSON parsing error:**
```bash
# Validate JSON
python -c "import json; json.load(open('./my_project/feature_list.json'))"
```

3. **Wrong test ID:**
   - Agent may be updating wrong test
   - Check IDs match

---

### Sandbox Errors

**Error:**
```
Sandbox: command not allowed in container
```

**Solutions:**

1. **Disable sandbox for development:**
```python
# In .claude_settings.json
{
    "sandbox": "none"
}
```

2. **Or add command to container allowlist**

> **Warning**: Never disable sandbox in production

---

### Out of Context

**Symptoms:**
- Agent forgets previous work
- Repeats completed tasks

**Solutions:**

1. **Check progress file exists:**
```bash
ls -la ./my_project/claude-progress.txt
```

2. **Verify git history:**
```bash
cd ./my_project && git log --oneline -20
```

3. **Ensure clean session end:**
   - Agent should commit before ending
   - Progress notes should be updated

---

### Browser Automation Fails

**Error:**
```
Puppeteer: Could not launch browser
```

**Solutions:**

1. **Install dependencies:**
```bash
npx playwright install
# or
npx puppeteer install
```

2. **Check Node.js:**
```bash
node --version  # Should be 18+
```

3. **Headless environment:**
```bash
# In CI/Docker, may need
export PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
export PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium
```

---

### Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'claude_code_sdk'
```

**Solution:**
```bash
# Activate venv
source .venv/bin/activate

# Install package
uv pip install -e ".[dev]"

# Or with pip
pip install claude-code-sdk
```

---

### Permission Denied

**Error:**
```
Permission denied: ./init.sh
```

**Solution:**
```bash
chmod +x ./my_project/init.sh
```

---

## Debugging

### Enable Verbose Output

```python
# In src/agent.py, add logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspect Tool Calls

```python
async for event in client.process_query(prompt):
    if event.type == "tool_use":
        print(f"Tool: {event.name}")
        print(f"Input: {json.dumps(event.input, indent=2)}")
```

### Test Security Hooks

```bash
pytest tests/test_security.py -v

# Test specific command
python -c "
from src.security import bash_security_hook
import asyncio

result = asyncio.run(bash_security_hook({
    'tool_name': 'Bash',
    'tool_input': {'command': 'your-command-here'}
}))
print(result)
"
```

### Check Project State

```bash
# Full state dump
echo "=== Progress ===" && cat ./my_project/claude-progress.txt
echo "=== Tests ===" && cat ./my_project/feature_list.json | jq '.[] | {id, passes}'
echo "=== Git ===" && cd ./my_project && git log --oneline -10
echo "=== Files ===" && ls -la ./my_project/
```

## Getting Help

1. **Check logs:**
   - `claude-progress.txt` for agent notes
   - Git history for changes
   - Console output for errors

2. **Reproduce minimally:**
   - Create small test case
   - Single feature test

3. **Contact support:**
   - Slack: #platform-help
   - Include: error message, project state, steps to reproduce
