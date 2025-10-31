"""
Style Guide Validation Fixer
Validates documentation against Claude Docs Style Guide using validation_rules.yaml

Features:
- Loads rules from validation_rules.yaml
- Highly automatable rules: regex-based auto-fixes
- Moderately automatable rules: pattern detection with suggestions
- Human judgment rules: Claude AI API analysis for voice, tone, context quality

Author: Alden Weaver and Claude
Version: 1.0.0
"""

import re
import yaml
import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Import anthropic for AI analysis
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from .base import BaseFixer
from core.models import Issue, FixResult
from core.config import Config


def sanitize_content_for_ai(content: str) -> str:
    """
    Sanitize content before sending to AI API to prevent JSON parsing errors.

    Handles:
    - Control characters that break JSON
    - Escape sequences
    - Null bytes
    - Invalid Unicode
    """
    # Remove null bytes
    content = content.replace('\x00', '')

    # Replace other control characters (except newlines, tabs, carriage returns)
    control_chars = ''.join(chr(i) for i in range(32) if i not in (9, 10, 13))
    translator = str.maketrans('', '', control_chars)
    content = content.translate(translator)

    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')

    # Remove invalid Unicode sequences
    content = content.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')

    return content


@dataclass
class ValidationRule:
    """Represents a validation rule from the YAML"""
    rule_id: str
    name: str
    severity: str
    category: str
    description: str
    rationale: str
    automation_level: str
    detection_method: str
    pattern: Optional[str] = None
    remediation: Optional[str] = None
    replacement: Optional[str] = None
    case_sensitive: bool = True
    incorrect_patterns: Optional[List[Dict]] = None
    max_occurrences: Optional[int] = None


class StyleGuideValidationFixer(BaseFixer):
    """
    Validates and fixes documentation against style guide rules

    Uses validation_rules.yaml for comprehensive style checking with three levels:
    1. Highly Automatable: Auto-fix with regex (terminology, formatting)
    2. Moderately Automatable: Detect and suggest (word count, language patterns)
    3. Human Judgment: AI analysis for voice, tone, context quality
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self.rules_file = Path(__file__).parent.parent / "style_guide" / "validation_rules.yaml"
        self.rules = self._load_rules()

        # Initialize Claude AI client for complex analysis
        self.ai_client = None
        self.ai_model = None

        api_key = os.getenv('ANTHROPIC_API_KEY')
        model = os.getenv('CLAUDE_MODEL')

        if api_key and model:
            self.ai_client = anthropic.Anthropic(api_key=api_key)
            self.ai_model = model
        elif api_key and not model:
            print("⚠ Warning: ANTHROPIC_API_KEY set but CLAUDE_MODEL not found in .env")
            print("  Style guide AI analysis will be disabled. Add CLAUDE_MODEL to .env")
        elif not api_key and model:
            print("⚠ Warning: CLAUDE_MODEL set but ANTHROPIC_API_KEY not found in .env")
            print("  Style guide AI analysis will be disabled. Add ANTHROPIC_API_KEY to .env")

        # Categorize rules by automation level
        self.highly_automatable = []
        self.moderately_automatable = []
        self.human_judgment = []
        self._categorize_rules()

    @property
    def name(self) -> str:
        return "Style Guide Validator"

    def _load_rules(self) -> Dict[str, Any]:
        """Load validation rules from YAML file"""
        if not self.rules_file.exists():
            print(f"Warning: validation_rules.yaml not found at {self.rules_file}")
            return {}

        with open(self.rules_file, 'r') as f:
            content = f.read()
            # Parse multi-document YAML
            documents = list(yaml.safe_load_all(content))

            # Combine all documents into single dict
            rules = {}
            for doc in documents:
                if doc:
                    rules.update(doc)

            return rules

    def _categorize_rules(self):
        """Categorize rules by automation level"""
        for rule_type in ['critical_rules', 'high_priority_rules', 'medium_priority_rules', 'low_priority_rules']:
            if rule_type not in self.rules:
                continue

            for rule_data in self.rules[rule_type]:
                rule = ValidationRule(
                    rule_id=rule_data.get('rule_id'),
                    name=rule_data.get('name'),
                    severity=rule_data.get('severity'),
                    category=rule_data.get('category'),
                    description=rule_data.get('description'),
                    rationale=rule_data.get('rationale'),
                    automation_level=rule_data.get('automation_level'),
                    detection_method=rule_data.get('detection_method'),
                    pattern=rule_data.get('pattern'),
                    remediation=rule_data.get('remediation'),
                    replacement=rule_data.get('replacement'),
                    case_sensitive=rule_data.get('case_sensitive', True),
                    incorrect_patterns=rule_data.get('incorrect_patterns'),
                    max_occurrences=rule_data.get('max_occurrences')
                )

                # Categorize by automation level
                if rule.automation_level == 'highly_automatable':
                    self.highly_automatable.append(rule)
                elif rule.automation_level == 'moderately_automatable':
                    self.moderately_automatable.append(rule)
                else:
                    self.human_judgment.append(rule)

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """
        Check file against all validation rules

        Process:
        1. Check highly automatable rules (regex, pattern matching)
        2. Check moderately automatable rules (heuristics, counting)
        3. Use Claude AI API for human judgment rules (voice, tone, context)
        """
        issues = []

        # Skip non-MDX files
        if not file_path.endswith(('.md', '.mdx')):
            return issues

        # Extract frontmatter and body
        frontmatter, body = self._extract_frontmatter(content)

        # 1. Check highly automatable rules
        issues.extend(self._check_highly_automatable(file_path, content, frontmatter, body))

        # 2. Check moderately automatable rules
        issues.extend(self._check_moderately_automatable(file_path, content, body))

        # 3. Use Claude AI for human judgment rules
        if self.ai_client:
            issues.extend(self._check_with_ai(file_path, content, body))

        return issues

    def _extract_frontmatter(self, content: str) -> tuple:
        """Extract YAML frontmatter and body content"""
        if not content.startswith('---\n'):
            return {}, content

        try:
            # Find end of frontmatter
            end_match = re.search(r'\n---\n', content[4:])
            if not end_match:
                return {}, content

            end_pos = end_match.end() + 4
            frontmatter_text = content[4:end_pos-4]
            body = content[end_pos:]

            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter or {}, body
        except:
            return {}, content

    def _check_highly_automatable(self, file_path: str, content: str, frontmatter: dict, body: str) -> List[Issue]:
        """Check highly automatable rules (regex-based, auto-fixable)"""
        issues = []

        for rule in self.highly_automatable:
            # Frontmatter checks
            if rule.category == 'frontmatter':
                if rule.rule_id == 'FMT-001':
                    if not content.startswith('---\n'):
                        issues.append(Issue(
                            severity=rule.severity,
                            category=rule.category,
                            file_path=file_path,
                            line_number=1,
                            issue_type=rule.rule_id,
                            description=rule.description,
                            suggestion=rule.remediation,
                            auto_fixable=False  # Requires template
                        ))

                elif rule.rule_id == 'FMT-002':
                    if 'title' not in frontmatter:
                        issues.append(Issue(
                            severity=rule.severity,
                            category=rule.category,
                            file_path=file_path,
                            line_number=1,
                            issue_type=rule.rule_id,
                            description=rule.description,
                            suggestion=rule.remediation,
                            auto_fixable=False
                        ))

                elif rule.rule_id == 'FMT-003':
                    if 'description' not in frontmatter:
                        issues.append(Issue(
                            severity=rule.severity,
                            category=rule.category,
                            file_path=file_path,
                            line_number=1,
                            issue_type=rule.rule_id,
                            description=rule.description,
                            suggestion=rule.remediation,
                            auto_fixable=False
                        ))

            # Pattern-based checks (terminology, links, code blocks)
            elif rule.pattern:
                flags = 0 if rule.case_sensitive else re.IGNORECASE
                multiline = getattr(rule, 'multiline', False)
                if multiline:
                    flags |= re.MULTILINE

                matches = list(re.finditer(rule.pattern, body, flags))

                # Check max occurrences
                if rule.max_occurrences and len(matches) > rule.max_occurrences:
                    for i, match in enumerate(matches[rule.max_occurrences:], start=rule.max_occurrences+1):
                        line_num = content[:match.start()].count('\n') + 1
                        issues.append(Issue(
                            severity=rule.severity,
                            category=rule.category,
                            file_path=file_path,
                            line_number=line_num,
                            issue_type=rule.rule_id,
                            description=f"{rule.description} (occurrence #{i})",
                            suggestion=rule.remediation,
                            context=match.group(),
                            auto_fixable=rule.replacement is not None
                        ))

                # Regular pattern violations
                elif matches and not rule.max_occurrences:
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        issues.append(Issue(
                            severity=rule.severity,
                            category=rule.category,
                            file_path=file_path,
                            line_number=line_num,
                            issue_type=rule.rule_id,
                            description=rule.description,
                            suggestion=rule.remediation,
                            context=match.group(),
                            auto_fixable=rule.replacement is not None
                        ))

            # Incorrect patterns (terminology capitalization)
            elif rule.incorrect_patterns:
                for pattern_dict in rule.incorrect_patterns:
                    pattern = pattern_dict.get('pattern')
                    correct = pattern_dict.get('correct')
                    flags = 0 if rule.case_sensitive else re.IGNORECASE

                    matches = list(re.finditer(pattern, body, flags))
                    for match in matches:
                        # Skip if already correct
                        if match.group() == correct:
                            continue

                        line_num = content[:match.start()].count('\n') + 1
                        issues.append(Issue(
                            severity=rule.severity,
                            category=rule.category,
                            file_path=file_path,
                            line_number=line_num,
                            issue_type=rule.rule_id,
                            description=f"{rule.description}: '{match.group()}'",
                            suggestion=f"Use '{correct}'",
                            context=match.group(),
                            auto_fixable=True
                        ))

        return issues

    def _check_moderately_automatable(self, file_path: str, content: str, body: str) -> List[Issue]:
        """Check moderately automatable rules (heuristics, counting)"""
        issues = []

        for rule in self.moderately_automatable:
            # Word count check
            if 'word_count' in rule.detection_method:
                words = body.split()
                word_count = len(words)

                min_words = getattr(rule, 'min_words', 0)
                max_words = getattr(rule, 'max_words', float('inf'))

                if word_count < min_words or word_count > max_words:
                    issues.append(Issue(
                        severity=rule.severity,
                        category=rule.category,
                        file_path=file_path,
                        line_number=None,
                        issue_type=rule.rule_id,
                        description=f"{rule.description} (current: {word_count} words)",
                        suggestion=rule.remediation,
                        auto_fixable=False
                    ))

            # Sentence length check
            if rule.rule_id == 'SENT-001':
                sentences = re.findall(r'[A-Z][^.!?]*[.!?]', body)
                for i, sentence in enumerate(sentences, 1):
                    word_count = len(sentence.split())
                    if word_count > 30:
                        # Find line number
                        pos = body.find(sentence)
                        line_num = content[:pos].count('\n') + 1

                        issues.append(Issue(
                            severity=rule.severity,
                            category=rule.category,
                            file_path=file_path,
                            line_number=line_num,
                            issue_type=rule.rule_id,
                            description=f"Sentence {i} has {word_count} words (max: 30)",
                            suggestion=rule.remediation,
                            context=sentence[:100] + "..." if len(sentence) > 100 else sentence,
                            auto_fixable=False
                        ))

            # Paragraph length check
            if rule.rule_id == 'PARA-001':
                paragraphs = body.split('\n\n')
                for i, para in enumerate(paragraphs, 1):
                    # Skip code blocks
                    if para.strip().startswith('```'):
                        continue

                    sentences = re.findall(r'[.!?]\s', para)
                    if len(sentences) > 7:
                        pos = body.find(para)
                        line_num = content[:pos].count('\n') + 1

                        issues.append(Issue(
                            severity=rule.severity,
                            category=rule.category,
                            file_path=file_path,
                            line_number=line_num,
                            issue_type=rule.rule_id,
                            description=f"Paragraph {i} has {len(sentences)} sentences (max: 7)",
                            suggestion=rule.remediation,
                            auto_fixable=False
                        ))

        return issues

    def _check_with_ai(self, file_path: str, content: str, body: str) -> List[Issue]:
        """
        Use Claude AI API to analyze human judgment rules

        AI checks for:
        - Voice and tone consistency (second person, active voice)
        - Context quality and completeness
        - Example relevance and clarity
        - Progressive complexity flow
        - Overall documentation quality
        """
        issues = []

        if not self.ai_client or not body.strip():
            return issues

        max_retries = 3
        base_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                # Sanitize content before sending to prevent JSON parsing errors
                sanitized_body = sanitize_content_for_ai(body[:3000])

                # Prepare content for AI analysis
                analysis_prompt = f"""You are a technical documentation quality analyzer for Claude Documentation.

Analyze this documentation content against these style guide criteria:

**Voice and Tone:**
- Second person ("you") - not first person ("I", "we")
- Active voice preferred over passive voice
- Professional-conversational balance
- Clear and direct language

**Content Quality:**
- Adequate context and prerequisites
- Clear examples that illustrate concepts
- Logical flow and progressive complexity
- Completeness - no missing steps or assumptions

**Style Issues:**
- Avoid weak/dismissive words: "simply", "just", "easily", "obviously"
- Avoid passive voice where active is clearer
- Keep language precise and technical where appropriate

Content to analyze:
{sanitized_body}{'...' if len(body) > 3000 else ''}

Respond ONLY with a JSON array of issues found. Each issue should have:
- "type": One of ["voice", "tone", "context", "clarity", "style"]
- "severity": One of ["high", "medium", "low"]
- "description": Brief description of the issue
- "line_hint": Excerpt of problematic text (first 50 chars)
- "suggestion": Specific suggestion for improvement

If no issues found, respond with empty array: []

Example response format:
[
  {{
    "type": "voice",
    "severity": "medium",
    "description": "Uses first person 'we' instead of second person 'you'",
    "line_hint": "We recommend that you configure...",
    "suggestion": "Change to: 'Configure your settings...'"
  }}
]
"""

                response = self.ai_client.messages.create(
                    model=self.ai_model,
                    max_tokens=2000,
                    messages=[{
                        "role": "user",
                        "content": analysis_prompt
                    }]
                )

                # Parse AI response
                ai_response = response.content[0].text.strip()

                # Extract JSON array (handle markdown code blocks and explanatory text)
                if '```json' in ai_response:
                    ai_response = ai_response.split('```json')[1].split('```')[0].strip()
                elif '```' in ai_response:
                    ai_response = ai_response.split('```')[1].split('```')[0].strip()

                # Try to find JSON array with regex as fallback
                if not ai_response or not ai_response.startswith('['):
                    import re
                    json_match = re.search(r'\[.*?\]', ai_response, re.DOTALL)
                    if json_match:
                        ai_response = json_match.group()
                    else:
                        # AI returned no issues (empty or explanatory text)
                        return issues

                # Handle empty arrays gracefully
                ai_response = ai_response.strip()
                if ai_response == '[]' or not ai_response:
                    return issues

                ai_issues = json.loads(ai_response)

                # Convert AI issues to Issue objects
                for ai_issue in ai_issues:
                    # Find approximate line number from line_hint
                    line_num = None
                    if 'line_hint' in ai_issue and ai_issue['line_hint']:
                        hint_pos = body.find(ai_issue['line_hint'][:50])
                        if hint_pos >= 0:
                            line_num = content[:hint_pos].count('\n') + 1

                    issues.append(Issue(
                        severity=ai_issue.get('severity', 'medium'),
                        category='style',
                        file_path=file_path,
                        line_number=line_num,
                        issue_type=f"AI-{ai_issue.get('type', 'quality').upper()}",
                        description=ai_issue.get('description', 'Quality issue detected by AI'),
                        suggestion=ai_issue.get('suggestion', 'Review and improve'),
                        context=ai_issue.get('line_hint'),
                        auto_fixable=False  # Human judgment required
                    ))

                # Success - break retry loop
                return issues

            except anthropic.RateLimitError as e:
                # Rate limit error (529) - retry with exponential backoff
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff: 2s, 4s, 8s
                    print(f"  ⏳ Rate limit hit for {file_path}, retrying in {delay}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(delay)
                else:
                    print(f"  ⚠️  AI analysis failed for {file_path} after {max_retries} retries: Rate limit exceeded")

            except json.JSONDecodeError as e:
                # JSON parsing error - log and skip
                print(f"  ⚠️  AI analysis failed for {file_path}: JSON parsing error - {str(e)}")
                return issues

            except Exception as e:
                # Other errors - log and skip
                print(f"  ⚠️  AI analysis error for {file_path}: {e}")
                return issues

        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        """
        Apply auto-fixes for highly automatable rules

        Can auto-fix:
        - Deprecated terminology (TERM-001)
        - Product name capitalization (TERM-002)
        - Weak language words (LANG-001, LANG-002, LANG-003)
        """
        fixed_content = content
        fixes_applied = []
        issues_fixed = []

        for issue in issues:
            if not issue.auto_fixable:
                continue

            # Terminology replacement
            if issue.issue_type == 'TERM-001' and issue.context:
                # Replace deprecated "Claude Code SDK" with "Claude Agent SDK"
                fixed_content = fixed_content.replace(issue.context, "Claude Agent SDK")
                fixes_applied.append(f"{issue.issue_type}: Fixed deprecated terminology")
                issues_fixed.append(issue)

            # Product name capitalization
            elif issue.issue_type == 'TERM-002' and issue.context:
                # Extract correct form from suggestion
                if "Use \"" in issue.suggestion:
                    correct_form = issue.suggestion.split("Use \"")[1].split("\"")[0]
                    fixed_content = fixed_content.replace(issue.context, correct_form)
                    fixes_applied.append(f"{issue.issue_type}: Fixed capitalization")
                    issues_fixed.append(issue)

            # Weak language
            elif issue.issue_type in ['LANG-001', 'LANG-002', 'LANG-003']:
                # Remove weak words (simply, just, easily)
                weak_words = {
                    'LANG-001': r'\bsimply\s+',
                    'LANG-002': r'\bjust\s+',
                    'LANG-003': r'\beasily\s+'
                }
                pattern = weak_words.get(issue.issue_type)
                if pattern:
                    fixed_content = re.sub(pattern, '', fixed_content, flags=re.IGNORECASE)
                    fixes_applied.append(f"{issue.issue_type}: Removed weak language")
                    issues_fixed.append(issue)

        return FixResult(
            file_path=file_path,
            original_content=content,
            fixed_content=fixed_content,
            fixes_applied=fixes_applied,
            issues_fixed=issues_fixed
        )
