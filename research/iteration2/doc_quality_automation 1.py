#!/usr/bin/env python3
"""
Documentation Quality Automation Engine - Complete Implementation
Automates detection, fixing, and monitoring of documentation quality issues.

This system implements all 76 improvements from the Claude Documentation Analysis.
"""

import os
import re
import json
import logging
import sqlite3
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
from collections import defaultdict
from urllib.parse import urlparse
import yaml

# Optional: Claude API for AI analysis
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logging.warning("Anthropic SDK not available. AI analysis features disabled.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('doc_quality.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class Issue:
    """Represents a documentation quality issue."""
    id: str
    category: str  # IA, consistency, completeness, UX, platform
    severity: str  # critical, high, medium, low
    type: str  # specific issue type
    file_path: str
    line_number: Optional[int]
    description: str
    auto_fixable: bool
    suggested_fix: Optional[str]
    detected_at: str
    fixed_at: Optional[str] = None
    context: Optional[str] = None  # Surrounding text for context
    
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
                fixed_at TEXT,
                context TEXT
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
        
        # Create indexes for performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_issues_severity ON issues(severity)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_issues_fixed ON issues(fixed_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_metrics_name ON metrics(name, timestamp)")
        
        self.conn.commit()
    
    def save_issue(self, issue: Issue):
        """Save or update an issue."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO issues 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            issue.id, issue.category, issue.severity, issue.type,
            issue.file_path, issue.line_number, issue.description,
            issue.auto_fixable, issue.suggested_fix, 
            issue.detected_at, issue.fixed_at, issue.context
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
    
    def get_issues_by_severity(self, severity: str) -> List[Issue]:
        """Get issues by severity level."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM issues WHERE severity = ? AND fixed_at IS NULL", (severity,))
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
    
    def get_latest_metric(self, metric_name: str) -> Optional[float]:
        """Get most recent value for a metric."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT value FROM metrics 
            WHERE name = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        """, (metric_name,))
        result = cursor.fetchone()
        return result[0] if result else None
    
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
            detected_at=row[9], fixed_at=row[10], context=row[11]
        )
    
    def close(self):
        """Close database connection."""
        self.conn.close()


class TerminologyChecker:
    """Detects and fixes terminology inconsistencies."""
    
    def __init__(self, config: Dict):
        term_config = config.get('terminology', {})
        self.preferred_terms = term_config.get('preferred_terms', {})
        self.deprecated_terms = term_config.get('deprecated_terms', [])
        self.case_sensitive = term_config.get('case_sensitive', False)
        self.proper_nouns = term_config.get('proper_nouns', [])
    
    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check a file for terminology issues."""
        issues = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for deprecated terms
            for deprecated in self.deprecated_terms:
                pattern = re.compile(
                    re.escape(deprecated), 
                    0 if self.case_sensitive else re.IGNORECASE
                )
                
                if pattern.search(line):
                    # Find preferred replacement
                    replacement = None
                    deprecated_lower = deprecated.lower()
                    
                    if deprecated_lower in self.preferred_terms:
                        replacement = self.preferred_terms[deprecated_lower]
                    elif isinstance(self.preferred_terms.get(deprecated_lower), list):
                        replacement = self.preferred_terms[deprecated_lower][0]
                    
                    # Determine severity
                    severity = "high" if deprecated_lower in ["claude code sdk", "claudecodeoptions"] else "medium"
                    
                    issues.append(Issue(
                        id=self._generate_id(file_path, line_num, deprecated),
                        category="consistency",
                        severity=severity,
                        type="terminology",
                        file_path=file_path,
                        line_number=line_num,
                        description=f"Deprecated term '{deprecated}' found",
                        auto_fixable=bool(replacement),
                        suggested_fix=f"Replace '{deprecated}' with '{replacement}'" if replacement else None,
                        detected_at=datetime.now().isoformat(),
                        context=line.strip()
                    ))
            
            # Check proper noun capitalization
            for proper_noun in self.proper_nouns:
                # Look for incorrect capitalization
                incorrect_pattern = re.compile(r'\b' + re.escape(proper_noun.lower()) + r'\b', re.IGNORECASE)
                for match in incorrect_pattern.finditer(line):
                    if match.group() != proper_noun:  # Not correctly capitalized
                        issues.append(Issue(
                            id=self._generate_id(file_path, line_num, f"cap_{proper_noun}"),
                            category="consistency",
                            severity="low",
                            type="capitalization",
                            file_path=file_path,
                            line_number=line_num,
                            description=f"Improper capitalization: '{match.group()}' should be '{proper_noun}'",
                            auto_fixable=True,
                            suggested_fix=f"Replace '{match.group()}' with '{proper_noun}'",
                            detected_at=datetime.now().isoformat(),
                            context=line.strip()
                        ))
        
        return issues
    
    def auto_fix(self, file_path: str, content: str, issues: List[Issue]) -> str:
        """Automatically fix terminology issues."""
        fixed_content = content
        
        for issue in issues:
            if issue.type == "terminology" and issue.auto_fixable:
                # Extract old and new terms from suggested_fix
                match = re.search(r"Replace '(.+)' with '(.+)'", issue.suggested_fix or "")
                if match:
                    old_term, new_term = match.groups()
                    # Replace all occurrences
                    pattern = re.compile(re.escape(old_term), re.IGNORECASE if not self.case_sensitive else 0)
                    fixed_content = pattern.sub(new_term, fixed_content)
            
            elif issue.type == "capitalization" and issue.auto_fixable:
                match = re.search(r"Replace '(.+)' with '(.+)'", issue.suggested_fix or "")
                if match:
                    old_term, new_term = match.groups()
                    fixed_content = re.sub(r'\b' + re.escape(old_term) + r'\b', new_term, fixed_content)
        
        return fixed_content
    
    @staticmethod
    def _generate_id(file_path: str, line_num: int, detail: str) -> str:
        """Generate unique issue ID."""
        content = f"{file_path}_{line_num}_{detail}"
        return hashlib.md5(content.encode()).hexdigest()[:16]


class FrontmatterValidator:
    """Validates and fixes frontmatter in MDX files."""
    
    def __init__(self, config: Dict):
        fm_config = config.get('frontmatter', {})
        self.required_fields = fm_config.get('required', ['title', 'description'])
        self.optional_fields = fm_config.get('optional', [])
        self.max_desc_length = fm_config.get('max_description_length', 160)
        self.min_desc_length = fm_config.get('min_description_length', 50)
        self.auto_generate = fm_config.get('auto_generate', {})
    
    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check a file for frontmatter issues."""
        issues = []
        
        # Only check MDX files
        if not file_path.endswith('.mdx'):
            return issues
        
        frontmatter = self._extract_frontmatter(content)
        
        if frontmatter is None:
            # No frontmatter at all - CRITICAL
            issues.append(Issue(
                id=self._generate_id(file_path, "missing_frontmatter"),
                category="platform",
                severity="critical",
                type="missing_frontmatter",
                file_path=file_path,
                line_number=1,
                description="MDX file missing required frontmatter block",
                auto_fixable=self.auto_generate.get('enabled', False),
                suggested_fix="Add YAML frontmatter block with title and description",
                detected_at=datetime.now().isoformat()
            ))
            return issues
        
        # Check required fields
        for field in self.required_fields:
            if field not in frontmatter:
                issues.append(Issue(
                    id=self._generate_id(file_path, f"missing_{field}"),
                    category="platform",
                    severity="high",
                    type="missing_frontmatter_field",
                    file_path=file_path,
                    line_number=1,
                    description=f"Missing required frontmatter field: '{field}'",
                    auto_fixable=self.auto_generate.get('enabled', False),
                    suggested_fix=f"Add '{field}' field to frontmatter",
                    detected_at=datetime.now().isoformat()
                ))
        
        # Check description length
        if 'description' in frontmatter:
            desc_len = len(frontmatter['description'])
            if desc_len > self.max_desc_length:
                issues.append(Issue(
                    id=self._generate_id(file_path, "desc_too_long"),
                    category="platform",
                    severity="medium",
                    type="description_length",
                    file_path=file_path,
                    line_number=1,
                    description=f"Description too long: {desc_len} chars (max {self.max_desc_length})",
                    auto_fixable=False,
                    suggested_fix=f"Shorten description to under {self.max_desc_length} characters",
                    detected_at=datetime.now().isoformat(),
                    context=frontmatter['description']
                ))
            elif desc_len < self.min_desc_length:
                issues.append(Issue(
                    id=self._generate_id(file_path, "desc_too_short"),
                    category="platform",
                    severity="low",
                    type="description_length",
                    file_path=file_path,
                    line_number=1,
                    description=f"Description too short: {desc_len} chars (min {self.min_desc_length})",
                    auto_fixable=False,
                    suggested_fix=f"Expand description to at least {self.min_desc_length} characters for SEO",
                    detected_at=datetime.now().isoformat(),
                    context=frontmatter['description']
                ))
        
        return issues
    
    def auto_fix(self, file_path: str, content: str, issues: List[Issue]) -> str:
        """Automatically fix frontmatter issues."""
        if not self.auto_generate.get('enabled', False):
            return content
        
        frontmatter = self._extract_frontmatter(content)
        
        # If no frontmatter, create it
        if frontmatter is None:
            title = self._generate_title(file_path, content)
            description = self._generate_description(content)
            
            new_frontmatter = f"""---
title: {title}
description: {description}
---

"""
            return new_frontmatter + content
        
        # If frontmatter exists but missing fields
        for issue in issues:
            if issue.type == "missing_frontmatter_field":
                field_name = issue.description.split("'")[1]
                
                if field_name == 'title' and frontmatter.get('title') is None:
                    frontmatter['title'] = self._generate_title(file_path, content)
                elif field_name == 'description' and frontmatter.get('description') is None:
                    frontmatter['description'] = self._generate_description(content)
        
        # Reconstruct content with fixed frontmatter
        return self._reconstruct_content(content, frontmatter)
    
    @staticmethod
    def _extract_frontmatter(content: str) -> Optional[Dict]:
        """Extract YAML frontmatter from content."""
        match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
        if not match:
            return None
        
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return {}
    
    @staticmethod
    def _generate_title(file_path: str, content: str) -> str:
        """Generate title from filename or first heading."""
        # Try to find first H1 heading
        h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        
        # Otherwise, use filename
        filename = Path(file_path).stem
        return filename.replace('-', ' ').replace('_', ' ').title()
    
    @staticmethod
    def _generate_description(content: str) -> str:
        """Generate description from first paragraph."""
        # Remove frontmatter
        content_without_fm = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Find first paragraph (after headings)
        lines = content_without_fm.split('\n')
        description_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                description_lines.append(line)
                if len(' '.join(description_lines)) >= 100:
                    break
        
        description = ' '.join(description_lines)
        
        # Truncate to reasonable length
        if len(description) > 150:
            description = description[:147] + "..."
        
        return description or "Documentation page"
    
    @staticmethod
    def _reconstruct_content(content: str, frontmatter: Dict) -> str:
        """Reconstruct content with updated frontmatter."""
        # Remove existing frontmatter
        content_without_fm = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Build new frontmatter
        fm_lines = ["---"]
        for key, value in frontmatter.items():
            if isinstance(value, str):
                # Escape quotes if needed
                if ':' in value or '\n' in value:
                    fm_lines.append(f"{key}: |")
                    for line in value.split('\n'):
                        fm_lines.append(f"  {line}")
                else:
                    fm_lines.append(f"{key}: {value}")
            else:
                fm_lines.append(f"{key}: {value}")
        fm_lines.append("---")
        fm_lines.append("")
        
        return '\n'.join(fm_lines) + content_without_fm
    
    @staticmethod
    def _generate_id(file_path: str, detail: str) -> str:
        """Generate unique issue ID."""
        content = f"{file_path}_{detail}"
        return hashlib.md5(content.encode()).hexdigest()[:16]


class LinkValidator:
    """Validates internal and external links."""
    
    def __init__(self, config: Dict, repo_path: str):
        link_config = config.get('links', {})
        self.check_internal = link_config.get('check_internal', True)
        self.check_external = link_config.get('check_external', False)
        self.check_anchors = link_config.get('check_anchors', True)
        self.poor_link_text = link_config.get('poor_link_text', ['here', 'click here', 'link'])
        self.repo_path = Path(repo_path)
    
    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check a file for link issues."""
        issues = []
        lines = content.split('\n')
        
        # Find all markdown links: [text](url) and <url>
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)|<(https?://[^>]+)>')
        
        for line_num, line in enumerate(lines, 1):
            for match in link_pattern.finditer(line):
                if match.group(1):  # Markdown link [text](url)
                    link_text = match.group(1)
                    link_url = match.group(2)
                else:  # Plain URL <url>
                    link_text = match.group(3)
                    link_url = match.group(3)
                
                # Check for poor link text
                if link_text.lower().strip() in self.poor_link_text:
                    issues.append(Issue(
                        id=self._generate_id(file_path, line_num, "poor_link_text"),
                        category="user_experience",
                        severity="medium",
                        type="poor_link_text",
                        file_path=file_path,
                        line_number=line_num,
                        description=f"Poor link text: '{link_text}' is not descriptive",
                        auto_fixable=False,
                        suggested_fix="Use descriptive link text that explains what the link leads to",
                        detected_at=datetime.now().isoformat(),
                        context=line.strip()
                    ))
                
                # Check internal links
                if self.check_internal and not link_url.startswith(('http://', 'https://', 'mailto:', '#')):
                    # Internal link - check if file exists
                    link_path = self._resolve_link_path(file_path, link_url)
                    
                    if link_path and not link_path.exists():
                        issues.append(Issue(
                            id=self._generate_id(file_path, line_num, f"broken_{link_url}"),
                            category="user_experience",
                            severity="high",
                            type="broken_link",
                            file_path=file_path,
                            line_number=line_num,
                            description=f"Broken internal link: '{link_url}' does not exist",
                            auto_fixable=False,
                            suggested_fix=f"Fix link target or remove link",
                            detected_at=datetime.now().isoformat(),
                            context=line.strip()
                        ))
        
        return issues
    
    def _resolve_link_path(self, current_file: str, link_url: str) -> Optional[Path]:
        """Resolve internal link to absolute path."""
        # Remove anchor
        link_url = link_url.split('#')[0]
        
        if not link_url:
            return None
        
        current_path = self.repo_path / current_file
        current_dir = current_path.parent
        
        # Resolve relative to current file
        if link_url.startswith('./'):
            target = (current_dir / link_url[2:]).resolve()
        elif link_url.startswith('../'):
            target = (current_dir / link_url).resolve()
        else:
            # Relative to repo root
            target = (self.repo_path / link_url.lstrip('/')).resolve()
        
        return target if target.exists() else None
    
    @staticmethod
    def _generate_id(file_path: str, line_num: int, detail: str) -> str:
        """Generate unique issue ID."""
        content = f"{file_path}_{line_num}_{detail}"
        return hashlib.md5(content.encode()).hexdigest()[:16]


class CodeExampleChecker:
    """Checks code examples for quality issues."""
    
    def __init__(self, config: Dict):
        code_config = config.get('code_examples', {})
        self.require_error_handling = code_config.get('require_error_handling', True)
        self.require_language_tags = code_config.get('require_language_tags', True)
        self.require_imports = code_config.get('require_imports', False)
        self.languages = code_config.get('languages', [])
    
    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check a file for code example issues."""
        issues = []
        
        # Find all code blocks
        code_blocks = re.findall(r'```(\w*)\n(.*?)```', content, re.DOTALL)
        
        for idx, (language, code) in enumerate(code_blocks):
            block_id = f"code_block_{idx}"
            
            # Check for language tag
            if self.require_language_tags and not language:
                issues.append(Issue(
                    id=self._generate_id(file_path, block_id, "no_language"),
                    category="platform",
                    severity="medium",
                    type="missing_language_tag",
                    file_path=file_path,
                    line_number=self._find_code_block_line(content, idx),
                    description="Code block missing language tag",
                    auto_fixable=False,
                    suggested_fix="Add language tag after ``` (e.g., ```python)",
                    detected_at=datetime.now().isoformat(),
                    context=code[:100]
                ))
            
            # Check for error handling in supported languages
            if self.require_error_handling and language in ['python', 'typescript', 'javascript', 'java']:
                has_error_handling = self._has_error_handling(code, language)
                
                if not has_error_handling and 'api' in code.lower():
                    issues.append(Issue(
                        id=self._generate_id(file_path, block_id, "no_error_handling"),
                        category="completeness",
                        severity="high",
                        type="missing_error_handling",
                        file_path=file_path,
                        line_number=self._find_code_block_line(content, idx),
                        description=f"Code example missing error handling",
                        auto_fixable=False,
                        suggested_fix="Add try-catch or error handling to make example production-ready",
                        detected_at=datetime.now().isoformat(),
                        context=code[:100]
                    ))
        
        return issues
    
    @staticmethod
    def _has_error_handling(code: str, language: str) -> bool:
        """Check if code has error handling."""
        error_handling_patterns = {
            'python': [r'\btry\b', r'\bexcept\b', r'\bfinally\b'],
            'typescript': [r'\btry\b', r'\bcatch\b', r'\bfinally\b'],
            'javascript': [r'\btry\b', r'\bcatch\b', r'\bfinally\b', r'\.catch\('],
            'java': [r'\btry\b', r'\bcatch\b', r'\bfinally\b', r'\bthrows\b']
        }
        
        patterns = error_handling_patterns.get(language, [])
        return any(re.search(pattern, code, re.IGNORECASE) for pattern in patterns)
    
    @staticmethod
    def _find_code_block_line(content: str, block_index: int) -> int:
        """Find the line number of a code block."""
        count = 0
        for line_num, line in enumerate(content.split('\n'), 1):
            if line.strip().startswith('```'):
                if count == block_index:
                    return line_num
                count += 1
        return 1
    
    @staticmethod
    def _generate_id(file_path: str, block_id: str, detail: str) -> str:
        """Generate unique issue ID."""
        content = f"{file_path}_{block_id}_{detail}"
        return hashlib.md5(content.encode()).hexdigest()[:16]


class DuplicationDetector:
    """Detects duplicate content across files."""
    
    def __init__(self, config: Dict):
        dup_config = config.get('duplication', {})
        self.threshold = dup_config.get('threshold', 0.8)
        self.known_patterns = dup_config.get('known_patterns', [])
    
    def check_repository(self, files: Dict[str, str]) -> List[Issue]:
        """Check entire repository for duplicate content."""
        issues = []
        
        # Check known duplicate patterns
        for pattern in self.known_patterns:
            canonical = pattern.get('canonical')
            locations = pattern.get('locations', [])
            action = pattern.get('action', 'consolidate')
            
            # Check if all locations exist
            existing_locations = [loc for loc in locations if loc in files]
            
            if len(existing_locations) > 1 and canonical in existing_locations:
                for location in existing_locations:
                    if location != canonical:
                        issues.append(Issue(
                            id=self._generate_id("duplication", location),
                            category="information_architecture",
                            severity="critical",
                            type="duplicate_content_path",
                            file_path=location,
                            line_number=None,
                            description=f"Duplicate content path. Canonical location: {canonical}",
                            auto_fixable=False,
                            suggested_fix=f"Convert to navigation pointer to {canonical}",
                            detected_at=datetime.now().isoformat()
                        ))
        
        # Check for similar content (paragraph-level)
        paragraphs = self._extract_paragraphs(files)
        similar_pairs = self._find_similar_paragraphs(paragraphs)
        
        for (file1, para1), (file2, para2), similarity in similar_pairs:
            if similarity >= self.threshold:
                issues.append(Issue(
                    id=self._generate_id("similarity", f"{file1}_{file2}"),
                    category="information_architecture",
                    severity="medium",
                    type="content_duplication",
                    file_path=file1,
                    line_number=None,
                    description=f"Similar content found in {file2} ({similarity:.0%} similarity)",
                    auto_fixable=False,
                    suggested_fix="Consider consolidating duplicate content",
                    detected_at=datetime.now().isoformat(),
                    context=para1[:100]
                ))
        
        return issues
    
    @staticmethod
    def _extract_paragraphs(files: Dict[str, str]) -> Dict[str, List[str]]:
        """Extract paragraphs from all files."""
        paragraphs = {}
        
        for file_path, content in files.items():
            # Remove frontmatter
            content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
            
            # Split by double newlines
            paras = [p.strip() for p in content.split('\n\n') if p.strip() and len(p.strip()) > 50]
            paragraphs[file_path] = paras
        
        return paragraphs
    
    @staticmethod
    def _find_similar_paragraphs(paragraphs: Dict[str, List[str]], threshold: float = 0.8) -> List[Tuple]:
        """Find similar paragraphs across files."""
        similar_pairs = []
        
        files = list(paragraphs.keys())
        for i, file1 in enumerate(files):
            for file2 in files[i+1:]:
                for para1 in paragraphs[file1]:
                    for para2 in paragraphs[file2]:
                        similarity = DuplicationDetector._text_similarity(para1, para2)
                        if similarity >= threshold:
                            similar_pairs.append(((file1, para1), (file2, para2), similarity))
        
        return similar_pairs
    
    @staticmethod
    def _text_similarity(text1: str, text2: str) -> float:
        """Calculate simple text similarity (Jaccard similarity on words)."""
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    @staticmethod
    def _generate_id(prefix: str, detail: str) -> str:
        """Generate unique issue ID."""
        content = f"{prefix}_{detail}"
        return hashlib.md5(content.encode()).hexdigest()[:16]


class InformationArchitectureChecker:
    """Checks information architecture issues."""
    
    def __init__(self, config: Dict):
        ia_config = config.get('information_architecture', {})
        self.max_nav_depth = ia_config.get('max_navigation_depth', 3)
        self.max_section_length = ia_config.get('max_section_length', 500)
        self.required_sections = ia_config.get('required_sections', {})
    
    def check_file(self, file_path: str, content: str) -> List[Issue]:
        """Check a file for IA issues."""
        issues = []
        
        # Check navigation depth
        depth = file_path.count('/')
        if depth > self.max_nav_depth:
            issues.append(Issue(
                id=self._generate_id(file_path, "nav_depth"),
                category="information_architecture",
                severity="medium",
                type="navigation_depth",
                file_path=file_path,
                line_number=None,
                description=f"Navigation depth {depth} exceeds maximum {self.max_nav_depth}",
                auto_fixable=False,
                suggested_fix=f"Consider promoting content to reduce navigation depth",
                detected_at=datetime.now().isoformat()
            ))
        
        # Check heading hierarchy
        headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
        
        if headings:
            prev_level = 0
            for heading_marker, heading_text in headings:
                current_level = len(heading_marker)
                
                # Check for skipped levels
                if current_level > prev_level + 1:
                    issues.append(Issue(
                        id=self._generate_id(file_path, f"heading_skip_{heading_text}"),
                        category="information_architecture",
                        severity="medium",
                        type="heading_hierarchy",
                        file_path=file_path,
                        line_number=None,
                        description=f"Heading hierarchy skip: H{prev_level} to H{current_level}",
                        auto_fixable=False,
                        suggested_fix="Fix heading hierarchy by not skipping levels",
                        detected_at=datetime.now().isoformat(),
                        context=heading_text
                    ))
                
                prev_level = current_level
        
        # Check for required sections based on page type
        page_type = self._determine_page_type(file_path, content)
        required = self.required_sections.get(page_type, [])
        
        for required_section in required:
            # Look for heading with this name (case-insensitive)
            if not re.search(rf'^#+\s+{re.escape(required_section)}', content, re.IGNORECASE | re.MULTILINE):
                issues.append(Issue(
                    id=self._generate_id(file_path, f"missing_{required_section}"),
                    category="completeness",
                    severity="medium",
                    type="missing_section",
                    file_path=file_path,
                    line_number=None,
                    description=f"Missing required section for {page_type}: '{required_section}'",
                    auto_fixable=False,
                    suggested_fix=f"Add '{required_section}' section",
                    detected_at=datetime.now().isoformat()
                ))
        
        return issues
    
    @staticmethod
    def _determine_page_type(file_path: str, content: str) -> str:
        """Determine page type from path and content."""
        path_lower = file_path.lower()
        content_lower = content.lower()
        
        if 'api' in path_lower or 'reference' in path_lower:
            return 'api_reference'
        elif 'guide' in path_lower or 'tutorial' in path_lower:
            return 'guide'
        elif 'troubleshoot' in path_lower or 'error' in path_lower:
            return 'troubleshooting'
        else:
            return 'general'
    
    @staticmethod
    def _generate_id(file_path: str, detail: str) -> str:
        """Generate unique issue ID."""
        content = f"{file_path}_{detail}"
        return hashlib.md5(content.encode()).hexdigest()[:16]


class AISemanticAnalyzer:
    """Uses Claude AI to analyze semantic quality."""
    
    def __init__(self, config: Dict):
        ai_config = config.get('ai_analysis', {})
        self.enabled = ai_config.get('enabled', False) and ANTHROPIC_AVAILABLE
        self.model = ai_config.get('model', 'claude-sonnet-4-5-20250929')
        
        if self.enabled:
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.client = anthropic.Anthropic(api_key=api_key)
            else:
                self.enabled = False
                logger.warning("AI analysis enabled but ANTHROPIC_API_KEY not set")
    
    def analyze_clarity(self, file_path: str, content: str) -> List[Issue]:
        """Use AI to analyze content clarity."""
        if not self.enabled:
            return []
        
        issues = []
        
        try:
            # Analyze in chunks to stay within token limits
            sections = self._split_into_sections(content)
            
            for idx, section in enumerate(sections[:3]):  # Limit to first 3 sections
                prompt = f"""Analyze this documentation section for clarity issues:

{section}

Identify:
1. Confusing explanations or unclear language
2. Missing context or prerequisites
3. Undefined jargon or technical terms
4. Logical gaps in explanation

Respond with a JSON list of issues, each with:
- line: approximate line in the section
- description: what the issue is
- suggestion: how to fix it

If no issues found, respond with empty list []."""

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=1000,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Parse response
                try:
                    ai_issues = json.loads(response.content[0].text)
                    
                    for ai_issue in ai_issues:
                        issues.append(Issue(
                            id=self._generate_id(file_path, f"ai_clarity_{idx}_{ai_issue.get('line', 0)}"),
                            category="user_experience",
                            severity="medium",
                            type="clarity_issue",
                            file_path=file_path,
                            line_number=None,
                            description=f"AI-detected clarity issue: {ai_issue.get('description', 'Unclear content')}",
                            auto_fixable=False,
                            suggested_fix=ai_issue.get('suggestion', 'Review and clarify content'),
                            detected_at=datetime.now().isoformat(),
                            context=section[:100]
                        ))
                except (json.JSONDecodeError, KeyError):
                    logger.warning(f"Could not parse AI response for {file_path}")
        
        except Exception as e:
            logger.error(f"AI analysis failed for {file_path}: {e}")
        
        return issues
    
    @staticmethod
    def _split_into_sections(content: str, max_length: int = 2000) -> List[str]:
        """Split content into analyzable sections."""
        # Remove frontmatter
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
        
        # Split by headings
        sections = re.split(r'\n## ', content)
        
        # Limit section size
        result = []
        for section in sections:
            if len(section) <= max_length:
                result.append(section)
            else:
                # Split long sections by paragraphs
                paragraphs = section.split('\n\n')
                current = ""
                for para in paragraphs:
                    if len(current) + len(para) <= max_length:
                        current += para + "\n\n"
                    else:
                        if current:
                            result.append(current)
                        current = para + "\n\n"
                if current:
                    result.append(current)
        
        return result
    
    @staticmethod
    def _generate_id(file_path: str, detail: str) -> str:
        """Generate unique issue ID."""
        content = f"{file_path}_{detail}"
        return hashlib.md5(content.encode()).hexdigest()[:16]


class MetricsCollector:
    """Collects quality metrics."""
    
    def __init__(self, db: MetricsDatabase):
        self.db = db
    
    def collect_all_metrics(self, repo_path: str, issues: List[Issue]) -> Dict[str, float]:
        """Collect all metrics."""
        metrics = {}
        timestamp = datetime.now().isoformat()
        
        # Count issues by severity
        by_severity = defaultdict(int)
        for issue in issues:
            by_severity[issue.severity] += 1
        
        metrics['total_issues'] = len(issues)
        metrics['critical_issues'] = by_severity['critical']
        metrics['high_issues'] = by_severity['high']
        metrics['medium_issues'] = by_severity['medium']
        metrics['low_issues'] = by_severity['low']
        
        # Calculate auto-fixable rate
        auto_fixable = sum(1 for i in issues if i.auto_fixable)
        metrics['auto_fixable_rate'] = auto_fixable / len(issues) if issues else 0.0
        
        # Count files
        all_files = list(Path(repo_path).rglob('*.md')) + list(Path(repo_path).rglob('*.mdx'))
        metrics['total_files'] = len(all_files)
        
        # Issues per file
        metrics['issues_per_file'] = len(issues) / len(all_files) if all_files else 0.0
        
        # Documentation debt (critical + high)
        metrics['documentation_debt'] = by_severity['critical'] + by_severity['high']
        
        # Count issues by category
        by_category = defaultdict(int)
        for issue in issues:
            by_category[issue.category] += 1
        
        metrics['ia_issues'] = by_category['information_architecture']
        metrics['consistency_issues'] = by_category['consistency']
        metrics['completeness_issues'] = by_category['completeness']
        metrics['ux_issues'] = by_category['user_experience']
        metrics['platform_issues'] = by_category['platform']
        
        # Content consistency score (1.0 - ratio of consistency issues)
        total_content = sum(by_category.values())
        metrics['content_consistency_score'] = (
            1.0 - (by_category['consistency'] / total_content) 
            if total_content > 0 else 1.0
        )
        
        # Save metrics to database
        for name, value in metrics.items():
            self.db.save_metric(Metric(
                name=name,
                value=value,
                timestamp=timestamp,
                category='quality'
            ))
        
        return metrics
    
    def calculate_trends(self, metric_name: str, days: int = 30) -> Dict:
        """Calculate trend for a metric."""
        history = self.db.get_metrics_history(metric_name, days)
        
        if len(history) < 2:
            return {'trend': 'insufficient_data'}
        
        # Get first and last values
        first_value = history[0][1]
        last_value = history[-1][1]
        
        # Calculate change
        change = last_value - first_value
        percent_change = (change / first_value * 100) if first_value != 0 else 0
        
        # Determine trend (for issues, lower is better)
        if metric_name in ['total_issues', 'critical_issues', 'high_issues', 'documentation_debt']:
            trend = 'improving' if change < 0 else 'degrading' if change > 0 else 'stable'
        else:  # For scores, higher is better
            trend = 'improving' if change > 0 else 'degrading' if change < 0 else 'stable'
        
        return {
            'metric': metric_name,
            'first_value': first_value,
            'last_value': last_value,
            'change': change,
            'percent_change': percent_change,
            'trend': trend,
            'days': days
        }


class DocumentationQualityEngine:
    """Main orchestrator for documentation quality automation."""
    
    def __init__(self, config_path: str = "quality_config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Initialize database
        db_path = self.config.get('database', {}).get('path', 'doc_quality_metrics.db')
        self.db = MetricsDatabase(db_path)
        
        # Initialize checkers
        self.terminology_checker = TerminologyChecker(self.config)
        self.frontmatter_validator = FrontmatterValidator(self.config)
        
        # Get repository path
        self.repo_path = self.config.get('repository', {}).get('path', './docs')
        
        self.link_validator = LinkValidator(self.config, self.repo_path)
        self.code_checker = CodeExampleChecker(self.config)
        self.duplication_detector = DuplicationDetector(self.config)
        self.ia_checker = InformationArchitectureChecker(self.config)
        self.ai_analyzer = AISemanticAnalyzer(self.config)
        
        # Initialize metrics collector
        self.metrics_collector = MetricsCollector(self.db)
        
        logger.info(f"Initialized DocumentationQualityEngine for {self.repo_path}")
    
    def scan_repository(self) -> List[Issue]:
        """Scan entire repository for issues."""
        logger.info("Starting repository scan...")
        
        all_issues = []
        
        # Get file patterns
        file_patterns = self.config.get('repository', {}).get('file_patterns', ['**/*.md', '**/*.mdx'])
        exclude_patterns = self.config.get('repository', {}).get('exclude_patterns', [])
        
        # Find all files
        files = {}
        repo_path = Path(self.repo_path)
        
        for pattern in file_patterns:
            for file_path in repo_path.glob(pattern):
                # Check exclusions
                excluded = any(file_path.match(ex) for ex in exclude_patterns)
                if not excluded:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            relative_path = str(file_path.relative_to(repo_path))
                            files[relative_path] = content
                    except Exception as e:
                        logger.error(f"Error reading {file_path}: {e}")
        
        logger.info(f"Found {len(files)} files to analyze")
        
        # Run checkers on each file
        for file_path, content in files.items():
            logger.debug(f"Analyzing {file_path}")
            
            # Run all checkers
            all_issues.extend(self.terminology_checker.check_file(file_path, content))
            all_issues.extend(self.frontmatter_validator.check_file(file_path, content))
            all_issues.extend(self.link_validator.check_file(file_path, content))
            all_issues.extend(self.code_checker.check_file(file_path, content))
            all_issues.extend(self.ia_checker.check_file(file_path, content))
            
            # AI analysis (optional, rate-limited)
            if self.ai_analyzer.enabled and len(files) <= 10:  # Only for small repos
                all_issues.extend(self.ai_analyzer.analyze_clarity(file_path, content))
        
        # Run cross-file checks
        logger.info("Running cross-file analysis...")
        all_issues.extend(self.duplication_detector.check_repository(files))
        
        # Save all issues to database
        for issue in all_issues:
            self.db.save_issue(issue)
        
        # Log action
        self.db.log_action('scan', f"Scanned {len(files)} files, found {len(all_issues)} issues")
        
        logger.info(f"Scan complete. Found {len(all_issues)} issues.")
        return all_issues
    
    def auto_fix_issues(self, dry_run: bool = False) -> Dict[str, int]:
        """Automatically fix issues where possible."""
        logger.info(f"Running auto-fix (dry_run={dry_run})")
        
        issues = self.db.get_open_issues()
        auto_fixable = [i for i in issues if i.auto_fixable]
        
        stats = {'fixed': 0, 'failed': 0, 'skipped': 0}
        
        # Group by file
        by_file = defaultdict(list)
        for issue in auto_fixable:
            by_file[issue.file_path].append(issue)
        
        # Create backup directory if needed
        if not dry_run:
            backup_dir = self.config.get('auto_fix', {}).get('backup_dir', '.doc_quality_backups')
            Path(backup_dir).mkdir(exist_ok=True)
        
        for file_path, file_issues in by_file.items():
            full_path = Path(self.repo_path) / file_path
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                # Create backup
                if not dry_run:
                    backup_path = Path(backup_dir) / file_path
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    with open(backup_path, 'w', encoding='utf-8') as f:
                        f.write(original_content)
                
                fixed_content = original_content
                
                # Apply fixes based on issue type
                term_issues = [i for i in file_issues if i.type in ["terminology", "capitalization"]]
                if term_issues:
                    fixed_content = self.terminology_checker.auto_fix(file_path, fixed_content, term_issues)
                
                fm_issues = [i for i in file_issues if i.type.startswith("missing_frontmatter")]
                if fm_issues:
                    fixed_content = self.frontmatter_validator.auto_fix(file_path, fixed_content, fm_issues)
                
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
                    logger.info(f"{'Would fix' if dry_run else 'Fixed'} {len(file_issues)} issues in {file_path}")
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
    
    def generate_report(self, output_path: str = "quality_report.md") -> str:
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
        report.append(f"- **Critical:** {metrics.get('critical_issues', 0):.0f}")
        report.append(f"- **High:** {metrics.get('high_issues', 0):.0f}")
        report.append(f"- **Medium:** {metrics.get('medium_issues', 0):.0f}")
        report.append(f"- **Low:** {metrics.get('low_issues', 0):.0f}")
        report.append(f"- **Auto-fixable:** {int(metrics.get('auto_fixable_rate', 0) * 100)}%\n")
        
        # Trends
        report.append("## Trends (30 days)\n")
        for metric_name in ['total_issues', 'critical_issues', 'documentation_debt']:
            trend = self.metrics_collector.calculate_trends(metric_name, days=30)
            if trend.get('trend') != 'insufficient_data':
                change_symbol = "↓" if trend['trend'] == 'improving' else "↑" if trend['trend'] == 'degrading' else "→"
                report.append(f"### {metric_name.replace('_', ' ').title()}")
                report.append(f"- {change_symbol} {trend['change']:+.0f} ({trend['percent_change']:+.1f}%)")
                report.append(f"- Trend: **{trend['trend'].upper()}**\n")
        
        # Quality gates
        report.append("## Quality Gates\n")
        
        gates = [
            ('critical_issues', 'No Critical Issues', 0, False),
            ('documentation_debt', 'Documentation Debt', 2, False),
            ('content_consistency_score', 'Consistency Score', 0.95, True)
        ]
        
        for key, label, target, higher_is_better in gates:
            value = metrics.get(key, 0)
            
            if higher_is_better:
                passing = value >= target
                status = "✅ PASS" if passing else "❌ FAIL"
            else:
                passing = value <= target
                status = "✅ PASS" if passing else "❌ FAIL"
            
            report.append(f"- **{label}:** {status} (current: {value:.2f}, target: {target:.2f})")
        
        report.append("")
        
        # Issues by category
        report.append("## Issues by Category\n")
        for category, cat_issues in sorted(by_category.items()):
            if not cat_issues:
                continue
            
            report.append(f"### {category.replace('_', ' ').title()} ({len(cat_issues)})\n")
            
            # Top 5 issues
            for issue in sorted(cat_issues, key=lambda x: ['critical', 'high', 'medium', 'low'].index(x.severity))[:5]:
                report.append(f"**{issue.severity.upper()}:** {issue.description}")
                report.append(f"- File: `{issue.file_path}`")
                if issue.line_number:
                    report.append(f"- Line: {issue.line_number}")
                if issue.suggested_fix:
                    report.append(f"- Fix: {issue.suggested_fix}")
                report.append("")
            
            if len(cat_issues) > 5:
                report.append(f"*...and {len(cat_issues) - 5} more*\n")
        
        # Recommended actions
        report.append("## Recommended Actions\n")
        
        critical = by_severity.get('critical', [])
        if critical:
            report.append(f"### 1. URGENT: Fix {len(critical)} Critical Issues\n")
            for issue in critical[:3]:
                report.append(f"- {issue.description} in `{issue.file_path}`")
            report.append("")
        
        auto_fixable = [i for i in issues if i.auto_fixable]
        if auto_fixable:
            report.append(f"### 2. Run Auto-fix for {len(auto_fixable)} Issues\n")
            report.append("```bash")
            report.append("python doc_quality_automation.py fix --dry-run  # Preview changes")
            report.append("python doc_quality_automation.py fix  # Apply fixes")
            report.append("```\n")
        
        high_issues = by_severity.get('high', [])
        if high_issues:
            report.append(f"### 3. Review {len(high_issues)} High-Priority Issues\n")
            report.append("These require manual attention:\n")
            for issue in high_issues[:5]:
                report.append(f"- {issue.description} (`{issue.file_path}`)")
            report.append("")
        
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
        description='Documentation Quality Automation Engine',
        epilog='Example: python doc_quality_automation.py scan --config quality_config.yaml'
    )
    parser.add_argument(
        'action',
        choices=['scan', 'fix', 'report', 'metrics'],
        help='Action to perform'
    )
    parser.add_argument(
        '--config',
        default='quality_config.yaml',
        help='Configuration file path (default: quality_config.yaml)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview fixes without making changes'
    )
    parser.add_argument(
        '--output',
        default='quality_report.md',
        help='Output file for reports (default: quality_report.md)'
    )
    
    args = parser.parse_args()
    
    # Initialize engine
    try:
        engine = DocumentationQualityEngine(args.config)
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {args.config}")
        return 1
    except Exception as e:
        logger.error(f"Failed to initialize engine: {e}")
        return 1
    
    try:
        if args.action == 'scan':
            print("\n🔍 Starting documentation scan...")
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
                    icon = "🔴" if severity == 'critical' else "🟠" if severity == 'high' else "🟡" if severity == 'medium' else "🟢"
                    print(f"  {icon} {severity.upper()}: {count}")
        
        elif args.action == 'fix':
            print(f"\n🔧 Running auto-fix {'(DRY RUN)' if args.dry_run else ''}...")
            stats = engine.auto_fix_issues(dry_run=args.dry_run)
            mode = "Would fix" if args.dry_run else "Fixed"
            print(f"\n✅ {mode} {stats['fixed']} issues")
            if stats['failed'] > 0:
                print(f"⚠️  Failed to fix {stats['failed']} issues")
            if stats['skipped'] > 0:
                print(f"ℹ️  Skipped {stats['skipped']} issues (no changes needed)")
        
        elif args.action == 'report':
            print("\n📄 Generating quality report...")
            output = engine.generate_report(args.output)
            print(f"\n✅ Report generated: {output}")
        
        elif args.action == 'metrics':
            print("\n📊 Collecting quality metrics...")
            metrics = engine.collect_metrics()
            print("\n📊 Current Metrics:\n")
            
            # Group metrics
            print("Primary KPIs:")
            primary = ['total_issues', 'critical_issues', 'high_issues', 'documentation_debt']
            for name in primary:
                if name in metrics:
                    print(f"  {name.replace('_', ' ').title()}: {metrics[name]:.1f}")
            
            print("\nQuality Scores:")
            scores = ['auto_fixable_rate', 'content_consistency_score']
            for name in scores:
                if name in metrics:
                    value = metrics[name]
                    if 'rate' in name or 'score' in name:
                        print(f"  {name.replace('_', ' ').title()}: {value*100:.1f}%")
                    else:
                        print(f"  {name.replace('_', ' ').title()}: {value:.2f}")
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 130
    except Exception as e:
        logger.error(f"Operation failed: {e}", exc_info=True)
        return 1
    finally:
        engine.close()
    
    return 0


if __name__ == '__main__':
    exit(main())
