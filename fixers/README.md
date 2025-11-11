# Documentation Fixers Module

Comprehensive automated documentation quality fixer system with 18 specialized modules.

## Overview

The `fixers` module provides automated fixing capabilities for common documentation issues. Each fixer can detect specific problems and automatically apply safe, non-breaking corrections.

## Architecture

```
fixers/
├── base.py                              # Base fixer interface
├── __init__.py                          # Module exports
│
├── Core Fixers (Always Enabled)
├── frontmatter.py                       # Frontmatter validation & fixing
├── terminology.py                       # Terminology consistency
├── urls.py                              # URL formatting & validation
├── code_blocks.py                       # Code block quality
├── github_informed_fixer.py             # GitHub issue-based fixes
├── style_guide_validator.py             # AI-powered style validation*
│
├── High-Impact Fixers (Enabled by Default)
├── code_language_tags.py                # Code language tag detection
├── heading_hierarchy.py                 # Heading structure validation
├── capitalization_fixer.py              # Capitalization consistency
├── accessibility_fixer.py               # WCAG 2.1 AA compliance
│
└── Advanced Fixers (Manual Enable Required)
    ├── link_text_improver.py            # Link text quality
    ├── long_sentence_splitter.py        # Readability improvement
    ├── passive_voice_converter.py       # Active voice conversion
    ├── missing_prerequisites_detector.py # Content gap detection
    ├── terminology_consistency_fixer.py  # Advanced terminology
    ├── callout_standardization_fixer.py  # Callout formatting
    ├── broken_link_detector.py          # Broken link detection
    └── production_code_validator.py     # Production-ready patterns

* Requires ANTHROPIC_API_KEY
```

## Usage

### Command Line

```bash
# Dry run (preview changes without applying)
python doc_fixer.py /path/to/docs --dry-run

# Apply fixes with backups (recommended)
python doc_fixer.py /path/to/docs

# Apply fixes without backups
python doc_fixer.py /path/to/docs --no-backup

# Use custom config
python doc_fixer.py /path/to/docs --config custom_config.yaml
```

### Python API

```python
from doc_fixer import DocFixer
from pathlib import Path

# Initialize fixer
fixer = DocFixer()

# Process directory
stats = fixer.process_directory(
    docs_path=Path("./docs"),
    dry_run=True,  # Preview mode
    backup=True    # Create backups
)

# Print summary
print(stats.summary())
```

## Fixer Modules

### Core Fixers

#### 1. FrontmatterFixer
**Auto-fix:** ✅ Yes
**Impact:** Critical

Validates and adds missing frontmatter blocks required for documentation platforms.

**Fixes:**
- Missing frontmatter blocks
- Incomplete frontmatter (missing title/description)
- Invalid frontmatter formatting

**Example:**
```markdown
# Before
# My Page

Content here...

# After
---
title: "My Page"
description: "Description of my page"
---

# My Page

Content here...
```

#### 2. TerminologyFixer
**Auto-fix:** ✅ Yes
**Impact:** Medium

Replaces deprecated terminology and wordy phrases.

**Fixes:**
- "leverage" → "use"
- "in order to" → "to"
- "prior to" → "before"
- "utilize" → "use"
- "due to the fact that" → "because"
- "a number of" → "several"

#### 3. URLFixer
**Auto-fix:** ✅ Yes
**Impact:** Medium

Ensures proper URL formatting for internal and external links.

**Fixes:**
- Absolute URLs that should be relative
- Malformed URLs
- Missing protocols

#### 4. CodeBlockFixer
**Auto-fix:** ⚠️ Partial
**Impact:** High

Validates code blocks for proper formatting and language tags.

**Detects:**
- Missing language identifiers
- Unclosed code blocks
- Invalid syntax

**Note:** Language detection requires manual review for context.

#### 5. GitHubInformedFixer
**Auto-fix:** ✅ Yes
**Impact:** Medium

Applies fixes based on GitHub issues and user feedback patterns.

**Fixes:**
- Common user-reported issues
- Documentation gaps identified via GitHub
- Frequently confused concepts

#### 6. StyleGuideValidationFixer
**Auto-fix:** ⚠️ Partial
**Impact:** High
**Requires:** ANTHROPIC_API_KEY

AI-powered style guide validation using Claude.

**Checks:**
- Tone and voice consistency
- Clarity and conciseness
- Technical accuracy
- Style guide compliance

**Toggle:**
```bash
ENABLE_STYLE_GUIDE_VALIDATOR=false python doc_fixer.py ./docs
```

### High-Impact Fixers

#### 7. CodeLanguageTagFixer
**Auto-fix:** ❌ No (detection only)
**Impact:** Critical
**Enabled by default:** Yes

Detects code blocks missing language identifiers (required for Mintlify).

**Toggle:**
```bash
ENABLE_CODE_LANGUAGE_FIXER=false python doc_fixer.py ./docs
```

#### 8. HeadingHierarchyFixer
**Auto-fix:** ❌ No (detection only)
**Impact:** High
**Enabled by default:** Yes

Validates heading structure for proper hierarchy.

**Detects:**
- Skipped heading levels (H1 → H3)
- Multiple H1 tags
- Improper nesting

**Toggle:**
```bash
ENABLE_HEADING_HIERARCHY_FIXER=false python doc_fixer.py ./docs
```

#### 9. CapitalizationFixer
**Auto-fix:** ✅ Yes
**Impact:** High
**Enabled by default:** Yes

Enforces consistent capitalization for technical terms.

**Fixes:**
- "claude" → "Claude"
- "api" → "API"
- "json" → "JSON"
- "sdk" → "SDK"
- "rest" → "REST"
- "prompt caching" → "Prompt Caching"
- "extended thinking" → "Extended Thinking"

**Toggle:**
```bash
ENABLE_CAPITALIZATION_FIXER=false python doc_fixer.py ./docs
```

#### 10. AccessibilityFixer
**Auto-fix:** ⚠️ Partial
**Impact:** High
**Enabled by default:** Yes

Ensures WCAG 2.1 AA accessibility compliance.

**Auto-fixes:**
- Missing alt text (adds placeholders)
- Missing button types
- Basic semantic HTML issues

**Detects (manual review):**
- Poor/non-descriptive alt text
- Tables without proper headers
- Color-only information
- Complex accessibility issues

**Toggle:**
```bash
ENABLE_ACCESSIBILITY_FIXER=false python doc_fixer.py ./docs
```

### Advanced Fixers (Manual Enable)

#### 11. LinkTextImprover
**Auto-fix:** ❌ No
**Impact:** Medium
**Enabled by default:** No

Suggests improvements to link text for better SEO and accessibility.

**Detects:**
- Generic link text ("click here", "read more")
- Non-descriptive anchors
- Missing link context

**Enable:**
```bash
ENABLE_LINK_TEXT_IMPROVER=true python doc_fixer.py ./docs
```

#### 12. LongSentenceSplitter
**Auto-fix:** ❌ No
**Impact:** Medium
**Enabled by default:** No

Identifies sentences that are too long and complex.

**Detects:**
- Sentences >30 words
- Complex compound sentences
- Run-on sentences

**Enable:**
```bash
ENABLE_LONG_SENTENCE_SPLITTER=true python doc_fixer.py ./docs
```

#### 13. PassiveVoiceConverter
**Auto-fix:** ❌ No
**Impact:** Low
**Enabled by default:** No

Detects passive voice usage and suggests active alternatives.

**Enable:**
```bash
ENABLE_PASSIVE_VOICE_CONVERTER=true python doc_fixer.py ./docs
```

#### 14. MissingPrerequisitesDetector
**Auto-fix:** ❌ No
**Impact:** High
**Enabled by default:** No

Identifies procedural content missing prerequisites sections.

**Detects:**
- Installation guides without prereqs
- Tutorials missing setup steps
- Missing environment requirements

**Enable:**
```bash
ENABLE_MISSING_PREREQUISITES_DETECTOR=true python doc_fixer.py ./docs
```

#### 15. TerminologyConsistencyFixer
**Auto-fix:** ⚠️ Partial
**Impact:** Medium
**Enabled by default:** No

Advanced terminology consistency beyond basic replacements.

**Enable:**
```bash
ENABLE_TERMINOLOGY_CONSISTENCY_FIXER=true python doc_fixer.py ./docs
```

#### 16. CalloutStandardizationFixer
**Auto-fix:** ✅ Yes
**Impact:** Medium
**Enabled by default:** No

Standardizes callout/admonition formatting across documentation.

**Fixes:**
- Inconsistent callout syntax
- Missing callout types
- Improper callout formatting

**Enable:**
```bash
ENABLE_CALLOUT_STANDARDIZATION_FIXER=true python doc_fixer.py ./docs
```

#### 17. BrokenLinkDetector
**Auto-fix:** ❌ No
**Impact:** High
**Enabled by default:** No

Detects broken internal links and missing pages.

**Detects:**
- Links to non-existent files
- Broken anchor links
- Expected pages that don't exist
- Invalid URL formats

**Enable:**
```bash
ENABLE_BROKEN_LINK_DETECTOR=true python doc_fixer.py ./docs
```

#### 18. ProductionCodeValidator
**Auto-fix:** ❌ No
**Impact:** High
**Enabled by default:** No

Validates code examples for production-ready patterns.

**Detects:**
- Missing error handling
- Missing retry logic
- Hardcoded credentials (critical!)
- Missing timeout configuration
- Lack of logging

**Enable:**
```bash
ENABLE_PRODUCTION_CODE_VALIDATOR=true python doc_fixer.py ./docs
```

## Configuration

### config.yaml

```yaml
# Core settings
repo_type: mintlify  # or 'docusaurus', 'vitepress', etc.

# Terminology replacements
terminology:
  deprecated:
    - old: "leverage"
      new: "use"
    - old: "in order to"
      new: "to"

# Capitalization rules
capitalization:
  proper_nouns:
    - "Claude"
    - "Anthropic"
  acronyms:
    - "API"
    - "JSON"
    - "SDK"
    - "REST"
  brand_terms:
    - pattern: "prompt caching"
      replacement: "Prompt Caching"
    - pattern: "extended thinking"
      replacement: "Extended Thinking"

# URL validation
urls:
  allow_absolute: false
  internal_domains:
    - "docs.anthropic.com"
    - "claude.ai"

# Code validation
code_blocks:
  require_language_tag: true
  allowed_languages:
    - "python"
    - "typescript"
    - "javascript"
    - "bash"
    - "json"

# Accessibility
accessibility:
  require_alt_text: true
  require_table_headers: true
  check_color_only: true
```

### Environment Variables

```bash
# AI-powered features (requires API key)
export ANTHROPIC_API_KEY="your-key-here"

# Toggle individual fixers
export ENABLE_STYLE_GUIDE_VALIDATOR=true
export ENABLE_CODE_LANGUAGE_FIXER=true
export ENABLE_HEADING_HIERARCHY_FIXER=true
export ENABLE_CAPITALIZATION_FIXER=true
export ENABLE_ACCESSIBILITY_FIXER=true

# Advanced fixers (disabled by default)
export ENABLE_LINK_TEXT_IMPROVER=false
export ENABLE_LONG_SENTENCE_SPLITTER=false
export ENABLE_PASSIVE_VOICE_CONVERTER=false
export ENABLE_MISSING_PREREQUISITES_DETECTOR=false
export ENABLE_TERMINOLOGY_CONSISTENCY_FIXER=false
export ENABLE_CALLOUT_STANDARDIZATION_FIXER=false
export ENABLE_BROKEN_LINK_DETECTOR=false
export ENABLE_PRODUCTION_CODE_VALIDATOR=false
```

## Testing

### Run Fixers in Dry-Run Mode

```bash
# Test all enabled fixers
python doc_fixer.py ./docs --dry-run

# Test specific directory
python doc_fixer.py ./docs/api --dry-run

# Test with all advanced fixers enabled
ENABLE_BROKEN_LINK_DETECTOR=true \
ENABLE_PRODUCTION_CODE_VALIDATOR=true \
ENABLE_LONG_SENTENCE_SPLITTER=true \
python doc_fixer.py ./docs --dry-run
```

### Verify Fixes

```bash
# Run analyzer before fixing
python doc_analyzer.py ./docs --format markdown --output reports/before

# Apply fixes
python doc_fixer.py ./docs

# Run analyzer after fixing
python doc_analyzer.py ./docs --format markdown --output reports/after

# Compare results
diff reports/before reports/after
```

## Best Practices

### 1. Always Use Dry-Run First
```bash
# Preview changes
python doc_fixer.py ./docs --dry-run

# Review output carefully
# Apply fixes only after verification
python doc_fixer.py ./docs
```

### 2. Enable Backups
```bash
# Default (backups enabled)
python doc_fixer.py ./docs

# Backups saved to .doc_fixer_backups/
```

### 3. Start with Core Fixers
Enable advanced fixers gradually after understanding their impact:

```bash
# Stage 1: Core fixers only (default)
python doc_fixer.py ./docs --dry-run

# Stage 2: Add high-impact fixers
ENABLE_CODE_LANGUAGE_FIXER=true python doc_fixer.py ./docs --dry-run

# Stage 3: Add advanced detectors
ENABLE_BROKEN_LINK_DETECTOR=true \
ENABLE_PRODUCTION_CODE_VALIDATOR=true \
python doc_fixer.py ./docs --dry-run
```

### 4. Review Manual-Fix Issues
Some fixers only detect issues and require manual intervention:

```bash
# Generate report of manual fixes needed
python doc_analyzer.py ./docs --format markdown > manual_fixes.md

# Review and prioritize
cat manual_fixes.md | grep "Auto-fixable: False"
```

### 5. Integrate into CI/CD
```yaml
# .github/workflows/docs-quality.yml
name: Documentation Quality

on: [pull_request]

jobs:
  check-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt

      - name: Run doc fixer (dry-run)
        run: |
          python doc_fixer.py ./docs --dry-run

      - name: Run doc analyzer
        run: |
          python doc_analyzer.py ./docs --format markdown --output reports/pr_analysis

      - name: Comment PR with results
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('reports/pr_analysis', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

## Performance

### Benchmarks
- **Small docs (10-50 files):** ~30 seconds
- **Medium docs (50-150 files):** ~2-4 minutes
- **Large docs (150-300 files):** ~5-10 minutes

### Optimization Tips
1. Disable unnecessary fixers for faster execution
2. Use `--no-backup` for repeated testing (not recommended for production)
3. Process directories in parallel for very large documentation sets
4. Cache AI analysis results to avoid repeated API calls

## Troubleshooting

### Issue: AI Analysis Failures
```
⚠️  AI analysis failed: JSON parsing error
```

**Solution:**
- Non-critical - fixer continues with other checks
- Set `ENABLE_STYLE_GUIDE_VALIDATOR=false` to disable AI analysis
- Check ANTHROPIC_API_KEY is set correctly

### Issue: Too Many Issues Detected
```
Found 5000+ issues across 100 files
```

**Solution:**
- Start with high-severity issues first
- Enable fixers gradually
- Use dry-run mode to preview changes
- Filter by category: `--category critical`

### Issue: Fixer Modified Wrong Content
```
Fixer changed code block content
```

**Solution:**
- Restore from .doc_fixer_backups/
- Report issue with example
- Disable specific fixer temporarily
- Review fixer configuration

## Contributing

### Adding a New Fixer

1. Create new fixer class inheriting from `BaseFixer`:

```python
from .base import BaseFixer
from core.models import Issue, FixResult

class MyCustomFixer(BaseFixer):
    @property
    def name(self) -> str:
        return "My Custom Fixer"

    def check_file(self, file_path: str, content: str) -> List[Issue]:
        issues = []
        # Detection logic here
        return issues

    def fix(self, file_path: str, content: str, issues: List[Issue]) -> FixResult:
        # Fixing logic here
        return FixResult(...)
```

2. Register in `__init__.py`:

```python
from .my_custom_fixer import MyCustomFixer

__all__ = [
    # ... existing fixers
    'MyCustomFixer',
]
```

3. Add to `doc_fixer.py`:

```python
if os.getenv('ENABLE_MY_CUSTOM_FIXER', 'false').lower() not in ['false', '0', 'no']:
    self.fixers.append(MyCustomFixer(self.config))
    print("✓ My Custom Fixer enabled")
```

4. Add tests:

```python
def test_my_custom_fixer():
    fixer = MyCustomFixer(Config())
    issues = fixer.check_file("test.md", "test content")
    assert len(issues) > 0
```

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions:
- GitHub: https://github.com/your-username/docs_analyzer
- Email: your-email@example.com

---

**Version:** 1.0.0
**Last Updated:** 2025-10-31
**Maintainer:** Alden Weaver
