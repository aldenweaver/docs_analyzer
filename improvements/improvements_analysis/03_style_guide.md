# Claude Documentation Style Guide
## Consistency Standards for Technical Writing

**Version:** 1.0
**Last Updated:** October 28, 2025
**Purpose:** Ensure consistent voice, style, and formatting across all Claude documentation

---

## Table of Contents

1. [Voice & Tone](#voice--tone)
2. [Capitalization](#capitalization)
3. [Formatting](#formatting)
4. [Terminology](#terminology)
5. [Code Examples](#code-examples)
6. [Links & Navigation](#links--navigation)
7. [Structure & Headers](#structure--headers)
8. [Callouts & Alerts](#callouts--alerts)
9. [Lists & Tables](#lists--tables)
10. [Accessibility](#accessibility)

---

## 1. Voice & Tone

### General Principles

**Do:** Write in second person ("you")
```markdown
✅ You can use prompt caching to reduce costs
❌ Users can use prompt caching to reduce costs
❌ Developers can use prompt caching to reduce costs
```

**Do:** Use active voice
```markdown
✅ Claude processes your request
❌ Your request is processed by Claude
```

**Do:** Be direct and concise
```markdown
✅ Set max_tokens to limit response length
❌ You should set the max_tokens parameter in order to limit the length of the response
```

### Tone by Section

**API Reference:** Professional, precise, technical
```markdown
✅ Returns a Message object with role="assistant"
```

**Getting Started Guides:** Friendly, encouraging, action-oriented
```markdown
✅ Let's make your first API call! This will take about 2 minutes.
```

**Advanced Topics:** Informative, assumption of knowledge, still clear
```markdown
✅ When implementing retry logic, use exponential backoff to avoid overwhelming the rate limiter.
```

### Avoid

❌ Marketing language in technical docs
```markdown
❌ Claude is the most amazing AI assistant ever created!
✅ Claude is Anthropic's AI assistant, designed for safety and helpfulness.
```

❌ Unnecessary jargon without definition
```markdown
❌ Implement a backpressure mechanism for token management
✅ Use rate limiting to control token usage and avoid hitting API limits
```

❌ Apologies or hedging
```markdown
❌ Unfortunately, we don't support this feature yet
✅ This feature is not currently supported
❌ This might work, but we're not sure
✅ This approach works for most use cases
```

---

## 2. Capitalization

### Product Names (Always Capitalize)

✅ **Claude**
✅ **Claude Code**
✅ **Claude API**
✅ **Anthropic Console**
✅ **Model Context Protocol** (full name)
❌ claude, claude code, api, console, model context protocol

### Feature Names (Title Case for Proper Nouns)

✅ **Extended Thinking** (official feature name)
✅ **Prompt Caching** (official feature name)
✅ **Agent Skills** (official feature name)
✅ **MCP** (acronym when referring to protocol)

### Feature Names (Lowercase for General Concepts)

✅ batch processing (general concept)
✅ streaming (general concept)
✅ tool use (general concept)
✅ vision (general concept)

### Rule of Thumb
If it's a branded feature with a specific implementation, capitalize it. If it's a general capability concept, use lowercase.

**Examples:**
```markdown
✅ Use Extended Thinking for complex reasoning tasks
✅ Claude supports vision capabilities across all models
✅ Prompt Caching reduces costs for repeated content
✅ The streaming API allows real-time responses
```

### Model Names

✅ **Claude Sonnet 4.5** (with spaces)
✅ **Claude Opus 4.1** (with spaces)
✅ **Claude Haiku 4.5** (with spaces)
❌ Claude-sonnet-4-5, claude-sonnet-4.5, Sonnet 4.5 (missing "Claude")

### Technical Terms

✅ API (all caps)
✅ SDK (all caps)
✅ MCP (all caps when acronym)
✅ REST (all caps)
✅ JSON (all caps)
✅ OAuth (capital O, capital A)

### URLs & Endpoints

✅ Always lowercase in code/URLs
```markdown
✅ https://api.anthropic.com/v1/messages
✅ /en/docs/build-with-claude
```

---

## 3. Formatting

### Bold

Use bold for:
- UI elements: Click **Save**
- First mention of important terms: The **context window** is...
- Emphasis sparingly: This is **required**

Don't use bold for:
- Headers (they're already styled)
- Entire paragraphs
- Links (they're already styled)

### Italic

Use italic for:
- Book/publication titles: *The Alignment Problem*
- Introducing new terms (first use): *Prompt injection* is...
- Mathematical variables: *n* tokens

Don't use italic for:
- Emphasis (use bold sparingly instead)
- Code or technical terms (use backticks)

### Code Formatting

**Inline code:** Use backticks for:
- Parameter names: `max_tokens`
- Values: `true`, `false`, `null`
- Functions: `client.messages.create()`
- File names: `config.json`
- Endpoints: `/v1/messages`

```markdown
✅ Set `max_tokens` to `1024`
❌ Set max_tokens to 1024
```

**Code blocks:** Use fenced code blocks with language tags

```python
# ✅ Good: Language specified, syntax highlighting works
def example():
    return "Hello"
```

    # ❌ Bad: No language specified
    def example():
        return "Hello"

### Special Characters

- Em dash (—) for parenthetical breaks: "Claude processes requests—typically within seconds—and returns results"
- En dash (–) for ranges: "200–500 tokens"
- Hyphen (-) for compound words: "user-facing", "well-known"

---

## 4. Terminology

### Canonical Terms (Use These)

| ✅ Use This | ❌ Not This |
|------------|-------------|
| documentation | docs (except in URLs) |
| API key | api key, API-key, apikey |
| request | API call (unless specifically referring to the call) |
| response | API response, return value |
| parameter | param, argument |
| endpoint | API endpoint, route |
| context window | context, window |
| message | prompt (in API context) |
| tool use | function calling, tool calling |
| model | LLM, AI, model name |

### Pronouns

**For Claude:**
- ✅ Use "it" or "Claude"
- ❌ Don't use "he/she"

```markdown
✅ Claude processes the request and returns its response
✅ The model analyzes the input
❌ Claude processes the request and returns his response
```

**For Users:**
- ✅ Use "you" (second person)
- ❌ Avoid "the user", "developers" in instructions

### Abbreviations

**First use:** Spell out, then show abbreviation
```markdown
✅ Model Context Protocol (MCP) enables...
   Later in the same page: MCP allows you to...

❌ MCP enables... (no definition)
```

**Common abbreviations (don't need definition):**
- API
- SDK
- REST
- JSON
- HTTP
- HTTPS
- URL

---

## 5. Code Examples

### Always Include

1. **Comments** explaining non-obvious parts
2. **Complete, runnable** examples (not fragments)
3. **Error handling** for production examples
4. **Expected output** when helpful

### Code Block Structure

```python
# ✅ Good example
from anthropic import Anthropic

# Initialize client with your API key
client = Anthropic()  # Reads ANTHROPIC_API_KEY from environment

# Create a message with error handling
try:
    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Hello, Claude!"}
        ]
    )
    print(message.content)
except Exception as e:
    print(f"Error: {e}")
```

```python
# ❌ Bad example (fragment, no context, no error handling)
messages.create(
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Multi-Language Examples

Use tabs for multi-language code:

```markdown
<CodeGroup>
```python Python
client = Anthropic()
message = client.messages.create(...)
```

```typescript TypeScript
const client = new Anthropic();
const message = await client.messages.create(...);
```
</CodeGroup>
```

### What to Show vs Hide

**Show:**
- Required imports
- Client initialization
- Main logic
- Error handling

**Can hide/simplify:**
- Long environment setup
- Boilerplate that's always the same
- Test data generation

---

## 6. Links & Navigation

### Link Text Guidelines

**Do:** Use descriptive link text
```markdown
✅ See the [prompt caching guide](/en/docs/build-with-claude/prompt-caching)
✅ Learn more about [model selection](/en/docs/about-claude/models)
```

**Don't:** Use generic link text
```markdown
❌ Click [here](/en/docs/prompt-caching) to learn about caching
❌ See [this page](/en/docs/models) for model information
❌ [Read more](/en/docs/streaming)
```

### External Links

- Always open in new tab: `target="_blank"`
- Use full URL for external sites
- Add icon or indicator when possible

```markdown
✅ [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) <Icon icon="external-link" />
```

### Cross-References

**Within same section:**
```markdown
✅ See [Streaming](#streaming) below
✅ As mentioned in the [Quick Start](#quick-start) section
```

**To other pages:**
```markdown
✅ Learn about [Extended Thinking](/en/docs/build-with-claude/extended-thinking)
✅ See the [API Reference](/en/api/messages)
```

### Broken Link Prevention

- Use relative paths: `/en/docs/...` not `https://docs.anthropic.com/en/docs/...`
- Link to anchors carefully (they break if headers change)
- Regular link audits

---

## 7. Structure & Headers

### Header Hierarchy

```markdown
# Page Title (H1 - Only one per page)

## Major Section (H2)

### Subsection (H3)

#### Detail Level (H4)

##### Rare Detail (H5 - use sparingly)
```

**Rules:**
- Only ONE H1 per page (the title)
- Don't skip levels (H2 → H4 is wrong)
- Keep hierarchy consistent

### Header Capitalization

**Use sentence case:**

```markdown
✅ ## How prompt caching works
✅ ## Quick start guide
✅ ## Best practices for production

❌ ## How Prompt Caching Works
❌ ## Quick Start Guide
❌ ## Best Practices For Production
```

**Exceptions:** Capitalize proper nouns

```markdown
✅ ## Using Extended Thinking
✅ ## Connecting to PostgreSQL
✅ ## Claude Code installation
```

### Header Style

**Use action-oriented headers:**
```markdown
✅ ## Create your first API call
✅ ## Configure authentication
✅ ## Debug common errors
```

**Not noun phrases when possible:**
```markdown
❌ ## API Call Creation
❌ ## Authentication Configuration
❌ ## Error Debugging
```

---

## 8. Callouts & Alerts

### Standard Callout Types

Use Mintlify callout components:

**Note:** General information
```markdown
<Note>
This feature is available in all Claude models.
</Note>
```

**Tip:** Helpful suggestion or best practice
```markdown
<Tip>
Use prompt caching for documents over 10K tokens to maximize savings.
</Tip>
```

**Warning:** Important caution
```markdown
<Warning>
Changing this parameter will invalidate your cache.
</Warning>
```

**Info:** Additional context (use sparingly)
```markdown
<Info>
This feature is in beta. The API may change.
</Info>
```

### When to Use Each

| Type | Use For | Example |
|------|---------|---------|
| **Note** | Important info that's not critical | "Extended Thinking is only available in Claude 4.5+" |
| **Tip** | Optimization, best practice | "Enable caching for repeated content to save 90%" |
| **Warning** | Potential issues, breaking changes | "Don't store API keys in client-side code" |
| **Info** | Beta features, additional context | "This feature will GA in Q2 2025" |

### Don't Overuse

❌ Too many callouts make pages hard to scan
✅ Use 1-3 callouts per section maximum

---

## 9. Lists & Tables

### Bulleted Lists

Use for:
- Unordered collections
- Feature lists
- Requirements

```markdown
✅
- Fast performance
- Low cost
- High availability
```

**Formatting:**
- Parallel structure (all nouns, all verbs, etc.)
- End with period if complete sentences
- No period if fragments

### Numbered Lists

Use for:
- Steps in a process
- Ordered procedures
- Rankings

```markdown
✅
1. Install the SDK
2. Set your API key
3. Make your first request
```

### Tables

Use for:
- Comparisons
- Parameters
- Reference data

**Good table example:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Model identifier |
| `max_tokens` | integer | Yes | Maximum tokens to generate |
| `temperature` | number | No | Randomness (0-1) |

**Best practices:**
- Include header row
- Align text consistently
- Keep cells concise
- Use code formatting for technical terms

---

## 10. Accessibility

### Alt Text for Images

Always provide descriptive alt text:

```markdown
✅ ![Diagram showing MCP architecture with client, server, and tool components](mcp-architecture.png)
❌ ![Diagram](mcp-architecture.png)
❌ ![](mcp-architecture.png)
```

### Color & Contrast

- Don't rely on color alone to convey information
- Use ✅ and ❌ symbols in addition to color
- Maintain WCAG AAA contrast (19.13:1)

### Link Text

- Avoid "click here" (not screen-reader friendly)
- Make link purpose clear from text alone

### Code Accessibility

- Provide text description of complex code
- Use comments to explain logic
- Don't hide information in images

---

## Quick Reference Checklist

Before publishing any documentation page:

**Voice & Tone:**
- [ ] Written in second person ("you")
- [ ] Active voice used
- [ ] Concise and direct

**Capitalization:**
- [ ] Product names capitalized (Claude, Claude Code)
- [ ] Feature names follow convention (Extended Thinking vs streaming)
- [ ] Model names with spaces (Claude Sonnet 4.5)

**Formatting:**
- [ ] Code in backticks
- [ ] Bold for UI elements and emphasis
- [ ] Headers in sentence case

**Code:**
- [ ] Complete, runnable examples
- [ ] Comments explain non-obvious parts
- [ ] Error handling included
- [ ] Expected output shown

**Links:**
- [ ] Descriptive link text (no "click here")
- [ ] External links open in new tab
- [ ] Relative paths used

**Structure:**
- [ ] Only one H1 (page title)
- [ ] Hierarchy doesn't skip levels
- [ ] Headers in sentence case

**Callouts:**
- [ ] 1-3 callouts per section max
- [ ] Appropriate type used (Note/Tip/Warning)
- [ ] Not overused

**Accessibility:**
- [ ] Alt text for all images
- [ ] Don't rely on color alone
- [ ] Link purpose clear from text

---

## Examples of Style Guide Application

### Before Style Guide Applied

```markdown
# PROMPT CACHING

Prompt Caching is a feature that lets users reuse content.

Click here to learn more about caching.

Example:
cache_control = {"type": "ephemeral"}

Note: Make sure you use the right Model.
```

**Issues:**
- Title in all caps
- Third person ("users")
- Generic link text
- Incomplete code example
- Inconsistent capitalization in callout

### After Style Guide Applied

```markdown
# Prompt caching

Prompt caching lets you reuse repeated content across multiple requests, reducing costs by up to 90%.

Learn more about [how caching works](/en/docs/build-with-claude/prompt-caching#how-it-works).

**Example:**
```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "Your large system prompt here...",
            "cache_control": {"type": "ephemeral"}  # Cache this content
        }
    ],
    messages=[
        {"role": "user", "content": "Your question"}
    ]
)
```

<Note>
Prompt caching is available for Claude Sonnet 4.5 and Claude Opus 4.1.
</Note>
```

**Improvements:**
- ✅ Sentence case title
- ✅ Second person, clear value prop
- ✅ Descriptive link text
- ✅ Complete, runnable code
- ✅ Proper callout formatting

---

## Updating This Guide

This is a living document. To propose changes:

1. Document the inconsistency found
2. Propose the new standard
3. Show before/after examples
4. Update this guide
5. Create tracking issue for applying across docs

**Version History:**
- v1.0 (Oct 28, 2025): Initial version based on comprehensive audit
