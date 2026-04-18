---
title: "Ntfy Push Notifications for Service Monitoring"
type: concept
created: 2026-04-18
last_verified: 2026-04-18
source_hash: "047e464d50e32062c5eb82637072ff9ad4eca8476f8f0c7369fe4664be464407"
sources:
  - raw/backfill-copilot-sessions-2026-04-18/2026-04-18-copilot-session-ntfy-notifications-galloping-bot-alerts-monitor--27e974be.md
quality_score: 100
concepts:
  - ntfy-push-notifications-for-service-monitoring
related:
  - "[[Agent Feedback Loop Mechanism]]"
  - "[[The Observability Imperative]]"
  - "[[Copilot Session Checkpoint: ntfy Notifications, Galloping-Bot Alerts, Monitor Fixes]]"
tier: hot
tags: [monitoring, notifications, docker, ntfy, uptime-kuma]
---

# Ntfy Push Notifications for Service Monitoring

## Overview

Ntfy is a lightweight, open-source push notification service used here to provide real-time alerts for service monitoring and cron job outcomes. Integrating ntfy with monitoring tools like Uptime Kuma and Docker event watchers enables proactive notification of service health changes, container failures, and operational events.

## How It Works

Ntfy operates as a publish-subscribe notification system where clients subscribe to topics and receive messages pushed by publishers. In this homelab setup, the ntfy.sh cloud service is used with a dedicated topic (`jbl-homelab-alerts`) for all alerts. The integration involves:

1. **Uptime Kuma Integration:** The Python script `update_uptime_kuma.py` was enhanced to add ntfy as a notification provider via its API. This includes setting `isDefault=True` and `applyExisting=True` to attach notifications to all existing monitors automatically. The script supports authentication and explicit accepted HTTP status code checks to accurately detect service health.

2. **Docker Event Watching:** A POSIX sh script `docker-notify.sh` runs inside a lightweight Alpine `docker:cli` container. It listens to Docker events such as container die, OOM, unhealthy, and restart loops. Upon detecting these events, it sends ntfy notifications using `wget` HTTP POST requests since `curl` is not available in the image.

3. **Galloping-Bot Cron Job Alerts:** The golf tee time sniping script `galloping-snipe.sh` captures output via `tee`, parses for booking confirmation lines, and sends ntfy notifications with different priority levels depending on booking success, no bookings, or failures.

This setup enables centralized, real-time alerting for critical service states and operational events, improving observability and rapid response capabilities.

## Key Properties

- **Notification Topics:** All alerts are published to a dedicated ntfy topic `jbl-homelab-alerts` hosted on ntfy.sh cloud.
- **Integration Points:** Uptime Kuma monitors, Docker event watcher script, and galloping-bot cron jobs are integrated as ntfy publishers.
- **Notification Priorities:** Notifications include priority levels: high priority for errors and bookings, default for no bookings.
- **Transport Protocol:** HTTP POST requests using `wget` are used for sending notifications due to container image constraints.

## Limitations

The Docker event watcher must run in an environment with Docker socket access and uses a minimal Alpine image lacking curl, requiring POSIX sh compatibility and wget usage. Ntfy notifications depend on external cloud service availability (ntfy.sh). Authentication and API quirks in Uptime Kuma require careful handling to avoid silent failures.

## Example

Example snippet from `docker-notify.sh` sending ntfy notification on container die event:

```sh
wget -qO- --method POST --header "Title: Container Down" --body "Container $CONTAINER_NAME died" $NTFY_SERVER/$NTFY_TOPIC
```

Example Python snippet adding ntfy provider to Uptime Kuma monitors:

```python
kuma.add_notification_provider(
    type="ntfy",
    isDefault=True,
    applyExisting=True,
    auth=(KUMA_USER, KUMA_PASS),
    extra_kwargs={"server": NTFY_SERVER, "topic": NTFY_TOPIC}
)
```

## Relationship to Other Concepts

- **[[Agent Feedback Loop Mechanism]]** — Ntfy notifications provide real-time feedback signals for monitoring agents.
- **[[The Observability Imperative]]** — Ntfy integration enhances observability by providing timely alerts on service health.

## Practical Applications

This concept is applied in homelab environments and production systems to monitor containerized services, detect failures, and notify operators or automated agents immediately. It supports proactive incident response and operational awareness.

## Sources

- [[Copilot Session Checkpoint: ntfy Notifications, Galloping-Bot Alerts, Monitor Fixes]] — primary source for this concept
