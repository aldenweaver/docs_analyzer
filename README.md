# Documentation Quality Analyzer MVP

> **A comprehensive documentation quality analyzer and fixer for .mdx files that generates detailed reports in multiple formats (HTML, Markdown, JSON).**

## 🎯 Project Overview

This MVP provides a unified command-line tool that analyzes Mintlify-based documentation (like Claude Docs) and generates both quality analysis reports and fix suggestions. It processes .mdx documentation files and provides actionable insights for improvement.

### Key Features

- **Single Command Operation**: One simple CLI command runs both analysis and fix generation
- **Multiple Report Formats**: Generates 6 comprehensive reports (analysis + fixes in HTML, MD, JSON)
- **AI-Powered Analysis**: Optional Claude API integration for semantic analysis
- **20+ Automated Fixers**: Modular system for documentation improvements
- **Platform Auto-Detection**: Works with Mintlify, Docusaurus, MkDocs, or generic documentation

## 🚀 Quick Start

### Simple Setup & Run

```bash
# 1. Clone the repository
git clone <repository-url>
cd docs_analyzer

# 2. Run setup script (creates venv and installs dependencies)
./setup.sh          # Linux/macOS
setup.bat           # Windows

# 3. Configure environment (optional for AI features)
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY (optional)

# 4. Run the unified analyzer (single command for everything!)
python analyze_docs.py /path/to/docs --format all
```

**That's it!** This single command will:
- Analyze all .mdx files in your documentation
- Generate analysis reports (HTML, Markdown, JSON)
- Generate fix suggestion reports (HTML, Markdown, JSON)
- Save all 6 reports in a timestamped directory under `/reports/`

## 📖 Usage Examples

### Basic Usage

```bash
# Analyze docs and generate all report formats (recommended)
python analyze_docs.py /path/to/docs --format all

# Analyze with specific configuration
python analyze_docs.py /path/to/docs --config custom_config.yaml

# Analyze without AI features (faster, no API key needed)
python analyze_docs.py /path/to/docs --no-ai

# Apply fixes instead of just previewing
python analyze_docs.py /path/to/docs --apply-fixes

# Analyze remote repository
python analyze_docs.py --repo-url https://github.com/user/docs --repo-type mintlify
```

### Advanced Usage (Individual Scripts)

While the unified `analyze_docs.py` is recommended, you can also run components individually:

```bash
# Run only analysis
python doc_analyzer.py /path/to/docs --format all

# Run only fixer
python doc_fixer.py /path/to/docs --format all
```

## 📊 Generated Reports

Running `python analyze_docs.py /path/to/docs --format all` generates:

### Analysis Reports
1. **doc_analysis_report.html** - Interactive HTML with filtering and color-coding
2. **doc_analysis_report.md** - GitHub-friendly Markdown format
3. **doc_analysis_report.json** - Machine-readable for CI/CD integration

### Fix Suggestion Reports
1. **doc_fixes_report.html** - Visual fix preview with before/after comparisons
2. **doc_fixes_report.md** - Markdown format for review and tracking
3. **doc_fixes_report.json** - Structured fix data for automation

All reports are saved in timestamped directories:
```
reports/
  2024-10-27_14-30-15/
    doc_analysis_report.html
    doc_analysis_report.md
    doc_analysis_report.json
    doc_fixes_report.html
    doc_fixes_report.md
    doc_fixes_report.json
```

## 🔍 What Gets Analyzed

### Analysis Categories

1. **✍️ Clarity**
   - Readability metrics (sentence length, complexity)
   - Passive voice detection
   - Jargon and undefined terminology
   - AI-powered clarity analysis (optional)

2. **🏗️ Information Architecture**
   - Document structure and heading hierarchy
   - Navigation and findability
   - Category balance and organization
   - Orphan content detection

3. **🎨 Consistency**
   - Terminology standardization
   - Formatting consistency
   - Style patterns across files
   - Voice and tone uniformity

4. **📋 Style Guide Compliance**
   - Configurable style rules
   - Preferred terminology enforcement
   - Weak language detection
   - Code block formatting standards

5. **📚 Content Gaps**
   - Missing topics and sections
   - Redundancy detection
   - Required section validation
   - Cross-file topic mapping

6. **📊 User Experience**
   - Link quality assessment
   - Context sufficiency
   - Example and prerequisite validation
   - Accessibility considerations

### Available Fixers (20+ Modules)

The fixer system includes:
- **Frontmatter validation** - Ensures proper MDX frontmatter
- **Terminology consistency** - Standardizes terms across docs
- **URL normalization** - Fixes link formatting
- **Code block formatting** - Adds missing language tags
- **Accessibility improvements** - WCAG 2.1 AA compliance
- **Heading hierarchy** - Fixes structure issues
- **Capitalization** - Standardizes title case
- **Passive voice conversion** - Improves readability
- **Long sentence splitting** - Enhances clarity
- **Link text improvement** - Makes links descriptive
- **Broken link detection** - Identifies dead links
- And many more...

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Optional - for AI-powered analysis
ANTHROPIC_API_KEY=your-api-key-here
ENABLE_AI_ANALYSIS=true
CLAUDE_MODEL=claude-3-5-haiku-20241022
AI_MAX_TOKENS=4000

# Other settings
DOCS_PATH=./docs
DEFAULT_OUTPUT_FORMAT=all
```

### Custom Configuration (config.yaml)

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

mintlify:
  required_frontmatter:
    - title
    - description
```

## 🚀 Docker Support

For containerized deployment:

```bash
# Build and run with Docker Compose
docker-compose up

# Run tests in Docker
docker-compose --profile testing run test

# Interactive shell
docker-compose --profile dev run shell
```

## 🧪 Testing

```bash
# Run all tests
pytest test_analyzer.py -v

# Run with coverage
pytest test_analyzer.py -v --cov=doc_analyzer

# Run specific test class
pytest test_analyzer.py::TestDocumentationAnalyzer -v
```

## 📋 Requirements

- Python 3.8+
- Optional: ANTHROPIC_API_KEY for AI features
- Dependencies (auto-installed by setup.sh):
  - anthropic
  - pyyaml
  - python-dotenv
  - GitPython
  - pytest
  - beautifulsoup4
  - textstat
  - jinja2

## 🏃 Running Without AI

The analyzer works perfectly without an API key:

```bash
# Disable AI features
python analyze_docs.py /path/to/docs --no-ai

# Or set in .env
ENABLE_AI_ANALYSIS=false
```

Without AI, you still get:
- All quality checks and metrics
- All 20+ fixer modules
- Complete report generation
- Full consistency and style analysis

## 🔧 CI/CD Integration

```yaml
# .github/workflows/docs-quality.yml
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
      - name: Run Documentation Analysis
        run: python analyze_docs.py ./docs --format json --no-ai
      - name: Upload reports
        uses: actions/upload-artifact@v2
        with:
          name: doc-reports
          path: reports/
```

## 🎓 Technical Implementation

### Architecture

- **doc_analyzer.py** - Main analysis engine
- **doc_fixer.py** - Fix orchestration system
- **analyze_docs.py** - Unified CLI entry point
- **/core/** - Shared data models and configuration
- **/fixers/** - Modular fixer implementations (20+ modules)
- **/api/** - FastAPI backend for programmatic access

### Key Components

1. **RepositoryManager** - Platform detection and file management
2. **MDXParser** - MDX/Markdown parsing with frontmatter support
3. **MintlifyValidator** - Platform-specific validation
4. **SemanticAnalyzer** - AI-powered content analysis
5. **DocumentationAnalyzer** - Main orchestration
6. **FixerOrchestrator** - Manages fix generation

## 📈 Metrics Tracked

- Total issues by severity (critical, high, medium, low)
- Issues by category (clarity, IA, consistency, style, gaps, UX)
- Files analyzed and modified
- Fix suggestions by type
- Processing time and performance metrics

## 🤝 API Access

The project includes a FastAPI backend for programmatic access:

```bash
# Start API server
cd api
uvicorn main:app --reload

# Access at http://localhost:8000/docs
```

## 📝 Project Documentation

- **CLAUDE.md** - Detailed project instructions and architecture
- **README.md** - This file
- **config.yaml** - Example configuration with best practices
- **.env.example** - Environment variable template

## 🏆 Why This Project Matters

This analyzer demonstrates:
1. **Deep understanding of documentation quality** at scale
2. **Technical proficiency** in Python and API integration
3. **Information Architecture expertise** with systematic analysis
4. **Style guide knowledge** with configurable rules
5. **User-centered thinking** with actionable recommendations
6. **Automation mindset** for documentation workflows

---

**Note:** This is an MVP focused on backend analysis and fix generation for .mdx documentation files. The unified CLI provides a simple, powerful interface for comprehensive documentation quality improvement.