"""Compile a resume .tex with tectonic, lint it, and store only the PDF in the company folder.

Usage:
    python scripts/render_pdf_only.py --tex .work/<company>/<folder>.tex \
        --company "<company-lowercase>" --folder "YYYY-MM-DD(Position-Name_JobID)" [--preview]

Exit code is non-zero if compilation fails, the PDF is not exactly one page, or lint finds errors.
"""

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from pypdf import PdfReader

RESUME_ROOT = Path(__file__).resolve().parent.parent
COMPANY_ROOT = RESUME_ROOT / "COMPANY"
TECTONIC_LOCAL = RESUME_ROOT / "tectonic-bin" / "tectonic.exe"
PDF_BASE = "Sahaj_Bhadja_Resume"
WORD_MIN, WORD_MAX = 27, 32
MIN_SKILLS = 40
REQUIRED_EXPERIENCES = 5
REQUIRED_PROJECTS = 3
BANNED = ["USC Annenberg Media"]
CONTACT_EMAIL = "sahaj.bhadja@gmail.com"


def find_tectonic() -> str:
    if sys.platform == "win32" and TECTONIC_LOCAL.exists():
        return str(TECTONIC_LOCAL)
    found = shutil.which("tectonic")
    if found:
        return found
    raise SystemExit(f"tectonic not found at {TECTONIC_LOCAL} or on PATH")


def brace_bodies(text: str, command: str) -> list[str]:
    """Return the first-argument body of every `\\command{...}`, honoring nested braces."""
    bodies = []
    token = "\\" + command + "{"
    start = 0
    while (idx := text.find(token, start)) != -1:
        depth, i = 1, idx + len(token)
        while i < len(text) and depth:
            if text[i] == "{" and text[i - 1] != "\\":
                depth += 1
            elif text[i] == "}" and text[i - 1] != "\\":
                depth -= 1
            i += 1
        bodies.append(text[idx + len(token) : i - 1])
        start = i
    return bodies


def plain_text(latex: str) -> str:
    text = re.sub(r"\\(textbf|textit|emph|underline)\{", "", latex)
    text = re.sub(r"\\href\{[^}]*\}\{", "", text)
    text = text.replace("\\%", "%").replace("\\&", "&").replace("\\#", "#").replace("\\$", "$")
    text = re.sub(r"\\[a-zA-Z]+", " ", text)
    return text.replace("{", "").replace("}", "")


def count_skills(tex: str) -> int:
    match = re.search(r"\\section\{Skills\}(.*?)\\section\{", tex, re.S)
    if not match:
        return 0
    total = 0
    for line in match.group(1).splitlines():
        if ":" not in line or "\\textbf" not in line:
            continue
        items, depth, buf = [], 0, ""
        for ch in plain_text(line.split(":", 1)[1]).replace("\\\\", ""):
            depth += ch == "("
            depth -= ch == ")"
            if ch == "," and depth == 0:
                items.append(buf)
                buf = ""
            else:
                buf += ch
        items.append(buf)
        total += sum(1 for item in items if item.strip())
    return total


def section_body(tex: str, section: str, next_section: str | None = None) -> str:
    end = rf"\\section\{{{re.escape(next_section)}\}}" if next_section else r"\\end\{document\}"
    match = re.search(rf"\\section\{{{re.escape(section)}\}}(.*?){end}", tex, re.S)
    return match.group(1) if match else ""


def lint(tex: str) -> list[str]:
    problems = []
    experience_count = len(
        re.findall(r"\\resumeSubheading(?:Long)?\s*\{", section_body(tex, "Experience", "Skills"))
    )
    project_count = len(re.findall(r"\\resumeProjectHeading\s*\{", section_body(tex, "Projects")))
    if experience_count != REQUIRED_EXPERIENCES:
        problems.append(
            f"experience section has {experience_count} entries (need exactly {REQUIRED_EXPERIENCES})"
        )
    if project_count != REQUIRED_PROJECTS:
        problems.append(f"projects section has {project_count} entries (need exactly {REQUIRED_PROJECTS})")
    bullets = brace_bodies(tex, "resumeItem")
    for body in bullets:
        words = len(plain_text(body).split())
        if not WORD_MIN <= words <= WORD_MAX:
            problems.append(f"bullet has {words} words (need {WORD_MIN}-{WORD_MAX}): {plain_text(body)[:70]}...")
    skills = count_skills(tex)
    if skills < MIN_SKILLS:
        problems.append(f"skills section has {skills} terms (need >= {MIN_SKILLS})")
    for phrase in BANNED:
        if phrase in tex:
            problems.append(f"banned content present: {phrase}")
    if "%%" in re.sub(r"\\%", "", tex):
        problems.append("unfilled template placeholder (%%...%%) remains")
    print(
        f"lint: {experience_count} experiences, {project_count} projects, "
        f"{len(bullets)} bullets, {skills} skills"
    )
    return problems


def next_pdf_path(folder: Path) -> Path:
    candidate = folder / f"{PDF_BASE}.pdf"
    version = 2
    while candidate.exists():
        candidate = folder / f"{PDF_BASE}_v{version}.pdf"
        version += 1
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tex", required=True, type=Path)
    parser.add_argument("--company", required=True, help="lowercase company folder name")
    parser.add_argument("--folder", required=True, help="YYYY-MM-DD(Position-Name_JobID)")
    parser.add_argument("--preview", action="store_true", help="also render a PNG preview next to the .tex")
    parser.add_argument("--overwrite", action="store_true", help="replace the latest PDF instead of versioning")
    parser.add_argument("--email", default=CONTACT_EMAIL, help="contact email expected in the header (one-off override)")
    args = parser.parse_args()

    tex_path = args.tex.resolve()
    tex = tex_path.read_text(encoding="utf-8")
    problems = lint(tex)

    with tempfile.TemporaryDirectory(prefix="resume_build_") as tmp:
        result = subprocess.run(
            [find_tectonic(), "--outdir", tmp, str(tex_path)],
            capture_output=True,
            text=True,
        )
        built = Path(tmp) / f"{tex_path.stem}.pdf"
        if result.returncode or not built.exists():
            print(result.stdout[-3000:], result.stderr[-3000:], sep="\n")
            raise SystemExit("tectonic failed")

        reader = PdfReader(str(built))
        pages = len(reader.pages)
        if pages != 1:
            problems.append(f"PDF has {pages} pages (need exactly 1)")
        # ATS parsers read the text layer: the email must extract as a standalone token with no glyph junk.
        header = reader.pages[0].extract_text().split("Summary", 1)[0]
        if not re.search(rf"(?<!\S){re.escape(args.email)}(?!\S)", header):
            problems.append(f"header text does not contain a clean '{args.email}' token: {header!r}")
        if any(ord(ch) > 127 for ch in header):
            problems.append(f"header text contains non-ASCII characters (icon glyph leak?): {header!r}")

        out_dir = COMPANY_ROOT / args.company.strip().lower() / args.folder
        out_dir.mkdir(parents=True, exist_ok=True)
        existing = sorted(
            out_dir.glob(f"{PDF_BASE}*.pdf"),
            key=lambda p: int(m.group(1)) if (m := re.search(r"_v(\d+)$", p.stem)) else 1,
        )
        target = existing[-1] if args.overwrite and existing else next_pdf_path(out_dir)
        shutil.copyfile(built, target)

    if args.preview:
        import pymupdf as fitz

        preview = tex_path.with_suffix(".png")
        doc = fitz.open(target)
        doc[0].get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).save(preview)
        print(f"preview: {preview}")
        print(f"last text line at y={doc[0].get_text('blocks')[-1][3]:.0f} of {doc[0].rect.height:.0f}")

    print(f"pdf: {target}")
    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
