"""
Capitalization Fixer
Enforces consistent capitalization for product names, feature names, and technical terms

Improves: Consistency, brand perception, professionalism

Based on style-consistency-analysis.md findings (47+ inconsistencies)

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
from typing import List, Dict, Tuple

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class CapitalizationFixer(BaseFixer):
    """
    Fixes inconsistent capitalization across documentation

    Detection: Incorrect capitalization of products, features, models, technical terms
    Auto-fix: Replaces with canonical capitalization
    """

    def __init__(self, config: Config):
        super().__init__(config)

        # Canonical product names (always capitalize these)
        self.product_names = {
            r'\bclaude\b(?! code| api| console)': 'Claude',  # Claude alone
            r'\bclaude code\b': 'Claude Code',
            r'\bclaude api\b': 'Claude API',
            r'\banthropiconsole\b': 'Anthropic Console',
            r'\bapi\b(?= key| endpoint| reference)': 'API',  # API in specific contexts
        }

        # Feature names (Title Case for branded features)
        self.feature_names = {
            r'\bextended thinking\b': 'Extended Thinking',
            r'\bprompt caching\b': 'Prompt Caching',
            r'\bagent skills\b': 'Agent Skills',
            r'\bmodel context protocol\b': 'Model Context Protocol',
            r'\bcomputer use\b(?! tool)': 'Computer Use',  # "Computer Use" feature but "computer use tool"
        }

        # Model names (with spaces, proper capitalization)
        self.model_names = {
            r'\bclaude[- ]sonnet[- ]4[\.-]5\b': 'Claude Sonnet 4.5',
            r'\bclaude[- ]opus[- ]4[\.-]1\b': 'Claude Opus 4.1',
            r'\bclaude[- ]haiku[- ]4[\.-]5\b': 'Claude Haiku 4.5',
            r'\bsonnet 4\.5\b(?!-)': 'Claude Sonnet 4.5',  # Add "Claude" if missing
            r'\bopus 4\.1\b(?!-)': 'Claude Opus 4.1',
            r'\bhaiku 4\.5\b(?!-)': 'Claude Haiku 4.5',
        }

        # Technical terms (standard capitalization)
        self.technical_terms = {
            r'\bapi\b(?= [a-z])': 'API',  # API before lowercase word
            r'\bsdk\b': 'SDK',
            r'\bmcp\b(?= [a-z])': 'MCP',  # MCP before lowercase (acronym usage)
            r'\brest\b(?= api| endpoint)': 'REST',
            r'\bjson\b': 'JSON',
            r'\bhttp\b': 'HTTP',
            r'\bhttps\b': 'HTTPS',
            r'\boauth\b': 'OAuth',
            r'\bxml\b': 'XML',
            r'\bttl\b': 'TTL',
        }

        # General concepts (lowercase)
        self.general_concepts = {
            r'\bStreaming\b(?! API)': 'streaming',  # "streaming" as concept, "Streaming API" as proper noun
            r'\bBatch Processing\b': 'batch processing',
            r'\bTool Use\b(?! API)': 'tool use',  # General concept
            r'\bVision\b(?! API)': 'vision',  # General capability
        }

    @property
    def name(self) -> str:
        return "Capitalization Fixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Find capitalization inconsistencies"""
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

            # Don't check URLs or code identifiers
            if line.strip().startswith(('http://', 'https://', '`')):
                continue

            # Check all capitalization patterns
            all_patterns = {
                **self.product_names,
                **self.feature_names,
                **self.model_names,
                **self.technical_terms,
                **self.general_concepts
            }

            for pattern, correct_form in all_patterns.items():
                matches = list(re.finditer(pattern, line, re.IGNORECASE))

                for match in matches:
                    incorrect_form = match.group(0)

                    # Skip if already correct (case-sensitive check)
                    if incorrect_form == correct_form:
                        continue

                    # Skip if inside inline code
                    if self._is_in_code(line, match.start()):
                        continue

                    issues.append(Issue(
                        severity='low',
                        category='style',
                        file_path=file_path,
                        line_number=i,
                        issue_type='incorrect_capitalization',
                        description=f'Inconsistent capitalization: "{incorrect_form}" should be "{correct_form}"',
                        suggestion=f'Use "{correct_form}"',
                        context=self._get_context(line, match),
                        auto_fixable=True
                    ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Fix capitalization inconsistencies"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        lines = fixed_content.split('\n')
        in_code_block = False

        # Combine all patterns
        all_patterns = {
            **self.product_names,
            **self.feature_names,
            **self.model_names,
            **self.technical_terms,
            **self.general_concepts
        }

        for i, line in enumerate(lines):
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Don't fix URLs or code identifiers
            if line.strip().startswith(('http://', 'https://', '`')):
                continue

            original_line = line
            changes_in_line = []

            # Apply all capitalization fixes
            for pattern, correct_form in all_patterns.items():
                def replace_func(match):
                    incorrect = match.group(0)
                    if incorrect == correct_form:
                        return incorrect
                    if self._is_in_code(original_line, match.start()):
                        return incorrect
                    changes_in_line.append((incorrect, correct_form))
                    return correct_form

                line = re.sub(pattern, replace_func, line, flags=re.IGNORECASE)

            if line != original_line:
                lines[i] = line
                for incorrect, correct in changes_in_line:
                    fixes_applied.append(f'Fixed capitalization at line {i + 1}: "{incorrect}" → "{correct}"')

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
        # Odd number of backticks means we're inside code
        return backtick_count % 2 == 1

    def _get_context(self, line: str, match: re.Match, context_len: int = 40) -> str:
        """Extract context around the match"""
        start = max(0, match.start() - context_len // 2)
        end = min(len(line), match.end() + context_len // 2)
        context = line[start:end].strip()
        if len(context) > 80:
            context = context[:80] + '...'
        return context
