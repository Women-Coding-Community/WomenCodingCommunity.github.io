# Jekyll Build & Deploy Skill

Manage Jekyll site building and deployment:
- Build the Jekyll site locally
- Check for build errors
- Validate configuration
- Preview changes
- Prepare for GitHub Pages deployment

## Process

1. Check Jekyll installation and dependencies
2. Review _config.yml for errors
3. Build the site with `bundle exec jekyll build`
4. Serve locally for preview if requested
5. Check for common issues:
   - Missing front matter
   - Broken links
   - Invalid Liquid syntax
   - Plugin compatibility with GitHub Pages
6. Validate deployment readiness

## Commands

```bash
# Build site
bundle exec jekyll build

# Serve locally
bundle exec jekyll serve

# Build for production
JEKYLL_ENV=production bundle exec jekyll build

# Clean build
bundle exec jekyll clean
```

## GitHub Pages Considerations

- Only GitHub Pages-approved plugins
- Proper baseurl configuration
- CNAME file for custom domain
- _config.yml compatibility

## Example Usage

User: "Build the Jekyll site and check for errors"
Assistant: *Uses this skill to build the site and report any issues*