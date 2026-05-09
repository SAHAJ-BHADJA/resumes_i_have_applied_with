import argparse
import shutil
import subprocess
import tempfile
from datetime import date
from pathlib import Path


PDFLATEX_CANDIDATES = [
    "pdflatex",
    r"C:\Users\sahaj\AppData\Local\Programs\MiKTeX\miktex\bin\x64\pdflatex.exe",
    r"C:\Program Files\MiKTeX\miktex\bin\x64\pdflatex.exe",
    r"C:\Program Files\MiKTeX\miktex\bin\pdflatex.exe",
    r"C:\texlive\2025\bin\windows\pdflatex.exe",
]


def find_pdflatex() -> str | None:
    for candidate in PDFLATEX_CANDIDATES:
        resolved = shutil.which(candidate) if "\\" not in candidate else candidate
        if resolved and Path(resolved).exists():
            return resolved
    return None


def next_version_path(base_dir: Path, filename_base: str) -> Path:
    base_path = base_dir / f"{filename_base}.pdf"
    if not base_path.exists():
        return base_path

    version = 2
    while True:
        path = base_dir / f"{filename_base}_v{version}.pdf"
        if not path.exists():
            return path
        version += 1


def compile_pdf(pdflatex: str, tex_source: Path, output_dir: Path) -> Path:
    with tempfile.TemporaryDirectory(prefix="resume_build_") as temp_dir:
        temp_path = Path(temp_dir)
        temp_tex = temp_path / tex_source.name
        temp_tex.write_text(tex_source.read_text(encoding="utf-8"), encoding="utf-8")

        for _ in range(2):
            subprocess.run(
                [pdflatex, "-interaction=nonstopmode", "-halt-on-error", temp_tex.name],
                cwd=temp_path,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

        produced_pdf = temp_path / f"{temp_tex.stem}.pdf"
        target_pdf = output_dir / produced_pdf.name
        shutil.copy2(produced_pdf, target_pdf)
        return target_pdf


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile a LaTeX resume and store only the PDF.")
    parser.add_argument("--company", required=True, help="Lowercase company folder name.")
    parser.add_argument(
        "--date",
        default=str(date.today()),
        help="Folder date in YYYY-MM-DD format. Defaults to today.",
    )
    parser.add_argument("--tex", required=True, help="Path to the temporary or source TeX file.")
    parser.add_argument(
        "--name",
        default="Sahaj_Bhavesh_Bhadja",
        help="Base filename without version suffix.",
    )
    args = parser.parse_args()

    pdflatex = find_pdflatex()
    if not pdflatex:
        raise SystemExit(
            "pdflatex was not found. Install a LaTeX distribution or add pdflatex to PATH before rendering."
        )

    company = args.company.strip().lower()
    output_dir = Path(r"E:\Projects\Random\Resume") / company / args.date
    output_dir.mkdir(parents=True, exist_ok=True)

    tex_source = Path(args.tex).resolve()
    compiled_pdf = compile_pdf(pdflatex, tex_source, output_dir)
    final_pdf = next_version_path(output_dir, args.name)
    compiled_pdf.replace(final_pdf)
    print(final_pdf)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
