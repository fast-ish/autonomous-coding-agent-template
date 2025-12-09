#!/usr/bin/env python3
"""
${{ values.name }}
{{ '=' * (values.name | length) }}

${{ values.description }}

Usage:
    python -m src.main --project-dir ./my_project
    python -m src.main --project-dir ./my_project --max-iterations 10
"""

import argparse
import asyncio
import os
from pathlib import Path

from .agent import run_autonomous_agent

DEFAULT_MODEL = "${{ values.defaultModel }}"
DEFAULT_MAX_ITERATIONS = ${{ values.maxIterations }}


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="${{ values.description }}",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start fresh project
  python -m src.main --project-dir ./my_project

  # Limit iterations
  python -m src.main --project-dir ./my_project --max-iterations 10

  # Use a specific model
  python -m src.main --project-dir ./my_project --model claude-sonnet-4-5-20250929

Environment Variables:
  ANTHROPIC_API_KEY    Your Anthropic API key (required)
        """,
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path("./output"),
        help="Directory for the project output (default: ./output)",
    )

    parser.add_argument(
        "--max-iterations",
        type=int,
        default=DEFAULT_MAX_ITERATIONS,
        help=f"Maximum agent iterations (default: {DEFAULT_MAX_ITERATIONS})",
    )

    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )

    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable not set")
        print("\nGet your API key from: https://console.anthropic.com/")
        print("\nThen set it:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        return

    try:
        asyncio.run(
            run_autonomous_agent(
                project_dir=args.project_dir,
                model=args.model,
                max_iterations=args.max_iterations,
            )
        )
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        print("To resume, run the same command again")
    except Exception as e:
        print(f"\nFatal error: {e}")
        raise


if __name__ == "__main__":
    main()
