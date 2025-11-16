# Inkeep Preparation Guide

This guide explains how to use the documentation analyzer's new Inkeep-ready features to prepare your documentation for AI-powered search systems like Inkeep.

## What is Inkeep?

Inkeep is an AI agent platform that enables intelligent AI assistants across documentation, support, and operational workflows. It provides:
- AI-powered search with RAG (Retrieval-Augmented Generation)
- Conversational interfaces grounded in your documentation
- Automatic content gap detection based on user queries
- Multi-source ingestion from GitHub, Confluence, Notion, and more

## Why Prepare Documentation for Inkeep?

Well-structured, AI-optimized documentation enables Inkeep to:
- Provide more accurate answers with proper citations
- Understand content context when chunked for vector search
- Navigate documentation relationships effectively
- Extract metadata for better categorization and discovery

## New Features for Inkeep Readiness

### 1. AI Searchability Analysis

The analyzer now checks for:
- **Semantic Chunking Readiness**: Ensures sections are self-contained
- **Citation Readiness**: Validates unique, descriptive headings
- **Standalone Comprehension**: Checks that sections can be understood independently
- **Question-Answer Opportunities**: Identifies content that could be Q&A formatted

### 2. Metadata Enrichment Validation

Validates and suggests improvements for:
- Rich frontmatter with title, description, and keywords
- Content type classification (guide, tutorial, reference, concept)
- Audience level specification
- Related topics and prerequisites

### 3. Automated Fixers

Three new fixers help prepare documentation:
- **Heading Descriptiveness Fixer**: Replaces generic headings with descriptive ones
- **Context Enrichment Fixer**: Adds context to orphaned references
- **Metadata Enrichment Fixer**: Enhances frontmatter with keywords and metadata

## Usage

### Running Inkeep Readiness Analysis

```bash
# Analyze documentation and generate Inkeep readiness report
python doc_analyzer.py /path/to/docs --format inkeep

# Run without AI for faster analysis
python doc_analyzer.py /path/to/docs --format inkeep --no-ai

# Generate all report formats including Inkeep
python doc_analyzer.py /path/to/docs --format all
```

### Understanding the Inkeep Readiness Report

The report provides:
- **Overall Score** (0-100): Combined readiness score
- **Readiness Level**: ready, nearly_ready, needs_work, or not_ready
- **Category Scores**:
  - AI Searchability
  - Metadata Richness
  - Citation Readiness
  - Content Structure
- **Critical Blockers**: Issues that must be fixed
- **File Analysis**: Per-file scores and top issues
- **Recommendations**: Specific actions to improve readiness

### Applying Automated Fixes

```bash
# Preview fixes (dry run)
python doc_fixer.py /path/to/docs --dry-run

# Apply fixes with AI searchability fixers enabled (default)
python doc_fixer.py /path/to/docs

# Disable specific fixers if needed
export ENABLE_HEADING_DESCRIPTIVENESS_FIXER=false
export ENABLE_CONTEXT_ENRICHMENT_FIXER=false
export ENABLE_METADATA_ENRICHMENT_FIXER=false
python doc_fixer.py /path/to/docs
```

## Configuration

Add these settings to your `config.yaml`:

```yaml
# AI Search & RAG Optimization
ai_search_optimization:
  enabled: true

  semantic_chunking:
    enabled: true
    require_topic_sentences: true
    check_standalone_comprehension: true
    require_descriptive_headings: true

  citation_readiness:
    enabled: true
    require_unique_headings: true

  metadata:
    require_keywords: false
    min_description_length: 50
    max_description_length: 160

# Inkeep Integration
inkeep_integration:
  enabled: true
  readiness_thresholds:
    minimum_overall_score: 70
    critical_issues_allowed: 0
```

## Best Practices for Inkeep-Ready Documentation

### 1. Use Descriptive Headings

**Bad:**
```markdown
## Overview
## Details
## Example
```

**Good:**
```markdown
## How Claude API Authentication Works
## API Rate Limits and Quotas
## Example: Send Your First API Request
```

### 2. Provide Context for References

**Bad:**
```markdown
As mentioned above, the API requires authentication.
This method works similarly to the previous one.
```

**Good:**
```markdown
As described in the Authentication section, the API requires authentication.
This method works similarly to the GET request method described earlier.
```

### 3. Add Rich Metadata

**Bad:**
```yaml
---
title: API Documentation
---
```

**Good:**
```yaml
---
title: API Documentation
description: Complete guide to using the Claude API including authentication, endpoints, and examples
keywords: [claude, api, authentication, endpoints, rest, sdk]
content_type: reference
audience_level: intermediate
---
```

### 4. Make Sections Self-Contained

Each section should be understandable without reading other sections:
- Define technical terms on first use in each major section
- Provide context for code examples
- Use descriptive link text that explains the destination

### 5. Consider Question Format for Troubleshooting

**Bad:**
```markdown
## Troubleshooting
Authentication errors can occur when...
```

**Good:**
```markdown
## Troubleshooting

### What if I get an authentication error?
Authentication errors typically occur when...

### How do I handle rate limiting?
When you exceed the rate limit...
```

## Interpreting Scores

- **85-100**: Documentation is ready for Inkeep integration
- **70-84**: Nearly ready, minor improvements needed
- **50-69**: Needs work before optimal Inkeep performance
- **Below 50**: Significant restructuring recommended

## Common Issues and Solutions

| Issue | Impact | Solution |
|-------|--------|----------|
| Non-descriptive headings | Poor citation accuracy | Use HeadingDescriptivenessFixer or manually update |
| Orphaned references | Content not understandable when chunked | Use ContextEnrichmentFixer or add explicit references |
| Missing metadata | Poor discoverability | Use MetadataEnrichmentFixer or add frontmatter |
| Undefined pronouns | Confusing for AI | Replace with specific nouns |
| Code without context | Unclear purpose | Add explanatory text before code blocks |

## Integration with CI/CD

```bash
# Add to CI pipeline to ensure Inkeep readiness
python doc_analyzer.py docs --format inkeep --no-ai

# Fail build if score is too low
score=$(python doc_analyzer.py docs --format json | jq '.inkeep_readiness.overall_score')
if (( $(echo "$score < 70" | bc -l) )); then
  echo "Documentation not Inkeep-ready (score: $score)"
  exit 1
fi
```

## Next Steps

1. Run the analyzer with `--format inkeep` on your documentation
2. Review the readiness report and critical blockers
3. Apply automated fixes with `doc_fixer.py`
4. Manually address issues that can't be auto-fixed
5. Re-run analysis to verify improvements
6. Integrate with Inkeep once score is above 70

## Resources

- [Inkeep Documentation](https://inkeep.com/docs)
- [Documentation Analyzer README](README.md)
- [Configuration Guide](config.yaml)