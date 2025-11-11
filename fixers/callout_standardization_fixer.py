"""
Callout Standardization Fixer
Standardizes callout/alert box formatting using Mintlify components

Improves: Consistency, visual hierarchy, content scanability

Based on style-consistency-analysis.md findings

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
from typing import List, Tuple, Optional

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class CalloutStandardizationFixer(BaseFixer):
    """
    Standardizes callout/alert boxes to Mintlify components

    Detection: Inconsistent callout patterns (**Note:**, > Note:, markdown bold)
    Auto-fix: Converts to standard Mintlify components (<Note>, <Warning>, <Tip>)
    """

    def __init__(self, config: Config):
        super().__init__(config)

        # Callout type mappings (pattern → component name)
        self.callout_patterns = {
            # Note patterns
            'Note': [
                r'^\*\*Note:\*\*\s+',
                r'^\*\*NOTE:\*\*\s+',
                r'^> Note:\s+',
                r'^> \*\*Note:\*\*\s+',
                r'^ℹ️\s+',
                r'^Note:\s+',
            ],

            # Warning patterns
            'Warning': [
                r'^\*\*Warning:\*\*\s+',
                r'^\*\*WARNING:\*\*\s+',
                r'^⚠️\s+',
                r'^> Warning:\s+',
                r'^\*\*Caution:\*\*\s+',
                r'^\*\*Important:\*\*\s+',
                r'^> \*\*Warning:\*\*\s+',
            ],

            # Tip patterns
            'Tip': [
                r'^\*\*Tip:\*\*\s+',
                r'^\*\*TIP:\*\*\s+',
                r'^💡\s+',
                r'^> Tip:\s+',
                r'^\*\*Best practice:\*\*\s+',
                r'^\*\*Pro tip:\*\*\s+',
                r'^> \*\*Tip:\*\*\s+',
            ],

            # Info patterns
            'Info': [
                r'^\*\*Info:\*\*\s+',
                r'^\*\*INFO:\*\*\s+',
                r'^> Info:\s+',
                r'^\*\*Important limitation:\*\*\s+',
                r'^\*\*Beta:\*\*\s+',
            ],
        }

        # Already-standard Mintlify components (don't fix these)
        self.mintlify_components = [
            '<Note>',
            '<Warning>',
            '<Tip>',
            '<Info>',
            '</Note>',
            '</Warning>',
            '</Tip>',
            '</Info>',
        ]

    @property
    def name(self) -> str:
        return "Callout Standardization Fixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Find non-standard callout formatting"""
        issues = []
        lines = content.split('\n')
        in_code_block = False

        i = 0
        while i < len(lines):
            line = lines[i]

            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                i += 1
                continue

            if in_code_block:
                i += 1
                continue

            # Check if already using Mintlify component (skip)
            if any(comp in line for comp in self.mintlify_components):
                i += 1
                continue

            # Check for non-standard callout patterns
            for callout_type, patterns in self.callout_patterns.items():
                for pattern in patterns:
                    match = re.match(pattern, line.strip())
                    if match:
                        # Found non-standard callout
                        callout_content, end_line = self._extract_callout_content(lines, i)

                        issues.append(Issue(
                            severity='low',
                            category='style',
                            file_path=file_path,
                            line_number=i + 1,
                            issue_type='non_standard_callout',
                            description=f'Non-standard {callout_type.lower()} callout format',
                            suggestion=f'Convert to <{callout_type}> component',
                            context=line.strip()[:100],
                            auto_fixable=True
                        ))
                        break

            i += 1

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Convert non-standard callouts to Mintlify components"""
        fixes_applied = []
        issues_fixed = []

        lines = content.split('\n')
        in_code_block = False

        i = 0
        while i < len(lines):
            line = lines[i]

            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                i += 1
                continue

            if in_code_block:
                i += 1
                continue

            # Skip if already Mintlify component
            if any(comp in line for comp in self.mintlify_components):
                i += 1
                continue

            # Check for non-standard callouts
            converted = False
            for callout_type, patterns in self.callout_patterns.items():
                for pattern in patterns:
                    match = re.match(pattern, line.strip())
                    if match:
                        # Extract full callout content
                        callout_content, end_line = self._extract_callout_content(lines, i)

                        # Remove the pattern prefix from content
                        clean_content = re.sub(pattern, '', callout_content, flags=re.MULTILINE)
                        clean_content = clean_content.strip()

                        # Create Mintlify component
                        component_lines = [
                            f'<{callout_type}>',
                            clean_content,
                            f'</{callout_type}>'
                        ]

                        # Replace lines
                        lines[i:end_line + 1] = component_lines

                        fixes_applied.append(
                            f'Converted {callout_type.lower()} callout to Mintlify component at line {i + 1}'
                        )

                        # Mark corresponding issue as fixed
                        line_issues = [issue for issue in issues
                                      if issue.line_number == i + 1 and issue.auto_fixable]
                        issues_fixed.extend(line_issues)

                        converted = True
                        i += len(component_lines)  # Skip past the new component
                        break

                if converted:
                    break

            if not converted:
                i += 1

        if fixes_applied:
            fixed_content = '\n'.join(lines)
        else:
            fixed_content = content

        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=fixed_content,
            fixes_applied=fixes_applied,
            issues_fixed=issues_fixed
        )

    def _extract_callout_content(self, lines: List[str], start_line: int) -> Tuple[str, int]:
        """
        Extract multi-line callout content.
        Returns (content, end_line_index)
        """
        content_lines = [lines[start_line]]
        current_line = start_line + 1

        # Continue until we hit blank line or different content type
        while current_line < len(lines):
            line = lines[current_line].strip()

            # Stop at blank line
            if not line:
                break

            # Stop at new heading
            if line.startswith('#'):
                break

            # Stop at code block
            if line.startswith('```'):
                break

            # Stop at new callout
            is_new_callout = False
            for callout_type, patterns in self.callout_patterns.items():
                for pattern in patterns:
                    if re.match(pattern, line):
                        is_new_callout = True
                        break
                if is_new_callout:
                    break

            if is_new_callout:
                break

            # Add to content
            content_lines.append(lines[current_line])
            current_line += 1

        # Join content
        content = '\n'.join(content_lines)
        end_line = current_line - 1

        return content, end_line
