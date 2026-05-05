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

`E:\Projects\Random\Resume\<company-lowercase>\<YYYY-MM-DD>\`

Filename pattern:

`Sahaj_Bhavesh_Bhadja.pdf`

If a second resume is generated for the same company on the same date, use:

`Sahaj_Bhavesh_Bhadja_v2.pdf`

## Note

The current machine does not have `pdflatex` available on PATH, so PDF rendering will require a LaTeX distribution to be installed or exposed before the render script can succeed.
