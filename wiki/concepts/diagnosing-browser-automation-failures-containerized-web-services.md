---
title: "Diagnosing Browser Automation Failures in Containerized Web Services"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "9087cb7649f7304dd2917525af12c2fd1f436fd5b0eb12bcf0b6c9787bb8f3f4"
sources:
  - raw/2026-04-18-copilot-session-knightcrawler-done-routing-traced-7bbbddcd.md
quality_score: 56
concepts:
  - diagnosing-browser-automation-failures-containerized-web-services
related:
  - "[[Opencode Docker Container Bash Shell Configuration]]"
  - "[[Copilot Session Checkpoint: Knightcrawler done, routing traced]]"
tier: hot
tags: [containerization, browser-automation, diagnostics, web-scraping, opencode]
---

# Diagnosing Browser Automation Failures in Containerized Web Services

## Overview

A methodology for distinguishing between generic network egress and browser-based web automation failures in containerized services, using the opencode container as a case study. The process highlights the importance of matching runtime tooling to application requirements.

## How It Works

The diagnosis begins with a user report that the opencode container 'can't reach the web.' The investigation first verifies the service's basic health: the container is running, reachable on the LAN, and responds as expected (HTTP 401 for unauthenticated requests). Next, the focus shifts to outbound network access from within the container. Using command-line tools, the investigation confirms that HTTPS requests to a wide variety of external sites (e.g., GitHub, PyPI, Google) succeed, indicating that generic network egress is fully functional.

However, a subtlety arises: requests to `https://opencode.ai` return 403 with a default user agent but succeed (HTTP 200) when a browser-like user agent is used. This suggests that some web endpoints may require browser automation or specific headers to function as intended. Further inspection of the container reveals that no browser binaries or automation tooling (e.g., Chromium, Playwright) are present. Meanwhile, the configuration references a 'stealth-browser' skill path, implying that browser-based automation is an expected capability.

The root cause is thus identified: while generic HTTPS fetches work, any workflow or skill that depends on actual browser automation (e.g., headless browsing, JavaScript execution, advanced scraping) will fail due to missing dependencies. The next step is to clarify the user's intended workflow—if browser automation is required, the container image must be rebuilt to include the necessary binaries and libraries.

This diagnostic pattern is crucial in environments where containers are used for automation, scraping, or integration testing. It demonstrates the importance of matching the runtime environment to the application's requirements and not assuming that network egress alone is sufficient for all web interactions.

## Key Properties

- **Separation of Concerns:** Distinguishes between basic network egress (e.g., curl, urllib) and browser-based automation (e.g., Chromium, Playwright).
- **Configuration-Driven Expectations:** Container configuration may reference skills or features (like 'stealth-browser') that require additional runtime dependencies.
- **User-Agent Sensitivity:** Some endpoints return different responses based on the User-Agent header, highlighting the need for browser automation in some cases.

## Limitations

If the user's workflow does not require browser automation, adding browser tooling is unnecessary and increases image size and attack surface. Conversely, if browser automation is required but not installed, failures may be silent or misattributed to network issues. Diagnosing the exact failure mode requires clear reproduction steps and understanding of the application's expectations.

## Example

The opencode container can fetch `https://github.com` with curl, but fails to interact with a site that requires JavaScript or a browser-like User-Agent. Attempting to run a 'stealth-browser' skill fails because no browser binary is present. Rebuilding the container with Chromium and Playwright resolves the issue.

## Visual

No images or diagrams are present; all information is from text.

## Relationship to Other Concepts

- **[[Opencode Docker Container Bash Shell Configuration]]** — Both deal with the configuration and troubleshooting of the opencode container environment.

## Practical Applications

This diagnostic approach is essential for teams deploying automation, scraping, or testing workloads in containers. It ensures that the runtime environment matches the application's needs and prevents wasted debugging effort on non-existent network issues. It is also relevant for CI/CD pipelines, integration testing, and any scenario where browser automation is a requirement.

## Sources

- [[Copilot Session Checkpoint: Knightcrawler done, routing traced]] — primary source for this concept
