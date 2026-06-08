# Resume Generation Workflow

Use this process every time you apply to a new job.

## 1. Read the Job Description

Extract:

- Role family (backend, frontend, full-stack, data, ML, etc.)
- Core tech stack required
- Key responsibilities
- Level (junior, mid, senior)
- Domain keywords (fintech, healthcare, e-commerce, etc.)

## 2. Research the Company

Before tailoring your resume, research:

- Company's product/service
- Recent company news or direction
- Likely engineering stack
- Team context if available

Use this research to refine:

- Experience selection
- Project selection
- Summary wording
- Skills section (from full company/team research)

## 3. Select Best-Fit Content

From your `master_resume_data.json`, select:

**Default target:**
- 5 experiences (or fewer if early career)
- 3 projects

**Rules:**
- Experiences stay in strict reverse chronological order
- Choose strongest fit experiences from your master data
- Use projects to patch fit gaps and strengthen stack/domain alignment

## 4. Start from the Locked Baseline

1. Copy `resume_template.tex` to your output folder
2. Reference `sample_resume.tex` for structure

**Rule:** Content changes per JD, formatting stays anchored to this baseline.

## 5. Tailor the Content

Customize for this specific job:

- **Summary** - Align with role type and company
- **Coursework** - Highlight relevant courses
- **Experience bullets** - `27-32` words each; match JD and research keywords
- **Skills section** - Build from full research (JD + product + news + stack + team); minimum `30` terms; put researched stack first
- **Project bullets** - `27-32` words each; emphasize relevant tech and impact

Keep:
- One page
- Consistent location formatting (e.g., "Los Angeles, CA")
- Readable spacing
- Strong JD keyword coverage

## 6. Compile and Visual QA

Compile your `.tex` file and check:

- [ ] Output is exactly one page
- [ ] No text overflow on right edge
- [ ] No awkward section gaps
- [ ] No cramped experience blocks
- [ ] No broken project spacing
- [ ] Locations and dates are consistent
- [ ] Skills section has at least 30 individual skill terms
- [ ] Experience and project bullets are each 27-32 words

## 7. Fix Wording First, Spacing Second

If it doesn't fit on one page, fix in this order:

1. Remove weak or redundant wording
2. Shorten bullets (target 27-32 words)
3. Verify skills section includes at least 30 individual skill terms
4. Only then touch spacing values

## 8. Save and Deliver

Recommended folder structure:
```
OUTPUT/
└── CompanyName/
    └── YYYY-MM-DD/
        ├── resume.tex
        └── resume.pdf
```

## Drift Check

If a future resume looks visually off:

1. Compare against `sample_resume.tex`
2. Check section gaps first
3. Check project-title-to-bullet spacing
4. Check location consistency
5. Only then tweak spacing macros
