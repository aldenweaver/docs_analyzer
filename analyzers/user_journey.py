"""User journey validation"""

from typing import Dict, Any, List
from dataclasses import dataclass
from typing import Optional


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


class UserJourneyAnalyzer:
    """Analyze if documentation supports common user journeys"""

    def __init__(self, config: dict):
        self.config = config.get('gap_detection', {})
        self.required_journeys = self.config.get('required_journeys', [])

    def validate_journeys(self, doc_structure: Dict[str, Any], issues: List[Issue]):
        """Check if required user journeys are supported"""
        print("\n🚶 Validating user journeys...")

        files = doc_structure.get('files', [])
        file_names = [f.lower() for f in files]

        for journey in self.required_journeys:
            name = journey.get('name', 'Unknown journey')
            steps = journey.get('steps', [])

            missing_steps = []
            for step in steps:
                # Check if any file name contains this step
                if not any(step.lower() in fname for fname in file_names):
                    missing_steps.append(step)

            if missing_steps:
                issues.append(Issue(
                    severity='high',
                    category='gaps',
                    file_path='[documentation set]',
                    line_number=None,
                    issue_type='incomplete_user_journey',
                    description=f'User journey "{name}" is incomplete',
                    suggestion=f'Add documentation for: {", ".join(missing_steps)}'
                ))
