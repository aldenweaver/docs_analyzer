"""
Configuration management for doc_fixer
Loads and manages config.yaml settings
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration manager for doc_fixer"""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize configuration

        Args:
            config_path: Path to config.yaml file. If None, looks in current directory.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"

        self.config_path = Path(config_path)
        self.data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by dot-notation key

        Args:
            key: Configuration key (e.g., 'frontmatter.required')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split('.')
        value = self.data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    @property
    def preferred_terms(self) -> Dict[str, str]:
        """Get preferred terminology mappings"""
        return self.get('terminology.preferred_terms', {})

    @property
    def avoid_terms(self) -> list:
        """Get terms to avoid"""
        return self.get('terminology.avoid_terms', [])

    @property
    def required_frontmatter(self) -> list:
        """Get required frontmatter fields"""
        return self.get('frontmatter.required', ['title', 'description'])

    @property
    def frontmatter_formats(self) -> Dict[str, Any]:
        """Get frontmatter format specifications"""
        return self.get('frontmatter.formats', {})

    @property
    def internal_links_must_be_relative(self) -> bool:
        """Check if internal links must be relative"""
        return self.get('links.internal_must_be_relative', True)

    @property
    def code_blocks_require_language(self) -> bool:
        """Check if code blocks require language specification"""
        return self.get('code_blocks.require_language', True)

    @property
    def max_line_length(self) -> int:
        """Get maximum line length"""
        return self.get('formatting.max_line_length', 120)

    def __repr__(self) -> str:
        return f"Config(config_path='{self.config_path}')"
