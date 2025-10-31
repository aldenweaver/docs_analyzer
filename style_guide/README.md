# Claude Documentation Style Guide & Standards

**Version**: 1.0
**Last Updated**: October 31, 2025
**Status**: Production-Ready
**Research Basis**: Analysis of 142 GitHub issues, 115 documentation files, 3,023 quality issues

---

## 📚 What's Inside

This style guide was created through systematic user research and documentation analysis. It's designed to be:
- **Actionable**: Clear rules you can apply immediately
- **Research-backed**: Based on 142 real user complaints
- **Automatable**: Rules can be validated programmatically
- **Team-friendly**: Usable by writers, engineers, and PMs

## 📖 Documentation Set

| Document | Audience | Use Case |
|----------|----------|----------|
| **[Core Style Guide](research_artifacts/Claude_Docs_Style_Guide.md)** | Everyone | Complete documentation standards |
| **[Quick Reference](research_artifacts/Claude_Docs_Quick_Reference.md)** | Everyone | 1-page cheat sheet for daily use |
| **[Mintlify Standards](research_artifacts/Mintlify_Technical_Implementation_Guide.md)** | Technical Writers | Platform-specific implementation |
| **[Template Library](research_artifacts/Claude_Docs_Template_Library.md)** | Everyone | 10 ready-to-use content templates |
| **[Programmatic Enforcement](research_artifacts/Programmatic_Enforcement_Specification.md)** | Engineers | Automated quality checks specification |
| **[Validation Rules](validation_rules.yaml)** | Engineers | Machine-readable validation rules |
| **[Research Report](research_artifacts/compass_artifact_wf-81775969-5c59-4fb2-8e4d-7b2620a2abff_text_markdown.md)** | Documentation Leaders | Comprehensive research and best practices analysis |

## 🎯 Quick Start

### For Technical Writers
1. Read [Core Style Guide](research_artifacts/Claude_Docs_Style_Guide.md)
2. Bookmark [Quick Reference](research_artifacts/Claude_Docs_Quick_Reference.md)
3. Use [Template Library](research_artifacts/Claude_Docs_Template_Library.md) for new pages
4. Check [Mintlify Standards](research_artifacts/Mintlify_Technical_Implementation_Guide.md) for MDX specifics

### For Engineers Contributing Docs
1. Read [Quick Reference](research_artifacts/Claude_Docs_Quick_Reference.md) (5 minutes)
2. Copy appropriate template from [Template Library](research_artifacts/Claude_Docs_Template_Library.md)
3. Fill in your content
4. Run validation tool before PR

### For Product Managers
1. Read [Quick Reference](research_artifacts/Claude_Docs_Quick_Reference.md)
2. Use Conceptual Template from [Template Library](research_artifacts/Claude_Docs_Template_Library.md) for feature docs
3. Focus on prerequisites and use cases

### For Documentation Leaders
1. Review [Research Report](research_artifacts/compass_artifact_wf-81775969-5c59-4fb2-8e4d-7b2620a2abff_text_markdown.md) for comprehensive analysis
2. See [Programmatic Enforcement Specification](research_artifacts/Programmatic_Enforcement_Specification.md) for automation strategy
3. Reference [validation_rules.yaml](validation_rules.yaml) for machine-readable rules

## 🔍 Research Foundation

This guide is based on systematic analysis of Claude documentation and user feedback:

### User Research (142 GitHub Issues)
- **72% complained about "missing" documentation**
- **90% of requested topics were actually documented** (findability problem)
- **13% complained about missing context** (prerequisites, examples)
- **4% found content unclear** (weak language, long paragraphs)

### Quality Analysis (3,023 Issues Found)
- **52% were missing documentation elements** (short pages, no examples, no prerequisites)
- **31% were clarity problems** (vague language, complex paragraphs)
- **12% were missing prerequisites**
- **5% were readability issues** (long paragraphs)

### Key Insight
> **The #1 problem isn't missing content - it's that users can't find existing content.**
>
> This style guide emphasizes findability through:
> - Consistent structure and naming
> - Clear prerequisites and related topics
> - Strategic cross-referencing
> - Descriptive titles and headings

## 🚀 Implementation

### Phase 1: Immediate Use
- Technical writers use style guide for new documentation
- Templates available for common doc types
- Quick reference for daily decisions

### Phase 2: Validation (Coming Soon)
```bash
# Run style guide validator on a file
python doc_analyzer.py --style-guide ./docs/api/authentication.mdx

# Output:
✓ Word count: 450 words (min: 100)
✓ Code examples: 2 found
✓ Prerequisites section: Present
✗ Related topics: Missing (add 3-5 related links)
✓ Heading hierarchy: Valid
```

### Phase 3: Automated Enforcement
- Pre-commit hooks check style guide compliance
- CI/CD pipeline validates new documentation
- Automatic suggestions for improvements

## 📊 Success Metrics

Track these to measure style guide adoption:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Style guide compliance | >90% | Automated validation pass rate |
| Average page word count | >150 words | Analyzer reports |
| Code examples | 100% of technical pages | Automated detection |
| Prerequisites sections | 100% of procedural docs | Pattern matching |
| Related topics | 80% of pages | Link analysis |
| User complaints about "missing" docs | <50% | GitHub issue categorization |

## 🤝 Contributing to This Guide

### How to Propose Changes
1. File an issue with proposed change and rationale
2. Include examples (good and bad)
3. Reference user feedback or pain points if available

### When to Update
- User research reveals new patterns
- New Mintlify features added
- Feedback from documentation team
- Quarterly review of GitHub issues

## 📈 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Oct 31, 2025 | Initial release based on 142 issue analysis |

## 💬 Questions?

- **For style guide questions**: Check [Core Style Guide](core_style_guide.md)
- **For quick answers**: Check [Quick Reference](quick_reference.md)
- **For Mintlify specifics**: Check [Mintlify Standards](mintlify_standards.md)
- **For examples**: Check [templates/](templates/)

---

**Note**: This style guide is a living document. It evolves based on user feedback, documentation analysis, and team needs. Your feedback is welcome!
