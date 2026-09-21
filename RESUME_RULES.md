# Resume Rules

Single source of truth for generating Sahaj Bhadja's JD-tailored one-page resumes. Input: a company name and a job description. The agent makes every selection and layout decision itself; it asks the user only where this file says to.

## Files

| Path | Role |
|---|---|
| `E:\Projects\Random\master_resume_data.json` | All candidate facts. Nothing goes on a resume that is not here, except the new project built for that specific resume (step 3). |
| `FORMAT_BASELINE/resume_template.tex` | Locked template: preamble, macros, header, `%%PLACEHOLDER%%` slots. |
| `FORMAT_BASELINE/FORMAT_LOCK.md` | Locked spacing values and the fit ladder. |
| `scripts/render_pdf_only.py` | Compile (tectonic), lint, page-count check, versioned PDF output, optional preview. |
| `.work/<company>/<folder>.tex` | Source for each generated resume. Kept so later fixes edit it instead of rebuilding. |
| `COMPANY/<company>/<folder>/` | Deliverables. PDF only. |

## Flow

### 1. Parse the JD

Extract: role family, required vs. preferred stack, responsibilities, level, domain terms, location, work mode, job/requisition ID.

### 2. Research (mandatory, before any selection)

Web-search the company and team: product and customers, domain, recent news/launches, likely engineering stack beyond the JD, and what the specific team owns. Record 3-6 findings in the delivery message. Use them to order skills, choose emphasis, and phrase bullets. Research never becomes a personal claim.

### 3. Fit analysis and new project

List the JD's must-have hard skills (languages, frameworks, platforms, practices). Fit = share of them evidenced by an existing experience or project in master data. Report the fit and the uncovered skills in the delivery message.

Every resume gets exactly one new project, built for this JD. Its stack is the uncovered must-haves; if nothing is uncovered, it targets the JD's core product domain and most differentiating stack instead.

**New project**, scoped so it can be built and demoed:

1. Post the spec in chat: name, stack, what it does, the two resume bullets it will support.
2. Build it for real as a new git repo at `E:\Projects\<ProjectName>`: working code, tests, README with run instructions. The resume bullets may only claim what the repo actually does.
3. Ask before pushing to GitHub (`SAHAJ-BHADJA`), since that is public. Once pushed, the repo URL is the project's `Code` link.
4. The project belongs to this one resume only. Do not add it to master data, and do not reuse it for other JDs; each JD gets its own new project. Its only record is the repo and the resume's `.work/` source.

### 4. Select content

**Experience (5; minimum 4)**

- Strict reverse-chronological order by actual dates. If dates overlap, the later start date goes first. Never reorder for relevance.
- Company names, titles, dates, and locations are copied from master data. The only permitted title rewording is truthful alternate phrasing for USC AD Labs and the PDEU research role.
- Locations are the historical ones from master data, never the JD's city.

**Projects (exactly 3)**

- 1 new project (step 3), listed first, plus 2 projects from master data. Never more than one new project, never fewer than 3 projects in total.
- Choose the 2 master-data projects to patch the stack/domain gaps that experience and the new project leave open.
- A project with a URL in master data gets a clickable title plus a red, underlined `Live` (deployed app) or `Code` (repo) label via `\resumeProjectLink`. A project without a URL is shown as a plain title. Prefer linked projects when fit is equal.
- Never invent or infer a URL.

**Education**: both entries, always with GPA and coursework; coursework reordered/swapped toward the JD.

### 5. Write

- **Summary**: 1-2 lines. Role family, years of experience (2+), strongest JD stack, 3-5 bolded keywords. No filler.
- **Bullets**: 2 per role, 1 per project (2 allowed for the new project; cut it to 1 before cutting anything else when space is tight). 27-32 words each. Impact-first, JD-critical terms bolded. Rewrite, merge, or reframe freely, but facts and metrics must come from master data.
- **Skills**: each category on its own line, >= 30 terms. Order: JD must-haves, then credible adjacent terms, then remaining defensible skills. Baseline categories (rename/reorder/drop per JD): Languages, Backend & APIs, Frontend, Databases, Cloud & Infrastructure, AI/ML, Engineering Practices.

### 6. Truthfulness gate

Allowed: reframing emphasis, compressing real tasks into sharper bullets, bolding, choosing among real metrics.

Not allowed without the user's confirmation:

- a technology, company, role, or collaboration that master data does not support
- an adjacent skill, unless the JD itself says "X or similar" and the candidate's real work maps to it credibly

If a true-but-unrecorded detail about existing work would improve fit, propose it as an unverified enhancement, get Yes/No, and write confirmed details into master data before using them. This applies to real past work only; new projects never go into master data.

### 7. Build

1. Copy `FORMAT_BASELINE/resume_template.tex` to `.work/<company>/<folder>.tex` and fill every `%%...%%` slot. Put `\roleGap` before each role after the first and `\projGap` before each project after the first.
2. Render:
   ```
   python scripts/render_pdf_only.py --tex ".work/<company>/<folder>.tex" --company "<company>" --folder "<folder>" --preview
   ```
   The script lints (27-32 words per bullet, >= 30 skills, banned content, leftover placeholders), compiles with `tectonic-bin/tectonic.exe`, checks for exactly 1 page, and writes the next free `Sahaj_Bhadja_Resume[_vN].pdf`. Use `--overwrite` to replace the latest PDF while iterating on the same version. Non-zero exit means something must be fixed.
3. Open the preview PNG and check: right-edge overflow, long education rows, bullets visually merging, cramped vs. loose sections, chronology.
4. If it overflows, fix wording first, then walk the fit ladder in `FORMAT_LOCK.md`. Never go below the locked bullet spacing.

### 8. Deliver

- Output: `COMPANY/<company-lowercase>/<YYYY-MM-DD(Position-Name_JobID)>/Sahaj_Bhadja_Resume.pdf`
  - date = the day it is generated; position title sanitized (spaces to hyphens, special characters dropped); `_JobID` only when the posting has one
  - regenerations become `_v2`, `_v3`, ...
  - the folder contains PDFs only; the `.tex` stays in `.work/` and the preview PNG is deleted
- Message to the user:
  1. PDF path, confirmed 1 page
  2. research findings used (3-6 bullets)
  3. each selected experience/project with its JD-specific reason; each credible excluded alternative with the exact signal it lacked (stack, responsibility, domain, evidence, recency, duplication, missing link); note when the 5/3 limit decided it
  4. fit before the new project (share of must-haves covered by master data, and what was uncovered)
  5. anything new: the new project built, enhancements confirmed, adjacent skills added

## Invariants

- One page, `article`, `letterpaper`, `10pt`, template fonts. Section order: Summary, Education, Experience, Skills, Projects (reorder only if the user asks).
- Header: `Sahaj Bhadja`, phone, `bhadja@usc.edu`, LinkedIn, GitHub, portfolio. Never remove a link.
- `USC Annenberg Media` never appears.
- Bullets render as `•`.

## Role and project heuristics

Defaults, not constraints. The Projects column lists master-data candidates for the 2 existing-project slots; the new project is designed per JD.

| Role family | Experience first | Projects | Emphasize |
|---|---|---|---|
| Backend / Platform | USC Dornsife, Aasma SecureSync, Grad8 | Chat2SQL, Big-Brain, Linguistix | APIs, SQL, cloud, reliability, scaling |
| .NET / Azure enterprise | USC Dornsife, Aasma VibrantChem, Aasma SecureSync | FinNexus, Chat2SQL | C#, Azure, SQL Server, microservices, CI/CD |
| Full-stack product | Grad8, Aasma VibrantChem, LST Capitals | PiXMod, FinNexus, HMIS | React, TypeScript, end-to-end ownership |
| AI / Applied LLM | USC Dornsife, Grad8, USC AD Labs | Big-Brain, CaptionCraft, PiXMod | LLM workflows, retrieval, multimodal, production AI |
| Data engineering | USC Dornsife, Aasma SecureSync, LST Capitals | Chat2SQL, Linguistix | ETL, SQL tuning, validation, pipelines |
| Research / Systems / Autonomy | USC AD Labs, USC Dornsife | CPU-Scheduling Simulator, Chat2SQL | Python, C++, simulation, testing |
| Support / Solutions / Client-facing | LST Capitals, Aasma SecureSync, USC Dornsife | Chat2SQL, HMIS | triage, debugging, stakeholder communication |
| Fintech / Payments | LST Capitals | FinNexus | transactions, security, payments |
| Healthcare | | HMIS | workflows, sensitive-data handling |
| Blockchain / Web3 | PDEU Research Fellowship, LST Capitals | Blockchain Authentication paper | cryptography, consensus |

Coursework defaults: backend/data use Database Systems, Analysis of Algorithms, Web Technologies; systems use Operating Systems, Analysis of Algorithms, Software Engineering; AI keeps Advanced NLP.
