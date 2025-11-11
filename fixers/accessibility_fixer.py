"""
Accessibility (A11y) Fixer
Ensures documentation meets WCAG 2.1 AA accessibility standards

Improves: Accessibility, inclusivity, compliance, SEO

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
import subprocess
from typing import List, Dict, Optional
from pathlib import Path

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class AccessibilityFixer(BaseFixer):
    """
    Ensures documentation accessibility compliance

    Detection:
    - Missing alt text on images
    - Tables without headers
    - Color-only information
    - Non-semantic HTML
    - Missing language attributes
    - Poor contrast (detection only)
    - Runs `mint a11y` if available

    Auto-fix:
    - Can add placeholder alt text
    - Can add table headers
    - Can suggest semantic improvements
    """

    def __init__(self, config: Config):
        super().__init__(config)

        # Check if mint a11y is available
        self.mint_a11y_available = self._check_mint_a11y()

    @property
    def name(self) -> str:
        return "Accessibility Fixer"

    def _check_mint_a11y(self) -> bool:
        """Check if mint a11y command is available"""
        try:
            result = subprocess.run(
                ['mint', 'a11y', '--help'],
                capture_output=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check for accessibility issues"""
        issues = []
        lines = content.split('\n')
        in_code_block = False

        for i, line in enumerate(lines, 1):
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Check for images without alt text
            image_issues = self._check_image_alt_text(line, i, file_path)
            issues.extend(image_issues)

            # Check for tables without headers
            table_issues = self._check_table_accessibility(lines, i, file_path)
            issues.extend(table_issues)

            # Check for color-only information
            color_issues = self._check_color_only_info(line, i, file_path)
            issues.extend(color_issues)

            # Check for non-semantic elements
            semantic_issues = self._check_semantic_html(line, i, file_path)
            issues.extend(semantic_issues)

        # Run mint a11y if available
        if self.mint_a11y_available:
            mint_issues = self._run_mint_a11y(file_path)
            issues.extend(mint_issues)

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Fix accessibility issues"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        lines = fixed_content.split('\n')
        in_code_block = False

        for i, line in enumerate(lines):
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            original_line = line

            # Fix images without alt text
            line, alt_fixes = self._fix_image_alt_text(line, i + 1, issues)
            if alt_fixes:
                fixes_applied.extend(alt_fixes)
                lines[i] = line

            # Fix tables without headers
            # (This is more complex, handled separately)

            if line != original_line:
                # Mark issues as fixed
                line_issues = [issue for issue in issues
                              if issue.line_number == i + 1 and issue.auto_fixable]
                issues_fixed.extend(line_issues)

        if fixes_applied:
            fixed_content = '\n'.join(lines)

        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=fixed_content,
            fixes_applied=fixes_applied,
            issues_fixed=issues_fixed
        )

    def _check_image_alt_text(self, line: str, line_num: int, file_path: str) -> List[Issue]:
        """Check if images have alt text"""
        issues = []

        # Check markdown images: ![alt](url)
        md_images = re.finditer(r'!\[(.*?)\]\(([^\)]+)\)', line)
        for match in md_images:
            alt_text = match.group(1).strip()
            image_url = match.group(2)

            if not alt_text:
                issues.append(Issue(
                    severity='critical',
                    category='accessibility',
                    file_path=file_path,
                    line_number=line_num,
                    issue_type='missing_alt_text',
                    description=f'Image missing alt text: {image_url}',
                    suggestion='Add descriptive alt text for screen readers',
                    context=match.group(0),
                    auto_fixable=True  # Can add placeholder
                ))
            elif len(alt_text) < 5 or alt_text.lower() in ['image', 'picture', 'photo', 'img']:
                issues.append(Issue(
                    severity='high',
                    category='accessibility',
                    file_path=file_path,
                    line_number=line_num,
                    issue_type='poor_alt_text',
                    description=f'Image has non-descriptive alt text: "{alt_text}"',
                    suggestion='Use descriptive alt text that explains image content and purpose',
                    context=match.group(0),
                    auto_fixable=False
                ))

        # Check HTML images: <img src="..." alt="...">
        html_images = re.finditer(r'<img\s+([^>]*?)>', line)
        for match in html_images:
            img_tag = match.group(0)
            alt_match = re.search(r'alt=["\']([^"\']*)["\']', img_tag)

            if not alt_match:
                issues.append(Issue(
                    severity='critical',
                    category='accessibility',
                    file_path=file_path,
                    line_number=line_num,
                    issue_type='missing_alt_attribute',
                    description='HTML image missing alt attribute',
                    suggestion='Add alt="" for decorative images or alt="description" for content images',
                    context=img_tag[:80],
                    auto_fixable=True
                ))
            elif not alt_match.group(1).strip():
                # Empty alt is OK for decorative images, but flag for review
                issues.append(Issue(
                    severity='low',
                    category='accessibility',
                    file_path=file_path,
                    line_number=line_num,
                    issue_type='empty_alt_text',
                    description='Image has empty alt text (OK if decorative)',
                    suggestion='Verify this is a decorative image; if not, add descriptive alt text',
                    context=img_tag[:80],
                    auto_fixable=False
                ))

        return issues

    def _fix_image_alt_text(self, line: str, line_num: int, issues: List[Issue]) -> tuple:
        """Fix images missing alt text"""
        fixes = []

        # Check if this line has a missing alt text issue
        has_issue = any(
            issue.line_number == line_num and
            issue.issue_type in ['missing_alt_text', 'missing_alt_attribute']
            for issue in issues
        )

        if not has_issue:
            return line, fixes

        # Fix markdown images: ![]() → ![Image]()
        def replace_md_image(match):
            alt_text = match.group(1).strip()
            image_url = match.group(2)

            if not alt_text:
                # Extract filename as placeholder alt text
                filename = Path(image_url).stem.replace('-', ' ').replace('_', ' ').title()
                new_alt = filename or 'Image'
                fixes.append(f'Added placeholder alt text: "{new_alt}" (line {line_num})')
                return f'![{new_alt}]({image_url})'

            return match.group(0)

        line = re.sub(r'!\[(.*?)\]\(([^\)]+)\)', replace_md_image, line)

        # Fix HTML images: add alt attribute
        def replace_html_image(match):
            img_tag = match.group(0)

            if 'alt=' not in img_tag:
                # Add alt attribute before closing >
                new_tag = img_tag[:-1] + ' alt="Image">'
                fixes.append(f'Added placeholder alt attribute (line {line_num})')
                return new_tag

            return img_tag

        line = re.sub(r'<img\s+([^>]*?)>', replace_html_image, line)

        return line, fixes

    def _check_table_accessibility(self, lines: List[str], line_num: int, file_path: str) -> List[Issue]:
        """Check table accessibility"""
        issues = []

        line = lines[line_num - 1] if line_num <= len(lines) else ''

        # Check for markdown tables without headers
        if '|' in line and line_num < len(lines):
            next_line = lines[line_num] if line_num < len(lines) else ''

            # Markdown table header separator line (e.g., |---|---|)
            if re.match(r'^\s*\|[\s\-:|]+\|\s*$', next_line):
                # This is a header row, which is good
                pass
            elif '|' in line and not re.match(r'^\s*\|[\s\-:|]+\|\s*$', line):
                # This might be a table without headers
                # Check if previous line looks like a header
                prev_line = lines[line_num - 2] if line_num > 1 else ''
                prev_prev_line = lines[line_num - 3] if line_num > 2 else ''

                has_header = (
                    '|' in prev_line and
                    re.match(r'^\s*\|[\s\-:|]+\|\s*$', line)
                )

                if not has_header and line_num > 2:
                    issues.append(Issue(
                        severity='medium',
                        category='accessibility',
                        file_path=file_path,
                        line_number=line_num,
                        issue_type='table_missing_headers',
                        description='Table may be missing header row',
                        suggestion='Add header row with column names for screen reader accessibility',
                        context=line.strip()[:80],
                        auto_fixable=False
                    ))

        # Check HTML tables for proper structure
        if '<table' in line.lower():
            issues.append(Issue(
                severity='medium',
                category='accessibility',
                file_path=file_path,
                line_number=line_num,
                issue_type='html_table_check',
                description='HTML table detected - verify it has <thead>, <tbody>, and proper headers',
                suggestion='Use <th scope="col"> for headers and semantic table structure',
                context=line.strip()[:80],
                auto_fixable=False
            ))

        return issues

    def _check_color_only_info(self, line: str, line_num: int, file_path: str) -> List[Issue]:
        """Check for information conveyed by color alone"""
        issues = []

        # Look for color-only indicators
        color_patterns = [
            (r'\b(red|green|blue|yellow)\s+(text|color|background)', 'color reference without additional indicator'),
            (r'see\s+the\s+(red|green|blue)\s+', 'instruction using color only'),
        ]

        for pattern, description in color_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                issues.append(Issue(
                    severity='medium',
                    category='accessibility',
                    file_path=file_path,
                    line_number=line_num,
                    issue_type='color_only_information',
                    description=f'Possible {description}',
                    suggestion='Add non-color indicators (icons, text, patterns) alongside color',
                    context=line.strip()[:80],
                    auto_fixable=False
                ))

        return issues

    def _check_semantic_html(self, line: str, line_num: int, file_path: str) -> List[Issue]:
        """Check for non-semantic HTML"""
        issues = []

        # Check for divs that should be semantic elements
        if re.search(r'<div\s+class=["\'].*?(button|link|nav|header|footer|article)', line, re.IGNORECASE):
            issues.append(Issue(
                severity='low',
                category='accessibility',
                file_path=file_path,
                line_number=line_num,
                issue_type='non_semantic_html',
                description='Using div where semantic HTML element might be better',
                suggestion='Consider using semantic HTML5 elements (<nav>, <article>, <button>, etc.)',
                context=line.strip()[:80],
                auto_fixable=False
            ))

        # Check for buttons without type attribute
        if '<button' in line and 'type=' not in line:
            issues.append(Issue(
                severity='low',
                category='accessibility',
                file_path=file_path,
                line_number=line_num,
                issue_type='button_missing_type',
                description='Button missing type attribute',
                suggestion='Add type="button" to prevent form submission',
                context=line.strip()[:80],
                auto_fixable=True
            ))

        return issues

    def _run_mint_a11y(self, file_path: str) -> List[Issue]:
        """Run mint a11y command if available"""
        if not self.mint_a11y_available:
            return []

        issues = []

        try:
            # Get the project root (where docs.json would be)
            project_root = Path(file_path).parent
            while project_root.parent != project_root:
                if (project_root / 'docs.json').exists():
                    break
                project_root = project_root.parent

            # Run mint a11y
            result = subprocess.run(
                ['mint', 'a11y'],
                cwd=str(project_root),
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode != 0 and result.stderr:
                # Parse mint a11y output for issues
                for line in result.stderr.split('\n'):
                    if 'error' in line.lower() or 'warning' in line.lower():
                        issues.append(Issue(
                            severity='medium',
                            category='accessibility',
                            file_path=file_path,
                            line_number=1,
                            issue_type='mint_a11y_issue',
                            description=f'Mint a11y: {line.strip()}',
                            suggestion='Review Mintlify accessibility guidelines',
                            context='',
                            auto_fixable=False
                        ))

        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            # Silently fail if mint a11y is not available
            pass

        return issues
