"""
URL fixer - fixes URL and link issues
Focuses on converting absolute internal URLs to relative paths
"""

import re
from typing import List
from pathlib import Path
from urllib.parse import urlparse

from core.models import Issue, FixResult
from core.config import Config
from fixers.base import BaseFixer


class URLFixer(BaseFixer):
    """Fixes URL and link issues"""

    def __init__(self, config: Config):
        super().__init__(config)
        self.internal_must_be_relative = config.internal_links_must_be_relative
        self.poor_link_text = ['here', 'click here', 'link', 'this', 'read more']

        # Common domains that should use relative paths (Mintlify docs)
        self.internal_domains = [
            'docs.anthropic.com',
            'anthropic.com/docs',
            'localhost',
        ]

    @property
    def name(self) -> str:
        return "URLFixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check file for URL issues"""
        issues = []
        lines = content.split('\n')

        # Pattern to match markdown links: [text](url)
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')

        # Skip frontmatter
        in_frontmatter = False

        for line_num, line in enumerate(lines, 1):
            # Track frontmatter
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue

            if in_frontmatter:
                continue

            # Find all links in the line
            for match in link_pattern.finditer(line):
                link_text = match.group(1)
                link_url = match.group(2)

                # Check for poor link text
                if link_text.lower().strip() in self.poor_link_text:
                    issues.append(Issue(
                        severity="medium",
                        category="ux",
                        file_path=file_path,
                        line_number=line_num,
                        issue_type="poor_link_text",
                        description=f"Poor link text: '{link_text}' is not descriptive",
                        suggestion="Use descriptive link text that explains the destination",
                        context=line.strip(),
                        auto_fixable=False  # Requires human judgment
                    ))

                # Check for absolute URLs that should be relative
                if self.internal_must_be_relative:
                    parsed = urlparse(link_url)

                    # If it's an absolute URL with a domain
                    if parsed.scheme in ['http', 'https'] and parsed.netloc:
                        # Check if it's an internal domain
                        is_internal = any(domain in parsed.netloc for domain in self.internal_domains)

                        if is_internal:
                            issues.append(Issue(
                                severity="high",
                                category="mintlify",
                                file_path=file_path,
                                line_number=line_num,
                                issue_type="absolute_internal_url",
                                description=f"Internal link uses absolute URL: {link_url}",
                                suggestion=f"Convert to relative path",
                                context=line.strip(),
                                auto_fixable=True
                            ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Apply URL fixes"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        # Only fix absolute internal URLs
        absolute_url_issues = [i for i in issues if i.issue_type == "absolute_internal_url"]

        for issue in absolute_url_issues:
            # Extract the URL from the context
            link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
            match = link_pattern.search(issue.context)

            if match:
                link_text = match.group(1)
                absolute_url = match.group(2)

                # Convert to relative URL
                relative_url = self._convert_to_relative(absolute_url)

                if relative_url:
                    # Replace in content
                    old_link = f"[{link_text}]({absolute_url})"
                    new_link = f"[{link_text}]({relative_url})"

                    before_fix = fixed_content
                    fixed_content = fixed_content.replace(old_link, new_link)

                    if before_fix != fixed_content:
                        fix_msg = f"Converted absolute URL to relative: {absolute_url} → {relative_url}"
                        if fix_msg not in fixes_applied:
                            fixes_applied.append(fix_msg)
                            issues_fixed.append(issue)

        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=fixed_content,
            fixes_applied=fixes_applied,
            issues_fixed=issues_fixed
        )

    def _convert_to_relative(self, absolute_url: str) -> str:
        """Convert absolute URL to relative path"""
        parsed = urlparse(absolute_url)

        # Extract the path component
        path = parsed.path

        # For docs sites, typically we want to keep the /en/docs/ structure
        # or convert to relative based on common patterns

        # If path starts with /en/docs/, keep it as-is
        if path.startswith('/en/docs/'):
            return path

        # If path starts with /docs/, keep it
        if path.startswith('/docs/'):
            return path

        # Otherwise, return the path component
        return path if path else '/'
