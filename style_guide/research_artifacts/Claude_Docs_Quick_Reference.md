# Claude Docs Quick Reference Card
## Essential Rules for Daily Use

---

## Voice & Tone

✅ **DO**
- Use "you" (second person)
- Use active voice
- Be specific and concrete
- Write conversationally but authorit

atively

❌ **AVOID**
- Weak words: simply, just, easily, obviously, clearly, basically
- Passive voice: "The API can be used"
- Vague statements: "Claude is fast"
- First person: "we recommend" (use "we" only for Anthropic company statements)

**Examples:**
- ❌ "Simply configure your API key"
- ✅ "Configure your API key"
- ❌ "The model is invoked by the API"
- ✅ "The API invokes the model"

---

## Product Names & Terminology

| Correct | Incorrect | Notes |
|---------|-----------|-------|
| Claude Sonnet 4.5 | Claude 4.5 Sonnet, claude sonnet 4.5 | Specific order, capitalize |
| Claude Haiku 4.5 | Haiku, claude haiku | Full name, capitalize |
| Claude Agent SDK | Claude Code SDK | Agent SDK is current |
| Claude Code | claude code | Capitalize (product name) |
| Built-in tools | Tools, Server Tools | Specific term for toolset |
| Agent Skills | Skills, agent skills | Capitalize when feature name |
| API key | api key, API Key | Two words, capitalize API |
| Prompt caching | Caching, Prompt Caching | Lowercase unless sentence start |

---

## Sentence & Paragraph Rules

- **Max sentence length**: 30 words
- **Max paragraph length**: 3-5 sentences
- **Use Oxford comma**: Always (A, B, and C)
- **Numbers**: Spell out 1-9, numerals for 10+ (except with units: always "5 minutes")

---

## Formatting

| Element | Format | Example |
|---------|--------|---------|
| **New terms** | Bold on first mention | **Prompt caching** reduces latency |
| **Code elements** | Inline code | Set `max_tokens` parameter |
| **UI elements** | Bold | Click **Settings** page |
| **Filenames** | Inline code | Edit `config.yaml` |
| **Parameters** | Inline code | `temperature` controls randomness |
| **Values** | Inline code | Set to `true` or `false` |

---

## Code Examples

✅ **Required:**
- Specify language on ALL code blocks
- Include error handling
- Add helpful comments (explain why)
- Make copy-paste ready
- Test before publishing

**Code Block Format:**
````markdown
```python
import anthropic
import os

client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
```
````

**Multi-language:**
Use `<CodeGroup>` component for Python, TypeScript, cURL examples

---

## Links

✅ **DO:**
- Use descriptive link text
- Use relative paths for internal links
- Verify all links work

❌ **AVOID:**
- "Click here" / "here" link text
- Absolute URLs for internal links
- Broken links

**Examples:**
- ✅ `[Learn about streaming](/en/docs/streaming)`
- ❌ `[Click here](https://docs.anthropic.com/en/docs/streaming)`
- ❌ `Read more [here](/en/docs/streaming)`

---

## Headings

- **One H1 per page** (the title)
- **Never skip levels** (H2 → H3 → H4, never H2 → H4)
- **Max 4 levels** (H1, H2, H3, H4)
- **Sentence case** ("Working with tools" not "Working With Tools")
- **No punctuation** at end of headings

---

## Required Frontmatter

```yaml
---
title: "Page Title Here"
description: "150-160 character SEO description with keywords and period at end."
---
```

**Rules:**
- `title`: 50-60 characters, unique across site
- `description`: 150-160 characters, keywords at start, end with period

---

## Mintlify Components

### Most Common

**Cards** (navigation):
```mdx
<CardGroup cols={2}>
  <Card title="Title" icon="icon-name" href="/path">
    Description
  </Card>
</CardGroup>
```

**Tabs** (multi-language):
```mdx
<Tabs>
  <Tab title="Python">
    Content
  </Tab>
</Tabs>
```

**Callouts**:
```mdx
<Warning>Important caution</Warning>
<Tip>Best practice</Tip>
<Info>Helpful context</Info>
```

**Steps**:
```mdx
<Steps>
  <Step title="First">Instructions</Step>
  <Step title="Second">Instructions</Step>
</Steps>
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Absolute internal links | Use relative: `/en/docs/page` |
| Missing language tag | Add ```python not just ``` |
| Missing frontmatter | Add title and description |
| Skipped heading level | H2 → H3 not H2 → H4 |
| "simply" / "just" / "easily" | Remove these words |
| Passive voice | Change to active |
| Multiple H1s | Only one H1 per page |
| No alt text on images | Add descriptive alt text |

---

## Page Structure

```markdown
---
title: "Page Title"
description: "Description here."
---

# Page Title (H1)

Brief introduction (1-2 sentences)

## Prerequisites (if needed)

What users need

## Main Content Section (H2)

Content organized in H2 sections

## Next Steps / Related Pages

Where to go next
```

---

## Writing Checklist

Before publishing:
- [ ] Frontmatter complete (title, description)
- [ ] One H1, proper hierarchy
- [ ] Active voice, no weak words
- [ ] Code examples tested
- [ ] All links work (relative for internal)
- [ ] Alt text on images
- [ ] Terminology consistent
- [ ] Max 30 words per sentence
- [ ] Language tags on code blocks
- [ ] Follows style guide

---

## Emergency Contacts

**Style questions:** #documentation Slack
**Technical accuracy:** Engineering team
**Template questions:** Senior technical writer
**Tool issues:** DevOps team

---

## Key Resources

- **Full Style Guide**: `Claude_Docs_Style_Guide.md`
- **Templates**: `Claude_Docs_Template_Library.md`
- **Mintlify Docs**: https://mintlify.com/docs
- **Docs Analyzer**: Run `python enhanced_doc_analyzer.py` before publishing

---

## Remember

**Core principle**: Write for users, not for us. Clear, helpful, findable.

**When in doubt**: Choose clarity over cleverness.

---

*Print this guide and keep it handy while writing!*
*Version 1.0 | Last updated: October 30, 2025*
