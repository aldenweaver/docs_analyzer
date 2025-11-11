# Sample Documentation for Testing

This directory contains sample MDX documentation files with **intentional quality issues** designed to demonstrate the analyzer's capabilities.

## Files

### quickstart.mdx
**Intentional Issues:**
- **Clarity**: Weak words (simply, really, easily, quickly, just, basically)
- **Style**: Passive voice throughout
- **Style**: Long, hard-to-parse sentences
- **UX**: Poor link text (generic "click here" style)
- **Mintlify**: Code block without language specification
- **Mintlify**: Short description lacking detail

### api-reference.mdx
**Intentional Issues:**
- **Mintlify**: Missing description in frontmatter (required field)
- **Consistency**: Inconsistent capitalization ("api reference" in title)
- **IA**: Broken heading hierarchy (##, ####, #####, ######)
- **Mintlify**: Code blocks without language tags
- **Consistency**: Inconsistent terminology and formatting
- **UX**: Absolute URL instead of relative path
- **UX**: Poor link text ("Click here")
- **Style**: Passive voice

### tutorial.mdx
**Intentional Issues:**
- **Mintlify**: Description too long (>160 chars, bad for SEO)
- **IA**: Severely broken heading hierarchy (skips levels, uses multiple H1s)
- **IA**: Vague section headings ("Feature 1", "Issue 1")
- **Mintlify**: Code blocks without language specification
- **UX**: Absolute URL to external docs
- **Gaps**: Vague, incomplete instructions

### concepts.mdx
**Intentional Issues:**
- **Consistency**: Highly inconsistent terminology (API Key/api keys/API-key/api key)
- **Consistency**: Inconsistent capitalization throughout
- **Consistency**: Inconsistent field naming conventions
- **Consistency**: Inconsistent error code formatting
- **Style**: Weak words (basically, simply)
- **Mintlify**: Code block without language tag
- **Mintlify**: Short description lacking detail

## Purpose

These files are used to:
1. Generate example analyzer reports (with AI and without AI)
2. Demonstrate the doc_fixer capabilities
3. Provide reproducible test cases
4. Show the variety of issues the tool catches

## Running the Analyzer

From the repository root:

```bash
# With AI analysis
python analyze_docs.py examples/sample_docs/ --format all

# Without AI analysis
python analyze_docs.py examples/sample_docs/ --format all --no-ai

# Run the fixer (preserves originals in sample_docs_fixed/)
python doc_fixer.py examples/sample_docs_fixed/
```

See `/examples/reports/` for the actual output generated from these sample files.
