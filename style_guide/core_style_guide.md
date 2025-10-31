# Claude Documentation Style Guide

**Version**: 1.0
**Last Updated**: October 31, 2025
**Research Basis**: Analysis of 142 GitHub issues, 115 documentation files, 3,023 quality issues

---

## Executive Summary

This style guide is based on systematic analysis of 142 user-reported GitHub issues and comprehensive quality analysis of Claude's documentation. The key finding that shapes this entire guide:

> **90% of "missing" documentation complaints aren't about missing content - they're about users being unable to find existing content.**

**Implication**: Our #1 priority is **findability**, not creating more content.

---

## Part 1: Research-Backed Principles

### The Six Quality Issues (Based on Real User Complaints)

Analysis of 142 GitHub issues revealed these patterns:

| Issue Type | % of Issues | What Users Said | Our Rule |
|------------|-------------|-----------------|----------|
| Missing Documentation | 72% | "This feature isn't documented" | Make content **discoverable** through clear titles, cross-links, search terms |
| Missing Context | 13% | "I don't know the prerequisites" | Always include **prerequisites** and **related topics** |
| Short Pages | 52%* | "Documentation is incomplete" | Minimum **100 words** per page with examples |
| Missing Examples | 31%* | "No code examples provided" | **Every technical page** must have code examples |
| Unclear Language | 4% | "I don't understand what this means" | Use **clear, direct language**; avoid weak words |
| Long Paragraphs | 5%* | "Hard to scan/read" | Maximum **4 lines** per paragraph |

*From automated quality analysis of 115 files, 3,023 issues detected

---

## Part 2: Core Documentation Standards

### 2.1 Page Structure (Required)

Every documentation page MUST include:

#### Frontmatter (YAML)
```yaml
---
title: "Clear, Descriptive Title (What This Page Is About)"
description: "Concise 1-2 sentence summary for SEO and navigation"
---
```

#### Content Structure
1. **Opening paragraph** - What this page covers (1-2 sentences)
2. **Prerequisites** (if procedural/technical) - What users need to know first
3. **Main content** - Organized with clear headings
4. **Code examples** (if technical) - At least one working example
5. **Related topics** - 3-5 links to related pages

**Example**:
```markdown
---
title: "Prompt Caching"
description: "Learn how to use prompt caching to reduce latency and costs for repeated API calls"
---

Prompt caching allows you to reuse previously processed prompts, reducing both latency and costs when making repeated API calls with similar context.

## Prerequisites

Before using prompt caching, you should:
- Understand [basic API usage](../api-basics)
- Have an API key configured
- Be familiar with [token counting](../tokens)

## How Prompt Caching Works

[Main content here...]

## Example: Caching a System Prompt

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello"}],
    system=[
        {
            "type": "text",
            "text": "You are a helpful assistant...",
            "cache_control": {"type": "ephemeral"}
        }
    ]
)
```

## Related Topics

- [API Rate Limits](../rate-limits)
- [Token Counting](../tokens)
- [Cost Optimization](../cost-optimization)
```

### 2.2 Word Count Requirements

**Minimum word counts** (based on "incomplete documentation" complaints):

| Page Type | Minimum Words | Why |
|-----------|---------------|-----|
| Conceptual | 150 words | Need enough context to understand the concept |
| How-to Guide | 200 words | Include prerequisites, steps, examples, troubleshooting |
| API Reference | 100 words | Description, parameters, examples, related endpoints |
| Tutorial | 300 words | Step-by-step with context and examples |

**Red flags**:
- Page < 100 words = Likely incomplete
- Page with code-related terms but no code blocks = Missing critical examples
- How-to without prerequisites = Users will get stuck

### 2.3 Code Examples (Required)

**Rule**: Every page that mentions technical implementation MUST include code examples.

**Code-related terms that trigger this requirement**:
- API, SDK, CLI, command
- Function, method, class, module
- Request, response, endpoint
- Authentication, configuration
- Integration, implementation

**Code block standards**:
```python
# ✅ GOOD: Language specified, complete working example
import anthropic

client = anthropic.Anthropic(api_key="your-api-key")
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)
print(message.content)
```

```
# ❌ BAD: No language tag, incomplete snippet
client.messages.create(
    model=...
```

**Code example requirements**:
- Language tag on every code block
- Complete, runnable examples (not fragments)
- Include necessary imports
- Show both request and response where applicable
- Include error handling for complex examples

### 2.4 Prerequisites Section

**When required**: All how-to guides, tutorials, and procedural documentation

**Format**:
```markdown
## Prerequisites

Before [doing this task], you should:
- [First prerequisite with link if applicable]
- [Second prerequisite]
- [Third prerequisite]

You'll need:
- [Required tool/account/access]
- [Another requirement]
```

**Example**:
```markdown
## Prerequisites

Before setting up computer use, you should:
- Understand [basic API usage](../api-basics)
- Have Docker installed and running
- Be familiar with [tool use concepts](../tool-use)

You'll need:
- An Anthropic API key
- A machine with at least 2GB RAM
- Python 3.9 or higher
```

**Red flag**: How-to or tutorial without prerequisites = users will get stuck and file GitHub issues

---

## Part 3: Writing Standards

### 3.1 Voice and Tone

**Voice**: Second person ("you"), active voice, direct

✅ **Good Examples**:
- "You can use prompt caching to reduce costs"
- "Send a POST request to the `/messages` endpoint"
- "Configure your API key before making requests"

❌ **Bad Examples**:
- "One can use prompt caching..." (too formal)
- "Costs can be reduced by using prompt caching" (passive voice)
- "It is possible to configure..." (weak language)

### 3.2 Clear, Direct Language

**Avoid weak qualifiers** (from quality analysis):

| ❌ Avoid | ✅ Use Instead | Why |
|---------|----------------|-----|
| simply, just, easily | [omit] | Dismissive to struggling users |
| utilize, leverage | use | Unnecessarily complex |
| in order to | to | Wordier than needed |
| please note that | [omit or restructure] | Adds no value |
| it is important to note | [state directly] | Weak opening |

**Before and After**:

❌ Before: "You can simply leverage the API to easily implement this feature. Please note that you should configure authentication first."

✅ After: "Configure authentication, then call the API to implement this feature."

### 3.3 Paragraph Length

**Maximum**: 4 lines in rendered output

**Rationale**: Users complained about readability. Shorter paragraphs are scannable.

**How to fix long paragraphs**:
1. Split into multiple paragraphs
2. Convert to bulleted list
3. Add subheadings to break up content

### 3.4 Terminology Standards

**Capitalization**:
- Claude (always capitalized)
- API, SDK, CLI, JSON, HTTP (all caps)
- Anthropic (capitalized)
- markdown (lowercase unless starting sentence)

**Consistent terms**:
- "API key" (not "api key" or "API Key")
- "prompt caching" (not "Prompt Caching" in body text)
- "system prompt" (not "System Prompt" in body text)

---

## Part 4: Findability Standards

### 4.1 Page Titles

**Rule**: Titles must be descriptive and searchable

✅ **Good titles**:
- "Prompt Caching" (clear, searchable)
- "Rate Limits and Quotas" (describes content)
- "Authentication: API Keys" (hierarchical, clear)

❌ **Bad titles**:
- "Overview" (what is this an overview of?)
- "Getting Started" (with what?)
- "Advanced Features" (which features?)

**Title formula**: `[Main Topic]` or `[Main Topic]: [Specific Aspect]`

### 4.2 Headings

**Rule**: Headings must be descriptive and front-loaded with keywords

✅ **Good headings**:
- "## How Prompt Caching Works"
- "## Set Up Authentication"
- "## Common Error Messages"

❌ **Bad headings**:
- "## Introduction" (to what?)
- "## Next Steps" (which steps?)
- "## More Information" (what information?)

### 4.3 Cross-Referencing

**Rule**: Include 3-5 related topic links at the end of every page

**Format**:
```markdown
## Related Topics

- [Topic 1](link) - Brief description of what users will find
- [Topic 2](link) - Brief description
- [Topic 3](link) - Brief description
```

**Strategic cross-linking**:
- Link to prerequisites
- Link to next logical steps
- Link to related concepts
- Link to troubleshooting pages

**Example**:
```markdown
## Related Topics

- [API Authentication](../auth) - Learn how to configure API keys
- [Token Counting](../tokens) - Understand how tokens are counted for caching
- [Cost Optimization](../costs) - Additional strategies to reduce API costs
- [Error Handling](../errors) - Handle cache-related errors
```

### 4.4 Search Optimization

**Include searchable keywords** users might use:

**Example**: For a page about prompt caching, include:
- "prompt caching"
- "cache prompts"
- "reduce latency"
- "reduce costs"
- "reuse prompts"
- Common error messages users might search for

**Where to include keywords**:
- Page title
- Description (frontmatter)
- First paragraph
- Headings
- Code comments (for code searches)

---

## Part 5: Content Types and When to Use Them

### 5.1 Conceptual Documentation

**Purpose**: Explain what something is and why it matters

**Structure**:
1. What is it? (1-2 sentences)
2. Why would you use it?
3. How does it work? (high-level)
4. When should you use it?
5. Related concepts

**Template**: [See templates/conceptual.mdx](templates/conceptual.mdx)

### 5.2 How-To Guides

**Purpose**: Task-oriented instructions

**Structure**:
1. What you'll accomplish
2. Prerequisites
3. Step-by-step instructions
4. Verification (how to know it worked)
5. Troubleshooting (common issues)
6. Next steps

**Template**: [See templates/how_to_guide.mdx](templates/how_to_guide.mdx)

### 5.3 API Reference

**Purpose**: Technical reference for endpoints, parameters, responses

**Structure**:
1. Brief description
2. Endpoint/method signature
3. Parameters table
4. Request example
5. Response example
6. Error codes
7. Related endpoints

**Template**: [See templates/api_reference.mdx](templates/api_reference.mdx)

### 5.4 Tutorials

**Purpose**: Learning-oriented, step-by-step journey

**Structure**:
1. What you'll build/learn
2. Prerequisites
3. Step 1: [First step with explanation]
4. Step 2: [Second step with explanation]
5. ...
6. What you learned
7. Next steps

**Template**: [See templates/tutorial.mdx](templates/tutorial.mdx)

### 5.5 Troubleshooting Guides

**Purpose**: Help users diagnose and fix problems

**Structure**:
1. Error message or symptom
2. Possible causes
3. Solutions (ordered by likelihood)
4. Prevention
5. Related issues

**Template**: [See templates/troubleshooting.mdx](templates/troubleshooting.mdx)

---

## Part 6: Quality Checklist

Before publishing any documentation page, verify:

### Content Completeness
- [ ] Page is at least 100 words (150+ for conceptual, 200+ for how-to)
- [ ] Includes frontmatter with title and description
- [ ] Has at least one code example (if technical content)
- [ ] Includes prerequisites (if how-to/tutorial)
- [ ] Has 3-5 related topic links

### Clarity
- [ ] Uses second person ("you")
- [ ] Uses active voice
- [ ] Avoids weak qualifiers (simply, just, leverage)
- [ ] No paragraphs longer than 4 lines
- [ ] All technical terms defined on first use

### Findability
- [ ] Title is descriptive and searchable
- [ ] Headings are front-loaded with keywords
- [ ] First paragraph clearly states what page covers
- [ ] Includes searchable keywords users might look for
- [ ] Cross-links to related pages

### Technical Accuracy
- [ ] All code examples are complete and runnable
- [ ] Code blocks have language tags
- [ ] All links work (internal and external)
- [ ] API endpoints and parameters are current
- [ ] Error messages match current implementation

---

## Part 7: Common Mistakes to Avoid

### Mistake 1: Creating New Content Instead of Improving Findability

**Problem**: User files issue saying "X feature isn't documented"
**Wrong response**: Write new documentation for X
**Right response**:
1. Search if X is already documented
2. If yes (90% of cases), improve findability:
   - Add cross-links from related pages
   - Improve page title/description
   - Add to navigation
   - Add to search keywords
3. If no (10% of cases), then create new content

### Mistake 2: Short Pages Without Examples

**Problem**: Created page with 50 words and no code examples
**Why it's bad**: Users will file issues saying it's "incomplete"
**Fix**: Expand to minimum word count, add working code example

### Mistake 3: How-To Without Prerequisites

**Problem**: Dive straight into steps without listing prerequisites
**Why it's bad**: Users get stuck and frustrated
**Fix**: Always include "Prerequisites" section

### Mistake 4: Using Weak Language

**Problem**: "You can simply use the API to easily implement this feature"
**Why it's bad**: Dismissive to users who are struggling
**Fix**: "Use the API to implement this feature"

### Mistake 5: Vague Titles and Headings

**Problem**: Page titled "Overview" or heading "Introduction"
**Why it's bad**: Not searchable, not scannable
**Fix**: "Prompt Caching Overview" or "How Prompt Caching Works"

---

## Part 8: Editorial Workflow

### For New Pages

1. **Choose template** based on content type
2. **Fill in required sections** (frontmatter, prerequisites, examples, related topics)
3. **Run quality checklist** (see Part 6)
4. **Test code examples** - ensure they run
5. **Check word count** - meet minimums
6. **Validate with tool** (when available): `python doc_analyzer.py --style-guide your-file.mdx`
7. **Peer review** - have another writer review
8. **Publish**

### For Existing Pages

1. **Identify issue** (user complaint, quality scan, etc.)
2. **Diagnose root cause**:
   - Findability problem? → Improve cross-links, title, navigation
   - Completeness problem? → Add examples, prerequisites, detail
   - Clarity problem? → Simplify language, shorten paragraphs
   - Accuracy problem? → Update technical details
3. **Apply fix** using style guide rules
4. **Re-validate** with quality checklist
5. **Update**

---

## Part 9: Metrics and Success Criteria

### Page-Level Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Word count | >100 (varies by type) | Automated word count |
| Code examples | 100% of technical pages | Pattern matching for code blocks |
| Prerequisites | 100% of how-to/tutorials | Section detection |
| Related topics | 80% of pages | Link count in footer |
| Paragraph length | Max 4 lines | Line count per paragraph |
| Language quality | 0 weak qualifiers | Pattern matching for "simply", "just", etc. |

### Documentation Set Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| User complaints about "missing" docs | <50% of doc issues | GitHub issue categorization |
| Average page word count | >150 words | Aggregate word count |
| Pages with code examples | >80% | Automated detection |
| Style guide compliance | >90% | Automated validation pass rate |
| Broken links | 0 | Link checker |

### Research-Backed Success Indicators

- ✅ Users can find documented features (reduce "missing" complaints)
- ✅ How-to guides include clear prerequisites
- ✅ Technical pages include working code examples
- ✅ Pages meet minimum word count requirements
- ✅ Language is clear and direct (no weak qualifiers)
- ✅ Content is scannable (short paragraphs, clear headings)

---

## Part 10: For Review and Updates

### When to Update This Style Guide

- Quarterly review of GitHub issues reveals new patterns
- New Mintlify features are released
- User research shows new pain points
- Team feedback suggests improvements
- Automated validation reveals frequent violations

### How to Propose Changes

1. File issue with proposed change
2. Include rationale (preferably with user research data)
3. Provide examples of good and bad
4. Update validation rules if applicable

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Oct 31, 2025 | Initial release based on 142 issue analysis |

---

## Resources

- [Quick Reference](quick_reference.md) - 1-page cheat sheet
- [Mintlify Standards](mintlify_standards.md) - Platform-specific technical standards
- [Template Library](templates/) - Ready-to-use templates
- [Validation Rules](validation_rules.yaml) - Automated quality checks

---

**Questions or Feedback?**

This style guide is based on real user research and data analysis. If you find issues or have suggestions, please file an issue with your proposed changes and rationale.
