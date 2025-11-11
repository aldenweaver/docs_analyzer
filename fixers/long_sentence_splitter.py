"""
Long Sentence Splitter
Splits sentences longer than 30 words to improve readability

Improves: Cognitive load, comprehension, readability scores

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
from typing import List, Tuple

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


class LongSentenceSplitter(BaseFixer):
    """
    Splits overly long sentences

    Detection: Sentences >30 words
    Auto-fix: Splits at conjunctions, commas, or semicolons
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self.max_sentence_length = 30  # words

        # Split points (in order of preference)
        self.split_points = [
            (r',\s+and\s+', '. '),  # ", and" → ". "
            (r',\s+but\s+', '. However, '),  # ", but" → ". However,"
            (r',\s+which\s+', '. This '),  # ", which" → ". This"
            (r',\s+so\s+', '. Therefore, '),  # ", so" → ". Therefore,"
            (r';\s+', '. '),  # ";" → ". "
            (r',\s+', '. '),  # Last resort: any comma
        ]

    @property
    def name(self) -> str:
        return "Long Sentence Splitter"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Find sentences longer than max length"""
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

            # Skip list items, links, and empty lines
            if not line.strip() or line.strip().startswith(('*', '-', '>', '|', '[')):
                continue

            # Split line into sentences
            sentences = re.split(r'[.!?]+\s+', line)

            for sentence in sentences:
                word_count = len(sentence.split())

                if word_count > self.max_sentence_length:
                    # Check if we can split it
                    can_split = any(re.search(pattern, sentence) for pattern, _ in self.split_points)

                    issues.append(Issue(
                        severity='medium',
                        category='clarity',
                        file_path=file_path,
                        line_number=i,
                        issue_type='sentence_too_long',
                        description=f'Sentence has {word_count} words (recommend <{self.max_sentence_length})',
                        suggestion='Break into shorter sentences for better readability',
                        context=sentence[:100] + '...' if len(sentence) > 100 else sentence,
                        auto_fixable=can_split
                    ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Split long sentences at natural break points"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        lines = fixed_content.split('\n')
        in_code_block = False

        for i, line in enumerate(lines):
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue

            if in_code_block:
                continue

            # Check if this line has a fixable long sentence issue
            line_issues = [issue for issue in issues
                          if issue.line_number == i + 1 and issue.auto_fixable]

            if not line_issues:
                continue

            # Try to split the line
            new_line = line
            splits_made = 0

            for pattern, replacement in self.split_points:
                # Count words
                word_count = len(new_line.split())
                if word_count <= self.max_sentence_length:
                    break  # Already short enough

                # Try splitting
                if re.search(pattern, new_line):
                    # Split at first occurrence in second half of sentence
                    parts = new_line.split()
                    midpoint = len(parts) // 2

                    # Find split point after midpoint
                    second_half = ' '.join(parts[midpoint:])
                    match = re.search(pattern, second_half)

                    if match:
                        # Calculate position in full sentence
                        split_pos = new_line.find(second_half) + match.start()

                        # Apply split
                        before = new_line[:split_pos]
                        after = new_line[split_pos + len(match.group()):]

                        # Capitalize first word of new sentence
                        after = after.strip()
                        if after:
                            after = after[0].upper() + after[1:]

                        new_line = before + replacement + after
                        splits_made += 1
                        break

            if splits_made > 0:
                lines[i] = new_line
                fixes_applied.append(f'Split long sentence at line {i + 1} ({splits_made} splits)')
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
