"""
Metadata Enrichment Fixer - Enhances frontmatter for better AI discoverability.

This fixer improves documentation metadata by adding missing fields, enhancing descriptions,
generating keywords from content, and ensuring metadata quality for AI search systems.
"""

import re
import yaml
from typing import List, Dict, Optional, Set, Tuple
from collections import Counter
from core.models import Issue, FixResult
from core.config import Config
from fixers.base import BaseFixer


class MetadataEnrichmentFixer(BaseFixer):
    """Enhance frontmatter metadata for better AI discoverability"""

    def __init__(self, config: Config):
        super().__init__(config)

        # Valid content types
        self.valid_content_types = {
            'guide', 'tutorial', 'reference', 'concept', 'explanation',
            'how-to', 'quickstart', 'api-reference', 'troubleshooting',
            'faq', 'glossary', 'overview', 'example', 'best-practices'
        }

        # Valid audience levels
        self.valid_audience_levels = {
            'beginner', 'intermediate', 'advanced', 'expert', 'all'
        }

        # Stop words to exclude from keyword generation
        self.stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 'was', 'were',
            'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'from', 'by', 'this',
            'that', 'these', 'those', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'could',
            'it', 'its', 'our', 'your', 'their', 'his', 'her', 'we', 'you', 'they',
            'am', 'been', 'being', 'get', 'got', 'getting', 'make', 'made', 'making'
        }

        # Generic description patterns to improve
        self.generic_description_patterns = [
            r'^This (page|document|section|article) (describes|explains|covers|discusses)',
            r'^(Learn|Read) about',
            r'^(Overview|Introduction|Guide) to',
            r'^Documentation for',
            r'^Information about'
        ]

    @property
    def name(self) -> str:
        return "MetadataEnrichmentFixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check file for metadata issues"""
        issues = []

        # Parse frontmatter and content
        frontmatter, content_body = self._parse_frontmatter(content)

        if not frontmatter:
            issues.append(Issue(
                severity="critical",
                category="ai_search",
                file_path=file_path,
                line_number=1,
                issue_type="missing_frontmatter",
                description="No frontmatter found",
                suggestion="Add frontmatter with title, description, and keywords",
                context="",
                auto_fixable=True
            ))
            return issues

        # Check for missing required fields
        required_fields = ['title', 'description']
        for field in required_fields:
            if field not in frontmatter or not frontmatter[field]:
                issues.append(Issue(
                    severity="critical",
                    category="ai_search",
                    file_path=file_path,
                    line_number=1,
                    issue_type="missing_required_metadata",
                    description=f"Required field '{field}' is missing",
                    suggestion=f"Add '{field}' field to frontmatter",
                    context="",
                    auto_fixable=True if field == 'description' else False
                ))

        # Check description quality
        if 'description' in frontmatter:
            desc_issues = self._check_description_quality(
                frontmatter['description'],
                frontmatter.get('title', ''),
                file_path
            )
            issues.extend(desc_issues)

        # Check for missing valuable fields
        valuable_fields = ['keywords', 'tags', 'content_type', 'audience_level']
        missing_valuable = [f for f in valuable_fields if f not in frontmatter]

        if len(missing_valuable) >= 2:
            issues.append(Issue(
                severity="medium",
                category="ai_search",
                file_path=file_path,
                line_number=1,
                issue_type="metadata_lacks_richness",
                description=f"Metadata lacks richness (missing: {', '.join(missing_valuable[:2])})",
                suggestion="Add keywords and content_type for better AI discoverability",
                context="",
                auto_fixable=True
            ))

        # Check if keywords match content
        if 'keywords' in frontmatter or 'tags' in frontmatter:
            keyword_issues = self._check_keyword_relevance(
                frontmatter.get('keywords', frontmatter.get('tags', [])),
                content_body,
                file_path
            )
            issues.extend(keyword_issues)

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Apply metadata enrichment fixes"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        # Parse frontmatter
        frontmatter, content_body = self._parse_frontmatter(content)

        # Handle missing frontmatter
        if not frontmatter and any(i.issue_type == "missing_frontmatter" for i in issues):
            frontmatter = {}
            title = self._extract_title_from_content(content_body)
            frontmatter['title'] = title or "Untitled Document"
            frontmatter['description'] = self._generate_description(content_body, title)

            fixes_applied.append({
                'type': 'add_frontmatter',
                'original': 'No frontmatter',
                'fixed': 'Added frontmatter with title and description'
            })

            # Find the issue to mark as fixed
            for issue in issues:
                if issue.issue_type == "missing_frontmatter":
                    issues_fixed.append(issue)
                    break

        # Fix missing description
        if 'description' not in frontmatter or not frontmatter.get('description'):
            for issue in issues:
                if issue.issue_type == "missing_required_metadata" and "description" in issue.description:
                    title = frontmatter.get('title', '')
                    description = self._generate_description(content_body, title)
                    frontmatter['description'] = description

                    fixes_applied.append({
                        'type': 'add_description',
                        'original': 'No description',
                        'fixed': f'Added: "{description}"'
                    })
                    issues_fixed.append(issue)
                    break

        # Improve poor quality description
        if 'description' in frontmatter:
            for issue in issues:
                if issue.issue_type in ["description_too_short", "description_identical_to_title", "generic_description"]:
                    title = frontmatter.get('title', '')
                    improved_desc = self._improve_description(
                        frontmatter['description'],
                        content_body,
                        title
                    )
                    if improved_desc != frontmatter['description']:
                        fixes_applied.append({
                            'type': 'improve_description',
                            'original': frontmatter['description'],
                            'fixed': improved_desc
                        })
                        frontmatter['description'] = improved_desc
                        issues_fixed.append(issue)

        # Add missing keywords
        if 'keywords' not in frontmatter and 'tags' not in frontmatter:
            for issue in issues:
                if "keywords" in issue.description or issue.issue_type == "metadata_lacks_richness":
                    keywords = self._generate_keywords(content_body, frontmatter.get('title', ''))
                    if keywords:
                        frontmatter['keywords'] = keywords
                        fixes_applied.append({
                            'type': 'add_keywords',
                            'original': 'No keywords',
                            'fixed': f'Added: {", ".join(keywords)}'
                        })
                        issues_fixed.append(issue)
                        break

        # Add content_type if missing
        if 'content_type' not in frontmatter:
            for issue in issues:
                if "content_type" in issue.description or issue.issue_type == "metadata_lacks_richness":
                    content_type = self._detect_content_type(content_body, frontmatter.get('title', ''))
                    if content_type:
                        frontmatter['content_type'] = content_type
                        fixes_applied.append({
                            'type': 'add_content_type',
                            'original': 'No content_type',
                            'fixed': f'Added: {content_type}'
                        })
                        # Don't mark metadata_lacks_richness as fixed since it might need more fields
                        if "content_type" in issue.description:
                            issues_fixed.append(issue)
                        break

        # Rebuild content with updated frontmatter
        if fixes_applied:
            fixed_content = self._rebuild_content_with_frontmatter(frontmatter, content_body)

        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=fixed_content,
            fixes_applied=fixes_applied,
            issues_fixed=issues_fixed,
            content_changed=fixed_content != content
        )

    def _parse_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Parse frontmatter and return (frontmatter_dict, content_body)"""
        lines = content.split('\n')

        if not lines or lines[0].strip() != '---':
            return None, content

        # Find the closing ---
        end_index = None
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_index = i
                break

        if not end_index:
            return None, content

        # Parse YAML frontmatter
        frontmatter_text = '\n'.join(lines[1:end_index])
        try:
            frontmatter = yaml.safe_load(frontmatter_text) or {}
        except yaml.YAMLError:
            return None, content

        # Return frontmatter and remaining content
        content_body = '\n'.join(lines[end_index + 1:])
        return frontmatter, content_body

    def _rebuild_content_with_frontmatter(self, frontmatter: Dict, content_body: str) -> str:
        """Rebuild content with updated frontmatter"""
        # Convert frontmatter to YAML
        yaml_text = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)

        # Build the complete content
        return f"---\n{yaml_text}---\n{content_body}"

    def _check_description_quality(self, description: str, title: str, file_path: str) -> List[Issue]:
        """Check the quality of the description"""
        issues = []

        # Check length
        desc_length = len(description)
        if desc_length < 50:
            issues.append(Issue(
                severity="high",
                category="ai_search",
                file_path=file_path,
                line_number=1,
                issue_type="description_too_short",
                description=f"Description too short ({desc_length} chars, minimum 50)",
                suggestion="Expand description to provide more context",
                context=description,
                auto_fixable=True
            ))
        elif desc_length > 160:
            issues.append(Issue(
                severity="medium",
                category="ai_search",
                file_path=file_path,
                line_number=1,
                issue_type="description_too_long",
                description=f"Description too long ({desc_length} chars, maximum 160)",
                suggestion="Shorten description for better search display",
                context=description,
                auto_fixable=False
            ))

        # Check if description is identical to title
        if title and description.lower().strip() == title.lower().strip():
            issues.append(Issue(
                severity="high",
                category="ai_search",
                file_path=file_path,
                line_number=1,
                issue_type="description_identical_to_title",
                description="Description identical to title",
                suggestion="Write a unique description that expands on the title",
                context=description,
                auto_fixable=True
            ))

        # Check for generic patterns
        for pattern in self.generic_description_patterns:
            if re.match(pattern, description, re.IGNORECASE):
                issues.append(Issue(
                    severity="medium",
                    category="ai_search",
                    file_path=file_path,
                    line_number=1,
                    issue_type="generic_description",
                    description="Generic description pattern detected",
                    suggestion="Write a specific description highlighting unique value",
                    context=description,
                    auto_fixable=True
                ))
                break

        return issues

    def _check_keyword_relevance(self, keywords: List, content: str, file_path: str) -> List[Issue]:
        """Check if keywords are relevant to content"""
        issues = []

        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(',')]
        elif not isinstance(keywords, list):
            return issues

        content_lower = content.lower()
        missing_keywords = []

        for keyword in keywords:
            if isinstance(keyword, str) and keyword.lower() not in content_lower:
                missing_keywords.append(keyword)

        if missing_keywords:
            issues.append(Issue(
                severity="medium",
                category="ai_search",
                file_path=file_path,
                line_number=1,
                issue_type="keywords_not_in_content",
                description=f"Keywords not found in content: {', '.join(missing_keywords[:3])}",
                suggestion="Use keywords that actually appear in the content",
                context=str(keywords),
                auto_fixable=False
            ))

        return issues

    def _extract_title_from_content(self, content: str) -> Optional[str]:
        """Extract title from first heading in content"""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return None

    def _generate_description(self, content: str, title: str) -> str:
        """Generate a description from content"""
        # Remove code blocks and special formatting
        clean_content = re.sub(r'```[\s\S]*?```', '', content)
        clean_content = re.sub(r'`[^`]+`', '', clean_content)
        clean_content = re.sub(r'[#*_\[\]()]', '', clean_content)

        # Get first substantive paragraph
        paragraphs = clean_content.split('\n\n')
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50 and not para.startswith('-'):
                # Truncate to ~150 chars at word boundary
                if len(para) > 150:
                    para = para[:150]
                    last_space = para.rfind(' ')
                    if last_space > 100:
                        para = para[:last_space] + '...'
                return para

        # Fallback: use title-based description
        if title:
            return f"Documentation for {title}"

        return "Technical documentation page"

    def _improve_description(self, current_desc: str, content: str, title: str) -> str:
        """Improve an existing description"""
        # If description is too short or generic, generate a better one
        if len(current_desc) < 50 or any(
            re.match(p, current_desc, re.IGNORECASE)
            for p in self.generic_description_patterns
        ):
            return self._generate_description(content, title)

        # If description is identical to title, generate new one
        if title and current_desc.lower().strip() == title.lower().strip():
            return self._generate_description(content, title)

        return current_desc

    def _generate_keywords(self, content: str, title: str) -> List[str]:
        """Generate keywords from content"""
        # Clean content
        clean_content = re.sub(r'```[\s\S]*?```', '', content)
        clean_content = re.sub(r'`[^`]+`', '', clean_content)
        clean_content = re.sub(r'[#*_\[\](){}|]', '', clean_content)

        # Combine title and content
        full_text = f"{title} {clean_content}".lower()

        # Extract words
        words = re.findall(r'\b[a-z]+\b', full_text)

        # Count word frequency
        word_freq = Counter(words)

        # Remove stop words
        for word in self.stop_words:
            word_freq.pop(word, None)

        # Extract technical terms (capitalized words, acronyms)
        tech_pattern = re.compile(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)*|[A-Z]{2,})\b')
        technical_terms = set()
        for match in tech_pattern.finditer(content):
            term = match.group(1)
            if term not in ['The', 'This', 'That', 'These', 'Those']:
                technical_terms.add(term)

        # Get top words
        keywords = []

        # Add technical terms first
        for term in list(technical_terms)[:3]:
            keywords.append(term)

        # Add high-frequency meaningful words
        for word, freq in word_freq.most_common(20):
            if len(word) > 3 and freq > 2 and word not in [k.lower() for k in keywords]:
                keywords.append(word)
                if len(keywords) >= 8:
                    break

        return keywords[:8]  # Limit to 8 keywords

    def _detect_content_type(self, content: str, title: str) -> Optional[str]:
        """Detect content type based on patterns"""
        content_lower = content.lower()
        title_lower = title.lower()

        # Check title patterns
        if any(word in title_lower for word in ['guide', 'how to', 'getting started', 'quickstart']):
            return 'guide'
        elif any(word in title_lower for word in ['tutorial', 'walkthrough', 'step by step']):
            return 'tutorial'
        elif any(word in title_lower for word in ['reference', 'api', 'methods', 'properties']):
            return 'reference'
        elif any(word in title_lower for word in ['concept', 'overview', 'introduction', 'understanding']):
            return 'concept'
        elif 'troubleshoot' in title_lower or 'problem' in title_lower:
            return 'troubleshooting'

        # Check content patterns
        if '## prerequisites' in content_lower or '## requirements' in content_lower:
            return 'guide'
        elif re.search(r'\n\d+\.\s+', content):  # Numbered steps
            return 'tutorial'
        elif '## parameters' in content_lower or '## returns' in content_lower:
            return 'reference'
        elif 'frequently asked' in content_lower or 'faq' in content_lower:
            return 'faq'
        elif '## example' in content_lower and '## code' in content_lower:
            return 'example'

        # Default based on content structure
        code_blocks = len(re.findall(r'```', content))
        if code_blocks > 3:
            return 'example'

        return 'concept'  # Default fallback