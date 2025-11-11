"""
Tests for FrontmatterFixer
"""

import pytest
from pathlib import Path
from core.config import Config
from core.models import Issue, FixResult
from fixers.frontmatter import FrontmatterFixer


class TestFrontmatterFixer:
    """Test suite for FrontmatterFixer"""

    @pytest.fixture
    def config(self):
        """Load configuration"""
        config_path = Path(__file__).parent / "config.yaml"
        return Config(config_path)

    @pytest.fixture
    def fixer(self, config):
        """Create FrontmatterFixer instance"""
        return FrontmatterFixer(config)

    def test_missing_frontmatter(self, fixer):
        """Test detection of missing frontmatter"""
        content = """# Test Page

This is a test page without frontmatter.
"""
        issues = fixer.check_file("test.mdx", content)

        assert len(issues) == 1
        assert issues[0].severity == "critical"
        assert issues[0].issue_type == "missing_frontmatter"
        assert issues[0].auto_fixable is True

    def test_fix_missing_frontmatter(self, fixer):
        """Test fixing missing frontmatter"""
        content = """# Test Page

This is a test page without frontmatter.
"""
        issues = fixer.check_file("test.mdx", content)
        result = fixer.fix("test.mdx", content, issues)

        assert result.content_changed is True
        assert len(result.fixes_applied) > 0
        assert "Added missing frontmatter block" in result.fixes_applied
        assert "---" in result.fixed_content
        assert "title:" in result.fixed_content
        assert "description:" in result.fixed_content

    def test_missing_title_field(self, fixer):
        """Test detection of missing title field"""
        content = """---
description: This is a properly sized description with enough characters for testing purposes.
---

# Test Page

This is a test page.
"""
        issues = fixer.check_file("test.mdx", content)

        assert len(issues) == 1
        assert issues[0].issue_type == "missing_frontmatter_field"
        assert "title" in issues[0].description
        assert issues[0].auto_fixable is True

    def test_missing_description_field(self, fixer):
        """Test detection of missing description field"""
        content = """---
title: Test Page
---

# Test Page

This is a test page.
"""
        issues = fixer.check_file("test.mdx", content)

        assert len(issues) == 1
        assert issues[0].issue_type == "missing_frontmatter_field"
        assert "description" in issues[0].description
        assert issues[0].auto_fixable is True

    def test_fix_missing_fields(self, fixer):
        """Test fixing missing frontmatter fields"""
        content = """---
title: Test Page
---

# Test Page

This is a test page with enough content to generate a description.
"""
        issues = fixer.check_file("test.mdx", content)
        result = fixer.fix("test.mdx", content, issues)

        assert result.content_changed is True
        assert "description:" in result.fixed_content
        assert "Added missing 'description' field" in result.fixes_applied

    def test_description_too_long(self, fixer):
        """Test detection of description that's too long"""
        long_description = "A" * 200
        content = f"""---
title: Test Page
description: {long_description}
---

# Test Page
"""
        issues = fixer.check_file("test.mdx", content)

        desc_issues = [i for i in issues if i.issue_type == "description_too_long"]
        assert len(desc_issues) == 1
        assert desc_issues[0].severity == "medium"
        assert desc_issues[0].auto_fixable is False

    def test_description_too_short(self, fixer):
        """Test detection of description that's too short"""
        content = """---
title: Test Page
description: Too short
---

# Test Page
"""
        issues = fixer.check_file("test.mdx", content)

        desc_issues = [i for i in issues if i.issue_type == "description_too_short"]
        assert len(desc_issues) == 1
        assert desc_issues[0].severity == "low"
        assert desc_issues[0].auto_fixable is False

    def test_valid_frontmatter(self, fixer):
        """Test that valid frontmatter passes all checks"""
        content = """---
title: Test Page
description: This is a well-formed description with appropriate length for SEO purposes.
---

# Test Page

Content here.
"""
        issues = fixer.check_file("test.mdx", content)

        assert len(issues) == 0

    def test_generate_title_from_h1(self, fixer):
        """Test title generation from H1 heading"""
        content = """# My Awesome Title

Content here.
"""
        title = fixer._generate_title("test.mdx", content)
        assert title == "My Awesome Title"

    def test_generate_title_from_filename(self, fixer):
        """Test title generation from filename when no H1"""
        content = """Content without heading."""
        title = fixer._generate_title("my-test-page.mdx", content)
        assert title == "My Test Page"

    def test_generate_description(self, fixer):
        """Test description generation from content"""
        content = """---
title: Test
---

# Test Page

This is the first paragraph that should be used for description generation.

This is the second paragraph.
"""
        description = fixer._generate_description(content)
        assert len(description) > 0
        assert "first paragraph" in description.lower()

    def test_process_file_integration(self, fixer, tmp_path):
        """Test complete file processing workflow"""
        # Create test file
        test_file = tmp_path / "test.mdx"
        content = """# Test Page

This is a test page without frontmatter but with content.
"""
        test_file.write_text(content)

        # Process file
        result = fixer.process_file(str(test_file))

        assert result.error is None
        assert result.content_changed is True
        assert len(result.fixes_applied) > 0

    def test_only_mdx_files(self, fixer):
        """Test that non-MDX files are skipped"""
        content = "Some Python code"
        issues = fixer.check_file("test.py", content)

        assert len(issues) == 0

    def test_empty_frontmatter_fields(self, fixer):
        """Test detection of empty frontmatter fields"""
        content = """---
title: ""
description: ""
---

# Test Page

Content here.
"""
        issues = fixer.check_file("test.mdx", content)

        # Should detect both as missing
        assert len(issues) == 2
        field_issues = [i for i in issues if i.issue_type == "missing_frontmatter_field"]
        assert len(field_issues) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
