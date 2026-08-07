# Format Lock

This file records the locked spacing and formatting values from the currently accepted baseline.

## Locked spacing values

- Section header rule: full-width `\rule{\linewidth}{0.4pt}` on its own line below each title via `[\color{black}\vspace{-3pt}\rule{\linewidth}{0.4pt}\vspace{-2pt}]` — **never use `\titlerule`** (causes line-through text overlap)
- Section spacing: `\titlespacing*{\section}{0pt}{6pt}{0pt}` — breathing room between prior section content and the next header
- Header to Summary: `\vspace{-16pt}`
- Summary bottom spacing: `\vspace{-6pt}`
- Education to Experience: `\vspace{-6pt}`
- Experience to Skills: `\vspace{-6pt}` (never exceed `-8pt`; overlap occurs at `-10pt` or tighter)
- Skills to Projects: `\vspace{-6pt}`
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

- Keep visible locations consistent with the JD city/state, e.g. `Los Angeles, CA`
- If the JD is multi-location, remote-only, or lacks one clear city/state, infer the main location from JD/team/company context when possible
- If no stronger signal exists, use the main listed company location, defaulting to the first listed location when necessary
- Keep the template on exactly one page
- Keep bullets dense but readable
- Shorten wording before increasing compression
- Preserve the current header/link structure
- Section headers must never overlap prior content; if overlap appears, reduce negative `\vspace` before `\section{}` before trimming content

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
4. Check JD-location consistency
5. Only then tweak spacing macros
