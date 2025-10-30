"""
Data models for doc_fixer
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Issue:
    """Represents a documentation issue (imported from doc_analyzer for compatibility)"""
    severity: str  # 'critical', 'high', 'medium', 'low'
    category: str  # 'clarity', 'ia', 'consistency', 'style', 'gaps', 'ux', 'mintlify'
    file_path: str
    line_number: Optional[int]
    issue_type: str
    description: str
    suggestion: str
    context: Optional[str] = None
    auto_fixable: bool = False  # New field to indicate if issue can be auto-fixed

    def to_dict(self) -> dict:
        return {
            'severity': self.severity,
            'category': self.category,
            'file': self.file_path,
            'line': self.line_number,
            'type': self.issue_type,
            'description': self.description,
            'suggestion': self.suggestion,
            'context': self.context,
            'auto_fixable': self.auto_fixable
        }


@dataclass
class FixResult:
    """Result of applying fixes to a file"""
    file_path: str
    original_content: str
    fixed_content: str
    fixes_applied: List[str] = field(default_factory=list)
    issues_fixed: List[Issue] = field(default_factory=list)
    content_changed: bool = False
    error: Optional[str] = None

    def __post_init__(self):
        """Auto-detect if content changed"""
        if self.original_content != self.fixed_content:
            self.content_changed = True

    def to_dict(self) -> dict:
        return {
            'file_path': self.file_path,
            'fixes_applied': self.fixes_applied,
            'issues_fixed': [issue.to_dict() for issue in self.issues_fixed],
            'content_changed': self.content_changed,
            'error': self.error
        }

    def summary(self) -> str:
        """Generate human-readable summary"""
        if self.error:
            return f"❌ Error in {self.file_path}: {self.error}"

        if not self.content_changed:
            return f"✅ No changes needed in {self.file_path}"

        fixes_count = len(self.fixes_applied)
        return f"✅ Applied {fixes_count} fix(es) to {self.file_path}: {', '.join(self.fixes_applied)}"


@dataclass
class FixerStats:
    """Statistics about fixes applied across all files"""
    total_files_processed: int = 0
    files_modified: int = 0
    total_fixes_applied: int = 0
    fixes_by_type: dict = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)

    def add_result(self, result: FixResult):
        """Add a FixResult to statistics"""
        self.total_files_processed += 1

        if result.error:
            self.errors.append(f"{result.file_path}: {result.error}")
            return

        if result.content_changed:
            self.files_modified += 1
            self.total_fixes_applied += len(result.fixes_applied)

            for fix in result.fixes_applied:
                self.fixes_by_type[fix] = self.fixes_by_type.get(fix, 0) + 1

    def to_dict(self) -> dict:
        return {
            'total_files_processed': self.total_files_processed,
            'files_modified': self.files_modified,
            'total_fixes_applied': self.total_fixes_applied,
            'fixes_by_type': self.fixes_by_type,
            'errors': self.errors
        }

    def summary(self) -> str:
        """Generate human-readable summary"""
        summary_lines = [
            f"\n{'='*60}",
            f"Fix Summary:",
            f"{'='*60}",
            f"Total files processed: {self.total_files_processed}",
            f"Files modified: {self.files_modified}",
            f"Total fixes applied: {self.total_fixes_applied}",
        ]

        if self.fixes_by_type:
            summary_lines.append("\nFixes by type:")
            for fix_type, count in sorted(self.fixes_by_type.items(), key=lambda x: x[1], reverse=True):
                summary_lines.append(f"  - {fix_type}: {count}")

        if self.errors:
            summary_lines.append(f"\nErrors encountered: {len(self.errors)}")
            for error in self.errors[:5]:  # Show first 5 errors
                summary_lines.append(f"  - {error}")
            if len(self.errors) > 5:
                summary_lines.append(f"  ... and {len(self.errors) - 5} more")

        summary_lines.append(f"{'='*60}\n")
        return "\n".join(summary_lines)
