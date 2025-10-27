# Claude Docs Quality Analyzer

> **A proof-of-concept project demonstrating technical documentation polish and information architecture skills for the Anthropic Technical Writer position.**

## 🎯 Project Overview

This project automates the key responsibilities of a Technical Writer focused on documentation polish and information architecture. It analyzes Mintlify-based documentation (like Claude Docs) and provides actionable insights for improvement.

### Key Capabilities

This analyzer addresses all key responsibilities from the job posting:

1. **✍️ Review and Rewrite for Clarity**
   - Readability metrics (sentence length, complexity)
   - Passive voice detection
   - Jargon and undefined terminology flagging
   - AI-powered clarity analysis using Claude API

2. **🏗️ Information Architecture**
   - Document structure analysis
   - Heading hierarchy validation
   - Navigation and findability assessment
   - Category balance and organization
   - Orphan content detection

3. **🎨 Consistency**
   - Terminology standardization
   - Formatting consistency checks
   - Style pattern analysis across files
   - Voice and tone uniformity

4. **📋 Style Guide Compliance**
   - Configurable style rules
   - Preferred terminology enforcement
   - Weak language detection
   - Code block formatting standards

5. **📚 Content Audits**
   - Gap analysis (missing topics)
   - Redundancy detection
   - Required section validation
   - Cross-file topic mapping

6. **📊 User Comprehension**
   - Link quality assessment
   - Context sufficiency checks
   - Example and prerequisite validation
   - Accessibility considerations

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8+
python --version

# Install dependencies
pip install anthropic pyyaml
```

### Basic Usage

```bash
# Analyze your documentation
python doc_analyzer.py /path/to/docs

# With configuration file
python doc_analyzer.py /path/to/docs --config config.yaml

# Generate multiple report formats
python doc_analyzer.py /path/to/docs --format all
```

### With Claude API (Optional but Recommended)

The analyzer can use Claude to perform AI-powered clarity checks:

```bash
export ANTHROPIC_API_KEY='your-api-key-here'
python doc_analyzer.py /path/to/docs
```

## 📖 How It Demonstrates Key Responsibilities

### 1. Review and Rewrite for Clarity

**What it does:**
- Detects overly long sentences (>30 words)
- Identifies passive voice constructions
- Flags weak or unnecessary words ("simply", "just", "easily")
- Uses Claude AI to analyze clarity and identify confusing explanations

**Example output:**
```
Medium | clarity | guides/quickstart.md:45
Type: sentence_too_long
Issue: Sentence has 42 words (recommend <30)
Suggestion: Break into shorter sentences for better readability
```

### 2. Information Architecture

**What it does:**
- Validates heading hierarchy (no H1 → H4 jumps)
- Detects overloaded categories (>20 docs)
- Identifies orphan files not in standard categories
- Checks for long sections without subheadings

**Example output:**
```
Medium | ia | api/reference.md:120
Type: heading_skip
Issue: Heading skips from H2 to H4
Suggestion: Use H3 instead to maintain hierarchy
```

### 3. Consistency

**What it does:**
- Tracks term variations across documentation
- Detects inconsistent list markers
- Identifies formatting inconsistencies
- Monitors code block language specifications

**Example output:**
```
Low | consistency | [multiple]
Type: term_inconsistency
Issue: Inconsistent usage of "setup": 4 variants found
Suggestion: Standardize on one term throughout documentation
```

### 4. Style Guide Compliance

**What it does:**
- Enforces preferred terminology
- Detects wordy phrases ("utilize" → "use")
- Validates code block syntax highlighting
- Checks for non-descriptive link text

**Example output:**
```
Low | style | concepts/architecture.md:78
Type: terminology
Issue: Use "use" instead of "utilize"
Suggestion: Replace with preferred term: "use"
```

### 5. Content Audits

**What it does:**
- Identifies missing required sections (overview, examples)
- Detects redundant content across files
- Maps topic coverage
- Flags missing documentation types (troubleshooting, migration)

**Example output:**
```
Medium | gaps | [documentation set]
Type: missing_content_type
Issue: No troubleshooting documentation found
Suggestion: Consider adding troubleshooting section
```

### 6. User Comprehension Improvements

**What it does:**
- Validates link quality and descriptions
- Checks for broken relative links
- Identifies empty or non-descriptive link text
- Ensures proper context and prerequisites

**Example output:**
```
Low | ux | tutorials/getting-started.md:34
Type: non_descriptive_link
Issue: Link text is non-descriptive: "here"
Suggestion: Use descriptive link text that explains destination
```

## 📊 Report Formats

### HTML Report (Recommended)
Interactive report with filtering, statistics, and color-coded severity:

```bash
python doc_analyzer.py /path/to/docs --format html
```

Features:
- Executive summary with key metrics
- Interactive filtering by severity
- Color-coded issues
- Actionable recommendations
- Context snippets for each issue

### JSON Report
Machine-readable format for CI/CD integration:

```bash
python doc_analyzer.py /path/to/docs --format json
```

### Markdown Report
GitHub-friendly format for issue tracking:

```bash
python doc_analyzer.py /path/to/docs --format markdown
```

## ⚙️ Configuration

Create a `config.yaml` file to customize analysis:

```yaml
style_rules:
  max_line_length: 100
  max_sentence_length: 30
  preferred_terms:
    utilize: use
    leverage: use
  avoid_terms:
    - simply
    - just
    - obviously

required_sections:
  - overview
  - prerequisites
  - examples

ia_patterns:
  guides:
    - overview
    - quickstart
    - tutorial
  reference:
    - api
    - cli
    - config
```

## 🔧 Advanced Features

### AI-Powered Analysis

When `ANTHROPIC_API_KEY` is set, the analyzer uses Claude to:
- Identify confusing explanations
- Detect missing context
- Flag jargon without definitions
- Spot logical gaps
- Suggest improvements

### Extensibility

The analyzer is designed to be extended:

```python
class CustomAnalyzer(DocumentationAnalyzer):
    def check_custom_rule(self, content: str, file_path: str):
        # Add custom checks
        pass
```

### CI/CD Integration

```yaml
# .github/workflows/docs-quality.yml
name: Documentation Quality Check

on: [pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Doc Analyzer
        run: |
          pip install anthropic pyyaml
          python doc_analyzer.py ./docs --format json
          # Fail if critical issues found
```

## 📈 Metrics Tracked

The analyzer tracks:
- **Total issues** by severity (critical, high, medium, low)
- **Issues by category** (clarity, IA, consistency, style, gaps, UX)
- **Per-file statistics**
- **Trend analysis** (when run repeatedly)

## 🎓 Demonstrating Technical Writer Skills

This project showcases:

1. **Deep understanding of documentation quality**
   - Automated checks based on best practices
   - Comprehensive coverage of common issues

2. **Technical proficiency**
   - Python development
   - API integration (Claude)
   - Multiple output formats
   - Extensible architecture

3. **Information Architecture expertise**
   - Systematic IA analysis
   - Category and navigation logic
   - Content organization principles

4. **Style guide knowledge**
   - Configurable rule engine
   - Terminology management
   - Voice and tone consistency

5. **User-centered thinking**
   - Actionable suggestions
   - Context-aware recommendations
   - Prioritization by impact

## 📝 Real-World Application

This analyzer can be used to:

1. **Onboarding new documentation**
   - Quick quality assessment
   - Identify improvement areas
   - Establish baseline metrics

2. **Continuous quality monitoring**
   - CI/CD integration
   - Track improvements over time
   - Prevent regression

3. **Style guide enforcement**
   - Automated compliance checking
   - Consistent application of standards
   - Reduce manual review burden

4. **Content planning**
   - Gap analysis informs roadmap
   - Redundancy reduction priorities
   - IA improvement initiatives

## ⭐ Future Enhancements

Potential additions:
- [ ] Accessibility checker (WCAG compliance)
- [ ] Screenshot and diagram validation
- [ ] API documentation linting
- [ ] User journey mapping
- [ ] Readability scoring (Flesch-Kincaid)
- [ ] Multi-language support
- [ ] Integration with documentation platforms
- [ ] A/B testing recommendations

## 🤝 Why This Matters for Anthropic

This project demonstrates:

1. **Immediate value**: Can be deployed on Claude Docs day one
2. **Scalability**: Handles large documentation sets efficiently
3. **Quality focus**: Aligns with Anthropic's high standards
4. **Technical depth**: Shows coding ability beyond basic writing
5. **User empathy**: Focuses on developer experience
6. **Continuous improvement**: Built for iteration and enhancement

## 📚 Additional Resources

- [Mintlify Documentation](https://mintlify.com/docs)
- [Claude API Documentation](https://docs.claude.com/en/api)
- [Documentation Style Guides](https://github.com/topics/documentation-style-guide)
- [Information Architecture Principles](https://www.nngroup.com/articles/information-architecture-study-guide/)

## 👤 About

Created as a proof-of-concept for the Anthropic Technical Writer position, demonstrating the ability to:
- Understand documentation quality at scale
- Build tools to support documentation work
- Think systematically about information architecture
- Apply best practices programmatically
- Deliver actionable insights

---

**Note:** This is a demonstration project. While functional, it would benefit from additional testing, refinement, and customization for production use at Anthropic.
