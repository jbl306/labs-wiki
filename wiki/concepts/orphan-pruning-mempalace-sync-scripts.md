---
title: "Orphan Pruning in MemPalace Sync Scripts"
type: concept
created: 2026-04-20
last_verified: 2026-04-20
source_hash: "6d9e0eba162a694001ac48a61830fb7a5d3740b481f8691d5ba2c7bd6a7488d2"
sources:
  - raw/2026-04-20-copilot-session-wiki-audit-followups-92b1089b.md
quality_score: 59
concepts:
  - orphan-pruning-mempalace-sync-scripts
related:
  - "[[MemPalace Architecture and Migration]]"
  - "[[Migration from OpenMemory to MemPalace]]"
  - "[[Copilot Session Checkpoint: Wiki Audit Followups]]"
tier: hot
tags: [mempalace, memory-hygiene, orphan-pruning, wiki-sync, knowledge-management]
---

# Orphan Pruning in MemPalace Sync Scripts

## Overview

Orphan pruning is a process in MemPalace sync scripts that removes drawers (memory artifacts) associated with renamed or deleted wiki pages, ensuring that the memory system remains consistent with the current wiki state. This prevents accumulation of stale or irrelevant memories and maintains parity between the wiki and MemPalace.

## How It Works

MemPalace is a memory architecture used to store and retrieve knowledge artifacts linked to wiki pages. Previously, the sync script (`scripts/wiki_to_mempalace.py`) only upserted stable IDs for wiki pages, meaning that memories were added or updated as pages changed, but never deleted. This led to orphaned drawers—memory artifacts with no corresponding wiki page—especially when pages were renamed or deleted.

To address this, the sync script was enhanced to include orphan pruning. During each sync cycle, the script compares the set of current wiki pages with the set of drawers in MemPalace. Any drawer that does not have a matching wiki page is identified as an orphan and deleted from MemPalace. This ensures that the memory system accurately reflects the current state of the wiki, with no lingering artifacts from removed or renamed pages.

The process was validated by checking parity: after pruning, the number of wiki pages and injected docs matched exactly, with zero orphaned docs. This improvement is particularly important for long-running knowledge systems, where frequent page renames, deletions, or reorganizations can otherwise lead to memory bloat and retrieval errors.

Edge cases include rapid renaming or deletion cycles, where drawers may be temporarily orphaned before new pages are created. The script is designed to handle these cases gracefully, only pruning drawers that remain orphaned after a full sync cycle. Trade-offs involve the risk of accidental deletion if page renames are not properly tracked, but overall, the process improves system hygiene and retrieval accuracy.

## Key Properties

- **Parity Validation:** Ensures that the number of wiki pages and memory drawers matches, with zero orphaned docs after pruning.
- **Automated Orphan Detection:** Compares wiki page IDs to memory drawer IDs, deleting any without a match.
- **Consistent Memory Hygiene:** Maintains a clean, accurate memory system aligned with the current wiki structure.

## Limitations

If page renames are not properly tracked, drawers may be deleted prematurely. Rapid changes can lead to temporary orphaning, but the script only prunes after a full sync cycle. Accidental deletion is possible if the mapping logic is incorrect.

## Example

After deleting a wiki page 'nba-ml-training-status.md', the corresponding drawer in MemPalace remains. On the next sync, the script detects that the drawer is orphaned and deletes it:

```python
for drawer in mempalace_drawers:
    if drawer.id not in wiki_page_ids:
        delete_drawer(drawer)
```

## Relationship to Other Concepts

- **[[MemPalace Architecture and Migration]]** — Orphan pruning supports migration and maintenance of MemPalace memory artifacts.
- **[[Migration from OpenMemory to MemPalace]]** — Orphan pruning is critical during migration to prevent stale artifacts.

## Practical Applications

Used in labs-wiki and MemPalace to maintain accurate, clean memory systems, especially during page renames, deletions, or migrations. Prevents retrieval errors and memory bloat in long-running knowledge environments.

## Sources

- [[Copilot Session Checkpoint: Wiki Audit Followups]] — primary source for this concept
