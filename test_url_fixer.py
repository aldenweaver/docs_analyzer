"""
Basic tests for URLFixer
"""

import pytest
from pathlib import Path
from core.config import Config
from fixers.urls import URLFixer


class TestURLFixer:
    """Test suite for URLFixer"""

    @pytest.fixture
    def config(self):
        config_path = Path(__file__).parent / "config.yaml"
        return Config(config_path)

    @pytest.fixture
    def fixer(self, config):
        return URLFixer(config)

    def test_poor_link_text_detection(self, fixer):
        """Test detection of poor link text"""
        content = """---
title: Test
description: Test page
---

# Test Page

Click [here](/docs/guide) to learn more.
"""
        issues = fixer.check_file("test.mdx", content)
        poor_text_issues = [i for i in issues if i.issue_type == "poor_link_text"]
        assert len(poor_text_issues) == 1
        assert poor_text_issues[0].auto_fixable is False

    def test_absolute_url_detection(self, fixer):
        """Test detection of absolute internal URLs"""
        content = """---
title: Test
description: Test page
---

# Test Page

See the [API reference](https://docs.anthropic.com/en/docs/api) for details.
"""
        issues = fixer.check_file("test.mdx", content)
        absolute_issues = [i for i in issues if i.issue_type == "absolute_internal_url"]
        assert len(absolute_issues) == 1
        assert absolute_issues[0].auto_fixable is True

    def test_fix_absolute_urls(self, fixer):
        """Test fixing absolute URLs to relative"""
        content = """---
title: Test
description: Test page
---

# Test Page

See the [API reference](https://docs.anthropic.com/en/docs/api) for details.
"""
        issues = fixer.check_file("test.mdx", content)
        absolute_issues = [i for i in issues if i.issue_type == "absolute_internal_url"]

        result = fixer.fix("test.mdx", content, absolute_issues)

        assert result.content_changed is True
        assert "/en/docs/api" in result.fixed_content
        assert "https://docs.anthropic.com" not in result.fixed_content

    def test_external_urls_not_flagged(self, fixer):
        """Test that external URLs are not flagged"""
        content = """---
title: Test
description: Test page
---

# Test Page

Visit [GitHub](https://github.com) for the code.
"""
        issues = fixer.check_file("test.mdx", content)
        absolute_issues = [i for i in issues if i.issue_type == "absolute_internal_url"]
        assert len(absolute_issues) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
