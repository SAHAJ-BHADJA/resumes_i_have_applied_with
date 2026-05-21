# Template Analysis

This document captures how the current LaTeX resume works so future tailoring stays inside the same visual envelope.

## Core Layout

- Document class: `article`
- Page size: `letterpaper`
- Font size: `10pt`
- Margin strategy is aggressive and intentionally tuned for dense one-page output.
- The template depends on negative vertical spacing in multiple places to compress sections tightly.

## Preamble Decisions

- `fullpage` with manual margin adjustments creates the dense one-page layout.
- `titlesec` is used to create compact section headers with a bottom rule.
- `tabularx` and fixed `tabular*` layouts drive alignment for experience, education, and project headers.
- `fontawesome5` provides link icons in the header.
- `glyphtounicode` and `\pdfgentounicode=1` preserve ATS readability.

## Spacing Behavior

- Header block ends with `\vspace{-20pt}` to reclaim whitespace.
- Summary is followed by `\vspace{-18pt}`.
- Education ends with `\vspace{-20pt}`.
- Experience and Projects use multiple local negative `\vspace` calls to keep entries compact.
- Bullets are compressed through:
  - `\item\small`
  - `\vspace{-2pt}` inside `\resumeItem`
  - `\resumeItemListEnd` ending with `\vspace{-5pt}`

## Section Macros

### `\resumeSubheading`

- Used for experience entries.
- Left column: company
- Right column: location
- Second row left: title
- Second row right: date range

### `\resumeEduSubheading`

- Used for education entries.
- Adds a third line for coursework.

### `\resumeProjectHeading`

- Used for projects.
- Left side contains project name, link, and tech stack.
- Right side is usually empty in current usage.

## Practical Consequences

- Experience is the vertical budget bottleneck.
- Skills section is dense but efficient.
- Projects consume more height than skills because each project uses a heading plus a bullet list.
- Summary must stay short or it will crowd out experience/projects.

## Safe Adjustments

- Reorder sections if needed.
- Adjust local `\vspace` values.
- Shorten or expand bullets.
- Reduce project count to preserve stronger experience coverage.

## Unsafe Adjustments

- Changing font family
- Changing `10pt`
- Expanding margins
- Letting the resume spill to page 2
- Adding verbose multi-line summaries

