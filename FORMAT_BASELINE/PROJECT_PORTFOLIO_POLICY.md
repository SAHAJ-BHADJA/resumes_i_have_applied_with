# Reusable Project Portfolio Policy

Projects should make the resume stronger for the target JD while staying defensible in interviews. Each resume uses its first two projects as the closest possible JD matches; both may be newly drafted JD-specific real-world concepts. The third is the strongest matching verified project. This policy applies to every project considered for the resume project section.

## Core Rule

Every resume includes exactly three projects:

1. One **Primary Direct Match Project**, optimized as a closest possible JD match and allowed to be newly drafted.
2. One **Secondary Direct Match Project**, also optimized as a closest possible JD match and allowed to be newly drafted.
3. One strongest matching project selected from the existing verified project pool.

Both Direct Match Projects may be verified projects or realistic JD-aligned project concepts. Never create more than two JD-specific concepts. Prefer verified projects when fit is equally strong; draft a second concept only when it materially improves truthful JD alignment. The third project must remain a verified portfolio selection. The three-project count is compulsory and has no page-fit or layout exception.

Both Direct Match Projects should receive direct JD-optimized positioning. For the third verified project, tailoring may change emphasis and may substitute or add an analogous technology when the implementation effect is technically equivalent and supported by the JD and company research (for example, AWS to Azure). Its product purpose, responsibilities, scale, metrics, implementation status, and outcomes must remain truthful. Drafted concepts must avoid unsupported metrics, public links, production scale, employer-specific claims, or technologies the candidate cannot defend.

## Portfolio Requirements

Each verified portfolio project should:

- solve a general engineering problem that exists independently of a particular employer or posting
- be useful across at least three related roles, teams, or industries
- have a name and README that describe the engineering problem rather than copied job-description terminology
- demonstrate meaningful architecture or implementation depth instead of functioning as a keyword showcase
- contain working code, tests, and clear setup or run instructions when it is an implemented portfolio artifact
- use reproducible metrics or behavior when metrics are claimed; never invent scale, performance, users, or business impact
- be discussable in an interview without mentioning the employer or posting that motivated the work
- have canonical facts recorded in `master_resume_data.json` after verification, when it is implemented and intended for reuse

Prefer projects with a working deployment or public repository when fit is otherwise equal. A project without a public link remains eligible when its implementation is locally verified and recorded accurately.

## Selection For A Resume

1. Extract the JD's required technical and responsibility signals.
2. Enumerate and score the entire verified project pool in `master_resume_data.json` against those signals using only canonical master-data evidence. No project may be skipped because it was absent from a previous resume, a role-family heuristic, or a familiar default set.
3. Choose the Primary Direct Match Project; use a verified project or draft a realistic JD-aligned concept.
4. Choose the Secondary Direct Match Project; use a verified project or draft a second realistic JD-aligned concept.
5. Choose the third project as the strongest matching selection from the verified pool.
6. Do not create a third JD-specific concept. For the verified project, allow only technically equivalent, interview-defensible parallel adaptations supported by the JD and company research.
7. Tailor all three bullets to the JD while keeping claims defensible. Direct keyword mirroring may be used when technically and factually supported.
8. Report important uncovered requirements instead of manufacturing false alignment.
9. Retain concise selection rationale for all selected projects and every credible excluded alternative so the final choice is auditable.

## JD-Specific Project Concepts

Create up to two resume-ready JD-specific project concepts and use them as the two Direct Match Projects. This is a writing and positioning step only. The third project must come from the verified pool; no third concept may be added for the same resume.

- **Discover from the role.** Base the concept on the target team's real problem, surfaced from the JD and company research.
- **Keep it general.** Name the project after the engineering problem, not the employer or exact posting language.
- **Stay defensible.** Use stacks and architecture the candidate can reasonably explain from verified work, coursework, or adjacent projects.
- **No fake proof.** Do not invent benchmarks, public users, production deployment, repository links, awards, or business outcomes.
- **No automatic build work.** Do not create code, tests, README files, docs, GitHub repositories, deployments, or master-data records unless the user explicitly asks.
- **Use concise resume language.** The project should read like a credible portfolio project and support the JD keywords without pretending to have verified metrics.

## Creating Or Extending Other Projects

Outside the resume-only JD concept, propose an implemented new project or extension only when the user asks for project-building work or when analysis identifies a durable portfolio gap that appears across multiple target job families and the user agrees to build it.

Before optional implementation, document:

- the general engineering problem
- at least three job families or industries it supports
- the reusable architecture and planned capabilities
- why an existing portfolio project cannot absorb the work naturally
- working-code, testing, documentation, and deployment acceptance criteria

Prefer extending an existing project when the feature belongs naturally on its roadmap. Create a separate project only when it has a distinct problem, architecture, and long-term identity.

After optional implementation:

1. Verify the code and tests in the available environment.
2. Record the canonical name, overview, technologies, implemented capabilities, verified metrics, links, and bullet bank in `master_resume_data.json`.
3. Ask before making a repository public or pushing to GitHub.
4. Make the verified project available for future resumes; never reserve it for one company.

## Anti-Patterns

Reject or revise a project when:

- its name copies one posting's terminology or the company's name
- its README describes the target company or application rather than a general user problem
- it claims built, tested, measured, deployed, or public-repository status without evidence
- technologies were added only to match keywords and have no architectural purpose
- the repository is a shallow demo with no tests, documentation, or meaningful behavior
- resume claims exceed what verified work or a defensible JD-specific project concept supports
- multiple near-duplicate repositories exist for adjacent applications
- more than two projects have been newly created, the third project is not from the verified pool, or a verified project has been rewritten beyond truthful and technically equivalent adaptation

## Truthfulness

Up to two realistic JD-specific project concepts may cover the two most important project-section gaps as the Direct Match Projects. The third must be the strongest defensible verified selection. Parallel technology adaptation is allowed only where the engineering effect is genuinely analogous; do not infer unrelated hardware, protocols, users, scale, metrics, or production deployment from adjacent work.
