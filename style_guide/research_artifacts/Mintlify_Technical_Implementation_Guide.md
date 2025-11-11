# Mintlify Technical Implementation Guide
## Platform-Specific Standards for Claude Docs

---

## Overview

This guide provides detailed technical standards for implementing documentation on the Mintlify platform. It covers frontmatter schemas, component specifications, navigation configuration, and platform optimization.

**Audience**: Technical writers and engineers contributing to Claude Docs
**Prerequisites**: Basic understanding of MDX and YAML

---

## Table of Contents

1. [File Format Requirements](#file-format-requirements)
2. [Frontmatter Schema](#frontmatter-schema)
3. [Component Reference](#component-reference)
4. [Navigation Configuration](#navigation-configuration)
5. [Code Block Standards](#code-block-standards)
6. [Image and Media](#image-and-media)
7. [SEO Optimization](#seo-optimization)
8. [Performance](#performance)
9. [Troubleshooting](#troubleshooting)

---

## File Format Requirements

### MDX vs Markdown

**Use MDX (.mdx)** for:
- Pages using Mintlify components
- Interactive content
- Pages with custom layouts
- Most documentation pages

**Use Markdown (.md)** for:
- Simple, text-only pages
- Generated content
- Legacy content (will work but limited)

### File Naming

**Rules**:
- Use kebab-case: `getting-started.mdx` not `Getting_Started.mdx`
- No spaces or special characters
- Descriptive names matching content
- Avoid version numbers in filenames

**Examples:**
- ✅ `quickstart.mdx`
- ✅ `api-reference.mdx`
- ✅ `tool-use-guide.mdx`
- ❌ `Quickstart.mdx`
- ❌ `API Reference.mdx`
- ❌ `guide_v2.mdx`

### Directory Structure

```
docs/
â"œâ"€â"€ en/
â"‚   â"œâ"€â"€ docs/
â"‚   â"‚   â"œâ"€â"€ intro.mdx
â"‚   â"‚   â"œâ"€â"€ quickstart.mdx
â"‚   â"‚   â""â"€â"€ guides/
â"‚   â"‚       â"œâ"€â"€ streaming.mdx
â"‚   â"‚       â""â"€â"€ tool-use.mdx
â"‚   â"œâ"€â"€ api/
â"‚   â"‚   â"œâ"€â"€ messages.mdx
â"‚   â"‚   â""â"€â"€ streaming.mdx
â"‚   â""â"€â"€ assets/
â"‚       â"œâ"€â"€ images/
â"‚       â""â"€â"€ videos/
â"œâ"€â"€ mint.json
â""â"€â"€ README.md
```

---

## Frontmatter Schema

### Required Fields

Every MDX page **must** include:

```yaml
---
title: "Page Title"
description: "SEO-optimized description 150-160 characters."
---
```

### Field Specifications

#### `title` (required)

**Type**: String
**Length**: 50-60 characters optimal, 70 max
**Rules**:
- Unique across entire documentation site
- Matches H1 heading in content
- Use title case for proper nouns only
- No punctuation at end

**Examples:**
```yaml
✅ title: "Getting Started with Claude"
✅ title: "Messages API Reference"
❌ title: "Getting started with claude"  # Improper capitalization
❌ title: "Getting Started with Claude!" # No punctuation
❌ title: "This Is An Extremely Long Title That Exceeds The Recommended Character Limit"  # Too long
```

#### `description` (required)

**Type**: String
**Length**: 150-160 characters (optimal for SERP display)
**Rules**:
- Front-load important keywords
- Complete sentence with period
- Natural language, not keyword stuffing
- Include primary keyword and value proposition

**Examples:**
```yaml
✅ description: "Learn to implement streaming responses with Claude API for real-time output display and improved user experience. Complete guide with code examples."

❌ description: "Streaming guide"  # Too short, no value

❌ description: "This is a super long description that goes on and on providing way too much detail and definitely exceeds the recommended 160 character limit for search engine display which will cause truncation in search results making it less effective."  # Too long
```

### Optional Fields

#### `sidebarTitle`

**Type**: String
**Purpose**: Shorter title for navigation sidebar
**Use when**: Page title is too long for sidebar

```yaml
---
title: "Complete Guide to Building Production-Ready Agents"
sidebarTitle: "Building Agents"
description: "..."
---
```

#### `icon`

**Type**: String
**Purpose**: Icon to display in navigation
**Values**: Font Awesome or Lucide icon names

```yaml
---
title: "Quickstart Guide"
description: "..."
icon: "rocket"
---
```

**Available icon sources:**
- Font Awesome (https://fontawesome.com/icons)
- Lucide (https://lucide.dev/icons)

#### `mode`

**Type**: String
**Purpose**: Control page width
**Values**: `"wide"` (full width) or omit for standard

```yaml
---
title: "API Reference"
description: "..."
mode: "wide"  # Use full width for tables/examples
---
```

### Complete Example

```yaml
---
title: "Streaming Responses Guide"
sidebarTitle: "Streaming"
description: "Implement streaming responses with Claude API for real-time output. Complete guide with Python and TypeScript examples and best practices."
icon: "water"
---
```

### Validation Rules

Frontmatter will be validated for:
- ✅ Both `title` and `description` present
- ✅ Title length 50-70 characters
- ✅ Description length 150-160 characters
- ✅ Description ends with period
- ✅ No HTML in frontmatter
- ✅ Title is unique (no duplicates)

---

## Component Reference

### Card & CardGroup

**Purpose**: Create clickable navigation cards or feature highlights

**Syntax:**
```mdx
<CardGroup cols={2}>
  <Card 
    title="Card Title" 
    icon="icon-name" 
    href="/relative/path"
  >
    Brief description of destination
  </Card>
  
  <Card title="Second Card" icon="code" href="/path">
    Another description
  </Card>
</CardGroup>
```

**Props:**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `title` | string | Yes | Card heading (30 chars max) |
| `icon` | string | No | Icon name (Font Awesome/Lucide) |
| `href` | string | Yes* | Link destination (relative path) |
| `children` | ReactNode | Yes | Card description (100 chars max) |

*Required if card is clickable

**CardGroup Props:**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `cols` | number | 2 | Number of columns (2 or 3 recommended) |

**Best Practices:**
- Use `cols={2}` for feature highlights
- Use `cols={3}` for navigation grids
- Keep descriptions under 100 characters
- Always use relative paths for `href`
- Provide icon for visual scanning

**Example Use Cases:**
```mdx
<!-- Navigation hub -->
<CardGroup cols={3}>
  <Card title="Quickstart" icon="rocket" href="/en/docs/quickstart">
    Get started in 5 minutes
  </Card>
  <Card title="API Reference" icon="code" href="/en/api/messages">
    Complete endpoint docs
  </Card>
  <Card title="Examples" icon="flask" href="/en/examples">
    Working code samples
  </Card>
</CardGroup>

<!-- Feature highlights (non-clickable) -->
<CardGroup cols={2}>
  <Card title="Fast Performance" icon="bolt">
    Responses in under 3 seconds
  </Card>
  <Card title="Cost Effective" icon="dollar">
    Save 90% with caching
  </Card>
</CardGroup>
```

### Tabs & Tab

**Purpose**: Show multiple alternatives (languages, platforms, approaches)

**Syntax:**
```mdx
<Tabs>
  <Tab title="Python">
    Content for Python
  </Tab>
  
  <Tab title="TypeScript">
    Content for TypeScript
  </Tab>
  
  <Tab title="cURL">
    Content for cURL
  </Tab>
</Tabs>
```

**Props:**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `title` | string | Yes | Tab label |
| `children` | ReactNode | Yes | Tab content |

**Best Practices:**
- Primary use: Multi-language code examples
- Standard order: Python, TypeScript, cURL, Java, Go, Ruby, PHP, C#
- Keep tab count under 5 when possible
- Ensure content across tabs is parallel in structure
- Use CodeGroup for code-only tabs

**Example:**
```mdx
<Tabs>
  <Tab title="Python">
    ```python
    import anthropic
    client = anthropic.Anthropic()
    ```
  </Tab>
  
  <Tab title="TypeScript">
    ```typescript
    import Anthropic from '@anthropic-ai/sdk';
    const client = new Anthropic();
    ```
  </Tab>
</Tabs>
```

### CodeGroup

**Purpose**: Cleaner alternative to Tabs specifically for code examples

**Syntax:**
````mdx
<CodeGroup>
```python
import anthropic
client = anthropic.Anthropic()
```

```typescript
import Anthropic from '@anthropic-ai/sdk';
const client = new Anthropic();
```

```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY"
```
</CodeGroup>
````

**Best Practices:**
- Preferred over Tabs for code-only content
- Automatically generates language labels
- Must specify language on each code block
- Order: Python, TypeScript, JavaScript, cURL, then others alphabetically

### Steps & Step

**Purpose**: Display sequential procedures

**Syntax:**
```mdx
<Steps>
  <Step title="Install Dependencies">
    Run `npm install @anthropic-ai/sdk`
  </Step>
  
  <Step title="Configure API Key">
    Set your `ANTHROPIC_API_KEY` environment variable
  </Step>
  
  <Step title="Make First Request">
    Create a message using the code below
  </Step>
</Steps>
```

**Props:**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `title` | string | Yes | Step heading |
| `icon` | string | No | Custom icon (default: numbered) |
| `children` | ReactNode | Yes | Step instructions |

**Best Practices:**
- Use for 3-7 steps (under 3: use list; over 7: break into sections)
- Each step should be actionable
- Keep step titles short (under 50 characters)
- Include what users should expect after each step
- Use parallel structure across steps

**When to Use:**
- ✅ Setup instructions
- ✅ Configuration procedures
- ✅ Multi-step workflows
- ❌ Conceptual explanations (use regular text)
- ❌ Single actions (use regular text)

### Callout Components

**Purpose**: Highlight important information

**Available Types:**

```mdx
<Info>
Helpful context or additional information
</Info>

<Warning>
Important cautions or things to watch out for
</Warning>

<Tip>
Best practices or optimization suggestions
</Tip>

<Note>
Additional clarifications or side notes
</Note>
```

**Usage Guidelines:**

| Component | Icon | When to Use |
|-----------|------|-------------|
| `<Info>` | ℹ️ | Helpful context, clarifications, FYI items |
| `<Warning>` | ⚠️ | Breaking changes, security concerns, gotchas |
| `<Tip>` | 💡 | Best practices, optimizations, pro tips |
| `<Note>` | 📝 | Additional details, clarifications, asides |

**Best Practices:**
- Use sparingly (max 2-3 per page)
- Keep content concise (under 100 words)
- Don't nest components
- Place close to relevant content
- Don't use for content that belongs in main text

**Examples:**
```mdx
<Warning>
Store your API key securely. Never commit it to version control or expose it in client-side code.
</Warning>

<Tip>
Use prompt caching to reduce latency by up to 85% on repeated queries.
</Tip>

<Info>
Extended context (200K+ tokens) uses different pricing. See our [pricing page](/en/docs/pricing).
</Info>
```

### Accordion & AccordionGroup

**Purpose**: Collapsible content for FAQs or optional details

**Syntax:**
```mdx
<AccordionGroup>
  <Accordion title="Question or Section Title">
    Content that can be expanded/collapsed
  </Accordion>
  
  <Accordion title="Another Question">
    More collapsible content
  </Accordion>
</AccordionGroup>
```

**Props:**

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `title` | string | Yes | Accordion heading (50 chars max) |
| `icon` | string | No | Custom icon |
| `defaultOpen` | boolean | No | Whether open by default |

**Best Practices:**
- Ideal for FAQs and troubleshooting
- Use for optional/advanced content
- Keep titles as questions when possible
- Don't nest accordions
- Limit to 5-10 per page

**Example:**
```mdx
<AccordionGroup>
  <Accordion title="How do I get an API key?">
    Generate an API key from your [account settings](https://console.anthropic.com/settings/keys).
  </Accordion>
  
  <Accordion title="What are rate limits?">
    Rate limits vary by usage tier. See our [rate limits guide](/en/docs/rate-limits) for details.
  </Accordion>
</AccordionGroup>
```

### Component Validation

Components will be validated for:
- ✅ Proper prop types
- ✅ Required props present
- ✅ Correct nesting structure
- ✅ Relative paths in hrefs
- ✅ Valid icon names
- ✅ No unsupported props

---

## Navigation Configuration

### mint.json Structure

The `mint.json` file controls site-wide navigation and configuration.

**Location**: Project root (`/mint.json`)

### Basic Structure

```json
{
  "name": "Claude Docs",
  "logo": {
    "light": "/logo/light.svg",
    "dark": "/logo/dark.svg"
  },
  "favicon": "/favicon.svg",
  "colors": {
    "primary": "#0D9373",
    "light": "#07C983",
    "dark": "#0D9373"
  },
  "navigation": [
    {
      "group": "Getting Started",
      "pages": [
        "docs/intro",
        "docs/quickstart"
      ]
    }
  ]
}
```

### Navigation Array

**Group Object:**
```json
{
  "group": "Group Name",
  "pages": [
    "path/to/file",
    "path/to/another"
  ]
}
```

**Rules:**
- Groups organize related pages
- Pages reference file paths without extension
- Paths relative to project root
- Maximum 3 levels of nesting recommended

### Advanced Navigation

**Nested Groups:**
```json
{
  "group": "API Reference",
  "pages": [
    "api/overview",
    {
      "group": "Endpoints",
      "pages": [
        "api/messages",
        "api/streaming",
        "api/batches"
      ]
    }
  ]
}
```

**Icons in Navigation:**
```json
{
  "group": "Getting Started",
  "icon": "rocket",
  "pages": ["docs/intro"]
}
```

### Anchors (Always Visible Links)

```json
{
  "anchors": [
    {
      "name": "API Reference",
      "icon": "code",
      "url": "api"
    },
    {
      "name": "Discord",
      "icon": "discord",
      "url": "https://discord.gg/anthropic"
    }
  ]
}
```

**Anchor Rules:**
- Display at top of navigation
- Maximum 4-5 anchors
- Can link externally (full URL) or internally (path)

### Navigation Best Practices

1. **Logical Grouping**: Organize by user intent, not internal structure
2. **Progressive Disclosure**: Beginner → Intermediate → Advanced
3. **Consistent Naming**: Use parallel structure for similar items
4. **Depth Limit**: Maximum 3 levels (Group → Subgroup → Page)
5. **Page Limit**: 5-10 pages per group ideal

**Example Structure:**
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
        {
          "group": "Features",
          "pages": [
            "docs/streaming",
            "docs/tool-use",
            "docs/vision"
          ]
        }
      ]
    },
    {
      "group": "API Reference",
      "pages": [
        "api/overview",
        "api/messages",
        "api/streaming"
      ]
    }
  ]
}
```

---

## Code Block Standards

### Language Specification

**Always specify language** on code blocks:

````markdown
```python
import anthropic
```

```typescript
import Anthropic from '@anthropic-ai/sdk';
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

### Supported Languages

**Common:**
- `python`
- `typescript` / `javascript` / `tsx` / `jsx`
- `bash` / `sh` / `shell`
- `json`
- `yaml`

**Additional:**
- `java`
- `go`
- `ruby`
- `php`
- `csharp` / `cs`
- `sql`
- `html`
- `css`
- `markdown`

### Advanced Features

**Filename Display:**
````markdown
```python title="quickstart.py"
import anthropic
```
````

**Line Highlighting:**
````markdown
```python {2-4}
import anthropic

client = anthropic.Anthropic()  # Highlighted
message = client.messages.create()  # Highlighted
```
````

**Copy Button:**
Automatically added to all code blocks (no configuration needed)

### Code Block Best Practices

1. **Always Specify Language**: Never use ``` without language
2. **Test All Code**: Ensure examples work as written
3. **Include Imports**: Show all necessary imports
4. **Add Comments**: Explain non-obvious code
5. **Error Handling**: Show production-ready patterns
6. **Keep Focused**: One concept per example

---

## Image and Media

### Image Requirements

**File Formats:**
- PNG (preferred for screenshots)
- JPG/JPEG (photos)
- SVG (icons, diagrams)
- GIF (animations, under 5MB)

**File Size:**
- Maximum: 5MB per image
- Recommended: Under 500KB
- Optimize before upload

**Dimensions:**
- Width: 1200px maximum
- Maintain aspect ratio
- Responsive by default

### Image Syntax

**Standard:**
```markdown
![Descriptive alt text](./path/to/image.png)
```

**With Caption:**
```mdx
<Frame caption="Caption text appears below image">
  ![Alt text](./image.png)
</Frame>
```

### Alt Text Requirements

**Rules:**
- Required on ALL images
- Describe image content
- Include text visible in image
- 125 characters maximum
- No "Image of" or "Picture of"

**Examples:**
```markdown
✅ ![Claude Code terminal showing successful API call with JSON response](./terminal.png)

❌ ![](./terminal.png)  # Missing alt text

❌ ![Image of terminal](./terminal.png)  # Don't start with "Image of"

❌ ![This is an image showing the Claude Code terminal interface with a successful API call displaying a JSON response with the message content and metadata](./terminal.png)  # Too long
```

### Video Embedding

**YouTube/Vimeo:**
```mdx
<Frame>
  <iframe
    width="560"
    height="315"
    src="https://www.youtube.com/embed/VIDEO_ID"
    title="Video Title"
    frameborder="0"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowfullscreen
  ></iframe>
</Frame>
```

**Self-Hosted:**
```mdx
<video
  controls
  src="/path/to/video.mp4"
  title="Video Title"
>
  Your browser does not support the video tag.
</video>
```

### Asset Organization

```
assets/
â"œâ"€â"€ images/
â"‚   â"œâ"€â"€ screenshots/
â"‚   â"‚   â"œâ"€â"€ console-api-keys.png
â"‚   â"‚   â""â"€â"€ vscode-extension.png
â"‚   â"œâ"€â"€ diagrams/
â"‚   â"‚   â"œâ"€â"€ architecture.svg
â"‚   â"‚   â""â"€â"€ workflow.svg
â"‚   â""â"€â"€ icons/
â"‚       â""â"€â"€ logo.svg
â""â"€â"€ videos/
    â""â"€â"€ demo.mp4
```

---

## SEO Optimization

### Page Titles

**Format:** Primary Keyword | Secondary Keyword | Brand (optional)

**Examples:**
```yaml
✅ title: "Messages API Reference | Claude Documentation"
✅ title: "Streaming Responses Guide"
❌ title: "Documentation Page"
```

**Rules:**
- 50-60 characters optimal
- Front-load important keywords
- Include brand for competitive terms
- Unique across site

### Meta Descriptions

**Format:** Value proposition + Keywords + Call to action

**Examples:**
```yaml
✅ description: "Learn to implement streaming responses with Claude API for real-time output display. Complete guide with Python and TypeScript code examples."

❌ description: "This page covers streaming."
```

**Rules:**
- 150-160 characters
- Include primary keyword
- Natural language
- End with period
- Include benefit/value

### URL Structure

**Rules:**
- Use kebab-case
- Short and descriptive
- No dates or versions
- Stable over time
- Logical hierarchy

**Examples:**
```
✅ /en/docs/streaming-responses
✅ /en/api/messages
✅ /en/docs/claude-code/quickstart

❌ /en/docs/2025/streaming-guide
❌ /en/docs/page-123
❌ /en/docs/how_to_stream_responses_v2
```

### Heading Optimization

**Use keywords naturally in headings:**
```markdown
# Streaming Responses with Claude API

## How to Implement Streaming

## Streaming Best Practices
```

**Avoid keyword stuffing:**
```markdown
❌ # Streaming Responses Streaming Guide Streaming API Streaming Claude
```

### Internal Linking

**Benefits:**
- Improves navigation
- Distributes page authority
- Increases time on site
- Helps crawlers discover content

**Best Practices:**
- Link from high-traffic pages to new content
- Use descriptive anchor text
- Link to relevant, related pages
- Add "Related Pages" sections
- Create topic clusters

---

## Performance

### Page Load Optimization

**Image Optimization:**
- Compress before upload
- Use appropriate formats (WebP when possible)
- Lazy load images below fold
- Serve scaled images

**Code Block Optimization:**
- Limit code block size (under 100 lines per block)
- Use CodeGroup for cleaner presentation
- Consider line ranges for long examples

**Component Usage:**
- Don't overuse heavy components
- Limit Accordions to 10 per page
- Avoid nesting complex components

### Build Performance

**Reduce Build Time:**
- Keep total pages under 1000 if possible
- Optimize image assets
- Minimize external dependencies
- Use incremental builds

### Monitoring

**Track:**
- Page load time (target: under 3s)
- Time to interactive (target: under 5s)
- Lighthouse scores (target: 90+)
- Core Web Vitals

---

## Troubleshooting

### Common Issues

#### Build Failures

**Symptom:** Build fails with MDX parse error

**Causes & Solutions:**
```markdown
❌ Unclosed components:
<Card title="Test">

✅ Properly closed:
<Card title="Test">
  Content
</Card>

❌ Invalid frontmatter:
---
title: Test
description: Missing quotes for multi-word value
---

✅ Quoted values:
---
title: "Test"
description: "Properly quoted description"
---
```

#### Navigation Not Showing

**Symptom:** Page exists but doesn't appear in navigation

**Solution:**
1. Check `mint.json` includes page path
2. Verify path matches file location
3. Confirm no typos in path
4. Check file has required frontmatter

#### Components Not Rendering

**Symptom:** Component shows as text instead of rendering

**Causes & Solutions:**
```markdown
❌ Using markdown syntax:
```<Card>```

✅ Use JSX syntax:
<Card title="Test">
  Content
</Card>

❌ Missing closing tag:
<CardGroup>
  <Card title="Test">

✅ Proper nesting:
<CardGroup>
  <Card title="Test">
    Content
  </Card>
</CardGroup>
```

#### Images Not Displaying

**Symptom:** Broken image icon

**Causes & Solutions:**
1. Check file path is correct
2. Verify image file exists
3. Confirm image is under 5MB
4. Check file extension matches actual format
5. Ensure path is relative to project root

### Validation Tools

**Pre-Deployment Checks:**
1. Run `mintlify dev` to test locally
2. Check for TypeScript/MDX errors
3. Verify all links work
4. Test navigation structure
5. Validate frontmatter
6. Check image loading
7. Review responsive display

---

## Validation Checklist

Before publishing, verify:

**Content:**
- [ ] Frontmatter complete (title, description)
- [ ] One H1 per page
- [ ] Proper heading hierarchy
- [ ] Alt text on all images
- [ ] Language tags on code blocks
- [ ] All links work (relative for internal)

**Mintlify:**
- [ ] File named with kebab-case
- [ ] Components properly closed
- [ ] CodeGroup for multi-language examples
- [ ] Steps for sequential procedures
- [ ] Callouts used appropriately

**SEO:**
- [ ] Title 50-60 characters
- [ ] Description 150-160 characters
- [ ] Keywords in title and description
- [ ] URL follows structure conventions
- [ ] Internal links added

**Performance:**
- [ ] Images optimized (<500KB)
- [ ] Code blocks under 100 lines
- [ ] No more than 10 accordions
- [ ] Page loads in under 3 seconds

---

## Resources

**Official Docs:**
- Mintlify Documentation: https://mintlify.com/docs
- Component Showcase: https://mintlify.com/docs/components
- MDX Documentation: https://mdxjs.com

**Internal Resources:**
- Core Style Guide: `Claude_Docs_Style_Guide.md`
- Template Library: `Claude_Docs_Template_Library.md`
- Quick Reference: `Claude_Docs_Quick_Reference.md`

**Tools:**
- Mintlify CLI: `npm install -g mintlify`
- Dev Server: `mintlify dev`
- Image Optimizer: https://tinypng.com
- YAML Validator: https://www.yamllint.com

---

*This guide is maintained by the Technical Writing Team. Last updated: October 30, 2025*
