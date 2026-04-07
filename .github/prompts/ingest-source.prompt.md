---
agent: 'wiki-capture'
description: "Capture a URL or text as a new raw source — auto-ingest processes it automatically"
---

Capture this as a new raw source in the wiki:

{{ input }}

Steps:
1. If it's a URL, fetch the content and extract the main article text
2. Create a properly formatted raw source file in `raw/`
3. Use today's date in the filename
4. Infer appropriate tags from the content
5. Report what was captured — auto-ingest will process it within ~5 seconds
