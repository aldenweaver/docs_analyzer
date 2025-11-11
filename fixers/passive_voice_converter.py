"""
Passive Voice Converter
Detects and suggests converting passive voice to active voice

Improves: Clarity, directness, engagement

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
from typing import List, Tuple

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class PassiveVoiceConverter(BaseFixer):
    """
    Detects passive voice constructions

    Detection: "is/are/was/were/be/been/being" + past participle
    Auto-fix: Not auto-fixable (requires context understanding for proper conversion)
    """

    def __init__(self, config: Config):
        super().__init__(config)

        # Common passive voice patterns
        # Format: (pattern, example)
        self.passive_patterns = [
            (r'\b(is|are|was|were|be|been|being)\s+([\w]+ed)\b', 'is configured'),
            (r'\b(is|are|was|were|be|been|being)\s+(shown|given|taken|made|done|run|written|sent|used)\b', 'is shown'),
            (r'\b(can|could|should|would|may|might|must)\s+be\s+([\w]+ed)\b', 'can be configured'),
            (r'\b(can|could|should|would|may|might|must)\s+be\s+(shown|given|taken|made|done|run|written|sent|used)\b', 'should be run'),
        ]

        # Exceptions (these are often acceptable in technical writing)
        self.exceptions = [
            r'\b(is|are)\s+required\b',  # "is required" is often clearest
            r'\b(is|are)\s+recommended\b',  # "is recommended" is standard
            r'\b(is|are)\s+supported\b',  # "is supported" is common
            r'\b(is|are)\s+deprecated\b',  # "is deprecated" is technical term
            r'\b(is|are)\s+enabled\b',  # "is enabled" is common in config
            r'\b(is|are)\s+disabled\b',  # "is disabled" is common in config
        ]

    @property
    def name(self) -> str:
        return "Passive Voice Converter"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Find passive voice constructions"""
        issues = []
        lines = content.split('\n')
        in_code_block = False

        for i, line in enumerate(lines, 1):
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block or line.strip().startswith('#'):
                continue

            # Skip list items and empty lines
            if not line.strip() or line.strip().startswith(('*', '-', '>', '|', '[')):
                continue

            # Check for passive voice patterns
            for pattern, example in self.passive_patterns:
                matches = list(re.finditer(pattern, line, re.IGNORECASE))

                for match in matches:
                    # Check if this matches an exception
                    is_exception = any(re.search(exc, match.group(0), re.IGNORECASE)
                                     for exc in self.exceptions)

                    if not is_exception:
                        # Extract context around the match
                        context_start = max(0, match.start() - 20)
                        context_end = min(len(line), match.end() + 30)
                        context = line[context_start:context_end].strip()

                        # Try to suggest active voice conversion
                        suggestion = self._suggest_active_voice(line, match)

                        issues.append(Issue(
                            severity='low',
                            category='clarity',
                            file_path=file_path,
                            line_number=i,
                            issue_type='passive_voice',
                            description=f'Passive voice detected: "{match.group(0)}"',
                            suggestion=suggestion,
                            context=context if len(context) < 100 else context[:100] + '...',
                            auto_fixable=False  # Requires context understanding
                        ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Passive voice conversion requires human judgment - report only"""
        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=content,
            fixes_applied=[],
            issues_fixed=[]
        )

    def _suggest_active_voice(self, line: str, match: re.Match) -> str:
        """Suggest active voice conversion based on context"""
        passive_phrase = match.group(0).lower()

        # Common conversions
        conversions = {
            'is configured': 'Configure',
            'are configured': 'Configure',
            'can be configured': 'You can configure',
            'should be configured': 'You should configure',
            'is shown': 'shows / displays',
            'are shown': 'show / display',
            'is used': 'Use / uses',
            'are used': 'Use',
            'can be used': 'You can use',
            'should be used': 'You should use',
            'is created': 'Create / creates',
            'are created': 'Create',
            'is sent': 'Send / sends',
            'are sent': 'Send',
            'is returned': 'returns',
            'are returned': 'return',
            'was created': 'created',
            'were created': 'created',
        }

        for passive, active in conversions.items():
            if passive in passive_phrase:
                return f'Consider using active voice: "{active}"'

        return 'Consider rephrasing in active voice (subject performs the action)'
