# Resume Rules

Single source of truth for generating Sahaj Bhadja's JD-tailored one-page resumes. Input: a company name and a job description. The agent makes every selection and layout decision itself; it asks the user only where this file says to.

## Files

| Path | Role |
|---|---|
| `E:\Projects\Random\master_resume_data.json` | All verified candidate facts, including canonical records for reusable portfolio projects. JD-specific project concepts may be added directly to a resume under the project policy. |
| `FORMAT_BASELINE/resume_template.tex` | Locked template: preamble, macros, header, `%%PLACEHOLDER%%` slots. |
| `FORMAT_BASELINE/FORMAT_LOCK.md` | Locked spacing values and the fit ladder. |
| `FORMAT_BASELINE/CONTENT_SELECTION_POLICY.md` | Mandatory full-pool scoring for experience, projects, and JD-specific skills. |
| `FORMAT_BASELINE/PROJECT_PORTFOLIO_POLICY.md` | Project quality, selection, creation, extension, verification, and reuse rules. |
| `scripts/render_pdf_only.py` | Compile (tectonic), lint, page-count check, versioned PDF output, optional preview. |
| `.work/<company>/<folder>.tex` | Source for each generated resume. Kept so later fixes edit it instead of rebuilding. |
| `COMPANY/<company>/<folder>/` | Deliverables. PDF only. |

## Flow

### 1. Parse the JD

Extract: role family, required vs. preferred stack, responsibilities, level, domain terms, location, work mode, job/requisition ID.

### 2. Research (mandatory, before any selection)

Web-search the company and team: product and customers, domain, recent news/launches, likely engineering stack beyond the JD, and what the specific team owns. Record 3-6 findings in the delivery message. Use them to order skills, choose emphasis, and phrase bullets. Research never becomes a personal claim.

### 3. Fit analysis and portfolio-gap review

List the JD's must-have hard skills, responsibilities, and domain signals. Fit = the share evidenced by verified experience or projects in master data. Report the fit and material uncovered signals in the delivery message.

### 3a. JD-aligned project review

Every resume should carry the strongest possible project section for the JD. First check whether an existing verified project in master data already covers the JD and company research. If one fits well, reuse it and tailor the bullet emphasis.

If the existing project pool leaves a clear gap, add one realistic, real-world project concept directly to the resume. This is a resume-tailoring step, not an implementation task. Do not build code, create tests, write a README, generate docs, add a repository, or record benchmarks unless the user explicitly asks for that work.

The added project must:

- solve a general real-world engineering problem related to the JD
- use technologies the candidate can credibly discuss from verified experience or adjacent coursework/projects
- avoid employer-specific naming or copying the target company's terminology
- avoid invented production users, deployments, repository links, or measured performance metrics
- be phrased as a defensible portfolio/project entry, with honest scope and no unsupported claims

Project discovery is allowed for resume fit. Project implementation is opt-in only.

### 4. Select content

Before selecting anything, follow `FORMAT_BASELINE/CONTENT_SELECTION_POLICY.md`. For every JD, enumerate and score the entire eligible work-experience pool and the entire verified project pool in `master_resume_data.json`, then decide whether one JD-specific project concept is needed. Never begin from the previous resume, a default five-role set, role-family heuristics, or recently used projects. Prior selections create no preference or entitlement for future resumes.

**Experience (exactly 5)**

- Select exactly 5 experiences only after comparing every eligible experience in master data against the JD and company research. This count is compulsory and has no page-fit or layout exception.
- Score relevance using required stack, responsibilities, domain, evidence strength, recency, and non-duplication. Record a concise reason for every selected experience and every credible excluded alternative.
- Strict reverse-chronological order by actual dates. If dates overlap, the later start date goes first. Never reorder for relevance.
- Company names, titles, dates, and locations are copied from master data. USC Dornsife may use the master-data title or approved alternate titles (`Software Engineer`, `Forward Deployed Engineer`, `Forward Deployed Software Engineer`) based on JD fit. Other permitted title rewording is truthful alternate phrasing for USC AD Labs and the PDEU research role.
- Locations are the historical ones from master data, never the JD's city.
- **Stack re-mapping (user-authorized, two roles only): Aasma VibrantChem internship and LST Capitals internship.** Their technologies may be reworded toward the JD and research stack. What must stay fixed: the product (VibrantChem = resource-management/CRM platform with real-time updates, microservices, cross-location sync, CI/CD; LST = cross-platform house-help booking app backend with bookings, payments, coupons, real-time status sync, analytics), its goal, scope, responsibilities, and every metric. Prefer substitute technologies the candidate has verified elsewhere in master data, so they can be defended in interviews. Never re-map USC Dornsife, Grad8, Aasma SecureSync, USC AD Labs, or the research roles. List every re-mapping in the delivery message.

- **Projects (exactly 3)**

- Exactly 3 projects total. Prefer verified projects from master data when they fit.
- Score every verified project in master data for each JD according to `FORMAT_BASELINE/PROJECT_PORTFOLIO_POLICY.md`. Never limit consideration to projects used in recent resumes or listed in a role-family heuristic.
- If no verified project covers an important JD signal, add one JD-aligned real-world project concept directly to the resume and list it first when it is the strongest project match.
- Choose the remaining projects for complementary evidence (stack, responsibility, domain); avoid three projects that prove the same narrow capability.
- Resume-only project concepts do not need implementation, testing, documentation, repository creation, or master-data insertion unless the user explicitly asks.
- A project with a URL in master data gets a clickable title plus a red, underlined `Live` (deployed app) or `Code` (repo) label via `\resumeProjectLink`. A project without a URL is shown as a plain title. Prefer linked projects when fit is equal.
- Never invent or infer a URL.

**Education**: both entries, always with GPA and coursework; coursework reordered/swapped toward the JD.

### 5. Write

- **Summary**: 1-2 lines. Role family, years of experience (2+), strongest JD stack, 3-5 bolded keywords. No filler.
- **Bullets**: 2 per role and 1 per project. Each bullet is 27-32 words, impact-first, and must bold the most relevant JD-critical keyword(s) in that bullet using `\textbf{...}`. Bold only truthful technologies, responsibilities, domains, or outcomes supported by master data, company/JD research, or an allowed JD-specific project concept; never bold filler or unsupported keyword stuffing. Rewrite or merge for emphasis. Experience bullets and verified project facts come from master data; JD-specific project concepts must avoid unsupported metrics, links, production scale, or claims the candidate cannot defend.
- **Skills**: each category on its own line, **at least 40 distinct, evidence-supported terms**. Build the list from the JD, mandatory company/team research, and verified master data; order JD must-haves first, then research-supported role signals, credible adjacent terms, and remaining defensible skills. Never add an unsupported skill merely to reach 40. Baseline categories (rename/reorder/drop per JD): Languages, Backend & APIs, Frontend, Databases, Cloud & Infrastructure, AI/ML, Engineering Practices.

### 6. Truthfulness gate

Allowed: reframing emphasis, compressing real tasks into sharper bullets, bolding, choosing among real metrics.

Not allowed without the user's confirmation:

- a technology, company, role, or collaboration that master data does not support
- an adjacent skill, unless the JD itself says "X or similar" and the candidate's real work maps to it credibly

If a true-but-unrecorded detail about existing work or a portfolio project would improve fit, propose it as an unverified enhancement, get Yes/No, and write confirmed details into master data before using them.

The one standing exception is the user-authorized stack re-mapping for the Aasma VibrantChem and LST Capitals internships (step 4), within its product-scope limits.

All projects follow `FORMAT_BASELINE/PROJECT_PORTFOLIO_POLICY.md`. Resume-only project concepts are allowed when useful for JD fit, but they must not claim unverified metrics, public links, production users, or completed implementation details beyond what the candidate can defend.

### 7. Build

1. Copy `FORMAT_BASELINE/resume_template.tex` to `.work/<company>/<folder>.tex` and fill every `%%...%%` slot. Put `\roleGap` before each role after the first and `\projGap` before each project after the first.
2. Render:
   ```
   python scripts/render_pdf_only.py --tex ".work/<company>/<folder>.tex" --company "<company>" --folder "<folder>" --preview
   ```
   The script lints (exactly 5 experiences, exactly 3 projects, 27-32 words per bullet, >= 40 skills, banned content, leftover placeholders), compiles with `tectonic-bin/tectonic.exe`, checks for exactly 1 page, and writes the next free `Sahaj_Bhadja_Resume[_vN].pdf`. Use `--overwrite` to replace the latest PDF while iterating on the same version. Non-zero exit means something must be fixed.
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
  4. fit from verified master data (share of must-haves covered and what remains uncovered)
  5. the strongest project match: what it solves, why it matches the research, and whether it was reused from master data or added as a JD-specific resume project concept
  6. every stack re-mapping applied to VibrantChem / LST (original stack -> resume stack)
  7. anything new: portfolio additions or extensions verified and added to master data, enhancements confirmed, adjacent skills added

## Invariants

- One page, `article`, `letterpaper`, `10pt`, template fonts. Section order: Summary, Education, Experience, Skills, Projects (reorder only if the user asks).
- Every resume contains exactly 5 work-experience entries and exactly 3 project entries. Neither count may be reduced to solve layout overflow.
- Header: `Sahaj Bhadja`, phone, `bhadja@usc.edu`, LinkedIn, GitHub, portfolio. Never remove a link.
- `USC Annenberg Media` never appears.
- Bullets render as `•`.

## Role and project heuristics

Discovery aids only, never candidate shortlists. The Experience and Projects columns do not override mandatory full-pool scoring. For every JD, evaluate all eligible master-data experiences and all verified projects before selecting exactly five experiences and exactly three projects.

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
