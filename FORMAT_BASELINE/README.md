# Resume Format Baseline

This folder is the permanent source of truth for the current accepted resume formatting.

Purpose:

- preserve the exact one-page visual rhythm that was accepted in the FirmPilot resume
- provide a reusable LaTeX template for future resumes
- provide an exact sample file to compare against if spacing drifts
- document the future workflow for generating new resumes after a JD is shared

Use these files:

- `resume_template.tex`
  - clean reusable LaTeX shell with locked macros and spacing
- `firmpilot_reference_sample.tex`
  - exact accepted sample resume with the current formatting
- `FORMAT_LOCK.md`
  - locked spacing values and formatting rules
- `GENERATION_WORKFLOW.md`
  - the process to follow each time a new JD is shared

Source-of-truth rule:

- Start every future resume from `resume_template.tex`
- If a future resume looks visually off, compare it against `firmpilot_reference_sample.tex`
- Fix wording first, spacing second

Content targets (every resume):

- Experience bullets: `27-32` words each (`2` per role)
- Project bullets: `27-32` words each (`1` per project)
- Skills section: minimum `30` individual skill terms, selected from full company/team research

Visible location rule:

- If the JD has one clear city/state, use that JD city/state as the visible location throughout the generated resume.
- If the JD is multi-location, remote-only, or unclear, infer the main location from JD/team/company context when possible.
- If no stronger signal exists, use the company's main listed location, defaulting to the first listed location when necessary.

Location:

- This folder intentionally lives outside `/COMPANY`
- It is meant to be reusable across all future company-specific resumes
