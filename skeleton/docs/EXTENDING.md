# Extending

## Adding Custom Tools

### MCP Servers

Add Model Context Protocol servers for new capabilities:

```python
# In src/client.py

mcp_servers = {}

# Browser automation
mcp_servers["puppeteer"] = {
    "command": "npx",
    "args": ["-y", "@anthropic-ai/puppeteer-mcp"],
}

# Database access
mcp_servers["postgres"] = {
    "command": "npx",
    "args": ["-y", "@my-org/postgres-mcp"],
    "env": {
        "DATABASE_URL": os.environ.get("DATABASE_URL"),
    },
}

# Custom tool
mcp_servers["my_tool"] = {
    "command": "python",
    "args": ["-m", "my_mcp_server"],
}
```

### Built-in Tools

Enable additional Claude Code tools:

```python
tools = [
    # File operations
    "Read", "Write", "Edit", "Glob", "Grep",
    # Command execution
    "Bash",
    # Web access (if needed)
    "WebFetch",
]
```

## Custom Commands

### Adding to Allowlist

```python
# In src/security.py

ALLOWED_COMMANDS = {
    # Existing
    "ls", "cat", "git",

    # Add new commands
    "docker",
    "kubectl",
    "terraform",
}
```

### Custom Validation

For commands needing extra checks:

```python
COMMANDS_NEEDING_EXTRA_VALIDATION.add("docker")

def validate_docker_command(command_string: str) -> tuple[bool, str]:
    """Only allow safe docker operations."""
    try:
        tokens = shlex.split(command_string)
    except ValueError:
        return False, "Could not parse docker command"

    if len(tokens) < 2:
        return False, "Docker requires a subcommand"

    subcommand = tokens[1]

    # Only allow safe subcommands
    allowed_subcommands = {"ps", "logs", "images", "build", "run"}
    if subcommand not in allowed_subcommands:
        return False, f"Docker subcommand '{subcommand}' not allowed"

    # Block dangerous flags
    dangerous_flags = {"--privileged", "--net=host", "-v /:/host"}
    for token in tokens:
        if token in dangerous_flags:
            return False, f"Docker flag '{token}' not allowed"

    return True, ""
```

## Custom Prompts

### New Prompt Types

Create specialized prompts for different phases:

```
prompts/
├── app_spec.txt
├── initializer_prompt.md
├── coding_prompt.md
├── review_prompt.md      # New: Code review phase
└── deploy_prompt.md      # New: Deployment phase
```

### Loading Custom Prompts

```python
# In src/prompts.py

def get_review_prompt() -> str:
    """Load the code review prompt."""
    return load_prompt("review_prompt")

def get_deploy_prompt() -> str:
    """Load the deployment prompt."""
    return load_prompt("deploy_prompt")
```

### Using in Agent Loop

```python
# In src/agent.py

async def run_autonomous_agent(...):
    # ... existing code

    # Add review phase
    if all_tests_pass and not reviewed:
        prompt = get_review_prompt()
        await run_agent_session(client, prompt)
        reviewed = True
```

## Custom Progress Tracking

### Additional Metrics

```python
# In src/progress.py

def count_by_category(project_dir: Path) -> dict[str, tuple[int, int]]:
    """Count passing tests by category."""
    tests_file = project_dir / "feature_list.json"

    if not tests_file.exists():
        return {}

    try:
        with open(tests_file) as f:
            tests = json.load(f)

        categories = {}
        for test in tests:
            cat = test.get("category", "uncategorized")
            if cat not in categories:
                categories[cat] = [0, 0]
            categories[cat][1] += 1  # Total
            if test.get("passes"):
                categories[cat][0] += 1  # Passing

        return {k: tuple(v) for k, v in categories.items()}
    except (json.JSONDecodeError, OSError):
        return {}
```

### Custom Progress Display

```python
def print_detailed_progress(project_dir: Path) -> None:
    """Print detailed progress by category."""
    by_category = count_by_category(project_dir)

    print("\nProgress by Category:")
    for category, (passing, total) in by_category.items():
        pct = (passing / total * 100) if total > 0 else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  {category:15} [{bar}] {passing}/{total}")
```

## Custom Session Logic

### Multiple Agents

Run different agents for different phases:

```python
async def run_multi_agent_pipeline(project_dir: Path, model: str):
    """Run a pipeline of specialized agents."""

    # Phase 1: Architecture
    arch_client = create_client(project_dir, model, tools=["Read", "Write"])
    await run_agent_session(arch_client, get_architecture_prompt())

    # Phase 2: Implementation
    impl_client = create_client(project_dir, model, tools=["Read", "Write", "Edit", "Bash"])
    while not all_tests_pass(project_dir):
        await run_agent_session(impl_client, get_coding_prompt())

    # Phase 3: Review
    review_client = create_client(project_dir, model, tools=["Read", "Grep"])
    await run_agent_session(review_client, get_review_prompt())
```

### Conditional Tool Access

Grant tools based on session type:

```python
def get_tools_for_phase(phase: str) -> list[str]:
    """Get allowed tools for each phase."""
    base_tools = ["Read", "Glob", "Grep"]

    phase_tools = {
        "planning": base_tools,
        "coding": base_tools + ["Write", "Edit", "Bash"],
        "testing": base_tools + ["Bash"],
        "review": base_tools,
    }

    return phase_tools.get(phase, base_tools)
```

## Integration Points

### Webhooks

Send notifications on progress:

```python
async def notify_progress(project_dir: Path, webhook_url: str):
    """Send progress update to webhook."""
    passing, total = count_passing_tests(project_dir)

    payload = {
        "project": str(project_dir),
        "passing": passing,
        "total": total,
        "percentage": (passing / total * 100) if total > 0 else 0,
    }

    async with aiohttp.ClientSession() as session:
        await session.post(webhook_url, json=payload)
```

### Database Logging

Store session history:

```python
async def log_session(db: Database, session_data: dict):
    """Log session to database."""
    await db.execute(
        """
        INSERT INTO sessions (project, iteration, tests_passing, tests_total, duration)
        VALUES ($1, $2, $3, $4, $5)
        """,
        session_data["project"],
        session_data["iteration"],
        session_data["passing"],
        session_data["total"],
        session_data["duration"],
    )
```
