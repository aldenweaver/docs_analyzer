# MCP Documentation Reorganization: Detailed Mockup
## Proposed New Information Architecture

This document shows the complete proposed structure for reorganizing MCP documentation, including page-by-page outlines and navigation flow.

---

## Current Problems (Summary)

1. **Fragmentation:** MCP documented in 7+ locations
2. **Thin entry point:** Main page is 32 lines (just a router)
3. **Overwhelming detail:** Claude Code MCP page is 1,270 lines
4. **Split platforms:** Support site vs docs site
5. **Contradictions:** Platform availability differs across pages
6. **Missing integration:** No cross-product guidance

---

## Proposed New Structure

```
/en/docs/mcp/ (MCP Documentation Hub)
├── overview.mdx (NEW - comprehensive overview)
├── getting-started.mdx (NEW - 5-minute quickstart)
├── comparison.mdx (NEW - feature matrix)
│
├── integration-guides/ (Reorganized)
│   ├── messages-api.mdx (moved from /en/docs/agents-and-tools/)
│   ├── claude-code/
│   │   ├── overview.mdx (split from mega-page)
│   │   ├── installation.mdx (split from mega-page)
│   │   ├── server-catalog.mdx (split from mega-page)
│   │   └── enterprise.mdx (split from mega-page)
│   ├── claude-ai.mdx (migrated from support site)
│   └── claude-desktop.mdx (migrated from support site)
│
├── advanced/
│   ├── building-servers.mdx (NEW)
│   ├── security.mdx (NEW - consolidated)
│   ├── enterprise-deployment.mdx (NEW)
│   └── migration-guides.mdx (NEW)
│
└── reference/
    ├── glossary.mdx
    ├── troubleshooting.mdx (NEW)
    └── faq.mdx (NEW)
```

---

## Detailed Page Outlines

### 1. `/en/docs/mcp/overview.mdx` (NEW)

**Purpose:** Comprehensive introduction to MCP across all Anthropic products

**Estimated length:** ~800 lines (vs current 32)

**Outline:**

```markdown
# Model Context Protocol (MCP)

Connect Claude to any tool, database, or API using an open standard.

## What is MCP?

[Current USB-C analogy, expanded]
[Visual architecture diagram showing MCP flow]

## How MCP works

### The MCP architecture

```
┌─────────────┐      ┌─────────────┐      ┌──────────────┐
│   Claude    │◄────►│ MCP Server  │◄────►│ External Tool│
│  (Client)   │      │  (Adapter)  │      │  (Database)  │
└─────────────┘      └─────────────┘      └──────────────┘
```

### Three key components

1. **MCP Client** (Claude in various products)
2. **MCP Server** (Adapter that speaks MCP protocol)
3. **External Resource** (Your tool/database/API)

[Explain each with examples]

## MCP across Anthropic products

### Feature comparison matrix

| Feature | Messages API | Claude Code | Claude.ai | Claude Desktop |
|---------|--------------|-------------|-----------|----------------|
| HTTP Servers | ✅ Beta | ✅ Stable | ✅ | ✅ |
| SSE Servers | ❌ | ⚠️ Deprecated | ❌ | ❌ |
| Stdio Servers | ❌ | ✅ | ❌ | ✅ |
| OAuth | ✅ | ✅ | ✅ | ✅ |
| Enterprise Config | ⚠️ Limited | ✅ Full | ✅ Full | ⚠️ Limited |
| Resources | ✅ | ✅ | ✅ | ✅ |
| Prompts | ✅ | ✅ | ✅ | ✅ |
| Tools | ✅ | ✅ | ✅ | ✅ |

### When to use which product

**Use Messages API MCP Connector when:**
- Building production applications
- Need programmatic control
- Integrating into existing services
- Want API-first approach

**Use Claude Code MCP when:**
- Developing in terminal
- Need local file access
- Building dev workflows
- Want CLI integration

**Use Claude.ai MCP when:**
- Individual productivity
- Web-based workflows
- No coding required
- Team collaboration

**Use Claude Desktop MCP when:**
- Desktop application user
- Want local servers
- Need native app integration
- Using macOS/Windows

## Popular MCP servers

[Top 10 servers with one-liner descriptions]
[Links to detailed catalog]

## Quick start

Choose your product and follow the 5-minute guide:
[Cards linking to getting-started page with product selection]

## Architecture deep-dive

[Detailed explanation of MCP protocol]
[Transport types explained]
[Security model]

## Use cases

### Database integration
[Example: Connect to PostgreSQL]

### Project management
[Example: Jira integration]

### Developer tools
[Example: GitHub integration]

## Security considerations

[High-level security overview]
[Link to detailed security page]

## Next steps

- [Get started in 5 minutes](/en/docs/mcp/getting-started)
- [Browse MCP server catalog](/en/docs/mcp/integration-guides/claude-code/server-catalog)
- [Build your own MCP server](/en/docs/mcp/advanced/building-servers)
- [Read external protocol docs](https://modelcontextprotocol.io)
```

---

### 2. `/en/docs/mcp/getting-started.mdx` (NEW)

**Purpose:** Universal getting-started guide with product selection

**Estimated length:** ~400 lines

**Outline:**

```markdown
# Get Started with MCP in 5 Minutes

## Step 1: Choose your product

<Tabs>
  <Tab title="Messages API">
    I'm building an application using the Claude API
    → Follow API integration guide
  </Tab>

  <Tab title="Claude Code">
    I'm using the terminal/CLI for development
    → Follow CLI setup
  </Tab>

  <Tab title="Claude.ai">
    I'm using Claude in my web browser
    → Follow web setup
  </Tab>

  <Tab title="Claude Desktop">
    I'm using the Claude desktop app
    → Follow desktop setup
  </Tab>
</Tabs>

## Step 2: Install your first MCP server

[Product-specific tabs showing installation]

### Messages API
```python
# Add MCP connector to your API call
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    mcp_servers=[{
        "name": "github",
        "url": "https://api.githubcopilot.com/mcp/"
    }],
    messages=[{"role": "user", "content": "List my GitHub repos"}]
)
```

### Claude Code
```bash
# Install GitHub MCP server
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# Authenticate
claude mcp

# Use it
claude "List my GitHub repos"
```

[Similar for other products]

## Step 3: Verify it works

[Product-specific verification steps]

## Step 4: Add more servers

[Links to server catalog]

## Common issues

[Quick troubleshooting]

## Next steps

[Links to product-specific guides]
```

---

### 3. `/en/docs/mcp/integration-guides/claude-code/overview.mdx`

**Purpose:** Claude Code-specific overview (split from mega-page)

**Estimated length:** ~250 lines

**Outline:**

```markdown
# MCP in Claude Code

Claude Code can connect to hundreds of external tools through MCP servers.

## What you can do

- Query databases directly from chat
- Create issues in project trackers
- Analyze monitoring data
- Integrate with design tools
- Automate workflows

## How it works

[Architecture diagram specific to Claude Code]

## MCP server types

### HTTP Servers (Recommended)
- Remote cloud services
- OAuth authentication
- Examples: GitHub, Notion, Stripe

### Stdio Servers
- Local processes
- Direct system access
- Examples: Airtable, Postgres

### SSE Servers (Deprecated)
- Legacy remote servers
- Use HTTP instead when available

## Quick links

- [Installation guide](/en/docs/mcp/integration-guides/claude-code/installation)
- [Browse 40+ servers](/en/docs/mcp/integration-guides/claude-code/server-catalog)
- [Enterprise setup](/en/docs/mcp/integration-guides/claude-code/enterprise)

## Example workflow

[Complete workflow example]
```

---

### 4. `/en/docs/mcp/integration-guides/claude-code/installation.mdx`

**Purpose:** Step-by-step installation (split from mega-page)

**Estimated length:** ~500 lines

**Outline:**

```markdown
# Installing MCP Servers in Claude Code

## Three ways to add servers

1. Remote HTTP servers (cloud services)
2. Remote SSE servers (deprecated)
3. Local stdio servers (system access)

## Installing remote HTTP servers

[Complete guide with examples]
[Common HTTP servers]
[OAuth setup]

## Installing stdio servers

[Complete guide]
[Windows special notes]
[Environment variables]

## Managing servers

```bash
# List all servers
claude mcp list

# Get server details
claude mcp get github

# Remove server
claude mcp remove github

# Check status
/mcp  # Within Claude Code
```

## Configuration scopes

[Local, project, user scopes explained]
[When to use each]

## Troubleshooting

[Common installation issues]
```

---

### 5. `/en/docs/mcp/integration-guides/claude-code/server-catalog.mdx`

**Purpose:** Searchable catalog of MCP servers (split from mega-page)

**Estimated length:** ~600 lines

**Outline:**

```markdown
# MCP Server Catalog

Browse 40+ integrations for Claude Code.

<Note>
Use third-party MCP servers at your own risk. Anthropic has not verified all servers.
Be especially careful with servers that fetch untrusted content (prompt injection risk).
</Note>

## Filter by category

[Interactive filter buttons]
- All (40+)
- Development Tools (8)
- Project Management (12)
- Databases (6)
- Payments (5)
- Design & Media (5)
- Infrastructure (4)

## Development & Testing Tools

[Detailed cards with:]
- Server name
- Description
- Installation command
- Authentication requirements
- Documentation link
- Example use case

### GitHub
Manage repos, PRs, and issues directly from Claude Code.

**Install:**
```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

**Authentication:** OAuth (use `/mcp` command)

**Popular actions:**
- List repositories
- Create pull requests
- Review code changes
- Search issues

[Link to GitHub MCP docs]

[Continue for all 40+ servers...]

## Building your own server

Don't see what you need?
[Link to building-servers guide]
```

---

### 6. `/en/docs/mcp/integration-guides/claude-code/enterprise.mdx`

**Purpose:** Enterprise configuration (split from mega-page)

**Estimated length:** ~400 lines

**Outline:**

```markdown
# Enterprise MCP Configuration

Centrally manage MCP servers across your organization.

## Overview

Enterprise configuration allows IT administrators to:
- Deploy standardized MCP servers
- Restrict unauthorized servers
- Disable MCP entirely if needed

## Setting up managed configuration

[File locations by OS]
[Configuration format]
[Examples]

## Allowlists and denylists

[Complete guide]
[Examples]
[Precedence rules]

## Security best practices

[Enterprise security guide]

## Deployment examples

### AWS deployment
[Example]

### Azure deployment
[Example]

### GCP deployment
[Example]
```

---

### 7. `/en/docs/mcp/integration-guides/messages-api.mdx`

**Purpose:** API-specific MCP guide (moved and enhanced)

**Estimated length:** ~350 lines

**Outline:**

```markdown
# MCP Connector in Messages API

Use MCP servers in your API applications.

## Current status

**Beta:** `anthropic-beta: mcp-client-2025-04-04`
**Availability:** Claude API only (not Bedrock/Vertex yet)

## Quick start

[API examples]

## Supported server types

Currently: HTTP remote servers only
Coming: Stdio servers (future)

## Authentication

[OAuth flow]
[API key headers]

## Examples

### GitHub integration
[Complete example]

### Database queries
[Complete example]

## Limitations

[Current beta limitations]
[Roadmap]

## Migration from Claude Code

[Guide for developers moving from CLI to API]
```

---

### 8. `/en/docs/mcp/advanced/security.mdx` (NEW - CONSOLIDATED)

**Purpose:** All security best practices in one place

**Estimated length:** ~600 lines

**Outline:**

```markdown
# MCP Security Best Practices

## Threat model

### What could go wrong?

1. **Prompt injection via MCP tools**
2. **Data exfiltration through server responses**
3. **Unauthorized server access**
4. **Malicious server installation**

[Detailed examples of each]

## Security by product

### Messages API security
[API-specific security]

### Claude Code security
[CLI-specific security]

### Claude.ai security
[Web-specific security]

### Claude Desktop security
[Desktop-specific security]

## Server trust model

### Verifying servers

[How to audit MCP servers before installation]
[Code review checklist]

### Official vs third-party servers

[Differences]
[Risk assessment]

## Network security

[Isolation strategies]
[Firewall rules]
[VPN considerations]

## Data protection

[Secrets management]
[PII handling]
[Encryption]

## Enterprise controls

[Allowlists/denylists]
[Monitoring]
[Audit logging]

## Incident response

[What to do if compromised]
[Revoking access]
[Post-incident review]
```

---

### 9. `/en/docs/mcp/advanced/building-servers.mdx` (NEW)

**Purpose:** Guide for creating custom MCP servers

**Estimated length:** ~500 lines

**Outline:**

```markdown
# Building Your Own MCP Server

## When to build vs use existing

[Decision framework]

## Architecture

[MCP server components]
[Protocol overview]

## Quick start with SDKs

### Python SDK
[Example server]

### TypeScript SDK
[Example server]

### Go SDK
[Example server]

## Transport implementations

### HTTP server
[Complete example]

### Stdio server
[Complete example]

## Best practices

[Performance]
[Error handling]
[Testing]

## Publishing

[How to share your server]
[Adding to official catalog]

## Next steps

[External MCP docs]
```

---

### 10. `/en/docs/mcp/reference/troubleshooting.mdx` (NEW)

**Purpose:** Comprehensive troubleshooting matrix

**Estimated length:** ~400 lines

**Outline:**

```markdown
# MCP Troubleshooting

## Common errors by product

### Messages API errors

| Error | Cause | Solution |
|-------|-------|----------|
| "mcp_servers parameter not supported" | Not using beta header | Add `anthropic-beta: mcp-client-2025-04-04` |
| "Server authentication failed" | Invalid OAuth | Re-authenticate with `/mcp` |

[Continue for all products...]

## Authentication issues

[Common OAuth problems]
[Token expiration]
[Permissions]

## Connection issues

[Network problems]
[Firewall blocking]
[Timeout errors]

## Server errors

[Server-specific issues]
[Output too large]
[Rate limiting]

## Getting help

[Community forums]
[Support channels]
[Bug reports]
```

---

## Navigation Implementation

### Homepage (en/docs/home) Updates

Add MCP card to main page:

```markdown
## Popular Features

<CardGroup>
  <Card title="MCP Integrations" icon="plug" href="/en/docs/mcp/overview">
    Connect Claude to 40+ tools and databases using Model Context Protocol
  </Card>
  ...
</CardGroup>
```

### Top Navigation

MCP tab already exists, keep it:

```json
{
  "tab": "MCP",
  "groups": [
    {
      "group": "Getting Started",
      "pages": [
        "pages/mcp/overview",
        "pages/mcp/getting-started",
        "pages/mcp/comparison"
      ]
    },
    {
      "group": "Integration Guides",
      "pages": [
        "pages/mcp/integration-guides/messages-api",
        {
          "group": "Claude Code",
          "pages": [
            "pages/mcp/integration-guides/claude-code/overview",
            "pages/mcp/integration-guides/claude-code/installation",
            "pages/mcp/integration-guides/claude-code/server-catalog",
            "pages/mcp/integration-guides/claude-code/enterprise"
          ]
        },
        "pages/mcp/integration-guides/claude-ai",
        "pages/mcp/integration-guides/claude-desktop"
      ]
    },
    {
      "group": "Advanced",
      "pages": [
        "pages/mcp/advanced/building-servers",
        "pages/mcp/advanced/security",
        "pages/mcp/advanced/enterprise-deployment",
        "pages/mcp/advanced/migration-guides"
      ]
    },
    {
      "group": "Reference",
      "pages": [
        "pages/mcp/reference/glossary",
        "pages/mcp/reference/troubleshooting",
        "pages/mcp/reference/faq"
      ]
    }
  ]
}
```

---

## Implementation Plan

### Phase 1: Foundation (Week 1)
1. Create comprehensive overview page
2. Create getting-started page with product selector
3. Update main homepage to link prominently

### Phase 2: Split Claude Code Content (Week 2)
1. Split 1,270-line page into 4 focused pages
2. Improve navigation within Claude Code section
3. Add internal cross-links

### Phase 3: Migrate External Content (Week 3)
1. Bring Claude.ai docs from support site
2. Bring Claude Desktop docs from support site
3. Ensure consistent formatting

### Phase 4: Advanced Content (Week 4)
1. Create security consolidated page
2. Create building-servers guide
3. Create troubleshooting matrix

### Phase 5: Reference & Polish (Week 5)
1. Enhance glossary
2. Create FAQ
3. Add visual diagrams
4. Final cross-linking audit

---

## Expected Outcomes

### Metrics

**Before:**
- MCP entry page: 32 lines
- Claude Code MCP: 1,270 lines (overwhelming)
- 7+ fragmented locations
- 404 errors on agent-tools section
- Support site split

**After:**
- MCP hub: ~800-line comprehensive overview
- Claude Code split into 4 pages (~250-600 lines each)
- Single unified location
- All cross-links working
- Consolidated on docs site

### User Experience Improvements

1. **Discoverability:** Comprehensive overview vs thin router
2. **Clarity:** Product comparison matrix upfront
3. **Navigation:** Clear hierarchy vs flat structure
4. **Completeness:** Consolidated security vs scattered
5. **Consistency:** Single location vs 7+ fragments

This reorganization transforms MCP documentation from fragmented and confusing to cohesive and navigable.
