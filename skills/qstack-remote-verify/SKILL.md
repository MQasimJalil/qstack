---
name: qstack-remote-verify
description: "Run a heavy suite on an authorized disposable compute runner and confirm teardown."
---

# Remote Verify

## Requirements

- An authorized runner provider with quota checks, bounded lifetime and resource status.

## Procedure

1. Establish the suite and exact revision. Use checked-in bootstrap and verification commands, and preflight environment capacity, budget, and source state.
2. Provision the authorized runner with an owner identifier and expiry. Record the resource ID, start the job, and use supported completion or hang handling.
3. Preserve logs, outputs and exit status. Confirm resource teardown on every exit path. Treat unknown cleanup as incomplete and report the resource identity.

## Upstream sources

- Use a quota-checked ephemeral runner, bounded job, logs, watchdog, and verified cleanup. [gstack/ubicloud](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/ubicloud/SKILL.md#L161)
