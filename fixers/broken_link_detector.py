"""
Broken Link Detector
Identifies broken internal links, missing pages, and invalid anchors

Improves: Navigation, user experience, findability

Based on 00_comprehensive_analysis.md findings (10+ broken links found)

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
import os
from typing import List, Set, Dict
from pathlib import Path

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class BrokenLinkDetector(BaseFixer):
    """
    Detects broken links and missing pages

    Detection:
    - Internal links to non-existent files
    - Broken anchor links
    - Expected pages that don't exist
    - Invalid URL formats

    Auto-fix: Not auto-fixable (requires creating missing content or updating links)
    """

    def __init__(self, config: Config):
        super().__init__(config)

        # Common expected pages that are often missing
        self.expected_pages = {
            '/en/api/authentication',
            '/en/api/endpoints',
            '/en/api/complete-reference',
            '/en/docs/agents-and-tools',
        }

        # Cache of existing files (populated during check)
        self.existing_files: Set[str] = set()
        self.file_anchors: Dict[str, Set[str]] = {}  # file_path -> set of anchor IDs

    @property
    def name(self) -> str:
        return "Broken Link Detector"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Find broken links and missing pages"""
        issues = []

        # Build cache of existing files if not already done
        if not self.existing_files:
            self._build_file_cache(file_path)

        # Extract anchors from this file
        self._extract_anchors(file_path, content)

        lines = content.split('\n')
        in_code_block = False

        for i, line in enumerate(lines, 1):
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Find markdown links [text](url)
            markdown_links = re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', line)

            for match in markdown_links:
                link_text = match.group(1)
                link_url = match.group(2).strip()

                # Skip external links (we can't validate these easily)
                if link_url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                    continue

                # Check internal links
                link_issue = self._validate_internal_link(file_path, link_url, link_text, i)
                if link_issue:
                    issues.append(link_issue)

            # Find HTML links
            html_links = re.finditer(r'<a\s+href=["\']([^"\']+)["\']', line)

            for match in html_links:
                link_url = match.group(1).strip()

                if link_url.startswith(('http://', 'https://', 'mailto:', 'tel:')):
                    continue

                link_issue = self._validate_internal_link(file_path, link_url, '', i)
                if link_issue:
                    issues.append(link_issue)

        # Check for expected missing pages (only once per file)
        for expected_page in self.expected_pages:
            if not self._page_exists(expected_page):
                issues.append(Issue(
                    severity='high',
                    category='ia',
                    file_path=file_path,
                    line_number=1,
                    issue_type='missing_expected_page',
                    description=f'Expected page is missing: {expected_page}',
                    suggestion=f'Create {expected_page} page',
                    context='',
                    auto_fixable=False
                ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Broken links require manual fixing - report only"""
        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=content,
            fixes_applied=[],
            issues_fixed=[]
        )

    def _build_file_cache(self, current_file: str):
        """Build cache of all existing .md and .mdx files"""
        # Get project root (go up until we find docs/ or api/ directory)
        current_path = Path(current_file).parent

        # Find root by looking for common docs directories
        root_path = current_path
        while root_path.parent != root_path:
            if (root_path / 'docs').exists() or (root_path / 'api').exists():
                break
            root_path = root_path.parent

        # Scan for all .md and .mdx files
        for pattern in ['**/*.md', '**/*.mdx']:
            for file_path in root_path.rglob(pattern):
                relative_path = file_path.relative_to(root_path)
                self.existing_files.add(str(relative_path))
                self.existing_files.add('/' + str(relative_path))  # Also with leading slash

    def _extract_anchors(self, file_path: str, content: str):
        """Extract all heading anchors from file content"""
        anchors = set()
        lines = content.split('\n')

        for line in lines:
            # Find markdown headings
            heading_match = re.match(r'^(#+)\s+(.+)$', line.strip())
            if heading_match:
                heading_text = heading_match.group(2)
                # Convert to anchor ID (lowercase, replace spaces with hyphens)
                anchor_id = heading_text.lower()
                anchor_id = re.sub(r'[^\w\s-]', '', anchor_id)  # Remove special chars
                anchor_id = re.sub(r'[-\s]+', '-', anchor_id)  # Replace spaces/hyphens with single hyphen
                anchor_id = anchor_id.strip('-')  # Remove leading/trailing hyphens
                anchors.add(anchor_id)

        self.file_anchors[file_path] = anchors

    def _validate_internal_link(self, current_file: str, link_url: str, link_text: str, line_number: int) -> Issue | None:
        """Validate an internal link and return Issue if broken"""

        # Split anchor from path
        if '#' in link_url:
            file_part, anchor_part = link_url.split('#', 1)
        else:
            file_part = link_url
            anchor_part = None

        # Skip if it's just an anchor (same-page link)
        if not file_part and anchor_part:
            # Validate anchor exists in current file
            if anchor_part not in self.file_anchors.get(current_file, set()):
                return Issue(
                    severity='medium',
                    category='ia',
                    file_path=current_file,
                    line_number=line_number,
                    issue_type='broken_anchor',
                    description=f'Broken anchor link: #{anchor_part} does not exist in this file',
                    suggestion='Check heading exists or fix anchor link',
                    context=f'[{link_text}](#{anchor_part})',
                    auto_fixable=False
                )
            return None

        # Check if file exists
        if file_part and not self._page_exists(file_part):
            return Issue(
                severity='high',
                category='ia',
                file_path=current_file,
                line_number=line_number,
                issue_type='broken_link',
                description=f'Broken link: {file_part} does not exist',
                suggestion='Create the missing page or update the link',
                context=f'[{link_text}]({link_url})',
                auto_fixable=False
            )

        # If file exists and has anchor, validate anchor
        if file_part and anchor_part:
            target_anchors = self.file_anchors.get(file_part, set())
            if target_anchors and anchor_part not in target_anchors:
                return Issue(
                    severity='medium',
                    category='ia',
                    file_path=current_file,
                    line_number=line_number,
                    issue_type='broken_anchor',
                    description=f'Broken anchor link: {file_part}#{anchor_part} (anchor does not exist)',
                    suggestion='Check target heading exists or fix anchor',
                    context=f'[{link_text}]({link_url})',
                    auto_fixable=False
                )

        return None

    def _page_exists(self, page_path: str) -> bool:
        """Check if a page exists in the file cache"""
        # Normalize path
        page_path = page_path.strip()

        # Handle different path formats
        variations = [
            page_path,
            page_path + '.md',
            page_path + '.mdx',
            page_path.lstrip('/'),
            page_path.lstrip('/') + '.md',
            page_path.lstrip('/') + '.mdx',
            'docs' + page_path,
            'docs' + page_path + '.md',
            'docs' + page_path + '.mdx',
            'api' + page_path,
            'api' + page_path + '.md',
            'api' + page_path + '.mdx',
        ]

        return any(var in self.existing_files for var in variations)
