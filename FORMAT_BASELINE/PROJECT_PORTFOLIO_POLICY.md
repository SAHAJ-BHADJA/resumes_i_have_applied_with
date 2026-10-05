# Reusable Project Portfolio Policy

Projects should make the resume stronger for the target JD while staying defensible in interviews. Verified portfolio projects remain preferred, but a JD-specific real-world project concept may be added directly to a resume when the existing pool leaves an important gap. This policy applies to every project considered for the resume project section.

## Core Rule

Every resume includes exactly three projects. Prefer verified portfolio projects from master data. If the verified pool does not strongly cover the JD, add one realistic JD-aligned project concept directly to the resume and use the two strongest complementary projects from the verified pool. This count is compulsory and has no page-fit or layout exception. Do not rename or reshape an existing project to imitate one employer's job description.

Resume tailoring may change which verified facts receive emphasis, but it must not change a verified project's canonical name, capabilities, technologies, metrics, implementation status, or links. A JD-specific project concept may be named and written for the resume, but it must avoid unsupported metrics, public links, production scale, employer-specific claims, or technologies the candidate cannot defend.

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
3. If the verified pool covers the JD well, select exactly three verified projects.
4. If the verified pool leaves a clear gap, add one realistic JD-aligned project concept directly to the resume and select the two strongest complementary verified projects.
5. Prefer complementary evidence: for example, one systems project, one production application, and one domain or infrastructure project when those dimensions matter.
6. Tailor bullet emphasis to the JD, but preserve every underlying fact for verified projects.
7. Report important uncovered requirements instead of manufacturing false alignment.
8. Retain concise selection rationale for all selected projects and every credible excluded alternative so the final choice is auditable.

## JD-Specific Project Concepts

When the JD calls for a capability not covered well by verified projects, create one resume-ready project concept. This is a writing and positioning step only.

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

## Truthfulness

If no verified project covers a requirement, a realistic JD-specific project concept may cover the project-section gap, but do not infer experience with hardware, protocols, platforms, users, scale, or production deployment from adjacent work. A lower but defensible match is preferable to artificial alignment.
