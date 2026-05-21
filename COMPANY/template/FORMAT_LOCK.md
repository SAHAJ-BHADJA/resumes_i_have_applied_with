# Resume Format Lock

This folder preserves the current known-good one-page formatting baseline.

Use these files:

- `resume_template.tex`
  - clean reusable template with locked spacing macros
- `firmpilot_reference_sample.tex`
  - exact reference sample that produced the current accepted visual result

Locked spacing values:

- Summary top spacing after header: `\vspace{-18pt}`
- Summary bottom spacing: `\vspace{-16pt}`
- Education to Experience gap: `\vspace{-14pt}`
- Experience to Skills gap: `\vspace{-14pt}`
- Skills to Projects gap: `\vspace{-16pt}`
- `\resumeSubheading` tail spacing: `\vspace{-2pt}`
- `\resumeEduSubheading` tail spacing: `\vspace{-4pt}`
- `\resumeProjectHeading` tail spacing: `\vspace{-2pt}`
- `\resumeItemListEnd`: `\vspace{-4pt}`
- `\resumeProjItemListEnd`: `\vspace{-4pt}`
- Between projects: `\vspace{3pt}`

Formatting notes:

- Keep locations consistent, e.g. `Los Angeles, CA`
- Keep bullets dense but readable; shorten wording before compressing spacing further
- Use `firmpilot_reference_sample.tex` as the visual truth source if a future template drifts
