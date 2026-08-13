---
title: "The next generation of MCP | Cloudflare Blog"
type: url
captured: 2026-08-08T12:43:46.942667+00:00
source: android-share
url: "https://blog.cloudflare.com/mcp-v2/"
content_hash: "sha256:f66aea27eeabe66a6361457106cbd6fabdc6a20f48f41aa0edcc84596bef73ca"
tags: []
status: ingested
---

https://blog.cloudflare.com/mcp-v2/

<!-- fetched-content:start -->
## Fetched Metadata
- fetched_at: 2026-08-08T12:43:52+00:00
- source_url: https://blog.cloudflare.com/mcp-v2/
- resolved_url: https://blog.cloudflare.com/mcp-v2/
- content_type: text/html
- image_urls: ["https://blog.cloudflare.com/_image?href=https%3A%2F%2Fblog.cloudflare.com%2F_emdash%2Fapi%2Fmedia%2Ffile%2F01KZA53A6RYJARJY0Q83JSH53M.png&w=715&h=334&f=webp&fit=cover&position=center", "https://blog.cloudflare.com/_image?href=https%3A%2F%2Fblog.cloudflare.com%2F_emdash%2Fapi%2Fmedia%2Ffile%2F01KZA53A5N7VQM3QTA57A2FN83.png&w=715&h=415&f=webp&fit=cover&position=center", "https://blog.cloudflare.com/_emdash/api/media/file/01KZA53A9E3R79TDV6T6RCNDKG.png", "https://blog.cloudflare.com/_image?href=https%3A%2F%2Fblog.cloudflare.com%2F_emdash%2Fapi%2Fmedia%2Ffile%2F01KZA53A5G2PQVSM15SFEAYVAS.png&w=1200&h=675&f=webp&fit=cover&position=center", "https://blog.cloudflare.com/_image?href=https%3A%2F%2Fblog.cloudflare.com%2F_emdash%2Fapi%2Fmedia%2Ffile%2F01KZA53A660J99FJBX7DAWZ4MZ.png&w=715&h=232&f=webp&fit=cover&position=center"]

## Fetched Content
Over the last year and a half, the
Model Context Protocol
(MCP) has become the universal standard for how agents interact with external services.
But one of the main criticisms of MCP was that the protocol required a stateful connection between Client and Server. This evolved from MCP’s origins and the
first STDIO transport,
designed for local applications
. When MCP Servers went remote, it translated the stateful connection that worked so well locally and transposed it onto web infrastructure. Building a well-behaved MCP Server meant managing request routing to sticky sessions, holding open streams, message replay, and generally more overhead and complexity than a traditional web server. This changes now.
The latest MCP
2026-07-28 specification
was released last week, together with updated TypeScript, Python, Go, and C# SDKs. MCP is now a fully stateless protocol. The specification, interaction model and SDKs have all been rewritten to leverage this new protocol and simplify usage. This means that MCP servers can now run in just a Worker, no stateful infrastructure needed, and customers benefit from the operational simplicity and reduced cost of less moving parts.
## A new MCP
At Cloudflare, our journey with MCP goes back to the very beginning. In March 2025, we released our McpAgent primitive for
building MCP servers with Cloudflare Agents SDK
. Two months later, we ran an
MCP Demo Day
showcasing customers such as Asana, Atlassian, Block, Intercom, Linear, PayPal, Sentry, Stripe, and Webflow launching their own MCP Servers along with
13 Cloudflare product-specific MCP servers
. A year ago, we released
MCP Server Portals
, to help enterprises securely adopt MCP in their organisations.
Cloudflare Durable Objects
were uniquely positioned to be the best place to host these new applications. They are stateful servers that combine compute, persistent transactional storage (via embedded SQLite), and real-time coordination. They scale up on demand, hibernate when not in use, and keep the stateful connection needed by MCP for Agent-to-Human interaction.
`McpAgent`
combined with the
Workers OAuth Provider
package was the best place to host remote MCP servers. However, it became apparent that MCP could be simpler, more efficient, and easier to host, while keeping all capabilities we have grown to love.
This release of the MCP 2026-07-28 specification has been months of work by the whole MCP team and the SDK maintainers. In this post, we will outline the protocol changes that matter most for developers, share testimonials from customers running it in production, and explain how to start building with the new specification.
## MCP is now stateless
Earlier MCP transports began with an
`initialize`
and
`initialized`
exchange that would start a session. A server could assign an Mcp-Session-Id header, and every subsequent request had to find the state associated with that session. In practice this meant that autoscaling infrastructure had to preserve active sessions, deployments had to drain or migrate them, and losing an active instance could force clients to reconnect or lead to broken sessions. Serverless platforms could run MCP servers, but only by adding coordination for a protocol session that most interactions never even needed.
The new protocol removes the required handshake, the
`Mcp-Session-Id`
header, and protocol sessions from the core request path. Each request carries the protocol version, client identity, and client capabilities it needs. A client that wants to inspect a server before making another request can call
`server/discover`
, but this is optional.
That simple detail changes how an MCP server can be deployed. A request can arrive at a server, invoke a tool, prompt, or resource, and simply return the result. There is no protocol session to store. This removes a huge part of MCP complexity, while preserving all the functionality that’s expected from it, making MCP servers easier to deploy, scale, and maintain over time.
This new specification thus also removes the need for
`McpAgent`
. While Durable Objects remain the right primitive when an application itself needs state, MCP itself no longer requires a Durable Object to speak the protocol. Servers can scale faster on request scoped infrastructure such as Cloudflare Workers.
Cloudflare's Agents SDK has supported the new specification since day one
. Customers and partners have used the release candidate on Cloudflare before the specification was finalized, giving us confidence that the
migration path
from
`McpAgent`
to the new
`createMcpHandler`
(see below) works with production traffic.
## Elicitation no longer needs an open stream
An MCP server sometimes needs more information before it can finish a request. For example, a deployment tool may need approval before releasing to production. A design tool may need the user to choose colors. A billing tool may need confirmation before issuing a refund. MCP calls this interaction an
elicitation
.
Previously, server-initiated requests such as
`elicitation/create`
depended on an open stream. Deployment of such a server requires balancing the complexity around streams, cost, and request timeouts.
The new protocol reworks this with
Multi Round-Trip Requests (MRTR)
. A server can return an
`input_required`
result that describes what it needs. The client collects the answer and retries the operation with that input. The original operation can then complete, without either side preserving a transport session between those requests.
This is a breaking change from the old way of doing elicitations. However, it is operationally much simpler to implement, and we believe that it will allow more developers to make use of this capability to build rich agentic applications.
## HTTP infrastructure understands MCP
MCP requests are JSON-RPC messages sent over HTTP, but information about the request previously lived only inside the JSON body. A gateway had to parse that body to learn whether a request called
`tools/list`
, invoked a tool, or read a resource.
The new specification requires
`Mcp-Method`
and
`Mcp-Name`
headers on Streamable HTTP requests. For example, a tool invocation can look like this:
```
POST /mcp HTTP/1.1
MCP-Protocol-Version: 2026-07-28
Mcp-Method: tools/call
Mcp-Name: search
Content-Type: application/json
{
"jsonrpc": "2.0",
"id": 1,
"method": "tools/call",
"params": {
"name": "search",
"arguments": { "q": "otters" }
}
}
```
A gateway, rate limiter, or Web Application Firewall can now make decisions from headers without parsing arbitrary JSON. Operators can apply different rules to different methods or record tool-level metrics using the same HTTP primitives they already use elsewhere.
The specification also adds
`ttlMs`
and
`cacheScope`
hints to results from
`tools/list`
,
`prompts/list`
,
`resources/list`
, and
`resources/read`
. Tool catalogs are deterministically ordered, allowing clients to reuse them while keeping upstream prompt caches stable across reconnects.
## Authorization continues to evolve
The new specification also tightens MCP authorization. MCP now prefers pre-registered clients when the server and client already have a relationship, then
Client ID Metadata Documents
(CIMD) for dynamic registrations, with Dynamic Client Registration (DCR) as a fallback. DCR is deprecated for new implementations and is slated for removal after summer 2027.
The specification also adopts
RFC 9207
issuer identification. An authorization server advertises
`authorization_response_iss_parameter_supported: true`
and includes iss in successful authorization responses. The client compares it with the issuer discovered before starting the authorization flow. This prevents an authorization response from one issuer from being confused with a response from another.
There are several less visible changes that close gaps in production deployments. MCP clients now send the canonical server URI as the RFC 8707
`resource`
in authorization and token requests. Tokens must be issued for, and accepted only by, that audience.
Workers OAuth Provider
implements all these requirements for MCP servers on Workers. Just wrap your handler functions like so:
```
import
{ OAuthProvider }
from
"@cloudflare/workers-oauth-provider"
;
export
default
new
OAuthProvider
({
apiRoute:
"/mcp"
,
apiHandler: mcpHandler,
defaultHandler: authorizationHandler,
authorizeEndpoint:
"/authorize"
,
tokenEndpoint:
"/oauth/token"
,
clientIdMetadataDocumentEnabled:
true
,
resourceMetadata: {
resource:
"https://mcp.example.com/mcp"
,
authorization_servers: [
"https://mcp.example.com"
],
scopes_supported: [
"mcp:read"
],
},
});
```
## A lifecycle for a maturing standard
The technical changes are only part of this release. MCP 2026-07-28 also introduces a formal feature lifecycle.
Features are classified as Active, Deprecated, or Removed. A deprecated feature must remain available for at least 12 months before it can be removed. Roots, Sampling, Logging, Dynamic Client Registration, and the legacy HTTP+SSE transport are deprecated in this release, but existing implementations have a defined migration window.
This policy gives teams a minimum amount of time to plan upgrades rather than react to sudden removals. It also gives the core protocol room to stabilize.
New ideas can move faster through the new extensions framework without immediately becoming part of the core protocol.
MCP Apps
and
Enterprise-Managed Authorization
are already extensions, while
Tasks
have been moved over to provide a path for reliable, long-running work. Implementers can adopt those capabilities as and when needed.
## A new MCP with new SDKs
In November 2025, we introduced
`createMcpHandler`
to our Agents SDK, built on an experimental stateless mode in the MCP TypeScript SDK. This let MCP servers that only made use of tools, prompts, and resources be deployed to a Cloudflare Worker for lower complexity, cost and easier deployments.
We are happy to see
`createMcpHandler`
graduate into
the official MCP TypeScript SDK
with this release!
In early 2026, we also worked with MCP maintainers on replatforming the MCP TypeScript SDK from Node.js to Web Standards, helping to improve interoperability with alternative JavaScript runtimes like Bun, Deno, and Cloudflare Workers. We contributed bundling, runtime shims, and split packages in the TypeScript SDK, lowering deployment sizes and benefitting the whole ecosystem.
Customers can migrate to the new specification whilst keeping backward compatibility with older specifications. The
`/mcp`
endpoint accepts both the new protocol and stateless requests from 2025 Streamable HTTP clients, so most clients can reconnect without configuration changes.
For example, in February we released our Code Mode
MCP Server for the entire Cloudflare API
using this unofficial stateless mode and the (catchy)
`WebStandardsStreamableHTTPServerTransport`
. Since then, it has scaled up to thousands of requests per second and served billions of tool calls.
Here is the shape of a minimal server using the official SDK and the
Cloudflare Agents SDK
:
```
import
{ McpServer }
from
"@modelcontextprotocol/server"
;
import
{ createMcpHandler }
from
"agents/mcp/server"
;
import
{ z }
from
"zod"
;
function
createServer
() {
const
server
=
new
McpServer
({
name:
"hello-server"
,
version:
"1.0.0"
,
});
server.
registerTool
(
"hello"
,
{
description:
"Return a greeting"
,
inputSchema: { name: z.
string
().
optional
() },
},
async
({
name
})
=>
({
content: [
{
type:
"text"
,
text:
`Hello, ${
name
??
"World"}!`
,
},
],
}),
);
return
server;
}
export
default
{
fetch
(
request
,
env
,
ctx
) {
return
createMcpHandler
(createServer)(request, env, ctx);
},
}
```
Servers that truly depend on legacy protocol sessions, server-to-client requests, or standalone streams need a more deliberate migration. They can run a strict stateless route beside the existing sessionful route, move features over, allow active sessions to drain, and then remove the legacy path during the deprecation period. Our
MCP SDK v2 migration guide
covers that process. For MCP clients the process is even easier: just upgrade your version of agents, and it will just work.
The
`createMcpHandler`
API began in the Agents SDK, and will continue to live there. We will also continue to wrap the upstream handler to provide a Worker-focused interface with functional defaults and richer interaction patterns than the lower level MCP TypeScript SDK.
## Next gen MCP is already in production
David Cramer, co-founder and chief product officer at
Sentry
, is a noted voice on both
the promise of MCP
and its
early opportunities for improvement
. In his early real-world experience, the latest MCP spec delivers on that promise while addressing the early criticism.
"We built Sentry's MCP on Cloudflare's SDK. Big fans,” Cramer told us. “We went live with this new one before the 7-28 spec was even finalized, and it didn't break prod. Big fans of that, too. This new spec cleans up a bunch of the nonsense around auth and tools, which is exactly what I wanted. Agents only get useful once the plumbing stops being the whole story."
Linear
builds a fast, modern issue tracking and project management tool. They’ve adopted MCP to let agents access Linear data in a simple and secure way.
“MCP is a clear example of why open standards matter,” said Tom Moor, Head of Engineering at Linear. “The latest iteration of the spec is a great improvement that makes hosting an MCP server easier, more reliable, and at the same time adds much needed functionality. I still think MCP is massively underestimated — we built our server once on the standard and it works with whatever AI client our users want to bring. Linear's stance has always been to make your Linear data accessible wherever you need it and the shared spec makes that possible without building hundreds of integrations.”
Anthropic
created MCP and donated it to the
Agentic AI Foundation
. For the team that started the protocol, the new spec is a measure of how far it has come, and of how much the community now carries it forward.
“We donated MCP to the Agentic AI Foundation so it could become open, vendor-neutral infrastructure for the whole ecosystem. MCP is now foundational for agentic software. It’s the layer applications build on to connect with the tools and data people rely on every day and this is the most significant advance to the protocol since launch. Clients gain meaningful performance with minimal engineering work.
Security follows the same proven standards that protect the rest of the internet. Maintainers and contributors from across the community, drawing on real production experience at enterprise scale, made that possible. We can't wait to see what developers build on MCP." said David Soria Parra, Co-creator and Lead Maintainer of MCP, and Member of Technical Staff at Anthropic.
## Long live MCP
The new MCP specification is available for both clients and servers on Cloudflare today. You can run a stateless MCP server in a
Cloudflare Worker
, secured with
Workers OAuth Provider
and connect to an MCP client in an
`Agent`
. Use
Cloudflare Durable Objects
when your application actually needs coordinated state, and serve new and legacy stateless clients from the same route while users migrate.
Install the latest
Agents SDK
and the MCP TypeScript server SDK, follow the
migration guide
, or start with the
`createMcpHandler`
documentation
. You can also connect to Cloudflare's
MCP servers
, which already support the new specification.
MCP no longer needs stateful infrastructure to do useful, interactive work. Servers can run as an ordinary HTTP workload on Workers, close to users, with the scale, security, and observability primitives developers use for the rest of the web.
## Related tags
Agents
Agents Week
AI
Developer Platform
Developers
MCP
Product News
Follow on Social Media
- Cloudflare
- Matt Carey
## Subscribe to receive notifications of new posts
<!-- fetched-content:end -->
