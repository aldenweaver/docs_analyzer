"""
Link Text Improver
Makes link text more descriptive and accessible

Improves: Accessibility, SEO, user experience

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
from typing import List

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class LinkTextImprover(BaseFixer):
    """
    Improves non-descriptive link text

    Detection: "click here", "here", "link", "this" as link text
    Auto-fix: Extracts context from surrounding text or URL
    """

    def __init__(self, config: Config):
        super().__init__(config)

        # Non-descriptive link patterns
        self.bad_link_patterns = [
            r'\[click here\]',
            r'\[here\]',
            r'\[link\]',
            r'\[this\]',
            r'\[read more\]',
        ]

    @property
    def name(self) -> str:
        return "Link Text Improver"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Find non-descriptive link text"""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for markdown links
            for match in re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', line):
                link_text = match.group(1).strip().lower()
                link_url = match.group(2)

                # Check if link text is non-descriptive
                if any(re.search(pattern, f'[{link_text}]', re.IGNORECASE) for pattern in self.bad_link_patterns):
                    # Try to infer better text from URL or surrounding context
                    better_text = self._infer_better_link_text(link_url, line, link_text)

                    issues.append(Issue(
                        severity='medium',
                        category='ux',
                        file_path=file_path,
                        line_number=i,
                        issue_type='non_descriptive_link',
                        description=f'Link text is non-descriptive: "{link_text}"',
                        suggestion=f'Consider using: "{better_text}"',
                        context=match.group(0),
                        auto_fixable=False  # Requires human judgment for best text
                    ))

                # Check for empty link text
                elif not link_text:
                    issues.append(Issue(
                        severity='high',
                        category='ux',
                        file_path=file_path,
                        line_number=i,
                        issue_type='empty_link_text',
                        description='Link has empty text',
                        suggestion='Provide descriptive link text',
                        context=match.group(0),
                        auto_fixable=False
                    ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Link text improvement requires human judgment - report only"""
        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=content,
            fixes_applied=[],
            issues_fixed=[]
        )

    def _infer_better_link_text(self, url: str, context_line: str, current_text: str) -> str:
        """Infer better link text from URL or context"""
        # Try to extract from URL
        if url.startswith('http'):
            # Extract domain or path
            parts = url.replace('https://', '').replace('http://', '').split('/')
            if len(parts) > 1:
                # Use path segments
                path_parts = [p for p in parts[1:] if p and p not in ['index.html', 'index.mdx']]
                if path_parts:
                    # Convert kebab-case to title case
                    return ' '.join(path_parts[-1].replace('-', ' ').replace('_', ' ').split()).title()

            # Use domain
            return f"Visit {parts[0]}"

        # For relative links, use the page name
        if url.endswith('.mdx') or url.endswith('.md'):
            page_name = url.split('/')[-1].replace('.mdx', '').replace('.md', '')
            return page_name.replace('-', ' ').replace('_', ' ').title()

        # Look for context around the link
        # Extract sentence containing the link
        sentence_match = re.search(r'([^.!?]*\[' + re.escape(current_text) + r'\][^.!?]*[.!?])', context_line)
        if sentence_match:
            sentence = sentence_match.group(1).strip()
            # Remove the link itself
            sentence = re.sub(r'\[' + re.escape(current_text) + r'\]\([^\)]+\)', '', sentence)
            # Take first few words as suggestion
            words = sentence.split()[:5]
            if words:
                return ' '.join(words)

        return "Read more"
