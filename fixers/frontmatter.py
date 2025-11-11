"""
Frontmatter fixer - validates and fixes YAML frontmatter in MDX files
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib

from core.models import Issue, FixResult
from core.config import Config
from fixers.base import BaseFixer
from utils.text_utils import extract_frontmatter, replace_frontmatter


class FrontmatterFixer(BaseFixer):
    """Validates and fixes frontmatter in MDX files"""

    def __init__(self, config: Config):
        super().__init__(config)
        self.required_fields = config.required_frontmatter
        self.max_desc_length = config.get('frontmatter.max_description_length', 160)
        self.min_desc_length = config.get('frontmatter.min_description_length', 50)

    @property
    def name(self) -> str:
        return "FrontmatterFixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check a file for frontmatter issues"""
        issues = []

        # Only check MDX files
        if not file_path.endswith('.mdx') and not file_path.endswith('.md'):
            return issues

        frontmatter, body, fm_lines = extract_frontmatter(content)

        if frontmatter is None:
            # No frontmatter at all - CRITICAL
            issues.append(Issue(
                severity="critical",
                category="mintlify",
                file_path=file_path,
                line_number=1,
                issue_type="missing_frontmatter",
                description="MDX file missing required frontmatter block",
                suggestion="Add YAML frontmatter block with title and description",
                auto_fixable=True
            ))
            return issues

        # Check required fields
        for field in self.required_fields:
            if field not in frontmatter or not frontmatter[field]:
                issues.append(Issue(
                    severity="high",
                    category="mintlify",
                    file_path=file_path,
                    line_number=1,
                    issue_type="missing_frontmatter_field",
                    description=f"Missing required frontmatter field: '{field}'",
                    suggestion=f"Add '{field}' field to frontmatter",
                    context=f"Required field: {field}",
                    auto_fixable=True
                ))

        # Check description length
        if 'description' in frontmatter and frontmatter['description']:
            desc = str(frontmatter['description'])
            desc_len = len(desc)

            if desc_len > self.max_desc_length:
                issues.append(Issue(
                    severity="medium",
                    category="style",
                    file_path=file_path,
                    line_number=1,
                    issue_type="description_too_long",
                    description=f"Description too long: {desc_len} chars (max {self.max_desc_length})",
                    suggestion=f"Shorten description to under {self.max_desc_length} characters",
                    context=desc,
                    auto_fixable=False
                ))
            elif desc_len < self.min_desc_length:
                issues.append(Issue(
                    severity="low",
                    category="style",
                    file_path=file_path,
                    line_number=1,
                    issue_type="description_too_short",
                    description=f"Description too short: {desc_len} chars (min {self.min_desc_length})",
                    suggestion=f"Expand description to at least {self.min_desc_length} characters for SEO",
                    context=desc,
                    auto_fixable=False
                ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Apply fixes to frontmatter"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        frontmatter, body, fm_lines = extract_frontmatter(content)

        # If no frontmatter at all, create it
        if frontmatter is None:
            title = self._generate_title(file_path, content)
            description = self._generate_description(content)

            new_frontmatter = {
                'title': title,
                'description': description
            }

            fixed_content = replace_frontmatter(content, new_frontmatter)
            fixes_applied.append("Added missing frontmatter block")
            issues_fixed = [i for i in issues if i.issue_type == "missing_frontmatter"]

        # If frontmatter exists but missing fields
        else:
            modified = False
            updated_frontmatter = frontmatter.copy()

            for issue in issues:
                if issue.issue_type == "missing_frontmatter_field":
                    # Extract field name from description
                    match = re.search(r"'([^']+)'", issue.description)
                    if match:
                        field_name = match.group(1)

                        if field_name == 'title' and not updated_frontmatter.get('title'):
                            updated_frontmatter['title'] = self._generate_title(file_path, content)
                            fixes_applied.append(f"Added missing '{field_name}' field")
                            issues_fixed.append(issue)
                            modified = True

                        elif field_name == 'description' and not updated_frontmatter.get('description'):
                            updated_frontmatter['description'] = self._generate_description(content)
                            fixes_applied.append(f"Added missing '{field_name}' field")
                            issues_fixed.append(issue)
                            modified = True

            if modified:
                fixed_content = replace_frontmatter(content, updated_frontmatter)

        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=fixed_content,
            fixes_applied=fixes_applied,
            issues_fixed=issues_fixed
        )

    @staticmethod
    def _generate_title(file_path: str, content: str) -> str:
        """Generate title from filename or first heading"""
        # Remove frontmatter for search
        content_without_fm = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        # Try to find first H1 heading
        h1_match = re.search(r'^#\s+(.+)$', content_without_fm, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()

        # Otherwise, use filename
        filename = Path(file_path).stem
        return filename.replace('-', ' ').replace('_', ' ').title()

    @staticmethod
    def _generate_description(content: str) -> str:
        """Generate description from first paragraph"""
        # Remove frontmatter
        content_without_fm = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)

        # Find first paragraph (after headings)
        lines = content_without_fm.split('\n')
        description_lines = []

        for line in lines:
            line = line.strip()
            # Skip empty lines, headings, and code blocks
            if line and not line.startswith('#') and not line.startswith('```'):
                description_lines.append(line)
                if len(' '.join(description_lines)) >= 100:
                    break

        description = ' '.join(description_lines)

        # Truncate to reasonable length
        if len(description) > 150:
            description = description[:147] + "..."

        return description if description else "Documentation page"
