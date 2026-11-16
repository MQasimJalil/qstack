---
name: qstack-browser-pairing
description: "Pair another authorized agent with a scoped browser session."
---

# Browser Pairing

## Requirements

- A browser controller with authenticated, revocable pairing and an authorized receiving agent.

## Procedure

1. Confirm the receiving agent, permitted domains or tabs, purpose and time window. Choose a dedicated profile when the current profile contains unrelated data.
2. Issue a short-lived and minimally scoped connection through the supported browser controller. Deliver setup information through its secure pairing mechanism.
3. Have the receiving agent verify the intended tab with a harmless scoped read. Report the connection and how its owner can revoke it. Revoke or close the dedicated session when pairing ends.

## Upstream sources

- Temporary pairing with receiving-agent setup, connection proof and revocation. [gstack/pair-agent](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/pair-agent/SKILL.md#L97)
