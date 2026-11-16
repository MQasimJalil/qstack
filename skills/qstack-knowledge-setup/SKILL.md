---
name: qstack-knowledge-setup
description: "Connect a project knowledge service and verify its access scope."
---

# Knowledge Setup

## Requirements

- A supported local index or knowledge service with its authorized connector or CLI.

## Procedure

1. Inspect current settings, repository identity and service health. Reuse a verified working instance when it satisfies the request.
2. Configure the chosen service or local index through its approved package or connector. Keep credentials in its secure store and record permitted remotes and access modes.
3. Treat transcript ingestion as a separate opt-in scope. Verify the intended service with a scoped query and report registered scope, readiness and unavailable capabilities.

## Upstream sources

- Verify the connection, record per-remote access policy and handle transcript opt-in separately. [gstack/setup-gbrain](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/setup-gbrain/SKILL.md#L411)
