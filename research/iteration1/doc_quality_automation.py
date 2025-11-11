#!/usr/bin/env python3
"""
Documentation Quality Automation Engine
Automates detection, fixing, and monitoring of documentation quality issues.

This system implements the comprehensive improvements identified in the
Claude Documentation Analysis, with automated fixing where possible and
manual review workflows for complex changes.
"""

import os
import re
import json
import logging
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from collections import defaultdict
import anthropic
import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class Issue:
    """Represents a documentation quality issue."""
    id: str
    category: str  # IA, consistency, completeness, UX, platform
    severity: str  # critical, high, medium, low
    type: str  # duplicate_content, terminology, missing_section, etc.
    file_path: str
    line_number: Optional[int]
    description: str
    auto_fixable: bool
    suggested_fix: Optional[str]
    detected_at: str
    fixed_at: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class Metric:
    """Represents a tracked metric."""
    name: str
    value: float
    timestamp: str
    category: str
    metadata: Optional[Dict] = None


class MetricsDatabase:
    """Stores and retrieves metrics and issues over time."""
    
    def __init__(self, db_path: str = "doc_quality_metrics.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self._initialize_schema()
    
    def _initialize_schema(self):
        """Create database tables if they don't exist."""
        cursor = self.conn.cursor()
        
        # Issues table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id TEXT PRIMARY KEY,
                category TEXT,
                severity TEXT,
                type TEXT,
                file_path TEXT,
                line_number INTEGER,
                description TEXT,
                auto_fixable BOOLEAN,
                suggested_fix TEXT,
                detected_at TEXT,
                fixed_at TEXT
            )
        """)
        
        # Metrics table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                value REAL,
                timestamp TEXT,
                category TEXT,
                metadata TEXT
            )
        """)
        
        # Audit log
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action TEXT,
                details TEXT,
                user TEXT
            )
        """)
        
        self.conn.commit()
    
    def save_issue(self, issue: Issue):
        """Save or update an issue."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO issues 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            issue.id, issue.category, issue.severity, issue.type,
            issue.file_path, issue.line_number, issue.description,
            issue.auto_fixable, issue.suggested_fix, 
            issue.detected_at, issue.fixed_at
        ))
        self.conn.commit()
    
    def save_metric(self, metric: Metric):
        """Save a metric measurement."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO metrics (name, value, timestamp, category, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            metric.name, metric.value, metric.timestamp, metric.category,
            json.dumps(metric.metadata) if metric.metadata else None
        ))
        self.conn.commit()
    
    def get_open_issues(self) -> List[Issue]:
        """Get all unresolved issues."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM issues WHERE fixed_at IS NULL")
        rows = cursor.fetchall()
        return [self._row_to_issue(row) for row in rows]
    
    def get_metrics_history(self, metric_name: str, days: int = 30) -> List[Tuple[str, float]]:
        """Get metric history for the last N days."""
        cursor = self.conn.cursor()
        since = (datetime.now() - timedelta(days=days)).isoformat()
        cursor.execute("""
            SELECT timestamp, value FROM metrics 
            WHERE name = ? AND timestamp > ?
            ORDER BY timestamp
        """, (metric_name, since))
        return cursor.fetchall()
    
    def log_action(self, action: str, details: str, user: str = "system"):
        """Log an action to audit trail."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO audit_log (timestamp, action, details, user)
            VALUES (?, ?, ?, ?)
        """, (datetime.now().isoformat(), action, details, user))
        self.conn.commit()
    
    @staticmethod
    def _row_to_issue(row) -> Issue:
        """Convert database row to Issue object."""
        return Issue(
            id=row[0], category=row[1], severity=row[2], type=row[3],
            file_path=row[4], line_number=row[5], description=row[6],
            auto_fixable=bool(row[7]), suggested_fix=row[8],
            detected_at=row[9], fixed_at=row[10]
        )
    
    def close(self):
        """Close database connection."""
        self.conn.close()


class TerminologyChecker:
    """Detects and fixes terminology inconsistencies."""
    
    def __init__(self, config: Dict):
        self.preferred_terms = config.get('terminology', {}).get('preferred_terms', {})
        self.deprecated_terms = config.get('terminology', {}).get('deprecated_terms', [])
        self.case_sensitive = config.get('terminology', {}).get('case_sensitive', False)
    
    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check a file for terminology issues."""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for deprecated terms
            for deprecated in self.deprecated_terms:
                pattern = re.compile(
                    re.escape(deprecated) if self.case_sensitive 
                    else re.escape(deprecated), 
                    re.IGNORECASE if not self.case_sensitive else 0
                )
                
                if pattern.search(line):
                    replacement = self.preferred_terms.get(deprecated.lower(), None)
                    issues.append(Issue(
                        id=f"term_{file_path}_{line_num}_{deprecated}",
                        category="consistency",
                        severity="high" if deprecated.lower() == "claude code sdk" else "medium",
                        type="terminology",
                        file_path=file_path,
                        line_number=line_num,
                        description=f"Deprecated term '{deprecated}' found",
                        auto_fixable=True if replacement else False,
                        suggested_fix=f"Replace '{deprecated}' with '{replacement}'" if replacement else None,
                        detected_at=datetime.now().isoformat()
                    ))
        
        return issues
    
    def auto_fix(self, file_path: str, content: str, issues: List[Issue]) -> str:
        """Automatically fix terminology issues."""
        fixed_content = content
        
        for issue in issues:
            if issue.auto_fixable and issue.type == "terminology":
                # Extract old and new terms from suggested fix
                match = re.search(r"Replace '(.+?)' with '(.+?)'", issue.suggested_fix)
                if match:
                    old_term, new_term = match.groups()
                    pattern = re.compile(
                        re.escape(old_term),
                        re.IGNORECASE if not self.case_sensitive else 0
                    )
                    fixed_content = pattern.sub(new_term, fixed_content)
        
        return fixed_content


class DuplicateContentDetector:
    """Detects duplicate and scattered content."""
    
    def __init__(self, config: Dict):
        self.similarity_threshold = config.get('duplication', {}).get('threshold', 0.8)
        self.known_duplicates = config.get('duplication', {}).get('known_patterns', [])
    
    def check_repository(self, repo_path: str) -> List[Issue]:
        """Check entire repository for duplicate content."""
        issues = []
        
        # Check for known duplicate content patterns
        for duplicate_pattern in self.known_duplicates:
            locations = duplicate_pattern.get('locations', [])
            if len(locations) > 1:
                canonical = duplicate_pattern.get('canonical', locations[0])
                
                for location in locations:
                    if location != canonical:
                        full_path = os.path.join(repo_path, location)
                        if os.path.exists(full_path):
                            issues.append(Issue(
                                id=f"dup_{location.replace('/', '_')}",
                                category="information_architecture",
                                severity="critical",
                                type="duplicate_content",
                                file_path=location,
                                line_number=None,
                                description=f"Duplicate content path. Canonical: {canonical}",
                                auto_fixable=False,  # Requires review
                                suggested_fix=f"Convert to navigation pointer to {canonical}",
                                detected_at=datetime.now().isoformat()
                            ))
        
        return issues


class FrontmatterValidator:
    """Validates and fixes MDX frontmatter."""
    
    def __init__(self, config: Dict):
        self.required_fields = config.get('frontmatter', {}).get('required', ['title', 'description'])
        self.optional_fields = config.get('frontmatter', {}).get('optional', [])
        self.max_description_length = config.get('frontmatter', {}).get('max_description_length', 160)
    
    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check frontmatter in an MDX file."""
        issues = []
        
        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        
        if not frontmatter_match:
            issues.append(Issue(
                id=f"fm_{file_path}_missing",
                category="platform",
                severity="critical",
                type="missing_frontmatter",
                file_path=file_path,
                line_number=1,
                description="Missing frontmatter in MDX file",
                auto_fixable=True,
                suggested_fix="Add default frontmatter block",
                detected_at=datetime.now().isoformat()
            ))
            return issues
        
        # Parse frontmatter YAML
        try:
            frontmatter = yaml.safe_load(frontmatter_match.group(1))
        except yaml.YAMLError:
            issues.append(Issue(
                id=f"fm_{file_path}_invalid",
                category="platform",
                severity="critical",
                type="invalid_frontmatter",
                file_path=file_path,
                line_number=1,
                description="Invalid YAML in frontmatter",
                auto_fixable=False,
                suggested_fix="Fix YAML syntax",
                detected_at=datetime.now().isoformat()
            ))
            return issues
        
        # Check required fields
        for field in self.required_fields:
            if field not in frontmatter or not frontmatter[field]:
                issues.append(Issue(
                    id=f"fm_{file_path}_{field}",
                    category="platform",
                    severity="high",
                    type="missing_frontmatter_field",
                    file_path=file_path,
                    line_number=None,
                    description=f"Missing required frontmatter field: {field}",
                    auto_fixable=True,
                    suggested_fix=f"Add {field} field to frontmatter",
                    detected_at=datetime.now().isoformat()
                ))
        
        # Check description length
        if 'description' in frontmatter:
            desc_len = len(frontmatter['description'])
            if desc_len > self.max_description_length:
                issues.append(Issue(
                    id=f"fm_{file_path}_desc_length",
                    category="platform",
                    severity="medium",
                    type="frontmatter_seo",
                    file_path=file_path,
                    line_number=None,
                    description=f"Description too long ({desc_len} > {self.max_description_length})",
                    auto_fixable=False,
                    suggested_fix="Shorten description to improve SEO",
                    detected_at=datetime.now().isoformat()
                ))
        
        return issues
    
    def auto_fix(self, file_path: str, content: str, issues: List[Issue]) -> str:
        """Auto-fix frontmatter issues where possible."""
        # Check if file needs frontmatter added
        if not re.match(r'^---\n', content):
            # Generate default frontmatter from file path
            title = Path(file_path).stem.replace('-', ' ').replace('_', ' ').title()
            frontmatter = f"---\ntitle: {title}\ndescription: TODO - Add description\n---\n\n"
            return frontmatter + content
        
        return content


class CodeExampleEnhancer:
    """Enhances code examples with error handling."""
    
    def __init__(self, config: Dict):
        self.languages = config.get('code_examples', {}).get('languages', ['python', 'typescript'])
    
    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check code examples for missing error handling."""
        issues = []
        
        # Find all code blocks
        code_blocks = re.finditer(r'```(\w+)\n(.*?)```', content, re.DOTALL)
        
        for block in code_blocks:
            language = block.group(1)
            code = block.group(2)
            
            if language in self.languages:
                # Check for error handling
                has_try_catch = 'try:' in code or 'try {' in code or 'catch' in code
                
                # Check if it's making API calls (likely needs error handling)
                makes_api_calls = any(keyword in code for keyword in [
                    'client.', 'fetch(', 'requests.', 'axios.'
                ])
                
                if makes_api_calls and not has_try_catch:
                    issues.append(Issue(
                        id=f"code_{file_path}_{block.start()}",
                        category="completeness",
                        severity="medium",
                        type="missing_error_handling",
                        file_path=file_path,
                        line_number=content[:block.start()].count('\n') + 1,
                        description=f"{language} code example missing error handling",
                        auto_fixable=False,  # Requires understanding context
                        suggested_fix="Add try-catch block with appropriate error handling",
                        detected_at=datetime.now().isoformat()
                    ))
        
        return issues


class LinkValidator:
    """Validates internal and external links."""
    
    def __init__(self, config: Dict):
        self.repo_path = config.get('repository', {}).get('path', '.')
        self.check_external = config.get('links', {}).get('check_external', False)
    
    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check all links in a file."""
        issues = []
        
        # Find all markdown links
        links = re.finditer(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        
        for link in links:
            link_text = link.group(1)
            link_url = link.group(2)
            
            # Check for empty link text
            if not link_text or link_text.strip() in ['here', 'click here', 'link']:
                issues.append(Issue(
                    id=f"link_{file_path}_{link.start()}_text",
                    category="user_experience",
                    severity="medium",
                    type="poor_link_text",
                    file_path=file_path,
                    line_number=content[:link.start()].count('\n') + 1,
                    description=f"Poor link text: '{link_text}'",
                    auto_fixable=False,
                    suggested_fix="Use descriptive link text",
                    detected_at=datetime.now().isoformat()
                ))
            
            # Check internal links
            if not link_url.startswith(('http://', 'https://', '#')):
                # Resolve relative path
                full_path = os.path.join(
                    os.path.dirname(file_path),
                    link_url
                )
                full_path = os.path.normpath(full_path)
                
                if not os.path.exists(os.path.join(self.repo_path, full_path)):
                    issues.append(Issue(
                        id=f"link_{file_path}_{link.start()}_broken",
                        category="user_experience",
                        severity="high",
                        type="broken_link",
                        file_path=file_path,
                        line_number=content[:link.start()].count('\n') + 1,
                        description=f"Broken internal link: {link_url}",
                        auto_fixable=False,
                        suggested_fix="Fix or remove broken link",
                        detected_at=datetime.now().isoformat()
                    ))
        
        return issues


class MetricsCollector:
    """Collects and tracks documentation quality metrics."""
    
    def __init__(self, db: MetricsDatabase):
        self.db = db
    
    def collect_all_metrics(self, repo_path: str, issues: List[Issue]) -> Dict[str, float]:
        """Collect all current metrics."""
        metrics = {}
        timestamp = datetime.now().isoformat()
        
        # Issue counts by severity
        severity_counts = defaultdict(int)
        for issue in issues:
            severity_counts[issue.severity] += 1
        
        metrics['critical_issues'] = severity_counts['critical']
        metrics['high_issues'] = severity_counts['high']
        metrics['medium_issues'] = severity_counts['medium']
        metrics['low_issues'] = severity_counts['low']
        metrics['total_issues'] = len(issues)
        
        # Auto-fixable rate
        auto_fixable = sum(1 for i in issues if i.auto_fixable)
        metrics['auto_fixable_rate'] = auto_fixable / len(issues) if issues else 0
        
        # File-level metrics
        file_count = self._count_files(repo_path)
        metrics['total_files'] = file_count
        metrics['issues_per_file'] = len(issues) / file_count if file_count else 0
        
        # Category breakdown
        category_counts = defaultdict(int)
        for issue in issues:
            category_counts[issue.category] += 1
        
        for category, count in category_counts.items():
            metrics[f'{category}_issues'] = count
        
        # Save all metrics
        for name, value in metrics.items():
            self.db.save_metric(Metric(
                name=name,
                value=value,
                timestamp=timestamp,
                category='quality'
            ))
        
        return metrics
    
    @staticmethod
    def _count_files(repo_path: str) -> int:
        """Count documentation files in repository."""
        count = 0
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(('.md', '.mdx')):
                    count += 1
        return count
    
    def calculate_trends(self, metric_name: str, days: int = 30) -> Dict[str, Any]:
        """Calculate trend for a metric."""
        history = self.db.get_metrics_history(metric_name, days)
        
        if len(history) < 2:
            return {'trend': 'insufficient_data'}
        
        first_value = history[0][1]
        last_value = history[-1][1]
        change = last_value - first_value
        percent_change = (change / first_value * 100) if first_value != 0 else 0
        
        return {
            'first_value': first_value,
            'last_value': last_value,
            'change': change,
            'percent_change': percent_change,
            'trend': 'improving' if change < 0 else 'degrading',
            'data_points': len(history)
        }


class DocumentationQualityEngine:
    """Main engine coordinating all quality checks and fixes."""
    
    def __init__(self, config_path: str = "quality_config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.db = MetricsDatabase(self.config['database']['path'])
        self.repo_path = self.config['repository']['path']
        
        # Initialize checkers
        self.terminology_checker = TerminologyChecker(self.config)
        self.duplicate_detector = DuplicateContentDetector(self.config)
        self.frontmatter_validator = FrontmatterValidator(self.config)
        self.code_enhancer = CodeExampleEnhancer(self.config)
        self.link_validator = LinkValidator(self.config)
        self.metrics_collector = MetricsCollector(self.db)
    
    def scan_repository(self) -> List[Issue]:
        """Scan entire repository for issues."""
        logger.info(f"Scanning repository: {self.repo_path}")
        all_issues = []
        
        # Repository-level checks
        all_issues.extend(self.duplicate_detector.check_repository(self.repo_path))
        
        # File-level checks
        for root, dirs, files in os.walk(self.repo_path):
            for file in files:
                if file.endswith(('.md', '.mdx')):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.repo_path)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Run all checks
                        all_issues.extend(self.terminology_checker.check_file(rel_path, content))
                        all_issues.extend(self.frontmatter_validator.check_file(rel_path, content))
                        all_issues.extend(self.code_enhancer.check_file(rel_path, content))
                        all_issues.extend(self.link_validator.check_file(rel_path, content))
                        
                    except Exception as e:
                        logger.error(f"Error scanning {rel_path}: {e}")
        
        # Save issues to database
        for issue in all_issues:
            self.db.save_issue(issue)
        
        logger.info(f"Scan complete. Found {len(all_issues)} issues.")
        return all_issues
    
    def auto_fix_issues(self, dry_run: bool = True) -> Dict[str, int]:
        """Automatically fix issues where possible."""
        logger.info(f"Running auto-fix (dry_run={dry_run})")
        
        issues = self.db.get_open_issues()
        auto_fixable = [i for i in issues if i.auto_fixable]
        
        stats = {'fixed': 0, 'failed': 0, 'skipped': 0}
        
        # Group by file
        by_file = defaultdict(list)
        for issue in auto_fixable:
            by_file[issue.file_path].append(issue)
        
        for file_path, file_issues in by_file.items():
            full_path = os.path.join(self.repo_path, file_path)
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                fixed_content = original_content
                
                # Apply fixes based on issue type
                for issue in file_issues:
                    if issue.type == "terminology":
                        fixed_content = self.terminology_checker.auto_fix(
                            file_path, fixed_content, [issue]
                        )
                    elif issue.type in ["missing_frontmatter", "missing_frontmatter_field"]:
                        fixed_content = self.frontmatter_validator.auto_fix(
                            file_path, fixed_content, [issue]
                        )
                
                if fixed_content != original_content:
                    if not dry_run:
                        with open(full_path, 'w', encoding='utf-8') as f:
                            f.write(fixed_content)
                        
                        # Mark issues as fixed
                        for issue in file_issues:
                            issue.fixed_at = datetime.now().isoformat()
                            self.db.save_issue(issue)
                        
                        self.db.log_action(
                            'auto_fix',
                            f"Fixed {len(file_issues)} issues in {file_path}"
                        )
                    
                    stats['fixed'] += len(file_issues)
                    logger.info(f"Fixed {len(file_issues)} issues in {file_path}")
                else:
                    stats['skipped'] += len(file_issues)
            
            except Exception as e:
                logger.error(f"Error fixing {file_path}: {e}")
                stats['failed'] += len(file_issues)
        
        return stats
    
    def collect_metrics(self) -> Dict[str, float]:
        """Collect current metrics."""
        issues = self.db.get_open_issues()
        return self.metrics_collector.collect_all_metrics(self.repo_path, issues)
    
    def generate_report(self, output_path: str = "quality_report.md"):
        """Generate comprehensive quality report."""
        logger.info(f"Generating report: {output_path}")
        
        issues = self.db.get_open_issues()
        metrics = self.collect_metrics()
        
        # Group issues
        by_category = defaultdict(list)
        by_severity = defaultdict(list)
        
        for issue in issues:
            by_category[issue.category].append(issue)
            by_severity[issue.severity].append(issue)
        
        # Build report
        report = []
        report.append("# Documentation Quality Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Repository:** {self.repo_path}\n")
        
        # Executive summary
        report.append("## Executive Summary\n")
        report.append(f"- **Total Issues:** {len(issues)}")
        report.append(f"- **Critical:** {metrics.get('critical_issues', 0)}")
        report.append(f"- **High:** {metrics.get('high_issues', 0)}")
        report.append(f"- **Medium:** {metrics.get('medium_issues', 0)}")
        report.append(f"- **Low:** {metrics.get('low_issues', 0)}")
        report.append(f"- **Auto-fixable:** {int(metrics.get('auto_fixable_rate', 0) * 100)}%\n")
        
        # Trends
        report.append("## Trends\n")
        for metric_name in ['total_issues', 'critical_issues']:
            trend = self.metrics_collector.calculate_trends(metric_name, days=30)
            if trend.get('trend') != 'insufficient_data':
                report.append(f"### {metric_name}")
                report.append(f"- Change: {trend['change']:+.0f} ({trend['percent_change']:+.1f}%)")
                report.append(f"- Trend: {trend['trend']}\n")
        
        # Issues by category
        report.append("## Issues by Category\n")
        for category, cat_issues in sorted(by_category.items()):
            report.append(f"### {category.replace('_', ' ').title()} ({len(cat_issues)})\n")
            
            # Top 5 issues
            for issue in cat_issues[:5]:
                report.append(f"**{issue.severity.upper()}:** {issue.description}")
                report.append(f"- File: `{issue.file_path}`")
                if issue.suggested_fix:
                    report.append(f"- Fix: {issue.suggested_fix}")
                report.append("")
            
            if len(cat_issues) > 5:
                report.append(f"*...and {len(cat_issues) - 5} more*\n")
        
        # Recommendations
        report.append("## Recommended Actions\n")
        
        critical = by_severity.get('critical', [])
        if critical:
            report.append(f"1. **URGENT:** Fix {len(critical)} critical issues immediately")
            for issue in critical[:3]:
                report.append(f"   - {issue.description} in `{issue.file_path}`")
        
        auto_fixable = [i for i in issues if i.auto_fixable]
        if auto_fixable:
            report.append(f"2. Run auto-fix to resolve {len(auto_fixable)} issues automatically")
        
        report.append(f"3. Review and address {len(by_severity.get('high', []))} high-priority issues")
        
        # Write report
        with open(output_path, 'w') as f:
            f.write('\n'.join(report))
        
        logger.info(f"Report written to {output_path}")
        return output_path
    
    def close(self):
        """Clean up resources."""
        self.db.close()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Documentation Quality Automation Engine'
    )
    parser.add_argument(
        'action',
        choices=['scan', 'fix', 'report', 'metrics'],
        help='Action to perform'
    )
    parser.add_argument(
        '--config',
        default='quality_config.yaml',
        help='Configuration file path'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be fixed without making changes'
    )
    parser.add_argument(
        '--output',
        default='quality_report.md',
        help='Output file for reports'
    )
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = DocumentationQualityEngine(args.config)
    
    try:
        if args.action == 'scan':
            issues = engine.scan_repository()
            print(f"\n✅ Scan complete. Found {len(issues)} issues.")
            
            # Show summary
            by_severity = defaultdict(int)
            for issue in issues:
                by_severity[issue.severity] += 1
            
            print("\nSummary:")
            for severity in ['critical', 'high', 'medium', 'low']:
                count = by_severity.get(severity, 0)
                if count > 0:
                    print(f"  {severity.upper()}: {count}")
        
        elif args.action == 'fix':
            stats = engine.auto_fix_issues(dry_run=args.dry_run)
            mode = "Would fix" if args.dry_run else "Fixed"
            print(f"\n✅ {mode} {stats['fixed']} issues")
            if stats['failed'] > 0:
                print(f"⚠️  Failed to fix {stats['failed']} issues")
        
        elif args.action == 'report':
            output = engine.generate_report(args.output)
            print(f"\n✅ Report generated: {output}")
        
        elif args.action == 'metrics':
            metrics = engine.collect_metrics()
            print("\n📊 Current Metrics:")
            for name, value in sorted(metrics.items()):
                print(f"  {name}: {value:.2f}")
    
    finally:
        engine.close()


if __name__ == '__main__':
    main()
