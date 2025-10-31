"""
Production Code Validator
Identifies code examples that lack production-ready patterns

Improves: Code quality, reliability, developer experience

Based on 00_comprehensive_analysis.md findings (zero production examples found)

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
from typing import List

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class ProductionCodeValidator(BaseFixer):
    """
    Validates code examples for production-ready patterns

    Detection:
    - Missing error handling (try/except, error checking)
    - Missing retry logic for API calls
    - Missing rate limit handling
    - Hardcoded credentials or API keys
    - Missing timeout configuration
    - Missing logging

    Auto-fix: Not auto-fixable (requires understanding context and requirements)
    """

    def __init__(self, config: Config):
        super().__init__(config)

        # Production patterns to check for (by language)
        self.production_patterns = {
            'python': {
                'error_handling': [
                    r'try:',
                    r'except\s+\w+Error',
                    r'raise\s+',
                ],
                'retry_logic': [
                    r'for\s+\w+\s+in\s+range\(.*(retries?|attempts?)',
                    r'@retry',
                    r'while.*retries?',
                ],
                'rate_limit_handling': [
                    r'RateLimitError',
                    r'sleep\(',
                    r'time\.sleep',
                ],
                'credentials': [
                    r'ANTHROPIC_API_KEY',
                    r'os\.getenv',
                    r'os\.environ',
                ],
                'timeout': [
                    r'timeout\s*=',
                ],
                'logging': [
                    r'logging\.',
                    r'logger\.',
                    r'print\(',  # Basic logging acceptable
                ],
            },
            'typescript': {
                'error_handling': [
                    r'try\s*\{',
                    r'catch\s*\(',
                    r'throw\s+',
                ],
                'retry_logic': [
                    r'for.*retries?',
                    r'while.*retries?',
                ],
                'credentials': [
                    r'process\.env\.ANTHROPIC_API_KEY',
                    r'process\.env\.',
                ],
                'timeout': [
                    r'timeout:',
                ],
            },
            'javascript': {
                'error_handling': [
                    r'try\s*\{',
                    r'catch\s*\(',
                    r'throw\s+',
                ],
                'retry_logic': [
                    r'for.*retries?',
                    r'while.*retries?',
                ],
                'credentials': [
                    r'process\.env\.ANTHROPIC_API_KEY',
                    r'process\.env\.',
                ],
            },
        }

        # Anti-patterns (things that should NOT appear)
        self.anti_patterns = {
            'hardcoded_credentials': [
                r'api[_-]?key\s*=\s*["\'][a-zA-Z0-9_-]{20,}["\']',
                r'ANTHROPIC_API_KEY\s*=\s*["\']sk-',
            ],
            'missing_environment_check': [
                r'api[_-]?key\s*=\s*["\']your[_-]api[_-]key[_-]here["\']',
            ],
        }

    @property
    def name(self) -> str:
        return "Production Code Validator"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Validate code examples for production readiness"""
        issues = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i]

            # Check for code block start
            if line.strip().startswith('```'):
                language = line.strip()[3:].strip().lower()

                # Extract code block
                code_block, end_line = self._extract_code_block(lines, i + 1)

                if code_block and language in ['python', 'javascript', 'typescript', 'js', 'ts']:
                    # Normalize language
                    lang = 'python' if language == 'python' else 'typescript' if language in ['typescript', 'ts'] else 'javascript'

                    # Check if this is an API call example
                    is_api_call = self._contains_api_call(code_block)

                    if is_api_call:
                        # Validate production patterns
                        validation_issues = self._validate_code_block(
                            file_path,
                            code_block,
                            lang,
                            i + 1
                        )
                        issues.extend(validation_issues)

                    # Check for anti-patterns
                    anti_pattern_issues = self._check_anti_patterns(
                        file_path,
                        code_block,
                        i + 1
                    )
                    issues.extend(anti_pattern_issues)

                i = end_line
            else:
                i += 1

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Production code examples require manual enhancement - report only"""
        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=content,
            fixes_applied=[],
            issues_fixed=[]
        )

    def _extract_code_block(self, lines: List[str], start_line: int) -> tuple:
        """Extract code block content"""
        code_lines = []
        current_line = start_line

        while current_line < len(lines):
            if lines[current_line].strip().startswith('```'):
                break
            code_lines.append(lines[current_line])
            current_line += 1

        code = '\n'.join(code_lines)
        return code, current_line + 1

    def _contains_api_call(self, code: str) -> bool:
        """Check if code block contains API calls"""
        api_indicators = [
            r'messages\.create',
            r'client\.messages',
            r'Anthropic\(',
            r'anthropic\.',
            r'fetch\(',
            r'axios\.',
            r'requests\.',
        ]

        return any(re.search(pattern, code) for pattern in api_indicators)

    def _validate_code_block(self, file_path: str, code: str, language: str, line_number: int) -> List[Issue]:
        """Validate code block for production patterns"""
        issues = []

        if language not in self.production_patterns:
            return issues

        patterns = self.production_patterns[language]

        # Check for error handling
        has_error_handling = any(
            re.search(pattern, code)
            for pattern in patterns.get('error_handling', [])
        )

        if not has_error_handling:
            issues.append(Issue(
                severity='medium',
                category='style',
                file_path=file_path,
                line_number=line_number,
                issue_type='missing_error_handling',
                description='Code example lacks error handling',
                suggestion='Add try/catch or error handling for production readiness',
                context='API call without error handling',
                auto_fixable=False
            ))

        # Check for retry logic (lower priority)
        has_retry_logic = any(
            re.search(pattern, code)
            for pattern in patterns.get('retry_logic', [])
        )

        if not has_retry_logic:
            issues.append(Issue(
                severity='low',
                category='style',
                file_path=file_path,
                line_number=line_number,
                issue_type='missing_retry_logic',
                description='Code example lacks retry logic for rate limiting',
                suggestion='Consider adding exponential backoff retry logic',
                context='API call without retry handling',
                auto_fixable=False
            ))

        # Check for proper credential handling
        has_credential_handling = any(
            re.search(pattern, code)
            for pattern in patterns.get('credentials', [])
        )

        if not has_credential_handling and 'api' in code.lower():
            issues.append(Issue(
                severity='medium',
                category='style',
                file_path=file_path,
                line_number=line_number,
                issue_type='missing_credential_handling',
                description='Code example does not show proper credential handling',
                suggestion='Show how to load API key from environment variables',
                context='API initialization without environment variable example',
                auto_fixable=False
            ))

        return issues

    def _check_anti_patterns(self, file_path: str, code: str, line_number: int) -> List[Issue]:
        """Check for anti-patterns that should not appear"""
        issues = []

        # Check for hardcoded credentials
        for pattern in self.anti_patterns['hardcoded_credentials']:
            if re.search(pattern, code):
                issues.append(Issue(
                    severity='critical',
                    category='style',
                    file_path=file_path,
                    line_number=line_number,
                    issue_type='hardcoded_credentials',
                    description='Code example contains hardcoded API key',
                    suggestion='Never show actual API keys in code examples. Use environment variables.',
                    context='Hardcoded credential detected',
                    auto_fixable=False
                ))

        # Check for placeholder API keys
        for pattern in self.anti_patterns['missing_environment_check']:
            if re.search(pattern, code):
                issues.append(Issue(
                    severity='low',
                    category='style',
                    file_path=file_path,
                    line_number=line_number,
                    issue_type='placeholder_credentials',
                    description='Code example uses placeholder API key',
                    suggestion='Show how to load from environment instead of placeholders',
                    context='Placeholder credential',
                    auto_fixable=False
                ))

        return issues
