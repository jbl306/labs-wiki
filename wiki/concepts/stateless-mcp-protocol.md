---
title: "Stateless MCP Protocol"
type: concept
created: 2026-08-13
last_verified: 2026-08-13
source_hash: "b2f410bb2e6174f3e9d94131513a3a7120a9ff33a9a6e89ddf3ea5ee238dd898"
sources:
  - raw/2026-08-08-the-next-generation-of-mcp-cloudflare-blog.md
quality_score: 88
concepts:
  - stateless-mcp-protocol
  - request-scoped-infrastructure
  - mcp-migration
related:
  - "[[The Next Generation of MCP | Cloudflare Blog]]"
  - "[[Multi Round-Trip Requests for MCP Elicitation]]"
  - "[[Code Mode MCP Server]]"
tier: hot
tags: [mcp, stateless, http, serverless, cloudflare]
---

# Stateless MCP Protocol

## Overview

The stateless MCP protocol removes protocol-session state from the normal request path. Under the MCP 2026-07-28 specification described by Cloudflare, each request carries the protocol version, client identity, and client capabilities it needs, so a server can process a tool, prompt, or resource request and return a result without maintaining an MCP session.

## Mechanism

Earlier MCP transports used an `initialize`/`initialized` exchange and could assign an `Mcp-Session-Id` header. Every later request then had to reach the infrastructure holding the associated session state. This created deployment concerns around sticky routing, autoscaling, draining, migration, reconnects, and stream management.

The new model removes the required handshake, `Mcp-Session-Id`, and core protocol sessions. Optional `server/discover` gives a client a way to inspect a server before a later request, but discovery is not required for ordinary request processing. Application state can still exist; the change is that MCP itself no longer requires stateful infrastructure to speak the protocol.

## Trade-offs and Limitations

Stateless requests simplify horizontal scaling, reduce coordination overhead, and fit request-scoped platforms such as Cloudflare Workers. Durable Objects or another stateful primitive remain appropriate when the application—not the MCP transport—needs coordinated state, persistent storage, or real-time interaction. Servers that depend on legacy sessions, server-to-client requests, or standalone streams require a deliberate migration and may need a temporary legacy route.

The transition is also version-sensitive. Cloudflare describes a compatibility path in which one `/mcp` endpoint accepts the new protocol and stateless requests from 2025 Streamable HTTP clients, but implementations with genuinely sessionful behavior cannot be converted merely by removing a header.

## Concrete Example

A Worker receives a `tools/call` request containing the protocol version, client metadata, capabilities, tool name, and arguments. It invokes the tool, returns the result, and retains no MCP session between calls. If the application must coordinate a long-running workflow, it can store that workflow in a Durable Object while keeping the MCP transport itself stateless.

## Sources

- [[The Next Generation of MCP | Cloudflare Blog]] — primary source
