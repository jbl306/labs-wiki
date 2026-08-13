---
title: "MCP Authorization Evolution"
type: concept
created: 2026-08-13
last_verified: 2026-08-13
source_hash: "b2f410bb2e6174f3e9d94131513a3a7120a9ff33a9a6e89ddf3ea5ee238dd898"
sources:
  - raw/2026-08-08-the-next-generation-of-mcp-cloudflare-blog.md
quality_score: 87
concepts:
  - mcp-authorization
  - client-id-metadata-documents
  - resource-audience-validation
related:
  - "[[The Next Generation of MCP | Cloudflare Blog]]"
  - "[[Stateless MCP Protocol]]"
  - "[[Cloudflare]]"
tier: hot
tags: [mcp, authorization, oauth, security, cloudflare]
---

# MCP Authorization Evolution

## Overview

The MCP 2026-07-28 specification tightens authorization for remote MCP servers by defining a preference order for client registration, adding issuer identification, and requiring resource-oriented token audience handling. Cloudflare describes these changes as production hardening that lets MCP authorization fit established web security infrastructure more reliably.

## Mechanism

When a client and server already have a relationship, pre-registered clients are preferred. For dynamic relationships, Client ID Metadata Documents (CIMD) are preferred, with Dynamic Client Registration (DCR) retained as a fallback. The article states that DCR is deprecated for new implementations and is planned for removal after summer 2027.

The specification adopts RFC 9207 issuer identification. An authorization server advertises `authorization_response_iss_parameter_supported: true` and includes `iss` in successful authorization responses. The client compares that issuer with the issuer discovered before authorization, reducing the risk that a response from one issuer is confused with a response from another.

MCP clients also send the canonical server URI as the RFC 8707 `resource` in authorization and token requests. Tokens must be issued for and accepted only by that audience. Cloudflare's Workers OAuth Provider exposes configuration for CIMD and resource metadata, including the MCP resource URI, authorization servers, and supported scopes.

## Trade-offs and Limitations

The stricter flow improves issuer and audience binding but increases implementation requirements for clients, authorization servers, and MCP server operators. Existing deployments using DCR or assumptions about loosely scoped tokens need migration planning. The article documents Cloudflare's implementation pattern but does not establish that every OAuth provider supports all of these MCP-specific settings.

## Concrete Example

A Worker-hosted MCP server publishes resource metadata for `https://mcp.example.com/mcp`, identifies its authorization server, enables CIMD, and requests tokens for that resource URI. After authorization, the client checks the returned issuer before accepting the response and the server accepts the token only when its audience is the canonical MCP resource.

## Sources

- [[The Next Generation of MCP | Cloudflare Blog]] — primary source
