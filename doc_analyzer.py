#!/usr/bin/env python3
"""
Documentation Quality Analyzer for Claude Docs
Comprehensive tool with Mintlify support, MDX validation, AI analysis, and advanced gap detection

This version includes:
- Phase 1: MDX/frontmatter validation, Mintlify-specific checks, configurable repository
- Phase 2: AI semantic analysis, cross-reference validation, doc map integration
- Phase 3: User journey mapping, advanced duplication detection, platform-specific analyzers

Author: Alden Weaver and Claude
Created for: Anthropic Technical Writer Proof of Concept
Version: 2.0.0 (Enhanced)
"""

import os
import re
import json
import yaml
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set, Any
from dataclasses import dataclass, field
from collections import defaultdict, Counter
from datetime import datetime
from urllib.parse import urlparse
import anthropic
from difflib import SequenceMatcher

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Try to import optional dependencies
try:
    import git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False


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


@dataclass
class AnalysisReport:
    """Comprehensive analysis report"""
    timestamp: str
    total_files: int
    total_issues: int
    repository_info: Dict[str, Any] = field(default_factory=dict)
    issues_by_severity: Dict[str, int] = field(default_factory=dict)
    issues_by_category: Dict[str, int] = field(default_factory=dict)
    issues: List[Issue] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    ai_insights: List[str] = field(default_factory=list)
    
    def add_issue(self, issue: Issue):
        self.issues.append(issue)
        self.total_issues += 1
        self.issues_by_severity[issue.severity] = \
            self.issues_by_severity.get(issue.severity, 0) + 1
        self.issues_by_category[issue.category] = \
            self.issues_by_category.get(issue.category, 0) + 1


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
            # Check for Mintlify
            if (search_path / 'mint.json').exists():
                self.repo_root = search_path  # Update to where we found it
                return 'mintlify'
            elif (search_path / 'docs.json').exists():
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
        """Load Mintlify configuration"""
        config_file = self.repo_root / 'mint.json'
        if not config_file.exists():
            config_file = self.repo_root / 'docs.json'

        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def get_files(self) -> List[Path]:
        """Get all documentation files based on config"""
        include_patterns = self.config.get('include_patterns', ['**/*.md', '**/*.mdx'])
        exclude_patterns = self.config.get('exclude_patterns', [])
        
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


class MDXParser:
    """Parse MDX files and extract frontmatter"""
    
    @staticmethod
    def parse_frontmatter(content: str) -> Tuple[Optional[dict], str]:
        """Extract YAML frontmatter and content"""
        if not content.startswith('---'):
            return None, content
        
        # Find end of frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            return None, content
        
        try:
            frontmatter = yaml.safe_load(parts[1])
            content_body = parts[2]
            return frontmatter, content_body
        except yaml.YAMLError:
            return None, content
    
    @staticmethod
    def extract_components(content: str) -> List[Tuple[str, int]]:
        """Extract Mintlify components from MDX"""
        components = []
        
        # Match JSX-style components
        component_pattern = r'<(\w+)(?:\s+[^>]*)?>.*?</\1>|<(\w+)(?:\s+[^>]*)?/>'
        
        for match in re.finditer(component_pattern, content, re.DOTALL):
            component_name = match.group(1) or match.group(2)
            line_number = content[:match.start()].count('\n') + 1
            components.append((component_name, line_number))
        
        return components


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
        if not file_path.endswith('.mdx') and not file_path.endswith('.md'):
            return
        
        frontmatter, _ = MDXParser.parse_frontmatter(content)
        
        # Check if frontmatter exists (critical for MDX)
        if file_path.endswith('.mdx') and frontmatter is None:
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
        """AI-powered clarity analysis"""
        if not self.enabled:
            return
        
        try:
            # Sample content to stay within limits
            lines = content.split('\n')
            sample = '\n'.join(lines[:200])  # First 200 lines
            
            prompt = f"""Analyze this documentation excerpt for clarity issues. 
Focus on:
1. Confusing explanations
2. Missing context or prerequisites
3. Undefined jargon or acronyms
4. Ambiguous instructions
5. Logical gaps or unclear flow

Documentation excerpt from {file_path}:

{sample}

Provide a JSON array of issues (max 5 most important). Each issue should have:
- line_number (approximate)
- issue_type
- description (brief, specific)
- suggestion (actionable fix)

Return ONLY valid JSON array, no other text."""

            message = self.claude_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            
            # Try to extract JSON
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                ai_issues = json.loads(json_match.group())
                
                for issue in ai_issues[:5]:  # Limit to 5
                    issues.append(Issue(
                        severity='medium',
                        category='clarity',
                        file_path=file_path,
                        line_number=issue.get('line_number'),
                        issue_type='ai_clarity_check',
                        description=issue.get('description', 'AI-identified clarity issue'),
                        suggestion=issue.get('suggestion', 'Review and clarify')
                    ))
        
        except Exception as e:
            print(f"  ⚠️  AI clarity check failed for {file_path}: {str(e)}")
    
    def analyze_semantic_gaps(self, doc_structure: Dict[str, Any], issues: List[Issue], insights: List[str]):
        """Identify conceptual gaps in documentation coverage"""
        if not self.enabled:
            return
        
        try:
            # Build structure summary
            structure_summary = {
                'total_files': len(doc_structure.get('files', [])),
                'categories': list(doc_structure.get('categories', {}).keys()),
                'topics_covered': list(doc_structure.get('topics', {}).keys())[:50],
                'has_quickstart': any('quickstart' in f.lower() for f in doc_structure.get('files', [])),
                'has_troubleshooting': any('troubleshoot' in f.lower() for f in doc_structure.get('files', [])),
                'has_api_reference': any('api' in f.lower() for f in doc_structure.get('files', [])),
            }
            
            prompt = f"""Analyze this documentation structure and identify semantic gaps.

Documentation structure:
{json.dumps(structure_summary, indent=2)}

Identify:
1. Missing user journey steps (e.g., no migration guide, no upgrade path)
2. Concepts mentioned but not explained
3. Features without examples
4. Incomplete coverage areas
5. Missing troubleshooting scenarios

Provide:
1. Top 5 most critical gaps
2. Each as: {{"gap_type": "...", "description": "...", "impact": "...", "suggestion": "..."}}

Return ONLY valid JSON array."""

            message = self.claude_client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = message.content[0].text
            
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                gaps = json.loads(json_match.group())
                
                for gap in gaps[:5]:
                    issues.append(Issue(
                        severity='high',
                        category='gaps',
                        file_path='[documentation set]',
                        line_number=None,
                        issue_type='semantic_gap',
                        description=gap.get('description', 'Semantic gap identified'),
                        suggestion=gap.get('suggestion', 'Address this gap')
                    ))
                    
                    insights.append(f"Gap: {gap.get('gap_type')} - {gap.get('impact')}")
        
        except Exception as e:
            print(f"  ⚠️  Semantic gap analysis failed: {str(e)}")


class ContentDuplicationDetector:
    """Detect content duplication and redundancy"""
    
    def __init__(self, config: dict):
        self.config = config.get('duplication_detection', {})
        self.threshold = self.config.get('similarity_threshold', 0.8)
        self.enabled = self.config.get('enabled', True)
    
    def find_duplicates(self, files: List[Path], issues: List[Issue]):
        """Find duplicate or highly similar content"""
        if not self.enabled:
            return
        
        print("\n🔍 Detecting content duplication...")
        
        # Extract paragraphs from all files
        file_paragraphs = {}
        for file_path in files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract paragraphs (2+ lines of text)
                    paragraphs = [p.strip() for p in content.split('\n\n') if len(p.strip()) > 100]
                    file_paragraphs[str(file_path)] = paragraphs
            except Exception:
                continue
        
        # Compare paragraphs across files
        checked_pairs = set()
        
        for file1, paras1 in file_paragraphs.items():
            for file2, paras2 in file_paragraphs.items():
                if file1 >= file2:  # Skip self and already checked pairs
                    continue
                
                pair_key = (file1, file2)
                if pair_key in checked_pairs:
                    continue
                checked_pairs.add(pair_key)
                
                # Compare paragraphs
                for i, p1 in enumerate(paras1):
                    for j, p2 in enumerate(paras2):
                        similarity = self._calculate_similarity(p1, p2)
                        
                        if similarity >= self.threshold:
                            issues.append(Issue(
                                severity='medium',
                                category='gaps',
                                file_path=f'{file1} & {file2}',
                                line_number=None,
                                issue_type='duplicate_content',
                                description=f'Highly similar content detected ({int(similarity*100)}% similar)',
                                suggestion='Consider consolidating or cross-referencing instead of duplicating',
                                context=p1[:100] + '...'
                            ))
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity ratio"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


class UserJourneyAnalyzer:
    """Analyze if documentation supports common user journeys"""
    
    def __init__(self, config: dict):
        self.config = config.get('gap_detection', {})
        self.required_journeys = self.config.get('required_journeys', [])
    
    def validate_journeys(self, doc_structure: Dict[str, Any], issues: List[Issue]):
        """Check if required user journeys are supported"""
        print("\n🚶 Validating user journeys...")
        
        files = doc_structure.get('files', [])
        file_names = [f.lower() for f in files]
        
        for journey in self.required_journeys:
            name = journey.get('name', 'Unknown journey')
            steps = journey.get('steps', [])
            
            missing_steps = []
            for step in steps:
                # Check if any file name contains this step
                if not any(step.lower() in fname for fname in file_names):
                    missing_steps.append(step)
            
            if missing_steps:
                issues.append(Issue(
                    severity='high',
                    category='gaps',
                    file_path='[documentation set]',
                    line_number=None,
                    issue_type='incomplete_user_journey',
                    description=f'User journey "{name}" is incomplete',
                    suggestion=f'Add documentation for: {", ".join(missing_steps)}'
                ))


class DocumentationAnalyzer:
    """
    Documentation analyzer with full Phase 1-3 features
    """
    
    def __init__(self, repo_manager: RepositoryManager, config: dict):
        self.repo_manager = repo_manager
        self.config = config
        self.report = AnalysisReport(
            timestamp=datetime.now().isoformat(),
            total_files=0,
            total_issues=0,
            repository_info={
                'path': str(repo_manager.repo_path),
                'type': repo_manager.repo_type,
            }
        )
        
        # Load style rules
        self.style_rules = config.get('style_rules', {})
        
        # Initialize specialized analyzers
        self.mintlify_validator = MintlifyValidator(config, repo_manager)
        self.semantic_analyzer = SemanticAnalyzer(config)
        self.duplication_detector = ContentDuplicationDetector(config)
        self.journey_analyzer = UserJourneyAnalyzer(config)
    
    def analyze_all(self) -> AnalysisReport:
        """Run comprehensive analysis"""
        print("🔍 Starting documentation analysis...")
        print(f"Repository type: {self.repo_manager.repo_type}")
        
        # Get files
        files = self.repo_manager.get_files()
        self.report.total_files = len(files)
        
        print(f"Found {len(files)} documentation files")
        
        # Phase 1: File-level analysis
        for file_path in files:
            print(f"  Analyzing: {file_path.relative_to(self.repo_manager.repo_path)}")
            self.analyze_file(file_path)
        
        # Phase 2: Cross-file analysis
        print("\n📊 Running cross-file analysis...")
        doc_structure = self._build_doc_structure(files)
        self.analyze_information_architecture(files)
        self.analyze_consistency(files)
        
        # Phase 3: Advanced analysis
        print("\n🧠 Running advanced analysis...")
        self.detect_content_gaps(doc_structure)
        self.duplication_detector.find_duplicates(files, self.report.issues)
        self.journey_analyzer.validate_journeys(doc_structure, self.report.issues)
        
        # AI semantic analysis
        if self.semantic_analyzer.enabled:
            print("\n🤖 Running AI semantic analysis...")
            self.semantic_analyzer.analyze_semantic_gaps(
                doc_structure, 
                self.report.issues, 
                self.report.ai_insights
            )
        
        # Generate recommendations
        self.generate_recommendations()
        
        print(f"\n✅ Analysis complete! Found {self.report.total_issues} issues")
        return self.report
    
    def analyze_file(self, file_path: Path):
        """Analyze a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            relative_path = str(file_path.relative_to(self.repo_manager.repo_path))
            
            # Phase 1 checks
            if self.repo_manager.repo_type == 'mintlify':
                self.mintlify_validator.validate_frontmatter(relative_path, content, self.report.issues)
                self.mintlify_validator.validate_components(relative_path, content, self.report.issues)
                self.mintlify_validator.validate_internal_links(relative_path, content, self.report.issues)
            
            # Core checks
            self.check_readability(content, relative_path)
            self.check_style_guide(content, relative_path)
            self.check_structure(content, relative_path)
            self.check_formatting(content, relative_path)
            self.check_links(content, relative_path, file_path)
            
            # AI-powered clarity check
            if self.semantic_analyzer.enabled and self.config.get('analysis', {}).get('enable_ai_analysis', True):
                self.semantic_analyzer.analyze_clarity(relative_path, content, self.report.issues)
        
        except Exception as e:
            self.report.add_issue(Issue(
                severity='high',
                category='technical',
                file_path=str(file_path),
                line_number=None,
                issue_type='file_error',
                description=f'Error analyzing file: {str(e)}',
                suggestion='Check file encoding and permissions'
            ))
    
    def check_readability(self, content: str, file_path: str):
        """Check readability metrics"""
        lines = content.split('\n')
        in_code_block = False
        
        for i, line in enumerate(lines, 1):
            # Track code blocks
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block or line.strip().startswith('#'):
                continue
            
            # Check line length
            max_length = self.style_rules.get('max_line_length', 100)
            if len(line) > max_length and not line.strip().startswith('http'):
                self.report.add_issue(Issue(
                    severity='low',
                    category='clarity',
                    file_path=file_path,
                    line_number=i,
                    issue_type='line_too_long',
                    description=f'Line exceeds {max_length} characters',
                    suggestion='Break into shorter lines or sentences',
                    context=line[:100] + '...' if len(line) > 100 else line
                ))
            
            # Check sentence length
            if line.strip() and not line.strip().startswith(('*', '-', '>', '|')):
                word_count = len(line.split())
                max_words = self.style_rules.get('max_sentence_length', 30)
                if word_count > max_words:
                    self.report.add_issue(Issue(
                        severity='medium',
                        category='clarity',
                        file_path=file_path,
                        line_number=i,
                        issue_type='sentence_too_long',
                        description=f'Sentence has {word_count} words (recommend <{max_words})',
                        suggestion='Break into shorter sentences for better readability',
                        context=line[:100] + '...' if len(line) > 100 else line
                    ))
            
            # Check for weak words
            avoid_terms = self.style_rules.get('avoid_terms', [])
            for term in avoid_terms:
                if re.search(rf'\b{re.escape(term)}\b', line, re.IGNORECASE):
                    self.report.add_issue(Issue(
                        severity='low',
                        category='style',
                        file_path=file_path,
                        line_number=i,
                        issue_type='weak_language',
                        description=f'Avoid weak or unnecessary word: "{term}"',
                        suggestion='Remove or replace with more precise language',
                        context=line.strip()
                    ))
    
    def check_style_guide(self, content: str, file_path: str):
        """Check style guide compliance"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check preferred terminology
            preferred_terms = self.style_rules.get('preferred_terms', {})
            for old_term, new_term in preferred_terms.items():
                if re.search(rf'\b{re.escape(old_term)}\b', line, re.IGNORECASE):
                    self.report.add_issue(Issue(
                        severity='low',
                        category='style',
                        file_path=file_path,
                        line_number=i,
                        issue_type='terminology',
                        description=f'Use "{new_term}" instead of "{old_term}"',
                        suggestion=f'Replace with preferred term: "{new_term}"',
                        context=line.strip()
                    ))
            
            # Check for passive voice
            passive_patterns = [
                r'\bis\s+\w+ed\b', r'\bare\s+\w+ed\b', r'\bwas\s+\w+ed\b',
                r'\bwere\s+\w+ed\b', r'\bbeen\s+\w+ed\b', r'\bbe\s+\w+ed\b'
            ]
            for pattern in passive_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.report.add_issue(Issue(
                        severity='low',
                        category='style',
                        file_path=file_path,
                        line_number=i,
                        issue_type='passive_voice',
                        description='Consider using active voice',
                        suggestion='Rewrite in active voice for clarity',
                        context=line.strip()
                    ))
                    break
    
    def check_structure(self, content: str, file_path: str):
        """Check document structure"""
        lines = content.split('\n')
        headings = []
        heading_levels = []
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('#'):
                level = len(re.match(r'^#+', line.strip()).group())
                heading = line.strip('#').strip()
                headings.append((level, heading, i))
                heading_levels.append(level)
        
        # Check heading hierarchy
        for i in range(len(heading_levels) - 1):
            current = heading_levels[i]
            next_level = heading_levels[i + 1]
            
            if next_level > current + 1:
                self.report.add_issue(Issue(
                    severity='medium',
                    category='ia',
                    file_path=file_path,
                    line_number=headings[i + 1][2],
                    issue_type='heading_skip',
                    description=f'Heading skips from H{current} to H{next_level}',
                    suggestion=f'Use H{current + 1} instead to maintain hierarchy',
                    context=headings[i + 1][1]
                ))
    
    def check_formatting(self, content: str, file_path: str):
        """Check formatting consistency"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check code blocks have language
            if line.strip().startswith('```'):
                lang = line.strip()[3:].strip()
                if not lang and i < len(lines) and lines[i].strip():
                    self.report.add_issue(Issue(
                        severity='critical' if self.repo_manager.repo_type == 'mintlify' else 'medium',
                        category='style',
                        file_path=file_path,
                        line_number=i,
                        issue_type='missing_language_tag',
                        description='Code block missing language identifier (REQUIRED in Mintlify)',
                        suggestion='Specify language for syntax highlighting (e.g., ```python)'
                    ))
    
    def check_links(self, content: str, file_path: str, full_path: Path):
        """Check link quality"""
        lines = content.split('\n')
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        
        for i, line in enumerate(lines, 1):
            for match in re.finditer(link_pattern, line):
                link_text = match.group(1)
                link_url = match.group(2)
                
                # Empty link text
                if not link_text.strip():
                    self.report.add_issue(Issue(
                        severity='high',
                        category='ux',
                        file_path=file_path,
                        line_number=i,
                        issue_type='empty_link_text',
                        description='Link has empty text',
                        suggestion='Provide descriptive link text',
                        context=match.group(0)
                    ))
                
                # Non-descriptive text
                if re.match(r'^(click here|here|link|this)$', link_text.strip(), re.IGNORECASE):
                    self.report.add_issue(Issue(
                        severity='medium',
                        category='ux',
                        file_path=file_path,
                        line_number=i,
                        issue_type='non_descriptive_link',
                        description=f'Link text is non-descriptive: "{link_text}"',
                        suggestion='Use descriptive link text explaining destination',
                        context=match.group(0)
                    ))
                
                # Check relative links exist
                if link_url.startswith('./') or link_url.startswith('../'):
                    target = (full_path.parent / link_url).resolve()
                    if not target.exists():
                        self.report.add_issue(Issue(
                            severity='critical',
                            category='technical',
                            file_path=file_path,
                            line_number=i,
                            issue_type='broken_link',
                            description=f'Broken relative link: {link_url}',
                            suggestion='Fix link or update target path',
                            context=match.group(0)
                        ))
    
    def analyze_information_architecture(self, files: List[Path]):
        """Analyze overall IA"""
        print("\n🏗️  Analyzing information architecture...")
        
        structure = defaultdict(list)
        for file_path in files:
            rel_path = file_path.relative_to(self.repo_manager.repo_path)
            if len(rel_path.parts) > 1:
                category = rel_path.parts[0]
                structure[category].append(str(rel_path))
        
        # Check for overloaded categories
        max_docs = self.config.get('ia_patterns', {}).get('max_docs_per_category', 20)
        for category, docs in structure.items():
            if len(docs) > max_docs:
                self.report.add_issue(Issue(
                    severity='medium',
                    category='ia',
                    file_path=f'[{category}]',
                    line_number=None,
                    issue_type='category_overload',
                    description=f'Category "{category}" has {len(docs)} documents (>{max_docs})',
                    suggestion='Consider splitting into subcategories'
                ))
    
    def analyze_consistency(self, files: List[Path]):
        """Analyze consistency across docs"""
        print("\n🎨 Analyzing consistency...")
        
        term_usage = defaultdict(lambda: defaultdict(list))
        
        term_variants = self.config.get('consistency', {}).get('term_variants', {})
        
        for file_path in files:
            try:
                with open(file_path, 'r') as f:
                    content = f.read().lower()
                    
                    for canonical, variant_info in term_variants.items():
                        variants = variant_info.get('variants', [])
                        for variant in variants:
                            if variant.lower() in content:
                                term_usage[canonical][variant].append(str(file_path))
            except Exception:
                pass
        
        # Report inconsistencies
        for canonical, variants in term_usage.items():
            if len(variants) > 2:
                variant_info = self.config['consistency']['term_variants'][canonical]
                correct_term = variant_info.get('canonical', canonical)
                
                self.report.add_issue(Issue(
                    severity='low',
                    category='consistency',
                    file_path='[multiple]',
                    line_number=None,
                    issue_type='term_inconsistency',
                    description=f'Inconsistent usage of "{canonical}": {len(variants)} variants',
                    suggestion=f'Standardize on: "{correct_term}"'
                ))
    
    def detect_content_gaps(self, doc_structure: Dict[str, Any]):
        """Detect content gaps"""
        print("\n🔍 Detecting content gaps...")
        
        files = doc_structure.get('files', [])
        topics = doc_structure.get('topics', {})
        
        # Check for redundant content
        for topic, locations in topics.items():
            if len(locations) > 3:
                self.report.add_issue(Issue(
                    severity='medium',
                    category='gaps',
                    file_path='[multiple]',
                    line_number=None,
                    issue_type='redundant_content',
                    description=f'Topic "{topic}" appears in {len(locations)} files',
                    suggestion='Consider consolidating or cross-referencing'
                ))
        
        # Check for missing content types
        required_types = self.config.get('content_rules', {}).get('required_content_types', [])
        file_names_lower = [f.lower() for f in files]
        
        for content_type in required_types:
            if not any(content_type in fname for fname in file_names_lower):
                self.report.add_issue(Issue(
                    severity='high',
                    category='gaps',
                    file_path='[documentation set]',
                    line_number=None,
                    issue_type='missing_content_type',
                    description=f'No {content_type} documentation found',
                    suggestion=f'Add {content_type} section'
                ))
    
    def _build_doc_structure(self, files: List[Path]) -> Dict[str, Any]:
        """Build documentation structure for analysis"""
        structure = {
            'files': [],
            'categories': defaultdict(list),
            'topics': defaultdict(list)
        }
        
        for file_path in files:
            rel_path = file_path.relative_to(self.repo_manager.repo_path)
            structure['files'].append(str(rel_path))
            
            # Category
            if len(rel_path.parts) > 1:
                category = rel_path.parts[0]
                structure['categories'][category].append(str(rel_path))
            
            # Extract topics from headings
            try:
                with open(file_path, 'r') as f:
                    content = f.read()
                    headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
                    for heading in headings:
                        structure['topics'][heading.lower()].append(str(rel_path))
            except Exception:
                pass
        
        return structure
    
    def generate_recommendations(self):
        """Generate high-level recommendations"""
        print("\n💡 Generating recommendations...")
        
        # Category-based recommendations
        for category, count in self.report.issues_by_category.items():
            if count > 50:
                self.report.recommendations.append(
                    f"High number of {category} issues ({count}). Recommend focused audit in this area."
                )
        
        # Severity-based recommendations
        critical = self.report.issues_by_severity.get('critical', 0)
        high = self.report.issues_by_severity.get('high', 0)
        
        if critical > 0:
            self.report.recommendations.append(
                f"{critical} critical issues require immediate attention (broken links, missing frontmatter, etc.)"
            )
        
        if high > 20:
            self.report.recommendations.append(
                f"{high} high-priority issues found. Prioritize these in next sprint."
            )
        
        # AI insights
        if self.report.ai_insights:
            self.report.recommendations.append(
                f"AI analysis identified {len(self.report.ai_insights)} key insights. Review AI insights section."
            )
    
    def _create_timestamped_report_dir(self) -> Path:
        """Create timestamped report directory (cached for this analysis run)"""
        from datetime import datetime

        # Cache the report directory to ensure all formats go to the same place
        if not hasattr(self, '_report_dir'):
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            self._report_dir = Path('reports') / timestamp
            self._report_dir.mkdir(parents=True, exist_ok=True)
            print(f"\n📁 Creating report directory: {self._report_dir}")

        return self._report_dir

    def export_report(self, output_format: str = 'json', output_path: Optional[str] = None):
        """Export analysis report"""
        if output_format == 'json':
            return self._export_json(output_path)
        elif output_format == 'html':
            return self._export_html(output_path)
        elif output_format == 'markdown':
            return self._export_markdown(output_path)
    
    def _export_json(self, output_path: Optional[str]) -> str:
        """Export as JSON"""
        if not output_path:
            report_dir = self._create_timestamped_report_dir()
            output_path = str(report_dir / 'doc_analysis_report.json')

        report_data = {
            'timestamp': self.report.timestamp,
            'repository': self.report.repository_info,
            'summary': {
                'total_files': self.report.total_files,
                'total_issues': self.report.total_issues,
                'by_severity': self.report.issues_by_severity,
                'by_category': self.report.issues_by_category,
            },
            'recommendations': self.report.recommendations,
            'ai_insights': self.report.ai_insights,
            'issues': [issue.to_dict() for issue in self.report.issues]
        }

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)

        print(f"\n📄 JSON report exported to: {output_path}")
        return output_path
    
    def _export_html(self, output_path: Optional[str]) -> str:
        """Export as HTML (using existing implementation)"""
        if not output_path:
            report_dir = self._create_timestamped_report_dir()
            output_path = str(report_dir / 'doc_analysis_report.html')

        # Use HTML template with AI insights
        html = self._generate_html_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\n📄 HTML report exported to: {output_path}")
        return output_path
    
    def _generate_html_report(self) -> str:
        """Generate HTML report"""
        # Implementation similar to original but with AI insights section
        # (Keeping it concise - full implementation would be quite long)
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Documentation Analysis Report</title>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
        .header {{ background: white; padding: 30px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 2.5em; font-weight: bold; margin: 10px 0; }}
        .critical {{ color: #dc2626; }}
        .high {{ color: #ea580c; }}
        .medium {{ color: #ca8a04; }}
        .low {{ color: #65a30d; }}
        .recommendations {{ background: #dbeafe; border-left: 4px solid #3b82f6; padding: 20px; margin: 20px 0; border-radius: 4px; }}
        .ai-insights {{ background: #f0fdf4; border-left: 4px solid #10b981; padding: 20px; margin: 20px 0; border-radius: 4px; }}
        .issues {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .issue-item {{ border-left: 4px solid #e5e7eb; padding: 15px; margin: 10px 0; background: #f9fafb; border-radius: 4px; }}
        .issue-item.critical {{ border-left-color: #dc2626; }}
        .issue-item.high {{ border-left-color: #ea580c; }}
        .issue-item.medium {{ border-left-color: #ca8a04; }}
        .issue-item.low {{ border-left-color: #65a30d; }}
        .badge {{ display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; font-weight: 600; margin-right: 8px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Documentation Analysis Report</h1>
        <p><strong>Generated:</strong> {self.report.timestamp}</p>
        <p><strong>Repository:</strong> {self.report.repository_info.get('path')}</p>
        <p><strong>Platform:</strong> {self.report.repository_info.get('type')}</p>
        <p><strong>Files Analyzed:</strong> {self.report.total_files}</p>
    </div>
    
    <div class="summary">
        <div class="stat-card">
            <div>Total Issues</div>
            <div class="stat-number">{self.report.total_issues}</div>
        </div>
        <div class="stat-card">
            <div>Critical</div>
            <div class="stat-number critical">{self.report.issues_by_severity.get('critical', 0)}</div>
        </div>
        <div class="stat-card">
            <div>High</div>
            <div class="stat-number high">{self.report.issues_by_severity.get('high', 0)}</div>
        </div>
        <div class="stat-card">
            <div>Medium</div>
            <div class="stat-number medium">{self.report.issues_by_severity.get('medium', 0)}</div>
        </div>
        <div class="stat-card">
            <div>Low</div>
            <div class="stat-number low">{self.report.issues_by_severity.get('low', 0)}</div>
        </div>
    </div>
    
    {self._generate_recommendations_html()}
    {self._generate_ai_insights_html()}
    
    <div class="issues">
        <h2>Issues Found</h2>
        <p>Showing first 100 issues. See JSON report for complete list.</p>
        {self._generate_issues_html()}
    </div>
</body>
</html>"""
        return html
    
    def _generate_recommendations_html(self) -> str:
        if not self.report.recommendations:
            return ""
        
        html = '<div class="recommendations">\n<h3>💡 Recommendations</h3>\n<ul>\n'
        for rec in self.report.recommendations:
            html += f'<li>{rec}</li>\n'
        html += '</ul>\n</div>\n'
        return html
    
    def _generate_ai_insights_html(self) -> str:
        if not self.report.ai_insights:
            return ""
        
        html = '<div class="ai-insights">\n<h3>🤖 AI Insights</h3>\n<ul>\n'
        for insight in self.report.ai_insights:
            html += f'<li>{insight}</li>\n'
        html += '</ul>\n</div>\n'
        return html
    
    def _generate_issues_html(self) -> str:
        html = ""
        for issue in self.report.issues[:100]:
            html += f"""
        <div class="issue-item {issue.severity}">
            <div>
                <span class="badge {issue.severity}">{issue.severity.upper()}</span>
                <span class="badge">{issue.category}</span>
                <strong>{issue.issue_type.replace('_', ' ').title()}</strong>
            </div>
            <div style="margin-top: 10px;">
                <strong>File:</strong> {issue.file_path}
                {f'<strong> Line:</strong> {issue.line_number}' if issue.line_number else ''}
            </div>
            <div style="margin-top: 10px;">
                <strong>Issue:</strong> {issue.description}
            </div>
            <div style="margin-top: 5px; color: #059669;">
                <strong>Suggestion:</strong> {issue.suggestion}
            </div>
            {f'<div style="margin-top: 10px; font-family: monospace; background: #f3f4f6; padding: 10px; border-radius: 4px; font-size: 0.9em;">{issue.context}</div>' if issue.context else ''}
        </div>
        """
        return html
    
    def _export_markdown(self, output_path: Optional[str]) -> str:
        """Export as Markdown"""
        if not output_path:
            report_dir = self._create_timestamped_report_dir()
            output_path = str(report_dir / 'doc_analysis_report.md')

        md = f"""# Documentation Analysis Report

**Generated:** {self.report.timestamp}
**Repository:** {self.report.repository_info.get('path')}
**Platform:** {self.report.repository_info.get('type')}
**Files Analyzed:** {self.report.total_files}
**Total Issues:** {self.report.total_issues}

## Summary

| Severity | Count |
|----------|-------|
| Critical | {self.report.issues_by_severity.get('critical', 0)} |
| High | {self.report.issues_by_severity.get('high', 0)} |
| Medium | {self.report.issues_by_severity.get('medium', 0)} |
| Low | {self.report.issues_by_severity.get('low', 0)} |

## Issues by Category

"""
        for category, count in sorted(self.report.issues_by_category.items(), key=lambda x: x[1], reverse=True):
            md += f"- **{category.title()}:** {count} issues\n"
        
        if self.report.recommendations:
            md += "\n## 💡 Recommendations\n\n"
            for rec in self.report.recommendations:
                md += f"- {rec}\n"
        
        if self.report.ai_insights:
            md += "\n## 🤖 AI Insights\n\n"
            for insight in self.report.ai_insights:
                md += f"- {insight}\n"
        
        md += "\n## Detailed Issues\n\n"
        
        for severity in ['critical', 'high', 'medium', 'low']:
            severity_issues = [i for i in self.report.issues if i.severity == severity]
            if severity_issues:
                md += f"\n### {severity.title()} Priority ({len(severity_issues)} issues)\n\n"
                for issue in severity_issues[:25]:  # Limit per severity
                    md += f"""
#### {issue.issue_type.replace('_', ' ').title()}

- **File:** `{issue.file_path}`{f' (Line {issue.line_number})' if issue.line_number else ''}
- **Category:** {issue.category}
- **Issue:** {issue.description}
- **Suggestion:** {issue.suggestion}
{f'- **Context:** `{issue.context}`' if issue.context else ''}

---

"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(md)
        
        print(f"\n📄 Markdown report exported to: {output_path}")
        return output_path


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Documentation Quality Analyzer with Mintlify support'
    )
    
    # Repository specification
    parser.add_argument(
        'docs_path',
        nargs='?',
        help='Path to documentation directory (optional if using --config)'
    )
    
    parser.add_argument(
        '--config',
        help='Path to configuration file (YAML)',
        default=None
    )
    
    parser.add_argument(
        '--repo-url',
        help='Remote repository URL (clone and analyze)',
        default=None
    )
    
    parser.add_argument(
        '--repo-type',
        choices=['auto', 'mintlify', 'docusaurus', 'mkdocs', 'generic'],
        default='auto',
        help='Documentation platform type'
    )

    parser.add_argument(
        '--repo-root',
        help='Repository root for platform detection (if analyzing subfolder). Auto-detects by default.',
        default=None
    )

    # Output options
    parser.add_argument(
        '--format',
        choices=['json', 'html', 'markdown', 'all'],
        default='html',
        help='Output format for report'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path',
        default=None
    )
    
    # Analysis options
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Disable AI-powered analysis (faster but less comprehensive)'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    if args.config:
        with open(args.config, 'r') as f:
            config = yaml.safe_load(f)
    elif os.path.exists('config.yaml'):
        # Load config.yaml by default if it exists
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {'repository': {}, 'analysis': {}}
    
    # Determine repository path
    if args.repo_url:
        config['repository']['remote'] = {
            'enabled': True,
            'url': args.repo_url,
            'branch': 'main'
        }
        docs_path = None  # Will be cloned
    elif args.docs_path:
        docs_path = args.docs_path
        config['repository']['path'] = docs_path
    elif 'repository' in config and 'path' in config['repository']:
        docs_path = config['repository']['path']
    else:
        parser.error("Must specify docs_path, --config with repository.path, or --repo-url")
    
    # Override config with CLI args
    if args.repo_type != 'auto':
        config['repository']['type'] = args.repo_type

    if args.repo_root:
        config['repository']['root'] = args.repo_root

    if args.no_ai:
        config['analysis']['enable_ai_analysis'] = False
        config['gap_detection'] = config.get('gap_detection', {})
        config['gap_detection']['semantic_analysis'] = {'enabled': False}
    
    # Initialize repository manager
    repo_manager = RepositoryManager(config)
    
    # Handle remote cloning
    if config.get('repository', {}).get('remote', {}).get('enabled'):
        print("📥 Cloning remote repository...")
        repo_manager.repo_path = repo_manager.clone_remote_repo()
    
    # Load platform config
    repo_manager.platform_config = repo_manager.load_platform_config()
    
    print(f"📁 Repository: {repo_manager.repo_path}")
    print(f"🔧 Platform: {repo_manager.repo_type}")
    
    # Initialize analyzer
    analyzer = DocumentationAnalyzer(repo_manager, config)
    
    # Run analysis
    report = analyzer.analyze_all()
    
    # Export report
    if args.format == 'all':
        analyzer.export_report('json', args.output)
        analyzer.export_report('html', args.output)
        analyzer.export_report('markdown', args.output)
    else:
        analyzer.export_report(args.format, args.output)
    
    # Print summary
    print(f"\n✅ Analysis complete!")
    print(f"   Repository: {repo_manager.repo_type}")
    print(f"   Total files: {report.total_files}")
    print(f"   Total issues: {report.total_issues}")
    print(f"   Critical: {report.issues_by_severity.get('critical', 0)}")
    print(f"   High: {report.issues_by_severity.get('high', 0)}")
    print(f"   Medium: {report.issues_by_severity.get('medium', 0)}")
    print(f"   Low: {report.issues_by_severity.get('low', 0)}")
    
    if report.ai_insights:
        print(f"   AI Insights: {len(report.ai_insights)}")


if __name__ == '__main__':
    main()
