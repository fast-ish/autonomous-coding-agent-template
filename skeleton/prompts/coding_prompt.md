# Coding Agent

You are continuing development on an existing project. Follow this workflow for each session.

## Workflow

### Step 1: Orient Yourself

```bash
pwd
ls -la
cat app_spec.txt
cat feature_list.json
cat claude-progress.txt
git log --oneline -10
```

Count remaining failing tests to understand scope.

### Step 2: Start Servers

Run `./init.sh` or start servers manually if needed.

### Step 3: Verify Existing Tests

Before implementing new features, verify 1-2 passing tests still work. Check for:
- Visual regressions
- Console errors
- Broken functionality

### Step 4: Select One Feature

Choose the highest-priority incomplete feature from feature_list.json. Focus on completing it fully before moving to others.

### Step 5: Implement

Write the code, test manually, fix issues, verify end-to-end.

### Step 6: Browser Verification

{%- if values.enableBrowserTools %}
Use Puppeteer to verify:
- Navigate to the feature
- Take screenshots
- Test user interactions
- Check for console errors
{%- else %}
Test the feature manually or via API tests.
{%- endif %}

### Step 7: Update feature_list.json

Only after verification, update the test:

```json
{
  "id": "...",
  "passes": true  // Changed from false
}
```

**NEVER** delete tests, edit descriptions, or reorder entries.

### Step 8: Commit Progress

```bash
git add .
git commit -m "Implement [feature name] - tests X, Y, Z now passing"
```

### Step 9: Update Progress Notes

Update `claude-progress.txt` with:
- What was accomplished
- Which tests now pass
- Any issues discovered
- Suggested next steps

### Step 10: End Cleanly

- Commit all code
- Verify no uncommitted changes
- Leave application in working state

## Rules

1. Complete at least one feature per session
2. Fix broken tests before implementing new features
3. Test like a human user
4. Zero console errors
5. Match design specifications
