# 🚀 Quick Reference Card

## Installation (One-Time Setup)

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY='your-key-here'
```

## Basic Commands

```bash
# Simple analysis
python doc_analyzer.py ./docs

# With config
python doc_analyzer.py --config config.yaml

# All formats
python doc_analyzer.py ./docs --format all

# No AI (faster)
python doc_analyzer.py ./docs --no-ai

# Remote repo
python doc_analyzer.py --repo-url https://github.com/user/repo
```

## Files You Need

| File | Purpose |
|------|---------|
| `doc_analyzer.py` | The analyzer |
| `config.yaml` | Configuration |
| `requirements.txt` | Dependencies |
| `USAGE_GUIDE.md` | Full documentation |
| `RESEARCH_FINDINGS.md` | Background info |

## Issue Severities

- **Critical**: Fix immediately (broken links, missing frontmatter)
- **High**: Fix this week (gaps, inconsistencies)
- **Medium**: Next sprint (style, structure)
- **Low**: Nice to have (preferences, optimizations)

## Key Features

✅ MDX frontmatter validation
✅ Mintlify-specific checks
✅ AI semantic analysis
✅ Content duplication detection
✅ User journey validation
✅ Cross-reference checking
✅ Platform auto-detection

## Common Issues

**No API key**: `export ANTHROPIC_API_KEY='...'`
**Import error**: `pip install -r requirements.txt`
**Type not detected**: `--repo-type mintlify`

## Report Formats

- **HTML**: Interactive dashboard (recommended)
- **JSON**: CI/CD integration
- **Markdown**: GitHub tracking

## Success Checklist

- [ ] Clone 8-12 Claude Docs pages
- [ ] Run analyzer
- [ ] Fix all critical issues
- [ ] Fix 80% of high issues
- [ ] Document improvements
- [ ] Take screenshots
- [ ] Create case study
- [ ] Apply!

## Quick Test

```bash
mkdir test-docs
echo '# Test\nSimply check this.' > test-docs/test.md
python doc_analyzer.py ./test-docs
```

Should find: weak language ("simply")

## Links

- [Full Usage Guide](./USAGE_GUIDE.md)
- [Research Findings](./RESEARCH_FINDINGS.md)
- [Implementation Summary](./IMPLEMENTATION_SUMMARY.md)

## One-Liner

```bash
pip install -r requirements.txt && export ANTHROPIC_API_KEY='...' && python doc_analyzer.py ./docs --format html && open doc_analysis_report.html
```

---

**Remember**: This tool demonstrates ALL key job responsibilities!
