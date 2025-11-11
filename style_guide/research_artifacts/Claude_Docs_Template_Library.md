# Claude Documentation Template Library
## Ready-to-Use Templates for All Page Types

---

## Table of Contents

1. [Quickstart Guide Template](#quickstart-guide-template)
2. [Tutorial Template](#tutorial-template)
3. [API Reference Template](#api-reference-template)
4. [Troubleshooting Guide Template](#troubleshooting-guide-template)
5. [Concept/Overview Template](#conceptoverview-template)
6. [How-To Guide Template](#how-to-guide-template)
7. [Migration Guide Template](#migration-guide-template)
8. [Release Notes Template](#release-notes-template)
9. [Code Example Template](#code-example-template)
10. [Use Case Guide Template](#use-case-guide-template)

---

## How to Use These Templates

Each template includes:
- **Filled Example**: Shows best practices in action
- **Blank Template**: Ready to copy and customize
- **Required Sections**: Must include
- **Optional Sections**: Include if relevant
- **Component Usage**: Mintlify components to use

**Steps to use**:
1. Copy the blank template
2. Fill in your content following the example
3. Remove optional sections if not needed
4. Verify against style guide
5. Run docs_analyzer before publishing

---

## 1. Quickstart Guide Template

**Purpose**: Get users from zero to first success in minimum time (5-15 minutes)

**When to use**: New features, getting started with products, first-time setup

### Filled Example

```mdx
---
title: "Quickstart: Send Your First Message"
description: "Get started with Claude in 5 minutes. Install the SDK, authenticate, and send your first API request with complete code examples."
---

# Quickstart: Send Your First Message

Get started with Claude in 5 minutes. You'll install the SDK, configure authentication, and send your first API request.

## Prerequisites

Before you begin, ensure you have:
- Python 3.7+ or Node.js 18+ installed
- An [Anthropic account](https://console.anthropic.com) with API access
- 5 minutes to complete this guide

## 1. Get Your API Key

Generate an API key from your [account settings](https://console.anthropic.com/settings/keys).

<Warning>
Store your API key securely. Never commit it to version control or expose it in client-side code.
</Warning>

## 2. Install the SDK

<Tabs>
  <Tab title="Python">
    ```bash
    pip install anthropic
    ```
  </Tab>
  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/sdk
    ```
  </Tab>
</Tabs>

## 3. Set Your API Key

<Tabs>
  <Tab title="Python">
    ```bash
    export ANTHROPIC_API_KEY='your-api-key-here'
    ```
  </Tab>
  <Tab title="TypeScript">
    ```bash
    export ANTHROPIC_API_KEY='your-api-key-here'
    ```
  </Tab>
</Tabs>

## 4. Send Your First Message

Create a file with this code:

<CodeGroup>
```python quickstart.py
import anthropic
import os

# Initialize the client
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)

# Send a message
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

# Print the response
print(message.content[0].text)
```

```typescript quickstart.ts
import Anthropic from '@anthropic-ai/sdk';

// Initialize the client
const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Send a message
const message = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Hello, Claude!' }
  ],
});

// Print the response
console.log(message.content[0].text);
```
</CodeGroup>

## 5. Run Your Code

<Tabs>
  <Tab title="Python">
    ```bash
    python quickstart.py
    ```
  </Tab>
  <Tab title="TypeScript">
    ```bash
    npx ts-node quickstart.ts
    ```
  </Tab>
</Tabs>

You should see Claude's response printed to your console.

## What's Next?

Now that you've sent your first message, explore these features:

<CardGroup cols={2}>
  <Card title="Streaming Responses" icon="water" href="/en/docs/streaming">
    Display responses as they're generated
  </Card>
  <Card title="Use Tools" icon="wrench" href="/en/docs/tool-use">
    Give Claude access to external functions
  </Card>
  <Card title="Prompt Engineering" icon="pen" href="/en/docs/prompt-engineering">
    Optimize prompts for better results
  </Card>
  <Card title="Model Guide" icon="brain" href="/en/docs/models">
    Choose the right model for your use case
  </Card>
</CardGroup>

## Troubleshooting

<AccordionGroup>
  <Accordion title="I'm getting authentication errors">
    Verify your API key is set correctly:
    ```bash
    echo $ANTHROPIC_API_KEY
    ```
    If empty, set it again following step 3.
  </Accordion>
  
  <Accordion title="Import errors in Python">
    Ensure you installed the SDK:
    ```bash
    pip install anthropic --upgrade
    ```
  </Accordion>
</AccordionGroup>

## Related Pages

- [API Reference: Messages](/en/api/messages)
- [Authentication Guide](/en/docs/authentication)
- [Error Handling](/en/docs/error-handling)
```

### Blank Template

```mdx
---
title: "Quickstart: [Feature Name]"
description: "[150-160 character description of what users will accomplish and time estimate]"
---

# Quickstart: [Feature Name]

[1-2 sentence introduction explaining what users will accomplish and estimated time]

## Prerequisites

Before you begin, ensure you have:
- [Prerequisite 1]
- [Prerequisite 2]
- [Time estimate] to complete this guide

## 1. [First Step Title]

[Instructions for first step]

[Code example or UI guidance]

## 2. [Second Step Title]

[Instructions for second step]

[Code example or UI guidance]

## 3. [Third Step Title]

[Instructions for third step]

[Code example or UI guidance]

## What's Next?

Now that you've [accomplished goal], explore these features:

<CardGroup cols={2}>
  <Card title="[Next Topic 1]" icon="[icon]" href="[path]">
    [Brief description]
  </Card>
  <Card title="[Next Topic 2]" icon="[icon]" href="[path]">
    [Brief description]
  </Card>
</CardGroup>

## Troubleshooting

<AccordionGroup>
  <Accordion title="[Common Issue 1]">
    [Solution]
  </Accordion>
</AccordionGroup>

## Related Pages

- [Related Topic 1](/path)
- [Related Topic 2](/path)
```

---

## 2. Tutorial Template

**Purpose**: Teach a specific skill or build a complete project (15-60 minutes)

**When to use**: Building applications, implementing features, learning workflows

### Filled Example

```mdx
---
title: "Tutorial: Build a Customer Support Bot"
description: "Learn to build a production-ready customer support bot using Claude, tool use, and streaming. Complete tutorial with code examples and best practices."
---

# Tutorial: Build a Customer Support Bot

Learn to build a production-ready customer support bot that can answer questions, look up orders, and escalate complex issues. This tutorial covers tool use, streaming, and error handling.

**What you'll build**: A complete customer support bot with order lookup, FAQ answers, and human escalation
**Time to complete**: 45 minutes
**Skill level**: 🟡 Intermediate

## What You'll Learn

By the end of this tutorial, you'll know how to:
- Implement tool use for external data access
- Stream responses for better UX
- Handle errors gracefully
- Structure prompts for specific domains
- Deploy to production

## Prerequisites

- Python 3.9+ installed
- Anthropic API key ([get one here](https://console.anthropic.com))
- Basic understanding of REST APIs
- Familiarity with async programming (helpful but not required)

## Step 1: Project Setup

Create a new project directory and install dependencies:

```bash
mkdir support-bot
cd support-bot
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install anthropic flask
```

## Step 2: Define Tools

Create a file `tools.py` with functions Claude can call:

```python tools.py
# Tool definitions for the support bot
import json
from typing import Dict, List

def get_order_status(order_id: str) -> Dict:
    """Look up order status by ID."""
    # In production, query your database
    mock_orders = {
        "ORD-12345": {
            "status": "shipped",
            "tracking": "1Z999AA10123456784",
            "eta": "2025-11-02"
        },
        "ORD-12346": {
            "status": "processing",
            "tracking": None,
            "eta": "2025-11-05"
        }
    }
    
    return mock_orders.get(order_id, {"error": "Order not found"})

def get_faq_answer(question: str) -> str:
    """Retrieve FAQ answer for common questions."""
    faqs = {
        "return policy": "Returns accepted within 30 days with receipt.",
        "shipping time": "Standard shipping: 5-7 business days. Express: 2-3 days.",
        "international": "We ship to 50+ countries. Customs fees may apply."
    }
    
    # Simple keyword matching (use semantic search in production)
    for key, answer in faqs.items():
        if key in question.lower():
            return answer
    
    return "I don't have a specific FAQ for that question."

def escalate_to_human(reason: str, customer_email: str) -> Dict:
    """Create a ticket for human agent review."""
    # In production, integrate with your ticketing system
    ticket_id = f"TKT-{hash(customer_email) % 100000}"
    return {
        "ticket_id": ticket_id,
        "status": "created",
        "message": f"Ticket {ticket_id} created. An agent will respond within 2 hours."
    }

# Tool definitions in Claude format
TOOLS = [
    {
        "name": "get_order_status",
        "description": "Look up the current status of an order by order ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "The order ID (format: ORD-12345)"
                }
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "get_faq_answer",
        "description": "Retrieve answers to frequently asked questions",
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The customer's question"
                }
            },
            "required": ["question"]
        }
    },
    {
        "name": "escalate_to_human",
        "description": "Escalate complex issues to a human agent",
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "Why this needs human attention"
                },
                "customer_email": {
                    "type": "string",
                    "description": "Customer email for follow-up"
                }
            },
            "required": ["reason", "customer_email"]
        }
    }
]

# Map tool names to functions
TOOL_FUNCTIONS = {
    "get_order_status": get_order_status,
    "get_faq_answer": get_faq_answer,
    "escalate_to_human": escalate_to_human
}
```

<Tip>
In production, replace mock data with actual database queries and ticketing system integrations.
</Tip>

## Step 3: Implement the Bot

Create `bot.py` with the main logic:

```python bot.py
import anthropic
import os
import json
from tools import TOOLS, TOOL_FUNCTIONS

class SupportBot:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=os.environ.get("ANTHROPIC_API_KEY")
        )
        self.conversation_history = []
        
        # System prompt defining bot behavior
        self.system_prompt = """You are a helpful customer support agent for an e-commerce company.

Your role:
- Answer customer questions using available tools
- Be friendly, professional, and concise
- Look up order information when customers ask about orders
- Check FAQs for common questions
- Escalate complex issues to human agents

Guidelines:
- Always verify order IDs before lookup
- Provide clear, actionable information
- Acknowledge customer frustration empathetically
- Explain next steps clearly
"""
    
    def process_tool_calls(self, tool_uses):
        """Execute tool calls and return results."""
        tool_results = []
        
        for tool_use in tool_uses:
            tool_name = tool_use.name
            tool_input = tool_use.input
            
            # Execute the tool function
            if tool_name in TOOL_FUNCTIONS:
                try:
                    result = TOOL_FUNCTIONS[tool_name](**tool_input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": json.dumps(result)
                    })
                except Exception as e:
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tool_use.id,
                        "content": json.dumps({"error": str(e)}),
                        "is_error": True
                    })
        
        return tool_results
    
    def chat(self, user_message: str) -> str:
        """Send a message and get response, handling tool use."""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Initial request to Claude
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=2048,
                system=self.system_prompt,
                tools=TOOLS,
                messages=self.conversation_history
            )
            
            # Process tool use if present
            while response.stop_reason == "tool_use":
                # Extract tool uses from response
                tool_uses = [
                    block for block in response.content 
                    if block.type == "tool_use"
                ]
                
                # Add assistant response to history
                self.conversation_history.append({
                    "role": "assistant",
                    "content": response.content
                })
                
                # Execute tools and add results to history
                tool_results = self.process_tool_calls(tool_uses)
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
                
                # Get next response
                response = self.client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=2048,
                    system=self.system_prompt,
                    tools=TOOLS,
                    messages=self.conversation_history
                )
            
            # Extract final text response
            assistant_message = ""
            for block in response.content:
                if hasattr(block, "text"):
                    assistant_message += block.text
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except anthropic.APIError as e:
            return f"I'm experiencing technical difficulties. Please try again. (Error: {e.status_code})"
        except Exception as e:
            return f"An unexpected error occurred. Please contact support. (Error: {str(e)})"

# Example usage
if __name__ == "__main__":
    bot = SupportBot()
    
    # Test conversation
    print("Bot: Hello! How can I help you today?")
    
    test_messages = [
        "What's the status of order ORD-12345?",
        "What's your return policy?",
        "I need help with a complex billing issue"
    ]
    
    for message in test_messages:
        print(f"\nCustomer: {message}")
        response = bot.chat(message)
        print(f"Bot: {response}")
```

## Step 4: Add Streaming

Enhance the bot with streaming for better UX:

```python streaming_bot.py
def chat_stream(self, user_message: str):
    """Stream responses for real-time display."""
    self.conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        with self.client.messages.stream(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2048,
            system=self.system_prompt,
            tools=TOOLS,
            messages=self.conversation_history
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
            
            # Get final message for tool use handling
            final_message = stream.get_final_message()
            
            # Handle tool use if needed
            if final_message.stop_reason == "tool_use":
                # Process tools (non-streaming)
                # ... tool use logic from previous step
                pass
    
    except Exception as e:
        print(f"\nError: {str(e)}")
```

## Step 5: Test Your Bot

Run the bot and test various scenarios:

```bash
python bot.py
```

**Test cases to try**:
1. Order lookup: "What's my order ORD-12345 status?"
2. FAQ question: "What's your return policy?"
3. Complex issue: "I was charged twice for my order"
4. Invalid order: "Check order ABC-123"

## Step 6: Deploy to Production

<Steps>
  <Step title="Add production database">
    Replace mock data with real database queries in `tools.py`
  </Step>
  
  <Step title="Implement authentication">
    Verify customer identity before order lookups
  </Step>
  
  <Step title="Add logging and monitoring">
    Track conversations, tool usage, and errors
  </Step>
  
  <Step title="Set up rate limiting">
    Protect your API key and prevent abuse
  </Step>
  
  <Step title="Deploy to your platform">
    Use Flask/FastAPI for web, integrate with chat platforms
  </Step>
</Steps>

## Next Steps

Enhance your bot with:

<CardGroup cols={2}>
  <Card title="Conversation Memory" icon="brain" href="/en/docs/conversation-memory">
    Remember context across sessions
  </Card>
  <Card title="Prompt Caching" icon="bolt" href="/en/docs/prompt-caching">
    Reduce latency and costs
  </Card>
  <Card title="Fine-Tuning" icon="sliders" href="/en/docs/fine-tuning">
    Customize for your domain
  </Card>
  <Card title="Production Best Practices" icon="check" href="/en/docs/production">
    Security, monitoring, scaling
  </Card>
</CardGroup>

## Troubleshooting

<AccordionGroup>
  <Accordion title="Bot doesn't call tools">
    Ensure tool descriptions are clear and match user intent. Try making tool names and descriptions more specific.
  </Accordion>
  
  <Accordion title="Streaming stops mid-response">
    Check network connection and increase timeout values. Verify API key has sufficient quota.
  </Accordion>
  
  <Accordion title="High latency on tool calls">
    Tool execution happens synchronously. Consider caching common queries or pre-loading data.
  </Accordion>
</AccordionGroup>

## Complete Code

View the complete working code on [GitHub](https://github.com/anthropics/support-bot-example).

## Related Pages

- [Tool Use Documentation](/en/docs/tool-use)
- [Streaming Guide](/en/docs/streaming)
- [System Prompts](/en/docs/system-prompts)
- [Production Deployment](/en/docs/production)
```

### Blank Template

```mdx
---
title: "Tutorial: [Project Name]"
description: "[150-160 character description of what users will build and learn]"
---

# Tutorial: [Project Name]

[2-3 sentence introduction explaining what users will build and key learning outcomes]

**What you'll build**: [One sentence description]
**Time to complete**: [Minutes]
**Skill level**: [🟢 Beginner | 🟡 Intermediate | 🔴 Advanced]

## What You'll Learn

By the end of this tutorial, you'll know how to:
- [Learning objective 1]
- [Learning objective 2]
- [Learning objective 3]

## Prerequisites

- [Prerequisite 1]
- [Prerequisite 2]
- [Prerequisite 3]

## Step 1: [Step Title]

[Instructions and explanation]

[Code example]

## Step 2: [Step Title]

[Instructions and explanation]

[Code example]

## Step 3: [Step Title]

[Instructions and explanation]

[Code example]

## Step 4: [Step Title]

[Instructions and explanation]

[Code example]

## Next Steps

[Guidance on what to explore next]

## Troubleshooting

<AccordionGroup>
  <Accordion title="[Common Issue]">
    [Solution]
  </Accordion>
</AccordionGroup>

## Complete Code

[Link to complete code repository]

## Related Pages

- [Related Topic 1](/path)
- [Related Topic 2](/path)
```

---

## 3. API Reference Template

**Purpose**: Complete, precise documentation of API endpoints, parameters, and responses

**When to use**: Every API endpoint, SDK method, configuration option

### Filled Example

```mdx
---
title: "Messages API"
description: "Send messages to Claude models, receive responses, and implement streaming, tool use, and prompt caching with the Messages API."
---

# Messages API

Send messages to Claude and receive responses. The Messages API supports streaming, tool use, vision, and prompt caching.

## Endpoint

```
POST https://api.anthropic.com/v1/messages
```

## Authentication

Include your API key in the `x-api-key` header:

```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json"
```

## Request Body

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model identifier (e.g., `"claude-sonnet-4-5-20250929"`) |
| `max_tokens` | integer | Maximum tokens to generate (1-8192) |
| `messages` | array | Array of message objects with `role` and `content` |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `temperature` | float | 1.0 | Randomness (0-1). Lower is more deterministic |
| `top_p` | float | null | Nucleus sampling threshold (0-1) |
| `top_k` | integer | null | Top-k sampling |
| `system` | string | null | System prompt providing context |
| `stop_sequences` | array | null | Sequences that stop generation |
| `stream` | boolean | false | Enable streaming responses |
| `tools` | array | null | Available tools for Claude to use |
| `tool_choice` | object | null | Control tool selection behavior |

<Warning>
Don't use both `temperature` and `top_p`. Choose one sampling method.
</Warning>

### Message Format

Each message in the `messages` array must have:

```json
{
  "role": "user",  // or "assistant"
  "content": "Hello, Claude!"
}
```

**Content types supported**:
- String: Simple text
- Array: Mix of text and images for vision

## Response Format

### Success Response (200 OK)

```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello! How can I assist you today?"
    }
  ],
  "model": "claude-sonnet-4-5-20250929",
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "usage": {
    "input_tokens": 12,
    "output_tokens": 8
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique message identifier |
| `type` | string | Always `"message"` |
| `role` | string | Always `"assistant"` |
| `content` | array | Response content blocks |
| `model` | string | Model used for generation |
| `stop_reason` | string | Why generation stopped (see below) |
| `usage` | object | Token usage statistics |

### Stop Reasons

| Value | Description |
|-------|-------------|
| `end_turn` | Model completed response naturally |
| `max_tokens` | Reached `max_tokens` limit |
| `stop_sequence` | Hit a stop sequence |
| `tool_use` | Model wants to use a tool |

## Code Examples

<CodeGroup>
```python Python SDK
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

```typescript TypeScript SDK
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const message = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [
    { role: 'user', content: 'Hello, Claude!' }
  ],
});

console.log(message.content[0].text);
```

```bash cURL
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-sonnet-4-5-20250929",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello, Claude!"}
    ]
  }'
```
</CodeGroup>

## Streaming

Enable streaming to receive responses as they're generated:

<CodeGroup>
```python Python Streaming
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain quantum computing"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

```typescript TypeScript Streaming
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const stream = await client.messages.stream({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Explain quantum computing' }],
});

for await (const chunk of stream) {
  if (chunk.type === 'content_block_delta' && chunk.delta.type === 'text_delta') {
    process.stdout.write(chunk.delta.text);
  }
}
```
</CodeGroup>

[Learn more about streaming](/en/docs/streaming)

## Error Responses

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | `invalid_request_error` | Invalid request parameters |
| 401 | `authentication_error` | Invalid API key |
| 403 | `permission_error` | API key lacks permissions |
| 429 | `rate_limit_error` | Rate limit exceeded |
| 500 | `api_error` | Internal server error |
| 529 | `overloaded_error` | API temporarily overloaded |

### Error Response Format

```json
{
  "type": "error",
  "error": {
    "type": "rate_limit_error",
    "message": "Rate limit exceeded. Please try again in 60 seconds."
  }
}
```

[See complete error handling guide](/en/docs/error-handling)

## Rate Limits

Rate limits vary by usage tier:

| Tier | Requests/min | Tokens/min |
|------|--------------|------------|
| Free | 5 | 25,000 |
| Build | 50 | 100,000 |
| Scale | 1,000 | 400,000 |

[View your rate limits](https://console.anthropic.com/settings/limits)

## Best Practices

<CardGroup cols={2}>
  <Card title="Use Prompt Caching" icon="bolt">
    Cache system prompts to reduce latency and costs by up to 90%
  </Card>
  <Card title="Implement Retry Logic" icon="rotate">
    Handle rate limits with exponential backoff
  </Card>
  <Card title="Monitor Token Usage" icon="chart-line">
    Track input/output tokens to control costs
  </Card>
  <Card title="Set Timeouts" icon="clock">
    Configure appropriate timeout values for your use case
  </Card>
</CardGroup>

## Related Endpoints

- [Streaming Messages](/en/api/streaming-messages)
- [Message Batches](/en/api/message-batches)
- [Count Tokens](/en/api/count-tokens)

## SDK Documentation

- [Python SDK Reference](/en/api/python-sdk)
- [TypeScript SDK Reference](/en/api/typescript-sdk)
- [Java SDK Reference](/en/api/java-sdk)
```

### Blank Template

```mdx
---
title: "[Endpoint or Method Name]"
description: "[What this endpoint does, key features, use cases in 150-160 characters]"
---

# [Endpoint/Method Name]

[2-3 sentence introduction explaining purpose and key capabilities]

## Endpoint

```
[HTTP METHOD] [URL]
```

## Authentication

[Authentication requirements and example]

## Request Body

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `[name]` | [type] | [Description] |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `[name]` | [type] | [default] | [Description] |

## Response Format

### Success Response ([Status Code])

```json
{
  "[field]": "[value]"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `[name]` | [type] | [Description] |

## Code Examples

<CodeGroup>
```python Python
[code]
```

```typescript TypeScript
[code]
```

```bash cURL
[code]
```
</CodeGroup>

## Error Responses

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| [code] | `[type]` | [Description] |

## Related Endpoints

- [Related API 1](/path)
- [Related API 2](/path)
```

---

## 4. Troubleshooting Guide Template

**Purpose**: Help users diagnose and resolve issues systematically

**When to use**: Common errors, debugging workflows, symptom-based problem solving

### Filled Example

```mdx
---
title: "Troubleshooting: Authentication Errors"
description: "Resolve common authentication errors with Claude API including invalid API keys, permission errors, and account configuration issues."
---

# Troubleshooting: Authentication Errors

This guide helps you resolve authentication errors when using the Claude API.

## Common Symptoms

- `401 Unauthorized` errors
- `authentication_error` responses
- "Invalid API key" messages
- Requests succeed in Console but fail in code

## Quick Diagnosis

Follow this decision tree to identify your issue:

```mermaid
graph TD
    A[Authentication Error] --> B{Getting 401?}
    B -->|Yes| C{API key set?}
    B -->|No| D{Getting 403?}
    
    C -->|Yes| E{Correct format?}
    C -->|No| F[Set API key]
    
    E -->|Yes| G{Recently rotated?}
    E -->|No| H[Check format]
    
    G -->|Yes| I[Update to new key]
    G -->|No| J[Verify key in Console]
    
    D -->|Yes| K[Check permissions]
    D -->|No| L[Check other errors]
```

## Issue 1: API Key Not Set

**Symptoms**:
- `authentication_error` with "API key required"
- Works in Console, fails in code
- Environment variable not found errors

**Solution**:

<Steps>
  <Step title="Verify API key exists">
    Check your environment variable:
    ```bash
    echo $ANTHROPIC_API_KEY
    ```
    If empty, the key isn't set.
  </Step>
  
  <Step title="Set the environment variable">
    ```bash
    # Linux/Mac
    export ANTHROPIC_API_KEY='your-api-key-here'
    
    # Windows Command Prompt
    set ANTHROPIC_API_KEY=your-api-key-here
    
    # Windows PowerShell
    $env:ANTHROPIC_API_KEY="your-api-key-here"
    ```
  </Step>
  
  <Step title="Restart your application">
    Environment variables are loaded at startup. Restart your application to pick up the new value.
  </Step>
  
  <Step title="Test the connection">
    ```python
    import anthropic
    import os
    
    print(f"API Key is {'set' if os.environ.get('ANTHROPIC_API_KEY') else 'NOT set'}")
    
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=10,
        messages=[{"role": "user", "content": "Hi"}]
    )
    print("Success!")
    ```
  </Step>
</Steps>

<Tip>
For production, use a secrets manager (AWS Secrets Manager, Azure Key Vault, etc.) instead of environment variables.
</Tip>

## Issue 2: Invalid API Key Format

**Symptoms**:
- `authentication_error` with "Invalid API key format"
- Key looks correct but doesn't work

**Common causes**:
- Extra spaces or newlines in key
- Wrong key type (test vs. production)
- Corrupted clipboard paste

**Solution**:

1. **Verify key format**:
   Valid API keys start with `sk-ant-` and are 64+ characters:
   ```
   sk-ant-api03-AbCdEf1234567890...
   ```

2. **Check for hidden characters**:
   ```python
   import os
   key = os.environ.get('ANTHROPIC_API_KEY')
   print(f"Length: {len(key)}")
   print(f"Starts with 'sk-ant-': {key.startswith('sk-ant-')}")
   print(f"Has spaces: {' ' in key}")
   print(f"Has newlines: {chr(10) in key}")
   ```

3. **Regenerate the key**:
   Go to [API Keys settings](https://console.anthropic.com/settings/keys) and create a new key.

## Issue 3: API Key Expired or Rotated

**Symptoms**:
- Worked before, now getting 401
- Recent key rotation

**Solution**:

1. **Check key status in Console**:
   - Visit [API Keys page](https://console.anthropic.com/settings/keys)
   - Verify key is "Active"
   - Check last used date

2. **Generate new key if needed**:
   - Click "Create Key"
   - Update your environment variable
   - Revoke the old key

3. **Update all environments**:
   Remember to update:
   - Development environment
   - Staging servers
   - Production servers
   - CI/CD pipelines
   - Team members' local setups

## Issue 4: Permission Errors (403)

**Symptoms**:
- `permission_error` response
- "API key lacks required permissions"
- Certain endpoints work, others don't

**Solution**:

1. **Check workspace access**:
   - Verify you're in the correct workspace
   - Ensure workspace has API access enabled

2. **Review account tier**:
   Some features require higher tiers:
   | Feature | Required Tier |
   |---------|---------------|
   | Basic API access | Build+ |
   | Extended context (1M tokens) | Scale |
   | Fine-tuning | Enterprise |

3. **Verify feature flags**:
   Beta features require specific headers:
   ```python
   headers = {
       "anthropic-beta": "feature-name-2025-01-01"
   }
   ```

## Issue 5: Works in Console, Fails in Code

**Symptoms**:
- Requests succeed in API Console
- Same request fails in your code

**Debug steps**:

<Accordion title="Compare request details">
1. **Export Console request**:
   - Use "View Code" in Console
   - Copy exact headers and body

2. **Compare with your code**:
   ```python
   # Print your actual request
   print(f"Headers: {client.headers}")
   print(f"Model: {model}")
   print(f"Messages: {messages}")
   ```

3. **Common differences**:
   - Missing `anthropic-version` header
   - Different model name format
   - Incorrect message structure
   - Missing required beta headers
</Accordion>

<Accordion title="Verify network access">
1. **Test connectivity**:
   ```bash
   curl -I https://api.anthropic.com/v1/messages
   ```

2. **Check firewall rules**:
   - Allow outbound HTTPS (port 443)
   - Whitelist `api.anthropic.com`

3. **Proxy configuration**:
   ```python
   client = anthropic.Anthropic(
       proxies={
           "https": "http://proxy.company.com:8080"
       }
   )
   ```
</Accordion>

## Prevention Best Practices

<CardGroup cols={2}>
  <Card title="Secure Storage" icon="lock">
    Never commit API keys to git. Use secrets managers in production.
  </Card>
  <Card title="Key Rotation" icon="rotate">
    Rotate keys quarterly. Use multiple keys for different environments.
  </Card>
  <Card title="Error Handling" icon="shield">
    Implement retry logic with exponential backoff for transient auth errors.
  </Card>
  <Card title="Monitoring" icon="chart-line">
    Alert on authentication failures. Track key usage patterns.
  </Card>
</CardGroup>

## Still Having Issues?

If you've tried these solutions and still have authentication problems:

1. **Collect diagnostic information**:
   - Error message and status code
   - Request ID from response headers
   - Timestamp of failed request
   - SDK version and language

2. **Check system status**:
   - Visit [status.anthropic.com](https://status.anthropic.com)
   - Check for ongoing incidents

3. **Contact support**:
   - Email: [support@anthropic.com](mailto:support@anthropic.com)
   - Include diagnostic information above
   - Mention this troubleshooting guide

## Related Pages

- [Authentication Guide](/en/docs/authentication)
- [API Keys Management](/en/docs/api-keys)
- [Error Handling](/en/docs/error-handling)
- [Security Best Practices](/en/docs/security)
```

### Blank Template

```mdx
---
title: "Troubleshooting: [Issue Category]"
description: "[What issues this guide helps resolve, common symptoms, in 150-160 characters]"
---

# Troubleshooting: [Issue Category]

[Introduction explaining the types of issues covered]

## Common Symptoms

- [Symptom 1]
- [Symptom 2]
- [Symptom 3]

## Quick Diagnosis

[Decision tree or checklist to identify the issue]

## Issue 1: [Specific Problem]

**Symptoms**:
- [Symptom]
- [Symptom]

**Solution**:

<Steps>
  <Step title="[Step]">
    [Instructions]
  </Step>
</Steps>

## Issue 2: [Specific Problem]

[Follow same pattern]

## Prevention Best Practices

[How to avoid these issues]

## Still Having Issues?

[Contact information and next steps]

## Related Pages

- [Related Topic 1](/path)
- [Related Topic 2](/path)
```

---

## 5. Concept/Overview Template

**Purpose**: Explain what something is, how it works, and when to use it

**When to use**: Feature introductions, architectural explanations, conceptual foundations

### Filled Example

```mdx
---
title: "Prompt Caching"
description: "Learn how prompt caching reduces latency by up to 85% and costs by up to 90% by reusing recently processed prompts in Claude API requests."
---

# Prompt Caching

Prompt caching reduces latency by up to 85% and costs by up to 90% by reusing recently processed prompts across API requests.

## What is Prompt Caching?

When you send a request to Claude, the model processes your prompt before generating a response. Prompt caching stores the processed results of long prompts, so repeated requests with the same content skip this processing step.

**Key benefits**:
- **Lower latency**: Cached prompts process in milliseconds instead of seconds
- **Reduced costs**: Pay 90% less for cached content
- **Better UX**: Faster responses improve user experience
- **Scale efficiently**: Handle more requests with the same budget

## How It Works

```mermaid
sequenceDiagram
    participant Client
    participant Cache
    participant Claude
    
    Client->>Cache: Request with system prompt
    Cache->>Cache: Check for cached content
    alt Cache Miss
        Cache->>Claude: Process full prompt
        Claude->>Cache: Store processed result
        Cache->>Client: Response (full processing time)
    else Cache Hit
        Cache->>Client: Response (minimal processing time)
    end
```

1. **First request**: Claude processes the entire prompt. The processed result is cached for 5 minutes.
2. **Subsequent requests**: Cached portions are reused. Only new content is processed.
3. **Cache lifetime**: Caches expire after 5 minutes of inactivity. Frequent requests maintain the cache.

## When to Use Prompt Caching

Prompt caching is ideal for:

<CardGroup cols={2}>
  <Card title="Agentic Workflows" icon="robot">
    Multi-step processes with consistent system prompts and tool definitions
  </Card>
  <Card title="Large Context Applications" icon="file">
    Processing the same large documents (code repositories, books, documentation)
  </Card>
  <Card title="Conversational Agents" icon="comments">
    Chatbots with long system prompts defining personality and behavior
  </Card>
  <Card title="Coding Assistants" icon="code">
    Development tools with consistent codebase context
  </Card>
</CardGroup>

### When NOT to Use Caching

- **Single-use prompts**: Cache overhead adds latency for one-time requests
- **Frequently changing content**: Dynamic prompts invalidate caches constantly
- **Small prompts**: Benefit is minimal for short prompts (<1024 tokens)
- **User-specific content**: Don't cache PII or user data

## Implementation

Mark content for caching using `cache_control` breakpoints:

<CodeGroup>
```python Python
import anthropic

client = anthropic.Anthropic()

# Content marked for caching
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert Python developer with deep knowledge of FastAPI, SQLAlchemy, and modern Python patterns.",
            "cache_control": {"type": "ephemeral"}  # Cache this
        }
    ],
    messages=[
        {"role": "user", "content": "How do I implement pagination?"}
    ]
)
```

```typescript TypeScript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const message = await client.messages.create({
  model: 'claude-sonnet-4-5-20250929',
  max_tokens: 1024,
  system: [
    {
      type: 'text',
      text: 'You are an expert Python developer...',
      cache_control: { type: 'ephemeral' }  // Cache this
    }
  ],
  messages: [
    { role: 'user', content: 'How do I implement pagination?' }
  ]
});
```
</CodeGroup>

<Warning>
Caching is supported only on Claude Sonnet 3.5, Claude Sonnet 4, Claude Haiku 3.5, and Claude Opus 4.1.
</Warning>

## Cache Efficiency

### Understanding Cache Behavior

- **Minimum cache size**: 1024 tokens
- **Cache lifetime**: 5 minutes of inactivity
- **Pricing**: 90% discount on cached input tokens

### Optimizing Cache Hits

1. **Structure prompts consistently**:
   ```python
   # ✅ Good: Consistent structure
   system = [
       {"type": "text", "text": STATIC_INSTRUCTIONS, "cache_control": ...},
       {"type": "text", "text": CODE_CONTEXT, "cache_control": ...},
       {"type": "text", "text": dynamic_user_context}
   ]
   
   # ❌ Bad: Mixing static and dynamic
   system = f"{STATIC_INSTRUCTIONS}\n{dynamic_context}"
   ```

2. **Place dynamic content last**:
   Cache static content first, append dynamic content after cached portions.

3. **Monitor cache performance**:
   ```python
   response = client.messages.create(...)
   print(f"Cache read tokens: {response.usage.cache_read_input_tokens}")
   print(f"Cache creation tokens: {response.usage.cache_creation_input_tokens}")
   print(f"Input tokens: {response.usage.input_tokens}")
   ```

### Cost Comparison

| Scenario | Without Caching | With Caching | Savings |
|----------|----------------|--------------|---------|
| 10K token system prompt, 10 requests | $3.00 | $0.32 | 89% |
| 50K token codebase, 100 requests | $150.00 | $15.20 | 90% |
| 5K token prompt, 1 request | $0.15 | $0.15 | 0% |

## Best Practices

<AccordionGroup>
  <Accordion title="Cache expensive content">
    Prioritize caching:
    - Long system prompts
    - Large documents or code
    - Tool definitions
    - Few-shot examples
  </Accordion>
  
  <Accordion title="Structure for cache hits">
    - Put static content first
    - Use consistent formatting
    - Maintain stable token boundaries
    - Avoid minor variations
  </Accordion>
  
  <Accordion title="Monitor and optimize">
    - Track cache hit rates
    - Measure latency improvements
    - Calculate cost savings
    - Adjust strategy based on data
  </Accordion>
</AccordionGroup>

## Common Patterns

### Pattern 1: Agentic Workflow

```python
# Cache tool definitions and system prompt
system = [
    {
        "type": "text",
        "text": "You are a helpful assistant...",
        "cache_control": {"type": "ephemeral"}
    }
]

tools = [...] # Tool definitions

# Each step in workflow benefits from cache
for step in workflow:
    response = client.messages.create(
        system=system,
        tools=tools,
        messages=conversation_history + [{"role": "user", "content": step}]
    )
```

### Pattern 2: Document Q&A

```python
# Cache the document once
document_messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "document",
                "source": {"type": "base64", "media_type": "application/pdf", "data": doc_data},
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": question
            }
        ]
    }
]

# Subsequent questions reuse cached document
```

## Troubleshooting

<AccordionGroup>
  <Accordion title="Cache hit rate is low">
    - Ensure prompts are consistent (exact match required)
    - Check for dynamic timestamps or IDs in cached content
    - Verify requests occur within 5-minute cache lifetime
    - Confirm cached content exceeds 1024 tokens
  </Accordion>
  
  <Accordion title="Not seeing cost savings">
    - Check `usage` object in response for cache metrics
    - Verify you're being charged for cache creation on first request
    - Ensure subsequent requests show `cache_read_input_tokens`
    - Review billing page for cache-specific charges
  </Accordion>
</AccordionGroup>

## Learn More

<CardGroup cols={2}>
  <Card title="Pricing Details" icon="dollar" href="/en/docs/pricing">
    Complete pricing for cached vs. uncached tokens
  </Card>
  <Card title="System Prompts" icon="file-text" href="/en/docs/system-prompts">
    Best practices for system prompt engineering
  </Card>
  <Card title="Tool Use" icon="wrench" href="/en/docs/tool-use">
    Combine caching with tool use
  </Card>
  <Card title="API Reference" icon="code" href="/en/api/messages">
    Complete API documentation
  </Card>
</CardGroup>

## Related Pages

- [Prompt Engineering](/en/docs/prompt-engineering)
- [Cost Optimization](/en/docs/cost-optimization)
- [Performance Guide](/en/docs/performance)
```

### Blank Template

```mdx
---
title: "[Feature/Concept Name]"
description: "[What it is, key benefit, use case in 150-160 characters]"
---

# [Feature/Concept Name]

[1-2 sentence introduction with key benefit or definition]

## What is [Feature]?

[Detailed explanation of the concept]

**Key benefits**:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

## How It Works

[Explanation with diagram if applicable]

## When to Use [Feature]

[Use cases and scenarios]

### When NOT to Use [Feature]

[Anti-patterns and limitations]

## Implementation

[Code examples showing how to use it]

## Best Practices

[Guidelines for effective use]

## Common Patterns

[Typical usage patterns with examples]

## Troubleshooting

[Common issues and solutions]

## Learn More

[Related resources]

## Related Pages

- [Related Topic 1](/path)
- [Related Topic 2](/path)
```

---

## 6. How-To Guide Template

**Purpose**: Task-focused instructions for accomplishing a specific goal

**When to use**: Specific tasks, configuration procedures, implementation guides

### Filled Example

```mdx
---
title: "How to Implement Streaming Responses"
description: "Step-by-step guide to implement streaming responses with Claude for real-time output display, improved UX, and lower perceived latency."
---

# How to Implement Streaming Responses

Learn to implement streaming responses for real-time output display, improving user experience and perceived latency.

## Before You Begin

**You'll need**:
- Claude SDK installed (Python or TypeScript)
- API key configured
- Basic understanding of async programming

**Time to complete**: 15 minutes

## Overview

Streaming sends response tokens as they're generated instead of waiting for the complete response. This improves:
- **Perceived latency**: Users see output immediately
- **User experience**: Progress indication for long responses
- **Interactivity**: Enable stop/pause functionality

## Step 1: Enable Streaming

Streaming is enabled via the SDK's stream methods:

<Tabs>
  <Tab title="Python">
    ```python
    import anthropic
    
    client = anthropic.Anthropic()
    
    # Use messages.stream() instead of messages.create()
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Explain Python decorators"}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    ```
  </Tab>
  
  <Tab title="TypeScript">
    ```typescript
    import Anthropic from '@anthropic-ai/sdk';
    
    const client = new Anthropic();
    
    // Use messages.stream()
    const stream = await client.messages.stream({
      model: 'claude-sonnet-4-5-20250929',
      max_tokens: 1024,
      messages: [{ role: 'user', content: 'Explain Python decorators' }],
    });
    
    for await (const chunk of stream) {
      if (chunk.type === 'content_block_delta' && 
          chunk.delta.type === 'text_delta') {
        process.stdout.write(chunk.delta.text);
      }
    }
    ```
  </Tab>
</Tabs>

<Tip>
The `flush=True` parameter in Python ensures output displays immediately instead of buffering.
</Tip>

## Step 2: Handle Stream Events

Streaming emits different event types. Handle each appropriately:

```python
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a poem about coding"}]
) as stream:
    # Handle different event types
    for event in stream:
        if event.type == "message_start":
            print(f"Message ID: {event.message.id}")
        
        elif event.type == "content_block_start":
            print(f"\nContent block {event.index} started")
        
        elif event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
        
        elif event.type == "content_block_stop":
            print(f"\nContent block {event.index} finished")
        
        elif event.type == "message_delta":
            print(f"\nStop reason: {event.delta.stop_reason}")
        
        elif event.type == "message_stop":
            print("\nMessage complete")
```

### Event Types

| Event | Description | When to Handle |
|-------|-------------|----------------|
| `message_start` | Stream begins | Initialize UI, log request |
| `content_block_start` | New content block | Handle multiple response parts |
| `content_block_delta` | Incremental content | Display to user |
| `content_block_stop` | Content block ends | Finalize block display |
| `message_delta` | Message metadata | Check stop reason |
| `message_stop` | Stream complete | Cleanup, finalize |

## Step 3: Add Error Handling

Always handle streaming errors gracefully:

```python
import anthropic

client = anthropic.Anthropic()

try:
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            
except anthropic.APIStatusError as e:
    print(f"\nAPI error: {e.status_code} - {e.message}")
    
except anthropic.APITimeoutError as e:
    print("\nRequest timed out. Please try again.")
    
except Exception as e:
    print(f"\nUnexpected error: {str(e)}")
```

<Warning>
Network interruptions during streaming can cause incomplete responses. Always implement error handling and consider retry logic.
</Warning>

## Step 4: Implement in Web Applications

### Backend (Flask Example)

```python
from flask import Flask, Response, stream_with_context
import anthropic

app = Flask(__name__)
client = anthropic.Anthropic()

@app.route('/stream')
def stream():
    def generate():
        with client.messages.stream(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": "Explain AI"}]
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {text}\n\n"
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream'
    )
```

### Frontend (JavaScript)

```javascript
const eventSource = new EventSource('/stream');

eventSource.onmessage = (event) => {
  // Append each chunk to the display
  document.getElementById('response').textContent += event.data;
};

eventSource.onerror = (error) => {
  console.error('Stream error:', error);
  eventSource.close();
};
```

## Step 5: Optimize Performance

### Buffer Management

Balance responsiveness with efficiency:

```python
def stream_with_buffering(stream, buffer_size=10):
    """Buffer tokens for more efficient updates"""
    buffer = []
    
    for text in stream.text_stream:
        buffer.append(text)
        
        if len(buffer) >= buffer_size:
            yield ''.join(buffer)
            buffer = []
    
    # Flush remaining buffer
    if buffer:
        yield ''.join(buffer)

# Usage
with client.messages.stream(...) as stream:
    for chunk in stream_with_buffering(stream):
        print(chunk, end="", flush=True)
```

### Timeout Configuration

```python
client = anthropic.Anthropic(
    timeout=30.0,  # 30 second timeout
    max_retries=2   # Retry on transient failures
)
```

## Step 6: Handle Tool Use with Streaming

When using tools, streaming pauses for tool execution:

```python
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    tools=[...],
    messages=[...]
) as stream:
    for event in stream:
        if event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
        
        elif event.type == "content_block_start":
            if event.content_block.type == "tool_use":
                print(f"\n[Using tool: {event.content_block.name}]")
    
    # Get final message to process tool uses
    final_message = stream.get_final_message()
    
    if final_message.stop_reason == "tool_use":
        # Process tool uses (non-streaming)
        tool_results = process_tools(final_message)
        
        # Continue with another streaming request
        with client.messages.stream(
            messages=conversation_history + [
                {"role": "assistant", "content": final_message.content},
                {"role": "user", "content": tool_results}
            ]
        ) as continued_stream:
            for text in continued_stream.text_stream:
                print(text, end="", flush=True)
```

## Testing Your Implementation

Verify streaming works correctly:

```python
def test_streaming():
    """Test streaming implementation"""
    client = anthropic.Anthropic()
    
    # Test 1: Basic streaming
    print("Test 1: Basic streaming")
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=50,
        messages=[{"role": "user", "content": "Count to 10"}]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print("\n✓ Basic streaming works\n")
    
    # Test 2: Error handling
    print("Test 2: Error handling")
    try:
        with client.messages.stream(
            model="invalid-model",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        ) as stream:
            for text in stream.text_stream:
                print(text, end="")
    except anthropic.APIStatusError as e:
        print(f"✓ Caught error correctly: {e.status_code}\n")
    
    # Test 3: Stream interruption
    print("Test 3: Stream interruption")
    with client.messages.stream(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1000,
        messages=[{"role": "user", "content": "Write a long story"}]
    ) as stream:
        count = 0
        for text in stream.text_stream:
            print(text, end="", flush=True)
            count += len(text)
            if count > 100:  # Stop early
                break
    print("\n✓ Can interrupt stream\n")

if __name__ == "__main__":
    test_streaming()
```

## Best Practices

<CardGroup cols={2}>
  <Card title="Display Progress" icon="spinner">
    Show loading indicators while waiting for first tokens
  </Card>
  <Card title="Enable Stop" icon="stop">
    Let users stop generation if response goes off-track
  </Card>
  <Card title="Buffer Wisely" icon="memory">
    Balance update frequency with performance
  </Card>
  <Card title="Handle Interruptions" icon="circle-exclamation">
    Gracefully recover from network issues
  </Card>
</CardGroup>

## Common Issues

<AccordionGroup>
  <Accordion title="Buffering delays output">
    **Problem**: Output appears in large chunks instead of smoothly.
    
    **Solution**: Use `flush=True` in Python or ensure your web server supports Server-Sent Events properly.
  </Accordion>
  
  <Accordion title="Stream disconnects randomly">
    **Problem**: Stream stops mid-response without clear error.
    
    **Solution**: 
    - Increase timeout values
    - Check network stability
    - Implement retry logic with exponential backoff
  </Accordion>
  
  <Accordion title="High memory usage">
    **Problem**: Streaming long responses causes memory issues.
    
    **Solution**:
    - Process chunks immediately instead of accumulating
    - Limit max_tokens for expected response length
    - Implement pagination for very long outputs
  </Accordion>
</AccordionGroup>

## Next Steps

<CardGroup cols={3}>
  <Card title="Prompt Caching" icon="bolt" href="/en/docs/prompt-caching">
    Reduce streaming latency further
  </Card>
  <Card title="Tool Use" icon="wrench" href="/en/docs/tool-use">
    Combine streaming with tools
  </Card>
  <Card title="Production Guide" icon="check" href="/en/docs/production">
    Deploy streaming to production
  </Card>
</CardGroup>

## Related Pages

- [Messages API Reference](/en/api/messages)
- [Error Handling](/en/docs/error-handling)
- [Performance Optimization](/en/docs/performance)
```

### Blank Template

```mdx
---
title: "How to [Task]"
description: "[What users will accomplish, key benefits, in 150-160 characters]"
---

# How to [Task]

[Brief introduction explaining what users will accomplish and why]

## Before You Begin

**You'll need**:
- [Requirement 1]
- [Requirement 2]

**Time to complete**: [Minutes]

## Overview

[Brief explanation of the approach and benefits]

## Step 1: [First Step]

[Instructions]

[Code example]

## Step 2: [Second Step]

[Instructions]

[Code example]

## Step 3: [Third Step]

[Instructions]

[Code example]

## Testing Your Implementation

[How to verify it works]

## Best Practices

[Guidelines for optimal use]

## Common Issues

<AccordionGroup>
  <Accordion title="[Issue]">
    [Solution]
  </Accordion>
</AccordionGroup>

## Next Steps

[What to learn or implement next]

## Related Pages

- [Related Topic 1](/path)
- [Related Topic 2](/path)
```

---

## 7. Migration Guide Template

**Purpose**: Help users transition from one version, product, or approach to another

**When to use**: Version upgrades, platform migrations, deprecation notices

### Filled Example

```mdx
---
title: "Migration Guide: Claude 3.5 to Claude 4"
description: "Migrate from Claude 3.5 to Claude 4 with this comprehensive guide covering API changes, prompt updates, and new features."
---

# Migration Guide: Claude 3.5 to Claude 4

Update your applications to Claude 4 to access improved performance, new features, and better capabilities.

## Overview

**Migration difficulty**: 🟢 Low
**Estimated time**: 30-60 minutes
**Breaking changes**: Minimal

<Warning>
Claude 3.5 will be deprecated on July 1, 2026. Plan your migration accordingly.
</Warning>

## What's New in Claude 4

| Feature | Claude 3.5 | Claude 4 |
|---------|------------|----------|
| Context window | 200K tokens | 200K-1M tokens |
| Extended thinking | Not available | Available |
| Computer use | Beta | Generally available |
| Agent performance | Good | Excellent |
| Code generation | Strong | State-of-the-art |

## Migration Checklist

<Steps>
  <Step title="Review changes">
    Read this complete guide to understand all changes
  </Step>
  
  <Step title="Update model identifiers">
    Change model names in your code
  </Step>
  
  <Step title="Test in development">
    Verify functionality with new models
  </Step>
  
  <Step title="Update prompts if needed">
    Optimize prompts for Claude 4 improvements
  </Step>
  
  <Step title="Deploy to staging">
    Test with production-like workloads
  </Step>
  
  <Step title="Monitor and roll out">
    Gradual rollout with monitoring
  </Step>
</Steps>

## Step 1: Update Model Identifiers

Change your model identifiers to Claude 4 versions:

<Tabs>
  <Tab title="Python">
    ```python
    # Before (Claude 3.5)
    message = client.messages.create(
        model="claude-3-5-sonnet-20250622",
        # ...
    )
    
    # After (Claude 4)
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",  # New identifier
        # ...
    )
    ```
  </Tab>
  
  <Tab title="TypeScript">
    ```typescript
    // Before (Claude 3.5)
    const message = await client.messages.create({
      model: 'claude-3-5-sonnet-20250622',
      // ...
    });
    
    // After (Claude 4)
    const message = await client.messages.create({
      model: 'claude-sonnet-4-5-20250929',  // New identifier
      // ...
    });
    ```
  </Tab>
</Tabs>

### Model Name Mapping

| Claude 3.5 Model | Claude 4 Equivalent |
|------------------|---------------------|
| `claude-3-5-sonnet-20250622` | `claude-sonnet-4-5-20250929` |
| `claude-3-5-haiku-20250307` | `claude-haiku-4-5-20250929` |
| `claude-3-opus-20240229` | `claude-opus-4-1-20250929` |

<Tip>
Use model aliases for easier migrations: `claude-sonnet-4-5` automatically points to the latest version.
</Tip>

## Step 2: Update SDK Version

Ensure you're using a compatible SDK version:

```bash
# Python
pip install --upgrade anthropic

# TypeScript
npm update @anthropic-ai/sdk

# Verify version
pip show anthropic  # Should be 0.40.0+
npm list @anthropic-ai/sdk  # Should be 0.30.0+
```

## Step 3: Handle Extended Context (Optional)

Claude 4 supports up to 1M token context with a beta header:

```python
# Enable extended context
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    messages=[...],
    extra_headers={
        "anthropic-beta": "context-1m-2025-08-07"
    }
)
```

<Info>
Extended context (200K+ tokens) uses different pricing. See [pricing page](/en/docs/pricing) for details.
</Info>

## Step 4: Adopt Extended Thinking (Optional)

Claude 4 introduces extended thinking for complex reasoning:

```python
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=4096,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Tokens for reasoning
    },
    messages=[
        {"role": "user", "content": "Solve this complex math problem..."}
    ]
)

# Access thinking process
for block in message.content:
    if block.type == "thinking":
        print(f"Thinking: {block.thinking}")
    elif block.type == "text":
        print(f"Answer: {block.text}")
```

[Learn more about extended thinking](/en/docs/extended-thinking)

## Step 5: Update Prompts for Better Performance

Claude 4 benefits from updated prompt patterns:

### Before (Claude 3.5)
```python
prompt = """You are a helpful assistant. Please analyze this data and provide insights.

Data: {data}

Provide your analysis."""
```

### After (Claude 4)
```python
prompt = """Analyze the following data and identify key trends, anomalies, and actionable insights.

Data: {data}

Structure your analysis:
1. Key findings
2. Notable patterns or anomalies
3. Recommended actions

Be specific and data-driven."""
```

**Key improvements**:
- ✅ More specific instructions
- ✅ Clear structure expectations
- ✅ Emphasis on data-driven analysis
- ✅ Action-oriented output

## Step 6: Test Behavioral Changes

Test these areas where behavior may differ:

### 1. Response Length
Claude 4 may generate longer, more thorough responses:

```python
# May need to adjust max_tokens
message = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2048,  # Increased from 1024
    messages=[...]
)
```

### 2. Reasoning Depth
Claude 4 provides deeper analysis. Adjust prompts if responses are too detailed:

```python
# Add conciseness instruction if needed
prompt = """Provide a concise analysis (under 200 words) of...

{content}"""
```

### 3. Code Generation
Claude 4 generates more complete code with better error handling:

```python
# Test generated code more thoroughly
# May include more edge case handling
```

## Step 7: Update Tool Definitions (If Applicable)

Tool use syntax remains the same, but Claude 4 is better at:
- Choosing appropriate tools
- Handling complex tool orchestration
- Error recovery

No code changes needed, but you may see improved tool usage.

## Step 8: Monitor Performance

After migration, monitor these metrics:

| Metric | What to Watch |
|--------|---------------|
| **Latency** | May improve with Claude 4's efficiency |
| **Token usage** | May increase slightly with more thorough responses |
| **Error rates** | Should remain stable or decrease |
| **Output quality** | User feedback and satisfaction scores |

## Rollback Procedure

If you need to rollback to Claude 3.5:

<Steps>
  <Step title="Revert model identifiers">
    Change model names back to Claude 3.5 versions
  </Step>
  
  <Step title="Remove new features">
    Remove extended thinking or extended context usage
  </Step>
  
  <Step title="Deploy previous version">
    Deploy your last working configuration
  </Step>
  
  <Step title="Investigate issues">
    Document problems for resolution
  </Step>
</Steps>

## Cost Implications

### Pricing Comparison

| Model | Input (per MTok) | Output (per MTok) |
|-------|------------------|-------------------|
| Claude 3.5 Sonnet | $3.00 | $15.00 |
| Claude Sonnet 4.5 | $3.00 | $15.00 |
| Claude 4 Extended (>200K) | $12.00 | $60.00 |

**Key points**:
- Standard context pricing unchanged
- Extended context (200K+) costs more
- Extended thinking uses additional tokens

[View complete pricing](/en/docs/pricing)

## Breaking Changes

<Warning>
Review these potential breaking changes:
</Warning>

### None for Standard Usage

Claude 4 maintains API compatibility with Claude 3.5. No breaking changes for standard usage.

### Optional Feature Additions

New optional features (extended thinking, extended context) require opt-in headers. Existing code works without changes.

## Common Migration Issues

<AccordionGroup>
  <Accordion title="'Model not found' error">
    **Cause**: Using Claude 3.5 model name with old SDK version
    
    **Solution**: Upgrade SDK to latest version
  </Accordion>
  
  <Accordion title="Responses are too long">
    **Cause**: Claude 4 provides more thorough responses
    
    **Solution**: 
    - Add conciseness instructions to prompts
    - Reduce max_tokens if needed
    - Request specific response length
  </Accordion>
  
  <Accordion title="Unexpected billing increases">
    **Cause**: Extended context or thinking enabled unintentionally
    
    **Solution**: Review for extended context headers or thinking parameters
  </Accordion>
</AccordionGroup>

## Migration Examples

### Complete Before/After

<Tabs>
  <Tab title="Python">
    ```python
    # Before: Claude 3.5
    import anthropic
    import os
    
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20250622",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "Explain quantum computing"}
        ]
    )
    
    print(message.content[0].text)
    
    # After: Claude 4
    import anthropic
    import os
    
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    
    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",  # Updated
        max_tokens=2048,  # Increased for more thorough responses
        messages=[
            {"role": "user", "content": "Explain quantum computing"}
        ]
    )
    
    print(message.content[0].text)
    ```
  </Tab>
  
  <Tab title="TypeScript">
    ```typescript
    // Before: Claude 3.5
    import Anthropic from '@anthropic-ai/sdk';
    
    const client = new Anthropic();
    
    const message = await client.messages.create({
      model: 'claude-3-5-sonnet-20250622',
      max_tokens: 1024,
      messages: [
        { role: 'user', content: 'Explain quantum computing' }
      ],
    });
    
    console.log(message.content[0].text);
    
    // After: Claude 4
    import Anthropic from '@anthropic-ai/sdk';
    
    const client = new Anthropic();
    
    const message = await client.messages.create({
      model: 'claude-sonnet-4-5-20250929',  // Updated
      max_tokens: 2048,  // Increased
      messages: [
        { role: 'user', content: 'Explain quantum computing' }
      ],
    });
    
    console.log(message.content[0].text);
    ```
  </Tab>
</Tabs>

## Need Help?

<CardGroup cols={2}>
  <Card title="Migration Support" icon="headset" href="mailto:support@anthropic.com">
    Email support for migration assistance
  </Card>
  <Card title="Developer Discord" icon="discord" href="https://discord.gg/anthropic">
    Community support and discussion
  </Card>
  <Card title="API Reference" icon="code" href="/en/api/messages">
    Complete API documentation
  </Card>
  <Card title="Pricing Calculator" icon="calculator" href="/en/pricing">
    Estimate migration costs
  </Card>
</CardGroup>

## Related Pages

- [Claude 4 Release Notes](/en/docs/release-notes/claude-4)
- [Extended Thinking Guide](/en/docs/extended-thinking)
- [Model Comparison](/en/docs/models/comparison)
- [Pricing](/en/docs/pricing)
```

### Blank Template

```mdx
---
title: "Migration Guide: [From] to [To]"
description: "[What's changing, migration difficulty, benefits in 150-160 characters]"
---

# Migration Guide: [From] to [To]

[Introduction explaining what's changing and why to migrate]

## Overview

**Migration difficulty**: [🟢 Low | 🟡 Medium | 🔴 High]
**Estimated time**: [Time estimate]
**Breaking changes**: [Yes/No/Minimal]

## What's New

[Comparison table or list of key changes]

## Migration Checklist

<Steps>
  <Step title="[Step]">
    [Instructions]
  </Step>
</Steps>

## Step 1: [Migration Step]

[Detailed instructions with before/after code examples]

## Step 2: [Migration Step]

[Continue for each major step]

## Rollback Procedure

[How to revert if needed]

## Breaking Changes

[List any breaking changes with solutions]

## Common Migration Issues

<AccordionGroup>
  <Accordion title="[Issue]">
    [Solution]
  </Accordion>
</AccordionGroup>

## Need Help?

[Support resources]

## Related Pages

- [Related Topic 1](/path)
- [Related Topic 2](/path)
```

---

## 8. Release Notes Template

**Purpose**: Announce new features, changes, and fixes in product releases

**When to use**: Version releases, feature launches, updates

### Filled Example

```mdx
---
title: "Release Notes: Claude Code v2.5"
description: "Claude Code v2.5 brings improved context awareness, faster performance, new agent skills, and enhanced VS Code integration."
---

# Release Notes: Claude Code v2.5

**Released**: October 29, 2025
**Version**: 2.5.0

Claude Code v2.5 brings improved context awareness, faster performance, and new capabilities for autonomous coding.

## What's New

### 🚀 Major Features

#### Enhanced Context Awareness
Claude Code now maintains better context across multi-file edits and complex refactoring tasks. The system automatically tracks related files and suggests relevant context when making changes.

**Benefits**:
- 40% improvement in cross-file refactoring accuracy
- Automatic detection of affected test files
- Smart import management

```bash
# Example: Refactoring now automatically updates imports
claude refactor rename_function --from calculateTotal --to computeSum
# Automatically updates all imports and references across the project
```

#### New Agent Skills

Three new Agent Skills expand Claude Code's capabilities:

1. **Database Migration Skill**: Generate and validate database migration scripts
2. **API Testing Skill**: Create comprehensive API test suites
3. **Performance Profiling Skill**: Analyze and suggest performance optimizations

[Learn about Agent Skills](/en/docs/claude-code/agent-skills)

#### Improved VS Code Integration

Native VS Code extension improvements:
- Inline code suggestions
- One-click test generation
- Integrated terminal commands
- Custom keyboard shortcuts

### âœ¨ Enhancements

| Feature | Improvement |
|---------|-------------|
| **Response Speed** | 25% faster for typical coding tasks |
| **Token Efficiency** | 30% reduction in token usage via prompt caching |
| **Error Recovery** | Better handling of network interruptions |
| **Multi-file Edits** | Support for 50+ simultaneous file changes |

### 🐛 Bug Fixes

- Fixed: Incorrect line numbers in diff output (#3421)
- Fixed: Memory leak in long-running sessions (#3398)
- Fixed: Git integration issues with worktrees (#3365)
- Fixed: Unicode handling in file paths (#3342)
- Fixed: Timeout errors on large file operations (#3289)

### 🔄 Changed

<Warning>
**Breaking Change**: The `--no-verify` flag has been removed. Pre-commit hooks now always run.
</Warning>

- `claude-code` command now defaults to interactive mode
- Configuration file format updated to YAML (old format still supported)
- Minimum Node.js version: 18+ (previously 16+)

### ⚠️ Deprecated

The following features are deprecated and will be removed in v3.0:

| Feature | Replacement | Removal Date |
|---------|-------------|--------------|
| `ClaudeCodeOptions` | `ClaudeAgentOptions` | March 2026 |
| `--legacy-mode` flag | Native mode | January 2026 |
| JSON config files | YAML config files | June 2026 |

### 🔐 Security Updates

- Updated authentication flow with enhanced security
- Improved API key storage encryption
- Added audit logging for sensitive operations

## Upgrade Instructions

<Steps>
  <Step title="Update Claude Code">
    ```bash
    npm update -g @anthropic-ai/claude-code
    ```
  </Step>
  
  <Step title="Verify installation">
    ```bash
    claude --version
    # Should show: 2.5.0
    ```
  </Step>
  
  <Step title="Update configuration (if needed)">
    Convert JSON config to YAML:
    ```bash
    claude config migrate
    ```
  </Step>
  
  <Step title="Test in your project">
    ```bash
    claude test --dry-run
    ```
  </Step>
</Steps>

### Migration from v2.4

Most changes are backward compatible. Key actions:

1. **Replace `ClaudeCodeOptions`** with `ClaudeAgentOptions` in SDK code
2. **Remove `--no-verify` flags** from scripts (no longer supported)
3. **Update Node.js** to 18+ if still on 16

<Tip>
Run `claude migrate` for automated migration assistance.
</Tip>

## Known Issues

| Issue | Workaround | Tracking |
|-------|------------|----------|
| Slow performance on Windows with large repos | Use WSL2 | #3456 |
| VS Code extension doesn't activate on ARM Linux | Manual activation required | #3445 |

## Feedback

We'd love to hear your thoughts on v2.5:

- [Report bugs](https://github.com/anthropics/claude-code/issues)
- [Request features](https://github.com/anthropics/claude-code/discussions)
- [Join Discord](https://discord.gg/anthropic) for community support

## What's Next

Coming in v2.6 (planned for December 2025):
- Multi-agent collaboration
- Enhanced debugging capabilities
- Custom skill marketplace
- Improved prompt caching

[View roadmap](/en/docs/claude-code/roadmap)

## Related Pages

- [Claude Code Overview](/en/docs/claude-code/overview)
- [Agent Skills Guide](/en/docs/claude-code/agent-skills)
- [VS Code Extension](/en/docs/claude-code/vs-code)
- [Migration Guide v2.4 → v2.5](/en/docs/claude-code/migration-v2-5)
```

### Blank Template

```mdx
---
title: "Release Notes: [Product Version]"
description: "[Key features and improvements in 150-160 characters]"
---

# Release Notes: [Product Version]

**Released**: [Date]
**Version**: [Version number]

[Brief summary of release highlights]

## What's New

### 🚀 Major Features

#### [Feature Name]

[Description and benefits]

[Code example or usage]

### âœ¨ Enhancements

| Feature | Improvement |
|---------|-------------|
| [Feature] | [Improvement description] |

### 🐛 Bug Fixes

- Fixed: [Issue description] (#ticket)
- Fixed: [Issue description] (#ticket)

### 🔄 Changed

[Changes to existing behavior]

### ⚠️ Deprecated

[Deprecated features and timeline]

### 🔐 Security Updates

[Security improvements]

## Upgrade Instructions

<Steps>
  <Step title="[Step]">
    [Instructions]
  </Step>
</Steps>

## Known Issues

| Issue | Workaround | Tracking |
|-------|------------|----------|
| [Issue] | [Workaround] | [Link] |

## Feedback

[How to provide feedback]

## What's Next

[Upcoming features]

## Related Pages

- [Related Topic 1](/path)
- [Related Topic 2](/path)
```

---

## 9. Code Example Template

**Purpose**: Standalone, reusable code examples for common tasks

**When to use**: Example libraries, code snippets, cookbook entries

### Structure

```markdown
# [Example Name]

**Use case**: [What this example demonstrates]
**Complexity**: [🟢 Beginner | 🟡 Intermediate | 🔴 Advanced]
**Time to adapt**: [Minutes]

## What This Example Does

[2-3 sentences explaining the example's purpose and key concepts demonstrated]

## Prerequisites

- [Requirement 1]
- [Requirement 2]

## Complete Code

[Full, working code example with comments]

## Key Concepts

- **[Concept 1]**: [Brief explanation]
- **[Concept 2]**: [Brief explanation]

## How to Adapt

1. [Adaptation step 1]
2. [Adaptation step 2]

## Related Examples

- [Related example 1]
- [Related example 2]
```

---

## 10. Use Case Guide Template

**Purpose**: Show how to solve real business problems with Claude

**When to use**: Industry-specific guides, solution templates, use case showcases

### Structure

```mdx
---
title: "[Use Case]: [Solution]"
description: "[Industry/problem, solution approach, key benefit in 150-160 characters]"
---

# [Use Case]: [Solution]

[Introduction explaining the business problem and solution approach]

## Business Challenge

[Detailed explanation of the problem companies face]

## Solution Overview

[High-level explanation of how Claude solves this]

## Implementation

[Step-by-step implementation with code]

## Results and Benefits

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| [Metric] | [Value] | [Value] | [%] |

## Real-World Example

[Customer story or detailed example]

## Scaling to Production

[Considerations for production deployment]

## ROI Calculator

[Tool or framework to calculate business value]

## Related Use Cases

- [Related use case 1]
- [Related use case 2]
```

---

## Usage Guidelines

### Choosing the Right Template

| Content Need | Use This Template |
|--------------|-------------------|
| Get user started quickly | Quickstart Guide |
| Teach a complete skill/project | Tutorial |
| Document API/SDK details | API Reference |
| Help users fix problems | Troubleshooting Guide |
| Explain concepts | Concept/Overview |
| Show how to do specific task | How-To Guide |
| Guide version transitions | Migration Guide |
| Announce releases | Release Notes |
| Provide reusable code | Code Example |
| Demonstrate business solutions | Use Case Guide |

### Template Modification

Feel free to adapt templates:
- **Add sections** relevant to your content
- **Remove optional sections** if not applicable
- **Combine templates** for complex pages
- **Maintain consistency** with style guide

### Quality Checklist

Before publishing, verify:
- [ ] Used appropriate template
- [ ] All required sections present
- [ ] Code examples tested and working
- [ ] Links verified
- [ ] Frontmatter complete
- [ ] Follows style guide
- [ ] Reviewed by peer
- [ ] Passes docs_analyzer checks

---

## Getting Help

**Questions about templates?**
- Consult the [Core Style Guide](/path/to/style-guide)
- Ask in #documentation Slack channel
- Contact senior technical writer

**Found an issue with a template?**
- Submit PR with improvements
- Discuss in style guide meetings
- Document exceptions needed

---

**Remember**: Templates are starting points, not straitjackets. Adapt them to serve your users' needs while maintaining consistency with the style guide.
