# Claude Documentation Quick Reference

**Print this and keep it at your desk** | Version 1.0 | [Full Style Guide](core_style_guide.md)

---

## 📏 The Golden Rules

### #1: Findability > New Content
**90% of "missing" docs aren't missing** - users just can't find them. Before writing new content, improve discoverability of existing content.

### #2: Every Page Needs These 5 Things
1. **Frontmatter** (title + description)
2. **Prerequisites** (for how-to/tutorials)
3. **Code examples** (for technical pages)
4. **100+ words minimum**
5. **3-5 related topic links**

### #3: Make It Scannable
- Max **4 lines** per paragraph
- **Descriptive headings** (not "Introduction" or "Overview")
- **Bulleted lists** for sequences
- **Code blocks** with language tags

---

## ✅ Quick Quality Checklist

Before publishing ANY page:

```
[ ] Frontmatter has title and description
[ ] At least 100 words (150+ conceptual, 200+ how-to)
[ ] Has code example (if technical)
[ ] Has prerequisites section (if how-to/tutorial)
[ ] Has 3-5 related topics links
[ ] No paragraphs >4 lines
[ ] All code blocks have language tags
[ ] All links work
```

---

## 📝 Page Structure Template

```markdown
---
title: "Clear, Descriptive Title"
description: "Concise 1-2 sentence summary"
---

Opening paragraph - what this page covers.

## Prerequisites

- [What users need to know first]
- [Links to prerequisite docs]

## [Main Content Heading]

[Content here...]

## Example: [Specific Use Case]

```language
[Complete, runnable code example]
```

## Related Topics

- [Topic 1](link) - Brief description
- [Topic 2](link) - Brief description
- [Topic 3](link) - Brief description
```

---

## ❌ Words to Avoid

| Don't Write | Write Instead |
|------------|---------------|
| simply, just, easily | [omit] |
| utilize, leverage | use |
| in order to | to |
| please note that | [state directly] |

---

## 📐 Word Count Requirements

| Page Type | Minimum |
|-----------|---------|
| API Reference | 100 words |
| Conceptual | 150 words |
| How-To Guide | 200 words |
| Tutorial | 300 words |

**Red flag**: Page < 100 words = incomplete

---

## 🎯 When to Use Each Template

| If you're... | Use Template |
|-------------|--------------|
| Explaining what/why | [Conceptual](templates/conceptual.mdx) |
| Showing how to do a task | [How-To Guide](templates/how_to_guide.mdx) |
| Documenting an endpoint | [API Reference](templates/api_reference.mdx) |
| Teaching step-by-step | [Tutorial](templates/tutorial.mdx) |
| Helping fix problems | [Troubleshooting](templates/troubleshooting.mdx) |

---

## 🔍 Findability Checklist

To make content discoverable:

```
[ ] Title contains searchable keywords
[ ] First paragraph states what page covers
[ ] Headings are descriptive (not "Overview")
[ ] Cross-linked from 3+ related pages
[ ] Added to navigation menu
[ ] Includes terms users might search for
```

---

## 💻 Code Example Requirements

Every code block MUST have:
- **Language tag**: ` ```python `
- **Complete code**: Can run as-is
- **Includes imports**: All necessary imports shown
- **Shows output**: Request + response where applicable

**Example**:
```python
# ✅ GOOD
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.content)
```

```
# ❌ BAD - No language tag, incomplete
client.messages.create(
    model=...
```

---

## 📋 Prerequisites Format

```markdown
## Prerequisites

Before [task name], you should:
- [Prerequisite 1 with link]
- [Prerequisite 2]

You'll need:
- [Required tool/account]
- [Another requirement]
```

---

## 🔗 Cross-Referencing Format

```markdown
## Related Topics

- [Specific Topic](link) - What users will find there
- [Another Topic](link) - Brief description
- [Third Topic](link) - Why it's related
```

**Minimum**: 3 related links
**Ideal**: 5 related links

---

## 📊 Common Issues & Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| User can't find documented feature | "This isn't documented" | Add cross-links, improve title, add to nav |
| Page feels incomplete | Very short page | Add examples, expand to 100+ words |
| User gets stuck | No prerequisites | Add "Prerequisites" section |
| Hard to understand | Long paragraphs | Break into <4 line chunks |
| Can't use it | No code example | Add complete, runnable example |

---

## ✍️ Voice & Tone

**Do**:
- Use "you" (second person)
- Use active voice
- Be direct and clear
- Front-load important info

**Don't**:
- Use passive voice
- Be vague or indirect
- Use jargon without definition
- Bury the lede

**Examples**:

✅ "Configure your API key before making requests"
❌ "API keys should be configured before requests are made"

✅ "Send a POST request to `/messages`"
❌ "A POST request can be sent to the messages endpoint"

---

## 🏃 Quick Decisions

### Should I create a new page?
1. Does this topic already exist? (Search first!)
2. If yes → improve findability of existing page
3. If no → create using appropriate template

### What template should I use?
- **Explaining a concept?** → Conceptual
- **Teaching a task?** → How-To Guide
- **Step-by-step learning?** → Tutorial
- **Documenting API?** → API Reference
- **Helping debug?** → Troubleshooting

### Is this page ready to publish?
Run through the checklist:
- [ ] 5 required elements present
- [ ] Meets word count minimum
- [ ] Code examples work
- [ ] Links all work
- [ ] Passes quality checklist

---

## 🎯 Priority Fixes

When improving existing docs, prioritize in this order:

1. **Findability** - Add cross-links, improve titles
2. **Prerequisites** - Add to how-to/tutorials
3. **Code examples** - Add to technical pages
4. **Word count** - Expand short pages
5. **Clarity** - Simplify language, shorten paragraphs

---

## 📚 Full Resources

- **[Full Style Guide](core_style_guide.md)** - Complete documentation standards
- **[Mintlify Standards](mintlify_standards.md)** - Platform-specific technical details
- **[Templates](templates/)** - Ready-to-use page templates
- **[Validation Rules](validation_rules.yaml)** - Automated quality checks

---

## 🚨 Emergency Reference

### "User says feature X isn't documented"
1. ✅ Search: Does X exist in docs?
2. ✅ If yes (90% of time): Improve findability
3. ✅ If no: Use template to create

### "My page feels incomplete"
1. ✅ Check word count (100+ minimum)
2. ✅ Add code example if technical
3. ✅ Add prerequisites if how-to
4. ✅ Add 3-5 related links

### "How do I know if it's good enough?"
1. ✅ Run quality checklist
2. ✅ Have peer review
3. ✅ Test code examples
4. ✅ Validate with tool (when available)

---

**Print this page and keep it visible while writing docs!**

*Version 1.0 - Based on analysis of 142 GitHub issues - [Full Guide](core_style_guide.md)*
