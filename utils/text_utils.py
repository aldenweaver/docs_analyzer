"""
Text processing utilities for doc_fixer
"""

import re
import yaml
from typing import Optional, Tuple, Dict, Any


def extract_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str, int]:
    """
    Extract YAML frontmatter from markdown content

    Args:
        content: Markdown file content

    Returns:
        Tuple of (frontmatter_dict, body_content, frontmatter_end_line)
        Returns (None, content, 0) if no frontmatter found
    """
    # Match YAML frontmatter between --- delimiters
    pattern = r'^---\s*\n(.*?)\n---\s*\n'
    match = re.match(pattern, content, re.DOTALL)

    if not match:
        return None, content, 0

    frontmatter_text = match.group(1)
    body = content[match.end():]

    # Count lines in frontmatter (including delimiters)
    frontmatter_lines = content[:match.end()].count('\n')

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter, body, frontmatter_lines
    except yaml.YAMLError:
        return None, content, 0


def replace_frontmatter(content: str, new_frontmatter: Dict[str, Any]) -> str:
    """
    Replace or add YAML frontmatter in markdown content

    Args:
        content: Original markdown content
        new_frontmatter: Dictionary of frontmatter fields

    Returns:
        Updated markdown content with new frontmatter
    """
    # Remove existing frontmatter if present
    pattern = r'^---\s*\n.*?\n---\s*\n'
    body = re.sub(pattern, '', content, count=1, flags=re.DOTALL)

    # Generate new frontmatter
    frontmatter_yaml = yaml.dump(new_frontmatter, default_flow_style=False, sort_keys=False)

    # Combine frontmatter and body
    return f"---\n{frontmatter_yaml}---\n{body}"


def normalize_whitespace(text: str) -> str:
    """
    Normalize whitespace in text
    - Remove trailing whitespace
    - Ensure single blank line between sections
    - Ensure file ends with single newline

    Args:
        text: Input text

    Returns:
        Normalized text
    """
    # Split into lines and strip trailing whitespace
    lines = [line.rstrip() for line in text.split('\n')]

    # Remove multiple consecutive blank lines (keep max 2)
    normalized = []
    blank_count = 0

    for line in lines:
        if line == '':
            blank_count += 1
            if blank_count <= 2:
                normalized.append(line)
        else:
            blank_count = 0
            normalized.append(line)

    # Join and ensure single trailing newline
    result = '\n'.join(normalized)

    # Ensure file ends with exactly one newline
    result = result.rstrip('\n') + '\n'

    return result


def count_lines(text: str) -> int:
    """Count number of lines in text"""
    return text.count('\n') + 1 if text else 0


def find_line_number(content: str, search_text: str, start_line: int = 1) -> Optional[int]:
    """
    Find line number of text in content

    Args:
        content: Full file content
        search_text: Text to search for
        start_line: Line number to start search from (1-indexed)

    Returns:
        Line number (1-indexed) or None if not found
    """
    lines = content.split('\n')

    for i, line in enumerate(lines[start_line - 1:], start=start_line):
        if search_text in line:
            return i

    return None


def extract_code_blocks(content: str) -> list:
    """
    Extract all code blocks from markdown content

    Returns:
        List of tuples: (language, code, line_number)
    """
    pattern = r'^```(\w*)\n(.*?)\n```'
    matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)

    code_blocks = []
    for match in matches:
        language = match.group(1) or None
        code = match.group(2)
        line_number = content[:match.start()].count('\n') + 1
        code_blocks.append((language, code, line_number))

    return code_blocks


def replace_text_preserve_case(text: str, old: str, new: str) -> str:
    """
    Replace text while attempting to preserve case patterns

    Args:
        text: Input text
        old: Text to replace
        new: Replacement text

    Returns:
        Text with replacements
    """
    # If old text is all uppercase, keep new text uppercase
    if old.isupper():
        return text.replace(old, new.upper())

    # If old text is title case, make new text title case
    if old.istitle():
        return text.replace(old, new.title())

    # Otherwise, use new text as-is
    return text.replace(old, new)


def word_boundary_replace(text: str, old: str, new: str, case_sensitive: bool = True) -> str:
    """
    Replace whole words only (respecting word boundaries)

    Args:
        text: Input text
        old: Word to replace
        new: Replacement word
        case_sensitive: Whether replacement should be case-sensitive

    Returns:
        Text with whole-word replacements
    """
    flags = 0 if case_sensitive else re.IGNORECASE
    pattern = r'\b' + re.escape(old) + r'\b'
    return re.sub(pattern, new, text, flags=flags)
