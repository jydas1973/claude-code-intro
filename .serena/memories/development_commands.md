# Development Commands and Workflows

## Essential System Commands
- `git` - Git version control
- `gh` - GitHub CLI for issue/PR management
- `npm` - Node.js package manager
- `docker` - Container management
- `rg` - Ripgrep for fast searching (preferred over grep/find)

## Claude Code Commands
### Built-in Slash Commands
- `/init` - Generate initial CLAUDE.md
- `/permissions` - Manage tool permissions
- `/clear` - Clear context between tasks
- `/agents` - Manage subagents
- `/help` - Get help with Claude Code
- `/primer` - Analyze repository structure
- `/fix-github-issue [number]` - Auto-fix GitHub issues

### Custom Commands (when available)
- `/generate-prp INITIAL.md` - Create implementation blueprint
- `/execute-prp PRPs/feature.md` - Implement from blueprint
- `/prep-parallel [feature] [count]` - Setup parallel worktrees
- `/execute-parallel [feature] [plan] [count]` - Run parallel implementations

## Testing and Validation
Since this is primarily a documentation/educational project:
- No specific test framework configured
- Validation focuses on documentation accuracy
- Examples should be runnable where applicable

## GitHub Integration
- `gh issue view [number]` - View issue details
- `gh issue list` - List issues
- `gh pr create` - Create pull request
- `gh pr list` - List pull requests

## Development Environment
- Uses standard terminal/command line
- Supports dev containers for safe experimentation
- No specific build system (documentation-focused project)