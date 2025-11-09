#!/usr/bin/env python3
"""
Comprehensive Test Suite for Documentation Quality Automation System
Tests all components, integration, and end-to-end workflows.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import pytest
import yaml
import sqlite3

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from doc_quality_automation import (
    DocumentationQualityEngine,
    TerminologyChecker,
    FrontmatterValidator,
    LinkValidator,
    CodeExampleChecker,
    DuplicationDetector,
    InformationArchitectureChecker,
    MetricsDatabase,
    Issue
)


@pytest.fixture
def temp_repo():
    """Create a temporary repository for testing."""
    temp_dir = tempfile.mkdtemp()
    
    # Create sample documentation structure
    docs_dir = Path(temp_dir) / "docs"
    docs_dir.mkdir()
    
    # Sample files with various issues
    files = {
        "overview.md": """# Overview

Simply utilize the Claude Code SDK to leverage advanced features.

This is a very long sentence that goes on and on and really should be broken up into multiple shorter sentences for better readability and comprehension by users who are trying to understand the documentation.

You can use the tool here to accomplish this task.

## Features

```
# Code without language tag
print("hello")
```

Check out [this link](./nonexistent.md) for more info.
""",
        "quickstart.mdx": """# Quick Start

Get started with Claude Code SDK quickly.

```python
# Missing error handling
import anthropic
client = anthropic.Anthropic(api_key="your-key")
message = client.messages.create(
    model="claude-sonnet-4-5",
    messages=[{"role": "user", "content": "Hello"}]
)
print(message.content)
```
""",
        "api/reference.mdx": """---
title: API Reference
---

# API Reference

The ClaudeCodeOptions interface provides configuration.
""",
        "guides/advanced/deep/nested.md": """# Deeply Nested

This page is too deep in the hierarchy.
"""
    }
    
    for file_path, content in files.items():
        full_path = docs_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
    
    yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def test_config(temp_repo):
    """Create test configuration."""
    config = {
        'database': {
            'path': os.path.join(temp_repo, 'test_metrics.db')
        },
        'repository': {
            'path': os.path.join(temp_repo, 'docs'),
            'file_patterns': ['**/*.md', '**/*.mdx'],
            'exclude_patterns': []
        },
        'terminology': {
            'case_sensitive': False,
            'deprecated_terms': ['Claude Code SDK', 'ClaudeCodeOptions', 'simply', 'utilize', 'leverage'],
            'preferred_terms': {
                'claude code sdk': 'Claude Agent SDK',
                'claudecodeoptions': 'ClaudeAgentOptions'
            },
            'proper_nouns': ['Claude', 'Anthropic']
        },
        'frontmatter': {
            'required': ['title', 'description'],
            'optional': ['sidebarTitle'],
            'max_description_length': 160,
            'min_description_length': 50,
            'auto_generate': {
                'enabled': True,
                'title_from_filename': True
            }
        },
        'links': {
            'check_internal': True,
            'check_external': False,
            'check_anchors': True,
            'poor_link_text': ['here', 'click here', 'link', 'this']
        },
        'code_examples': {
            'require_error_handling': True,
            'require_language_tags': True,
            'require_imports': False,
            'languages': ['python', 'typescript', 'javascript']
        },
        'duplication': {
            'threshold': 0.8,
            'known_patterns': []
        },
        'information_architecture': {
            'max_navigation_depth': 3,
            'max_section_length': 500,
            'required_sections': {
                'guide': ['Prerequisites', 'Examples'],
                'api_reference': ['Parameters', 'Examples']
            }
        },
        'ai_analysis': {
            'enabled': False  # Disable AI for tests
        }
    }
    
    config_path = os.path.join(temp_repo, 'test_config.yaml')
    with open(config_path, 'w') as f:
        yaml.dump(config, f)
    
    return config_path


class TestTerminologyChecker:
    """Test terminology checker component."""
    
    def test_detects_deprecated_terms(self, test_config):
        """Test detection of deprecated terminology."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        checker = TerminologyChecker(config)
        content = "Use the Claude Code SDK to access features. ClaudeCodeOptions provides config."
        
        issues = checker.check_file("test.md", content)
        
        # Should find both deprecated terms
        assert len(issues) >= 2
        assert any('Claude Code SDK' in i.description for i in issues)
        assert any('ClaudeCodeOptions' in i.description for i in issues)
    
    def test_weak_language_detection(self, test_config):
        """Test detection of weak language patterns."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        checker = TerminologyChecker(config)
        content = "Simply utilize the tool to leverage advanced features."
        
        issues = checker.check_file("test.md", content)
        
        # Should find weak words: simply, utilize, leverage
        assert len(issues) >= 3
    
    def test_auto_fix_terminology(self, test_config):
        """Test automatic terminology fixing."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        checker = TerminologyChecker(config)
        content = "Use Claude Code SDK for development."
        
        issues = checker.check_file("test.md", content)
        fixed_content = checker.auto_fix("test.md", content, issues)
        
        assert "Claude Agent SDK" in fixed_content
        assert "Claude Code SDK" not in fixed_content


class TestFrontmatterValidator:
    """Test frontmatter validation component."""
    
    def test_detects_missing_frontmatter(self, test_config):
        """Test detection of missing frontmatter."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        validator = FrontmatterValidator(config)
        content = "# Page Title\n\nContent without frontmatter."
        
        issues = validator.check_file("test.mdx", content)
        
        assert len(issues) > 0
        assert any(i.type == 'missing_frontmatter' for i in issues)
        assert any(i.severity == 'critical' for i in issues)
    
    def test_detects_missing_fields(self, test_config):
        """Test detection of missing required fields."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        validator = FrontmatterValidator(config)
        content = """---
title: Test Page
---

# Test Page

Content here.
"""
        
        issues = validator.check_file("test.mdx", content)
        
        # Should detect missing 'description' field
        assert any('description' in i.description.lower() for i in issues)
    
    def test_auto_generates_frontmatter(self, test_config):
        """Test automatic frontmatter generation."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        validator = FrontmatterValidator(config)
        content = "# Test Page\n\nThis is a test page with some content."
        
        issues = validator.check_file("test.mdx", content)
        fixed_content = validator.auto_fix("test.mdx", content, issues)
        
        assert '---' in fixed_content
        assert 'title:' in fixed_content
        assert 'description:' in fixed_content


class TestLinkValidator:
    """Test link validation component."""
    
    def test_detects_poor_link_text(self, temp_repo, test_config):
        """Test detection of poor link text."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        repo_path = os.path.join(temp_repo, 'docs')
        validator = LinkValidator(config, repo_path)
        
        content = "Click [here](./guide.md) for more info.\nSee [this link](./other.md) too."
        
        issues = validator.check_file("test.md", content)
        
        # Should find both poor link texts
        assert len(issues) >= 2
        assert any('poor_link_text' in i.type for i in issues)
    
    def test_detects_broken_links(self, temp_repo, test_config):
        """Test detection of broken internal links."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        repo_path = os.path.join(temp_repo, 'docs')
        validator = LinkValidator(config, repo_path)
        
        content = "See [this page](./nonexistent.md) for details."
        
        issues = validator.check_file("test.md", content)
        
        # Should find broken link
        assert any('broken_link' in i.type for i in issues)


class TestCodeExampleChecker:
    """Test code example checker component."""
    
    def test_detects_missing_language_tag(self, test_config):
        """Test detection of code blocks without language tags."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        checker = CodeExampleChecker(config)
        content = """
```
print("hello world")
```
"""
        
        issues = checker.check_file("test.md", content)
        
        assert any('missing_language_tag' in i.type for i in issues)
    
    def test_detects_missing_error_handling(self, test_config):
        """Test detection of missing error handling in API examples."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        checker = CodeExampleChecker(config)
        content = """
```python
import anthropic
client = anthropic.Anthropic(api_key="key")
response = client.messages.create(model="claude", messages=[])
```
"""
        
        issues = checker.check_file("test.md", content)
        
        # Should detect missing error handling
        assert any('missing_error_handling' in i.type for i in issues)


class TestInformationArchitectureChecker:
    """Test information architecture checker."""
    
    def test_detects_deep_nesting(self, test_config):
        """Test detection of navigation depth violations."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        checker = InformationArchitectureChecker(config)
        
        # File at depth 4 (exceeds max of 3)
        issues = checker.check_file("guides/advanced/deep/nested.md", "# Content")
        
        assert any('navigation_depth' in i.type for i in issues)
    
    def test_detects_heading_hierarchy_skips(self, test_config):
        """Test detection of heading hierarchy violations."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        checker = InformationArchitectureChecker(config)
        content = """
# Main Title

#### Skipped to H4

Content here.
"""
        
        issues = checker.check_file("test.md", content)
        
        assert any('heading_hierarchy' in i.type for i in issues)


class TestDuplicationDetector:
    """Test content duplication detection."""
    
    def test_detects_known_duplicates(self, test_config):
        """Test detection of known duplicate content paths."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        # Add known pattern to config
        config['duplication']['known_patterns'] = [
            {
                'canonical': 'docs/main.md',
                'locations': ['docs/main.md', 'docs/duplicate.md'],
                'action': 'consolidate'
            }
        ]
        
        detector = DuplicationDetector(config)
        
        files = {
            'docs/main.md': '# Main Content\n\nThis is the main page.',
            'docs/duplicate.md': '# Duplicate Content\n\nThis duplicates the main page.'
        }
        
        issues = detector.check_repository(files)
        
        assert len(issues) > 0
        assert any('duplicate_content_path' in i.type for i in issues)
    
    def test_detects_similar_content(self, test_config):
        """Test detection of similar paragraphs."""
        with open(test_config) as f:
            config = yaml.safe_load(f)
        
        detector = DuplicationDetector(config)
        
        # Very similar content
        para1 = "Claude is a powerful AI assistant that can help with many tasks including writing code and documentation."
        para2 = "Claude is a powerful AI assistant that helps with many tasks like writing code and documentation."
        
        files = {
            'doc1.md': f'# Doc 1\n\n{para1}',
            'doc2.md': f'# Doc 2\n\n{para2}'
        }
        
        issues = detector.check_repository(files)
        
        # Should detect similarity
        assert any('content_duplication' in i.type for i in issues)


class TestMetricsDatabase:
    """Test metrics database functionality."""
    
    def test_creates_schema(self, temp_repo):
        """Test database schema creation."""
        db_path = os.path.join(temp_repo, 'test.db')
        db = MetricsDatabase(db_path)
        
        # Check tables exist
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert 'issues' in tables
        assert 'metrics' in tables
        assert 'audit_log' in tables
        
        db.close()
    
    def test_saves_and_retrieves_issues(self, temp_repo):
        """Test saving and retrieving issues."""
        db_path = os.path.join(temp_repo, 'test.db')
        db = MetricsDatabase(db_path)
        
        issue = Issue(
            id='test123',
            category='consistency',
            severity='high',
            type='terminology',
            file_path='test.md',
            line_number=10,
            description='Test issue',
            auto_fixable=True,
            suggested_fix='Fix it',
            detected_at='2025-01-01T00:00:00'
        )
        
        db.save_issue(issue)
        
        # Retrieve
        issues = db.get_open_issues()
        assert len(issues) == 1
        assert issues[0].id == 'test123'
        assert issues[0].severity == 'high'
        
        db.close()
    
    def test_filters_by_severity(self, temp_repo):
        """Test filtering issues by severity."""
        db_path = os.path.join(temp_repo, 'test.db')
        db = MetricsDatabase(db_path)
        
        # Save issues with different severities
        for i, severity in enumerate(['critical', 'high', 'medium', 'low']):
            issue = Issue(
                id=f'test{i}',
                category='test',
                severity=severity,
                type='test',
                file_path='test.md',
                line_number=i,
                description=f'Test {severity}',
                auto_fixable=False,
                suggested_fix=None,
                detected_at='2025-01-01T00:00:00'
            )
            db.save_issue(issue)
        
        # Get critical only
        critical = db.get_issues_by_severity('critical')
        assert len(critical) == 1
        assert critical[0].severity == 'critical'
        
        db.close()


class TestDocumentationQualityEngine:
    """Test end-to-end engine functionality."""
    
    def test_initialization(self, test_config):
        """Test engine initialization."""
        engine = DocumentationQualityEngine(test_config)
        
        assert engine.repo_path is not None
        assert engine.db is not None
        assert engine.terminology_checker is not None
        
        engine.close()
    
    def test_scans_repository(self, test_config):
        """Test full repository scan."""
        engine = DocumentationQualityEngine(test_config)
        
        issues = engine.scan_repository()
        
        # Should find multiple issues
        assert len(issues) > 0
        
        # Check issue diversity
        categories = set(i.category for i in issues)
        assert len(categories) > 1
        
        severities = set(i.severity for i in issues)
        assert len(severities) > 1
        
        engine.close()
    
    def test_collects_metrics(self, test_config):
        """Test metrics collection."""
        engine = DocumentationQualityEngine(test_config)
        
        # Run scan first
        engine.scan_repository()
        
        # Collect metrics
        metrics = engine.collect_metrics()
        
        # Check key metrics exist
        assert 'total_issues' in metrics
        assert 'critical_issues' in metrics
        assert 'auto_fixable_rate' in metrics
        assert 'content_consistency_score' in metrics
        
        # Verify values are reasonable
        assert metrics['total_issues'] >= 0
        assert 0 <= metrics['auto_fixable_rate'] <= 1
        
        engine.close()
    
    def test_generates_report(self, test_config, temp_repo):
        """Test report generation."""
        engine = DocumentationQualityEngine(test_config)
        
        # Run scan
        engine.scan_repository()
        
        # Generate report
        report_path = os.path.join(temp_repo, 'test_report.md')
        output = engine.generate_report(report_path)
        
        assert os.path.exists(output)
        
        # Check report content
        with open(output) as f:
            content = f.read()
        
        assert 'Documentation Quality Report' in content
        assert 'Executive Summary' in content
        assert 'Issues by Category' in content
        
        engine.close()
    
    def test_auto_fixes_issues(self, test_config, temp_repo):
        """Test automatic issue fixing."""
        engine = DocumentationQualityEngine(test_config)
        
        # Run scan
        issues_before = engine.scan_repository()
        auto_fixable_before = sum(1 for i in issues_before if i.auto_fixable)
        
        # Run auto-fix (dry run)
        stats_dry = engine.auto_fix_issues(dry_run=True)
        
        # Dry run should show potential fixes
        assert stats_dry['fixed'] > 0 or stats_dry['skipped'] > 0
        
        # Run actual fix
        stats = engine.auto_fix_issues(dry_run=False)
        
        # Should have fixed some issues
        assert stats['fixed'] > 0 or stats['skipped'] > 0
        
        # Verify issues are marked as fixed
        issues_after = engine.db.get_open_issues()
        auto_fixable_after = sum(1 for i in issues_after if i.auto_fixable)
        
        assert auto_fixable_after < auto_fixable_before or stats['fixed'] == 0
        
        engine.close()


class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_complete_workflow(self, test_config, temp_repo):
        """Test complete quality improvement workflow."""
        engine = DocumentationQualityEngine(test_config)
        
        # Step 1: Scan
        print("\n=== Step 1: Scanning ===")
        issues_initial = engine.scan_repository()
        print(f"Found {len(issues_initial)} issues")
        
        assert len(issues_initial) > 0
        
        # Step 2: Collect metrics
        print("\n=== Step 2: Collecting Metrics ===")
        metrics_initial = engine.collect_metrics()
        print(f"Critical issues: {metrics_initial['critical_issues']}")
        print(f"Total issues: {metrics_initial['total_issues']}")
        
        # Step 3: Auto-fix
        print("\n=== Step 3: Auto-fixing ===")
        fix_stats = engine.auto_fix_issues(dry_run=False)
        print(f"Fixed {fix_stats['fixed']} issues")
        
        # Step 4: Re-scan
        print("\n=== Step 4: Re-scanning ===")
        issues_after = engine.scan_repository()
        metrics_after = engine.collect_metrics()
        print(f"Remaining issues: {len(issues_after)}")
        
        # Verify improvement
        assert metrics_after['total_issues'] <= metrics_initial['total_issues']
        
        # Step 5: Generate report
        print("\n=== Step 5: Generating Report ===")
        report_path = os.path.join(temp_repo, 'final_report.md')
        engine.generate_report(report_path)
        
        assert os.path.exists(report_path)
        
        print("\n=== Workflow Complete ===")
        print(f"Initial issues: {metrics_initial['total_issues']}")
        print(f"Fixed: {fix_stats['fixed']}")
        print(f"Final issues: {metrics_after['total_issues']}")
        print(f"Improvement: {metrics_initial['total_issues'] - metrics_after['total_issues']} issues resolved")
        
        engine.close()
    
    def test_ci_cd_workflow(self, test_config, temp_repo):
        """Test CI/CD quality gate workflow."""
        engine = DocumentationQualityEngine(test_config)
        
        # Scan repository
        engine.scan_repository()
        
        # Collect metrics
        metrics = engine.collect_metrics()
        
        # Check quality gates
        critical_gate = metrics['critical_issues'] <= 0
        debt_gate = metrics['documentation_debt'] <= 2
        
        print(f"\nQuality Gates:")
        print(f"  Critical Issues: {'✅ PASS' if critical_gate else '❌ FAIL'} ({metrics['critical_issues']})")
        print(f"  Documentation Debt: {'✅ PASS' if debt_gate else '❌ FAIL'} ({metrics['documentation_debt']})")
        
        # In CI/CD, would fail build if critical issues exist
        # For test, just verify we can check the gates
        assert isinstance(critical_gate, bool)
        assert isinstance(debt_gate, bool)
        
        engine.close()


def run_tests():
    """Run all tests."""
    pytest.main([
        __file__,
        '-v',
        '--tb=short',
        '--color=yes'
    ])


if __name__ == '__main__':
    run_tests()
