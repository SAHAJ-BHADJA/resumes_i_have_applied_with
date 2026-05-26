# Resume Generator System

A professional LaTeX-based resume generation system with locked formatting and a structured workflow for creating tailored, one-page resumes.

## What's Included

```
ResumeGeneratorPackage/
├── README.md                        # This file - getting started guide
├── SETUP_GUIDE.md                   # Detailed setup instructions
├── master_resume_data_TEMPLATE.json # Template for your resume data
├── FORMAT_BASELINE/
│   ├── README.md                    # Format baseline documentation
│   ├── GENERATION_WORKFLOW.md       # Step-by-step resume generation process
│   ├── FORMAT_LOCK.md               # Locked spacing and formatting values
│   ├── resume_template.tex          # Clean LaTeX template to start from
│   └── sample_resume.tex            # Example resume with placeholder content
└── OUTPUT/                          # Your generated resumes go here
    └── .gitkeep
```

## Quick Start

1. **Set up LaTeX** - Install a LaTeX distribution (see `SETUP_GUIDE.md`)
2. **Fill your data** - Copy `master_resume_data_TEMPLATE.json` to `master_resume_data.json` and add your info
3. **Generate a resume** - Follow `FORMAT_BASELINE/GENERATION_WORKFLOW.md` for each job application

## How It Works

1. You maintain ONE master data file (`master_resume_data.json`) with ALL your experiences, projects, and skills
2. For each job application, you select the best-fit content from your master data
3. You tailor the wording to match the job description
4. The locked formatting ensures every resume looks professional and fits on one page

## Key Principles

- **Content changes per JD, formatting stays locked** - Don't touch spacing unless absolutely necessary
- **Fix wording first, spacing second** - If it doesn't fit, shorten bullets before adjusting spacing
- **Keep it to one page** - The format is optimized for a dense, readable single page

## Requirements

- LaTeX distribution (TeX Live, MiKTeX, or Overleaf)
- Required packages: `latexsym`, `fullpage`, `titlesec`, `enumitem`, `hyperref`, `fancyhdr`, `fontawesome5`

See `SETUP_GUIDE.md` for detailed installation instructions.
