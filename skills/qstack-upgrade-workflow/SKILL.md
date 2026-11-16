---
name: qstack-upgrade-workflow
description: "Upgrade a workflow package from its chosen release channel while protecting local work."
---

# Upgrade Workflow

## Requirements

- A known release channel and a supported method to reinstall the prior version.

## Procedure

1. Identify the installation method, current version, configured channel and intended target. Record how to restore the current release.
2. Check package authenticity, dependencies, local modifications and settings. Preserve user work and upgrade through its existing manager or managed path.
3. Refresh only managed registrations. Verify the reported version, skill discovery, and one representative invocation. Restore the prior supported state if verification fails.

## Upstream sources

- Channel-bound update with version checks, local-change handling, and recovery state. [gstack/gstack-upgrade](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/gstack-upgrade/SKILL.md#L138)
