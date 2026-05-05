# Resume Rules

This file is the strict operating guide for generating Sahaj Bhadja's resumes from `E:\Projects\Random\master_resume_data.json`.

## Output Rules

- Output root: `E:\Projects\Random\Resume`
- Company folder name must be lowercase.
- Folder pattern:
  - `E:\Projects\Random\Resume\<company-name>\<YYYY-MM-DD>\`
- If multiple resumes are generated for the same company on the same date, create versioned PDFs:
  - `Sahaj_Bhavesh_Bhadja.pdf`
  - `Sahaj_Bhavesh_Bhadja_v2.pdf`
  - `Sahaj_Bhavesh_Bhadja_v3.pdf`
- Do not save `.tex` files in company output folders.
- Final output for each JD run is a PDF only.

## Immutable Template Constraints

The generated resume must preserve the current template's visual identity unless explicitly overridden by the user:

- LaTeX class: `article`
- Page size: `letterpaper`
- Font size: `10pt`
- Font family: preserve the template defaults exactly
- One page only
- Keep the existing section style, macro system, and overall visual language
- Header links must remain present:
  - phone
  - email
  - LinkedIn
  - GitHub
  - portfolio
- Default resume email: `bhadja@usc.edu`

## Allowed Layout Adjustments

- `\vspace` values may be adjusted as needed.
- Section ordering may be changed per JD.
- Minor spacing changes are allowed if needed to keep the resume at exactly one page.
- Font family and `10pt` size must not change.

## Candidate Identity Rules

- Filename base must always be `Sahaj_Bhavesh_Bhadja`.
- Display name in header remains `Sahaj Bhadja`.
- `USC Annenberg Media` must never appear on any resume.

## JD Tailoring Priorities

Primary optimization order:

1. ATS keyword match
2. Recruiter readability
3. Hiring-manager technical depth

For weak or vague JDs:

- Optimize based on the role responsibilities and company context.
- Prefer the role track that best matches the candidate profile.

## Section Selection Rules

### Summary

- Always include a summary.
- Summary length: 1 to 2 lines only.
- Tailor summary to:
  - role family
  - years of experience
  - strongest domain fit
  - 3 to 5 high-value JD keywords
- Avoid generic filler and obvious statements.

### Education

- Always include both education entries.
- Always show GPA.
- Always show coursework.
- Coursework should be tailored to the JD where possible.

### Experience

- Use at least 4 experience entries when the page is already full with relevant content.
- There is no strict 4-experience cap; add a 5th relevant role when space remains and it improves JD alignment.
- Fill the page as effectively as possible without spilling past 1 page or adding low-signal filler.
- Maximum recommended experience entries: 5.
- Always order work experience from most recent to oldest across all included roles with no exceptions.
- Chronology must be evaluated by the actual date ranges, not by role type or section preference.
- Prioritize `USC Dornsife` and `Grad8` for backend, AI, platform, and applied-ML roles unless the JD strongly suggests otherwise.
- Allowed title changes:
  - `USC AD Labs`: alternate truthful ML/research phrasing is allowed
  - `Pandit Deendayal Energy University` research/data role: alternate truthful phrasing is allowed
- Other roles should keep their stored titles unless there is a compelling reason and the change stays truthful.
- Entire roles may be dropped if irrelevant.

### Experience Bullet Rules

- Bullets may be rewritten, merged, split, compressed, or expanded.
- Project idea and factual direction must remain aligned with the master data.
- Default to 2 bullets for each included work experience.
- Bolding should be used strategically for high-signal technologies, impact, metrics, and role-relevant terms.
- Every finalized resume bullet should include bolded JD-critical keywords (stack, domain terms, impact terms, metrics) where natural and readable.
- Top roles can use up to 3 bullets.
- Other roles should typically use 1 to 2 bullets.
- Metrics may be introduced if needed for tailoring, but should stay coherent with the project/work narrative.

### Unverified Enhancement Verification Flow

- Do not place unverified or fabricated claims directly into the resume.
- If potentially true-but-unlisted details could improve fit, propose them to the user first as **unverified enhancement bullets**.
- Ask the user to confirm each proposed enhancement (`Yes/No`).
- Only confirmed enhancements may be added to the resume.
- After user confirmation, add the confirmed details into `master_resume_data.json` under the relevant experience/project record so future runs can reuse them safely.

### Skills

- Skills may be fully reordered and trimmed per JD.
- Skill category headers may be renamed for better match.
- Dense one-block presentation is allowed, but restructuring within the same section is also allowed.
- Prefer high-density keyword coverage without turning the section into noise.
- Default behavior should preserve the candidate's original dense skills backbone rather than aggressively shrinking it.
- Start from the baseline categories:
  - Languages
  - Backend & APIs
  - Frontend
  - Databases
  - Cloud & Infrastructure
  - AI/ML
  - Engineering Practices
- Then tailor by:
  - reordering categories
  - swapping weaker items for stronger JD-relevant items
  - appending adjacent JD terms when justified
- Do not compress the skills section so far that major core categories disappear unless the user explicitly asks for a minimal skills section.
- When a JD explicitly accepts similar or alternative technologies, adjacent stack terms may be surfaced in `Skills` even if the exact wording is not present in the master data, as long as they map credibly from the candidate's actual experience.
- Typical examples:
  - event-driven workflows or streaming systems can justify `Kafka`-adjacent targeting
  - large-scale data pipelines can justify `Apache Flink`-adjacent targeting
  - backend/distributed systems experience can justify `Golang`-adjacent targeting

### Projects

- Project count is flexible, but experience must remain at a minimum of 4 entries.
- Projects should be selected to maximize JD fit.
- Use 0 to 3 projects depending on space and relevance.
- Projects may be rewritten aggressively as long as the underlying idea remains consistent.
- If a completely new project is created for fit, the user must be told in chat.
- If the experience section becomes visually cramped while the projects section has spare space, rebalance spacing and/or content so the page looks intentionally distributed rather than bottom-light and middle-dense.

## Layout Quality Rules

- No text may overflow past the right page boundary.
- Education rows must be checked specifically for long institution/location combinations and adjusted using wrapping, abbreviations, or spacing changes as needed.
- When space is available in lower sections, do not over-compress experience entries; rebalance vertical spacing so the page reads evenly.
- Do not allow one section to be visually cramped while another has noticeably loose spacing; spacing should feel intentionally balanced across the full page.
- Default preference is readability over maximal compression once ATS coverage and one-page fit are satisfied.
- If experience bullets are wrapping too tightly line-to-line, shorten bullet wording before collapsing vertical spacing further.
- If projects appear jammed together, add breathing room between project entries and reclaim space elsewhere by tightening wording, not by removing structure.
- Before finalizing any resume, visually inspect for:
  - cramped experience bullets
  - cramped project bullets
  - inconsistent whitespace distribution between sections
  - long right-column locations/dates pushing layout out of balance
- Reverse-chronological ordering must also remain visually obvious; entries should never appear out of timeline order because of spacing or grouping decisions.

## Role/Project Fit Heuristics

These are default heuristics, not hard constraints:

- Backend / Platform:
  - USC Dornsife
  - Aasma SecureSync
  - Big-Brain
  - Chat2SQL
  - Linguistix
- AI / ML / Applied AI:
  - Grad8
  - USC Dornsife
  - USC AD Labs
  - CaptionCraft
  - Big-Brain
- Data Engineering:
  - USC Dornsife
  - Aasma SecureSync
  - LST Capitals
  - Chat2SQL
  - Linguistix
- Fintech / Payments:
  - LST Capitals
  - FinNexus
- Healthcare:
  - HMIS
- Blockchain / Web3:
  - PDEU Research Fellowship
  - Comprehensive Analysis of Blockchain for User Authentication
  - LST Capitals

## Banned and Sensitive Content Rules

- Never include `USC Annenberg Media`.
- Do not weaken the resume with filler bullets that add no selection advantage.
- Do not exceed one page.
- Do not remove phone, email, LinkedIn, GitHub, or portfolio from the header.
- Do not include unverified claims that have not been confirmed by the user.

## Template Section Intent

### Header

- Must be compact, link-rich, and ATS-readable.
- Must preserve the current icon + underline style.

### Summary

- Should position the candidate immediately for the target role.
- Must not consume excessive vertical space.

### Education

- Signals academic strength, current USC status, and relevant coursework.
- Coursework should be customized to the role family.

### Experience

- Main decision section.
- Should carry the strongest JD match and most recruiter value.
- Prefer concise impact-first bullets with technologies and outcomes.

### Skills

- High-density ATS compression zone.
- Must reflect the chosen role family rather than every possible skill.

### Projects

- Used to patch fit gaps or strengthen domain alignment.
- Should be highly relevant and compact.

## Future Run Workflow

For each JD:

1. Analyze the JD deeply.
2. Identify target role family and company context.
3. Select best 4 to 5 experiences.
4. Select best projects, if any.
5. Tailor coursework, skills, summary, titles, and bullets.
6. If needed, propose unverified enhancement bullets and get explicit user confirmation before inclusion.
7. Persist confirmed new details to `master_resume_data.json`.
8. Ensure the result is exactly one page.
9. Render a PDF only to the company/date folder with versioning.
