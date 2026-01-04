# VS Code Extension Setup Guide

Complete guide to using Claude Code in Visual Studio Code for the WCC project.

## Installation

### Step 1: Install the Extension

1. Open VS Code
2. Press `Cmd+Shift+X` (Mac) or `Ctrl+Shift+X` (Windows/Linux)
3. Search for "Claude Code"
4. Click "Install"

**OR** install from terminal:
```bash
code --install-extension anthropic.claude-code
```

### Step 2: Sign In

1. After installation, click the Claude icon in the activity bar
2. Sign in with your Anthropic account
3. Authorize VS Code access

## Key Features for Frontend Development

### 1. Inline Diff Viewer
- See proposed changes directly in your editor
- Accept/reject changes with one click
- Compare side-by-side

### 2. File References with Line Numbers
**Keyboard shortcut**: `Cmd+Option+K` (Mac) or `Alt+Ctrl+K` (Windows/Linux)

Example:
```
Review verify.html:50-100 for accessibility issues
```

### 3. Multiple Conversation Tabs
- Work on different features simultaneously
- Keep context separated
- Switch between tabs easily

### 4. Auto-Accept Mode
Enable in settings to automatically apply Claude's edits as they're generated.

### 5. Drag-and-Drop Panels
Customize your layout:
- Move Claude panel to sidebar
- Create split views
- Dock as bottom panel

## Essential Keyboard Shortcuts

### File Operations
- `Cmd+Option+K` / `Alt+Ctrl+K` - Insert file reference with line numbers
- `Cmd+K` / `Ctrl+K` - Quick file mention

### Navigation
- `Cmd+Esc` / `Ctrl+Esc` - Toggle focus between editor and Claude
- `Cmd+Shift+Esc` / `Ctrl+Shift+Esc` - New conversation tab

### Conversation Management
- `Cmd+N` / `Ctrl+N` - New conversation
- `Cmd+W` / `Ctrl+W` - Close current tab
- `Cmd+Tab` / `Ctrl+Tab` - Switch tabs

### Code Actions
- `Cmd+Enter` / `Ctrl+Enter` - Send message
- `Cmd+.` - Accept current suggestion
- `Esc` - Dismiss suggestion

## Project-Specific Workflows

### 1. Certificate Verification Development
```
Open verify.html
@verify.html Review this page for accessibility issues
```

### 2. Python Certificate Automation
```
@tools/certificate_automation/src/generate_certificates.py
Add error handling for missing template files
```

### 3. Jekyll Template Editing
```
@_layouts/default.html
Update the navigation to include certificate verification link
```

### 4. Batch File Operations
```
Update all files in assets/css/ to use CSS custom properties
```

## Settings Configuration

Access Claude Code settings:
1. `Cmd+,` / `Ctrl+,` to open Settings
2. Search for "Claude Code"

### Recommended Settings

```json
{
  "claude.autoAccept": false,
  "claude.inlineSuggestions": true,
  "claude.contextLines": 3,
  "claude.showDiff": true,
  "claude.panelPosition": "sidebar"
}
```

## Integration with Your Workflow

### Git Integration
Claude Code works seamlessly with VS Code's built-in Git:
1. Make changes with Claude
2. Review in Source Control panel
3. Commit with descriptive messages
4. Push to repository

### Terminal Integration
Use VS Code's integrated terminal:
```bash
# Run certificate generation
cd tools/certificate_automation
python3 src/generate_certificates.py

# Build Jekyll site
bundle exec jekyll serve
```

### Extension Compatibility

Works well with:
- **GitLens** - Enhanced Git capabilities
- **Prettier** - Code formatting
- **ESLint** - JavaScript linting
- **Live Server** - Preview HTML changes
- **Path Intellisense** - File path autocompletion

## Troubleshooting

### Extension Not Loading
1. Reload VS Code window: `Cmd+Shift+P` → "Reload Window"
2. Check extension is enabled
3. Sign out and sign back in

### Slow Performance
1. Close unused conversation tabs
2. Clear conversation history
3. Restart VS Code

### Context Not Working
1. Ensure files are in workspace
2. Check file is saved
3. Try explicit file reference: `@filename.ext`

## Tips for Maximum Productivity

1. **Use File References**: Always reference specific files for focused help
2. **Break Down Tasks**: Create separate conversations for different features
3. **Review Before Accepting**: Always review suggested changes in diff view
4. **Save Frequently**: Claude works best with saved files
5. **Use Search**: `Cmd+P` to quickly open files, then reference them

## Advanced Features

### Custom Keybindings
Add to `keybindings.json`:
```json
{
  "key": "cmd+shift+c",
  "command": "claude.openPanel"
}
```

### Workspace Settings
Create `.vscode/settings.json` in project:
```json
{
  "claude.contextFiles": [
    "tools/certificate_automation/**/*.py",
    "verify.html",
    "_config.yml"
  ]
}
```

## Next Steps

1. ✅ Install Claude Code extension
2. ✅ Learn keyboard shortcuts
3. ✅ Try file referencing
4. ✅ Explore inline diffs
5. ✅ Customize your layout
6. ✅ Set up project-specific settings

## Resources

- Official Docs: https://code.claude.com/docs/en/vs-code.md
- Keyboard Shortcuts: `Cmd+K Cmd+S` in VS Code
- Extension Marketplace: https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code

---

**Pro Tip**: Use `@` to mention files and Claude will automatically include their content in context!