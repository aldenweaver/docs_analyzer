"""
Heading Descriptiveness Fixer - Makes headings more descriptive for AI understanding.

This fixer identifies generic headings and replaces them with more descriptive ones
that help AI systems better understand and cite content.
"""

import re
from typing import List, Dict, Optional, Tuple
from core.models import Issue, FixResult
from core.config import Config
from fixers.base import BaseFixer


class HeadingDescriptivenessFixer(BaseFixer):
    """Make headings more descriptive for AI understanding and searchability"""

    def __init__(self, config: Config):
        super().__init__(config)

        # Generic headings that need improvement
        self.generic_headings = {
            'overview', 'introduction', 'details', 'example', 'examples',
            'description', 'summary', 'conclusion', 'notes', 'note',
            'info', 'information', 'more info', 'additional info',
            'other', 'misc', 'miscellaneous', 'various', 'general',
            'usage', 'setup', 'configuration', 'options', 'parameters'
        }

        # Context-based heading improvements
        self.heading_improvements = {
            # API documentation patterns
            'example': 'Code Example: {context}',
            'examples': 'Usage Examples for {context}',
            'overview': 'How {context} Works',
            'introduction': 'Getting Started with {context}',
            'setup': 'Setting Up {context}',
            'configuration': 'Configuring {context}',
            'parameters': '{context} Parameters and Options',
            'options': 'Available Options for {context}',

            # Guide patterns
            'details': 'Understanding {context} in Detail',
            'information': 'Key Information About {context}',
            'notes': 'Important Notes About {context}',
            'summary': 'Summary of {context}',

            # Troubleshooting patterns
            'troubleshooting': 'Troubleshooting {context} Issues',
            'errors': 'Common {context} Errors and Solutions',
            'debugging': 'Debugging {context}',

            # Generic improvements
            'usage': 'How to Use {context}',
            'description': 'What is {context}',
            'conclusion': 'Next Steps After {context}',
        }

    @property
    def name(self) -> str:
        return "HeadingDescriptivenessFixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check file for non-descriptive headings"""
        issues = []
        lines = content.split('\n')

        # Track document context
        document_title = self._extract_document_title(lines)
        current_section = None
        heading_stack = []  # Track heading hierarchy

        # Skip frontmatter
        in_frontmatter = False

        for line_num, line in enumerate(lines, 1):
            # Track frontmatter
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue

            if in_frontmatter:
                continue

            # Check if line is a heading
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if heading_match:
                level = len(heading_match.group(1))
                heading_text = heading_match.group(2).strip()
                heading_lower = heading_text.lower().strip('#').strip()

                # Update heading stack
                while len(heading_stack) >= level:
                    heading_stack.pop()
                heading_stack.append(heading_text)

                # Check if heading is generic
                if heading_lower in self.generic_headings:
                    # Get context from parent headings or document title
                    context = self._determine_context(
                        heading_stack, document_title, lines, line_num
                    )

                    # Generate improved heading
                    improved_heading = self._generate_improved_heading(
                        heading_lower, heading_text, context
                    )

                    issues.append(Issue(
                        severity="high" if level <= 2 else "medium",
                        category="ai_search",
                        file_path=file_path,
                        line_number=line_num,
                        issue_type="non_descriptive_heading",
                        description=f"Non-descriptive heading '{heading_text}' reduces AI search effectiveness",
                        suggestion=f"Replace with more descriptive: '{improved_heading}'",
                        context=line.strip(),
                        auto_fixable=True
                    ))

                # Check for question opportunities (headings that could be questions)
                if self._could_be_question(heading_text):
                    question_form = self._convert_to_question(heading_text)
                    if question_form and question_form != heading_text:
                        issues.append(Issue(
                            severity="low",
                            category="ai_search",
                            file_path=file_path,
                            line_number=line_num,
                            issue_type="heading_could_be_question",
                            description=f"Heading could be formatted as a question for better AI comprehension",
                            suggestion=f"Consider: '{question_form}'",
                            context=line.strip(),
                            auto_fixable=True
                        ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Apply heading improvements"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        # Sort issues by line number in reverse to fix from bottom to top
        # This prevents line number shifts
        sorted_issues = sorted(
            [i for i in issues if i.auto_fixable],
            key=lambda x: x.line_number,
            reverse=True
        )

        lines = fixed_content.split('\n')

        for issue in sorted_issues:
            if issue.issue_type == "non_descriptive_heading":
                # Extract the improved heading from suggestion
                match = re.search(r"Replace with more descriptive: '(.+)'", issue.suggestion)
                if match:
                    improved_heading = match.group(1)
                    line_idx = issue.line_number - 1

                    if 0 <= line_idx < len(lines):
                        original_line = lines[line_idx]
                        # Preserve the heading level
                        heading_match = re.match(r'^(#{1,6})\s+(.+)$', original_line)
                        if heading_match:
                            heading_level = heading_match.group(1)
                            new_line = f"{heading_level} {improved_heading}"

                            lines[line_idx] = new_line

                            fixes_applied.append({
                                'line': issue.line_number,
                                'original': original_line.strip(),
                                'fixed': new_line.strip(),
                                'type': 'non_descriptive_heading'
                            })
                            issues_fixed.append(issue)

            elif issue.issue_type == "heading_could_be_question":
                # Extract the question form from suggestion
                match = re.search(r"Consider: '(.+)'", issue.suggestion)
                if match:
                    question_form = match.group(1)
                    line_idx = issue.line_number - 1

                    if 0 <= line_idx < len(lines):
                        original_line = lines[line_idx]
                        # Preserve the heading level
                        heading_match = re.match(r'^(#{1,6})\s+(.+)$', original_line)
                        if heading_match:
                            heading_level = heading_match.group(1)
                            new_line = f"{heading_level} {question_form}"

                            lines[line_idx] = new_line

                            fixes_applied.append({
                                'line': issue.line_number,
                                'original': original_line.strip(),
                                'fixed': new_line.strip(),
                                'type': 'heading_could_be_question'
                            })
                            issues_fixed.append(issue)

        fixed_content = '\n'.join(lines)

        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=fixed_content,
            fixes_applied=fixes_applied,
            issues_fixed=issues_fixed,
            content_changed=fixed_content != content
        )

    def _extract_document_title(self, lines: List[str]) -> Optional[str]:
        """Extract document title from frontmatter or first heading"""
        in_frontmatter = False
        title = None

        for line in lines:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                if not in_frontmatter and title:
                    return title
                continue

            if in_frontmatter:
                # Look for title in frontmatter
                if line.startswith('title:'):
                    title = line.replace('title:', '').strip().strip('"').strip("'")
                    return title
            else:
                # Look for first heading
                heading_match = re.match(r'^#\s+(.+)$', line)
                if heading_match:
                    return heading_match.group(1).strip()

        return None

    def _determine_context(self, heading_stack: List[str], document_title: Optional[str],
                          lines: List[str], current_line: int) -> str:
        """Determine context for improving a generic heading"""
        # Try parent heading
        if len(heading_stack) > 1:
            parent_heading = heading_stack[-2]
            # Clean up the parent heading
            context = re.sub(r'^(How to|Getting Started with|Understanding)\s+', '', parent_heading)
            return context

        # Try document title
        if document_title:
            return document_title

        # Try to extract context from surrounding content
        # Look at the next few lines for context clues
        for i in range(current_line, min(current_line + 5, len(lines))):
            line = lines[i].strip()
            # Look for technical terms or product names
            tech_terms = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b', line)
            if tech_terms:
                return tech_terms[0]

        # Default context
        return "This Section"

    def _generate_improved_heading(self, heading_lower: str, original_heading: str,
                                  context: str) -> str:
        """Generate an improved, more descriptive heading"""
        # Check if we have a template for this heading type
        if heading_lower in self.heading_improvements:
            template = self.heading_improvements[heading_lower]
            # Replace {context} with actual context
            improved = template.format(context=context)
            return improved

        # Default improvements for common patterns
        if heading_lower == 'example':
            return f"{context} Example"
        elif heading_lower == 'examples':
            return f"{context} Examples"
        elif heading_lower == 'overview':
            return f"{context} Overview"
        elif heading_lower == 'introduction':
            return f"Introduction to {context}"
        elif heading_lower == 'details':
            return f"{context} Details"
        elif heading_lower == 'configuration':
            return f"Configuring {context}"
        elif heading_lower == 'setup':
            return f"Setting Up {context}"
        elif heading_lower == 'usage':
            return f"Using {context}"
        elif heading_lower == 'notes':
            return f"Notes on {context}"

        # Fallback: just add context
        return f"{original_heading}: {context}"

    def _could_be_question(self, heading_text: str) -> bool:
        """Check if a heading could be reformatted as a question"""
        question_patterns = [
            r'^(How to|How do I|How can I)\s+',
            r'^(When to|When should I|When do I)\s+',
            r'^(Why does|Why is|Why should)\s+',
            r'^(What is|What are|What does)\s+',
            r'^(Where to|Where do|Where should)\s+',
            r'^(Should I|Can I|Do I need to)\s+',
        ]

        heading_lower = heading_text.lower()
        for pattern in question_patterns:
            if re.match(pattern, heading_lower):
                return not heading_text.endswith('?')

        return False

    def _convert_to_question(self, heading_text: str) -> Optional[str]:
        """Convert a heading to question format"""
        if heading_text.endswith('?'):
            return None

        # Simple conversion: add question mark
        heading_lower = heading_text.lower()

        # Check for patterns that indicate questions
        if any(heading_lower.startswith(q) for q in [
            'how to', 'how do', 'when to', 'when should',
            'why does', 'why is', 'what is', 'what are',
            'where to', 'where do', 'should i', 'can i'
        ]):
            return heading_text + '?'

        return None