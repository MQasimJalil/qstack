---
name: qstack-verify
description: Prove selected behavior using the normal entry point and save reviewable evidence tied to the exact input.
---

# Verify

Use the accepted plan and reviewed input. Start an isolated instance, wait for readiness, and drive the normal user path. Exercise application controls for user actions and use a fixture for external events with controlled timing.

For a modeled browser scenario, drive the recorded witness through the preview. If the verification is new or changed, confirm the same check catches the deliberately broken control. Keep the action sequence and observed result together. Use the browser trace and captured UI state for the user-visible result.

Record the model, source, check versions, reasons for selected checks, and links to their results. Treat a missing tool, missing observation, or changed input as incomplete evidence. Reuse completed checks for the same input. Clean up instances created by the run and preserve the evidence.
