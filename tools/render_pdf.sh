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
tool_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

font_available() {
    command -v fc-list >/dev/null 2>&1 && fc-list 2>/dev/null | grep -qi "$1"
}

# A readable serif body font. Preference order: Georgia (designed for
# screen reading), then two common fallbacks, then none (Latin Modern,
# LaTeX's default, if the system has none of these).
mainfont=""
for candidate in "Georgia" "Constantia" "Cambria"; do
    if font_available "$candidate"; then
        mainfont="$candidate"
        break
    fi
done
mainfont_args=()
if [ -n "$mainfont" ]; then
    mainfont_args=(-V "mainfont=$mainfont")
fi

# This project's notes/practice files use a few Unicode symbols (⭐ ⚠ ≈ →)
# for emphasis, uncertainty marks, and arrows that most text fonts
# (including the ones above) don't include, so they'd otherwise silently
# vanish from the PDF. Rather than switch the whole document to a symbol
# font, substitute just those glyphs from "Segoe UI Symbol" (ships with
# Windows), via a small generated header file. Skipped where that font
# isn't available — rendering still succeeds, just possibly missing those
# specific glyphs.
include_args=(--include-in-header="$tool_dir/pdf_style.tex")
symbol_header=""
if font_available "Segoe UI Symbol"; then
    symbol_header="${output}.symbols.tex.tmp"
    cat > "$symbol_header" <<'EOF'
\usepackage{newunicodechar}
\newfontfamily\pdfsymbolfont{Segoe UI Symbol}
\newunicodechar{⭐}{{\color{ens-heading!60!orange}\pdfsymbolfont⭐}}
\newunicodechar{⚠}{{\color{orange!80!red}\pdfsymbolfont⚠}}
\newunicodechar{≈}{{\pdfsymbolfont≈}}
\newunicodechar{→}{{\pdfsymbolfont→}}
EOF
    include_args+=(--include-in-header="$symbol_header")
    trap 'rm -f "$symbol_header"' EXIT
fi

# Read as GitHub-Flavored Markdown (what these files are actually written
# in) plus $...$ math (gfm alone doesn't support LaTeX math) and "smart"
# typography (curly quotes, proper dashes — off by default for gfm, unlike
# pandoc's own markdown dialect).
pandoc "$input" \
    --from=gfm+tex_math_dollars+smart \
    --pdf-engine=xelatex \
    -V geometry:margin=1in \
    -V linestretch=1.15 \
    -V fontsize=11pt \
    -V colorlinks=true \
    -V linkcolor=ens-heading \
    "${mainfont_args[@]}" \
    "${include_args[@]}" \
    -o "$output"

[ -n "$symbol_header" ] && rm -f "$symbol_header"

echo "Wrote $output"
