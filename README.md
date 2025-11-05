# Documentation Quality Analyzer

> **Automated quality analysis and fixing for .mdx documentation with comprehensive reporting in HTML, Markdown, and JSON formats.**

## 🎯 Overview

A unified CLI tool that analyzes Mintlify-based documentation (like Claude Docs) and generates both quality analysis reports and automated fix suggestions. Processes .mdx documentation files with optional AI-powered semantic analysis.

**Key Features:**
- ✨ Single command runs both analysis and fix generation
- 📊 Generates 6 comprehensive reports (3 formats × 2 report types)
- 🤖 Optional Claude API integration for advanced analysis
- 🔧 20+ automated fixers for documentation improvements
- 🎨 Platform auto-detection (Mintlify, Docusaurus, MkDocs, generic)

---

## 🚀 Quick Start

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd docs_analyzer

# 2. Run automated setup (creates venv + installs dependencies)
./setup.sh          # Linux/macOS
setup.bat           # Windows

# 3. Configure API key (optional - enables AI analysis)
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your-key-here
```

### Basic Usage

```bash
# Activate virtual environment
source venv/bin/activate    # Linux/macOS
venv\Scripts\activate.bat   # Windows

# Analyze your documentation (generates all 6 reports)
python analyze_docs.py /path/to/docs
```

**That's it!** The tool will:
1. ✅ Analyze all .mdx files in the directory
2. ✅ Run 20+ automated quality checks
3. ✅ Generate fix suggestions
4. ✅ Save 6 reports in `reports/<timestamp>/`

---

## 📖 Usage Guide

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
| `html` | `.html` | 🌐 Interactive web report with filtering and color-coding - best for human review |
| `markdown` | `.md` | 📝 GitHub-friendly format - great for issues and PR comments |
| `json` | `.json` | 🔧 Machine-readable data - perfect for CI/CD and custom tooling |
| `all` | All 3 | 💎 Maximum flexibility - **default and recommended** |

### Generated Reports

Each run creates a timestamped directory with up to 6 reports:

```
reports/2024-11-04_14-30-15/
├── doc_analysis_report.html    # Analysis: Interactive web view
├── doc_analysis_report.md      # Analysis: GitHub-friendly
├── doc_analysis_report.json    # Analysis: Raw data
├── doc_fixes_report.html       # Fixes: Visual preview
├── doc_fixes_report.md         # Fixes: List format
└── doc_fixes_report.json       # Fixes: Structured data
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

## ⚙️ Configuration

### Environment Variables

Create a `.env` file for optional settings:

```bash
# AI-Powered Analysis (optional)
ANTHROPIC_API_KEY=your-api-key-here
ENABLE_AI_ANALYSIS=true
CLAUDE_MODEL=claude-3-5-haiku-20241022
AI_MAX_TOKENS=4000

# Output Settings
DEFAULT_OUTPUT_FORMAT=all
DOCS_PATH=./docs
```

**Running Without AI:**
- Omit `ANTHROPIC_API_KEY` or use `--no-ai` flag
- All quality checks still run except AI semantic analysis
- Significantly faster execution (30-60 seconds vs 5-10 minutes)

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

## 🔍 What Gets Analyzed

### Analysis Categories

1. **Clarity** - Readability metrics, passive voice, jargon detection, AI-powered clarity analysis
2. **Information Architecture** - Document structure, heading hierarchy, navigation patterns
3. **Consistency** - Terminology standardization, formatting uniformity, style patterns
4. **Style Guide** - Configurable rules, preferred terminology, weak language detection
5. **Content Gaps** - Missing topics, redundancy, incomplete user journeys
6. **User Experience** - Link quality, context sufficiency, accessibility

### Automated Fixers (20+)

- ✅ **Frontmatter validation** - Ensures proper MDX frontmatter
- ✅ **Code block formatting** - Adds missing language tags
- ✅ **URL normalization** - Fixes link formatting
- ✅ **Heading hierarchy** - Corrects structure issues
- ✅ **Terminology consistency** - Standardizes terms
- ✅ **Accessibility** - WCAG 2.1 AA compliance
- ✅ **Capitalization** - Standardizes title case
- ✅ **Link text improvement** - Makes links descriptive
- And many more...

---

## 🧪 Testing

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

## 🐳 Docker Support

```bash
# Build and run with Docker Compose
docker-compose up

# Run tests in Docker
docker-compose --profile testing run test

# Interactive shell for development
docker-compose --profile dev run shell
```

---

## 💡 Performance Tips

**For Faster Analysis:**
- Use `--no-ai` to skip AI-powered checks (reduces time by 80-90%)
- Use `--format json` if you only need machine-readable output
- Process smaller documentation sets at a time
- Disable optional fixers via environment variables

**Typical Processing Times:**
- **Without AI**: 30-60 seconds for 50-100 files
- **With AI**: 5-10 minutes for 50-100 files (depends on API response time)

---

## 🔧 CI/CD Integration

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

## 🛠️ Advanced Usage

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

## 📋 Requirements

- **Python**: 3.8 or higher
- **Optional**: Anthropic API key for AI-powered analysis
- **Dependencies**: Auto-installed by `setup.sh`
  - anthropic, pyyaml, python-dotenv, GitPython
  - pytest, beautifulsoup4, textstat, jinja2

---

## ❓ Troubleshooting

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

## 📁 Project Structure

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

## 🏆 Key Capabilities

This analyzer demonstrates:
- **Documentation Quality at Scale** - Automated checks based on industry best practices
- **Technical Proficiency** - Python, API integration, multiple output formats
- **Information Architecture** - Systematic IA analysis and validation
- **Style Guide Automation** - Configurable rules with intelligent enforcement
- **User-Centered Design** - Actionable recommendations prioritized by impact

---

## 📚 Additional Documentation

- **[CLAUDE.md](CLAUDE.md)** - Detailed architecture and development guide
- **[config.yaml](config.yaml)** - Full configuration options with examples
- **[.env.example](.env.example)** - All environment variables explained

---

**Built for technical writers who want to automate documentation quality checks and focus on high-value content improvements.**
