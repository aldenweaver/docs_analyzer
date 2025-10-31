# Mintlify Technical Implementation Standards

**Platform**: Mintlify
**Format**: MDX (Markdown + JSX)
**Version**: 1.0
**Last Updated**: October 31, 2025

---

## Overview

This guide covers Mintlify-specific technical requirements for Claude documentation. For general writing standards, see the [Core Style Guide](core_style_guide.md).

---

## 1. Frontmatter Requirements

### 1.1 Required Fields

Every MDX file MUST have YAML frontmatter with these fields:

```yaml
---
title: "Page Title"
description: "SEO and navigation summary (1-2 sentences)"
---
```

### 1.2 Optional Fields

```yaml
---
title: "Page Title"
description: "SEO summary"
icon: "icon-name"  # Mintlify icon
iconType: "solid"  # or "regular", "light", "duotone"
mode: "wide"  # For wider content layout
---
```

### 1.3 Frontmatter Validation Rules

**Title**:
- ✅ Must be a string
- ✅ Maximum 60 characters (for SEO)
- ✅ Should be descriptive and searchable
- ❌ Should NOT contain JavaScript or code
- ❌ Should NOT be generic ("Overview", "Introduction")

**Description**:
- ✅ Must be a string
- ✅ 50-160 characters (optimal for SEO)
- ✅ Should summarize page content
- ✅ Should include searchable keywords

**Example - Valid Frontmatter**:
```yaml
---
title: "Prompt Caching"
description: "Reduce latency and costs by reusing previously processed prompts in your API calls"
icon: "bolt"
iconType: "solid"
---
```

**Example - Invalid Frontmatter**:
```yaml
---
title: "export function openSearch() {"  # ❌ Contains JavaScript
description: "Overview of features"  # ❌ Too vague
---
```

---

## 2. Heading Hierarchy (CRITICAL FOR MINTLIFY)

### 2.1 The H1 Rule

**🚨 CRITICAL**: Mintlify auto-renders the frontmatter `title` field as an H1 heading.

**Rule**: Content MUST NOT contain H1 headings (`# Heading`)

**Why**: Mintlify displays the frontmatter title as H1. If your content also has H1, you get duplicate headings.

### 2.2 Heading Structure

```markdown
---
title: "My Page Title"  # This becomes H1 automatically
---

Opening paragraph goes here.

## First Main Section  # Use H2 for top-level content headings

Content for first section.

### Subsection  # Use H3 for subsections

Content for subsection.

#### Detail Level  # Use H4 for detailed points

Content for details.
```

### 2.3 Heading Hierarchy Rules

- ✅ **H2 (`##`)**: Top-level content sections
- ✅ **H3 (`###`)**: Subsections under H2
- ✅ **H4 (`####`)**: Detailed points under H3
- ❌ **H1 (`#`)**: Never use in content (frontmatter title is H1)
- ❌ **H5 (`#####`)**: Avoid - too deep for scannability
- ❌ **H6 (`######`)**: Avoid - too deep for scannability

### 2.4 Detecting and Fixing H1 Issues

**Detection script**: Use `/Users/alden/dev/claude_docs_clone_mintlify/check_duplicate_headings.py`

```bash
python3 check_duplicate_headings.py
```

**Automated fix**: Use `/Users/alden/dev/claude_docs_clone_mintlify/fix_duplicate_h1s.py`

```bash
python3 fix_duplicate_h1s.py
```

**Manual fix**: Convert all H1 to H2

```diff
---
title: "Authentication"
---

- # Authentication Overview  # ❌ Remove this H1
+ ## Authentication Overview  # ✅ Use H2 instead
```

---

## 3. MDX Components

### 3.1 Available Mintlify Components

Mintlify provides custom MDX components. Use them appropriately:

#### Callout Boxes

```mdx
<Note>
This is a note - use for helpful tips or clarifications
</Note>

<Warning>
This is a warning - use for important caveats or potential issues
</Warning>

<Info>
This is info - use for contextual information
</Info>

<Tip>
This is a tip - use for best practices or helpful suggestions
</Tip>
```

#### Code Groups (Multiple Languages)

```mdx
<CodeGroup>

```python Python
import anthropic
client = anthropic.Anthropic()
```

```javascript JavaScript
import Anthropic from '@anthropic-ai/sdk';
const client = new Anthropic();
```

```bash cURL
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY"
```

</CodeGroup>
```

#### Accordion (Collapsible Content)

```mdx
<Accordion title="Click to expand">
Hidden content goes here. Use for optional details or advanced topics.
</Accordion>
```

#### Cards (Link Grids)

```mdx
<CardGroup cols={2}>
  <Card title="First Card" icon="star" href="/link1">
    Description of first card
  </Card>
  <Card title="Second Card" icon="bolt" href="/link2">
    Description of second card
  </Card>
</CardGroup>
```

### 3.2 Component Usage Guidelines

**When to use callouts**:
- `<Note>`: Additional context or helpful information
- `<Warning>`: Potential gotchas or breaking changes
- `<Tip>`: Best practices or optimization suggestions
- `<Info>`: Background information or related concepts

**When to use CodeGroup**:
- Showing same example in multiple languages
- Minimum 2 languages, maximum 4 (for readability)
- Always include language labels

**When to use Accordion**:
- Optional advanced content
- Troubleshooting details
- FAQ sections
- Long technical details that might overwhelm

**When to use Cards**:
- Navigation to related pages
- Feature overviews
- API endpoint listings

---

## 4. Code Blocks

### 4.1 Language Tags (Required)

Every code block MUST have a language tag:

```markdown
✅ Correct:
```python
import anthropic
```

❌ Incorrect:
```
import anthropic
```
```

### 4.2 Supported Language Tags

Common languages:
- `python`
- `javascript`
- `typescript`
- `bash`
- `curl`
- `json`
- `yaml`
- `jsx`
- `tsx`

### 4.3 Code Block Features

**Syntax highlighting**: Automatic with language tag

**Line highlighting**: Add `{line-numbers}`

```python {3-5}
import anthropic

client = anthropic.Anthropic(
    api_key="your-key-here"  # This line is highlighted
)
```

**Filename labels**: Add filename before code block

```python title="example.py"
import anthropic
```

---

## 5. Internal Links

### 5.1 Link Format

Use **relative paths** for internal links:

```markdown
✅ Correct:
[Authentication](../api/authentication)
[Prompt Caching](./prompt-caching)

❌ Incorrect:
[Authentication](https://docs.anthropic.com/api/authentication)
[Prompt Caching](/api/prompt-caching)  # Absolute path
```

### 5.2 Link Validation

- All internal links must resolve to existing pages
- Use link checker to validate: `mintlify broken-links`

```bash
npx mintlify broken-links
```

---

## 6. Images and Media

### 6.1 Image Format

```markdown
![Alt text describing image](./images/image-name.png)
```

### 6.2 Image Requirements

- ✅ **Alt text**: Required for accessibility
- ✅ **Relative paths**: Store in `/images` directory
- ✅ **Formats**: PNG, JPG, GIF, SVG
- ✅ **Optimization**: Compress images before upload
- ✅ **Max width**: 1200px recommended

### 6.3 Accessibility

Alt text MUST:
- Describe the image content
- Be concise (under 125 characters)
- Avoid "image of" or "picture of"

```markdown
✅ Good alt text:
![Claude API authentication flow diagram showing steps from key creation to request](./images/auth-flow.png)

❌ Bad alt text:
![image](./images/auth-flow.png)
```

---

## 7. docs.json Configuration

### 7.1 Navigation Structure

The `docs.json` file controls site navigation. Reference the [docs.json schema](https://mintlify.com/docs.json).

**Example structure**:
```json
{
  "name": "Claude Docs",
  "navigation": [
    {
      "group": "Getting Started",
      "pages": [
        "docs/quickstart",
        "docs/authentication"
      ]
    },
    {
      "group": "API Reference",
      "pages": [
        "api/messages",
        "api/streaming"
      ]
    }
  ]
}
```

### 7.2 Navigation Best Practices

- **Logical grouping**: Group related pages together
- **Flat hierarchy**: Avoid deeply nested groups (max 2-3 levels)
- **Descriptive group names**: Use clear, searchable names
- **Page order**: Order by user journey (basic → advanced)

---

## 8. Search Optimization

### 8.1 Searchable Content

Mintlify indexes:
- Page titles
- Headings
- Body content
- Code comments

### 8.2 Search Best Practices

**Include keywords users search for**:
- Feature names
- Common error messages
- Alternative terminology
- Common questions

**Example**:
```markdown
## Prompt Caching

Prompt caching (also called prompt reuse or prompt memoization) allows you to...
```

By including "prompt reuse" and "prompt memoization", users searching for those terms will find this page.

---

## 9. Deployment and Preview

### 9.1 Local Preview

```bash
# Start local dev server
npx mintlify dev

# Server runs on http://localhost:3000
```

### 9.2 Pre-deployment Checks

Before deploying:

```bash
# Check for broken links
npx mintlify broken-links

# Validate docs.json
npx mintlify check

# Check for duplicate H1 headings
python3 check_duplicate_headings.py
```

---

## 10. Common Mintlify Issues and Fixes

### Issue 1: Duplicate H1 Headings

**Problem**: Content has H1 (`#`) which duplicates frontmatter title
**Detection**: Run `check_duplicate_headings.py`
**Fix**: Convert all H1 to H2 in content
**Result**: Frontmatter title is the only H1

### Issue 2: Frontmatter Display in UI

**Problem**: Frontmatter YAML appears in rendered page
**Causes**:
1. JavaScript code leaked into frontmatter fields
2. Improper YAML formatting
3. Missing closing `---`

**Fix**:
```markdown
❌ Incorrect:
---
title: "export function openSearch() {"
---

✅ Correct:
---
title: "Search Functions"
---

export function openSearch() {
  // JavaScript goes AFTER frontmatter
}
```

### Issue 3: Code Blocks Not Highlighting

**Problem**: Code appears as plain text
**Cause**: Missing language tag
**Fix**: Add language tag to every code block

### Issue 4: Broken Internal Links

**Problem**: Links return 404
**Cause**: Using absolute paths or incorrect relative paths
**Fix**: Use correct relative paths
**Validation**: Run `npx mintlify broken-links`

### Issue 5: Navigation Not Updating

**Problem**: New pages don't appear in navigation
**Cause**: Not added to `docs.json`
**Fix**: Add page path to appropriate group in `docs.json`

---

## 11. Mintlify-Specific Validation Rules

When validating Claude docs, check:

### Frontmatter
- [ ] Has `title` field (string, 1-60 chars)
- [ ] Has `description` field (string, 50-160 chars)
- [ ] No JavaScript or code in frontmatter
- [ ] Proper YAML formatting

### Headings
- [ ] No H1 (`#`) in content
- [ ] Uses H2 (`##`) for top-level sections
- [ ] Logical hierarchy (H2 → H3 → H4)

### Code Blocks
- [ ] All code blocks have language tags
- [ ] Language tags are valid
- [ ] Code is complete and runnable

### Links
- [ ] Internal links use relative paths
- [ ] All links resolve (run broken-links check)
- [ ] External links use https://

### Components
- [ ] MDX components used appropriately
- [ ] CodeGroup has 2+ languages with labels
- [ ] Callouts used for appropriate content

### docs.json
- [ ] New pages added to navigation
- [ ] Pages in logical groups
- [ ] Paths match file structure

---

## 12. Testing Checklist

Before merging changes:

```bash
# 1. Check for H1 duplicates
python3 check_duplicate_headings.py

# 2. Start local preview
npx mintlify dev

# 3. Manual checks in browser:
#    - Page renders correctly
#    - Frontmatter doesn't display
#    - Code blocks highlight properly
#    - Links work
#    - Navigation shows page

# 4. Validate links
npx mintlify broken-links

# 5. Check docs.json
npx mintlify check
```

---

## 13. Resources

- **Mintlify Docs**: https://mintlify.com/docs
- **docs.json Schema**: https://mintlify.com/docs.json
- **MDX Documentation**: https://mdxjs.com/
- **Core Style Guide**: [core_style_guide.md](core_style_guide.md)

---

## 14. Quick Reference

### Mintlify File Structure
```
docs/
├── api/
│   ├── messages.mdx
│   └── streaming.mdx
├── guides/
│   └── quickstart.mdx
├── images/
│   └── diagram.png
└── docs.json
```

### Valid MDX Page Template
```mdx
---
title: "Descriptive Page Title"
description: "Concise summary for SEO and navigation"
---

Opening paragraph explaining what this page covers.

## Main Section (H2)

Content here.

### Subsection (H3)

More content.

## Code Example

```python
# Complete, runnable example
import anthropic
client = anthropic.Anthropic()
```

## Related Topics

- [Topic 1](../path/to/topic1)
- [Topic 2](./topic2)
- [Topic 3](../path/to/topic3)
```

---

**Version 1.0** - Based on analysis of Mintlify documentation and Claude docs implementation
**Last Updated**: October 31, 2025
