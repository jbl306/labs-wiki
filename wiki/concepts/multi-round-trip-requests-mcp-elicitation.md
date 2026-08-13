---
title: "Multi Round-Trip Requests for MCP Elicitation"
type: concept
created: 2026-08-13
last_verified: 2026-08-13
source_hash: "b2f410bb2e6174f3e9d94131513a3a7120a9ff33a9a6e89ddf3ea5ee238dd898"
sources:
  - raw/2026-08-08-the-next-generation-of-mcp-cloudflare-blog.md
quality_score: 86
concepts:
  - multi-round-trip-requests
  - mcp-elicitation
  - stateless-interaction
related:
  - "[[The Next Generation of MCP | Cloudflare Blog]]"
  - "[[Stateless MCP Protocol]]"
  - "[[MCP Authorization Evolution]]"
tier: hot
tags: [mcp, elicitation, agent-human-interaction, stateless, http]
---

# Multi Round-Trip Requests for MCP Elicitation

## Overview

Multi Round-Trip Requests (MRTR) are the MCP 2026-07-28 approach to elicitation: when a server needs additional information or approval, it returns an `input_required` result, the client collects the answer, and the client retries the operation with that input. The interaction preserves multi-step agent-human workflows without requiring an open transport stream or a protocol session between requests.

## Mechanism

An operation such as a production deployment, design choice, or billing refund can stop at the point where user input is needed. Instead of issuing a server-initiated `elicitation/create` request over an open stream, the server describes the missing input in its response. The client presents that request to the user or agent, then sends a new request containing the answer. The original operation can complete from the retried request.

This makes the interaction compatible with request-scoped infrastructure. The transport does not need to hold a stream open while waiting for a human response, and neither client nor server needs to preserve an MCP transport session solely for elicitation.

## Trade-offs and Limitations

MRTR is operationally simpler and avoids stream timeout, balancing, and connection-cost problems. It is also a breaking change from the previous server-initiated elicitation behavior, so clients and servers must agree on the new interaction model. Applications must define how the retried request identifies the pending operation and how they prevent duplicate side effects; the source describes the protocol shape but does not specify application-level idempotency semantics.

MRTR does not eliminate application state when a workflow itself needs durable progress, authorization records, or coordination. It only removes the requirement that the MCP transport keep an open stream while input is collected.

## Concrete Example

A deployment tool receives a request to release a build. It returns `input_required` asking for production approval. The client obtains approval and retries the operation with that answer. The server then performs the deployment without relying on an open connection from the first request.

## Sources

- [[The Next Generation of MCP | Cloudflare Blog]] — primary source
