---
title: "htmx Attribute API"
type: concept
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "241ccd0756ba8b32170ef8926eb8e21ef7a4a5e8450e14851d915d820e753c51"
sources:
  - raw/2026-04-07-test-github-repo.md
quality_score: 0
concepts:
  - htmx-attribute-api
related:
  - "[[HTML Over The Wire With htmx]]"
  - "[[htmx - HTML Over The Wire]]"
tier: hot
tags: [html, attributes, api, declarative, ajax, websockets, sse]
---

# htmx Attribute API

## Overview

The htmx Attribute API is a set of custom HTML attributes (prefixed with `hx-`) that declaratively define client-server interactions, event triggers, and DOM update strategies. This API is the primary interface for developers to add dynamic behavior to web pages without writing imperative JavaScript.

## How It Works

The htmx Attribute API consists of a family of attributes that can be added to any HTML element to control its behavior in response to user interactions or other events. The most important attributes include:

- `hx-get`, `hx-post`, `hx-put`, `hx-delete`: Define the HTTP method and endpoint to request when the element is triggered.
- `hx-trigger`: Specifies the event(s) that will trigger the request (e.g., `click`, `change`, `mouseenter`, or custom events).
- `hx-target`: Identifies the DOM element to be updated with the server response (using CSS selectors or special keywords).
- `hx-swap`: Determines how the server response is inserted into the DOM (e.g., `outerHTML`, `innerHTML`, `beforebegin`, `afterend`, etc.).
- `hx-include`: Specifies additional elements whose values should be included in the request payload.

When a specified event occurs, htmx intercepts it, gathers any necessary data (from the triggering element and any included elements), and sends an HTTP request to the specified endpoint. The server's response is then used to update the target element according to the swap strategy. This process is entirely declarative and does not require custom JavaScript event handlers or DOM manipulation code.

Advanced attributes allow for fine-grained control over request timing (`hx-trigger` modifiers), request headers, indicators for loading states, and more. The API is designed to be composable and extensible, with support for extensions that add new attributes or behaviors (such as WebSockets or SSE integration).

The Attribute API also supports progressive enhancement: if JavaScript is disabled, the underlying HTML elements (e.g., forms, links) will still function as normal, ensuring accessibility and graceful degradation.

## Key Properties

- **Composability:** Attributes can be combined on any element to achieve complex behaviors with simple markup.
- **Event and Method Flexibility:** Supports any DOM event and any HTTP method, not limited to traditional HTML constraints.
- **DOM Targeting and Swapping:** Fine-grained control over which elements are updated and how.
- **Progressive Enhancement:** Degrades gracefully if JavaScript is disabled.

## Limitations

The Attribute API is best suited for server-driven applications where the server returns HTML fragments. It may not fit SPA architectures or applications that rely heavily on JSON APIs and client-side rendering. Complex interactions may require custom extensions or imperative JavaScript.

## Example

```html
<!-- Issue a GET request on mouseenter, updating only the #details div -->
<div hx-get="/details" hx-trigger="mouseenter" hx-target="#details" hx-swap="innerHTML">
  Hover for details
</div>
<div id="details"></div>
```

## Relationship to Other Concepts

- **[[HTML Over The Wire With htmx]]** — The Attribute API is the mechanism that enables HTML Over The Wire.

## Practical Applications

Used for adding interactivity to forms, buttons, navigation elements, and any other HTML elements without writing JavaScript. Enables rapid prototyping and development of dynamic interfaces in server-rendered web applications.

## Sources

- [[htmx - HTML Over The Wire]] — primary source for this concept
