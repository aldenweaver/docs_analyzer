"""
Terminology fixer - fixes terminology and capitalization issues
"""

import re
from typing import List, Dict
from datetime import datetime

from core.models import Issue, FixResult
from core.config import Config
from fixers.base import BaseFixer
from utils.text_utils import word_boundary_replace


class TerminologyFixer(BaseFixer):
    """Fixes terminology and capitalization issues"""

    def __init__(self, config: Config):
        super().__init__(config)
        self.preferred_terms = config.preferred_terms
        self.avoid_terms = config.avoid_terms

        # Proper nouns that should be capitalized correctly
        # From the style guide
        self.proper_nouns = {
            "Claude": "Claude",
            "Claude Code": "Claude Code",
            "Claude API": "Claude API",
            "Anthropic Console": "Anthropic Console",
            "Model Context Protocol": "Model Context Protocol",
            "Extended Thinking": "Extended Thinking",
            "Prompt Caching": "Prompt Caching",
            "Agent Skills": "Agent Skills",
            "MCP": "MCP",
            "API": "API",
            "SDK": "SDK",
            "REST": "REST",
            "JSON": "JSON",
            "OAuth": "OAuth",
        }

    @property
    def name(self) -> str:
        return "TerminologyFixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check file for terminology issues"""
        issues = []
        lines = content.split('\n')

        # Skip checking frontmatter
        in_frontmatter = False

        for line_num, line in enumerate(lines, 1):
            # Track frontmatter
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue

            if in_frontmatter:
                continue

            # Skip code blocks
            if line.strip().startswith('```'):
                continue

            # Skip lines that are primarily URLs (to avoid capitalizing URLs)
            if self._is_url_line(line):
                continue

            # Check for deprecated terms (preferred_terms)
            for old_term, new_term in self.preferred_terms.items():
                # Use word boundary matching to avoid partial matches
                pattern = r'\b' + re.escape(old_term) + r'\b'

                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(Issue(
                        severity="medium",
                        category="consistency",
                        file_path=file_path,
                        line_number=line_num,
                        issue_type="deprecated_terminology",
                        description=f"Deprecated term '{old_term}' found",
                        suggestion=f"Replace '{old_term}' with '{new_term}'",
                        context=line.strip(),
                        auto_fixable=True
                    ))

            # Check for terms to avoid (weak language)
            for avoid_term in self.avoid_terms:
                pattern = r'\b' + re.escape(avoid_term) + r'\b'

                if re.search(pattern, line, re.IGNORECASE):
                    issues.append(Issue(
                        severity="low",
                        category="style",
                        file_path=file_path,
                        line_number=line_num,
                        issue_type="weak_language",
                        description=f"Weak language term '{avoid_term}' found",
                        suggestion=f"Remove or rephrase without '{avoid_term}'",
                        context=line.strip(),
                        auto_fixable=False  # Requires human judgment
                    ))

            # Check proper noun capitalization
            for proper_noun_key, proper_noun_value in self.proper_nouns.items():
                # Look for incorrect capitalization
                # Match word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(proper_noun_value) + r'\b'

                # Find all case-insensitive matches
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    matched_text = match.group()

                    # If capitalization is incorrect
                    if matched_text != proper_noun_value:
                        issues.append(Issue(
                            severity="low",
                            category="consistency",
                            file_path=file_path,
                            line_number=line_num,
                            issue_type="improper_capitalization",
                            description=f"Improper capitalization: '{matched_text}' should be '{proper_noun_value}'",
                            suggestion=f"Replace '{matched_text}' with '{proper_noun_value}'",
                            context=line.strip(),
                            auto_fixable=True
                        ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Apply terminology fixes"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        # Group issues by type for efficient processing
        deprecated_issues = [i for i in issues if i.issue_type == "deprecated_terminology"]
        capitalization_issues = [i for i in issues if i.issue_type == "improper_capitalization"]

        # Fix deprecated terminology
        for issue in deprecated_issues:
            # Extract old and new terms from suggestion
            match = re.search(r"Replace '(.+)' with '(.+)'", issue.suggestion)
            if match:
                old_term, new_term = match.groups()

                # Use word boundary replacement to avoid partial matches
                pattern = r'\b' + re.escape(old_term) + r'\b'
                before_fix = fixed_content
                fixed_content = re.sub(pattern, new_term, fixed_content, flags=re.IGNORECASE)

                if before_fix != fixed_content:
                    fix_msg = f"Replaced '{old_term}' with '{new_term}'"
                    if fix_msg not in fixes_applied:
                        fixes_applied.append(fix_msg)
                        issues_fixed.append(issue)

        # Fix capitalization
        for issue in capitalization_issues:
            # Extract old and new from suggestion
            match = re.search(r"Replace '(.+)' with '(.+)'", issue.suggestion)
            if match:
                old_text, new_text = match.groups()

                # Use exact word boundary replacement
                pattern = r'\b' + re.escape(old_text) + r'\b'
                before_fix = fixed_content
                fixed_content = re.sub(pattern, new_text, fixed_content)

                if before_fix != fixed_content:
                    fix_msg = f"Fixed capitalization: '{old_text}' → '{new_text}'"
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

    def _is_url_line(self, line: str) -> bool:
        """
        Check if a line contains URLs that we should skip
        Returns True if line contains markdown links or bare URLs
        """
        # Check for markdown links: [text](url)
        if '](http' in line or '](./' in line or '](..' in line or '](/en/' in line:
            return True

        # Check for bare URLs
        if line.strip().startswith('http://') or line.strip().startswith('https://'):
            return True

        # Check for href attributes
        if 'href=' in line:
            return True

        return False
