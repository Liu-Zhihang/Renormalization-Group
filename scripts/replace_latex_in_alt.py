#!/usr/bin/env python3
"""
Replace LaTeX formulas in image alt text with Unicode equivalents.
This is needed because glightbox captions don't render LaTeX.
"""

import re
from pathlib import Path

# LaTeX command to Unicode mapping (without $ wrapping)
LATEX_COMMANDS = {
    # Greek letters (lowercase)
    r'\\alpha': 'α',
    r'\\beta': 'β',
    r'\\gamma': 'γ',
    r'\\delta': 'δ',
    r'\\epsilon': 'ε',
    r'\\varepsilon': 'ε',
    r'\\zeta': 'ζ',
    r'\\eta': 'η',
    r'\\theta': 'θ',
    r'\\vartheta': 'ϑ',
    r'\\iota': 'ι',
    r'\\kappa': 'κ',
    r'\\lambda': 'λ',
    r'\\mu': 'μ',
    r'\\nu': 'ν',
    r'\\xi': 'ξ',
    r'\\pi': 'π',
    r'\\rho': 'ρ',
    r'\\sigma': 'σ',
    r'\\tau': 'τ',
    r'\\upsilon': 'υ',
    r'\\phi': 'φ',
    r'\\varphi': 'φ',
    r'\\chi': 'χ',
    r'\\psi': 'ψ',
    r'\\omega': 'ω',
    # Greek letters (uppercase)
    r'\\Gamma': 'Γ',
    r'\\Delta': 'Δ',
    r'\\Theta': 'Θ',
    r'\\Lambda': 'Λ',
    r'\\Xi': 'Ξ',
    r'\\Pi': 'Π',
    r'\\Sigma': 'Σ',
    r'\\Upsilon': 'Υ',
    r'\\Phi': 'Φ',
    r'\\Psi': 'Ψ',
    r'\\Omega': 'Ω',
    # Operators and symbols
    r'\\to': '→',
    r'\\rightarrow': '→',
    r'\\leftarrow': '←',
    r'\\leftrightarrow': '↔',
    r'\\Rightarrow': '⇒',
    r'\\Leftarrow': '⇐',
    r'\\infty': '∞',
    r'\\approx': '≈',
    r'\\sim': '~',
    r'\\simeq': '≃',
    r'\\equiv': '≡',
    r'\\neq': '≠',
    r'\\leq': '≤',
    r'\\geq': '≥',
    r'\\ll': '≪',
    r'\\gg': '≫',
    r'\\times': '×',
    r'\\cdot': '·',
    r'\\pm': '±',
    r'\\mp': '∓',
    r'\\partial': '∂',
    r'\\nabla': '∇',
    r'\\sum': 'Σ',
    r'\\prod': 'Π',
    r'\\int': '∫',
    r'\\propto': '∝',
    r'\\subset': '⊂',
    r'\\supset': '⊃',
    r'\\in': '∈',
    r'\\forall': '∀',
    r'\\exists': '∃',
    r'\\langle': '⟨',
    r'\\rangle': '⟩',
    r'\\sqrt': '√',
    r'\\prime': '′',
    # Special
    r'\\bar': '',  # Will handle separately
    r'\\hat': '',
    r'\\tilde': '',
    r'\\vec': '',
    r'\\overline': '',
}

# Superscripts and subscripts
SUPERSCRIPTS = {
    '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
    '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
    '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
    'n': 'ⁿ', 'i': 'ⁱ',
}

SUBSCRIPTS = {
    '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
    '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
    '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
    'a': 'ₐ', 'e': 'ₑ', 'o': 'ₒ', 'x': 'ₓ',
    'h': 'ₕ', 'k': 'ₖ', 'l': 'ₗ', 'm': 'ₘ', 'n': 'ₙ',
    'p': 'ₚ', 's': 'ₛ', 't': 'ₜ',
}


def replace_latex_in_text(text):
    """Replace all LaTeX commands in text with Unicode."""
    result = text
    
    # Replace LaTeX commands
    for latex, unicode_char in LATEX_COMMANDS.items():
        result = re.sub(latex, unicode_char, result)
    
    # Handle superscripts: ^{...} or ^x
    def replace_superscript(m):
        content = m.group(1) if m.group(1) else m.group(2)
        return ''.join(SUPERSCRIPTS.get(c, c) for c in content)
    result = re.sub(r'\^\{([^}]+)\}|\^([0-9a-zA-Z+-])', replace_superscript, result)
    
    # Handle subscripts: _{...} or _x
    def replace_subscript(m):
        content = m.group(1) if m.group(1) else m.group(2)
        return ''.join(SUBSCRIPTS.get(c, c) for c in content)
    result = re.sub(r'_\{([^}]+)\}|_([0-9a-zA-Z])', replace_subscript, result)
    
    # Remove remaining braces
    result = re.sub(r'\{([^}]*)\}', r'\1', result)
    
    # Remove $ signs
    result = result.replace('$', '')
    
    # Clean up extra backslashes
    result = re.sub(r'\\([a-zA-Z]+)', r'\1', result)  # Remove remaining \commands
    
    return result


def replace_latex_in_alt_text(content):
    """Replace LaTeX in image alt text only, preserving body text."""
    
    def process_alt(match):
        alt_text = match.group(1)
        path = match.group(2)
        
        # Apply LaTeX replacements to alt text
        new_alt = replace_latex_in_text(alt_text)
        
        # Return complete image syntax with closing paren
        return f'![{new_alt}]({path})'
    
    # Match image syntax: ![alt text](path)
    # Handle multiline alt text with DOTALL flag
    pattern = r'!\[((?:[^\[\]]|\[(?:[^\[\]]|\[[^\[\]]*\])*\])*)\]\(([^)]+)\)'
    
    return re.sub(pattern, process_alt, content, flags=re.DOTALL)


def process_file(filepath):
    """Process a single markdown file."""
    print(f"Processing: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = replace_latex_in_alt_text(content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  Updated: {filepath.name}")
        return True
    else:
        print(f"  No changes: {filepath.name}")
        return False


def main():
    script_dir = Path(__file__).parent
    docs_dir = script_dir.parent / 'docs'
    
    md_files = list(docs_dir.glob('**/*.md'))
    
    updated_count = 0
    for md_file in md_files:
        if process_file(md_file):
            updated_count += 1
    
    print(f"\nDone! Updated {updated_count} files.")


if __name__ == '__main__':
    main()
