# Example Reports

This directory contains sample reports from real-world documentation analysis runs.

## Reports Included

### `baseline_no_ai/`
Results from analyzing 287 MDX files in 60 seconds using no-AI mode.

**Configuration**:
```bash
python analyze_docs.py /path/to/docs --no-ai --format all
```

**Highlights**:
- **73,977 issues found** across 6 categories
- **~60 second runtime** (4.8 files/second)
- **$0 cost** (no AI API calls)
- **8,713 critical issues** (missing frontmatter, code language tags)
- **11,340 medium issues** (heading hierarchy, passive voice)
- **53,924 low priority issues** (line length, style preferences)

**Files**:
- `doc_analysis_report.html` - Interactive web report with filtering and search
- `doc_analysis_report.md` - GitHub-friendly Markdown format

### `targeted_ai/` (Coming Soon)
Results from strategic AI analysis on 65 high-value documentation files.

**Purpose**: Demonstrates practical AI usage - targeted analysis on key sections rather than expensive analysis of all files.

## Report Formats

### HTML Report (`doc_analysis_report.html`)
**Best for**: Human review, sharing with teams

**Features**:
- Color-coded by severity (critical, medium, low)
- Interactive filtering and search
- Organized by file and category
- Executive summary at top
- Can be opened directly in browser

### Markdown Report (`doc_analysis_report.md`)
**Best for**: GitHub integration, issue tracking

**Features**:
- GitHub-friendly formatting
- Grouped by severity
- Easy to paste into GitHub issues
- Command-line friendly
- Version control friendly

### JSON Report (not included - too large)
**Best for**: CI/CD integration, automation, custom processing

**Note**: JSON reports can be 30-40 MB for large documentation sets. They're perfect for programmatic access but too large for git repositories. These reports are generated fresh on each run.

## How to Generate Your Own

### Quick Start
```bash
# Analyze your docs (no AI, fast)
python analyze_docs.py /path/to/your/docs --no-ai --format all

# With AI analysis (slower, more insights)
python analyze_docs.py /path/to/your/docs --format all

# Analyze specific section with AI
python analyze_docs.py /path/to/your/docs/section --format all
```

### Output Location
Reports are automatically saved to timestamped directories in `reports/`:
```
reports/
  2025-11-05_14-30-15/
    doc_analysis_report.json
    doc_analysis_report.html
    doc_analysis_report.md
```

## Understanding the Results

### Severity Levels
- **Critical**: Must fix (broken links, missing required frontmatter, missing code language tags)
- **Medium**: Should fix (heading hierarchy, passive voice, accessibility)
- **Low**: Consider fixing (line length, style preferences, weak language)

### Category Breakdown
- **Clarity**: Readability metrics, sentence complexity, weak language
- **Information Architecture**: Heading hierarchy, category organization, nesting depth
- **Consistency**: Terminology variations, formatting inconsistencies
- **Style**: Style guide compliance, passive voice, preferred terminology
- **Content Gaps**: Missing documentation types, incomplete user journeys, duplication
- **User Experience**: Link quality, accessibility, SEO optimization

## Real-World Context

These sample reports come from analyzing a comprehensive documentation clone (287 MDX files, Mintlify platform). The analysis demonstrates:

✅ **Scale**: Tool handles hundreds of files reliably
✅ **Speed**: 60 seconds for complete analysis
✅ **Value**: Identifies thousands of actionable issues
✅ **Practicality**: Reports are readable and actionable
✅ **Cost-effectiveness**: $0 for no-AI mode, practical costs for AI mode

For detailed testing history and methodology, see [TESTING_HISTORY.md](../../TESTING_HISTORY.md).

---

**Last Updated**: November 5, 2025
