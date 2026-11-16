---
name: qstack-make-pdf
description: "Render Markdown as a checked PDF or a related publication artifact."
---

# Make PDF

## Requirements

- Use a document renderer that supports the requested output format and the required diagram converters.

## Procedure

1. Read the Markdown, links, diagrams, and assets relative to the source. Decide whether the target is a memo, draft, or publication and apply the requested branding and page structure.
2. Use a renderer that respects code and headings, fits images to the content box, and supports page numbers and navigation. Render Mermaid or Excalidraw blocks with the available converter and make any parse error visible.
3. In strict mode, validate assets and fail for missing or unsupported files, remote references, or out-of-tree paths according to the chosen policy. A preview may identify failed assets without calling the result complete.
4. Render and inspect representative pages and every troublesome break. Deliver the PDF with stable links and include HTML or an editable document when requested and supported.

## Upstream sources

- Publication and draft modes, offline diagrams, image fitting, strict validation, and export options [gstack/make-pdf](https://github.com/garrytan/gstack/blob/5dcd76b4eae6bb06f73460d3ab29cef8e33e8537/make-pdf/SKILL.md#L190)
