---
name: qstack-runaway-work
description: "Identify stalled or spending-heavy agent work and perform an authorized stop or clean handoff."
---

# Runaway Work

## Requirements

- A job or agent scheduler that reports reliable identities, status and metrics.

## Procedure

1. Inspect metrics and recent actions for in-scope sessions. Distinguish a legitimate wait from looping, uncontrolled spend and repeated no-op wakes. Record objective evidence and configured caps.
2. For an authorized stop, confirm exact job identity and preserve its artifacts. Route another controller's work through its coordination interface.
3. For rotation, capture state, open decisions and evidence. Start a successor only under the existing authorization and verify handoff before ending the original. Replace duplicate polling with completion notifications when available.

## Upstream sources

- Detect empty wakes and runaway activity, then stop or rotate exactly scoped work. [gstack/runaway-stopper](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/runaway-stopper/SKILL.md#L161)
