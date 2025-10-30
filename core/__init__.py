"""
Core module for doc_fixer
Contains shared models, configuration, and base classes
"""

from .models import FixResult, Issue
from .config import Config

__all__ = ['FixResult', 'Issue', 'Config']
