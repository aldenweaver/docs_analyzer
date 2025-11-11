"""
GitHub-Informed Documentation Fixer

Based on analysis of 50 real GitHub issues from the Claude Code repository,
this fixer detects patterns that users report as problematic:

1. Missing Documentation (72% of issues)
   - Very short pages (< 100 words)
   - Code features without examples
   - Procedural content without prerequisites

2. Clarity Issues (4% of issues)
   - Jargon without definitions
   - Code mentions without examples
   - Long paragraphs without structure

Research date: 2025-10-30
Source: https://github.com/anthropics/claude-code/issues?q=state:open+label:documentation
"""

from typing import List, Dict, Any
import re

from core.models import Issue, FixResult
from core.config import Config
from fixers.base import BaseFixer
from utils.text_utils import extract_frontmatter


class GitHubInformedFixer(BaseFixer):
    """Detects documentation issues based on real user-reported GitHub issues."""

    def __init__(self, config: Config):
        """Initialize the GitHub-informed fixer."""
        super().__init__(config)

        # Technical terms that often need definitions
        # Based on themes from GitHub issues analysis
        self.technical_terms = {
            "ultrathink", "thinking mode", "subagent", "mcp", "oauth",
            "bedrock", "api key", "marketplace", "yaml frontmatter",
            "claude code", "slash command", "skill", "agent", "tool",
            "context window", "token", "prompt", "completion"
        }

        # Procedural indicators that should have prerequisites
        self.procedural_indicators = [
            "how to", "step", "install", "setup", "configure",
            "create", "run", "execute", "deploy", "build"
        ]

    @property
    def name(self) -> str:
        return "GitHubInformedFixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """
        Check file for GitHub user-reported issues.

        Args:
            file_path: Path to the file being analyzed
            content: The markdown content

        Returns:
            List of detected issues
        """
        issues = []

        # Extract frontmatter
        frontmatter, body, _ = extract_frontmatter(content)
        if frontmatter is None:
            frontmatter = {}

        # Fix #1: Missing Documentation Detection
        issues.extend(self._check_missing_documentation(content, frontmatter, file_path))

        # Fix #2: Clarity Improvements
        issues.extend(self._check_clarity_issues(content, file_path))

        return issues

    def _check_missing_documentation(
        self, content: str, frontmatter: Dict[str, Any], filepath: str
    ) -> List[Issue]:
        """
        Detect missing documentation patterns (72% of GitHub issues).

        Checks for:
        - Very short content (< 100 words)
        - Missing code examples when discussing code features
        - Missing prerequisites for procedural content
        """
        issues = []

        # Check 1: Very short pages
        word_count = len(content.split())
        if word_count < 100:
            issues.append(
                Issue(
                    severity="medium",
                    category="gaps",
                    file_path=filepath,
                    line_number=1,
                    issue_type="missing_documentation",
                    description=f"Page is very short ({word_count} words). Users report difficulty finding complete information in brief pages.",
                    suggestion="Consider expanding with: examples, use cases, prerequisites, or related concepts.",
                    auto_fixable=False
                )
            )

        # Check 2: Missing code examples
        # Look for code-related terms without code blocks
        code_terms = ["function", "method", "class", "command", "cli", "api", "code", "script", "execute", "run"]
        has_code_terms = any(term in content.lower() for term in code_terms)
        has_code_block = "```" in content

        if has_code_terms and not has_code_block:
            issues.append(
                Issue(
                    severity="high",
                    category="gaps",
                    file_path=filepath,
                    line_number=1,
                    issue_type="missing_code_example",
                    description="Page discusses code/CLI features but contains no code examples. This is a common user complaint.",
                    suggestion="Add code examples showing practical usage.",
                    auto_fixable=False
                )
            )

        # Check 3: Missing prerequisites for procedural content
        is_procedural = any(indicator in content.lower() for indicator in self.procedural_indicators)
        has_prerequisites = bool(re.search(r'prerequisite|before you begin|requirements?|you.*need', content, re.IGNORECASE))

        if is_procedural and not has_prerequisites:
            issues.append(
                Issue(
                    severity="medium",
                    category="gaps",
                    file_path=filepath,
                    line_number=1,
                    issue_type="missing_prerequisites",
                    description="Procedural content without prerequisites section. Users report getting stuck when assumptions aren't stated.",
                    suggestion="Add a 'Prerequisites' or 'Before you begin' section listing required setup, knowledge, or permissions.",
                    auto_fixable=False
                )
            )

        return issues

    def _check_clarity_issues(self, content: str, filepath: str) -> List[Issue]:
        """
        Detect clarity issues (4% of GitHub issues, but high impact).

        Checks for:
        - Technical jargon without definitions
        - Code mentions without examples
        - Long paragraphs without structure
        """
        issues = []

        # Check 1: Technical terms without definitions
        # Look for first mention of technical terms
        content_lower = content.lower()
        for term in self.technical_terms:
            if term in content_lower:
                # Check if term appears near definition indicators
                pattern = rf'\b{re.escape(term)}\b.{{0,200}}(?:is|are|means|refers to|called)'
                has_definition = bool(re.search(pattern, content, re.IGNORECASE))

                if not has_definition:
                    # Find approximate line number
                    lines = content.split('\n')
                    line_num = 1
                    for i, line in enumerate(lines, 1):
                        if term in line.lower():
                            line_num = i
                            break

                    issues.append(
                        Issue(
                            severity="low",
                            category="clarity",
                            file_path=filepath,
                            line_number=line_num,
                            issue_type="undefined_jargon",
                            description=f"Technical term '{term}' used without definition. Users report confusion with undefined jargon.",
                            suggestion=f"Add brief definition or link to glossary when first introducing '{term}'.",
                            auto_fixable=False
                        )
                    )

        # Check 2: Inline code without examples
        # Find inline code mentions like `functionName` without nearby code blocks
        inline_code_pattern = r'`([^`]+)`'
        inline_codes = re.finditer(inline_code_pattern, content)

        lines = content.split('\n')
        for match in inline_codes:
            code_text = match.group(1)

            # Skip if it's just a value or very short
            if len(code_text) < 3:
                continue

            # Find which line this is on
            char_pos = match.start()
            current_pos = 0
            line_num = 1
            for i, line in enumerate(lines, 1):
                if current_pos + len(line) >= char_pos:
                    line_num = i
                    break
                current_pos += len(line) + 1  # +1 for newline

            # Check if there's a code block within 10 lines
            start_line = max(0, line_num - 10)
            end_line = min(len(lines), line_num + 10)
            nearby_lines = '\n'.join(lines[start_line:end_line])

            if '```' not in nearby_lines and len(code_text) > 5:
                issues.append(
                    Issue(
                        severity="low",
                        category="clarity",
                        file_path=filepath,
                        line_number=line_num,
                        issue_type="code_without_example",
                        description=f"Code element '{code_text}' mentioned without nearby example. Users request more practical examples.",
                        suggestion=f"Consider adding a code example showing '{code_text}' in use.",
                        auto_fixable=False
                    )
                )

        # Check 3: Long paragraphs (> 5 lines without breaks)
        paragraphs = content.split('\n\n')
        for para_num, para in enumerate(paragraphs):
            para_lines = para.split('\n')
            # Count non-empty, non-heading lines
            content_lines = [line for line in para_lines if line.strip() and not line.strip().startswith('#')]

            if len(content_lines) > 5:
                # Find approximate line number
                lines_before = sum(len(p.split('\n')) + 1 for p in paragraphs[:para_num])
                line_num = lines_before + 1

                issues.append(
                    Issue(
                        severity="low",
                        category="clarity",
                        file_path=filepath,
                        line_number=line_num,
                        issue_type="long_paragraph",
                        description="Long paragraph (>5 lines) without structure. Users report difficulty parsing dense text.",
                        suggestion="Break into smaller paragraphs, add bullet points, or use subheadings.",
                        auto_fixable=False
                    )
                )

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """
        Apply fixes to content.

        Note: Most GitHub-informed issues require human judgment and cannot be
        auto-fixed. This method flags them for manual review.

        Args:
            file_path: Path to the file being fixed
            content: The original content
            issues: List of issues to fix

        Returns:
            FixResult (unchanged, as these are manual review items)
        """
        # These issues are flagged for manual review, not auto-fixed
        # The value is in the detection, not automatic fixing
        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=content,
            fixes_applied=[],
            issues_fixed=[],
            content_changed=False
        )

    def get_statistics(self) -> Dict[str, Any]:
        """Return statistics about the GitHub research that informed this fixer."""
        return {
            "research_date": "2025-10-30",
            "issues_analyzed": 50,
            "repository": "anthropics/claude-code",
            "category_breakdown": {
                "Missing": "72%",
                "Findability": "12%",
                "Outdated": "10%",
                "Unclear": "4%",
                "Context": "2%"
            },
            "top_insight": "72% of documentation issues are about MISSING content, not unclear content",
            "checks_implemented": [
                "Very short pages detection",
                "Missing code examples detection",
                "Missing prerequisites detection",
                "Undefined jargon detection",
                "Code without examples detection",
                "Long paragraphs detection"
            ]
        }
