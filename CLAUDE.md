# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **documentation quality analyzer** designed for Mintlify-based documentation (like Claude Docs). It's a proof-of-concept that demonstrates technical documentation polish and information architecture skills. The analyzer performs automated quality checks on documentation and generates reports in multiple formats (JSON, HTML, Markdown).

**Core Purpose:** Automate key technical writing responsibilities including clarity checks, information architecture validation, style guide compliance, consistency analysis, and content gap detection.

## Key Commands

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set API key for AI-powered analysis (optional but recommended)
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Running the Analyzer
```bash
# Basic analysis
python doc_analyzer.py /path/to/docs

# With configuration file
python doc_analyzer.py /path/to/docs --config config.yaml

# Generate specific report format
python doc_analyzer.py /path/to/docs --format html
python doc_analyzer.py /path/to/docs --format json
python doc_analyzer.py /path/to/docs --format markdown
python doc_analyzer.py /path/to/docs --format all

# Analyze remote repository
python doc_analyzer.py --repo-url https://github.com/user/docs --repo-type mintlify

# Disable AI analysis (faster, less comprehensive)
python doc_analyzer.py /path/to/docs --no-ai
```

### Testing
```bash
# Run all tests
pytest test_analyzer.py -v

# Run with coverage
pytest test_analyzer.py -v --cov=doc_analyzer

# Run specific test class
pytest test_analyzer.py::TestDocumentationAnalyzer -v

# Skip tests requiring API key
pytest test_analyzer.py -v -m "not skipif"
```

## Architecture

### Core Components

**RepositoryManager** (`doc_analyzer.py:85-174`)
- Auto-detects documentation platform (Mintlify, Docusaurus, MkDocs, generic)
- Handles local and remote repositories (with git cloning)
- Manages file inclusion/exclusion patterns
- Loads platform-specific configuration (e.g., `mint.json` for Mintlify)

**MDXParser** (`doc_analyzer.py:176-211`)
- Extracts YAML frontmatter from MDX files
- Parses JSX-style Mintlify components
- Handles both `.md` and `.mdx` formats

**MintlifyValidator** (`doc_analyzer.py:213-347`)
- Validates frontmatter requirements (title, description)
- Checks component usage against valid Mintlify components
- **CRITICAL:** Validates internal links use relative paths (absolute URLs break Mintlify builds)
- Enforces SEO-optimal description lengths (20-160 characters)

**SemanticAnalyzer** (`doc_analyzer.py:349-481`)
- AI-powered clarity analysis using Claude API
- Detects confusing explanations, missing context, undefined jargon
- Identifies conceptual gaps across documentation set
- Requires `ANTHROPIC_API_KEY` environment variable

**ContentDuplicationDetector** (`doc_analyzer.py:483-543`)
- Finds duplicate/similar content across files using SequenceMatcher
- Configurable similarity threshold (default: 80%)
- Helps identify redundancy and consolidation opportunities

**UserJourneyAnalyzer** (`doc_analyzer.py:545-579`)
- Validates documentation supports required user journeys
- Checks for missing journey steps (e.g., installation, authentication, first-use)

**EnhancedDocumentationAnalyzer** (`doc_analyzer.py:581-1269`)
- Main orchestrator that runs all analysis phases
- Phase 1: File-level checks (readability, style, structure, formatting, links)
- Phase 2: Cross-file analysis (IA, consistency)
- Phase 3: Advanced analysis (content gaps, duplication, user journeys, AI semantic analysis)
- Generates reports with recommendations and AI insights

### Analysis Categories

Issues are categorized as:
- **clarity**: Readability, sentence length, weak language
- **ia**: Information architecture, heading hierarchy, category organization
- **consistency**: Terminology variations, formatting inconsistencies
- **style**: Style guide compliance, preferred terminology, passive voice
- **gaps**: Missing content types, redundancy, incomplete user journeys
- **ux**: Link quality, descriptive text, broken links
- **mintlify**: Platform-specific requirements (frontmatter, components, relative links)

### Severity Levels

- **critical**: Broken links, missing frontmatter, absolute internal URLs, missing code block language tags (Mintlify)
- **high**: Empty link text, file errors, missing required sections
- **medium**: Heading hierarchy issues, passive voice, long sections
- **low**: Line length, terminology preferences, weak language

## Configuration System

Configuration is loaded from `config.yaml` (or specified via `--config`). Key configuration sections:

**repository**: Path, type, remote settings, file patterns
**mintlify**: Frontmatter requirements, valid components, link validation
**style_rules**: Line/sentence limits, preferred terminology, avoid terms
**ia_patterns**: Category structure, max docs per category
**gap_detection**: Semantic analysis, required user journeys
**duplication_detection**: Similarity thresholds
**claude_api**: Model selection, rate limits, retry configuration

The config file is extensively documented with best practices for Claude Docs/Mintlify.

## Critical Mintlify Requirements

When working with Mintlify documentation:

1. **Internal links MUST use relative paths**: `./page.md` or `../section/page.md`, NOT absolute URLs like `https://docs.claude.com/page`
2. **MDX files MUST have frontmatter** with at minimum `title` and `description`
3. **Code blocks MUST specify language**: ` ```python ` not just ` ``` `
4. **Description length**: 20-160 characters for SEO optimization
5. **Valid Mintlify components only**: Card, CardGroup, Accordion, Tabs, CodeGroup, Info, Warning, etc.

Violations of these are marked as **critical** severity.

## Data Flow

1. `RepositoryManager` detects platform and loads files
2. `EnhancedDocumentationAnalyzer` runs three phases:
   - Phase 1: File-by-file analysis (all validators run on each file)
   - Phase 2: Cross-file analysis (IA patterns, consistency checks)
   - Phase 3: Advanced analysis (AI semantic gaps, duplication, user journeys)
3. Issues are collected in `AnalysisReport` with categorization
4. Reports are exported in requested format(s)

## AI Integration

The analyzer uses the Anthropic API (Claude) for:
- **Clarity checks** (`analyze_clarity`): Identifies confusing explanations, missing context, undefined jargon per file
- **Semantic gap analysis** (`analyze_semantic_gaps`): Identifies missing user journey steps, concepts without explanations, incomplete coverage areas across the entire documentation set

AI analysis is optional and controlled by:
- `ANTHROPIC_API_KEY` environment variable presence
- `--no-ai` CLI flag
- `analysis.enable_ai_analysis` config setting

## Report Formats

**JSON** (`doc_analysis_report.json`): Machine-readable, complete issue list, suitable for CI/CD integration
**HTML** (`doc_analysis_report.html`): Interactive, color-coded by severity, includes executive summary
**Markdown** (`doc_analysis_report.md`): GitHub-friendly, grouped by severity, suitable for issue tracking

## Extension Points

To add custom checks, extend `EnhancedDocumentationAnalyzer` and add methods:
```python
class CustomAnalyzer(EnhancedDocumentationAnalyzer):
    def check_custom_rule(self, content: str, file_path: str):
        # Add issues to self.report
        self.report.add_issue(Issue(...))
```

To add platform support, extend `RepositoryManager.detect_repo_type()` and add platform-specific validator.

## Test Architecture

Tests use pytest with fixtures for temporary documentation directories. Key test classes:
- `TestDocumentationAnalyzer`: Core functionality tests
- `TestInformationArchitecture`: IA-specific tests
- `TestConsistency`: Terminology consistency tests
- `TestAIIntegration`: AI-powered analysis (requires API key, marked with `@pytest.mark.skipif`)
- `TestPerformance`: Large file handling tests

## Dependencies

Core: `anthropic`, `pyyaml`
Repository: `GitPython` (for remote cloning)
Testing: `pytest`, `coverage`
Optional: `markdown`, `beautifulsoup4`, `textstat`, `jinja2`
