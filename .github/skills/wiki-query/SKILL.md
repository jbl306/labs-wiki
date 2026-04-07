---
name: wiki-query
description: Search the wiki and synthesize answers from existing pages.
allowed-tools:
  - read
  - grep
  - glob
---

# /wiki-query

Search the wiki and synthesize answers from compiled knowledge pages. Never hallucinate — if information isn't in the wiki, say so.

## Usage

```
/wiki-query What is positional encoding?
/wiki-query Compare attention mechanisms vs SSMs
/wiki-query What sources discuss transformer architecture?
```

## How It Works

1. **Read `wiki/index.md`** to get an overview of all available pages
2. **Identify relevant pages** based on the query:
   - Match against page titles, concepts, and tags in the index
   - Use `grep` to search page content if index matching is insufficient
3. **Read identified pages** — focus on the most relevant sections
4. **Synthesize an answer** from the page content:
   - Cite sources using `[[wikilinks]]` (e.g., "According to [[Positional Encoding]]...")
   - If multiple pages contribute, reference all of them
   - If information is incomplete, state what's known and what's missing
5. **Suggest follow-ups** if the query reveals gaps:
   - "No page exists for X — consider ingesting a source about it"
   - "The [[Page]] page was last verified 120 days ago — consider updating"

## Rules

- **Never hallucinate** — only answer from wiki content
- **Always cite** — use `[[wikilinks]]` to reference source pages
- **Report gaps** — if the wiki doesn't cover the topic, say so clearly
- **Check staleness** — warn if cited pages have `last_verified` > 90 days
- **Read `index.md` first** — it's the cheapest way to find relevant pages (saves tokens)
