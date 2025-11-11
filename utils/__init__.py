"""
Utility functions for doc_fixer
"""

from .text_utils import (
    extract_frontmatter,
    replace_frontmatter,
    normalize_whitespace,
    count_lines,
    find_line_number
)

__all__ = [
    'extract_frontmatter',
    'replace_frontmatter',
    'normalize_whitespace',
    'count_lines',
    'find_line_number'
]
