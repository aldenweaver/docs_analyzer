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
import time
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

# Import analyzer modules
from analyzers import (
    RepositoryManager,
    MDXParser,
    MintlifyValidator,
    SemanticAnalyzer,
    ContentDuplicationDetector,
    UserJourneyAnalyzer
)


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

    def _recalculate_summary(self):
        """Recalculate summary stats from actual issues list (fixes Phase 3 count bug)"""
        actual_total = len(self.report.issues)
        actual_by_severity = {}
        actual_by_category = {}
        for issue in self.report.issues:
            actual_by_severity[issue.severity] = actual_by_severity.get(issue.severity, 0) + 1
            actual_by_category[issue.category] = actual_by_category.get(issue.category, 0) + 1
        return actual_total, actual_by_severity, actual_by_category

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
        elif Path(output_path).is_dir():
            # If output_path is a directory, use default filename in that directory
            output_path = str(Path(output_path) / 'doc_analysis_report.json')

        # Recalculate summary stats from actual issues list
        actual_total, actual_by_severity, actual_by_category = self._recalculate_summary()

        report_data = {
            'timestamp': self.report.timestamp,
            'repository': self.report.repository_info,
            'summary': {
                'total_files': self.report.total_files,
                'total_issues': actual_total,
                'by_severity': actual_by_severity,
                'by_category': actual_by_category,
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
        elif Path(output_path).is_dir():
            # If output_path is a directory, use default filename in that directory
            output_path = str(Path(output_path) / 'doc_analysis_report.html')

        # Use HTML template with AI insights
        html = self._generate_html_report()

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"\n📄 HTML report exported to: {output_path}")
        return output_path
    
    def _generate_html_report(self) -> str:
        """Generate HTML report"""
        # Recalculate summary stats from actual issues list
        actual_total, actual_by_severity, actual_by_category = self._recalculate_summary()

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
            <div class="stat-number">{actual_total}</div>
        </div>
        <div class="stat-card">
            <div>Critical</div>
            <div class="stat-number critical">{actual_by_severity.get('critical', 0)}</div>
        </div>
        <div class="stat-card">
            <div>High</div>
            <div class="stat-number high">{actual_by_severity.get('high', 0)}</div>
        </div>
        <div class="stat-card">
            <div>Medium</div>
            <div class="stat-number medium">{actual_by_severity.get('medium', 0)}</div>
        </div>
        <div class="stat-card">
            <div>Low</div>
            <div class="stat-number low">{actual_by_severity.get('low', 0)}</div>
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
        elif Path(output_path).is_dir():
            # If output_path is a directory, use default filename in that directory
            output_path = str(Path(output_path) / 'doc_analysis_report.md')

        # Recalculate summary stats from actual issues list
        actual_total, actual_by_severity, actual_by_category = self._recalculate_summary()

        md = f"""# Documentation Analysis Report

**Generated:** {self.report.timestamp}
**Repository:** {self.report.repository_info.get('path')}
**Platform:** {self.report.repository_info.get('type')}
**Files Analyzed:** {self.report.total_files}
**Total Issues:** {actual_total}

## Summary

| Severity | Count |
|----------|-------|
| Critical | {actual_by_severity.get('critical', 0)} |
| High | {actual_by_severity.get('high', 0)} |
| Medium | {actual_by_severity.get('medium', 0)} |
| Low | {actual_by_severity.get('low', 0)} |

## Issues by Category

"""
        for category, count in sorted(actual_by_category.items(), key=lambda x: x[1], reverse=True):
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
        default='all',
        help='Output format for report (default: all formats)'
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
