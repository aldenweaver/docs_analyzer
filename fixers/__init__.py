"""
Fixers module for doc_fixer
Contains all concrete fixer implementations
"""

from .base import BaseFixer
from .frontmatter import FrontmatterFixer
from .terminology import TerminologyFixer
from .urls import URLFixer
from .code_blocks import CodeBlockFixer
from .github_informed_fixer import GitHubInformedFixer
from .style_guide_validator import StyleGuideValidationFixer

# High-impact fixers from comprehensive research
from .code_language_tags import CodeLanguageTagFixer
from .heading_hierarchy import HeadingHierarchyFixer
from .link_text_improver import LinkTextImprover
from .long_sentence_splitter import LongSentenceSplitter
from .passive_voice_converter import PassiveVoiceConverter
from .missing_prerequisites_detector import MissingPrerequisitesDetector

# Style consistency fixers from style-consistency-analysis
from .capitalization_fixer import CapitalizationFixer
from .terminology_consistency_fixer import TerminologyConsistencyFixer
from .callout_standardization_fixer import CalloutStandardizationFixer
from .broken_link_detector import BrokenLinkDetector
from .production_code_validator import ProductionCodeValidator

# Accessibility fixer
from .accessibility_fixer import AccessibilityFixer

__all__ = [
    'BaseFixer',
    'FrontmatterFixer',
    'TerminologyFixer',
    'URLFixer',
    'CodeBlockFixer',
    'GitHubInformedFixer',
    'StyleGuideValidationFixer',
    # High-impact fixers
    'CodeLanguageTagFixer',
    'HeadingHierarchyFixer',
    'LinkTextImprover',
    'LongSentenceSplitter',
    'PassiveVoiceConverter',
    'MissingPrerequisitesDetector',
    # Style consistency fixers
    'CapitalizationFixer',
    'TerminologyConsistencyFixer',
    'CalloutStandardizationFixer',
    'BrokenLinkDetector',
    'ProductionCodeValidator',
    # Accessibility
    'AccessibilityFixer',
]
