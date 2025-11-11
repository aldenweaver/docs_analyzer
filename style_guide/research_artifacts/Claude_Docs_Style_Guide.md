# Claude Documentation Style Guide
## Version 1.0 | Production-Ready Standards

---

## Executive Summary

This style guide establishes clear, enforceable standards for Claude documentation at docs.anthropic.com. It serves technical writers, engineers, and product managers contributing to documentation, providing:

- **Clear voice and tone guidelines** with before/after examples
- **Terminology standards** ensuring consistency across all pages
- **Content structure patterns** for every documentation type
- **Mintlify-specific technical standards** for proper implementation
- **Programmatically enforceable rules** for automated quality checks

**Core principle**: Documentation succeeds when users find what they need quickly, understand it immediately, and implement successfully without support.

**Quick reference**: See the [Quick Reference Card](#quick-reference-card) for most-used rules.

---

## Table of Contents

1. [Voice and Tone](#voice-and-tone)
2. [Terminology Standards](#terminology-standards)
3. [Grammar and Mechanics](#grammar-and-mechanics)
4. [Content Structure](#content-structure)
5. [Formatting Standards](#formatting-standards)
6. [Code Examples](#code-examples)
7. [Links and References](#links-and-references)
8. [Accessibility](#accessibility)
9. [Mintlify Technical Standards](#mintlify-technical-standards)
10. [Page Type Templates](#page-type-templates)
11. [Quick Reference Card](#quick-reference-card)
12. [Enforcement Rules](#enforcement-rules)

---

## Voice and Tone

### Core Principles

**Voice**: Helpful, knowledgeable, and direct
**Tone**: Conversational but authoritative
**Perspective**: Second person ("you") for all user-facing content

### Guidelines

#### ✅ DO: Use active voice

```markdown
❌ AVOID: The API key can be found in your settings
✅ USE: Find your API key in your settings

❌ AVOID: Errors are returned in the response body
✅ USE: The API returns errors in the response body
```

#### ✅ DO: Address the user directly

```markdown
❌ AVOID: Users should configure their API key
✅ USE: Configure your API key

❌ AVOID: One can improve performance by caching
✅ USE: Improve performance by caching prompts
```

#### ✅ DO: Be conversational without being casual

```markdown
❌ TOO FORMAL: It is imperative that one ascertains
✅ BETTER: Make sure you check

❌ TOO CASUAL: Just throw your API key in there
✅ BETTER: Add your API key to the request
```

#### ❌ AVOID: Weak or unnecessary words

**Eliminate these words:**
- Simply/just/easily/obviously/clearly
- Basically/actually/really
- Very/quite/rather

```markdown
❌ AVOID: Simply add your API key to get started
✅ USE: Add your API key to get started

❌ AVOID: This feature is very powerful and quite useful
✅ USE: This feature handles complex workflows efficiently

❌ AVOID: Claude can easily process large documents
✅ USE: Claude processes documents up to 200K tokens
```

#### ✅ DO: Use specific, concrete language

```markdown
❌ VAGUE: Claude is fast
✅ SPECIFIC: Claude Haiku responds in under 3 seconds

❌ VAGUE: Our models are powerful
✅ SPECIFIC: Claude Sonnet 4.5 achieves 92% on HumanEval coding benchmarks

❌ VAGUE: This improves performance
✅ SPECIFIC: Prompt caching reduces latency by up to 85% on repeated queries
```

### Tone by Content Type

| Content Type | Tone | Example |
|--------------|------|---------|
| **Quickstart** | Encouraging, supportive | "Let's get you up and running in 5 minutes" |
| **Tutorial** | Instructional, patient | "Follow these steps to build your first agent" |
| **Reference** | Precise, technical | "`max_tokens` (integer, required): Maximum tokens to generate" |
| **Troubleshooting** | Reassuring, solution-focused | "Here's how to resolve this error" |
| **Concept** | Educational, clear | "Extended thinking allows Claude to reason step-by-step" |

---

## Terminology Standards

### Product Names

| Term | Correct Usage | Notes |
|------|---------------|-------|
| **Claude** | Always capitalized | The AI assistant/model |
| **Claude Sonnet 4.5** | Full model name, numbers included | Not "Claude 4.5 Sonnet" |
| **Claude Haiku 4.5** | Full model name | Not "Haiku" alone |
| **Claude Opus 4.1** | Full model name | Not "Opus" alone |
| **Claude Agent SDK** | Current official name | NOT "Claude Code SDK" (deprecated) |
| **Claude Code** | Terminal tool name | When referring to the CLI tool |
| **Anthropic API** | Anthropic API or Claude API | Either is acceptable |

### Features and Concepts

| Preferred Term | Avoid | Notes |
|----------------|-------|-------|
| **Built-in tools** | Tools, Server Tools | When referring to the standard toolset |
| **Agent Skills** | Skills | Capitalize when referring to the feature |
| **MCP** | Model Context Protocol | Use full name on first mention |
| **Prompt caching** | Caching | Lowercase unless starting sentence |
| **Extended thinking** | Deep thinking | Official feature name |
| **Computer use** | Computer control | Official feature name |
| **API key** | api key, API Key | Two words, capitalize "API" |
| **Context window** | Context size | Standard industry term |
| **Streaming** | Stream | When referring to the feature |

### Technical Terms

| Term | Usage | Example |
|------|-------|---------|
| **Token** | Unit of text | "The model processes 1,000 tokens per second" |
| **Parameter** | API/SDK values | "`temperature` parameter controls randomness" |
| **Argument** | Function inputs | "Pass the filename as an argument" |
| **Endpoint** | API URL | "Send requests to the `/messages` endpoint" |
| **Request/Response** | API communication | Not "query/answer" for API calls |
| **Workspace** | Project environment | Claude Code workspace |

### Capitalization Rules

**Capitalize**:
- Product names (Claude, Claude Code, Anthropic API)
- Feature names when used as proper nouns (Agent Skills, Extended Thinking)
- UI element names (Settings, API Keys page)

**Lowercase**:
- Generic usage ("extended thinking enables", "use built-in tools")
- Technical concepts (tokens, parameters, endpoints)
- File formats (JSON, YAML, markdown)

### Consistency Checklist

✅ Same term throughout a document
✅ Same capitalization pattern
✅ Same spelling (American English: "optimize" not "optimise")
✅ Same hyphenation (e.g., "real-time" consistently)

---

## Grammar and Mechanics

### Sentence Structure

**Maximum sentence length**: 30 words
- Longer sentences reduce readability
- Break complex ideas into multiple sentences
- Exception: Code comments can be longer for technical precision

```markdown
❌ TOO LONG: To get started with Claude you'll need to create an account at console.anthropic.com where you can generate an API key that you'll use to authenticate your requests to the API and you should store this key securely.

✅ BETTER: To get started with Claude, create an account at console.anthropic.com. Generate an API key from your account settings. Store this key securely—you'll use it to authenticate API requests.
```

**Paragraph length**: 3-5 sentences maximum
- One main idea per paragraph
- Use headings to break up longer content
- White space improves scannability

### Lists

**Use lists when**:
- Presenting 3+ items
- Order matters (numbered) or doesn't (bulleted)
- Information is parallel in structure

**List formatting**:
```markdown
✅ Parallel structure:
- Configure your environment
- Install the SDK
- Authenticate with your API key
- Make your first request

❌ Not parallel:
- Configure your environment
- You should install the SDK
- Authenticating with your API key
- First request to the API
```

**List punctuation**:
- No periods for simple items (single word or short phrase)
- Use periods for complete sentences
- Be consistent within each list

```markdown
✅ Simple items (no periods):
- Python 3.7+
- API key
- Internet connection

✅ Complete sentences (with periods):
- Install Python 3.7 or later on your system.
- Generate an API key from your account settings.
- Ensure you have a stable internet connection.
```

### Punctuation

**Oxford comma**: Always use
```markdown
✅ Claude supports Python, TypeScript, and Java
❌ Claude supports Python, TypeScript and Java
```

**Em dash**: Use for emphasis or clarification (—)
```markdown
✅ Claude Sonnet 4.5—our smartest model—excels at complex reasoning
```

**Colons**: Introduce lists, examples, or explanations
```markdown
✅ Configure three settings: model, temperature, and max_tokens
```

**Semicolons**: Connect related independent clauses (use sparingly)
```markdown
✅ Claude Sonnet handles complex tasks; Claude Haiku prioritizes speed
```

### Numbers and Dates

**Numbers**:
- Spell out one through nine: "three parameters"
- Use numerals for 10+: "15 examples"
- Always use numerals with units: "5 minutes", "2 MB"
- Use commas for thousands: "1,000 tokens"

**Dates**:
- Format: Month DD, YYYY (e.g., "October 29, 2024")
- No ordinal indicators: "October 29" not "October 29th"

**Time**:
- 12-hour format with AM/PM: "2:30 PM"
- Use "midnight" and "noon" instead of "12:00 AM/PM"

---

## Content Structure

### Page Structure

Every documentation page should follow this structure:

```markdown
# Page Title (H1) - One per page

Brief introduction (1-2 sentences explaining what this page covers)

## Prerequisites (if applicable)
What users need before starting

## [Main Content Section]
Core content broken into logical H2 sections

## Next Steps (for tutorials/guides)
Where to go next

## Related Pages
Links to related documentation
```

### Heading Hierarchy

**Rules**:
1. One H1 per page (the title)
2. Never skip levels (H2 → H3 → H4, never H2 → H4)
3. Maximum 4 heading levels
4. Use sentence case for headings

```markdown
✅ Proper hierarchy:
# Working with Tools (H1)
## Built-in Tools (H2)
### Text Editor Tool (H3)
#### Configuration Options (H4)

❌ Skip levels:
# Working with Tools (H1)
### Text Editor Tool (H3) ← Skipped H2!
```

**Heading guidelines**:
- Be descriptive: "Configure Authentication" not "Setup"
- Use parallel structure in series
- Keep under 70 characters
- No punctuation at end

### Content Organization Patterns

**Progressive disclosure**: Simple → Complex
```markdown
1. What is this? (Concept)
2. Quick example (Simple use case)
3. How to use it (Step-by-step)
4. Advanced usage (Complex scenarios)
5. Reference (Complete API details)
```

**Task-based organization**: Organize by what users want to do
```markdown
✅ Good:
- Send your first message
- Stream responses
- Use tools
- Cache prompts

❌ Avoid feature-dump:
- Messages API overview
- Streaming parameter
- Tool use parameter
- Caching header
```

### Introductions

Every page needs a clear introduction:

```markdown
✅ Good introduction:
"This guide shows you how to use streaming to display responses as they're generated. Streaming reduces perceived latency and improves user experience for longer responses. You'll learn how to implement streaming in Python and TypeScript."

❌ Weak introduction:
"This page is about streaming."
```

**Introduction checklist**:
- ✅ What this page covers
- ✅ Why it matters
- ✅ Who should read it (if not everyone)
- ✅ Time estimate (for tutorials)

---

## Formatting Standards

### Text Formatting

| Format | Use Case | Example |
|--------|----------|---------|
| **Bold** | First mention of new terms, UI elements, emphasis | **API key**, **Settings** page |
| *Italic* | Book titles, emphasis (sparingly) | *The Pragmatic Programmer* |
| `Code` | Code elements, parameters, filenames, paths | `max_tokens`, `config.yaml` |

**Formatting rules**:
- Don't combine bold and italic
- Don't use ALL CAPS for emphasis
- Use code formatting for technical terms users might type

```markdown
✅ To configure the `max_tokens` parameter...
✅ Navigate to the **API Keys** page
✅ Set your `ANTHROPIC_API_KEY` environment variable

❌ To configure the MAX TOKENS parameter...
❌ Navigate to the *API Keys* page
```

### Code Formatting

**Inline code**: Use for:
- Parameter names: `temperature`
- Function/method names: `client.messages.create()`
- Filenames: `requirements.txt`
- Environment variables: `ANTHROPIC_API_KEY`
- Values: `true`, `false`, `null`

**Code blocks**: Use for:
- Complete code examples
- Command-line commands
- Configuration files
- API requests/responses

**Always specify language**:
````markdown
```python
import anthropic
```

```bash
npm install @anthropic-ai/sdk
```

```json
{
  "model": "claude-sonnet-4-5-20250929"
}
```
````

### Callout Boxes

Use Mintlify callout components for important information:

| Type | When to Use | Icon |
|------|-------------|------|
| `<Info>` | Helpful context, tips | ℹ️ |
| `<Warning>` | Important cautions, breaking changes | ⚠️ |
| `<Tip>` | Best practices, optimization tips | 💡 |
| `<Note>` | Additional information, clarifications | 📝 |

```mdx
<Warning>
Store your API key securely. Never commit it to version control or expose it in client-side code.
</Warning>

<Tip>
Use prompt caching to reduce latency by up to 85% on repeated queries.
</Tip>
```

### Tables

**When to use tables**:
- Comparing options
- Listing parameters
- Showing relationships

**Table formatting**:
- Header row required
- Left-align text columns
- Right-align number columns
- Keep cells concise (under 100 characters)

```markdown
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Model identifier |
| `max_tokens` | integer | Yes | Maximum tokens to generate |
| `temperature` | float | No | Randomness (0-1) |
```

---

## Code Examples

### Code Quality Standards

Every code example must:
1. **Run as written** (copy-paste ready)
2. **Include error handling** (production-ready)
3. **Use current best practices** (not deprecated patterns)
4. **Be properly commented** (explain why, not just what)

### Example Structure

```python
# ✅ Complete, production-ready example

import anthropic
import os

# Initialize the client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

try:
    # Create a message with streaming
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": "Explain quantum computing in simple terms"
        }]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            
except anthropic.APIError as e:
    print(f"API error: {e.status_code} - {e.message}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")
```

### Example Complexity Levels

**Basic Example** (Getting started):
- Minimal code showing core concept
- Inline comments for key points
- One clear purpose

**Intermediate Example** (Common use cases):
- Error handling included
- Multiple related features
- Comments explaining decisions

**Production Example** (Real-world ready):
- Comprehensive error handling
- Logging and monitoring
- Configuration management
- Performance optimizations

### Multi-Language Examples

Always provide examples in:
1. **Python** (primary)
2. **TypeScript** (primary)
3. **cURL** (for API endpoint docs)

Additional languages as relevant:
- Java, Go, Ruby, PHP, C#

Use Mintlify's `<CodeGroup>` component:

```mdx
<CodeGroup>
```python
import anthropic

client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
print(message.content)
```

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();
const message = await client.messages.create({
  model: "claude-sonnet-4-5-20250929",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello" }],
});
console.log(message.content);
```

```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```
</CodeGroup>
```

### Code Comments

**Comment style**:
- Use clear, complete sentences
- Explain why, not just what
- Keep comments concise
- Update comments when code changes

```python
# ✅ Good comments
# Initialize with extended context window for processing large documents
client = anthropic.Anthropic()

# Use streaming to show progress for long generations
with client.messages.stream(...) as stream:
    # Process each token as it arrives
    for text in stream.text_stream:
        print(text, end="")

# ❌ Bad comments
# Create client
client = anthropic.Anthropic()

# Stream
with client.messages.stream(...) as stream:
    # Print
    for text in stream.text_stream:
        print(text)
```

---

## Links and References

### Link Guidelines

**Link text**:
- Must be descriptive (not "click here")
- Should make sense out of context
- Keep under 100 characters

```markdown
✅ [Learn about prompt caching](/en/docs/prompt-caching)
✅ See our [model comparison guide](/en/docs/models)

❌ [Click here](/en/docs/prompt-caching) to learn about caching
❌ Read more [here](/en/docs/models)
```

### Internal Links

**Rules**:
1. **Always use relative paths** for internal links
2. Start with `/en/` for English docs
3. Include section anchors when linking to specific content
4. Verify all links during review

```markdown
✅ Correct:
[Get started](/en/docs/quickstart)
[View API reference](/en/api/messages)
[Learn about streaming](/en/docs/streaming#implementation)

❌ Incorrect:
[Get started](https://docs.anthropic.com/en/docs/quickstart)
[View API reference](../../api/messages)
```

### External Links

**When to use external links**:
- GitHub repositories
- Third-party tools/services
- Academic papers
- Industry standards

**External link format**:
- Use full URLs
- Open in new tab (Mintlify default)
- Add context about destination

```markdown
✅ [GitHub repository](https://github.com/anthropics/anthropic-sdk-python)
✅ [OAuth 2.0 specification](https://oauth.net/2/)
```

### Cross-References

Add "Related pages" sections at page end:

```markdown
## Related Pages

- [Streaming responses](/en/docs/streaming)
- [Error handling](/en/docs/errors)
- [API reference](/en/api/messages)
```

**Cross-reference guidelines**:
- 3-5 related links
- Most relevant first
- Brief context if needed

---

## Accessibility

### Writing for Accessibility

**Use clear, simple language**:
- Short sentences
- Common words
- Active voice
- Logical organization

**Structure for screen readers**:
- Proper heading hierarchy
- Descriptive links
- Alt text for images
- Table headers

### Image Alt Text

**Alt text requirements**:
- Describe the image content
- Include text visible in the image
- Keep under 150 characters
- Don't start with "Image of" or "Picture of"

```markdown
✅ ![Claude Code terminal showing successful API call with response output](./terminal-example.png)

❌ ![](./terminal-example.png)
❌ ![Image of terminal](./terminal-example.png)
```

**When to use empty alt text**:
- Decorative images only
- Use: `![](./image.png)` or `alt=""`

### Keyboard Navigation

Ensure all interactive elements are keyboard-accessible:
- Logical tab order
- Skip links for long pages
- Visible focus indicators

### Color and Contrast

- Don't rely on color alone to convey information
- Maintain WCAG AA contrast ratios (4.5:1 for text)
- Use icons with text labels

---

## Mintlify Technical Standards

### Frontmatter Requirements

Every MDX page **must** include frontmatter:

```yaml
---
title: "Page Title"
description: "150-160 character SEO-optimized summary"
---
```

**Required fields**:
- `title`: Page title (50-60 characters, matches H1)
- `description`: SEO description (150-160 characters)

**Optional fields**:
- `sidebarTitle`: Shorter title for navigation
- `icon`: Icon name from available set
- `mode`: "wide" for full-width content

**Frontmatter checklist**:
✅ Title is unique across site
✅ Description includes target keywords
✅ Description ends with period
✅ No HTML in frontmatter values

### Component Usage

#### Cards

Use for navigation hubs and feature highlights:

```mdx
<CardGroup cols={2}>
  <Card title="Quickstart" icon="rocket" href="/en/docs/quickstart">
    Get started in 5 minutes
  </Card>
  <Card title="API Reference" icon="code" href="/en/api/overview">
    Complete endpoint documentation
  </Card>
</CardGroup>
```

**Card guidelines**:
- Use `cols={2}` or `cols={3}` for layout
- Keep titles short (under 30 characters)
- Brief description (under 100 characters)
- Always include `href` for clickable cards

#### Tabs

Use for multi-language code examples or multiple approaches:

```mdx
<Tabs>
  <Tab title="Python">
    ```python
    import anthropic
    ```
  </Tab>
  <Tab title="TypeScript">
    ```typescript
    import Anthropic from "@anthropic-ai/sdk";
    ```
  </Tab>
</Tabs>
```

#### Steps

Use for sequential procedures:

```mdx
<Steps>
  <Step title="Install the SDK">
    Run `npm install @anthropic-ai/sdk`
  </Step>
  <Step title="Set your API key">
    Export `ANTHROPIC_API_KEY` environment variable
  </Step>
  <Step title="Make your first request">
    Create a message using the examples below
  </Step>
</Steps>
```

#### Accordions

Use for optional content, FAQs, or collapsible details:

```mdx
<AccordionGroup>
  <Accordion title="How do I get an API key?">
    Generate an API key from your [account settings](https://console.anthropic.com).
  </Accordion>
  <Accordion title="What are rate limits?">
    Rate limits vary by usage tier. See our [rate limits guide](/en/docs/rate-limits).
  </Accordion>
</AccordionGroup>
```

### Navigation Configuration

Edit `mint.json` for site navigation:

```json
{
  "navigation": [
    {
      "group": "Getting Started",
      "pages": [
        "docs/intro",
        "docs/quickstart",
        "docs/get-started"
      ]
    },
    {
      "group": "Build with Claude",
      "pages": [
        "docs/prompt-engineering",
        "docs/tool-use",
        "docs/streaming"
      ]
    }
  ]
}
```

**Navigation rules**:
- Maximum 3 levels deep
- Group related pages
- Use clear group names
- Order by user journey

### Code Block Best Practices

**Language tags** (required):
- `python`, `typescript`, `javascript`, `bash`, `json`, `yaml`, `jsx`, `tsx`
- Use lowercase
- No spaces or special characters

**Features to use**:
```python
# Line highlighting
```python {2-4}
import anthropic

client = anthropic.Anthropic()  # Highlighted
message = client.messages.create()  # Highlighted
```

# Filename display
```python title="example.py"
import anthropic
```
```

### SEO Optimization

**Page titles**:
- Include target keywords
- Keep under 60 characters
- Front-load important words

**Descriptions**:
- Include primary keyword naturally
- Call to action when appropriate
- 150-160 characters (full SERP display)

**URL structure**:
- Use clear, descriptive paths
- Lowercase with hyphens
- Avoid dates or versions in URLs

---

## Page Type Templates

See the separate **Template Library** document for complete templates including:

1. **Quickstart Guide Template**
2. **Tutorial Template**
3. **API Reference Template**
4. **Troubleshooting Guide Template**
5. **Concept/Overview Template**
6. **How-To Guide Template**
7. **Migration Guide Template**
8. **Release Notes Template**

Each template includes:
- Filled example showing best practices
- Blank template ready to use
- Required sections and optional sections
- Frontmatter example
- Component usage examples

---

## Quick Reference Card

### Most Common Rules

**Voice & Tone**
- ✅ Use "you" (second person)
- ✅ Use active voice
- ❌ Avoid "simply", "just", "easily"
- ✅ Be specific, not vague

**Terminology**
- Claude Sonnet 4.5 (not "Claude 4.5 Sonnet")
- Claude Agent SDK (not "Claude Code SDK")
- Built-in tools (not "Tools" alone)
- Agent Skills (capitalize when feature name)
- API key (two words)

**Formatting**
- **Bold**: First mentions, UI elements
- `Code`: Parameters, filenames, code elements
- *Italic*: Rarely (book titles only)

**Sentences**
- Maximum 30 words
- Active voice preferred
- Eliminate weak words

**Lists**
- Use Oxford comma
- Parallel structure required
- No periods on simple items
- Periods on complete sentences

**Code Examples**
- Always specify language
- Include error handling
- Add helpful comments
- Make copy-paste ready

**Links**
- Descriptive text (not "click here")
- Relative paths for internal
- Verify all links work

**Mintlify**
- Required frontmatter: `title`, `description`
- Always use relative internal links
- Specify language on all code blocks
- Use components: Cards, Tabs, Steps

### Quick Checklist for New Pages

- [ ] Frontmatter complete (`title`, `description`)
- [ ] One H1 (page title)
- [ ] Proper heading hierarchy (no skipped levels)
- [ ] Introduction explains what, why, who
- [ ] Active voice throughout
- [ ] No weak words (simply, just, easily)
- [ ] Code examples have language tags
- [ ] All links are relative (internal)
- [ ] Alt text on all images
- [ ] Consistent terminology
- [ ] Related pages section

---

## Enforcement Rules

### Automated Check Categories

These rules can be programmatically enforced by the docs_analyzer tool:

#### Critical Priority (Block Publishing)

| Rule ID | Description | Check Method |
|---------|-------------|--------------|
| `FMT-001` | Missing frontmatter | Parse YAML frontmatter |
| `FMT-002` | Missing `title` field | Check frontmatter keys |
| `FMT-003` | Missing `description` field | Check frontmatter keys |
| `LNK-001` | Broken internal link | Verify target file exists |
| `LNK-002` | Absolute URL for internal link | Regex: `https?://docs\.(anthropic\|claude)\.com` |
| `CODE-001` | Code block missing language tag | Check for ` ``` ` without language |

#### High Priority (Fix Within 1 Week)

| Rule ID | Description | Check Method |
|---------|-------------|--------------|
| `TERM-001` | "Claude Code SDK" (deprecated) | Text search |
| `TERM-002` | Inconsistent product capitalization | Pattern matching |
| `STR-001` | Heading hierarchy skip | Parse heading levels |
| `STR-002` | Multiple H1 headings | Count `#` headers |
| `SENT-001` | Sentence exceeds 30 words | Word count per sentence |
| `VOICE-001` | Passive voice usage | Linguistic pattern matching |

#### Medium Priority (Fix Within 1 Month)

| Rule ID | Description | Check Method |
|---------|-------------|--------------|
| `WEAK-001` | Usage of "simply" | Text search |
| `WEAK-002` | Usage of "just" | Text search |
| `WEAK-003` | Usage of "easily" | Text search |
| `WEAK-004` | Usage of "obviously" / "clearly" | Text search |
| `IMG-001` | Image missing alt text | Parse markdown image syntax |
| `PARA-001` | Paragraph exceeds 5 sentences | Sentence count per paragraph |

#### Low Priority (Best Practice)

| Rule ID | Description | Check Method |
|---------|-------------|--------------|
| `STYLE-001` | Oxford comma not used | Parse list structures |
| `STYLE-002` | Link text is "click here" / "here" | Check link text patterns |
| `STYLE-003` | Line exceeds 100 characters | Character count (excluding code) |
| `SEO-001` | Description under 100 or over 160 chars | String length |

### Enforcement Workflow

**Pre-Commit** (Local):
- Run critical checks only
- Fast execution (<5 seconds)
- Block commit if critical issues found

**Pull Request** (CI/CD):
- Run all automated checks
- Generate report with issue locations
- Require review for high-priority issues
- Auto-approve low-priority only changes

**Weekly Audit**:
- Full site scan
- Trend analysis
- Prioritized remediation list
- Track improvements over time

### Exemption Process

Some pages may need rule exemptions:

```yaml
# In page frontmatter
styleGuideExemptions:
  - SENT-001  # Technical specification requires long sentences
  - WEAK-001  # Marketing page approved by communications team
```

**Exemption approval**:
- Must be documented in PR
- Requires senior writer approval
- Time-limited (review quarterly)
- Tracked in audit reports

---

## Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-10-30 | Initial production release | Technical Writing Team |

---

## Questions or Suggestions?

This is a living document. Suggest improvements via:
- Documentation pull requests
- Style guide discussion channel
- Technical writing team meetings

For questions about specific cases, consult:
1. This style guide
2. Template library
3. Senior technical writer
4. Style guide committee

---

**Remember**: The goal is clear, consistent, helpful documentation. When rules conflict with clarity, choose clarity and document the exception.
