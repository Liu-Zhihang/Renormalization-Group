#!/usr/bin/env python3
"""
Replace LaTeX formulas in image alt text with Unicode equivalents.
This is needed because glightbox captions don't render LaTeX.
"""

import re
import os
from pathlib import Path

# LaTeX to Unicode replacement rules
LATEX_REPLACEMENTS = [
    # Greek letters
    (r'\$\\alpha\$', 'α'),
    (r'\$\\beta\$', 'β'),
    (r'\$\\gamma\$', 'γ'),
    (r'\$\\delta\$', 'δ'),
    (r'\$\\epsilon\$', 'ε'),
    (r'\$\\zeta\$', 'ζ'),
    (r'\$\\eta\$', 'η'),
    (r'\$\\theta\$', 'θ'),
    (r'\$\\lambda\$', 'λ'),
    (r'\$\\mu\$', 'μ'),
    (r'\$\\nu\$', 'ν'),
    (r'\$\\xi\$', 'ξ'),
    (r'\$\\pi\$', 'π'),
    (r'\$\\rho\$', 'ρ'),
    (r'\$\\sigma\$', 'σ'),
    (r'\$\\tau\$', 'τ'),
    (r'\$\\phi\$', 'φ'),
    (r'\$\\chi\$', 'χ'),
    (r'\$\\psi\$', 'ψ'),
    (r'\$\\omega\$', 'ω'),
    (r'\$\\Gamma\$', 'Γ'),
    (r'\$\\Delta\$', 'Δ'),
    (r'\$\\Theta\$', 'Θ'),
    (r'\$\\Lambda\$', 'Λ'),
    (r'\$\\Xi\$', 'Ξ'),
    (r'\$\\Pi\$', 'Π'),
    (r'\$\\Sigma\$', 'Σ'),
    (r'\$\\Phi\$', 'Φ'),
    (r'\$\\Psi\$', 'Ψ'),
    (r'\$\\Omega\$', 'Ω'),
    
    # Subscripts
    (r'_\{c\}', 'c'),
    (r'_c', 'c'),
    (r'_0', '₀'),
    (r'_1', '₁'),
    (r'_2', '₂'),
    (r'_\{0\}', '₀'),
    (r'_\{1\}', '₁'),
    (r'_\{2\}', '₂'),
    (r'_V', 'V'),
    
    # Superscripts
    (r'\^\{-1\}', '⁻¹'),
    (r'\^\{-2\}', '⁻²'),
    (r'\^2', '²'),
    (r'\^\{2\}', '²'),
    (r'\^3', '³'),
    (r'\^\{3\}', '³'),
    (r'\^\*', '*'),
    
    # Operators and symbols
    (r'\\to', '→'),
    (r'\\rightarrow', '→'),
    (r'\\leftarrow', '←'),
    (r'\\leftrightarrow', '↔'),
    (r'\\infty', '∞'),
    (r'\\approx', '≈'),
    (r'\\sim', '~'),
    (r'\\times', '×'),
    (r'\\cdot', '·'),
    (r'\\pm', '±'),
    (r'\\mp', '∓'),
    (r'\\leq', '≤'),
    (r'\\geq', '≥'),
    (r'\\neq', '≠'),
    (r'\\partial', '∂'),
    (r'\\nabla', '∇'),
    (r'\\sum', 'Σ'),
    (r'\\prod', 'Π'),
    (r'\\int', '∫'),
    
    # Common patterns
    (r'\\bar\{c\}', 'c̄'),
    (r'\\bar\{T\}', 'T̄'),
    (r'\\bar\{\\nu\}', 'ν̄'),
    (r'\\tilde\{', ''),
    (r'\\hat\{', ''),
    (r'\\vec\{', ''),
    (r'\\mathbb\{Z\}', 'ℤ'),
    (r'\\mathbb\{R\}', 'ℝ'),
    
    # Fractions (simplified)
    (r'\\frac\{1\}\{2\}', '1/2'),
    (r'\\frac\{1\}\{3\}', '1/3'),
    (r'\\frac\{1\}\{4\}', '1/4'),
    
    # Text commands
    (r'\\text\{', ''),
    (r'\\mathrm\{', ''),
    
    # Clean up remaining braces
    (r'\{', ''),
    (r'\}', ''),
]


def replace_latex_in_alt_text(content):
    """Replace LaTeX in image alt text only, preserving body text."""
    
    def process_alt(match):
        alt_text = match.group(1)
        path = match.group(2)
        
        # Apply all LaTeX replacements to alt text
        new_alt = alt_text
        for pattern, replacement in LATEX_REPLACEMENTS:
            new_alt = re.sub(pattern, replacement, new_alt)
        
        # Remove remaining $ signs
        new_alt = new_alt.replace('$', '')
        
        # Return complete image syntax with closing paren
        return f'![{new_alt}]({path})'
    
    # Match image syntax: ![alt text](path)
    # Handle multiline alt text with DOTALL flag
    pattern = r'!\[((?:[^\[\]]|\[(?:[^\[\]]|\[[^\[\]]*\])*\])*)\]\(([^)]+)\)'
    
    return re.sub(pattern, process_alt, content, flags=re.DOTALL)


def process_file(filepath):
    """Process a single markdown file."""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = replace_latex_in_alt_text(content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Updated: {filepath}")
        return True
    else:
        print(f"  No changes: {filepath}")
        return False


def main():
    # Get the docs directory
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / 'docs'
    
    # Find all markdown files
    md_files = list(docs_dir.glob('**/*.md'))
    
    updated_count = 0
    for md_file in md_files:
        if process_file(md_file):
            updated_count += 1
    
    print(f"\nDone! Updated {updated_count} files.")


if __name__ == '__main__':
    main()
