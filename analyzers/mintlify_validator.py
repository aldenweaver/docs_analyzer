"""Mintlify-specific validation"""

import re
from typing import List
from dataclasses import dataclass
from typing import Optional

# Import from parent package
from analyzers.mdx_parser import MDXParser
from analyzers.repository_manager import RepositoryManager


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


class MintlifyValidator:
    """Validate Mintlify-specific requirements"""

    def __init__(self, config: dict, repo_manager: RepositoryManager):
        self.config = config.get('mintlify', {})
        self.repo_manager = repo_manager
        self.platform_config = repo_manager.platform_config

        # Valid Mintlify components
        self.valid_components = set(self.config.get('components', {}).get('valid_components', [
            'Card', 'CardGroup', 'Accordion', 'AccordionGroup',
            'Tab', 'Tabs', 'CodeGroup', 'Frame', 'Steps',
            'Info', 'Warning', 'Tip', 'Note', 'Check', 'ParamField'
        ]))

    def validate_frontmatter(self, file_path: str, content: str, issues: List[Issue]):
        """Validate frontmatter requirements"""
        if not file_path.endswith('.mdx'):
            return

        frontmatter, _ = MDXParser.parse_frontmatter(content)

        # Check if frontmatter exists (critical for MDX)
        if frontmatter is None:
            issues.append(Issue(
                severity='critical',
                category='mintlify',
                file_path=file_path,
                line_number=1,
                issue_type='missing_frontmatter',
                description='MDX files MUST have YAML frontmatter',
                suggestion='Add frontmatter with at minimum: title and description'
            ))
            return

        if frontmatter:
            # Check required fields
            required = self.config.get('required_frontmatter', ['title', 'description'])
            for field in required:
                if field not in frontmatter:
                    issues.append(Issue(
                        severity='critical',
                        category='mintlify',
                        file_path=file_path,
                        line_number=1,
                        issue_type='missing_required_frontmatter',
                        description=f'Missing required frontmatter field: {field}',
                        suggestion=f'Add "{field}: <value>" to frontmatter'
                    ))

            # Validate field values
            if 'title' in frontmatter:
                if len(str(frontmatter['title'])) < 3:
                    issues.append(Issue(
                        severity='medium',
                        category='mintlify',
                        file_path=file_path,
                        line_number=1,
                        issue_type='short_title',
                        description='Title is too short',
                        suggestion='Provide a clear, descriptive title (at least 3 characters)'
                    ))

            if 'description' in frontmatter:
                desc_len = len(str(frontmatter['description']))
                if desc_len < 20:
                    issues.append(Issue(
                        severity='medium',
                        category='mintlify',
                        file_path=file_path,
                        line_number=1,
                        issue_type='short_description',
                        description='Description is too short for SEO',
                        suggestion='Provide a concise but informative description (20-160 characters)'
                    ))
                elif desc_len > 160:
                    issues.append(Issue(
                        severity='low',
                        category='mintlify',
                        file_path=file_path,
                        line_number=1,
                        issue_type='long_description',
                        description='Description exceeds SEO-optimal length',
                        suggestion='Keep description under 160 characters for better SEO'
                    ))

    def validate_components(self, file_path: str, content: str, issues: List[Issue]):
        """Validate Mintlify component usage"""
        if not self.config.get('components', {}).get('enabled', True):
            return

        components = MDXParser.extract_components(content)

        for component_name, line_number in components:
            if component_name not in self.valid_components:
                # Check if it's a standard HTML element
                html_elements = {'div', 'span', 'p', 'a', 'img', 'video', 'iframe', 'br', 'hr'}
                if component_name.lower() not in html_elements:
                    issues.append(Issue(
                        severity='medium',
                        category='mintlify',
                        file_path=file_path,
                        line_number=line_number,
                        issue_type='invalid_component',
                        description=f'Unknown Mintlify component: <{component_name}>',
                        suggestion=f'Verify component name or use standard Mintlify components'
                    ))

    def validate_internal_links(self, file_path: str, content: str, issues: List[Issue]):
        """Validate that internal links use relative paths (critical for Mintlify)"""
        if not self.config.get('links', {}).get('internal_must_be_relative', True):
            return

        lines = content.split('\n')

        # Pattern for markdown links
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'

        for i, line in enumerate(lines, 1):
            for match in re.finditer(link_pattern, line):
                link_url = match.group(2)

                # Check if it's an internal docs link (absolute URL)
                if any(domain in link_url for domain in ['docs.claude.com', 'docs.anthropic', 'mintlify.app']):
                    issues.append(Issue(
                        severity='critical',
                        category='mintlify',
                        file_path=file_path,
                        line_number=i,
                        issue_type='absolute_internal_url',
                        description='Internal links MUST use relative paths, not absolute URLs',
                        suggestion=f'Convert "{link_url}" to relative path (e.g., ./page.md or ../section/page.md)',
                        context=line.strip()
                    ))
