# Architecture

## Overview

This autonomous coding agent uses a two-phase pattern to build applications across multiple sessions.

```
┌─────────────────────────────────────────────────────────────────┐
│                        Agent Harness                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐ │
│  │   main.py   │───▶│  agent.py   │───▶│     client.py       │ │
│  │  (CLI)      │    │  (Loop)     │    │  (Claude SDK)       │ │
│  └─────────────┘    └─────────────┘    └─────────────────────┘ │
│         │                  │                      │             │
│         │                  ▼                      ▼             │
│         │          ┌─────────────┐    ┌─────────────────────┐  │
│         │          │ progress.py │    │    security.py      │  │
│         │          │ (Tracking)  │    │  (Bash Allowlist)   │  │
│         │          └─────────────┘    └─────────────────────┘  │
│         │                                                       │
│         ▼                                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                      prompts/                            │   │
│  │  app_spec.txt │ initializer_prompt.md │ coding_prompt.md │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### main.py - Entry Point

- Parses CLI arguments
- Validates API key
- Launches the agent loop

### agent.py - Session Loop

- Determines if starting new project or continuing
- Selects appropriate prompt (initializer vs coding)
- Runs sessions until completion or max iterations
- Tracks progress between sessions

### client.py - Claude SDK Configuration

- Creates Claude Code client with configured tools
- Sets up MCP servers (Puppeteer for browser automation)
- Configures file permissions and sandbox
- Registers security hooks

### security.py - Command Validation

- Defines allowed bash commands
- Validates sensitive commands (pkill, chmod, rm)
- Blocks unauthorized operations
- Implements pre-tool-use hook

### progress.py - Progress Tracking

- Counts passing/failing tests from feature_list.json
- Prints session headers and progress summaries
- Tracks completion percentage

### prompts.py - Prompt Management

- Loads prompt templates from prompts/ directory
- Copies app spec to project directory

## Two-Phase Pattern

### Phase 1: Initialization

```
┌─────────────────┐
│   app_spec.txt  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────────┐
│  Initializer    │────▶│ feature_list.json│
│  Prompt         │     │ (50+ tests)      │
└─────────────────┘     └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Project Setup  │
│  - init.sh      │
│  - Git repo     │
│  - Structure    │
└─────────────────┘
```

### Phase 2: Coding Sessions

```
┌─────────────────┐     ┌─────────────────┐
│ feature_list.json│────▶│  Select Feature │
│ (source of truth)│     │  (highest prio) │
└─────────────────┘     └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   Implement     │
                        │   + Test        │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Update passes:  │
                        │ false → true    │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  Commit + Notes │
                        └─────────────────┘
```

## Security Model

### Defense in Depth

```
┌─────────────────────────────────────────────┐
│            Layer 1: OS Sandbox              │
│  ┌───────────────────────────────────────┐  │
│  │       Layer 2: File Permissions       │  │
│  │  ┌─────────────────────────────────┐  │  │
│  │  │   Layer 3: Command Allowlist    │  │  │
│  │  │  ┌───────────────────────────┐  │  │  │
│  │  │  │     Agent Execution       │  │  │  │
│  │  │  └───────────────────────────┘  │  │  │
│  │  └─────────────────────────────────┘  │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### Command Validation Flow

```
Bash Command
     │
     ▼
┌─────────────┐     ┌─────────────┐
│ Extract     │────▶│ In Allowed  │──No──▶ BLOCK
│ Commands    │     │ List?       │
└─────────────┘     └──────┬──────┘
                           │Yes
                           ▼
                   ┌─────────────┐
                   │ Needs Extra │──No──▶ ALLOW
                   │ Validation? │
                   └──────┬──────┘
                          │Yes
                          ▼
                   ┌─────────────┐
                   │ Validate    │
                   │ (pkill/chmod)│
                   └──────┬──────┘
                          │
                    ┌─────┴─────┐
                    │           │
                  Valid      Invalid
                    │           │
                    ▼           ▼
                  ALLOW       BLOCK
```

## Data Flow

### Session Data

```
Project Directory
├── app_spec.txt           # Input: What to build
├── feature_list.json      # State: Test definitions + status
├── claude-progress.txt    # State: Session notes
├── .claude_settings.json  # Config: Permissions
├── init.sh                # Generated: Setup script
└── [application files]    # Output: Built application
```

### Test Lifecycle

```
                    ┌─────────────┐
                    │   Created   │
                    │ passes:false│
                    └──────┬──────┘
                           │
                           │ Implementation
                           │ + Verification
                           │
                           ▼
                    ┌─────────────┐
                    │  Verified   │
                    │ passes:true │
                    └─────────────┘

Note: Tests NEVER go back to false or get deleted
```

## Extension Points

### Custom Tools

Add MCP servers in `client.py`:

```python
mcp_servers["my_tool"] = {
    "command": "npx",
    "args": ["-y", "@my-org/my-mcp-tool"],
}
```

### Custom Validation

Add command validators in `security.py`:

```python
COMMANDS_NEEDING_EXTRA_VALIDATION.add("my_cmd")

def validate_my_cmd(command_string: str) -> tuple[bool, str]:
    # Custom validation logic
    return True, ""
```

### Custom Prompts

Create new prompts in `prompts/` and load them in `prompts.py`.
