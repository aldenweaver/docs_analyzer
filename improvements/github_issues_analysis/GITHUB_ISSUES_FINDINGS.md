# GitHub Issues Research - Automated Analysis

**Research Date:** 2025-10-30
**Repository:** https://github.com/anthropics/claude-code
**Filter:** `state:open label:documentation`
**Issues Analyzed:** 142
**Analysis Method:** Automated via GitHub API

---

## Executive Summary

Analyzed 142 open documentation issues from the Claude Code repository.

**Category Breakdown:**
- **Missing:** 58 issues (40.8%)
- **Outdated:** 37 issues (26.1%)
- **Unclear:** 36 issues (25.4%)
- **Findability:** 6 issues (4.2%)
- **Context:** 5 issues (3.5%)

---

## Issues Data Collection

| Issue # | Title | Category | Upvotes (👍) | Comments | Age (days) | Impact Score |
|---------|-------|----------|--------------|----------|------------|-------------|
| #1234 | Support for other IDEs (Neovim/Emacs) | Unclear | 76 | 10 | 161 | 4.72 |
| #1202 | Documentation error: settings.json location | Unclear | 37 | 15 | 163 | 3.40 |
| #8327 | [Bug/Documentation] 'Organization has been disable... | Outdated | 2 | 54 | 32 | 3.38 |
| #9072 | [DOCS] Document the difference between `ultrathink... | Missing | 25 | 1 | 23 | 1.09 |
| #9681 | [DOCS] Bedrock setup missing AWS Marketplace subsc... | Missing | 5 | 3 | 14 | 1.07 |

---

## Pattern Analysis by Category

### Missing Documentation

**Count:** 58 issues (40.8%)

**Common themes:**
- error (2 mentions)
- cli (2 mentions)
- command (9 mentions)
- feature (7 mentions)

**Example issues:**
- [#10504](https://github.com/anthropics/claude-code/issues/10504): [FEATURE] Subagent YAML frontmatter description field has UX and design issues
- [#10491](https://github.com/anthropics/claude-code/issues/10491): [DOCS] Improve documentation for VS Code setting `claude-code.claudeProcessWrapper` with usage examples on different platforms.
- [#10469](https://github.com/anthropics/claude-code/issues/10469): [DOCS] Missing Documentation for Built-in 'Plan' / 'Explore' Subagent

### Outdated Documentation

**Count:** 37 issues (26.1%)

**Common themes:**
- error (2 mentions)
- command (3 mentions)
- feature (6 mentions)

**Example issues:**
- [#10193](https://github.com/anthropics/claude-code/issues/10193): [Feature Request] Document Ctrl+G system editor shortcut in documentation
- [#10037](https://github.com/anthropics/claude-code/issues/10037): [BUG] Claude is unable to write a working wildcard
- [#9959](https://github.com/anthropics/claude-code/issues/9959): [FEATURE] Feature Enhancement: Skills Documentation Pattern Support

### Unclear Documentation

**Count:** 36 issues (25.4%)

**Common themes:**
- error (4 mentions)
- cli (3 mentions)
- command (5 mentions)
- feature (3 mentions)

**Example issues:**
- [#10247](https://github.com/anthropics/claude-code/issues/10247): [Bug] Documentation typo: "Tech Claude" should be "Teach Claude" on agent skills overview page
- [#9186](https://github.com/anthropics/claude-code/issues/9186): [Feature Request] Add Documentation URLs for CLI Slash Commands
- [#7166](https://github.com/anthropics/claude-code/issues/7166): Clarify whether subagents read the user-scoped `~/.claude/CLAUDE.md` file

### Findability Documentation

**Count:** 6 issues (4.2%)

**Common themes:**
- feature (2 mentions)

**Example issues:**
- [#8858](https://github.com/anthropics/claude-code/issues/8858): [BUG] MCP with oauth in headless mode
- [#8728](https://github.com/anthropics/claude-code/issues/8728): [FEATURE] Please provide changelogs for VSCode extension
- [#8100](https://github.com/anthropics/claude-code/issues/8100): Clearly indicate Terminal.app can only support Opt+Enter

### Context Documentation

**Count:** 5 issues (3.5%)


**Example issues:**
- [#9307](https://github.com/anthropics/claude-code/issues/9307): Improve Claude Code documentation accessibility in Claude's context
- [#7151](https://github.com/anthropics/claude-code/issues/7151): Clarification needed on Statsig dependency following OpenAI acquisition
- [#7100](https://github.com/anthropics/claude-code/issues/7100): feat(docs, auth): Document Headless/Remote Authentication and Support CI/CD

---

## Top 5 Most-Impactful Issues

*Ranked by: (Upvotes × Comments) ÷ Age*

1. **Issue #1234:** [Support for other IDEs (Neovim/Emacs)](https://github.com/anthropics/claude-code/issues/1234)
   - Category: Unclear
   - Impact: MEDIUM (score: 4.72)
   - Engagement: 76 upvotes, 10 comments
   - Age: 161 days

2. **Issue #1202:** [Documentation error: settings.json location](https://github.com/anthropics/claude-code/issues/1202)
   - Category: Unclear
   - Impact: MEDIUM (score: 3.40)
   - Engagement: 37 upvotes, 15 comments
   - Age: 163 days

3. **Issue #8327:** [[Bug/Documentation] 'Organization has been disabled' error when ANTHROPIC_API_KEY overrides Max/Pro subscription](https://github.com/anthropics/claude-code/issues/8327)
   - Category: Outdated
   - Impact: MEDIUM (score: 3.38)
   - Engagement: 2 upvotes, 54 comments
   - Age: 32 days

4. **Issue #9072:** [[DOCS] Document the difference between `ultrathink` and Thinking Mode On/Off](https://github.com/anthropics/claude-code/issues/9072)
   - Category: Missing
   - Impact: MEDIUM (score: 1.09)
   - Engagement: 25 upvotes, 1 comments
   - Age: 23 days

5. **Issue #9681:** [[DOCS] Bedrock setup missing AWS Marketplace subscription requirements causing permission errors](https://github.com/anthropics/claude-code/issues/9681)
   - Category: Missing
   - Impact: MEDIUM (score: 1.07)
   - Engagement: 5 upvotes, 3 comments
   - Age: 14 days

---

## Implementable Fixes Analysis

### Fix Candidate #1: Missing Documentation Detection
**Pattern:** Users reporting features/concepts that lack documentation
**Example Issues:** #10504, #10491, #10469
**How to detect:** Flag pages with:
- Very short content (< 100 words)
- Missing code examples when discussing code features
- No 'Prerequisites' section for procedural content

**How to fix:** Flag for manual review with suggested templates
**Effort:** MEDIUM
**Impact:** HIGH
**Implement?** YES

### Fix Candidate #2: Clarity Improvements
**Pattern:** Users finding existing documentation confusing
**Example Issues:** #10247, #9186, #7166
**How to detect:** Look for:
- Jargon without definitions
- Missing examples
- Long paragraphs without structure

**How to fix:** Add warnings/suggestions for:
- Technical terms that need glossary entries
- Code mentions without examples
**Effort:** SMALL
**Impact:** MEDIUM
**Implement?** YES

### Fix Candidate #3: Findability/Navigation
**Pattern:** Users can't locate existing information
**Example Issues:** #8858, #8728, #8100
**How to detect:** Check for:
- Missing cross-references
- Inconsistent terminology across pages

**How to fix:** Suggest adding cross-links for related concepts
**Effort:** MEDIUM
**Impact:** MEDIUM
**Implement?** MAYBE


---

## Requested Topics (TRUE Gap Detection)

**Extracted 105 specific topic requests from issues:**

| Topic | Mentions | Related Issues |
|-------|----------|----------------|
| tool | 29 | [#10377](https://github.com/anthropics/claude-code/issues/10377), [#9600](https://github.com/anthropics/claude-code/issues/9600), [#8600](https://github.com/anthropics/claude-code/issues/8600) (+26 more) |
| Bedrock | 17 | [#10037](https://github.com/anthropics/claude-code/issues/10037), [#8946](https://github.com/anthropics/claude-code/issues/8946), [#8369](https://github.com/anthropics/claude-code/issues/8369) (+14 more) |
| MCP | 16 | [#10079](https://github.com/anthropics/claude-code/issues/10079), [#8858](https://github.com/anthropics/claude-code/issues/8858), [#7672](https://github.com/anthropics/claude-code/issues/7672) (+13 more) |
| subagent | 10 | [#10504](https://github.com/anthropics/claude-code/issues/10504), [#9681](https://github.com/anthropics/claude-code/issues/9681), [#9595](https://github.com/anthropics/claude-code/issues/9595) (+7 more) |
| slash command | 8 | [#9307](https://github.com/anthropics/claude-code/issues/9307), [#9186](https://github.com/anthropics/claude-code/issues/9186), [#8758](https://github.com/anthropics/claude-code/issues/8758) (+5 more) |
| Plan | 4 | [#8327](https://github.com/anthropics/claude-code/issues/8327), [#7179](https://github.com/anthropics/claude-code/issues/7179), [#3658](https://github.com/anthropics/claude-code/issues/3658) (+1 more) |
| agent | 4 | [#6973](https://github.com/anthropics/claude-code/issues/6973), [#6920](https://github.com/anthropics/claude-code/issues/6920), [#4347](https://github.com/anthropics/claude-code/issues/4347) (+1 more) |
| ultrathink | 3 | [#10099](https://github.com/anthropics/claude-code/issues/10099), [#8360](https://github.com/anthropics/claude-code/issues/8360), [#7668](https://github.com/anthropics/claude-code/issues/7668) |
| skill | 2 | [#10247](https://github.com/anthropics/claude-code/issues/10247), [#9959](https://github.com/anthropics/claude-code/issues/9959) |
| thinking mode | 2 | [#8780](https://github.com/anthropics/claude-code/issues/8780), [#8368](https://github.com/anthropics/claude-code/issues/8368) |
| Built-in 'Plan' / 'Explore' Subagent | 1 | [#10469](https://github.com/anthropics/claude-code/issues/10469) |
| AskUserQuestion Tool | 1 | [#10346](https://github.com/anthropics/claude-code/issues/10346) |
| modifying tool inputs in PreToolUse hooks | 1 | [#9185](https://github.com/anthropics/claude-code/issues/9185) |
| the difference between `ultrathink` and Thinking Mode On/Off | 1 | [#9072](https://github.com/anthropics/claude-code/issues/9072) |
| default OAuth token `expires_in` behavior when omitted | 1 | [#9017](https://github.com/anthropics/claude-code/issues/9017) |
| Various Claude Code Features | 1 | [#8584](https://github.com/anthropics/claude-code/issues/8584) |
| new mascot 'Clawd' and implement an introductory welcome screen | 1 | [#8536](https://github.com/anthropics/claude-code/issues/8536) |
| the Bash tool's sandbox parameter | 1 | [#8194](https://github.com/anthropics/claude-code/issues/8194) |
| Explore | 1 | [#2659](https://github.com/anthropics/claude-code/issues/2659) |
| AWS | 1 | [#1028](https://github.com/anthropics/claude-code/issues/1028) |

**These are the specific features/topics users are requesting documentation for.**
To truly address these gaps, check if these topics exist in the actual Claude docs.


---

## Key Insights

**1. Root Causes:**
- Documentation completeness: 58 issues about missing docs
- Content clarity: 36 issues about comprehension
- Information architecture: 6 issues about finding content

**2. Systematic Patterns:**
- Most common issue type: Missing (58 issues)
- Average issue age: 72.7 days
- Average engagement: 1.8 comments per issue

**3. Quick Wins:**
- Issues will be identified after manual review of top-impact items

---

## Next Steps

- [ ] Review top 5 high-impact issues manually
- [ ] Validate these patterns exist in docs/about-claude/
- [ ] Design GitHubInformedFixer class structure
- [ ] Implement detection and fixing logic
- [ ] Run comparative analysis

---

**Analysis completed:** 2025-10-30 21:03:14
**Tool:** Automated GitHub Issues Researcher
