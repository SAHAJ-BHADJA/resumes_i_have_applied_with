# Format Lock

This file records the locked spacing and formatting values from the currently accepted baseline.

## Locked spacing values

- Header to Summary: `\vspace{-18pt}`
- Summary bottom spacing: `\vspace{-16pt}`
- Education to Experience: `\vspace{-14pt}`
- Experience to Skills: `\vspace{-14pt}`
- Skills to Projects: `\vspace{-16pt}`
- `\resumeSubheading` tail spacing: `\vspace{-2pt}`
- `\resumeEduSubheading` tail spacing: `\vspace{-4pt}`
- `\resumeProjectHeading` tail spacing: `\vspace{-2pt}`
- `\resumeItemListEnd`: `\vspace{-4pt}`
- `\resumeProjItemListEnd`: `\vspace{-4pt}`
- Between project entries: `\vspace{3pt}`

## Locked list settings

- `\resumeItemListStart`
  - `leftmargin=0.15in`
  - `label=\textbullet`
  - `itemsep=2pt`
  - `topsep=0pt`
  - `parsep=0pt`
  - `partopsep=0pt`
- `\resumeProjItemListStart`
  - `leftmargin=0.15in`
  - `label=\textbullet`
  - `itemsep=0pt`
  - `topsep=0pt`
  - `parsep=0pt`
  - `partopsep=0pt`

## Formatting rules

- Keep locations consistent, e.g. `Los Angeles, CA`
- Keep the template on exactly one page
- Keep bullets dense but readable
- Shorten wording before increasing compression
- Preserve the current header/link structure
- Use the same visual style for section rules and typography

## Content rules that pair with this format

- Default target: `Summary + Education + 5 Experiences + Skills + 3 Projects`
- Experience order must be strict reverse chronological
- Default bullets:
  - `2` bullets per experience
  - `1` bullet per project
- Bullet target length:
  - `27-32` words for every experience and project bullet
- Skills section:
  - minimum `30` individual skill terms (not counting category headers)
  - terms selected and ordered from full company/team research, not JD-only

## Drift check

If a future resume looks off:

1. Compare against `firmpilot_reference_sample.tex`
2. Check section gaps first
3. Check project-title-to-bullet spacing
4. Check location consistency
5. Only then tweak spacing macros
