# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **documentation quality analyzer** designed for Mintlify-based documentation (like Claude Docs). It's a proof-of-concept that demonstrates technical documentation polish and information architecture skills. The analyzer performs automated quality checks on documentation and generates reports in multiple formats (JSON, HTML, Markdown).

**Core Purpose:** Automate key technical writing responsibilities including clarity checks, information architecture validation, style guide compliance, consistency analysis, and content gap detection.

## 🎯 Code Quality Principles

### Naming Conventions: No Version Suffixes

**CRITICAL PRINCIPLE**: Never accumulate deprecated code with version suffixes like "Enhanced", "New", "V2", "Improved", "Better", "Updated", etc.

**Wrong Approach:**
```python
class DocumentationAnalyzer:
    # Old version
    pass

class EnhancedDocumentationAnalyzer:
    # Better version - but now we have two classes!
    pass

class SuperEnhancedDocumentationAnalyzerV3:
    # Even better - but name is getting ridiculous!
    pass
```

**Correct Approach:**
```python
class DocumentationAnalyzer:
    # Just replace the old code with the better code
    # Keep the same name - Git tracks the evolution!
    pass
```

**Rationale:**
- Prevents accumulation of deprecated files and classes
- Avoids increasingly verbose names (EnhancedSuperImprovedAnalyzerV4Final)
- Makes it clear what the "current" version is
- Simplifies imports and documentation
- Git history naturally tracks the evolution

**How to Handle Improvements:**
1. **Replace** the old code with the new code in the same file
2. **Keep** the same class/function/file name
3. **Update** the docstring to reflect new capabilities
4. **Remove** any "Enhanced", "V2", etc. from names
5. **Commit** with a clear message about what improved

**Exception:** Only use version suffixes for:
- Genuine API versions that must coexist (e.g., `APIv1`, `APIv2` where both are actively maintained for backward compatibility)
- Migration periods where both old and new must temporarily coexist (document deprecation timeline clearly)

## Key Commands

### Setup

**Docker (Recommended):**
```bash
# Build and run with Docker Compose
docker-compose up

# Run tests in Docker
docker-compose --profile testing run test

# Interactive shell
docker-compose --profile dev run shell
```

**Local with Virtual Environment:**
```bash
# Automated setup (creates venv, installs deps)
./setup.sh          # Linux/macOS
setup.bat           # Windows

# Manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Environment Configuration:**
```bash
# Copy example environment file
cp .env.example .env

# Edit .env and configure:
# - ANTHROPIC_API_KEY (optional - for AI analysis)
# - ENABLE_AI_ANALYSIS=true/false
# - CLAUDE_MODEL (default: claude-sonnet-4-5-20250929)
# - AI_MAX_TOKENS (default: 2000)
```

### Running the Analyzer

```bash
# Using convenience script (auto-activates venv)
./run.sh /path/to/docs

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

# Disable AI analysis (faster, works without API key)
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

**DocumentationAnalyzer** (`doc_analyzer.py:581-1269`)
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
2. `DocumentationAnalyzer` runs three phases:
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

To add custom checks, extend `DocumentationAnalyzer` and add methods:
```python
class CustomAnalyzer(DocumentationAnalyzer):
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

Core: `anthropic`, `pyyaml`, `python-dotenv`
Repository: `GitPython` (for remote cloning)
Testing: `pytest`, `coverage`
Optional: `markdown`, `beautifulsoup4`, `textstat`, `jinja2`

## Infrastructure & Security

### Containerization

The project is fully containerized for easy deployment:

**Dockerfile**: Multi-stage build with non-root user (UID 1000) for security. Includes all dependencies and runs as `analyzer` user.

**docker-compose.yml**: Provides three service profiles:
- `analyzer` (default): Runs analysis on mounted docs
- `test`: Runs test suite
- `shell`: Interactive development shell

**Volumes**:
- `./docs_input:/app/docs_input:ro` - Mount documentation (read-only)
- `./reports:/app/reports` - Output reports
- `./config.yaml:/app/config.yaml:ro` - Custom configuration

### Environment Variables & Security

**Security Best Practices:**
1. API keys stored in `.env` (gitignored, never committed)
2. `.env.example` provides template without secrets
3. Environment variables override config file settings
4. Analyzer works without API key (graceful degradation)

**Key Environment Variables:**
- `ANTHROPIC_API_KEY`: Claude API key (optional)
- `ENABLE_AI_ANALYSIS`: Enable/disable AI features (default: true)
- `CLAUDE_MODEL`: Model selection (default: claude-sonnet-4-5-20250929)
- `AI_MAX_TOKENS`: Token limit per request (default: 2000)

**Loading Order:**
1. `.env` file loaded via `python-dotenv` at startup
2. Environment variables override config.yaml values
3. CLI flags override environment variables

### Virtual Environment Management

**Setup Scripts:**
- `setup.sh` / `setup.bat`: Automated venv creation and dependency installation
- `run.sh`: Convenience wrapper that activates venv and runs analyzer

**Manual venv:**
```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
pip install -r requirements.txt
```

### Running Without API Key

The analyzer is designed to run in two modes:

**Full Mode (with API key):**
- All quality checks
- AI-powered clarity analysis
- Semantic gap detection
- User journey validation

**Basic Mode (without API key):**
- All quality checks except AI-powered analysis
- Readability metrics
- Style guide compliance
- Information architecture validation
- Consistency checks
- Content duplication detection

Set `ENABLE_AI_ANALYSIS=false` or omit `ANTHROPIC_API_KEY` to run in basic mode.
