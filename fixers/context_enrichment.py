"""
Context Enrichment Fixer - Adds context to orphaned references and code examples.

This fixer identifies content that lacks sufficient context for AI systems to understand
when chunked or cited independently, and suggests or adds contextual improvements.
"""

import re
from typing import List, Dict, Optional, Tuple, Set
from core.models import Issue, FixResult
from core.config import Config
from fixers.base import BaseFixer


class ContextEnrichmentFixer(BaseFixer):
    """Add context to orphaned references and improve standalone comprehension"""

    def __init__(self, config: Config):
        super().__init__(config)

        # Orphaned reference patterns that need context
        self.orphaned_patterns = [
            (r'\b(as mentioned above|as mentioned below)\b', 'as described in the previous/following section'),
            (r'\b(as stated earlier|as discussed earlier)\b', 'as explained previously'),
            (r'\b(the above|the below)\b(?!\s+\w+)', 'the content shown above/below'),
            (r'^(This|That|These|Those)\s+', 'The {subject} '),
            (r'\b(see above|see below)\b(?!\s+for)', 'refer to the section above/below'),
            (r'\b(aforementioned|above-mentioned)\b', 'previously described'),
            (r'\bthe previous\b(?!\s+\w+)', 'the previous section'),
            (r'\bthe following\b(?!\s+\w+)', 'the following section'),
        ]

        # Undefined pronoun patterns at section/paragraph starts
        self.undefined_pronouns = ['it', 'they', 'this', 'that', 'these', 'those']

        # Technical terms that commonly need definition
        self.common_tech_terms = {
            'API': 'Application Programming Interface',
            'SDK': 'Software Development Kit',
            'CLI': 'Command Line Interface',
            'GUI': 'Graphical User Interface',
            'REST': 'Representational State Transfer',
            'OAuth': 'Open Authorization',
            'JWT': 'JSON Web Token',
            'MFA': 'Multi-Factor Authentication',
            '2FA': 'Two-Factor Authentication',
            'SSO': 'Single Sign-On',
            'CORS': 'Cross-Origin Resource Sharing',
            'CDN': 'Content Delivery Network',
            'CI/CD': 'Continuous Integration/Continuous Deployment',
            'RBAC': 'Role-Based Access Control',
            'CRUD': 'Create, Read, Update, Delete',
            'SLA': 'Service Level Agreement',
            'TLS': 'Transport Layer Security',
            'SSL': 'Secure Sockets Layer',
            'DNS': 'Domain Name System',
            'VPN': 'Virtual Private Network',
        }

    @property
    def name(self) -> str:
        return "ContextEnrichmentFixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check file for context issues"""
        issues = []
        lines = content.split('\n')

        # Track section boundaries and code blocks
        in_frontmatter = False
        in_code_block = False
        section_start = None
        paragraph_start = None
        defined_terms = set()
        undefined_terms = set()

        for line_num, line in enumerate(lines, 1):
            # Track frontmatter
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue

            if in_frontmatter:
                continue

            # Track code blocks
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    # Check if code block has context
                    if line_num > 1:
                        prev_line = lines[line_num - 2].strip()
                        if prev_line == '' or prev_line.startswith('#'):
                            # Get code block language
                            lang_match = re.match(r'^```(\w+)', line)
                            lang = lang_match.group(1) if lang_match else 'code'

                            issues.append(Issue(
                                severity="medium",
                                category="ai_search",
                                file_path=file_path,
                                line_number=line_num,
                                issue_type="code_block_lacks_context",
                                description=f"Code block lacks explanatory context",
                                suggestion=f"Add a sentence before the code block explaining what this {lang} code demonstrates",
                                context=line[:50] + '...',
                                auto_fixable=False  # Requires understanding code purpose
                            ))
                else:
                    in_code_block = False
                continue

            if in_code_block:
                continue

            # Check for section starts (headings)
            if re.match(r'^#{1,6}\s+', line):
                section_start = line_num
                paragraph_start = None
                continue

            # Check for paragraph starts
            if line.strip() and (not paragraph_start or lines[line_num - 2].strip() == ''):
                paragraph_start = line_num

                # Check for undefined pronouns at paragraph start
                stripped = line.strip()
                for pronoun in self.undefined_pronouns:
                    pattern = f'^{pronoun}\\s+'
                    if re.match(pattern, stripped, re.IGNORECASE):
                        # Determine if this is a section or paragraph start
                        context_type = "section" if section_start == paragraph_start else "paragraph"

                        issues.append(Issue(
                            severity="critical" if context_type == "section" else "high",
                            category="ai_search",
                            file_path=file_path,
                            line_number=line_num,
                            issue_type="undefined_pronoun",
                            description=f"{context_type.capitalize()} starts with undefined pronoun '{pronoun}'",
                            suggestion=f"Replace '{pronoun}' with a specific noun or add context",
                            context=line[:100],
                            auto_fixable=False  # Requires understanding context
                        ))
                        break

            # Check for orphaned references
            for pattern, replacement in self.orphaned_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    issues.append(Issue(
                        severity="high",
                        category="ai_search",
                        file_path=file_path,
                        line_number=line_num,
                        issue_type="orphaned_reference",
                        description=f"Orphaned reference '{match.group()}' found",
                        suggestion=f"Replace with explicit reference or include full context",
                        context=line.strip(),
                        auto_fixable=True if replacement else False
                    ))

            # Check for undefined technical terms
            for term, definition in self.common_tech_terms.items():
                if term in line and term not in defined_terms:
                    # Check if it's being defined in this line
                    defining_patterns = [
                        f'{term} \\({definition}',
                        f'{term} \\(',
                        f'{term} (is|are|means)',
                        f'{definition} \\({term}\\)',
                    ]

                    is_defined = any(re.search(p, line, re.IGNORECASE) for p in defining_patterns)

                    if is_defined:
                        defined_terms.add(term)
                    elif term not in undefined_terms:
                        undefined_terms.add(term)
                        issues.append(Issue(
                            severity="low",
                            category="ai_search",
                            file_path=file_path,
                            line_number=line_num,
                            issue_type="undefined_technical_term",
                            description=f"Technical term '{term}' used without definition",
                            suggestion=f"Define '{term}' ({definition}) on first use",
                            context=line.strip(),
                            auto_fixable=True
                        ))

            # Check for lists without context
            if re.match(r'^[\*\-\+]\s+', line):
                if line_num > 1:
                    prev_line = lines[line_num - 2].strip()
                    if prev_line == '' or prev_line.startswith('#') or re.match(r'^[\*\-\+]\s+', prev_line):
                        issues.append(Issue(
                            severity="medium",
                            category="ai_search",
                            file_path=file_path,
                            line_number=line_num,
                            issue_type="list_lacks_context",
                            description="List lacks introductory context",
                            suggestion="Add a sentence before the list explaining what it contains",
                            context=line[:50],
                            auto_fixable=False  # Requires understanding list purpose
                        ))

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """Apply context enrichment fixes"""
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        # Only fix auto-fixable issues
        fixable_issues = [i for i in issues if i.auto_fixable]

        # Sort by line number in reverse to prevent line shifts
        sorted_issues = sorted(fixable_issues, key=lambda x: x.line_number, reverse=True)

        lines = fixed_content.split('\n')

        for issue in sorted_issues:
            line_idx = issue.line_number - 1
            if 0 <= line_idx < len(lines):
                original_line = lines[line_idx]

                if issue.issue_type == "orphaned_reference":
                    # Try to fix orphaned references with generic improvements
                    fixed_line = self._fix_orphaned_reference(original_line)

                    if fixed_line != original_line:
                        lines[line_idx] = fixed_line
                        fixes_applied.append({
                            'line': issue.line_number,
                            'original': original_line.strip(),
                            'fixed': fixed_line.strip(),
                            'type': 'orphaned_reference'
                        })
                        issues_fixed.append(issue)

                elif issue.issue_type == "undefined_technical_term":
                    # Add definition for technical terms
                    fixed_line = self._add_term_definition(original_line, issue)

                    if fixed_line != original_line:
                        lines[line_idx] = fixed_line
                        fixes_applied.append({
                            'line': issue.line_number,
                            'original': original_line.strip(),
                            'fixed': fixed_line.strip(),
                            'type': 'undefined_technical_term'
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

    def _fix_orphaned_reference(self, line: str) -> str:
        """Fix orphaned references with more explicit text"""
        fixed_line = line

        # Apply replacements for known patterns
        replacements = [
            (r'\bas mentioned above\b', 'as described in the previous section'),
            (r'\bas mentioned below\b', 'as described in the following section'),
            (r'\bas stated earlier\b', 'as explained previously in this document'),
            (r'\bas discussed earlier\b', 'as covered in the previous section'),
            (r'\bthe above\b(?!\s+\w+)', 'the content shown above'),
            (r'\bthe below\b(?!\s+\w+)', 'the content shown below'),
            (r'\bsee above\b(?!\s+for)', 'refer to the previous section'),
            (r'\bsee below\b(?!\s+for)', 'refer to the following section'),
            (r'\baforementioned\b', 'previously described'),
            (r'\babove-mentioned\b', 'previously mentioned'),
            (r'\bthe previous\b(?!\s+\w+)', 'the previous section'),
            (r'\bthe following\b(?!\s+\w+)', 'the following content'),
        ]

        for pattern, replacement in replacements:
            fixed_line = re.sub(pattern, replacement, fixed_line, flags=re.IGNORECASE)

        return fixed_line

    def _add_term_definition(self, line: str, issue: Issue) -> str:
        """Add definition for technical terms on first use"""
        # Extract term and definition from the issue
        match = re.search(r"term '(\w+)' used without definition", issue.description)
        if not match:
            return line

        term = match.group(1)

        # Get definition
        definition = self.common_tech_terms.get(term)
        if not definition:
            return line

        # Find the term in the line and add definition
        # Use word boundary to avoid partial matches
        pattern = r'\b' + re.escape(term) + r'\b'

        # Check if term is already defined (has parentheses after it)
        if re.search(pattern + r'\s*\(', line):
            return line  # Already has definition

        # Add definition after first occurrence
        def replacer(match):
            return f"{match.group()} ({definition})"

        # Replace only the first occurrence
        fixed_line = re.sub(pattern, replacer, line, count=1)

        return fixed_line

    def suggest_code_context(self, code_language: str, code_content: str) -> str:
        """Suggest context for a code block based on its content"""
        # This is a simplified version - could be enhanced with more sophisticated analysis

        context_suggestions = {
            'python': "This Python code example shows",
            'javascript': "This JavaScript code demonstrates",
            'typescript': "This TypeScript example illustrates",
            'java': "This Java code shows",
            'bash': "This command demonstrates",
            'shell': "This shell command shows",
            'json': "This JSON configuration shows",
            'yaml': "This YAML configuration defines",
            'sql': "This SQL query demonstrates",
            'html': "This HTML markup shows",
            'css': "This CSS styling defines",
            'markdown': "This Markdown example shows",
            'go': "This Go code demonstrates",
            'rust': "This Rust code shows",
            'cpp': "This C++ code illustrates",
            'c': "This C code demonstrates",
        }

        # Analyze code content for specific patterns
        if 'function' in code_content or 'def' in code_content:
            suffix = " how to define a function"
        elif 'class' in code_content:
            suffix = " a class implementation"
        elif 'import' in code_content or 'require' in code_content:
            suffix = " the required imports"
        elif 'SELECT' in code_content.upper():
            suffix = " how to query data"
        elif 'INSERT' in code_content.upper():
            suffix = " how to insert data"
        elif 'CREATE' in code_content.upper():
            suffix = " how to create a table or resource"
        else:
            suffix = " the implementation"

        base_context = context_suggestions.get(code_language.lower(), "This code example shows")
        return base_context + suffix