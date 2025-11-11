# Documentation Quality Analyzer

> Automated quality analysis and fixing for .mdx documentation with comprehensive reporting in HTML, Markdown, and JSON formats.

## Overview

A unified CLI tool that analyzes Mintlify-based documentation (like Claude Docs) and generates both quality analysis reports and automated fix suggestions. Processes .mdx documentation files with optional AI-powered semantic analysis.

**Key Features:**
- Single command runs both analysis and fix generation
- Generates 6 comprehensive reports (3 formats × 2 report types)
- Optional Claude API integration for advanced analysis
- 20+ automated fixers for documentation improvements
- Platform auto-detection (Mintlify, Docusaurus, MkDocs, generic)

---

## Quick Start

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/aldenweaver/docs_analyzer
cd docs_analyzer

# 2. Run automated setup (creates venv + installs dependencies)
./setup.sh          # Linux/macOS
setup.bat           # Windows

# 3. Configure API key (optional - enables AI analysis)
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your-key-here
# IMPORTANT: Never commit .env to git (already in .gitignore)
```

### Basic Usage

```bash
# Activate virtual environment
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate.bat   # Windows

# Analyze your documentation (recommended: use --no-ai for speed)
python analyze_docs.py /path/to/docs --no-ai

# Or with AI analysis (slower, but more comprehensive)
python analyze_docs.py /path/to/docs
```

**That's it!** The tool will:
1. Analyze all .mdx files in the directory
2. Run 20+ automated quality checks
3. Generate fix suggestions
4. Save 6 reports in `reports/<timestamp>/`

> **Note**: Use `--no-ai` for documentation sets with 50+ files to avoid long processing times (30+ minutes). See [Performance Tips](#performance-tips) for details.

---

## Usage Guide

### Command Options

```bash
# Basic analysis (generates all 3 report formats by default)
python analyze_docs.py /path/to/docs

# Generate specific report format only
python analyze_docs.py /path/to/docs --format html      # HTML only
python analyze_docs.py /path/to/docs --format json      # JSON only
python analyze_docs.py /path/to/docs --format markdown  # Markdown only

# Run without AI (faster, no API key required)
python analyze_docs.py /path/to/docs --no-ai

# Apply fixes automatically (default is preview/dry-run)
python analyze_docs.py /path/to/docs --apply-fixes

# Use custom configuration
python analyze_docs.py /path/to/docs --config custom_config.yaml

# Analyze remote repository
python analyze_docs.py --repo-url https://github.com/user/docs --repo-type mintlify

# Skip analysis, only generate fixes
python analyze_docs.py /path/to/docs --skip-analysis

# Skip fixes, only run analysis
python analyze_docs.py /path/to/docs --skip-fixes
```

### Report Formats Explained

The `--format` flag controls which report file types are generated:

| Format | File Type | Use Case |
|--------|-----------|----------|
| `html` | `.html` | Interactive web report with filtering and color-coding - best for human review |
| `markdown` | `.md` | GitHub-friendly format - great for issues and PR comments |
| `json` | `.json` | Machine-readable data - perfect for CI/CD and custom tooling |
| `all` | All 3 | Maximum flexibility - **default and recommended** |

### Generated Reports

Each run creates a timestamped directory with up to 6 reports:

```
reports/2024-11-04_14-30-15/
├── doc_analysis_report.html    # Analysis: Interactive web view
├── doc_analysis_report.md      # Analysis: GitHub-friendly
├── doc_analysis_report.json    # Analysis: Raw data
├── doc_fix_report.html         # Fixes: Visual preview
├── doc_fix_report.md           # Fixes: List format
└── doc_fix_report.json         # Fixes: Structured data
```

**Analysis Reports** show issues found:
- Clarity problems, readability metrics
- Information architecture issues
- Consistency checks, style guide violations
- Content gaps, broken links

**Fix Reports** show suggested corrections:
- Frontmatter additions/corrections
- Code block language tag additions
- Terminology standardization
- Heading hierarchy fixes
- And 20+ other automated improvements

---

## Configuration

### Environment Variables

The repository includes a comprehensive `.env.example` file with all available configuration options. To configure the analyzer:

```bash
# 1. Copy the example file
cp .env.example .env

# 2. Edit .env and add your configuration
# Note: .env is gitignored and will never be committed
```

**Key Configuration Options:**

```bash
# AI-Powered Analysis (optional - analyzer works without API key)
ANTHROPIC_API_KEY=your-api-key-here
ENABLE_AI_ANALYSIS=true
CLAUDE_MODEL=claude-3-5-haiku-20241022  # Budget-friendly: ~$0.14 for 60 files
# Alternative models:
# - claude-sonnet-4-5-20250929 (recommended: ~$0.54 for 60 files)
# - claude-opus-4-20250514 (highest quality: ~$2.68 for 60 files)
AI_MAX_TOKENS=4000

# Output Settings
DEFAULT_OUTPUT_FORMAT=all  # Options: json, html, markdown, all
OUTPUT_DIR=./reports
DOCS_PATH=./docs

# Performance Settings
PARALLEL_THREADS=4
ENABLE_DUPLICATION_DETECTION=true
DUPLICATION_THRESHOLD=0.8

# Repository Settings
REPO_TYPE=auto  # Options: auto, mintlify, docusaurus, mkdocs, generic
ENABLE_REMOTE_CLONE=false
GITHUB_TOKEN=  # For private repositories (optional)
```

> **Important**: The `.env.example` file includes detailed comments and cost estimates for each Claude model. Review it for the complete list of options.

### Performance Impact

**Running Without AI (--no-ai flag):**

| Aspect | Impact |
|--------|--------|
| **Speed** | 95% faster - typical runs complete in 30-60 seconds |
| **API Costs** | $0 - no Claude API calls |
| **Coverage** | 95% of quality checks still run |
| **Reports** | All 6 reports generated (HTML, MD, JSON) |
| **Reliability** | No timeouts or rate limiting issues |

**Running With AI (default):**

| Aspect | Impact |
|--------|--------|
| **Speed** | Calls Claude API for every file - 30-60+ minutes for 100 files |
| **API Costs** | ~$0.01-0.05 per file analyzed (estimate) |
| **Coverage** | 100% including advanced semantic analysis |
| **Reports** | All 6 reports with AI insights |
| **Limitations** | May timeout on large doc sets (100+ files) |

### Recommended Usage

**Use `--no-ai` when:**
- Processing 50+ documentation files
- Running in CI/CD pipelines (speed critical)
- Regular automated quality checks
- You want results in under 1 minute
- API costs are a concern

**Use AI analysis when:**
- Small documentation sets (< 20 files)
- Deep semantic analysis needed
- Detecting subtle clarity issues
- One-time comprehensive audits
- You have 30+ minutes to wait

### What You Still Get With --no-ai

Even without AI, you get comprehensive quality analysis:

**All 20+ Automated Fixers:**
- Frontmatter validation and correction
- Code block language tag insertion
- Heading hierarchy fixes
- URL normalization
- Capitalization standardization
- Terminology consistency checks
- Accessibility improvements (WCAG 2.1 AA)
- Broken link detection

**Complete Quality Checks:**
- Readability metrics (sentence length, complexity)
- Passive voice detection
- Style guide compliance
- Information architecture validation
- Content consistency analysis
- Formatting standardization

**Full Reporting:**
- All 6 report formats (HTML, Markdown, JSON)
- Interactive web reports with filtering
- GitHub-friendly markdown reports
- Machine-readable JSON for automation

**Only Skipped:**
- AI-powered semantic clarity analysis
- Advanced context understanding
- Subtle jargon detection
- Nuanced writing style suggestions

**Bottom Line:** --no-ai provides 95% of value at 20x the speed.

### Custom Style Rules

Create `config.yaml` to customize analysis:

```yaml
style_rules:
  max_sentence_length: 30
  preferred_terms:
    utilize: use
    leverage: use
  avoid_terms:
    - simply
    - just

required_sections:
  - overview
  - prerequisites

mintlify:
  required_frontmatter:
    - title
    - description
```

---

## What Gets Analyzed

### Analysis Categories

1. **Clarity** - Readability metrics, passive voice, jargon detection, AI-powered clarity analysis
2. **Information Architecture** - Document structure, heading hierarchy, navigation patterns
3. **Consistency** - Terminology standardization, formatting uniformity, style patterns
4. **Style Guide** - Configurable rules, preferred terminology, weak language detection
5. **Content Gaps** - Missing topics, redundancy, incomplete user journeys
6. **User Experience** - Link quality, context sufficiency, accessibility

### Automated Fixers (20+)

- **Frontmatter validation** - Ensures proper MDX frontmatter
- **Code block formatting** - Adds missing language tags
- **URL normalization** - Fixes link formatting
- **Heading hierarchy** - Corrects structure issues
- **Terminology consistency** - Standardizes terms
- **Accessibility** - WCAG 2.1 AA compliance
- **Capitalization** - Standardizes title case
- **Link text improvement** - Makes links descriptive
- And many more...

---

## Testing

```bash
# Activate venv first
source venv/bin/activate

# Run all tests
pytest test_analyzer.py -v

# Run with coverage report
pytest test_analyzer.py -v --cov=doc_analyzer

# Run specific test class
pytest test_analyzer.py::TestDocumentationAnalyzer -v
```

---

## Docker Support

```bash
# Build and run with Docker Compose
docker-compose up

# Run tests in Docker
docker-compose --profile testing run test

# Interactive shell for development
docker-compose --profile dev run shell
```

---

## Performance Tips

### Recommended: Use --no-ai for Production

**For large documentation sets (50+ files), use `--no-ai` to avoid timeouts:**

```bash
python analyze_docs.py /path/to/docs --no-ai
```

**Why?**
- AI-powered analysis calls Claude API for **every file** analyzed and fixed
- For 80+ files, this can take **30-60+ minutes** and may timeout
- You still get all quality checks except AI semantic analysis
- **95% faster** execution time

**Typical Processing Times:**

| Files | Without AI | With AI |
|-------|-----------|---------|
| 10-20 files | 10-20 seconds | 2-5 minutes |
| 50-100 files | 30-60 seconds | 10-30 minutes |
| 100+ files | 1-2 minutes | 30-60+ minutes |

**When to use AI:**
- Small documentation sets (< 20 files)
- Deep semantic analysis needed
- You have time to wait
- Testing/experimentation

**When to skip AI (use --no-ai):**
- Production CI/CD pipelines
- Large documentation sets
- Quick quality checks
- Regular automated runs

### Future Performance Optimizations

Several optimization strategies have been identified to make the analyzer even faster. See [OPTIMIZATION_PLAN.md](OPTIMIZATION_PLAN.md) for full details.

**Planned Improvements:**

1. **Parallel Processing** (4-8x speedup)
   - Process multiple files simultaneously using CPU cores
   - Target: 100 files in ~10 seconds (vs current 45 seconds)

2. **Incremental Analysis** (10-100x speedup)
   - Only analyze changed files (git-aware)
   - Cache results based on file content hash
   - Target: PR analysis in 2-5 seconds

3. **Batch API Requests** (2-3x speedup for AI)
   - Send 10-20 files per API call instead of 1
   - Reduce network overhead
   - Target: 100 files with AI in ~8 minutes (vs current 30 minutes)

4. **Async I/O** (2-3x overall speedup)
   - Non-blocking file operations
   - Concurrent API requests
   - Better resource utilization

**Implementation Status:**
- Phase 0: --no-ai flag (completed)
- Phase 1: Parallel processing + caching (planned)
- Phase 2: Batch API + async (planned)
- Phase 3: ML-based optimization (planned)

**Performance Targets:**

| Optimization | Current | Target | Speedup |
|--------------|---------|--------|---------|
| No AI, 100 files | 45 sec | 5 sec | 9x |
| With AI, 100 files | 30 min | 3 min | 10x |
| Changed files only | N/A | 2-5 sec | 100x+ |

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Documentation Quality Check

on: [pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run Analysis (no AI for speed)
        run: python analyze_docs.py ./docs --format json --no-ai

      - name: Upload Reports
        uses: actions/upload-artifact@v2
        with:
          name: doc-reports
          path: reports/
```

---

## Advanced Usage

### Individual Components

While `analyze_docs.py` is recommended, you can run components separately:

```bash
# Run only analysis
python doc_analyzer.py /path/to/docs --format all

# Run only fixer
python doc_fixer.py /path/to/docs --dry-run
```

### API Server

Start the FastAPI backend for programmatic access:

```bash
cd api
uvicorn main:app --reload

# Access interactive docs at http://localhost:8000/docs
```

---

## Requirements

- **Python**: 3.8 or higher
- **Optional**: Anthropic API key for AI-powered analysis
- **Dependencies**: Auto-installed by `setup.sh`
  - anthropic, pyyaml, python-dotenv, GitPython
  - pytest, beautifulsoup4, textstat, jinja2

---

## Troubleshooting

### Common Issues

**"Command appears to hang"**
- The tool shows real-time output - if AI is enabled, it may take 5-10 minutes
- Use `--no-ai` for much faster execution
- Check your API key is valid in `.env`

**"No reports generated"**
- Check the `reports/` directory for timestamped folders
- Ensure you have write permissions
- Look for error messages in the output

**"JSON parsing errors"**
- These are warnings from AI analysis and don't stop execution
- The tool will skip problematic files and continue
- Reports will still be generated successfully

---

## Project Structure

```
docs_analyzer/
├── analyze_docs.py          # Unified CLI entry point (main command)
├── doc_analyzer.py          # Analysis engine
├── doc_fixer.py             # Fix orchestration
├── config.yaml              # Example configuration
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
├── setup.sh / setup.bat     # Automated setup scripts
├── core/                    # Data models and configuration
├── fixers/                  # 20+ fixer modules
├── api/                     # FastAPI backend
├── style_guide/             # Validation rules and templates
└── reports/                 # Generated reports (timestamped)
```

---

## Features

### Documentation Quality at Scale
Automated checks based on industry best practices for technical documentation, including readability analysis, style guide enforcement, and information architecture validation.

### Comprehensive Analysis
Analyzes multiple dimensions of documentation quality:
- Clarity and readability
- Information architecture and navigation
- Terminology consistency
- Style guide compliance
- Content completeness
- User experience and accessibility

### Intelligent Automation
20+ automated fixers handle common documentation issues, from frontmatter validation to heading hierarchy correction, reducing manual review time.

### Flexible Integration
Multiple output formats (HTML, Markdown, JSON) support different workflows, from human review to CI/CD automation. Works with or without AI analysis depending on speed and depth requirements.

---

## Additional Documentation

- **[CLAUDE.md](CLAUDE.md)** - Detailed architecture and development guide
- **[TESTING_HISTORY.md](TESTING_HISTORY.md)** - Real-world testing results and tool evolution
- **[examples/reports/](examples/reports/)** - Sample analysis reports from production documentation
- **[config.yaml](config.yaml)** - Full configuration options with examples
- **[.env.example](.env.example)** - All environment variables explained

---

## Real-World Results

Validated on production documentation (287 MDX files):
- **73,977 issues identified** across 6 categories
- **60 second runtime** (4.8 files/second with --no-ai)
- **8,713 critical issues** caught (missing frontmatter, broken links)
- **0 broken links** in automated fixes (URL protection validated)

See [TESTING_HISTORY.md](TESTING_HISTORY.md) for detailed metrics and [examples/reports/](examples/reports/) for sample output.

---

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
