---
name: qstack-browser-session-setup
description: "Set up an authorized browser profile for pages that require the user's signed-in session."
---

# Browser Session Setup

## Requirements

- An authorized browser interface. The user may need to complete authentication.

## Procedure

1. Check whether an existing authorized session already has access to the requested page. Reuse it when appropriate and leave unrelated sessions intact.
2. Use the browser's native sign-in or an explicitly approved secure session handoff offered by the host. Scope the profile and target domains to the task.
3. Verify access through a harmless in-scope read and report the verified profile, domains, remaining permission constraints and how to disconnect.

## Upstream sources

- Consent, domain scope, approved profile handoff, and verification of usable access. [gstack/setup-browser-cookies](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/setup-browser-cookies/SKILL.md#L160)
