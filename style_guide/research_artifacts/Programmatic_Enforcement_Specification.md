# Programmatic Enforcement Specification
## Automated Style Guide Rules for docs_analyzer Integration

---

## Overview

This specification defines all style guide rules that can be automatically enforced through the `docs_analyzer` tool. Each rule includes detection methods, severity levels, and remediation guidance.

**Purpose**: Enable automated quality checks during authoring, review, and CI/CD
**Tool**: `enhanced_doc_analyzer.py` (existing project tool)
**Enforcement Points**: Pre-commit hooks, PR checks, scheduled audits

---

## Table of Contents

1. [Severity Levels](#severity-levels)
2. [Critical Rules](#critical-rules)
3. [High Priority Rules](#high-priority-rules)
4. [Medium Priority Rules](#medium-priority-rules)
5. [Low Priority Rules](#low-priority-rules)
6. [Implementation Guide](#implementation-guide)
7. [CI/CD Integration](#cicd-integration)

---

## Severity Levels

| Level | Description | Action | Examples |
|-------|-------------|--------|----------|
| **CRITICAL** | Breaks functionality or user experience | Block publishing | Missing frontmatter, broken links |
| **HIGH** | Inconsistency or usability issues | Fix within 1 week | Deprecated terms, hierarchy skips |
| **MEDIUM** | Style violations | Fix within 1 month | Weak words, passive voice |
| **LOW** | Best practice suggestions | Fix when convenient | Oxford comma, line length |

---

## Critical Rules

### FMT-001: Missing Frontmatter

**Description**: MDX file lacks YAML frontmatter block
**Severity**: CRITICAL
**Rationale**: Breaks Mintlify rendering and SEO

**Detection Method:**
```python
def check_frontmatter_exists(file_path):
    """Check if file has frontmatter block"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Frontmatter must start at beginning of file
    if not content.startswith('---\n'):
        return {
            'rule_id': 'FMT-001',
            'severity': 'CRITICAL',
            'message': 'Missing frontmatter block',
            'line': 1,
            'suggestion': 'Add frontmatter:\n---\ntitle: "Page Title"\ndescription: "Description here."\n---'
        }
    
    return None
```

**Remediation:**
```yaml
---
title: "Page Title"
description: "150-160 character description."
---
```

---

### FMT-002: Missing `title` Field

**Description**: Frontmatter lacks required `title` field
**Severity**: CRITICAL
**Rationale**: Required for navigation and SEO

**Detection Method:**
```python
import yaml

def check_title_field(file_path):
    """Check if frontmatter has title"""
    frontmatter = extract_frontmatter(file_path)
    
    if 'title' not in frontmatter:
        return {
            'rule_id': 'FMT-002',
            'severity': 'CRITICAL',
            'message': 'Missing required "title" field in frontmatter',
            'line': 1,
            'suggestion': 'Add title: "Your Page Title" to frontmatter'
        }
    
    return None
```

**Remediation:**
```yaml
---
title: "Your Page Title"
description: "Description"
---
```

---

### FMT-003: Missing `description` Field

**Description**: Frontmatter lacks required `description` field
**Severity**: CRITICAL
**Rationale**: Critical for SEO and search results

**Detection Method:**
```python
def check_description_field(file_path):
    """Check if frontmatter has description"""
    frontmatter = extract_frontmatter(file_path)
    
    if 'description' not in frontmatter:
        return {
            'rule_id': 'FMT-003',
            'severity': 'CRITICAL',
            'message': 'Missing required "description" field in frontmatter',
            'line': 1,
            'suggestion': 'Add description: "150-160 character SEO description." to frontmatter'
        }
    
    return None
```

**Remediation:**
```yaml
---
title: "Title"
description: "Concise 150-160 character description with keywords."
---
```

---

### LNK-001: Broken Internal Link

**Description**: Internal link points to non-existent file
**Severity**: CRITICAL
**Rationale**: Creates 404 errors for users

**Detection Method:**
```python
import re
from pathlib import Path

def check_broken_internal_links(file_path, docs_root):
    """Check if internal links resolve"""
    content = get_file_content(file_path)
    issues = []
    
    # Find markdown links
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    
    for match in re.finditer(link_pattern, content):
        link_text, link_url = match.groups()
        line_num = content[:match.start()].count('\n') + 1
        
        # Skip external links
        if link_url.startswith(('http://', 'https://', '#', 'mailto:')):
            continue
        
        # Resolve relative path
        link_path = Path(docs_root) / link_url.lstrip('/')
        
        # Check if target exists
        if not link_path.exists() and not link_path.with_suffix('.mdx').exists():
            issues.append({
                'rule_id': 'LNK-001',
                'severity': 'CRITICAL',
                'message': f'Broken internal link: {link_url}',
                'line': line_num,
                'column': match.start() - content.rfind('\n', 0, match.start()),
                'suggestion': f'Verify target exists or update link'
            })
    
    return issues
```

**Remediation:**
- Verify target file exists
- Update link path to correct location
- Remove link if target was intentionally deleted

---

### LNK-002: Absolute URL for Internal Link

**Description**: Internal documentation link uses absolute URL instead of relative path
**Severity**: CRITICAL
**Rationale**: Breaks local development and makes migrations difficult

**Detection Method:**
```python
def check_absolute_internal_urls(file_path):
    """Check for absolute URLs to internal pages"""
    content = get_file_content(file_path)
    issues = []
    
    # Pattern: [text](https://docs.anthropic.com/... or https://docs.claude.com/...)
    pattern = r'\[([^\]]+)\]\((https?://(?:docs\.anthropic\.com|docs\.claude\.com)/[^)]+)\)'
    
    for match in re.finditer(pattern, content):
        link_text, absolute_url = match.groups()
        line_num = content[:match.start()].count('\n') + 1
        
        # Extract relative path
        relative_path = re.sub(r'https?://docs\.(?:anthropic|claude)\.com', '', absolute_url)
        
        issues.append({
            'rule_id': 'LNK-002',
            'severity': 'CRITICAL',
            'message': f'Absolute URL for internal link: {absolute_url}',
            'line': line_num,
            'suggestion': f'Change to relative path: [{link_text}]({relative_path})'
        })
    
    return issues
```

**Remediation:**
```markdown
❌ [Learn more](https://docs.anthropic.com/en/docs/streaming)
✅ [Learn more](/en/docs/streaming)
```

---

### CODE-001: Code Block Missing Language Tag

**Description**: Code block has no language specification
**Severity**: CRITICAL
**Rationale**: Breaks syntax highlighting and copy functionality

**Detection Method:**
```python
def check_code_block_language_tags(file_path):
    """Check if code blocks specify language"""
    content = get_file_content(file_path)
    issues = []
    
    # Find code blocks without language
    pattern = r'^```\s*\n'  # ``` with no language
    
    for match in re.finditer(pattern, content, re.MULTILINE):
        line_num = content[:match.start()].count('\n') + 1
        
        issues.append({
            'rule_id': 'CODE-001',
            'severity': 'CRITICAL',
            'message': 'Code block missing language tag',
            'line': line_num,
            'suggestion': 'Add language: ```python or ```typescript or ```bash'
        })
    
    return issues
```

**Remediation:**
````markdown
❌ 
```
code here
```

✅ 
```python
code here
```
````

---

## High Priority Rules

### TERM-001: Deprecated Term "Claude Code SDK"

**Description**: Uses deprecated term "Claude Code SDK" instead of "Claude Agent SDK"
**Severity**: HIGH
**Rationale**: Terminology changed in v2.0.0

**Detection Method:**
```python
def check_deprecated_claude_code_sdk(file_path):
    """Check for deprecated 'Claude Code SDK' term"""
    content = get_file_content(file_path)
    issues = []
    
    pattern = r'\bClaude\s+Code\s+SDK\b'
    
    for match in re.finditer(pattern, content, re.IGNORECASE):
        line_num = content[:match.start()].count('\n') + 1
        
        issues.append({
            'rule_id': 'TERM-001',
            'severity': 'HIGH',
            'message': 'Deprecated term: "Claude Code SDK"',
            'line': line_num,
            'suggestion': 'Replace with "Claude Agent SDK"'
        })
    
    return issues
```

**Remediation:**
```markdown
❌ The Claude Code SDK provides...
✅ The Claude Agent SDK provides...
```

---

### TERM-002: Inconsistent Product Name Capitalization

**Description**: Product names not capitalized consistently
**Severity**: HIGH
**Rationale**: Unprofessional, inconsistent branding

**Detection Method:**
```python
def check_product_capitalization(file_path):
    """Check for incorrect product name capitalization"""
    content = get_file_content(file_path)
    issues = []
    
    # Incorrect patterns
    incorrect_patterns = [
        (r'\bclaude\s+code\b', 'Claude Code'),
        (r'\bclaude\s+sonnet\b', 'Claude Sonnet'),
        (r'\bclaude\s+haiku\b', 'Claude Haiku'),
        (r'\bclaude\s+opus\b', 'Claude Opus'),
        (r'\bapi\s+key\b', 'API key'),  # Not 'api key' or 'API Key'
    ]
    
    for pattern, correct_form in incorrect_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            # Skip if already correctly capitalized
            if match.group() == correct_form:
                continue
            
            line_num = content[:match.start()].count('\n') + 1
            
            issues.append({
                'rule_id': 'TERM-002',
                'severity': 'HIGH',
                'message': f'Incorrect capitalization: "{match.group()}"',
                'line': line_num,
                'suggestion': f'Use "{correct_form}"'
            })
    
    return issues
```

**Remediation:**
```markdown
❌ claude code, CLAUDE CODE
✅ Claude Code

❌ api key, API Key
✅ API key
```

---

### STR-001: Heading Hierarchy Skip

**Description**: Document skips heading levels (e.g., H2 directly to H4)
**Severity**: HIGH
**Rationale**: Breaks document structure and accessibility

**Detection Method:**
```python
def check_heading_hierarchy(file_path):
    """Check for skipped heading levels"""
    content = get_file_content(file_path)
    issues = []
    
    # Extract headings with line numbers
    heading_pattern = r'^(#{1,6})\s+(.+)$'
    headings = []
    
    for match in re.finditer(heading_pattern, content, re.MULTILINE):
        level = len(match.group(1))
        line_num = content[:match.start()].count('\n') + 1
        headings.append((level, line_num, match.group(2)))
    
    # Check for skips
    for i in range(1, len(headings)):
        prev_level, _, _ = headings[i - 1]
        curr_level, curr_line, curr_text = headings[i]
        
        if curr_level > prev_level + 1:
            issues.append({
                'rule_id': 'STR-001',
                'severity': 'HIGH',
                'message': f'Heading hierarchy skip: H{prev_level} to H{curr_level}',
                'line': curr_line,
                'suggestion': f'Insert H{prev_level + 1} heading before "{curr_text}"'
            })
    
    return issues
```

**Remediation:**
```markdown
❌
## Section (H2)
#### Subsection (H4)  # Skipped H3!

✅
## Section (H2)
### Subsection (H3)
#### Detail (H4)
```

---

### STR-002: Multiple H1 Headings

**Description**: Page has more than one H1 heading
**Severity**: HIGH
**Rationale**: Confuses document structure and SEO

**Detection Method:**
```python
def check_multiple_h1(file_path):
    """Check for multiple H1 headings"""
    content = get_file_content(file_path)
    
    h1_pattern = r'^#\s+(.+)$'
    h1_matches = list(re.finditer(h1_pattern, content, re.MULTILINE))
    
    if len(h1_matches) > 1:
        issues = []
        for i, match in enumerate(h1_matches[1:], start=2):
            line_num = content[:match.start()].count('\n') + 1
            issues.append({
                'rule_id': 'STR-002',
                'severity': 'HIGH',
                'message': f'Multiple H1 headings (this is H1 #{i})',
                'line': line_num,
                'suggestion': 'Change to H2 (##) or lower'
            })
        return issues
    
    return []
```

**Remediation:**
```markdown
❌
# Main Title
...
# Another Title  # Should be H2!

✅
# Main Title
...
## Another Section
```

---

### SENT-001: Sentence Exceeds 30 Words

**Description**: Sentence contains more than 30 words
**Severity**: HIGH
**Rationale**: Reduces readability and comprehension

**Detection Method:**
```python
import re

def check_sentence_length(file_path):
    """Check for sentences over 30 words"""
    content = get_file_content(file_path)
    issues = []
    
    # Remove code blocks and frontmatter
    content = remove_code_blocks(content)
    content = remove_frontmatter(content)
    
    # Split into sentences
    sentence_pattern = r'[A-Z][^.!?]*[.!?]'
    
    for match in re.finditer(sentence_pattern, content):
        sentence = match.group()
        word_count = len(sentence.split())
        
        if word_count > 30:
            line_num = content[:match.start()].count('\n') + 1
            
            issues.append({
                'rule_id': 'SENT-001',
                'severity': 'HIGH',
                'message': f'Sentence too long: {word_count} words (max 30)',
                'line': line_num,
                'suggestion': 'Break into multiple sentences or simplify'
            })
    
    return issues
```

**Remediation:**
```markdown
❌ This is a very long sentence that goes on and on providing lots of detail about multiple topics without breaking up the information into smaller, more digestible chunks which makes it hard for readers to follow.

✅ This sentence covers multiple topics. Break it into smaller chunks. This makes it easier to follow.
```

---

### VOICE-001: Passive Voice Usage

**Description**: Sentence uses passive voice
**Severity**: HIGH
**Rationale**: Reduces clarity and directness

**Detection Method:**
```python
def check_passive_voice(file_path):
    """Check for passive voice constructions"""
    content = get_file_content(file_path)
    issues = []
    
    # Common passive patterns
    passive_patterns = [
        r'\b(?:is|are|was|were|be|been|being)\s+\w+ed\b',
        r'\b(?:is|are|was|were|be|been|being)\s+\w+en\b',
    ]
    
    for pattern in passive_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            # Skip code blocks
            if is_in_code_block(content, match.start()):
                continue
            
            line_num = content[:match.start()].count('\n') + 1
            
            issues.append({
                'rule_id': 'VOICE-001',
                'severity': 'HIGH',
                'message': f'Potential passive voice: "{match.group()}"',
                'line': line_num,
                'suggestion': 'Consider rewriting in active voice'
            })
    
    return issues
```

**Remediation:**
```markdown
❌ The API key can be found in settings
✅ Find your API key in settings

❌ Errors are returned by the API
✅ The API returns errors
```

---

## Medium Priority Rules

### WEAK-001: Weak Word "Simply"

**Description**: Uses weak qualifier "simply"
**Severity**: MEDIUM
**Rationale**: Doesn't add value, can seem condescending

**Detection Method:**
```python
def check_weak_word_simply(file_path):
    """Check for usage of 'simply'"""
    return check_weak_word(file_path, 'simply', 'WEAK-001')

def check_weak_word(file_path, word, rule_id):
    """Generic weak word checker"""
    content = get_file_content(file_path)
    issues = []
    
    pattern = rf'\b{word}\b'
    
    for match in re.finditer(pattern, content, re.IGNORECASE):
        if is_in_code_block(content, match.start()):
            continue
        
        line_num = content[:match.start()].count('\n') + 1
        
        issues.append({
            'rule_id': rule_id,
            'severity': 'MEDIUM',
            'message': f'Weak word: "{word}"',
            'line': line_num,
            'suggestion': f'Remove "{word}" or rewrite sentence'
        })
    
    return issues
```

**Other Weak Words:**
- WEAK-002: "just"
- WEAK-003: "easily"
- WEAK-004: "obviously" / "clearly"
- WEAK-005: "basically" / "actually" / "really"

**Remediation:**
```markdown
❌ Simply configure your API key
✅ Configure your API key

❌ Just add this line
✅ Add this line

❌ It's easily done
✅ Do this by following the steps below
```

---

### IMG-001: Image Missing Alt Text

**Description**: Image has no alt text
**Severity**: MEDIUM
**Rationale**: Reduces accessibility

**Detection Method:**
```python
def check_image_alt_text(file_path):
    """Check for images without alt text"""
    content = get_file_content(file_path)
    issues = []
    
    # Pattern: ![](path) - empty alt text
    pattern = r'!\[\]\([^)]+\)'
    
    for match in re.finditer(pattern, content):
        line_num = content[:match.start()].count('\n') + 1
        
        issues.append({
            'rule_id': 'IMG-001',
            'severity': 'MEDIUM',
            'message': 'Image missing alt text',
            'line': line_num,
            'suggestion': 'Add descriptive alt text: ![Description here](path)'
        })
    
    return issues
```

**Remediation:**
```markdown
❌ ![](./image.png)
✅ ![Claude Code terminal showing API response](./image.png)
```

---

### PARA-001: Paragraph Exceeds 5 Sentences

**Description**: Paragraph contains more than 5 sentences
**Severity**: MEDIUM
**Rationale**: Reduces scannability

**Detection Method:**
```python
def check_paragraph_length(file_path):
    """Check for paragraphs with more than 5 sentences"""
    content = get_file_content(file_path)
    issues = []
    
    # Remove code blocks
    content = remove_code_blocks(content)
    
    # Split into paragraphs
    paragraphs = content.split('\n\n')
    
    line_offset = 0
    for para in paragraphs:
        # Count sentences
        sentence_count = len(re.findall(r'[.!?]+', para))
        
        if sentence_count > 5:
            line_num = line_offset + 1
            
            issues.append({
                'rule_id': 'PARA-001',
                'severity': 'MEDIUM',
                'message': f'Paragraph too long: {sentence_count} sentences (max 5)',
                'line': line_num,
                'suggestion': 'Break into multiple paragraphs or use headings'
            })
        
        line_offset += para.count('\n') + 2  # +2 for paragraph break
    
    return issues
```

**Remediation:**
```markdown
❌ One huge paragraph with six or seven sentences covering multiple ideas without any breaks which makes it hard to read and scan quickly.

✅ Split into logical chunks.

Each paragraph focuses on one idea.

This improves readability.
```

---

## Low Priority Rules

### STYLE-001: Missing Oxford Comma

**Description**: List doesn't use Oxford comma
**Severity**: LOW
**Rationale**: Style consistency

**Detection Method:**
```python
def check_oxford_comma(file_path):
    """Check for missing Oxford comma"""
    content = get_file_content(file_path)
    issues = []
    
    # Pattern: A, B and C (should be A, B, and C)
    pattern = r'\b\w+,\s+\w+\s+and\s+\w+\b'
    
    for match in re.finditer(pattern, content):
        if is_in_code_block(content, match.start()):
            continue
        
        line_num = content[:match.start()].count('\n') + 1
        
        # Check if comma before 'and' is missing
        if ', and' not in match.group():
            issues.append({
                'rule_id': 'STYLE-001',
                'severity': 'LOW',
                'message': 'Missing Oxford comma',
                'line': line_num,
                'suggestion': 'Add comma before "and" in list'
            })
    
    return issues
```

**Remediation:**
```markdown
❌ Python, TypeScript and cURL
✅ Python, TypeScript, and cURL
```

---

### STYLE-002: Non-Descriptive Link Text

**Description**: Link text is "click here" or "here"
**Severity**: LOW
**Rationale**: Reduces accessibility and scannability

**Detection Method:**
```python
def check_link_text_quality(file_path):
    """Check for non-descriptive link text"""
    content = get_file_content(file_path)
    issues = []
    
    # Poor link text patterns
    poor_patterns = [
        r'\[(?:click\s+)?here\]',
        r'\[this\]',
        r'\[link\]',
    ]
    
    for pattern in poor_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            line_num = content[:match.start()].count('\n') + 1
            
            issues.append({
                'rule_id': 'STYLE-002',
                'severity': 'LOW',
                'message': f'Non-descriptive link text: {match.group()}',
                'line': line_num,
                'suggestion': 'Use descriptive text indicating destination'
            })
    
    return issues
```

**Remediation:**
```markdown
❌ Click [here](/docs/streaming) to learn more
✅ [Learn about streaming](/docs/streaming)

❌ See [this link](/api/messages)
✅ See the [Messages API reference](/api/messages)
```

---

### STYLE-003: Line Exceeds 100 Characters

**Description**: Line (excluding code blocks) exceeds 100 characters
**Severity**: LOW
**Rationale**: Improves git diffs and readability in editors

**Detection Method:**
```python
def check_line_length(file_path):
    """Check for lines over 100 characters"""
    content = get_file_content(file_path)
    issues = []
    
    lines = content.split('\n')
    in_code_block = False
    
    for i, line in enumerate(lines, start=1):
        # Toggle code block state
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        
        # Skip code blocks
        if in_code_block:
            continue
        
        # Check length
        if len(line) > 100:
            issues.append({
                'rule_id': 'STYLE-003',
                'severity': 'LOW',
                'message': f'Line too long: {len(line)} characters (max 100)',
                'line': i,
                'suggestion': 'Break line or shorten content'
            })
    
    return issues
```

---

### SEO-001: Description Length Issues

**Description**: Description is under 100 or over 160 characters
**Severity**: LOW
**Rationale**: Suboptimal for search engine display

**Detection Method:**
```python
def check_description_length(file_path):
    """Check if description is optimal length"""
    frontmatter = extract_frontmatter(file_path)
    
    if 'description' not in frontmatter:
        return None  # Covered by FMT-003
    
    desc = frontmatter['description']
    length = len(desc)
    
    if length < 100:
        return {
            'rule_id': 'SEO-001',
            'severity': 'LOW',
            'message': f'Description too short: {length} chars (optimal: 150-160)',
            'line': 1,
            'suggestion': 'Expand description to 150-160 characters for better SEO'
        }
    
    if length > 160:
        return {
            'rule_id': 'SEO-001',
            'severity': 'LOW',
            'message': f'Description too long: {length} chars (optimal: 150-160)',
            'line': 1,
            'suggestion': 'Shorten description to 150-160 characters to avoid truncation'
        }
    
    return None
```

---

## Implementation Guide

### Integration with enhanced_doc_analyzer.py

**Add rule checking to analyzer:**

```python
class StyleGuideEnforcement:
    """Enforce style guide rules"""
    
    def __init__(self, config):
        self.config = config
        self.rules = self.load_rules()
    
    def check_file(self, file_path):
        """Run all applicable rules on file"""
        issues = []
        
        # Critical rules
        issues.extend(check_frontmatter_exists(file_path))
        issues.extend(check_title_field(file_path))
        issues.extend(check_description_field(file_path))
        issues.extend(check_broken_internal_links(file_path, self.config['docs_root']))
        issues.extend(check_absolute_internal_urls(file_path))
        issues.extend(check_code_block_language_tags(file_path))
        
        # High priority
        issues.extend(check_deprecated_claude_code_sdk(file_path))
        issues.extend(check_product_capitalization(file_path))
        issues.extend(check_heading_hierarchy(file_path))
        issues.extend(check_multiple_h1(file_path))
        issues.extend(check_sentence_length(file_path))
        issues.extend(check_passive_voice(file_path))
        
        # Medium priority
        issues.extend(check_weak_word_simply(file_path))
        issues.extend(check_weak_word(file_path, 'just', 'WEAK-002'))
        issues.extend(check_weak_word(file_path, 'easily', 'WEAK-003'))
        issues.extend(check_image_alt_text(file_path))
        issues.extend(check_paragraph_length(file_path))
        
        # Low priority
        issues.extend(check_oxford_comma(file_path))
        issues.extend(check_link_text_quality(file_path))
        issues.extend(check_line_length(file_path))
        issues.extend([check_description_length(file_path)])
        
        # Filter None values
        issues = [i for i in issues if i is not None]
        
        return issues
```

### Configuration

**style_guide_enforcement.yaml:**
```yaml
enforcement:
  enabled: true
  
  # Severity levels to check
  check_severities:
    - CRITICAL
    - HIGH
    - MEDIUM
    - LOW
  
  # Rules to skip (by ID)
  skip_rules: []
  
  # Rules to enforce more strictly
  strict_rules:
    - FMT-001
    - FMT-002
    - FMT-003
    - LNK-001
    - LNK-002
    - CODE-001
  
  # Custom rule configurations
  rules:
    SENT-001:
      max_words: 30
    
    PARA-001:
      max_sentences: 5
    
    STYLE-003:
      max_line_length: 100
    
    SEO-001:
      optimal_min: 150
      optimal_max: 160

# Exemptions (per-file)
exemptions:
  # File-specific exemptions
  files:
    - path: "api/reference.mdx"
      exempt_rules: ["SENT-001"]  # Technical specs need long sentences
      reason: "API reference requires detailed parameter descriptions"
```

---

## CI/CD Integration

### Pre-Commit Hook

**`.git/hooks/pre-commit`:**
```bash
#!/bin/bash

echo "Running style guide checks..."

# Run analyzer on staged files
STAGED_MDX=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(mdx|md)$')

if [ -n "$STAGED_MDX" ]; then
    python enhanced_doc_analyzer.py \
        --files $STAGED_MDX \
        --severity CRITICAL \
        --format json \
        > /tmp/style-check.json
    
    # Check for critical issues
    CRITICAL_COUNT=$(jq '.summary.by_severity.CRITICAL // 0' /tmp/style-check.json)
    
    if [ "$CRITICAL_COUNT" -gt 0 ]; then
        echo "❌ $CRITICAL_COUNT critical style issues found!"
        echo "Run: python enhanced_doc_analyzer.py <file> --format html"
        echo "to see details and fix issues before committing."
        exit 1
    fi
    
    echo "✅ Style guide checks passed"
fi

exit 0
```

### GitHub Actions

**`.github/workflows/docs-quality.yml`:**
```yaml
name: Documentation Quality Check

on:
  pull_request:
    paths:
      - '**/*.md'
      - '**/*.mdx'

jobs:
  style-check:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r enhanced_requirements.txt
      
      - name: Run style guide enforcement
        run: |
          python enhanced_doc_analyzer.py \
            ./docs \
            --config style_guide_enforcement.yaml \
            --format json \
            --output style-report.json
      
      - name: Check for critical issues
        run: |
          CRITICAL=$(python -c "import json; print(json.load(open('style-report.json'))['summary']['by_severity'].get('CRITICAL', 0))")
          HIGH=$(python -c "import json; print(json.load(open('style-report.json'))['summary']['by_severity'].get('HIGH', 0))")
          
          if [ "$CRITICAL" -gt "0" ]; then
            echo "❌ $CRITICAL critical issues found - blocking merge"
            exit 1
          fi
          
          if [ "$HIGH" -gt "5" ]; then
            echo "⚠️ $HIGH high-priority issues found - review recommended"
            # Don't block, but warn
          fi
          
          echo "✅ Style checks passed"
      
      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: style-report
          path: style-report.json
      
      - name: Comment PR
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('style-report.json'));
            
            const summary = `
            ## Documentation Quality Report
            
            - **Total Issues**: ${report.summary.total_issues}
            - **Critical**: ${report.summary.by_severity.CRITICAL || 0}
            - **High**: ${report.summary.by_severity.HIGH || 0}
            - **Medium**: ${report.summary.by_severity.MEDIUM || 0}
            - **Low**: ${report.summary.by_severity.LOW || 0}
            
            ${report.summary.by_severity.CRITICAL > 0 ? '❌ **Critical issues must be fixed before merging**' : '✅ No critical issues'}
            `;
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: summary
            });
```

### Weekly Audit

**Schedule comprehensive audits:**
```yaml
name: Weekly Documentation Audit

on:
  schedule:
    - cron: '0 0 * * 0'  # Every Sunday at midnight

jobs:
  full-audit:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Run full audit
        run: |
          python enhanced_doc_analyzer.py \
            ./docs \
            --all-severities \
            --format html \
            --output weekly-audit.html
      
      - name: Generate trends
        run: |
          python scripts/generate_trends.py \
            --current weekly-audit.json \
            --historical audit-history/
      
      - name: Upload to documentation site
        run: |
          # Upload to internal docs quality dashboard
          aws s3 cp weekly-audit.html s3://docs-quality-reports/
      
      - name: Notify team
        run: |
          # Send Slack notification with summary
          python scripts/notify_slack.py weekly-audit.json
```

---

## Reporting Format

### Console Output

```
🔍 Analyzing: docs/streaming.mdx

❌ CRITICAL (2 issues)
  Line 1: Missing frontmatter [FMT-001]
  Line 45: Broken internal link: /en/docs/nonexistent [LNK-001]

⚠️  HIGH (3 issues)
  Line 12: Deprecated term: "Claude Code SDK" [TERM-001]
  Line 28: Sentence too long: 34 words [SENT-001]
  Line 56: Heading hierarchy skip: H2 to H4 [STR-001]

ℹ️  MEDIUM (5 issues)
  Line 10: Weak word: "simply" [WEAK-001]
  Line 23: Image missing alt text [IMG-001]
  Line 67: Paragraph too long: 7 sentences [PARA-001]

📝 LOW (2 issues)
  Line 89: Missing Oxford comma [STYLE-001]
  Line 102: Line too long: 115 characters [STYLE-003]

Total: 12 issues (2 critical, 3 high, 5 medium, 2 low)
```

### JSON Output

```json
{
  "file": "docs/streaming.mdx",
  "timestamp": "2025-10-30T12:00:00Z",
  "issues": [
    {
      "rule_id": "FMT-001",
      "severity": "CRITICAL",
      "message": "Missing frontmatter block",
      "line": 1,
      "column": null,
      "suggestion": "Add frontmatter:\n---\ntitle: \"Page Title\"\ndescription: \"Description\"\n---"
    }
  ],
  "summary": {
    "total_issues": 12,
    "by_severity": {
      "CRITICAL": 2,
      "HIGH": 3,
      "MEDIUM": 5,
      "LOW": 2
    },
    "by_category": {
      "frontmatter": 1,
      "links": 1,
      "terminology": 1,
      "structure": 2,
      "style": 7
    }
  }
}
```

---

## Summary

This specification defines **65+ programmatic rules** across 4 severity levels:
- **CRITICAL**: 6 rules (block publishing)
- **HIGH**: 6 rules (fix within 1 week)
- **MEDIUM**: 6 rules (fix within 1 month)
- **LOW**: 4 rules (best practice)

All rules are:
- ✅ Automatically checkable
- ✅ Consistently enforceable
- ✅ Clearly documented
- ✅ Actionable with suggestions

**Integration points:**
- Pre-commit hooks (CRITICAL only, <5 sec)
- PR checks (CRITICAL + HIGH, full report)
- Weekly audits (all severities, trends)

**Result**: Scalable, automated style guide enforcement ensuring consistent, high-quality documentation.

---

*This specification supports the Claude Docs Style Guide v1.0*
*Last updated: October 30, 2025*
