# Enhanced Documentation Analyzer - Usage Guide

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up Claude API key
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Basic Usage

```bash
# Analyze local documentation
python doc_analyzer.py ./docs

# Analyze with configuration file
python doc_analyzer.py --config config.yaml

# Clone and analyze remote repository
python doc_analyzer.py --repo-url https://github.com/username/docs

# Generate all report formats
python doc_analyzer.py ./docs --format all
```

## 📋 What's New in Enhanced Version

### Phase 1: Core Improvements ✅
- **MDX Support**: Full frontmatter parsing and validation
- **Mintlify Integration**: Platform-specific checks for Mintlify docs
- **Configurable Repository**: Analyze local or remote repositories
- **Enhanced Style Rules**: Pre-populated with Claude Docs best practices

### Phase 2: Advanced Analysis ✅
- **AI Semantic Analysis**: Claude-powered clarity and gap detection
- **Cross-Reference Validation**: Detect broken links and missing prerequisites
- **Component Validation**: Check Mintlify component usage
- **Internal Link Enforcement**: Ensure relative paths for internal navigation

### Phase 3: Intelligence Features ✅
- **User Journey Mapping**: Validate documentation supports common user paths
- **Content Duplication Detection**: Find similar/duplicate content
- **Platform Detection**: Auto-detect Mintlify, Docusaurus, MkDocs, etc.
- **Comprehensive Gap Analysis**: Missing sections, incomplete journeys

## 🔧 Configuration

### Enhanced Config File

The `config.yaml` includes:

```yaml
# Repository settings
repository:
  path: "./docs"
  type: "auto"  # or: mintlify, docusaurus, mkdocs, generic

# Mintlify-specific validation
mintlify:
  enabled: true
  required_frontmatter: [title, description]
  components:
    enabled: true

# Claude Docs style rules (pre-populated)
style_rules:
  max_sentence_length: 30
  voice:
    person: "second"  # Use "you"
  avoid_terms: [simply, just, easily, obviously]
  code_blocks:
    require_language_tag: true

# Gap detection with AI
gap_detection:
  semantic_analysis:
    enabled: true
    model: "claude-sonnet-4-5-20250929"
  required_journeys:
    - name: "First time setup"
      steps: [overview, install, authenticate, first-use]

# And much more...
```

### Key Configuration Sections

#### 1. Repository Configuration

```yaml
repository:
  path: "./my-docs"
  type: "mintlify"  # or auto-detect
  
  # For remote repositories
  remote:
    enabled: false
    url: "https://github.com/user/repo"
    branch: "main"
```

#### 2. Mintlify Settings

```yaml
mintlify:
  enabled: true
  config_file: "mint.json"
  required_frontmatter: [title, description]
  
  links:
    internal_must_be_relative: true  # Critical!
    check_broken_links: true
```

#### 3. AI Analysis

```yaml
claude_api:
  api_key_env: "ANTHROPIC_API_KEY"
  default_model: "claude-sonnet-4-5-20250929"
  
gap_detection:
  semantic_analysis:
    enabled: true
    max_tokens: 4000
```

## 📊 Understanding Reports

### HTML Report (Recommended)

The HTML report includes:
- **Executive Summary**: Key metrics at a glance
- **Severity Breakdown**: Critical, High, Medium, Low issues
- **Category Analysis**: Issues grouped by type
- **Recommendations**: Actionable next steps
- **AI Insights**: Semantic gaps and patterns identified by Claude
- **Detailed Issues**: Each issue with context and suggestions

### JSON Report

Perfect for CI/CD integration:

```json
{
  "timestamp": "2025-10-26T...",
  "repository": {
    "path": "./docs",
    "type": "mintlify"
  },
  "summary": {
    "total_files": 42,
    "total_issues": 87,
    "by_severity": {
      "critical": 5,
      "high": 12,
      "medium": 35,
      "low": 35
    }
  },
  "recommendations": [...],
  "ai_insights": [...],
  "issues": [...]
}
```

### Markdown Report

GitHub-friendly format for tracking:

```markdown
# Enhanced Documentation Analysis Report

**Generated:** 2025-10-26
**Files Analyzed:** 42
**Total Issues:** 87

## Summary
| Severity | Count |
|----------|-------|
| Critical | 5     |
| High     | 12    |
...
```

## 🎯 Issue Categories Explained

### Critical Issues (Fix Immediately)
- **missing_frontmatter**: MDX files without YAML frontmatter
- **absolute_internal_urls**: Internal links using absolute URLs (breaks Mintlify)
- **broken_links**: Links to non-existent files
- **missing_language_tag**: Code blocks without language specification

### High Priority
- **missing_required_section**: Missing essential documentation sections
- **semantic_gap**: AI-identified conceptual gaps
- **incomplete_user_journey**: User paths not fully supported
- **empty_link_text**: Links with no descriptive text

### Medium Priority
- **heading_skip**: Heading hierarchy violations
- **long_section**: Sections that need subheadings
- **passive_voice**: Use of passive voice
- **term_inconsistency**: Inconsistent terminology usage

### Low Priority
- **line_too_long**: Lines exceeding recommended length
- **sentence_too_long**: Sentences with too many words
- **weak_language**: Words like "simply", "just", "easily"
- **terminology_preference**: Non-preferred terms

## 🔍 Advanced Features

### 1. AI Semantic Analysis

When enabled (requires `ANTHROPIC_API_KEY`):
- Analyzes clarity and comprehension
- Identifies conceptual gaps
- Detects missing prerequisites
- Finds undefined jargon
- Maps user journey completeness

**Disable for faster analysis:**
```bash
python doc_analyzer.py ./docs --no-ai
```

### 2. Platform-Specific Validation

#### Mintlify Checks:
- Frontmatter validation (title, description required)
- Component usage validation
- Relative link enforcement (critical!)
- Navigation structure validation

#### Generic Markdown:
- Standard readability checks
- Style guide compliance
- Link validation
- Structure analysis

### 3. Content Duplication Detection

Finds:
- Similar paragraphs (80%+ similarity)
- Duplicate code examples
- Redundant explanations

**Configuration:**
```yaml
duplication_detection:
  enabled: true
  similarity_threshold: 0.8  # 80% similar = duplicate
  check_levels:
    - paragraph
    - code_block
    - heading_structure
```

### 4. User Journey Validation

Checks if documentation supports common paths:

```yaml
required_journeys:
  - name: "First time setup"
    steps: [overview, install, authenticate, first-use]
  
  - name: "Troubleshooting"
    steps: [error-identification, diagnostic-guide, solution]
```

## 📈 Best Practices

### For Your Clone

1. **Start with Configuration**
   ```bash
   # Copy and customize
   cp config.yaml my_config.yaml
   # Edit repository path and rules
   ```

2. **Run Initial Analysis**
   ```bash
   python doc_analyzer.py --config my_config.yaml --format all
   ```

3. **Review Critical Issues First**
   - Fix broken links
   - Add missing frontmatter
   - Convert absolute to relative URLs

4. **Document Improvements**
   - Track changes in CHANGELOG.md
   - Create before/after examples
   - Measure improvement metrics

### For Project

1. **Set Up Your Clone**
   ```bash
   # Create docs directory
   mkdir -p docs/claude-code
   
   # Add 8-12 key pages
   # - overview.md(x)
   # - quickstart.md(x)
   # - common-workflows.md(x)
   # - cli-reference.md(x)
   # etc.
   ```

2. **Run Analysis**
   ```bash
   python doc_analyzer.py ./docs --config config.yaml --format all
   ```

3. **Fix Top Issues**
   - Address all critical issues
   - Fix 80% of high priority issues
   - Document your fixes

4. **Create Before/After**
   ```bash
   # Before
   - Had 15 critical issues
   - Missing frontmatter on all MDX files
   - Used absolute URLs
   
   # After
   - 0 critical issues
   - All files have proper frontmatter
   - All internal links are relative
   ```

## 🚨 Common Issues & Solutions

### "ImportError: No module named 'anthropic'"

```bash
pip install anthropic
```

### "No API key found"

```bash
export ANTHROPIC_API_KEY='your-key-here'
# Or add to ~/.bashrc or ~/.zshrc
```

### "Repository type not detected"

Specify manually:
```bash
python doc_analyzer.py ./docs --repo-type mintlify
```

### "Too many issues found"

Start with critical only:
```python
# In config.yaml
severity_thresholds:
  critical: [...]  # Focus here first
```

## 🎓 Understanding the Output

### Example Analysis

```
🔍 Starting enhanced documentation analysis...
Repository type: mintlify
Found 12 documentation files

  Analyzing: claude-code/overview.mdx
  Analyzing: claude-code/quickstart.mdx
  ...

📊 Running cross-file analysis...
🏗️  Analyzing information architecture...
🎨 Analyzing consistency...

🧠 Running advanced analysis...
🔍 Detecting content gaps...
🔍 Detecting content duplication...
🚶 Validating user journeys...

🤖 Running AI semantic analysis...

💡 Generating recommendations...

✅ Analysis complete! Found 47 issues
```

### Reading the Numbers

```
✅ Analysis complete!
   Repository: mintlify
   Total files: 12
   Total issues: 47
   Critical: 2   ← Fix immediately!
   High: 8       ← Address this week
   Medium: 23    ← Next sprint
   Low: 14       ← Nice to have
   AI Insights: 5  ← Review for strategic improvements
```

## 🔗 Integration Examples

### GitHub Actions

```yaml
name: Documentation Quality Check

on: [pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run analyzer
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python doc_analyzer.py ./docs --format json
      
      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: analysis-report
          path: doc_analysis_report.json
      
      - name: Check critical issues
        run: |
          CRITICAL=$(python -c "import json; print(json.load(open('doc_analysis_report.json'))['summary']['by_severity'].get('critical', 0))")
          if [ "$CRITICAL" -gt "0" ]; then
            echo "❌ $CRITICAL critical issues found!"
            exit 1
          fi
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running documentation quality check..."
python doc_analyzer.py ./docs --no-ai --format json

CRITICAL=$(python -c "import json; print(json.load(open('doc_analysis_report.json'))['summary']['by_severity'].get('critical', 0))")

if [ "$CRITICAL" -gt "0" ]; then
    echo "❌ Cannot commit: $CRITICAL critical documentation issues found"
    echo "Run: python doc_analyzer.py ./docs --format html"
    echo "Then fix critical issues before committing"
    exit 1
fi

echo "✅ Documentation quality check passed"
```

## 🎯 Success Metrics

Track improvements over time:

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Critical Issues | 15 | 0 | 100% |
| High Priority | 32 | 5 | 84% |
| Total Issues | 127 | 47 | 63% |
| Files with Frontmatter | 0% | 100% | N/A |
| Relative Link Usage | 40% | 100% | 150% |

## 📞 Getting Help

### Debug Mode

```bash
# More verbose output
python doc_analyzer.py ./docs --format json | tee analysis.log
```

### Test with Sample Data

```bash
# Create sample docs
mkdir -p test-docs
cat > test-docs/sample.mdx << 'EOF'
---
title: Sample Page
description: This is a test
---

# Sample Page

Simply use this [link](https://docs.example.com/absolute) to navigate.

```
# Code without language tag
print("hello")
```
EOF

# Run analysis
python doc_analyzer.py ./test-docs
```

## 🎉 Summary

The enhanced analyzer provides:
- ✅ Comprehensive quality checking
- ✅ AI-powered semantic analysis
- ✅ Platform-specific validation
- ✅ Configurable rules and thresholds
- ✅ Multiple report formats
- ✅ CI/CD integration ready
- ✅ Pre-populated with Claude Docs best practices

Perfect for demonstrating technical writing expertise to Anthropic!
