# Resume Autopilot Guide

This file is the complete operating manual for generating Sahaj Bhadja's tailored resumes in this repository.

It is written for another coding model or coding agent such as Cursor, Windsurf/Cascade, Claude Code, or any other agentic IDE assistant.

If you follow this guide exactly, you should be able to take only:

1. a `company name`
2. a `job description`

and produce a resume in the same style, structure, and quality bar as the resumes already generated in this workspace.

This is intentionally detailed. It is meant to remove ambiguity.

## Goal

Generate a tailored, one-page PDF resume for Sahaj Bhadja that:

- matches the job description aggressively
- preserves the existing LaTeX visual style
- keeps the candidate identity consistent
- is ATS-dense but still readable
- fits exactly on one page
- is saved to the correct company/date folder with the correct versioning


This workflow is not just about swapping projects. It includes rewriting summary, coursework, experience bullets, skills, and projects to align with the JD while staying coherent.

## Repository Context

Root:

- `E:\Projects\Random`

Primary files:

- Master data: [master_resume_data.json](E:/Projects/Random/master_resume_data.json)
- Rules: [RESUME_RULES.md](E:/Projects/Random/Resume/RESUME_RULES.md)
- This guide: [RESUME_AUTOPILOT_GUIDE.md](E:/Projects/Random/Resume/RESUME_AUTOPILOT_GUIDE.md)
- LaTeX template: [resume_template.tex](E:/Projects/Random/Resume/template/resume_template.tex)
- PDF renderer: [render_pdf_only.py](E:/Projects/Random/Resume/COMPANY/scripts/render_pdf_only.py)

## What The Agent Receives

The user typically provides:

- company name
- job description

The agent is expected to do everything else.

Do not ask the user to manually decide:

- which experiences to use
- which projects to use
- how to order sections
- whether to use one or two bullets
- how to fit to one page

Those decisions should be made automatically using this guide.

## High-Level Workflow

For every new resume request:

1. Read the JD carefully.
2. Identify the role family and infer the likely team/product area from JD clues.
3. Extract the JD location details and determine whether the posting has one clear city/state.
4. Research team-specific stack, responsibilities, and recent initiatives where available.
5. Research company priorities, current products, and recent news/engineering direction.
6. Select the best 5 experiences using JD + external research context.
7. Select the best 3 projects using JD + external research context.
8. Rewrite summary, coursework, bullets (`27-32` words each), and skills (minimum `30` terms).
9. Provide explicit rationale for selected experiences/projects and why they were chosen over non-selected options.
10. If gaps remain, create a short list of unverified enhancement bullets and get explicit user confirmation.
11. Update `master_resume_data.json` with confirmed enhancements only.
12. Create a temporary `.tex` file in the Resume root.
13. Compile it with the renderer.
14. Verify it is exactly one page.
15. Render a preview image and visually inspect layout quality.
16. Fix any layout or chronology issues.
17. Delete the temporary `.tex` and preview image.
18. Return the PDF path to the user.

Do not stop after drafting. The workflow is only complete after:

- PDF exists
- page count is `1`
- layout is visually checked
- temp artifacts are cleaned up

## Required Output Location

All resumes must be saved under:

- `E:\Projects\Random\Resume\COMPANY\<company-lowercase>\<YYYY-MM-DD(Position-Name_JobID)>\`

Examples:

- `E:\Projects\Random\Resume\COMPANY\seatgeek\2026-06-01(Software-Engineer-New-Grad)\`
- `E:\Projects\Random\Resume\COMPANY\deloitte-cyber\2026-06-01(Cyber-Full-Stack-Software-Engineer_350393)\`
- `E:\Projects\Random\Resume\COMPANY\nvidia\2026-06-08(Formal-Verification-Engineer-New-College-Grad-2026_JR2013065)\`

Folder naming:

- `Position-Name` = sanitized JD title (hyphens, no special chars)
- `JobID` = requisition / JR code when available; omit `_JobID` if not in posting

Rules:

- company folder name must be lowercase
- spaces in company names are allowed
- after compile, delete `*.tex`, `*.aux`, `*.log`, `*.out` from the company output folder
- final deliverable in the folder is **only** the PDF

## File Naming Rules

Base filename must always be:

- `Sahaj_Bhavesh_Bhadja.pdf`

If the same company/date already has a generated PDF, use versioning:

- `Sahaj_Bhavesh_Bhadja_v2.pdf`
- `Sahaj_Bhavesh_Bhadja_v3.pdf`
- and so on

Never invent other filename patterns.

## Temporary Working File Rules

Draft LaTeX files should be created in:

- `E:\Projects\Random\Resume\temp_<company>_<date>.tex`

Examples:

- `E:\Projects\Random\Resume\temp_aura_2026-04-23.tex`
- `E:\Projects\Random\Resume\temp_salesforce_2026-04-22.tex`

After successful generation and QA:

- delete the temp `.tex`
- delete preview images used for inspection

## Renderer Command

Use this exact script:

- [render_pdf_only.py](E:/Projects/Random/Resume/COMPANY/scripts/render_pdf_only.py)

Command pattern:

```powershell
python "E:\Projects\Random\Resume\COMPANY\scripts\render_pdf_only.py" --company "<company-lowercase>" --date YYYY-MM-DD --tex "E:\Projects\Random\Resume\temp_<company>_<date>.tex" --name Sahaj_Bhavesh_Bhadja
```

Example:

```powershell
python "E:\Projects\Random\Resume\COMPANY\scripts\render_pdf_only.py" --company "aura" --date 2026-04-23 --tex "E:\Projects\Random\Resume\temp_aura_2026-04-23.tex" --name Sahaj_Bhavesh_Bhadja
```

## Mandatory PDF Verification

Always verify page count after rendering.

Use Python:

```powershell
@'
from pypdf import PdfReader
from pathlib import Path
p = Path(r'E:\Projects\Random\Resume\aura\2026-04-23\Sahaj_Bhavesh_Bhadja.pdf')
print(len(PdfReader(str(p)).pages))
'@ | python -
```

Required result:

- exactly `1`

If page count is `2`, fix the layout and rerender.

## Mandatory Visual QA

Do not trust page count alone.

Always render a preview image and visually inspect:

- right-edge overflow
- cramped experience bullets
- cramped project bullets
- uneven whitespace distribution
- chronology mistakes
- education/location lines running out of page bounds
- incorrect or mixed visible location text for a single-location JD
- obviously over-compressed sections

Preview generation pattern:

```powershell
@'
import fitz
from pathlib import Path
pdf = Path(r'E:\Projects\Random\Resume\aura\2026-04-23\Sahaj_Bhavesh_Bhadja.pdf')
out = Path(r'E:\Projects\Random\Resume\aura\2026-04-23\preview.png')
doc = fitz.open(pdf)
pix = doc[0].get_pixmap(matrix=fitz.Matrix(1.5,1.5), alpha=False)
pix.save(out)
print(out)
'@ | python -
```

Then inspect the preview image.

Delete the preview after the resume is accepted.

## Non-Negotiable Identity Rules

These must never change:

- display name: `Sahaj Bhadja`
- base filename: `Sahaj_Bhavesh_Bhadja`
- email in header: `bhadja@usc.edu`
- phone in header
- LinkedIn in header
- GitHub in header
- portfolio in header

Never remove header links.

## Banned Content

Never include:

- `USC Annenberg Media`

No exceptions.

## Template Constraints

You must preserve the existing visual identity.

From the template:

- LaTeX class: `article`
- page size: `letterpaper`
- font size: `10pt`
- font family: preserve current defaults

Do not:

- switch to another template
- change the font family
- increase font size
- make it multi-page

Minor spacing changes are allowed and expected.

Bullet rendering requirement:

- Resume bullets must render as `•` consistently.
- In LaTeX macros, set explicit itemize labels (for example, `label=\textbullet`) in the list definitions used by experience/project bullets.
- Do not rely on default itemize markers, which can fallback to dashes in some renders.

## Default Section Order

Unless the user explicitly changes it, use:

1. `Summary`
2. `Education`
3. `Experience`
4. `Skills`
5. `Projects`

This is the user’s preferred default and should be respected.

## Experience Count Rules

Default target:

- `5` experiences when the page can support it cleanly

Minimum:

- `4` experiences

If `5` fits and improves relevance, use `5`.

Do not arbitrarily drop to `4` if there is still space on the page.

## Experience Order Rules

This is strict:

- all experience entries must be in strict reverse-chronological order (newest first)
- order must be based on actual dates only
- do not group roles out of order because they “fit better”
- do not reorder for narrative flow, technology grouping, or company preference
- if dates overlap, list the role with the latest start date first

Example of correct ordering:

1. USC Dornsife
2. Grad8
3. USC AD Labs
4. Aasma SecureSync
5. Aasma VibrantChem

If a later-dated research role exists, it must not be placed after older industry roles.

## Visible Location Rules

For generated resumes in this repository:

- If the JD provides **one clear city/state**, use that **exact JD city/state** as the visible location shown in the resume.
- Apply that visible location consistently across the resume instead of mixing historical per-role locations.
- This is a **display rule only**. Do not modify the underlying company names, titles, or dates stored in `master_resume_data.json`.
- If the JD is **multi-location**, **remote-only**, or does **not** provide one clear city/state, infer the **main location** from JD team clues, product context, org context, or company/team research.
- If no single main location can be inferred from team/JD context, use the company's **main listed location**.
- When multiple locations are listed and there is no stronger signal, default to the **first listed location** as the visible location.
- Only ask the user if there is still no defensible main location after those steps.

Examples:

- Single-location JD: use `Minneapolis, MN` consistently in the generated resume.
- Multi-location JD: infer the main location from team/company context; otherwise use the first listed location.
- Remote JD: infer the main location from team/company context; otherwise use the company's main listed location.

## Bullet Count Rules

Every included work experience should have:

- `2` bullets

That is the default user preference and should be followed unless there is a very strong reason not to.

Avoid:

- single-bullet experiences
- 3-bullet experiences unless absolutely necessary

Project bullets:

- Prefer `1` bullet per selected project in concise one-page mode.
- Keep each project bullet between `27 to 32` words.

Bullet wording and emphasis:

- Keep each experience bullet between `27 to 32` words.
- Bold JD-critical keywords in both experience and project bullets (technology, domain terms, metrics, and impact words) where natural and readable.

## Education Rules

Always include both education entries.

Always include:

- degree
- date range
- GPA
- coursework

### Education Entries

1. University of Southern California
2. Pandit Deendayal Energy University

### Education Layout Rules

This is a known failure mode:

- long location strings can overflow off the right edge

Therefore:

- always visually inspect the education row
- shorten degree wording if needed
- abbreviate degree names if needed
- adjust the education row formatting if needed

Examples of acceptable abbreviations:

- `Master of Science in Computer Science` -> `M.S. in Computer Science`
- `Bachelor of Technology in Computer Science and Engineering` -> `B.Tech. in Computer Science and Engineering`
- `Object-Oriented Programming` -> `OOP` if space is tight

The goal is:

- no overflow
- still readable

## Skills Section Rules

The user does not want the skills section to be too thin.

### Skills Selection From Full Research

Skills are **not** chosen from the JD alone or from `master_resume_data.json` alone.

Build the `Skills` section from the **same full research package** used to select experiences and projects:

- job description keywords
- company product and domain
- recent company news and direction
- confirmed or likely engineering stack
- team responsibilities and platform conventions

Then:

1. List researched must-have and high-signal skills first.
2. Add credible adjacent skills supported by the candidate's background.
3. Fill to at least 30 terms using remaining defensible skills from `master_resume_data.json`.
4. Order categories and terms so the section reads like a direct match to that company/team.

### Minimum Skills Count

- Include a **minimum of 30 skills** in the `Skills` section on every resume.
- Start every skill category on a new line; do not run multiple category headers together in one paragraph.
- Count individual skill terms (languages, frameworks, tools, platforms, practices), not category headers.
- Do not pad with nonsense or unrelated buzzwords just to hit 30.

Start from this dense baseline structure:

- Languages
- Backend & APIs
- Frontend
- Databases
- Cloud & Infrastructure
- AI/ML
- Engineering Practices

Then tailor within that structure.

You may:

- reorder categories
- rename a category slightly if it helps
- swap weaker items for stronger JD-aligned ones
- add adjacent technologies when justified

You should not:

- collapse the skills section into a tiny 2-line dump
- deliver fewer than 30 skills unless the user explicitly overrides this rule
- remove major categories unless the JD truly makes them irrelevant and space is impossible

### Adjacent Skills Rule

If the JD says something like:

- “experience with X or similar technologies”

then it is acceptable to surface adjacent technologies in `Skills` when they are credibly supported by the candidate’s background.

Examples:

- event-driven systems -> Kafka-adjacent
- large-scale pipelines -> Flink-adjacent
- backend/distributed services -> Golang-adjacent

Do not invent nonsense. Keep it defensible.

## Layout Quality Rules

These are hard requirements.

### General

- no text may overflow off the page
- spacing should feel balanced across sections
- the page should look intentional, not randomly compressed
- when the JD has one clear city/state, the visible resume location should match it consistently

### Readability Preference

Once ATS coverage and one-page fit are satisfied:

- prefer readability over maximal compression

### What Not To Do

Do not create a page where:

- experience is extremely tight
- projects have visible spare space
- one section is visually jammed while another breathes too much

### Corrective Rule

If a section is too cramped:

1. shorten bullet text first
2. simplify wording
3. reduce redundant adjectives
4. then rebalance spacing

Do not immediately solve everything by collapsing vertical space harder.

### Project Section Readability

If projects are visually jammed:

- add breathing room between project entries
- shorten the project bullets
- reclaim space elsewhere

### Experience Section Readability

If experience bullets are wrapping too tightly:

- shorten the bullet text
- remove repeated technology words
- compress phrasing
- only then adjust vertical spacing

## Tailoring Philosophy

The resume is not produced by only swapping projects.

You should actively tailor:

- summary
- education coursework
- selected experiences
- bullet wording
- metrics emphasis
- skills section
- projects

This means:

- choose relevant experiences
- rewrite bullets for the role family
- emphasize different technologies depending on the JD
- change the framing of the same role for different companies

Additionally:

- Bold JD-critical keywords in finalized bullets (core stack, role-specific domain terms, impact terms, and metrics) while preserving readability.

## Truthfulness Boundary

The user prefers aggressive tailoring.

You may:

- reframe bullet emphasis
- compress multiple real tasks into a sharper bullet
- introduce coherent metrics when they remain believable
- use alternate truthful role phrasing where already permitted

You may not:

- invent absurdly fake experience
- create obviously fabricated systems unrelated to the master data
- claim a company, role, or core tech stack with no basis

### User-Confirmed Enhancement Protocol

When the user indicates they have done additional relevant work not yet captured in `master_resume_data.json`:

1. Draft candidate bullets as **unverified enhancements** based on the existing project/work story.
2. Ask the user to confirm each enhancement.
3. Include only confirmed enhancements in the resume.
4. Persist confirmed details into `master_resume_data.json` for future resumes.
5. Never include unverified enhancements as facts.

## Master Data Structure

Primary source:

- [master_resume_data.json](E:/Projects/Random/master_resume_data.json)

Important top-level keys:

- `personal`
- `summary`
- `education`
- `experience`
- `skills`
- `projects`

Experience is nested under:

- `experience.active_roles`
- `experience.other_roles`

Use those sections, not a flat `experience` list.

## Important Experience Entries

These are the most commonly used roles.

### USC Dornsife

Use for:

- backend
- data engineering
- AI systems
- multi-tenant architecture
- SQL-heavy roles
- platform roles

Common signals:

- Azure SQL
- PostgreSQL
- SQL Server
- FastAPI
- cloud storage
- validation workflows
- production reliability

### Grad8

Use for:

- AI application roles
- edtech roles
- full-stack product roles
- user-facing AI workflows
- OCR / LLM integration

Common signals:

- Flask
- React
- multimodal LLMs
- MySQL / AWS RDS
- CI/CD
- production usage

### USC AD Labs

Use for:

- research software
- simulation
- Python
- ML systems
- experimental workflows
- scientific or technical environments

### Aasma Technology Solutions - SecureSync

Use for:

- enterprise backend
- integration-heavy roles
- CI/CD
- testing
- microservices
- AWS Glue / S3
- OOP
- API troubleshooting

### Aasma Technology Solutions - VibrantChem

Use for:

- full-stack roles
- web application roles
- microservices
- REST APIs
- WebSockets
- deployment automation

### LST Capitals

Use for:

- fintech
- payments
- cross-platform apps
- client-facing integration work
- Flask API
- Firebase sync
- architecture / workflow mapping

## Common Project Entries

### Chat2SQL

Use for:

- Java roles
- SQL roles
- developer tooling
- enterprise data tooling
- backend/full-stack roles

Common signals:

- Java
- TypeScript
- SQL
- Maven
- Docker
- multi-database support

### Big-Brain

Use for:

- AI product roles
- semantic search
- cloud pipelines
- retrieval
- LLM application roles

### FinNexus

Use for:

- fintech
- user-facing product roles
- high-volume workflows
- secure transaction platforms

### HMIS

Use for:

- workflow systems
- healthcare
- monitoring-backed ops flows
- structured APIs and CRUD systems

### CPU-Scheduling Simulator

Use for:

- C++
- systems
- algorithms
- educational software
- debugging / instrumentation

### PiXMod

Use for:

- AI SaaS
- product design
- polished UI
- subscription flows
- modern full-stack AI product roles

## Role Family Mapping

Use this to decide what to emphasize.

### Backend / Platform

Prioritize:

- USC Dornsife
- Aasma SecureSync
- Grad8
- Chat2SQL
- Big-Brain

Emphasize:

- APIs
- SQL
- cloud
- ETL
- reliability
- scaling

### Full-Stack Product

Prioritize:

- Grad8
- Aasma VibrantChem
- LST Capitals
- USC Dornsife
- PiXMod / FinNexus

Emphasize:

- React
- TypeScript
- Flask / Node
- UX workflows
- end-to-end ownership

### AI / Applied LLM

Prioritize:

- USC Dornsife
- Grad8
- Big-Brain
- CaptionCraft
- PiXMod

Emphasize:

- LLM workflows
- prompt-oriented systems
- multimodal models
- retrieval
- production AI features

### Research / Scientific / Systems

Prioritize:

- USC AD Labs
- USC Dornsife
- CPU-Scheduling Simulator
- Chat2SQL
- Aasma SecureSync

Emphasize:

- Python
- Java
- C++
- Linux
- testing
- simulation
- documentation

### Solutions / Forward Deployed / Client-Facing Technical

Prioritize:

- LST Capitals
- Aasma SecureSync
- USC Dornsife
- Grad8
- Big-Brain

Emphasize:

- requirements gathering
- integration mapping
- implementation lifecycle
- troubleshooting
- documentation
- technical communication

## Summary Writing Rules

Summary must always be included.

Target:

- 1 to 2 lines

Should include:

- role family
- years of experience
- strongest technologies for the JD
- 3 to 5 high-value keywords

Avoid:

- generic fluff
- “hardworking team player”
- vague statements without signal

## Coursework Tailoring Rules

Coursework should be slightly tailored by JD.

Examples:

- backend/data roles -> `Analysis of Algorithms`, `Database Systems`, `Web Technologies`
- systems roles -> `Analysis of Algorithms`, `Operating Systems`, `Software Engineering`
- AI roles -> may keep `Advanced NLP` if space allows

If space is tight:

- shorten coursework names
- use fewer items

## Editing Rules For The Agent

When modifying files in this repo:

- prefer editing by patch
- do not create random temp files outside the Resume workflow
- do not overwrite user files destructively

For resume generation:

- create temporary `.tex`
- render
- verify
- clean up

## Final User Response Format

Once the resume is ready, keep the final answer concise.

Use this structure:

1. direct link to the PDF
2. exactly 1 bullet explaining why those 5 experiences + 3 projects were selected for this JD
3. confirm it is exactly `1` page

Example pattern:

```text
The CompanyName resume is ready:

[Sahaj_Bhavesh_Bhadja.pdf](</absolute/path/to/file.pdf>)

I tailored it toward:
- backend APIs and cloud services
- Java/Python/SQL foundations
- testing, CI/CD, and production reliability

It’s verified as exactly `1` page.
```

If a corrected version is generated:

- link the latest versioned PDF
- mention what was fixed

## Required QA Checklist Before Finalizing

Before returning the PDF to the user, confirm all of the following:

- company folder is lowercase
- output is in the correct date folder
- filename is correct and versioned correctly
- page count is exactly `1`
- temp `.tex` deleted
- preview image deleted
- header contains phone, email, LinkedIn, GitHub, portfolio
- `USC Annenberg Media` does not appear
- visible location matches the JD city/state when the JD has one clear location
- experience count is `4` or `5`
- work experiences each have `2` bullets
- experience order is strict reverse chronological
- education entries both appear
- GPA appears for both education entries
- coursework appears for both education entries
- skills section includes at least `30` individual skill terms
- experience and project bullets are each `27-32` words
- no text overflows page boundaries
- layout is not visibly cramped in one section and loose in another

## Minimal Operational Recipe

If another model needs the shortest possible execution recipe:

1. Read [RESUME_RULES.md](E:/Projects/Random/Resume/RESUME_RULES.md) and this file.
2. Read the JD.
3. Pull relevant items from [master_resume_data.json](E:/Projects/Random/master_resume_data.json).
4. Draft `E:\Projects\Random\Resume\temp_<company>_<date>.tex`.
5. Render with [render_pdf_only.py](E:/Projects/Random/Resume/COMPANY/scripts/render_pdf_only.py).
6. Check page count.
7. Render preview and inspect layout.
8. Fix chronology, overflow, and spacing.
9. Delete temp artifacts.
10. Return final PDF path.

That is the standard operating procedure.
