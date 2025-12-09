# ${{ values.name }}

> ${{ values.description }}

## Quick Start

### Prerequisites

- Python ${{ values.pythonVersion }}+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Anthropic API key

### Setup

```bash
# Clone the repository
git clone https://github.com/fast-ish/${{ values.name }}.git
cd ${{ values.name }}

# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"

# Set your API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Running the Agent

```bash
# Start a new project
python -m src.main --project-dir ./my_project

# Continue an existing project
python -m src.main --project-dir ./my_project

# Limit iterations
python -m src.main --project-dir ./my_project --max-iterations 10
```

## Configuration

### Template Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--project-dir` | Working directory for the agent | `./output` |
| `--max-iterations` | Maximum agent iterations | ${{ values.maxIterations }} |
| `--model` | Claude model to use | `${{ values.defaultModel }}` |

### Security Settings

This agent uses an allowlist approach for bash commands:

**Allowed commands:**
{%- for cmd in values.allowedCommands %}
- `${{ cmd }}`
{%- endfor %}

Commands like `pkill`, `chmod`, and `rm` have additional validation rules.

### Customizing Prompts

Edit the files in `prompts/`:

- `app_spec.txt` - Application specification
- `initializer_prompt.md` - First session instructions
- `coding_prompt.md` - Continuation session instructions

## Development

```bash
# Run tests
pytest

# Run linting
ruff check src tests

# Run type checking
mypy src
```

## How It Works

1. **Initializer Session**: Creates `feature_list.json` with test cases and sets up the project
2. **Coding Sessions**: Implements features one at a time, updating tests as they pass
3. **Progress Tracking**: Uses `feature_list.json` as source of truth for completion

The agent runs autonomously until all tests pass or max iterations is reached.

## Support

- **Slack**: #platform-help
- **Docs**: [Internal Platform Docs](https://docs.yourcompany.com)
