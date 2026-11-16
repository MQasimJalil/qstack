---
name: qstack-maintain-runtime-verification
description: "Reconcile a project verification skill, feature map, and live driving harness with the current app."
---

# Maintain Runtime Verification

## Requirements

- An existing launchable app and verification skill with a feature map are required for this maintenance workflow.

## Procedure

1. Locate the existing verification skill and map. Reconcile its index against feature files, then read each feature’s source entry point and current recipe. Collect missing user surfaces only when you can point to a real source path.
2. Launch the documented app and run its readiness check. Drive every mapped feature through the public surface, using a single coordinator for shared state and fresh isolated instances when the harness calls for them.
3. Capture the reached feature, action, result, and evidence before teardown. Repeat the readiness check after unexpected behavior, then reset, relaunch, or document the specific unreachable prerequisite.
4. Fix only map, harness, or verification skill drift. Re-drive every changed recipe. Report genuine product regressions separately and preserve evidence while cleaning up.
5. Summarize clean, changed, or blocked coverage. Keep proven verification corrections together and prepare a PR only if the user requested one.

## Upstream sources

- Keep index and feature recipes in sync, exercise every mapped feature on a real instance, and classify drift. [pstack/maintain-verification-skill](https://github.com/cursor/plugins/blob/bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7/pstack/skills/maintain-verification-skill/SKILL.md#L23)
