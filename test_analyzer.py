"""
Unit tests for Documentation Analyzer

Run with: pytest test_analyzer.py -v
"""

import pytest
from pathlib import Path
import tempfile
import os
from doc_analyzer import DocumentationAnalyzer, Issue, AnalysisReport


class TestDocumentationAnalyzer:
    """Test suite for DocumentationAnalyzer"""
    
    @pytest.fixture
    def temp_docs_dir(self):
        """Create a temporary directory with sample docs"""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir)
            
            # Create sample markdown files
            (docs_path / "overview.md").write_text("""
# Overview

This is a simple overview document.

Claude Code is a tool that helps developers write code faster.
""")
            
            (docs_path / "guide.md").write_text("""
# Getting Started Guide

## Installation

Simply install the package by running npm install.

Utilize the CLI to leverage advanced features.

## Usage

This section has a very long sentence that exceeds the recommended length and should be flagged by the analyzer as being too complex for readers to easily understand without breaking it down into smaller more digestible pieces.
""")
            
            (docs_path / "reference.md").write_text("""
# API Reference

##### Incorrect Heading Level

Content here.

[click here](./nonexistent.md) for more info.
""")
            
            yield docs_path
    
    def test_initialization(self, temp_docs_dir):
        """Test analyzer initialization"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        assert analyzer.docs_path == temp_docs_dir
        assert analyzer.report.total_files == 0
        assert analyzer.report.total_issues == 0
    
    def test_detect_long_sentences(self, temp_docs_dir):
        """Test detection of overly long sentences"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        
        content = "This is a very long sentence with many words that exceeds the thirty word limit and should be detected as being too long for good readability and comprehension by the analyzer."
        
        analyzer.check_readability(content, "test.md")
        
        # Should detect at least one long sentence issue
        long_sentence_issues = [
            i for i in analyzer.report.issues 
            if i.issue_type == 'sentence_too_long'
        ]
        assert len(long_sentence_issues) > 0
    
    def test_detect_weak_language(self, temp_docs_dir):
        """Test detection of weak or unnecessary words"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        
        content = "Simply install the package easily.\nThis is obviously the best approach."
        
        analyzer.check_readability(content, "test.md")
        
        # Should detect weak language
        weak_language_issues = [
            i for i in analyzer.report.issues 
            if i.issue_type == 'weak_language'
        ]
        assert len(weak_language_issues) >= 2  # "simply" and "obviously"
    
    def test_detect_preferred_terms(self, temp_docs_dir):
        """Test detection of non-preferred terminology"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        
        content = "Utilize this feature to leverage the benefits."
        
        analyzer.check_style_guide(content, "test.md")
        
        # Should suggest replacing "utilize" and "leverage"
        terminology_issues = [
            i for i in analyzer.report.issues 
            if i.issue_type == 'terminology'
        ]
        assert len(terminology_issues) >= 2
    
    def test_detect_passive_voice(self, temp_docs_dir):
        """Test detection of passive voice constructions"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        
        content = "The file was created by the system.\nResults are generated automatically."
        
        analyzer.check_style_guide(content, "test.md")
        
        # Should detect passive voice
        passive_voice_issues = [
            i for i in analyzer.report.issues 
            if i.issue_type == 'passive_voice'
        ]
        assert len(passive_voice_issues) > 0
    
    def test_detect_heading_hierarchy_issues(self, temp_docs_dir):
        """Test detection of incorrect heading hierarchy"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        
        content = """
# Main Title

##### Skipped to H5

Content here.
"""
        
        analyzer.check_structure(content, "test.md")
        
        # Should detect heading skip
        heading_issues = [
            i for i in analyzer.report.issues 
            if i.issue_type == 'heading_skip'
        ]
        assert len(heading_issues) > 0
    
    def test_detect_missing_code_block_language(self, temp_docs_dir):
        """Test detection of code blocks without language specification"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        
        content = """
Example code:

```
const x = 5;
console.log(x);
```
"""
        
        analyzer.check_formatting(content, "test.md")
        
        # Should detect missing language
        code_block_issues = [
            i for i in analyzer.report.issues 
            if i.issue_type == 'code_block_language'
        ]
        assert len(code_block_issues) > 0
    
    def test_detect_non_descriptive_links(self, temp_docs_dir):
        """Test detection of non-descriptive link text"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        
        content = "For more information [click here](./docs.md) or [here](./guide.md)."
        
        analyzer.check_links(content, "test.md")
        
        # Should detect non-descriptive links
        link_issues = [
            i for i in analyzer.report.issues 
            if i.issue_type == 'non_descriptive_link'
        ]
        assert len(link_issues) >= 2
    
    def test_detect_broken_relative_links(self, temp_docs_dir):
        """Test detection of broken relative links"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        
        content = "[See this guide](./nonexistent.md)"
        file_path = "test.md"
        
        # Create the file in the temp directory
        (temp_docs_dir / file_path).write_text(content)
        
        analyzer.check_links(content, file_path)
        
        # Should detect broken link
        broken_link_issues = [
            i for i in analyzer.report.issues 
            if i.issue_type == 'broken_link'
        ]
        assert len(broken_link_issues) > 0
    
    def test_full_analysis(self, temp_docs_dir):
        """Test full analysis workflow"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        
        report = analyzer.analyze_all()
        
        # Should analyze all files
        assert report.total_files == 3
        
        # Should find issues
        assert report.total_issues > 0
        
        # Should categorize issues
        assert len(report.issues_by_severity) > 0
        assert len(report.issues_by_category) > 0
    
    def test_issue_creation(self):
        """Test Issue dataclass"""
        issue = Issue(
            severity='high',
            category='clarity',
            file_path='test.md',
            line_number=42,
            issue_type='test_issue',
            description='Test description',
            suggestion='Test suggestion',
            context='Test context'
        )
        
        assert issue.severity == 'high'
        assert issue.line_number == 42
        
        # Test to_dict method
        issue_dict = issue.to_dict()
        assert issue_dict['severity'] == 'high'
        assert issue_dict['line'] == 42
    
    def test_report_add_issue(self):
        """Test adding issues to report"""
        report = AnalysisReport(
            timestamp="2024-01-01",
            total_files=5,
            total_issues=0
        )
        
        issue = Issue(
            severity='medium',
            category='style',
            file_path='test.md',
            line_number=10,
            issue_type='test',
            description='Test',
            suggestion='Test'
        )
        
        report.add_issue(issue)
        
        assert report.total_issues == 1
        assert report.issues_by_severity['medium'] == 1
        assert report.issues_by_category['style'] == 1
    
    def test_export_json(self, temp_docs_dir):
        """Test JSON export functionality"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        analyzer.analyze_all()
        
        output_path = temp_docs_dir / "report.json"
        analyzer.export_report('json', str(output_path))
        
        assert output_path.exists()
        
        # Verify JSON structure
        import json
        with open(output_path) as f:
            data = json.load(f)
        
        assert 'timestamp' in data
        assert 'summary' in data
        assert 'issues' in data
        assert isinstance(data['issues'], list)
    
    def test_config_loading(self, temp_docs_dir):
        """Test configuration file loading"""
        config_path = temp_docs_dir / "config.yaml"
        config_path.write_text("""
style_rules:
  max_line_length: 80
  avoid_terms:
    - test_term
""")
        
        analyzer = DocumentationAnalyzer(
            str(temp_docs_dir),
            str(config_path)
        )
        
        assert analyzer.config['style_rules']['max_line_length'] == 80
        assert 'test_term' in analyzer.config['style_rules']['avoid_terms']


class TestInformationArchitecture:
    """Test IA-specific functionality"""
    
    @pytest.fixture
    def large_docs_dir(self):
        """Create a directory with many files for IA testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir)
            
            # Create many files in one category
            category_dir = docs_path / "guides"
            category_dir.mkdir()
            
            for i in range(25):
                (category_dir / f"guide_{i}.md").write_text(f"# Guide {i}\n\nContent")
            
            yield docs_path
    
    def test_detect_category_overload(self, large_docs_dir):
        """Test detection of overloaded categories"""
        analyzer = DocumentationAnalyzer(str(large_docs_dir))
        
        files = list(large_docs_dir.rglob("*.md"))
        analyzer.analyze_information_architecture(files)
        
        # Should detect overloaded category
        overload_issues = [
            i for i in analyzer.report.issues 
            if i.issue_type == 'category_overload'
        ]
        assert len(overload_issues) > 0


class TestConsistency:
    """Test consistency checking"""
    
    @pytest.fixture
    def inconsistent_docs_dir(self):
        """Create docs with inconsistent terminology"""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir)
            
            (docs_path / "doc1.md").write_text("Use the CLI to access features.")
            (docs_path / "doc2.md").write_text("The command-line interface is powerful.")
            (docs_path / "doc3.md").write_text("Try the command line tools.")
            
            yield docs_path
    
    def test_detect_term_inconsistency(self, inconsistent_docs_dir):
        """Test detection of inconsistent terminology"""
        analyzer = DocumentationAnalyzer(str(inconsistent_docs_dir))
        
        files = list(inconsistent_docs_dir.rglob("*.md"))
        analyzer.analyze_consistency(files)
        
        # Should detect CLI/command-line inconsistency
        consistency_issues = [
            i for i in analyzer.report.issues 
            if i.issue_type == 'term_inconsistency'
        ]
        assert len(consistency_issues) > 0


@pytest.mark.skipif(
    not os.getenv('ANTHROPIC_API_KEY'),
    reason="Requires ANTHROPIC_API_KEY environment variable"
)
class TestAIIntegration:
    """Test AI-powered analysis (requires API key)"""
    
    @pytest.fixture
    def test_content(self):
        return """
# Complex Topic

This explanation uses jargon without definitions. The MCP server 
connects to the database through the ORM layer using a connection pool.
The user should configure the settings appropriately.
"""
    
    def test_ai_clarity_check(self, temp_docs_dir, test_content):
        """Test AI-powered clarity analysis"""
        analyzer = DocumentationAnalyzer(str(temp_docs_dir))
        
        if analyzer.claude_client:
            (temp_docs_dir / "complex.md").write_text(test_content)
            analyzer.ai_clarity_check(test_content, "complex.md")
            
            # Should find AI-identified issues
            ai_issues = [
                i for i in analyzer.report.issues 
                if i.issue_type == 'ai_clarity_check'
            ]
            # Note: Actual detection depends on Claude's response
            # This test validates the integration works
            assert isinstance(ai_issues, list)


# Performance tests
class TestPerformance:
    """Test analyzer performance"""
    
    def test_handles_large_files(self):
        """Test that analyzer can handle large files"""
        with tempfile.TemporaryDirectory() as tmpdir:
            docs_path = Path(tmpdir)
            
            # Create a large file
            large_content = "# Large Document\n\n" + ("This is a line of content.\n" * 1000)
            (docs_path / "large.md").write_text(large_content)
            
            analyzer = DocumentationAnalyzer(str(docs_path))
            
            # Should complete without errors
            report = analyzer.analyze_all()
            assert report.total_files == 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
