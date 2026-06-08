# Future Resume Generation Workflow

Use this process every time a new JD is shared.

## 1. Read the JD

Extract:

- role family
- core stack
- responsibilities
- level
- domain keywords

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

## 4. Start from the locked baseline

Files:

- `resume_template.tex`
- `firmpilot_reference_sample.tex`

Rule:

- content changes per JD
- formatting stays anchored to this baseline unless there is a specific layout problem

## 5. Tailor the content

Rewrite:

- summary
- coursework
- experience bullets (`27-32` words each)
- skills section (minimum `30` individual skill terms, built from full company/team research)
- project bullets (`27-32` words each)

Keep:

- one page
- location consistency
- readable spacing
- strong JD keyword coverage

## 6. Compile and visually QA

Check:

- one-page output
- no right-edge overflow
- no awkward section gaps
- no cramped experience block
- no broken projects spacing
- no inconsistent locations/dates
- skills section has at least 30 individual skill terms
- experience and project bullets are each 27-32 words

## 7. Fix wording first, spacing second

Preferred order:

1. remove weak wording
2. shorten bullets (stay within `27-32` words when possible)
3. verify skills section has at least `30` terms
4. only then touch spacing

## 8. Deliver

Return:

- final company PDF
- working `.tex` draft for iteration

## Baseline rule

If the future resume drifts visually, compare it against `firmpilot_reference_sample.tex` and bring it back into alignment.
