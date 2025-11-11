"""
Base fixer class that all fixers inherit from
"""

from abc import ABC, abstractmethod
from typing import List
from pathlib import Path

from core.models import Issue, FixResult
from core.config import Config


class BaseFixer(ABC):
    """Abstract base class for all fixers"""

    def __init__(self, config: Config):
        """
        Initialize fixer with configuration

        Args:
            config: Configuration object
        """
        self.config = config

    @abstractmethod
    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """
        Check file for issues that this fixer can address

        Args:
            file_path: Path to the file being checked
            content: File content

        Returns:
            List of issues found
        """
        pass

    @abstractmethod
    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """
        Apply fixes to file content

        Args:
            file_path: Path to the file being fixed
            content: Original file content
            issues: List of issues to fix

        Returns:
            FixResult with original content, fixed content, and metadata
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of this fixer"""
        pass

    def can_fix(self, issue: Issue) -> bool:
        """
        Check if this fixer can handle a specific issue

        Args:
            issue: Issue to check

        Returns:
            True if this fixer can handle the issue
        """
        return issue.auto_fixable

    def process_file(self, file_path: str) -> FixResult:
        """
        Complete processing pipeline: check and fix a file

        Args:
            file_path: Path to the file to process

        Returns:
            FixResult with fixes applied
        """
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for issues
            issues = self.check_file(file_path, content)

            # Filter to only auto-fixable issues
            fixable_issues = [issue for issue in issues if self.can_fix(issue)]

            if not fixable_issues:
                return FixResult(
                    file_path=file_path,
                    original_content=content,
                    fixed_content=content,
                    fixes_applied=[],
                    issues_fixed=[],
                    content_changed=False
                )

            # Apply fixes
            return self.fix(file_path, content, fixable_issues)

        except Exception as e:
            return FixResult(
                file_path=file_path,
                original_content="",
                fixed_content="",
                error=str(e)
            )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
