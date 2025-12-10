"""
Claude SDK Client Configuration
===============================

Configured client with security hooks and tool permissions.
"""

import json
import os
from pathlib import Path

from claude_code_sdk import ClaudeCodeClient, ClaudeCodeOptions

from .security import bash_security_hook

# System prompt for the agent
SYSTEM_PROMPT = """You are an expert full-stack developer working on an autonomous coding project.

Your capabilities:
- Read, write, and edit files
- Execute bash commands (within allowed list)
{%- if values.enableBrowserTools %}
- Browser automation via Puppeteer for testing
{%- endif %}

Guidelines:
1. Always read existing files before modifying them
2. Test your changes thoroughly
3. Commit progress frequently with descriptive messages
4. Update progress notes after each session
5. Focus on one feature at a time until complete
"""


def create_client(project_dir: Path, model: str) -> ClaudeCodeClient:
    """
    Create a configured Claude Code client.

    Args:
        project_dir: Working directory for the agent
        model: Claude model to use

    Returns:
        Configured ClaudeCodeClient
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY not set. Get your key from https://console.anthropic.com/"
        )

    # Configure tools
    tools = []
{%- if values.enableFileTools %}
    tools.extend(["Read", "Write", "Edit", "Glob", "Grep"])
{%- endif %}
{%- if values.enableBashTools %}
    tools.append("Bash")
{%- endif %}

    # Configure MCP servers
    mcp_servers = {}
{%- if values.enableBrowserTools %}
    mcp_servers["puppeteer"] = {
        "command": "npx",
        "args": ["-y", "@anthropic-ai/puppeteer-mcp"],
    }
{%- endif %}
{%- if values.enableGitHubTools %}
    mcp_servers["github"] = {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-github"],
    }
{%- endif %}
{%- if values.enableDatabaseTools %}
    mcp_servers["postgres"] = {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-postgres"],
    }
{%- endif %}

    # Write settings file
    settings = {
        "permissions": {
            "allow": ["./**"],
            "deny": ["../**", "~/**"],
        },
        "sandbox": "${{ values.sandboxMode }}",
    }
    settings_path = project_dir / ".claude_settings.json"
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)

    # Create options
    options = ClaudeCodeOptions(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        tools=tools,
        mcp_servers=mcp_servers if mcp_servers else None,
        max_turns=${{ values.maxTurns }},
        cwd=str(project_dir),
{%- if values.enableBashTools %}
        pre_tool_use_hook=bash_security_hook,
{%- endif %}
    )

    return ClaudeCodeClient(api_key=api_key, options=options)
