# Format Lock

This file records the locked spacing and formatting values. Don't change these unless you have a specific layout problem that can't be solved by rewording.

## Locked Spacing Values

| Location | Value |
|----------|-------|
| Header to Summary | `\vspace{-18pt}` |
| Summary bottom spacing | `\vspace{-16pt}` |
| Education to Experience | `\vspace{-14pt}` |
| Experience to Skills | `\vspace{-14pt}` |
| Skills to Projects | `\vspace{-16pt}` |
| `\resumeSubheading` tail spacing | `\vspace{-2pt}` |
| `\resumeEduSubheading` tail spacing | `\vspace{-4pt}` |
| `\resumeProjectHeading` tail spacing | `\vspace{-2pt}` |
| `\resumeItemListEnd` | `\vspace{-4pt}` |
| `\resumeProjItemListEnd` | `\vspace{-4pt}` |
| Between project entries | `\vspace{3pt}` |

## Locked List Settings

### Experience Bullets (`\resumeItemListStart`)
```latex
leftmargin=0.15in
label=\textbullet
itemsep=2pt
topsep=0pt
parsep=0pt
partopsep=0pt
```

### Project Bullets (`\resumeProjItemListStart`)
```latex
leftmargin=0.15in
label=\textbullet
itemsep=0pt
topsep=0pt
parsep=0pt
partopsep=0pt
```

## Formatting Rules

- Keep locations consistent (e.g., "Los Angeles, CA" not "LA, California")
- Keep the template on exactly one page
- Keep bullets dense but readable
- Shorten wording before increasing compression
- Preserve the header/link structure
- Use the same visual style for section rules and typography

## Content Rules That Pair with This Format

| Element | Target |
|---------|--------|
| Structure | Summary + Education + 5 Experiences + Skills + 3 Projects |
| Experience order | Strict reverse chronological |
| Bullets per experience | 2 bullets |
| Bullets per project | 1 bullet |
| Bullet length | 27-32 words for every experience and project bullet |
| Skills count | Minimum 30 individual skill terms (not category headers), from full company/team research |

## Drift Check Process

If a future resume looks off:

1. Compare against `sample_resume.tex`
2. Check section gaps first
3. Check project-title-to-bullet spacing
4. Check location consistency
5. Only then tweak spacing macros
