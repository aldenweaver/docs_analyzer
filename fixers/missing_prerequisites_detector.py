"""
Missing Prerequisites Detector
Identifies tutorials and guides that lack "Before you begin" sections

Improves: User experience, clarity, reduced support burden

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
from typing import List

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class MissingPrerequisitesDetector(BaseFixer):
    """
    Detects tutorials/guides missing prerequisite sections

    Detection: Files with procedural content (steps, actions) but no "Before you begin" or "Prerequisites"
    Auto-fix: Not auto-fixable (requires domain knowledge to determine prerequisites)
    """

    def __init__(self, config: Config):
        super().__init__(config)

        # Indicators that a page is procedural/tutorial content
        self.procedural_indicators = [
            r'##\s+(Step\s+\d+|Steps?|Getting\s+Started|Quick\s+Start|Tutorial|Walkthrough|How\s+to)',
            r'\d+\.\s+\w+',  # Numbered lists
            r'First,\s+\w+',
            r'Then,\s+\w+',
            r'Next,\s+\w+',
            r'Finally,\s+\w+',
            r'To\s+\w+,\s+follow\s+these\s+steps',
            r'Follow\s+these\s+steps',
            r'Let\'s\s+\w+',
        ]

        # Prerequisites section indicators (if found, no issue)
        self.prerequisite_indicators = [
            r'##\s+(Before\s+you\s+begin|Prerequisites?|Requirements?|What\s+you\'ll\s+need)',
            r'\*\*Before\s+you\s+begin',
            r'\*\*Prerequisites?',
            r'\*\*Requirements?',
            r'<Prerequisites',  # Mintlify component
        ]

        # Common prerequisites to suggest
        self.common_prerequisites = [
            'Required tools or software installed',
            'API keys or credentials configured',
            'Prior knowledge or completed tutorials',
            'System requirements or environment setup',
        ]

    @property
    def name(self) -> str:
        return "Missing Prerequisites Detector"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Find procedural content without prerequisites section"""
        issues = []

        # Check if this is procedural content
        is_procedural = any(re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
                           for pattern in self.procedural_indicators)

        if not is_procedural:
            return issues  # Not a tutorial/guide, skip

        # Check if prerequisites are already present
        has_prerequisites = any(re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
                               for pattern in self.prerequisite_indicators)

        if has_prerequisites:
            return issues  # Prerequisites already exist

        # This is procedural content without prerequisites
        # Try to infer what prerequisites might be needed
        inferred_prereqs = self._infer_prerequisites(content)

        suggestion_text = 'Add a "Before you begin" or "Prerequisites" section'
        if inferred_prereqs:
            suggestion_text += f' (may need: {", ".join(inferred_prereqs)})'

        issues.append(Issue(
            severity='medium',
            category='ux',
            file_path=file_path,
            line_number=1,  # Top of file
            issue_type='missing_prerequisites',
            description='Tutorial/guide lacks prerequisites section',
            suggestion=suggestion_text,
            context='Procedural content detected but no "Before you begin" section found',
            auto_fixable=False  # Requires domain knowledge
        ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Prerequisites require domain knowledge - report only"""
        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=content,
            fixes_applied=[],
            issues_fixed=[]
        )

    def _infer_prerequisites(self, content: str) -> List[str]:
        """Infer likely prerequisites from content"""
        prereqs = []

        # Check for installation/setup commands
        if re.search(r'(npm\s+install|pip\s+install|brew\s+install|apt\s+install)', content):
            prereqs.append('Package manager installed')

        # Check for API usage
        if re.search(r'(API\s+key|api[_-]key|ANTHROPIC[_-]API[_-]KEY|auth.*token)', content, re.IGNORECASE):
            prereqs.append('API credentials configured')

        # Check for command-line usage
        if re.search(r'```bash\n\$', content):
            prereqs.append('Command-line access')

        # Check for specific tools
        if 'claude-code' in content.lower() or 'claude code' in content.lower():
            prereqs.append('Claude Code installed')

        if 'python' in content.lower() and re.search(r'```python', content):
            prereqs.append('Python installed')

        if 'node' in content.lower() or 'npm' in content.lower():
            prereqs.append('Node.js installed')

        if 'docker' in content.lower():
            prereqs.append('Docker installed')

        # Check for file creation/editing
        if re.search(r'(create\s+a\s+file|create\s+a\s+new\s+file|add\s+the\s+following\s+to)', content, re.IGNORECASE):
            prereqs.append('Text editor')

        # Limit to top 3 most relevant
        return prereqs[:3]
