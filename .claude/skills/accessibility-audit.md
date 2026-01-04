# Accessibility Audit Skill

Perform comprehensive accessibility (a11y) audits following WCAG 2.1 AA standards:
- Keyboard navigation
- Screen reader compatibility
- Color contrast
- ARIA attributes
- Form accessibility
- Focus management

## Process

1. Review HTML structure and semantics
2. Check keyboard navigation:
   - Tab order logical
   - All interactive elements accessible
   - Focus indicators visible
   - No keyboard traps
3. Validate ARIA usage:
   - Proper roles, states, properties
   - Label associations
   - Live regions for dynamic content
4. Test color contrast (WCAG AA: 4.5:1 for normal text, 3:1 for large text)
5. Check form accessibility:
   - Labels associated with inputs
   - Error messages announced
   - Required fields indicated
6. Verify image alt text
7. Check heading hierarchy (h1-h6)
8. Test with screen reader flow simulation

## WCAG 2.1 AA Criteria

- **Perceivable**: Text alternatives, captions, adaptable content
- **Operable**: Keyboard accessible, enough time, seizure-safe
- **Understandable**: Readable, predictable, input assistance
- **Robust**: Compatible with assistive technologies

## Common Issues to Check

- Missing alt text on images
- Poor color contrast
- Missing form labels
- Improper heading hierarchy
- Missing skip links
- Non-semantic HTML
- Missing ARIA labels on icon buttons
- Inactive focus indicators

## Example Usage

User: "Audit the verify page for accessibility"
Assistant: *Performs comprehensive a11y audit and provides improvement recommendations*