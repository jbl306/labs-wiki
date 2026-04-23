---
title: "Mobile-First Node Viewer For Wiki Graph UI"
type: concept
created: 2026-04-22
last_verified: 2026-04-22
source_hash: "0a4ff72c02c43a07f603a8baab32716ef2cb63b6d31b3dd941b64676f49cd7bd"
sources:
  - raw/2026-04-22-copilot-session-mobile-node-viewer-and-richer-github-ingestion-8b1dee20.md
quality_score: 59
concepts:
  - mobile-first-node-viewer-wiki-graph-ui
related:
  - "[[Mobile-First Graph UI Design for Wiki Systems]]"
  - "[[Mobile-Friendly Graph UI Tap Handling]]"
  - "[[Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion]]"
tier: hot
tags: [mobile-ui, wiki-graph, responsive-design, markdown-rendering]
---

# Mobile-First Node Viewer For Wiki Graph UI

## Overview

The mobile-first node viewer is a UI enhancement for the labs-wiki graph interface, allowing users to click on any node and view its wiki page content in a responsive, tabbed bottom-sheet layout. This design addresses usability and accessibility on mobile devices, providing a richer, more interactive experience for navigating wiki content.

## How It Works

The mobile node viewer is implemented as a bottom-sheet panel within the graph UI, triggered when a user selects a node. The panel is structured with tabs for Overview, Content, and Neighbors, enabling users to switch between summary information, full markdown-rendered content, and related nodes. 

The Content tab lazy-loads the wiki page content using a new API endpoint (`/graph/page-content/{node_id:path}`), which resolves the node's path, appends `.md`, and reads the file from the wiki directory. Frontmatter is parsed using PyYAML, with a fallback for missing dependencies. Markdown rendering is handled client-side by a zero-dependency renderer (~100 LOC), supporting headings, lists, code blocks, tables, blockquotes, and wikilinks. Wikilinks are clickable and resolve to other nodes by title or ID, enabling seamless navigation within the wiki graph.

Mobile-specific CSS rules extend the panel to a maximum height of 92dvh, with a drag handle for ergonomic interaction. Font sizes are increased for readability on screens ≤768px. The panel is initialized and managed via JavaScript, with tab logic, content loading, and event wiring handled in `app.js`. The UI is validated for asset presence (HTML structure, JS functions), but real-device QA is recommended for full verification.

The viewer is designed to be robust against path traversal attacks, guarding file access via `relative_to(WIKI_PATH.resolve())`. It supports lazy loading to optimize performance and avoid unnecessary data transfer on mobile networks. The tabbed layout and bottom-sheet paradigm are chosen for their familiarity and effectiveness in mobile UX.

Edge cases include handling private or empty repos (skip threshold of 200 chars), collision of node slugs (last write wins, but deduplication is recommended), and legacy source pages (multiple pages for the same repo). These are addressed via planned follow-up scripts and QA steps.

## Key Properties

- **Responsive Design:** Panel adapts to mobile screens, using bottom-sheet layout and larger font sizes for accessibility.
- **Tabbed Navigation:** Overview, Content, and Neighbors tabs allow users to switch between summary, full content, and related nodes.
- **Lazy Loading:** Content is loaded on demand via API calls, reducing initial load time and bandwidth usage.
- **Markdown Rendering:** Zero-dependency renderer supports headings, lists, code blocks, tables, blockquotes, and wikilinks.
- **Wikilink Navigation:** Clickable wikilinks resolve to other nodes by title or ID, enabling graph traversal.

## Limitations

Real-device QA is pending; only container asset inspection has been performed. Node slug collisions and legacy source page deduplication are not yet fully addressed. Private repos and empty content are skipped, which may result in missing pages.

## Example

A user clicks on the 'midudev/autoskills' node in the graph UI. The bottom-sheet panel opens, showing tabs for Overview, Content, and Neighbors. On the Content tab, the full markdown-rendered wiki page is displayed, including clickable wikilinks. The user taps a wikilink to 'hkuds-autoagent', and the panel updates to show that node's content.

## Visual

The UI consists of a bottom-sheet panel with tabs at the top, a drag handle, and a content area. On mobile, the panel covers up to 92% of the viewport height, with larger text and touch-friendly controls. The Content tab shows rendered markdown, including headings, lists, and wikilinks.

## Relationship to Other Concepts

- **[[Mobile-First Graph UI Design for Wiki Systems]]** — Builds upon the principles of mobile-first graph UI design, extending them to detailed node content viewing.
- **[[Mobile-Friendly Graph UI Tap Handling]]** — Shares ergonomic tap handling and responsive layout strategies.

## Practical Applications

Ideal for knowledge graph navigation on smartphones and tablets, enabling field researchers, students, or remote workers to access wiki content interactively. Useful for any wiki system where mobile access and rich content display are priorities.

## Sources

- [[Copilot Session Checkpoint: Mobile Node Viewer And Richer GitHub Ingestion]] — primary source for this concept
