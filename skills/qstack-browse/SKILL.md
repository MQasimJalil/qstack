---
name: qstack-browse
description: "Open a browser for a focused page check, interaction, or visible walkthrough."
---

# Browse

## Requirements

- An available browser interface. A walkthrough requires a visible session.

## Procedure

1. Identify the target URL or tab, accessible session, and whether the user needs a visible browser. Reuse the named tab or create a dedicated tab when isolation is needed.
2. Start the configured browser visibly when requested and verify readiness. Keep existing sessions and profiles available when a new tab suffices.
3. Snapshot before acting. Scope actions to intent, then capture page change, meaningful console errors or a screenshot. Leave a requested visible session available.

## Upstream sources

- Focused browser inspection and evidence capture. [gstack/browse](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/browse/SKILL.md#L398)
- Visible browser launch and intentional reuse of an active session. [gstack/open-gstack-browser](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/open-gstack-browser/SKILL.md#L152)
