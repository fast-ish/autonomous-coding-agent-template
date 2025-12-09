# Getting Started

## Prerequisites

- Python ${{ values.pythonVersion }}+
- [uv](https://github.com/astral-sh/uv) package manager
- Anthropic API key

## Setup

### 1. Clone and Install

```bash
git clone https://github.com/fast-ish/${{ values.name }}.git
cd ${{ values.name }}

# Create virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e ".[dev]"
```

### 2. Configure API Key

```bash
# Get your key from https://console.anthropic.com/
export ANTHROPIC_API_KEY='sk-ant-...'

# Or add to .env file
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### 3. Define Your Application

Edit `prompts/app_spec.txt` to describe what you want the agent to build:

```
# Application Specification

## Overview
A todo list web application with user authentication.

## Requirements
1. Users can register and log in
2. Users can create, edit, and delete todos
3. Todos have title, description, due date, and status

## Technology Stack
- Frontend: React with TypeScript
- Backend: Node.js with Express
- Database: SQLite
```

### 4. Run the Agent

```bash
# Start a new project
python -m src.main --project-dir ./my_todo_app

# The agent will:
# 1. Read app_spec.txt
# 2. Create feature_list.json with test cases
# 3. Set up project structure
# 4. Begin implementing features
```

### 5. Monitor Progress

```bash
# Check test status
cat ./my_todo_app/feature_list.json | jq '[.[] | select(.passes == true)] | length'

# View progress notes
cat ./my_todo_app/claude-progress.txt

# View git history
cd ./my_todo_app && git log --oneline
```

## Common Workflows

### Continue an Existing Project

```bash
python -m src.main --project-dir ./my_todo_app
```

The agent will:
1. Read existing `feature_list.json`
2. Check which tests are still failing
3. Continue implementing from where it left off

### Limit Session Length

```bash
# Run for max 5 iterations
python -m src.main --project-dir ./my_todo_app --max-iterations 5
```

### Use a Different Model

```bash
python -m src.main --project-dir ./my_todo_app --model claude-sonnet-4-5-20250929
```

## Troubleshooting

### "ANTHROPIC_API_KEY not set"

```bash
export ANTHROPIC_API_KEY='your-key-here'
```

### "Command not in allowed list"

Edit `src/security.py` to add the command to `ALLOWED_COMMANDS`.

### Agent Stuck in Loop

1. Check `claude-progress.txt` for issues
2. Review `feature_list.json` for impossible tests
3. Reduce `--max-iterations` and review output

## Next Steps

- Read [Architecture](./architecture.md) to understand how it works
- Read [Security](./SECURITY.md) for safety configuration
- Customize prompts in `prompts/` directory
