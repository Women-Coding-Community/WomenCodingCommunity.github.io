# Claude Code Workflows for WCC Project

Common workflows optimized for the Women Coding Community GitHub Pages site.

## Frontend Development Workflows

### 1. Create New Page

**Objective**: Add a new page to the Jekyll site

**Steps**:
```
1. "Create a new page called team-profiles.html"
2. Review the generated HTML
3. "Add this page to the navigation in _includes/header.html"
4. "Update _config.yml with the new page"
5. Test locally: bundle exec jekyll serve
```

**Example Prompt**:
```
Create a new Jekyll page for team profiles at /team-profiles.html.
Include:
- Front matter with layout: default
- Responsive grid layout for profile cards
- Accessibility features (ARIA labels, alt text)
- Match the style of existing pages

Reference @_layouts/default.html for layout structure
```

### 2. Update Certificate Verification Page

**Objective**: Enhance the verify.html page

**Steps**:
```
1. @verify.html Review this page for accessibility
2. Implement suggested improvements
3. "Test the verification flow with a sample certificate ID"
4. "Add loading states and better error messages"
5. Preview changes in browser
```

**Example Prompt**:
```
@verify.html
Improve the user experience:
1. Add a loading spinner during verification
2. Show clearer success/error states
3. Make it mobile-responsive
4. Ensure WCAG 2.1 AA compliance
```

### 3. Optimize Website Performance

**Objective**: Improve page load times

**Steps**:
```
1. "Analyze assets/css/ and assets/js/ for optimization"
2. "Identify large images in assets/images/"
3. "Suggest lazy loading for images"
4. "Recommend CSS minification strategy"
5. Implement optimizations
6. Test with Lighthouse
```

**Example Prompt**:
```
Optimize website performance:
1. Find all images over 100KB
2. Suggest WebP conversion
3. Identify unused CSS
4. Recommend bundling strategy
```

### 4. Add New Feature Section

**Objective**: Add a new section to the homepage

**Steps**:
```
1. @index.html Review current structure
2. "Add a 'Success Stories' section after the hero"
3. "Make it responsive with flexbox/grid"
4. "Include proper semantic HTML"
5. "Style it consistently with existing sections"
```

## Certificate Automation Workflows

### 5. Generate Certificates

**Objective**: Generate certificates for a new cohort

**Steps**:
```
1. "Update tools/certificate_automation/data/input/names/mentees.txt"
2. "Run the certificate generation script"
3. "Verify QR codes are embedded"
4. "Check the certificate registry"
5. "Preview generated certificates"
```

**Example Prompt**:
```
Help me generate certificates:
1. Read names from mentees.txt
2. Run generate_certificates.py
3. Verify all QR codes link to correct URLs
4. Check certificate_registry.json for accuracy
```

### 6. Add New Certificate Type

**Objective**: Create certificates for a new program

**Steps**:
```
1. @tools/certificate_automation/src/config.json
2. "Add a new certificate type configuration for 'speaker'"
3. "Create speaker.txt in data/input/names/"
4. "Update the documentation"
5. Test generation
```

**Example Prompt**:
```
@tools/certificate_automation/src/config.json
Add a new certificate type for speakers:
- Template: speaker.pptx
- Names file: speakers.txt
- Output directories
- Same style as existing types
```

### 7. Test Certificate Verification

**Objective**: Ensure verification system works

**Steps**:
```
1. "Generate a test certificate"
2. "Extract the certificate ID"
3. "Test verification at /verify"
4. "Verify QR code scanning works"
5. "Test error handling with invalid ID"
```

**Example Prompt**:
```
Test the complete verification workflow:
1. Generate a certificate for "Test User"
2. Find the certificate ID in the registry
3. Test URL: /verify?cert=CERTIFICATE_ID
4. Verify correct information displays
5. Test with invalid ID "INVALID123"
```

## Content Management Workflows

### 8. Add New Team Member

**Objective**: Add a team member profile

**Steps**:
```
1. @_data/team.yml
2. "Add new team member entry"
3. "Add profile image to assets/images/team/"
4. "Ensure image is optimized (< 50KB)"
5. Preview on the team page
```

**Example Prompt**:
```
@_data/team.yml
Add a new team member:
Name: Jane Smith
Role: Community Lead
Bio: [description]
Image: /assets/images/team/jane-smith.jpg
LinkedIn: [url]
GitHub: [url]
```

### 9. Create Blog Post

**Objective**: Publish a new blog post

**Steps**:
```
1. "Create a new post in _posts/"
2. "Use YYYY-MM-DD-title.md naming"
3. "Add proper front matter"
4. "Include featured image"
5. "Add categories and tags"
6. Preview with Jekyll serve
```

**Example Prompt**:
```
Create a blog post:
Title: "Women in Tech: Success Stories 2026"
Date: 2026-01-04
Author: WCC Team
Categories: community, success-stories
Include:
- Front matter with layout: post
- Featured image
- SEO meta tags
- Share buttons
```

### 10. Update Navigation

**Objective**: Add/update menu items

**Steps**:
```
1. @_includes/navigation.html
2. "Add 'Certificate Verification' link"
3. "Ensure mobile menu works"
4. "Test accessibility (keyboard navigation)"
5. "Update active state styling"
```

**Example Prompt**:
```
@_includes/navigation.html
Add a new menu item:
- Label: "Verify Certificate"
- URL: /verify
- Icon: certificate icon
- Position: after "Programs"
- Accessible (ARIA labels)
```

## Testing & Quality Workflows

### 11. Accessibility Audit

**Objective**: Ensure WCAG 2.1 AA compliance

**Steps**:
```
1. @verify.html Run accessibility audit
2. "Check color contrast"
3. "Verify keyboard navigation"
4. "Test with screen reader simulation"
5. "Fix identified issues"
6. Re-audit
```

**Example Prompt**:
```
@verify.html
Perform comprehensive accessibility audit:
- Color contrast (WCAG AA)
- Keyboard navigation
- ARIA labels
- Form accessibility
- Heading hierarchy
- Screen reader compatibility
```

### 12. Cross-Browser Testing

**Objective**: Ensure compatibility

**Steps**:
```
1. "List potential browser compatibility issues"
2. "Check CSS for vendor prefixes"
3. "Review JavaScript for ES6+ features"
4. "Test flexbox/grid fallbacks"
5. "Verify on mobile browsers"
```

**Example Prompt**:
```
Review for cross-browser compatibility:
- Chrome, Firefox, Safari, Edge
- Mobile Safari, Chrome Mobile
- Check CSS Grid fallbacks
- Verify ES6 transpilation
```

### 13. SEO Optimization

**Objective**: Improve search engine ranking

**Steps**:
```
1. @_config.yml Review SEO settings
2. "Check meta tags on all pages"
3. "Verify Open Graph tags"
4. "Optimize heading hierarchy"
5. "Add structured data"
6. "Review sitemap.xml"
```

**Example Prompt**:
```
Optimize SEO:
1. Review meta descriptions
2. Check title tags (< 60 chars)
3. Add Open Graph images
4. Verify canonical URLs
5. Check structured data markup
```

## Deployment Workflows

### 14. Pre-Deployment Checklist

**Objective**: Ensure ready for production

**Steps**:
```
1. "Run all tests"
2. "Build Jekyll site"
3. "Check for broken links"
4. "Verify certificate registry is updated"
5. "Review git diff"
6. "Create PR with description"
```

**Example Prompt**:
```
Pre-deployment checklist:
1. Run: bundle exec jekyll build
2. Check build errors
3. Verify certificate registry
4. Test verification page
5. Check responsive design
6. Review all changes in git
```

### 15. Create Pull Request

**Objective**: Submit changes for review

**Steps**:
```
1. "Review all modified files"
2. "Write PR description"
3. "Link related issues"
4. "Add screenshots if UI changes"
5. Submit PR
```

**Example Prompt**:
```
Create a PR for certificate verification improvements:
1. Summarize changes made
2. List files modified
3. Include screenshots
4. Reference issue #123
5. Add testing steps
```

## Quick Commands

### Daily Tasks
```bash
# Start development
bundle exec jekyll serve

# Generate certificates
cd tools/certificate_automation
python3 src/generate_certificates.py

# Run tests
python3 run_tests.py

# Check git status
git status
```

### With Claude Code
```
# Review changes
"Show me what changed in the last commit"

# Get help
"How do I add a new certificate type?"

# Debug
"Why is the verification page not loading the registry?"

# Optimize
"How can I improve the performance of this page?"
```

## Pro Tips

1. **Start with File References**: Always use `@filename` for context
2. **Break Down Tasks**: One workflow step per conversation
3. **Test Incrementally**: Test after each major change
4. **Use Skills**: Leverage custom skills for common tasks
5. **Save Templates**: Keep successful prompts for reuse
6. **Review Before Deploy**: Always review changes before pushing

---

**Remember**: Claude Code works best when you provide clear context and specific requirements!