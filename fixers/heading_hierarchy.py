"""
Heading Hierarchy Fixer
Fixes skipped heading levels (e.g., H1 → H3 becomes H1 → H2)

Improves: Navigation, accessibility, SEO, document structure

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
from typing import List

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class HeadingHierarchyFixer(BaseFixer):
    """
    Fixes heading hierarchy skips

    Detection: H1 → H3, H2 → H4 (skips a level)
    Auto-fix: Adjusts heading levels to be sequential
    """

    @property
    def name(self) -> str:
        return "Heading Hierarchy Fixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Find heading hierarchy violations"""
        issues = []
        lines = content.split('\n')

        # Extract headings with their levels and line numbers
        headings = []
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                match = re.match(r'^(#+)\s+(.+)$', line.strip())
                if match:
                    level = len(match.group(1))
                    text = match.group(2)
                    headings.append((level, text, i, line))

        # Check for skips in hierarchy
        for i in range(len(headings) - 1):
            current_level, current_text, current_line, _ = headings[i]
            next_level, next_text, next_line, _ = headings[i + 1]

            if next_level > current_level + 1:
                # Heading skip detected
                issues.append(Issue(
                    severity='medium',
                    category='ia',
                    file_path=file_path,
                    line_number=next_line,
                    issue_type='heading_skip',
                    description=f'Heading skips from H{current_level} to H{next_level}',
                    suggestion=f'Use H{current_level + 1} instead to maintain hierarchy',
                    context=next_text,
                    auto_fixable=True
                ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Fix heading hierarchy by adjusting levels"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        lines = fixed_content.split('\n')

        # Build heading map
        headings = []
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                match = re.match(r'^(#+)\s+(.+)$', line.strip())
                if match:
                    level = len(match.group(1))
                    headings.append((i, level))

        # Adjust heading levels to fix hierarchy
        max_level = 1
        for line_idx, current_level in headings:
            # Determine correct level based on previous max
            if current_level > max_level + 1:
                # Need to adjust down
                correct_level = max_level + 1

                # Replace heading level
                old_line = lines[line_idx]
                match = re.match(r'^(#+)(\s+.+)$', old_line.strip())
                if match:
                    new_line = '#' * correct_level + match.group(2)
                    lines[line_idx] = new_line

                    fixes_applied.append(
                        f'Fixed heading hierarchy at line {line_idx + 1}: '
                        f'H{current_level} → H{correct_level}'
                    )

                    # Find and mark corresponding issue as fixed
                    for issue in issues:
                        if issue.line_number == line_idx + 1:
                            issues_fixed.append(issue)

                    max_level = correct_level
            else:
                max_level = current_level

        if fixes_applied:
            fixed_content = '\n'.join(lines)

        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=fixed_content,
            fixes_applied=fixes_applied,
            issues_fixed=issues_fixed
        )
