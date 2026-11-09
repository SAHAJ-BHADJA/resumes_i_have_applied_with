# Mandatory Full-Pool Content Selection Policy

This policy applies to every resume generated from a job description. It is a hard gate, not a recommendation.

## Complete Candidate Pool

Before drafting the resume:

1. Enumerate every eligible work experience from every experience collection in `master_resume_data.json`, including research, fellowship, assistantship, internship, and professional roles.
2. Enumerate every verified project in `master_resume_data.json`.
3. Do not use the prior resume, the most common five roles, role-family heuristics, or recently selected projects as the candidate pool.
4. Treat heuristics only as discovery aids after the complete pool has been enumerated.

## Mandatory Scoring

Score every eligible experience and every verified project against:

- required and preferred technologies
- primary responsibilities and expected deliverables
- company product, customer, domain, and team signals found through mandatory research
- strength and specificity of verified evidence
- measurable impact
- recency
- overlap or duplication with other selected entries
- portfolio breadth and interview value

Select exactly the strongest five experiences and exactly three projects. The first two must be **Direct Match Projects** optimized as the closest possible matches to the JD; both may be newly drafted realistic real-world concepts. The third must be the strongest matching project from verified master data. It may use a technically equivalent, interview-defensible parallel technology adaptation when supported by the JD and company research, but its responsibilities, scale, metrics, and outcomes must remain truthful. Never add more than two concepts. Prefer verified projects when fit is equally strong; use a second concept only when it materially improves truthful JD alignment. Both counts are compulsory and have no page-fit, layout, role-family, or relevance-score exception. After selection, place experiences in strict reverse chronology; relevance determines inclusion, never ordering.

For delivery, provide a concise JD-specific reason for each selection and each credible excluded alternative. When the five-experience or three-project limit decides an exclusion, state that explicitly.

## Skills Gate

Every resume must contain at least 40 distinct skills or competency terms. Skills must be:

- supported by verified master data
- relevant to the JD or credible company/team research
- ordered with explicit JD requirements first, research-supported role signals second, and defensible adjacent skills afterward
- free of unsupported keyword stuffing

If fewer than 40 relevant verified terms are available, do not fabricate terms. Report the evidence gap and expand only with truthful broader competencies already supported by the candidate's work. The renderer must reject resumes with fewer than 40 skills.

## Prohibited Shortcuts

- Reusing the same five experiences without rescoring the full pool
- Considering only projects used in recent resumes
- Drafting more than two JD-specific project concepts, or reshaping a verified project beyond truthful, technically equivalent adaptation
- Drafting all three projects instead of keeping the third as the strongest verified project
- Treating role-family tables as fixed selections
- Keeping an entry solely because its source text already fits the template
- Adding unsupported skills to satisfy the minimum
- Building code, tests, README files, repositories, or project documentation unless the user explicitly asks
