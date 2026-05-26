# Setup Guide

Follow these steps to set up the resume generator on your machine.

## Step 1: Install LaTeX

Choose ONE of these options:

### Option A: Overleaf (Easiest - No Installation)

1. Go to [overleaf.com](https://www.overleaf.com/)
2. Create a free account
3. Upload the `FORMAT_BASELINE/resume_template.tex` file
4. Edit directly in the browser and download PDFs

### Option B: TeX Live (Windows/Mac/Linux)

**Windows:**
1. Download from [tug.org/texlive](https://www.tug.org/texlive/)
2. Run the installer (full installation recommended)
3. Restart your terminal

**Mac:**
```bash
brew install --cask mactex
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install texlive-full
```

### Option C: MiKTeX (Windows)

1. Download from [miktex.org](https://miktex.org/download)
2. Run installer
3. Select "Install missing packages on-the-fly: Yes"

## Step 2: Verify Installation

Open a terminal and run:
```bash
pdflatex --version
```

You should see version information if installed correctly.

## Step 3: Install Required Packages

If using TeX Live or MiKTeX, these packages should be included. If any are missing:

**TeX Live:**
```bash
tlmgr install fontawesome5 enumitem fancyhdr titlesec
```

**MiKTeX:** Packages install automatically when you first compile.

## Step 4: Set Up Your Data

1. Copy `master_resume_data_TEMPLATE.json` to `master_resume_data.json`
2. Fill in your personal information
3. Add your education, experiences, projects, and skills

## Step 5: Generate Your First Resume

1. Copy `FORMAT_BASELINE/resume_template.tex` to `OUTPUT/MyResume.tex`
2. Open `FORMAT_BASELINE/sample_resume.tex` as a reference
3. Replace the placeholder content with your actual data
4. Compile:

```bash
cd OUTPUT
pdflatex MyResume.tex
```

Your PDF will be generated as `MyResume.pdf`.

## Troubleshooting

### "Package fontawesome5 not found"
Install the package:
```bash
tlmgr install fontawesome5
```

### PDF doesn't fit on one page
1. First, shorten your bullet points (aim for 25-30 words each)
2. Only then adjust spacing values in the template

### Text overflows to the right
Reword the bullet to be shorter - don't break lines manually.

## Editor Recommendations

- **VS Code** with LaTeX Workshop extension
- **TeXstudio** - dedicated LaTeX editor
- **Overleaf** - browser-based, no setup needed

## Folder Structure for Multiple Applications

Recommended organization:
```
OUTPUT/
├── Google/
│   └── 2024-01-15/
│       ├── resume.tex
│       └── resume.pdf
├── Microsoft/
│   └── 2024-01-20/
│       ├── resume.tex
│       └── resume.pdf
```

This keeps each tailored resume organized and versioned by date.
