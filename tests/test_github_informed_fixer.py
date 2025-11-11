"""
Tests for GitHubInformedFixer

Based on real GitHub issues analysis showing:
- 72% of issues are about missing documentation
- 4% are about clarity
- Top complaints: no examples, no prerequisites, undefined jargon
"""

import pytest
from fixers.github_informed_fixer import GitHubInformedFixer
from core.config import Config
from core.models import Issue


class TestMissingDocumentationDetection:
    """Test detection of missing documentation patterns (72% of issues)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = Config()
        self.fixer = GitHubInformedFixer(self.config)

    def test_detects_very_short_pages(self):
        """Should flag pages with < 100 words."""
        short_content = "This is a very short page. Only a few words here."
        issues = self.fixer.check_file("test.md",short_content)

        # Should find short page issue
        short_page_issues = [i for i in issues if i.issue_type == "missing_documentation"]
        assert len(short_page_issues) == 1
        assert "very short" in short_page_issues[0].description.lower()
        assert short_page_issues[0].severity == "medium"

    def test_does_not_flag_adequate_length_pages(self):
        """Should not flag pages with >= 100 words."""
        # Create content with exactly 100 words
        words = ["word"] * 100
        long_content = " ".join(words)

        issues = self.fixer.check_file("test.md",long_content)

        # Should not find short page issue
        short_page_issues = [i for i in issues if i.issue_type == "missing_documentation"]
        assert len(short_page_issues) == 0

    def test_detects_missing_code_examples(self):
        """Should flag pages that discuss code without examples."""
        content = """
        This page explains the API endpoint for getting messages.
        You can use the function to retrieve data.
        The CLI command is very useful for this task.
        """

        issues = self.fixer.check_file("test.md",content)

        # Should find missing code example issue
        code_issues = [i for i in issues if i.issue_type == "missing_code_example"]
        assert len(code_issues) == 1
        assert "code examples" in code_issues[0].description.lower()
        assert code_issues[0].severity == "high"

    def test_does_not_flag_when_code_examples_present(self):
        """Should not flag pages with code blocks."""
        content = """
        This page explains the API endpoint.

        ```python
        response = api.get_messages()
        ```

        The function retrieves data.
        """

        issues = self.fixer.check_file("test.md",content)

        # Should not find missing code example issue
        code_issues = [i for i in issues if i.issue_type == "missing_code_example"]
        assert len(code_issues) == 0

    def test_detects_missing_prerequisites(self):
        """Should flag procedural content without prerequisites."""
        content = """
        # How to Install Claude Code

        Step 1: Download the installer
        Step 2: Run the setup
        Step 3: Configure your settings
        """

        issues = self.fixer.check_file("test.md",content)

        # Should find missing prerequisites issue
        prereq_issues = [i for i in issues if i.issue_type == "missing_prerequisites"]
        assert len(prereq_issues) == 1
        assert "prerequisites" in prereq_issues[0].description.lower()

    def test_does_not_flag_when_prerequisites_present(self):
        """Should not flag when prerequisites are included."""
        content = """
        # How to Install Claude Code

        ## Prerequisites
        Before you begin, ensure you have Python 3.9+ installed.

        Step 1: Download the installer
        Step 2: Run the setup
        """

        issues = self.fixer.check_file("test.md",content)

        # Should not find missing prerequisites issue
        prereq_issues = [i for i in issues if i.issue_type == "missing_prerequisites"]
        assert len(prereq_issues) == 0

    def test_detects_multiple_missing_patterns(self):
        """Should detect multiple missing documentation issues."""
        # Short page + code mention without examples + procedural without prereqs
        content = """
        How to use the API function to execute commands.
        Step 1: Run the script.
        """

        issues = self.fixer.check_file("test.md",content)

        # Should find all three issues
        assert len(issues) >= 3
        issue_types = {i.issue_type for i in issues}
        assert "missing_documentation" in issue_types  # Short page
        assert "missing_code_example" in issue_types   # No code block
        assert "missing_prerequisites" in issue_types  # Procedural without prereqs


class TestClarityDetection:
    """Test detection of clarity issues (4% of issues, but high impact)."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = Config()
        self.fixer = GitHubInformedFixer(self.config)

    def test_detects_undefined_jargon(self):
        """Should flag technical terms without definitions."""
        content = """
        You can use ultrathink to improve your results.
        The subagent will handle the processing.
        Configure your MCP settings in the YAML frontmatter.
        """

        issues = self.fixer.check_file("test.md",content)

        # Should find undefined jargon issues
        jargon_issues = [i for i in issues if i.issue_type == "undefined_jargon"]
        assert len(jargon_issues) > 0

        # Check that it found at least one of the technical terms
        descriptions = [i.description for i in jargon_issues]
        all_descriptions = " ".join(descriptions)
        assert any(term in all_descriptions for term in ["ultrathink", "subagent", "MCP", "YAML frontmatter"])

    def test_does_not_flag_defined_jargon(self):
        """Should not flag technical terms that are defined."""
        content = """
        Ultrathink is an advanced reasoning mode that provides deeper analysis.
        You can enable ultrathink by setting the flag in your configuration.
        """

        issues = self.fixer.check_file("test.md",content)

        # Should not find jargon issue for 'ultrathink' since it's defined
        jargon_issues = [i for i in issues if i.issue_type == "undefined_jargon" and "ultrathink" in i.description]
        assert len(jargon_issues) == 0

    def test_detects_code_without_nearby_examples(self):
        """Should flag inline code mentions without nearby code blocks."""
        content = """
        # Introduction

        You can use the `get_messages` function for this task.
        """ + "\n" * 20 + """
        # Unrelated Section

        Here's some other information.
        """

        issues = self.fixer.check_file("test.md",content)

        # Should find code without example issue
        code_issues = [i for i in issues if i.issue_type == "code_without_example"]
        assert len(code_issues) > 0

    def test_does_not_flag_code_with_nearby_examples(self):
        """Should not flag inline code with nearby code blocks."""
        content = """
        You can use the `get_messages` function for this task.

        ```python
        result = get_messages()
        ```

        This returns the messages.
        """

        issues = self.fixer.check_file("test.md",content)

        # Should not find code without example issue for get_messages
        code_issues = [i for i in issues if i.issue_type == "code_without_example" and "get_messages" in i.description]
        assert len(code_issues) == 0

    def test_detects_long_paragraphs(self):
        """Should flag paragraphs with > 5 lines without breaks."""
        content = """
        Line 1 of a very long paragraph.
        Line 2 continues the thought.
        Line 3 adds more information.
        Line 4 keeps going.
        Line 5 is still part of it.
        Line 6 makes it too long.
        Line 7 should trigger the warning.
        """

        issues = self.fixer.check_file("test.md",content)

        # Should find long paragraph issue
        para_issues = [i for i in issues if i.issue_type == "long_paragraph"]
        assert len(para_issues) > 0
        assert "long paragraph" in para_issues[0].description.lower()

    def test_does_not_flag_broken_up_paragraphs(self):
        """Should not flag well-structured content."""
        content = """
        This is a short paragraph.
        Just a few lines.

        This is another short paragraph.
        Also brief.

        - Bullet point 1
        - Bullet point 2
        """

        issues = self.fixer.check_file("test.md",content)

        # Should not find long paragraph issues
        para_issues = [i for i in issues if i.issue_type == "long_paragraph"]
        assert len(para_issues) == 0


class TestFixerIntegration:
    """Test overall fixer behavior."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = Config()
        self.fixer = GitHubInformedFixer(self.config)

    def test_returns_github_statistics(self):
        """Should provide statistics about GitHub research."""
        stats = self.fixer.get_statistics()

        assert stats["issues_analyzed"] == 50
        assert stats["repository"] == "anthropics/claude-code"
        assert stats["category_breakdown"]["Missing"] == "72%"
        assert "72% of documentation issues" in stats["top_insight"]

    def test_fix_method_preserves_content(self):
        """Fix method should preserve content (these are manual review items)."""
        content = "Original content"
        issues = []  # Empty issues list

        result = self.fixer.fix("test.md", content, issues)

        assert result.fixed_content == content
        assert result.content_changed == False

    def test_realistic_documentation_page(self):
        """Test on a realistic documentation page."""
        content = """
        # Claude Code API

        The API provides access to claude code functionality.

        You can use the function to execute commands and get results.

        The MCP protocol enables integration with external tools.
        """

        issues = self.fixer.check_file("test.md",content)

        # Should find several issues:
        # - Missing code example (mentions function without showing it)
        # - Undefined jargon (MCP)
        # - Possibly code without example
        assert len(issues) >= 2

        # Verify we're catching the key problems
        issue_types = {i.issue_type for i in issues}
        assert "missing_code_example" in issue_types or "undefined_jargon" in issue_types

    def test_well_written_documentation_page(self):
        """Test on well-written documentation."""
        content = """
        # Claude Code API Guide

        This guide explains how to use the Claude Code API to automate
        your documentation workflow. The API provides programmatic access
        to all Claude Code features.

        ## Prerequisites

        Before you begin, ensure you have:
        - Python 3.9 or higher installed
        - Claude Code installed and configured
        - API credentials from your Anthropic account

        ## Basic Usage

        Here's how to get started with the API:

        ```python
        from claude_code import Client

        # Initialize the client
        client = Client(api_key="your-key")

        # Execute a command
        result = client.execute("analyze docs/")
        print(result)
        ```

        ## Understanding MCP

        MCP (Model Context Protocol) is a standardized protocol for
        integrating external tools with Claude Code. It enables:

        - Secure tool integration
        - Standardized communication
        - Easy configuration

        Learn more in the [MCP documentation](../mcp/).

        ## Next Steps

        Now that you understand the basics:
        - Try the advanced examples
        - Read the API reference
        - Join the community forum
        """

        issues = self.fixer.check_file("test.md",content)

        # Well-written page should have few/no issues
        # Should not flag: long enough, has code examples, has prerequisites,
        # defines MCP, has good structure
        assert len(issues) <= 2  # Allow for minor issues, but should be clean
