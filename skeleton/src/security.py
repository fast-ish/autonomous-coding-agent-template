"""
Security Hooks
==============

Pre-tool-use hooks that validate bash commands using an allowlist.
"""

import os
import re
import shlex
from typing import Any

# Allowed commands - configurable via template
ALLOWED_COMMANDS: set[str] = {
{%- for cmd in values.allowedCommands %}
    "${{ cmd }}",
{%- endfor %}
}

# Commands requiring extra validation
COMMANDS_NEEDING_EXTRA_VALIDATION = {"pkill", "chmod", "rm"}


def extract_commands(command_string: str) -> list[str]:
    """
    Extract command names from a shell command string.

    Handles pipes, command chaining (&&, ||, ;), and subshells.
    """
    commands = []

    # Split on semicolons not inside quotes
    segments = re.split(r'(?<!["\'])\s*;\s*(?!["\'])', command_string)

    for segment in segments:
        segment = segment.strip()
        if not segment:
            continue

        try:
            tokens = shlex.split(segment)
        except ValueError:
            return []  # Malformed - fail safe

        if not tokens:
            continue

        expect_command = True

        for token in tokens:
            if token in ("|", "||", "&&", "&"):
                expect_command = True
                continue

            if token in ("if", "then", "else", "fi", "for", "while", "do", "done"):
                continue

            if token.startswith("-"):
                continue

            if "=" in token and not token.startswith("="):
                continue

            if expect_command:
                cmd = os.path.basename(token)
                commands.append(cmd)
                expect_command = False

    return commands


def validate_pkill_command(command_string: str) -> tuple[bool, str]:
    """Validate pkill - only allow killing dev processes."""
    allowed_processes = {"node", "npm", "npx", "python", "uvicorn", "gunicorn"}

    try:
        tokens = shlex.split(command_string)
    except ValueError:
        return False, "Could not parse pkill command"

    args = [t for t in tokens[1:] if not t.startswith("-")]
    if not args:
        return False, "pkill requires a process name"

    target = args[-1].split()[0] if " " in args[-1] else args[-1]

    if target in allowed_processes:
        return True, ""
    return False, f"pkill only allowed for: {allowed_processes}"


def validate_chmod_command(command_string: str) -> tuple[bool, str]:
    """Validate chmod - only allow +x for making files executable."""
    try:
        tokens = shlex.split(command_string)
    except ValueError:
        return False, "Could not parse chmod command"

    if not tokens or tokens[0] != "chmod":
        return False, "Not a chmod command"

    mode = None
    for token in tokens[1:]:
        if token.startswith("-"):
            return False, "chmod flags not allowed"
        elif mode is None:
            mode = token

    if mode is None:
        return False, "chmod requires a mode"

    if not re.match(r"^[ugoa]*\+x$", mode):
        return False, f"chmod only allowed with +x, got: {mode}"

    return True, ""


def validate_rm_command(command_string: str) -> tuple[bool, str]:
    """Validate rm - block recursive and force deletes."""
    try:
        tokens = shlex.split(command_string)
    except ValueError:
        return False, "Could not parse rm command"

    for token in tokens[1:]:
        if token.startswith("-") and ("r" in token or "f" in token):
            return False, "rm -r and rm -f are not allowed"

    return True, ""


async def bash_security_hook(
    input_data: dict[str, Any],
    tool_use_id: str | None = None,
    context: Any | None = None,
) -> dict[str, Any]:
    """
    Pre-tool-use hook that validates bash commands.

    Returns empty dict to allow, or {"decision": "block", "reason": "..."} to block.
    """
    if input_data.get("tool_name") != "Bash":
        return {}

    command = input_data.get("tool_input", {}).get("command", "")
    if not command:
        return {}

    commands = extract_commands(command)
    if not commands:
        return {
            "decision": "block",
            "reason": f"Could not parse command: {command}",
        }

    for cmd in commands:
        if cmd not in ALLOWED_COMMANDS:
            return {
                "decision": "block",
                "reason": f"Command '{cmd}' not in allowed list: {ALLOWED_COMMANDS}",
            }

        if cmd in COMMANDS_NEEDING_EXTRA_VALIDATION:
            if cmd == "pkill":
                allowed, reason = validate_pkill_command(command)
            elif cmd == "chmod":
                allowed, reason = validate_chmod_command(command)
            elif cmd == "rm":
                allowed, reason = validate_rm_command(command)
            else:
                allowed, reason = True, ""

            if not allowed:
                return {"decision": "block", "reason": reason}

    return {}
