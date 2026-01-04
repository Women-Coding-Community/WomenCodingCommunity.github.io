# Claude Code Configuration for WCC Project

Welcome to the Women Coding Community Claude Code setup! This directory contains all the configuration, skills, and guides for using Claude Code effectively with this project.

## Quick Start

### 1. Set Up Local Settings (First Time)
```bash
# Copy the example settings file
cp .claude/settings.example.json .claude/settings.local.json

# Edit settings.local.json with your preferences (optional)
```

### 2. Install Claude Code Extension

**Option A: VS Code**
```
1. Open VS Code
2. Press Cmd+Shift+X (Mac) or Ctrl+Shift+X (Windows/Linux)
3. Search "Claude Code"
4. Click Install
```

**Option B: JetBrains IDEs (IntelliJ IDEA, WebStorm, PyCharm, etc.)**
```
1. Open your JetBrains IDE
2. Go to Settings/Preferences → Plugins
3. Search for "Claude Code"
4. Click Install and restart IDE
5. Quick launch: Cmd+Esc (Mac) or Ctrl+Esc (Windows/Linux)
```

See [vscode-setup-guide.md](vscode-setup-guide.md) or [JetBrains docs](https://code.claude.com/docs/en/jetbrains.md) for detailed setup.

### 3. Use Custom Skills
Your project has the following custom skills available:

- **review-html** - Review HTML/Liquid templates for best practices
- **optimize-assets** - Analyze and optimize website assets
- **jekyll-build** - Build and validate Jekyll site
- **test-verification** - Test certificate verification system
- **accessibility-audit** - Comprehensive a11y audit

**Usage**: Just mention the skill in conversation:
```
"Use the accessibility-audit skill on verify.html"
```

### 4. Quick Reference

**VS Code & JetBrains:**
```
Cmd+Option+K (Alt+Ctrl+K) - Insert file reference
Cmd+Esc (Ctrl+Esc)        - Toggle focus / Quick launch
@filename.ext             - Reference file
/help                     - Show help
```

## Documentation

### 📚 Guides

| Guide | Description |
|-------|-------------|
| [vscode-setup-guide.md](vscode-setup-guide.md) | Complete VS Code extension setup |
| [mcp-servers-guide.md](mcp-servers-guide.md) | MCP server installation and usage |
| [keyboard-shortcuts.md](keyboard-shortcuts.md) | All keyboard shortcuts reference |
| [workflows-guide.md](workflows-guide.md) | Common workflows and examples |

### 🎯 Custom Skills

| Skill | Purpose |
|-------|---------|
| [review-html.md](skills/review-html.md) | HTML/Liquid template review |
| [optimize-assets.md](skills/optimize-assets.md) | Asset optimization |
| [jekyll-build.md](skills/jekyll-build.md) | Jekyll build management |
| [test-verification.md](skills/test-verification.md) | Certificate verification testing |
| [accessibility-audit.md](skills/accessibility-audit.md) | Accessibility audits |

## Project Structure

```
.claude/
├── README.md                    # This file
├── QUICK_START.md               # 5-minute quick start guide
├── settings.example.json        # Example settings (copy to settings.local.json)
├── settings.local.json          # Your local settings (gitignored)
├── vscode-setup-guide.md        # VS Code extension guide
├── mcp-servers-guide.md         # MCP servers setup
├── keyboard-shortcuts.md        # Shortcuts reference
├── workflows-guide.md           # Common workflows
└── skills/                      # Custom skills
    ├── review-html.md
    ├── optimize-assets.md
    ├── jekyll-build.md
    ├── test-verification.md
    └── accessibility-audit.md
```

## Common Tasks

### Frontend Development
```
# Review a page for accessibility
@verify.html Run accessibility audit

# Optimize images
Find all images over 100KB and suggest optimizations

# Update navigation
@_includes/navigation.html Add a "Verify Certificate" link
```

### Certificate Automation
```
# Generate certificates
@tools/certificate_automation/src/generate_certificates.py
Run this script and verify QR codes

# Test verification
Test the certificate verification system end-to-end

# Add new certificate type
@tools/certificate_automation/src/config.json
Add configuration for "speaker" certificates
```

### Content Management
```
# Add team member
@_data/team.yml Add a new team member profile

# Create blog post
Create a new blog post about "Women in Tech 2026"

# Update SEO
Review and optimize SEO meta tags across all pages
```

## Keyboard Shortcuts (Essential)

### VS Code Extension

| Action | Mac | Windows/Linux |
|--------|-----|---------------|
| File reference | `Cmd+Option+K` | `Alt+Ctrl+K` |
| Toggle focus | `Cmd+Esc` | `Ctrl+Esc` |
| New tab | `Cmd+Shift+Esc` | `Ctrl+Shift+Esc` |
| Send message | `Cmd+Enter` | `Ctrl+Enter` |

See [keyboard-shortcuts.md](keyboard-shortcuts.md) for complete list.

## MCP Servers

Extend Claude Code with external tools:

### Recommended for This Project

1. **GitHub** - PR management, issue tracking
   ```bash
   claude mcp add github
   ```

2. **Sentry** (Optional) - Error monitoring
   ```bash
   claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
   ```

See [mcp-servers-guide.md](mcp-servers-guide.md) for setup instructions.

## Tips & Best Practices

### 1. Always Reference Files
```
# ❌ Don't
"Review the verification page"

# ✅ Do
@verify.html "Review this page for accessibility"
```

### 2. Use Skills for Common Tasks
```
# ❌ Don't
"Check if this page is accessible"

# ✅ Do
"Use the accessibility-audit skill on @verify.html"
```

### 3. Break Down Complex Tasks
```
# ❌ Don't
"Build the entire new feature"

# ✅ Do
1. "Create the HTML structure"
2. "Add the CSS styling"
3. "Implement the JavaScript"
4. "Add tests"
```

### 4. Test Incrementally
```
# After each change
1. Review the diff
2. Test locally
3. Verify functionality
4. Move to next step
```

### 5. Use Specific Line References
```
# For large files
@verify.html:50-100 "Review the verification function"
```

## Project-Specific Context

### Website Stack
- **Framework**: Jekyll (GitHub Pages)
- **Frontend**: HTML, CSS, JavaScript
- **Templating**: Liquid
- **Build**: Bundler, Jekyll
- **Deploy**: GitHub Pages

### Certificate Automation
- **Language**: Python 3
- **Libraries**: python-pptx, qrcode, pillow, comtypes
- **Input**: Text files, PPTX templates
- **Output**: PPTX, PDF certificates with QR codes
- **Registry**: JSON file for verification

### Key Files
```
# Frontend
verify.html                      # Certificate verification page
_config.yml                      # Jekyll configuration
_includes/navigation.html        # Site navigation
_layouts/default.html           # Default layout

# Certificate Automation
tools/certificate_automation/
├── src/generate_certificates.py        # Main script
├── src/config.json                     # Configuration
├── data/output/certificate_registry.json  # Verification registry
└── tests/                              # Test suite
```

## Getting Help

### In Conversation
```
/help                 # Show available commands
/skills               # List custom skills
```

### Documentation
- [VS Code Setup](vscode-setup-guide.md)
- [MCP Servers](mcp-servers-guide.md)
- [Keyboard Shortcuts](keyboard-shortcuts.md)
- [Workflows](workflows-guide.md)

### Resources
- Claude Code Docs: https://code.claude.com/docs
- Jekyll Docs: https://jekyllrb.com/docs
- GitHub Pages: https://pages.github.com

## Troubleshooting

### Extension Not Working
1. Reload VS Code: `Cmd+Shift+P` → "Reload Window"
2. Check extension is enabled
3. Sign out and back in

### Skills Not Showing
1. Ensure `.claude/skills/` directory exists
2. Skills must be in Markdown format
3. Restart Claude Code

### MCP Servers Not Connecting
1. Check installation: `claude mcp list`
2. Verify authentication: `/mcp`
3. Check environment variables

## Contributing

When adding new skills or workflows:
1. Create skill in `.claude/skills/`
2. Document in this README
3. Add usage examples
4. Test thoroughly

## Updates

This configuration is version controlled. To update:
```bash
git pull origin main
```

---

**Happy coding with Claude! 🚀**

For questions or improvements, open an issue or PR in the repository.
