"""Repository manager for different documentation platforms"""

import json
import hashlib
from pathlib import Path
from typing import List

# Try to import optional dependencies
try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False


class RepositoryManager:
    """Manages different documentation repository sources and types"""

    def __init__(self, config: dict):
        self.config = config.get('repository', {})
        self.repo_path = Path(self.config.get('path', './docs'))
        self.repo_root = Path(self.config.get('root', self.repo_path))  # For platform detection
        self.repo_type = None
        self.platform_config = None

    def detect_repo_type(self) -> str:
        """Auto-detect documentation platform"""
        if self.config.get('type') != 'auto':
            return self.config.get('type')

        # Look for platform files starting from repo_root, then check parents
        search_paths = [self.repo_root] + list(self.repo_root.parents)[:3]  # Check up to 3 levels up

        for search_path in search_paths:
            # Check for Mintlify (docs.json is current standard, mint.json is legacy)
            if (search_path / 'docs.json').exists():
                self.repo_root = search_path  # Update to where we found it
                return 'mintlify'
            elif (search_path / 'mint.json').exists():
                self.repo_root = search_path
                return 'mintlify'
            # Check for other platforms
            elif (search_path / 'docusaurus.config.js').exists():
                self.repo_root = search_path
                return 'docusaurus'
            elif (search_path / 'mkdocs.yml').exists():
                self.repo_root = search_path
                return 'mkdocs'

        return 'generic'

    def load_platform_config(self) -> dict:
        """Load platform-specific configuration"""
        self.repo_type = self.detect_repo_type()

        if self.repo_type == 'mintlify':
            return self._load_mintlify_config()
        else:
            return {}

    def _load_mintlify_config(self) -> dict:
        """Load Mintlify configuration (docs.json is current standard, mint.json is legacy)"""
        # Try docs.json first (current standard), then mint.json (backward compatibility)
        config_file = self.repo_root / 'docs.json'
        if not config_file.exists():
            config_file = self.repo_root / 'mint.json'

        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}

    def get_files(self) -> List[Path]:
        """Get all documentation files based on config"""
        include_patterns = self.config.get('include_patterns', ['**/*.mdx'])  # Only .mdx files by default
        exclude_patterns = self.config.get('exclude_patterns', [
            '**/node_modules/**',
            '**/build/**',
            '**/dist/**',
            '**/.git/**',
            '**/CLAUDE.md',
            '**/README.md'
        ])

        files = []
        for pattern in include_patterns:
            files.extend(self.repo_path.glob(pattern))

        # Filter out excluded patterns
        filtered_files = []
        for file in files:
            should_exclude = False
            for exclude_pattern in exclude_patterns:
                if file.match(exclude_pattern):
                    should_exclude = True
                    break
            if not should_exclude:
                filtered_files.append(file)

        return filtered_files

    def clone_remote_repo(self) -> Path:
        """Clone remote repository if configured"""
        remote_config = self.config.get('remote', {})
        if not remote_config.get('enabled') or not GIT_AVAILABLE:
            return self.repo_path

        url = remote_config.get('url')
        branch = remote_config.get('branch', 'main')

        clone_path = Path('/tmp') / hashlib.md5(url.encode()).hexdigest()

        if clone_path.exists():
            # Pull latest if exists
            repo = git.Repo(clone_path)
            repo.remotes.origin.pull(branch)
        else:
            # Clone repository
            git.Repo.clone_from(url, clone_path, branch=branch)

        return clone_path
