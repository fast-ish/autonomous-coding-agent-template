# ADR 003: Progress Tracking via Feature List

## Status

Accepted

## Context

Autonomous agents working across sessions need:
- Persistent state for continuation
- Clear progress measurement
- Verification of completion
- Audit trail of changes

Options considered:
- Database tracking
- Git history analysis
- Custom state files
- Test suite as state

## Decision

Use `feature_list.json` as the single source of truth for progress:

### Structure
```json
[
  {
    "id": "unique-id",
    "name": "Human-readable name",
    "category": "functional|styling|accessibility",
    "priority": "high|medium|low",
    "passes": false,
    "steps": ["Step 1", "Step 2"],
    "expected": "Expected outcome"
  }
]
```

### Immutability Rules
- Tests are created once (initializer phase)
- Only `passes` field changes (false → true)
- Never delete tests
- Never modify test definitions
- Never reorder tests

### Progress Calculation
```python
passing = sum(1 for t in tests if t["passes"])
total = len(tests)
percentage = passing / total * 100
```

## Consequences

### Positive
- Simple to understand and implement
- Human-readable format
- Git-friendly (easy diffs)
- Works offline (no database)
- Self-documenting progress

### Negative
- Manual JSON editing possible (risk)
- No history of when tests passed
- Limited metadata per test
- File can grow large

### Mitigations
- Agent trained to never edit definitions
- Git history provides when-passed info
- Keep tests focused and numerous
- Use IDs for programmatic access

## Implementation

### Counting Progress
```python
def count_passing_tests(project_dir: Path) -> tuple[int, int]:
    tests_file = project_dir / "feature_list.json"
    tests = json.load(tests_file.open())
    passing = sum(1 for t in tests if t.get("passes", False))
    return passing, len(tests)
```

### Updating Status
```python
# Agent updates via file edit
# Only valid change:
{"passes": false} → {"passes": true}
```

## References

- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)
- [JSON Schema for validation](https://json-schema.org/)
