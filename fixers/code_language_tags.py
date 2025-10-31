"""
Code Language Tag Fixer
Automatically adds missing language identifiers to code blocks

This is CRITICAL for Mintlify - code blocks without language tags break syntax highlighting.

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
from pathlib import Path
from typing import List, Dict

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class CodeLanguageTagFixer(BaseFixer):
    """
    Adds missing language tags to code blocks

    Detection: Finds ``` without language identifier
    Auto-fix: Infers language from:
    1. File path context (api/* → json, claude-code/* → bash)
    2. Content patterns (import/export → js, def/class → python)
    3. Shebang lines (#!/bin/bash → bash)
    """

    def __init__(self, config: Config):
        super().__init__(config)

        # Language inference rules based on file path
        self.path_language_map = {
            'api': 'json',
            'claude-code': 'bash',
            'agent-sdk': 'typescript',
        }

        # Content pattern matchers for language detection
        self.content_patterns = [
            (r'^\s*import\s+.*\s+from\s+["\']', 'javascript'),
            (r'^\s*export\s+(default|const|function|class)', 'javascript'),
            (r'^\s*def\s+\w+\s*\(', 'python'),
            (r'^\s*class\s+\w+:', 'python'),
            (r'^\s*function\s+\w+\s*\(', 'javascript'),
            (r'^\s*const\s+\w+\s*=', 'javascript'),
            (r'^\s*interface\s+\w+\s*\{', 'typescript'),
            (r'^\s*type\s+\w+\s*=', 'typescript'),
            (r'^\s*\$\s+[\w-]+', 'bash'),
            (r'^\s*#\s*!/bin/(bash|sh)', 'bash'),
            (r'^\s*curl\s+', 'bash'),
            (r'^\s*npm\s+(install|run)', 'bash'),
            (r'^\s*<\?php', 'php'),
            (r'^\s*package\s+\w+', 'go'),
            (r'^\s*use\s+\w+', 'rust'),
            (r'^\s*\{[\s\n]*"', 'json'),
            (r'^\s*<[a-zA-Z]+', 'jsx'),
        ]

    @property
    def name(self) -> str:
        return "Code Language Tag Fixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Find code blocks without language tags"""
        issues = []
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Check for code block start without language
            if line.strip().startswith('```'):
                lang = line.strip()[3:].strip()

                # Check if next line exists and has content (not closing block)
                if i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('```'):
                    if not lang:  # Missing language tag
                        # Look ahead to get code block content for inference
                        code_content = self._extract_code_block(lines, i)
                        inferred_lang = self._infer_language(file_path, code_content)

                        issues.append(Issue(
                            severity='critical',
                            category='style',
                            file_path=file_path,
                            line_number=i,
                            issue_type='missing_language_tag',
                            description='Code block missing language identifier (REQUIRED in Mintlify)',
                            suggestion=f'Add language tag: ```{inferred_lang}',
                            context=line.strip(),
                            auto_fixable=True
                        ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Add language tags to code blocks"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        lines = fixed_content.split('\n')

        for issue in issues:
            if not issue.auto_fixable or issue.issue_type != 'missing_language_tag':
                continue

            line_idx = issue.line_number - 1
            if line_idx >= len(lines):
                continue

            # Extract code block to infer language
            code_content = self._extract_code_block(lines, issue.line_number)
            inferred_lang = self._infer_language(file_path, code_content)

            # Replace ``` with ```language
            old_line = lines[line_idx]
            if old_line.strip() == '```':
                lines[line_idx] = f'```{inferred_lang}'
                fixes_applied.append(f'Added language tag: ```{inferred_lang} at line {issue.line_number}')
                issues_fixed.append(issue)

        if fixes_applied:
            fixed_content = '\n'.join(lines)

        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=fixed_content,
            fixes_applied=fixes_applied,
            issues_fixed=issues_fixed
        )

    def _extract_code_block(self, lines: List[str], start_line: int) -> str:
        """Extract code block content for language inference"""
        code_lines = []

        # Get up to 10 lines of code block content
        for i in range(start_line, min(start_line + 10, len(lines))):
            if lines[i].strip().startswith('```'):
                break
            code_lines.append(lines[i])

        return '\n'.join(code_lines)

    def _infer_language(self, file_path: str, code_content: str) -> str:
        """Infer language from file path and content"""
        # Check shebang first
        if code_content.strip().startswith('#!'):
            first_line = code_content.split('\n')[0]
            if 'python' in first_line:
                return 'python'
            elif 'bash' in first_line or 'sh' in first_line:
                return 'bash'
            elif 'node' in first_line:
                return 'javascript'

        # Check path-based rules
        path_parts = file_path.split('/')
        for part in path_parts:
            if part in self.path_language_map:
                return self.path_language_map[part]

        # Check content patterns
        for pattern, language in self.content_patterns:
            if re.search(pattern, code_content, re.MULTILINE):
                return language

        # Check for JSON-like structure
        if code_content.strip().startswith('{') or code_content.strip().startswith('['):
            try:
                import json
                json.loads(code_content)
                return 'json'
            except:
                pass

        # Default to bash for command-line examples
        if any(cmd in code_content.lower() for cmd in ['npm', 'git', 'curl', 'python', 'node', 'cd ', 'mkdir', 'export']):
            return 'bash'

        # Fall back to python (common in technical docs)
        return 'python'
