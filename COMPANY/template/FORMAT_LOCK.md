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

- Section headers must be unnumbered (`Summary`, `Education`, etc.). Always include `\setcounter{secnumdepth}{0}` immediately after `\usepackage{titlesec}`.
- **Locked experience headers:** company name, job title, dates, and location come from `master_resume_data.json` and must not be renamed to match the target JD. Only bullets change per role.
- **Dated output folders:** use today's actual date in `YYYY-MM-DD(Position-Name_JobID)` — e.g. `mlb\2026-06-11(Associate-Software-Engineer-Web-Platform-Architecture)\` when generated on June 11, 2026.
- Keep locations consistent, e.g. `Los Angeles, CA`
- Keep bullets dense but readable; shorten wording before compressing spacing further
- Use `firmpilot_reference_sample.tex` as the visual truth source if a future template drifts
