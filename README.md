# Resume Framework

This folder contains the reusable resume framework for JD-tailored one-page resumes.

## Files

- `RESUME_RULES.md`
  - strict tailoring rules and output conventions
- `TEMPLATE_ANALYSIS.md`
  - detailed analysis of the current one-page LaTeX structure
- `template/resume_template.tex`
  - exact reusable template shell with the current visual identity
- `scripts/render_pdf_only.py`
  - compiles a TeX file and stores only the PDF in the company/date folder

## Output Convention

Generated PDFs must go to:

`E:\Projects\Random\Resume\COMPANY\<company-lowercase>\<YYYY-MM-DD(Position-Name_JobID)>\`

Filename pattern:

`Sahaj_Bhavesh_Bhadja.pdf`

If additional resumes are generated for the same company on the same date, use:

`Sahaj_Bhavesh_Bhadja_v2.pdf`

and increment (`_v3`, `_v4`, ...).

## Note

The current machine does not have `pdflatex` available on PATH, so PDF rendering will require a LaTeX distribution to be installed or exposed before the render script can succeed.

## Resume Ordering Rule

Experience entries must always be listed in strict reverse-chronological order:

- newest role first
- then older roles in date order

## Visible Location Rule

- If a JD provides one clear city/state, use that JD city/state as the visible location in the generated resume.
- If a JD is multi-location, remote-only, or unclear, infer the main location from JD/team/company context when possible.
- If no stronger signal exists, use the company's main listed location, defaulting to the first listed location when necessary.
