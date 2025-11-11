# Documentation Topic Coverage Report

**Analysis of GitHub-requested topics against actual Claude documentation**

## Executive Summary

- **Total unique topics requested:** 105
- **Topics with documentation found:** 18 (17.1%)
- **TRUE documentation gaps:** 2 (1.9%)

### Confidence Breakdown
- **High confidence** (exact/case-insensitive match): 11 topics
- **Medium confidence** (word boundary match): 0 topics
- **Low confidence** (related terms): 7 topics

---

## ✅ Topics with Existing Documentation

**These GitHub issues may be INVALID - documentation already exists!**

### Built-in 'Plan' / 'Explore' Subagent (LOW confidence)

**Match types:** related_terms

**Related GitHub issues that could potentially be closed:**
- [#10469](https://github.com/anthropics/claude-code/issues/10469): [DOCS] Missing Documentation for Built-in 'Plan' / 'Explore' Subagent

**Found in 35 file(s):**
- `intro.mdx` (line 2) - related_terms
  > --- title: "Intro to Claude" ---  Claude is a highly performant, trustworthy, and intelligent AI pla...
- `claude-code/plugins.mdx` (line 371) - related_terms
  > lash-commands) - Command development details   * [Subagents](/en/docs/claude-code/sub-agents) - Agen...
- `claude-code/data-usage.mdx` (line 9) - related_terms
  > olicies for Claude  ## Data policies  ### Data training policy  **Consumer users (Free, Pro, and Max...
  _(and 32 more files)_

### modifying tool inputs in PreToolUse hooks (LOW confidence)

**Match types:** related_terms

**Related GitHub issues that could potentially be closed:**
- [#9185](https://github.com/anthropics/claude-code/issues/9185): [DOCS] Missing documentation for modifying tool inputs in PreToolUse hooks

**Found in 10 file(s):**
- `claude-code/settings.mdx` (line 2) - related_terms
  > --- title: "Claude Code settings" ---  Configure Claude Code with global and project-level settings,...
- `claude-code/hooks.mdx` (line 5) - related_terms
  > age provides reference documentation for implementing hooks in Claude Code.  <Tip>   For a quickstar...
- `claude-code/sub-agents.mdx` (line 5) - related_terms
  > nts" ---  Create and use specialized AI subagents in Claude Code for task-specific workflows and imp...
  _(and 7 more files)_

### the difference between `ultrathink` and Thinking Mode On/Off (LOW confidence)

**Match types:** related_terms

**Related GitHub issues that could potentially be closed:**
- [#9072](https://github.com/anthropics/claude-code/issues/9072): [DOCS] Document the difference between `ultrathink` and Thinking Mode On/Off

**Found in 41 file(s):**
- `claude-code/interactive-mode.mdx` (line 5) - related_terms
  > te reference for keyboard shortcuts, input modes, and interactive features in Claude Code sessions. ...
- `claude-code/settings.mdx` (line 5) - related_terms
  >  settings" ---  Configure Claude Code with global and project-level settings, and environment variab...
- `claude-code/monitoring-usage.mdx` (line 5) - related_terms
  > --- title: "Monitoring" ---  Learn how to enable and configure OpenTelemetry for Claude Code.  Claud...
  _(and 38 more files)_

### default OAuth token `expires_in` behavior when omitted (LOW confidence)

**Match types:** related_terms

**Related GitHub issues that could potentially be closed:**
- [#9017](https://github.com/anthropics/claude-code/issues/9017): [DOCS] Document default OAuth token `expires_in` behavior when omitted

**Found in 8 file(s):**
- `claude-code/settings.mdx` (line 7) - related_terms
  > ode offers a variety of settings to configure its behavior to meet your needs. You can configure Cla...
- `claude-code/common-workflows.mdx` (line 143) - related_terms
  > to use ES2024 features while maintaining the same behavior     ```   </Step>    <Step title="Verify ...
- `claude-code/github-actions.mdx` (line 635) - related_terms
  > PI      | No       |  \*Prompt is optional - when omitted for issue/PR comments, Claude responds to ...
  _(and 5 more files)_

### Various Claude Code Features (LOW confidence)

**Match types:** related_terms

**Related GitHub issues that could potentially be closed:**
- [#8584](https://github.com/anthropics/claude-code/issues/8584): [DOCS] Missing Documentation for Various Claude Code Features (CLI Flags, Slash Commands, & Tools)

**Found in 76 file(s):**
- `get-started.mdx` (line 2) - related_terms
  > --- title: "Get started with Claude" ---  Make your first API call to Claude and build a simple web ...
- `mcp.mdx` (line 22) - related_terms
  >  to MCP servers.   </Card>    <Card title="MCP in Claude Code" icon="head-side-gear" href="/en/docs/...
- `claude-code/google-vertex-ai.mdx` (line 2) - related_terms
  > --- title: "Claude Code on Google Vertex AI" ---  Learn about configuring Claude Code through Google...
  _(and 73 more files)_

### new mascot 'Clawd' and implement an introductory welcome screen (LOW confidence)

**Match types:** related_terms

**Related GitHub issues that could potentially be closed:**
- [#8536](https://github.com/anthropics/claude-code/issues/8536): [DOCS] Document new mascot 'Clawd' and implement an introductory welcome screen

**Found in 2 file(s):**
- `claude-code/quickstart.mdx` (line 7) - related_terms
  >  in just a few minutes. By the end, you'll understand how to use Claude Code for common development ...
- `about-claude/use-case-guides/customer-support-chat.mdx` (line 5) - related_terms
  > Claude's advanced conversational capabilities to handle customer inquiries in real time, providing 2...

### the Bash tool's sandbox parameter (LOW confidence)

**Match types:** related_terms

**Related GitHub issues that could potentially be closed:**
- [#8194](https://github.com/anthropics/claude-code/issues/8194): [DOCS] Missing documentation for the Bash tool's sandbox parameter

**Found in 64 file(s):**
- `claude-code/plugins.mdx` (line 5) - related_terms
  > s, agents, hooks, Skills, and MCP servers through the plugin system.  <Tip>   For complete technical...
- `claude-code/sandboxing.mdx` (line 9) - related_terms
  > re environment for agent execution while reducing the need for constant permission prompts. Instead ...
- `claude-code/checkpointing.mdx` (line 11) - related_terms
  > with Claude, checkpointing automatically captures the state of your code before each edit. This safe...
  _(and 61 more files)_

### subagent (HIGH confidence)

**Match types:** case_insensitive, exact

**Related GitHub issues that could potentially be closed:**
- [#10504](https://github.com/anthropics/claude-code/issues/10504): [FEATURE] Subagent YAML frontmatter description field has UX and design issues
- [#9681](https://github.com/anthropics/claude-code/issues/9681): [DOCS] Bedrock setup missing AWS Marketplace subscription requirements causing permission errors
- [#9595](https://github.com/anthropics/claude-code/issues/9595): [DOCS] Documentation missing for new 'Explore' subagent
- [#8670](https://github.com/anthropics/claude-code/issues/8670): [DOCS] CHANGELOG.md for v 2.0.2
- [#8624](https://github.com/anthropics/claude-code/issues/8624): [DOCS]   Update documentation to reflect that  the /agents slash command has been removed
- [#8501](https://github.com/anthropics/claude-code/issues/8501): [BUG] Claude Code subagent YAML Frontmatter authoritive documentation
- [#7166](https://github.com/anthropics/claude-code/issues/7166): Clarify whether subagents read the user-scoped `~/.claude/CLAUDE.md` file
- [#5865](https://github.com/anthropics/claude-code/issues/5865): Clarify documentation on subagent loading behavior (manual file creation vs. `/agents` command)
- [#5068](https://github.com/anthropics/claude-code/issues/5068): Docs: Comprehensive documentation out of sync with changelog features
- [#4750](https://github.com/anthropics/claude-code/issues/4750): Ambiguity in Subagent Behavior When Main Agent is in Plan Mode

**Found in 12 file(s):**
- `claude-code/plugins.mdx` (line 371) - case_insensitive
  > lash-commands) - Command development details   * [Subagents](/en/docs/claude-code/sub-agents) - Agen...
- `claude-code/vs-code.mdx` (line 78) - exact
  > se them * **Subagents configuration**: Configure [subagents through the CLI](/en/docs/claude-code/su...
- `claude-code/cli-reference.mdx` (line 28) - exact
  > `--agents`                       | Define custom [subagents](/en/docs/claude-code/sub-agents) dynami...
  _(and 9 more files)_

### tool (HIGH confidence)

**Match types:** exact, case_insensitive

**Related GitHub issues that could potentially be closed:**
- [#10377](https://github.com/anthropics/claude-code/issues/10377): [DOCS] Sandbox Edit permissions for bash write access not clearly documented
- [#9600](https://github.com/anthropics/claude-code/issues/9600): [DOCS] publish default system prompt (with tools)
- [#8600](https://github.com/anthropics/claude-code/issues/8600): [DOCS] Undocumented feature .rgignore
- [#7740](https://github.com/anthropics/claude-code/issues/7740): [BUG] Simplify issue reporting
- [#7722](https://github.com/anthropics/claude-code/issues/7722): [BUG] Update `Fetch` tool docstring to indicate that it cannot open `localhost` URLs
- [#7613](https://github.com/anthropics/claude-code/issues/7613): [BUG] Broken documentation links - incorrect redirects with double path ending
- [#7611](https://github.com/anthropics/claude-code/issues/7611): [DOCS] Ambiguity in 'piped input' deprecation between changelog and `common-workflows` documentation
- [#7321](https://github.com/anthropics/claude-code/issues/7321): [DOCS] Broken link from "Claude Code Best Practices" doc
- [#7151](https://github.com/anthropics/claude-code/issues/7151): Clarification needed on Statsig dependency following OpenAI acquisition
- [#7109](https://github.com/anthropics/claude-code/issues/7109): Feature Request: Enhance Changelog with Rich Content and Improved Discoverability
- [#7103](https://github.com/anthropics/claude-code/issues/7103): [Idea/Suggestion] A Powerful Pattern for an Agentic Documentation GitHub Action (for internal use)
- [#7100](https://github.com/anthropics/claude-code/issues/7100): feat(docs, auth): Document Headless/Remote Authentication and Support CI/CD
- [#6975](https://github.com/anthropics/claude-code/issues/6975): [Documentation] Add TodoWrite to PreToolUse Hook Matchers
- [#6971](https://github.com/anthropics/claude-code/issues/6971): Docs: Explicit `Bash` tool restriction against `find` and `grep` is undocumented
- [#6970](https://github.com/anthropics/claude-code/issues/6970): [Docs] Ambiguity and Contradiction in `Read` Permission Rule Enforcement
- [#6968](https://github.com/anthropics/claude-code/issues/6968): Docs: Proactive Planning Behavior with `TodoWrite` Tool is Undocumented
- [#6966](https://github.com/anthropics/claude-code/issues/6966): [Docs] Clarify behavior and precedence of advanced JSON output fields for Hooks
- [#6940](https://github.com/anthropics/claude-code/issues/6940): [Bug] File Import Instruction Parsing Failure in Claude Code
- [#6491](https://github.com/anthropics/claude-code/issues/6491): Docs: Update settings documentation for live-reloading feature (v1.0.90)
- [#5735](https://github.com/anthropics/claude-code/issues/5735): Docs: Clarify "stable" vs. "latest" installation versions and update CHANGELOG
- [#4392](https://github.com/anthropics/claude-code/issues/4392): 🤖📚 FR: Local Docs Bundle - Stop Making Me Download 2MB to Learn What `/agents` Does 🐌💸
- [#3671](https://github.com/anthropics/claude-code/issues/3671): [Docs] Missing `tool_input` and `tool_response` Schemes for Hook Development
- [#2950](https://github.com/anthropics/claude-code/issues/2950): Imports or CLAUDE.local.md?
- [#2509](https://github.com/anthropics/claude-code/issues/2509): [QUESTION] Conda environment workflow guidance needed - inherited environment but missing shell functions
- [#2508](https://github.com/anthropics/claude-code/issues/2508): [DOCS] Environment variables don't persist between bash commands - documentation inconsistency
- [#2028](https://github.com/anthropics/claude-code/issues/2028): [BUG] `LS` vs `List` - lack of clarity
- [#1936](https://github.com/anthropics/claude-code/issues/1936): Bug Report: Typo in /help Command - Incorrect Spelling of /compact
- [#1330](https://github.com/anthropics/claude-code/issues/1330): [BUG] Confusing limits
- [#1206](https://github.com/anthropics/claude-code/issues/1206): Improve Renaming/Moving tool usage

**Found in 77 file(s):**
- `intro.mdx` (line 38) - exact
  > ith Claude  Anthropic has best-in-class developer tools to build scalable applications with Claude. ...
- `mcp.mdx` (line 7) - exact
  > o connect AI models to different data sources and tools.  ## Build your own MCP products  <Card titl...
- `claude-code/plugins.mdx` (line 20) - exact
  > our machine * Basic familiarity with command-line tools  ### Create your first plugin  <Steps>   <St...
  _(and 74 more files)_

### skill (HIGH confidence)

**Match types:** exact

**Related GitHub issues that could potentially be closed:**
- [#10247](https://github.com/anthropics/claude-code/issues/10247): [Bug] Documentation typo: "Tech Claude" should be "Teach Claude" on agent skills overview page
- [#9959](https://github.com/anthropics/claude-code/issues/9959): [FEATURE] Feature Enhancement: Skills Documentation Pattern Support

**Found in 15 file(s):**
- `claude-code/plugins.mdx` (line 134) - exact
  >  # Custom agents (optional) │   └── helper.md ├── skills/                   # Agent Skills (optional...
- `claude-code/skills.mdx` (line 27) - exact
  >  Skills overview](/en/docs/agents-and-tools/agent-skills/overview).  <Note>   For a deep dive into t...
- `claude-code/plugins-reference.mdx` (line 67) - exact
  > e them based on the task context.  **Location**: `skills/` directory in plugin root  **File format**...
  _(and 12 more files)_

### MCP (HIGH confidence)

**Match types:** exact

**Related GitHub issues that could potentially be closed:**
- [#10079](https://github.com/anthropics/claude-code/issues/10079): [DOCS] DISABLE_AUTOUPDATER env documentation refers to undocumented or non-existent setting
- [#8858](https://github.com/anthropics/claude-code/issues/8858): [BUG] MCP with oauth in headless mode
- [#7672](https://github.com/anthropics/claude-code/issues/7672): [BUG] Confusing UX and silent failures for claude mcp add on Windows
- [#6986](https://github.com/anthropics/claude-code/issues/6986): Request: clean up hooks
- [#6888](https://github.com/anthropics/claude-code/issues/6888): Docs: Discrepancy in `claude mcp add` scope storage locations
- [#6493](https://github.com/anthropics/claude-code/issues/6493): Documentation Update: Missing CLI Slash Commands and Flags
- [#5793](https://github.com/anthropics/claude-code/issues/5793): How to - migration from CC spec workflow to CCSW MCP
- [#5004](https://github.com/anthropics/claude-code/issues/5004): Add explicit documentation that MCP permissions do not support wildcards
- [#4930](https://github.com/anthropics/claude-code/issues/4930): [BUG]: CLI error with system prompt and doesn't recognize permissions
- [#4109](https://github.com/anthropics/claude-code/issues/4109): Unhelpful error message when MCP server configuration was invalid
- [#3120](https://github.com/anthropics/claude-code/issues/3120): Unclear how Claude Code handles image results from MCP tool calls
- [#2324](https://github.com/anthropics/claude-code/issues/2324): [BUG] Fix the docs. You use --header to add an authorization header, not -e
- [#2308](https://github.com/anthropics/claude-code/issues/2308): Documentation error: SSE server with custom headers
- [#1234](https://github.com/anthropics/claude-code/issues/1234): Support for other IDEs (Neovim/Emacs)
- [#1052](https://github.com/anthropics/claude-code/issues/1052): Field notes: git worktree pattern
- [#1022](https://github.com/anthropics/claude-code/issues/1022): Outdated Documentation at docs.anthropic.com/en/docs/claude-code/tutorials

**Found in 27 file(s):**
- `mcp.mdx` (line 2) - exact
  > --- title: "Model Context Protocol (MCP)" ---  MCP is an open protocol that standardizes ...
- `claude-code/plugins.mdx` (line 5) - exact
  >  with custom commands, agents, hooks, Skills, and MCP servers through the plugin system.  <Tip>   Fo...
- `claude-code/sandboxing.mdx` (line 184) - exact
  > s you may wish to run. For example, to sandbox an MCP server you could run:  ```bash  theme={null} n...
  _(and 24 more files)_

### Bedrock (HIGH confidence)

**Match types:** exact

**Related GitHub issues that could potentially be closed:**
- [#10037](https://github.com/anthropics/claude-code/issues/10037): [BUG] Claude is unable to write a working wildcard
- [#8946](https://github.com/anthropics/claude-code/issues/8946): [DOCS] VS Code Settings for Amazon Bedrock
- [#8369](https://github.com/anthropics/claude-code/issues/8369): [DOCS] Unclear default model behavior for Claude Code on Amazon Bedrock when ANTHROPIC_MODEL is not set
- [#7017](https://github.com/anthropics/claude-code/issues/7017): [BUG] Windows Alt+V shortcut not documented - users receive inaccurate CTRL+V paste tooltip instructions
- [#6962](https://github.com/anthropics/claude-code/issues/6962): [BUG] `theme` property in settings.json not recognized despite being documented
- [#6544](https://github.com/anthropics/claude-code/issues/6544): Docs: Add All Environment Variables from Changelog and Docs to Settings Page
- [#6445](https://github.com/anthropics/claude-code/issues/6445): [BUG] Tab switching functionality broken on Japanese Claude Code SDK documentation
- [#5891](https://github.com/anthropics/claude-code/issues/5891): Documentation inconsistency: SDK Quick Start requires API key but Claude Code uses subscription auth
- [#5792](https://github.com/anthropics/claude-code/issues/5792): Fix broken links to deprecated bedrock-vertex-proxies documentation page
- [#4958](https://github.com/anthropics/claude-code/issues/4958): Auto-detect and add missing language tags to generated markdown code blocks
- [#3833](https://github.com/anthropics/claude-code/issues/3833): [BUG]  CLAUDE_CONFIG_DIR environment variable behavior unclear - still creates local .claude/ directories
- [#3556](https://github.com/anthropics/claude-code/issues/3556): Wrong Documentation for Config settings.
- [#2062](https://github.com/anthropics/claude-code/issues/2062): [BUG] Inconsistent documentation about "# to memorize" and CLAUDE.md persistence
- [#2013](https://github.com/anthropics/claude-code/issues/2013): [BUG] `/bug` does not report bug, 🤣
- [#1805](https://github.com/anthropics/claude-code/issues/1805): [BUG] Claude displays `offline` unless some additional domains are allowed
- [#1298](https://github.com/anthropics/claude-code/issues/1298): [BUG]  Documentation fix for Claude CLI error in WSL + Windows Detection
- [#1155](https://github.com/anthropics/claude-code/issues/1155): [BUG] Docs feedback widget unresponsive

**Found in 26 file(s):**
- `claude-code/data-usage.mdx` (line 26) - exact
  > e only for Anthropic first-party API, and not for Bedrock or Vertex users.  ### Feedback using the `...
- `claude-code/legal-and-compliance.mdx` (line 18) - exact
  > ude API directly (1P) or accessing it through AWS Bedrock or Google Vertex (3P), your existing comme...
- `claude-code/vs-code.mdx` (line 45) - exact
  > ails  ### Using Third-Party Providers (Vertex and Bedrock)  The VS Code extension supports using Cla...
  _(and 23 more files)_

### slash command (HIGH confidence)

**Match types:** exact, case_insensitive, related_terms

**Related GitHub issues that could potentially be closed:**
- [#9307](https://github.com/anthropics/claude-code/issues/9307): Improve Claude Code documentation accessibility in Claude's context
- [#9186](https://github.com/anthropics/claude-code/issues/9186): [Feature Request] Add Documentation URLs for CLI Slash Commands
- [#8758](https://github.com/anthropics/claude-code/issues/8758): [DOCS] Slash commands documentation incorrectly shows $1, $2, $3 positional parameters
- [#6681](https://github.com/anthropics/claude-code/issues/6681): Docs: Align changelog with new feature rollouts (e.g., slash command positional arguments)
- [#5709](https://github.com/anthropics/claude-code/issues/5709): Feature Documentation Request: Background Commands and Process Management
- [#5268](https://github.com/anthropics/claude-code/issues/5268): Documentation missing for `/security-review` slash command and its git dependency
- [#5194](https://github.com/anthropics/claude-code/issues/5194): Docs: Clarify that only users, not the AI, can invoke slash commands
- [#2177](https://github.com/anthropics/claude-code/issues/2177): Documentation Error in Claude Code Slash Commands Section

**Found in 24 file(s):**
- `claude-code/plugins.mdx` (line 119) - exact
  >  directory** (`commands/`) - Contains your custom slash commands * **Test marketplace** - Allows you...
- `claude-code/sandboxing.mdx` (line 65) - exact
  > u can enable sandboxing by running the `/sandbox` slash command:  ``` > /sandbox ```  This activates...
- `claude-code/checkpointing.mdx` (line 66) - case_insensitive
  > ode) - Keyboard shortcuts and session controls * [Slash commands](/en/docs/claude-code/slash-command...
  _(and 21 more files)_

### thinking mode (HIGH confidence)

**Match types:** related_terms, case_insensitive, exact

**Related GitHub issues that could potentially be closed:**
- [#8780](https://github.com/anthropics/claude-code/issues/8780): [DOCS] Doc Missing for alwaysThinkingEnabled Setting
- [#8368](https://github.com/anthropics/claude-code/issues/8368): [DOCS] Comprehensive Documentation Update for Claude Code v2.0.0 Release

**Found in 33 file(s):**
- `claude-code/interactive-mode.mdx` (line 25) - related_terms
  >                                | Toggle [extended thinking](/en/docs/build-with-claude/extended-thin...
- `claude-code/settings.mdx` (line 355) - related_terms
  >                                          | | `MAX_THINKING_TOKENS`                      | Enable [ex...
- `claude-code/amazon-bedrock.mdx` (line 151) - related_terms
  > ort CLAUDE_CODE_MAX_OUTPUT_TOKENS=4096 export MAX_THINKING_TOKENS=1024 ```  **Why these values:**  *...
  _(and 30 more files)_

### Plan (HIGH confidence)

**Match types:** case_insensitive, exact

**Related GitHub issues that could potentially be closed:**
- [#8327](https://github.com/anthropics/claude-code/issues/8327): [Bug/Documentation] 'Organization has been disabled' error when ANTHROPIC_API_KEY overrides Max/Pro subscription
- [#7179](https://github.com/anthropics/claude-code/issues/7179): Documentation: Consolidate Disparate Claude Code Documentation into a Single Source of Truth
- [#3658](https://github.com/anthropics/claude-code/issues/3658): Clarify documentation about Claude Github integration
- [#1516](https://github.com/anthropics/claude-code/issues/1516): [FEATURE REQUEST] Ability to move directories and not break --continue

**Found in 44 file(s):**
- `claude-code/data-usage.mdx` (line 11) - case_insensitive
  > ning policy  **Consumer users (Free, Pro, and Max plans)**: Starting August 28, 2025, we're giving y...
- `claude-code/sandboxing.mdx` (line 196) - case_insensitive
  > rrently supports Linux and macOS; Windows support planned  ## See also  * [Security](/en/docs/claude...
- `claude-code/interactive-mode.mdx` (line 26) - exact
  >                | Switch between Auto-Accept Mode, Plan Mode, and normal mode |  ### Multiline input ...
  _(and 41 more files)_

### agent (HIGH confidence)

**Match types:** exact

**Related GitHub issues that could potentially be closed:**
- [#6973](https://github.com/anthropics/claude-code/issues/6973): Docs: Clarify how `CLAUDE.md` and `--append-system-prompt` influence Claude's instructions
- [#6920](https://github.com/anthropics/claude-code/issues/6920): No uninstall documentation for the native Claud Code build (Windows)
- [#4347](https://github.com/anthropics/claude-code/issues/4347): “Due to character-limit constraints…” message when using claude -p — CLI safeguard or model hallucination?
- [#1813](https://github.com/anthropics/claude-code/issues/1813): Background Worker For Memory and Docs

**Found in 58 file(s):**
- `intro.mdx` (line 8) - exact
  > nnet 4.5** - Our smartest model. Best for complex agents, coding, and most advanced tasks. [Learn mo...
- `mcp.mdx` (line 18) - exact
  >  in the Messages API" icon="cloud" href="/en/docs/agents-and-tools/mcp-connector">     Use the MCP c...
- `claude-code/plugins.mdx` (line 5) - exact
  > ns" ---  Extend Claude Code with custom commands, agents, hooks, Skills, and MCP servers through the...
  _(and 55 more files)_

### Explore (HIGH confidence)

**Match types:** exact, case_insensitive

**Related GitHub issues that could potentially be closed:**
- [#2659](https://github.com/anthropics/claude-code/issues/2659): Windows Explorer Integration for Claude Code

**Found in 26 file(s):**
- `get-started.mdx` (line 118) - exact
  >  EPA clean energy updates\n\n**Specific Topics to Explore:**\n- Perovskite and next-gen solar cells\...
- `intro.mdx` (line 30) - exact
  >  href="/en/resources/prompt-library/library">     Explore example prompts for inspiration.   </Card>...
- `claude-code/plugins.mdx` (line 364) - exact
  > age multiple plugin sources * **Advanced usage**: Explore plugin combinations and workflows  ### For...
  _(and 23 more files)_

### AWS (HIGH confidence)

**Match types:** exact, case_insensitive

**Related GitHub issues that could potentially be closed:**
- [#1028](https://github.com/anthropics/claude-code/issues/1028): [BUG] Lack of Databricks Support

**Found in 20 file(s):**
- `claude-code/legal-and-compliance.mdx` (line 18) - exact
  >  Claude API directly (1P) or accessing it through AWS Bedrock or Google Vertex (3P), your existing c...
- `claude-code/vs-code.mdx` (line 60) - exact
  > ur-api-key"`                                 | | `AWS_REGION`                  | AWS region for Bedr...
- `claude-code/overview.mdx` (line 46) - exact
  > nterprise-ready**: Use the Claude API, or host on AWS or GCP. Enterprise-grade [security](/en/docs/c...
  _(and 17 more files)_

---

## ❌ TRUE Documentation Gaps

**These GitHub issues are VALID - no documentation found!**

### AskUserQuestion Tool

**Related GitHub issues (valid requests):**
- [#10346](https://github.com/anthropics/claude-code/issues/10346): [DOCS] Missing Documentation for AskUserQuestion Tool

**Action needed:** Create documentation for this topic

### ultrathink

**Related GitHub issues (valid requests):**
- [#10099](https://github.com/anthropics/claude-code/issues/10099): [DOCS] What does ultrathink do?
- [#8360](https://github.com/anthropics/claude-code/issues/8360): [DOCS] Documentation for Extended Thinking feature is unclear and incomplete
- [#7668](https://github.com/anthropics/claude-code/issues/7668): [FEATURE] Configuration and Documentation for Thinking Mode

**Action needed:** Create documentation for this topic

---

## Recommendations

### For GitHub Issue Triage

1. **Review 18 'covered' topics** - documentation exists, consider:
   - Closing issues as duplicate/invalid
   - Or improving discoverability if users can't find it

2. **Address 2 TRUE gaps** - create missing documentation

### For Documentation Team

Focus on the TRUE gaps, especially topics with multiple issue requests:

- **ultrathink** (3 issue requests)
- **AskUserQuestion Tool** (1 issue requests)
