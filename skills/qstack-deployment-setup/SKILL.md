---
name: qstack-deployment-setup
description: "Configure a project's deploy target and readiness checks for later release workflows."
---

# Deployment Setup

## Requirements

- Project deploy metadata and a supported platform status interface.

## Procedure

1. Read project and CI configuration for release platform, workflow, build artifact, environments and readiness signals. Resolve the target when several environments match.
2. Record release command, target identity, exact revision check, smoke checks, wait bounds and rollback process in the repository's normal config.
3. Validate read-only status and health commands against the chosen target. Use an available dry-run or existing release record. Report dependencies and point the landing procedure to the configuration.

## Upstream sources

- Detect platform, target and health commands, and persist the chosen configuration. [gstack/setup-deploy](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/setup-deploy/SKILL.md#L135)
