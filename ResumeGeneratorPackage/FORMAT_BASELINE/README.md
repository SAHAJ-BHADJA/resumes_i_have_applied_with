# Resume Format Baseline

This folder is the permanent source of truth for the accepted resume formatting.

## Purpose

- Preserve the exact one-page visual rhythm that works for ATS and human reviewers
- Provide a reusable LaTeX template for all future resumes
- Provide a sample file to compare against if spacing drifts
- Document the workflow for generating new resumes

## Files

| File | Purpose |
|------|---------|
| `resume_template.tex` | Clean reusable LaTeX shell with locked macros and spacing |
| `sample_resume.tex` | Example resume with placeholder content showing proper structure |
| `FORMAT_LOCK.md` | Locked spacing values and formatting rules - don't change these |
| `GENERATION_WORKFLOW.md` | Step-by-step process to follow for each new job application |

## How to Use

1. **Start every resume from `resume_template.tex`** - Never start from scratch
2. **Reference `sample_resume.tex`** - See how content should be structured
3. **Follow `GENERATION_WORKFLOW.md`** - For each new application
4. **Consult `FORMAT_LOCK.md`** - If something looks visually off

## Source-of-Truth Rule

- Start every future resume from `resume_template.tex`
- If a resume looks visually off, compare it against `sample_resume.tex`
- Fix wording first, spacing second

## Important

This folder is meant to be reusable across all future company-specific resumes. Don't modify these files for individual applications - copy them to your output folder instead.
