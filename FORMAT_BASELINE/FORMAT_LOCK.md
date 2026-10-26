# Format Lock

Locked visual values for `resume_template.tex`. These are the values Sahaj approved after review (Mitratech / U.S. Bank, 2026-09). Do not change them except through the fit ladder below.

## Invariants

- `article`, `letterpaper`, `10pt`, default font family. One page.
- Header: name + phone, email (`sahaj.bhadja@gmail.com`), LinkedIn, GitHub, portfolio, with icons and underlines.
- Header icons are PNG images (`FORMAT_BASELINE/icons/*.png`, inserted by `\hicon`), never Font Awesome glyphs: glyph icons can leak junk characters into the PDF text layer next to the email, which job-application parsers autofill. `render_pdf_only.py` fails the build if the header text is not clean ASCII or the email is not a standalone token.
- Section order: Summary, Education, Experience, Skills, Projects.
- Content counts: exactly 5 experience entries and exactly 3 project entries. Never reduce either count for page fit.
- Project composition: exactly two Direct Match Projects, both of which may be newly drafted, plus one strongest matching verified project with only defensible parallel-technology adaptation, as defined in `PROJECT_PORTFOLIO_POLICY.md`.
- Section rule sits on its own line under the title: `[\color{black}\vspace{-7pt}\rule{\linewidth}{0.4pt}\vspace{-2pt}]`. Never use `\titlerule`.
- The first project heading must never touch the Projects rule: `\vspace{3pt}` right after `\resumeSubHeadingListStart` in the Projects section (approved 2026-10-02; `-2pt` made them touch).
- Bullets render as `•` via explicit `label=\textbullet`.
- No `\input{glyphtounicode}` / `\pdfgentounicode`: the compiler is tectonic (XeTeX), where they fail.

## Locked spacing

| Knob | Value | Where |
|---|---|---|
| Bullet-to-bullet (experience and projects) | `itemsep=3pt` | `\resumeItemListStart`, `\resumeProjItemListStart` |
| Bullet tail | `\itemTail` = `-4pt` | `\resumeItem` |
| Between roles | `\roleGap` = `2pt` | before every role after the first |
| Between projects | `\projGap` = `3pt` | before every project after the first |
| Between sections | `\sectionGap` = `-8pt` | after each section |
| Header to Summary | `-16pt` | fixed |
| Section title to its rule | `-7pt` | `\titleformat` (was `-6pt`) |
| Projects rule to first project | `3pt` | after `\resumeSubHeadingListStart` in Projects (was `-2pt`) |

## Fit ladder (only if the page overflows)

Apply in order and re-render after each step. Stop as soon as the page count is 1.

1. Shorten wording (stay within 27-32 words per bullet), trim a skill line that wraps.
2. Ensure every project has exactly 1 bullet; shorten or swap the weakest selected project using the reusable portfolio policy.
3. `\itemTail` -> `-5pt`, then `-6pt`.
4. `\roleGap` -> `0pt`; `\projGap` -> `1pt`.
5. Re-score the entire project and experience pools, then swap a selected entry for a comparably relevant entry whose verified facts can be expressed more compactly. Preserve exactly 5 experiences and exactly 3 projects.

Never:

- reduce `itemsep` below `3pt` (bullets visibly merge; rejected twice)
- push `\sectionGap` past `-8pt` (the next header collides with prior content)
- change font, font size, or margins
- reduce the resume below exactly 5 experiences or exactly 3 projects
