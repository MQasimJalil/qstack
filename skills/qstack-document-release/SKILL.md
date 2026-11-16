---
name: qstack-document-release
description: "Audit release documentation against the exact changes that will ship."
---

# Document Release

## Procedure

1. Resolve the release base and candidate revision. Include selected working changes when the release workflow owns them. Inventory additions, renames, removals, and behavior changes in public APIs, flags, configuration, and user workflows.
2. Map each public change to its reference, guide, tutorial, and explanation coverage. Trace obsolete names in diagrams and cross-links to their current implementation.
3. Read the affected documents in full. Correct existing claims, commands, examples, changelog text, and diagrams while preserving unrelated entries. Record substantial missing pages as separate work.
4. Check cross-document consistency and release readiness. Report reviewed and changed documents, coverage gaps, remaining debt, and any version decision the release owner needs.

## Upstream sources

- Release diff coverage map by documentation purpose and discovered debt [gstack/document-release](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/document-release/SKILL.md#L247)
