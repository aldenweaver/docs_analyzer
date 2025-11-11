"""AI-powered semantic analysis using Claude"""

import os
import re
import json
import time
import sys
from typing import List, Dict, Any
from dataclasses import dataclass
from typing import Optional
import anthropic


# Import sanitize function from parent
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


class SemanticAnalyzer:
    """AI-powered semantic analysis using Claude"""

    def __init__(self, config: dict):
        self.config = config.get('claude_api', {})
        self.gap_config = config.get('gap_detection', {})
        self.claude_client = None

        # Check if AI analysis is enabled via environment variable or config
        ai_enabled_env = os.getenv('ENABLE_AI_ANALYSIS', 'true').lower() in ('true', '1', 'yes')
        ai_enabled_config = self.gap_config.get('semantic_analysis', {}).get('enabled', True)

        # Load configuration from environment variables (with fallbacks to config)
        self.model = os.getenv('CLAUDE_MODEL') or self.config.get('default_model', 'claude-sonnet-4-5-20250929')
        self.max_tokens = int(os.getenv('AI_MAX_TOKENS', '2000'))

        # Load API key from environment
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if api_key and ai_enabled_env and ai_enabled_config:
            self.claude_client = anthropic.Anthropic(api_key=api_key)

        self.enabled = self.claude_client is not None

    def analyze_clarity(self, file_path: str, content: str, issues: List[Issue]):
        """AI-powered clarity analysis with evidence-based recommendations"""
        if not self.enabled:
            return

        max_retries = 3
        base_delay = 2  # seconds

        for attempt in range(max_retries):
            try:
                # Sample and sanitize content to stay within limits and prevent JSON errors
                lines = content.split('\n')
                sample = '\n'.join(lines[:200])  # First 200 lines
                sample = sanitize_content_for_ai(sample)  # Sanitize before sending

                prompt = f"""You are a technical documentation analyst. Analyze this documentation for clarity issues using evidence-based criteria.

Documentation file: {file_path}

Content:
{sample}

Apply these research-backed principles:

1. **Cognitive Load (Nielsen Norman Group)**: Identify sentences >25 words that increase cognitive load
2. **Information Scent (Pirolli & Card)**: Find unclear headings that don't indicate content
3. **Progressive Disclosure**: Spot missing prerequisite information or context
4. **Plain Language (plainlanguage.gov)**: Flag jargon/acronyms undefined on first use
5. **Task-Oriented Writing (Redish)**: Identify ambiguous instructions lacking concrete steps

For EVERY issue found (prioritize by severity, but include ALL), provide:

{{
  "line_number": <exact line number>,
  "quoted_text": "<exact text with issue>",
  "issue_type": "<specific issue: cognitive_load | unclear_heading | missing_context | undefined_jargon | ambiguous_instruction>",
  "severity": "<critical | high | medium based on user impact>",
  "evidence": "<research principle violated and why it matters>",
  "user_impact": "<specific consequence for reader: 'Users cannot...' or 'Developers will...')>",
  "fix_approach": "<what strategy to use: simplify, split, define, add context, etc>",
  "before": "<quoted problematic text>",
  "after": "<concrete rewrite example>",
  "citation": "<principle: Nielsen Norman Group, Google Dev Docs Style, etc>"
}}

Prioritize issues by user impact. Return ONLY valid JSON array."""

                message = self.claude_client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    messages=[{"role": "user", "content": prompt}]
                )

                response_text = message.content[0].text.strip()

                # Extract JSON array (handle markdown code blocks and explanatory text)
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0].strip()
                elif '```' in response_text:
                    response_text = response_text.split('```')[1].split('```')[0].strip()

                # Try to extract JSON array with better regex (non-greedy to avoid capturing too much)
                # Look for array starting with [ and try to find matching ]
                json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
                if not json_match:
                    # AI returned no issues or invalid response
                    return

                response_text = json_match.group().strip()

                # Handle empty arrays gracefully
                if response_text == '[]' or not response_text:
                    return

                try:
                    ai_issues = json.loads(response_text)
                except json.JSONDecodeError as e:
                    # Try to fix common JSON issues
                    # Remove trailing commas
                    response_text = re.sub(r',\s*}', '}', response_text)
                    response_text = re.sub(r',\s*\]', ']', response_text)

                    # Try again
                    try:
                        ai_issues = json.loads(response_text)
                    except json.JSONDecodeError:
                        # If still failing, skip this clarity check
                        print(f"⚠️ Skipping AI clarity check for {file_path}: Invalid JSON response", file=sys.stderr)
                        return

                for issue in ai_issues:  # Process all issues
                        # Build detailed description with evidence
                        description = (
                            f"[{issue.get('issue_type', 'clarity_issue').replace('_', ' ').title()}] "
                            f"{issue.get('user_impact', 'Impacts user comprehension')}. "
                            f"Evidence: {issue.get('evidence', 'See citation')} "
                            f"(Source: {issue.get('citation', 'Documentation research')})"
                        )

                        # Build actionable suggestion with before/after
                        before_text = issue.get('before', issue.get('quoted_text', ''))[:100]
                        after_text = issue.get('after', '')[:150]

                        suggestion = (
                            f"{issue.get('fix_approach', 'Review and improve')}. "
                            f"Before: \"{before_text}{'...' if len(before_text) == 100 else ''}\" "
                            f"→ After: \"{after_text}{'...' if len(after_text) == 150 else ''}\""
                        )

                        issues.append(Issue(
                            severity=issue.get('severity', 'medium'),
                            category='clarity',
                            file_path=file_path,
                            line_number=issue.get('line_number'),
                            issue_type=f"ai_{issue.get('issue_type', 'clarity_check')}",
                            description=description,
                            suggestion=suggestion,
                            context=issue.get('quoted_text', '')[:200]  # Add quoted text as context
                        ))

                # Success - break retry loop
                return

            except anthropic.RateLimitError as e:
                # Rate limit error (529) - retry with exponential backoff
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)  # Exponential backoff: 2s, 4s, 8s
                    print(f"  ⏳ Rate limit hit for {file_path}, retrying in {delay}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(delay)
                else:
                    print(f"  ⚠️  AI clarity check failed for {file_path} after {max_retries} retries: Rate limit exceeded")

            except json.JSONDecodeError as e:
                # JSON parsing error - log and skip (content sanitization should prevent most of these)
                print(f"  ⚠️  AI clarity check failed for {file_path}: JSON parsing error - {str(e)}")
                return

            except Exception as e:
                # Other errors - log and skip
                print(f"  ⚠️  AI clarity check failed for {file_path}: {str(e)}")
                return

    def analyze_semantic_gaps(self, doc_structure: Dict[str, Any], issues: List[Issue], insights: List[str]):
        """Identify conceptual gaps in documentation coverage with evidence-based analysis"""
        if not self.enabled:
            return

        try:
            # Build detailed structure summary with file names
            files_list = doc_structure.get('files', [])
            structure_summary = {
                'total_files': len(files_list),
                'file_names': [str(f) for f in files_list[:100]],  # Show actual file names
                'categories': list(doc_structure.get('categories', {}).keys()),
                'topics_covered': list(doc_structure.get('topics', {}).keys())[:50],
                'has_quickstart': any('quickstart' in f.lower() for f in files_list),
                'has_troubleshooting': any('troubleshoot' in f.lower() for f in files_list),
                'has_api_reference': any('api' in f.lower() or 'reference' in f.lower() for f in files_list),
            }

            prompt = f"""You are analyzing documentation structure using the Divio Documentation Framework and user journey mapping.

Documentation structure:
{json.dumps(structure_summary, indent=2)}

Apply these frameworks:

1. **Divio Documentation System**: Check for all four types
   - Tutorials (learning-oriented): Getting started, first steps
   - How-To Guides (task-oriented): Specific problem solutions
   - Reference (information-oriented): Technical specifications, API docs
   - Explanation (understanding-oriented): Concepts, architecture, design decisions

2. **User Journey Analysis (Nielsen Norman Group)**: Identify gaps in typical user paths
   - First-time setup → Configuration → First success
   - Problem encountered → Troubleshooting → Resolution
   - Basic use → Advanced features → Optimization

3. **Information Architecture (Rosenfeld & Morville)**: Assess completeness

For EVERY gap found (prioritize critical gaps first, but include ALL), provide:

{{
  "gap_type": "<specific gap: missing_tutorial | missing_reference | incomplete_journey | orphaned_concept | missing_troubleshooting>",
  "severity": "<critical | high | medium based on user impact>",
  "evidence": "<what's missing and how you identified it from the file list>",
  "affected_files": ["<list specific files that reference this missing content>"],
  "user_journey_blocked": "<which user journey is broken: setup | learning | troubleshooting | etc>",
  "user_impact": "<specific consequence: 'Users cannot complete...' or 'Developers must guess...')>",
  "framework_principle": "<Divio type missing or user journey gap>",
  "concrete_suggestion": "<exactly what page/section to create with title suggestion>",
  "example_content": "<brief outline of what this missing doc should contain>",
  "priority_reason": "<why this gap is critical: frequency, severity, user stage>"
}}

Cite SPECIFIC files from the provided list. Return ONLY valid JSON array."""

            message = self.claude_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text.strip()

            # Extract JSON array (handle markdown code blocks and explanatory text)
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()

            # Try to extract JSON array with better regex
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if not json_match:
                # AI returned no gaps
                return

            response_text = json_match.group().strip()

            # Handle empty arrays gracefully
            if response_text == '[]' or not response_text:
                return

            try:
                gaps = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to fix common JSON issues
                # Remove trailing commas
                response_text = re.sub(r',\s*}', '}', response_text)
                response_text = re.sub(r',\s*\]', ']', response_text)

                # Try again
                try:
                    gaps = json.loads(response_text)
                except json.JSONDecodeError:
                    # If still failing, skip this semantic gap check
                    print(f"⚠️ Skipping semantic gap analysis: Invalid JSON response", file=sys.stderr)
                    return

            for gap in gaps:  # Process all gaps
                    # Build evidence-based description
                    affected = gap.get('affected_files', [])
                    affected_str = ', '.join(affected[:3]) if affected else 'Multiple files'
                    if len(affected) > 3:
                        affected_str += f' (+{len(affected) - 3} more)'

                    description = (
                        f"[{gap.get('gap_type', 'gap').replace('_', ' ').title()}] "
                        f"{gap.get('user_impact', 'Documentation gap identified')}. "
                        f"Evidence: {gap.get('evidence', 'See analysis')}. "
                        f"Framework: {gap.get('framework_principle', 'Divio/User Journey')}. "
                        f"Affected files: {affected_str}. "
                        f"Priority: {gap.get('priority_reason', 'High impact on users')}"
                    )

                    # Build concrete suggestion with example content
                    suggestion = (
                        f"{gap.get('concrete_suggestion', 'Add missing documentation')}. "
                        f"User journey blocked: {gap.get('user_journey_blocked', 'Unknown')}. "
                        f"Suggested content: {gap.get('example_content', 'See gap analysis')[:200]}"
                    )

                    issues.append(Issue(
                        severity=gap.get('severity', 'high'),
                        category='gaps',
                        file_path='[documentation set]',
                        line_number=None,
                        issue_type=f"gap_{gap.get('gap_type', 'semantic')}",
                        description=description,
                        suggestion=suggestion
                    ))

                    # Add detailed insight
                    insights.append(
                        f"📊 {gap.get('gap_type', 'Gap').replace('_', ' ').title()}: "
                        f"{gap.get('concrete_suggestion', 'Documentation needed')} "
                        f"(Affects: {affected_str})"
                    )

        except Exception as e:
            print(f"  ⚠️  Semantic gap analysis failed: {str(e)}")
