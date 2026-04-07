---
agent: 'wiki-orchestrate'
description: "Run a full daily maintenance cycle — ingest pending, lint, fix, report"
---

Run the full daily maintenance workflow:

1. **Ingest**: Process any `status: pending` raw sources
2. **Lint**: Run a full quality audit across all wiki pages
3. **Auto-fix**: Fix safe issues (rebuild index, update scores, add missing timestamps)
4. **Stale review**: Check pages not verified in 90+ days
5. **Report**: Summarize everything that was done and what needs human attention

Be thorough but efficient. Skip sources that haven't changed (check source_hash).
