# Claude Code Quick Start Guide

Get up and running with Claude Code in 5 minutes!

## Step 1: Install VS Code Extension (2 minutes)

### Option A: From VS Code
1. Open VS Code
2. Press `Cmd+Shift+X` (Mac) or `Ctrl+Shift+X` (Windows/Linux)
3. Search for "Claude Code"
4. Click "Install"
5. Sign in with your Anthropic account

### Option B: From Command Line
```bash
code --install-extension anthropic.claude-code
```

## Step 2: Learn 3 Essential Shortcuts (1 minute)

```
Cmd+Option+K (Alt+Ctrl+K)  - Reference a file
Cmd+Esc (Ctrl+Esc)         - Toggle between editor and Claude
@filename.ext              - Mention file in conversation
```

## Step 3: Try Your First Command (2 minutes)

### Example 1: Review a File
```
@verify.html Review this page for accessibility issues
```

### Example 2: Update Code
```
@tools/certificate_automation/src/generate_certificates.py
Add error handling for missing template files
```

### Example 3: Use a Custom Skill
```
Use the accessibility-audit skill on @verify.html
```

## That's It! 🎉

You're ready to use Claude Code effectively!

---

## Next Steps (Optional)

### Install MCP Servers (5 minutes)
```bash
# GitHub integration
claude mcp add github
```

### Explore Custom Skills
- `review-html` - Review HTML/Liquid templates
- `optimize-assets` - Optimize website assets
- `jekyll-build` - Build Jekyll site
- `test-verification` - Test certificate verification
- `accessibility-audit` - Accessibility audits

### Read More
- [Complete VS Code Setup](vscode-setup-guide.md)
- [All Keyboard Shortcuts](keyboard-shortcuts.md)
- [Common Workflows](workflows-guide.md)
- [MCP Servers Guide](mcp-servers-guide.md)

---

## Quick Reference Card

```
┌─────────────────────────────────────────────┐
│         Claude Code Essentials             │
├─────────────────────────────────────────────┤
│                                             │
│ 📁 Reference File:                          │
│    @filename.ext                            │
│    Cmd+Opt+K (Alt+Ctrl+K)                  │
│                                             │
│ 🔄 Toggle Focus:                            │
│    Cmd+Esc (Ctrl+Esc)                      │
│                                             │
│ 📤 Send Message:                            │
│    Cmd+Enter (Ctrl+Enter)                  │
│                                             │
│ ✅ Accept Change:                           │
│    Cmd+. (Ctrl+.)                          │
│                                             │
│ 🆕 New Tab:                                 │
│    Cmd+Shift+Esc (Ctrl+Shift+Esc)         │
│                                             │
│ 💬 Commands:                                │
│    /help     - Show help                   │
│    /skills   - List skills                 │
│    /mcp      - MCP servers                 │
│                                             │
└─────────────────────────────────────────────┘
```

---

## Common First Tasks

### Frontend Development
```
# Review HTML for accessibility
@verify.html Check accessibility compliance

# Optimize assets
Find images over 100KB and suggest compression

# Update navigation
@_includes/navigation.html Add "Verify Certificate" link
```

### Certificate Automation
```
# Generate certificates
@tools/certificate_automation/src/generate_certificates.py
Explain how this works

# Test verification
Test the certificate verification page with a sample ID

# Add certificate type
@tools/certificate_automation/src/config.json
Add configuration for "speaker" certificates
```

### Content Updates
```
# Add team member
@_data/team.yml Add new team member profile

# Create blog post
Create a new blog post about our latest event

# Update SEO
Review SEO meta tags on all pages
```

---

## Troubleshooting

### Extension not loading?
```
1. Reload VS Code: Cmd+Shift+P → "Reload Window"
2. Check extension is enabled
3. Sign out and sign back in
```

### Can't reference files?
```
1. Ensure file is saved
2. File must be in workspace
3. Try absolute path: @/path/to/file.ext
```

### Skills not showing?
```
1. Check .claude/skills/ directory exists
2. Skills must be .md files
3. Restart Claude Code
```

---

## Get Help

- In conversation: `/help`
- Full docs: [README.md](README.md)
- VS Code guide: [vscode-setup-guide.md](vscode-setup-guide.md)
- Online: https://code.claude.com/docs

---

**Pro Tip**: Use `@` to reference files - Claude will understand the context automatically!

Happy coding! 🚀