# ADR 001: Two-Phase Agent Pattern

## Status

Accepted

## Context

Autonomous coding agents face challenges with long-running tasks:
- Context window limitations
- Goal drift over time
- Difficulty measuring progress
- Uncertainty about completion

We need a pattern that enables:
- Clear progress tracking
- Reliable continuation across sessions
- Measurable completion criteria
- Consistent output quality

## Decision

Implement a two-phase agent pattern:

### Phase 1: Initializer
- Reads application specification
- Creates comprehensive test suite (`feature_list.json`)
- Sets up project structure
- Establishes baseline for measurement

### Phase 2: Coding Agent
- Implements features from test suite
- Updates test status (false → true) on completion
- Commits progress and notes
- Continues until all tests pass

### Key Rules
- Tests are immutable once created
- Only `passes` field changes
- Never delete or reorder tests

## Consequences

### Positive
- Clear progress metrics (X/Y tests passing)
- Reliable continuation (test suite is persistent)
- Prevents goal drift (tests are source of truth)
- Easy to verify completion (all tests pass)

### Negative
- Requires upfront test design
- May miss emergent requirements
- Initial session takes longer
- Test quality affects overall outcome

### Mitigations
- Require minimum test count (50+)
- Include both functional and styling tests
- Document verification steps in each test
- Allow manual test additions between sessions

## References

- [Anthropic Long-Running Agents Guide](https://docs.anthropic.com/en/docs/agents/long-running-agents)
- [autonomous-coding quickstart](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)
