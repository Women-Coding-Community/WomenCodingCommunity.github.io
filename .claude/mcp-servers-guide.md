# MCP Servers Setup Guide

Model Context Protocol (MCP) servers extend Claude Code with external tool integrations.

## Recommended MCP Servers for WCC Project

### 1. GitHub MCP Server
**Purpose**: Manage PRs, issues, and repository operations

**Installation**:
```bash
claude mcp add github
```

**Use cases**:
- Review pull requests
- Create issues for bugs/features
- Check repository status
- Manage branches
- Review code changes

**Usage**:
```
/mcp github list-prs
/mcp github create-issue "Bug in certificate verification"
```

### 2. Sentry MCP Server (Optional)
**Purpose**: Monitor errors and performance

**Installation**:
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

**Use cases**:
- Monitor production errors
- Track certificate verification errors
- Performance monitoring

### 3. PostgreSQL/Database MCP (If using database)
**Purpose**: Query and manage database

**Installation**:
```bash
claude mcp add postgres
```

**Use cases**:
- Query certificate data
- Database migrations
- Data validation

## How to Use MCP Servers

1. **List available servers**:
   ```bash
   claude mcp list
   ```

2. **Authenticate** (first time):
   ```
   /mcp
   ```
   Then follow authentication prompts

3. **Use in conversations**:
   ```
   /mcp github list-prs
   /mcp github create-issue "title" "description"
   ```

## Configuration File

MCP servers are configured in: `~/.claude/settings.json`

Example configuration:
```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "your-token-here"
      }
    }
  }
}
```

## Security Note

Store sensitive tokens in environment variables or use secure token management:
```bash
# In your shell profile (.bashrc, .zshrc):
export GITHUB_TOKEN="your_token_here"
```

## Troubleshooting

**MCP server not working?**
1. Check installation: `claude mcp list`
2. Verify authentication: `/mcp`
3. Check logs: `claude mcp logs <server-name>`

**Token issues?**
- Ensure tokens have proper scopes
- Verify environment variables are set
- Re-authenticate: `/mcp`

## Next Steps

1. Install GitHub MCP server (most useful for your project)
2. Authenticate with your GitHub account
3. Test with `/mcp github list-prs`
4. Add other servers as needed