# Claude Code Masterclass Project Overview

## Purpose
This is a comprehensive educational repository focused on teaching Claude Code usage and best practices. It serves as a complete guide for developers to master Claude Code from installation through advanced features like context engineering, subagents, hooks, and parallel agent workflows.

## Tech Stack
- **Primary Language**: Primarily documentation and examples (Markdown, Python, TypeScript, JavaScript)
- **Tools**: Claude Code CLI, GitHub CLI (gh), Node.js, Docker
- **AI Framework Examples**: Pydantic AI examples included in use-cases

## Project Structure
```
claude-code-intro/
├── README.md                 # Main comprehensive guide (currently needs improvement per issue #1)
├── CLAUDE.md                 # Python-specific project instructions and conventions  
├── use-cases/               # Real-world examples and templates
│   ├── template-generator/   # Template generation system
│   ├── mcp-server/          # MCP server implementation example
│   └── pydantic-ai/         # Pydantic AI agent examples
├── examples/                # Basic code examples
│   ├── main_agent_reference/
│   ├── structured_output_agent/
│   ├── basic_chat_agent/
│   ├── testing_examples/
│   └── tool_enabled_agent/
└── .claude/                 # Claude Code configuration (if present)
```

## Core Focus Areas
1. **Claude Code Installation & Setup**
2. **Context Engineering with CLAUDE.md files**
3. **Permission Management**  
4. **Custom Slash Commands**
5. **MCP Server Integration (especially Serena)**
6. **Subagents for Specialized Tasks**
7. **Automation with Hooks**
8. **GitHub CLI Integration**
9. **Safe Development with Dev Containers**
10. **Parallel Development with Git Worktrees**