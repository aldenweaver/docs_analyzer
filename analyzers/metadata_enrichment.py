"""
Metadata Enrichment Validator - Validates metadata that helps AI systems understand content.

This module ensures documentation has rich metadata (frontmatter) that enables AI systems
to better categorize, discover, and understand the content context.
"""

import re
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass
from collections import Counter


@dataclass
class MetadataIssue:
    """Represents a metadata enrichment issue."""
    file_path: str
    issue_type: str  # 'missing_metadata', 'poor_quality', 'keyword_mismatch', 'categorization'
    severity: str    # 'critical', 'high', 'medium', 'low'
    message: str
    field: Optional[str] = None
    suggestion: Optional[str] = None
    current_value: Optional[Any] = None


class MetadataEnrichmentValidator:
    """
    Validates metadata that helps AI systems understand and categorize content.

    This validator ensures:
    1. Frontmatter provides rich context
    2. Keywords match content
    3. Categorization aids discovery
    4. Descriptions are substantive
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Metadata Enrichment Validator.

        Args:
            config: Configuration dictionary with metadata requirements
        """
        self.config = config or {}
        self.metadata_config = self.config.get('ai_search_optimization', {}).get('metadata', {})

        # Required fields
        self.required_fields = ['title', 'description']
        if self.metadata_config.get('require_content_type', False):
            self.required_fields.append('content_type')
        if self.metadata_config.get('require_audience_level', False):
            self.required_fields.append('audience_level')
        if self.metadata_config.get('require_keywords', False):
            self.required_fields.append('keywords')

        # Content types for categorization
        self.valid_content_types = {
            'guide', 'tutorial', 'reference', 'concept', 'explanation',
            'how-to', 'quickstart', 'api-reference', 'troubleshooting',
            'faq', 'glossary', 'overview', 'example', 'best-practices'
        }

        # Audience levels
        self.valid_audience_levels = {
            'beginner', 'intermediate', 'advanced', 'expert', 'all'
        }

        # Description quality parameters
        self.min_description_length = self.metadata_config.get('min_description_length', 50)
        self.max_description_length = self.metadata_config.get('max_description_length', 160)

        # Common stop words to exclude from keyword analysis
        self.stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 'was', 'were',
            'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'from', 'by', 'this',
            'that', 'these', 'those', 'be', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'could',
            'it', 'its', 'our', 'your', 'their', 'his', 'her'
        }

    def validate(self, frontmatter: Optional[Dict[str, Any]], content: str, file_path: str) -> List[MetadataIssue]:
        """
        Validate metadata for AI system optimization.

        Args:
            frontmatter: The frontmatter/metadata dictionary
            content: The document content
            file_path: Path to the file being validated

        Returns:
            List of metadata issues found
        """
        issues = []

        # Check if frontmatter exists
        if not frontmatter:
            issues.append(MetadataIssue(
                file_path=file_path,
                issue_type='missing_metadata',
                severity='critical',
                message='No frontmatter found',
                suggestion='Add frontmatter with at least title and description'
            ))
            return issues

        # Check required fields
        issues.extend(self.check_required_fields(frontmatter, file_path))

        # Check frontmatter richness
        issues.extend(self.check_frontmatter_richness(frontmatter, file_path))

        # Check description quality
        if 'description' in frontmatter:
            issues.extend(self.check_description_quality(frontmatter['description'], frontmatter.get('title', ''), file_path))

        # Check semantic keywords
        if 'keywords' in frontmatter or 'tags' in frontmatter:
            issues.extend(self.check_semantic_keywords(content, frontmatter, file_path))

        # Check content categorization
        issues.extend(self.check_content_categorization(frontmatter, content, file_path))

        # Check for related topics
        issues.extend(self.check_related_topics(frontmatter, file_path))

        return issues

    def check_required_fields(self, frontmatter: Dict[str, Any], file_path: str) -> List[MetadataIssue]:
        """
        Check for required metadata fields.

        Args:
            frontmatter: The frontmatter dictionary
            file_path: Path to the file

        Returns:
            List of issues for missing required fields
        """
        issues = []

        for field in self.required_fields:
            if field not in frontmatter or not frontmatter[field]:
                severity = 'critical' if field in ['title', 'description'] else 'high'
                issues.append(MetadataIssue(
                    file_path=file_path,
                    issue_type='missing_metadata',
                    severity=severity,
                    message=f'Required field "{field}" is missing or empty',
                    field=field,
                    suggestion=self._get_field_suggestion(field)
                ))

        return issues

    def check_frontmatter_richness(self, frontmatter: Dict[str, Any], file_path: str) -> List[MetadataIssue]:
        """
        Ensures frontmatter provides rich context for AI.

        Checks:
        - Presence of optional but valuable fields
        - Quality of metadata provided
        """
        issues = []

        # Check for valuable optional fields
        valuable_fields = {
            'keywords': 'Add keywords to improve discoverability',
            'tags': 'Add tags for better categorization',
            'content_type': 'Specify content type (guide, tutorial, reference, etc.)',
            'audience_level': 'Specify audience level (beginner, intermediate, advanced)',
            'related': 'List related documentation pages',
            'prerequisites': 'List prerequisite knowledge or pages',
            'last_updated': 'Add last updated date for freshness',
            'estimated_time': 'Add estimated reading/completion time'
        }

        # Count how many valuable fields are present
        present_fields = sum(1 for field in valuable_fields if field in frontmatter and frontmatter[field])

        if present_fields < 3:
            issues.append(MetadataIssue(
                file_path=file_path,
                issue_type='poor_quality',
                severity='medium',
                message=f'Metadata lacks richness (only {present_fields} enrichment fields present)',
                suggestion='Add more metadata fields: ' + ', '.join(
                    field for field in valuable_fields if field not in frontmatter
                )[:3]  # Suggest top 3 missing fields
            ))

        # Check content_type if present
        if 'content_type' in frontmatter:
            content_type = str(frontmatter['content_type']).lower()
            if content_type not in self.valid_content_types:
                issues.append(MetadataIssue(
                    file_path=file_path,
                    issue_type='categorization',
                    severity='medium',
                    message=f'Invalid content_type "{content_type}"',
                    field='content_type',
                    current_value=content_type,
                    suggestion=f'Use one of: {", ".join(sorted(self.valid_content_types))}'
                ))

        # Check audience_level if present
        if 'audience_level' in frontmatter:
            audience_level = str(frontmatter['audience_level']).lower()
            if audience_level not in self.valid_audience_levels:
                issues.append(MetadataIssue(
                    file_path=file_path,
                    issue_type='categorization',
                    severity='low',
                    message=f'Invalid audience_level "{audience_level}"',
                    field='audience_level',
                    current_value=audience_level,
                    suggestion=f'Use one of: {", ".join(sorted(self.valid_audience_levels))}'
                ))

        return issues

    def check_description_quality(self, description: str, title: str, file_path: str) -> List[MetadataIssue]:
        """
        Check the quality of the description field.

        Args:
            description: The description text
            title: The title for comparison
            file_path: Path to the file

        Returns:
            List of description quality issues
        """
        issues = []

        # Check length
        desc_length = len(description)
        if desc_length < self.min_description_length:
            issues.append(MetadataIssue(
                file_path=file_path,
                issue_type='poor_quality',
                severity='high',
                message=f'Description too short ({desc_length} chars, minimum {self.min_description_length})',
                field='description',
                current_value=description,
                suggestion='Expand description to provide more context about the content'
            ))
        elif desc_length > self.max_description_length:
            issues.append(MetadataIssue(
                file_path=file_path,
                issue_type='poor_quality',
                severity='medium',
                message=f'Description too long ({desc_length} chars, maximum {self.max_description_length})',
                field='description',
                current_value=description,
                suggestion='Shorten description to improve readability in search results'
            ))

        # Check if description is just title repeated
        if title and description.lower().strip() == title.lower().strip():
            issues.append(MetadataIssue(
                file_path=file_path,
                issue_type='poor_quality',
                severity='high',
                message='Description identical to title',
                field='description',
                current_value=description,
                suggestion='Write a unique description that expands on the title'
            ))

        # Check if description starts with title (common issue)
        if title and description.lower().startswith(title.lower()):
            issues.append(MetadataIssue(
                file_path=file_path,
                issue_type='poor_quality',
                severity='medium',
                message='Description starts with title',
                field='description',
                current_value=description,
                suggestion='Rewrite description to provide additional context beyond the title'
            ))

        # Check for generic descriptions
        generic_patterns = [
            r'^This (page|document|section|article) (describes|explains|covers|discusses)',
            r'^(Learn|Read) about',
            r'^(Overview|Introduction|Guide) to',
            r'^Documentation for',
            r'^Information about'
        ]

        for pattern in generic_patterns:
            if re.match(pattern, description, re.IGNORECASE):
                issues.append(MetadataIssue(
                    file_path=file_path,
                    issue_type='poor_quality',
                    severity='medium',
                    message='Generic description pattern detected',
                    field='description',
                    current_value=description,
                    suggestion='Write a specific description that highlights unique value or key points'
                ))
                break

        return issues

    def check_semantic_keywords(self, content: str, frontmatter: Dict[str, Any], file_path: str) -> List[MetadataIssue]:
        """
        Validates keywords match content and aid discovery.

        Args:
            content: Document content
            frontmatter: Frontmatter with keywords/tags
            file_path: Path to file

        Returns:
            List of keyword-related issues
        """
        issues = []

        # Get keywords from frontmatter (could be 'keywords' or 'tags')
        keywords = frontmatter.get('keywords', frontmatter.get('tags', []))
        if isinstance(keywords, str):
            keywords = [k.strip() for k in keywords.split(',')]
        elif not isinstance(keywords, list):
            keywords = []

        if not keywords:
            return issues

        # Extract significant words from content
        content_lower = content.lower()
        # Simple word extraction (could be enhanced with NLP)
        words = re.findall(r'\b[a-z]+\b', content_lower)
        word_freq = Counter(words)

        # Remove stop words
        for word in self.stop_words:
            word_freq.pop(word, None)

        # Get top content words
        top_words = {word for word, _ in word_freq.most_common(50)}

        # Check each keyword
        missing_keywords = []
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Check if keyword appears in content
            if keyword_lower not in content_lower:
                # Check if any word from keyword phrase appears
                keyword_words = keyword_lower.split()
                if not any(word in top_words for word in keyword_words if word not in self.stop_words):
                    missing_keywords.append(keyword)

        if missing_keywords:
            issues.append(MetadataIssue(
                file_path=file_path,
                issue_type='keyword_mismatch',
                severity='medium',
                message=f'Keywords not found in content: {", ".join(missing_keywords[:3])}',
                field='keywords',
                current_value=keywords,
                suggestion='Use keywords that actually appear in the content'
            ))

        # Check for important technical terms not in keywords
        # Look for capitalized terms, acronyms, or technical-looking words in content
        tech_pattern = re.compile(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+|[A-Z]{2,})\b')
        technical_terms = set()
        for match in tech_pattern.finditer(content):
            term = match.group(1)
            # Skip common terms
            if term not in ['API', 'URL', 'JSON', 'HTML', 'CSS', 'HTTP', 'HTTPS', 'The', 'This', 'That']:
                technical_terms.add(term.lower())

        # Check if important technical terms are in keywords
        keywords_lower = [k.lower() for k in keywords]
        missing_tech_terms = technical_terms - set(keywords_lower)

        if len(missing_tech_terms) > 2:
            suggested_terms = list(missing_tech_terms)[:3]
            issues.append(MetadataIssue(
                file_path=file_path,
                issue_type='keyword_mismatch',
                severity='low',
                message='Important technical terms missing from keywords',
                field='keywords',
                suggestion=f'Consider adding: {", ".join(suggested_terms)}'
            ))

        return issues

    def check_content_categorization(self, frontmatter: Dict[str, Any], content: str, file_path: str) -> List[MetadataIssue]:
        """
        Check if content is properly categorized for AI understanding.

        Args:
            frontmatter: Frontmatter dictionary
            content: Document content
            file_path: Path to file

        Returns:
            List of categorization issues
        """
        issues = []

        # If content_type is not specified, try to detect it
        if 'content_type' not in frontmatter:
            detected_type = self._detect_content_type(content, frontmatter.get('title', ''))
            if detected_type:
                issues.append(MetadataIssue(
                    file_path=file_path,
                    issue_type='categorization',
                    severity='medium',
                    message='Content type not specified',
                    field='content_type',
                    suggestion=f'Based on content analysis, consider adding: content_type: {detected_type}'
                ))

        # Check for category/section metadata
        if 'category' not in frontmatter and 'section' not in frontmatter:
            issues.append(MetadataIssue(
                file_path=file_path,
                issue_type='categorization',
                severity='low',
                message='No category or section specified',
                suggestion='Add category or section field to group related content'
            ))

        return issues

    def check_related_topics(self, frontmatter: Dict[str, Any], file_path: str) -> List[MetadataIssue]:
        """
        Check if related topics are specified for better AI navigation.

        Args:
            frontmatter: Frontmatter dictionary
            file_path: Path to file

        Returns:
            List of related topic issues
        """
        issues = []

        # Check for related content fields
        related_fields = ['related', 'related_topics', 'see_also', 'related_pages']
        has_related = any(field in frontmatter for field in related_fields)

        if not has_related:
            issues.append(MetadataIssue(
                file_path=file_path,
                issue_type='missing_metadata',
                severity='low',
                message='No related topics specified',
                suggestion='Add related topics to help AI understand content relationships'
            ))

        return issues

    def _get_field_suggestion(self, field: str) -> str:
        """
        Get a helpful suggestion for a missing field.

        Args:
            field: The field name

        Returns:
            Suggestion text
        """
        suggestions = {
            'title': 'Add a clear, descriptive title',
            'description': 'Add a 50-160 character description summarizing the content',
            'keywords': 'Add comma-separated keywords that appear in the content',
            'content_type': 'Specify type: guide, tutorial, reference, or concept',
            'audience_level': 'Specify level: beginner, intermediate, or advanced',
            'tags': 'Add tags for categorization',
            'related': 'List related documentation pages'
        }
        return suggestions.get(field, f'Add {field} field to frontmatter')

    def _detect_content_type(self, content: str, title: str) -> Optional[str]:
        """
        Try to detect content type based on content patterns.

        Args:
            content: Document content
            title: Document title

        Returns:
            Detected content type or None
        """
        content_lower = content.lower()
        title_lower = title.lower()

        # Check for patterns indicating content type
        if any(word in title_lower for word in ['guide', 'how to', 'getting started', 'quickstart']):
            return 'guide'
        elif any(word in title_lower for word in ['tutorial', 'walkthrough', 'step by step']):
            return 'tutorial'
        elif any(word in title_lower for word in ['reference', 'api', 'methods', 'properties']):
            return 'reference'
        elif any(word in title_lower for word in ['concept', 'overview', 'introduction', 'understanding']):
            return 'concept'
        elif 'troubleshoot' in content_lower or 'problem' in title_lower or 'issue' in title_lower:
            return 'troubleshooting'
        elif '## prerequisites' in content_lower or '## requirements' in content_lower:
            return 'guide'
        elif '## example' in content_lower or '## code' in content_lower:
            return 'example'
        elif any(pattern in content_lower for pattern in ['frequently asked', 'faq', 'question']):
            return 'faq'

        # Check for numbered steps indicating tutorial
        if re.search(r'\n\d+\.\s+', content):
            return 'tutorial'

        return None

    def suggest_keywords(self, content: str, existing_keywords: List[str] = None) -> List[str]:
        """
        Suggest keywords based on content analysis.

        Args:
            content: Document content
            existing_keywords: Already present keywords to avoid

        Returns:
            List of suggested keywords
        """
        existing_keywords = existing_keywords or []
        existing_lower = [k.lower() for k in existing_keywords]

        # Extract words
        words = re.findall(r'\b[a-z]+\b', content.lower())
        word_freq = Counter(words)

        # Remove stop words
        for word in self.stop_words:
            word_freq.pop(word, None)

        # Extract technical terms
        tech_pattern = re.compile(r'\b([A-Z][a-z]+(?:[A-Z][a-z]+)+|[A-Z]{2,})\b')
        technical_terms = []
        for match in tech_pattern.finditer(content):
            term = match.group(1)
            if term not in ['API', 'URL', 'JSON', 'HTML', 'CSS', 'HTTP', 'HTTPS']:
                technical_terms.append(term)

        # Get top words that aren't already keywords
        suggestions = []
        for word, freq in word_freq.most_common(20):
            if word not in existing_lower and len(word) > 3 and freq > 2:
                suggestions.append(word)
                if len(suggestions) >= 5:
                    break

        # Add technical terms
        for term in technical_terms[:3]:
            if term.lower() not in existing_lower:
                suggestions.append(term)

        return suggestions[:8]  # Return top 8 suggestions