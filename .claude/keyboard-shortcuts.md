# Claude Code Keyboard Shortcuts - Quick Reference

## Essential Shortcuts

### VS Code Extension

| Action | Mac | Windows/Linux | Description |
|--------|-----|---------------|-------------|
| **Insert file reference** | `Cmd+Option+K` | `Alt+Ctrl+K` | Add file with line numbers |
| **Quick file mention** | `Cmd+K` | `Ctrl+K` | Mention file in conversation |
| **Toggle focus** | `Cmd+Esc` | `Ctrl+Esc` | Switch between editor and Claude |
| **New conversation tab** | `Cmd+Shift+Esc` | `Ctrl+Shift+Esc` | Open new tab |
| **New conversation** | `Cmd+N` | `Ctrl+N` | Start fresh conversation |
| **Send message** | `Cmd+Enter` | `Ctrl+Enter` | Send your message |
| **Accept suggestion** | `Cmd+.` | `Ctrl+.` | Accept current code change |
| **Dismiss suggestion** | `Esc` | `Esc` | Reject current change |
| **Close tab** | `Cmd+W` | `Ctrl+W` | Close conversation tab |
| **Switch tabs** | `Cmd+Tab` | `Ctrl+Tab` | Navigate between tabs |

### JetBrains (WebStorm, IntelliJ, etc.)

| Action | Mac | Windows/Linux | Description |
|--------|-----|---------------|-------------|
| **Quick launch** | `Cmd+Esc` | `Ctrl+Esc` | Open Claude Code |
| **File reference** | `Cmd+Option+K` | `Alt+Ctrl+K` | Add file to context |

## CLI Commands

```bash
# Start Claude Code
claude

# Start in specific directory
claude --dir /path/to/project

# New conversation
claude new

# List conversations
claude list

# Resume conversation
claude resume <conversation-id>

# Clear history
claude clear

# Show help
claude help
```

## Slash Commands in Conversation

```
/help              - Show available commands
/clear             - Clear conversation history
/new               - Start new conversation
/save              - Save conversation
/settings          - Open settings
/mcp               - Manage MCP servers
/skills            - List available skills
```

## Custom Skills (WCC Project)

```
/review-html       - Review HTML/Liquid templates
/optimize-assets   - Analyze and optimize assets
/jekyll-build      - Build and validate Jekyll site
/test-verification - Test certificate verification
/accessibility     - Accessibility audit
```

## File Reference Syntax

```
# Reference entire file
@filename.ext

# Reference specific lines
@filename.ext:10-20

# Reference multiple files
@file1.html @file2.js @file3.css

# Reference directory
@directory/**/*.py
```

## Pro Tips

### Quick File Operations
- `Cmd+P` / `Ctrl+P` - Quick open file, then use `@` to reference it
- `Cmd+Shift+F` / `Ctrl+Shift+F` - Search across all files
- `Cmd+Shift+E` / `Ctrl+Shift+E` - Focus on file explorer

### Efficient Context Management
1. Use `@` for specific files rather than describing them
2. Reference line ranges for large files: `@file.py:100-150`
3. Close unused conversation tabs to maintain performance

### Code Review Workflow
1. Open file: `Cmd+P`
2. Reference it: `@filename.ext`
3. Ask for review: "Review this file for [specific aspect]"
4. Review diff in inline viewer
5. Accept/reject changes individually

### Batch Operations
```
Update all Python files in tools/certificate_automation/src/
to add type hints
```

## Cheat Sheet Print Version

```
┌─────────────────────────────────────────────────────┐
│          Claude Code Quick Reference                │
├─────────────────────────────────────────────────────┤
│ File Reference:    Cmd+Opt+K  (Alt+Ctrl+K)         │
│ Toggle Focus:      Cmd+Esc    (Ctrl+Esc)           │
│ New Tab:           Cmd+Shift+Esc                    │
│ Send Message:      Cmd+Enter  (Ctrl+Enter)         │
│ Accept Change:     Cmd+.      (Ctrl+.)             │
│                                                     │
│ In Conversation:                                    │
│   @file.ext           - Reference file             │
│   @file.ext:10-20     - Reference lines            │
│   /help               - Show help                  │
│   /skills             - List skills                │
│                                                     │
│ CLI:                                                │
│   claude              - Start Claude Code          │
│   claude help         - Show help                  │
└─────────────────────────────────────────────────────┘
```

## Customization

### Add Your Own Shortcuts

1. Open VS Code Command Palette: `Cmd+Shift+P` / `Ctrl+Shift+P`
2. Type "Preferences: Open Keyboard Shortcuts (JSON)"
3. Add custom keybindings:

```json
{
  "key": "cmd+shift+c",
  "command": "claude.openPanel",
  "when": "editorTextFocus"
}
```

## Platform-Specific Notes

### macOS
- Use `Cmd` key for most shortcuts
- `Option` = `Alt` on other platforms

### Windows/Linux
- Use `Ctrl` key for most shortcuts
- Some shortcuts may conflict with system shortcuts

### Web (if using Claude Code in browser)
- Some keyboard shortcuts may be handled by browser
- Use command palette as alternative: `Cmd/Ctrl+Shift+P`

---

**Remember**: Most shortcuts mirror standard VS Code shortcuts with Claude-specific additions!