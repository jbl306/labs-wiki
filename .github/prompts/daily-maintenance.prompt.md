---
agent: 'wiki-orchestrate'
description: "Run a maintenance cycle — audit, lint, fix, gap analysis"
---

Run the wiki maintenance workflow:

1. **Lint**: Run a full quality audit across all wiki pages
2. **Auto-fix**: Fix safe issues (rebuild index, update scores, add missing timestamps)
3. **Stale review**: Check pages not verified in 90+ days
4. **Gap analysis**: Find missing concepts and synthesis opportunities
5. **Report**: Summarize everything that was done and what needs human attention

Note: Source ingestion is handled automatically by the `wiki-auto-ingest` service.
Be thorough but efficient. Skip sources that haven't changed (check source_hash).
