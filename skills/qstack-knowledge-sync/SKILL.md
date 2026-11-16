---
name: qstack-knowledge-sync
description: "Refresh a configured repository knowledge index and confirm source health."
---

# Knowledge Sync

## Requirements

- A configured knowledge service and the appropriate repository indexing permissions.

## Procedure

1. Verify the registered service, repository source identity, access policy and permitted memory sources. Choose incremental, full or dry-run mode.
2. Synchronize only approved sources through the service's supported tool. Serialize shared-state updates and report skipped and failed sources individually.
3. Check a known result or indexed count for the intended source. Refresh only the managed guidance for verified capabilities and report freshness and remaining errors.

## Upstream sources

- Scoped sync, source health verification, and managed agent guidance refresh. [gstack/sync-gbrain](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/sync-gbrain/SKILL.md#L357)
