"""
Terminology Consistency Fixer
Enforces consistent usage of technical terms across documentation

Improves: Clarity, professionalism, user comprehension

Based on style-consistency-analysis.md terminology findings

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
from typing import List, Dict

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class TerminologyConsistencyFixer(BaseFixer):
    """
    Fixes inconsistent terminology usage

    Detection: Multiple terms used for the same concept
    Auto-fix: Replaces with canonical term from glossary
    """

    def __init__(self, config: Config):
        super().__init__(config)

        # Canonical terminology (preferred term: [variations to replace])
        # Format: {preferred_term: [(pattern_to_match, context_pattern)]}

        self.terminology_map = {
            # Documentation terminology
            'documentation': [
                (r'\bdocs\b(?! ?\.json)', 'general reference'),  # "docs" → "documentation" (except docs.json)
            ],

            # API interaction terms
            'request': [
                (r'\bAPI call\b', None),  # "API call" → "request"
                (r'\bquery\b(?= to the API)', None),  # "query to API" → "request"
            ],

            'response': [
                (r'\breturn value\b(?= from (the )?API)', None),  # "return value from API" → "response"
                (r'\bAPI response\b', None),  # "API response" → "response" (redundant)
            ],

            # Parameter terminology
            'parameter': [
                (r'\bparam\b(?!s?\b)', None),  # "param" → "parameter" (but keep "params")
                (r'\bargument\b(?= (to|for) )', None),  # "argument to" → "parameter"
            ],

            # API structure terms
            'endpoint': [
                (r'\bAPI endpoint\b', None),  # "API endpoint" → "endpoint" (redundant)
                (r'\broute\b(?= (for|to) )', None),  # "route for" → "endpoint"
            ],

            # Context terminology
            'context window': [
                (r'\bcontext\b(?= size| limit)', None),  # "context size" → "context window"
                (r'\bwindow\b(?= size)', None),  # "window size" → "context window"
            ],

            # Claude interaction terms
            'message': [
                (r'\bprompt\b(?= in the messages)', None),  # "prompt in messages" → "message"
            ],

            # Tool terminology
            'tool use': [
                (r'\bfunction calling\b', None),  # "function calling" → "tool use"
                (r'\btool calling\b', None),  # "tool calling" → "tool use"
            ],

            # Model terminology
            'model': [
                (r'\bLLM\b(?= (for|to|that))', None),  # "LLM for" → "model"
                (r'\bAI\b(?= (for|to|that) )', None),  # "AI for" → "model" (in specific contexts)
            ],
        }

        # Terms that should NOT be replaced in certain contexts
        self.exceptions = {
            'docs.json',  # File name
            'params:',  # Common parameter syntax
            '/docs/',  # URL path
            'docs/',  # URL path
        }

    @property
    def name(self) -> str:
        return "Terminology Consistency Fixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Find inconsistent terminology usage"""
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

            # Skip URLs and code
            if line.strip().startswith(('http://', 'https://', '`')):
                continue

            # Check terminology patterns
            for preferred_term, variations in self.terminology_map.items():
                for pattern, context_pattern in variations:
                    # Skip if in exception list
                    if any(exc in line for exc in self.exceptions):
                        continue

                    matches = list(re.finditer(pattern, line, re.IGNORECASE))

                    for match in matches:
                        incorrect_term = match.group(0)

                        # Skip if already correct
                        if incorrect_term.lower() == preferred_term.lower():
                            continue

                        # Skip if inside inline code
                        if self._is_in_code(line, match.start()):
                            continue

                        # Check context pattern if specified
                        if context_pattern:
                            context_start = max(0, match.start() - 50)
                            context_end = min(len(line), match.end() + 50)
                            context = line[context_start:context_end]
                            if context_pattern not in context:
                                continue

                        issues.append(Issue(
                            severity='low',
                            category='style',
                            file_path=file_path,
                            line_number=i,
                            issue_type='inconsistent_terminology',
                            description=f'Use "{preferred_term}" instead of "{incorrect_term}"',
                            suggestion=f'Replace "{incorrect_term}" with "{preferred_term}" for consistency',
                            context=self._get_context(line, match),
                            auto_fixable=True
                        ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Fix terminology inconsistencies"""
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

            # Skip URLs and code
            if line.strip().startswith(('http://', 'https://', '`')):
                continue

            # Skip if in exception list
            if any(exc in line for exc in self.exceptions):
                continue

            original_line = line

            # Apply terminology fixes
            for preferred_term, variations in self.terminology_map.items():
                for pattern, context_pattern in variations:
                    def replace_func(match):
                        if self._is_in_code(original_line, match.start()):
                            return match.group(0)

                        # Check context if specified
                        if context_pattern:
                            context_start = max(0, match.start() - 50)
                            context_end = min(len(original_line), match.end() + 50)
                            context = original_line[context_start:context_end]
                            if context_pattern not in context:
                                return match.group(0)

                        return preferred_term

                    line = re.sub(pattern, replace_func, line, flags=re.IGNORECASE)

            if line != original_line:
                lines[i] = line
                fixes_applied.append(f'Fixed terminology at line {i + 1}')

                # Mark corresponding issues as fixed
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

    def _is_in_code(self, line: str, position: int) -> bool:
        """Check if position is inside inline code backticks"""
        before_pos = line[:position]
        backtick_count = before_pos.count('`')
        return backtick_count % 2 == 1

    def _get_context(self, line: str, match: re.Match, context_len: int = 60) -> str:
        """Extract context around the match"""
        start = max(0, match.start() - context_len // 2)
        end = min(len(line), match.end() + context_len // 2)
        context = line[start:end].strip()
        if len(context) > 100:
            context = context[:100] + '...'
        return context
