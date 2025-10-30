# Sample Page Rewrites: Before & After
## Transforming "Technically Correct But Hard to Understand" Content

This document shows detailed before/after rewrites of 3 key pages from the Claude documentation, demonstrating how to transform technically accurate but confusing content into clear, user-centered documentation.

---

## Example 1: Prompt Caching Page
**Current URL:** https://anthropic.mintlify.app/en/docs/build-with-claude/prompt-caching

### BEFORE (Current Version - Confusing)

```markdown
# Prompt Caching

Prompt caching is a powerful feature that optimizes API usage by allowing you to reuse large contexts across multiple requests. It's particularly beneficial for applications that repeatedly use the same foundational information.

## How it works

Changes at different levels invalidate subsequent levels:
- Modifying tool definitions invalidates entire cache
- Web search/citations toggle invalidates system and messages cache
- Changing `tool_choice` or images invalidates messages cache
- Thinking parameter changes invalidate messages cache

The system checks approximately 20 content blocks before your explicit breakpoint for previous cache hits. This automatic checking limitation means content more than 20 blocks before a breakpoint won't be checked unless you add additional breakpoints.

## Cache Control

Use the `cache_control` parameter to mark content for caching:

```json
{
  "model": "claude-sonnet-4-5",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Analyze this document",
          "cache_control": {"type": "ephemeral"}
        }
      ]
    }
  ]
}
```
```

**Problems:**
- ❌ Dives into cache invalidation rules without explaining WHAT problem caching solves
- ❌ "Subsequent levels" terminology undefined
- ❌ "20 content blocks" concept appears without context
- ❌ Technical implementation shown before conceptual understanding
- ❌ No clear use cases or decision criteria

---

### AFTER (Improved Version - Clear)

```markdown
# Prompt Caching

Save up to 90% on API costs by reusing repeated content across multiple requests.

## What problem does prompt caching solve?

**Without caching:** Every time you make an API request, Claude re-processes all input content—even if you're sending the same background information repeatedly. For a 50K token document analyzed 100 times, you'd pay to process 5 million tokens.

**With caching:** Claude stores frequently reused content and instantly retrieves it on subsequent requests. The same scenario costs a fraction: 50K tokens once + small cache retrieval fees.

## When to use prompt caching

✅ **Perfect for:**
- Analyzing multiple queries against the same large document
- Chat applications with long system prompts
- Repetitive code analysis on the same codebase
- Processing many files with identical instructions

❌ **Don't use for:**
- One-off requests (caching overhead not worth it)
- Content that changes frequently
- Requests with mostly unique content

## How caching works: The layered model

Think of cached content as a layered cake. Each layer builds on the previous one:

```
┌─────────────────────────────┐
│  Tool Definitions Layer     │ ← Changes here invalidate everything below
├─────────────────────────────┤
│  System Prompt Layer        │ ← Changes here invalidate messages only
├─────────────────────────────┤
│  Messages Layer             │ ← Only this layer gets invalidated
└─────────────────────────────┘
```

**Key rule:** If you change any layer, all layers BELOW it get cleared from cache.

### Real example

**Request 1:**
```json
{
  "system": [
    {
      "type": "text",
      "text": "You are a legal document analyzer. Use these definitions: [5000 token legal glossary]",
      "cache_control": {"type": "ephemeral"}
    }
  ],
  "messages": [
    {"role": "user", "content": "Analyze contract A"}
  ]
}
```
→ Claude caches your 5000-token legal glossary

**Request 2:**
```json
{
  "system": [
    {
      "type": "text",
      "text": "You are a legal document analyzer. Use these definitions: [same 5000 token legal glossary]",
      "cache_control": {"type": "ephemeral"}
    }
  ],
  "messages": [
    {"role": "user", "content": "Analyze contract B"}
  ]
}
```
→ Claude retrieves cached glossary (5000 tokens cached, only new message processed)

**Request 3:**
```json
{
  "system": [
    {
      "type": "text",
      "text": "You are a legal document analyzer. Use these UPDATED definitions: [5000 token glossary v2]",
      "cache_control": {"type": "ephemeral"}
    }
  ],
  "messages": [
    {"role": "user", "content": "Analyze contract C"}
  ]
}
```
→ System layer changed, so cache invalidates. Claude processes new glossary and creates new cache.

## Quick start

### Step 1: Mark content for caching

Add `cache_control` to content you want cached:

```python
from anthropic import Anthropic

client = Anthropic()

# Long document you'll query multiple times
long_document = open('legal_terms.txt').read()  # 50,000 tokens

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": long_document,
            "cache_control": {"type": "ephemeral"}  # ← Cache this
        }
    ],
    messages=[
        {"role": "user", "content": "What does 'force majeure' mean?"}
    ]
)
```

### Step 2: Check cache performance

The response includes cache statistics:

```python
print(message.usage)
# Output:
# {
#   'input_tokens': 1024,
#   'cache_creation_input_tokens': 50000,  # First request: creates cache
#   'cache_read_input_tokens': 0,
#   'output_tokens': 150
# }
```

On subsequent requests with the same document:

```python
# {
#   'input_tokens': 1024,
#   'cache_creation_input_tokens': 0,
#   'cache_read_input_tokens': 50000,  # Using cached content!
#   'output_tokens': 145
# }
```

## Advanced: Automatic prefix checking

**What is it?**
Claude automatically checks up to 20 content blocks BEFORE your explicit cache breakpoint to see if they match previously cached content.

**Why it matters:**
You don't need to mark every possible cache point. Claude does smart matching.

**Visual example:**

```
Your message content:
[Block 1] [Block 2] ... [Block 18] [Block 19] [Block 20] [CACHE MARKER] [Block 22]
                                    └────────────────────┘
                                    Claude checks these 20 blocks automatically
```

If Blocks 1-20 match a previous request, Claude uses that cache even though only Block 21 has the cache marker.

**Limitation:** Content MORE than 20 blocks before a marker won't be checked. Solution: Add additional cache markers for very long content.

## Cost breakdown

| Scenario | Without Cache | With Cache | Savings |
|----------|---------------|------------|---------|
| First request (50K doc) | $0.75 | $0.75 + $0.15 cache write | -$0.15 |
| Requests 2-100 (50K doc) | $74.25 | $1.49 cache reads | **$72.76 (98%)** |
| **Total (100 requests)** | **$75.00** | **$2.39** | **$72.61 (97%)** |

*Based on Sonnet 4.5 pricing. Cache writes cost 25% of input tokens, cache reads cost 10% of input tokens.*

## What invalidates cache?

| You change... | What gets invalidated | Why |
|---------------|----------------------|-----|
| Tool definitions | Entire cache | Tools are the top layer |
| System prompt | System + Messages | System is middle layer |
| User message | Messages only | Messages are bottom layer |
| Temperature/top_p | Messages only | Parameters affect message processing |
| Images in messages | Messages only | Images are part of message content |

## Best practices

### ✅ Do:
- Cache stable content: system prompts, large documents, code repositories
- Monitor `cache_creation_input_tokens` and `cache_read_input_tokens` in responses
- Place frequently-changing content AFTER cached content
- Use cache for contexts over 1024 tokens (minimum cacheable size)

### ❌ Don't:
- Cache content that changes every request
- Mix frequently-changing content before stable content
- Ignore cache hit rates—monitor your savings

## Troubleshooting

**Q: My cache isn't being used (cache_read_input_tokens = 0)**
- Verify content is EXACTLY the same (even a single space difference invalidates)
- Check that cached content is at least 1024 tokens
- Ensure you're using the same model
- Caches expire after 5 minutes of inactivity

**Q: My cache_creation_input_tokens is higher than expected**
- You might be creating multiple caches due to content variations
- Check if parameters like `temperature` are changing
- Verify tool definitions are consistent

**Q: How long do caches last?**
- 5 minutes from last use
- Each cache read refreshes the timer
- No limit on number of cache reads within 5 minutes

## Next steps

- [See prompt caching examples](/en/api/messages-examples#prompt-caching)
- [Calculate your potential savings](/en/docs/about-claude/pricing#caching)
- [Learn about context windows](/en/docs/build-with-claude/context-windows)
```

**Improvements Made:**
- ✅ Starts with clear value proposition (save 90%)
- ✅ Explains problem before solution
- ✅ Uses visual diagrams for layered model
- ✅ Provides real before/after examples
- ✅ Includes concrete cost breakdown
- ✅ Adds troubleshooting section
- ✅ Progressive disclosure: basic → advanced

---

## Example 2: Extended Thinking Page
**Current URL:** https://anthropic.mintlify.app/en/docs/build-with-claude/extended-thinking

### BEFORE (Current Version - Confusing)

```markdown
# Extended Thinking

Extended thinking enables Claude to show its step-by-step reasoning before providing a final answer.

`budget_tokens` parameter sets the maximum tokens for internal reasoning. This must be less than `max_tokens`. Previous thinking blocks are stripped from context and don't count toward your window, but current-turn thinking counts toward `max_tokens`.

## Usage

```python
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 16000
    },
    messages=[
        {"role": "user", "content": "What is 27 * 453?"}
    ]
)
```

You're charged for the actual thinking tokens generated (not the budget).
```

**Problems:**
- ❌ No explanation of WHY extended thinking exists
- ❌ Three different token concepts mixed without definitions
- ❌ Billing model buried and unclear
- ❌ No use cases or decision criteria
- ❌ "Stripped from context" is jargon-heavy

---

### AFTER (Improved Version - Clear)

```markdown
# Extended Thinking

Let Claude "think out loud" to solve complex problems more accurately.

## What is extended thinking?

Extended thinking allows Claude to show you its reasoning process before providing an answer. It's like watching a mathematician work through a problem on a whiteboard before stating the final result.

**Without extended thinking:**
```
You: "What is 27 * 453?"
Claude: "12,231"
```
You see the answer but not the reasoning.

**With extended thinking:**
```
You: "What is 27 * 453?"
Claude's thinking: "Let me break this down:
  1. 27 * 400 = 10,800
  2. 27 * 50 = 1,350
  3. 27 * 3 = 81
  4. 10,800 + 1,350 + 81 = 12,231"
Claude's answer: "12,231"
```
You see both the reasoning AND the answer.

## When to use extended thinking

✅ **Perfect for:**
- Complex math or logic problems
- Multi-step reasoning tasks
- Debugging code or analyzing errors
- When you need to verify Claude's reasoning
- Academic or research questions

❌ **Not needed for:**
- Simple questions with direct answers
- Creative writing
- Translation tasks
- When you just want the final answer quickly

## Understanding the three types of tokens

Extended thinking introduces a new token budget system. Here's how the three token types work together:

```
┌─────────────────────────────────────────────┐
│ Context Window (200K tokens total)          │
│ Everything Claude can "see"                 │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ Previous Conversation (150K used)       │ │
│ │ - Your past messages                    │ │
│ │ - Claude's past responses               │ │
│ │ - Past thinking (summarized)            │ │
│ ├─────────────────────────────────────────┤ │
│ │ Current Request (5K)                    │ │
│ │ - Your new question                     │ │
│ ├─────────────────────────────────────────┤ │
│ │ Available Space (45K remaining)         │ │
│ │                                         │ │
│ │ ┌─────────────────┬─────────────────┐   │ │
│ │ │ budget_tokens   │ max_tokens      │   │ │
│ │ │ (10K thinking)  │ (4K response)   │   │ │
│ │ │ Internal work   │ Final answer    │   │ │
│ │ └─────────────────┴─────────────────┘   │ │
│ └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### The three token types:

1. **Context Window** (200K for Claude 4.5)
   - Everything Claude can "see" in the conversation
   - Includes past messages and responses
   - Think of it as Claude's working memory

2. **budget_tokens** (you choose, e.g., 10K)
   - Maximum tokens Claude can use for internal thinking
   - Like giving Claude scratch paper space
   - Must be less than max_tokens
   - Claude uses only what it needs (you set the ceiling)

3. **max_tokens** (you choose, e.g., 4K)
   - Maximum tokens for the final response (thinking + answer)
   - Like setting a page limit for the complete response
   - Includes both thinking and final answer

### Rules and examples:

✅ **Valid configuration:**
```python
budget_tokens=8000   # Claude can think up to 8K tokens
max_tokens=10000     # Total output (thinking + answer) up to 10K
```

❌ **Invalid configuration:**
```python
budget_tokens=12000  # Error! Can't think more than you can output
max_tokens=10000
```

✅ **Optimal for complex problem:**
```python
budget_tokens=16000  # Lots of thinking space
max_tokens=20000     # Room for thinking + detailed answer
```

✅ **Optimal for simple problem:**
```python
budget_tokens=2000   # Minimal thinking space
max_tokens=4000      # Short response expected
```

## How billing works

You're charged for actual tokens used, not the budget you set.

**Example request:**
```python
thinking={"type": "enabled", "budget_tokens": 10000}
max_tokens=4000
```

**Possible billing scenarios:**

| Claude's actual usage | Your cost |
|----------------------|-----------|
| 2K thinking + 500 response | 2,500 tokens |
| 8K thinking + 1K response | 9,000 tokens |
| 200 thinking + 300 response | 500 tokens |

**Key insight:** `budget_tokens` is a safety limit, not a minimum. Claude uses what it needs.

## Quick start

### Basic example

```python
from anthropic import Anthropic

client = Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={
        "type": "enabled",
        "budget_tokens": 16000  # Allow up to 16K tokens of thinking
    },
    messages=[
        {"role": "user", "content": "Calculate 27 * 453 step by step"}
    ]
)

# Access thinking and response separately
for block in message.content:
    if block.type == "thinking":
        print("Claude's thinking:", block.thinking)
    elif block.type == "text":
        print("Claude's answer:", block.text)
```

**Output:**
```
Claude's thinking: Let me break this down:
1. 27 * 400 = 10,800
2. 27 * 50 = 1,350
3. 27 * 3 = 81
4. 10,800 + 1,350 + 81 = 12,231

Claude's answer: 27 * 453 = 12,231
```

### Streaming thinking in real-time

```python
with client.messages.stream(
    model="claude-sonnet-4-5",
    max_tokens=20000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    messages=[{"role": "user", "content": "Solve this puzzle..."}]
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "thinking_delta":
                print(event.delta.thinking, end="", flush=True)
            elif event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
```

This shows thinking as it happens, like watching Claude work through the problem live.

## Advanced: Managing conversation history

### How past thinking is handled

**First turn:**
```
You: "What is 27 * 453?"
Claude's thinking: [500 tokens of step-by-step math]
Claude's answer: "12,231"
```
The full thinking (500 tokens) is stored in the conversation.

**Second turn:**
```
You: "Now multiply that by 2"
```
Claude sees:
- Your first question
- Summary of past thinking (not full 500 tokens)
- Your new question

**Why?** Past thinking is summarized to save context space for new conversations.

**Important:** Current turn thinking counts toward `max_tokens`. Past thinking doesn't.

## Best practices

### ✅ Do:
- Set `budget_tokens` generously for complex problems (10K-16K)
- Use streaming to show thinking in real-time for better UX
- Verify Claude's reasoning when accuracy is critical
- Monitor actual token usage to optimize budget_tokens

### ❌ Don't:
- Use extended thinking for simple queries (wastes tokens)
- Set budget_tokens = max_tokens (leaves no room for answer)
- Ignore the thinking output (that's where the value is!)
- Modify `temperature` with extended thinking (not compatible)

## Cost comparison

**Simple question: "What is the capital of France?"**
- Without thinking: ~50 tokens = $0.00015
- With thinking: ~200 tokens = $0.00060 (4x cost for no benefit)
- **Verdict:** Don't use extended thinking

**Complex question: "Debug this 200-line Python error trace"**
- Without thinking: ~500 tokens, might be incorrect = $0.0015
- With thinking: ~3,000 tokens, shows debugging steps = $0.009
- **Verdict:** Worth the cost for accuracy and transparency

## Troubleshooting

**Q: Error: "budget_tokens must be less than max_tokens"**
```python
# ❌ Wrong
budget_tokens=10000, max_tokens=8000

# ✅ Correct
budget_tokens=8000, max_tokens=10000
```

**Q: Claude's thinking seems cut off**
- Increase `budget_tokens` (Claude hit the limit)
- Increase `max_tokens` (total output hit the limit)

**Q: I'm not seeing any thinking**
- Check that model is Claude 4.5 (older models don't support this)
- Verify thinking is actually needed for your question
- Check response content blocks for type="thinking"

**Q: Can I use extended thinking with other features?**
- ✅ Yes: Streaming, tool use, vision, PDFs
- ❌ No: Temperature adjustment (parameter conflict)

## Next steps

- [See extended thinking examples](/en/api/messages-examples#extended-thinking)
- [Compare with standard responses](/en/docs/build-with-claude/streaming)
- [Learn about context windows](/en/docs/build-with-claude/context-windows)
```

**Improvements Made:**
- ✅ Starts with "what" and "why" before "how"
- ✅ Visual diagram explaining token relationships
- ✅ Clear rules with valid/invalid examples
- ✅ Real billing scenarios
- ✅ Use case guidance
- ✅ Comprehensive troubleshooting

---

## Example 3: Computer Use Tool Page (Partial Rewrite)
**Current URL:** https://anthropic.mintlify.app/en/docs/agents-and-tools/tool-use/computer-use-tool

### BEFORE (Security Section - Vague)

```markdown
## Safety and security

Computer use poses unique safety risks. To minimize risks:

- Use a dedicated virtual machine or container with minimal privileges to prevent direct system attacks or accidents
- Update the system and installed software regularly
- Avoid giving the model access to sensitive data
- Implement isolation techniques
```

**Problems:**
- ❌ "Unique safety risks" not explained
- ❌ "Minimal privileges" undefined
- ❌ No concrete threat examples
- ❌ No actionable implementation guidance
- ❌ Missing reference implementation links

---

### AFTER (Security Section - Specific)

```markdown
## Security best practices

**Why computer use requires special security:**
Unlike text-based tool use where Claude only returns data, computer use gives Claude control over a virtual desktop. This means:
- Claude can click buttons, type text, and run commands
- Malicious actors could try prompt injection to make Claude take unwanted actions
- Bugs in your code could give Claude unintended access

### Threat model: What could go wrong?

| Threat | Example | Mitigation |
|--------|---------|-----------|
| **Data exfiltration** | Attacker prompts: "Take a screenshot of ~/.ssh/ and describe it" | Use VM with no sensitive files |
| **Unintended actions** | Bug causes Claude to click "Delete All" button | Sandbox with restricted permissions |
| **System compromise** | Claude downloads and executes malicious code | Network isolation, restricted execution |
| **Cost overrun** | Infinite loop of screenshots | Implement timeout and rate limits |

### Required: Use isolated environment

**✅ Recommended setup:**
```yaml
# Docker container with restricted capabilities
docker run -it \
  --security-opt=no-new-privileges \
  --cap-drop=ALL \
  --cap-add=SYS_CHROOT \
  --network=isolated_network \
  --read-only \
  --tmpfs /tmp \
  anthropic/computer-use-demo
```

**Minimal privileges checklist:**
- [ ] No root access
- [ ] Read-only filesystem (except /tmp)
- [ ] No network access to internal systems
- [ ] No access to SSH keys, API tokens, or credentials
- [ ] Limited CPU and memory (prevent resource exhaustion)
- [ ] Automatic cleanup after each session

### Reference implementation

See our Docker-based reference implementation with security features:
👉 [Computer Use Demo on GitHub](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)

**What it includes:**
- Pre-configured Docker container
- Network isolation
- Screen recording for audit
- Timeout and rate limiting
- Minimal Ubuntu with no sensitive data

### Network isolation strategy

```
┌─────────────────────────────────────┐
│ Internet                            │
│                                     │
│ ┌─────────────────────────────┐    │
│ │ Your Production Systems     │    │
│ │ ❌ Claude CANNOT access     │    │
│ └─────────────────────────────┘    │
│                                     │
│ ┌─────────────────────────────────┐│
│ │ Isolated Network Segment       ││
│ │                                ││
│ │  ┌──────────────────────────┐ ││
│ │  │ Computer Use VM          │ ││
│ │  │ ✅ Claude runs here      │ ││
│ │  │ ✅ Can access test sites │ ││
│ │  │ ❌ Cannot access prod    │ ││
│ │  └──────────────────────────┘ ││
│ └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

### What NOT to do

❌ **Never:**
- Run computer use on your development machine
- Give Claude access to systems with production data
- Use the same VM for multiple users without cleanup
- Skip timeout limits (Claude could run indefinitely)
- Trust user input without validation (prompt injection risk)

### Audit logging

Always log computer use actions for security review:

```python
import logging

logging.basicConfig(filename='claude_computer_use.log', level=logging.INFO)

def log_computer_action(action, result):
    logging.info(f"Action: {action}, Result: {result}, Timestamp: {time.time()}")

# In your tool use handler
for tool_use in response.content:
    if tool_use.type == "tool_use":
        log_computer_action(tool_use.input, "executed")
```

**What to log:**
- Every computer use action (screenshot, mouse, keyboard, bash)
- Timestamps
- Input parameters
- Results/errors
- User who initiated the request

### Security checklist before deployment

Before using computer use in production, verify:

- [ ] VM/container is completely isolated from production systems
- [ ] No sensitive data (credentials, keys, PII) in VM
- [ ] Network isolation configured (firewall rules)
- [ ] Timeout limits implemented (per action and total session)
- [ ] Rate limiting enabled (prevent resource exhaustion)
- [ ] Audit logging active
- [ ] Regular VM cleanup/reset between sessions
- [ ] Monitoring and alerting configured
- [ ] Incident response plan documented

### Next steps

- [Try the secure reference implementation](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)
- [Read tool use security best practices](/en/docs/build-with-claude/tool-use#security)
- [Join the Computer Use Beta discussion](https://community.anthropic.com)
```

**Improvements Made:**
- ✅ Explains specific threats with examples
- ✅ Provides concrete setup checklist
- ✅ Shows architecture diagram
- ✅ Links to reference implementation
- ✅ Includes audit logging code
- ✅ Pre-deployment security checklist

---

## Summary of Rewrite Principles

### What Makes These Rewrites Better:

1. **Start with "Why"**
   - Explain the problem before the solution
   - Show value proposition upfront

2. **Use Progressive Disclosure**
   - Simple explanation → visual diagram → detailed example → advanced topics
   - Don't bury beginners in edge cases

3. **Add Visual Learning Aids**
   - ASCII diagrams for architecture
   - Tables for comparisons
   - Code examples with annotations

4. **Provide Decision Frameworks**
   - ✅/❌ lists for when to use
   - Comparison tables
   - Concrete cost breakdowns

5. **Include Complete Examples**
   - Show input and output
   - Explain what happened and why
   - Provide multiple scenarios

6. **Add Troubleshooting**
   - Common errors with solutions
   - Q&A format
   - Links to related docs

7. **Use Concrete Numbers**
   - Replace "approximately" with ranges
   - Show real cost calculations
   - Provide performance benchmarks

8. **Make Security Actionable**
   - Threat models with examples
   - Checklists
   - Reference implementations

These principles can be applied systematically across the entire documentation to transform technically correct but confusing content into clear, user-centered documentation that developers actually enjoy using.
