---
title: "htmx - HTML Over The Wire"
type: source
created: 2026-04-08
last_verified: 2026-04-08
source_hash: "241ccd0756ba8b32170ef8926eb8e21ef7a4a5e8450e14851d915d820e753c51"
sources:
  - raw/2026-04-07-test-github-repo.md
quality_score: 100
concepts:
  - html-over-the-wire-with-htmx
  - htmx-attribute-api
related:
  - "[[HTML Over The Wire With htmx]]"
  - "[[htmx Attribute API]]"
  - "[[htmx]]"
tier: hot
tags: [rest, websockets, tool, html, javascript, ajax, sse, declarative]
---

# htmx - HTML Over The Wire

## Summary

htmx is a lightweight, dependency-free JavaScript library that enables dynamic web application features—such as AJAX, CSS transitions, WebSockets, and Server Sent Events—directly from HTML using custom attributes. It aims to extend the capabilities of HTML by removing arbitrary limitations on what elements and events can trigger HTTP requests, allowing developers to build modern, interactive interfaces with minimal JavaScript. The project is actively maintained, well-documented, and supports an extension ecosystem for further customization.

## Key Points

- htmx allows AJAX, CSS transitions, WebSockets, and Server Sent Events to be triggered directly from HTML attributes.
- It removes traditional constraints of HTML, enabling any element and event to initiate HTTP requests with any method.
- The library is small (~14k minified and gzipped), dependency-free, and highly extensible.

## Concepts Extracted

- **[[HTML Over The Wire With htmx]]** — HTML Over The Wire is a web development paradigm enabled by htmx, where dynamic interactions and server communication are managed directly through HTML attributes rather than imperative JavaScript. This approach brings the power of AJAX, CSS transitions, WebSockets, and Server Sent Events into the HTML layer, allowing developers to create modern, interactive user interfaces with minimal JavaScript code.
- **[[htmx Attribute API]]** — The htmx Attribute API is a set of custom HTML attributes (prefixed with `hx-`) that declaratively define client-server interactions, event triggers, and DOM update strategies. This API is the primary interface for developers to add dynamic behavior to web pages without writing imperative JavaScript.

## Entities Mentioned

- **[[htmx]]** — htmx is an open-source JavaScript library that enables dynamic, interactive web applications by allowing HTML elements to issue HTTP requests and update the DOM declaratively via custom attributes. It is designed to extend the capabilities of HTML while minimizing the need for custom JavaScript.

## Notable Quotes

> "Why should only <a> and <form> be able to make HTTP requests? Why should only click & submit events trigger them? Why should only GET & POST be available? Why should you only be able to replace the entire screen?" — htmx README
> "By removing these arbitrary constraints htmx completes HTML as a hypertext" — htmx README

## Source Details

| Field | Value |
|-------|-------|
| Original | `raw/2026-04-07-test-github-repo.md` |
| Type | repo |
| Author | bigskysoftware |
| Date | Unknown |
| URL | https://github.com/bigskysoftware/htmx |
