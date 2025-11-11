"""
Code block fixer - fixes code block formatting issues
"""

import re
from typing import List
from datetime import datetime

from core.models import Issue, FixResult
from core.config import Config
from fixers.base import BaseFixer


class CodeBlockFixer(BaseFixer):
    """Fixes code block formatting issues"""

    def __init__(self, config: Config):
        super().__init__(config)
        self.require_language = config.code_blocks_require_language

    @property
    def name(self) -> str:
        return "CodeBlockFixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check file for code block issues"""
        issues = []

        if not self.require_language:
            return issues

        lines = content.split('\n')

        # Track code blocks
        in_code_block = False
        block_start_line = None

        for line_num, line in enumerate(lines, 1):
            # Check for code block start
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Starting a code block
                    in_code_block = True
                    block_start_line = line_num

                    # Extract language tag (everything after ```)
                    lang_tag = line.strip()[3:].strip()

                    # If no language tag, flag it
                    if not lang_tag:
                        issues.append(Issue(
                            severity="medium",
                            category="style",
                            file_path=file_path,
                            line_number=line_num,
                            issue_type="missing_code_language",
                            description="Code block missing language identifier",
                            suggestion="Add language identifier (e.g., ```python, ```typescript, ```bash)",
                            context=line.strip(),
                            auto_fixable=False  # Requires knowing what language the code is
                        ))
                else:
                    # Ending a code block
                    in_code_block = False
                    block_start_line = None

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Apply code block fixes"""
        # Code block fixes are not auto-fixable as they require
        # knowing what programming language the code is written in
        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=content,
            fixes_applied=[],
            issues_fixed=[]
        )
