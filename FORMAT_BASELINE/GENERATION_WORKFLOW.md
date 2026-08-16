# Future Resume Generation Workflow

Use this process every time a new JD is shared.

## 1. Read the JD

Extract:

- role family
- core stack
- responsibilities
- level
- domain keywords
- job location details (city/state, remote, or multi-location)

## 2. Do company and team research first

**This step is mandatory. Do not skip to resume generation.**

### What to research

| Area | What to find |
|------|--------------|
| **Company product** | What do they build/sell? Who are their customers? B2B or B2C? |
| **Domain** | Industry vertical (fintech, healthcare, defense, SaaS, etc.) |
| **Recent direction** | News, acquisitions, pivots, funding rounds, product launches |
| **Engineering stack** | Languages, frameworks, cloud providers, databases they actually use |
| **Team context** | Team size, engineering culture, what problems they're solving |

### Where to research

- **Company website** - About page, careers page, product pages
- **LinkedIn** - Company page, engineering team profiles, job posts
- **Glassdoor** - Interview reviews, tech stack mentions
- **Web search** - "[Company] engineering blog", "[Company] tech stack", "[Company] news 2026"
- **GitHub** - Public repos, open source contributions
- **Crunchbase** - Funding, company size, investors
- **News** - TechCrunch, industry publications

### How to apply research

Use findings to refine:

| Resume section | How research informs it |
|----------------|------------------------|
| **Experience selection** | Prioritize experiences matching their domain (e.g., healthcare company → emphasize HMIS) |
| **Project selection** | Choose projects that patch stack/domain gaps |
| **Summary wording** | Use their language, mention relevant domain experience |
| **Skills section** | Build from full research (JD + product + news + stack + team); minimum 30 terms; put researched stack first |
| **Bullet phrasing** | Mirror their terminology, emphasize relevant impact |

### Research output checklist

Before proceeding to Step 3, confirm you know:

- [ ] What the company's core product/service is
- [ ] What industry/domain they operate in
- [ ] Their likely tech stack (beyond JD mentions)
- [ ] Recent company news or direction
- [ ] What the specific team/role focuses on

## 3. Select best-fit resume content

Default target:

- `5` experiences
- `3` projects

Rules:

- experiences stay in strict reverse chronological order
- choose the strongest fit from `E:\Projects\Random\master_resume_data.json`
- use projects to patch fit gaps and strengthen stack/domain alignment

### Mandatory selection rationale

For every generated resume, provide a concise post-generation selection report in chat. The report must:

- name every selected experience and state the JD-specific evidence that earned its place
- name every selected project and state the stack, domain, responsibility, or evidence gap it covers
- identify each credible non-selected experience and project and explain why it ranked below the selected alternatives
- compare alternatives directly; do not use generic explanations such as "less relevant"
- mention constraints that affected selection, including recency, strict chronology, evidence strength, duplication, link availability, and the fixed `5` experience / `3` project target
- keep all reasoning outside the resume PDF unless the user explicitly requests it inside the document

## 4. Start from the locked baseline

Files:

- `resume_template.tex`
- `firmpilot_reference_sample.tex`

Rule:

- content changes per JD
- formatting stays anchored to this baseline unless there is a specific layout problem
- section headers must be unnumbered (`Summary`, `Education`, etc.); always include `\setcounter{secnumdepth}{0}` immediately after `\usepackage{titlesec}`

## 5. Tailor the content

Rewrite:

- summary
- coursework
- experience bullets (`27-32` words each)
- skills section (minimum `30` individual skill terms, built from full company/team research); place each skill category on its own line
- project bullets (`27-32` words each)

Project links:

- Make the **project title itself clickable** with `\href{<verified-url>}{\textbf{<project-name>}}`.
- Add a clickable `Live` or `Code` label immediately beside the project title using `\resumeProjectLink{<verified-url>}{Live}` or `\resumeProjectLink{<verified-url>}{Code}`.
- The `Live` or `Code` label must render **red and underlined**.
- Use `Live` for a verified deployed application URL and `Code` for a verified repository-only URL.
- Use only project URLs verified in `master_resume_data.json`.

**Never change (locked from `master_resume_data.json`):**

- experience **company names**
- experience **job titles** (e.g. USC Dornsife stays `Software Engineer`, not the target JD title)
- experience **dates** unless correcting a factual error in master data

### Location rule

- Preserve every experience and education location exactly as supported by `master_resume_data.json`.
- Never replace historical work-experience locations with the JD location.
- Use the JD location only for job-targeting decisions and optional application metadata, not as an experience-location override.

Tailor JD fit through bullet wording, summary, skills, coursework, and project selection only.

Keep:

- one page
- location consistency using the selected primary JD/company location
- readable spacing
- strong JD keyword coverage

## 6. Compile, clean up, and visually QA

Compile with `pdflatex`, then **delete all non-PDF artifacts** from the company output folder:

- remove `*.tex`, `*.aux`, `*.log`, `*.out` (and any other LaTeX build files)
- **keep only** `Sahaj_Bhadja_Resume.pdf` (or versioned `Sahaj_Bhadja_Resume_v2.pdf`, etc.)

The company folder is PDF-only. Do not leave source or build files there.

Check:

- one-page output
- no right-edge overflow
- no awkward section gaps
- no cramped experience block
- no broken projects spacing
- no inconsistent locations/dates
- skills section has at least 30 individual skill terms
- experience and project bullets are each 27-32 words
- folder contains **only** the final PDF

## 7. Fix wording first, spacing second

Preferred order:

1. remove weak wording
2. shorten bullets (stay within `27-32` words when possible)
3. verify skills section has at least `30` terms
4. only then touch spacing

## 8. Save to the correct folder

Output root:

- `E:\Projects\Random\Resume\COMPANY\<company-name>\<folder-name>\`

Folder name pattern:

- `YYYY-MM-DD(Position-Name_JobID)`

Rules:

- `YYYY-MM-DD` = **today's actual calendar date** on the day the resume is generated (not a fixed placeholder). If generating on June 11, 2026, the folder must start with `2026-06-11`.
- `Position-Name` = JD title sanitized (spaces → hyphens, remove special characters)
- `JobID` = requisition / job / JR code from the posting (e.g. `350393`, `JR2013065`)
- If the JD has no job ID, omit the underscore suffix: `YYYY-MM-DD(Position-Name)`
- Company folder stays lowercase; spaces in company names are allowed
- Each new generation day gets its own dated folder; do not reuse `2026-06-01` unless that is actually today's date

Examples:

- `mlb\2026-06-11(Associate-Software-Engineer-Web-Platform-Architecture)\`
- `Deloitte-Cyber\2026-06-11(Cyber-Full-Stack-Software-Engineer_350393)\`
- `nvidia\2026-06-08(Formal-Verification-Engineer-New-College-Grad-2026_JR2013065)\`

PDF filename stays:

- `Sahaj_Bhadja_Resume.pdf`

If the same company + folder already has a PDF and you are regenerating, version the PDF:

- `Sahaj_Bhadja_Resume_v2.pdf`

## 9. Deliver

Return:

- final PDF path using the folder pattern above
- confirm the output folder contains **only** the PDF
- provide the mandatory selected-versus-not-selected experience and project rationale

## Baseline rule

If the future resume drifts visually, compare it against `firmpilot_reference_sample.tex` and bring it back into alignment.
