---
title: "Uptime Kuma Monitor Authentication and Notification Integration"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "047e464d50e32062c5eb82637072ff9ad4eca8476f8f0c7369fe4664be464407"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-ntfy-notifications-galloping-bot-alerts-monitor--27e974be.md
quality_score: 75
concepts:
  - uptime-kuma-monitor-authentication-and-notification-integration
related:
  - "[[Ntfy Push Notifications for Service Monitoring]]"
  - "[[The Observability Imperative]]"
  - "[[Copilot Session Checkpoint: ntfy Notifications, Galloping-Bot Alerts, Monitor Fixes]]"
tier: hot
tags: [uptime-kuma, monitoring, authentication, notifications]
---

# Uptime Kuma Monitor Authentication and Notification Integration

## Overview

Uptime Kuma is a self-hosted monitoring tool that supports various notification providers and authentication methods for monitored services. Proper configuration of authentication enums and notification payloads is critical to ensure accurate monitoring and alerting.

## How It Works

Key technical details discovered during this session include:

1. **Notification ID Handling:** Uptime Kuma's API returns `notificationIDList` as a list (e.g., `[1]`) but requires updates to be sent as a dictionary with keys as strings and values as booleans (e.g., `{"1": true}`) to apply notification edits correctly.

2. **Authentication Method Enum:** The `authMethod` field must use the string enum `AuthMethod.HTTP_BASIC` (value `'basic'`) for HTTP Basic Authentication. Using the integer `1` silently fails, causing monitors to report incorrect status.

3. **Notification Provider Addition:** Adding a notification provider with `isDefault=True` and `applyExisting=True` automatically attaches the provider to all existing monitors, simplifying setup.

4. **Accepted Status Codes:** Monitoring scripts must explicitly check HTTP response status codes against accepted codes to detect service health changes accurately.

5. **Credential Management:** Credentials for OpenCode and Giniecode services are injected from environment variables, with fixes applied for username correctness.

These refinements ensure that Uptime Kuma monitors authenticate properly against protected services and that notifications via ntfy are reliably triggered on status changes.

## Key Properties

- **Notification ID Format:** Must be a dict with string keys and boolean values, not a list.
- **AuthMethod Enum:** Use string `'basic'` for HTTP Basic Auth, not integer 1.
- **Automatic Notification Attachment:** `isDefault=True, applyExisting=True` attaches notifications to all monitors.
- **Status Code Checking:** Explicit comparison of returned HTTP status codes is necessary.

## Limitations

Misconfiguration of auth enums or notification payloads can cause silent failures or false alerts. Uptime Kuma API quirks require careful handling in automation scripts. Changes in Uptime Kuma API versions may require script updates.

## Example

Python snippet adding notification provider:

```python
kuma.add_notification_provider(
    type="ntfy",
    isDefault=True,
    applyExisting=True,
    auth=(KUMA_USER, KUMA_PASS),
    extra_kwargs={"server": NTFY_SERVER, "topic": NTFY_TOPIC}
)
```

Correct auth method usage:

```python
authMethod = "basic"  # Correct
# authMethod = 1  # Incorrect, silently fails
```

Notification ID update format:

```json
{"1": true}
```

## Relationship to Other Concepts

- **[[Ntfy Push Notifications for Service Monitoring]]** — Uptime Kuma uses ntfy as a notification provider.
- **[[The Observability Imperative]]** — Accurate monitoring and alerting are key observability practices.

## Practical Applications

This concept applies to configuring self-hosted monitoring systems to authenticate against protected endpoints and reliably send alerts via external notification services.

## Sources

- [[Copilot Session Checkpoint: ntfy Notifications, Galloping-Bot Alerts, Monitor Fixes]] — primary source for this concept
