"""
Agent Session Logic
===================

Core agent execution and session management.
"""

import asyncio
from pathlib import Path

from claude_code_sdk import ClaudeCodeClient

from .client import create_client
from .prompts import copy_spec_to_project, get_coding_prompt, get_initializer_prompt
from .progress import count_passing_tests, print_progress_summary, print_session_header


async def run_agent_session(
    client: ClaudeCodeClient,
    prompt: str,
) -> None:
    """
    Run a single agent session.

    Args:
        client: Configured Claude Code client
        prompt: The prompt to send to the agent
    """
    print(f"\nSending prompt ({len(prompt)} chars)...")
    print("-" * 50)

    async for event in client.process_query(prompt):
        if event.type == "text":
            print(event.text, end="", flush=True)
        elif event.type == "tool_use":
            tool_name = event.name
            print(f"\n[Tool: {tool_name}]")
        elif event.type == "tool_result":
            # Brief confirmation
            result_preview = str(event.result)[:100]
            if len(str(event.result)) > 100:
                result_preview += "..."
            print(f"  -> {result_preview}")
        elif event.type == "error":
            print(f"\n[Error: {event.error}]")

    print("\n" + "-" * 50)


async def run_autonomous_agent(
    project_dir: Path,
    model: str,
    max_iterations: int | None = None,
) -> None:
    """
    Run the autonomous agent loop.

    Args:
        project_dir: Directory for the project
        model: Claude model to use
        max_iterations: Maximum iterations (None for unlimited)
    """
    # Create project directory
    project_dir = Path(project_dir).resolve()
    project_dir.mkdir(parents=True, exist_ok=True)

    # Check if this is a continuation
    feature_list = project_dir / "feature_list.json"
    is_continuation = feature_list.exists()

    if is_continuation:
        print(f"\nContinuing existing project: {project_dir}")
        print_progress_summary(project_dir)
    else:
        print(f"\nStarting new project: {project_dir}")
        copy_spec_to_project(project_dir)

    # Create client
    client = create_client(project_dir, model)

    iteration = 0
    while max_iterations is None or iteration < max_iterations:
        iteration += 1

        # Determine prompt type
        if not is_continuation and iteration == 1:
            prompt = get_initializer_prompt()
            is_initializer = True
        else:
            prompt = get_coding_prompt()
            is_initializer = False

        print_session_header(iteration, is_initializer)

        # Run session
        await run_agent_session(client, prompt)

        # Show progress
        print_progress_summary(project_dir)

        # Check completion
        passing, total = count_passing_tests(project_dir)
        if total > 0 and passing == total:
            print("\n" + "=" * 70)
            print("  ALL TESTS PASSING - PROJECT COMPLETE!")
            print("=" * 70)
            break

        # Continue?
        if max_iterations is None or iteration < max_iterations:
            print("\nContinuing in 3 seconds... (Ctrl+C to stop)")
            await asyncio.sleep(3)
        is_continuation = True

    print("\n" + "=" * 70)
    print("  SESSION COMPLETE")
    print("=" * 70)
    print(f"\nProject directory: {project_dir}")
    print("\nTo continue later, run:")
    print(f"  python -m src.main --project-dir {project_dir}")
