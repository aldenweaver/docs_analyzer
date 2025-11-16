"""
AI Searchability Analyzer - Ensures documentation is optimized for AI search and RAG systems.

This module validates that documentation works well with AI-powered search systems like Inkeep,
ensuring content is properly structured for semantic chunking, accurate citation, and
standalone comprehension.
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class AISearchabilityIssue:
    """Represents an issue affecting AI searchability."""
    file_path: str
    issue_type: str  # 'semantic_chunking', 'citation_readiness', 'standalone_comprehension', 'qa_format'
    severity: str    # 'critical', 'high', 'medium', 'low'
    message: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    context: Optional[str] = None


class AISearchabilityAnalyzer:
    """
    Ensures documentation is optimized for AI search and RAG (Retrieval-Augmented Generation) systems.

    This analyzer checks that documentation:
    1. Is ready for semantic chunking
    2. Can be cited accurately
    3. Has standalone comprehension for each section
    4. Uses formats that AI can parse effectively
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the AI Searchability Analyzer.

        Args:
            config: Configuration dictionary with AI search optimization settings
        """
        self.config = config or {}
        self.ai_config = self.config.get('ai_search_optimization', {})
        self.semantic_config = self.ai_config.get('semantic_chunking', {})
        self.citation_config = self.ai_config.get('citation_readiness', {})
        self.conversational_config = self.ai_config.get('conversational', {})
        self.atomicity_config = self.ai_config.get('atomicity', {})

        # Common generic headings that are not descriptive
        self.generic_headings = {
            'overview', 'introduction', 'details', 'example', 'examples',
            'description', 'summary', 'conclusion', 'notes', 'note',
            'info', 'information', 'more info', 'additional info',
            'other', 'misc', 'miscellaneous', 'various', 'general'
        }

        # Orphaned reference patterns
        self.orphaned_patterns = [
            r'\b(as mentioned above|as mentioned below|as stated earlier|as discussed)\b',
            r'\b(the above|the below|the following|the previous)\b(?!\s+\w+)',
            r'^(This|That|These|Those)\s+(?!is|are|was|were)',
            r'\b(see above|see below)\b(?!\s+for)',
            r'\b(aforementioned|above-mentioned|previously mentioned)\b'
        ]

        # Undefined pronoun patterns at section starts
        self.undefined_pronoun_patterns = [
            r'^(It|They|This|That|These|Those)\s+',
            r'^(He|She|We|You)\s+'
        ]

    def analyze(self, content: str, file_path: str, frontmatter: Optional[Dict[str, Any]] = None) -> List[AISearchabilityIssue]:
        """
        Analyze content for AI searchability issues.

        Args:
            content: The document content to analyze
            file_path: Path to the file being analyzed
            frontmatter: Optional frontmatter metadata

        Returns:
            List of AI searchability issues found
        """
        issues = []

        # Check semantic chunking readiness
        if self.semantic_config.get('enabled', True):
            issues.extend(self.check_semantic_chunking_readiness(content, file_path))

        # Check citation readiness
        if self.citation_config.get('enabled', True):
            issues.extend(self.check_citation_readiness(content, file_path))

        # Check standalone comprehension
        if self.semantic_config.get('check_standalone_comprehension', True):
            issues.extend(self.check_standalone_comprehension(content, file_path))

        # Check question-answer format opportunities
        if self.ai_config.get('check_qa_opportunities', True):
            issues.extend(self.check_question_answer_format(content, file_path))

        # Check conversational tone if enabled
        if self.conversational_config.get('enabled', False):
            issues.extend(self.check_conversational_readiness(content, file_path))

        return issues

    def check_semantic_chunking_readiness(self, content: str, file_path: str) -> List[AISearchabilityIssue]:
        """
        Validates that content is optimized for semantic chunking by AI systems.

        Checks:
        - Each section has clear topic sentences
        - Headings are descriptive (not just "Overview" or "Details")
        - Context is self-contained (no orphaned references)
        - Paragraphs have logical boundaries
        - Code examples have explanatory text
        """
        issues = []
        lines = content.split('\n')

        # Check for non-descriptive headings
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
        for i, line in enumerate(lines, 1):
            match = heading_pattern.match(line)
            if match:
                heading_text = match.group(2).strip()
                heading_lower = heading_text.lower().strip('#').strip()

                if heading_lower in self.generic_headings:
                    issues.append(AISearchabilityIssue(
                        file_path=file_path,
                        issue_type='semantic_chunking',
                        severity='high',
                        message=f'Non-descriptive heading "{heading_text}" reduces AI search effectiveness',
                        line_number=i,
                        suggestion=f'Replace with a descriptive heading that explains the content, e.g., "How to Configure API Authentication" instead of "Configuration"',
                        context=line
                    ))

        # Check for orphaned references
        for pattern in self.orphaned_patterns:
            regex = re.compile(pattern, re.IGNORECASE)
            for i, line in enumerate(lines, 1):
                if regex.search(line):
                    issues.append(AISearchabilityIssue(
                        file_path=file_path,
                        issue_type='semantic_chunking',
                        severity='critical',
                        message=f'Orphaned reference found that AI cannot resolve when content is chunked',
                        line_number=i,
                        suggestion='Replace with explicit reference or include full context in the same section',
                        context=line.strip()
                    ))

        # Check for code blocks without explanatory text
        in_code_block = False
        code_block_start = 0
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_start = i
                    # Check if there's explanatory text before the code block
                    if i > 1:
                        prev_line = lines[i-2].strip()
                        if prev_line == '' or prev_line.startswith('#'):
                            issues.append(AISearchabilityIssue(
                                file_path=file_path,
                                issue_type='semantic_chunking',
                                severity='medium',
                                message='Code block lacks explanatory context',
                                line_number=i,
                                suggestion='Add a sentence before the code block explaining what it demonstrates',
                                context=f'Line {i}: {line[:50]}...'
                            ))
                else:
                    in_code_block = False

        # Check for very long sections without subheadings
        section_lines = []
        current_section_start = 1
        for i, line in enumerate(lines, 1):
            if heading_pattern.match(line):
                if len(section_lines) > 50:  # More than 50 lines without subheading
                    issues.append(AISearchabilityIssue(
                        file_path=file_path,
                        issue_type='semantic_chunking',
                        severity='medium',
                        message=f'Section too long ({len(section_lines)} lines) for optimal semantic chunking',
                        line_number=current_section_start,
                        suggestion='Break into smaller sections with descriptive subheadings',
                        context=f'Section starting at line {current_section_start}'
                    ))
                section_lines = []
                current_section_start = i
            else:
                section_lines.append(line)

        return issues

    def check_citation_readiness(self, content: str, file_path: str) -> List[AISearchabilityIssue]:
        """
        Ensures AI can cite content accurately.

        Checks:
        - Headings are unique and descriptive
        - Important points are in their own paragraphs
        - Lists have context sentences
        - Examples are clearly labeled
        """
        issues = []
        lines = content.split('\n')

        # Check for duplicate headings
        headings = {}
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
        for i, line in enumerate(lines, 1):
            match = heading_pattern.match(line)
            if match:
                heading_text = match.group(2).strip()
                heading_key = heading_text.lower()
                if heading_key in headings:
                    issues.append(AISearchabilityIssue(
                        file_path=file_path,
                        issue_type='citation_readiness',
                        severity='high',
                        message=f'Duplicate heading "{heading_text}" makes accurate citation difficult',
                        line_number=i,
                        suggestion='Make each heading unique and descriptive',
                        context=f'Also appears on line {headings[heading_key]}'
                    ))
                else:
                    headings[heading_key] = i

        # Check for lists without context
        list_pattern = re.compile(r'^[\*\-\+]\s+.+$')
        for i, line in enumerate(lines, 1):
            if list_pattern.match(line):
                # Check if previous line provides context
                if i > 1:
                    prev_line = lines[i-2].strip()
                    if prev_line == '' or prev_line.startswith('#') or list_pattern.match(prev_line):
                        issues.append(AISearchabilityIssue(
                            file_path=file_path,
                            issue_type='citation_readiness',
                            severity='medium',
                            message='List lacks introductory context',
                            line_number=i,
                            suggestion='Add a sentence before the list explaining what it contains',
                            context=line[:50]
                        ))
                        break  # Only flag once per list

        # Check for buried important information in long paragraphs
        current_paragraph = []
        paragraph_start = 1
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped == '':
                if len(' '.join(current_paragraph).split()) > 150:  # Long paragraph
                    # Check for important keywords buried in the middle
                    important_keywords = ['must', 'required', 'critical', 'important', 'warning', 'caution', 'note']
                    paragraph_text = ' '.join(current_paragraph).lower()
                    for keyword in important_keywords:
                        if keyword in paragraph_text:
                            issues.append(AISearchabilityIssue(
                                file_path=file_path,
                                issue_type='citation_readiness',
                                severity='high',
                                message=f'Important information with "{keyword}" buried in long paragraph',
                                line_number=paragraph_start,
                                suggestion='Break out important points into separate paragraphs or callout boxes',
                                context=f'Paragraph at line {paragraph_start} ({len(" ".join(current_paragraph).split())} words)'
                            ))
                            break
                current_paragraph = []
                paragraph_start = i + 1
            else:
                current_paragraph.append(stripped)

        return issues

    def check_standalone_comprehension(self, content: str, file_path: str) -> List[AISearchabilityIssue]:
        """
        Validates that each section can be understood independently.

        Checks:
        - No dangling pronouns without antecedents
        - Technical terms defined on first use
        - Context provided for code snippets
        - Links have descriptive text
        """
        issues = []
        lines = content.split('\n')

        # Track technical terms that need definition
        technical_terms = set()
        defined_terms = set()

        # Check sections for standalone comprehension
        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')
        current_section = []
        section_start = 1

        for i, line in enumerate(lines, 1):
            if heading_pattern.match(line) and current_section:
                # Analyze the completed section
                section_text = '\n'.join(current_section)

                # Check for undefined pronouns at section start
                if current_section:
                    first_content_line = next((l for l in current_section if l.strip()), '')
                    for pattern in self.undefined_pronoun_patterns:
                        if re.match(pattern, first_content_line.strip()):
                            issues.append(AISearchabilityIssue(
                                file_path=file_path,
                                issue_type='standalone_comprehension',
                                severity='critical',
                                message='Section starts with undefined pronoun',
                                line_number=section_start,
                                suggestion='Replace pronoun with specific noun or add context',
                                context=first_content_line[:100]
                            ))

                # Reset for new section
                current_section = []
                section_start = i
            else:
                current_section.append(line)

                # Check for non-descriptive link text
                link_pattern = re.compile(r'\[([^\]]+)\]\([^\)]+\)')
                for match in link_pattern.finditer(line):
                    link_text = match.group(1).lower()
                    if link_text in ['here', 'click here', 'this', 'link', 'more', 'read more']:
                        issues.append(AISearchabilityIssue(
                            file_path=file_path,
                            issue_type='standalone_comprehension',
                            severity='high',
                            message=f'Non-descriptive link text "{match.group(1)}"',
                            line_number=i,
                            suggestion='Use descriptive link text that explains the destination',
                            context=line[:100]
                        ))

                # Check for undefined technical terms (simplified check)
                # Look for capitalized terms, acronyms, or technical-looking words
                tech_pattern = re.compile(r'\b([A-Z]{2,}|[A-Z][a-z]+(?:[A-Z][a-z]+)+)\b')
                for match in tech_pattern.finditer(line):
                    term = match.group(1)
                    if term not in defined_terms and term not in ['API', 'URL', 'JSON', 'HTML', 'CSS', 'HTTP', 'HTTPS']:
                        technical_terms.add(term)

                # Check if terms are being defined
                if 'is' in line or 'are' in line or 'means' in line or '(' in line:
                    for term in technical_terms.copy():
                        if term in line:
                            defined_terms.add(term)
                            technical_terms.remove(term)

        # Report undefined technical terms
        for term in technical_terms:
            issues.append(AISearchabilityIssue(
                file_path=file_path,
                issue_type='standalone_comprehension',
                severity='medium',
                message=f'Technical term "{term}" used but not defined',
                line_number=None,
                suggestion='Define technical terms on first use in each major section',
                context=term
            ))

        return issues

    def check_question_answer_format(self, content: str, file_path: str) -> List[AISearchabilityIssue]:
        """
        Identifies content that could be reformatted as Q&A for better AI comprehension.

        Checks:
        - Implicit questions that could be explicit
        - Troubleshooting sections not in Q&A format
        - How-to content that could be question-based
        """
        issues = []
        lines = content.split('\n')

        # Look for implicit questions
        implicit_question_patterns = [
            r'^(How to|How do I|How can I)\s+',
            r'^(When to|When should I|When do I)\s+',
            r'^(Why does|Why is|Why should)\s+',
            r'^(What is|What are|What does)\s+',
            r'^(Where to|Where do|Where should)\s+',
            r'^(Should I|Can I|Do I need to)\s+',
        ]

        heading_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

        for i, line in enumerate(lines, 1):
            # Check if headings could be questions
            match = heading_pattern.match(line)
            if match:
                heading_text = match.group(2)
                for pattern in implicit_question_patterns:
                    if re.match(pattern, heading_text, re.IGNORECASE):
                        if not heading_text.endswith('?'):
                            issues.append(AISearchabilityIssue(
                                file_path=file_path,
                                issue_type='qa_format',
                                severity='low',
                                message='Heading could be formatted as a question',
                                line_number=i,
                                suggestion=f'Consider: "{heading_text}?"',
                                context=line
                            ))

            # Check for troubleshooting content not in Q&A format
            if 'troubleshoot' in line.lower() or 'problem' in line.lower() or 'issue' in line.lower():
                # Check if it's already in Q&A format
                if not any(q in line for q in ['?', 'Q:', 'A:', 'Question:', 'Answer:']):
                    issues.append(AISearchabilityIssue(
                        file_path=file_path,
                        issue_type='qa_format',
                        severity='medium',
                        message='Troubleshooting content could benefit from Q&A format',
                        line_number=i,
                        suggestion='Format as "Q: What if X happens? A: Do Y"',
                        context=line[:100]
                    ))
                    break  # Only flag once per file

        # Check for FAQ-like content
        faq_keywords = ['frequently asked', 'common question', 'often ask', 'faq']
        content_lower = content.lower()
        for keyword in faq_keywords:
            if keyword in content_lower and '?' not in content:
                issues.append(AISearchabilityIssue(
                    file_path=file_path,
                    issue_type='qa_format',
                    severity='medium',
                    message='FAQ section without question format',
                    line_number=None,
                    suggestion='Format FAQ sections with explicit questions',
                    context='FAQ content detected'
                ))
                break

        return issues

    def check_conversational_readiness(self, content: str, file_path: str) -> List[AISearchabilityIssue]:
        """
        Ensures documentation reads naturally for AI voice interfaces.

        Checks:
        - Answer directness (key info first)
        - Natural language patterns
        - Abbreviation handling
        """
        issues = []
        lines = content.split('\n')

        # Check for parenthetical asides that are hard for voice
        parenthetical_pattern = re.compile(r'\([^)]{50,}\)')  # Long parentheticals
        for i, line in enumerate(lines, 1):
            matches = parenthetical_pattern.findall(line)
            for match in matches:
                issues.append(AISearchabilityIssue(
                    file_path=file_path,
                    issue_type='conversational',
                    severity='low',
                    message='Long parenthetical aside difficult for voice interfaces',
                    line_number=i,
                    suggestion='Move parenthetical content to a separate sentence',
                    context=match[:50] + '...)'
                ))

        # Check for unexpanded abbreviations
        abbrev_pattern = re.compile(r'\b([A-Z]{2,})\b')
        expanded = set()
        for i, line in enumerate(lines, 1):
            for match in abbrev_pattern.finditer(line):
                abbrev = match.group(1)
                # Skip common abbreviations
                if abbrev not in ['AI', 'API', 'URL', 'JSON', 'HTML', 'CSS', 'HTTP', 'HTTPS', 'FAQ', 'UI', 'UX']:
                    if abbrev not in expanded:
                        # Check if it's expanded in the same line
                        if f'{abbrev} (' not in line and f'({abbrev})' not in line:
                            issues.append(AISearchabilityIssue(
                                file_path=file_path,
                                issue_type='conversational',
                                severity='low',
                                message=f'Abbreviation "{abbrev}" not expanded on first use',
                                line_number=i,
                                suggestion='Expand abbreviations on first use',
                                context=line[:100]
                            ))
                            expanded.add(abbrev)

        return issues

    def calculate_ai_searchability_score(self, issues: List[AISearchabilityIssue]) -> float:
        """
        Calculate an overall AI searchability score (0-100).

        Args:
            issues: List of issues found

        Returns:
            Score from 0-100 indicating AI searchability readiness
        """
        if not issues:
            return 100.0

        # Weight issues by severity
        severity_weights = {
            'critical': 10,
            'high': 5,
            'medium': 2,
            'low': 1
        }

        total_weight = sum(severity_weights.get(issue.severity, 1) for issue in issues)

        # Deduct points based on weighted issues
        # Start at 100 and deduct up to 100 points based on issues
        max_deduction = 100
        deduction_per_weight = min(2, max_deduction / max(total_weight, 1))

        score = max(0, 100 - (total_weight * deduction_per_weight))

        return round(score, 1)