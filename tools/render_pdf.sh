#!/usr/bin/env bash
# Render a markdown notes/practice file to PDF with properly typeset math.
#
# Usage: bash tools/render_pdf.sh <file.md>

set -euo pipefail

if [ $# -ne 1 ]; then
    echo "Usage: bash tools/render_pdf.sh <file.md>" >&2
    exit 1
fi

input="$1"

if [ ! -f "$input" ]; then
    echo "Error: file not found: $input" >&2
    exit 1
fi

if ! command -v pandoc >/dev/null 2>&1; then
    cat >&2 <<'EOF'
Error: pandoc is not installed (or not on your PATH).

Install it, then re-run this script:
  - macOS:   brew install pandoc
  - Linux:   apt install pandoc   (or your distro's package manager)
  - Windows: winget install pandoc  (or scoop install pandoc)
  - Any OS:  https://pandoc.org/installing.html

You also need a LaTeX engine (xelatex) for math-heavy PDFs:
  - macOS:   brew install --cask mactex-no-gui
  - Linux:   apt install texlive-xetex
  - Windows: install MiKTeX (https://miktex.org) or TeX Live
EOF
    exit 1
fi

if ! command -v xelatex >/dev/null 2>&1; then
    cat >&2 <<'EOF'
Error: xelatex is not installed (or not on your PATH).

pandoc needs a LaTeX engine to produce a PDF:
  - macOS:   brew install --cask mactex-no-gui
  - Linux:   apt install texlive-xetex
  - Windows: install MiKTeX (https://miktex.org) or TeX Live
EOF
    exit 1
fi

output="${input%.md}.pdf"

pandoc "$input" \
    --pdf-engine=xelatex \
    -V geometry:margin=1in \
    -o "$output"

echo "Wrote $output"
