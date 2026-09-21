# Format Lock

Locked visual values for `resume_template.tex`. These are the values Sahaj approved after review (Mitratech / U.S. Bank, 2026-09). Do not change them except through the fit ladder below.

## Invariants

- `article`, `letterpaper`, `10pt`, default font family. One page.
- Header: name + phone, email (`bhadja@usc.edu`), LinkedIn, GitHub, portfolio, with icons and underlines.
- Section order: Summary, Education, Experience, Skills, Projects.
- Section rule sits on its own line under the title: `[\color{black}\vspace{-6pt}\rule{\linewidth}{0.4pt}\vspace{-2pt}]`. Never use `\titlerule`.
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

## Fit ladder (only if the page overflows)

Apply in order and re-render after each step. Stop as soon as the page count is 1.

1. Shorten wording (stay within 27-32 words per bullet), trim a skill line that wraps.
2. Cut the new project from 2 bullets to 1.
3. `\itemTail` -> `-5pt`, then `-6pt`.
4. `\roleGap` -> `0pt`; `\projGap` -> `1pt`.
5. Swap the weakest master-data project for one with a shorter bullet, or drop the fifth experience (minimum 4). The project count always stays at 3.

Never:

- reduce `itemsep` below `3pt` (bullets visibly merge; rejected twice)
- push `\sectionGap` past `-8pt` (the next header collides with prior content)
- change font, font size, or margins
