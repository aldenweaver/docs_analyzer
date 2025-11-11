"""Content duplication detection"""

from pathlib import Path
from typing import List
from dataclasses import dataclass
from typing import Optional
from difflib import SequenceMatcher


# Re-import Issue dataclass (will be in __init__.py)
@dataclass
class Issue:
    """Represents a documentation issue"""
    severity: str  # 'critical', 'high', 'medium', 'low'
    category: str  # 'clarity', 'ia', 'consistency', 'style', 'gaps', 'ux', 'mintlify'
    file_path: str
    line_number: Optional[int]
    issue_type: str
    description: str
    suggestion: str
    context: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            'severity': self.severity,
            'category': self.category,
            'file': self.file_path,
            'line': self.line_number,
            'type': self.issue_type,
            'description': self.description,
            'suggestion': self.suggestion,
            'context': self.context
        }


class ContentDuplicationDetector:
    """Detect content duplication and redundancy"""

    def __init__(self, config: dict):
        self.config = config.get('duplication_detection', {})
        self.threshold = self.config.get('similarity_threshold', 0.8)
        self.enabled = self.config.get('enabled', True)

    def find_duplicates(self, files: List[Path], issues: List[Issue]):
        """Find duplicate or highly similar content"""
        if not self.enabled:
            return

        print("\n🔍 Detecting content duplication...")

        # Extract paragraphs from all files
        file_paragraphs = {}
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract paragraphs (2+ lines of text)
                    paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 100]
                    file_paragraphs[str(file_path)] = paragraphs
            except Exception:
                continue

        # Compare paragraphs across files
        checked_pairs = set()

        for file1, paras1 in file_paragraphs.items():
            for file2, paras2 in file_paragraphs.items():
                if file1 >= file2:  # Skip self and already checked pairs
                    continue

                pair_key = (file1, file2)
                if pair_key in checked_pairs:
                    continue
                checked_pairs.add(pair_key)

                # Compare paragraphs
                for i, p1 in enumerate(paras1):
                    for j, p2 in enumerate(paras2):
                        similarity = self._calculate_similarity(p1, p2)

                        if similarity >= self.threshold:
                            issues.append(Issue(
                                severity='medium',
                                category='gaps',
                                file_path=f'{file1} & {file2}',
                                line_number=None,
                                issue_type='duplicate_content',
                                description=f'Highly similar content detected ({int(similarity*100)}% similar)',
                                suggestion='Consider consolidating or cross-referencing instead of duplicating',
                                context=p1[:100] + '...'
                            ))

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity ratio"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()
